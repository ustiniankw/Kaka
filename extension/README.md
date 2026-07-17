# Kaka Chrome 扩展（开发版）

这个目录下是 Kaka 的 **浏览器扩展版本**，可以在任意网页右下角养一只小 Kaka。

> ⚠️ 当前为开发者预览版本，图标和部分交互为占位实现，欢迎根据需要继续美化。

## 功能概览

- 在页面底部随机行走的像素风 Kaka
- 简单的饥饿 / 心情 / 好感度数值系统（随时间衰减）
- 右键 Kaka 弹出菜单：
  - `🍪 喂食`
  - `🤚 摸摸`
  - `🔕 勿扰` 开关（与内容脚本内的 DND 状态同步）
  - `🖥 打开完整 Web 体验`（GitHub Pages landing）
- 所有状态持久化在 `chrome.storage.local`，跨页面共享
- 扩展图标弹出页（popup）中可快速查看当前状态并执行快捷操作

## 安装方式（开发加载）

1. 在 GitHub 上下载本仓库 ZIP 压缩包并解压
2. 打开 Chrome / Edge，访问 `chrome://extensions/`
3. 右上角打开 **开发者模式**
4. 点击 **“加载已解压的扩展程序”**
5. 选择本项目根目录下的 `extension/` 文件夹

安装完成后：

- 页面右下角会出现一只小 Kaka（如未出现，可刷新页面）
- 工具栏中会出现 `Kaka — 桌面宠物` 图标，点击可打开弹出页查看状态

## 图标说明

当前仓库中的图标为脚本生成的 **占位透明 PNG**：

- `gen-icons.js` 会利用内置 base64 字符串生成 `icon16.png`、`icon48.png`、`icon128.png`
- 默认是一张 1×1 的透明像素，只为满足 Chrome 对 PNG 资源的要求

如果你想换成真正的 Kaka 图标，可以：

1. 用任意设计工具导出 16 / 48 / 128 尺寸的 PNG 图标
2. 覆盖 `extension/` 目录下对应的 `icon*.png` 文件
3. 在 `chrome://extensions/` 页面点击 **重新加载** 该扩展

也可以修改 `gen-icons.js`，替换为你自己的 base64 PNG 数据，或拓展为使用 Canvas/Node 绘制真正的像素猫图标。

## 目录结构

```text
extension/
├── manifest.json      # Chrome 扩展清单（MV3）
├── content.js         # 内容脚本：在页面中注入小 Kaka
├── content.css        # 内容脚本样式，所有选择器都带 kaka-ext 前缀
├── popup.html         # 工具栏图标点击后的弹出界面
├── popup.js           # 读取 / 更新 chrome.storage.local 中的状态
├── gen-icons.js       # 生成占位 PNG 图标的小脚本
├── icon16.png         # 由 gen-icons.js 生成，占位图标
├── icon48.png         # 同上
└── icon128.png        # 同上
```

## 开发提示

- 内容脚本和 popup 共用同一个存储键：`kaka_ext_state_v1`
- 如果你需要增加更多属性（例如金币、玩具、性格等），可以在该对象上按需拓展
- 若修改了 `content.js` / `popup.html` / `popup.js`，记得在扩展管理页面点击 **重新加载**

---

后续计划：

- 与 Web 版 demo 的零食币 / 每日签到 / 每周报告联动
- 更多动作和小动画（打工模式、睡觉、玩玩具）
- 更精致的图标与 Setting 面板
