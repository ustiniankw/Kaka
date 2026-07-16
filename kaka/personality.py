"""Personality system for Kaka.

Every Kaka is born with a personality. It affects walking speed, poop
frequency, mood/hunger decay, and (in future) special behaviours.

Multipliers are applied on top of the base values defined in
``kaka.config`` and ``kaka.stats``.
"""
from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class Personality:
    key: str
    name_zh: str
    emoji: str
    walk_speed_mult: float
    walk_prob: float            # 0..1 probability of choosing "walk" vs "idle"
    poop_freq_mult: float       # >1 → more poop, <1 → less
    hunger_decay_mult: float
    mood_decay_mult: float
    flavor: str
    # optional quirks:
    reject_petting_chance: float = 0.0   # tsundere quirk
    speech_bubble_chance: float = 0.0    # chatty quirk

    def to_dict(self) -> dict:
        return {
            "key": self.key,
            "name_zh": self.name_zh,
            "emoji": self.emoji,
            "walk_speed_mult": self.walk_speed_mult,
            "walk_prob": self.walk_prob,
            "poop_freq_mult": self.poop_freq_mult,
            "hunger_decay_mult": self.hunger_decay_mult,
            "mood_decay_mult": self.mood_decay_mult,
            "flavor": self.flavor,
            "reject_petting_chance": self.reject_petting_chance,
            "speech_bubble_chance": self.speech_bubble_chance,
        }


PERSONALITIES: Dict[str, Personality] = {
    "introvert": Personality(
        key="introvert",
        name_zh="社恐",
        emoji="🫥",
        walk_speed_mult=0.75,
        walk_prob=0.30,
        poop_freq_mult=1.0,
        hunger_decay_mult=0.9,
        mood_decay_mult=1.1,
        flavor="喜欢待在墙角，被摸时会稍稍愣一下",
    ),
    "chatty": Personality(
        key="chatty",
        name_zh="话痨",
        emoji="🗣️",
        walk_speed_mult=1.1,
        walk_prob=0.60,
        poop_freq_mult=1.0,
        hunger_decay_mult=1.0,
        mood_decay_mult=0.9,
        flavor="总有话想说，会时不时冒对话气泡",
        speech_bubble_chance=0.35,
    ),
    "lazy": Personality(
        key="lazy",
        name_zh="懒鬼",
        emoji="😴",
        walk_speed_mult=0.55,
        walk_prob=0.20,
        poop_freq_mult=0.7,
        hunger_decay_mult=0.75,
        mood_decay_mult=0.85,
        flavor="能坐着就不站着，看到食物才勉强动一下",
    ),
    "foodie": Personality(
        key="foodie",
        name_zh="干饭王",
        emoji="🍗",
        walk_speed_mult=1.2,
        walk_prob=0.55,
        poop_freq_mult=1.5,
        hunger_decay_mult=1.4,
        mood_decay_mult=1.0,
        flavor="看到食物飞奔而至，也拉得多",
    ),
    "grumpy": Personality(
        key="grumpy",
        name_zh="暴躁",
        emoji="😤",
        walk_speed_mult=1.3,
        walk_prob=0.60,
        poop_freq_mult=1.2,
        hunger_decay_mult=1.1,
        mood_decay_mult=1.4,
        flavor="心情容易掉，掉到底会跺脚",
    ),
    "tsundere": Personality(
        key="tsundere",
        name_zh="傲娇",
        emoji="😳",
        walk_speed_mult=1.0,
        walk_prob=0.50,
        poop_freq_mult=1.0,
        hunger_decay_mult=1.0,
        mood_decay_mult=1.0,
        flavor="摸头有 30% 概率不领情，但心里其实很开心",
        reject_petting_chance=0.30,
    ),
    "extrovert": Personality(
        key="extrovert",
        name_zh="社牛",
        emoji="🥳",
        walk_speed_mult=1.4,
        walk_prob=0.75,
        poop_freq_mult=1.0,
        hunger_decay_mult=1.1,
        mood_decay_mult=0.8,
        flavor="满屏跑，跑到屏幕边缘会挥手",
    ),
}


DEFAULT_KEY = "chatty"


def random_personality() -> Personality:
    return random.choice(list(PERSONALITIES.values()))


def by_key(key: str) -> Personality:
    return PERSONALITIES.get(key, PERSONALITIES[DEFAULT_KEY])
