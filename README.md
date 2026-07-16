<div align="center">

# 🐾 Kaka — 你的桌面摸鱼搭子

*一只会在你屏幕上乱走、乱拉、卖萌，让繁琐工作有点意思的小怪。*

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![PySide6](https://img.shields.io/badge/UI-PySide6-brightgreen)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)
![License](https://img.shields.io/badge/License-MIT-yellow)

</div>

---

## 🎮 立即试玩

不想安装？浏览器里就能玩到大部分手感 👉 **[在线 Web 试玩版](https://d1346a0046a9.aime-app.bytedance.net)**

> Web 版是行为模拟器（含走动 / 重力 / 拉屎 / 清理 / 喂食 / 拖拽 / 老板键 / 状态条），完整"透明桌面窗口"体验需运行桌面版。

## 一句话简介

**Kaka**（卡卡 / 咔咔 / 你懂的 💩）是一款用 Python + PySide6 写的桌面宠物：
- 它会在你的桌面上到处乱逛
- 会突然掉下来（重力开关随你切）
- 时不时会 💩 或 💦，需要你点掉清理
- 你可以喂它东西吃
- 老板来了按 `Ctrl+Alt+H` 一秒隐身
- 每工作 25 分钟它会跳出来提醒你摸个鱼

## ✨ 已实现功能（MVP v0.1）

| 分类 | 功能 |
|---|---|
| 🚶 移动 | 桌面随机行走 / 空闲发呆 / 拖拽扔飞 |
| 🌍 物理 | **无重力**（自由飘）与 **有重力**（下落到屏幕底）两种模式一键切换 |
| 💩 排泄 | 定时随机拉屎 / 尿尿，落在桌面上 |
| 🧹 清理 | 单击任意屎尿 → 消失，卫生度回升 |
| 🍪 喂食 | 右键菜单「喂食」→ 屏幕上出现食物，宠物走过去吃掉 |
| 🕶 老板键 | 全局热键 `Ctrl+Alt+H` 秒藏、再按秒回 |
| ⏱ 摸鱼提醒 | 番茄钟拟人化，Kaka 每 25 分钟提醒你歇会儿 |
| 📊 状态面板 | 右键 → 查看饥饿 / 心情 / 卫生 / 好感度 |
| 🖱 交互 | 左键点击互动、拖拽移动、右键出菜单 |

## 🗺 计划中（欢迎 PR）

- [ ] 睡眠周期（凌晨自动睡觉）
- [ ] 性格随机化（社恐 / 话痨 / 干饭王）
- [ ] 好感度解锁新动作 / 皮肤
- [ ] 「代打工」动画（假装帮你敲键盘）
- [ ] CPU 高负载时 Kaka 喘气擦汗
- [ ] 多屏漫游 / 掉下屏幕再爬回来
- [ ] 局域网互访：同款桌宠可以互相打招呼
- [ ] 皮肤 pack 系统（json + png 就能加新宠物）

## 🚀 快速开始

```bash
# 1. 克隆
git clone https://github.com/ustiniankw/Kaka.git
cd Kaka

# 2. 安装依赖（建议用 venv / conda）
pip install -r requirements.txt

# 3. 跑起来
python run.py
```

首次启动后屏幕右下角会出现一只**像素小怪**。它长这样（procedural 像素画，无需外部素材）：

```
   ██████
 ██  ●● ██
 ██  ██ ██
 ██ ████ ██
   ██████
    ██ ██
```

## 🎮 操作说明

| 操作 | 效果 |
|---|---|
| **左键单击 Kaka** | 摸摸头，心情 +1 |
| **左键拖拽 Kaka** | 提起来到处扔（松手时若开重力会自由落体） |
| **单击地上的 💩 / 💦** | 清理，卫生度 +1 |
| **右键 Kaka** | 打开菜单：喂食 / 切换重力 / 状态 / 老板键 / 退出 |
| **Ctrl + Alt + H** | 老板键，秒藏 / 秒回 |
| **右键菜单 → 状态** | 查看当前所有属性 |

## 🧠 状态系统

Kaka 有 4 个隐藏属性，每分钟自然变化，也会影响它的表情和动作：

| 属性 | 初值 | 变化 | 影响 |
|---|---|---|---|
| 饥饿 (Hunger) | 50 | 时间流逝会饿；喂食 +30 | 太饿会不想动 |
| 心情 (Mood) | 60 | 摸头 +1；饿到 <20 会掉 | 影响乱跑频率 |
| 卫生 (Hygiene) | 80 | 拉屎/尿会掉；清理 +10 | 太脏会有苍蝇（TODO） |
| 好感度 (Affinity) | 0 | 综合互动累计 | 未来解锁新皮肤 |

## 🛠 技术栈

- **UI**：[PySide6](https://doc.qt.io/qtforpython-6/) —— 透明无边框窗口 + 全局置顶
- **物理**：自写的轻量 tick 循环（QTimer 60fps）
- **热键**：[pynput](https://pypi.org/project/pynput/)（全局老板键）
- **状态存档**：本地 JSON（`~/.kaka/state.json`）

## 📁 项目结构

```
Kaka/
├── run.py                  # 启动入口
├── requirements.txt
├── kaka/
│   ├── __init__.py
│   ├── main.py             # 应用生命周期
│   ├── pet.py              # 宠物本体：窗口 + 行为
│   ├── world.py            # 世界管理器（重力、事件、屎尿）
│   ├── waste.py            # 💩 / 💦 / 🍪 等桌面小物件
│   ├── stats.py            # 属性数值系统 & 存档
│   ├── sprites.py          # 无外部素材，procedural 像素画
│   ├── hotkeys.py          # 全局老板键
│   ├── reminders.py        # 番茄钟提醒
│   └── menu.py             # 右键菜单
└── assets/                 # 可选：以后放皮肤 / 音效
```

## ❓ 常见问题

**Q: 在 macOS 上宠物点不动 / 无法接收点击？**
A: 需要在 `系统偏好设置 → 隐私与安全性 → 辅助功能` 里勾选运行 Kaka 的终端 / IDE，否则透明窗口在 Mac 上有点击穿透问题。

**Q: 我不想它自己拉屎，能关掉吗？**
A: 右键菜单 → 设置 → 关闭"排泄系统"（TODO：v0.2 加设置面板；v0.1 可以改 `kaka/world.py` 里的 `POOP_INTERVAL_S`）。

**Q: 多显示器？**
A: 目前只识别主屏；多屏漫游在 Roadmap 里。

## 🐣 贡献

欢迎提 Issue 或 PR！好玩、无聊、犯病的想法都欢迎：
- 想加个宠物形象？扔个 PR 到 `kaka/sprites.py`
- 想加个反差萌事件？改 `kaka/world.py` 就行
- 觉得默认参数太扰人？改 `kaka/config.py`

## 📜 License

MIT © 2026 [ustiniankw](https://github.com/ustiniankw)

---

<div align="center"><i>Kaka 陪你上班，一起摸鱼。</i></div>
