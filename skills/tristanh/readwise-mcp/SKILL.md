---
name: readwise-mcp
description: 通过 `mcporter` CLI 设置、使用 OAuth 进行身份验证，并使用 Readwise MCP 服务器（mcp2.readwise.io/mcp）。当用户请求连接/验证 Readwise MCP 的身份、重置 OAuth 登录信息、解决登录问题（如重定向端口失效、状态异常），或者需要验证连接状态，或者希望通过 `mcporter` 运行 Readwise 工具时，可以使用此方法。
---

# Readwise MCP (mcporter)

此技能的文档内容被刻意设计得较为简短。详细的工作流程请参考：`skills/readwise-mcp/RECIPES.md`。

## 准备工作

```bash
command -v mcporter && mcporter --version
```

请确保您位于 Clawdbot 工作空间的根目录下，该目录中包含 `config/mcporter.json` 文件。

## 快速设置（首次使用）

```bash
# Add the server to the *project* config
mcporter config add readwise https://mcp2.readwise.io/mcp \
  --auth oauth \
  --description "Readwise MCP"

# Start OAuth login (will open a browser)
mcporter auth readwise --reset
```

## 验证功能是否正常

```bash
mcporter list readwise --output json
mcporter call readwise.reader_list_tags --args '{}' --output json
```

## OAuth 错误排查（常见问题）

### “无效的 OAuth 状态”
原因：您可能在已关闭的浏览器标签页中完成了授权操作（旧的授权尝试或旧的端口）。

解决方法：
- 关闭所有旧的 Readwise OAuth 标签页。
- 重新运行程序。

```bash
mcporter auth readwise --reset
```

### 即使重置后仍被重定向到旧端口
原因：浏览器会重用会话信息。

解决方法：
- 使用无痕模式（Incognito）或隐私模式（Private window）。
- 或者将新的授权 URL 复制到新的用户配置文件中。

### 显示 “等待浏览器授权…” 信息，但实际上您已经完成授权
您应该被重定向到以下地址：
`http://127.0.0.1:<PORT>/callback?code=...&state=...`

如果重定向到了其他端口，mcporter 会持续等待授权。

要找到正确的端口，请查看：
```bash
cat ~/.mcporter/credentials.json
```

检查 `redirect_uris` 的值，确保浏览器实际重定向的地址与预期一致。

## 使用服务器端功能

通用操作模式：

```bash
mcporter call readwise.<tool_name> --args '{...}' --output json
```

注意事项：
- `--args` 参数必须为有效的 JSON 格式（在 shell 命令中建议使用单引号）。
- 关于 Readwise 的文档存储位置：
  - `new`：收件箱（inbox）、稍后阅读（later）、收藏夹（shortlist）、归档（archive）、订阅源（feed，仅支持 RSS 格式）。

## 可用工具列表
- `readwise_search_highlights` — 搜索高亮显示的内容（支持矢量数据及可选的字段过滤）
- `reader_search_documents` — 搜索 Readwise 文档（混合搜索方式）
- `reader_create_document` — 将 URL 或 HTML 内容保存到 Readwise 文档中
- `reader_list_documents` — 列出最新文档（支持分页）
- `reader_get_document_details` — 获取文档的完整 Markdown 内容
- `reader_get_document_highlights` — 获取文档的高亮显示部分
- `reader_list_tags` — 列出文档的标签名称
- `reader_add_tags_to_document` / `reader_remove_tags_from_document` — 为文档添加/删除标签
- `reader_add_tags_to_highlight` / `reader_remove_tags_from_highlight` — 为高亮显示的内容添加/删除标签
- `reader_set_document_notes` / `reader_set_highlight_notes` — 设置文档的备注
- `reader_move_document` — 在收件箱、稍后阅读、收藏夹、归档之间移动文档
- `reader_edit_document_metadata` — 编辑文档元数据（包括标记为 “已阅读”）
- `reader_export_documents` — 将 Readwise 文档导出为 ZIP 文件

## 常用示例

### 1) 搜索高亮显示的内容（按主题或语义搜索）
```bash
mcporter call readwise.readwise_search_highlights \
  --args '{"vector_search_term":"incentives", "limit": 10}' \
  --output json
```

### 2) 搜索 Readwise 文档（混合搜索方式）
```bash
mcporter call readwise.reader_search_documents \
  --args '{"query":"MCP", "limit": 10}' \
  --output json
```

### 3) 列出收件箱中的最新文档（仅显示基本信息）
```bash
mcporter call readwise.reader_list_documents \
  --args '{
    "limit": 10,
    "location": "new",
    "response_fields":["title","author","url","category","location","created_at","tags"]
  }' \
  --output json
```

### 4) 获取文档的完整 Markdown 内容
```bash
mcporter call readwise.reader_get_document_details \
  --args '{"document_id":"<id>"}' \
  --output json
```

## 使用技巧的详细步骤（请参阅：`skills/readwise-mcp/RECIPES.md`）

相关技巧名称：
- 分类处理收件箱中的文档（或将其移至 “稍后阅读” 列表）
- 汇总订阅源中的内容（过去一天/一周）并标记为 “已阅读”
- 通过测验让用户确认是否已阅读归档文档
- 根据用户的阅读习惯推荐下一份合适的文档
- 文档管理工具（支持标签分类及清空收件箱）

## 收藏夹的功能说明（重要）
Readwise 支持将文档添加到 “收藏夹” 中，但不同用户的使用方式可能有所不同。

默认设置（大多数用户）：
- 将文档添加到收藏夹的同时，会将其移至 “稍后阅读” 列表。
- 另一种设置方式是：将文档直接移至收藏夹。

因此，在执行任何收藏操作之前，请先确认用户的具体设置。如果不确定用户的设置方式，请默认按照上述默认规则操作。

## 安全性/默认行为
当某个工作流程涉及对文档的修改操作（如添加标签、移动文档、设置备注或标记为 “已阅读”）时，系统会首先显示一个 **只读版本**，并请求用户确认是否同意这些更改。