---
name: pdf-co
description: >
  **PDF.co API集成与OAuth认证**  
  支持PDF文件的转换、合并、拆分、编辑以及数据提取功能。  
  当用户需要将PDF文件转换为其他格式、合并或拆分PDF文件、添加水印或文本、提取文本/表格内容，或解析发票信息时，可使用此功能。  
  对于其他第三方应用程序，建议使用`api-gateway`功能（https://clawhub.ai/byungkyu/api-gateway）。
compatibility: Requires network access and valid Maton API key
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 📄
    homepage: "https://maton.ai"
    requires:
      env:
        - MATON_API_KEY
---
# PDF.co

使用受管理的身份验证方式访问 PDF.co API。支持转换、合并、拆分和编辑 PDF 文件，并提供全面的文档操作功能。

## 快速入门

```bash
# Get PDF info
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'url': 'https://example.com/sample.pdf'}).encode()
req = urllib.request.Request('https://gateway.maton.ai/pdf-co/v1/pdf/info', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/pdf-co/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的 PDF.co API 端点路径。该网关会将请求代理到 `api.pdf.co` 并自动注入您的 API 凭据。

## 身份验证

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

您可以在 `https://ctrl.maton.ai` 上管理您的 PDF.co 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=pdf-co&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'pdf-co'}).encode()
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
    "connection_id": "21fd90f9-5935-43cd-b6c8-bde9d915ca80",
    "status": "ACTIVE",
    "creation_time": "2025-12-08T07:20:53.488460Z",
    "last_updated_time": "2026-01-31T20:03:32.593153Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "pdf-co",
    "metadata": {}
  }
}
```

在浏览器中打开返回的 `url` 以完成身份验证。

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

如果您有多个 PDF.co 连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'url': 'https://example.com/sample.pdf'}).encode()
req = urllib.request.Request('https://gateway.maton.ai/pdf-co/v1/pdf/info', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此字段，网关将使用默认的（最旧的）活动连接。

## API 参考

### 获取 PDF 文件信息

获取 PDF 文件的元数据和相关信息。

```bash
POST /pdf-co/v1/pdf/info
Content-Type: application/json

{
  "url": "https://example.com/document.pdf"
}
```

### 将 PDF 转换为文本

```bash
POST /pdf-co/v1/pdf/convert/to/text
Content-Type: application/json

{
  "url": "https://example.com/document.pdf",
  "pages": "0-",
  "inline": true
}
```

**响应：**
```json
{
  "body": "Extracted text content...",
  "pageCount": 5,
  "error": false,
  "status": 200,
  "name": "document.txt",
  "credits": 10,
  "remainingCredits": 9990
}
```

### 将 PDF 转换为 CSV

```bash
POST /pdf-co/v1/pdf/convert/to/csv
Content-Type: application/json

{
  "url": "https://example.com/document.pdf",
  "pages": "0-",
  "inline": true,
  "lang": "eng"
}
```

### 将 PDF 转换为 JSON

```bash
POST /pdf-co/v1/pdf/convert/to/json
Content-Type: application/json

{
  "url": "https://example.com/document.pdf",
  "pages": "0-",
  "inline": true
}
```

### 将 PDF 转换为 HTML

```bash
POST /pdf-co/v1/pdf/convert/to/html
Content-Type: application/json

{
  "url": "https://example.com/document.pdf",
  "pages": "0-",
  "name": "output.html"
}
```

### 将 PDF 转换为 XLSX（Excel）

```bash
POST /pdf-co/v1/pdf/convert/to/xlsx
Content-Type: application/json

{
  "url": "https://example.com/document.pdf",
  "pages": "0-",
  "name": "output.xlsx"
}
```

### 将 PDF 转换为 PNG

```bash
POST /pdf-co/v1/pdf/convert/to/png
Content-Type: application/json

{
  "url": "https://example.com/document.pdf",
  "pages": "0",
  "name": "page.png"
}
```

### 将 PDF 转换为 JPG

```bash
POST /pdf-co/v1/pdf/convert/to/jpg
Content-Type: application/json

{
  "url": "https://example.com/document.pdf",
  "pages": "0",
  "name": "page.jpg"
}
```

### 将 HTML 转换为 PDF

```bash
POST /pdf-co/v1/pdf/convert/from/html
Content-Type: application/json

{
  "html": "<html><body><h1>Hello World</h1></body></html>",
  "name": "output.pdf",
  "paperSize": "Letter",
  "orientation": "Portrait",
  "margins": "10 10 10 10"
}
```

**响应：**
```json
{
  "url": "https://pdf-temp-files.s3.amazonaws.com/...",
  "pageCount": 1,
  "error": false,
  "status": 200,
  "name": "output.pdf",
  "remainingCredits": 9980
}
```

### 将 URL 转换为 PDF

```bash
POST /pdf-co/v1/pdf/convert/from/url
Content-Type: application/json

{
  "url": "https://example.com",
  "name": "webpage.pdf",
  "paperSize": "A4",
  "orientation": "Portrait"
}
```

### 合并 PDF 文件

将多个 PDF 文件合并为一个文档。

```bash
POST /pdf-co/v1/pdf/merge
Content-Type: application/json

{
  "url": "https://example.com/doc1.pdf,https://example.com/doc2.pdf",
  "name": "merged.pdf"
}
```

**响应：**
```json
{
  "url": "https://pdf-temp-files.s3.amazonaws.com/merged.pdf",
  "pageCount": 10,
  "error": false,
  "status": 200,
  "name": "merged.pdf",
  "remainingCredits": 9970,
  "duration": 1500
}
```

### 拆分 PDF 文件

将 PDF 文件拆分为多个文件。

```bash
POST /pdf-co/v1/pdf/split
Content-Type: application/json

{
  "url": "https://example.com/document.pdf",
  "pages": "1-3,4-6,7-"
}
```

**响应：**
```json
{
  "urls": [
    "https://pdf-temp-files.s3.amazonaws.com/part1.pdf",
    "https://pdf-temp-files.s3.amazonaws.com/part2.pdf",
    "https://pdf-temp-files.s3.amazonaws.com/part3.pdf"
  ],
  "pageCount": 10,
  "error": false,
  "status": 200,
  "remainingCredits": 9960
}
```

### 删除页面

```bash
POST /pdf-co/v1/pdf/edit/delete-pages
Content-Type: application/json

{
  "url": "https://example.com/document.pdf",
  "pages": "2,4,6"
}
```

### 向 PDF 中添加文本和图片

向 PDF 文件中添加文本、图片或其他内容。

```bash
POST /pdf-co/v1/pdf/edit/add
Content-Type: application/json

{
  "url": "https://example.com/document.pdf",
  "name": "annotated.pdf",
  "annotations": [
    {
      "text": "CONFIDENTIAL",
      "x": 100,
      "y": 100,
      "size": 24,
      "pages": "0-"
    }
  ]
}
```

### 搜索和替换文本

```bash
POST /pdf-co/v1/pdf/edit/replace-text
Content-Type: application/json

{
  "url": "https://example.com/document.pdf",
  "searchString": "old text",
  "replaceString": "new text"
}
```

### 搜索和删除文本

```bash
POST /pdf-co/v1/pdf/edit/delete-text
Content-Type: application/json

{
  "url": "https://example.com/document.pdf",
  "searchString": "text to remove"
}
```

### 设置密码

```bash
POST /pdf-co/v1/pdf/security/add
Content-Type: application/json

{
  "url": "https://example.com/document.pdf",
  "ownerPassword": "owner123",
  "userPassword": "user456"
}
```

### 删除密码

```bash
POST /pdf-co/v1/pdf/security/remove
Content-Type: application/json

{
  "url": "https://example.com/document.pdf",
  "password": "currentpassword"
}
```

### AI 发票解析器

自动从发票中提取结构化数据。

```bash
POST /pdf-co/v1/ai-invoice-parser
Content-Type: application/json

{
  "url": "https://example.com/invoice.pdf"
}
```

### 文档解析器

使用模板提取数据。

```bash
POST /pdf-co/v1/pdf/documentparser
Content-Type: application/json

{
  "url": "https://example.com/document.pdf",
  "templateId": "your-template-id"
}
```

### 生成条形码

```bash
POST /pdf-co/v1/barcode/generate
Content-Type: application/json

{
  "value": "1234567890",
  "type": "QRCode",
  "name": "barcode.png"
}
```

### 读取条形码

```bash
POST /pdf-co/v1/barcode/read/from/url
Content-Type: application/json

{
  "url": "https://example.com/barcode.png",
  "types": "QRCode,Code128,Code39,EAN13,UPCA"
}
```

### 检查作业状态（异步）

对于异步操作，请检查作业状态。

```bash
POST /pdf-co/v1/job/check
Content-Type: application/json

{
  "jobId": "abc123"
}
```

## 异步处理

对于大文件或批量操作，请使用异步处理：

```bash
POST /pdf-co/v1/pdf/merge
Content-Type: application/json

{
  "url": "https://example.com/large1.pdf,https://example.com/large2.pdf",
  "async": true,
  "name": "merged.pdf"
}
```

**响应：**
```json
{
  "jobId": "abc123",
  "status": "working",
  "error": false
}
```

然后轮询作业状态：

```bash
POST /pdf-co/v1/job/check
Content-Type: application/json

{
  "jobId": "abc123"
}
```

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/pdf-co/v1/pdf/merge',
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      url: 'https://example.com/doc1.pdf,https://example.com/doc2.pdf',
      name: 'merged.pdf'
    })
  }
);
const result = await response.json();
console.log(result.url);
```

### Python

```python
import os
import requests

response = requests.post(
    'https://gateway.maton.ai/pdf-co/v1/pdf/merge',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    json={
        'url': 'https://example.com/doc1.pdf,https://example.com/doc2.pdf',
        'name': 'merged.pdf'
    }
)
result = response.json()
print(result['url'])
```

## 注意事项

- 所有文件 URL 必须是公开可访问的，或者使用 PDF.co 的临时存储服务。
- 合并操作所需的多个 URL 应用逗号分隔。
- 页面索引从 0 开始（第一页为 `0`）。
- 页面范围格式如下：`0-2`（第 0、1、2 页），`3-`（从第 3 页开始），`0,2,4`（指定页面）。
- 输出文件默认会临时存储，并在 60 分钟后过期。
- 对于大文件，请使用 `async: true` 以避免超时。
- 使用 `inline: true` 可以直接在响应中获取内容，而无需通过 URL。
- 重要提示：当 URL 包含括号时，使用 `curl -g` 可以避免全局解析问题。
- 重要提示：当将 curl 输出传递给 `jq` 或其他命令时，在某些 shell 环境中 `$MATON_API_KEY` 环境变量可能无法正确解析。

## 错误处理

| 状态 | 含义 |
|--------|---------|
| 400 | 未找到 PDF.co 连接或请求无效 |
| 401 | Maton API 密钥无效或缺失 |
| 429 | 超过请求频率限制 |
| 4xx/5xx | 来自 PDF.co API 的传递错误 |

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

1. 确保您的 URL 路径以 `pdf-co` 开头。例如：
- 正确：`https://gateway.maton.ai/pdf-co/v1/pdf/merge`
- 错误：`https://gateway.maton.ai/v1/pdf/merge`

## 资源

- [PDF.co API 文档](https://docs.pdf.co)
- [PDF.co API 参考](https://docs.pdf.co/api-reference)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)