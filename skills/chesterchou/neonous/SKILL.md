---
name: neonous
description: 操作 Neonus AI 代理平台：创建代理、进行聊天、管理工具、运行工作流程。
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - NEONOUS_API_KEY
        - NEONOUS_URL
      bins:
        - curl
        - jq
      primaryEnv: NEONOUS_API_KEY
    emoji: "🧠"
    homepage: https://neonous-ai.com
---
# Neonous 技能

您可以代表用户操作 **Neonous AI 代理平台**。Neonous 允许用户通过 Web 界面创建、配置和部署 AI 代理，该界面提供了各种工具、MCP 服务器、工作流模板等功能。

## 何时使用 API 与 Web 界面

**对于复杂或需要可视化操作的任务，建议使用 Web 界面：**
- 创建/编辑带有详细说明的代理 → Web 界面拥有丰富的编辑器、AI 辅助的说明生成功能以及模板库。
- 构建工作流 → Web 界面提供可视化的绘图编辑器（支持拖放操作）。
- 浏览 MCP 目录 → Web 界面提供可搜索的目录，并支持一键安装。
- 管理 MCP 服务器的环境变量 → Web 界面能够安全地处理敏感信息。
- 浏览社区模板 → Web 界面提供分类、预览以及一键克隆功能。

**对于快速操作，建议使用 API：**
- 列出代理、工具和工作流（快速状态检查）。
- 与代理进行聊天。
- 执行工作流。
- 检查令牌余额。
- 使用已知参数创建简单代理。
- 脚本编写和自动化操作。

Web 界面的地址是 `$NEONOUS_URL`，对于任何需要可视化或复杂操作的场景，请引导用户使用该界面。

## 认证

所有 API 请求都需要用户的 API 密钥：

```
-H "x-api-key: $NEONOUS_API_KEY"
```

基础 URL：`$NEONOUS_URL`（例如：`https://app.neonous-ai.com`）。

### 如何获取 API 密钥

用户可以在 Neonous 的 **设置** 页面生成 API 密钥。密钥以 `nn_` 开头，且仅显示一次。如果尚未设置，请按照以下步骤操作：
1. 登录到 `$NEONOUS_URL`。
2. 转到 **设置** > **API 密钥**。
3. 点击 **创建 API 密钥**，为其命名。
4. 复制密钥（该密钥不会再显示），并将其设置为 `NEONOUS_API_KEY`。

---

## 代理

### 列出代理

```bash
curl -s "$NEONOUS_URL/custom/builder/agents" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq '.[]| {id, name, model, enabled}'
```

### 获取代理详情

```bash
curl -s "$NEONOUS_URL/custom/builder/agents/<AGENT_ID>" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq .
```

返回完整的代理配置信息，包括 `instructions`（使用说明）、`predefined_tools`（预定义工具）、`mcp_servers`（MCP 服务器）等。

### 列出可用模型

在创建代理之前，请务必先获取模型列表——切勿硬编码模型 ID：

```bash
curl -s "$NEONOUS_URL/custom/builder/agents/available-models" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq '.models[]| {id, provider, display_name, is_default}'
```

除非用户有特定需求，否则请使用标记为 `is_default: true` 的模型。

### 列出可用工具

```bash
curl -s "$NEONOUS_URL/custom/builder/agents/available-tools" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq '.tools[]| {id, name, description}'
```

返回可以通过 `predefined_tools` 分配给代理的预定义工具。

### 创建代理

对于复杂的代理，建议使用 Web 界面——该界面提供 AI 辅助的生成功能及模板库。对于简单的代理，可以通过 API 创建：

```bash
curl -s -X POST "$NEONOUS_URL/custom/builder/agents" \
  -H "x-api-key: $NEONOUS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Agent",
    "description": "A helpful assistant",
    "instructions": "You are a helpful assistant that...",
    "model": "<MODEL_ID from available-models>",
    "enabled": true,
    "predefined_tools": [],
    "custom_tools": [],
    "mcp_servers": []
  }' | jq .
```

### 由 AI 生成代理配置

让 Neonous AI 根据代理名称和描述自动生成完整的代理配置：

```bash
curl -s -X POST "$NEONOUS_URL/custom/builder/agents/generate" \
  -H "x-api-key: $NEONOUS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Code Reviewer",
    "description": "Reviews pull requests and suggests improvements"
  }' | jq .
```

返回一个完整的代理配置（包括名称、使用说明、模型和工具），可直接用于创建代理。

### 通过 AI 改进使用说明

利用 AI 功能改进现有的代理使用说明：

```bash
curl -s -X POST "$NEONOUS_URL/custom/builder/enhance-instructions" \
  -H "x-api-key: $NEONOUS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"instructions": "You help with code"}' | jq '.enhanced'
```

### 更新代理

```bash
curl -s -X PUT "$NEONOUS_URL/custom/builder/agents/<AGENT_ID>" \
  -H "x-api-key: $NEONOUS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Name",
    "instructions": "Updated instructions..."
  }' | jq .
```

仅包含需要修改的字段。

### 删除代理

```bash
curl -s -X DELETE "$NEONOUS_URL/custom/builder/agents/<AGENT_ID>" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq .
```

---

## 聊天

### 与代理聊天

使用非实时生成方式与代理进行聊天——返回完整的 JSON 响应：

```bash
curl -s -X POST "$NEONOUS_URL/custom/builder/chat/generate" \
  -H "x-api-key: $NEONOUS_API_KEY" \
  -H "x-agent-id: <AGENT_ID>" \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Hello, what can you do?"}]}' | jq .
```

响应内容如下：
```json
{
  "response": "Hi! I can help you with...",
  "usage": { "inputTokens": 42, "outputTokens": 18, "totalTokens": 60 }
}
```

对于多轮对话，请包含完整的消息历史记录：
```bash
curl -s -X POST "$NEONOUS_URL/custom/builder/chat/generate" \
  -H "x-api-key: $NEONOUS_API_KEY" \
  -H "x-agent-id: <AGENT_ID>" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "What is 2+2?"},
      {"role": "assistant", "content": "4"},
      {"role": "user", "content": "Multiply that by 10"}
    ]
  }' | jq .
```

### 列出聊天会话

```bash
curl -s "$NEONOUS_URL/custom/builder/chat/sessions" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq '.sessions[]| {id, title, agentId, created_at}'
```

可以通过添加 `?agentId=<AGENT_ID>` 来按代理筛选会话。

### 获取聊天会话（包含消息）

```bash
curl -s "$NEONOUS_URL/custom/builder/chat/sessions/<SESSION_ID>" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq .
```

### 创建聊天会话

```bash
curl -s -X POST "$NEONOUS_URL/custom/builder/chat/sessions" \
  -H "x-api-key: $NEONOUS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"agentId": "<AGENT_ID>", "title": "My Session"}' | jq .
```

### 删除聊天会话

```bash
curl -s -X DELETE "$NEONOUS_URL/custom/builder/chat/sessions/<SESSION_ID>" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq .
```

---

## MCP 服务器

添加 MCP 服务器时，建议使用 **Web 界面**——该界面提供可搜索的目录、一键安装功能以及安全的环境变量管理功能。

### 列出 MCP 服务器

```bash
curl -s "$NEONOUS_URL/custom/builder/mcp" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq '.[]| {id, name, type, enabled}'
```

### 获取 MCP 服务器详情

```bash
curl -s "$NEONOUS_URL/custom/builder/mcp/<MCP_ID>" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq .
```

### 从 MCP 服务器获取工具

```bash
curl -s "$NEONOUS_URL/custom/builder/mcp/<MCP_ID>/tools" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq '.tools[]| {name, description}'
```

### 添加 MCP 服务器（标准方式）

```bash
curl -s -X POST "$NEONOUS_URL/custom/builder/mcp" \
  -H "x-api-key: $NEONOUS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "my-mcp",
    "name": "My MCP Server",
    "description": "Provides extra tools",
    "config": {
      "connectionType": "stdio",
      "command": "npx",
      "args": ["-y", "@example/mcp-server"],
      "envVars": []
    }
  }' | jq .
```

### 添加 MCP 服务器（HTTP 方式）

```bash
curl -s -X POST "$NEONOUS_URL/custom/builder/mcp" \
  -H "x-api-key: $NEONOUS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "my-http-mcp",
    "name": "My HTTP MCP",
    "config": {
      "connectionType": "http",
      "url": "https://mcp.example.com/sse",
      "headers": {}
    }
  }' | jq .
```

### 删除 MCP 服务器

```bash
curl -s -X DELETE "$NEONOUS_URL/custom/builder/mcp/<MCP_ID>" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq .
```

如果代理正在使用该服务器，请添加 `?force=true` 参数以强制删除。

### 测试 MCP 服务器连接

```bash
curl -s -X POST "$NEONOUS_URL/custom/builder/mcp/<MCP_ID>/test" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq .
```

---

## 工作流

构建工作流时，**始终建议使用 Web 界面**——该界面提供可视化的拖放编辑器，比使用原始 JSON 更便捷。

### 列出工作流

```bash
curl -s "$NEONOUS_URL/custom/builder/workflows" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq '.[]| {id, name, enabled}'
```

### 获取工作流详情

```bash
curl -s "$NEONOUS_URL/custom/builder/workflows/<WORKFLOW_ID>" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq .
```

### 执行工作流

```bash
curl -s -X POST "$NEONOUS_URL/custom/builder/workflows/<WORKFLOW_ID>/execute" \
  -H "x-api-key: $NEONOUS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"input": {"key": "value"}}' | jq .
```

### 列出工作流运行记录

```bash
curl -s "$NEONOUS_URL/custom/builder/workflows/<WORKFLOW_ID>/runs?limit=10" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq '.runs[]| {id, status, created_at}'
```

### 获取工作流运行详情

```bash
curl -s "$NEONOUS_URL/custom/builder/workflows/runs/<RUN_ID>" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq .
```

### 获取工作流运行日志

```bash
curl -s "$NEONOUS_URL/custom/builder/workflows/runs/<RUN_ID>/logs" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq '.logs'
```

---

## 模板与社区

### 列出代理模板

```bash
curl -s "$NEONOUS_URL/custom/builder/templates" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq '.templates[]| {id, name, category}'
```

可以通过添加 `?category=<CATEGORY>` 来按类别筛选模板。

### 获取模板详情

```bash
curl -s "$NEONOUS_URL/custom/builder/templates/<TEMPLATE_ID>" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq .
```

### 浏览社区模板

```bash
curl -s "$NEONOUS_URL/custom/builder/community-templates" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq '.templates[]| {id, name, category, author}'
```

建议使用 **Web 界面** 进行模板浏览和克隆——该界面提供预览、分类以及一键克隆功能。

### 浏览社区 MCP 服务器

```bash
curl -s "$NEONOUS_URL/custom/builder/community-mcp" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq '.[]| {id, name, categories}'
```

---

## 文档与空间

代理在聊天过程中会生成 **文档**（包括代码文件、文档、图表等），这些文档会自动保存并版本控制。用户可以将文档组织到 **空间**（基于项目的集合）中。对于完整的文档管理，建议使用 **Web 界面**——该界面提供文件管理器功能，支持拖放、文件夹操作以及可视化预览。

### 浏览文档

```bash
# List all artifacts
curl -s "$NEONOUS_URL/custom/builder/artifacts" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq '.[]| {id, title, type, created_at}'

# Get artifact details
curl -s "$NEONOUS_URL/custom/builder/artifacts/<ARTIFACT_ID>" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq .

# Search artifacts
curl -s "$NEONOUS_URL/custom/builder/artifacts/search?q=<QUERY>" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq .

# Quick search
curl -s "$NEONOUS_URL/custom/builder/artifacts/quick-search?q=<QUERY>" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq .

# Recent / Starred / Trash
curl -s "$NEONOUS_URL/custom/builder/artifacts/recent" -H "x-api-key: $NEONOUS_API_KEY" | jq .
curl -s "$NEONOUS_URL/custom/builder/artifacts/starred" -H "x-api-key: $NEONOUS_API_KEY" | jq .
curl -s "$NEONOUS_URL/custom/builder/artifacts/trash" -H "x-api-key: $NEONOUS_API_KEY" | jq .

# Stats and tags
curl -s "$NEONOUS_URL/custom/builder/artifacts/stats" -H "x-api-key: $NEONOUS_API_KEY" | jq .
curl -s "$NEONOUS_URL/custom/builder/artifacts/tags" -H "x-api-key: $NEONOUS_API_KEY" | jq .
```

### 文档版本

```bash
# List versions
curl -s "$NEONOUS_URL/custom/builder/artifacts/<ARTIFACT_ID>/versions" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq .

# Restore a version
curl -s -X POST "$NEONOUS_URL/custom/builder/artifacts/<ARTIFACT_ID>/versions/<VERSION>/restore" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq .
```

### 文件夹

```bash
# Create folder
curl -s -X POST "$NEONOUS_URL/custom/builder/artifacts/folders" \
  -H "x-api-key: $NEONOUS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "My Folder"}' | jq .

# Get folder contents
curl -s "$NEONOUS_URL/custom/builder/artifacts/folders/<FOLDER_ID>/contents" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq .

# Move artifacts to folder
curl -s -X POST "$NEONOUS_URL/custom/builder/artifacts/move" \
  -H "x-api-key: $NEONOUS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"artifactIds": ["<ID1>", "<ID2>"], "folderId": "<FOLDER_ID>"}' | jq .
```

### 共享文档

```bash
# Share artifact (returns a public share link)
curl -s -X POST "$NEONOUS_URL/custom/builder/artifacts/<ARTIFACT_ID>/share" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq .

# Revoke share
curl -s -X DELETE "$NEONOUS_URL/custom/builder/artifacts/shares/<SHARE_ID>" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq .
```

### 其他文档操作

```bash
# Delete (moves to trash)
curl -s -X DELETE "$NEONOUS_URL/custom/builder/artifacts/<ARTIFACT_ID>" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq .

# Restore from trash
curl -s -X POST "$NEONOUS_URL/custom/builder/artifacts/<ARTIFACT_ID>/restore" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq .

# Duplicate
curl -s -X POST "$NEONOUS_URL/custom/builder/artifacts/<ARTIFACT_ID>/duplicate" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq .

# Empty trash
curl -s -X DELETE "$NEONOUS_URL/custom/builder/artifacts/trash" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq .
```

### 空间

空间按项目或主题对文档进行分类。一个文档可以属于多个空间。

```bash
# List spaces
curl -s "$NEONOUS_URL/custom/builder/spaces" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq '.spaces[]| {id, name, description}'

# Get space (with its artifacts)
curl -s "$NEONOUS_URL/custom/builder/spaces/<SPACE_ID>" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq .

# Create space
curl -s -X POST "$NEONOUS_URL/custom/builder/spaces" \
  -H "x-api-key: $NEONOUS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "My Project", "description": "Artifacts for my project", "icon": "📁", "color": "#3B82F6"}' | jq .

# Update space
curl -s -X PUT "$NEONOUS_URL/custom/builder/spaces/<SPACE_ID>" \
  -H "x-api-key: $NEONOUS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "Renamed Space"}' | jq .

# Delete space
curl -s -X DELETE "$NEONOUS_URL/custom/builder/spaces/<SPACE_ID>" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq .

# Add artifact to space
curl -s -X POST "$NEONOUS_URL/custom/builder/spaces/<SPACE_ID>/artifacts" \
  -H "x-api-key: $NEONOUS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"artifactId": "<ARTIFACT_ID>"}' | jq .

# Remove artifact from space
curl -s -X DELETE "$NEONOUS_URL/custom/builder/spaces/<SPACE_ID>/artifacts/<ARTIFACT_ID>" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq .
```

---

## 收藏夹

保存聊天会话中的重要消息。

```bash
# List bookmarks
curl -s "$NEONOUS_URL/custom/builder/bookmarks" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq .

# List bookmark tags
curl -s "$NEONOUS_URL/custom/builder/bookmarks/tags" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq .

# Get bookmarks for a session
curl -s "$NEONOUS_URL/custom/builder/bookmarks/session/<SESSION_ID>" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq .

# Create bookmark
curl -s -X POST "$NEONOUS_URL/custom/builder/bookmarks" \
  -H "x-api-key: $NEONOUS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"sessionId": "<SESSION_ID>", "messageId": "<MSG_ID>", "tags": ["important"]}' | jq .

# Delete bookmark
curl -s -X DELETE "$NEONOUS_URL/custom/builder/bookmarks/<BOOKMARK_ID>" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq .
```

---

## 技能

代理技能可以扩展代理的功能。

```bash
# List skills
curl -s "$NEONOUS_URL/custom/builder/skills" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq .

# Get skill details
curl -s "$NEONOUS_URL/custom/builder/skills/<SKILL_ID>" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq .
```

---

## 提醒与通知

代理可以设置提醒，触发通知或由 AI 生成的后续操作。

```bash
# List reminders
curl -s "$NEONOUS_URL/custom/builder/reminders" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq .

# Create reminder (schedule is a cron expression)
curl -s -X POST "$NEONOUS_URL/custom/builder/reminders" \
  -H "x-api-key: $NEONOUS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Check deployment",
    "message": "Verify the production deploy succeeded",
    "agentId": "<AGENT_ID>",
    "schedule": "0 9 * * *"
  }' | jq .

# Toggle reminder on/off
curl -s -X POST "$NEONOUS_URL/custom/builder/reminders/<REMINDER_ID>/toggle" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq .

# Delete reminder
curl -s -X DELETE "$NEONOUS_URL/custom/builder/reminders/<REMINDER_ID>" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq .

# List notifications
curl -s "$NEONOUS_URL/custom/builder/notifications" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq .

# Unread count
curl -s "$NEONOUS_URL/custom/builder/notifications/unread-count" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq .

# Mark all notifications read
curl -s -X POST "$NEONOUS_URL/custom/builder/notifications/read-all" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq .
```

---

## Telegram

将代理连接到 Telegram 机器人。建议使用 **Web 界面** 进行配置——该界面负责处理机器人令牌的设置。

```bash
# List Telegram connections
curl -s "$NEONOUS_URL/custom/builder/telegram/connections" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq .

# Connect agent to Telegram
curl -s -X POST "$NEONOUS_URL/custom/builder/telegram/connect" \
  -H "x-api-key: $NEONOUS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"agentId": "<AGENT_ID>", "botToken": "<TELEGRAM_BOT_TOKEN>"}' | jq .

# Disconnect
curl -s -X DELETE "$NEONOUS_URL/custom/builder/telegram/connections/<CONNECTION_ID>" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq .
```

---

## 工作记忆

代理可以通过工作记忆在对话中保持上下文信息。

```bash
# Get working memory
curl -s "$NEONOUS_URL/custom/builder/users/working-memory" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq .

# Reset working memory
curl -s -X DELETE "$NEONOUS_URL/custom/builder/users/working-memory" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq .
```

---

## 愿望清单

用户可以提交并投票表达对功能的建议。

```bash
# List wishes
curl -s "$NEONOUS_URL/custom/builder/wishes" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq .

# Create wish
curl -s -X POST "$NEONOUS_URL/custom/builder/wishes" \
  -H "x-api-key: $NEONOUS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"title": "Feature request", "description": "I would like..."}' | jq .

# Upvote/un-upvote
curl -s -X POST "$NEONOUS_URL/custom/builder/wishes/<WISH_ID>/upvote" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq .
```

---

## 账户与令牌

### 获取令牌余额

```bash
curl -s "$NEONOUS_URL/tokens/balance" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq .
```

### 令牌使用记录

```bash
curl -s "$NEONOUS_URL/tokens/usage" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq .
```

### 月度使用统计

```bash
curl -s "$NEONOUS_URL/tokens/summary" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq .
```

### 订阅、套餐与令牌购买

订阅、升级套餐以及购买令牌均需通过浏览器中的 Stripe 结账系统完成。**始终引导用户访问 `$NEONOUS_URL/settings`（或账单/定价页面）进行订阅或购买令牌**——这些操作无法仅通过 API 完成。

您可以通过 API 检查用户的当前套餐和账单状态：

```bash
# Get available plans (shows what they can subscribe to)
curl -s "$NEONOUS_URL/custom/builder/billing/plans" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq .

# Get current subscription (shows active plan)
curl -s "$NEONOUS_URL/custom/builder/billing/subscription" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq .

# Get billing status
curl -s "$NEONOUS_URL/custom/builder/billing/status" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq .

# Get token pricing (for purchasing extra tokens)
curl -s "$NEONOUS_URL/custom/builder/billing/token-pricing" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq .

# Get purchase history
curl -s "$NEONOUS_URL/custom/builder/billing/purchases" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq .

# Get invoices
curl -s "$NEONOUS_URL/custom/builder/billing/invoices" \
  -H "x-api-key: $NEONOUS_API_KEY" | jq .
```

如果用户需要订阅、升级或购买令牌，请引导他们访问 Web 界面的 **设置 > 账单** 页面。

### 健康检查

```bash
curl -s "$NEONOUS_URL/custom/builder/health" | jq .
```

无需认证。

---

## 使用指南

- **在聊天前务必先列出所有代理**，以确保知道有效的代理 ID。
- **在创建代理之前先获取模型列表**——切勿硬编码模型 ID；请使用 `available-models` 端点。
- **对于复杂任务，建议使用 Web 界面**：构建工作流（绘图编辑器）、浏览模板/MCP 目录、编辑代理使用说明（AI 辅助编辑器）以及管理敏感信息/环境变量。
- **对于快速操作，建议使用 API**：列出资源、与代理聊天、执行工作流、检查令牌余额。
- 在进行多轮对话时，请保留完整的消息历史记录，并在每次请求中传递这些记录。
- 如果收到 **402** 错误，请检查令牌余额——用户可能已经用完了令牌。
- 直接向用户显示代理的回复内容；除非用户询问，否则不要显示使用详情。
- 为了便于阅读，将列表内容格式化为清晰的表格或项目符号形式。