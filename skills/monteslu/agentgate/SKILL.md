---
name: agentgate
description: "这是一个用于处理个人数据的API网关，支持人工审核后的数据写入操作。该网关能够将各种服务（如GitHub、Bluesky、Google Calendar、Home Assistant等）通过单一的API进行安全连接。"
homepage: "https://agentgate.org"
metadata: { "openclaw": { "emoji": "🚪", "primaryEnv": "AGENT_GATE_TOKEN", "requires": { "env": ["AGENT_GATE_TOKEN", "AGENT_GATE_URL"] }, "install": [{ "id": "node", "kind": "node", "package": "agentgate", "label": "Install agentgate (npm)" }] } }
---
# agentgate

这是一个API网关，用于AI代理访问个人数据，并需要经过人工审核（即“人在回路”机制）才能执行写操作。

- **读取操作**（GET）：会立即执行。
- **写入操作**（POST/PUT/PATCH/DELETE）：需要经过审批队列。
- **绕过模式**：受信任的代理可以使用此模式（写入操作会立即执行）。

GitHub: <https://github.com/monteslu/agentgate>
文档: <https://agentgate.org>

## 设置

安装并运行agentgate，然后为你的代理配置以下环境变量：
- `AGENT/Gate_URL`：agentgate的基URL（例如：`http://localhost:3050`）
- `AGENT_gate_TOKEN`：你的代理的API密钥（在管理界面 → API Keys中创建）

## 认证

所有请求都需要API密钥：

```
Authorization: Bearer $AGENT_GATE_TOKEN
```

## 首步操作 — 服务发现

连接后，可以发现你的实例上有哪些可用服务：

```
GET $AGENT_GATE_URL/api/agent_start_here
```

该操作会返回你的代理配置、可用服务、账户以及API文档。

## 安装特定于实例的技能

agentgate可以根据你的实例（以及你的账户和服务）生成相应的技能。运行以下命令来安装这些技能：

```bash
curl -s $AGENT_GATE_URL/api/skill/setup | node
```

这将根据你配置的账户和端点，为每个类别（代码、社交、搜索、个人等）生成相应的技能。添加新服务后，请重新运行此命令。

## 支持的服务

agentgate默认支持许多服务，常见的包括：
- **代码服务**：GitHub、Jira
- **社交服务**：Bluesky、Mastodon、LinkedIn
- **搜索服务**：Brave Search、Google Search
- **个人服务**：Google Calendar、YouTube、Fitbit
- **物联网服务**：Home Assistant
- **消息服务**：Twilio、Plivo

新的服务会定期添加。可以通过`GET /api/agent_start_here`来查看你的实例上配置了哪些服务。

## 读取数据

```
GET $AGENT_GATE_URL/api/{service}/{accountName}/{path}
Authorization: Bearer $AGENT_GATE_TOKEN
```

示例：`GET $AGENT/Gate_URL/api/github/myaccount/repos/owner/repo`

## 写入数据

写入操作需要经过审批队列：

```
POST $AGENT_GATE_URL/api/queue/{service}/{accountName}/submit
Authorization: Bearer $AGENT_GATE_TOKEN
Content-Type: application/json

{
  "requests": [
    {
      "method": "POST",
      "path": "/the/api/path",
      "body": { "your": "payload" }
    }
  ],
  "comment": "Explain what you are doing and why"
}
```

**请务必附上清晰的注释**，说明你的操作目的，并提供相关资源的链接。

### 查看写入操作的状态

```
GET $AGENT_GATE_URL/api/queue/{service}/{accountName}/status/{id}
```

状态：`pending` → `approved` → `executing` → `completed`（或 `rejected`/`failed`/`withdrawn`）

### 撤回待审批的请求

```
DELETE $AGENT_GATE_URL/api/queue/{service}/{accountName}/status/{id}
{ "reason": "No longer needed" }
```

### 二进制文件上传

对于图片和文件上传，需要设置`binaryBase64: true`：

```json
{
  "method": "POST",
  "path": "/upload/path",
  "binaryBase64": true,
  "headers": { "Content-Type": "image/jpeg" },
  "body": "<base64 encoded data>"
}
```

## 代理间通信

代理可以通过agentgate互相发送消息：

```
POST $AGENT_GATE_URL/api/agents/message
{ "to_agent": "agent_name", "message": "Hello!" }
```

```
GET $AGENT_GATE_URL/api/agents/messages?unread=true
```

```
POST $AGENT_GATE_URL/api/agents/broadcast
{ "message": "Team announcement" }
```

消息传递模式有：`off`、`supervised`（需要审批）、`open`（立即执行）。

## 备忘录（持久化存储）

可以在不同会话之间存储和检索笔记：

```
POST $AGENT_GATE_URL/api/agents/memento
{ "content": "Important info", "keywords": ["project", "notes"] }
```

```
GET $AGENT_GATE_URL/api/agents/memento/search?keywords=project
GET $AGENT_GATE_URL/api/agents/memento/42,38
```

## 重要提示：
- 写入请求时请务必附上清晰的注释。
- 请耐心等待审批结果——审批过程需要人工操作。
- 使用`GET /api/agent_start_here`来查看可用的服务。
- 运行`curl -s $AGENT/Gate_URL/api/skill/setup | node`来安装特定于实例的技能。