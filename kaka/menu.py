"""Right-click menu builder for Kaka."""
from __future__ import annotations

from typing import Callable

from PySide6.QtCore import QPoint
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu, QMessageBox

from .pet import Pet
from .stats import Stats
from .world import World


def build_and_show(parent: Pet, world: World, stats: Stats,
                   pos: QPoint, on_quit: Callable[[], None]) -> None:
    menu = QMenu(parent)

    feed = QAction("🍪 喂食", parent)
    feed.triggered.connect(lambda: world.spawn_food())
    menu.addAction(feed)

    grav_text = "🌍 关闭重力" if parent.gravity() else "🪶 开启重力"
    grav = QAction(grav_text, parent)
    grav.triggered.connect(lambda: parent.set_gravity(not parent.gravity()))
    menu.addAction(grav)

    menu.addSeparator()

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
    msg = (
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
        "<p>一只会乱走、乱拉、卖萌的桌面宠物。</p>"
        "<p>Made with ❤️ · Python + PySide6</p>"
        "<p><a href='https://github.com/ustiniankw/Kaka'>github.com/ustiniankw/Kaka</a></p>",
    )
