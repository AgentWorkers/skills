---
name: readwise
description: 管理 Readwise 的高亮标记、书籍、每日阅读内容以及“稍后阅读”功能（save-for-later/read-it-later）。当用户希望将文章或网址保存到 Readwise 中、浏览自己的阅读列表、搜索已保存的文档、查看高亮标记和笔记、查看每日阅读记录、列出书籍或资料来源，或以任何方式与 Readwise/Reader 进行交互时，可以使用该功能。
---

# Readwise 与 Reader

您可以通过捆绑提供的 CLI 脚本来操作 Readwise（高亮显示功能、书籍管理、每日阅读回顾）和 Reader（用于保存待阅读文档的功能）。

## 设置

需要设置 `READWISE_TOKEN` 环境变量。您可以在 [https://readwise.io/access_token](https://readwise.io/access_token) 获取该令牌，该令牌适用于 Readwise 和 Reader 的 API。

## CLI 使用方法

```bash
scripts/readwise.sh [--pretty] <command> [args...]
```

### Reader 命令（用于文档管理）

```bash
# Save a URL to Reader
readwise.sh save "https://example.com/article" --location later --tags "ai,research"

# List reading list (inbox)
readwise.sh list --location later --limit 10

# Search documents by title/author
readwise.sh search "transformer"

# Update a document
readwise.sh update DOC_ID --location archive --tags "done,good"

# Delete a document
readwise.sh delete DOC_ID

# List all tags
readwise.sh tags
```

### Readwise 命令（用于高亮显示功能及书籍管理）

```bash
# Get today's daily review
readwise.sh review

# Export highlights (optionally for a specific book)
readwise.sh highlights --book-id 12345 --limit 20

# Get a single highlight
readwise.sh highlight 456789

# Create a highlight
readwise.sh highlight-create --text "Important quote" --title "Book Name" --note "My thought"

# Update highlight color/note
readwise.sh highlight-update 456789 --color blue --note "Updated note"

# Delete a highlight
readwise.sh highlight-delete 456789

# List books/sources
readwise.sh books --category articles --limit 10

# Get book details
readwise.sh book 12345
```

### 输出结果

所有命令的输出均为 JSON 格式。若需格式化输出，请添加 `--pretty` 选项。

## 常见工作流程

**保存文章并添加标签：**
```bash
readwise.sh save "https://arxiv.org/abs/2401.12345" --title "Cool Paper" --tags "ml,papers" --location later
```

**查看阅读列表：**
```bash
readwise.sh list --location later --limit 5
```

**查看今日的阅读高亮内容：**
```bash
readwise.sh review
```

**查找特定主题的高亮内容：** 先导出所有高亮内容，然后进行筛选，或直接在 Reader 中搜索相关文档：
```bash
readwise.sh search "attention mechanism"
readwise.sh highlights --updated-after "2024-01-01"
```

**归档已读文章：**
```bash
readwise.sh update DOC_ID --location archive
```

## API 参考

有关端点的详细文档、参数及响应格式，请参阅 [references/api.md](references/api.md)。

**重要说明：**
- **请求限制**：
  - Readwise v2：每分钟 240 次请求（列表相关端点为每分钟 20 次请求）。
  - Reader v3：每分钟 20 次请求（创建/更新相关端点为每分钟 50 次请求）。
- **分类**：
  - Books（书籍）：`books, articles, tweets, podcasts`
  - Reader：`article, email, rss, highlight, note, pdf, epub, tweet, video`
- **存储位置**（Reader）：`new, later, shortlist, archive, feed`
- **高亮颜色**：`yellow, blue, pink, orange, green, purple`