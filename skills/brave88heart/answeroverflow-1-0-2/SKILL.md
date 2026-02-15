---
name: answeroverflow
description: 通过 Answer Overflow 搜索索引在 Discord 社区中的讨论。您可以在这里找到针对编程问题、库使用问题以及社区问答的解决方案，这些内容仅存在于 Discord 的对话中。
---

# Answer Overflow 技能

通过 Answer Overflow 搜索已索引的 Discord 社区讨论。非常适合查找编程问题、库相关问题的解决方案以及社区问答的答案。

## 什么是 Answer Overflow？

Answer Overflow 对公开的 Discord 支持频道进行索引，并允许通过 Google 或直接 API 访问这些频道。非常适合查找仅存在于 Discord 对话中的答案。

## 快速搜索

使用 `web_search` 来查找 Answer Overflow 的结果：
```bash
# Search for a topic (Answer Overflow results often appear in Google)
web_search "site:answeroverflow.com prisma connection pooling"
```

## 获取帖子内容

### Markdown 格式的内容
在 URL 前添加 `/m/` 前缀或在文件名后添加 `.md` 后缀，即可获取 Markdown 格式的内容：
```
# Standard URL
https://www.answeroverflow.com/m/1234567890123456789

# With .md suffix (alternative)
https://www.answeroverflow.com/m/1234567890123456789.md
```

### 使用 `web_fetch`

### 请求头
在发送请求时，API 会检查 `Accept: text/markdown` 请求头，以返回 Markdown 格式的内容。

## MCP 服务器（参考）

Answer Overflow 拥有一个名为 MCP 的服务器，地址为 `https://www.answeroverflow.com/mcp`，提供了以下工具：

| 工具 | 描述 |
|------|-------------|
| `search_answeroverflow` | 在所有已索引的 Discord 社区中搜索。可以按服务器或频道 ID 进行过滤。 |
| `search_servers` | 查找在 Answer Overflow 上被索引的 Discord 服务器，并返回服务器 ID 以供进一步搜索。 |
| `get_thread_messages` | 获取特定帖子/讨论的所有消息。 |
| `find_similar_threads` | 查找与给定帖子相似的帖子。 |

## URL 模式

| 模式 | 示例 |
|---------|---------|
| 帖子 | `https://www.answeroverflow.com/m/<message-id>` |
| 服务器 | `https://www.answeroverflow.com/c/<server-slug>` |
| 频道 | `https://www.answeroverflow.com/c/<server-slug>/<channel-slug>` |

## 常见搜索词

```bash
# Find Discord.js help
web_search "site:answeroverflow.com discord.js slash commands"

# Find Next.js solutions
web_search "site:answeroverflow.com nextjs app router error"

# Find Prisma answers
web_search "site:answeroverflow.com prisma many-to-many"
```

## 提示

- 结果来自真实的 Discord 对话，因此内容可能较为随意（非正式）。
- 许多帖子在给出解决方案之前会有来回的讨论。
- 请查看服务器/频道名称以了解上下文（例如，官方支持频道与社区频道）。
- 许多开源项目都会在这里索引他们的 Discord 支持频道。

## 链接

- **官方网站：** https://www.answeroverflow.com
- **文档：** https://docs.answeroverflow.com
- **MCP：** https://www.answeroverflow.com/mcp
- **Discord：** https://discord.answeroverflow.com