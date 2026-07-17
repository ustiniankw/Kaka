<div align="center">

# 🐾 Kaka — 你的桌面 / 浏览器摸鱼搭子

*一只会在屏幕上乱走、乱拉、卖萌、掉零食币的小怪。*

[![MIT License](https://img.shields.io/badge/License-MIT-yellow)](./LICENSE)
[![GitHub Pages](https://img.shields.io/badge/Landing-GitHub%20Pages-24292e?logo=github)](https://ustiniankw.github.io/Kaka/)
[![Desktop](https://img.shields.io/badge/Desktop-Electron-blue?logo=electron)](https://github.com/ustiniankw/Kaka/releases/latest)
[![Extension](https://img.shields.io/badge/Chrome%20Extension-v1.1.0-brightgreen?logo=googlechrome)](https://github.com/ustiniankw/Kaka/releases/latest)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)](https://www.python.org/)

**[🖥 下载桌面版（推荐）](https://github.com/ustiniankw/Kaka/releases/latest)** ·
**[🧩 安装浏览器扩展](https://github.com/ustiniankw/Kaka/releases/latest)** ·
**[🎮 在线试玩](https://08c7e4ef7824.aime-app.bytedance.net)** ·
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

## 🌐 四种形态

### 🖥 桌面版（Electron · 推荐）

真正意义上的**透明桌面宠物窗口** —— 覆盖全屏、总在最前、可选鼠标穿透；适合把 Kaka 当成「真的桌面宠物」。

- 👉 下载：<https://github.com/ustiniankw/Kaka/releases/latest>

#### macOS 打开提示“已损坏”怎么办

当前桌面版没有使用 Apple Developer 证书签名/公证，浏览器下载后 macOS Gatekeeper 可能会把它误判为“已损坏”。如果弹出 **“Kaka 已损坏，无法打开”**，请先把 Kaka 拖到「应用程序」，然后在终端运行：

```bash
xattr -cr /Applications/Kaka.app
open /Applications/Kaka.app
```

如果你还没有安装、只是下载了 DMG，也可以先清掉下载文件的隔离标记再打开：

```bash
xattr -cr ~/Downloads/Kaka-1.0.0-arm64.dmg
open ~/Downloads/Kaka-1.0.0-arm64.dmg
```

> 这是未签名/未公证应用的临时绕过方式；长期方案是接入 Apple Developer 证书签名和 notarization。

**平台支持**：

| 平台 | 发行物 | 说明 |
|---|---|---|
| Windows | `exe` / `-portable.exe` | 安装版 / 免安装 |
| macOS | `dmg` / `zip` | 直接拖拽安装 |
| Linux | `AppImage` / `deb` | 通用 / Debian 系 |

> 注意：桌面版的“自动更新”指的是 **UI 自动更新**（远端加载），
> 壳层（Electron app）只有在我们修改权限/窗口模型/托盘/快捷键等能力时才需要重新下载安装。

### 🧩 Chrome 扩展（v1.1.0+ 薄壳自动更新）

在**任意网页右下角**挂一只小 Kaka，跨页面同步状态，看到哪一页玩到哪一页。
**只需装一次**，未来所有新功能都会自动同步（原理见「[自动更新](#-自动更新原理)」）。

- 👉 [直接下载 Chrome 扩展 ZIP](https://github.com/ustiniankw/Kaka/releases/download/extension-v1.1.0/kaka-extension-v1.1.0.zip)
- 详细安装步骤见 [Chrome 扩展安装](#-chrome-扩展安装)

> 注意：Chrome 扩展需要下载 `kaka-extension-v1.1.0.zip`；`Kaka-1.0.0-arm64-mac.zip` 是 macOS 桌面版，不能作为浏览器扩展加载。

### 🎮 Web 版（推荐先玩）

最快的体验方式，**打开链接就能玩**：

> 👉 **<https://08c7e4ef7824.aime-app.bytedance.net>**

### 🖥 桌面版（Python · PySide6）

旧版真桌面宠物实现（需要 Python + pip install）。

- 详细运行步骤见 [桌面版快速开始](#-桌面版快速开始)

---

## 📦 详细安装

### Web 版

不需要装任何东西，直接访问：<https://08c7e4ef7824.aime-app.bytedance.net>。

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

1. 下载 [kaka-extension-v1.1.0.zip](https://github.com/ustiniankw/Kaka/releases/download/extension-v1.1.0/kaka-extension-v1.1.0.zip)（不要下载桌面版的 `Kaka-*-mac.zip`）
2. 解压到任意目录
3. Chrome / Edge 访问 `chrome://extensions/`，开启 **开发者模式**
4. 点 **「加载已解压的扩展程序」**，选中解压出来的目录（如果里面能看到 `manifest.json` 就选对了）
5. 打开任意网页，右下角会出现 Kaka —— 完成 ✅

想直接从源码装、跟随 main 分支开发也可以：把仓库 clone 下来直接选 `extension/` 目录即可。

### 🖥 桌面版快速开始（Python 版）

```bash
git clone https://github.com/ustiniankw/Kaka.git
cd Kaka
pip install -r requirements.txt
python run.py
```

全局老板键：`Ctrl+Shift+B` · 勿扰快捷键：`Ctrl+Shift+H`。

---

## 🔄 自动更新原理

Kaka 从扩展 v1.1.0 起就是一个薄壳（thin shell）：

- `extension/content.js` 只做 3 件事：注入 iframe、桥接 `chrome.storage`、代理外链
- 真正的 Kaka 逻辑全部在 [`docs/embed.html`](docs/embed.html) 里，由 **GitHub Pages** 托管
- 用户装完扩展后，每次刷新页面都会从 GH Pages 拉一份最新的 UI

桌面版（Electron）同样遵循薄壳原则：

- Electron 窗口只负责「透明置顶 + 托盘 + 全局快捷键」
- UI 从 GitHub Pages 加载：[`docs/embed-desktop.html`](docs/embed-desktop.html)

也就是说：

> **一次安装，UI 永远跟随 main 分支。**

**只有以下情况需要你重装 / 更新壳层**：

- 我们改了扩展/桌面壳权限或桥接协议（会发布新的 release）
- 系统/浏览器强制升级 API 或 manifest 版本

配套的 GitHub Actions（`.github/workflows/`）会：

- `pages.yml` —— 每次 `docs/` 或 `demo/` 有变动，自动重新部署 GitHub Pages
- `release-extension.yml` —— 每次 `extension/` 有变动，自动打包 ZIP 并发布新 release
- `release-desktop.yml` —— 每次 `desktop/`（或 workflow）有变动，自动构建并发布桌面版

---

## 🧱 项目结构

```text
Kaka/
├── docs/                     # GitHub Pages 内容
│   ├── index.html            # Landing 页
│   ├── embed.html            # 扩展 iframe 加载的宠物 UI
│   ├── embed-desktop.html    # 桌面版全屏 UI（Electron 加载）
│   └── CNAME
├── demo/                     # Web 完整试玩版
│   └── index.html
├── desktop/                  # Electron 桌面壳
│   ├── main.js
│   ├── preload.js
│   ├── package.json
│   └── build/                # 图标等构建资源
├── extension/                # Chrome 扩展（v1.1.0 薄壳）
│   ├── manifest.json
│   ├── content.js            # 薄壳内容脚本（< 80 行）
│   ├── content.css
│   ├── popup.html / popup.js
│   └── UPDATE_NOTE.md        # 自动更新说明
├── kaka/                     # Python 桌面版核心
│   ├── main.py
│   ├── pet.py
│   └── ...
├── .github/workflows/
│   ├── pages.yml             # 自动部署 GH Pages
│   ├── release-extension.yml # 自动打包并 release 扩展 ZIP
│   └── release-desktop.yml   # 自动构建并 release 桌面版
├── assets/
├── run.py
├── requirements.txt
└── README.md
```

---

## 🛠 技术栈

- **桌面版（Electron）**：透明全屏窗口 + 总在最前 + 托盘 + 全局快捷键
- **桌面版（Python）**：Python · [PySide6](https://doc.qt.io/qtforpython-6/) · 透明窗口 + 全局置顶
- **全局热键（Python）**：`pynput`
- **本地存档**：`localStorage`（Web/桌面 UI）· `chrome.storage.local`（扩展）· `~/.kaka/state.json`（Python 桌面版）
- **Web / embed**：原生 HTML + Canvas + 内联 JS，零依赖
- **Chrome 扩展**：MV3 薄壳，UI 由 GitHub Pages 远端加载
- **CI/CD**：GitHub Actions（Pages 部署 + Release 自动打包）

---

## 📜 License

MIT © 2026 [ustiniankw](https://github.com/ustiniankw)

<div align="center"><i>Kaka 陪你上班，一起摸鱼。</i></div>
