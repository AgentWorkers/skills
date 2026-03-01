---
name: Kanban
slug: kanban
version: 1.0.0
homepage: https://clawic.com/skills/kanban
description: 构建多项目看板系统，实现看板的自动发现、任务处理的统一性，以及会话之间的路由信息持久化存储。
changelog: Initial release with project routing, board templates, and deterministic Kanban processing rules.
metadata: {"clawdbot":{"emoji":"📋","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---
## 设置（Setup）

如果 `~/kanban/` 不存在或为空，请静默地读取 `setup.md` 文件，并仅在用户确认后进行初始化。

## 使用场景（When to Use）

当用户需要一个可以在多个项目和对话中使用的看板系统时，可以使用此技能。代理应创建特定于项目的看板，记住每个看板的位置，并按照一致的规则处理任务。

## 架构（Architecture）

所有数据都存储在 `~/kanban/` 目录下。基础文件请参考 `memory-template.md`，看板结构请参考 `board-template.md`，项目路由规则请参考 `discovery-protocol.md`。

### 可选的项目本地模式（Optional project-local mode）：
（具体内容请参见 ````
{workspace}/.kanban/
├── board.md
├── rules.md
└── log.md
````）

## 快速参考（Quick Reference）

根据当前任务的需要，选择相应的文件进行操作：

| 主题 | 文件          |
|-------|--------------|
| 设置行为 | `setup.md`       |
| 内存与注册表模板 | `memory-template.md`   |
| 看板结构及示例 | `board-template.md`   |
| 如何查找各个项目看板 | `discovery-protocol.md` |
| 如何处理和更新卡片 | `processing-rules.md` |

## 核心规则（Core Rules）

### 1. 在读取或写入数据前先确定项目上下文（Resolve Project Context Before Reading or Writing）
- 在每次对话开始时，运行 `discovery-protocol.md` 中定义的流程。
- 如果项目范围不明确，请在写入数据前先询问用户。

### 2. 保持路由信息的一致性（Persist Routing So Any Agent Can Continue）
- 确保看板索引文件中包含工作区路径、项目别名和主要看板路径。
- 每次成功写入数据后，更新该项目条目的 `last_used` 字段。

### 3. 允许自定义看板布局（Allow Custom Board Shapes with a Stable Core Schema）
- 用户可以在项目规则文件中重命名看板中的列或添加自定义列。
- 每张卡片都必须包含以下可解析的核心字段：`id`、`title`、`state`、`priority`、`owner`、`updated`。

### 4. 严格按照规则处理卡片（Process Cards Deterministically）
- 按照 `processing-rules.md` 中规定的优先级和移动规则来处理卡片。
- 严禁跳过任何阻塞因素、依赖关系或明确的进行中（WIP）限制。

### 5. 保持操作的原子性和日志记录（Keep Writes Atomic and Logged）
- 在同一个操作周期内，同时更新看板文件并在项目日志中添加一条记录。
- 如果写入操作中途失败，应报告部分更新状态，而不是声称操作成功。

### 6. 隔离不同项目之间的看板（Keep Project Boards Isolated）
- 未经用户明确许可，严禁在不同项目看板之间移动或编辑卡片。
- 对于跨项目操作，先制定计划，然后再分别更新各个看板。

### 7. 保持对话的连贯性（Preserve Continuity Across Conversations）
- 在新对话开始时，先确定看板的位置并加载当前状态，然后再开始处理任务。
- 如果没有看板，从 `board-template.md` 初始化看板，将其注册到索引文件中，然后再继续操作。

## 常见错误（Common Traps）

- 所有项目使用同一个全局看板 -> 会导致优先级和责任归属不明确。
- 重命名看板列时未更新项目规则文件中的映射关系 -> 会导致卡片无法被正确处理。
- 写入看板更新内容后未刷新索引文件 -> 下一次代理会话无法找到该看板。
- 任务没有唯一标识符 -> 会导致卡片更新重复或引用错误。
- 将任务标记为已完成但未记录日志 -> 会导致后续会话无法追踪任务状态。

## 安全性与隐私（Security & Privacy）

**仅存储在本地的数据：**
- 看板文件和项目注册表位于 `~/kanban/` 或 `{workspace}/.kanban/` 目录下。

**不会执行以下操作：**
- 发起未声明的网络请求。
- 修改选定的看板范围之外的文件。
- 在日志缺失的情况下伪造看板历史记录。

## 相关技能（Related Skills）

如果用户同意安装，请使用以下命令安装相关工具：
- `workflow`：用于设计和管理工作流程。
- `projects`：用于组织项目并进行跨项目协作。
- `delegate`：用于分配任务负责人和制定任务交接流程。
- `daily-planner`：用于日常规划和任务排序。

## 反馈（Feedback）

- 如果觉得本技能有用，请使用 `clawhub star kanban` 给予评分。
- 为了保持信息更新，请使用 `clawhub sync` 命令。

---

（注：由于提供的 ````
~/kanban/
├── memory.md                  # Global status, integration, defaults
├── index.md                   # Project registry and board location map
├── templates/
│   └── board-template.md      # Canonical board format copy
└── projects/
    └── {project-id}/
        ├── board.md           # Active board for this project
        ├── rules.md           # Project-specific lane and policy definitions
        ├── log.md             # Board write log
        └── archive/
```` 和 ````
{workspace}/.kanban/
├── board.md
├── rules.md
└── log.md
```` 部分为空，因此这些部分的翻译内容保持空白。在实际翻译中，您需要根据这些代码块的实际情况进行填充。）