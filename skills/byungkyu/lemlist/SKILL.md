---
name: lemlist
description: |
  Lemlist API integration with managed OAuth. Sales automation and cold outreach platform.
  Use this skill when users want to manage campaigns, leads, activities, schedules, or unsubscribes in Lemlist.
  For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
compatibility: Requires network access and valid Maton API key
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

# Lemlist

您可以使用受管理的 OAuth 认证来访问 Lemlist API。该 API 用于管理销售自动化和冷 Outreach 活动中的活动、潜在客户、日程安排、任务序列以及取消订阅等功能。

## 快速入门

```bash
# List campaigns
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/lemlist/api/campaigns')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/lemlist/api/{resource}
```

请将 `{resource}` 替换为实际的 Lemlist API 端点路径。该网关会将请求代理到 `api.lemlist.com/api`，并自动插入您的 OAuth 令牌。

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

您可以在 `https://ctrl.maton.ai` 上管理您的 Lemlist OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=lemlist&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'lemlist'}).encode()
req = urllib.request.Request('https://ctrl.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 获取连接信息

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "connection": {
    "connection_id": "3ecf268f-42ad-40cc-b77a-25e020fbf591",
    "status": "ACTIVE",
    "creation_time": "2026-02-12T02:00:53.023887Z",
    "last_updated_time": "2026-02-12T02:01:45.284131Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "lemlist",
    "metadata": {}
  }
}
```

在浏览器中打开返回的 `url` 以完成 OAuth 认证。

### 删除连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 指定连接

如果您有多个 Lemlist 连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/lemlist/api/campaigns')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '3ecf268f-42ad-40cc-b77a-25e020fbf591')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此字段，网关将使用默认的（最旧的）活动连接。

## API 参考

### 团队

#### 获取团队信息

```bash
GET /lemlist/api/team
```

返回团队信息，包括用户 ID 和设置。

#### 获取团队剩余信用

```bash
GET /lemlist/api/team/credits
```

返回团队的剩余信用余额。

#### 获取团队发送者

```bash
GET /lemlist/api/team/senders
```

返回所有团队成员及其关联的活动。

### 活动

#### 列出活动

```bash
GET /lemlist/api/campaigns
```

#### 创建活动

```bash
POST /lemlist/api/campaigns
Content-Type: application/json

{
  "name": "My Campaign"
}
```

创建一个新的活动，系统会自动添加一个空的任务序列和默认的日程安排。

#### 获取活动信息

```bash
GET /lemlist/api/campaigns/{campaignId}
```

#### 更新活动

```bash
PATCH /lemlist/api/campaigns/{campaignId}
Content-Type: application/json

{
  "name": "Updated Campaign Name"
}
```

#### 暂停活动

```bash
POST /lemlist/api/campaigns/{campaignId}/pause
```

暂停正在运行的活动。

### 活动序列

#### 获取活动序列

```bash
GET /lemlist/api/campaigns/{campaignId}/sequences
```

返回活动的所有任务序列和步骤。

### 活动日程安排

#### 获取活动日程安排

```bash
GET /lemlist/api/campaigns/{campaignId}/schedules
```

返回与活动关联的所有日程安排。

### 潜在客户

#### 将潜在客户添加到活动中

```bash
POST /lemlist/api/campaigns/{campaignId}/leads
Content-Type: application/json

{
  "email": "lead@example.com",
  "firstName": "John",
  "lastName": "Doe",
  "companyName": "Acme Inc"
}
```

创建一个新的潜在客户并将其添加到活动中。如果潜在客户已存在，系统会将其插入到相应的活动中。

#### 通过电子邮件获取潜在客户信息

```bash
GET /lemlist/api/leads/{email}
```

#### 更新活动中的潜在客户信息

```bash
PATCH /lemlist/api/campaigns/{campaignId}/leads/{email}
Content-Type: application/json

{
  "firstName": "Jane",
  "lastName": "Smith"
}
```

#### 从活动中删除潜在客户

```bash
DELETE /lemlist/api/campaigns/{campaignId}/leads/{email}
```

### 活动记录

#### 列出活动记录

```bash
GET /lemlist/api/activities
```

返回活动的历史记录（最近 100 条记录）。

查询参数：
- `campaignId` - 按活动进行过滤
- `type` - 按活动类型进行过滤（如：发送的邮件、打开的邮件、点击的邮件等）

### 日程安排

#### 列出日程安排

```bash
GET /lemlist/api/schedules
```

返回所有日程安排（支持分页）。

**响应：**
```json
{
  "schedules": [...],
  "pagination": {
    "totalRecords": 10,
    "currentPage": 1,
    "nextPage": 2,
    "totalPage": 2
  }
}
```

#### 创建日程安排

```bash
POST /lemlist/api/schedules
Content-Type: application/json

{
  "name": "Business Hours",
  "timezone": "America/New_York",
  "start": "09:00",
  "end": "17:00",
  "weekdays": [1, 2, 3, 4, 5]
}
```

工作日：0 = 星期日，1 = 星期一，...，6 = 星期六

#### 获取日程安排信息

```bash
GET /lemlist/api/schedules/{scheduleId}
```

#### 更新日程安排

```bash
PATCH /lemlist/api/schedules/{scheduleId}
Content-Type: application/json

{
  "name": "Updated Schedule",
  "start": "08:00",
  "end": "18:00"
}
```

#### 删除日程安排

```bash
DELETE /lemlist/api/schedules/{scheduleId}
```

### 公司

#### 列出公司信息

```bash
GET /lemlist/api/companies
```

返回公司的列表（支持分页）。

**响应：**
```json
{
  "data": [...],
  "total": 100
}
```

### 取消订阅

#### 列出取消订阅的信息

```bash
GET /lemlist/api/unsubscribes
```

返回所有已取消订阅的电子邮件地址和域名。

#### 添加取消订阅记录

```bash
POST /lemlist/api/unsubscribes
Content-Type: application/json

{
  "email": "unsubscribe@example.com"
}
```

也可以通过提供域名来添加取消订阅记录。

### 收件箱标签

#### 列出标签

```bash
GET /lemlist/api/inbox/labels
```

返回团队可用的所有标签。

## 分页

Lemlist 使用基于页面的分页机制，具体格式取决于端点：

**日程安排格式：**
```json
{
  "schedules": [...],
  "pagination": {
    "totalRecords": 100,
    "currentPage": 1,
    "nextPage": 2,
    "totalPage": 10
  }
}
```

**公司信息格式：**
```json
{
  "data": [...],
  "total": 100
}
```

## 代码示例

### JavaScript - 列出活动

```javascript
const response = await fetch(
  'https://gateway.maton.ai/lemlist/api/campaigns',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
const campaigns = await response.json();
console.log(campaigns);
```

### Python - 列出活动

```python
import os
import requests

response = requests.get(
    'https://gateway.maton.ai/lemlist/api/campaigns',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
)
campaigns = response.json()
for campaign in campaigns:
    print(f"{campaign['name']}: {campaign['_id']}")
```

### Python - 创建活动并添加潜在客户

```python
import os
import requests

headers = {'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
base_url = 'https://gateway.maton.ai/lemlist/api'

# Create campaign
campaign_response = requests.post(
    f'{base_url}/campaigns',
    headers=headers,
    json={'name': 'Q1 Outreach'}
)
campaign = campaign_response.json()
print(f"Created campaign: {campaign['_id']}")

# Add lead to campaign
lead_response = requests.post(
    f'{base_url}/campaigns/{campaign["_id"]}/leads',
    headers=headers,
    json={
        'email': 'prospect@example.com',
        'firstName': 'John',
        'lastName': 'Doe',
        'companyName': 'Acme Corp'
    }
)
lead = lead_response.json()
print(f"Added lead: {lead['_id']}")
```

## 注意事项

- 活动 ID 以 `cam_` 开头
- 潜在客户 ID 以 `lea_` 开头
- 日程安排 ID 以 `skd_` 开头
- 任务序列 ID 以 `seq_` 开头
- 团队 ID 以 `tea_` 开头
- 用户 ID 以 `usr_` 开头
- 活动无法通过 API 直接删除（只能暂停）
- 创建活动时，系统会自动添加一个空的任务序列和默认的日程安排
- 潜在客户的电子邮件地址用于标识操作对象
- 重要提示：当 URL 中包含括号时，使用 `curl -g` 命令可以避免全局解析问题
- 重要提示：将 curl 输出传递给 `jq` 时，环境变量可能无法正确解析。建议使用 Python 示例。

## 速率限制

| 操作 | 限制 |
|---------|------|
| API 调用 | 每个 API 密钥每 2 秒最多 20 次 |

当达到速率限制时，请使用指数退避策略进行重试。

## 错误处理

| 状态码 | 含义 |
|--------|--------|
| 400 | 请求错误或未建立 Lemlist 连接 |
| 401 | Maton API 密钥无效或缺失 |
| 404 | 资源未找到 |
| 405 | 不允许的方法 |
| 422 | 验证错误 |
| 429 | 速率限制 |
| 4xx/5xx | 来自 Lemlist API 的传递错误 |

### 故障排除：API 密钥问题

1. 确保设置了 `MATON_API_KEY` 环境变量：

```bash
echo $MATON_API_KEY
```

2. 通过列出连接来验证 API 密钥是否有效：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 故障排除：应用程序名称无效

1. 确保您的 URL 路径以 `lemlist` 开头。例如：
- 正确的格式：`https://gateway.maton.ai/lemlist/api/campaigns`
- 错误的格式：`https://gateway.maton.ai/api/campaigns`

## 资源

- [Lemlist API 文档](https://developer.lemlist.com/)
- [Lemlist API 参考](https://developer.lemlist.com/api-reference)
- [Lemlist 帮助中心 - API](https://help.lemlist.com/en/collections/17109856-api-webhooks)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)