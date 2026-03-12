---
name: Productivity
slug: productivity
version: 1.0.4
homepage: https://clawic.com/skills/productivity
description: "通过能源管理、时间规划、目标设定、项目管理、任务分配、习惯培养、工作审查、优先级排序以及针对特定情境的生产力系统来规划、集中精力并完成工作。适用于以下情况：  
1. 当用户需要在生产力、专注力、时间管理、计划制定、优先级设定、项目管理、任务处理或习惯培养方面获得帮助时；  
2. 当用户希望使用可重复使用的结构或工作空间来组织工作时；  
3. 当正在进行的工作需要通过专门的生产力框架来管理时。"
changelog: Expanded the system with clearer routing, setup, and folders for goals, tasks, habits, planning, and reviews
metadata: {"clawdbot":{"emoji":"⚡","requires":{"bins":[]},"os":["linux","darwin","win32"],"configPaths":["~/productivity/"]}}
---
## 使用场景

当用户需要一个真正能提升工作效率的系统，而不仅仅是短暂的动力激励时，就应该使用这项技能。该系统应涵盖目标管理、项目规划、任务分配、习惯培养、计划制定、任务优先级排序以及针对不同情境的调整措施，形成一个连贯的工作模式。

## 架构

工作效率相关的所有内容都存储在 `~/productivity/` 目录下。如果该目录还不存在，请先运行 `setup.md` 脚本进行初始化。

```
~/productivity/
├── memory.md                 # Work style, constraints, energy, preferences
├── inbox/
│   ├── capture.md            # Quick capture before sorting
│   └── triage.md             # Triage rules and current intake
├── dashboard.md              # High-level direction and current focus
├── goals/
│   ├── active.md             # Outcome goals and milestones
│   └── someday.md            # Goals not committed yet
├── projects/
│   ├── active.md             # In-flight projects
│   └── waiting.md            # Blocked or delegated projects
├── tasks/
│   ├── next-actions.md       # Concrete next steps
│   ├── this-week.md          # This week's commitments
│   ├── waiting.md            # Waiting-for items
│   └── done.md               # Completed items worth keeping
├── habits/
│   ├── active.md             # Current habits and streak intent
│   └── friction.md           # Things that break consistency
├── planning/
│   ├── daily.md              # Daily focus and must-win
│   ├── weekly.md             # Weekly plan and protected time
│   └── focus-blocks.md       # Deep work and recovery blocks
├── reviews/
│   ├── weekly.md             # Weekly reset
│   └── monthly.md            # Monthly reflection and adjustments
├── commitments/
│   ├── promises.md           # Commitments made to self or others
│   └── delegated.md          # Handed-off work to track
├── focus/
│   ├── sessions.md           # Deep work sessions and patterns
│   └── distractions.md       # Repeating focus breakers
├── routines/
│   ├── morning.md            # Startup routine and first-hour defaults
│   └── shutdown.md           # End-of-day reset and carry-over logic
└── someday/
    └── ideas.md              # Parked ideas and optional opportunities
```

这个系统应被视为用户的“生产力操作系统”：一个集成了方向设定、任务承诺、执行流程、习惯培养以及定期回顾功能的可靠平台。

## 快速参考

| 主题 | 对应文件 |
|-------|------|
| 初始化与任务分配 | `setup.md` |
| 记忆管理 | `memory-template.md` |
| 生产力系统模板 | `system-template.md` |
| 跨情境框架 | `frameworks.md` |
| 常见错误与陷阱 | `traps.md` |
| 学生情境 | `situations/student.md` |
| 高管情境 | `situations/executive.md` |
| 自由职业者情境 | `situations/freelancer.md` |
| 家长情境 | `situations/parent.md` |
| 创意工作者情境 | `situations/creative.md` |
| 疲劳状况 | `situations/burnout.md` |
| 创业者情境 | `situations/entrepreneur.md` |
| 多动症（ADHD）情境 | `situations/adhd.md` |
| 远程工作情境 | `situations/remote.md` |
| 管理者情境 | `situations/manager.md` |
| 习惯养成 | `situations/habits.md` |
| 内疚感与情绪恢复 | `situations/guilt.md` |

## 该技能的功能

| 功能层 | 作用 | 默认存储位置 |
|-------|---------|------------------|
| 信息收集 | 快速记录各种信息 | `~/productivity/inbox/` |
| 方向设定 | 明确目标与行动计划 | `~/productivity/dashboard.md` + `goals/` |
| 任务执行 | 下一步行动与任务承诺 | `~/productivity/tasks/` |
| 项目管理 | 管理正在进行和待处理的项目 | `~/productivity/projects/` |
| 习惯培养 | 培养重复性行为 | `~/productivity/habits/` |
| 计划制定 | 日常/每周/专注力规划 | `~/productivity/planning/` |
| 反思与调整 | 定期回顾与目标重置 | `~/productivity/reviews/` |
| 任务承诺 | 记录承诺与后续行动 | `~/productivity/commitments/` |
| 专注力管理 | 保护专注时间并记录干扰因素 | `~/productivity/focus/` |
| 习惯养成 | 建立日常作息习惯 | `~/productivity/routines/` |
| 暂存区 | 未确定的想法 | `~/productivity/someday/` |
| 个性化设置 | 根据个人情况调整系统 | `~/productivity/memory.md` |

## 常见问题与解决方案

| 用户问题 | 解决方案 |
|-----------|--------|
| “如何设置我的生产力系统？” | 创建 `~/productivity/` 目录结构并解释各文件夹的用途 |
| “我应该关注什么？” | 查看仪表盘、任务列表和任务承诺，确定优先事项 |
| “帮我规划一周的工作？” | 结合目标、项目、任务承诺和精力状况制定周计划 |
| “我感到压力太大” | 对任务进行优先级排序，缩减范围，重新安排行动步骤 |
| “如何将目标转化为具体计划？” | 将目标分解为项目，再分解为可执行的步骤 |
| “需要每周进行一次回顾” | 更新已完成的任务、阻碍因素以及下周的重点 |
| “如何帮助我养成好习惯？” | 使用 `habits/` 文件记录需要保留或改进的习惯 |
| “如何调整我的日常作息？” | 通过 `routines/` 和 `planning/` 文件简化工作流程 |
| “我想记住这个偏好设置” | 在用户确认后将其保存到 `~/productivity/memory.md` |

## 核心规则

### 1. 构建一个统一的系统，而非多个独立的系统
- 优先选择一套可靠的生产力框架，而非分散的笔记、随意的任务列表或重复的规划方案。
- 将目标、项目、任务、习惯、作息习惯、计划和回顾内容归类到相应的文件夹中，避免重复创建新的系统。
- 如果用户已有成熟的系统，应对其进行优化而非替换。

### 2. 从实际问题入手
- 先诊断问题的根源（是优先级混乱、任务过多、下一步行动不明确，还是其他原因）。
- 采取最有效的干预措施。
- 在用户真正需要明确下一步行动时，再考虑进行全面系统调整。

### 3. 明确区分目标、项目和任务
- 目标描述最终成果。
- 项目包含实现目标所需的具体工作内容。
- 任务是实现目标的直接行动步骤。
- 习惯是通过长期实践形成的行为模式。
- 不要让目标仅停留在模糊的愿望阶段，而缺乏具体的项目和行动计划。

### 4. 根据实际情况调整系统
- 当用户的实际情况比通用建议更重要时，应灵活调整系统设置。
- 考虑精力限制、家庭责任、截止日期、会议安排、疲劳状况（如 ADHD）等因素来制定计划。
- 可持续的系统比理想化的系统更实用，后者可能很快就会失效。

### 5. 定期回顾比频繁重新规划更重要
- 定期回顾有助于重建用户的信任感。
- 清理已完成的任务，重新命名模糊的条目，将任务与实际优先级对齐。
- 如果用户每天都在重复规划却毫无进展，应简化流程并重新评估。

### 6. 仅保存用户明确同意的设置
- 仅在用户明确要求或同意的情况下，才保存与工作方式相关的信息。
- 在写入 `~/productivity/memory.md` 之前，请先获得用户的确认。
- 不要通过用户的沉默、行为模式或一次性评论来推断其长期偏好。

## 常见误区

- 当问题本质上是结构性的时，却给予激励性建议。
- 将所有任务视为同等重要。
- 将目标、项目和任务混放在同一个列表中。
- 建立一个用户难以长期维护的完美系统。
- 推荐与用户实际情况不符的作息习惯。
- 因为删除某些设置会让人感到不适，而保留过时的设置。

## 使用范围

- 该技能仅用于构建或优化用户的工作效率系统。
- 提供生产力相关的建议和规划框架。
- 仅在使用者明确同意的情况下，才会读取相关参考文件以提供针对性指导。
- 未经用户明确授权，不会访问日历、电子邮件、联系人信息或外部服务。

## 外部接口

该技能不进行任何外部网络请求。

| 接口 | 发送的数据 | 用途 |
|----------|-----------|---------|
| 无 | 无 | 不发送任何数据 |

所有数据均存储在本地文件系统中：

- `~/productivity/memory.md`：保存用户确认的偏好设置、限制条件和工作方式相关内容。
- `~/productivity/inbox/`：存储临时记录和任务优先级排序。
- `~/productivity/dashboard.md`：显示总体工作方向和当前关注点。
- `~/productivity/goals/`：存储活跃中的目标和待处理的目标。
- `~/productivity/projects/`：存储正在进行和待处理的项目。
- `~/productivity/tasks/`：存储下一步行动、每周任务、待办事项和已完成的任务。
- `~/productivity/habits/`：存储正在培养的习惯和遇到的障碍。
- `~/productivity/planning/`：存储每日/每周计划和专注时间安排。
- `~/productivity/reviews/`：存储每周和每月的回顾记录。
- `~/productivity/commitments/`：存储任务承诺和后续执行情况。
- `~/productivity/focus/`：记录专注时间与干扰因素。
- `~/productivity/routines/`：存储日常作息习惯。
- `~/productivity/someday/`：存储暂存的想法。

**注意：** 只有在用户确认后才创建或更新这些文件。

## 迁移指南

如果要从旧版本升级，请先参考 `migration.md` 文件，再对 `~/productivity/` 目录下的文件进行结构调整。
在确认新系统适用之前，请保留旧版本文件。

## 安全性与隐私

- **数据传输**：该技能不会发送任何数据到外部。
- **本地数据存储**：仅存储用户明确同意保存在 `~/productivity/` 目录中的文件（包括工作偏好、限制条件、优先级设置和计划内容）。

**该技能不会**：
- 访问互联网或第三方服务。
- 自动读取日历、电子邮件、联系人信息或系统数据。
- 自动运行脚本或命令。
- 在后台监控用户行为。
- 仅根据用户行为推断其长期偏好设置。

## 信任说明

该技能仅提供使用指南，用于帮助用户规划生产力、设定优先级和进行定期回顾。只有在您同意将个人工作笔记以纯文本形式保存在 `~/productivity/` 目录下时，才建议安装该工具。

## 相关技能

- 如果用户同意，可同时安装以下扩展功能：
  - `self-improving`：提升任务执行效率并总结可复用的经验。
  - `goals`：帮助用户更深入地设定目标并设计里程碑。
  - `calendar-planner`：提供基于日历的规划和日程管理功能。
  - `notes`：帮助用户结构化地记录工作内容和思考过程。

## 用户反馈

- 如果觉得该技能有用，请点赞：`clawhub star productivity`。
- 保持更新：`clawhub sync`。