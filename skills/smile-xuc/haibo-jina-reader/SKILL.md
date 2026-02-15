---
name: jina-reader
description: 使用 Jina Reader API 从任何 URL 中提取干净、可读的 Markdown 内容。当您需要获取并解析网页内容，而无需处理 HTML、JavaScript 的渲染或支付墙时，这个工具非常实用。它非常适合用于研究、文章摘要、内容分析，以及处理来自 tavily-search、web_search 或 searxngskills 的搜索结果。
---

# Jina Reader

## 概述

Jina Reader 可以从任何 URL 中提取干净的 Markdown 内容，无需处理 HTML 复杂性、JavaScript 渲染以及许多付费墙的限制。它返回包含元数据（标题、URL、发布时间）的结构化文本，非常适合用于人工智能分析。

## 快速入门

### 提取 Markdown 内容
```bash
scripts/jina-reader.py <url>
```

### 带 JSON 元数据提取
```bash
scripts/jina-reader.py <url> --format json
```

### 保存到文件
```bash
scripts/jina-reader.py <url> -o output.md
```

## 核心功能

### 1. 基本提取

从任何 URL 中提取干净的 Markdown 内容：
```bash
scripts/jina-reader.py https://example.com/article
```

**返回内容：** 包含标题、元数据头和结构化文本的完整 Markdown 内容。

**适用场景：** 当你需要从网页中获取可读文本以进行总结、分析或内容处理时。

### 2. JSON 格式

获取带有元数据的结构化数据：
```bash
scripts/jina-reader.py https://example.com/article --format json
```

**返回内容：**
```json
{
  "status": "success",
  "metadata": {
    "title": "Article Title",
    "url": "https://example.com/article",
    "published": "Mon, 10 Feb 2026 12:00:00 GMT"
  },
  "content": "Markdown content..."
}
```

**适用场景：** 当你需要以编程方式访问元数据或希望与其他工具集成时。

### 3. Shell 脚本快速使用

对于简单的命令行操作：
```bash
scripts/jina-reader.sh https://example.com/article
```

**返回内容：** 直接将原始 Markdown 内容输出到标准输出（stdout）。

**适用场景：** 需要快速提取内容且不需要参数时，或者需要将提取结果传递给其他命令时。

## 使用模式

### 与搜索工具结合使用

在使用 tavily-search、web_search 或 searxng 等工具时：
1. 获取包含相关 URL 的搜索结果
2. 使用 jina-reader 从顶部结果中提取内容
3. 处理并总结提取的内容

```bash
# Example workflow
URL="https://example.com/article"
scripts/jina-reader.py "$URL" --format json | jq -r '.content'
```

### 批量处理

从多个 URL 中提取内容：
```bash
for url in $(cat urls.txt); do
  scripts/jina-reader.py "$url" -o "output/$(basename $url).md"
done
```

### 内容分析

将提取的内容传递给分析工具：
```bash
scripts/jina-reader.py https://example.com/article | wc -w
scripts/jina-reader.py https://example.com/article | grep -i "keyword"
```

## 选项

### Python 脚本 (`jina-reader.py`)

- `url`（必填）：要提取内容的 URL
- `-f, --format`：输出格式（`markdown` 或 `json`，默认为 `markdown`）
- `-t, --timeout`：请求超时时间（以秒为单位，默认为 30 秒）
- `-o, --output`：将输出保存到文件而不是标准输出

### Shell 脚本 (`jina-reader.sh`)

- `url`（必填）：要提取内容的 URL

## 限制

- **超时限制：** 默认为 30 秒。对于加载速度较慢的页面，可以使用 `-t` 参数延长超时时间。
- **速率限制：** Jina Reader API 有速率限制，请合理使用批量处理。
- **动态内容：** 无法提取页面加载后由客户端 JavaScript 生成的内容。
- **身份验证：** 无法访问需要登录或特殊请求头的页面。

## 故障排除

### 超时错误
```bash
scripts/jina-reader.py <url> -t 60  # Increase timeout
```

### 无效 URL
如果 URL 缺失，工具会自动添加 `https://` 前缀。为确保可靠性，请使用完整的 URL。

### 内容为空
某些页面可能会阻止爬取。可以尝试使用 Shell 脚本作为备用方案，或者验证 URL 是否可访问。

## 资源

### scripts/jina-reader.py
功能齐全的 Python 工具，支持 JSON 输出、元数据提取和文件保存。

### scripts/jina-reader.sh
轻量级的 Shell 脚本，用于快速提取 Markdown 内容。