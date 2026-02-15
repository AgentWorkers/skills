---
name: upstage-document-parse
description: 使用 Upstage Document Parse API 解析文档（PDF、图片、DOCX、PPTX、XLSX、HWP 格式）。该 API 可提取文本、表格、图表以及带有边界框的布局元素。适用于用户需要解析文档内容、提取数据、分析文档结构、将文档转换为 Markdown/HTML 格式，或从 PDF 和图片中提取结构化数据的情况。
homepage: https://console.upstage.ai/api/document-digitization/document-parsing
metadata: {"openclaw":{"emoji":"📑","requires":{"bins":["curl"],"env":["UPSTAGE_API_KEY"]},"primaryEnv":"UPSTAGE_API_KEY"}}
---

# Upstage 文档解析

使用 Upstage 的文档解析 API 从文档中提取结构化内容。

## 支持的格式

PDF（最多 1000 页，支持异步处理）、PNG、JPG、JPEG、TIFF、BMP、GIF、WEBP、DOCX、PPTX、XLSX、HWP

## 安装

```bash
openclaw install upstage-document-parse
```

## API 密钥设置

1. 从 [Upstage 控制台](https://console.upstage.ai) 获取您的 API 密钥。
2. 配置 API 密钥：

```bash
openclaw config set skills.entries.upstage-document-parse.apiKey "your-api-key"
```

或者将其添加到 `~/.openclaw/openclaw.json` 文件中：

```json5
{
  "skills": {
    "entries": {
      "upstage-document-parse": {
        "apiKey": "your-api-key"
      }
    }
  }
}
```

## 使用示例

只需请求代理解析您的文档即可：

```
"Parse this PDF: ~/Documents/report.pdf"
"Parse: ~/Documents/report.jpg"
```

---

## 同步 API（适用于小型文档）

适用于小型文档（建议页面数少于 20 页）。

### 参数

| 参数 | 类型 | 默认值 | 描述 |
|-----------|------|---------|-------------|
| `model` | string | 必需 | 使用 `document-parse`（最新版本）或 `document-parse-nightly` |
| `document` | file | 必需 | 需要解析的文档文件 |
| `mode` | string | `standard` | 标准模式（以文本为主）；`enhanced`（包含复杂的表格/图片）；`auto` |
| `ocr` | string | `auto` | 自动执行 OCR（仅针对图片）；`force`（始终执行 OCR） |
| `output_formats` | string | `['html']` | 输出格式：`text`、`html`、`markdown`（数组格式） |
| `coordinates` | boolean | `true` | 是否包含元素的边界框坐标 |
| `base64_encoding` | string | `[]` | 需要转换为 Base64 的元素：`["table"]`、`["figure"]` 等 |
| `chart_recognition` | boolean | `true` | 将图表转换为表格（测试版） |
| `merge_multipage_tables` | boolean | `false` | 是否合并跨页的表格（测试版，启用时最多合并 20 页的表格） |

### 基本解析

```bash
curl -X POST "https://api.upstage.ai/v1/document-digitization" \
  -H "Authorization: Bearer $UPSTAGE_API_KEY" \
  -F "document=@/path/to/file.pdf" \
  -F "model=document-parse"
```

### 提取 Markdown 格式内容

```bash
curl -X POST "https://api.upstage.ai/v1/document-digitization" \
  -H "Authorization: Bearer $UPSTAGE_API_KEY" \
  -F "document=@report.pdf" \
  -F "model=document-parse" \
  -F "output_formats=['markdown']"
```

### 复杂文档的增强模式

```bash
curl -X POST "https://api.upstage.ai/v1/document-digitization" \
  -H "Authorization: Bearer $UPSTAGE_API_KEY" \
  -F "document=@complex.pdf" \
  -F "model=document-parse" \
  -F "mode=enhanced" \
  -F "output_formats=['html', 'markdown']"
```

### 对扫描文档强制执行 OCR

```bash
curl -X POST "https://api.upstage.ai/v1/document-digitization" \
  -H "Authorization: Bearer $UPSTAGE_API_KEY" \
  -F "document=@scan.pdf" \
  -F "model=document-parse" \
  -F "ocr=force"
```

### 将表格图像提取为 Base64 格式

```bash
curl -X POST "https://api.upstage.ai/v1/document-digitization" \
  -H "Authorization: Bearer $UPSTAGE_API_KEY" \
  -F "document=@invoice.pdf" \
  -F "model=document-parse" \
  -F "base64_encoding=['table']"
```

---

## 响应结构

```json
{
  "api": "2.0",
  "model": "document-parse-251217",
  "content": {
    "html": "<h1>...</h1>",
    "markdown": "# ...",
    "text": "..."
  },
  "elements": [
    {
      "id": 0,
      "category": "heading1",
      "content": { "html": "...", "markdown": "...", "text": "..." },
      "page": 1,
      "coordinates": [{"x": 0.06, "y": 0.05}, ...]
    }
  ],
  "usage": { "pages": 1 }
}
```

### 元素类别

`paragraph`（段落）、`heading1`（标题 1）、`heading2`（标题 2）、`heading3`（标题 3）、`list`（列表）、`table`（表格）、`figure`（图表）、`chart`（图表）、`equation`（公式）、`caption`（图例）、`header`（页眉）、`footer`（页脚）、`index`（索引）、`footnote`（脚注）

---

## 异步 API（适用于大型文档）

适用于超过 1000 页的文档。文档会以每 10 页为一批进行处理。

### 提交请求

```bash
curl -X POST "https://api.upstage.ai/v1/document-digitization/async" \
  -H "Authorization: Bearer $UPSTAGE_API_KEY" \
  -F "document=@large.pdf" \
  -F "model=document-parse" \
  -F "output_formats=['markdown']"
```

响应：
```json
{"request_id": "uuid-here"}
```

### 检查状态并获取结果

```bash
curl "https://api.upstage.ai/v1/document-digitization/requests/{request_id}" \
  -H "Authorization: Bearer $UPSTAGE_API_KEY"
```

响应中包含每个批处理的 `download_url`（有效期为 30 天）。

### 列出所有请求

```bash
curl "https://api.upstage.ai/v1/document-digitization/requests" \
  -H "Authorization: Bearer $UPSTAGE_API_KEY"
```

### 状态值

- `submitted`：请求已接收
- `started`：处理中
- `completed`：处理完成，可下载
- `failed`：发生错误（请查看 `failure_message`）

### 注意事项

- 结果会保存 30 天
- 下载链接在 15 分钟后失效（需要重新请求以获取新的链接）
- 文档会被分割成每 10 页的批次进行处理

---

## Python 使用示例

```python
import requests

api_key = "up_xxx"

# Sync
with open("doc.pdf", "rb") as f:
    response = requests.post(
        "https://api.upstage.ai/v1/document-digitization",
        headers={"Authorization": f"Bearer {api_key}"},
        files={"document": f},
        data={"model": "document-parse", "output_formats": "['markdown']"}
    )
print(response.json()["content"]["markdown"])

# Async for large docs
with open("large.pdf", "rb") as f:
    r = requests.post(
        "https://api.upstage.ai/v1/document-digitization/async",
        headers={"Authorization": f"Bearer {api_key}"},
        files={"document": f},
        data={"model": "document-parse"}
    )
request_id = r.json()["request_id"]

# Poll for results
import time
while True:
    status = requests.get(
        f"https://api.upstage.ai/v1/document-digitization/requests/{request_id}",
        headers={"Authorization": f"Bearer {api_key}"}
    ).json()
    if status["status"] == "completed":
        break
    time.sleep(5)
```

## 与 LangChain 的集成

```python
from langchain_upstage import UpstageDocumentParseLoader

loader = UpstageDocumentParseLoader(
    file_path="document.pdf",
    output_format="markdown",
    ocr="auto"
)
docs = loader.load()
```

---

## 环境变量（另一种设置方式）

您也可以将 API 密钥设置为环境变量：

```bash
export UPSTAGE_API_KEY="your-api-key"
```

---

## 提示

- 对于包含复杂表格、图表或图片的文档，请使用 `mode=enhanced`。
- 使用 `mode=auto` 时，API 会根据页面内容自动选择合适的处理方式。
- 对于超过 20 页的文档，请使用异步 API。
- 对于扫描的 PDF 或图片文件，请使用 `ocr=force`。
- 使用 `merge_multipage_tables=true` 可以合并跨页的表格（在增强模式下最多合并 20 页的表格）。
- 异步 API 的结果会保存 30 天。
- 同步 API 的服务器端超时时间为每请求 5 分钟。
- 标准文档的处理时间约为 3 秒。