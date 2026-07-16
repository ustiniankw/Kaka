"""Time-driven events: Friday afternoon karaoke + payday dance.

Both features check the *user local time* (``datetime.now()``).

* Karaoke:  every Friday, between ``FRIDAY_START_HOUR`` and
            ``FRIDAY_END_HOUR`` (inclusive-exclusive), Kaka picks up the
            🎤 and sings a short lyric every ``KARAOKE_INTERVAL_S``.
* Payday:   on the configured day-of-month (default 15), Kaka does a
            🕺 dance the entire day.  Configurable via
            ``events.set_payday(day)``.
"""
from __future__ import annotations

import json
import os
import random
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional

from . import config

EVENTS_FILE = os.path.join(config.STATE_DIR, "events.json")

# --- Friday karaoke window ---
FRIDAY_START_HOUR = 15   # 15:00
FRIDAY_END_HOUR   = 18   # < 18:00
KARAOKE_INTERVAL_S = 90

LYRICS = [
    "🎵 平平淡淡才是真~",
    "🎵 咖咖咖咖 咔咔咔咔~",
    "🎵 Somebody 好想 fish 一下~",
    "🎵 抬头一看 又是周五~",
    "🎵 明明就 · 是 · 摸鱼 · 的 · 天~",
    "🎤 Kaka 麦克风 test test",
    "🎵 老板不在 我最帅~",
]

DANCE_MOVES = ["🕺", "💃", "🪩", "🎉"]


@dataclass
class EventConfig:
    payday_day: int = 15            # 1..28
    karaoke_enabled: bool = True
    payday_enabled: bool = True

    def save(self) -> None:
        os.makedirs(config.STATE_DIR, exist_ok=True)
        with open(EVENTS_FILE, "w", encoding="utf-8") as f:
            json.dump(asdict(self), f, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls) -> "EventConfig":
        try:
            with open(EVENTS_FILE, "r", encoding="utf-8") as f:
                return cls(**json.load(f))
        except Exception:
            return cls()


def is_friday_afternoon(now: Optional[datetime] = None) -> bool:
    now = now or datetime.now()
    return now.weekday() == 4 and FRIDAY_START_HOUR <= now.hour < FRIDAY_END_HOUR


def is_payday(day: int, now: Optional[datetime] = None) -> bool:
    now = now or datetime.now()
    return now.day == day


def pick_lyric() -> str:
    return random.choice(LYRICS)


def pick_dance_move() -> str:
    return random.choice(DANCE_MOVES)
