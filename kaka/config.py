"""Central configuration for Kaka.

Feel free to tweak values here — every knob for the pet's mood, poop
frequency, walking speed, etc. lives in this file.
"""
from __future__ import annotations

# ---------- Window / rendering ----------
PET_SIZE = 96                 # Pet sprite square side (px)
WASTE_SIZE = 32               # Poop / pee / food sprite side (px)
TICK_MS = 33                  # ~30 FPS main loop
TITLE = "Kaka"

# ---------- Movement ----------
WALK_SPEED_PX_PER_TICK = 2    # base horizontal speed
WALK_MIN_DURATION_MS = 2000
WALK_MAX_DURATION_MS = 6000
IDLE_MIN_DURATION_MS = 1500
IDLE_MAX_DURATION_MS = 5000

# Gravity mode
GRAVITY_ACC = 1.2             # px per tick^2
MAX_FALL_SPEED = 22           # px per tick
FLOAT_AMPLITUDE_PX = 10       # vertical bob when weightless
FLOAT_PERIOD_MS = 2600

# Drag / throw
THROW_DECAY = 0.9             # velocity decay per tick after release (gravity mode)

# ---------- Waste (poop / pee) ----------
POOP_INTERVAL_MIN_S = 45      # random pooping interval (min)
POOP_INTERVAL_MAX_S = 180
PEE_CHANCE = 0.4              # among poop events, chance it's actually pee

# ---------- Feeding ----------
FOOD_KINDS = ["🍪", "🍔", "🍎", "🍣", "🥕"]

# ---------- Reminders ----------
POMODORO_INTERVAL_S = 25 * 60
POMODORO_BREAK_TEXTS = [
    "已经 25 分钟啦，起来喝口水～",
    "老哥老姐，眼睛累了吧？看看远方！",
    "摸鱼时间到，我保你不被发现",
    "肩膀酸不？转转脖子！",
    "接下来这条 bug 是你的宿命，先歇会",
]

# ---------- Stats ----------
STAT_DECAY_PER_MIN = {         # every minute, apply these deltas
    "hunger": -1.5,            # gets hungrier (lower = hungrier)
    "mood":   -0.3,
    "hygiene": -0.5,
}

# ---------- Hotkeys ----------
BOSS_KEY_COMBO = "<ctrl>+<alt>+h"

# ---------- State persistence ----------
import os
STATE_DIR = os.path.expanduser("~/.kaka")
STATE_FILE = os.path.join(STATE_DIR, "state.json")
