# 文件转换工具 — Skill

## 概述

该工具使用由 Cloudflare Workers AI toMarkdown 提供支持的 `markdown.new` API，将各种文件格式转换为结构清晰、适合 AI 处理的 Markdown 格式。支持转换的文件类型包括文档、电子表格、图片和结构化数据等 20 多种格式。无需身份验证（每个 IP 每天最多 500 次请求）。

---

## 适用场景

在以下情况下可以使用此工具：

* 从文件中提取文本以供大型语言模型（LLM）处理
* 将 PDF 或 Office 文件转换为 Markdown 格式
* 将数据规范化为结构化文本
* 处理用户上传的文件
* 从网页中抓取内容并转换为 Markdown 格式
* 将图片转换为 AI 生成的描述和文本内容

常见应用场景包括：

* 信息检索与聚合（RAG）工作流程
* 知识库构建
* 文档摘要生成
* 数据集提取
* 电子表格分析
* 从图片中提取信息（类似光学字符识别 OCR 的功能）

---

## 支持的文件格式

### 文档格式

* `.pdf`
* `.docx`
* `.odt`

### 电子表格格式

* `.xlsx`
* `.xls`
* `.xlsm`
* `.xlsb`
* `.et`
* `.ods`
* `.numbers`

### 图片格式

* `.jpg`
* `.jpeg`
* `.png`
* `.webp`
* `.svg`

### 文本及结构化数据格式

* `.txt`
* `.md`
* `.csv`
* `.json`
* `.xml`
* `.html`
* `.htm`

**说明：**
- 图片转换利用 AI 对图片中的对象进行检测和总结。
- HTML 格式文件的转换通过网页解析机制完成。
- 上传的 HTML 文件则通过 Workers AI 进行转换。

---

## API 基本地址

```https://markdown.new
```

---

## API 端点

### 1️⃣ 转换远程文件（简单 GET 请求）

返回纯 Markdown 文本。

```bash
curl -s "https://markdown.new/https://example.com/report.pdf"
```

---

### 2️⃣ 转换远程文件（返回 JSON 格式的元数据）

返回文件的元数据以及转换后的 Markdown 内容。

```bash
curl -s "https://markdown.new/https://example.com/report.pdf?format=json"
```

---

### 3️⃣ 通过 POST 请求转换远程文件

适用于需要结构化 JSON 响应的情况。

```bash
curl -s https://markdown.new/ \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/report.pdf"}'
```

---

### 4️⃣ 上传本地文件

适用于文件无法公开访问的情况。

```bash
curl -s https://markdown.new/convert \
  -F "file=@document.pdf"
```

---

## 响应格式

### URL 转换结果

```json
{
  "success": true,
  "url": "https://example.com/report.pdf",
  "title": "季度报告",
  "content": "# 季度报告\n\n...",
  "method": "Workers AI (file)",
  "duration_ms": 1200,
  "tokens": 850
}
```

---

### 上传文件后的转换结果

```json
{
  "success": true,
  "data": {
    "title": "Q4 Report",
    "content": "# 第四季度报告\n\n...",
    "filename": "report.xlsx",
    "file_type": ".xlsx",
    "tokens": 1250,
    "processing_time_ms": 320
  }
}
```

---

## 对 AI 代理的最佳实践

### 简单流程推荐使用 GET 请求

- 当只需要 Markdown 文本时
- 当速度要求较高且不需要元数据时

### 结构化处理推荐使用 POST 请求

- 当需要元数据时
- 当需要统计转换次数时
- 当需要监控或记录转换过程时
- 当需要构建自动化工作流程时

---

### 文件上传策略

- 仅在文件为本地文件、需要私密访问权限或需要身份验证时，使用 `/convert` 端点。
- 其他情况下，优先使用 URL 转换方式。

---

## 错误处理策略

- 检查响应中的 `success` 字段是否为 `true`。
- 如遇到网络故障，尝试重新请求一次。
- 确保转换后的内容长度大于 0。
- 如有必要，可采取备用提取方法。

---

## 使用限制

- 每个 IP 每天最多 500 次请求（无需 API 密钥）。
- 无需注册即可使用。

**建议：**
- 尽可能缓存转换结果。
- 避免重复转换同一文件。

---

## 集成示例

### JavaScript（Node.js）

```js
const res = await fetch("https://markdown.new/", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    url: "https://example.com/file.pdf"
  })
});
const data = await res.json();
console.log(data.content);
```

---

### Python

```python
import requests

res = requests.post(
    "https://markdown.new/",
    json={"url": "https://example.com/file.pdf"}
)
data = res.json()
print(data["content"])
```

---

## 代理决策流程

根据用户提供的文件类型，选择合适的操作方式：

| 文件类型            | 应使用的请求方法           |
|-------------------|----------------------|
| 公开可访问的文件       | 使用 GET 或 POST 请求           |
| 本地文件           | 使用 POST 请求（通过 /convert 端点）      |
| 图片               | 先转换再提取内容           |
| 电子表格           | 先转换再进行分析         |
| 网页内容           | 先解析 HTML 内容再转换       |

---

## 输出要求

转换后的 Markdown 文本应满足以下要求：

- 结构清晰
- 适合 AI 处理
- 无多余信息（噪音较少）
- 可直接用于大型语言模型的处理

---

## 注意事项

- 复杂的 PDF 格式可能会丢失部分格式。
- 大型电子表格的内容可能会被截断。
- 图片的转换结果受 AI 解释能力的影响。
- 可能存在请求次数限制。

---

## 总结

该工具为 AI 系统提供了一个通用的文件转换到 Markdown 的解决方案，具备以下特点：

- 无需身份验证
- 使用简单的 HTTP 接口
- 支持多种文件格式
- 输出结果结构化
- 转换速度快

非常适合用于文档导入、信息检索与聚合（RAG）流程以及自动化任务。