"""Skin pack system.

A skin pack is a folder in ``assets/skins/<name>/`` containing:

    skin.json                # metadata + optional colour overrides
    idle.png     (optional)  # 90x90 sprite for the idle mood
    happy.png    (optional)
    sad.png      (optional)
    ...

Only ``skin.json`` is required.  If PNG frames are missing we fall back to
the procedural pixel-art pet drawn in :mod:`kaka.sprites`, but with the
colour palette overridden by the values in ``skin.json``.

``skin.json`` schema::

    {
      "name":        "Mochi",
      "description": "A round pink mochi pet",
      "colors": {
        "body":  "#F5C542",
        "dark":  "#C08A18",
        "cheek": "#F58A8A",
        "eye":   "#222222",
        "white": "#FFFFFF"
      },
      "frames": {           # (optional)
        "happy":   "happy.png",
        "sad":     "sad.png"
      }
    }
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from PySide6.QtGui import QColor, QPixmap


SKIN_DIRS_ENV = "KAKA_SKIN_DIRS"


@dataclass
class Skin:
    key: str
    name: str
    description: str = ""
    colors: Dict[str, QColor] = field(default_factory=dict)
    frames: Dict[str, str] = field(default_factory=dict)  # mood → abs path
    base_dir: str = ""

    def color(self, key: str, default: QColor) -> QColor:
        return self.colors.get(key, default)

    def has_frame(self, mood: str) -> bool:
        p = self.frames.get(mood)
        return bool(p and os.path.exists(p))

    def load_frame(self, mood: str) -> Optional[QPixmap]:
        p = self.frames.get(mood)
        if not p or not os.path.exists(p):
            return None
        return QPixmap(p)


def _search_dirs() -> List[str]:
    dirs: List[str] = []
    env = os.environ.get(SKIN_DIRS_ENV)
    if env:
        dirs.extend([p for p in env.split(os.pathsep) if p])
    # bundled skins (repo assets/skins)
    dirs.append(os.path.join(os.path.dirname(os.path.dirname(__file__)),
                             "assets", "skins"))
    # user-local skins
    dirs.append(os.path.expanduser("~/.kaka/skins"))
    return [d for d in dirs if os.path.isdir(d)]


def discover_skins() -> Dict[str, Skin]:
    skins: Dict[str, Skin] = {}
    for base in _search_dirs():
        for entry in os.listdir(base):
            path = os.path.join(base, entry)
            manifest = os.path.join(path, "skin.json")
            if not os.path.isfile(manifest):
                continue
            try:
                with open(manifest, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                continue
            key = entry
            colors = {k: QColor(v) for k, v in (data.get("colors") or {}).items()}
            frames = {}
            for mood, rel in (data.get("frames") or {}).items():
                frames[mood] = os.path.join(path, rel)
            skins[key] = Skin(
                key=key,
                name=data.get("name", key),
                description=data.get("description", ""),
                colors=colors,
                frames=frames,
                base_dir=path,
            )
    return skins


# Built-in colour variants without PNG frames.
BUILTIN_VARIANTS: Dict[str, Dict[str, str]] = {
    "default": {"body": "#F5C542", "dark": "#C08A18",
                "cheek": "#F58A8A", "eye": "#222222", "white": "#FFFFFF"},
    "mochi":   {"body": "#F7C0D3", "dark": "#C77F97",
                "cheek": "#FFF0B0", "eye": "#3A2036", "white": "#FFFFFF"},
    "matcha":  {"body": "#A6C97E", "dark": "#6D8C4F",
                "cheek": "#F5C4D0", "eye": "#2A3A1A", "white": "#F5FFEA"},
    "berry":   {"body": "#8C6BE8", "dark": "#5E43B0",
                "cheek": "#FFC1E0", "eye": "#1D1132", "white": "#FFFFFF"},
    "cocoa":   {"body": "#8A5A3B", "dark": "#5B3720",
                "cheek": "#F5B6A3", "eye": "#20120A", "white": "#FFF3E8"},
    "sakura":  {"body": "#FFD7E2", "dark": "#D793A6",
                "cheek": "#FFFFFF", "eye": "#3A1A28", "white": "#FFFDFB"},
    "cyber":   {"body": "#7A3CFF", "dark": "#3B1670",
                "cheek": "#12F5C6", "eye": "#F8F8F8", "white": "#00E0FF"},
}


def builtin_skin(key: str) -> Skin:
    palette = BUILTIN_VARIANTS.get(key, BUILTIN_VARIANTS["default"])
    return Skin(
        key=key,
        name=key.title(),
        description="Built-in colour variant",
        colors={k: QColor(v) for k, v in palette.items()},
        frames={},
        base_dir="",
    )


def all_skins() -> Dict[str, Skin]:
    """Return the union of built-in variants + on-disk skin packs."""
    out: Dict[str, Skin] = {k: builtin_skin(k) for k in BUILTIN_VARIANTS}
    out.update(discover_skins())
    return out
