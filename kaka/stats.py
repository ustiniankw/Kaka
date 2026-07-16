"""Pet stats: hunger, mood, hygiene, affinity.

Values are floats in the range ``[0, 100]``. Persistent state is stored on
disk so Kaka remembers you across launches.
"""
from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, asdict, field
from typing import Dict, List, Set

from . import config
from .personality import Personality, PERSONALITIES, random_personality, by_key, DEFAULT_KEY


def _clamp(v: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, v))


@dataclass
class Stats:
    hunger: float = 50.0     # 100 = 撑, 0 = 快饿死
    mood: float = 60.0
    hygiene: float = 80.0
    affinity: float = 0.0
    last_tick: float = field(default_factory=time.time)
    personality_key: str = ""  # empty = uninitialized → randomize on first load
    skin_key: str = "default"
    owned_skins: List[str] = field(default_factory=lambda: ["default"])
    owned_toys: List[str] = field(default_factory=list)
    placed_toys: List[Dict] = field(default_factory=list)
    room_layout: List[Dict] = field(default_factory=list)
    payday_day: int = 15

    def __post_init__(self) -> None:
        if not self.personality_key or self.personality_key not in PERSONALITIES:
            self.personality_key = random_personality().key
        if "default" not in self.owned_skins:
            self.owned_skins.insert(0, "default")

    # ----- personality shortcut -----
    @property
    def personality(self) -> Personality:
        return by_key(self.personality_key)

    def reroll_personality(self) -> Personality:
        old = self.personality_key
        while True:
            new = random_personality()
            if new.key != old:
                self.personality_key = new.key
                return new

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
        """Apply per-minute decay proportional to elapsed real time, modulated
        by the current personality."""
        now = time.time()
        dt_min = (now - self.last_tick) / 60.0
        p = self.personality
        deltas = dict(config.STAT_DECAY_PER_MIN)
        deltas["hunger"] *= p.hunger_decay_mult
        deltas["mood"]   *= p.mood_decay_mult
        for k, delta in deltas.items():
            cur = getattr(self, k)
            setattr(self, k, _clamp(cur + delta * dt_min))
        if self.hunger < 20:
            self.mood = _clamp(self.mood - 0.5 * dt_min)
        self.last_tick = now

    # ----- interactions -----
    def pet(self) -> bool:
        """Returns True if the pet accepted the petting (tsundere may reject)."""
        import random
        if random.random() < self.personality.reject_petting_chance:
            # tsundere rejects: no mood gain, tiny affinity gain
            self.affinity = _clamp(self.affinity + 0.3)
            return False
        self.mood = _clamp(self.mood + 3)
        self.affinity = _clamp(self.affinity + 1)
        return True

    def feed(self) -> None:
        boost = 30 * (1.1 if self.personality.key == "foodie" else 1.0)
        self.hunger = _clamp(self.hunger + boost)
        self.mood = _clamp(self.mood + 5)
        self.affinity = _clamp(self.affinity + 2)

    def poop(self) -> None:
        self.hygiene = _clamp(self.hygiene - 12)
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
            "personality": self.personality_key,
        }
