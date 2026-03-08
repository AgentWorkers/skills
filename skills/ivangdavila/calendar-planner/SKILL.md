---
name: Calendar Planner
slug: calendar-planner
version: 1.0.0
homepage: https://clawic.com/skills/calendar-planner
description: 通过 CLI（命令行接口）适配器，在 Google 日历、Outlook、Apple 日历和 CalDAV 之间协调工作和生活安排；实现冲突检测与修复功能，并定期进行周度回顾。
changelog: "Initial release with multi-calendar CLI playbooks, Life Grid planning rules, and local scripts for merge, guard, and weekly review workflows."
metadata: {"clawdbot":{"emoji":"C","requires":{"bins":["python3","jq"]},"os":["linux","darwin","win32"],"configPaths":["~/calendar-planner/"]}}
---
# 日历规划器

这是一个用于工作、家庭、健康、旅行、深度学习以及恢复等场景的日历规划工具，支持与多种命令行日历适配器集成。

## 设置

首次使用时，请阅读 `setup.md` 以获取集成指南。在创建 `~/calendar-planner/` 目录之前，请先思考当前需要解决的规划问题；在向任何日历添加内容或发送邀请之前，请先确认相关事宜。

## 使用场景

当用户需要日历规划、时间安排调整、每周任务规划、时间块分配、会议优先级排序、家庭事务管理、预约安排，或者多日历数据整理时，可以使用该工具。该工具特别适用于需要在 Google Calendar、Outlook、Apple Calendar 和 CalDAV 等日历之间协调任务和限制的情况。

该工具能够提供一个经过深思熟虑的规划方案，明确指出各项决策的权衡点，并提供安全的操作步骤。当不同日历之间的数据不一致、优先级冲突，或者用户需要调整整个星期的日程安排时，该工具比简单的日程辅助工具更为高效。

## 架构

本地数据持久化功能是可选的，且需用户明确同意后才会启用。

```text
~/calendar-planner/
├── memory.md        # User-stated planning rules and activation preferences
├── calendars.md     # Provider map, calendar names, and write boundaries
├── rules.md         # Buffers, focus rules, recurring constraints
├── plans.md         # Current week plans and reschedule decisions
└── inbox.md         # Loose commitments that still need placement
```

## 快速参考

仅加载对当前规划决策有帮助的信息。首先了解相关协议和命令；只有在用户需要数据持久化时，才启用内存存储功能。

| 主题 | 文件 |
|-------|------|
| 设置与激活 | `setup.md` |
| 可选的数据持久化设置 | `memory-template.md` |
| 日常任务规划方法 | `planning-protocol.md` |
| 针对不同领域的规划策略 | `life-domains.md` |
| 命令行适配器使用指南 | `commands.md` |
| 合并标准化日历数据 | `calendar_merge.py` |
| 检查时间冲突与缓冲区问题 | `calendar_guard.py` |
| 生成每周规划总结 | `week_plan.py` |

## 要求

请根据用户的实际需求，选择最合适的日历适配器。仅安装当前工作流程所需的工具。

| 功能需求 | 命令行工具 | 备注 |
|------|------------|-------|
| Google Calendar | `gcalcli` | 通过用户的 OAuth 客户端使用 Google Calendar API |
| Outlook / Microsoft 365 | Microsoft Graph PowerShell | 仅使用委托的日历访问权限 |
| Apple Calendar | `osascript` | 在 macOS 上自动化操作 Calendar.app |
| CalDAV 和 iCloud 同步 | `khal` 加 `vdirsyncer` | 先进行本地同步，再根据本地数据制定计划 |
| 本地数据分析 | `python3` 和 `jq` | 用于数据合并、冲突检测和每周规划审查 |

## 核心规则

### 1. 从实际需求出发，而非从 CRUD 操作开始
- 首先确定哪些任务需要保留、移动、取消、保护或推迟。
- 仅询问那些会影响任务安排的事实，例如截止日期、旅行时间、参与者限制或受保护的时间段。
- 使用 `planning-protocol.md` 将复杂的请求转化为明确的规划决策。

### 2. 区分固定任务和灵活任务
- 在重新安排日历之前，将所有任务分类为固定任务、灵活任务、待处理任务、旅行任务或恢复任务。
- 固定任务未经明确批准不得移动；灵活任务可以调整。
- 使用 `life-domains.md` 防止工作任务影响家庭、健康或睡眠时间。

### 3. 在进行任何操作前，先合并所有可见的日历数据
- 先读取所有相关的日历数据（包括用户指定的共享日历）。
- 将隐藏的日历视为潜在风险，而非空闲时间。
- 当需要合并多个日历的数据时，使用 `calendar_merge.py` 生成统一的时间线。

### 4. 保护关键时间节点、准备缓冲时间，并确保任务顺利完成
- 为会议和预约预留准备时间、通勤时间、任务切换时间和后续处理时间。
- 没有缓冲时间的日程安排实际上是没有实际执行能力的。
- 使用 `calendar_guard.py` 检查时间冲突、时间空白或日程过载的情况，再提出修改建议。

### 5. 所有修改操作均需用户明确批准
- 在通过任何适配器创建、更新、删除日历内容或发送邀请之前，请先获得用户同意。
- 默认情况下，先生成草稿计划或进行模拟操作。
- 如果用户选择数据持久化，需在本地笔记中区分只读和可写日历。

### 6. 保持数据记录的清晰性和简洁性
- 仅保存用户明确指定的规则、重复性任务、受保护的时间段以及使用偏好。
- 除非用户特别要求，否则不要存储参与者列表、详细事件说明或私人备注。
- 用户同意数据持久化后，再使用 `memory-template.md`。

### 7. 最终提供可执行的规划方案
- 每个规划结果应包括最终确定的任务安排、剩余的冲突事项以及后续处理方案。
- 如果有多个选项，需用一句话说明最佳方案。
- 当终端环境更适合执行时，可以使用 `week_plan.py` 或 `commands.md` 中的适配器命令。

## 日常任务规划协议（Life Grid Protocol）

详细内容请参阅 `planning-protocol.md`：

- **数据收集**：记录实际需要完成的任务，而不仅仅是用户请求的事件。
- **任务分类**：将任务分为固定任务、灵活任务、待处理任务、旅行任务或恢复任务。
- **规则制定**：在安排新任务之前，确保非可协商的内容得到保护。
- **问题解决**：如果当前周的日程已经混乱，需明确指出哪些任务需要调整、取消或降级。
- **最终结果**：为用户提供一个推荐的规划方案以及下一步的具体操作建议。

## 常见错误

- 仅解决会议请求，而忽略了其他相关问题（如接送孩子、旅行安排、用药时间或专注时间）。
- 在未查看所有相关日历数据的情况下就调整任务安排，可能导致隐藏的冲突和信任问题。
- 默认将某些任务视为不可更改或可随意调整的，会导致计划不稳固或日历混乱。
- 未预留足够的时间进行会议准备或恢复，可能导致日程安排失败。
- 未经批准就修改共享日历内容，可能会给他人带来不便或产生社交麻烦。
- 本地保存过多私人信息，会增加隐私风险。

## 外部接口

仅允许用户明确选择的适配器与远程服务进行数据交互。每次只使用一个接口，以确保数据传输的清晰性。

| 接口 | 发送的数据 | 用途 |
|----------|-----------|---------|
| https://www.googleapis.com/calendar/v3/* | 用于读取或写入 Google Calendar 的事件元数据 | 通过 `gcalcli` 进行 Google Calendar 操作 |
| https://graph.microsoft.com/v1.0/* | 用于读取或写入 Outlook 或 Microsoft 365 的事件元数据 | 通过 Microsoft Graph PowerShell 进行日历操作 |
| 用户配置的 CalDAV 服务器 | 用于同步配置的日历数据 | 通过 `vdirsyncer` 进行同步，并在本地使用 `khal` |

**注意**：不会向外部发送其他任何数据。

## 安全性与隐私

**本地保存的数据：**
- `~/calendar-planner/` 目录中的可选数据持久化设置
- 由 `calendar_merge.py`、`calendar_guard.py` 和 `week_plan.py` 生成的标准化日历数据
- 在 macOS 上通过 Calendar.app 自动化的 Apple Calendar 数据

**可能被传输到外部的数据：**
- 通过用户选择的 Google、Microsoft 或 CalDAV 适配器发送的日历元数据

**本工具不会：**
- 未经批准就创建、移动或删除日历条目
- 未经通知就发送邀请或更新共享日历
- 从未关联的文件或对话中推断用户规则
- 未经用户授权，不会访问用户的电子邮件、联系人或任务信息

## 信任机制

使用本工具时，如果选择了 Google Calendar、Microsoft Graph 或 CalDAV 适配器，日历元数据将通过配置的命令行工具传输给这些服务。请确保信任这些服务提供商以及运行这些命令的本地设备。

## 使用范围

本工具仅用于：
- 在用户认可的日历范围内规划和审核日程安排
- 生成模拟操作命令、标准化的规划文件以及本地审查报告
- 在用户明确同意的情况下，仅保存必要的规划数据

**本工具绝不会：**
- 自动修改自身的配置文件
- 未经批准就自动接受邀请或重新安排任务
- 未经确认就扩展对其他日历的访问权限
- 将凭证存储在本地内存文件中

## 相关工具

用户可安装以下工具（通过 `clawhub install <slug>`）：

- `daily-planner`：用于每日任务规划、排序和合理分配任务。
- `schedule`：适用于无需全面调整日历安排的常规日程管理工作。
- `assistant`：负责任务管理、消息处理和整体规划。
- `productivity`：帮助用户管理任务优先级、提高工作效率。
- `remember`：根据用户的长期需求和重复性任务模式进行持续规划。

## 反馈建议

- 如果觉得本工具有用，请给它打星评价：`clawhub star calendar-planner`
- 为了获取最新更新，请订阅：`clawhub sync`