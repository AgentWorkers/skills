---
name: meegle-api-credentials
description: >
  获取 Meegle API 访问凭据：域名（domain）、令牌（token）、上下文信息（project_key、user_key）以及请求头（request headers）。
  在尝试任何其他 Meegle API 相关操作之前，请先阅读本文档；所有 API 调用的前提条件都包含在本文档中。
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
  optional_credentials:
    authorization_code:
      description: "OAuth code from getAuthCode(); required for user_access_token"
    refresh_token:
      description: "From user_plugin_token response; for refreshing user_access_token"
  context:
    project_key: "Space identifier; in Meegle Developer Platform double-click the project icon to get it"
    user_key: "User identifier; in Meegle Developer Platform double-click the avatar to get it (or from user_access_token response)"
---
# Meegle API — 凭据（域名、访问令牌、上下文、请求头）

本技能用于生成 Meegle 的域名、访问令牌（插件或用户专用）、上下文信息（项目标识符、用户标识符）以及调用 OpenAPI 时所需的请求头。在调用其他 Meegle API 功能之前，需确保已获取这些凭据。

## 域名（API 基础主机）

在请求中将 `{domain}` 替换为适用于您所在地区的实际 Meegle API 主机地址：

| 地区 | 域名 |
|--------|--------|
| **国际** | `project.larksuite.com` — 基础 URL：`https://project.larksuite.com` |
| **中国（Feishu 项目）** | `project.feishu.cn` — 基础 URL：`https://project.feishu.cn` |

示例：插件令牌的 URL 为 `https://{domain}/open_api/authen/plugin_token` — 国际地区使用 `https://project.larksuite.com/open_api/authen/plugin_token`，中国地区使用 `https://project.feishu.cn/open_api/authen/plugin_token`。

---

## 获取访问令牌

生成 Meegle 的访问凭据，以便 OpenClaw 能够调用 OpenAPI。

### 使用场景

- 在调用任何 Meegle OpenAPI 之前
- 当插件访问令牌过期时（有效期为 2 小时）
- 当需要代表特定用户执行操作时

### 功能

- `generate_plugin_token` — 获取插件访问令牌或虚拟插件令牌
- `exchange_user_access_token` — 将授权码兑换为用户访问令牌
- `refresh_user_access_token` — 刷新过期的用户访问令牌

### API 规范：`obtain_access_token`

```yaml
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
```

### 如何使用令牌（调用其他 OpenAPI）

- **插件访问令牌**：在请求头中添加 `X-Plugin-Token: {{plugin_access_token}}`；可选地添加 `X-User-Key: {{user_key}}`。
- **用户访问令牌**：在请求头中添加 `X-Plugin-Token: {{user_access_token}}`（此处使用用户令牌，而非插件令牌）。

### 限制与建议

- 用户访问令牌必须通过服务器端获取；前端插件不能直接调用 OpenAPI。
- 权限取决于插件权限范围、空间安装情况以及用户角色。
- 建议：全局缓存插件访问令牌；将用户访问令牌绑定到会话/对话中；在令牌过期时刷新；根据权限需求为不同 API 选择合适的令牌类型。

---

## 上下文（项目标识符、用户标识符）

大多数 OpenAPI 调用都会使用以下上下文信息：

| 上下文 | 说明 | 获取方式 |
|---------|-------------|-----------------|
| **项目标识符** | 空间（项目）的标识符 | 在 Meegle 开发者平台中，双击 **项目图标** 获取；或从项目 URL 中获取 |
| **用户标识符** | 用户的标识符 | 在 Meegle 开发者平台中，双击 **头像** 获取；或从用户访问令牌中的 `user_key` 字段获取 |

在路径或请求体中使用 **项目标识符**（例如：`{project_key}`）。在使用插件访问令牌调用 API 时，在请求头中添加 `X-User-Key` 和 `user_key`。

---

## 请求头（调用 OpenAPI 时）

在调用任何 Meegle OpenAPI（如空间管理、工作项、设置等）时：

- **使用插件访问令牌**：设置 `X-Plugin-Token: {{plugin_access_token}}`。如果 API 需要以用户身份执行操作，可选地添加 `X-User-Key: {{user_key}}`。
- **使用用户访问令牌**：设置 `X-Plugin-Token: {{user_access_token}}`（此处使用用户令牌，而非插件令牌）。使用用户令牌时无需添加 `X-User-Key`。

所有请求均使用相同的域名（例如：`https://project.larksuite.com` 或 `https://project.feishu.cn`）作为基础 URL。

---

## 技能包（实现细节）

本技能提供了 OpenClaw 实现和集成所需的认证、上下文处理及请求头配置。

### 认证层

获取令牌的实现细节。

### 认证层

```yaml
name: meegle.auth.get_plugin_token
type: internal
description: Get or refresh Meegle plugin_access_token (cache and reuse)
inputs:
  plugin_id:
    type: string
    required: true
    source: secret
    description: |
      Plugin ID.
      Location: Meegle Developer Platform → Plugin → Basic Information → Plugin ID
  plugin_secret:
    type: string
    required: true
    source: secret
    description: |
      Plugin secret.
      Location: Meegle Developer Platform → Plugin → Basic Information → Plugin Secret
  type:
    type: integer
    required: false
    default: 0
    description: |
      0 = plugin_access_token
      1 = virtual_plugin_token (dev only)
http:
  method: POST
  url: https://{domain}/open_api/authen/plugin_token
  notes: domain = project.larksuite.com (international) or project.feishu.cn (China Feishu Project)
headers:
  Content-Type: application/json
outputs:
  token:
    type: string
    description: plugin_access_token
  expire_time:
    type: number
    description: Token validity in seconds

---

name: meegle.auth.get_user_token
type: flow
description: Exchange OAuth authorization code for user_access_token (act on behalf of user)
inputs:
  auth_code:
    type: string
    required: true
    description: |
      OAuth authorization code.
      Obtain via front-end: window.JSSDK.utils.getAuthCode()
  plugin_access_token:
    type: string
    required: true
http:
  method: POST
  url: https://{domain}/open_api/authen/user_plugin_token
headers:
  Content-Type: application/json
  X-Plugin-Token: "{{plugin_access_token}}"
body:
  code: "{{auth_code}}"
  grant_type: authorization_code
outputs:
  user_access_token:
    type: string
  refresh_token:
    type: string
  expire_time:
    type: number
  refresh_token_expire_time:
    type: number
  user_key:
    type: string
    description: |
      Current user unique identifier.
      Source: user_key field in this response

---

name: meegle.auth.refresh_user_token
type: internal
description: Refresh user_access_token
inputs:
  refresh_token:
    type: string
    required: true
  plugin_access_token:
    type: string
    required: true
http:
  method: POST
  url: https://{domain}/open_api/authen/refresh_token
headers:
  Content-Type: application/json
  X-Plugin-Token: "{{plugin_access_token}}"
body:
  type: 1
outputs:
  user_access_token:
    type: string
  expire_time:
    type: number
  refresh_token:
    type: string
  refresh_token_expire_time:
    type: number
```

### 上下文层

```yaml
name: meegle.context.resolve_project
type: utility
description: Resolve project_key
inputs:
  project_key:
    type: string
    required: false
    description: |
      Space unique identifier.
      How to get: In Meegle Developer Platform, double-click the project icon; or use project_key from project URL.
behavior:
  - If default project_key is configured, use it
  - Otherwise ask user to provide
outputs:
  project_key:
    type: string

---

name: meegle.context.resolve_user_key
type: utility
description: Resolve user_key
inputs:
  user_key:
    type: string
    required: false
    description: |
      User unique identifier.
      How to get: In Meegle Developer Platform, double-click the avatar; or use user_key from user_access_token response.
  user_access_token:
    type: string
    required: false
behavior:
  - If user_access_token exists, use its user_key first
  - Otherwise ask user to provide explicitly
outputs:
  user_key:
    type: string
```

### 请求头决策规则

```yaml
name: meegle.http.prepare_headers
type: internal
description: Build OpenAPI request headers by operation type
inputs:
  operation_type:
    type: string
    required: true
    description: read | write
  plugin_access_token:
    type: string
    required: true
  user_access_token:
    type: string
    required: false
  user_key:
    type: string
    required: false
rules:
  - if: operation_type == "write" and user_access_token exists
    headers:
      X-Plugin-Token: "{{user_access_token}}"
  - if: operation_type == "read"
    headers:
      X-Plugin-Token: "{{plugin_access_token}}"
      X-User-Key: "{{user_key}}"
```

### 全局限制

- 插件访问令牌的有效期为 7200 秒；可缓存并重复使用。
- 用户访问令牌必须仅在服务器端使用。
- 对于写操作，建议优先使用用户访问令牌。
- 所有 OpenAPI 调用均需遵守每令牌 15 次请求/秒（QPS）的限制。