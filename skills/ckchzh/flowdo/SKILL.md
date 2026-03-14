---
name: FlowDo
description: "这是一个任务和工作流程管理工具，支持看板式状态跟踪功能。用户可以添加任务、将任务在不同的工作流程状态（待办、进行中、已完成、受阻）之间切换、设置优先级、按状态筛选任务，并查看任务的完成百分比。这是一款简单的项目管理工具，可在终端中使用。"
version: "1.0.0"
author: "BytesAgain"
tags: ["task","todo","workflow","productivity","project","kanban","gtd","management"]
categories: ["Productivity", "Project Management"]
---
# FlowDo

FlowDo 为您的终端带来了类似看板（kanban）的任务管理功能。您可以跟踪任务的状态变化、设置任务的优先级，并监控任务的完成进度。

## 为什么选择 FlowDo？

- **任务状态管理**：支持任务从“待办”（todo）状态变为“进行中”（doing），最终变为“已完成”（done）。
- **优先级系统**：能够将紧急任务标记为高优先级。
- **可视化状态显示**：图标可一目了然地显示任务的状态。
- **完成进度追踪**：可以查看任务的完成百分比。
- **筛选视图**：可以仅显示处于特定状态的任务。
- **无需配置**：无需任何额外设置即可立即使用，数据存储在本地。

## 命令

- `add <text>` — 添加新任务
- `list [status]` — 按状态筛选任务列表（待办/进行中/已完成/全部）
- `done <id>` — 将任务标记为已完成
- `doing <id>` — 将任务标记为进行中
- `priority <id> <level>` — 设置任务的优先级（高/普通/低）
- `stats` — 查看任务完成统计信息
- `info` — 查看软件版本信息
- `help` — 显示可用命令列表

## 使用示例

```bash
flowdo add Write project proposal
flowdo add Review pull requests
flowdo doing 1710000001
flowdo priority 1710000001 high
flowdo done 1710000001
flowdo list todo
flowdo stats
```

## 状态图标说明

- ⬜ 待办（Todo）—— 任务尚未开始
- 🔄 进行中（Doing）—— 任务正在处理中
- ✅ 已完成（Done）—— 任务已经完成
- 🚫 被阻止（Blocked）—— 任务因依赖关系而被阻塞
- ❗ 高优先级指示器（High priority indicator）

---
💬 意见反馈与功能请求：https://bytesagain.com/feedback
由 BytesAgain 开发 | bytesagain.com