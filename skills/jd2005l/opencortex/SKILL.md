---
name: opencortex
description: >
  OpenClaw代理的自改进内存架构：该架构将默认的扁平化内存结构转换为一种结构化、能够自我维护的知识系统，并且这种系统会随着时间的推移变得越来越智能。适用场景包括：  
  (1) 设置新的OpenClaw实例时；  
  (2) 用户希望改进或整理内存管理方式时；  
  (3) 用户希望代理减少遗忘现象时；  
  (4) 使用最佳实践重新启动代理时。  
  **不适用场景**：运行时的内存搜索查询（请使用内置的内存管理工具）。  
  相关触发指令包括：  
  "set up memory"（设置内存结构）  
  "organize yourself"（整理内存内容）  
  "stop forgetting"（减少遗忘）  
  "memory architecture"（调整内存架构）  
  "self-improving"（实现自我优化）  
  "cortex"（内存管理核心模块）  
  "bootstrap memory"（重新初始化内存系统）  
  "memory optimization"（内存优化）。
---
# OpenCortex — 自我提升的记忆架构

将默认的 OpenClaw 代理转变为一个能够持续积累知识的系统。

## 功能介绍

1. **将记忆内容** 组织成特定用途的文件，而非单一的扁平化存储结构。
2. **执行夜间维护任务**，将每日的工作成果转化为永久性的知识记录。
3. **进行每周的整合分析**，发现跨日的行为模式和问题。
4. **建立行为准则**，以培养良好的记忆管理习惯。
5. **通过日常对话构建用户的语音特征档案**，用于代理的自动写作任务。
6. **提供安全的 Git 备份功能**，并自动清理敏感信息。

## 安装步骤

从该技能目录中运行 `scripts/install.sh` 脚本。该脚本是幂等的（可重复执行，不会造成数据丢失）。

```bash
bash scripts/install.sh
```

脚本将执行以下操作：
- 创建文件层次结构（不会覆盖现有文件）。
- 设置 cron 作业（每日数据整理、每周整合分析）。
- （可选）配置 Git 备份功能，并自动清理敏感信息。

安装完成后，您还可以自定义以下文件：
- `SOUL.md`：用于定义用户的个性和身份特征。
- `USER.md`：包含用户的个人信息。
- `MEMORY.md`：记录行为准则（根据需要添加或删除内容）。
- `.secrets-map`：用于存储用户的敏感信息，以便在备份时进行替换。

## 架构概述

```
SOUL.md          ← Identity, personality, boundaries
AGENTS.md        ← Operating protocol, delegation rules
MEMORY.md        ← Principles + memory index (< 3KB, loaded every session)
TOOLS.md         ← Tool shed: APIs, credentials, scripts with abilities descriptions
INFRA.md         ← Infrastructure atlas: hosts, IPs, services, network
USER.md          ← Human's preferences, projects, communication style
BOOTSTRAP.md     ← First-run checklist for new sessions

memory/
  projects/      ← One file per project (distilled, not raw)
  runbooks/      ← Step-by-step procedures (delegatable to sub-agents)
  archive/       ← Archived daily logs + weekly summaries
  YYYY-MM-DD.md  ← Today's working log (distilled nightly)
```

## 默认安装的行为准则

| 编号 | 名称 | 目的 |
|---|------|---------|
| P1 | 首先委托任务 | 评估任务，确定是否适合委托给子代理处理；确保自己随时可用。 |
| P2 | 将内容记录下来 | 将重要信息写入文件，而非仅保存在脑海中。 |
| P3 | 在执行外部操作前先询问 | 在发送邮件、发布公开内容或执行可能产生影响的操作前先确认。 |
| P4 | 文档化所有工具/API | 为每个工具/API 编写目标导向的使用说明。 |
| P5 | 记录决策过程 | 将决策及其理由都记录下来，避免重复提问。 |
| P6 | 子代理事后总结学习内容 | 子代理在完成任务后需将学习成果写入日志。 |

## 安装的 cron 作业

| 时间表 | 作业名称 | 功能描述 |
|----------|------|-------------|
| 每天凌晨 3 点（本地时间） | 数据整理 | 读取每日日志，整理成项目/工具/基础设施相关的文件，优化内容后存档。 |
| 每周日清晨 5 点 | 整合分析 | 分析一周内的行为模式、重复出现的问题及未完成的任务。 |

您可以通过编辑 `openclaw cron list`，然后使用 `openclaw cron edit <id> --cron "..."` 命令来调整 cron 作业的时间。

夜间数据整理任务还会通过 `clawhub update opencortex` 检查 OpenCortex 的更新情况。如果有新版本可用，系统会自动下载并安装。

## Git 备份（可选）

如果启用此功能，系统会生成以下文件：
- `scripts/git-backup.sh`：每 6 小时自动提交一次数据。
- `scripts/git-scrub-secrets.sh`：在提交前将敏感信息替换为占位符（`{{PLACEHOLDER}}`）。
- `scripts/git-restore-secrets.sh`：推送代码后恢复敏感信息。
- `.secrets-map`：将敏感信息映射到占位符（这些文件会被 Git 忽略，权限设置为 600）。

要将敏感信息添加到 `.secrets-map` 中，请使用以下格式：`actual_secret|{{PLACEHOLDER_NAME}}`。

## 自定义方法

- **添加新项目**：创建 `memory/projects/my-project.md` 文件，并将其添加到 `MEMORY.md` 的索引中。夜间数据整理任务会将相关的日志条目关联到该项目。
- **添加新行为准则**：将其添加到 `MEMORY.md` 的 `🔴 PRINCIPLES` 部分。内容应简短明了（一句话即可）。
- **添加操作手册**：创建 `memory/runbooks/my-procedure.md` 文件，其中包含详细的操作步骤。子代理可以直接参考这些手册。
- **添加新工具**：在 `TOOLS.md` 中记录工具的名称、使用方法及目标导向的功能描述，以便后续查询。

## 系统的持续改进机制

```
Daily work → daily log
  → nightly distill → routes to project/tools/infra/principles files
                     → optimization pass (dedup, prune stale, condense)
  → weekly synthesis → patterns, recurring problems, unfinished threads
Sub-agent work → debrief (P6) → daily log → same pipeline
Decisions → captured with reasoning (P5) → never re-asked
New tools → documented with abilities (P4) → findable by intent
```

每天，这个代理都会变得更加知识丰富、组织结构更加完善。