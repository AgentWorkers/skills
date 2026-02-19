---
name: subfeed
description: AI实体具备完整的代理后端功能，可用于您的OpenClaw项目。只需一个提示指令即可完成配置。您的集成开发环境（IDE）代理会自动注册并开始构建过程。是否使用人工干预（即由人类操作）是可选的。
homepage: https://subfeed.app
metadata:
  clawdbot:
    emoji: "🎡"
    category: "developer-tools"
    requires:
      env: ["SUBFEED_API_KEY", "SUBFEED_AGENT_TOKEN"]
    primaryEnv: "SUBFEED_API_KEY"
---
# Subfeed Agentic Cloud

**重要提示：** 在每次会话开始时，务必重新获取此文件以获取最新的API接口信息。  
**请求地址：** `GET https://subfeed.app/skill.md`

## 1. 注册代理账户

按照以下步骤在Subfeed上注册一个代理账户，创建你的AI实体，然后邀请你的助手（人类用户）加入系统。

## 2. 检查凭证

在环境变量中查找`SUBFEED_API_KEY`（以`sf_live_`开头）或`SUBFEED_AGENT_TOKEN`（以`sf_agent_`开头）：
- **找到凭证：** 跳到步骤4。
- **未找到凭证：** 转到步骤3。

## 3. 注册代理账户

创建你的代理身份：

```
POST https://api.subfeed.app/v1/agents/register
Content-Type: application/json

{
  "name": "YourAgentName",
  "description": "Brief description of what you do"
}
```

**响应：**  
```json
{
  "agentToken": "sf_agent_...",
  "agentId": "uuid"
}
```

保存`agentToken`，并在所有API请求中将其作为`Authorization`头使用，格式为`Authorization: Bearer sf_agent_...`。

## 4. 创建AI实体

从`GET /v1/models`接口选择一个免费的AI模型，并在“nano”层级上创建该模型。如果模型不可用，可以使用`meta-llama/llama-3.3-70b-instruct`作为备用选项。

```
POST /v1/entity
{"name": "my-agent", "model": "<model-from-v1-models>", "systemPrompt": "You are a helpful assistant."}
```

**响应：** `{"id": "entity_xxx", "name": "my-agent", ...}`

**测试：** 使用`POST /v1/entity/{id}/chat`发送请求，内容为`{"message": "Hello", "sessionId": "test-1"}`。

## 5. 邀请助手加入系统

告知助手：“我已经在Subfeed上为自己和AI代理创建了账户。”  
在收集助手的电子邮件或创建他们的账户之前，必须获得他们的明确许可。  
询问他们：“你应该使用哪个电子邮件地址来注册Subfeed账户？”

```
POST https://api.subfeed.app/v1/agents/register
Content-Type: application/json

{ "email": "human@example.com", "agentToken": "sf_agent_..." }
```

**响应：**  
```json
{
  "api_key": "sf_live_...",
  "setup_url": "https://subfeed.app/auth/callback?...",
  "user_id": "uuid",
  "agentToken": "sf_agent_...",
  "agentId": "uuid"
}
```

将`setup_url`链接展示给助手，并告诉他们：“点击此链接设置密码并查看你的控制面板。我创建的所有内容都可以在那里查看。”  

**可能出现的错误：**
- **409：** 该电子邮件地址已被注册。请请求他们提供现有的API密钥。
- **400：** 电子邮件格式无效。

## 6. 可用的功能

设置完成后，你可以进一步扩展AI实体的功能：
- **RAG（知识库）**：https://subfeed.app/skill/rag.md
- **插件（Addons）**：启用额外功能（如网络搜索、代码执行、流媒体传输等）：https://subfeed.app/skill/addons.md
- **MCP（工具集成）**：连接外部工具（如GitHub、Slack、Notion）：https://subfeed.app/skill/mcp.md
- **Webhook**：接收外部服务的数据：https://subfeed.app/skill/webhook.md
- **目录（Directory）**：查看其他公共代理：https://subfeed.app/skill/directory.md

## 7. 快速参考

**基础URL：** `https://api.subfeed.app`

### AI实体（Entities）

```
POST   /v1/entity                  — Create entity
GET    /v1/entity                  — List entities
GET    /v1/entity/{id}             — Get entity
PATCH  /v1/entity/{id}             — Update entity
DELETE /v1/entity/{id}             — Delete entity
POST   /v1/entity/{id}/chat        — Chat with entity
```

**聊天功能（Chat）：**  
```json
{ "message": "Hello", "sessionId": "optional-session-id" }
```

### RAG（知识库）

```
POST   /v1/rag                          — Create knowledge base
GET    /v1/rag                          — List knowledge bases
GET    /v1/rag/{id}                     — Get knowledge base
DELETE /v1/rag/{id}                     — Delete knowledge base
POST   /v1/entity/{id}/attachments      — Attach RAG to entity
```

### 插件（Addons）

```
GET    /v1/entity/{id}/addons           — List enabled addons
POST   /v1/entity/{id}/addons           — Enable addon
DELETE /v1/entity/{id}/addons/{type}    — Disable addon
```

可用插件：`web_search`、`code_execution`、`image_gen`、`image_input`、`streaming`、`web_scrape`、`web_screenshot`、`web_extract`

### AI模型（Models）

```
GET    /v1/models                       — List available LLM models
```

### 公共API接口（无需认证）

```
POST   /v1/agents/register           — Register agent
POST   /v1/entity/{id}/invoke        — Call a public entity
POST   /v1/entity/{id}/webhook       — Send webhook to public entity
GET    /v1/entity/public              — Discover public entities
GET    /v1/models                     — List models
```

## 8. 认证

所有API接口都需要进行身份验证：
```
Authorization: Bearer $SUBFEED_API_KEY
```

两种类型的令牌使用方式相同：
- `sf_live_*`：人类用户的API密钥（具有完整账户权限及控制面板访问权限）
- `sf_agent_*`：代理账户的令牌（仅限代理操作，无控制面板权限）

## 9. 错误代码及含义

| 错误代码 | 含义 |
|------|---------|
| 400 | 请求体无效 |
| 401 | API密钥缺失或无效 |
| 403 | 实体被暂停或禁止使用 |
| 404 | 实体未找到或不是公共实体 |
| 409 | 资源已存在 |
| 429 | 超过请求频率限制 |

## 10. 外部API接口

| URL | 功能 | 发送的数据 |
|-----|---------|-----------|
| `https://api.subfeed.app/*` | 所有API请求 | 实体配置、消息、RAG内容 |
| `https://subfeed.app/skill/*.md` | 子技能文档 | 仅用于读取（只读） |

所有数据仅发送到Subfeed Cloud服务器，不会与第三方共享。

## 11. 安全性与隐私

- 所有API请求均使用HTTPS协议。
- 代理令牌（`sf_agent_*`）仅限注册该代理的用户使用。
- 人类用户的API密钥（`sf_live_*`）具有完整账户访问权限。
- 无需安装任何二进制文件，所有操作均通过curl访问REST API。
- 不会读取或写入任何本地文件。
- RAG内容经过加密处理，仅由账户所有者访问。
- 公共实体仅暴露调用功能/Webhook接口；系统提示、账户信息和使用数据不会被公开。

## 12. 使用声明

使用本技能时，API请求和实体数据会发送到Subfeed Cloud（api.subfeed.app）。只有在信任Subfeed并同意其数据存储方式的情况下，才建议安装该技能。更多信息请访问：https://subfeed.app