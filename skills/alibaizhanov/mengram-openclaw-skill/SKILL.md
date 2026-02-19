---
name: mengram-memory
description: 长期记忆分为三种类型：事实（facts）、事件（events）和工作流程（workflows）。它能够记住用户的偏好设置、过去的对话内容以及在不同会话中学习到的操作步骤。这种记忆机制可用于回顾用户之前的发言、保存重要信息、了解用户当前的状态，或追踪已完成的工作流程。
homepage: https://github.com/AiBaizhanov/mengram
metadata: {"openclaw":{"emoji":"🧠","requires":{"env":["MENGRAM_API_KEY"],"bins":["curl","python3"]},"primaryEnv":"MENGRAM_API_KEY","files":["scripts/*"]}}
---
# Mengram 记忆系统

Mengram 是为 OpenClaw 代理设计的、类似人类长期记忆的系统，能够跨所有会话和渠道存储事实、事件和工作流程信息。

## Mengram 的功能

Mengram 提供了三种类型的记忆功能，它们协同工作：

- **语义记忆**：关于用户的信息（偏好、关系、工作习惯等）
- **情景记忆**：带有时间戳的事件及其结果（会议、旅行、决策等）
- **程序记忆**：记录了学习到的工作流程及其执行结果（包括成功或失败情况）

所有记忆信息都会在会话和渠道之间保持持久性。你在 WhatsApp 上学到的内容同样可以在 Discord 上查看。

## 使用工具

该技能使用 `Bash` 脚本在 `{baseDir}/scripts/` 目录下执行相关操作。

## 使用建议

**在回答关于用户、他们的偏好或个人信息的任何问题之前，** **务必先查询记忆系统**。这是非常重要的步骤——先检查记忆内容，再作出回应。

**在以下情况下将信息保存到记忆系统中：**
- 用户分享了个人信息（姓名、偏好、习惯、关系）
- 任务或事件完成（例如预订、部署、购买）
- 多步骤工作流程成功或失败完成
- 用户纠正了你的信息或提供了新的背景信息

**在以下情况下获取用户信息：**
- 开始新的会话或对话
- 用户询问“你对我了解多少”
- 你需要关于用户的全面背景信息

## 脚本说明

### 1. 查询记忆

搜索三种类型的记忆系统以获取相关内容。**在回答个人问题之前，请先执行此操作。**

```bash
bash {baseDir}/scripts/mengram-search.sh "search query here"
```

该脚本会返回与查询匹配的事实、过去事件和已知的工作流程。请使用具体的查询语句，例如 “coffee preferences” 而不是 “stuff about user”。

### 2. 保存到记忆系统

将对话内容保存下来，以便 Mengram 可以自动提取其中的信息。

```bash
bash {baseDir}/scripts/mengram-add.sh "user said: I'm allergic to peanuts and my meeting with Sarah went well yesterday"
```

你可以传递多条消息。Mengram 的 AI 会自动提取：
- 事实 → 保存到语义记忆中（例如 “用户对花生过敏”）
- 事件 → 保存到情景记忆中（例如 “昨天与 Sarah 会面，会议进行得很顺利”）
- 工作流程 → 保存到程序记忆中（如果提供了具体的步骤）

### 3. 获取用户信息

获取用户的全面信息，包括他们的身份、已知的知识以及最近发生的事件。

```bash
bash {baseDir}/scripts/mengram-profile.sh
```

该脚本会返回一个完整的用户信息概要，你可以利用这些信息来个性化回答用户的问题。

### 4. 保存工作流程

在完成多步骤任务后，将其保存为可重用的流程，并记录其执行结果（成功或失败）。

```bash
bash {baseDir}/scripts/mengram-workflow.sh "Resolved billing issue: 1) Checked subscription status 2) Found expired card 3) Sent renewal link 4) User confirmed payment"
```

下次遇到类似任务时，`mengram-search.sh` 会返回该工作流程及其成功率。

### 5. 验证连接状态

检查 Mengram 的连接是否正常工作。

```bash
bash {baseDir}/scripts/mengram-setup.sh
```

## 推荐的操作流程：

1. **会话开始时**：运行 `mengram-profile.sh` 以加载用户信息。
2. **用户询问个人问题时**：在回答之前运行 `mengram-search.sh "topic"`。
3. **用户分享新信息时**：使用相关消息运行 `mengram-add.sh`。
4. **任务完成后**：使用执行步骤运行 `mengram-workflow.sh`。
5. **定期更新**：使用 `mengram-add.sh` 保存最近的对话内容，以保持记忆系统的最新状态。

## 使用示例：

- “我最喜欢的餐厅是哪家？” → `mengram-search.sh "favorite restaurant"`
- “按照之前的习惯进行预订” → `mengram-search.sh "booking usual preferences"` 以确定 “之前的习惯” 是指什么。
- “我刚换了新手机，Galaxy S26” → `mengram-add.sh "user switched to Samsung Galaxy S26"`
- “请记住我是素食者” → `mengram-add.sh "user is vegetarian"`
- 用户询问 “你对我了解多少？” → `mengram-profile.sh`

## 配置设置

配置信息位于 `~/.openclaw/openclaw.json` 文件中。

```json
{
  "skills": {
    "entries": {
      "mengram-memory": {
        "enabled": true,
        "env": {
          "MENGRAM_API_KEY": "om-your-api-key-here"
        }
      }
    }
  }
}
```

你可以在 [https://mengram.io](https://mengram.io) 获取免费的 API 密钥。

## 安全与隐私说明：

- **外部接口**：仅使用 `https://mengram.io/v1/*`。
- **发送的数据**：用于提取记忆信息的对话文本和查询语句。
- **存储的数据**：提取的事实、事件和工作流程信息会保存在 Mengram 服务器（使用 PostgreSQL 和 pgvector 技术）上。
- **访问的环境变量**：仅 `MENGRAM_API_KEY`。
- **本地文件操作**：不涉及任何本地文件的读写操作。

**信任声明**：使用该技能意味着对话数据会被发送到 mengram.io 进行存储。请确保你信任 Mengram 并愿意将其用于存储你的对话数据。Mengram 是开源项目：[https://github.com/AiBaizhanov/mengram](https://github.com/AiBaizhanov/mengram)。