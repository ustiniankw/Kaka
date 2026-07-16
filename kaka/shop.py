"""Skin shop with personality-aware unlock rules.

Each skin has:

* ``affinity``: minimum affinity required (0–100)
* ``personality``: optional personality gate (e.g. ``mochi`` requires
  a chill / cute personality)
* ``description``

Owned skins are persisted in ``Stats.owned_skins``.  The default skin is
always owned.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Set


@dataclass(frozen=True)
class ShopItem:
    key: str
    name: str
    emoji: str
    affinity: float
    personality: Optional[str]   # None = any
    description: str


SHOP_ITEMS: Dict[str, ShopItem] = {
    "default": ShopItem("default", "原味 Kaka", "🟡", 0,   None,        "刚认识时候的样子，永久拥有"),
    "mochi":   ShopItem("mochi",   "麻薯 Kaka", "🌸", 25,  None,        "圆滚滚粉粉的 Q 弹皮肤"),
    "matcha":  ShopItem("matcha",  "抹茶 Kaka", "🍵", 40,  None,        "带一点苦涩的成熟绿"),
    "berry":   ShopItem("berry",   "莓紫 Kaka", "🫐", 55,  "tsundere",  "傲娇专属，微微高冷"),
    "cocoa":   ShopItem("cocoa",   "可可 Kaka", "🍫", 70,  "foodie",    "干饭王吃出来的巧克力色"),
    "sakura":  ShopItem("sakura",  "樱雪 Kaka", "🌸", 85,  "introvert", "社恐限定，柔粉带雪白"),
    "cyber":   ShopItem("cyber",   "赛博 Kaka", "🤖", 90,  "extrovert", "社牛专属，霓虹紫电"),
}


def unlockable(affinity: float, personality: str) -> List[ShopItem]:
    out = []
    for it in SHOP_ITEMS.values():
        if affinity < it.affinity:
            continue
        if it.personality and it.personality != personality:
            continue
        out.append(it)
    return out


def can_unlock(item: ShopItem, affinity: float, personality: str) -> bool:
    if affinity < item.affinity:
        return False
    if item.personality and item.personality != personality:
        return False
    return True


def status_of(item: ShopItem, affinity: float, personality: str,
              owned: Set[str]) -> str:
    if item.key in owned:
        return "owned"
    if can_unlock(item, affinity, personality):
        return "available"
    return "locked"
