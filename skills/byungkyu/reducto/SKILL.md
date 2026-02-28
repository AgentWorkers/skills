---
name: reducto
description: Reducto 文档处理 API 支持通过管理 API 密钥进行身份验证。该 API 可用于解析、提取、分割和编辑文档。当用户需要处理文档、提取结构化数据或修改 PDF 和 DOCX 文件时，可以使用此功能。对于其他第三方应用程序，请使用 `api-gateway` 功能（https://clawhub.ai/byungkyu/api-gateway）。
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
# Reducto

您可以使用管理的API密钥身份验证来访问Reducto的文档处理API。该API支持解析文档、提取结构化数据、将文档分割成多个部分以及编辑PDF/DOCX文件。

## 快速入门

```bash
# Parse a document
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'document_url': 'https://example.com/document.pdf'}).encode()
req = urllib.request.Request('https://gateway.maton.ai/reducto/parse', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本URL

```
https://gateway.maton.ai/reducto/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的Reducto API端点路径。该网关会将请求代理到 `platform.reducto.ai` 并自动插入您的API密钥。

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

您可以在 `https://ctrl.maton.ai` 管理您的Reducto API密钥连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=reducto&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'reducto'}).encode()
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
    "connection_id": "f7579208-276c-455f-9962-4635fca739b9",
    "status": "ACTIVE",
    "creation_time": "2026-02-28T00:12:24.797884Z",
    "last_updated_time": "2026-02-28T00:16:13.509841Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "reducto",
    "metadata": {},
    "method": "API_KEY"
  }
}
```

在浏览器中打开返回的 `url` 以输入您的Reducto API密钥。

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

如果您有多个Reducto连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/reducto/parse')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', 'f7579208-276c-455f-9962-4635fca739b9')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此字段，网关将使用默认的（最旧的）活动连接。

## API参考

### 解析文档

解析文档并提取结构化内容（文本、表格、图表）。

#### 同步解析

```bash
POST /reducto/parse
Content-Type: application/json

{
  "document_url": "https://example.com/document.pdf"
}
```

**响应：**
```json
{
  "job_id": "04b8aa38-7eb3-4151-98b0-dbaea71358d9",
  "duration": 17.85,
  "pdf_url": "https://...",
  "studio_link": "https://studio.reducto.ai/job/...",
  "usage": {
    "num_pages": 15,
    "credits": 15.0
  },
  "result": {
    "chunks": [
      {
        "content": "Extracted text content...",
        "blocks": [...]
      }
    ]
  }
}
```

#### 异步解析

对于较长的文档，使用异步方法以避免超时：

```bash
POST /reducto/parse_async
Content-Type: application/json

{
  "document_url": "https://example.com/document.pdf"
}
```

**响应：**
```json
{
  "job_id": "e234ba95-410a-4dd0-8a14-743dbfc49470"
}
```

使用 `GET /reducto/job/{job_id}` 查询任务状态。

---

### 提取数据

使用JSON模式从文档中提取特定字段。

#### 同步提取

```bash
POST /reducto/extract
Content-Type: application/json

{
  "document_url": "https://example.com/document.pdf",
  "schema": {
    "type": "object",
    "properties": {
      "title": {"type": "string", "description": "The document title"},
      "authors": {"type": "array", "items": {"type": "string"}, "description": "List of author names"}
    }
  }
}
```

**响应：**
```json
{
  "job_id": "36f01a34-7ef6-40da-9e74-7c14902b6182",
  "usage": {
    "num_pages": 15,
    "num_fields": 9,
    "credits": 45.0
  },
  "studio_link": "https://studio.reducto.ai/job/...",
  "result": [
    {
      "title": "Document Title",
      "authors": ["Author One", "Author Two"]
    }
  ]
}
```

#### 异步提取

```bash
POST /reducto/extract_async
Content-Type: application/json

{
  "document_url": "https://example.com/document.pdf",
  "schema": {
    "type": "object",
    "properties": {
      "title": {"type": "string"}
    }
  }
}
```

**响应：**
```json
{
  "job_id": "0cdb6a50-df92-438b-875b-8b5c72d5b089"
}
```

---

### 分割文档

根据内容类别将文档分割成多个部分。

#### 同步分割

```bash
POST /reducto/split
Content-Type: application/json

{
  "document_url": "https://example.com/document.pdf",
  "split_description": [
    {"name": "abstract", "description": "The abstract section"},
    {"name": "introduction", "description": "The introduction section"},
    {"name": "conclusion", "description": "The conclusion section"}
  ]
}
```

**响应：**
```json
{
  "usage": {
    "num_pages": 15,
    "credits": 15.0
  },
  "result": {
    "section_mapping": {
      "abstract": [1],
      "introduction": [1, 2],
      "conclusion": [14, 15]
    },
    "splits": [
      {
        "name": "abstract",
        "pages": [1],
        "conf": "high"
      }
    ]
  }
}
```

#### 异步分割

```bash
POST /reducto/split_async
Content-Type: application/json

{
  "document_url": "https://example.com/document.pdf",
  "split_description": [
    {"name": "abstract", "description": "The abstract section"}
  ]
}
```

**响应：**
```json
{
  "job_id": "381de5fe-e162-4039-9ef9-8522fb34056b"
}
```

---

### 编辑文档

根据自然语言指令填写表单并修改PDF/DOCX文档。

#### 同步编辑

```bash
POST /reducto/edit
Content-Type: application/json

{
  "document_url": "https://example.com/form.pdf",
  "edit_instructions": "Fill in the name field with 'John Doe' and check the consent box"
}
```

**响应：**
```json
{
  "document_url": "https://presigned-url.s3.amazonaws.com/...",
  "form_schema": [...],
  "usage": {
    "num_pages": 2,
    "credits": 2.0
  }
}
```

#### 异步编辑

```bash
POST /reducto/edit_async
Content-Type: application/json

{
  "document_url": "https://example.com/form.pdf",
  "edit_instructions": "Highlight all mentions of 'important' in red"
}
```

**响应：**
```json
{
  "job_id": "575189cb-8732-429a-ba8a-06de8ee03208"
}
```

---

### 上传文件

将文档上传到Reducto并获取预签名的URL以进行处理。

```bash
POST /reducto/upload
Content-Type: application/json

{}
```

**响应：**
```json
{
  "file_id": "reducto://18d574c7-4144-4f50-b7af-b8aba83ada5d",
  "presigned_url": "https://prod-storage.s3.amazonaws.com/...?AWSAccessKeyId=...&Signature=...&Expires=..."
}
```

使用 `PUT` 请求将文件上传到 `presigned_url`，然后在解析/提取/分割/编辑请求中使用 `file_id` 作为 `document_url`。

---

### 流程

执行预先配置的处理流程。

```bash
POST /reducto/pipeline
Content-Type: application/json

{
  "input": "https://example.com/document.pdf",
  "pipeline_id": "your-pipeline-id"
}
```

**注意：** `pipeline_id` 必须是通过Reducto Studio在您的Reducto账户中配置的有效流程ID。

**响应：**
```json
{
  "job_id": "...",
  "usage": {
    "num_pages": 15,
    "credits": 15.0
  },
  "result": {
    "parse": {...},
    "extract": {...},
    "split": {...},
    "edit": {...}
  }
}
```

---

### 任务

#### 列出任务

```bash
GET /reducto/jobs
```

**响应：**
```json
{
  "jobs": [
    {
      "job_id": "8c25561f-247a-4843-b561-1eb94c3792d1",
      "status": "Completed",
      "type": "Parse",
      "created_at": "2026-02-27T23:11:39.787917",
      "num_pages": 15,
      "duration": 6.62
    }
  ],
  "next_cursor": null
}
```

#### 获取任务状态

```bash
GET /reducto/job/{job_id}
```

**响应（待处理）：**
```json
{
  "status": "Pending",
  "result": null,
  "progress": 0.5,
  "reason": null
}
```

**响应（已完成）：**
```json
{
  "status": "Completed",
  "result": {
    "job_id": "...",
    "duration": 17.85,
    "usage": {...},
    "result": {...}
  },
  "progress": null,
  "reason": null
}
```

任务状态值：`Pending`、`InProgress`、`Completed`、`Failed`

---

### 版本

```bash
GET /reducto/version
```

**响应：**
```json
"VERSION_GOES_HERE"
```

---

## 文档URL格式

`document_url` 参数支持以下几种格式：

1. **公共URL**：`https://example.com/document.pdf`
2. **预签名的S3 URL**：`https://bucket.s3.amazonaws.com/key?...`
3. **Reducto上传**：`reducto://file-id`（来自 `/upload` 端点）
4. **上一个任务**：`jobid://job-id`（重用上一个任务解析的内容）

## 代码示例

### JavaScript

```javascript
// Parse a document
const response = await fetch(
  'https://gateway.maton.ai/reducto/parse',
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      document_url: 'https://example.com/document.pdf'
    })
  }
);
const data = await response.json();
console.log(data.result.chunks);
```

### Python

```python
import os
import requests

# Extract data from a document
response = requests.post(
    'https://gateway.maton.ai/reducto/extract',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'Content-Type': 'application/json'
    },
    json={
        'document_url': 'https://example.com/document.pdf',
        'schema': {
            'type': 'object',
            'properties': {
                'title': {'type': 'string'},
                'date': {'type': 'string'}
            }
        }
    }
)
result = response.json()
print(result['result'])
```

### 异步任务查询

```python
import os
import time
import requests

# Start async parse
response = requests.post(
    'https://gateway.maton.ai/reducto/parse_async',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'Content-Type': 'application/json'
    },
    json={'document_url': 'https://example.com/large-document.pdf'}
)
job_id = response.json()['job_id']

# Poll for completion
while True:
    status = requests.get(
        f'https://gateway.maton.ai/reducto/job/{job_id}',
        headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
    ).json()

    print(f"Status: {status['status']}, Progress: {status.get('progress')}")

    if status['status'] == 'Completed':
        print(status['result'])
        break
    elif status['status'] == 'Failed':
        print(f"Failed: {status['reason']}")
        break

    time.sleep(2)
```

## 注意事项

- 对于大型文档，同步端点可能会超时；请使用异步端点。
- 预签名的URL有效期较短；请在调用 `/upload` 后立即上传文件。
- 来自 `/upload` 的以 `reducto://` 开头的URL可以在后续的解析/提取/分割/编辑请求中使用。
- 使用 `jobid://` 前缀可以重用上一个任务解析的内容（节省处理时间）。
- 连接使用API_KEY进行身份验证（而非OAuth）。
- 资源消耗取决于页面数量和操作类型。

## 错误处理

| 状态 | 含义 |
|--------|---------|
| 400 | 请求无效（缺少必需字段或格式不正确） |
| 401 | Maton API密钥无效或缺失 |
| 404 | 资源未找到 |
| 422 | 验证错误（详情请查看响应正文） |
| 4xx/5xx | 来自Reducto API的传递错误 |

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

### 故障排除：应用程序名称无效

确保您的URL路径以 `reducto` 开头。例如：

- 正确：`https://gateway.maton.ai/reducto/parse`
- 错误：`https://gateway.maton.ai/parse`

## 资源

- [Reducto文档](https://docs.reducto.ai)
- [Reducto API参考](https://docs.reducto.ai/api-reference)
- [Reducto Studio](https://studio.reducto.ai)
- [Maton社区](https://discord.com/invite/dBfFAcefs2)
- [Maton支持](mailto:support@maton.ai)