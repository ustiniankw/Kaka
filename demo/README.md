# Kaka · Web 试玩版

一个纯前端（HTML + Canvas）的 Kaka 桌面宠物**行为模拟器**，直接在浏览器里就能玩。

## ✨ 支持的手感

- 🚶 随机行走 / 空闲
- 🌍 重力开关（可切换有 / 无重力）
- 💩 定时拉屎尿尿，`💩 立刻拉` 按钮可手动触发
- 🧹 单击 💩 / 💦 清理
- 🍪 喂食：按钮丢食物，Kaka 会自己走过去吃掉
- 👋 拖拽 Kaka 扔飞（带惯性）
- 🕶 老板键：一键隐藏 / 显示
- 📊 实时状态条：饥饿、心情、卫生、好感度

## ⚠️ 与桌面版的区别

Web 版是**在一个 Canvas 舞台里**的行为模拟，无法真正在你的桌面上乱走。想体验"透明窗口跨屏漫游 + 全局老板键"完整版本，请下载并运行仓库根目录的 Python 桌面版：

```bash
pip install -r requirements.txt
python run.py
```

## 部署方式

```bash
# 用任意静态服务器都行：
cd demo
python3 -m http.server 8000
# open http://localhost:8000
```

或者直接双击 `index.html` 在浏览器里打开。
