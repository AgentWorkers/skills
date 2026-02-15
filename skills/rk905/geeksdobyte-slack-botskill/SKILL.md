---
name: slack-actions
summary: Control Slack messaging, reactions, pins, and member information using Clawdbot.
description: 该功能允许使用安全的机器人令牌（bot token）与 Slack 进行身份验证后的交互，从而实现发送、编辑、删除、回复以及管理消息和置顶帖子的操作。
tags: ["slack","automation","collaboration","productivity","chatops"]
version: 1.2.0
author: Rayen Kamta / GEEKSDOBYTE LLC / GEEKSDOBYTE.COM
---
# Slack Actions 技能

## 概述

**Slack Actions 技能** 允许 Clawdbot 使用 Bot OAuth 令牌安全地与 Slack 频道和直接消息进行交互。

该技能使代理能够：

- 发送、编辑和删除消息
- 添加和列出反应（回复）
- 固定（pin）和取消固定（unpin）消息
- 阅读最近的频道历史记录
- 获取成员信息
- 列出工作区的表情符号

所有操作均基于配置的机器人账户所获得的权限来执行。

---

## 目的与功能

该技能通过 `SLACK_BOT_TOKEN` 环境变量提供的 Bot OAuth 令牌，实现经过身份验证的 Slack 操作。

使用有效的凭据，该技能可以：

- 管理消息和反应
- 维护固定的消息引用
- 获取基本用户元数据
- 支持轻量级的工作流自动化

该技能严格在配置的 Slack 机器人的授权范围内运行。

---

## 认证与配置

### 必需的环境变量

该技能需要一个 Slack 机器人用户的 OAuth 令牌。

使用前，请进行以下配置：

```

SLACK_BOT_TOKEN

```

示例：

```bash
export SLACK_BOT_TOKEN="xoxb-xxxxxxxxxxxx-xxxxxxxxxxxx-xxxxxxxxxxxx"
```

或者以 `.env` 格式：

```
SLACK_BOT_TOKEN=xoxb-xxxxxxxxxxxx-xxxxxxxxxxxx-xxxxxxxxxxxx
```

### 令牌要求

令牌必须包含以下 OAuth 权限范围：

* `chat:write`
* `channels:read`
* `channels:history`
* `reactions:write`
* `pins:write`
* `users:read`
* `emoji:read`

根据工作区政策，可能还需要其他权限范围。

### 凭据存储

* 令牌必须仅存储在环境变量中
* 严禁将令牌硬编码
* 严禁记录令牌信息
* 严禁在输出中暴露令牌

如果 `SLACK_BOT_TOKEN` 缺失、无效或被撤销，该技能将无法执行。

---

## 初始设置

要配置此技能，请按照以下步骤操作：

1. 在您的工作区创建一个 Slack 应用
2. 启用 Bot Token 认证
3. 分配所需的 OAuth 权限范围
4. 将应用安装到工作区
5. 复制机器人用户的 OAuth 令牌
6. 将令牌存储到 `SLACK_BOT_TOKEN` 变量中
7. 重启代理

设置完成后，该技能即可使用。

---

## 凭据限制

* 仅支持机器人用户令牌（格式为 `xoxb-`）
* 不支持用户令牌（格式为 `xoxp-`）
* 令牌必须属于单个工作区
* 不支持跨工作区的令牌
* 令牌必须定期轮换
* 令牌必须符合组织的安全政策

禁止未经授权使用凭据。

---

## 何时使用此技能

当用户请求以下操作时，激活此技能：

- 向 Slack 发送消息
- 对消息做出反应
- 编辑或删除内容
- 固定或取消固定消息
- 阅读最近的消息
- 查找用户信息
- 查看表情符号

示例触发语句：

> “将此消息发送到 #engineering。”
> “用勾号作为回复。”
> “将那条消息固定。”
> “U123 是谁？”

---

## 必需的输入参数

### 消息目标

* `channelId` — Slack 频道 ID（例如：`C1234567890`）
* `messageId` — Slack 消息 ID（例如：`1712023032.1234`）

### 反应（Reactions）

* `emoji` — Unicode 表情符号或 `:name:` 格式

### 发送消息

* `to` — `channel:<id>` 或 `user:<id>`
* `content` — 消息文本

消息上下文可能包含可重用的字段，如 `channel` 和 `slack message id`。

---

## 支持的操作组

| 操作组      | 状态    | 描述                                      |
| ---------- | ------- | --------------------------------- |
| reactions  | 已启用 | 添加和列出反应                              |
| messages   | 已启用 | 发送、编辑、删除和阅读消息                        |
| pins       | 已启用 | 管理固定的消息                              |
| memberInfo | 已启用 | 获取用户资料                              |
| emojiList  | 已启用 | 列出自定义表情符号                            |

---

## 可用的操作

### 对消息做出反应

```json
{
  "action": "react",
  "channelId": "C123",
  "messageId": "1712023032.1234",
  "emoji": "✅"
}
```

---

### 列出反应

```json
{
  "action": "reactions",
  "channelId": "C123",
  "messageId": "1712023032.1234"
}
```

---

### 发送消息

```json
{
  "action": "sendMessage",
  "to": "channel:C123",
  "content": "Hello from Clawdbot"
}
```

---

### 编辑消息

```json
{
  "action": "editMessage",
  "channelId": "C123",
  "messageId": "1712023032.1234",
  "content": "Updated text"
}
```

---

### 删除消息

```json
{
  "action": "deleteMessage",
  "channelId": "C123",
  "messageId": "1712023032.1234"
}
```

---

### 阅读最近的消息

```json
{
  "action": "readMessages",
  "channelId": "C123",
  "limit": 20
}
```

---

### 固定消息

```json
{
  "action": "pinMessage",
  "channelId": "C123",
  "messageId": "1712023032.1234"
}
```

---

### 取消固定消息

```json
{
  "action": "unpinMessage",
  "channelId": "C123",
  "messageId": "1712023032.1234"
}
```

---

### 列出固定的消息

```json
{
  "action": "listPins",
  "channelId": "C123"
}
```

---

### 获取成员信息

```json
{
  "action": "memberInfo",
  "userId": "U123"
}
```

---

### 列出工作区的表情符号

```json
{
  "action": "emojiList"
}
```

---

## 行为规则

* 在执行破坏性操作前确认身份
* 未经用户明确许可，严禁删除消息
* 对于确认操作，优先使用反应而非消息
* 在执行前验证输入内容
* 严禁泄露凭据

---

## 使用示例

### 标记任务完成

```json
{
  "action": "react",
  "channelId": "C123",
  "messageId": "1712023032.1234",
  "emoji": "✅"
}
```

---

### 发布状态更新

```json
{
  "action": "sendMessage",
  "to": "channel:C456",
  "content": "Deployment completed successfully."
}
```

---

### 保存重要消息

```json
{
  "action": "pinMessage",
  "channelId": "C123",
  "messageId": "1712023032.1234"
}
```

---

## 操作范围

该技能仅限于配置的机器人令牌授权的 Slack 工作区操作。

它不执行以下操作：

- 创建 Slack 应用
- 修改工作区设置
- 管理账单
- 绕过权限限制
- 升级权限

所有操作均遵守 Slack API 的限制。

---

## 合规性

该技能遵循 Slack API 服务条款和 OAuth 安全指南。

用户在部署前需获得组织的批准。

---

## 最佳实践

- 使用反应（reactions）实现轻量级的工作流
- 固定长期需要的信息
- 保持消息简洁
- 避免批量执行破坏性操作
- 定期轮换凭据

---