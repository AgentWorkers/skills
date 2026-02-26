---
name: meegle-api-users
description: 与 Meegle 用户相关的 OpenAPI（用户组、成员信息）。身份验证凭据来自 `meegle-api-credentials`。
metadata: { openclaw: {} }
---
# Meegle API — 用户相关功能

以下是与用户相关的 OpenAPI 接口。相关的数据（如域名、令牌、上下文信息以及请求头）均来自 `meegle-api-credentials`。

---

## 获取用户组成员

查询指定空间内的用户组成员。支持空间管理员、空间成员以及自定义用户组。

### 注意事项

**该 API 仅支持用户访问凭证（`user_access_token`），不支持插件访问凭证。** 如需获取 `user_access_token`，请参考 `meegle-api-credentials`。

### 使用场景

- 列出空间管理员、空间成员或自定义用户组的成员信息。
- 将 `user_group_ids` 解析为对应的 `user_keys`。
- 在权限或成员资格验证中用到这些信息。

### API 规范：`get_user_group_members`

```yaml
name: get_user_group_members
type: api
description: Query user group members. user_access_token only (no plugin token).
auth: { type: user_access_token }
http: { method: POST, url: "https://{domain}/open_api/{project_key}/user_groups/members/page" }
headers: { Content-Type: application/json, X-Plugin-Token: "{{user_access_token}}" }
path_params: { project_key: { type: string, required: true } }
inputs: { user_group_type: { type: string, required: true, enum: [PROJECT_ADMIN, PROJECT_MEMBER, CUSTOMIZE] }, user_group_ids: { type: array, max_items: 50 }, page_num: { type: integer, default: 1 }, page_size: { type: integer, default: 50, max: 100 } }
outputs: { data: { list: array, pagination: object } }
constraints: [Permission: Users, page_size max 100]
error_mapping: { 20002: Page size limit, 1000053008: Type not supported, 1000053010: User group not found, 1000053011: Max 50 groups }
```

### 使用说明

- **必须使用 `user_access_token`**：格式为 `X-Plugin-Token: {{user_access_token}}`；插件令牌无效。
- **user_group_type**：可选值：`PROJECT_ADMIN`、`PROJECT_MEMBER` 或 `CUSTOMIZE`。
- **user_group_ids**：对于 `CUSTOMIZE` 类型，此参数可选；省略该参数可获取所有自定义用户组的成员信息。这些 ID 可通过 URL `.../userGroup/{id}` 获得。
- **page_size**：最大值为 100；默认值为 50。

---

## 获取租户用户列表

在租户范围内进行模糊搜索，并返回用户的详细信息。支持按用户名或其他关键词进行搜索；例如，查询 "user1" 会返回 "user1" 和 "user1.1" 等用户。

### 使用场景

- 按用户名或关键词在租户内搜索用户。
- 从部分名称中解析出用户的唯一标识符（`user_key`）。
- 构建用户选择器或成员资格显示界面。

### API 规范：`get_tenant_user_list`

```yaml
name: get_tenant_user_list
type: api
description: Fuzzy search users in tenant by name; returns user details.
auth: { type: plugin_access_token, header: X-Plugin-Token, user_header: X-User-Key }
http: { method: POST, url: "https://{domain}/open_api/user/search" }
headers: { Content-Type: application/json, X-Plugin-Token: "{{resolved_token}}", X-User-Key: "{{user_key}}" }
inputs: { query: { type: string, required: false }, project_key: { type: string, required: false } }
outputs: { data: array }
constraints: [Permission: Users; project_key required for marketplace or when user tenant != plugin tenant]
error_mapping: { 30006: User not found, 1000052063: Project not exist }
```

### 使用说明

- **query**：按用户名进行模糊搜索；省略该参数可列出租户内的所有用户。
- **project_key**：对于市场插件是必填项；对于企业插件，当用户的所属租户与插件租户不同时也需要提供该参数。

---

## 获取用户详细信息

通过 `user_key`、`out_id`（UnionId）或电子邮件地址获取一个或多个用户的详细信息。

### 注意事项

- 如果使用 **虚拟令牌**，只能查询到该插件的协作用户；如需查询其他用户，请使用官方（非虚拟）令牌。
- 当使用 `plugin_access_token` 时，**不需要提供 `X-User-Key` 参数**。

### 使用场景

- 将 `user_key`、`out_id` 或电子邮件地址解析为完整的用户信息。
- 获取用户的头像、姓名、电子邮件地址及状态以供显示。
- 批量查询用户信息（每次请求最多 100 条记录）。

### API 规范：`get_user_details`

```yaml
name: get_user_details
type: api
description: User details by user_keys, out_ids, or emails; X-User-Key not required.
auth: { type: plugin_access_token, header: X-Plugin-Token }
http: { method: POST, url: "https://{domain}/open_api/user/query" }
headers: { Content-Type: application/json, X-Plugin-Token: "{{resolved_token}}" }
inputs: { user_keys: { type: array, max_items: 100 }, out_ids: { type: array, max_items: 100 }, emails: { type: array, max_items: 100 }, tenant_key: { type: string, required: false } }
outputs: { data: array }
constraints: [Permission: Users, at least one of user_keys/out_ids/emails, max 100 total]
error_mapping: { 30006: User not found, 20004: Exceeds 100 records }
```

### 使用说明

- 必须提供至少一个识别用户身份的参数（`user_keys`、`out_ids` 或 `emails`）；每次请求最多支持 100 个标识符。
- **tenant_key**：当查询属于其他租户的用户时，需要提供该租户的 `sas_tenant_key`。
- 使用 `plugin_access_token` 时，**不需要提供 `X-User-Key` 参数**。

---

## 获取空间内的团队成员

返回在指定空间内可见的团队列表，以及这些团队的成员（`user_keys`）和管理员信息。

### 使用场景

- 列出在空间内可见的团队。
- 获取团队成员及管理员信息。
- 构建团队选择器或成员资格显示界面。

### API 规范：`get_team_member_in_space`

```yaml
name: get_team_member_in_space
type: api
description: Teams visible in space (user_keys, administrators per team).
auth: { type: plugin_access_token, header: X-Plugin-Token, user_header: X-User-Key }
http: { method: GET, url: "https://{domain}/open_api/{project_key}/teams/all" }
headers: { X-Plugin-Token: "{{resolved_token}}", X-User-Key: "{{user_key}}" }
path_params: { project_key: { type: string, required: true } }
inputs: { offset: { type: integer, required: false }, limit: { type: integer, default: 300, max: 300 } }
outputs: { data: array, has_more: boolean }
constraints: [Permission: Users, limit max 300]
error_mapping: { 30006: User not found }
```

### 使用说明

- **project_key**：用于标识空间的路径参数。
- **offset / limit**：用于分页；偏移量从 0 开始计算；限制数量最大为 300，默认值为 300。

---

## 创建自定义用户组

在指定空间内创建一个自定义用户组。仅支持添加用户成员（`user_keys`），不支持添加部门成员。

### 注意事项

**该 API 仅支持用户访问凭证（`user_access_token`）。** 如需获取 `user_access_token`，请参考 `meegle-api-credentials`。

### 使用场景

- 在空间内创建新的自定义用户组。
- 根据用户列表定义用户组。
- 设置权限或通知规则。

### API 规范：`create_customized_user_group`

```yaml
name: create_customized_user_group
type: api
description: Create custom user group; user_access_token only; users = user_key list, max 100.
auth: { type: user_access_token }
http: { method: POST, url: "https://{domain}/open_api/{project_key}/user_group" }
headers: { Content-Type: application/json, X-Plugin-Token: "{{user_access_token}}" }
path_params: { project_key: { type: string, required: true } }
inputs: { name: { type: string, required: true, max_length: 250 }, users: { type: array, required: true, max_items: 100 } }
outputs: { data: { id: string } }
constraints: [Permission: Users, name unique no / max 250, users max 100]
error_mapping: { 1000053001: Name exists, 1000053002: Unsupported char, 1000053003: Name length, 1000053004: User invalid, 1000053005: Users limit 100, 1000053006: Need user, 1000053007: Need name }
```

### 使用说明

- **必须使用 `user_access_token`**：格式为 `X-Plugin-Token: {{user_access_token}}`；插件令牌无效。
- **name**：名称必须唯一，不能包含 "/" 或其他不支持的字符；长度最多为 250 个字符。
- **users**：需要提供用户 ID 的列表；最多支持 100 个用户 ID；无法添加已离职或不存在的用户。

---

## 更新用户组成员

更新用户组的成员信息。支持添加、删除或替换成员。适用于空间成员（`PROJECT_MEMBER`）或自定义用户组（`CUSTOMIZE`）。

### 注意事项

**该 API 仅支持用户访问凭证（`user_access_token`）。** 如需获取 `user_access_token`，请参考 `meegle-api-credentials`。

- 从非空间成员添加用户时，该用户会自动成为空间成员。
- 从空间成员中删除用户时，该用户也会从其他用户组中移除。

### 使用场景

- 向自定义用户组中添加或删除成员。
- 更新用户组的完整成员列表。
- 更新空间成员（`PROJECT_MEMBER`）或自定义用户组（`CUSTOMIZE`）的成员信息。

### API 规范：`update_user_group_member`

```yaml
name: update_user_group_member
type: api
description: Update user group members (add/delete/replace); user_access_token only; replace_users overrides add/delete.
auth: { type: user_access_token }
http: { method: PATCH, url: "https://{domain}/open_api/{project_key}/user_group/members" }
headers: { Content-Type: application/json, X-Plugin-Token: "{{user_access_token}}" }
path_params: { project_key: { type: string, required: true } }
inputs: { user_group_type: { type: string, required: true, enum: [PROJECT_MEMBER, CUSTOMIZE] }, user_group_id: string, add_users: { type: array, max_items: 100 }, delete_users: { type: array, max_items: 100 }, replace_users: { type: array, max_items: 100 } }
outputs: { data: object }
constraints: [Permission: Users, one of add/delete/replace non-empty, user_group_id when CUSTOMIZE, max 100 per field]
error_mapping: { 1000053004: User invalid, 1000053005: Users limit 100, 1000053008: Type not supported, 1000053009: Need user group ID, 1000053006: Need user, 1000053010: User group not found }
```

### 使用说明

- **必须使用 `user_access_token`**：格式为 `X-Plugin-Token: {{user_access_token}}`；插件令牌无效。
- **user_group_id**：当 `user_group_type` 为 `CUSTOMIZE` 时必填；该 ID 可通过用户组页面的 URL 获得。
- 参数 `replace_users` 具有优先级：如果该参数不为空，`add_users` 和 `delete_users` 的操作将被忽略。
- 如果 `add_users` 和 `delete_users` 中包含相同的 `user_key`，该用户将被忽略。