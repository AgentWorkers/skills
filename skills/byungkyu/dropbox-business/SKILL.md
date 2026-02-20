---
name: dropbox-business
description: >
  **Dropbox Business API集成与托管式OAuth**  
  该功能支持管理员工、管理团队、团队文件夹、设备以及查看Dropbox Business团队的审计日志。  
  当用户需要管理Dropbox Business团队、添加或删除成员、创建新团队文件夹或访问审计日志时，可使用此功能。  
  对于其他第三方应用程序，请使用`api-gateway`功能（https://clawhub.ai/byungkyu/api-gateway）。  
  使用此功能需具备网络访问权限及有效的Maton API密钥。
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    homepage: "https://maton.ai"
    requires:
      env:
        - MATON_API_KEY
---
# Dropbox Business

您可以使用托管的 OAuth 认证来访问 Dropbox Business API。该 API 允许您管理团队相关设置，包括团队成员、组、团队文件夹、设备、关联的应用程序以及审计日志。

## 快速入门

```bash
# Get team info
python3 <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/dropbox-business/2/team/get_info', data=b'null', method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/dropbox-business/2/{endpoint-path}
```

请将 `{endpoint-path}` 替换为实际的 Dropbox Business API 端点路径。该代理会将请求转发到 `api.dropboxapi.com` 并自动插入您的 OAuth 令牌。

**重要提示：** Dropbox Business API 几乎所有的接口（包括读取操作）都使用 **POST** 方法。请求体应为 JSON 格式（对于没有参数的接口，可以使用 `null`）。

## 认证

所有请求都必须在 `Authorization` 头部包含 Maton API 密钥：

```
Authorization: Bearer $MATON_API_KEY
```

**环境变量：** 将您的 API 密钥设置为 `MATON_API_KEY`：

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### 获取 API 密钥

1. 在 [maton.ai](https://maton.ai) 上登录或创建账户。
2. 访问 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的 API 密钥。

## 连接管理

您可以在 `https://ctrl.maton.ai` 上管理您的 Dropbox Business OAuth 连接。

### 列出连接

```bash
python3 <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=dropbox-business&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python3 <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'dropbox-business'}).encode()
req = urllib.request.Request('https://ctrl.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "connection_id": "09062f57-98a9-49f2-9e63-b2a7e03a9d7a",
  "status": "PENDING",
  "url": "https://connect.maton.ai/?session_token=...",
  "app": "dropbox-business"
}
```

在浏览器中打开返回的 `url` 以完成 OAuth 认证。

### 删除连接

```bash
python3 <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
urllib.request.urlopen(req)
print("Deleted")
EOF
```

### 指定连接

如果您有多个 Dropbox Business 连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```python
req.add_header('Maton-Connection', '{connection_id}')
```

如果省略此字段，代理将使用默认的（最旧的）活动连接。

## API 参考

### 团队信息

#### 获取团队信息

检索有关团队的信息，包括许可证使用情况和政策设置。

```bash
POST /dropbox-business/2/team/get_info
Content-Type: application/json

null
```

**响应：**
```json
{
  "name": "My Company",
  "team_id": "dbtid:AAC...",
  "num_licensed_users": 10,
  "num_provisioned_users": 5,
  "num_used_licenses": 5,
  "policies": {
    "sharing": {...},
    "emm_state": {".tag": "disabled"},
    "office_addin": {".tag": "enabled"}
  }
}
```

#### 获取团队功能

```bash
POST /dropbox-business/2/team/features/get_values
Content-Type: application/json

{
  "features": [{".tag": "upload_api_rate_limit"}]
}
```

### 团队成员

#### 列出团队成员

```bash
POST /dropbox-business/2/team/members/list
Content-Type: application/json

{
  "limit": 100
}
```

**响应：**
```json
{
  "members": [
    {
      "profile": {
        "team_member_id": "dbmid:AAA...",
        "account_id": "dbid:AAC...",
        "email": "user@company.com",
        "email_verified": true,
        "status": {".tag": "active"},
        "name": {
          "given_name": "John",
          "surname": "Doe",
          "display_name": "John Doe"
        },
        "membership_type": {".tag": "full"},
        "joined_on": "2026-01-15T10:00:00Z"
      },
      "role": {".tag": "team_admin"}
    }
  ],
  "cursor": "AAQ...",
  "has_more": false
}
```

#### 继续列出成员

```bash
POST /dropbox-business/2/team/members/list/continue
Content-Type: application/json

{
  "cursor": "AAQ..."
}
```

#### 获取成员信息

```bash
POST /dropbox-business/2/team/members/get_info
Content-Type: application/json

{
  "members": [{".tag": "email", "email": "user@company.com"}]
}
```

**成员选择器示例：**
- `{".tag": "team_member_id", "team_member_id": "dbmid:AAA..."}`
- `{".tag": "external_id", "external_id": "..."}`

#### 添加成员

```bash
POST /dropbox-business/2/team/members/add
Content-Type: application/json

{
  "new_members": [
    {
      "member_email": "newuser@company.com",
      "member_given_name": "Jane",
      "member_surname": "Smith",
      "send_welcome_email": true,
      "role": {".tag": "member_only"}
    }
  ]
}
```

#### 暂停成员资格

```bash
POST /dropbox-business/2/team/members/suspend
Content-Type: application/json

{
  "user": {".tag": "email", "email": "user@company.com"},
  "wipe_data": false
}
```

#### 恢复成员资格

```bash
POST /dropbox-business/2/team/members/unsuspend
Content-Type: application/json

{
  "user": {".tag": "email", "email": "user@company.com"}
}
```

#### 删除成员

```bash
POST /dropbox-business/2/team/members/remove
Content-Type: application/json

{
  "user": {".tag": "email", "email": "user@company.com"},
  "wipe_data": true,
  "transfer_dest_id": {".tag": "email", "email": "admin@company.com"},
  "keep_account": false
}
```

### 组

#### 列出组

```bash
POST /dropbox-business/2/team/groups/list
Content-Type: application/json

{
  "limit": 100
}
```

**响应：**
```json
{
  "groups": [
    {
      "group_name": "Engineering",
      "group_id": "g:1d31f47b...",
      "member_count": 5,
      "group_management_type": {".tag": "company_managed"}
    }
  ],
  "cursor": "AAZ...",
  "has_more": false
}
```

#### 获取组信息

```bash
POST /dropbox-business/2/team/groups/get_info
Content-Type: application/json

{
  ".tag": "group_ids",
  "group_ids": ["g:1d31f47b..."]
}
```

#### 创建组

```bash
POST /dropbox-business/2/team/groups/create
Content-Type: application/json

{
  "group_name": "Marketing Team",
  "group_management_type": {".tag": "company_managed"}
}
```

#### 将成员添加到组

```bash
POST /dropbox-business/2/team/groups/members/add
Content-Type: application/json

{
  "group": {".tag": "group_id", "group_id": "g:1d31f47b..."},
  "members": [
    {
      "user": {".tag": "email", "email": "user@company.com"},
      "access_type": {".tag": "member"}
    }
  ],
  "return_members": true
}
```

#### 从组中删除成员

```bash
POST /dropbox-business/2/team/groups/members/remove
Content-Type: application/json

{
  "group": {".tag": "group_id", "group_id": "g:1d31f47b..."},
  "users": [{".tag": "email", "email": "user@company.com"}],
  "return_members": true
}
```

#### 删除组

```bash
POST /dropbox-business/2/team/groups/delete
Content-Type: application/json

{
  ".tag": "group_id",
  "group_id": "g:1d31f47b..."
}
```

### 团队文件夹

#### 列出团队文件夹

```bash
POST /dropbox-business/2/team/team_folder/list
Content-Type: application/json

{
  "limit": 100
}
```

**响应：**
```json
{
  "team_folders": [
    {
      "team_folder_id": "13646676387",
      "name": "Company Documents",
      "status": {".tag": "active"},
      "is_team_shared_dropbox": false,
      "sync_setting": {".tag": "default"}
    }
  ],
  "cursor": "AAb...",
  "has_more": false
}
```

#### 获取团队文件夹信息

```bash
POST /dropbox-business/2/team/team_folder/get_info
Content-Type: application/json

{
  "team_folder_ids": ["13646676387"]
}
```

#### 创建团队文件夹

```bash
POST /dropbox-business/2/team/team_folder/create
Content-Type: application/json

{
  "name": "New Team Folder",
  "sync_setting": {".tag": "default"}
}
```

#### 重命名团队文件夹

```bash
POST /dropbox-business/2/team/team_folder/rename
Content-Type: application/json

{
  "team_folder_id": "13646676387",
  "name": "Renamed Folder"
}
```

#### 将团队文件夹归档

```bash
POST /dropbox-business/2/team/team_folder/archive
Content-Type: application/json

{
  "team_folder_id": "13646676387",
  "force_async_off": false
}
```

#### 永久删除团队文件夹

```bash
POST /dropbox-business/2/team/team_folder/permanently_delete
Content-Type: application/json

{
  "team_folder_id": "13646676387"
}
```

### 命名空间

#### 列出命名空间

```bash
POST /dropbox-business/2/team/namespaces/list
Content-Type: application/json

{
  "limit": 100
}
```

**响应：**
```json
{
  "namespaces": [
    {
      "name": "Team Folder",
      "namespace_id": "13646676387",
      "namespace_type": {".tag": "team_folder"}
    },
    {
      "name": "Root",
      "namespace_id": "13646219987",
      "namespace_type": {".tag": "team_member_folder"},
      "team_member_id": "dbmid:AAA..."
    }
  ],
  "cursor": "AAY...",
  "has_more": false
}
```

### 设备

#### 列出所有成员的设备

```bash
POST /dropbox-business/2/team/devices/list_members_devices
Content-Type: application/json

{}
```

**响应：**
```json
{
  "devices": [
    {
      "team_member_id": "dbmid:AAA...",
      "web_sessions": [
        {
          "session_id": "dbwsid:...",
          "ip_address": "192.168.1.1",
          "country": "United States",
          "created": "2026-02-15T08:26:33Z",
          "user_agent": "Mozilla/5.0...",
          "os": "Mac OS X",
          "browser": "Chrome"
        }
      ],
      "desktop_clients": [],
      "mobile_clients": []
    }
  ],
  "has_more": false
}
```

#### 列出成员的设备

```bash
POST /dropbox-business/2/team/devices/list_member_devices
Content-Type: application/json

{
  "team_member_id": "dbmid:AAA..."
}
```

#### 取消设备会话

```bash
POST /dropbox-business/2/team/devices/revoke_device_session
Content-Type: application/json

{
  ".tag": "web_session",
  "session_id": "dbwsid:...",
  "team_member_id": "dbmid:AAA..."
}
```

### 关联的应用程序

#### 列出成员关联的应用程序

```bash
POST /dropbox-business/2/team/linked_apps/list_members_linked_apps
Content-Type: application/json

{}
```

**响应：**
```json
{
  "apps": [
    {
      "team_member_id": "dbmid:AAA...",
      "linked_api_apps": [
        {
          "app_id": "...",
          "app_name": "Third Party App",
          "linked": "2026-01-15T10:00:00Z"
        }
      ]
    }
  ],
  "has_more": false
}
```

#### 取消关联的应用程序

```bash
POST /dropbox-business/2/team/linked_apps/revoke_linked_app
Content-Type: application/json

{
  "app_id": "...",
  "team_member_id": "dbmid:AAA..."
}
```

### 审计日志（团队日志）

#### 获取事件记录

```bash
POST /dropbox-business/2/team_log/get_events
Content-Type: application/json

{
  "limit": 100,
  "category": {".tag": "members"}
}
```

**事件类别：**
- `apps` - 第三方应用程序事件
- `comments` - 评论事件
- `devices` - 设备事件
- `domains` - 域名事件
- `file_operations` - 文件和文件夹操作事件
- `file_requests` - 文件请求事件
- `groups` - 组事件
- `logins` - 登录事件
- `members` - 成员事件
- `paper` - Paper 文档事件
- `passwords` - 密码事件
- `reports` - 报告事件
- `sharing` - 共享事件
- `showcase` - 展示会话事件
- `sso` - 单点登录（SSO）事件
- `team_folders` - 团队文件夹事件
- `team_policies` - 政策事件
- `team_profile` - 团队资料事件
- `tfa` - 双因素认证事件

#### 继续获取事件记录

```bash
POST /dropbox-business/2/team_log/get_events/continue
Content-Type: application/json

{
  "cursor": "..."
}
```

## 分页

Dropbox Business 使用基于游标的分页机制。列表接口会返回 `cursor` 和 `has_more` 字段。

**初始请求：**
```bash
POST /dropbox-business/2/team/members/list
Content-Type: application/json

{
  "limit": 100
}
```

**响应：**
```json
{
  "members": [...],
  "cursor": "AAQ...",
  "has_more": true
}
```

**使用游标继续获取数据：**
```bash
POST /dropbox-business/2/team/members/list/continue
Content-Type: application/json

{
  "cursor": "AAQ..."
}
```

## 代码示例

### JavaScript

```javascript
async function listTeamMembers() {
  const response = await fetch(
    'https://gateway.maton.ai/dropbox-business/2/team/members/list',
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${process.env.MATON_API_KEY}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ limit: 100 })
    }
  );
  return await response.json();
}
```

### Python

```python
import os
import json
import urllib.request

def list_team_members():
    url = 'https://gateway.maton.ai/dropbox-business/2/team/members/list'
    data = json.dumps({'limit': 100}).encode()
    req = urllib.request.Request(url, data=data, method='POST')
    req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
    req.add_header('Content-Type', 'application/json')
    return json.load(urllib.request.urlopen(req))

def get_team_info():
    url = 'https://gateway.maton.ai/dropbox-business/2/team/get_info'
    req = urllib.request.Request(url, data=b'null', method='POST')
    req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
    req.add_header('Content-Type', 'application/json')
    return json.load(urllib.request.urlopen(req))
```

## 注意事项

- **所有请求均使用 POST 方法**：Dropbox Business API 几乎所有的接口（包括读取操作）都使用 POST 方法。
- **请求体必须为 JSON 格式**：即使没有参数的接口，也请发送 `null` 作为请求体。
- **字段标签格式**：许多字段使用 `.tag` 来标识字段类型（例如：`{"tag": "email", "email": "..."}`）。
- **成员选择器**：可以使用 `.tag` 与 `email`、`team_member_id` 或 `external_id` 来识别成员。
- **异步操作**：某些操作（如更改组成员信息）可能是异步的；请查看 `team/groups/job_status/get` 的响应状态。
- **重要提示**：当将 curl 输出传递给 `jq` 或其他命令时，在某些 shell 环境中，环境变量（如 `$MATON_API_KEY`）可能无法正确展开。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 请求错误或参数无效 |
| 401 | API 密钥无效或令牌已过期 |
| 403 | 没有权限（需要团队管理员权限） |
| 404 | 资源未找到 |
| 409 | 冲突（例如，成员已存在） |
| 429 | 请求频率限制 |
| 4xx/5xx | 来自 Dropbox API 的传递错误 |

### 响应错误格式

```json
{
  "error_summary": "member_not_found/...",
  "error": {
    ".tag": "member_not_found"
  }
}
```

## 资源

- [Dropbox Business API 文档](https://www.dropbox.com/developers/documentation/http/teams)
- [团队管理指南](https://developers.dropbox.com/dbx-team-administration-guide)
- [团队文件指南](https://developers.dropbox.com/dbx-team-files-guide)
- [认证类型](https://www.dropbox.com/developers/reference/auth-types)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)