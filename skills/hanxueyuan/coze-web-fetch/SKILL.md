---
name: coze-web-fetch
description: 使用 coze-coding-dev-sdk 从 URL 中获取并提取内容。支持网页、PDF 文件、Office 文档（doc/docx/ppt/pptx/xls/xlsx/csv）、文本文件、电子书（epub/mobi）、XML 文件以及图片。返回包含文本、图片和链接的结构化内容。
homepage: https://www.coze.com
metadata: { "openclaw": { "emoji": "🦞", "requires": { "bins": ["npx"] } } }
---
# Coze Web Fetch

使用 coze-coding-dev-sdk 从任意 URL 获取并提取结构化内容。支持返回文本、图片和链接，并支持多种输出格式。

## 快速入门

### 基本获取

```bash
npx ts-node {baseDir}/scripts/fetch.ts -u "https://example.com/article"
```

### 多个 URL

```bash
npx ts-node {baseDir}/scripts/fetch.ts \
  -u "https://example.com/page1" \
  -u "https://example.com/page2"
```

### 以 Markdown 格式输出

```bash
npx ts-node {baseDir}/scripts/fetch.ts \
  -u "https://docs.python.org/3/tutorial/" \
  --format markdown
```

### 以 JSON 格式输出

```bash
npx ts-node {baseDir}/scripts/fetch.ts \
  -u "https://example.com/document.pdf" \
  --format json
```

### 仅返回文本（不含图片/链接）

```bash
npx ts-node {baseDir}/scripts/fetch.ts \
  -u "https://example.com/article" \
  --text-only
```

## 脚本选项

| 选项                | 描述                                      |
| ---------------------- | ---------------------------------------- |
| `-u, --url <url>`    | 需要获取的 URL（可重复输入）                   |
| `--format <fmt>`     | 输出格式（`json`, `text`, `markdown`，默认为 `text`）     |
| `--text-only`        | 仅提取文本内容                          |
| `--help`             | 显示帮助信息                               |

## 支持的文档格式

| 格式                | 扩展名                                      |
| ---------------------- | ---------------------------------------- |
| PDF                | .pdf                                        |
| Office 文档          | .doc, .docx, .ppt, .pptx, .xls, .xlsx, .csv         |
| 文本文件            | .txt, .text                                 |
| 电子书              | .epub, .mobi                                |
| XML                | .xml                                        |
| 图片                | .jpg, .png, .gif, .webp, etc.                       |
| 网页                | .html, .htm 或任意 URL                             |

## 输出格式

### 文本（默认格式）

```
============================================================
FETCHED CONTENT
============================================================
Title: Example Article
URL: https://example.com/article

------------------------------------------------------------
CONTENT
------------------------------------------------------------
[TEXT] This is the main article content...

[IMAGE] https://example.com/image.jpg

[LINK] Related Article -> https://example.com/related
```

### Markdown 格式

```markdown
# Example Article

**URL**: https://example.com/article

---

## Content

This is the main article content...

![Image](https://example.com/image.jpg)

- [Related Article](https://example.com/related)
```

### JSON 格式

以 JSON 格式输出原始 API 响应内容及完整结构。

## 内容类型

该工具可提取以下三种类型的内容：

| 类型                | 描述                                      |
| ---------------------- | ---------------------------------------- |
| 文本                | 从页面中提取的文本内容                         |
| 图片                | 包含显示信息的图片链接                         |
| 链接                | 页面中发现的超链接                             |

## 注意事项

- 如果只需要文本，可以使用 `--text-only` 选项以获得更简洁的输出结果。
- PDF 和 Office 文档会自动被解析。
- 图片在传输前会重新签名以确保安全访问。
- 可以通过单个命令同时获取多个 URL 的内容。