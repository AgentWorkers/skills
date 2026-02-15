---
name: signnow
description: |
  SignNow API integration with managed OAuth. E-signature platform for sending, signing, and managing documents.
  Use this skill when users want to upload documents, send signature invites, create templates, or manage e-signature workflows.
  For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
  Requires network access and valid Maton API key.
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    requires:
      env:
        - MATON_API_KEY
---

# SignNow

使用管理的OAuth认证来访问SignNow API。您可以上传文件、发送签名邀请、管理模板，并自动化电子签名工作流程。

## 快速入门

```bash
# Get current user info
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/signnow/user')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本URL

```
https://gateway.maton.ai/signnow/{resource}
```

该网关会将请求代理到`api.signnow.com`，并自动插入您的OAuth令牌。

## 认证

所有请求都需要在`Authorization`头部包含Maton API密钥：

```
Authorization: Bearer $MATON_API_KEY
```

**环境变量：** 将您的API密钥设置为`MATON_API_KEY`：

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### 获取API密钥

1. 在[maton.ai](https://maton.ai)登录或创建账户。
2. 访问[maton.ai/settings](https://maton.ai/settings)。
3. 复制您的API密钥。

## 连接管理

您可以在`https://ctrl.maton.ai`管理您的SignNow OAuth连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=signnow&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'signnow'}).encode()
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
    "connection_id": "5ff5474b-5f21-41ba-8bf3-afb33cce5a75",
    "status": "ACTIVE",
    "creation_time": "2026-02-08T20:47:23.019763Z",
    "last_updated_time": "2026-02-08T20:50:32.210896Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "signnow",
    "metadata": {}
  }
}
```

在浏览器中打开返回的`url`以完成OAuth认证。

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

如果您有多个SignNow连接，请使用`Maton-Connection`头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/signnow/user')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '5ff5474b-5f21-41ba-8bf3-afb33cce5a75')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略，则网关将使用默认的（最旧的）活动连接。

## API参考

### 用户操作

#### 获取当前用户

```bash
GET /signnow/user
```

**响应：**
```json
{
  "id": "59cce130e93a4e9488522ca67e3a6779f3e48a72",
  "first_name": "Chris",
  "last_name": "Kim",
  "active": "1",
  "verified": true,
  "emails": ["chris@example.com"],
  "primary_email": "chris@example.com",
  "document_count": 0,
  "subscriptions": [...],
  "teams": [...],
  "organization": {...}
}
```

#### 获取用户文档

```bash
GET /signnow/user/documents
```

**响应：**
```json
[
  {
    "id": "c63a7bc73f03449c987bf0feaa36e96212408352",
    "document_name": "Contract",
    "page_count": "3",
    "created": "1770598603",
    "updated": "1770598603",
    "original_filename": "contract.pdf",
    "owner": "chris@example.com",
    "template": false,
    "roles": [],
    "field_invites": [],
    "signatures": []
  }
]
```

### 文档操作

#### 上传文档

文档必须以multipart表单数据的形式上传，且文件格式应为PDF：

```bash
python <<'EOF'
import urllib.request, os, json

def encode_multipart_formdata(files):
    boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
    lines = []
    for (key, filename, content) in files:
        lines.append(f'--{boundary}'.encode())
        lines.append(f'Content-Disposition: form-data; name="{key}"; filename="{filename}"'.encode())
        lines.append(b'Content-Type: application/pdf')
        lines.append(b'')
        lines.append(content)
    lines.append(f'--{boundary}--'.encode())
    lines.append(b'')
    body = b'\r\n'.join(lines)
    content_type = f'multipart/form-data; boundary={boundary}'
    return content_type, body

with open('document.pdf', 'rb') as f:
    file_content = f.read()

content_type, body = encode_multipart_formdata([('file', 'document.pdf', file_content)])
req = urllib.request.Request('https://gateway.maton.ai/signnow/document', data=body, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', content_type)
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "id": "c63a7bc73f03449c987bf0feaa36e96212408352"
}
```

#### 获取文档

```bash
GET /signnow/document/{document_id}
```

**响应：**
```json
{
  "id": "c63a7bc73f03449c987bf0feaa36e96212408352",
  "document_name": "Contract",
  "page_count": "3",
  "created": "1770598603",
  "updated": "1770598603",
  "original_filename": "contract.pdf",
  "owner": "chris@example.com",
  "template": false,
  "roles": [],
  "viewer_roles": [],
  "attachments": [],
  "fields": [],
  "signatures": [],
  "texts": [],
  "checks": []
}
```

#### 更新文档

```bash
PUT /signnow/document/{document_id}
Content-Type: application/json

{
  "document_name": "Updated Contract Name"
}
```

**响应：**
```json
{
  "id": "c63a7bc73f03449c987bf0feaa36e96212408352",
  "signatures": [],
  "texts": [],
  "checks": []
}
```

#### 下载文档

```bash
GET /signnow/document/{document_id}/download?type=collapsed
```

以二进制数据形式返回PDF文件。
- `type` 参数：`collapsed`（扁平化的PDF），`zip`（所有页面作为图片）

#### 获取文档历史记录

```bash
GET /signnow/document/{document_id}/historyfull
```

**响应：**
```json
[
  {
    "unique_id": "c4eb89d84b2b407ba8ec1cf4d25b8b435bcef69d",
    "user_id": "59cce130e93a4e9488522ca67e3a6779f3e48a72",
    "document_id": "c63a7bc73f03449c987bf0feaa36e96212408352",
    "email": "chris@example.com",
    "created": 1770598603,
    "event": "created_document"
  }
]
```

#### 将文档移动到文件夹

```bash
POST /signnow/document/{document_id}/move
Content-Type: application/json

{
  "folder_id": "5e2798bdd3d642c3aefebe333bb5b723d6db01a4"
}
```

**响应：**
```json
{
  "result": "success"
}
```

#### 合并文档

将多个文档合并为一个PDF：

```bash
POST /signnow/document/merge
Content-Type: application/json

{
  "name": "Merged Document",
  "document_ids": ["doc_id_1", "doc_id_2"]
}
```

以二进制数据形式返回合并后的PDF。

#### 删除文档

```bash
DELETE /signnow/document/{document_id}
```

**响应：**
```json
{
  "status": "success"
}
```

### 模板操作

#### 从文档创建模板

```bash
POST /signnow/template
Content-Type: application/json

{
  "document_id": "c63a7bc73f03449c987bf0feaa36e96212408352",
  "document_name": "Contract Template"
}
```

**响应：**
```json
{
  "id": "47941baee4f74784bc1d37c25e88836fc38ed501"
}
```

#### 从模板创建文档

```bash
POST /signnow/template/{template_id}/copy
Content-Type: application/json

{
  "document_name": "New Contract from Template"
}
```

**响应：**
```json
{
  "id": "08f5f4a2cc1a4d6c8a986adbf90be2308807d4ae",
  "name": "New Contract from Template"
}
```

### 签名邀请操作

#### 发送自由格式的邀请

发送文档以供签名：

```bash
POST /signnow/document/{document_id}/invite
Content-Type: application/json

{
  "to": "signer@example.com",
  "from": "sender@example.com"
}
```

**响应：**
```json
{
  "result": "success",
  "id": "c38a57f08f2e48d98b5de52f75f7b1dd0a074c00",
  "callback_url": "none"
}
```

**注意：** 自定义主题和消息需要付费订阅计划。

#### 创建签名链接

创建一个可嵌入的签名链接（需要文档中包含签名字段）：

```bash
POST /signnow/link
Content-Type: application/json

{
  "document_id": "c63a7bc73f03449c987bf0feaa36e96212408352"
}
```

**注意：** 在创建签名链接之前，文档必须已添加签名字段。

### 文件夹操作

#### 获取所有文件夹

```bash
GET /signnow/folder
```

**响应：**
```json
{
  "id": "2ea71a3a9d06470d8e5ec0df6122971f47db7706",
  "name": "Root",
  "system_folder": true,
  "folders": [
    {
      "id": "5e2798bdd3d642c3aefebe333bb5b723d6db01a4",
      "name": "Documents",
      "document_count": "5",
      "template_count": "2"
    },
    {
      "id": "fafdef6de6d947fc84627e4ddeed6987bfeee02d",
      "name": "Templates",
      "document_count": "0",
      "template_count": "3"
    },
    {
      "id": "6063688b1e724a25aa98befcc3f2cb7795be7da1",
      "name": "Trash Bin",
      "document_count": "0"
    }
  ],
  "total_documents": 0,
  "documents": []
}
```

#### 通过ID获取文件夹

```bash
GET /signnow/folder/{folder_id}
```

**响应：**
```json
{
  "id": "5e2798bdd3d642c3aefebe333bb5b723d6db01a4",
  "name": "Documents",
  "user_id": "59cce130e93a4e9488522ca67e3a6779f3e48a72",
  "parent_id": "2ea71a3a9d06470d8e5ec0df6122971f47db7706",
  "system_folder": true,
  "folders": [],
  "total_documents": 5,
  "documents": [...]
}
```

### Webhook（事件订阅）操作

#### 列出事件订阅

```bash
GET /signnow/event_subscription
```

**响应：**
```json
{
  "subscriptions": [
    {
      "id": "b1d6700dfb0444ed9196e913b2515ae8d5f731a7",
      "event": "document.complete",
      "created": "1770598678",
      "callback_url": "https://example.com/webhook"
    }
  ]
}
```

#### 创建事件订阅

```bash
POST /signnow/event_subscription
Content-Type: application/json

{
  "event": "document.complete",
  "callback_url": "https://example.com/webhook"
}
```

**响应：**
```json
{
  "id": "b1d6700dfb0444ed9196e913b2515ae8d5f731a7",
  "created": 1770598678
}
```

**可用的事件：**
- `document.create` - 文档创建
- `document.update` - 文档更新
- `document.delete` - 文档删除
- `document.complete` - 所有方均已签名
- `invite.create` - 发送邀请
- `invite.update` - 邀请更新

#### 删除事件订阅

```bash
DELETE /signnow/event_subscription/{subscription_id}
```

**响应：**
```json
{
  "id": "b1d6700dfb0444ed9196e913b2515ae8d5f731a7",
  "status": "deleted"
}
```

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/signnow/user',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
const data = await response.json();
```

### Python

```python
import os
import requests

response = requests.get(
    'https://gateway.maton.ai/signnow/user',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
)
data = response.json()
```

### Python（上传文档）

```python
import os
import requests

with open('document.pdf', 'rb') as f:
    response = requests.post(
        'https://gateway.maton.ai/signnow/document',
        headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
        files={'file': ('document.pdf', f, 'application/pdf')}
    )
doc = response.json()
print(f"Uploaded document: {doc['id']}")
```

### Python（发送邀请）

```python
import os
import requests

doc_id = "c63a7bc73f03449c987bf0feaa36e96212408352"
response = requests.post(
    f'https://gateway.maton.ai/signnow/document/{doc_id}/invite',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'Content-Type': 'application/json'
    },
    json={
        'to': 'signer@example.com',
        'from': 'sender@example.com'
    }
)
result = response.json()
print(f"Invite sent: {result['id']}")
```

## 注意事项

- 上传的文档必须是PDF格式。
- 支持的文件类型：PDF、DOC、DOCX、ODT、RTF、PNG、JPG。
- 系统文件夹（Documents、Templates、Archive、Trash Bin）不能被重命名或删除。
- 创建签名链接之前，文档必须包含签名字段。
- 自定义邀请主题和消息需要付费订阅。
- 开发模式下的请求限制：每个应用程序每小时500次请求。
- 重要提示：当将curl输出传递给`jq`或其他命令时，在某些shell环境中，环境变量（如`$MATON_API_KEY`）可能无法正确解析。

## 错误处理

| 状态 | 含义 |
|--------|---------|
| 400 | 未找到SignNow连接或请求无效 |
| 401 | Maton API密钥无效或缺失 |
| 403 | 权限不足或需要订阅 |
| 404 | 资源未找到 |
| 405 | 方法不允许 |
| 429 | 请求次数达到限制 |
| 4xx/5xx | 来自SignNow API的传递错误 |

SignNow的错误会包含详细的错误信息：
```json
{
  "errors": [
    {
      "code": 65578,
      "message": "Invalid file type."
    }
  ]
}
```

### 故障排除：API密钥问题

1. 确保设置了`MATON_API_KEY`环境变量：

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

### 故障排除：应用程序名称无效

1. 确保您的URL路径以`signnow`开头。例如：
- 正确：`https://gateway.maton.ai/signnow/user`
- 错误：`https://gateway.maton.ai/user`

## 资源

- [SignNow API参考](https://docs.signnow.com/docs/signnow/reference)
- [SignNow开发者门户](https://www.signnow.com/developers)
- [SignNow Postman集合](https://github.com/signnow/postman-collection)
- [SignNow SDKs](https://github.com/signnow)
- [Maton社区](https://discord.com/invite/dBfFAcefs2)
- [Maton支持](mailto:support@maton.ai)