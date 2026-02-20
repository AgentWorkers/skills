---
name: mengram-memory
description: 长期记忆分为三种类型：事实、事件和工作流程。这些记忆机制会通过从失败中吸取经验而不断自我完善。系统能够记住用户的偏好、之前的对话内容以及用户在多次会话中学习到的操作流程。这些功能可用于回忆用户之前的发言内容、保存重要信息、了解用户背景、跟踪工作流程或报告操作结果。
homepage: https://github.com/AiBaizhanov/mengram
metadata: {"openclaw":{"emoji":"🧠","requires":{"env":["MENGRAM_API_KEY"],"bins":["curl","python3"]},"primaryEnv":"MENGRAM_API_KEY","files":["scripts/*"]}}
---
# Mengram 内存

Mengram 是为 OpenClaw 代理提供的一种类似人类长期记忆的功能，能够跨所有会话和渠道存储事实、事件和工作流程。

## Mengram 的功能

Mengram 提供了三种类型的记忆功能，它们协同工作：

- **语义记忆**：关于用户的信息（偏好、关系、工作习惯等）
- **情景记忆**：带有时间戳和结果的事件（会议、旅行、决策等）
- **程序记忆**：记录了包含成功/失败情况的工作流程（操作步骤）
- **基于经验的程序**：能够自我优化的流程：失败会触发自动进化，重复的成功会生成新的流程

所有记忆内容都会在会话和渠道之间保持持久性。你在 WhatsApp 上学到的信息同样可以在 Discord 上获取。

## 使用工具

该技能使用 `Bash` 脚本在 `{baseDir}/scripts/` 目录下执行相关操作。

## 使用时机

**在回答关于用户、他们的偏好、历史或任何个人信息的问题之前，** **务必先搜索记忆内容**。这是非常重要的——先查看记忆，再做出回答。

**在以下情况下将信息保存到记忆中：**
- 用户分享了个人信息（姓名、偏好、习惯、关系）
- 任务或事件完成（预订、部署、购买）
- 多步骤工作流程成功或失败
- 用户纠正了你的回答或提供了新的背景信息

**在以下情况下记录流程反馈：**
- 已知的工作流程成功时——运行 `mengram-feedback.sh` 并传入 `true`
- 已知的工作流程失败时——运行 `mengram-feedback.sh` 并传入 `false`，同时描述问题所在。这会触发流程的自动进化——流程会自我改进。

**在以下情况下获取用户档案：**
- 开始新的会话或对话时
- 用户询问“你了解我的哪些信息”
- 你需要关于用户的全面背景信息

## 脚本

### 1. 搜索记忆

在三种类型的记忆中搜索相关内容。**在回答个人问题之前，请先执行此操作。**

```bash
bash {baseDir}/scripts/mengram-search.sh "search query here"
```

返回与查询匹配的事实、过去事件和已知的工作流程。请使用具体的查询语句，例如 “coffee preferences” 而不是 “stuff about user”。

### 2. 保存到记忆中

将对话信息保存下来，以便 Mengram 可以自动提取其中的事实、事件和流程。

```bash
bash {baseDir}/scripts/mengram-add.sh "user said: I'm allergic to peanuts and my meeting with Sarah went well yesterday"
```

你可以传递多条消息。Mengram 的 AI 会自动提取：
- 事实 → 语义记忆（例如：“用户对花生过敏”）
- 事件 → 情景记忆（例如：“昨天与 Sarah 会面，进行得很顺利”）
- 流程 → 程序记忆（如果流程步骤被详细描述）

### 3. 获取用户档案

获取用户的全面信息——他们是谁、了解什么、最近发生了什么、掌握了哪些工作流程。

```bash
bash {baseDir}/scripts/mengram-profile.sh
```

返回一个完整的用户档案，你可以用它来个性化回答。

### 4. 保存工作流程

在完成多步骤任务后，将其保存为可重用的流程，并记录成功/失败情况。

```bash
bash {baseDir}/scripts/mengram-workflow.sh "Resolved billing issue: 1) Checked subscription status 2) Found expired card 3) Sent renewal link 4) User confirmed payment"
```

下次遇到类似任务时，`mengram-search.sh` 会返回该流程及其成功率。

### 5. 流程反馈（基于经验）

记录流程的成功或失败情况。**当流程失败时，系统会自动分析问题并生成改进后的版本。**

```bash
# Success
bash {baseDir}/scripts/mengram-feedback.sh "procedure-id" true

# Failure — triggers evolution
bash {baseDir}/scripts/mengram-feedback.sh "procedure-id" false "OOM error on step 3, forgot to increase memory limit" 3
```

参数：`<procedure-id> <true|false> [failure_context] [failed_at_step]`

流程 ID 会在搜索结果中返回。当流程进化时，系统会自动生成改进后的版本。

### 6. 查看所有流程

查看所有学到的流程，或深入查看特定流程以查看版本历史和进化记录。

```bash
# List all
bash {baseDir}/scripts/mengram-procedures.sh

# Specific procedure with version history
bash {baseDir}/scripts/mengram-procedures.sh "procedure-id"
```

显示流程名称、步骤、成功/失败次数、版本号以及完整的进化历史。

### 7. 检查连接状态

验证 Mengram 连接是否正常工作：

```bash
bash {baseDir}/scripts/mengram-setup.sh
```

## 推荐操作

1. **会话开始时：** 运行 `mengram-profile.sh` 以加载用户信息
2. **用户询问个人问题时：** 在回答之前运行 `mengram-search.sh "topic"`
3. **用户分享新信息时：** 运行 `mengram-add.sh` 并传入相关消息
4. **任务完成后：** 运行 `mengram-workflow.sh` 并传入操作步骤
5. **使用已知流程完成任务时：** 运行 `mengram-feedback.sh <id> true`
6. **使用已知流程完成任务但失败时：** 运行 `mengram-feedback.sh <id> false "what went wrong" <step>` — 这会触发流程的进化
7. **查看学到的流程：** 运行 `mengram-procedures.sh` 以查看所有流程及其版本
8. **定期：** 运行 `mengram-add.sh` 并传入最近的对话内容，以保持记忆的更新

## 示例

- “我最喜欢的餐厅是哪个？” → `mengram-search.sh "favorite restaurant"`
- “预订常规选项” → `mengram-search.sh "booking usual preferences"` 以确定“常规选项”的含义
- “我刚换了一部新手机，Galaxy S26” → `mengram-add.sh "user switched to Samsung Galaxy S26"`
- “记得我是素食者” → `mengram-add.sh "user is vegetarian"`
- 用户询问“你了解我的哪些信息？” → `mengram-profile.sh`
- 部署成功 → `mengram-feedback.sh "proc-id" true`
- 部署在第 3 步骤失败 → `mengram-feedback.sh "proc-id" false "forgot migrations" 3` → 流程会自动进化
- “展示我的工作流程” → `mengram-procedures.sh`

## 配置

配置信息请设置在 `~/.openclaw/openclaw.json` 文件中：

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

## 安全与隐私

- **外部接口：** `https://mengram.io/v1/*`（仅限此接口）
- **发送的数据：** 用于提取记忆内容的对话文本、搜索查询和流程反馈
- **存储的数据：** 提取的事实、事件和流程（包括版本历史）存储在 Mengram 服务器上（使用 PostgreSQL 和 pgvector）
- **访问的环境变量：** `MENGRAM_API_KEY`（仅用于此目的）
- **读取/写入的本地文件：** 无

**信任声明：** 使用此技能时，对话数据会被发送到 mengram.io 进行记忆提取和存储。只有在信任 Mengram 并愿意共享对话数据的情况下才请安装此技能。Mengram 是开源项目：[https://github.com/AiBaizhanov/mengram](https://github.com/AiBaizhanov/mengram)`