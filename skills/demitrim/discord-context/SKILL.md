---
name: discord-context
description: 为 Discord 论坛频道同步并缓存每个线程的上下文信息。在处理 `/discord-context` 命令时使用该功能，可以查询活跃的线程、列出缓存的上下文数据、检查线程缓存内容，或将某个线程链接到对应的内存 QMD 文件中。
user-invocable: true
metadata: {"openclaw":{"requires":{"bins":["node"],"env":["DISCORD_TOKEN"]}}}
---
# discord-context

运行 `node {baseDir}/scripts/discord-context-cli.js <command> ...`。

## 命令

- `poll [--guild <id>] [--forum <id>] [--workspace <path>]`
  - 从 Discord 中拉取活跃的讨论帖，并更新缓存中的新帖或已更新的帖子。
  - 需要 `DISCORD_TOKEN` 以及公会/论坛的 ID（可以通过参数或环境变量提供）。

- `context [threadId] [--workspace <path>] [--json]`
  - 不提供 `threadId` 时：列出缓存的讨论帖。
  - 提供 `threadId` 时：打印指定帖子的缓存内容和元数据。

- `link <threadId> <qmdName> [--workspace <path>]`
  - 将讨论帖链接到 `memory/<qmdName>.md` 文件，并更新其中的缓存内容。

## 环境变量

- `DISCORD_TOKEN`（`poll` 命令所需）
- `DISCORD_GUILD_ID`（`poll` 命令的默认公会 ID）
- `DISCORD_FORUM_CHANNEL_ID`（`poll` 命令的默认论坛 ID）
- `OPENCLAW_WORKSPACE`（默认工作区路径，通常为 `~/.openclaw/workspace`）

## 安全规则

- 绝不要将 Discord 令牌硬编码在代码中。
- 仅接受数字形式的公会/论坛 ID。
- `qmdName` 只能包含 `[a-zA-Z0-9_-]+` 的字符。
- 所有的读写操作都应限制在 `memory/` 目录及其子目录内进行。

## 文件路径

- 元数据缓存路径：`memory/discord-cache/thread-<id>.json`
- 文本缓存路径：`memory/discord-cache/thread-<id>-context.txt`
- 原始上下文文件路径：`memory/*.md`