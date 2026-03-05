---
name: qordinate-structured-memory
description: Qordinate是一个专为AI设计的平台，它为OpenClaw代理提供了持久且结构化的存储空间，用于存储文档、联系人、任务、提醒、网络搜索结果以及关联的应用程序。您可以通过使用API密钥，通过MCP（Management Console）连接到该平台。
compatibility: Requires MCP client support (Streamable HTTP transport)
metadata:
  author: qordinate
  version: "0.3"
  openclaw:
    requires:
      env:
        - QORDINATE_API_KEY
      bins:
        - curl
    primaryEnv: QORDINATE_API_KEY
---
# Qordinate – 专为 OpenClaw 代理设计的 AI 驱动型记忆与生产力工具

Qordinate 是一个 AI 代理平台，能够为用户和代理提供持久、结构化的记忆与生产力支持。OpenClaw 代理无需将所有数据存储在本地临时存储或自定义数据库中，而是可以通过 **MCP（模型上下文协议，Model Context Protocol）** 与 Qordinate 连接，并利用 Qordinate 的 AI 功能来实现以下操作：

- **存储和检索文档**（笔记、文件、PDF 等）
- **管理联系人**（个人、公司、潜在客户）
- **维护带有状态、截止日期和提醒的列表和任务**
- **在网络上搜索最新信息**
- **与用户关联的第三方应用进行交互**
- **创建和管理表单并收集用户提交的数据**
- **设置按计划或事件触发的自动化任务**

代理通过一个名为 `query_agent` 的强大工具与 Qordinate 的 AI 功能进行通信，该工具支持自然语言交互。

---

## 连接详情

| 参数 | 值         |
|-------|-------------|
| **协议** | MCP（模型上下文协议）——基于流式 HTTP 的通信协议 |
| **MCP 服务器地址** | `https://api.qordinate.ai/mcp` |
| **认证方式** | 承载令牌（Bearer Token）——`Authorization: Bearer qk_YOUR_API_KEY` |
| **API 密钥格式** | 以 `qk_` 为前缀 |

---

## 用户设置（代理需要向用户说明的步骤）

在代理能够连接之前，用户需要拥有一个 Qordinate 账户和 API 密钥：
1. 访问 [https://app.qordinate.ai](https://app.qordinate.ai) 使用手机号码和验证码进行注册。
2. 进入 **个人资料 → API 密钥 → 创建新 API 密钥** 以生成 API 密钥。
3. 将生成的 API 密钥（以 `qk_` 开头）提供给代理。

API 密钥仅在创建时显示一次。用户可以设置其有效期（1–365 天），也可以选择永久有效。

---

## MCP 工具：`query_agent`

Qordinate 的 MCP 服务器提供了一个名为 `query_agent` 的工具，它是一个用于与整个 Qordinate AI 功能进行交互的自然语言接口。代理可以通过该工具访问用户的文档、联系人、列表、网络搜索结果以及所有关联的应用程序。

### 输入格式

| 参数 | 类型 | 是否必填 | 说明         |
|--------|------|-------------|-------------------|
| `query` | 字符串 | ✅      | 你需要 Qordinate 代理执行的查询或请求 |
| `session_id` | 字符串 | ❌      | （可选）用于多轮对话的会话 ID           |

### 如何使用 `session_id`

- 单次查询时可以省略 `session_id`。
- 在进行多轮对话时，从第一个响应中获取会话 ID 并在后续请求中传递它，以便 Qordinate 代理能够保持对话的上下文。

---

## 代理通过 `query_agent` 可以实现的功能

`query_agent` 工具可以调用整个 Qordinate AI 功能，实现用户直接与 Qordinate 交互时所能完成的所有操作：

### 结构化记忆（列表与任务）
- 创建、更新和查询 **列表**（任务、联系人、潜在客户、项目等）
- 为列表项设置 **截止日期**、**状态** 和 **提醒**
- Qordinate 会自动管理提醒和通知。

### 文档
- 创建、阅读、更新和删除文档
- 上传和下载文件（PDF、图片等）
- 与其他用户共享文档

### 联系人
- 存储和检索联系人信息
- 导入联系人数据（包括 VCF 格式）
- 按姓名、公司、职位等条件搜索联系人

### 网络搜索
- 在网络上搜索最新信息
- 代理可以请求 Qordinate 进行特定主题的搜索并返回结果

### 关联的应用程序
- 与用户关联的第三方应用程序进行交互
- 从关联的服务中查询数据

### 表单与自动化
- 创建表单并收集用户提交的数据
- 设置按计划或事件触发的自动化任务

---

## 示例交互方式

OpenClaw 代理可以通过 `query_agent` 传递以下参数来执行相应操作：

### 管理任务
```
Add a new task: Follow up with ACME about the reorder pilot, due next Tuesday 3pm, status todo, notes: important client meeting
```

### 存储联系人信息
```
Save a new contact: Harpinder Singh, Co-founder at qordinate.ai, building Qordinate
```

### 查询信息
```
Show me all my open tasks due this week
```

### 在网络上搜索
```
Search the web for the latest pricing of OpenAI GPT-4o API
```

### 处理文档
```
Create a new document titled "Meeting Notes - ACME Q1 Review" with the following content: ...
```

### 更新列表项
```
Mark the task "Follow up with ACME" as done
```

---

## 代理应如何使用 Qordinate

- 将 Qordinate 视为关于 “需要完成的任务” 和 “相关人员”的权威信息来源。
- 将用户日后可能用到的信息存储在 Qordinate 中，避免保存在临时内存中。
- 使用自然语言进行交互——`query_agent` 工具能够理解简单的英语指令。
- 在进行多步骤操作时使用相同的 `session_id`（例如，先查询任务列表，再标记某个任务为已完成）。
- 在查询中提供详细信息——包括列表名称、字段值、日期和上下文。

---

## 用户交互渠道（可选）

用户还可以通过他们偏好的消息平台直接与 Qordinate 进行交互，这些渠道与代理的 MCP 连接无关：
- **WhatsApp**：通过 [https://qordinate.ai/whatsapp](https://qordinate.ai/whatsapp) 连接
- **Telegram**：通过 [https://qordinate.ai/telegram](https://qordinate.ai/telegram) 连接
- **Slack**：通过 [https://qordinate.ai/slack](https://qordinate.ai/slack) 连接

用户在这些渠道上的所有操作都会反映在代理通过 MCP 访问的同一账户中，因此所有数据是共享的。