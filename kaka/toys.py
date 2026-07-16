"""Toys the user can buy from the shop and place freely on the desktop.

Unlike ``room.Furniture`` (nest / bowl / litter, which snap to corners), toys
have free (x, y) coordinates on a specific screen so the user can drop them
anywhere.  Kaka periodically picks a nearby toy and plays with it.

Each toy has:

* ``key``           — unique id
* ``name``          — Chinese display name
* ``emoji``         — glyph rendered on the desktop
* ``affinity``      — minimum affinity to unlock (buy)
* ``personality``   — optional personality gate
* ``description``   — flavour text shown in the shop
* ``play_action``   — one of ``'swing' | 'ball' | 'scratch' | 'wheel' |
                          'laser' | 'climb' | 'tunnel' | 'cuddle' | 'zen'``
* ``mood_gain``     — mood delta per play cycle
* ``affinity_gain`` — affinity delta per play cycle
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, List, Optional


@dataclass(frozen=True)
class ToyDef:
    key: str
    name: str
    emoji: str
    affinity: float
    personality: Optional[str]
    description: str
    play_action: str
    mood_gain: float
    affinity_gain: float


TOYS: Dict[str, ToyDef] = {
    "swing":       ToyDef("swing",       "秋千",     "🪄", 20,  None,        "咯吱咯吱的荡秋千，蹲上去自动摇",      "swing",   5.0, 0.6),
    "ball":        ToyDef("ball",        "毛线球",   "🧶", 15,  None,        "扑一扑抓一抓，最基础的猫式快乐",       "ball",    3.5, 0.4),
    "scratcher":   ToyDef("scratcher",   "抓板",     "🪵", 30,  None,        "磨爪子解压，暴躁性格特别爱用",         "scratch", 4.0, 0.5),
    "wheel":       ToyDef("wheel",       "跑轮",     "🛞", 45,  None,        "空转型选手的最爱，一跑就停不下来",     "wheel",   6.0, 0.7),
    "laser":       ToyDef("laser",       "激光笔",   "🔴", 25,  None,        "点哪追哪，你的手指就是它的宿敌",       "laser",   5.5, 0.8),
    "cat_tree":    ToyDef("cat_tree",    "猫爬架",   "🌳", 55,  None,        "顶上有个小平台，Kaka 爬上去俯瞰",     "climb",   5.0, 0.6),
    "tunnel":      ToyDef("tunnel",      "钻洞",     "🕳", 35,  "introvert", "社恐限定，钻进去就假装不在",           "tunnel",  6.5, 0.9),
    "teddy":       ToyDef("teddy",       "小熊玩偶", "🧸", 40,  None,        "抱着睡觉的软软朋友",                   "cuddle",  5.5, 1.0),
    "hammock":     ToyDef("hammock",     "吊床",     "🛌", 50,  "lazy",      "懒鬼限定，一躺就是三小时",             "cuddle",  7.0, 1.1),
    "zen_stone":   ToyDef("zen_stone",   "禅意石",   "🪨", 60,  None,        "坐下来打坐冥想 · 心情大幅回升",         "zen",     8.0, 0.5),
    "gaming_pad":  ToyDef("gaming_pad",  "游戏手柄", "🎮", 65,  "chatty",    "话痨专属，一边玩一边解说",             "ball",    6.0, 0.9),
    "cardboard":   ToyDef("cardboard",   "瓦楞纸箱", "📦", 10,  None,        "永恒的浪漫。只要有箱子它就会钻",       "tunnel",  4.0, 0.6),
}


@dataclass
class PlacedToy:
    key: str            # matches TOYS[key]
    screen: int
    x: int              # top-left in screen local coordinates
    y: int
    size: int = 44

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "PlacedToy":
        return cls(**d)


class ToyBox:
    """Container of currently placed toys."""

    def __init__(self, placed: Optional[List[PlacedToy]] = None) -> None:
        self.placed: List[PlacedToy] = list(placed or [])

    def add(self, toy: PlacedToy) -> None:
        # allow multiple copies of the same toy, but not stacked on top of each other
        self.placed.append(toy)

    def remove(self, index: int) -> None:
        if 0 <= index < len(self.placed):
            self.placed.pop(index)

    def move(self, index: int, screen: int, x: int, y: int) -> None:
        if 0 <= index < len(self.placed):
            t = self.placed[index]
            self.placed[index] = PlacedToy(t.key, screen, x, y, t.size)

    def nearest(self, screen: int, x: int, y: int) -> Optional[int]:
        best = None
        best_d = 1e18
        for i, t in enumerate(self.placed):
            if t.screen != screen:
                continue
            d = (t.x - x) ** 2 + (t.y - y) ** 2
            if d < best_d:
                best_d = d; best = i
        return best

    def to_list(self) -> List[dict]:
        return [t.to_dict() for t in self.placed]

    @classmethod
    def from_list(cls, raw: List[dict]) -> "ToyBox":
        out: List[PlacedToy] = []
        for d in raw or []:
            try:
                out.append(PlacedToy.from_dict(d))
            except Exception:
                continue
        return cls(out)
