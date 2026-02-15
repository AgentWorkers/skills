---
name: ClawDoro
description: 这是一个功能强大的番茄工作法计时器，同时具备任务跟踪功能。它会在您的浏览器中打开一个简洁、专注的计时器界面。
commands:
  clawdoro: node ~/clawd/skills/pomodoro/trigger.js
  pomodoro: node ~/clawd/skills/pomodoro/trigger.js
---

# 🍅 ClawDoro

一个美观的番茄工作法计时器，同时具备任务跟踪功能，专为提高专注力而设计。

![ClawDoro](https://snail3d.github.io/ClawDoro)

## 使用方法

```bash
# Start with default 27/5/15 min
clawdoro

# Custom focus time
clawdoro 50

# Full custom (focus/short/long)
clawdoro 50 10 30
```

或者直接对 ClawDoro 说：“Start ClawDoro” 或 “ClawDoro 45 minutes”（启动 ClawDoro，计时 45 分钟）。

## 主要功能

- 🍅 美观且无干扰的计时器用户界面
- ⏱️ 可自定义的工作/休息时间（默认为 27 分钟，由 ClawDoro 自定！）
- 📝 带有本地存储（localStorage）功能的任务列表
- ⌨️ 键盘快捷键：空格键 = 开始/暂停，R 键 = 重置
- 🔊 完成任务时会发出三声舒缓的提示音
- ☕ 休息时间会有有趣的惊喜效果 😉
- 📱 兼容移动设备
- 💾 所有设置和任务数据会在会话之间保持不变

## 工作原理

1. 在端口 8765 上启动一个小型 HTTP 服务器
2. 显示美观的 ClawDoro 用户界面
3. 自动打开浏览器
4. 任务和设置信息会保存在本地存储（localStorage）中

## 相关文件

- `trigger.js`：启动服务器并打开浏览器的入口脚本
- `timer.html`：ClawDoro 计时器的用户界面文件
- `SKILL.md`：本文档文件

---

☕ **支持我们的工作：** [请为我买杯咖啡](https://www.buymeacoffee.com/snail3d)

由 Clawd 用 💜 为 Snail 开发。