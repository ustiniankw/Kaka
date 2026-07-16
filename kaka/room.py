"""Room / furniture system.

The user places 3 pieces of furniture in a screen corner:

* ``nest``    🛏  — sleeping spot; Kaka goes here when mood is low
* ``bowl``    🍚  — food bowl; feed items spawn here by default
* ``litter``  🚽  — litter box; if placed, Kaka walks to it before pooping,
                 which is much more civilised than random floor bombs.

Furniture is anchored to a corner of a screen so it stays in place across
resizes.  Corner slots keyed by ``(screen_idx, corner)`` where corner ∈
``{tl, tr, bl, br}``.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Tuple

FURNITURE_KIND = ("nest", "bowl", "litter")
FURNITURE_EMOJI = {"nest": "🛏", "bowl": "🍚", "litter": "🚽"}
FURNITURE_LABEL = {"nest": "窝", "bowl": "食盆", "litter": "便盆"}


@dataclass
class Furniture:
    kind: str          # 'nest' | 'bowl' | 'litter'
    screen: int
    corner: str        # 'tl' | 'tr' | 'bl' | 'br'

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "Furniture":
        return cls(**d)


def corner_xy(screen_w: int, screen_h: int, corner: str,
              size: int = 40, margin: int = 12) -> Tuple[int, int]:
    """Return top-left (x, y) for a furniture item in the given corner."""
    if corner == "tl":  return (margin,               margin)
    if corner == "tr":  return (screen_w - size - margin, margin)
    if corner == "bl":  return (margin,               screen_h - size - margin)
    if corner == "br":  return (screen_w - size - margin, screen_h - size - margin)
    return (margin, margin)


class RoomLayout:
    """Container for user-placed furniture."""

    def __init__(self, items: Optional[List[Furniture]] = None):
        self.items: List[Furniture] = list(items or [])

    def find(self, kind: str) -> Optional[Furniture]:
        for it in self.items:
            if it.kind == kind:
                return it
        return None

    def set(self, kind: str, screen: int, corner: str) -> None:
        assert kind in FURNITURE_KIND
        self.remove(kind)
        self.items.append(Furniture(kind, screen, corner))

    def remove(self, kind: str) -> None:
        self.items = [it for it in self.items if it.kind != kind]

    def to_list(self) -> List[dict]:
        return [it.to_dict() for it in self.items]

    @classmethod
    def from_list(cls, raw: List[dict]) -> "RoomLayout":
        out: List[Furniture] = []
        for d in raw or []:
            try:
                out.append(Furniture.from_dict(d))
            except Exception:
                continue
        return cls(out)
