# OpenClaw 集成 API

OpenClaw 是一个基于技能的集成系统，它允许基于 MakeX 构建的应用程序通过 Composio 发现并执行来自第三方服务（如 Gmail、Slack、GitHub 等）的操作。

## 认证

所有端点都需要包含 `X-Org-Token` 标头的请求，该头部包含组织的服务令牌。此令牌会与组织数据库进行验证。系统不使用用户会话 cookie——这些端点专为服务器之间的通信而设计。

```
X-Org-Token: <org-service-token>
```

**没有组织令牌？**

1. 访问 [https://www.makex.app/](https://www.makex.app/) 并注册一个账户。
2. 在您的仪表板中导航到 **设置**。
3. 从设置页面复制您的 API 密钥——这就是您的 `X-Org-Token`。

## 基本 URL

```
POST /api/openclaw/integrations/<endpoint>
```

所有端点都支持通过预检 `OPTIONS` 处理程序来实现 CORS（跨源资源共享）。

## 端点

### 1. 搜索操作

**POST** `/api/openclaw/integrations/search-actions`

在一个或多个集成中搜索可用的操作/工具。

**请求体：**
```json
{
  "integrations": ["gmail", "slack", "github"],
  "toolkit": "gmail",
  "search": "send"
}
```

- `integrations`（必填）：要搜索的集成名称数组。
- `toolkit`（可选）：如果提供，将覆盖 `integrations`，仅搜索该工具包中的操作。
- `search`（可选）：按关键词过滤操作。

**响应（200）：**
```json
{
  "total": 12,
  "actions": {
    "gmail": [
      { "slug": "GMAIL_SEND_EMAIL", "name": "Send Email" },
      { "slug": "GMAIL_CREATE_DRAFT", "name": "Create Draft" }
    ],
    "slack": [
      { "slug": "SLACK_SEND_MESSAGE", "name": "Send Message" }
    ]
  }
}
```

---

### 2. 已连接的账户

**POST** `/api/openclaw/integrations/connected-account`

检查特定集成是否已连接到组织，并检索账户详细信息。

**请求体：**
```json
{
  "integration": "gmail"
}
```

- `integration`（必填）：要检查的集成名称。

**响应（200）：**
```json
{
  "accountId": "conn_abc123",
  "userId": "org_xyz",
  "integration": "gmail",
  "status": "ACTIVE"
}
```

**响应（404）——未连接：**
```json
{
  "error": "No active connected account found for integration gmail",
  "availableIntegrations": ["slack", "github"]
}
```

---

### 3. 操作详情

**POST** `/api/openclaw/integrations/action-details`

获取特定操作的完整规范，包括其输入和输出参数。

**请求体：**
```json
{
  "action_slug": "GMAIL_SEND_EMAIL"
}
```

- `action_slug`（必填）：要获取的操作名称。

**响应（200）：**
```json
{
  "name": "Send Email",
  "slug": "GMAIL_SEND_EMAIL",
  "description": "Send an email via Gmail",
  "inputParameters": {
    "to": { "type": "string", "description": "Recipient email", "required": true },
    "subject": { "type": "string", "description": "Email subject" },
    "body": { "type": "string", "description": "Email body" }
  },
  "outputParameters": {
    "messageId": { "type": "string" },
    "threadId": { "type": "string" }
  }
}
```

---

### 4. 运行操作

**POST** `/api/openclaw/integrations/run-action`

在已连接的账户上执行特定操作。

**请求体：**
```json
{
  "toolName": "GMAIL_SEND_EMAIL",
  "accountId": "conn_abc123",
  "arguments": {
    "to": "user@example.com",
    "subject": "Hello",
    "body": "Hi there"
  }
}
```

- `toolName`（必填）：要执行的操作名称。
- `accountId`（必填）：已连接账户的 ID（来自 `connected-account` 端点）。
- `arguments`（可选）：操作的结构化键值参数。
- `text`（可选）：自然语言文本输入（如果未提供 `arguments` 时使用）。
- `version`（可选）：API 版本覆盖。
- `custom_auth_params`（可选）：自定义认证参数。
- `custom_connection_data`（可选）：自定义连接数据。
- `allow_tracing`（可选）：启用操作的跟踪功能。

**响应（200）**：Composio 的原始执行响应（因操作而异）。

---

### 5. 输出结构

**POST** `/api/openclaw/integrations/output-structure`

执行操作并返回其输出结构。这有助于确定操作响应的格式。

**请求体：**
```json
{
  "action_slug": "GMAIL_SEND_EMAIL",
  "accountId": "conn_abc123",
  "arguments": {
    "to": "test@example.com",
    "subject": "Test",
    "body": "Test body"
  }
}
```

- `action_slug`（必填）：要执行的操作名称。
- `accountId`（必填）：已连接账户的 ID。
- `arguments`（可选）：要传递给操作的参数。

**响应（200）：**
```json
{
  "successful": true,
  "data": { ... }
}
```

## 错误响应

所有端点都以一致的格式返回错误：

```json
{ "error": "Description of what went wrong" }
```

| 状态 | 含义 |
|--------|---------|
| 400 | 缺少必需参数 |
| 401 | 缺少或无效的 `X-Org-Token` |
| 404 | 资源未找到（例如，没有连接的账户） |
| 500 | 服务器错误或缺少 `COMPOSIO_API_KEY` |

## 典型工作流程

1. **搜索操作**，以发现已连接集成可用的操作。
2. **获取已连接的账户**，以获取特定集成的 `accountId`。
3. **获取操作详情**，以了解所选操作的输入/输出参数。
4. **运行操作**，使用所需的参数执行操作。