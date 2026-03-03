---
name: smart-followups
version: 2.1.6
description: 在用户输入“/followups”时，系统会生成相关的后续操作建议。此时会显示3个可点击的按钮：**Quick**（快速操作）、**Deep Dive**（深入探讨）和**Related**（相关内容）。
metadata: {"openclaw":{"requires":{"bins":["node"],"note":"No API keys needed. Uses OpenClaw-native auth."}}}
triggers:
  - /followups
  - followups
  - follow-ups
  - suggestions
  - give me suggestions
  - what should I ask
commands:
  - name: followups
    description: Generate 3 smart follow-up suggestions based on conversation context
    aliases: [fu, suggestions, next]
channels:
  - telegram
  - discord
  - slack
  - signal
  - whatsapp
  - imessage
  - sms
  - matrix
  - email
---
# 智能跟进功能

为 OpenClaw 对话生成合适的跟进问题。

## 🚀 斜杠命令（v2.1.0 新功能！）

**主要命令：**
```
/followups
```

**别名：**
```
/fu
/suggestions
```

当您输入 `/followups` 时，我会根据我们的对话生成 3 个合适的跟进问题：

1. ⚡ **快速问题** — 用于澄清或确定下一步行动
2. 🧠 **深入探讨** — 需要更深入的技术解释或详细分析
3. 🔗 **相关问题** — 与当前话题相关或提供更广泛的背景信息

---

## 如何触发

| 方法 | 示例 | 推荐方式 |
|--------|---------|-------------|
| `/followups` | 直接输入该命令 | ✅ 可以 |
| `/fu` | 简短别名 | ✅ 可以 |
| 使用自然语言 | “给我一些建议” | 也可以 |
| 在任何回答后 | “我接下来应该问什么？” | 也可以 |

## 使用方法

在任何对话中输入 “followups”：

```
You: What is Docker?
Bot: Docker is a containerization platform...

You: /followups

Bot: 💡 What would you like to explore next?
[⚡ How do I install Docker?]
[🧠 Explain container architecture]
[🔗 Docker vs Kubernetes?]
```

**在按钮式聊天渠道（Telegram/Discord/Slack）中：** 点击按钮来提问。

**在文本聊天渠道（Signal/WhatsApp/iMessage/SMS）中：** 回复数字 1、2 或 3。

## 分类

每个命令会生成 3 个问题：

| 分类 | 表情符号 | 用途 |
|----------|-------|---------|
| **快速问题** | ⚡ | 用于澄清疑问、定义概念或确定下一步行动 |
| **深入探讨** | 🧠 | 需要深入的技术解释或详细分析 |
| **相关问题** | 🔗 | 与当前话题相关或提供更广泛的背景信息 |

## 认证

**默认方式：** 使用 OpenClaw 的现有认证系统——与当前聊天相同的登录方式和模型。

**可选认证提供者：**
- `openrouter` — 需要 `OPENROUTER_API_KEY`
- `anthropic` — 需要 `ANTHROPIC_API_KEY`

## 配置

```json
{
  "skills": {
    "smart-followups": {
      "enabled": true,
      "provider": "openclaw",
      "model": null
    }
  }
}
```

| 选项 | 默认值 | 说明 |
|--------|---------|-------------|
| `provider` | `"openclaw"` | 认证提供者：`openclaw`、`openrouter`、`anthropic` |
| `model` | `null` | 模型覆盖（`null` 表示继承自会话设置） |
| `apiKey` | — | 非 OpenClaw 提供者的 API 密钥 |

## 支持的聊天渠道

| 聊天渠道 | 交互方式 | 使用方式 |
|---------|------|-------------|
| Telegram | 按钮 | 点击按钮提问 |
| Discord | 按钮 | 点击按钮提问 |
| Slack | 按钮 | 点击按钮提问 |
| Signal | 文本 | 回复数字 1-3 |
| WhatsApp | 文本 | 回复数字 1-3 |
| iMessage | 文本 | 回复数字 1-3 |
| SMS | 文本 | 回复数字 1-3 |
| Matrix | 文本 | 回复数字 1-3 |
| Email | 文本 | 回复数字 1-3 |

有关详细渠道信息，请参阅 [CHANNELS.md](CHANNELS.md)。

## 工作原理

1. 用户输入 `/followups`
2. 处理器捕获最近的对话内容
3. OpenClaw 使用当前模型和认证信息生成 3 个合适的跟进问题
4. 根据聊天渠道的不同，问题会以按钮或文本的形式显示
5. 用户点击按钮或回复相应的数字
6. OpenClaw 会回答相应的问题

## 相关文件

| 文件 | 用途 |
|------|---------|
| `handler.js` | 命令处理程序和聊天渠道格式化代码 |
| `cli/followups-cli.js` | 独立的 CLI 工具，用于测试或脚本编写 |
| `README.md` | 完整的文档 |
| `CHANNELS.md` | 各聊天渠道的使用指南 |
| `FAQ.md` | 常见问题解答 |

## 致谢

本功能的灵感来源于 [Chameleon AI Chat](https://github.com/robbyczgw-cla/Chameleon-AI-Chat) 的智能跟进功能。