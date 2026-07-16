"""Right-click menu builder for Kaka."""
from __future__ import annotations

from typing import Callable

from PySide6.QtCore import QPoint
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu, QMessageBox

from . import skins as skins_mod, sprites
from .personality import PERSONALITIES
from .pet import Pet
from .stats import Stats
from .world import World


def build_and_show(parent: Pet, world: World, stats: Stats,
                   pos: QPoint, on_quit: Callable[[], None],
                   friends=None) -> None:
    menu = QMenu(parent)

    p = stats.personality
    header = QAction(f"{p.emoji}  {p.name_zh} · Kaka", parent)
    header.setEnabled(False)
    menu.addAction(header)
    menu.addSeparator()

    feed = QAction("🍪 喂食", parent)
    feed.triggered.connect(lambda: world.spawn_food())
    menu.addAction(feed)

    grav_text = "🌍 关闭重力" if parent.gravity() else "🪶 开启重力"
    grav = QAction(grav_text, parent)
    grav.triggered.connect(lambda: parent.set_gravity(not parent.gravity()))
    menu.addAction(grav)

    # ---- Work mode ----
    if parent.work_mode.active:
        wm = QAction("💼 结束代打工", parent)
        wm.triggered.connect(parent.stop_work_mode)
    else:
        wm = QAction("💼 代打工 2 分钟", parent)
        wm.triggered.connect(lambda: parent.start_work_mode(120))
    menu.addAction(wm)

    menu.addSeparator()

    # ---- Personality submenu ----
    pers_menu = menu.addMenu("🎭 性格")
    for key, per in PERSONALITIES.items():
        text = f"{per.emoji} {per.name_zh}"
        if key == stats.personality_key:
            text = "✓ " + text
        act = QAction(text, parent)
        act.triggered.connect(
            lambda _=False, k=key: (setattr(stats, "personality_key", k), stats.save())
        )
        pers_menu.addAction(act)
    pers_menu.addSeparator()
    reroll = QAction("🎲 随机换一个", parent)
    reroll.triggered.connect(lambda: (stats.reroll_personality(), stats.save()))
    pers_menu.addAction(reroll)

    # ---- Skins submenu ----
    skins_menu = menu.addMenu("🎨 皮肤")
    all_skins = skins_mod.all_skins()
    for key, sk in all_skins.items():
        text = f"● {sk.name}"
        if key == getattr(stats, "skin_key", "default"):
            text = "✓ " + text
        act = QAction(text, parent)
        def apply(_=False, s=sk):
            sprites.set_palette(s.colors)
            frames = {}
            for mood, _p in s.frames.items():
                pm = s.load_frame(mood)
                if pm is not None:
                    frames[mood] = pm
            sprites.set_frame_overrides(frames)
            stats.skin_key = s.key
            stats.save()
        act.triggered.connect(apply)
        skins_menu.addAction(act)

    # ---- Friends submenu ----
    if friends is not None:
        fmenu = menu.addMenu("👋 好友互访")
        actives = friends.active_friends()
        if not actives:
            f_act = QAction("（暂无在线好友）", parent)
            f_act.setEnabled(False)
            fmenu.addAction(f_act)
        else:
            for f in actives:
                a = QAction(f"● {f.name}  ({f.addr})", parent)
                a.setEnabled(False)
                fmenu.addAction(a)
        fmenu.addSeparator()
        mine = QAction(f"我的 ID: {friends.my_id[:6]} · {friends.my_name}", parent)
        mine.setEnabled(False)
        fmenu.addAction(mine)

    stat_action = QAction("📊 查看状态", parent)
    stat_action.triggered.connect(lambda: _show_stats(parent, stats))
    menu.addAction(stat_action)

    boss = QAction("🕶 老板键 (Ctrl+Alt+H)", parent)
    boss.triggered.connect(lambda: parent.setVisible(not parent.isVisible()))
    menu.addAction(boss)

    menu.addSeparator()

    about = QAction("❓ 关于 Kaka", parent)
    about.triggered.connect(lambda: _show_about(parent))
    menu.addAction(about)

    quit_a = QAction("🚪 退出", parent)
    quit_a.triggered.connect(on_quit)
    menu.addAction(quit_a)

    menu.exec_(pos)


def _show_stats(parent, stats: Stats) -> None:
    s = stats.snapshot()
    p = stats.personality
    msg = (
        f"{p.emoji}  性格 : {p.name_zh}   《{p.flavor}》\n\n"
        f"💛  好感度  Affinity : {s['affinity']:>5} / 100\n"
        f"🍚  饥饿   Hunger   : {s['hunger']:>5} / 100\n"
        f"😊  心情   Mood     : {s['mood']:>5} / 100\n"
        f"🧼  卫生   Hygiene  : {s['hygiene']:>5} / 100\n"
    )
    QMessageBox.information(parent, "Kaka 状态", msg)


def _show_about(parent) -> None:
    QMessageBox.about(
        parent, "关于 Kaka",
        "<h3>Kaka — 桌面摸鱼搭子 🐾</h3>"
        "<p>Multi-screen 漫游 · 皮肤 pack · 代打工 · LAN 好友互访</p>"
        "<p><a href='https://github.com/ustiniankw/Kaka'>github.com/ustiniankw/Kaka</a></p>",
    )
