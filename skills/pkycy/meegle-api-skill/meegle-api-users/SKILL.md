---
name: meegle-api-users
description: >
  Meegle API：与用户相关的开放API（例如用户组、用户信息等）。  
  域名（Domain）、令牌（Token）、上下文信息（Context）以及请求头（Request Headers）均从 `meegle-api-credentials` 中获取。
metadata:
  openclaw: {}
---
# Meegle API — 用户

与用户相关的 Meegle OpenAPI（例如用户信息、成员列表等）需要使用 **meegle-api-credentials** 技能来获取域名、令牌、上下文（project_key、user_key）以及请求头信息；本文档仅针对这些用户相关的 API 进行说明。

---

## 获取用户组成员

查询指定空间内的用户组成员。支持空间管理员、空间成员以及自定义用户组。

### 注意事项

**此 API 仅支持用户访问凭证（user_access_token）**，不支持插件访问凭证。有关如何获取 user_access_token 的信息，请参阅 **meegle-api-credentials**。

### 使用场景

- 列出空间管理员、空间成员或自定义用户组的成员
- 将 user_group_ids 解析为空间内的 user_keys
- 在权限或成员资格检查中使用时

### API 规范：get_user_group_members

```yaml
name: get_user_group_members
type: api
description: >
  Query the members of user groups in a specified space.
  Supports PROJECT_ADMIN, PROJECT_MEMBER, and CUSTOMIZE user group types.

auth:
  type: user_access_token
  note: Only user_access_token is supported; plugin_access_token is NOT supported.

http:
  method: POST
  url: https://{domain}/open_api/{project_key}/user_groups/members/page
  headers:
    Content-Type: application/json
    X-Plugin-Token: "{{user_access_token}}"

path_params:
  project_key:
    type: string
    required: true
    description: >
      Space ID (project_key) or space domain name (simple_name).
      project_key: Double-click space name in Meegle.
      simple_name: From space URL, e.g. https://meegle.com/doc/overview → doc.

inputs:
  user_group_type:
    type: string
    required: true
    enum: [PROJECT_ADMIN, PROJECT_MEMBER, CUSTOMIZE]
    description: |
      PROJECT_ADMIN: Space administrator
      PROJECT_MEMBER: Space member
      CUSTOMIZE: Custom user group
  user_group_ids:
    type: array
    items: string
    required: false
    constraints:
      max_items: 50
    description: >
      List of user group IDs. From user group page URL, e.g.
      .../userGroup/756472096042365xxxx → 756472096042365xxxx.
      When user_group_type=CUSTOMIZE, if empty, returns all members of all custom user groups in the space.
      Max 50 user groups per request.
  page_num:
    type: integer
    required: false
    default: 1
    description: Page number. Default first page.
  page_size:
    type: integer
    required: false
    default: 50
    constraints:
      max: 100
    description: Items per page. Default 50, max 100.

outputs:
  data:
    type: object
    properties:
      list:
        type: array
        items:
          user_count: integer
          user_members: array
          id: string
          name: string
        description: |
          user_members: user_key list of members
          id: user group ID
          name: user group name
      pagination:
        page_num: integer
        page_size: integer
        has_more: boolean

constraints:
  - Permission: Permission Management – Users
  - user_group_ids max 50 when user_group_type=CUSTOMIZE
  - page_size max 100

error_mapping:
  20002: Page size limit (more than 100 per page)
  1000053008: User group type not supported
  1000053010: User group not found (no matching user group in the space)
  1000053011: User group limit (more than 50 user groups in one request)
```

### 使用说明

- **仅使用 user_access_token**：请使用 `X-Plugin-Token: {{user_access_token}}`；插件令牌无效。
- **user_group_type**：可选值：PROJECT_ADMIN、PROJECT_MEMBER、CUSTOMIZE。
- **user_group_ids**：对于 CUSTOMIZE 类型，此参数为可选；省略该参数将获取所有自定义用户组的成员。这些 ID 可通过 URL `.../userGroup/{id}` 获得。
- **page_size**：最大值为 100；默认值为 50。

---

## 获取租户用户列表

在租户内进行模糊搜索并返回用户的详细信息。支持按用户名或其他关键词进行搜索；例如，查询 "user1" 会返回 "user1" 和 "user1.1" 等用户。

### 使用场景

- 按用户名或关键词在租户内搜索用户
- 从部分名称中解析 user_key
- 构建用户选择器或成员选择界面时使用

### API 规范：get_tenant_user_list

```yaml
name: get_tenant_user_list
type: api
description: >
  Fuzzy search for users within the tenant and return detailed information.
  Supports query by user name. E.g. "user1" returns "user1", "user1.1", etc.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: POST
  url: https://{domain}/open_api/user/search
  headers:
    Content-Type: application/json
    X-Plugin-Token: "{{resolved_token}}"
    X-User-Key: "{{user_key}}"

inputs:
  query:
    type: string
    required: false
    description: Search keywords, e.g. user names.
  project_key:
    type: string
    required: false
    description: |
      Space ID (project_key). Determines which tenant to search.
      Required if:
      - Enterprise plugin: user's primary tenant != plugin tenant
      - Marketplace plugin: always required
      Obtain: Double-click space name in Meegle project space.

outputs:
  data:
    type: array
    items:
      avatar_url: string
      name_cn: string
      name_en: string
      user_id: integer
      user_key: string
      email: string
      name:
        en_us: string
        default: string
        zh_cn: string
      username: string
      out_id: string
      status: string
    description: List of matching user objects (avatar_url, name_cn/en, user_key, email, etc.).

constraints:
  - Permission: Permission Management – Users
  - project_key required for marketplace plugin; for enterprise plugin when user tenant != plugin tenant

error_mapping:
  30006: User not found (user_key in Header not found)
  1000052063: Project not exist (incorrect project_key)
```

### 使用说明

- **query**：按用户名进行模糊搜索；省略该参数将列出租户内的所有用户。
- **project_key**：对于市场插件是必需的；对于企业插件，当用户的默认租户与插件租户不同时也需要提供此参数。

---

## 获取用户详细信息

通过 user_key、out_id（UnionId）或电子邮件获取一个或多个指定用户的详细信息。

### 注意事项

- 当使用 **虚拟令牌** 时，只能检索到该插件的协作用户。如需查询其他用户，请使用官方（非虚拟）令牌。
- 当使用 **plugin_access_token** 调用此接口时，**X-User-Key** 参数是可选的。

### 使用场景

- 将 user_key、out_id 或电子邮件解析为完整的用户信息
- 获取用户的头像、姓名、电子邮件和状态以供显示
- 批量查询用户信息（每次请求最多 100 个用户）

### API 规范：get_user_details

```yaml
name: get_user_details
type: api
description: >
  Obtain detailed information of one or more specified users.
  Supports lookup by user_keys, out_ids (UnionId), or emails.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  note: X-User-Key is not required when using plugin_access_token.

http:
  method: POST
  url: https://{domain}/open_api/user/query
  headers:
    Content-Type: application/json
    X-Plugin-Token: "{{resolved_token}}"

inputs:
  user_keys:
    type: array
    items: string
    required: false
    constraints:
      max_items: 100
    description: |
      Array of Meegle user_keys.
      Obtain: Double-click personal avatar in Meegle space; or use Get Tenant User List.
      At least one of user_keys, out_ids, emails must be provided. Max 100 per request.
  out_ids:
    type: array
    items: string
    required: false
    constraints:
      max_items: 100
    description: |
      Array of UnionIds from Feishu Open Platform (unified identity across apps).
      At least one of user_keys, out_ids, emails must be provided. Max 100.
  emails:
    type: array
    items: string
    required: false
    constraints:
      max_items: 100
    description: |
      Array of emails. Emails must be bound on Feishu.
      At least one of user_keys, out_ids, emails must be provided. Max 100.
  tenant_key:
    type: string
    required: false
    description: |
      saas_tenant_key of the tenant where the user to be queried is located.
      For emails query when querying users from a tenant other than the plugin's
      (e.g. tenant Y installs plugin from tenant X — pass tenant Y's tenant_key).
      If empty, query is under the plugin's tenant.

outputs:
  data:
    type: array
    items:
      user_id: integer
      name_cn: string
      name_en: string
      out_id: string
      name:
        default: string
        en_us: string
        zh_cn: string
      user_key: string
      username: string
      email: string
      avatar_url: string
      status: string
    description: List of user detail objects.

constraints:
  - Permission: Permission Management – Users
  - At least one of user_keys, out_ids, emails must be provided
  - Max 100 users per request (across all three arrays)

error_mapping:
  30006: User not found (query result empty; check user_key / out_ids / emails)
  20004: Search user limit (exceeds 100 records)
```

### 使用说明

- **必须提供至少一个用户标识符（user_keys、out_ids 或 emails）**；每次请求最多可提供 100 个标识符。
- **tenant_key**：当查询非插件所属租户内的用户时，请提供该租户的 saas_tenant_key。
- 当使用 plugin_access_token 调用此 API 时，**X-User-Key** 参数是可选的。

---

## 获取空间内的团队成员

返回在指定空间内可见的团队列表，这些团队的可见范围为请求的空间。每个团队包含成员（user_keys）和管理员信息。

### 使用场景

- 列出在空间内可见的团队
- 获取团队成员和管理员信息
- 构建团队选择器或成员选择界面时使用

### API 规范：get_team_member_in_space

```yaml
name: get_team_member_in_space
type: api
description: >
  Return a list of teams whose visibility scope is searchable within the specified
  space and whose visible project space is the requested space.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: GET
  url: https://{domain}/open_api/{project_key}/teams/all
  headers:
    X-Plugin-Token: "{{resolved_token}}"
    X-User-Key: "{{user_key}}"

path_params:
  project_key:
    type: string
    required: true
    description: >
      Space ID (project_key) or space domain name (simple_name).
      project_key: Double-click space name in Meegle.
      simple_name: From space URL, e.g. https://meegle.com/doc/overview → doc.

inputs:
  offset:
    type: integer
    required: false
    description: Page offset (0-based).
  limit:
    type: integer
    required: false
    default: 300
    constraints:
      max: 300
    description: Items per page. Max 300. Default 300 if not provided.

outputs:
  data:
    type: array
    items:
      team_name: string
      user_keys: array
      administrators: array
      team_id: integer
    description: |
      user_keys: Member list of the team
      administrators: Admin list of the team
      team_id: Team ID
  has_more:
    type: boolean
    description: Whether more teams exist.

constraints:
  - Permission: Permission Management – Users
  - limit max 300; default 300

error_mapping:
  30006: User not found (user_key in Header not found)
```

### 使用说明

- **project_key**：用于标识空间的路径参数。
- **offset / limit**：用于分页；偏移量从 0 开始；限制值为 300，默认值为 300。

---

## 创建自定义用户组

在指定空间内创建一个自定义用户组。仅支持添加用户成员（user_key），不支持添加部门成员。

### 注意事项

**此 API 仅支持用户访问凭证（user_access_token）**。有关如何获取 user_access_token 的信息，请参阅 **meegle-api-credentials**。

### 使用场景

- 在空间内创建新的自定义用户组
- 根据 user_key 列表定义用户组
- 设置权限或通知组

### API 规范：create_customized_user_group

```yaml
name: create_customized_user_group
type: api
description: >
  Create a custom user group in a specified space.
  Only user members (user_key) are supported; department members cannot be added.

auth:
  type: user_access_token
  note: Only user_access_token is supported; plugin_access_token is NOT supported.

http:
  method: POST
  url: https://{domain}/open_api/{project_key}/user_group
  headers:
    Content-Type: application/json
    X-Plugin-Token: "{{user_access_token}}"

path_params:
  project_key:
    type: string
    required: true
    description: >
      Space ID (project_key) or space domain name (simple_name).
      project_key: Double-click space name in Meegle.
      simple_name: From space URL, e.g. https://meegle.com/doc/overview → doc.

inputs:
  name:
    type: string
    required: true
    constraints:
      max_length: 250
    description: |
      User group name. Cannot duplicate existing or system user group names
      (e.g. Space administrators, Space members). No special characters such as "/".
      Max 250 characters.
  users:
    type: array
    items: string
    required: true
    constraints:
      max_items: 100
    description: >
      List of user_keys for members. Max 100 per request.
      Only user members supported; department members cannot be added.

outputs:
  data:
    type: object
    properties:
      id: string
    description: ID of the newly created user group.

constraints:
  - Permission: Permission Management – Users
  - name: unique, no special chars (e.g. /), max 250 chars
  - users: max 100; only user members

error_mapping:
  1000053001: User group name exists (duplicate with existing or system name)
  1000053002: Name contains unsupported character (e.g. "/")
  1000053003: Name length not supported (exceeds 250)
  1000053004: User invalid (left company or does not exist)
  1000053005: Users limit 100 (more than 100 employees at a time)
  1000053006: Need user (no employees added)
  1000053007: Need name (name is empty)
```

### 使用说明

- **仅使用 user_access_token**：请使用 `X-Plugin-Token: {{user_access_token}}`；插件令牌无效。
- **name**：名称必须唯一，不能包含 "/" 或其他不支持的字符；最长长度为 250 个字符。
- **users**：用户键的列表；最多支持 100 个用户；无法添加已离职或不存在的用户。

---

## 更新用户组成员

更新用户组的成员信息。支持添加、删除或替换成员。支持操作空间成员（PROJECT_MEMBER）或自定义用户组（CUSTOMIZE）。

### 注意事项

**此 API 仅支持用户访问凭证（user_access_token）**。有关如何获取 user_access_token 的信息，请参阅 **meegle-api-credentials**。

- 当从非空间成员中添加用户时，该用户会自动成为空间成员。
- 当从空间成员中删除用户时，该用户也会从其他用户组中删除。

### 使用场景

- 向自定义用户组中添加或删除成员
- 更新用户组的完整成员列表
- 更新空间成员（PROJECT_MEMBER）或自定义用户组（CUSTOMIZE）的成员信息

### API 规范：update_user_group_member

```yaml
name: update_user_group_member
type: api
description: >
  Update the members of a user group. Supports add, delete, or replace members.
  Works with PROJECT_MEMBER or CUSTOMIZE user groups.

auth:
  type: user_access_token
  note: Only user_access_token is supported; plugin_access_token is NOT supported.

http:
  method: PATCH
  url: https://{domain}/open_api/{project_key}/user_group/members
  headers:
    Content-Type: application/json
    X-Plugin-Token: "{{user_access_token}}"

path_params:
  project_key:
    type: string
    required: true
    description: >
      Space ID (project_key) or space domain name (simple_name).
      project_key: Double-click space name in Meegle.
      simple_name: From space URL, e.g. https://meegle.com/doc/overview → doc.

inputs:
  user_group_type:
    type: string
    required: true
    enum: [PROJECT_MEMBER, CUSTOMIZE]
    description: |
      PROJECT_MEMBER: Space members
      CUSTOMIZE: Custom user groups
  user_group_id:
    type: string
    required: false
    description: >
      User group ID. Required when user_group_type=CUSTOMIZE.
      Obtain from user group page URL, e.g. .../userGroup/756472096042365xxxx → 756472096042365xxxx.
  add_users:
    type: array
    items: string
    required: false
    constraints:
      max_items: 100
    description: >
      List of user_keys to add. Max 100. Cannot add left/non-existent employees.
      At least one of add_users, delete_users, replace_users must be non-empty.
  delete_users:
    type: array
    items: string
    required: false
    constraints:
      max_items: 100
    description: >
      List of user_keys to delete. Max 100.
      If same user_key exists in add_users and delete_users, it is ignored.
      At least one of add_users, delete_users, replace_users must be non-empty.
  replace_users:
    type: array
    items: string
    required: false
    constraints:
      max_items: 100
    description: >
      Completely overwrite existing members. Max 100.
      If non-empty, add_users and delete_users are ignored.
      At least one of add_users, delete_users, replace_users must be non-empty.

outputs:
  data:
    type: object
    description: Empty object on success.

constraints:
  - Permission: Permission Management – Users
  - At least one of add_users, delete_users, replace_users must be non-empty
  - user_group_id required when user_group_type=CUSTOMIZE
  - Max 100 users per field (add_users, delete_users, replace_users)

error_mapping:
  1000053004: User invalid (employee left or does not exist)
  1000053005: Users limit 100 (more than 100 employees at a time)
  1000053008: User group type not supported (check user_group_type)
  1000053009: Need user group ID (user_group_id required when CUSTOMIZE)
  1000053006: Need user (add_users, delete_users, replace_users all empty)
  1000053010: User group not found (no matching user group in the space)
```

### 使用说明

- **仅使用 user_access_token**：请使用 `X-Plugin-Token: {{user_access_token}}`；插件令牌无效。
- **user_group_id**：当 `user_group_type` 为 CUSTOMIZE 时是必需的；该 ID 可通过用户组页面的 URL 获得。
- **replace_users** 参数优先级较高：如果提供了该参数，`add_users` 和 `delete_users` 的操作将被忽略。
- 如果 `add_users` 和 `delete_users` 中包含相同的 user_key，该 user_key 会被忽略。