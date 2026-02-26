---
name: meegle-api-credentials
description: >
  获取 Meegle API 访问凭据：域名（domain）、令牌（token）、上下文信息（project_key、user_key）以及请求头（request headers）。  
  在尝试任何与 Meegle API 相关的操作之前，请先阅读本文档；所有 API 调用的前提条件都包含在本技能说明中。
metadata:
  openclaw: {}
  required_credentials:
    plugin_id:
      description: "Plugin ID from Meegle Developer Platform → Plugin → Basic Information"
      source: secret
    plugin_secret:
      description: "Plugin secret from Meegle Developer Platform → Plugin → Basic Information"
      source: secret
    domain:
      description: "API host: project.larksuite.com (international) or project.feishu.cn (China)"
      default: project.larksuite.com
    project_key:
      description: "Space identifier; in Meegle platform double-click the project icon to get it"
    user_key:
      description: "User identifier; in Meegle platform double-click the avatar to get it (or from user_access_token response)"
  optional_credentials:
    authorization_code:
      description: "OAuth code from getAuthCode(); required for user_access_token"
    refresh_token:
      description: "From user_plugin_token response; for refreshing user_access_token"
  context:
    project_key: "Space identifier; in Meegle platform double-click the project icon to get it"
    user_key: "User identifier; in Meegle platform double-click the avatar to get it (or from user_access_token response)"
---
# Meegle API — 凭据（域名、访问令牌、上下文、请求头）

本技能将生成用于调用 Meegle OpenAPI 的所需凭证，包括 **域名**、**访问令牌**（插件或用户专用）、**上下文信息**（`project_key`、`user_key`）以及 **请求头**。在调用其他 Meegle API 之前，请确保已获取所有这些凭证。

## 凭据缺失时的处理方式

当缺少必要的凭证（如 `user_key`、`project_key`、`plugin_id`、`plugin_secret`）时，**不要直接报告错误**。首先检查 [环境变量](#environment-variables)：如果这些变量已设置，则直接使用它们，无需再次询问用户。只有当环境变量中不存在相应凭证时，才需要采取以下措施：

1. **主动提醒** 用户缺少哪些凭证。
2. **告知用户获取凭证的途径**：

| 缺失的凭证 | 获取途径 |
|----------------|-----------------|
| `plugin_id` | Meegle 开发者平台 → 插件 → 基本信息 |
| `plugin_secret` | Meegle 开发者平台 → 插件 → 基本信息 |
| `project_key` | Meegle 平台：双击 **项目图标**；或从项目 URL 获取 |
| `user_key` | Meegle 平台：双击 **头像**；或从 `user_access_token` API 响应中的 `user_key` 字段获取 |

获取凭证后，请让用户重新尝试请求。**在询问用户之前**，务必先检查 [环境变量](#environment-variables)。

## 环境变量

为了避免每次请求时都要求用户输入凭证，建议将它们存储在环境变量中。OpenClaw（或代理程序）应优先读取环境变量中的值；如果环境变量中存在相应凭证，则直接使用，无需再次询问用户。用户只需配置一次（例如在 `.env`、`~/.zshrc` 或 OpenClaw 配置文件中）。

| 环境变量 | 用途 | 是否必填 |
|----------------------|---------|----------|
| `MEEGLE_PLUGIN_ID` | 插件 ID | 是 |
| `MEEGLE_PLUGIN_SECRET` | 插件密钥 | 是 |
| `MEEGLE_DOMAIN` | API 主机（例如 `project.larksuite.com` 或 `project.feishu.cn`） | 是（或使用默认值） |
| `MEEGLEPROJECT_KEY` | 项目标识符（`project_key`） | 是 |
| `MEEGLE_USER_KEY` | 用户标识符（`user_key`） | 是 |

**优先级处理顺序**：优先使用环境变量中的凭证，其次使用用户提供的凭证或配置文件中的默认值；切勿请求环境变量中已存在的凭证。

## 域名（API 主机）

在请求中，将 `{domain}` 替换为适用于您所在地区的实际 Meegle API 主机地址：

| 地区 | 域名 |
|--------|--------|
| **国际地区** | `project.larksuite.com` — 基础 URL：`https://project.larksuite.com` |
| **中国（Feishu 项目）** | `project.feishu.cn` — 基础 URL：`https://project.feishu.cn` |

**示例**：插件令牌的 URL 为 `https://{domain}/open_api/authen/plugin_token`，则国际地区使用 `https://project.larksuite.com/open_api/authen/plugin_token`，中国地区使用 `https://project.feishu.cn/open_api/authen/plugin_token`。

---

## 获取访问令牌

本技能用于生成 OpenClaw 调用 Meegle OpenAPI 所需的访问凭证。

### 使用场景

- 在调用任何 Meegle OpenAPI 之前
- 当 `plugin_access_token` 过期时（有效期为 2 小时）
- 当需要代表特定用户执行操作时

**可用的 API 功能**：

- `generate_plugin_token`：生成插件访问令牌（`plugin_access_token`）或虚拟插件令牌（`virtual_plugin_token`）
- `exchange_user_access_token`：将授权码转换为用户访问令牌（`user_access_token`）
- `refresh_user_access_token`：刷新过期的用户访问令牌

**API 规范：** `generate_access_token` （详细内容见 **```yaml
name: meegle.obtain_access_token
description: >
  Generate Meegle access credentials for OpenClaw to call OpenAPI.
  Supports plugin_access_token, virtual_plugin_token (dev),
  and user_access_token (on behalf of a user).

when_to_use:
  - Before calling any Meegle OpenAPI
  - When plugin_access_token expires (2 hours)
  - When an operation must be performed on behalf of a specific user

capabilities:
  - generate_plugin_token
  - generate_virtual_plugin_token
  - exchange_user_access_token
  - refresh_user_access_token

flows:

  generate_plugin_token:
    description: Obtain plugin_access_token or virtual_plugin_token
    http:
      method: POST
      path: /open_api/authen/plugin_token
    headers:
      Content-Type: application/json
    body:
      plugin_id:
        type: string
        required: true
      plugin_secret:
        type: string
        required: true
      type:
        type: integer
        required: false
        default: 0
        enum:
          - 0  # plugin_access_token
          - 1  # virtual_plugin_token
    response:
      token:
        type: string
      expire_time:
        type: integer
        unit: seconds
    notes:
      - Token valid for 7200 seconds
      - Token must be cached and reused until expiration

  exchange_user_access_token:
    description: >
      Exchange authorization code for user_access_token.
      Must be called server-side.
    prerequisites:
      - plugin_access_token
      - authorization_code (from client getAuthCode)
    http:
      method: POST
      path: /open_api/authen/user_plugin_token
    headers:
      Content-Type: application/json
      X-Plugin-Token: "{{plugin_access_token}}"
    body:
      code:
        type: string
        required: true
      grant_type:
        type: string
        required: true
        fixed: authorization_code
    response:
      token:
        type: string
        description: user_access_token
      refresh_token:
        type: string
      expire_time:
        type: integer
      refresh_token_expire_time:
        type: integer
      user_key:
        type: string
      saas_tenant_key:
        type: string

  refresh_user_access_token:
    description: Refresh an expired user_access_token
    prerequisites:
      - plugin_access_token
      - refresh_token
    http:
      method: POST
      path: /open_api/authen/refresh_token
    headers:
      Content-Type: application/json
      X-Plugin-Token: "{{plugin_access_token}}"
    body:
      refresh_token:
        type: string
        required: true
      type:
        type: integer
        required: true
        fixed: 1
    response:
      token:
        type: string
      expire_time:
        type: integer
      refresh_token:
        type: string
      refresh_token_expire_time:
        type: integer

usage_in_other_skills:
  plugin_access_token:
    headers:
      X-Plugin-Token: "{{plugin_access_token}}"
      X-User-Key: "{{user_key}}"
  user_access_token:
    headers:
      X-Plugin-Token: "{{user_access_token}}"

constraints:
  - user_access_token must be generated server-side
  - front-end plugins cannot call OpenAPI directly
  - permissions depend on plugin scope, space installation, and user role

recommended_openclaw_strategy:
  - Cache plugin_access_token globally
  - Bind user_access_token to conversation/session
  - Auto-refresh user_access_token when expired
  - Choose token type per API based on permission requirements
```**）

## 如何使用令牌（调用其他 OpenAPI）

- **plugin_access_token**：在请求头中添加 `X-Plugin-Token: {{plugin_access_token}}`，并确保设置 `X-User-Key: {{user_key}}`。
- **user_access_token**：在请求头中添加 `X-Plugin-Token: {{user_access_token}}`（此处使用用户令牌，而非插件令牌）。

**注意事项**：
- `user_access_token` 必须通过服务器端的授权流程获取；前端插件不能直接调用 OpenAPI。
- 权限取决于插件权限、项目配置和用户角色。
- 建议：全局缓存 `plugin_access_token`；将 `user_access_token` 绑定到会话/对话中；在令牌过期时刷新；根据权限需求选择合适的令牌类型。

---

## 上下文信息（`project_key`、`user_key`）—— 必需的凭证

`project_key` 和 `user_key` 是所有 Meegle OpenAPI 调用所必需的参数：

| 参数 | 说明 | 获取途径 |
|---------|-------------|-----------------|
| **project_key** | 项目标识符 | Meegle 平台：双击 **项目图标**；或从项目 URL 获取 |
| **user_key** | 用户标识符 | Meegle 平台：双击 **头像**；或从 `user_access_token` 响应中的 `user_key` 字段获取 |

在请求路径或请求体中使用 `project_key`（例如：`{project_key}`）。在使用 `plugin_access_token` 调用 API 时，在请求头中添加 `X-User-Key: {{user_key}`。

## 请求头（调用 Meegle OpenAPI 时）

在调用任何 Meegle OpenAPI（如项目、工作项、设置等）时：

- **使用 `plugin_access_token` 时**：设置 `X-Plugin-Token: {{plugin_access_token}}`，并确保设置 `X-User-Key: {{user_key}}`。
- **使用 `user_access_token` 时**：设置 `X-Plugin-Token: {{user_access_token}}`（此处使用用户令牌）。使用用户令牌时，不要设置 `X-User-Key`。

所有请求均使用相同的 **域名**（例如 `https://project.larksuite.com` 或 `https://project.feishu.cn`）作为基础 URL。

---

## 技能包（实现细节）

本技能提供了 OpenClaw 的认证、上下文处理和请求头配置的实现细节。

### 认证层（Auth Layer）

包含获取令牌的实现细节。

### 上下文处理层（Context Layer）

### 请求头处理规则（Header Decision Rule）

### 全局限制

- `plugin_access_token` 的有效期为 7200 秒，建议缓存后重复使用。
- `user_access_token` 仅限在服务器端使用。
- 对于写操作，建议优先使用 `user_access_token`。
- 所有 OpenAPI 调用每条请求的频率不得超过 15 次/秒（QPS）。