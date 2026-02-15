---
name: smart-followups
version: 2.1.5
description: 在用户输入“/followups”后，系统会生成相关的后续操作建议。此时会显示3个可点击的按钮：**Quick**（快速操作）、**Deep Dive**（深入探讨）和**Related**（相关内容）。
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

该功能能够为 OpenClaw 对话生成合适的跟进问题。

## 🚀 斜杠命令（v2.1.0 新增！）

**主要命令：**
```
/followups
```

**别名：**
```
/fu
/suggestions
```

当您输入 `/followups` 时，我会根据我们的对话内容生成 3 个合适的跟进问题：

1. ⚡ **快速问题** — 用于澄清疑问或确定下一步行动
2. 🧠 **深入探讨** — 用于深入理解技术细节
3. 🔗 **相关问题** — 用于关联相关话题或扩展讨论范围

---

## 使用方法

| 方法 | 例子 | 推荐方式 |
|--------|---------|-------------|
| 输入 `/followups` | 直接输入该命令 | ✅ 可以 |
| 使用别名 `/fu` | 输入 `/fu` | ✅ 可以 |
| 通过自然语言 | 说 “给我提些建议” | 也可以 |
| 在任何回答后 | 问 “我接下来应该问什么？” | 也可以 |

## 使用场景

在任何对话中输入 “followups” 即可：

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

**在文本聊天渠道（Signal/WhatsApp/iMessage/SMS）中：** 回复数字 1、2 或 3 来选择问题。

## 问题分类

每次生成的问题分为三类：

| 类别 | 表情符号 | 用途 |
|----------|-------|---------|
| **快速问题** | ⚡ | 用于澄清疑问、定义概念或确定下一步行动 |
| **深入探讨** | 🧠 | 用于深入理解技术细节或探讨高级概念 |
| **相关问题** | 🔗 | 用于关联相关话题、扩展讨论范围或提供替代方案 |

## 认证方式

**默认方式：** 使用 OpenClaw 的现有认证系统——与当前聊天会话使用的登录信息和模型相同。

**可选认证提供者：**
- `openrouter` — 需要 `OPENROUTER_API_KEY`
- `anthropic` — 需要 `ANTHROPIC_API_KEY`

## 配置选项

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
| `model` | `null` | 模型覆盖（`null` 表示继承自当前会话模型） |
| `apiKey` | — | 非 OpenClaw 提供者的 API 密钥 |

## 支持的聊天渠道

| 聊天渠道 | 交互方式 | 使用方法 |
|---------|------|-------------|
| Telegram | 按钮 | 点击按钮提问 |
| Discord | 按钮 | 点击按钮提问 |
| Slack | 按钮 | 点击按钮提问 |
| Signal | 文本 | 回复数字 1-3 来选择问题 |
| WhatsApp | 文本 | 回复数字 1-3 来选择问题 |
| iMessage | 文本 | 回复数字 1-3 来选择问题 |
| SMS | 文本 | 回复数字 1-3 来选择问题 |
| Matrix | 文本 | 回复数字 1-3 来选择问题 |
| Email | 文本 | 回复数字 1-3 来选择问题 |

详细渠道使用方法请参阅 [CHANNELS.md](CHANNELS.md)。

## 工作原理

1. 用户输入 `/followups`
2. 处理器捕获最近的对话内容
3. OpenClaw 使用当前模型和认证信息生成 3 个合适的跟进问题
4. 根据聊天渠道的不同，问题会以按钮或文本的形式显示
5. 用户点击按钮或回复数字来选择问题
6. OpenClaw 会针对用户的选择给出相应的回答

## 相关文件

| 文件 | 用途 |
|------|---------|
| `handler.js` | 命令处理逻辑和渠道显示逻辑 |
| `cli/followups-cli.js` | 独立的 CLI 工具，用于测试或脚本编写 |
| `README.md` | 完整的使用说明 |
| `CHANNELS.md` | 各聊天渠道的使用指南 |
| `FAQ.md` | 常见问题解答 |

## 致谢

该功能的灵感来源于 [Chameleon AI Chat](https://github.com/robbyczgw-cla/Chameleon-AI-Chat) 的智能跟进功能。