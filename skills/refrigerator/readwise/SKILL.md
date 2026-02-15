---
name: readwise
description: **Access Readwise：高亮显示内容及用户保存的文章**  

Access Readwise 允许用户高亮标记阅读过程中的重点内容，并保存自己感兴趣的文章以供日后阅读。通过该功能，用户可以更高效地管理和组织自己的阅读材料。
homepage: https://readwise.io
metadata: {"clawdbot":{"emoji":"📚","requires":{"bins":["node"],"env":["READWISE_TOKEN"]},"primaryEnv":"READWISE_TOKEN"}}
---

# Readwise 与 Reader 功能

您可以访问 Readwise 中的精彩内容以及 Reader 保存的文章。

## 设置

从以下链接获取您的 API 令牌：https://readwise.io/access_token

将 API 令牌设置为您的环境变量：
```bash
export READWISE_TOKEN="your_token_here"
```

或者将其添加到 ~/.clawdbot/clawdbot.json 文件的 "env" 部分中。

## Readwise（精彩内容）

### 列出书籍/来源
```bash
node {baseDir}/scripts/readwise.mjs books [--limit 20]
```

### 从书籍中获取精彩内容
```bash
node {baseDir}/scripts/readwise.mjs highlights [--book-id 123] [--limit 20]
```

### 搜索精彩内容
```bash
node {baseDir}/scripts/readwise.mjs search "query"
```

### 导出所有精彩内容（分页显示）
```bash
node {baseDir}/scripts/readwise.mjs export [--updated-after 2024-01-01]
```

## Reader（保存的文章）

### 列出文档
```bash
node {baseDir}/scripts/reader.mjs list [--location new|later|archive|feed] [--category article|book|podcast|...] [--limit 20]
```

### 获取文档详情
```bash
node {baseDir}/scripts/reader.mjs get <document_id>
```

### 将 URL 保存到 Reader
```bash
node {baseDir}/scripts/reader.mjs save "https://example.com/article" [--location later]
```

### 在 Reader 中搜索
```bash
node {baseDir}/scripts/reader.mjs search "query"
```

## 注意事项：
- Readwise 的请求限制为每分钟 20 次；Reader 的请求限制可能有所不同。
- 所有命令的输出均为 JSON 格式，便于解析。
- 对于任何命令，可以使用 `--help` 选项查看详细帮助信息。