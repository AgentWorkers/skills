---
name: paperless-ngx
description: 在 Paperless-ngx 中管理文档：搜索、上传、添加标签以及检索文档。
homepage: https://github.com/paperless-ngx/paperless-ngx
metadata: {"clawdbot":{"requires":{"env":["PAPERLESS_URL","PAPERLESS_TOKEN"]},"primaryEnv":"PAPERLESS_TOKEN"}}
---

# Paperless-ngx

通过 Paperless-ngx REST API 进行文档管理。

## 配置

在 `~/.clawdbot/clawdbot.json` 中设置环境变量：

```json
{
  "env": {
    "PAPERLESS_URL": "http://your-paperless-host:8000",
    "PAPERLESS_TOKEN": "your-api-token"
  }
}
```

或者通过技能配置文件进行配置（支持使用 `apiKey` 简写）：

```json
{
  "skills": {
    "entries": {
      "paperless-ngx": {
        "env": { "PAPERLESS_URL": "http://your-paperless-host:8000" },
        "apiKey": "your-api-token"
      }
    }
  }
}
```

从 Paperless 的 Web 界面获取 API 密钥：设置 → 用户与组 → [用户] → 生成令牌。

## 快速参考

| 任务 | 命令 |
|------|---------|
| 搜索文档 | `node {baseDir}/scripts/search.mjs "query"` |
| 列出最近访问的文档 | `node {baseDir}/scripts/list.mjs [--limit N]` |
| 获取文档 | `node {baseDir}/scripts/get.mjs <id> [--content]` |
| 上传文档 | `node {baseDir}/scripts/upload.mjs <file> [--title "..."] [--tags "a,b"]` |
| 下载 PDF 文档 | `node {baseDir}/scripts/download.mjs <id> [--output path]` |
| 列出文档标签 | `node {baseDir}/scripts/tags.mjs` |
| 列出文档类型 | `node {baseDir}/scripts/types.mjs` |
| 列出相关联系人 | `node {baseDir}/scripts/correspondents.mjs` |

所有脚本均位于 `{baseDir}/scripts/` 目录下。

## 常见工作流程

### 查找文档

```bash
# Full-text search
node {baseDir}/scripts/search.mjs "electricity bill december"

# Filter by tag
node {baseDir}/scripts/search.mjs --tag "tax-deductible"

# Filter by document type
node {baseDir}/scripts/search.mjs --type "Invoice"

# Filter by correspondent
node {baseDir}/scripts/search.mjs --correspondent "AGL"

# Combine filters
node {baseDir}/scripts/search.mjs "2025" --tag "unpaid" --type "Invoice"
```

### 获取文档详情

```bash
# Metadata only
node {baseDir}/scripts/get.mjs 28

# Include OCR text content
node {baseDir}/scripts/get.mjs 28 --content

# Full content (no truncation)
node {baseDir}/scripts/get.mjs 28 --content --full
```

### 上传文档

```bash
# Basic upload (title auto-detected)
node {baseDir}/scripts/upload.mjs /path/to/invoice.pdf

# With metadata
node {baseDir}/scripts/upload.mjs /path/to/invoice.pdf \
  --title "AGL Electricity Jan 2026" \
  --tags "unpaid,utility" \
  --type "Invoice" \
  --correspondent "AGL" \
  --created "2026-01-15"
```

### 下载文档

```bash
# Download to current directory
node {baseDir}/scripts/download.mjs 28

# Specify output path
node {baseDir}/scripts/download.mjs 28 --output ~/Downloads/document.pdf

# Get original (not archived/OCR'd version)
node {baseDir}/scripts/download.mjs 28 --original
```

### 管理元数据

```bash
# List all tags
node {baseDir}/scripts/tags.mjs

# List document types
node {baseDir}/scripts/types.mjs

# List correspondents
node {baseDir}/scripts/correspondents.mjs

# Create new tag
node {baseDir}/scripts/tags.mjs --create "new-tag-name"

# Create new correspondent
node {baseDir}/scripts/correspondents.mjs --create "New Company Name"
```

## 输出格式

所有脚本均输出 JSON 格式的数据，便于解析。可以使用 `jq` 工具进行格式化：

```bash
node {baseDir}/scripts/search.mjs "invoice" | jq '.results[] | {id, title, created}'
```

## 高级用法

对于复杂的查询或批量操作，请参阅 [references/api.md](references/api.md) 以获取直接的 API 使用方法。

## 故障排除

- **“PAPERLESS_URL 未设置”**：请将其添加到 `~/.clawdbot/clawdbot.json` 的环境变量部分，或在 shell 中进行设置。
- **“401 Unauthorized”**：请检查 API 密钥（PAPERLESS_TOKEN）是否有效。如有需要，可在 Paperless 界面重新生成密钥。
- **“连接失败”**：请确认 Paperless 服务正在运行，并且提供的 URL 正确（包括端口号）。
- **上传失败且没有提示**：请查看 Paperless 的日志；可能是文件重复或格式不被支持。