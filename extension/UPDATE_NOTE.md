# Kaka 扩展 · 自动更新说明

从 **v1.1.0** 开始，Kaka Chrome 扩展改造成了 **薄壳（thin shell）** 架构：

## v1.3.0 这次修了什么

- **全屏漫游**：容器不再是右下角 260×210 的小格子，而是覆盖整个浏览器视口（`100vw × 100vh`）。
  Kaka 可以在整块视口里自由跑动、被抛掷、落地弹跳，物理上多了重力和摩擦。
- **不阻塞页面**：容器整体 `pointer-events: none`，iframe 本身也是 `pointer-events: none`；
  真正接收鼠标的是父页面上的一个 hitbox 元素，它 **只覆盖 Kaka 当前包围盒（和气泡）**。
  这样页面的滚动、点击、拖拽、右键都完全不受影响，只有真的点/摸/拖到 Kaka 时事件才被捕获。
- **事件转发协议**：iframe 每帧通过 `postMessage` 把命中盒（视口坐标）报给内容脚本；
  hitbox 触发的鼠标/触摸事件会以 `{type:'kaka:pointer'}` 转发回 iframe，
  由 iframe 内部的物理系统消化（拖拽 → 抛掷、点击 → 摸摸、右键 → 环形菜单）。
- 环形菜单打开时 hitbox 自动扩为全屏，确保按钮全都能点到。
- 打包版本：`v1.3.0`。

## v1.2.0 修了什么

- `host_permissions` 扩大到 `<all_urls>`，确保 MV3 扩展能在普通网页上稳定注入内容脚本。
- 新增扩展内置 `embed.html` 作为本地备用页；远端 `https://ustiniankw.github.io/Kaka/embed.html` 3 秒内不可用时会自动回退。
- 回退发生时会在页面右下角显示一条轻提示：`Kaka 加载失败：已切到本地备用模式（GH Pages 未就绪）`。

- 扩展本身几乎不包含 UI / 物理 / 交互逻辑，只做三件事：
  1. 在页面右下角挂一个固定定位的 `<iframe>`
  2. 把 `chrome.storage.local` 桥接给 iframe（`postMessage` 通信）
  3. 代理 iframe 请求的外链打开动作
- 真正的 Kaka 渲染、行走、菜单、气泡等，全部由远端的 [`embed.html`](https://ustiniankw.github.io/Kaka/embed.html) 提供。
- 该 HTML 托管在 GitHub Pages，仓库每次合并到 `main`，Actions 会自动重新部署。

## 用户视角的体验

- **只需安装一次**：任何时候我们更新了功能（新玩具、新性格、新签到、新皮肤……），
  你都会在下一次刷新页面时自动拿到最新版，无需重装扩展、无需手动更新。
- **数据仍在本地**：饥饿 / 心情 / 好感度 / DND 状态等都存在 `chrome.storage.local`，
  远端 iframe 通过 `postMessage` 拿数据，不会上传到任何服务器。
- **网络问题降级**：如果 GitHub Pages 暂时不可达，内容脚本会在 3 秒内自动切到扩展内置的备用 `embed.html`，
  Kaka 仍然会继续显示，其他数据也不受影响。

## 什么情况下需要重装 / 更新扩展本身？

只有以下几种改动才需要发布一个新的 `extension-vX.Y.Z` release：

- 新增 / 修改扩展权限（`manifest.json` 中的 `permissions` / `host_permissions`）
- 修改 `content.js`、`popup.html/.js`、图标等打包在扩展里的文件
- Chrome 强制升级 manifest 版本

其余功能升级（宠物行为、菜单、皮肤、玩法……）**只需要合并到 `main`**：

1. GitHub Actions 会自动把 `docs/` 部署到 GitHub Pages
2. 所有已安装扩展在下一次页面加载时立即拿到新版本

## 缓存策略

`content.js` 里的 iframe URL 会带上当日日期作为 query 参数，例如：

```
https://ustiniankw.github.io/Kaka/embed.html?ts=2026-07-17
```

- 同一天内可以吃到 GitHub Pages 的 CDN 缓存，加载最快
- 每天最多滞后一天拿到新版本；如果你想立即体验，把浏览器扩展 popup 里的
  「打开完整体验」链接手动打开，或直接刷新一次页面即可

## 相关文件

- `extension/manifest.json` — MV3 清单（v1.3.0）
- `extension/content.js` — 薄壳内容脚本（远端优先 + 本地回退）
- `extension/content.css` — 容器定位、投影与回退提示样式
- `extension/embed.html` — 扩展内置备用页（web_accessible_resources）
- `extension/popup.html` / `popup.js` — 3 个入口 + 状态 readonly 展示
- `docs/embed.html` — 真正的 Kaka 界面（远端加载）
- `.github/workflows/pages.yml` — Pages 自动部署
- `.github/workflows/release-extension.yml` — 扩展 ZIP 自动打包 & release
