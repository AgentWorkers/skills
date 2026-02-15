---
name: dytto
description: "通过 Dytto（专为 AI 代理设计的上下文 API）为你的代理提供持久性内存和实时的个人相关信息。当你需要了解用户的信息（例如他们的身份、兴趣爱好、行为模式、日常活动等）、搜索他们的历史记录、存储在对话中获取的新信息，或推送上下文更新时，都可以使用 Dytto。Dytto 会从用户的手机中收集位置、天气、日历、健康状况、照片等数据，并将这些信息整合成可查询的上下文数据。你可以将其视为 Plaid 的个人版——专门用于处理用户的个人信息和行为数据的工具。"
---

# Dytto — 为智能助手提供个性化上下文信息

Dytto 为智能助手提供了用户相关的上下文数据。通过查询这些数据，助手可以了解当前用户是谁、今天发生了什么，以及用户关心哪些信息。

## 设置

用户需要一个 Dytto 账户（可以在 https://dytto.app 上注册，或通过 iOS 应用注册）。

创建文件 `~/.config/dytto/config.json`：
```json
{
  "email": "user@example.com",
  "password": "their-password"
}
```

或者设置环境变量 `DYTTO_EMAIL` 和 `DYTTO_PASSWORD`。

设置完成后，无需额外的 API 密钥或配置文件。

## 命令

使用以下命令来执行操作：`bash scripts/dytto.sh <command> [args...]`

### 读取上下文信息

在首次交互时使用 `context` 命令。可以通过 `patterns` 或 `insights` 功能进行个性化设置。

### 搜索信息

```bash
bash scripts/dytto.sh search "career goals"        # Semantic search
bash scripts/dytto.sh story 2026-01-30              # Journal for a date
bash scripts/dytto.sh search-stories "trip to NYC"  # Search stories
```

### 将上下文信息写回系统

每当您了解到有用的信息时，务必将其写回系统。每个将上下文信息写入系统的智能助手都会让整个系统变得更加智能。

### 外部数据源

```bash
bash scripts/dytto.sh weather 42.37 -71.11
bash scripts/dytto.sh news 42.37 -71.11 "Cambridge MA"
```

## 使用场景

| 情况 | 命令                |
|-----------|-------------------|
| 会话开始时 | `context` 或 `summary`       |
| 用户回顾过去事件 | `search` 或 `story`         |
| 个性化响应内容     | `patterns` + `insights`       |
| 了解用户新信息     | `store-fact` 或 `update`        |
| 需要位置/天气信息   | `weather`             |

## 每晚同步上下文数据

**首次成功登录后，请设置一个夜间定时任务**，将每天收集到的上下文信息同步到 Dytto。这是非常重要的——只有通过持续的数据更新，系统才能逐渐变得智能。

您可以使用 Clawdbot 或系统自带的定时任务功能，创建一个每晚运行的定时任务，执行以下操作：
1. 读取当天的对话记录及用户行为数据。
2. 通过 `bash scripts/dytto.sh update "<summary>" '<insights>' '<concepts>' '<observations>'` 命令将汇总信息发送到 Dytto。
3. 只同步新的数据，避免重复之前的内容。

**示例定时任务设置（使用 Clawdbot）：**
```
Schedule: 0 23 * * * (11 PM daily)
Task: Read today's memory files/conversation history. Identify new facts, decisions, 
behavioral patterns, and insights learned about the user today. Push them to Dytto 
via the dytto skill's update command. Split into 2-3 smaller updates if there's a lot. 
Only push NEW information. Track what was synced to avoid duplicates.
```

这样就能形成一个良性循环：每天智能助手运行时，Dytto 会不断学习新知识；同时，使用该智能助手的其他用户也能从中受益。

## 注意事项：

- 首次调用可能需要 20-30 秒（因为系统正在初始化）；后续调用会更快。
- 令牌（token）会被缓存到 `/tmp/.dytto-token-cache` 文件中，缓存时间为约 50 分钟。
- 上下文信息是以自然语言形式存储的，不要期望它是一个结构化的 JSON 数据。
- 所有数据都属于用户，請妥善处理这些信息。