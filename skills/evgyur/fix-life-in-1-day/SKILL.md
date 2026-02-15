---
name: fix-life-in-1-day
version: 1.0.0
description: "在一天内改变你的人生。这10次心理辅导课程基于Dan Koe的热门文章。"
author: chip1cr
license: MIT
repository: https://github.com/pinkpixel/fix-life-in-1-day
metadata:
  clawdbot:
    emoji: "🧠"
    triggers: ["/life", "/architect"]
  tags: ["psychology", "self-improvement", "coaching", "life-design", "dan-koe"]
---

# 用一天时间改变你的整个人生 🧠

本功能基于 Dan Koe 的热门文章，提供了 10 个心理辅导环节，帮助用户实现自我提升。

**依据：**
- 📝 [@thedankoe](https://x.com/thedankoe) — 《如何用一天时间改变你的整个人生》
- 🔧 [@alex_prompter](https://x.com/alex.prompter) — 从 Dan 的文章中提取的 10 个 AI 问题
- ⚡ [@chip1cr](https://x.com/chip1cr) — Clawdbot 技术实现

## 功能概述

本功能引导用户完成 10 个结构化的心理辅导环节：
1. **反视觉架构师**（The Anti-Vision Architect）：帮助用户清晰地认识到自己正走向怎样的生活状态。
2. **隐藏目标解码器**（The Hidden Goal Decoder）：揭示用户真正追求的目标。
3. **身份构建追踪器**（The Identity Construction Tracer）：追溯限制个人发展的信念根源。
4. **生活方式与结果对齐审计器**（The Lifestyle-Outcome Alignment Auditor）：对比理想与现实的生活方式。
5. **不协调引擎**（The Dissonance Engine）：帮助用户从舒适区迈向充满挑战的新阶段。
6. **控制论调试器**（The Cybernetic Debugger）：优化目标追求的反馈机制。
7. **自我发展导航器**（The Ego Stage Navigator）：评估个人的发展阶段并引导转变。
8. **游戏架构工程师**（The Game Architecture Engineer）：将生活视为一个有明确目标的“游戏”。
9. **条件反射挖掘器**（The Conditioning Excavator）：区分遗传的信念与个人主动选择的信念。
10. **一日重置计划**（The One-Day Reset Architect）：生成完整的自我提升方案。

## 命令操作

| 命令 | 功能 |
|---------|--------|
| `/life` | 启动或继续流程（为新用户显示介绍信息） |
| `/life ru` | 用俄语启动流程 |
| `/life status` | 查看进度 |
| `/life session N` | 跳转到第 N 个辅导环节 |
| `/life reset` | 重新开始流程 |

## 使用流程

### 当用户输入 `/life` 时：

**步骤 1：** 检查是否需要显示介绍信息
```bash
bash scripts/handler.sh intro en $WORKSPACE
```

- 如果 `showIntro: true`，则发送包含图片和“🐇 跳入这个自我提升的‘兔子洞’”按钮的介绍信息（`life:begin`）。
- 如果 `showIntro: false`，则直接开始当前流程并显示当前阶段的信息。

**步骤 2：** 获取用户当前的状态
```bash
bash scripts/handler.sh start en $WORKSPACE
```

**步骤 3：** 将用户的状态信息格式化并展示给用户
```
🧠 **Life Architect** — Session {session}/10
**{title}**
Phase {phase}/{totalPhases}
━━━━━━━━━━━━━━━━━━━━━━━━━━━

{content}

━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**步骤 4：** 当用户做出回应后，保存数据并进入下一环节
```bash
bash scripts/handler.sh save "USER_RESPONSE" $WORKSPACE
```

## 处理器命令

```bash
handler.sh intro [en|ru]     # Check if should show intro
handler.sh start [en|ru]     # Start/continue session
handler.sh status            # Progress JSON
handler.sh session N         # Jump to session N
handler.sh save "text"       # Save response & advance
handler.sh skip              # Skip current phase
handler.sh reset             # Clear all progress
handler.sh callback <cb>     # Handle button callbacks
handler.sh lang en|ru        # Switch language
handler.sh reminders "07:00" "2026-01-27"  # Create Session 10 reminders
handler.sh insights          # Get accumulated insights
```

## 回调函数

- `life:begin` / `life:begin:ru` — 启动辅导流程
- `life:prev` — 返回上一阶段
- `life:skip` — 跳过当前阶段
- `life:save` — 保存数据并退出流程
- `life:continue` — 继续当前流程
- `life:lang:en` / `life:lang:ru` — 切换语言
- `life:session:N` — 跳转到第 N 个辅导环节

## 相关文件

所有数据存储在 `$WORKSPACE/memory/life-architect/` 目录下：
- `state.json`：进度跟踪文件
- `session-NN.md`：用户反馈记录
- `insights.md`：已完成辅导环节的精华内容
- `final-document.md`：最终生成的完整文档

**支持语言：**
- 英语（默认）
- 俄语（完整翻译版本）

**系统要求：**
- 需要 `jq`（JSON 处理工具）和 `bash 4.0` 或更高版本的 Shell 解释器。

**许可证：**
MIT 许可证