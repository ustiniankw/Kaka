# Kaka Desktop（Electron 桌面壳）

目标：一个**透明、总在最前、覆盖全屏**的 Electron 壳。

- 壳尽量“傻”：只负责窗口/托盘/快捷键
- UI 与逻辑从远端加载：`https://ustiniankw.github.io/Kaka/embed-desktop.html`
- 因此只要 GitHub Pages 更新，所有已安装桌面版用户**下次启动自动拿到新版本 UI**

## 开发

```bash
cd desktop
npm install
npm start
```

### Dev 模式加载本地 docs

```bash
cd desktop
KAKA_DEV=1 npm start
```

会直接加载 `../docs/embed-desktop.html`，方便本地调试 UI。

## 构建

```bash
cd desktop
npm run build:mac
npm run build:win
npm run build:linux
```

> 注意：桌面版的“自动更新”指的是 **UI 自动更新**（来自 GitHub Pages）。
> 只有当我们需要修改权限/窗口模型/托盘/快捷键等壳层能力时，才需要用户重新下载安装桌面壳。
