"""Pomodoro stats — persisted so the reminder card can show "已完成 X 个".

Records:

* ``sessions_total``: lifetime completed sessions
* ``sessions_today`` / ``today_date``: per-day counter, auto-reset at midnight
* ``streak_days``: consecutive days with at least one session
* ``last_completed_at``: unix timestamp of last completion
* ``running``: whether a session is currently running
* ``started_at``: unix timestamp of current session start
"""
from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, asdict, field
from datetime import datetime, date

from . import config


POMODORO_FILE = os.path.join(config.STATE_DIR, "pomodoro.json")
SESSION_S = config.POMODORO_INTERVAL_S


@dataclass
class PomodoroStats:
    sessions_total: int = 0
    sessions_today: int = 0
    today_date: str = ""             # ISO yyyy-mm-dd
    streak_days: int = 0
    last_completed_at: float = 0.0
    running: bool = False
    started_at: float = 0.0

    def _roll_day(self) -> None:
        today = date.today().isoformat()
        if self.today_date != today:
            # streak logic
            if self.today_date:
                try:
                    prev = date.fromisoformat(self.today_date)
                    if (date.today() - prev).days == 1 and self.sessions_today > 0:
                        pass  # keep streak
                    elif self.sessions_today > 0:
                        # broken
                        self.streak_days = 0
                except Exception:
                    self.streak_days = 0
            self.today_date = today
            self.sessions_today = 0

    def start(self) -> None:
        self._roll_day()
        self.running = True
        self.started_at = time.time()

    def cancel(self) -> None:
        self.running = False
        self.started_at = 0.0

    def complete(self) -> None:
        self._roll_day()
        self.sessions_total += 1
        if self.sessions_today == 0:
            self.streak_days += 1
        self.sessions_today += 1
        self.last_completed_at = time.time()
        self.running = False
        self.started_at = 0.0

    def elapsed(self) -> float:
        if not self.running:
            return 0.0
        return max(0.0, time.time() - self.started_at)

    def remaining(self) -> float:
        if not self.running:
            return 0.0
        return max(0.0, SESSION_S - self.elapsed())

    def summary_line(self) -> str:
        self._roll_day()
        return (f"今日已完成 {self.sessions_today} 个 · "
                f"累计 {self.sessions_total} · "
                f"连续 {self.streak_days} 天")

    def save(self) -> None:
        os.makedirs(config.STATE_DIR, exist_ok=True)
        with open(POMODORO_FILE, "w", encoding="utf-8") as f:
            json.dump(asdict(self), f, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls) -> "PomodoroStats":
        try:
            with open(POMODORO_FILE, "r", encoding="utf-8") as f:
                return cls(**json.load(f))
        except Exception:
            s = cls()
            s._roll_day()
            return s
