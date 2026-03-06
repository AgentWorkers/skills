---
name: Notion Calendar
slug: notion-calendar
version: 1.0.0
homepage: https://clawic.com/skills/notion-calendar
description: 使用具备日期感知功能的搜索、页面创建、重新调度等功能来管理 Notion 日历数据库，同时提供安全的工作流程以支持规划视图（planning views）。
changelog: "Initial release with date-aware Notion workflows, CLI fallback guidance, and safe create and reschedule patterns."
metadata: {"clawdbot":{"emoji":"N","requires":{"env":["NOTION_API_KEY"],"config":["~/notion-calendar/"]},"primaryEnv":"NOTION_API_KEY","os":["linux","darwin","win32"],"configPaths":["~/notion-calendar/"]}}
---
## 设置

首次使用时，请阅读 `setup.md` 以配置令牌访问权限、工作区范围以及数据写入的默认设置。

## 使用场景

用户希望将 Notion 数据库用作日历、编辑计划、任务调度表或带有日期标记的任务列表。该技能负责处理数据库模式的自动检测、时间窗口查询、页面创建、页面重新调度以及页面状态的更新。

## 所需条件

- `NOTION_API_KEY`：用于访问 Notion 官方 API。
- 需要与目标数据库集成 Notion 的相关工具或插件。
- 可选的外部命令行工具（CLI）：`notion`（来自 FroeMic/notion-cli），用于快速搜索和执行常见的创建（Create）、读取（Read）、更新（Update）、删除（Delete, CRUD）操作。

## 架构

所有数据存储在 `~/notion-calendar/` 目录下。具体数据结构请参考 `memory-template.md`。

```text
~/notion-calendar/
|-- memory.md        # Status, timezone defaults, and workspace context
|-- calendars.md     # Database and data source IDs plus property mappings
|-- templates.md     # Reusable page payload patterns
`-- safety-log.md    # Ambiguous matches, destructive confirmations, and rollbacks
```

## 快速参考

| 主题 | 对应文件 |
|-------|------|
| 设置与首次运行流程 | `setup.md` |
| 数据存储结构 | `memory-template.md` |
| 日历数据源映射 | `calendars.md` |
| 可重用的数据模板 | `templates.md` |
| 可选的 CLI 使用指南 | `cli-patterns.md` |
| 日历数据库模式说明 | `calendar-schema.md` |
| 数据查询、创建及重新调度流程 | `query-playbook.md` |
| 常见问题及解决方法 | `troubleshooting.md` |

## 核心规则

### 1. 将 Notion 日历视为基于日期的数据源
- 操作的基本单位是包含至少一个日期属性的 Notion 数据库或数据源。
- 该技能不提供对 Google 日历或 Notion 原生日历应用的直接控制功能。

### 2. 在执行操作前先检测数据库模式
- 在创建或更新数据之前，先获取数据库容器信息，并确定当前使用的 `data_source_id` 及相关属性名称。
- 在用户确认后，将页面的标题、日期、状态、负责人以及时区相关字段缓存到 `calendars.md` 中。

### 3. 使用明确的时间范围
- 将“下周”或“本季度”等时间描述转换为带有时区的 ISO 格式日期。
- 首先仅查询用户请求的时间窗口，如果结果集为空或不完整，再扩大查询范围。

### 4. 对于简单操作优先使用 CLI，复杂操作使用官方 HTTP 请求
- 如果已安装 `notion` CLI 且操作为基本搜索、读取或简单的页面 CRUD 操作，优先使用 CLI 以提高效率。
- 对于需要处理 `2025-09-03` 这类特定日期的数据源，或执行数据库模式迁移、执行不受支持的命令时，直接通过 `api.notion.com` 发送请求。

### 5. 写入前先读取数据，写入后验证结果
- 在创建、重新调度、归档或更改页面状态之前，先从数据库中获取目标时间窗口内的数据。
- 写入数据后，重新读取页面内容并确认最终的标题、日期、状态和 URL 是否正确。

### 6. 明确日历数据的含义
- 在写入日期值之前，确认数据行表示的是全天事件、单次事件还是特定时间范围内的事件。
- 该技能不支持重复事件；如果用户需要重复事件，应手动创建相应的模板或批量生成未来页面。

### 7. 遇到模糊情况时寻求明确信息
- 如果多个页面具有相同的标题，需询问具体的页面 URL 或页面 ID，或明确的时间范围。
- 对于标题匹配度较低的记录，切勿直接进行归档或移动操作。

## 常见错误

- 误以为仅使用数据库 ID 即可完成操作（注意：新版本的 Notion 可能需要 `data_source_id`）。
- 未检查数据库模式便直接写入名为“Date”的字段，可能导致错误地更新日历数据。
- 将 Notion 数据行视为重复事件（实际需要通过模板或批量操作来实现重复行为）。
- 仅根据标题进行重新调度，可能导致重复的调度计划或编辑内容被意外修改。
- 默认情况下查询过宽的时间范围，可能导致结果混乱或遗漏重要信息。

## 外部接口

| 接口 | 发送的数据 | 功能 |
|---------|-----------|---------|
| `https://api.notion.com/v1/search` | 搜索文本、设置过滤条件、分页参数 | 查找符合条件的数据库、数据源或页面 |
| `https://api.notion.com/v1/databases/*` | 数据库 ID | 获取数据库元数据和子数据源信息 |
| `https://api.notion.com/v1/data_sources/*` | 数据源 ID、过滤条件、排序规则、属性模式更新 | 查询数据行或更新日历模式 |
| `https://api.notion.com/v1/pages/*` | 页面属性和内容更新 | 创建页面、重新调度任务、更新页面状态 |

**注意：** 该技能不会向外部发送任何其他数据。

## 安全性与隐私

**会离开您机器的数据：**
- 通过 `api.notion.com` 发送的搜索文本、页面属性、日期和页面内容。

**保留在本地的数据：**
- 工作区上下文信息、属性映射关系以及存储在 `~/notion-calendar/` 目录中的默认设置。

**该技能不会：**
- 将 API 密钥存储在技能运行过程中使用的文件中。
- 访问未声明的第三方日历 API。
- 在未读取返回结果的情况下声明操作成功。
- 修改 `~/notion-calendar/` 目录之外的文件。

## 使用范围

该技能仅适用于以下场景：
- 与作为日历数据源使用的 Notion 数据库、数据源及页面配合使用。
- 当 `notion` CLI 可用时，优先使用该工具执行相关操作。
- 在 CLI 无法满足需求时，会直接调用 Notion 官方 API。

**该技能绝不会：**
- 配置 Notion 日历应用的偏好设置或账户信息。
- 代表用户同步 Google 日历账户。
- 对于不确定的数据进行隐藏性修改。

## 使用建议

在使用该技能前，请确保您信任 Notion，允许其访问页面标题、日期、状态字段及相关计划信息。

## 相关技能

如用户需要，可使用以下命令行工具进行扩展安装：
- `clawhub install <slug>`：
  - `api`：通用 REST API 请求模式及调试工具。
  - `dates`：精确的日期计算、时间范围处理及时区解析功能。
  - `pkm`：更全面的 workspace 组织管理工具。
  - `productivity`：用于任务和日程管理的执行系统。
  - `schedule`：处理多步骤调度任务的逻辑工具。

## 反馈建议

- 如觉得该技能有用，请给它点赞（使用 `clawhub star notion-calendar`）。
- 为了获取最新信息，请使用 `clawhub sync` 命令保持同步。