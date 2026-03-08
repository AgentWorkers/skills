---
name: opys-calendar-skill
description: 一个基于 Markdown 的本地日历工具，支持命令行界面（CLI）操作，并可选地与 Google 日历实现双向同步。
env:
  - GOOGLE_CLIENT_ID
  - GOOGLE_CLIENT_SECRET
  - GOOGLE_REDIRECT_URI
  - APP_BASE_URL
  - CALENDAR_AGENT_SNAPSHOT
  - CALENDAR_AGENT_DAYS
---# 日历 Markdown + Google 同步技能

使用此技能可以安全地查询/更新本地基于 Markdown 的日历，并将其与 Google 日历同步。

## 数据来源

- 文件：`calendar.md`
- 事件记录部分：`## Event Records`（包含被标记为 `event` 的 YAML 块）
- 事件检查列表部分：`## Event Checklist`

## 事件标识规则

- `id`：本地标识符
- `externalId`：用于唯一标识事件的跨系统标识符
- `googleEventIds`：每个日历对应的 Google 事件映射
- `updatedAt`：用于解决事件冲突的时间戳

请勿从现有记录中删除 `externalId`。

## 推荐的接口

通过仓库根目录下的 CLI 命令进行操作：

```bash
npm run cli -- <command>
```

## 安全的查询流程

1. 运行 `npm run cli -- summary` 以查看事件列表。
2. 如果需要原始 Markdown 格式的数据，运行 `npm run cli -- export`。

## 安全的更新流程

1. **添加新事件**：
   `npm run cli -- add --title "..." --start "<ISO>" --end "<ISO>" --category <id> [--shift-to-next|--allow-overlap]`
2. **更新事件**：
   `npm run cli -- update --id <event_id> [fields...]`
   在非交互式操作中，如果需要更改 `--start` 或 `--end`，请同时使用 `--shift-to-next` 或 `--allow-overlap` 参数。
3. **检查/取消事件**：
   `npm run cli -- check --id <event_id>` 或 `--undone`
4. **删除事件**：
   `npm run cli -- delete --id <event_id>`
5. **添加事件类别**：
   `npm run cli -- category-add --id <id> --label "Label" --color "#9ca3af" --description "..."`
6. **删除事件类别**：
   `npm run cli -- category-remove --id <id> --reassign <id>`

**冲突处理**：

- `add` 和 `update` 操作会检测与现有事件的冲突。
- 在交互式操作中，可以选择接受冲突、将事件时间调整到下一个可用时间槽，或指定自定义时间。
- 在非交互式操作中：
  - 使用 `--shift-to-next` 选项自动将事件时间调整到下一个可用时间槽。
  - 使用 `--allow-overlap` 选项允许事件时间与现有事件重叠。

**代理快照输出**：

- 每次执行修改操作的 CLI 命令都会生成一个 Markdown 快照。
- 默认路径：`./agent-snapshot.md`
- 可通过 `CALENDAR_AGENT_SNAPSHOT` 变量覆盖此路径。
- 默认情况下，快照包含过去 14 天内的事件；该时间范围可通过 `CALENDAR_AGENT_DAYS` 变量进行配置。
- 快照还会包含未来 7 天内的事件。

## 用户界面限制

- 用户界面不提供添加事件的表单或按钮。
- 事件只能通过 CLI 命令进行创建。
- 用户界面仍支持拖放、调整事件大小和标记事件状态（如已完成）。

## Google 同步流程

1. 在用户界面中登录 Google 账户。
2. 通过日历选择器选择目标日历。
3. 点击 **Sync Now** 以进行双向同步。

**同步状态文件**：

- 文件名：`.calendar-google-sync-state.json`

## 导出/导入

- **导出日历数据**：`npm run cli -- export --out backup-calendar.md`
- **导入日历数据**：`npm run cli -- import --in backup-calendar.md`

## 对代理的注意事项

- 请确保所有日期时间都使用 ISO 格式。
- 建议使用 CLI 命令进行操作，而非手动编辑 Markdown 文件。
- 如果在文档的开头部分（`frontmatter`）中手动修改了事件类别，请确保 `id`、`label` 和 `color` 字段的有效性。

## 环境变量

此技能使用以下环境变量（在 `.env` 文件中定义）：

- **Google 日历同步（可选）**
  - `GOOGLE_CLIENT_ID`：Google OAuth 客户端 ID
  - `GOOGLE_CLIENT_SECRET`：Google OAuth 客户端密钥
  - `GOOGLE_REDIRECT_URI`：重定向 URI，格式为 `http://localhost:<PORT>/api/google/auth/callback`

- **代理配置（可选）**
  - `CALENDAR_AGENT_SNAPSHOT`：用于保存 Markdown 快照的绝对或相对路径（默认为 `./agent-snapshot.md`）。
  - `CALENDAR_AGENT_DAYS`：快照中包含的历史天数（默认为 14 天）。
  - `PORT`：API 服务器端口（默认为 8787）。
  - `APP_BASE_URL`：前端界面的基础 URL。