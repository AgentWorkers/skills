---
name: mailgun
description: |
  Mailgun API integration with managed OAuth. Transactional email service for sending, receiving, and tracking emails.
  Use this skill when users want to send emails, manage domains, routes, templates, mailing lists, or suppressions in Mailgun.
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

# Mailgun

您可以使用管理的OAuth身份验证来访问Mailgun API。该API支持发送交易型电子邮件、管理域名、路由、模板、邮件列表、邮件抑制规则以及Webhook。

## 快速入门

```bash
# List domains
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/mailgun/v3/domains')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本URL

```
https://gateway.maton.ai/mailgun/v3/{resource}
```

请将 `{resource}` 替换为实际的Mailgun API端点路径。该代理会将请求转发到 `api.mailgun.net/v3`（美国地区），并自动插入您的OAuth令牌。

**区域说明：** Mailgun提供美国和欧盟两个区域。默认使用美国区域（api.mailgun.net）。

## 身份验证

所有请求都必须在 `Authorization` 头中包含Maton API密钥：

```
Authorization: Bearer $MATON_API_KEY
```

**环境变量：** 将您的API密钥设置为 `MATON_API_KEY`：

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### 获取API密钥

1. 在 [maton.ai](https://maton.ai) 上登录或创建账户。
2. 访问 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的API密钥。

## 连接管理

您可以在 `https://ctrl.maton.ai` 上管理您的Mailgun OAuth连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=mailgun&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'mailgun'}).encode()
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
    "connection_id": "78b5a036-c621-40c2-b74b-276195735af2",
    "status": "ACTIVE",
    "creation_time": "2026-02-12T02:24:16.551210Z",
    "last_updated_time": "2026-02-12T02:25:03.542838Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "mailgun",
    "metadata": {}
  }
}
```

在浏览器中打开返回的 `url` 以完成OAuth身份验证。

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

如果您有多个Mailgun连接，请使用 `Maton-Connection` 头来指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/mailgun/v3/domains')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '78b5a036-c621-40c2-b74b-276195735af2')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此头，代理将使用默认的（最旧的）活动连接。

## API参考

**重要提示：** Mailgun API在POST/PUT请求中使用 `application/x-www-form-urlencoded` 格式，而不是JSON。

### 域名

#### 列出域名

```bash
GET /mailgun/v3/domains
```

返回账户下的所有域名。

#### 获取域名信息

```bash
GET /mailgun/v3/domains/{domain_name}
```

#### 创建域名

```bash
POST /mailgun/v3/domains
Content-Type: application/x-www-form-urlencoded

name=example.com&smtp_password=supersecret
```

#### 删除域名

```bash
DELETE /mailgun/v3/domains/{domain_name}
```

### 消息

#### 发送邮件

```bash
POST /mailgun/v3/{domain_name}/messages
Content-Type: application/x-www-form-urlencoded

from=sender@example.com&to=recipient@example.com&subject=Hello&text=Hello World
```

参数：
- `from`（必填）- 发件人电子邮件地址
- `to`（必填）- 收件人地址（用逗号分隔）
- `cc` - 抄送收件人
- `bcc` - 密送收件人
- `subject`（必填）- 邮件主题
- `text` - 纯文本正文
- `html` - HTML正文
- `template` - 要使用的模板名称
- `o:tag` - 跟踪标签
- `o:tracking` - 启用/禁用跟踪（是/否）
- `o:tracking-clicks` - 启用点击跟踪
- `o:tracking-opens` - 启用打开跟踪
- `h:X-Custom-Header` - 自定义头部（前缀为 `h:`）
- `v:custom-var` - 模板中的自定义变量（前缀为 `v:`）

#### 发送MIME邮件

```bash
POST /mailgun/v3/{domain_name}/messages.mime
Content-Type: multipart/form-data

to=recipient@example.com&message=<MIME content>
```

### 事件

#### 列出事件

```bash
GET /mailgun/v3/{domain_name}/events
```

查询参数：
- `begin` - 开始时间（RFC 2822格式或Unix时间戳）
- `end` - 结束时间
- `ascending` - 排序方式（是/否）
- `limit` - 每页显示的结果数量（最多300条）
- `event` - 按事件类型过滤（已接受、已送达、失败、已打开、已点击、已取消订阅、已投诉、已存储）
- `from` - 按发件人过滤
- `to` - 按收件人过滤
- `tags` - 按标签过滤

### 路由

路由是针对整个账户全局定义的，而不是针对每个域名定义的。

#### 列出路由

```bash
GET /mailgun/v3/routes
```

查询参数：
- `skip` - 要跳过的记录数
- `limit` - 返回的记录数

#### 创建路由

```bash
POST /mailgun/v3/routes
Content-Type: application/x-www-form-urlencoded

priority=0&description=My Route&expression=match_recipient(".*@example.com")&action=forward("https://example.com/webhook")
```

参数：
- `priority` - 路由优先级（优先级越低，优先级越高）
- `description` - 路由描述
- `expression` - 过滤条件（match_recipient、match_header、catch_all）
- `action` - 要执行的操作（转发、存储、停止）

#### 获取路由信息

```bash
GET /mailgun/v3/routes/{route_id}
```

#### 更新路由

```bash
PUT /mailgun/v3/routes/{route_id}
Content-Type: application/x-www-form-urlencoded

priority=1&description=Updated Route
```

#### 删除路由

```bash
DELETE /mailgun/v3/routes/{route_id}
```

### Webhook

#### 列出Webhook

```bash
GET /mailgun/v3/domains/{domain_name}/webhooks
```

#### 创建Webhook

```bash
POST /mailgun/v3/domains/{domain_name}/webhooks
Content-Type: application/x-www-form-urlencoded

id=delivered&url=https://example.com/webhook
```

Webhook类型：`accepted`、`delivered`、`opened`、`clicked`、`unsubscribed`、`complained`、`permanent_fail`、`temporary_fail`

#### 获取Webhook信息

```bash
GET /mailgun/v3/domains/{domain_name}/webhooks/{webhook_type}
```

#### 更新Webhook

```bash
PUT /mailgun/v3/domains/{domain_name}/webhooks/{webhook_type}
Content-Type: application/x-www-form-urlencoded

url=https://example.com/new-webhook
```

#### 删除Webhook

```bash
DELETE /mailgun/v3/domains/{domain_name}/webhooks/{webhook_type}
```

### 模板

#### 列出模板

```bash
GET /mailgun/v3/{domain_name}/templates
```

#### 创建模板

```bash
POST /mailgun/v3/{domain_name}/templates
Content-Type: application/x-www-form-urlencoded

name=my-template&description=Welcome email&template=<html><body>Hello {{name}}</body></html>
```

#### 获取模板信息

```bash
GET /mailgun/v3/{domain_name}/templates/{template_name}
```

#### 删除模板

```bash
DELETE /mailgun/v3/{domain_name}/templates/{template_name}
```

### 邮件列表

#### 列出邮件列表

```bash
GET /mailgun/v3/lists/pages
```

#### 创建邮件列表

```bash
POST /mailgun/v3/lists
Content-Type: application/x-www-form-urlencoded

address=newsletter@example.com&name=Newsletter&description=Monthly newsletter&access_level=readonly
```

访问权限：`readonly`、`members`、`everyone`

#### 获取邮件列表信息

```bash
GET /mailgun/v3/lists/{list_address}
```

#### 更新邮件列表

```bash
PUT /mailgun/v3/lists/{list_address}
Content-Type: application/x-www-form-urlencoded

name=Updated Newsletter
```

#### 删除邮件列表

```bash
DELETE /mailgun/v3/lists/{list_address}
```

### 邮件列表成员

#### 列出成员

```bash
GET /mailgun/v3/lists/{list_address}/members/pages
```

#### 添加成员

```bash
POST /mailgun/v3/lists/{list_address}/members
Content-Type: application/x-www-form-urlencoded

address=member@example.com&name=John Doe&subscribed=yes
```

#### 获取成员信息

```bash
GET /mailgun/v3/lists/{list_address}/members/{member_address}
```

#### 更新成员信息

```bash
PUT /mailgun/v3/lists/{list_address}/members/{member_address}
Content-Type: application/x-www-form-urlencoded

name=Jane Doe&subscribed=no
```

#### 删除成员

```bash
DELETE /mailgun/v3/lists/{list_address}/members/{member_address}
```

### 邮件抑制规则

#### 处理邮件退回

```bash
# List bounces
GET /mailgun/v3/{domain_name}/bounces

# Add bounce
POST /mailgun/v3/{domain_name}/bounces
Content-Type: application/x-www-form-urlencoded

address=bounced@example.com&code=550&error=Mailbox not found

# Get bounce
GET /mailgun/v3/{domain_name}/bounces/{address}

# Delete bounce
DELETE /mailgun/v3/{domain_name}/bounces/{address}
```

#### 取消订阅

```bash
# List unsubscribes
GET /mailgun/v3/{domain_name}/unsubscribes

# Add unsubscribe
POST /mailgun/v3/{domain_name}/unsubscribes
Content-Type: application/x-www-form-urlencoded

address=unsubscribed@example.com&tag=*

# Delete unsubscribe
DELETE /mailgun/v3/{domain_name}/unsubscribes/{address}
```

#### 处理投诉

```bash
# List complaints
GET /mailgun/v3/{domain_name}/complaints

# Add complaint
POST /mailgun/v3/{domain_name}/complaints
Content-Type: application/x-www-form-urlencoded

address=complainer@example.com

# Delete complaint
DELETE /mailgun/v3/{domain_name}/complaints/{address}
```

#### 白名单

```bash
# List whitelists
GET /mailgun/v3/{domain_name}/whitelists

# Add to whitelist
POST /mailgun/v3/{domain_name}/whitelists
Content-Type: application/x-www-form-urlencoded

address=allowed@example.com

# Delete from whitelist
DELETE /mailgun/v3/{domain_name}/whitelists/{address}
```

### 统计数据

#### 获取统计信息

```bash
GET /mailgun/v3/{domain_name}/stats/total?event=delivered&event=opened
```

查询参数：
- `event`（必填）- 事件类型：已接受、已送达、失败、已打开、已点击、已取消订阅、已投诉
- `start` - 开始日期（RFC 2822格式或Unix时间戳）
- `end` - 结束日期
- `resolution` - 数据显示周期（小时、天、月）
- `duration` - 显示统计数据的期间

### 标签

#### 列出标签

```bash
GET /mailgun/v3/{domain_name}/tags
```

#### 获取标签信息

```bash
GET /mailgun/v3/{domain_name}/tags/{tag_name}
```

#### 删除标签

```bash
DELETE /mailgun/v3/{domain_name}/tags/{tag_name}
```

### IP地址

#### 列出IP地址

```bash
GET /mailgun/v3/ips
```

#### 获取IP地址信息

```bash
GET /mailgun/v3/ips/{ip_address}
```

### 域名跟踪

#### 获取跟踪设置

```bash
GET /mailgun/v3/domains/{domain_name}/tracking
```

#### 更新打开跟踪设置

```bash
PUT /mailgun/v3/domains/{domain_name}/tracking/open
Content-Type: application/x-www-form-urlencoded

active=yes
```

#### 更新点击跟踪设置

```bash
PUT /mailgun/v3/domains/{domain_name}/tracking/click
Content-Type: application/x-www-form-urlencoded

active=yes
```

#### 更新取消订阅跟踪设置

```bash
PUT /mailgun/v3/domains/{domain_name}/tracking/unsubscribe
Content-Type: application/x-www-form-urlencoded

active=yes&html_footer=<a href="%unsubscribe_url%">Unsubscribe</a>
```

### 凭据

#### 列出凭据

```bash
GET /mailgun/v3/domains/{domain_name}/credentials
```

#### 创建凭据

```bash
POST /mailgun/v3/domains/{domain_name}/credentials
Content-Type: application/x-www-form-urlencoded

login=alice&password=supersecret
```

#### 删除凭据

```bash
DELETE /mailgun/v3/domains/{domain_name}/credentials/{login}
```

## 分页

Mailgun使用基于游标的分页机制：

```json
{
  "items": [...],
  "paging": {
    "first": "https://api.mailgun.net/v3/.../pages?page=first&limit=100",
    "last": "https://api.mailgun.net/v3/.../pages?page=last&limit=100",
    "next": "https://api.mailgun.net/v3/.../pages?page=next&limit=100",
    "previous": "https://api.mailgun.net/v3/.../pages?page=prev&limit=100"
  }
}
```

使用 `limit` 参数来控制页面大小（默认值为100条）。

## 代码示例

### JavaScript - 发送电子邮件

```javascript
const formData = new URLSearchParams();
formData.append('from', 'sender@example.com');
formData.append('to', 'recipient@example.com');
formData.append('subject', 'Hello');
formData.append('text', 'Hello World!');

const response = await fetch(
  'https://gateway.maton.ai/mailgun/v3/example.com/messages',
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`,
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: formData.toString()
  }
);
const result = await response.json();
console.log(result);
```

### Python - 发送电子邮件

```python
import os
import requests

response = requests.post(
    'https://gateway.maton.ai/mailgun/v3/example.com/messages',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    data={
        'from': 'sender@example.com',
        'to': 'recipient@example.com',
        'subject': 'Hello',
        'text': 'Hello World!'
    }
)
print(response.json())
```

### Python - 列出域名

```python
import os
import requests

response = requests.get(
    'https://gateway.maton.ai/mailgun/v3/domains',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
)
domains = response.json()
for domain in domains['items']:
    print(f"{domain['name']}: {domain['state']}")
```

### Python - 创建路由和Webhook

```python
import os
import requests

headers = {'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
domain = 'example.com'

# Create route
route_response = requests.post(
    'https://gateway.maton.ai/mailgun/v3/routes',
    headers=headers,
    data={
        'priority': 0,
        'description': 'Forward to webhook',
        'expression': 'match_recipient("support@example.com")',
        'action': 'forward("https://myapp.com/incoming-email")'
    }
)
print(f"Route created: {route_response.json()}")

# Create webhook
webhook_response = requests.post(
    f'https://gateway.maton.ai/mailgun/v3/domains/{domain}/webhooks',
    headers=headers,
    data={
        'id': 'delivered',
        'url': 'https://myapp.com/webhook/delivered'
    }
)
print(f"Webhook created: {webhook_response.json()}")
```

## 注意事项

- Mailgun在POST/PUT请求中使用 `application/x-www-form-urlencoded` 格式，而不是JSON。
- 大多数端点路径中必须包含域名。
- 路由是针对整个账户全局定义的，而不是针对每个域名。
- 沙箱域名在发送邮件时需要授权的收件人。
- 日期以RFC 2822格式返回。
- 事件日志至少保存3天。
- 统计数据需要至少提供一个 `event` 参数。
- 模板默认使用Handlebars语法。
- **重要提示：** 当URL包含括号时，使用 `curl -g` 选项来禁用全局解析。
- **重要提示：** 当将curl输出传递给 `jq` 时，环境变量可能无法正确解析。建议使用Python示例。

## 速率限制

| 操作 | 限制 |
|---------|-------|
| 发送邮件 | 根据套餐不同而有所差异 |
| API调用 | 没有硬性限制，但过多的请求可能会被限制 |

当遇到速率限制时，请实施指数级退避策略进行重试。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 请求错误或未建立Mailgun连接 |
| 401 | Maton API密钥无效或缺失 |
| 403 | 被禁止（例如，由于沙箱域名限制） |
| 404 | 资源未找到 |
| 429 | 达到速率限制 |
| 4xx/5xx | 来自Mailgun API的传递错误 |

### 故障排除：API密钥问题

1. 确保设置了 `MATON_API_KEY` 环境变量：

```bash
echo $MATON_API_KEY
```

2. 通过列出连接来验证API密钥是否有效：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 故障排除：应用名称无效

1. 确保您的URL路径以 `mailgun` 开头。例如：
- 正确：`https://gateway.maton.ai/mailgun/v3/domains`
- 错误：`https://gateway.maton.ai/v3/domains`

### 故障排除：沙箱域名限制

沙箱域名只能发送给授权的收件人。要发送邮件，请：
1. 升级到付费套餐，或
2. 在Mailgun控制台中将收件人地址添加到授权收件人列表中。

## 资源

- [Mailgun API文档](https://documentation.mailgun.com/docs/mailgun/api-reference/api-overview)
- [Mailgun API参考](https://mailgun-docs.redoc.ly/docs/mailgun/api-reference/intro/)
- [Mailgun Postman集合](https://www.postman.com/mailgun/mailgun-s-public-workspace/documentation/ik8dl61/mailgun-api)
- [Maton社区](https://discord.com/invite/dBfFAcefs2)
- [Maton支持](mailto:support@maton.ai)