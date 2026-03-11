---
name: outlook-graph
description: 将 OpenClaw 连接到 Outlook 和 Microsoft Graph，以便进行电子邮件、日历、联系人和文件夹操作。这需要使用预先提供的访问令牌。当用户需要读取或发送 Outlook 邮件、搜索收件箱内容、管理日历事件、查看联系人信息，或调用与 Outlook 相关的 Microsoft Graph 端点时，可以使用此功能。该功能专为 openclaw 代理设计。
license: MIT
allowed-tools: Bash Read
metadata: {"clawdbot":{"emoji":"mailbox","requires":{"bins":["python3"],"env":["MS_GRAPH_ACCESS_TOKEN"]}}}
---
# Outlook Graph

该功能利用 Microsoft Graph，使 OpenClaw 能够与 Outlook 的邮件、日历、联系人及相关文件夹进行交互。专为 OpenClaw 代理设计。

## 使用场景

当用户需要执行以下操作时，可以使用此功能：
- 阅读最近的 Outlook 邮件
- 按关键词搜索邮件
- 发送 Outlook 邮件
- 查看邮件文件夹
- 列出即将发生的日历事件
- 创建日历事件
- 列出 Outlook 联系人
- 直接调用与 Outlook 相关的 Microsoft Graph 端点

## 默认工作流程

1. 选择最符合用户需求的特定命令。
2. 使用 `python3` 运行辅助脚本。
3. 读取 JSON 格式的输出结果。
4. 为用户提供有用的信息摘要（而非原始 JSON 数据），除非用户明确要求提供原始数据。

## 命令列表

### 阅读最近的邮件
```bash
python3 {baseDir}/scripts/outlook_graph.py mail-list --folder inbox --top 10
```

### 搜索邮件
```bash
python3 {baseDir}/scripts/outlook_graph.py mail-search --query "invoice OR payment" --top 10
```

### 发送邮件
```bash
python3 {baseDir}/scripts/outlook_graph.py mail-send \
  --to "alex@example.com" \
  --subject "Follow-up" \
  --body "Checking in on the open items."
```

### 列出即将发生的事件
```bash
python3 {baseDir}/scripts/outlook_graph.py calendar-list --days 7 --top 15
```

### 创建日历事件
```bash
python3 {baseDir}/scripts/outlook_graph.py calendar-create \
  --subject "Research sync" \
  --start "2026-03-10T15:00:00Z" \
  --end "2026-03-10T15:30:00Z" \
  --attendee "alex@example.com" \
  --body "Weekly research sync."
```

### 列出联系人
```bash
python3 {baseDir}/scripts/outlook_graph.py contacts-list --top 20
```

### 列出邮件文件夹
```bash
python3 {baseDir}/scripts/outlook_graph.py folders-list --top 50
```

### 获取通用 Graph 数据
```bash
python3 {baseDir}/scripts/outlook_graph.py graph-get \
  --path "/me/messages" \
  --query "\$top=5" \
  --query "\$select=subject,from,receivedDateTime"
```

### 发送通用 Graph 数据
```bash
python3 {baseDir}/scripts/outlook_graph.py graph-post \
  --path "/me/messages/{message-id}/reply" \
  --body-json '{"comment":"Thanks, received."}'
```

## 命令选择

优先使用专用命令：
- 浏览邮件箱或获取邮件摘要：`mail-list`
- 按关键词搜索邮件：`mail-search`
- 发送邮件：`mail-send`
- 查看即将召开的会议或日程安排：`calendar-list`
- 预订会议：`calendar-create`
- 查找联系人：`contacts-list`
- 查看文件夹结构：`folders-list`

仅当用户需要执行内置功能之外的操作时，才使用通用命令：
- `graph-get`
- `graph-post`
- `graph-patch`

## 数据收集与隐私

该功能仅在每次运行时收集用户的名称和域名，并将其发送到技能端点以用于匿名分析。**不会收集任何 Outlook Graph 数据或其他私人信息。**

如需停止数据收集，请设置以下环境变量：
```bash
export DISABLE_TELEMETRY=1
```

## 注意事项

- 时间格式应遵循 ISO 8601 标准（例如：`2026-03-10T15:00:00Z`）。
- `mail-search` 使用 Microsoft Graph 的搜索功能，依赖于邮件箱的索引机制。
- `calendar-create` 会在已登录用户的默认日历中创建事件。
- 有关端点详情和常用数据范围的详细信息，请参阅 [reference.md](reference.md)。