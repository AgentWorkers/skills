# ClickUp 操作大师技能 - 设计规范

## 核心理念

**仅执行确定性操作** — 每个命令要么成功并给出明确确认，要么失败并显示具体错误。不存在模棱两可的状态，也没有无声的失败。每一步都进行完整验证。

## 内置知识库

该技能内部包含了 **完整的 ClickUp API 文档**：
- 超过 50 个 API 端点
- 请求/响应模式
- 请求速率限制（每分钟 100 次请求）
- 错误代码及处理方式
- Webhook 模式
- 官方文档中的最佳实践

**MCP 上下文** — 仅作为边缘情况的备用方案提供（例如：复杂的工作区模板、超出速率限制的大量操作、跨工作区的任务转移）。

## 操作能力

### 1. 自然语言解析 → 结构化命令
```
Input: "Create a project for Acme Corp with onboarding, web design, and monthly retainer phases"
Parse: 
  - workspace: Delivery
  - client: Acme Corp
  - structure: folder → 3 lists (onboarding, web-design, retainer)
  - assignees: find by email/name
  - due dates: infer from phases
  - custom fields: budget, priority, status
  
Execute: deterministic sequence with rollback on failure
Verify: each list created, each task present, assignments correct
Confirm: "Project Acme Corp created with 3 phases, 12 tasks, assigned to George & Matthew, due 2026-03-15"
```

### 2. 进度诊断与时间线估算
```
Input: "What's blocking the Scent of a Milien project?"
Flow: 
  - Scan all tasks in folder
  - Identify status: blocked, overdue, no-assignee
  - Check dependencies: waiting on other tasks
  - Estimate completion: based on task complexity, assignee velocity
  - Report: "3 tasks blocked (waiting on George's video edits). ETA: +5 days. Suggest: reassign or parallelize"
```

### 3. 任务分配协调
```
Input: "Get Sharyar and Matthew on the Kortex onboarding task"
Flow:
  - Find Sharyar (check existing members or invite)
  - Find Matthew (check existing or invite)
  - Locate Kortex onboarding task
  - Add both as assignees
  - Comment: "@Sharyar @Matthew — Kortex onboarding ready for your review. See attached Loom."
  - Set due date: +3 days
  - Set priority: high
  - Set status: "in progress"
  - Confirm: "Sharyar and Matthew assigned to Kortex onboarding, due 2026-02-21"
```

### 4. 从模板创建工作区
```
Input: "Set up a new client workspace for Luxury Homes using our real estate template"
Parse:
  - Template: detect "real estate" → use predefined structure
  - Spaces: Delivery + Operations
  - Folders: Client Name → Market Research, Design, Build, Launch
  - Lists: Per-phase task lists with default tasks
  - Custom Fields: Budget, Timeline, Priority, Platform
  - Assignees: Based on team roles from People graph
  - Automations: Status change triggers, due date reminders
  
Execute: Create full hierarchy, validate each step
Confirm: "Luxury Homes workspace created: 2 spaces, 4 folders, 12 lists, 48 tasks, 5 team members assigned, automations active"
```

### 5. 智能任务生成
```
Input: "Break down the Clarify website project into technical tasks"
Generate: 
- [ ] Setup Git repository and CI/CD pipeline
- [ ] Install dependencies (npm, build tools)
- [ ] Create page components: Home, About, Contact, Services
- [ ] Implement contact form with validation
- [ ] SEO setup: sitemap.xml, robots.txt, LLMs.txt
- [ ] Lighthouse audit and performance optimization
- [ ] Deploy to Vercel/production
- [ ] Set up analytics tracking

Each task gets: estimated hours, assignee (based on skills), dependencies (creates task links), custom fields (priority: high, tags: website, client: Clarify)
```

## 错误处理与确定性

### 每个操作都遵循以下模式：
```python
def create_task(params):
    # 1. Validate inputs
    assert params.name, "Task name required"
    assert len(params.name) <= 200, "Name too long"
    
    # 2. Check preconditions
    if params.list_id:
        assert list_exists(params.list_id), f"List {params.list_id} not found"
    
    # 3. Execute API call
    try:
        result = api_post("/task", params.dict())
    except RateLimitError as e:
        # Retry with exponential backoff
        wait(e.retry_after + 1)
        result = api_post("/task", params.dict())
    except ValidationError as e:
        # Return explicit error
        raise ClickUpError(f"Invalid data: {e.details}")
    
    # 4. Verify result
    assert result.id, "No task ID returned"
    assert result.name == params.name, "Name mismatch"
    
    # 5. Confirm success
    return {
        "id": result.id,
        "name": result.name,
        "url": result.url,
        "created": True,
        "validated": True
    }
```

### 常见错误及其处理方式：
- `rate_limit` → 重试 + 退避策略
- `validation_failed` → 返回字段级别的错误信息
- `not_found` → 提供修正建议
- `permission_denied` → 建议获取工作区访问权限
- `conflict` → 提供解决方案（重命名、合并等）

## 诊断命令
```bash
# What's the status of project X?
clickup-op diagnose --project "Clarify" --depth full

# Who's blocking project Y?
clickup-op blockers --project "Scent Of A Milien" --format report

# Estimate completion date
clickup-op estimate --project "Mel website" --include-dependencies

# Suggest resource allocation
clickup-op allocate --team "George,Matthew,Sharyar" --capacity 40h/week
```

## 测试策略

**在宣布技能可用之前：**
1. 创建 10 个工作区
2. 生成 100 个任务，包含各种变量（分配者、截止日期、优先级、标签、依赖关系、注释、检查清单、时间记录）
3. 执行 50 次批量操作（更新 10 个任务、移动 5 个任务、删除 3 个任务、恢复 2 个任务）
4. 运行所有诊断命令，验证输出结果的准确性
5. 触发 20 种错误情况，验证错误信息的显示方式
6. 测试在达到速率限制时的备用方案（使用 MCP）

**成功标准：**
- 100% 的操作成功率，或出现明确的可解决错误
- 不存在模棱两可的状态（任务存在但未确认）
- 所有诊断结果都能提供合理的估算
- 自然语言解析能够处理 95% 的用户输入

## 与 Brain 系统的集成

**每次成功操作都会存储以下信息：**
- **Mem0：** “为 Acme Corp 项目创建了 12 个任务”
- **Neo4j：** `(Task) -[CREATED_IN]→ (Project "Acme Corp")`, `(George) -[ASSIGNED_TO]→ (Task)`
- **SQLite：** `decisions` 表：决策类型、参数、结果、时间戳

**支持以下查询：**
- “我上周创建了哪些项目？” → 通过 Mem0 进行搜索
- “谁的工作负担最重？” → 通过 Neo4j 查询分配者的任务数量
- “我的完成率是多少？” → 通过 SQLite 进行统计

## 文件结构
```
skills/clickup-operational/
├── SKILL.md                      # This spec + user docs
├── scripts/
│   ├── clickup_op.py            # Main CLI (800+ lines)
│   ├── diagnostic.py            # Progress/suggestion engine
│   ├── natural_parser.py        # NL → structured commands
│   └── brain_sync.py           # Auto-store to brain system
└── tests/
    ├── test_workspace_setup.py
    ├── test_task_lifecycle.py
    ├── test_diagnostics.py
    └── test_natural_language.py
```

## 构建此技能（需要 Model Council 的参与）

**对 4 个模型的查询要求：**
“设计一个尽可能强大的 ClickUp 操作技能。该技能必须能够处理工作区的创建、文件夹/列表结构、任务的创建/更新/删除、任务分配、注释、时间跟踪和诊断功能。操作必须具有确定性（无模棱两可的状态），对每个 API 响应进行验证，明确处理所有错误，并包含全面的测试。需要提供完整的 CLI 命令列表、请求/响应模式和错误处理方式。”

**合成响应** → 从每个模型中提取最佳实践 → 构建统一的实现方案。

**预计构建时间：** 在 Model Council 的协助下需要 4-6 小时
**代码行数：** 约 2,500 行（全面实现，非最小化代码）
**测试覆盖率：** 超过 95% 的 API 端点和错误路径

## 执行顺序**

1. **Model Council 设计会议**（在信用点数重置时进行）
2. **构建核心 CLI**（工作区、文件夹、列表、任务操作功能）
3. **添加诊断引擎**（进度显示、障碍识别、估算功能）
4. **构建自然语言解析器**（将用户意图转换为结构化数据）
5. **集成 Brain 系统**（自动存储操作记录）
6. **进行全面测试**（100 个任务、50 次批量操作、所有错误路径）
7. **操作验证**（创建真实项目，诊断实际存在的障碍）

此技能将成为您在 ClickUp 中的 **操作方面的副首席执行官**。

## 状态
- **设计规范已保存：** /home/node/.openclaw/workspace/skills/clickup-operational/spec.md
- **尚未实现** — 正在等待 Model Council 的信用点数重置以开始构建
- **优先级：** 关键 — 这将解锁完整的业务操作能力

## 相关决策
- 必须首先实现与 Brain 系统的集成（所有 ClickUp 操作都必须通过 Brain 系统处理）
- ClickUp MCP 作为备用方案，但此技能是主要操作路径
- 所有客户端项目存储在 Delivery 工作区中，代理操作存储在 AgxntSix-openclaw 工作区中
- 自然语言解析必须能够处理 95% 以上的业务请求，无需额外说明