"""Pet stats: hunger, mood, hygiene, affinity.

Values are floats in the range ``[0, 100]``. Persistent state is stored on
disk so Kaka remembers you across launches.
"""
from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, asdict, field
from typing import Dict

from . import config


def _clamp(v: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, v))


@dataclass
class Stats:
    hunger: float = 50.0     # 100 = 撑, 0 = 快饿死
    mood: float = 60.0
    hygiene: float = 80.0
    affinity: float = 0.0
    last_tick: float = field(default_factory=time.time)

    # ----- persistence -----
    def save(self) -> None:
        os.makedirs(config.STATE_DIR, exist_ok=True)
        with open(config.STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(asdict(self), f, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls) -> "Stats":
        try:
            with open(config.STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            return cls(**data)
        except Exception:
            return cls()

    # ----- update loop -----
    def natural_decay(self) -> None:
        """Apply per-minute decay proportional to elapsed real time."""
        now = time.time()
        dt_min = (now - self.last_tick) / 60.0
        for k, delta in config.STAT_DECAY_PER_MIN.items():
            cur = getattr(self, k)
            setattr(self, k, _clamp(cur + delta * dt_min))
        # mood also depends on hunger — being hungry sucks
        if self.hunger < 20:
            self.mood = _clamp(self.mood - 0.5 * dt_min)
        self.last_tick = now

    # ----- interactions -----
    def pet(self) -> None:
        self.mood = _clamp(self.mood + 3)
        self.affinity = _clamp(self.affinity + 1)

    def feed(self) -> None:
        self.hunger = _clamp(self.hunger + 30)
        self.mood = _clamp(self.mood + 5)
        self.affinity = _clamp(self.affinity + 2)

    def poop(self) -> None:
        self.hygiene = _clamp(self.hygiene - 12)
        # relief boost
        self.mood = _clamp(self.mood + 2)

    def cleaned(self) -> None:
        self.hygiene = _clamp(self.hygiene + 10)
        self.affinity = _clamp(self.affinity + 0.5)

    # ----- helpers -----
    def mood_label(self) -> str:
        if self.hunger < 20:
            return "hungry"
        if self.mood < 25:
            return "sad"
        if self.mood > 80:
            return "wink"
        return "happy"

    def snapshot(self) -> Dict[str, float]:
        return {
            "hunger": round(self.hunger, 1),
            "mood": round(self.mood, 1),
            "hygiene": round(self.hygiene, 1),
            "affinity": round(self.affinity, 1),
        }
