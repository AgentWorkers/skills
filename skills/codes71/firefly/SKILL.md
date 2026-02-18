---
name: firefly
description: 从 Firefly AI (fireflies.ai) 获取会议记录、会议摘要和待办事项。当用户询问有关会议、会议记录、会议笔记、待办事项或与 fireflies.ai 相关的任何信息时，可以使用此功能。该功能支持列出最近的会议、获取完整的会议记录、提取会议摘要以及通过关键词进行搜索。
---
# Firefly AI 集成

通过 Firefly AI 的 GraphQL API 获取会议数据。

## 设置

需要 `FIREFLY_API_KEY` 环境变量。请将其存储在网关的环境配置中。

## 使用方法

在 Node.js 环境中运行 `scripts/firefly.cjs` 脚本：

```bash
FIREFLY_API_KEY=<key> node scripts/firefly.cjs <command> [options]
```

### 命令

- **list** — 列出最近的会议。选项：`--days <n>`（默认值：14 天），`--limit <n>`（默认值：50 条）
- **transcript** — 包含时间戳的完整会议记录。需要提供 `--id <meeting_id>` 参数
- **summary** — 会议摘要、概述和待办事项。需要提供 `--id <meeting_id>` 参数
- **search** — 按会议标题或内容搜索。需要提供 `--keyword <text>` 参数，可选参数 `--limit <n>`

### 工作流程

1. 使用 `list` 命令查找会议并获取会议 ID。
2. 使用 `summary` 或 `transcript` 命令（并提供会议 ID）获取会议详细信息。
3. 使用 `search` 命令按主题搜索会议。

### 对于自定义查询

可以直接在 `https://api.fireflies.aigraphql` 上构建 GraphQL 查询。请参阅 `references/api.md` 以获取完整的查询规范和可用字段。

### 大量会议记录

完整的会议记录可能非常长（超过 2000 行）。当用户请求会议记录时：
- 如果用户希望保留记录，可以将其保存到工作区文件中。
- 如果用户需要特定信息，可以对记录进行总结或提取相关内容。
- 可以显示记录的前 50 行，并询问用户是否需要更多内容。