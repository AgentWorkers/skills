---
name: structured-memory
description: Build and maintain a structured memory system for OpenClaw workspaces using layered storage: daily memory as the source of truth, domain/module/entity/tag indexing, critical-facts extraction, and retrieval planning. Use when designing, initializing, updating, or operating a memory system that must scale across work topics such as business, finance, legal, HR, projects, operations, tech, routines, and personal context.
---

# 结构化内存（Structured Memory）

版本：`1.0.1`

使用此技能可在 OpenClaw 工作区中初始化和维护分层内存系统。

## 功能概述

- 以 `memory/YYYY-MM-DD.md` 作为数据源（即“事实的权威记录”）。
- 按日期、模块和实体构建可重建的索引。
- 将可重用的、对执行至关重要的信息提取到 `critical-facts/` 目录中。
- 在 `critical-facts/cards/` 目录下重新生成信息卡片（以对象形式展示）。
- 在首次初始化时，自动补充现有的 `memory/*.md` 文件中的历史数据。
- 通过 `preview` 和 `topic_summaries` 维护一个固定的、汇总的基准数据层。

## 默认操作规则

对于安装了此技能的代理来说，结构化内存不应仅被视为按需使用的工具。当当天有重要的任务进展、决策、阻碍因素、可重用的执行关键信息或其他对 `memory/YYYY-MM-DD.md` 有影响的更新时，代理应将其重建作为日常内存维护工作流程的一部分。

## 工作周期维护规则

在将重要更新写入 `memory/YYYY-MM-DD.md` 后，代理应在工作周期结束前重新生成当天的数据结构。这可确保索引、模块、实体和信息卡片与每日的数据源保持一致。

## 核心规则

1. 将 `memory/YYYY-MM-DD.md` 视为数据源。
2. 一级域名（`domain`）应保持固定且简洁。
3. 仅在需要时创建二级模块文件（`module`）。
4. 对于稳定的对象使用 `entities`，对于一次性使用的概念使用 `free_tags`。
5. 将可重用的执行关键信息存储在 `critical-facts/` 目录中。
6. 除非用户明确要求，否则不要以明文形式存储高敏感度的秘密信息。
7. 索引是可重建的缓存，而非事实的最终版本。
8. 每日的简短预览仅用于快速浏览；它不能替代多主题日的主题级摘要。

## 固定的第一级域名

使用以下固定域名：
- `strategy`（策略）
- `business`（业务）
- `organization`（组织）
- `finance`（财务）
- `legal`（法律）
- `project`（项目）
- `operations`（运营）
- `tech`（技术）
- `routines`（例行事务）
- `personal`（个人）
- `meta`（元数据）
- `misc`（其他）

## 创建模块时的注意事项

在创建新模块之前：
1. 检查是否已存在相应的模块。
2. 考虑该概念是否更适合作为实体（`entity`）来处理。
3. 判断该概念是否过于具体，是否应仅作为临时标签（`free_tag`）使用。
4. 仅当模块是一个可重用的主题类别时才创建它。

## 数据检索顺序

默认检索顺序：
1. `MEMORY.md`
2. `projects/*.md`
3. `critical-facts/cards/`（用于查询与服务器、服务、路径、ID、端点、仓库、依赖关系或稳定运营对象相关的关键信息）
4. `critical-facts/*.md`（在信息卡片缺失或内容过于简略时使用）
5. `memory-index/by-date.json`
6. `memory-modules/` 和 `memory-entities/`
7. 潜在的 `memory/YYYY-MM-DD.md` 文件

## 数据检索优先级规则

当代理需要检索跨日的任务记录、历史决策、稳定标识符、路径、端点、仓库名称、项目依赖关系或其他执行关键信息时，应优先查看结构化内存层，而不仅仅是依赖当前的聊天记录。

## 参考文档

根据需要阅读以下文档：
- `references/taxonomy.md`：域名和模块规则
- `references/write-rules.md`：写入/更新行为规范
- `references/retrieval-planner.md`：查询路由规则
- `references/index-schema.md`：JSON 和条目结构规范
- `references/critical-facts-policy.md`：敏感信息处理规则

## 脚本

### 操作模式

#### 1. 首次设置
在工作区启用此技能时运行一次：

```bash
python3 skills/structured-memory/scripts/init_structure.py
```

#### 2. 日常维护
在当天有重要更新后运行：

```bash
python3 skills/structured-memory/scripts/rebuild_one_day.py YYYY-MM-DD
```

#### 3. 验证/诊断
用于检查系统稳定性或搜索执行关键信息时使用：

```bash
python3 skills/structured-memory/scripts/check_idempotency.py YYYY-MM-DD
python3 skills/structured-memory/scripts/search_critical_facts.py <query>
```

- `scripts/init_structure.py`：安全地初始化工作区结构，并在首次运行时将现有的 `memory/*.md` 数据填充到索引和信息卡片中（除非明确跳过此步骤）。
- `scripts/parse_daily_memory.py`：将每日内存文件转换为标准化的索引条目，支持结构化条目和传统的列表式笔记格式。
- `scripts/upsert_by_date_index.py`：确定性地更新 `memory-index/by-date.json`。
- `scripts/update_topic_indexes.py`：从解析后的每日内存数据中添加模块和实体索引条目。
- `scripts/rebuild_one_day.py`：重新解析单日的记忆数据，并更新该日的按日期/模块/实体索引以及相应的 `critical-facts/` 条目。
- `scripts/check_idempotency.py`：验证重新构建同一天数据两次是否会产生稳定的结果。
- `scripts/summarize_daily_memory.py`：生成当前的稳定基准数据层：包括简短的预览内容（`preview`）和多主题日的主题摘要（`topic_summaries`）。
- `scripts/extract_critical_facts.py`：提取可重用的执行关键信息（如 IP 地址、路径、端点、服务名称、稳定 ID），并将其写入 `critical-facts/*.md`。
- `scripts/rebuild_critical_fact_cards.py`：根据相关实体/项目对信息进行分组，重新生成 `critical-facts/cards/` 目录下的信息卡片。该脚本能容忍格式错误、空值、全宽冒号或不规则的间距，以防止因单个错误条目导致整个重建过程失败。
- `scripts/search_critical_facts.py`：首先搜索信息卡片，然后搜索 `critical-facts/*.md` 文件。
- `tests/run_tests.py`：在代表性的内存数据样本上运行回归测试套件。

### 常用命令

```bash
python3 skills/structured-memory/tests/run_tests.py
python3 skills/structured-memory/scripts/init_structure.py
python3 skills/structured-memory/scripts/rebuild_one_day.py 2026-03-10
python3 skills/structured-memory/scripts/check_idempotency.py 2026-03-10
python3 skills/structured-memory/scripts/search_critical_facts.py structured-memory
```

## 数据源提醒

不要跳过或削弱 `memory/YYYY-MM-DD.md` 的作用。结构化内存依赖于每日的数据，并在此基础上提升检索效率；但它并不能替代数据源记录本身。

使用脚本进行结构化维护；对于小的、显而易见的更新，建议手动编辑。

## 稳定性说明

截至 2026-03-10，当前发布的版本为 `1.0.1`。在回归测试通过 206/206 项测试后，当前实现被固定下来。在再次更改摘要显示方式之前，请先更新测试代码，并确保与 `preview` 和 `topic_summaries` 的兼容性。