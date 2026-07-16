"""The Kaka pet widget."""
from __future__ import annotations

import math
import random
import time
from enum import Enum, auto
from typing import Optional

from PySide6.QtCore import Qt, QPoint, QTimer, Signal
from PySide6.QtGui import QMouseEvent, QContextMenuEvent
from PySide6.QtWidgets import QLabel

from . import config, screens, sprites
from .stats import Stats
from .work_mode import WorkModeState


class Behaviour(Enum):
    IDLE = auto()
    WALK = auto()
    FALL = auto()
    FLOAT = auto()
    DRAGGING = auto()
    EATING = auto()
    WORKING = auto()
    SITTING = auto()
    LYING = auto()
    SLEEPING = auto()
    STANDING_UP = auto()   # brief rotation snap-back after landing
    PLAY_TOY = auto()


class Pet(QLabel):

    request_context_menu = Signal(QPoint)

    def __init__(self, stats: Stats):
        super().__init__()
        self.stats = stats
        self.work_mode = WorkModeState()

        self.setWindowFlags(
            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool
            | Qt.NoDropShadowWindowHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        self.setFixedSize(config.PET_SIZE, config.PET_SIZE)
        self.setMouseTracking(True)

        self._facing_left = False
        self._behaviour = Behaviour.IDLE
        self._behaviour_until = time.time()
        self._vx = 0.0; self._vy = 0.0
        self._angular_vel = 0.0
        self._rotation = 0.0
        self._gravity = False
        self._target: Optional[QPoint] = None
        self._drag_offset: Optional[QPoint] = None
        self._drag_last_pos: Optional[QPoint] = None
        self._drag_last_ts: float = 0.0
        self._float_phase = random.random() * math.tau

        # position on the bottom-right of the whole desktop union
        u = screens.union_rect()
        self.move(u.right() - config.PET_SIZE - 40,
                  u.bottom() - config.PET_SIZE - 40)
        self._refresh_sprite()

        self._tick_timer = QTimer(self)
        self._tick_timer.timeout.connect(self._tick)
        self._tick_timer.start(config.TICK_MS)

    # ------------------------------------------------------------------ API
    def set_gravity(self, on: bool) -> None:
        self._gravity = on
        if on and self._behaviour in (Behaviour.IDLE, Behaviour.FLOAT):
            self._behaviour = Behaviour.FALL
        elif not on and self._behaviour == Behaviour.FALL:
            self._behaviour = Behaviour.FLOAT
        self._vy = 0.0

    def gravity(self) -> bool:
        return self._gravity

    def walk_toward(self, target: QPoint) -> None:
        self._target = QPoint(target)
        self._behaviour = Behaviour.WALK

    def clear_target(self) -> None:
        self._target = None

    def start_work_mode(self, duration_s: float = 120.0) -> None:
        u = screens.union_rect()
        kb_x = u.left() + (u.width() // 2) - self.width() // 2
        kb_y = screens.floor_y_for(kb_x, self.width(), self.height())
        self.work_mode.start(kb_x, kb_y, duration_s=duration_s)
        self.walk_toward(QPoint(kb_x, kb_y))

    def stop_work_mode(self) -> None:
        self.work_mode.stop()

    # ------------------------------------------------------------------ Events
    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self._behaviour = Behaviour.DRAGGING
            self._drag_offset = event.globalPosition().toPoint() - self.pos()
            self._drag_last_pos = event.globalPosition().toPoint()
            self._drag_last_ts = time.time()
        elif event.button() == Qt.RightButton:
            self.request_context_menu.emit(event.globalPosition().toPoint())

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self._behaviour == Behaviour.DRAGGING and self._drag_offset:
            gpos = event.globalPosition().toPoint()
            self.move(gpos - self._drag_offset)
            now = time.time()
            dt = max(1e-3, now - self._drag_last_ts)
            self._vx = (gpos.x() - self._drag_last_pos.x()) / (dt * (1000 / config.TICK_MS))
            self._vy = (gpos.y() - self._drag_last_pos.y()) / (dt * (1000 / config.TICK_MS))
            self._drag_last_pos = gpos
            self._drag_last_ts = now

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton and self._behaviour == Behaviour.DRAGGING:
            if abs(self._vx) < 1 and abs(self._vy) < 1:
                accepted = self.stats.pet()
                self._pop_action("♥" if accepted else "哼！")
                self._behaviour = Behaviour.IDLE
                self._pick_next_idle()
            else:
                # Thrown: apply spin proportional to horizontal speed
                self._angular_vel = self._vx * 3.0
                self._behaviour = Behaviour.FALL if self._gravity else Behaviour.FLOAT
            self._drag_offset = None

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        event.accept()

    # ------------------------------------------------------------------ Tick
    def _tick(self) -> None:
        u = screens.union_rect()
        x, y = self.x(), self.y()

        # ---------- WORK MODE takes priority ----------
        self.work_mode.tick(config.TICK_MS)
        if self.work_mode.active and self._behaviour != Behaviour.DRAGGING:
            # walk to keyboard first, then sit and jitter
            if abs(x - self.work_mode.keyboard_x) > 3:
                self.walk_toward(QPoint(self.work_mode.keyboard_x, self.work_mode.keyboard_y))
                self._walk_tick()
            else:
                self._behaviour = Behaviour.WORKING
                y = self.work_mode.keyboard_y + int(self.work_mode.typing_offset)
                self.move(x, y)
            self._refresh_sprite()
            return

        if self._behaviour == Behaviour.DRAGGING:
            self._refresh_sprite()
            return

        floor_y_here = screens.floor_y_for(x, self.width(), self.height())

        if self._gravity and self._behaviour in (Behaviour.FALL, Behaviour.IDLE):
            self._vy = min(config.MAX_FALL_SPEED, self._vy + config.GRAVITY_ACC)
            y += int(self._vy)
            self._vx *= config.THROW_DECAY
            x += int(self._vx)
            # bounce off union left/right
            if x <= u.left() and self._vx < 0:
                x = u.left(); self._vx = -self._vx * 0.5
            if x >= u.right() - self.width() and self._vx > 0:
                x = u.right() - self.width(); self._vx = -self._vx * 0.5
            floor_y_here = screens.floor_y_for(x, self.width(), self.height())
            if y >= floor_y_here:
                y = floor_y_here; self._vy = 0
                if abs(self._vx) < 0.5:
                    self._vx = 0; self._angular_vel = 0; self._rotation = 0
                    self._behaviour = Behaviour.IDLE
                    self._pick_next_idle()
        elif not self._gravity and self._behaviour in (Behaviour.FLOAT, Behaviour.IDLE):
            self._float_phase += (config.TICK_MS / config.FLOAT_PERIOD_MS) * math.tau
            y_offset = int(math.sin(self._float_phase) * config.FLOAT_AMPLITUDE_PX * 0.1)
            y += y_offset
            self._vx *= 0.98; self._vy *= 0.98
            x += int(self._vx); y += int(self._vy)
            self._behaviour = Behaviour.FLOAT
        elif self._behaviour == Behaviour.WALK:
            self._walk_tick()
            x, y = self.x(), self.y()

        # spin decay
        self._rotation = (self._rotation + self._angular_vel * (config.TICK_MS/1000)) % 360
        self._angular_vel *= 0.94
        if abs(self._angular_vel) < 0.5:
            self._angular_vel = 0

        # clamp to union
        x, y = screens.clamp_to_union(x, y, self.width(), self.height())
        self.move(x, y)

        if self._behaviour in (Behaviour.IDLE, Behaviour.FLOAT) and time.time() > self._behaviour_until:
            self._pick_next_action()

        self._refresh_sprite()

    def _walk_tick(self) -> None:
        speed = (config.WALK_SPEED_PX_PER_TICK
                 * (0.6 + self.stats.mood / 100)
                 * self.stats.personality.walk_speed_mult)
        u = screens.union_rect()
        x = self.x()
        floor_y_here = screens.floor_y_for(x, self.width(), self.height())
        if self._target is not None:
            dx = self._target.x() - x
            step = int(math.copysign(min(abs(dx), speed), dx or 1))
            self._facing_left = dx < 0
            new_x = x + step
            new_y = floor_y_here if self._gravity else self.y()
            self.move(new_x, new_y)
            if abs(self._target.x() - self.x()) < speed:
                self.clear_target()
                self._behaviour = Behaviour.IDLE
                self._pick_next_idle()
        else:
            step = -int(speed) if self._facing_left else int(speed)
            new_x = x + step
            new_y = floor_y_here if self._gravity else self.y()
            self.move(new_x, new_y)
            # bounce off union edges (whole multi-monitor rect)
            if new_x <= u.left() or new_x >= u.right() - self.width():
                self._facing_left = not self._facing_left
            if time.time() > self._behaviour_until:
                self._behaviour = Behaviour.IDLE
                self._pick_next_idle()

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

    def _refresh_sprite(self) -> None:
        mood = self.stats.mood_label()
        if self._behaviour == Behaviour.DRAGGING:
            mood = "wink"
        elif self._behaviour == Behaviour.WORKING:
            mood = "working"
        pm = sprites.pet_pixmap(mood=mood, flip=not self._facing_left,
                                rotation=self._rotation)
        self.setPixmap(pm)
        self.setScaledContents(True)

    def _pop_action(self, text: str) -> None:
        self.setToolTip(text)
