---
name: todo
description: 基于优先级的任务和项目管理工具，具备上下文感知的功能。当用户提及任务、待办事项列表、项目、承诺事项、截止日期或优先级设置时，该工具可提供相应的支持。它能够从任何上下文中捕获任务信息，根据任务的紧急性和重要性进行排序；根据用户的当前状态（精力水平）来展示需要处理的工作内容；跟踪对他人所做的承诺；并支持每周的回顾机制。所有数据均存储在本地。
---
# 待办事项（Todo）

这是一个任务和项目管理系统，用于记录所有需要完成的事项，并专注于真正重要的事情。

## 关键的隐私与安全措施

### 数据存储（至关重要）
- **所有任务数据仅存储在本地**：`memory/todo/`
- **不连接任何外部任务应用程序**
- **不进行云同步**——完全采用本地存储
- **不共享任务或项目信息**
- 用户可以控制数据的保留和删除

### 数据结构
任务存储在您的本地工作区中：
- `memory/todo/tasks.json` – 所有任务及其优先级
- `memory/todo/projects.json` – 项目定义及后续行动
- `memory/todo/commitments.json` – 与他人之间的承诺或约定
- `memory/todo/contexts.json` – 上下文信息（如能量状态、位置、时间）
- `memory/todo/reviews.json` – 每周回顾记录

## 核心工作流程

### 添加任务
```
User: "Call the accountant before Thursday"
→ Use scripts/add_task.py --task "Call accountant" --deadline "2024-03-14" --context phone
→ Extract task, identify deadline, store for later
```

### 任务优先级排序
```
User: "What should I work on now?"
→ Use scripts/what_next.py --energy high --time 120 --location desk
→ Surface tasks matching current context and energy
```

### 跟踪承诺或约定
```
User: "I promised Sarah I'd send the report by Friday"
→ Use scripts/add_commitment.py --to "Sarah" --what "Send report" --deadline "2024-03-15"
→ Track commitment with deadline and reminder
```

### 每周回顾
```
User: "Run my weekly review"
→ Use scripts/weekly_review.py
→ Guide through closing completed, updating projects, capturing new items
```

### 日终处理
```
User: "Close out my day"
→ Use scripts/close_day.py
→ Review what was done, capture loose ends, set up tomorrow
```

## 模块参考
- **任务添加系统**：请参阅 [references/capture.md](references/capture.md)
- **优先级框架**：请参阅 [references/priority.md](references/priority.md)
- **上下文与能量管理**：请参阅 [references/context.md](references/context.md)
- **承诺与约定**：请参阅 [references/commitments.md](references/commitments.md)
- **每周回顾**：请参阅 [references/weekly-review.md](references/weekly-review.md)
- **项目与任务的区别**：请参阅 [references/projects.md](references/projects.md)

## 脚本参考
| 脚本 | 用途 |
|--------|---------|
| `add_task.py` | 添加新任务 |
| `what_next.py` | 根据当前上下文显示合适的任务 |
| `add_commitment.py` | 记录对某人的承诺或约定 |
| `weekly_review.py` | 运行每周回顾 |
| `close_day.py` | 日终处理脚本 |
| `complete_task.py` | 标记任务已完成 |
| `add_project.py` | 创建新项目 |
| `set_context.py` | 定义上下文参数 |