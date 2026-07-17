<div align="center">

# 🐾 Kaka — 你的桌面 / 浏览器摸鱼搭子

*一只会在你屏幕上乱走、乱拉、睡觉、卖萌，让繁琐工作有点意思的小怪。*

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![PySide6](https://img.shields.io/badge/Desktop-PySide6-brightgreen)
![Web](https://img.shields.io/badge/Web-HTML%20%7C%20Canvas-orange)
![Chrome](https://img.shields.io/badge/Chrome-Extension-yellowgreen)
![License](https://img.shields.io/badge/License-MIT-yellow)

</div>

---

## 🎮 立即试玩 / 快速体验

- **在线 Web 试玩版（推荐）**：大部分行为和数值系统都可以体验
  - 👉 **[在线 Web 版 Demo](https://d1346a0046a9.aime-app.bytedance.net)**
- **Chrome 扩展开发版**：在任意网页右下角挂一只小 Kaka
  - 👉 安装方式见下文「[Chrome 扩展安装](#chrome-扩展安装)」
- **桌面版（Python）**：透明无边框窗口悬浮在桌面上
  - 👉 本地运行方式见「[桌面版快速开始](#桌面版快速开始)」

> Web 版是行为模拟器（含走动 / 重力 / 拉屎 / 清理 / 喂食 / 拖拽 / 便盆 / 家具 / 老板键 / 状态条 / 签到 / 周报 / 勿扰 / 屏保）。
> 真正的「透明桌面窗口 + 全局热键」体验仍由 Python 桌面版提供。

---

## 🧩 一句话简介

**Kaka**（卡卡 / 咔咔 / 你懂的 💩）是一款用 **Python + PySide6** 写的桌面宠物，同时带有 **Web 试玩版** 与 **Chrome 扩展**：

- 会在你的桌面 / 浏览器底部到处乱逛
- 会随机 **掉下来**（有重力 / 无重力 两种模式随时切）
- 时不时会 💩 或 💦，落在地板或便盆里，需要你点掉清理
- 你可以喂它东西吃、给它玩具玩、解锁新皮肤
- 支持多种性格（社恐 / 话痨 / 干饭王 / 懒鬼 / 傲娇 / 社牛）影响行为
- 支持每日签到、摸鱼周报、零食币经济、多屏漫游、代打工模式
- 老板来了还可以一键开启 **勿扰 / 老板键**，静音所有气泡和 toast

---

## ✨ 已实现功能总览（桌面版 + Web 版）

### 行为 & 物理

| 分类 | 功能 |
|------|------|
| 🚶 移动 | 桌面 / 浏览器底部随机行走 · 空闲发呆 · 跨屏游走 |
| 🪂 物理 | **无重力**（自由飘）与 **有重力**（下落到屏幕底）两种模式一键切换 |
| 🤾‍♂️ 抛掷 | 鼠标拖起后用力甩动可抛飞，带旋转 & 回弹；落地后会自己站起来 |
| 😴 休息 | 会根据心情和性格自动坐下 / 躺平 / 睡觉（窝里睡 / 地板睡） |
| 🧑‍💻 代打工 | 代打工模式下会跑到键盘上装模作样敲代码 |

### 排泄 & 清理

| 分类 | 功能 |
|------|------|
| 💩 排泄 | 定时随机拉屎 / 尿尿，支持落地 / 落在便盆里两种表现 |
| 🚽 便盆 | 可在房间里自由放置；会自动识别为上厕所目标位置 |
| 🧽 清理 | 单击任意 💩 / 💦 可清理，提升卫生度与好感度 |
| 🧴 便盆污垢 | 每次在便盆里解决一次，便盆污垢等级 +1；达到一定次数会变脏、带臭气特效 |
| 🤢 嫌弃 | 当便盆过脏时，Kaka 路过有几率冒泡「好臭好臭 🤢」，并小幅后退 |
| ✨ 一键冲厕所 | 点击便盆本体可一次性清理所有污垢、重置臭味并获得零食币奖励 |

### 经济 & 商店

| 分类 | 功能 |
|------|------|
| 🍬 零食币 | 统一货币，通过摸头、清理、喂食、玩玩具、番茄钟、签到等行为获得 |
| 🛍 商店 | 使用零食币解锁全新皮肤、玩具，部分对指定性格有折扣 |
| 🎨 皮肤 | 多种体色 / 气质皮肤，可在右侧面板自由切换 |
| 🧸 玩具 | 纸箱、毛线球、激光笔、猫爬架、禅石等多种玩具，拖到屏幕上 Kaka 会主动去玩 |

### 数值 & 性格系统

| 分类 | 功能 |
|------|------|
| 🧠 性格 | 7 种性格（社恐 / 话痨 / 懒鬼 / 干饭王 / 暴躁 / 傲娇 / 社牛），影响走路频率、拉屎频率、气泡频率等 |
| 📊 状态条 | 饥饿 (Hunger) / 心情 (Mood) / 卫生 (Hygiene) / 好感度 (Affinity) 四大属性，支持自然恢复和衰减 |
| 🧮 周报 | 每周统计番茄数、摸头次数、清理次数、玩具游玩次数等，生成摸鱼小报 |
| 🎁 每日签到 | 支持连续签到，七天一轮，满勤额外送大额零食币 |

### 时间感知 & 勿扰 / 屏保

| 分类 | 功能 |
|------|------|
| ⏱ 番茄钟 | 桌面版有完整番茄工作流；Web 版提供加速演示，番茄完成后会弹出 Kaka 提醒 |
| 📅 发薪日 & 周五事件 | 周五下午自动进入 KTV 模式、发薪日会触发跳舞事件（可强制开启 / 关闭） |
| 🔕 勿扰模式 | 快捷键 `Ctrl+Shift+H`（Web 版）或开关按钮，一键进入勿扰：隐藏宠物、关闭所有气泡 & toast，仅保留数值逻辑运行 |
| 💤 屏保睡觉 | 15 分钟无任何用户交互时，Kaka 会自动回窝睡觉，画面轻微变暗；下一次交互会醒来并给一点睡眠奖励 |

### 浏览器 & 扩展

| 分类 | 功能 |
|------|------|
| 🌐 Web 试玩 | `demo/index.html` 提供完整交互的浏览器版本，支持多屏、家具、玩具、签到、周报等新玩法 |
| 🧩 Chrome 扩展 | 内容脚本在页面底部注入一只小 Kaka，使用 `chrome.storage.local` 持久化状态 |
| 📊 扩展弹出页 | 点击工具栏图标可以查看当前饥饿/心情/好感度，并执行喂食、摸摸、签到等快捷操作 |
| 🔗 Landing Page | `docs/` 目录为 GitHub Pages 使用的静态 landing 页，集中展示玩法与安装说明 |

---

## 🖼 截图（占位）

> TODO：补充桌面版 / Web 版 / Chrome 扩展的实际截图。
>
> - 桌面版：透明窗口 + 多屏行走示例
> - Web 版：双屏舞台 + 右侧控制面板（皮肤 / 玩具 / 家具 / 状态条）
> - 扩展：任意网页右下角的小 Kaka + popup 状态面板

---

## 🚀 桌面版快速开始

```bash
# 1. 克隆仓库
git clone https://github.com/ustiniankw/Kaka.git
cd Kaka

# 2. 安装依赖（建议用 venv / conda）
pip install -r requirements.txt

# 3. 运行桌面版
python run.py
```

首次启动后屏幕右下角会出现一只 **像素小怪**。它长这样（procedural 像素画，无需外部素材）：

```
   ██████
 ██  ●● ██
 ██  ██ ██
 ██ ████ ██
   ██████
    ██ ██
```

---

## 🧩 Web 试玩版 & 本地预览

Web 试玩版本质上是一个纯 HTML + Canvas 的小页面，逻辑全部在 `demo/index.html` 内联 JS 中：

```bash
cd Kaka
# 用任意静态服务器打开 demo/，例如：
python -m http.server 8080
# 然后访问 http://localhost:8080/demo/
```

> 也可以直接访问托管好的在线版本：
> 
> 👉 **https://d1346a0046a9.aime-app.bytedance.net**

---

## 🧩 Chrome 扩展安装

> 当前扩展位于 `extension/` 目录，为开发者模式加载的 MV3 扩展。

1. 在 GitHub 上打开仓库：`github.com/ustiniankw/Kaka`
2. 点击 **Code › Download ZIP** 下载源码并解压
3. 打开 Chrome / Edge，访问 `chrome://extensions/`
4. 打开右上角 **开发者模式**
5. 点击 **“加载已解压的扩展程序”**
6. 选择解压后的项目中的 **`extension/`** 文件夹

完成后：

- 工具栏出现 **Kaka — 桌面宠物** 图标，点击可打开 popup 查看状态
- 任意网页右下角会注入一只小 Kaka（若未出现，刷新页面试试）

扩展主要文件：

- `extension/manifest.json` — MV3 清单
- `extension/content.js` — 内容脚本，在页面里注入小 Kaka
- `extension/content.css` — 内容脚本样式，全部使用 `kaka-ext-*` 前缀，减少对页面的影响
- `extension/popup.html` + `popup.js` — 工具栏弹出页，展示状态并提供快捷操作
- `extension/gen-icons.js` — 生成占位 PNG 图标的小脚本（默认生成 1×1 透明图标）

---

## 🧱 项目结构 / 架构

```text
Kaka/
├── demo/            # Web 试玩版（Canvas + 内联 JS）
│   └── index.html
├── extension/       # Chrome 扩展（content script + popup）
├── docs/            # GitHub Pages landing 页面（本 README 中链接的介绍站）
│   └── index.html
├── kaka/            # Python 桌面版核心逻辑
│   ├── main.py      # 应用生命周期
│   ├── pet.py       # 宠物本体：窗口 + 行为
│   ├── world.py     # 世界管理器（重力、事件、屎尿）
│   ├── waste.py     # 💩 / 💦 / 🍪 等桌面物件
│   ├── stats.py     # 属性 & 存档
│   ├── sprites.py   # 无外部素材，procedural 像素画
│   ├── hotkeys.py   # 全局老板键
│   ├── reminders.py # 番茄钟提醒
│   ├── shop.py      # 玩具 / 皮肤商店逻辑
│   └── ...          # 其它辅助模块
├── assets/          # 预留资源目录（皮肤 / 音效等）
├── run.py           # 桌面版启动入口
└── README.md        # 本文件
```

---

## 🧭 Roadmap（节选）

- ✅ Web 行为模拟器（多屏 / 家具 / 玩具 / 数值系统）
- ✅ 每日签到、零食币经济、摸鱼周报
- ✅ 便盆污垢等级 + 嫌弃气泡 + 点击便盆一键清理
- ✅ 勿扰 / 老板键（抑制所有气泡 & toast、隐藏宠物）
- ✅ 屏保模式：长时间无操作自动回窝睡觉
- ✅ Chrome 扩展开发版（content script + popup）
- ⏳ 更多玩具动作和特殊事件（CPU 高负载喘气 / 跨设备互访）
- ⏳ 更丰富的皮肤 pack 系统（json + png 自助加宠物）
- ⏳ 真·多端状态同步（桌面版 ↔ 浏览器 ↔ 扩展）

欢迎在 Issue / PR 里补充你想要的玩法：

- 想加个宠物形象？可以扔 PR 到 `kaka/sprites.py`
- 想加个反差萌事件？可以从 `kaka/world.py` 或 Web 版脚本入手
- 觉得默认参数太吵？可以改 `kaka/config.py` 或 `demo/index.html` 中对应常量

---

## 🛠 技术栈

- **桌面版**：Python · [PySide6](https://doc.qt.io/qtforpython-6/) · 透明无边框窗口 + 全局置顶
- **全局热键**：`pynput`（桌面老板键）
- **状态存档**：本地 JSON（`~/.kaka/state.json`）
- **Web 版**：原生 HTML + Canvas + 内联 JS（无外部依赖）
- **Chrome 扩展**：Manifest V3 · `chrome.storage.local` 做简单持久化

---

## 🐣 贡献

欢迎提 Issue 或 PR！好玩、无聊、犯病的想法都欢迎：

- 💠 新动作 / 表情
- 🧱 新玩具 / 家具
- 🎨 新皮肤 / 主题
- 📈 新的统计 / 周报指标

---

## 📜 License

MIT © 2026 [ustiniankw](https://github.com/ustiniankw)

---

<div align="center"><i>Kaka 陪你上班，一起摸鱼。</i></div>
