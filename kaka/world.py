"""World manager: handles poop timers, food spawning, cleaning.
Owns the list of :class:`FloorEntity` sitting on the desktop.
"""
from __future__ import annotations

import random
import time
from typing import List

from PySide6.QtCore import QObject, QPoint, QTimer, Signal

from . import config, screens
from .pet import Pet
from .stats import Stats
from .waste import FloorEntity, Poop, Pee, Food


class World(QObject):

    def __init__(self, pet: Pet, stats: Stats):
        super().__init__()
        self.pet = pet
        self.stats = stats
        self.entities: List[FloorEntity] = []

        # timers ---------------------------------------------------------
        self._poop_timer = QTimer(self)
        self._poop_timer.setSingleShot(True)
        self._poop_timer.timeout.connect(self._on_poop_timer)
        self._schedule_next_poop()

        self._stats_timer = QTimer(self)
        self._stats_timer.timeout.connect(self._on_stats_timer)
        self._stats_timer.start(5000)  # apply decay every 5s

    # ---------------------------------------------------------------- API
    def spawn_food(self, glyph: str = None) -> None:
        glyph = glyph or random.choice(config.FOOD_KINDS)
        u = screens.union_rect()
        pet_center = self.pet.geometry().center()
        x = pet_center.x() + random.randint(-200, 200)
        y = screens.floor_y_for(x, config.WASTE_SIZE, config.WASTE_SIZE) + config.PET_SIZE - config.WASTE_SIZE - 4
        y = min(y, u.bottom() - config.WASTE_SIZE - 4)
        x = max(u.left(), min(u.right() - config.WASTE_SIZE, x))
        pos = QPoint(x, y)
        food = Food(pos, glyph, self._on_food_click)
        food.show()
        self.entities.append(food)
        self.pet.walk_toward(QPoint(x, self.pet.y()))

    def teardown(self) -> None:
        for e in self.entities:
            e.hide()
            e.deleteLater()
        self.entities.clear()

    # ---------------------------------------------------------------- Handlers
    def _on_poop_timer(self) -> None:
        is_pee = random.random() < config.PEE_CHANCE
        pet_pos = self.pet.pos()
        x = pet_pos.x() + self.pet.width() // 2 - config.WASTE_SIZE // 2
        if self.pet.gravity():
            y = screens.floor_y_for(x, config.WASTE_SIZE, config.WASTE_SIZE) + config.PET_SIZE - config.WASTE_SIZE - 4
        else:
            y = pet_pos.y() + self.pet.height() // 2

        pos = QPoint(x, y)
        entity = Pee(pos, self._on_clean) if is_pee else Poop(pos, self._on_clean)
        entity.show()
        self.entities.append(entity)
        self.stats.poop()
        self._schedule_next_poop()

    def _on_clean(self, entity: FloorEntity) -> None:
        entity.hide()
        entity.deleteLater()
        if entity in self.entities:
            self.entities.remove(entity)
        self.stats.cleaned()

    def _on_food_click(self, entity: Food) -> None:
        # eat immediately if the pet is close, otherwise walk to it
        if abs(entity.x() - self.pet.x()) < config.PET_SIZE:
            self._eat(entity)
        else:
            self.pet.walk_toward(QPoint(entity.x(), self.pet.y()))
            # check periodically for arrival
            QTimer.singleShot(200, lambda: self._check_food_reach(entity))

    def _check_food_reach(self, entity: Food) -> None:
        if entity not in self.entities:
            return
        if abs(entity.x() - self.pet.x()) < config.PET_SIZE:
            self._eat(entity)
        else:
            QTimer.singleShot(300, lambda: self._check_food_reach(entity))

    def _eat(self, entity: Food) -> None:
        entity.hide()
        entity.deleteLater()
        if entity in self.entities:
            self.entities.remove(entity)
        self.stats.feed()
        self.pet.clear_target()

    def _on_stats_timer(self) -> None:
        self.stats.natural_decay()
        self.stats.save()

    # ---------------------------------------------------------------- helpers
    def _schedule_next_poop(self) -> None:
        mult = self.stats.personality.poop_freq_mult
        # higher mult = shorter interval
        lo = config.POOP_INTERVAL_MIN_S / max(0.4, mult)
        hi = config.POOP_INTERVAL_MAX_S / max(0.4, mult)
        delay_s = random.uniform(lo, hi)
        self._poop_timer.start(int(delay_s * 1000))
