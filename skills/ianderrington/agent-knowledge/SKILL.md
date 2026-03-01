---
name: knowledge
description: 统一的知识捕获与检索系统，支持处理URL、视频/文章/论文摘录、社交媒体帖子以及代理研究输出等内容。适用于保存任何日后可能需要再次查找的信息、总结外部内容、追踪信息来源，或回答“我们把那个资料存放在哪里了？”这类问题。
---
# 知识管理技能

基于文件的知识组织方式：快速捕获信息，便于后续搜索，同时实现自动清理。

## 安装

```bash
clawhub install knowledge
```

该命令用于安装 `scripts/know`；请将其添加到系统的 `PATH` 环境变量中，或直接使用完整路径进行安装：
```bash
~/.openclaw/skills/knowledge/scripts/know
```

## 存储位置

默认存储路径：`~/.soulshare/agent/knowledge/`

存储路径可通过 `~/.config/know/config` 文件或环境变量 `KNOWLEDGE_DIR` 进行配置：
```
knowledge/
├── INDEX.md      # Auto-maintained browsable index
├── urls/         # Bookmarked URLs
├── extracts/     # Video/article/paper summaries
├── posts/        # Social content (tweets, threads)
└── research/     # Agent-generated research
```

## 添加内容

```bash
know add url <url> --title "..." --tags "a,b" [--summary "..."]
know add video <url> --title "..." --tags "a,b" [--summary "..."]
know add extract --source <url> --type video|article|paper --title "..." --tags "a,b"
know add post --source <url> --title "..." --tags "a,b"
know add research --title "..." --tags "a,b" [--summary "..."]
```

每次添加新内容时，系统会自动生成一个带有 YAML 标签的 Markdown 文件，并更新 `INDEX.md` 文件以记录内容索引。

## 搜索

```bash
know search "query"           # Grep across all entries
know recent --limit 10        # Recent entries
know list --tags security     # Filter by tag
```

## 清理与维护

**建议**：定期运行 `know tidy --fix` 命令（例如在系统启动时或每晚通过 cron 任务执行）以保持数据整洁。

## 数据模型（Markdown 文件的格式要求）

```yaml
---
type: url|extract|post|research
title: "Entry title"
source_url: "https://..."
source_kind: url|video|article|paper|post|research
tags: ["tag1", "tag2"]
added: "2026-02-26"
added_by: "agent-name"
summary: "One-line summary"
---
```

## 与 QMD 的集成

普通的 Markdown 文件可以被 QMD 系统索引和查询：
```bash
qmd collection add ~/.soulshare/agent/knowledge --name knowledge
qmd search "query" --collection knowledge
```

## 使用规范：

- 如果某条信息日后可能会用到，请立即使用 `know add` 命令将其添加到知识库中。
- 不要将信息仅保存在格式为 `memory/YYYY-MM-DD.md` 的文件中。
- 每条信息都需要添加标签和简要说明。
- 让 `know tidy --fix` 命令负责处理内容的格式标准化工作。