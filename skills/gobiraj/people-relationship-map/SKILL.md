---
name: people-relationship-map
description: OpenClaw 的个人客户关系管理（CRM）工具及关系图功能：该工具可以记录个人信息、他们之间的联系关系，以及您对他们的了解。所有数据以 Obsidian 支持的 Markdown 格式存储，并通过 JSON 格式生成关系图索引。适用于需要了解谁认识谁、准备会议，或提醒您处理过时的人际关系的场景。
version: 0.1.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
    homepage: https://github.com/gobiraj/people-relationship-map
---
# 人物关系图

这是一个轻量级的个人CRM工具，它将人物视为节点，将他们之间的联系视为边来记录。所有数据都存储在兼容Obsidian的Markdown文件中（每个人对应一个文件），并使用JSON图谱索引以实现快速查询。

## 工作区布局

```
<workspace>/people/
├── _graph.json          # Node + edge index (source of truth for connections)
├── _alex-chen.md        # One Markdown file per person
├── _jordan-lee.md
└── ...
```

每个人对应的文件都使用以下模板：

```markdown
# Alex Chen

- **Tags:** #colleague #engineering
- **Org:** Acme Corp
- **Role:** Staff Engineer
- **Met:** 2025-06-15
- **Last contact:** 2026-02-20
- **Tier:** close

## Notes
- 2026-02-20 — Mentioned looking for a new apartment in Brooklyn
- 2026-01-10 — Helped me debug the auth migration

## Connections
- [[Jordan Lee]] — same team at Acme
- [[Sam Patel]] — college roommates
```

 `_graph.json` 文件存储了机器可读的图谱信息：

```json
{
  "nodes": {
    "alex-chen": {
      "displayName": "Alex Chen",
      "tags": ["colleague", "engineering"],
      "org": "Acme Corp",
      "role": "Staff Engineer",
      "met": "2025-06-15",
      "lastContact": "2026-02-20",
      "tier": "close",
      "file": "_alex-chen.md"
    }
  },
  "edges": [
    {
      "from": "alex-chen",
      "to": "jordan-lee",
      "label": "same team at Acme"
    }
  ]
}
```

## 命令

所有命令都通过Python脚本来执行。可以通过以下方式运行它们：

```bash
python3 {baseDir}/scripts/relmap.py <command> [options]
```

### 添加一个人物

```bash
python3 {baseDir}/scripts/relmap.py add \
  --name "Alex Chen" \
  --tags colleague,engineering \
  --org "Acme Corp" \
  --role "Staff Engineer" \
  --tier close \
  --note "Met at the offsite in Denver"
```

人物关系等级分为：`close`（亲密关系）、`regular`（普通关系）和`acquaintance`（熟人关系）（默认为`acquaintance`）。

### 连接两个人物

```bash
python3 {baseDir}/scripts/relmap.py link \
  --from "Alex Chen" \
  --to "Jordan Lee" \
  --label "same team at Acme"
```

### 为一个人物添加备注

```bash
python3 {baseDir}/scripts/relmap.py note \
  --person "Alex Chen" \
  --text "Mentioned looking for a new apartment in Brooklyn"
```

此操作同时会更新该人物的`lastContact`时间（即最后一次联系的时间）。

### 更新最后联系时间（不添加备注）

```bash
python3 {baseDir}/scripts/relmap.py touch --person "Alex Chen"
```

### 查询命令

```bash
# Show everything about a person
python3 {baseDir}/scripts/relmap.py show --person "Alex Chen"

# Find who is connected to a person
python3 {baseDir}/scripts/relmap.py connections --person "Alex Chen"

# Find all people at an org
python3 {baseDir}/scripts/relmap.py query --org "Acme Corp"

# Find by tag
python3 {baseDir}/scripts/relmap.py query --tag engineering

# Find by tier
python3 {baseDir}/scripts/relmap.py query --tier close

# Search notes for a keyword
python3 {baseDir}/scripts/relmap.py search --query "apartment"

# List all people
python3 {baseDir}/scripts/relmap.py list
```

### 关系更新报告

```bash
python3 {baseDir}/scripts/relmap.py stale \
  --close-days 14 \
  --regular-days 30 \
  --acquaintance-days 90 \
  --format message
```

该命令会生成一份报告，列出在你设定的关系等级阈值内、你尚未联系过的人物的信息。

### 将图谱导出为Mermaid格式（可选工具）

```bash
python3 {baseDir}/scripts/relmap.py mermaid
```

该命令会生成一个Mermaid格式的图谱（`graph LR`），你可以将其粘贴到任何Markdown渲染器中查看。

## 自动捕获行为

当用户在对话中提到某个人物并提供了相关关系信息时，系统应自动执行相应的命令：
- “我刚和Alex Chen喝了咖啡” → `touch --person "Alex Chen"` + `note --person "Alex Chen" --text "一起喝了咖啡"`
- “Alex和Jordan在同一团队工作” → `link --from "Alex" --to "Jordan" --label "同一团队"`
- “记得Sam的生日是3月12日” → `note --person "Sam" --text "生日：3月12日"`

只有当意图明确时才会自动执行操作；如果意图不明确，系统会先询问用户确认。确认信息应简洁明了（例如：“已为Alex记录”。）

## Cron任务——每周关系更新报告

系统应每周运行一次关系更新报告，并将结果发送到用户的主要通讯渠道（WhatsApp/Telegram）。推荐的时间安排是每周日早上9点。

```
python3 {baseDir}/scripts/relmap.py stale --format message
```

`--format message` 参数可以生成一份简洁、适合在聊天中使用的报告。

## 对系统代理的建议：
- 名称应统一格式化：例如“Alex”、“Alex Chen”和“alex chen”都应映射到同一个节点。脚本会对存储的名称进行模糊匹配。
- 当用户询问“我在[公司]认识谁？”时，使用`query --org`命令。
- 当用户询问“介绍一下[Person]”时，使用`show --person`命令。
- 当用户询问“[Person]和谁有联系？”时，使用`connections`命令。
- 在会议前，可以使用`show`命令展示相关人物的信息。
- 这些Markdown文件是专为Obsidian设计的——如果用户同步了`people`文件夹，其中的 wikilinks、标签和前言内容都能正常显示。