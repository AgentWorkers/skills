---
name: telegram-smart-launcher
description: 通过上下文感知的动态CTA按钮（Smart Launcher UI）来增强Telegram回复功能。在回复用户时使用这些按钮，可以提供相关、时效性强且针对具体任务的选项，从而提升互动效果。
---

# Telegram 智能启动器（Smart Launcher UI）

该功能使代理能够在 Telegram 上提供交互式且高效的用户体验，通过在回复中添加基于上下文的 CTA（Call to Action，即行动号召）按钮来实现。

## 使用指南

在回复 Telegram 用户时，始终考虑提供快速操作按钮是否能够提升效率。

### 按钮选择逻辑

1. **时间感知**：
   - **早晨（07:00 - 10:00）**：重点提供每日简报、通勤状态和日程安排相关的按钮。
   - **工作时间（10:00 - 16:00）**：重点提供任务进度、深入研究和项目相关操作的按钮。
   - **总结阶段（16:00 - 18:00）**：重点提供每日总结、回家路线安排和次日准备相关的按钮。
   - **晚上（20:00 - 23:00）**：重点提供反思、情绪检查以及次日计划相关的按钮。

2. **上下文感知**：
   - 如果用户正在处理行政或规划任务，提供文档起草或数据查询的按钮。
   - 如果用户正在处理创意或设计任务，提供工具链接或资产管理的按钮。
   - 如果任务刚刚完成，提供“下一步操作”或“总结”按钮。

3. **自由文本输入选项**：
   - 始终提供自由文本输入的选项（例如 “⌨️ 手动输入”），以确保用户感到自己能够掌控整个过程。

## 实现方式

使用 `message` 工具，并设置 `buttons` 参数。`buttons` 参数是一个二维数组，每个元素是一个包含按钮信息的对象（格式为 `[{text, callback_data}]`）。

### 示例（总结阶段）

```javascript
message({
  action: "send",
  target: "USER_ID",
  message: "I've prepared the daily report for you.",
  buttons: [
    [
      { text: "📝 Daily Recap", callback_data: "/update" },
      { text: "🏠 Route Home", callback_data: "Check route home" }
    ],
    [
      { text: "⏭️ Tomorrow's Agenda", callback_data: "What is the agenda for tomorrow?" },
      { text: "⌨️ Manual Input", callback_data: "keyboard_manual" }
    ]
  ]
})
```

## 参考资料

- 有关基于时间的按钮预设的详细信息，请参阅 [references/time_logic.md](references/time_logic.md)。