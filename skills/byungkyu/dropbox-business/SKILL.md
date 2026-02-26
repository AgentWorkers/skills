---
name: dropbox-business
description: >
  Dropbox Business API集成支持管理OAuth认证机制，可用于管理Dropbox Business团队的成员、组、团队文件夹以及审计日志。  
  当用户需要管理员工、创建团队、处理团队文件夹或查看审计日志时，可以使用此功能。  
  对于其他第三方应用程序，建议使用`api-gateway`功能（https://clawhub.ai/byungkyu/api-gateway）。  
  使用此功能需要网络连接以及有效的Maton API密钥。
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

您可以使用托管的 OAuth 认证来访问 Dropbox Business API。该 API 允许您管理团队相关设置，包括成员、组、团队文件夹、设备、关联的应用程序以及审计日志。

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

**重要提示：** Dropbox Business API 几乎所有的端点（包括读取操作）都使用 **POST** 方法。请求体应为 JSON 格式（对于没有参数的端点，请使用 `null`）。

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
2. 转到 [maton.ai/settings](https://maton.ai/settings)。
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

查询团队功能的可用性。

```bash
POST /dropbox-business/2/team/features/get_values
Content-Type: application/json

{
  "features": [
    {".tag": "upload_api_rate_limit"},
    {".tag": "has_team_shared_dropbox"},
    {".tag": "has_team_file_events"},
    {".tag": "has_team_selective_sync"}
  ]
}
```

**响应：**
```json
{
  "values": [
    {".tag": "upload_api_rate_limit", "upload_api_rate_limit": {".tag": "limit", "limit": 1000000000}},
    {".tag": "has_team_shared_dropbox", "has_team_shared_dropbox": {".tag": "has_team_shared_dropbox", "has_team_shared_dropbox": false}},
    {".tag": "has_team_file_events", "has_team_file_events": {".tag": "enabled", "enabled": true}},
    {".tag": "has_team_selective_sync", "has_team_selective_sync": {".tag": "has_team_selective_sync", "has_team_selective_sync": true}}
  ]
}
```

#### 获取当前登录的管理员信息

获取当前登录的管理员的相关信息。

```bash
POST /dropbox-business/2/team/token/get_authenticated_admin
Content-Type: application/json

null
```

**响应：**
```json
{
  "admin_profile": {
    "team_member_id": "dbmid:AAA...",
    "account_id": "dbid:AAC...",
    "email": "admin@company.com",
    "email_verified": true,
    "status": {".tag": "active"},
    "name": {"given_name": "Admin", "surname": "User", "display_name": "Admin User"},
    "membership_type": {".tag": "full"},
    "joined_on": "2026-02-15T08:27:35Z"
  }
}
```

### 团队成员

#### 列出成员

```bash
POST /dropbox-business/2/team/members/list
Content-Type: application/json

{
  "limit": 100
}
```

#### 列出成员（V2）

返回包含成员角色信息的成员列表（推荐使用）。

```bash
POST /dropbox-business/2/team/members/list_v2
Content-Type: application/json

{
  "limit": 100,
  "include_removed": false
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
        "secondary_emails": [],
        "status": {".tag": "active"},
        "name": {
          "given_name": "John",
          "surname": "Doe",
          "familiar_name": "John",
          "display_name": "John Doe",
          "abbreviated_name": "JD"
        },
        "membership_type": {".tag": "full"},
        "joined_on": "2026-01-15T10:00:00Z",
        "groups": ["g:1d31f47b..."],
        "member_folder_id": "13646219987",
        "root_folder_id": "13650024947"
      },
      "roles": [
        {
          "role_id": "pid_dbtmr:...",
          "name": "Team",
          "description": "Manage everything and access all permissions"
        }
      ]
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

#### 获取成员信息（V2）

返回包含成员角色信息的成员列表（推荐使用）。

**响应：**
```bash
POST /dropbox-business/2/team/members/get_info_v2
Content-Type: application/json

{
  "members": [{".tag": "email", "email": "user@company.com"}]
}
```

**成员筛选条件：**
- `{".tag": "email", "email": "user@company.com"}`
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
  "transfer_admin_id": {".tag": "email", "email": "admin@company.com"},
  "keep_account": false
}
```

#### 检查删除操作的状态

```bash
POST /dropbox-business/2/team/members/remove/job_status/get
Content-Type: application/json

{
  "async_job_id": "dbjid:..."
}
```

#### 发送欢迎邮件

向待处理的成员发送或重新发送欢迎邮件。

```bash
POST /dropbox-business/2/team/members/send_welcome_email
Content-Type: application/json

{".tag": "email", "email": "pending@company.com"}
```

#### 设置成员资料（V2）

更新成员的资料信息。

```bash
POST /dropbox-business/2/team/members/set_profile_v2
Content-Type: application/json

{
  "user": {".tag": "team_member_id", "team_member_id": "dbmid:AAA..."},
  "new_given_name": "John",
  "new_surname": "Smith",
  "new_external_id": "emp-123"
}
```

#### 删除资料照片（V2）

```bash
POST /dropbox-business/2/team/members/delete_profile_photo_v2
Content-Type: application/json

{
  "user": {".tag": "team_member_id", "team_member_id": "dbmid:AAA..."}
}
```

#### 设置资料照片（V2）

```bash
POST /dropbox-business/2/team/members/set_profile_photo_v2
Content-Type: application/json

{
  "user": {".tag": "team_member_id", "team_member_id": "dbmid:AAA..."},
  "photo": {".tag": "base64_data", "base64_data": "<base64-encoded-image>"}
}
```

#### 设置管理员权限（V2）

更改成员的管理员角色。

```bash
POST /dropbox-business/2/team/members/set_admin_permissions_v2
Content-Type: application/json

{
  "user": {".tag": "email", "email": "user@company.com"},
  "new_roles": ["pid_dbtmr:..."]
}
```

### 副本电子邮件

#### 添加副本电子邮件

```bash
POST /dropbox-business/2/team/members/secondary_emails/add
Content-Type: application/json

{
  "new_secondary_emails": [
    {
      "user": {".tag": "email", "email": "user@company.com"},
      "secondary_emails": ["alias@company.com"]
    }
  ]
}
```

#### 删除副本电子邮件

```bash
POST /dropbox-business/2/team/members/secondary_emails/delete
Content-Type: application/json

{
  "emails_to_delete": [
    {
      "user": {".tag": "email", "email": "user@company.com"},
      "secondary_emails": ["alias@company.com"]
    }
  ]
}
```

#### 重新发送验证邮件

```bash
POST /dropbox-business/2/team/members/secondary_emails/resend_verification_emails
Content-Type: application/json

{
  "emails_to_resend": [
    {
      "user": {".tag": "email", "email": "user@company.com"},
      "secondary_emails": ["alias@company.com"]
    }
  ]
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

#### 从组中移除成员

```bash
POST /dropbox-business/2/team/groups/members/remove
Content-Type: application/json

{
  "group": {".tag": "group_id", "group_id": "g:1d31f47b..."},
  "users": [{".tag": "email", "email": "user@company.com"}],
  "return_members": true
}
```

#### 列出组成员

```bash
POST /dropbox-business/2/team/groups/members/list
Content-Type: application/json

{
  "group": {".tag": "group_id", "group_id": "g:1d31f47b..."},
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
        "email": "user@company.com",
        "status": {".tag": "active"},
        "name": {...}
      },
      "access_type": {".tag": "member"}
    }
  ],
  "cursor": "...",
  "has_more": false
}
```

#### 更新组信息

```bash
POST /dropbox-business/2/team/groups/update
Content-Type: application/json

{
  "group": {".tag": "group_id", "group_id": "g:1d31f47b..."},
  "new_group_name": "Updated Name",
  "new_group_external_id": "ext-123"
}
```

**注意：** 系统管理的组（如 “Everyone at...”）无法被修改或删除。

#### 删除组

```bash
POST /dropbox-business/2/team/groups/delete
Content-Type: application/json

{
  ".tag": "group_id",
  "group_id": "g:1d31f47b..."
}
```

#### 检查组操作的状态

用于异步组操作。

```bash
POST /dropbox-business/2/team/groups/job_status/get
Content-Type: application/json

{
  "async_job_id": "dbjid:..."
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

#### 激活归档的团队文件夹

```bash
POST /dropbox-business/2/team/team_folder/activate
Content-Type: application/json

{
  "team_folder_id": "13646676387"
}
```

#### 更新同步设置

```bash
POST /dropbox-business/2/team/team_folder/update_sync_settings
Content-Type: application/json

{
  "team_folder_id": "13646676387",
  "sync_setting": {".tag": "default"}
}
```

**响应：**
```json
{
  "team_folder_id": "13646676387",
  "name": "Team Folder",
  "status": {".tag": "active"},
  "is_team_shared_dropbox": false,
  "sync_setting": {".tag": "default"},
  "content_sync_settings": []
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

#### 批量取消设备会话

```bash
POST /dropbox-business/2/team/devices/revoke_device_session_batch
Content-Type: application/json

{
  "revoke_devices": [
    {".tag": "web_session", "session_id": "dbwsid:...", "team_member_id": "dbmid:AAA..."}
  ]
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

#### 列出所有团队关联的应用程序

```bash
POST /dropbox-business/2/team/linked_apps/list_team_linked_apps
Content-Type: application/json

{}
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

### 成员的空间限制

#### 获取自定义配额

```bash
POST /dropbox-business/2/team/member_space_limits/get_custom_quota
Content-Type: application/json

{
  "users": [{".tag": "email", "email": "user@company.com"}]
}
```

#### 设置自定义配额

```bash
POST /dropbox-business/2/team/member_space_limits/set_custom_quota
Content-Type: application/json

{
  "users_and_quotas": [
    {
      "user": {".tag": "email", "email": "user@company.com"},
      "quota_gb": 100
    }
  ]
}
```

#### 列出被排除在自动备份之外的用户

```bash
POST /dropbox-business/2/team/member_space_limits/excluded_users/list
Content-Type: application/json

{}
```

### 共享允许列表

#### 列出共享允许列表

```bash
POST /dropbox-business/2/team/sharing_allowlist/list
Content-Type: application/json

{}
```

**响应：**
```json
{
  "domains": [],
  "emails": [],
  "cursor": "...",
  "has_more": false
}
```

#### 将用户添加到共享允许列表

```bash
POST /dropbox-business/2/team/sharing_allowlist/add
Content-Type: application/json

{
  "domains": ["partner.com"],
  "emails": ["external@client.com"]
}
```

#### 继续列出允许列表

```bash
POST /dropbox-business/2/team/sharing_allowlist/list/continue
Content-Type: application/json

{
  "cursor": "..."
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
- `showcase` - Showcase 文档事件
- `sso` - SSO（单点登录）事件
- `team_folders` - 团队文件夹事件
- `team_policies` - 团队政策事件
- `team_profile` - 团队资料事件
- `tfa` - 两步验证事件

#### 继续获取事件记录

```bash
POST /dropbox-business/2/team_log/get_events/continue
Content-Type: application/json

{
  "cursor": "..."
}
```

## 成员文件访问

要代表团队成员访问文件，请使用 `Dropbox-API-Select-User` 头部，并传入成员的 `team_member_id`。这允许管理员应用程序访问成员的文件、共享文件夹和文件请求。

### 列出成员的文件

```bash
python3 <<'EOF'
import urllib.request, os, json
data = json.dumps({"path": ""}).encode()
req = urllib.request.Request('https://gateway.maton.ai/dropbox-business/2/files/list_folder', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
req.add_header('Dropbox-API-Select-User', 'dbmid:AAA...')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 列出成员共享的文件夹

```bash
python3 <<'EOF'
import urllib.request, os, json
data = json.dumps({}).encode()
req = urllib.request.Request('https://gateway.maton.ai/dropbox-business/2/sharing/list_folders', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
req.add_header('Dropbox-API-Select-User', 'dbmid:AAA...')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 列出成员的文件请求

```bash
python3 <<'EOF'
import urllib.request, os, json
data = json.dumps({}).encode()
req = urllib.request.Request('https://gateway.maton.ai/dropbox-business/2/file_requests/list_v2', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
req.add_header('Dropbox-API-Select-User', 'dbmid:AAA...')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**注意：** `Dropbox-API-Select-User` 头部需要 `team_data.member` 权限范围。使用此头部可以代表团队成员操作用户级别的端点（文件、共享等）。

## 分页

Dropbox Business 使用基于游标的分页机制。列表端点会返回 `cursor` 和 `has_more` 字段。

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

**使用游标继续查询：**
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

- **所有请求都使用 POST 方法**：Dropbox Business API 几乎所有的端点（包括读取操作）都使用 POST 方法。
- **请求体必须是 JSON 格式**：即使没有参数的端点，也要发送 `null` 作为请求体。
- **字段标签格式**：许多字段使用 `.tag` 来表示类型（例如，`{"tag": "email", "email": "..."}`）。
- **成员筛选条件**：使用 `.tag` 与 `email`、`team_member_id` 或 `external_id` 来识别成员。
- **异步操作**：某些操作（如更改组成员或删除成员）可能是异步的；请检查相应的 `job_status` 端点。
- **Select-User 头部**：使用 `Dropbox-API-Select-User` 和 `team_member_id` 来代表成员访问用户级别的端点（文件、共享等）。
- **系统管理的组**：像 “Everyone at...” 这样的组是由系统管理的，无法被修改或删除。
- **使用 V2 版本的端点**：使用 V2 版本的端点（例如 `members/list_v2`、`members/get_info_v2`）以获取包含角色信息的更详细响应。
- **已弃用的端点**：`team/reports/get_activity`、`get_devices`、`get_membership`、`get_storage` 等端点已被弃用。
- **重要提示**：当将 curl 输出传递给 `jq` 或其他命令时，在某些 shell 环境中，环境变量 `$MATON_API_KEY` 可能无法正确解析。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 请求错误或参数无效 |
| 401 | API 密钥无效或令牌过期 |
| 403 | 没有权限（需要团队管理员权限） |
| 404 | 资源未找到 |
| 409 | 冲突（例如，成员已存在） |
| 429 | 请求次数受限 |
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