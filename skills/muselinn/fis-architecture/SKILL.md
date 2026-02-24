---
name: fis-architecture
description: >
  **多代理工作流框架：基于JSON工单和文件协作的解决方案**  
  适用于通过JSON工单管理多代理工作流、利用文件协作跟踪任务、生成代理徽章，或实现FIS（联邦情报系统）工作流模式的应用场景。
---
# FIS 架构

这是一个基于 JSON 工单和文件协作的多代理工作流框架。

## 概述

FIS（联邦情报系统）通过以下方式管理多代理工作流：
- 使用 **JSON 工单** 进行任务跟踪
- 采用 **基于文件的** 协作方式（无需数据库）
- 使用 **Markdown** 存储知识
- 提供 **可选的** Python 插件用于生成徽章

## 快速入门

### 1. 创建工单

```bash
python3 lib/fis_lifecycle.py create \
  --agent "worker" \
  --task "Your task description" \
  --role "worker"
```

或者通过 Python：
```python
from lib.fis_lifecycle import FISLifecycle

fis = FISLifecycle()
fis.create_ticket(
    agent="worker",
    task="Your task description",
    role="worker"
)
```

### 2. 完成任务

```bash
python3 lib/fis_lifecycle.py complete \
  --ticket-id "TASK_XXX"
```

### 3. 列出活跃工单

```bash
python3 lib/fis_lifecycle.py list
```

### 4. 生成徽章（可选）

**快速生成方式：**
```bash
cd lib
python3 badge_generator.py
```

**单个徽章：**
```python
from lib.badge_generator import generate_badge_with_task

path = generate_badge_with_task(
    agent_name="Worker-001",
    role="WORKER",
    task_desc="Your task description",
    task_requirements=["Step 1", "Step 2", "Step 3"]
)
```

**多个徽章：**
```python
from lib.badge_generator import generate_multi_badge

cards = [
    {
        'agent_name': 'Worker-001',
        'role': 'worker',
        'task_desc': 'Implement feature A',
        'task_requirements': ['Design', 'Code', 'Test']
    },
    {
        'agent_name': 'Reviewer-001',
        'role': 'reviewer',
        'task_desc': 'Review implementation',
        'task_requirements': ['Check code', 'Verify tests']
    }
]
path = generate_multi_badge(cards, "team_badges.png")
```

**自定义徽章（具有完全控制权）：**
```python
from lib.badge_generator import BadgeGenerator
from datetime import datetime

generator = BadgeGenerator()

agent_data = {
    'name': 'Custom-Agent',
    'id': f'AGENT-{datetime.now().year}-001',
    'role': 'WORKER',
    'task_id': '#TASK-001',
    'soul': '"Execute with precision"',
    'responsibilities': [
        "Complete assigned tasks",
        "Report progress promptly"
    ],
    'output_formats': 'MARKDOWN | JSON',
    'task_requirements': [
        "1. Analyze requirements",
        "2. Implement solution"
    ],
    'status': 'ACTIVE',
    # 'qr_url': 'https://your-link.com'  # Optional: adds QR code
}

path = generator.create_badge(agent_data)
```

## 文件结构

技能文件：
```
lib/
├── fis_lifecycle.py      # Ticket lifecycle management
├── badge_generator.py    # Badge image generation
└── fis_config.py         # Configuration

examples/
└── demo.py               # Runnable examples showing badge generation
```

工作流中心（在运行时创建）：
```
~/.openclaw/fis-hub/           # Your workflow hub
├── tickets/
│   ├── active/               # Active tasks
│   └── completed/            # Archived tasks
└── knowledge/                # Shared knowledge
```

## 工单格式

```json
{
  "ticket_id": "TASK_001",
  "agent_id": "worker-001",
  "role": "worker",
  "task": "Task description",
  "status": "active",
  "created_at": "2026-02-25T10:00:00",
  "updated_at": "2026-02-25T10:00:00"
}
```

## 工作流程

1. 使用任务描述创建工单
2. 由代理执行任务
3. 由审核员（可选）进行审核
4. 完成任务并归档工单

## 徽章输出

徽章保存路径：`~/.openclaw/output/badges/`

徽章特性：
- 显示安全级别和工作区 ID
- 可选 QR 码（提供 `qr_url` 时）
- 支持中文字体

## 依赖项

（徽章生成所需的可选依赖项：）
- `Pillow>=9.0.0`
- `qrcode>=7.0`

## 许可证

MIT