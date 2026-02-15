---
name: meegle-api-users
description: |
  Meegle API prerequisite: domain, access token (plugin/user), context (project_key, user_key),
  request headers, and global constraints. User-related OpenAPIs. Read this first before other Meegle API skills.
metadata:
  { "openclaw": {} }
---

# Meegle API — 用户（及共享的先决条件）

所有 Meegle OpenAPI 调用的共享先决条件。其他 Meegle API 功能（如空间管理、工作项、设置、评论、视图和测量）均假定您已经掌握了本技能中关于令牌（token）和请求头（headers）的相关内容。

## 域名（API 基础主机）

在请求中，将 `{domain}` 替换为您所在地区的实际 Meegle API 主机地址：

| 地区 | domain |
|--------|--------|
| **国际** | `project.larksuite.com` — 基础 URL: `https://project.larksuite.com` |
| **中国（Feishu 项目）** | `project.feishu.cn` — 基础 URL: `https://project.feishu.cn` |

示例：插件令牌（plugin token）的 URL 为 `https://{domain}/open_api/authen/plugin_token` — 国际地区使用 `https://project.larksuite.com/open_api/authen/plugin_token`，中国地区使用 `https://project.feishu.cn/open_api/authen/plugin_token`。

---

## 获取访问令牌（Obtain Access Token）

为 OpenClaw 生成 Meegle 访问凭据，以便调用 OpenAPI。

### 使用场景

- 在调用任何 Meegle OpenAPI 之前
- 当插件访问令牌（plugin_access_token）过期时（有效期为 2 小时）
- 当需要代表特定用户执行操作时

### 功能

- `generate_plugin_token` — 获取插件访问令牌（plugin_access_token）或虚拟插件令牌（virtual_plugin_token）
- `exchange_user_access_token` — 将授权码（authorization code）兑换为用户访问令牌（user_access_token）
- `refresh_user_access_token` — 刷新过期的用户访问令牌（user_access_token）

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

- **plugin_access_token**：在请求头中添加 `X-Plugin-Token: {{plugin_access_token}}`；可选地添加 `X-User-Key: {{user_key}}`。
- **user_access_token**：在请求头中添加 `X-Plugin-Token: {{user_access_token}}`（此处使用用户令牌，而非插件令牌）。

### 限制与建议

- 用户访问令牌（user_access_token）必须通过服务器端授权流程获取；前端插件不能直接调用 OpenAPI。
- 权限取决于插件权限范围、空间安装情况以及用户角色。
- 建议：全局缓存插件访问令牌（plugin_access_token）；将用户访问令牌（user_access_token）绑定到会话（conversation/session）中；令牌过期时及时刷新；根据权限要求为不同 API 选择合适的令牌类型。

---

## 用户相关功能（Users）

与用户相关的 Meegle OpenAPI 功能（如用户信息、成员列表等）将在此处进行说明。使用前提：需具备上述章节中提到的域名（domain）和令牌（token）。

---

## 技能包（实现细节）（Skill Pack – Implementation Details）

OpenClaw 的实现与集成所需的认证（Auth）、上下文管理（Context）、请求头（Request Headers）及全局限制（Global Constraints）。

### 认证层（Auth Layer）

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

### 上下文管理层（Context Layer）

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
      How to get: 1) Double-click space icon in Meegle project. 2) project_key in project URL.
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
      How to get: 1) Double-click user avatar in Meegle. 2) user_key from user_access_token response.
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

### 请求头规则（Header Decision Rule）

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

### 全局限制（Global Constraints）

- 插件访问令牌（plugin_access_token）的有效期为 7200 秒，可缓存并重复使用。
- 用户访问令牌（user_access_token）必须仅在服务器端使用。
- 对于写操作，建议优先使用用户访问令牌（user_access_token）。
- 所有 OpenAPI 调用都应遵守每令牌 15 次请求/秒（QPS）的速率限制。

---

## 用户相关 API（Users-related APIs）

与用户相关的 Meegle OpenAPI 功能（如用户信息、成员列表等）的详细说明。使用前提：需具备上述章节中提到的域名（domain）和令牌（token）。