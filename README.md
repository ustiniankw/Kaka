<div align="center">

# 🐾 Kaka — 你的桌面 / 浏览器摸鱼搭子

*一只会在屏幕上乱走、乱拉、卖萌、掉零食币的小怪。*

[![MIT License](https://img.shields.io/badge/License-MIT-yellow)](./LICENSE)
[![GitHub Pages](https://img.shields.io/badge/Landing-GitHub%20Pages-24292e?logo=github)](https://ustiniankw.github.io/Kaka/)
[![Extension](https://img.shields.io/badge/Chrome%20Extension-v1.1.0-brightgreen?logo=googlechrome)](https://github.com/ustiniankw/Kaka/releases/latest)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)](https://www.python.org/)

**[🎮 在线试玩](https://d1346a0046a9.aime-app.bytedance.net)** ·
**[📦 一键安装扩展](https://github.com/ustiniankw/Kaka/releases/latest)** ·
**[⭐ GitHub](https://github.com/ustiniankw/Kaka)** ·
**[🌐 Landing](https://ustiniankw.github.io/Kaka/)**

</div>

---

## ✨ 玩法一览

- 🚶 **随机行走** —— 在桌面 / 浏览器底部乱逛、跨屏漫游
- 🪂 **物理开关** —— 无重力自由飘 & 有重力自由落体两种模式
- 🤾 **拖拽抛飞** —— 抓起 Kaka 用力甩，落地会自己爬起来
- 💩 **拉屎清理** —— 会 💩/💦，脏了会嫌弃自己，也会奖励清理你
- 🚽 **便盆污垢等级** —— 便盆用久变脏，一键冲水掉 🍬
- 🎮 **玩具系统** —— 毛线球 / 纸箱 / 激光笔 / 猫爬架，拖到桌面自己会玩
- 🍬 **零食币经济** —— 摸头 / 清理 / 番茄钟 / 签到都掉币，可解锁皮肤和玩具
- 🧠 **性格系统** —— 社恐 / 话痨 / 干饭王 / 懒鬼 / 傲娇 / 社牛 / 暴躁，行为完全不同
- 🎁 **每日签到** —— 七天一轮，满勤额外 +50 🍬
- 📊 **摸鱼周报** —— 每周一自动汇总番茄 / 摸头 / 清理次数（纯本地）
- 🔕 **勿扰 / 老板键** —— `Ctrl+Shift+H` 一键静音所有气泡 & 隐身
- 💤 **屏保睡觉** —— 15 分钟无互动自动回窝，下次操作会醒
- 🧑‍💻 **代打工模式** —— 让 Kaka 假装帮你敲键盘赶进度（心理安慰）

---

## 🌐 三种形态

### 🎮 Web 版（推荐先玩）
最快的体验方式，**打开链接就能玩**，几乎覆盖了扩展的全部行为 + 桌面版的大部分玩法：

> 👉 **<https://d1346a0046a9.aime-app.bytedance.net>**

### 🧩 Chrome 扩展（v1.1.0+ 薄壳自动更新）
在**任意网页右下角**挂一只小 Kaka，跨页面同步状态，看到哪一页玩到哪一页。
**只需装一次**，未来所有新功能都会自动同步（原理见「[自动更新](#-自动更新原理)」）。

- 👉 [下载最新 Release ZIP](https://github.com/ustiniankw/Kaka/releases/latest)
- 详细安装步骤见 [Chrome 扩展安装](#-chrome-扩展安装)

### 🖥 桌面版（Python · PySide6）
真正意义上的**透明桌面宠物窗口** —— 悬浮在你桌面上、跨屏漫游、支持全局老板键。

- 详细运行步骤见 [桌面版快速开始](#-桌面版快速开始)

---

## 📦 详细安装

### Web 版
不需要装任何东西，直接访问：<https://d1346a0046a9.aime-app.bytedance.net>。

如需本地跑：

```bash
git clone https://github.com/ustiniankw/Kaka.git
cd Kaka
python -m http.server 8080
# 浏览器打开 http://localhost:8080/demo/
```

### 🧩 Chrome 扩展安装

从 v1.1.0 开始扩展改造成了**薄壳 + GitHub Pages 远端 UI**，安装完就再也不用手动升级了。

**30 秒安装流程**：

1. 前往 [Releases](https://github.com/ustiniankw/Kaka/releases/latest) 下载 `kaka-extension-vX.Y.Z.zip`
2. 解压到任意目录
3. Chrome / Edge 访问 `chrome://extensions/`，开启 **开发者模式**
4. 点 **「加载已解压的扩展程序」**，选中解压出来的 `extension/` 目录（如果解压后已经就是根，就选那个目录）
5. 打开任意网页，右下角会出现 Kaka —— 完成 ✅

**动画版**（landing 页面上有交互动画）：

```
📥 下载 ZIP  →  ⚙️ chrome://extensions  →  🎉 加载已解压 → Kaka 出现
```

想直接从源码装、跟随 main 分支开发也可以：把仓库 clone 下来直接选 `extension/` 目录即可。

### 🖥 桌面版快速开始

```bash
git clone https://github.com/ustiniankw/Kaka.git
cd Kaka
pip install -r requirements.txt
python run.py
```

首次启动屏幕右下角会出现一只 procedural 生成的像素小怪：

```
   ██████
 ██  ●● ██
 ██  ██ ██
 ██ ████ ██
   ██████
    ██ ██
```

全局老板键：`Ctrl+Shift+B` · 勿扰快捷键：`Ctrl+Shift+H`。

---

## 🔄 自动更新原理

**Kaka 扩展 v1.1.0 起是一个薄壳（thin shell）**：

- `extension/content.js` 只做 3 件事：注入 iframe、桥接 `chrome.storage`、代理外链
- 真正的 Kaka 逻辑全部在 [`docs/embed.html`](docs/embed.html) 里，由 **GitHub Pages** 托管
- 用户装完扩展后，每次刷新页面都会从 GH Pages 拉一份最新的 UI

也就是说：

> **一次安装，永久跟随 main 分支。**
> 我们改进宠物行为、新增皮肤 / 玩具 / 事件、修 bug 后合并到 `main`，
> 你在下一次刷新页面时就自动拿到新版本，**无需重装扩展**。

**只有以下情况需要你重装 / 更新扩展**：

- 我们改了扩展权限或桥接协议（会发布新的 `extension-vX.Y.Z` release）
- Chrome 强制升级 manifest 版本

配套的 GitHub Actions（`.github/workflows/`）会：

- `pages.yml` —— 每次 `docs/` 或 `demo/` 有变动，自动重新部署 GitHub Pages
- `release-extension.yml` —— 每次 `extension/` 有变动，自动打包 ZIP 并发布新 release

---

## 🧱 项目结构

```text
Kaka/
├── docs/                     # GitHub Pages 内容
│   ├── index.html            # Landing 页（3 大按钮）
│   ├── embed.html            # 扩展 iframe 加载的宠物 UI
│   └── CNAME
├── demo/                     # Web 完整试玩版
│   └── index.html
├── extension/                # Chrome 扩展（v1.1.0 薄壳）
│   ├── manifest.json
│   ├── content.js            # 薄壳内容脚本（< 80 行）
│   ├── content.css
│   ├── popup.html / popup.js
│   └── UPDATE_NOTE.md        # 自动更新说明
├── kaka/                     # Python 桌面版核心
│   ├── main.py
│   ├── pet.py
│   ├── world.py
│   ├── waste.py
│   ├── stats.py
│   ├── sprites.py            # procedural 像素画，无外部资源
│   ├── hotkeys.py
│   ├── reminders.py
│   ├── shop.py
│   └── ...
├── .github/workflows/
│   ├── pages.yml             # 自动部署 GH Pages
│   └── release-extension.yml # 自动打包并 release 扩展 ZIP
├── assets/
├── run.py
├── requirements.txt
└── README.md
```

---

## 🛠 技术栈

- **桌面版**：Python · [PySide6](https://doc.qt.io/qtforpython-6/) · 透明窗口 + 全局置顶
- **全局热键**：`pynput`
- **本地存档**：`~/.kaka/state.json`（桌面版）· `chrome.storage.local`（扩展）· `localStorage`（Web）
- **Web / embed**：原生 HTML + Canvas + 内联 JS，零依赖
- **Chrome 扩展**：MV3 薄壳，UI 由 GitHub Pages 远端加载
- **CI/CD**：GitHub Actions（Pages 部署 + Release 自动打包）

---

## 🐣 开发 & 贡献

任何想法都欢迎 —— 好玩的、无聊的、犯病的：

- 💠 新动作 / 新表情 → `kaka/sprites.py` or `demo/index.html`
- 🧱 新玩具 / 家具 → `kaka/shop.py` or `demo/index.html`
- 🎨 新皮肤 pack → 计划中的 json + png 自助加宠物系统
- 📈 新周报指标 → `kaka/stats.py`

开发流程：

```bash
# 直接改 docs/embed.html → push 到 main → 所有装了扩展的用户自动拿到更新
# 需要修改扩展本身 → 改 extension/*.js → push → Actions 自动打新 release
```

---

## 🧭 Roadmap（节选）

- ✅ Web 行为模拟器（多屏 / 家具 / 玩具 / 数值系统）
- ✅ 每日签到、零食币经济、摸鱼周报
- ✅ 便盆污垢等级 + 嫌弃气泡 + 一键冲水
- ✅ 勿扰 / 老板键（气泡 & toast 静音、宠物隐身）
- ✅ 屏保：长时间无操作回窝睡觉
- ✅ **Chrome 扩展薄壳 + GH Pages 自动更新（v1.1.0）**
- ✅ **GitHub Actions CI/CD（Pages + Release 自动打包）**
- ⏳ 更多玩具动作和特殊事件（CPU 高负载喘气 / 跨设备互访）
- ⏳ 皮肤 pack 系统（json + png 自助加宠物）
- ⏳ 真·多端状态同步（桌面 ↔ Web ↔ 扩展）

---

## 📜 License

MIT © 2026 [ustiniankw](https://github.com/ustiniankw)

<div align="center"><i>Kaka 陪你上班，一起摸鱼。</i></div>
