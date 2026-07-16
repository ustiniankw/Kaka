"""The Kaka pet widget.

A transparent, frameless, always-on-top window that walks around, falls
under gravity, gets dragged, and asks to be fed.
"""
from __future__ import annotations

import math
import random
import time
from enum import Enum, auto
from typing import Optional

from PySide6.QtCore import Qt, QPoint, QTimer, Signal, QObject
from PySide6.QtGui import QMouseEvent, QGuiApplication, QContextMenuEvent
from PySide6.QtWidgets import QLabel

from . import config, sprites
from .stats import Stats


class Behaviour(Enum):
    IDLE = auto()
    WALK = auto()
    FALL = auto()      # under gravity
    FLOAT = auto()     # weightless bob
    DRAGGING = auto()
    EATING = auto()


class Pet(QLabel):
    """The floating Kaka window."""

    request_context_menu = Signal(QPoint)
    poop_signal = Signal(QPoint, bool)   # position, is_pee
    ate_signal = Signal(object)          # the food entity eaten

    def __init__(self, stats: Stats):
        super().__init__()
        self.stats = stats

        # ---- window setup ----
        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.Tool
            | Qt.NoDropShadowWindowHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        self.setFixedSize(config.PET_SIZE, config.PET_SIZE)
        self.setMouseTracking(True)

        # ---- state ----
        self._facing_left = False
        self._behaviour: Behaviour = Behaviour.IDLE
        self._behaviour_until: float = time.time()
        self._vx = 0.0
        self._vy = 0.0
        self._gravity = False
        self._target: Optional[QPoint] = None  # for walking toward food
        self._drag_offset: Optional[QPoint] = None
        self._drag_last_pos: Optional[QPoint] = None
        self._drag_last_ts: float = 0.0
        self._float_phase = random.random() * math.tau

        # place at bottom-right initially
        screen = QGuiApplication.primaryScreen().availableGeometry()
        self.move(screen.right() - config.PET_SIZE - 40,
                  screen.bottom() - config.PET_SIZE - 40)

        # sprite
        self._refresh_sprite()

        # ---- tick loop ----
        self._tick_timer = QTimer(self)
        self._tick_timer.timeout.connect(self._tick)
        self._tick_timer.start(config.TICK_MS)

    # ---------------------------------------------------------------- API
    def set_gravity(self, on: bool) -> None:
        self._gravity = on
        # nudge behaviour to react
        if on and self._behaviour in (Behaviour.IDLE, Behaviour.FLOAT):
            self._behaviour = Behaviour.FALL
        elif not on and self._behaviour == Behaviour.FALL:
            self._behaviour = Behaviour.FLOAT
        self._vy = 0.0

    def gravity(self) -> bool:
        return self._gravity

    def walk_toward(self, target: QPoint) -> None:
        """Ask the pet to walk toward a target point (e.g. food)."""
        self._target = QPoint(target)
        self._behaviour = Behaviour.WALK

    def clear_target(self) -> None:
        self._target = None

    # ---------------------------------------------------------------- Events
    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            # begin drag
            self._behaviour = Behaviour.DRAGGING
            self._drag_offset = event.globalPosition().toPoint() - self.pos()
            self._drag_last_pos = event.globalPosition().toPoint()
            self._drag_last_ts = time.time()
        elif event.button() == Qt.RightButton:
            self.request_context_menu.emit(event.globalPosition().toPoint())
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self._behaviour == Behaviour.DRAGGING and self._drag_offset:
            gpos = event.globalPosition().toPoint()
            self.move(gpos - self._drag_offset)
            # compute drag velocity for throw
            now = time.time()
            dt = max(1e-3, now - self._drag_last_ts)
            self._vx = (gpos.x() - self._drag_last_pos.x()) / (dt * (1000 / config.TICK_MS))
            self._vy = (gpos.y() - self._drag_last_pos.y()) / (dt * (1000 / config.TICK_MS))
            self._drag_last_pos = gpos
            self._drag_last_ts = now
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton and self._behaviour == Behaviour.DRAGGING:
            # release: if barely moved -> treat as pet
            if abs(self._vx) < 1 and abs(self._vy) < 1:
                accepted = self.stats.pet()
                self._pop_action("♥" if accepted else "哼！")
                self._behaviour = Behaviour.IDLE
                self._pick_next_idle()
            else:
                # thrown
                self._behaviour = Behaviour.FALL if self._gravity else Behaviour.FLOAT
            self._drag_offset = None
        super().mouseReleaseEvent(event)

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        # handled via right button press above
        event.accept()

    # ---------------------------------------------------------------- Tick
    def _tick(self) -> None:
        screen = QGuiApplication.primaryScreen().availableGeometry()
        x, y = self.x(), self.y()

        if self._behaviour == Behaviour.DRAGGING:
            self._refresh_sprite()
            return

        # gravity? apply always if enabled, unless walking on ground
        floor_y = screen.bottom() - self.height()
        ceil_y = screen.top()
        left = screen.left()
        right = screen.right() - self.width()

        if self._gravity and self._behaviour in (Behaviour.FALL, Behaviour.IDLE):
            # falling / grounded
            self._vy = min(config.MAX_FALL_SPEED, self._vy + config.GRAVITY_ACC)
            y += int(self._vy)
            # horizontal drift from throw
            self._vx *= config.THROW_DECAY
            x += int(self._vx)
            if y >= floor_y:
                y = floor_y
                self._vy = 0
                if abs(self._vx) < 0.5:
                    self._vx = 0
                    self._behaviour = Behaviour.IDLE
                    self._pick_next_idle()
        elif not self._gravity and self._behaviour in (Behaviour.FLOAT, Behaviour.IDLE):
            # weightless bob
            self._float_phase += (config.TICK_MS / config.FLOAT_PERIOD_MS) * math.tau
            y_offset = int(math.sin(self._float_phase) * config.FLOAT_AMPLITUDE_PX * 0.1)
            y += y_offset
            # throw drift
            self._vx *= 0.98
            self._vy *= 0.98
            x += int(self._vx)
            y += int(self._vy)
            self._behaviour = Behaviour.FLOAT
        elif self._behaviour == Behaviour.WALK:
            self._walk_tick()
            x, y = self.x(), self.y()

        # clamp to screen
        x = max(left, min(right, x))
        y = max(ceil_y, min(floor_y, y))
        self.move(x, y)

        # idle timeout → pick new behaviour
        if self._behaviour in (Behaviour.IDLE, Behaviour.FLOAT) and time.time() > self._behaviour_until:
            self._pick_next_action()

        self._refresh_sprite()

    def _walk_tick(self) -> None:
        screen = QGuiApplication.primaryScreen().availableGeometry()
        floor_y = screen.bottom() - self.height()
        speed = (config.WALK_SPEED_PX_PER_TICK
                 * (0.6 + self.stats.mood / 100)
                 * self.stats.personality.walk_speed_mult)
        if self._target is not None:
            dx = self._target.x() - self.x()
            step = int(math.copysign(min(abs(dx), speed), dx or 1))
            self._facing_left = dx < 0
            new_x = self.x() + step
            new_y = floor_y if self._gravity else self.y()
            self.move(new_x, new_y)
            if abs(self._target.x() - self.x()) < speed:
                # reached target
                self.clear_target()
                self._behaviour = Behaviour.IDLE
                self._pick_next_idle()
        else:
            step = -int(speed) if self._facing_left else int(speed)
            new_x = self.x() + step
            new_y = floor_y if self._gravity else self.y()
            self.move(new_x, new_y)
            # bounce off edges
            if new_x <= screen.left() or new_x >= screen.right() - self.width():
                self._facing_left = not self._facing_left
            if time.time() > self._behaviour_until:
                self._behaviour = Behaviour.IDLE
                self._pick_next_idle()

    # ---------------------------------------------------------------- Behaviour picker
    def _pick_next_action(self) -> None:
        walk_prob = self.stats.personality.walk_prob
        if random.random() < walk_prob:
            self._facing_left = random.choice([True, False])
            self._behaviour = Behaviour.WALK
            self._behaviour_until = time.time() + random.uniform(
                config.WALK_MIN_DURATION_MS, config.WALK_MAX_DURATION_MS) / 1000
        else:
            self._pick_next_idle()

    def _pick_next_idle(self) -> None:
        self._behaviour_until = time.time() + random.uniform(
            config.IDLE_MIN_DURATION_MS, config.IDLE_MAX_DURATION_MS) / 1000

    # ---------------------------------------------------------------- Sprite
    def _refresh_sprite(self) -> None:
        mood = self.stats.mood_label()
        if self._behaviour == Behaviour.DRAGGING:
            mood = "wink"
        pm = sprites.pet_pixmap(mood=mood, flip=not self._facing_left)
        self.setPixmap(pm)
        self.setScaledContents(True)

    def _pop_action(self, text: str) -> None:
        # future: floating text effect. For now, just tooltip flash.
        self.setToolTip(text)
