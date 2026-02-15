---
name: cognito-forms
description: |
  Cognito Forms API integration with managed OAuth. Access forms, entries, and documents.
  Use this skill when users want to create, read, update, or delete form entries, or retrieve form submissions.
  For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
compatibility: Requires network access and valid Maton API key
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    requires:
      env:
        - MATON_API_KEY
---

# Cognito Forms

您可以使用托管的 OAuth 认证来访问 Cognito Forms API。该 API 允许您列出表单、管理表单中的条目（创建、读取、更新、删除）以及检索相关文档。

## 快速入门

```bash
# List all forms
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/cognito-forms/api/forms')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/cognito-forms/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的 Cognito Forms API 端点路径（以 `api/` 开头）。Maton 代理会将请求转发到 `www.cognitoforms.com`，并自动插入您的 OAuth 令牌。

## 认证

所有请求都必须在 `Authorization` 头中包含 Maton API 密钥：

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

您可以在 `https://ctrl.maton.ai` 管理您的 Cognito Forms OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=cognito-forms&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'cognito-forms'}).encode()
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
    "connection_id": "77de1a60-5f69-45fc-977c-9dfffe7a64d4",
    "status": "ACTIVE",
    "creation_time": "2026-02-08T10:39:10.245446Z",
    "last_updated_time": "2026-02-09T04:11:08.342101Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "cognito-forms",
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

如果您有多个 Cognito Forms 连接，请使用 `Maton-Connection` 头来指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/cognito-forms/api/forms')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '77de1a60-5f69-45fc-977c-9dfffe7a64d4')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此参数，Maton 代理将使用默认的（最旧的）活跃连接。

## API 参考

### 表单

#### 列出表单

```bash
GET /cognito-forms/api/forms
```

返回组织中的所有表单。

### 表单条目

#### 获取条目信息

```bash
GET /cognito-forms/api/forms/{formId}/entries/{entryId}
```

根据 ID 或条目编号获取特定条目的信息。

#### 创建条目

```bash
POST /cognito-forms/api/forms/{formId}/entries
Content-Type: application/json

{
  "Name": {
    "First": "John",
    "Last": "Doe"
  },
  "Email": "john.doe@example.com",
  "Phone": "555-1234"
}
```

字段名称与表单中的字段名称一致。对于名称（Name）和地址（Address）等复杂字段，需要使用嵌套对象进行表示。

#### 更新条目

```bash
PATCH /cognito-forms/api/forms/{formId}/entries/{entryId}
Content-Type: application/json

{
  "Name": {
    "First": "Jane",
    "Last": "Doe"
  },
  "Email": "jane.doe@example.com"
}
```

更新现有条目。使用 `PATCH` 方法（而非 `PUT`）。如果条目包含已支付的订单，操作将失败。

#### 删除条目

```bash
DELETE /cognito-forms/api/forms/{formId}/entries/{entryId}
```

删除条目。需要具有 `Read/Write/Delete` 的 API 权限。

### 文档

#### 获取文档

```bash
GET /cognito-forms/api/forms/{formId}/entries/{entryId}/documents/{templateNumber}
```

根据指定的模板编号从条目中生成并返回文档。

**响应：**
```json
{
  "Id": "abc123",
  "Name": "Entry-Document.pdf",
  "ContentType": "application/pdf",
  "Size": 12345,
  "File": "https://temporary-download-url..."
}
```

### 文件

#### 获取文件

```bash
GET /cognito-forms/api/files/{fileId}
```

检索上传到表单条目中的文件。

**响应：**
```json
{
  "Id": "file-id",
  "Name": "upload.pdf",
  "ContentType": "application/pdf",
  "Size": 54321,
  "File": "https://temporary-download-url..."
}
```

## 字段格式示例

### 名称字段

```json
{
  "Name": {
    "First": "John",
    "Last": "Doe"
  }
}
```

### 地址字段

```json
{
  "Address": {
    "Line1": "123 Main St",
    "Line2": "Suite 100",
    "City": "San Francisco",
    "State": "CA",
    "PostalCode": "94105"
  }
}
```

### 单选字段

```json
{
  "PreferredContact": "Email"
}
```

### 多选字段

```json
{
  "Interests": ["Sports", "Music", "Travel"]
}
```

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/cognito-forms/api/forms',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
const forms = await response.json();
```

### Python

```python
import os
import requests

response = requests.get(
    'https://gateway.maton.ai/cognito-forms/api/forms',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
)
forms = response.json()
```

### Python 示例：创建条目

```python
import os
import requests

entry_data = {
    "Name": {"First": "John", "Last": "Doe"},
    "Email": "john@example.com",
    "Message": "Hello from the API!"
}

response = requests.post(
    'https://gateway.maton.ai/cognito-forms/api/forms/ContactForm/entries',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'Content-Type': 'application/json'
    },
    json=entry_data
)
```

## 注意事项

- **条目列表：** Cognito Forms API 不支持批量列出所有条目。建议使用 Webhook 或 OData 进行条目同步。
- **获取表单信息：** 如果请求返回 404 错误，请使用 `List Forms` 方法获取表单信息。
- **表单可用性：** 该 API 端点可能因您的 Cognito Forms 计划而不可用。
- **条目 ID：** 条目 ID 可以是条目编号或 `{formId}-{entryNumber}` 的格式。
- **复杂字段（如名称和地址）：** 使用嵌套的 JSON 对象进行表示。
- **文件上传：** 上传的文件会返回临时下载链接。
- **文档生成：** 会根据表单模板生成 PDF 文件。
- **API 权限：** 控制访问权限（读取、读写或读写/删除）。
- **重要提示：** 当使用 `curl` 命令时，如果 URL 中包含括号，请使用 `curl -g` 以避免全局解析问题。
- **重要提示：** 在将 `curl` 输出传递给 `jq` 或其他命令时，某些 shell 环境中可能无法正确解析 `$MATON_API_KEY` 环境变量。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未找到 Cognito Forms 连接 |
| 401 | Maton API 密钥无效或缺失 |
| 404 | 未找到表单或条目 |
| 429 | 每 60 秒请求次数限制（100 次） |
| 4xx/5xx | 来自 Cognito Forms API 的传递错误 |

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

### 故障排除：应用名称无效

1. 确保您的 URL 路径以 `cognito-forms` 开头。例如：
  - 正确：`https://gateway.maton.ai/cognito-forms/api/forms`
  - 错误：`https://gateway.maton.ai/api/forms`

## 资源

- [Cognito Forms API 概述](https://www.cognitoforms.com/support/475/data-integration/cognito-forms-api)
- [REST API 参考](https://www.cognitoforms.com/support/476/data-integration/cognito-forms-api/rest-api-reference)
- [API 参考文档](https://www.cognitoforms.com/support/476/data-integration/cognito-forms-api/api-reference)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持团队](mailto:support@maton.ai)