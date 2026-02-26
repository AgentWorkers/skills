---
name: meegle-api-credentials
description: >
  获取 Meegle API 访问凭据：域名（domain）、令牌（token）、上下文信息（project_key、user_key）以及请求头（request headers）。  
  在尝试任何与 Meegle API 相关的操作之前，请先阅读本文档；所有调用所需的先决条件都包含在本技能说明中。
metadata: {"openclaw":{"requires":{"env":["MEEGLE_PLUGIN_ID","MEEGLE_PLUGIN_SECRET","MEEGLE_DOMAIN","MEEGLE_PROJECT_KEY","MEEGLE_USER_KEY"]}}}
---
# Meegle API — 凭据（域名、访问令牌、上下文、请求头）

本文档将介绍如何生成用于 OpenAPI 的 **域名**、**访问令牌**（插件或用户专用的令牌）、**上下文信息**（`project_key`、`user_key`）以及 **请求头**。在使用其他 Meegle API 功能之前，必须确保这些凭据已经准备好。

## 令牌缓存

**在同一会话中缓存并重用令牌。** `plugin_access_token` 的有效期为 7200 秒。获取一次后，将其存储在内存或会话中，并在有效期内重复使用；无需在每次请求时都重新调用令牌相关的 API。

## 凭据的获取与使用规则

**获取凭据的优先级：** 对于每个凭据，优先考虑 **环境变量**（来自 OpenClaw 配置文件），如果环境变量中已经设置了相应的值，则不再询问用户。对于 OpenClaw 来说，所有凭据都必须通过 OpenClaw 配置文件进行设置，这样才能确保它们在所有会话中生效；详情请参见 [环境变量](#environment-variables)。不建议使用其他配置方式（如 shell 中的 `export` 命令）。

| 凭据            | 环境变量             | 获取途径                         |
|-----------------|---------------------|-------------------------------------------|
| plugin_id        | MEEGLE_PLUGIN_ID       | 在 Meegle 开发者平台 → 插件 → 基本信息中设置         |
| plugin_secret     | MEEGLE_PLUGIN_SECRET     | 同上                             |
| domain          | MEEGLE_DOMAIN         | 请参阅下方的 [域名](#domain)                 |
| project_key      | MEEGLE PROJECT_KEY     | 双击项目图标或项目 URL；在路径/请求体中以 `{project_key}` 的形式使用 |
| user_key       | MEEGLE_USER_KEY       | 双击用户头像或从 `user_access_token` 响应中获取；与 `plugin_access_token` 一起用于 `X-User-Key` 请求头 |

**当缺少某些凭据时：** 首先检查环境变量；如果环境变量中未设置相应的值，告知用户缺少哪些凭据以及在哪里可以获取它们（参见上表），然后请求用户提供所需值并重试。

## 环境变量

为了确保凭据在 **每个 OpenClaw 会话中都可用**，必须将它们配置在 OpenClaw 的配置文件中。这是实现跨会话数据持久化的唯一推荐方式；不建议使用其他方法（如 shell 命令或 `.env` 文件）。OpenClaw 在启动时会读取该配置文件，并将其中的环境变量值注入到技能的运行时环境中。

**配置文件路径：** `~/.openclaw/openclaw.json`

**配置要求：** 在 `meegle-api` 技能条目下，设置 `env` 字段，包含所需的变量名及其值。技能名称必须与配置文件中的索引名称 `meegle-api` 一致。

```json
{
  "skills": {
    "entries": {
      "meegle-api": {
        "env": {
          "MEEGLE_PLUGIN_ID": "<your_plugin_id>",
          "MEEGLE_PLUGIN_SECRET": "<your_plugin_secret>",
          "MEEGLE_DOMAIN": "project.feishu.cn",
          "MEEGLE_PROJECT_KEY": "<your_project_key>",
          "MEEGLE_USER_KEY": "<your_user_key>"
        }
      }
    }
  }
}
```

- **国际区域：** 使用 `MEEGLE_DOMAIN`：`project.larksuite.com`。
- 如果配置文件中已有其他键（例如 `skill_source`），只需在 `skills.entries["meegle-api"]` 下添加或更新 `env` 对象即可。

## 域名设置

| 地区            | 域名                          |
|----------------|-----------------------------------------|
| 国际区域          | `project.larksuite.com`                    |
| 中国（飞书）        | `project.feishu.cn`                     |

**基础 URL：** `https://{domain}`。**示例：** `https://project.larksuite.com/open_api/authen/plugin_token`。

---

## 获取访问令牌

关于何时使用访问令牌、其功能、请求/响应格式、请求头、相关限制以及使用策略，请参阅下方的 **API 规范**。

### API 规范：`obtain_access_token`

```yaml
name: meegle.obtain_access_token
description: Meegle access credentials (plugin / virtual / user token) for OpenClaw.
when_to_use: [Before any Meegle OpenAPI, When plugin token expires (2h), On-behalf-of-user operations]
capabilities: [generate_plugin_token, generate_virtual_plugin_token, exchange_user_access_token, refresh_user_access_token]

flows:
  generate_plugin_token:
    description: plugin_access_token or virtual_plugin_token
    http: { method: POST, path: /open_api/authen/plugin_token }
    headers: { Content-Type: application/json }
    body:
      plugin_id: { type: string, required: true }
      plugin_secret: { type: string, required: true }
      type: { type: integer, required: false, default: 0, enum: [0, 1] }
    response: { token: string, expire_time: integer }
    notes: Token 7200s; cache and reuse (see Token caching).

  exchange_user_access_token:
    description: Exchange auth code for user_access_token (server-side).
    prerequisites: [plugin_access_token, authorization_code from getAuthCode]
    http: { method: POST, path: /open_api/authen/user_plugin_token }
    headers: { Content-Type: application/json, X-Plugin-Token: "{{plugin_access_token}}" }
    body: { code: string, grant_type: authorization_code }
    response: { token: user_access_token, refresh_token, expire_time, refresh_token_expire_time, user_key, saas_tenant_key }

  refresh_user_access_token:
    description: Refresh expired user_access_token
    prerequisites: [plugin_access_token, refresh_token]
    http: { method: POST, path: /open_api/authen/refresh_token }
    headers: { Content-Type: application/json, X-Plugin-Token: "{{plugin_access_token}}" }
    body: { refresh_token: string, type: 1 }
    response: { token, expire_time, refresh_token, refresh_token_expire_time }

usage_in_other_skills:
  plugin_access_token: { headers: { X-Plugin-Token: "{{plugin_access_token}}", X-User-Key: "{{user_key}}" } }
  user_access_token: { headers: { X-Plugin-Token: "{{user_access_token}}" } }
constraints: [user_access_token server-side only, no OpenAPI from front-end, permissions by scope/space/role]
recommended_openclaw_strategy: [Cache plugin token globally, Bind user token to session, Auto-refresh user token, Choose token type per API]
```

### 调用 OpenAPI 时的请求头

- **plugin_access_token：** `X-Plugin-Token: {{plugin_access_token}}`，并且必须设置 `X-User-Key: {{user_key}}`。
- **user_access_token：** `X-Plugin-Token: {{user_access_token}}`（用户令牌值）；**不要发送 `X-User-Key`**。

所有请求的基础 URL 为 `https://{domain}`（详见域名设置）。完整的请求头信息请参阅 API 规范中的 **usage_in_other_skills** 部分。

---

## 技能包（实现细节）

本文档还介绍了 OpenClaw 集成的认证、上下文处理及请求头设置方法。

### 认证层

```yaml
# meegle.auth.get_plugin_token (internal) — cache and reuse
name: meegle.auth.get_plugin_token
type: internal
inputs: { plugin_id: { type: string, required: true, source: secret }, plugin_secret: { type: string, required: true, source: secret }, type: { type: integer, default: 0 } }
http: { method: POST, url: "https://{domain}/open_api/authen/plugin_token" }
headers: { Content-Type: application/json }
outputs: { token: plugin_access_token, expire_time: number }
# domain = project.larksuite.com | project.feishu.cn

---
# meegle.auth.get_user_token (flow) — auth code → user_access_token
name: meegle.auth.get_user_token
type: flow
inputs: { auth_code: { type: string, required: true }, plugin_access_token: { type: string, required: true } }
http: { method: POST, url: "https://{domain}/open_api/authen/user_plugin_token" }
headers: { Content-Type: application/json, X-Plugin-Token: "{{plugin_access_token}}" }
body: { code: "{{auth_code}}", grant_type: authorization_code }
outputs: { user_access_token, refresh_token, expire_time, refresh_token_expire_time, user_key }

---
# meegle.auth.refresh_user_token (internal)
name: meegle.auth.refresh_user_token
type: internal
inputs: { refresh_token: { type: string, required: true }, plugin_access_token: { type: string, required: true } }
http: { method: POST, url: "https://{domain}/open_api/authen/refresh_token" }
headers: { Content-Type: application/json, X-Plugin-Token: "{{plugin_access_token}}" }
body: { type: 1 }
outputs: { user_access_token, expire_time, refresh_token, refresh_token_expire_time }
```

### 上下文处理层

```yaml
# meegle.context.resolve_project — project_key
name: meegle.context.resolve_project
type: utility
inputs: { project_key: { type: string, required: false } }
behavior: MEEGLE_PROJECT_KEY → config default → ask user
outputs: { project_key: string }

---
# meegle.context.resolve_user_key — user_key
name: meegle.context.resolve_user_key
type: utility
inputs: { user_key: { type: string, required: true }, user_access_token: { type: string, required: false } }
behavior: MEEGLE_USER_KEY → user_key from user_access_token → ask user
outputs: { user_key: string }
```

### 请求头决定规则

`meegle.http.prepare_headers` 函数的输入参数包括：`operation_type`（读取/写入操作）、`plugin_access_token`、`user_access_token?`、`user_key`。

| 操作类型          | 应设置的请求头                        |
|------------------|-----------------------------------------|
| 写入操作且 `user_access_token` 存在 | `X-Plugin-Token: {{user_access_token}}`         |
| 读取操作          | `X-Plugin-Token: {{plugin_access_token}}`, `X-User-Key: {{user_key}}` |

### 全局限制

- `plugin_access_token` 的缓存有效期为 7200 秒；`user_access_token` 仅在服务器端进行缓存；写入操作优先使用 `user_access_token`；每个令牌的并发请求数量限制为 15 次/秒。