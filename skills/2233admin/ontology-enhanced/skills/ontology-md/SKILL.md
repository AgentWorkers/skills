---
name: ontology
description: **结构化代理记忆与可组合技能的类型化知识图谱**  
该知识图谱用于存储和管理各种实体（如人员、项目、任务、事件、文档）的信息，并支持相关对象之间的关联操作。它还具备以下功能：  
- 强制执行约束规则；  
- 以图谱变换的形式规划多步骤操作；  
- 支持技能之间的状态共享；  
- 能够根据用户指令（如“记住某件事”、“我知道什么”、“将X与Y关联起来”等）触发相应的操作；  
- 提供实体的创建、读取、更新和删除（CRUD）功能；  
- 支持跨技能的数据访问。  

在需要处理以下场景时，该知识图谱尤为有用：  
- 创建或查询实体信息；  
- 建立实体之间的关联；  
- 确保数据遵循特定规则；  
- 设计复杂的操作流程；  
- 实现技能间的协同工作。
---

# 本体（Ontology）

一种类型化的词汇表与约束系统，用于将知识表示为可验证的图结构。

## 核心概念

所有事物都是一个**实体**，具有**类型**、**属性**以及与其他实体的**关系**。任何更改在提交之前都会根据类型约束进行验证。

```
Entity: { id, type, properties, relations, created, updated }
Relation: { from_id, relation_type, to_id, properties }
```

## 使用场景

| 触发条件 | 操作 |
|---------|--------|
| “记住……” | 创建/更新实体 |
| “我对X了解多少？” | 查询图结构 |
| “将X与Y关联起来” | 创建关系 |
| “显示项目Z的所有任务” | 图结构遍历 |
| “什么依赖于X？” | 依赖关系查询 |
| 规划多步骤工作 | 将工作流程建模为图结构转换 |
| 技能需要共享状态 | 读写本体对象 |

## 核心类型

```yaml
# Agents & People
Person: { name, email?, phone?, notes? }
Organization: { name, type?, members[] }

# Work
Project: { name, status, goals[], owner? }
Task: { title, status, due?, priority?, assignee?, blockers[] }
Goal: { description, target_date?, metrics[] }

# Time & Place
Event: { title, start, end?, location?, attendees[], recurrence? }
Location: { name, address?, coordinates? }

# Information
Document: { title, path?, url?, summary? }
Message: { content, sender, recipients[], thread? }
Thread: { subject, participants[], messages[] }
Note: { content, tags[], refs[] }

# Resources
Account: { service, username, credential_ref? }
Device: { name, type, identifiers[] }
Credential: { service, secret_ref }  # Never store secrets directly

# Meta
Action: { type, target, timestamp, outcome? }
Policy: { scope, rule, enforcement }
```

## 存储方式

默认存储路径：`memory/ontology/graph.jsonl`

**注：**对于复杂的图结构，建议迁移到SQLite数据库中存储。

### 只允许追加修改的规则

在处理现有的本体数据或模式时，应采用**追加/合并**修改的方式，而不是直接覆盖文件。这样可以保留历史记录，避免破坏之前的定义。

## 工作流程

### 创建实体

```bash
python3 scripts/ontology.py create --type Person --props '{"name":"Alice","email":"alice@example.com"}'
```

### 查询

```bash
python3 scripts/ontology.py query --type Task --where '{"status":"open"}'
python3 scripts/ontology.py get --id task_001
python3 scripts/ontology.py related --id proj_001 --rel has_task
```

### 关联实体

```bash
python3 scripts/ontology.py relate --from proj_001 --rel has_task --to task_001
```

### 验证

```bash
python3 scripts/ontology.py validate  # Check all constraints
```

## 约束条件

约束条件的定义位于文件 `memory/ontology/schema.yaml` 中：

```yaml
types:
  Task:
    required: [title, status]
    status_enum: [open, in_progress, blocked, done]
  
  Event:
    required: [title, start]
    validate: "end >= start if end exists"

  Credential:
    required: [service, secret_ref]
    forbidden_properties: [password, secret, token]  # Force indirection

relations:
  has_owner:
    from_types: [Project, Task]
    to_types: [Person]
    cardinality: many_to_one
  
  blocks:
    from_types: [Task]
    to_types: [Task]
    acyclic: true  # No circular dependencies
```

## 技能契约（Skill Contract）

使用本体的技能需要明确声明相关约束条件：

```yaml
# In SKILL.md frontmatter or header
ontology:
  reads: [Task, Project, Person]
  writes: [Task, Action]
  preconditions:
    - "Task.assignee must exist"
  postconditions:
    - "Created Task has status=open"
```

## 作为图结构转换进行规划

将多步骤计划建模为一系列图结构操作：

**注：**每个操作在执行前都会进行验证；如果违反约束条件，系统会回滚到之前的状态。

## 集成模式

### 与因果推理（Causal Inference）结合使用

将本体中的更改记录为因果事件：

```python
# When creating/updating entities, also log to causal action log
action = {
    "action": "create_entity",
    "domain": "ontology", 
    "context": {"type": "Task", "project": "proj_001"},
    "outcome": "created"
}
```

### 跨技能通信（Cross-Skill Communication）

```python
# Email skill creates commitment
commitment = ontology.create("Commitment", {
    "source_message": msg_id,
    "description": "Send report by Friday",
    "due": "2026-01-31"
})

# Task skill picks it up
tasks = ontology.query("Commitment", {"status": "pending"})
for c in tasks:
    ontology.create("Task", {
        "title": c.description,
        "due": c.due,
        "source": c.id
    })
```

## 快速入门

```bash
# Initialize ontology storage
mkdir -p memory/ontology
touch memory/ontology/graph.jsonl

# Create schema (optional but recommended)
python3 scripts/ontology.py schema-append --data '{
  "types": {
    "Task": { "required": ["title", "status"] },
    "Project": { "required": ["name"] },
    "Person": { "required": ["name"] }
  }
}'

# Start using
python3 scripts/ontology.py create --type Person --props '{"name":"Alice"}'
python3 scripts/ontology.py list --type Person
```

## 参考资料

- `references/schema.md` — 完整的类型定义和约束模式
- `references/queries.md` — 查询语言及遍历示例

## 指令范围

运行时指令操作本地文件（`memory/ontology/graph.jsonl` 和 `memory/ontology/schema.yaml`），并提供命令行接口（CLI）用于创建、查询、关联和验证操作。该技能会读取/写入工作区文件，并在使用时自动创建 `memory/ontology` 目录。验证内容包括属性检查、枚举类型检查、禁止的操作检查、标记为 `acyclic: true` 的关系的无环性检查，以及事件顺序（`end >= start`）的检查；其他更高级的约束条件可能仅存在于文档中，尚未在代码中实现。