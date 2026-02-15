---
name: dex
description: 异步/多步骤工作的任务跟踪。使用 dex 工具来创建、跟踪和完成那些需要跨多个会话执行或需要协调的任务（例如：代码代理的调度、PR 审查、后台作业等）。任务以 JSON 格式存储在 `.dex/tasks/` 目录下。
---

# Dex 任务跟踪

用于跟踪异步工作：代码代理的调度、多步骤项目，以及任何需要跟进的任务。

## 命令
```bash
dex create -d "Description" --context "Background, goal, done-when"
dex list                    # Pending tasks
dex list --all              # Include completed
dex show <id>               # View task
dex show <id> --full        # Full context
dex complete <id> --result "What was done, decisions, follow-ups"
dex edit <id> --context "Updated context"
dex delete <id>
```

## 任务结构
- **描述**：任务的简要概述
- **背景**：任务的背景信息、需求及完成标准
- **结果**：已完成的工作、所做的决策以及后续需要处理的事项

## 示例
```bash
# Before dispatching agent
dex create -d "Add caching to API" --context "Workspace: feat1 (100.x.x.x)
Branch: feat/cache
Done when: PR merged, CI green"

# After work complete
dex complete abc123 --result "Merged PR #50. Redis caching with 5min TTL."
```

## 存储方式
`.dex/tasks/{id}.json` — 每个任务对应一个文件，便于使用 Git 进行版本控制。