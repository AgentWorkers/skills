---
name: ogment
description: 通过 Ogment CLI 调用 MCP 工具——通过 Ogment 的治理层，安全地访问 Linear、Notion、Gmail、PostHog 以及 100 多种 SaaS 服务。
version: 1.0.5
metadata:
  openclaw:
    requires:
      bins:
        - ogment
      anyBins:
        - jq
      config:
        - "~/.config/ogment/credentials.json"
    install:
      - kind: node
        package: "@ogment-ai/cli"
        bins: [ogment]
      - kind: brew
        formula: jq
        bins: [jq]
    emoji: "🔌"
    homepage: https://ogment.ai
---
# Ogment CLI 技能

通过 Ogment CLI 安全地调用 MCP 工具。通过 Ogment 的管理层访问您已连接的 SaaS 工具（如 Linear、Notion、Gmail、PostHog 等）。

## 快速入门（首次使用）

**首次使用 Ogment 时，请按照以下步骤操作：**

### 第 1 步：检查认证状态
```bash
ogment auth status
```
- 如果 `loggedIn: true` → 跳到第 3 步
- 如果 `loggedIn: false` → 继续执行第 2 步

### 第 2 步：登录（如需要）
```bash
ogment auth login
```
从响应中提取代码，并**发送给相关人员**。

⚠️ **确保链接可点击！** 使用 markdown 或完整的 URL，以便相关人员可以直接点击。

> **🔐 批准此代码以连接 Ogment：`XXXX-XXXX`**
> 👉 [dashboard.ogment.ai/cli/approve](https://dashboard.ogment.ai/cli/approve)

等待批准，然后使用 `ogment auth status` 进行验证。

### 第 3 步：查看可用工具
```bash
ogment catalog
```
对于每个服务器，执行以下操作：
```bash
ogment catalog <serverId> | jq '[.data.tools[].name]'
```

### 第 4 步：向相关人员汇总信息
告诉他们您发现了什么：

> **✅ 已成功连接到 Ogment！** 可以访问以下工具：
> - **Linear：** 28 个工具（问题、项目、团队、文档）
> - **Gmail：** 11 个工具（消息、线程、草稿）
> - **Notion：** 5 个工具（搜索、获取、评论）
> - **Slack：** 7 个工具（对话、用户）
>
> 您需要我帮忙做什么？

## 先决条件

| 需求 | 安装方式 | 是否必需 |
|-------------|---------|----------|
| `ogment` CLI | `npm install -g @ogment-ai/cli` | ✅ 是 |
| `jq` | `brew install jq` / `apt install jq` | 可选（用于过滤） |

## 首次设置（登录流程）

⚠️ **重要提示（对于代理人）：** 不要让相关人员直接运行 `ogment auth login` — 请您自己运行该命令，然后将生成的代码发送给他们！

### 第 1 步：检查是否已认证
```bash
ogment auth status
```
如果 `loggedIn: true`，则跳转到核心工作流程。

### 第 2 步：如果未登录，请开始登录流程
```bash
ogment auth login
```
该命令会返回包含设备代码的 JSON 数据。提取代码并发送给相关人员：

**示例输出：**
```json
{
  "data": {
    "event": "auth_login.pending",
    "verification": {
      "userCode": "ABCD-1234",
      "verificationUri": "https://dashboard.ogment.ai/cli/approve"
    }
  }
}
```

### 第 3 步：将代码发送给相关人员
告诉他们：
> **批准此代码：`ABCD-1234`**
> 👉 https://dashboard.ogment.ai/cli/approve

### 第 4 步：等待批准
`ogment auth login` 命令在获得批准后会自动完成。之后请进行验证：
```bash
ogment auth status
```

## 认证与凭据

- **凭据存放位置：`~/.config/ogment/credentials.json`
- **令牌管理：** Ogment 为所有连接的服务器处理 OAuth 认证
- **访问权限：** 权限取决于您在 [Ogment 仪表板](https://dashboard.ogment.ai) 中设置的权限
- **每个代理的权限：** 每个代理只能看到您明确授予的工具

此技能不会存储任何凭据 — 所有认证操作均由 Ogment CLI 管理。

## 使用场景

- 当用户请求与他们的连接服务进行交互（如问题、文档、邮件、分析数据）
- 当您需要调用需要认证/凭据的 MCP 工具时
- 当您需要了解用户可用的集成服务时

## 核心工作流程

```
status → catalog → catalog <server> → catalog <server> <tool> → invoke
```

### 1. 检查连接状态（如有疑问）
```bash
ogment status
```

返回认证状态、连接状态和可用服务器列表。通过 `summary.status` 检查系统是否正常运行。

### 2. 查看可用服务器
```bash
ogment catalog
```

返回包含 `serverId` 和 `toolCount` 的服务器列表。后续调用时可以使用 `serverId`。

### 3. 列出服务器上的工具
```bash
ogment catalog <serverId>
```

返回所有工具的名称和描述。根据描述找到所需的工具。

### 4. 查看工具的详细信息
```bash
ogment catalog <serverId> <toolName>
```

返回工具的 `inputSchema`，其中包含属性、类型、必填字段和描述。

### 5. 调用工具
```bash
ogment invoke <serverId>/<toolName> --input '<json>'
```

通过 `--input` 标志以 JSON 格式提供输入数据。

### 6. 调试错误
```bash
ogment invoke <serverId>/<toolName> --input '{}' --debug
```

使用 `--debug` 标志可以查看详细的 MCP 错误信息及字段级别的验证详情。

## 安全考虑

### 网络安全

- 所有 API 调用都通过 `dashboard.ogment.ai` 进行路由
- 与 SaaS API 之间没有直接连接
- 数据传输过程中使用 TLS 加密

### 权限模型

- 工具的访问权限在您的 Ogment 仪表板中按代理进行设置
- 代理只能看到您授予其访问权限的工具
- 根据代理的权限，某些写入操作可能会受到限制

## 输出格式

所有命令返回结构化的 JSON 数据：

```json
{
  "ok": true,
  "data": { ... },
  "error": null,
  "meta": { "command": "..." },
  "next_actions": [
    { "command": "...", "title": "...", "reason": "..." }
  ]
}
```

- **首先检查 `ok` 字段** — 表示操作是否成功
- **`next_actions` — 建议的后续操作命令
- **`error.category` — 错误类型（如 `validation`、`not_found`、`remote`、`auth`、`internal`）
- **`error.retryable` — 是否可以重试

## 常用操作模式

### 根据需求查找工具
```bash
ogment catalog <serverId> | jq '.data.tools[] | select(.name + .description | test("email"; "i"))'
```

### 列出分配给用户的 issue
```bash
ogment invoke openclaw/Linear_list_issues --input '{"assignee": "me"}'
```

### 在 Notion 中搜索
```bash
ogment invoke openclaw/Notion_notion-search --input '{"query": "quarterly review", "query_type": "internal"}'
```

### 获取 Gmail 消息
```bash
ogment invoke openclaw/gmail_listMessages --input '{"q": "is:unread", "maxResults": 10}'
```

## 错误处理

| 错误代码 | 含义 | 处理方式 |
|------------|---------|--------|
| `TOOL_NOT_FOUND` | 服务器/工具名称不存在 | 重新运行 `ogment catalog` 以查找 |
| `VALIDATION_INVALID_INPUT` | JSON 格式错误 | 检查 JSON 语法 |
| `TRANSPORT_REQUEST_FAILED` | 服务器拒绝请求 | 使用 `--debug` 标志并检查工具的 API 描述 |
| `AUTH_INVALID_CREDENTIALS` | API 密钥无效/过期 | 重新运行 `ogment auth login` |
| `HTTP_401` | 服务连接已过期 | 告知相关人员重新连接（详见下文） |
| `HTTP_502` | 服务器不可用 | 延迟后重试 |

## 处理连接过期

当收到类似以下内容的 `HTTP_401` 错误时：
> “您与 [服务] 的连接已过期。请重新连接...”

**告知相关人员（并提供可点击的链接）：**
> **⚠️ 您与 [服务] 的连接已过期。**
> 请在此处重新连接：[dashboard.ogment.ai](https://dashboard.ogment.ai)
> （前往“集成” → [服务] → “重新连接”）
>
> 请在连接成功后通知我，我会再次尝试！

## 处理权限问题

如果某个工具不可用（例如 `gmail_createDraft` 不存在于工具列表中）：
- **这是正常现象** — 代理的权限是有限制的
- 某些写入操作可能被默认禁用

**告知相关人员（并提供可点击的链接）：**
> **您没有对 [服务] 的写入权限。**
> 请前往：[dashboard.ogment.ai](https://dashboard.ogment.ai)
> （进入“代理” → “[代理名称]” → “权限设置”）
>
> 请在权限更新后告知我，我会再次尝试！

## 错误代码

| 代码 | 含义 |
|------|---------|
| 0 | 操作成功 |
| 2 | 验证/解析错误 |
| 5 | 未找到相关工具 |
| 7 | 远程/传输错误 |
| 9 | 内部错误 |

## 标志说明

| 标志 | 功能 |
|------|--------|
| `--debug` | 显示详细的错误诊断信息 |
| `--human` | 以人类可读的形式显示输出 |
| `--yes` | 自动确认操作 |
| `--api-key <key>` | 替换 API 密钥 |

**注意：** **避免使用 `--quiet` 标志**（该标志会抑制所有输出，包括错误信息）

## 使用前的检查事项

在调用工具之前，请确保：
1. 确保服务器存在（通过 `catalog` 检查）
2. 确保所需工具存在（通过 `catalog <服务器>` 检查）
3. 检查工具的字段是否满足要求
4. 确保 ID 的大小写格式正确
5. 使用正确的格式输入 ID