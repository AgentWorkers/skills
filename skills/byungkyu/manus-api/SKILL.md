---
name: manus
description: >
  **Manus AI Agent API集成与受管理的API密钥认证**  
  该功能支持用户通过API密钥进行身份验证，以创建和管理AI代理任务、项目、文件以及Webhook。  
  当用户需要运行AI代理任务、管理项目、上传文件或设置Webhook时，可使用此功能。  
  对于其他第三方应用程序，建议使用`api-gateway`功能（https://clawhub.ai/byungkyu/api-gateway）。
compatibility: Requires network access and valid Maton API key
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji:
    homepage: "https://maton.ai"
    requires:
      env:
        - MATON_API_KEY
---
# Manus

您可以使用托管的API密钥进行身份验证来访问Manus AI Agent API。该API用于创建和管理AI代理任务、项目、文件以及Webhook。

## 快速入门

```bash
# Create a task
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'prompt': 'What is the capital of France?'}).encode()
req = urllib.request.Request('https://gateway.maton.ai/manus/v1/tasks', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本URL

```
https://gateway.maton.ai/manus/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的Manus API端点路径。该网关会将请求代理到 `api.manus.ai` 并自动插入您的API密钥。

## 身份验证

所有请求都必须在 `Authorization` 头部包含Maton API密钥：

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

您可以在 `https://ctrl.maton.ai` 管理您的Manus API密钥连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=manus&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'manus'}).encode()
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
    "connection_id": "f85eb0d5-87d6-41a7-8271-0449d3e407bd",
    "status": "ACTIVE",
    "creation_time": "2026-02-28T00:12:24.030143Z",
    "last_updated_time": "2026-02-28T00:16:08.920760Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "manus",
    "metadata": {},
    "method": "API_KEY"
  }
}
```

在浏览器中打开返回的 `url`，以输入您的Manus API密钥。

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

如果您有多个Manus连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/manus/v1/tasks')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', 'f85eb0d5-87d6-41a7-8271-0449d3e407bd')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此字段，网关将使用默认的（最旧的）活动连接。

## API参考

### 项目

#### 列出项目

```bash
GET /manus/v1/projects
```

**响应：**
```json
{
  "object": "list",
  "data": [
    {
      "id": "SJhyBaLtYgQwurQoaT5APi",
      "name": "My Project"
    }
  ]
}
```

#### 创建项目

```bash
POST /manus/v1/projects
Content-Type: application/json

{
  "name": "My Project",
  "default_instructions": "You are a helpful assistant."
}
```

**响应：**
```json
{
  "id": "SJhyBaLtYgQwurQoaT5APi",
  "object": "project",
  "name": "My Project",
  "created_at": "1772238309"
}
```

---

### 任务

#### 列出任务

```bash
GET /manus/v1/tasks
```

**响应：**
```json
{
  "object": "list",
  "data": [
    {
      "id": "X7PPAMPNRovuyTXejNeEpv",
      "object": "task",
      "created_at": "1772191227",
      "updated_at": "1772191230",
      "status": "completed",
      "model": "manus-1.6-lite-adaptive",
      "metadata": {
        "task_title": "What is 2+2?",
        "task_url": "https://manus.im/app/X7PPAMPNRovuyTXejNeEpv"
      },
      "output": [...],
      "credit_usage": 0
    }
  ]
}
```

#### 获取任务信息

```bash
GET /manus/v1/tasks/{task_id}
```

**响应：**
```json
{
  "id": "X7PPAMPNRovuyTXejNeEpv",
  "object": "task",
  "created_at": "1772191227",
  "updated_at": "1772191230",
  "status": "completed",
  "model": "manus-1.6-lite-adaptive",
  "metadata": {
    "task_title": "What is 2+2?",
    "task_url": "https://manus.im/app/X7PPAMPNRovuyTXejNeEpv"
  },
  "output": [
    {
      "id": "J9LlYFIfTlMWvR5hrC9FUL",
      "status": "completed",
      "role": "user",
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "What is 2+2? Reply in one word."
        }
      ]
    },
    {
      "id": "kR8Tj0ys7uwzorcSgzqMvZ",
      "status": "completed",
      "role": "assistant",
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "Four"
        }
      ]
    }
  ],
  "credit_usage": 0
}
```

任务状态值：`pending`（待处理）、`running`（运行中）、`completed`（已完成）、`failed`（失败）

#### 创建任务

```bash
POST /manus/v1/tasks
Content-Type: application/json

{
  "prompt": "What is the capital of France?"
}
```

可选字段：
- `project_id`（字符串）：将任务关联到项目
- `file_ids`（数组）：将文件附加到任务

**响应：**
```json
{
  "task_id": "3cbKzkyC9WwRoMwAH8dKuY",
  "task_title": "Capital of France?",
  "task_url": "https://manus.im/app/3cbKzkyC9WwRoMwAH8dKuY"
}
```

#### 删除任务

```bash
DELETE /manus/v1/tasks/{task_id}
```

**响应：**
```json
{
  "id": "3cbKzkyC9WwRoMwAH8dKuY",
  "object": "file",
  "deleted": true
}
```

---

### 文件

#### 列出文件

```bash
GET /manus/v1/files
```

返回最近上传的10个文件。

**响应：**
```json
{
  "object": "list",
  "data": [
    {
      "id": "file-2Gpoz5yhB8seSu9dxZdquR",
      "object": "file",
      "filename": "test.txt",
      "status": "pending",
      "created_at": "1772238309",
      "expires_at": "1772411109"
    }
  ]
}
```

文件状态值：`pending`（待处理）、`ready`（已准备好）、`expired`（已过期）

#### 获取文件信息

```bash
GET /manus/v1/files/{file_id}
```

**响应：**
```json
{
  "id": "file-2Gpoz5yhB8seSu9dxZdquR",
  "object": "file",
  "filename": "test.txt",
  "status": "pending",
  "created_at": "1772238309",
  "expires_at": "1772411109"
}
```

#### 创建文件

创建文件记录并返回一个预签名的S3上传URL。

```bash
POST /manus/v1/files
Content-Type: application/json

{
  "filename": "document.pdf"
}
```

**响应：**
```json
{
  "id": "file-2Gpoz5yhB8seSu9dxZdquR",
  "object": "file",
  "filename": "document.pdf",
  "status": "pending",
  "upload_url": "https://vida-private.s3.us-east-1.amazonaws.com/...",
  "upload_expires_at": "1772238489",
  "created_at": "1772238309"
}
```

请在有效期内使用 `PUT` 请求将文件上传到 `upload_url`。

#### 删除文件

```bash
DELETE /manus/v1/files/{file_id}
```

**响应：**
```json
{
  "id": "file-2Gpoz5yhB8seSu9dxZdquR",
  "object": "file",
  "deleted": true
}
```

---

### Webhook

#### 创建Webhook

注册一个Webhook URL以接收任务生命周期通知。

```bash
POST /manus/v1/webhooks
Content-Type: application/json

{
  "webhook": {
    "url": "https://example.com/webhook"
  }
}
```

**响应：**
```json
{
  "webhook_id": "J4dD3mwzZiWuJFiEWAvGnK"
}
```

#### 删除Webhook

```bash
DELETE /manus/v1/webhooks/{webhook_id}
```

**响应：**
```json
{}
```

---

## 代码示例

### JavaScript

```javascript
// Create a task
const response = await fetch(
  'https://gateway.maton.ai/manus/v1/tasks',
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ prompt: 'Summarize the latest news' })
  }
);
const data = await response.json();
console.log(data.task_url);
```

### Python

```python
import os
import requests

# Create a task
response = requests.post(
    'https://gateway.maton.ai/manus/v1/tasks',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'Content-Type': 'application/json'
    },
    json={'prompt': 'Summarize the latest news'}
)
task = response.json()
print(task['task_url'])
```

## 注意事项

- 任务是异步执行的。您可以使用 `GET /manus/v1/tasks/{task_id}` 来检查任务完成情况或设置Webhook。
- 文件上传使用预签名的S3 URL，这些URL在3分钟后失效。
- 如果未使用，文件将在大约48小时后过期。
- Webhook的负载数据使用RSA-SHA256进行签名以进行验证。
- 可用的模型：`manus-1.6`、`manus-1.6-lite`、`manus-1.6-max`、`manus-1.5`、`manus-1.5-lite`、`speed`。
- 连接使用API_KEY身份验证方法（而非OAuth）。

## 错误处理

| 状态 | 含义 |
|--------|---------|
| 400 | 请求无效（缺少必需字段或格式不正确） |
| 401 | Maton API密钥无效或缺失 |
| 404 | 资源未找到 |
| 4xx/5xx | 来自Manus API的传递错误 |

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

确保您的URL路径以 `manus` 开头。例如：

- 正确：`https://gateway.maton.ai/manus/v1/tasks`
- 错误：`https://gateway.maton.ai/v1/tasks`

## 资源

- [Manus API概述](https://open.manus.im/docs)
- [Manus API参考](https://open.manus.im/docs/api-reference)
- [Manus官方网站](https://manus.im)
- [Maton社区](https://discord.com/invite/dBfFAcefs2)
- [Maton支持](mailto:support@maton.ai)