# build/（桌面版资源）

这里放 Electron 构建用的图标资源：

- `icon.png`：Linux 图标（占位）
- `icon.ico`：Windows 图标（占位）
- `icon.icns`：macOS 图标（占位）
- `tray.png`：托盘图标（占位）

> 说明：仓库里自带的是**程序生成的占位图标**（橙色方块）。
> 如果你希望发布到 Release 的安装包显示成真正的 Kaka 图标，请用你自己的图标替换这些文件。

推荐替换方式：

1. 准备一张 1024×1024 的 `icon.png`（透明背景、正方形）
2. 使用 macOS `iconutil` 或在线工具生成 `icon.icns`
3. 使用 `png2ico` / `icotool` / 在线工具生成 `icon.ico`
4. `tray.png` 建议 16×16 或 32×32（透明）

本目录下的占位文件由 `desktop/gen-icons.js` 生成。
