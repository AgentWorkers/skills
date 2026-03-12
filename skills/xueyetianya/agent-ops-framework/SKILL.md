---
name: Agent Ops Framework
description: "这是一个面向生产环境的多智能体团队协调框架，用于定义智能体的角色、任务流程、质量检查机制以及监控仪表板。该框架的设计灵感来源于 Google Vertex AI、Microsoft AutoGen、CrewAI 和 Anthropic 等平台中的智能体架构。主要特性包括：基于角色的智能体注册系统、任务生命周期管理（待办→分配→进行中→审核→完成→部署）、支持上下文传递的结构化任务交接机制、部署前的质量检查流程、集中式状态存储（统一的数据源）、配额/预算管理功能、基于 Cron 任务的监控系统（附带警报功能）以及具备回滚能力。适用场景包括：(1) 管理项目中三个及以上的专用智能体；(2) 构建用于内容或代码处理的持续集成/持续交付（CI/CD）流程；(3) 跟踪多个智能体之间的任务进度；(4) 在部署前确保满足质量标准；(5) 监控智能体的性能及输出质量；(6) 管理不同账户的速率限制和配额。该框架涵盖了多智能体协调、团队管理、任务流程管理、质量保证、智能体协作、项目管理、工作流程自动化以及监控与警报等多个方面。"
---
# Agent Ops Framework

这是一个专为 OpenClaw 项目设计的、具备生产级多代理团队协调能力的框架。

## 为什么需要这个框架？

如果无序地运行多个代理，将会导致以下问题：
- ❌ 数据冲突（不同的列表显示不同的信息）
- ❌ 没有质量检查机制（有问题的技能会被发布）
- ❌ 缺乏责任追究机制（谁做了什么？）
- ❌ 无法了解当前状态（项目的进展如何？）

这个框架可以解决所有这些问题。

## 架构

```
┌─────────────────────────────────────────────┐
│  👑 ORCHESTRATOR (Main Session)             │
│  - Receives human requests                  │
│  - Makes decisions, delegates tasks          │
│  - Reviews reports, approves promotions      │
│  - NEVER does implementation work           │
├─────────────────────────────────────────────┤
│                                             │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐    │
│  │ 🔨 DEV  │→│ ✅ QA   │→│ 📦 DEPLOY│    │
│  │ Agent   │  │ Agent   │  │ Agent    │    │
│  └─────────┘  └─────────┘  └─────────┘    │
│       ↑                          │          │
│       │    ┌──────────┐          ↓          │
│       └────│ 📊 MON   │←────────┘          │
│            │ Agent    │                     │
│            └──────────┘                     │
│                                             │
│  ┌──────────────────────────────────┐       │
│  │  💾 STATE STORE (state.json)     │       │
│  │  Single source of truth          │       │
│  │  All agents read/write here      │       │
│  └──────────────────────────────────┘       │
└─────────────────────────────────────────────┘
```

## 快速入门

### 1. 初始化项目
```bash
bash scripts/ops.sh init --project "my-project" --state-dir /path/to/state
```

### 2. 注册代理
```bash
bash scripts/ops.sh agent add --name "dev" --role "developer" --desc "Builds features"
bash scripts/ops.sh agent add --name "qa" --role "reviewer" --desc "Tests and validates"
bash scripts/ops.sh agent add --name "deploy" --role "deployer" --desc "Ships to production"
bash scripts/ops.sh agent add --name "monitor" --role "observer" --desc "Tracks metrics"
```

### 3. 创建任务
```bash
bash scripts/ops.sh task add --id "SKILL-001" --title "Build chart-generator v2" \
  --assign "dev" --priority "high" --pipeline "dev→qa→deploy"
```

### 4. 通过流程线处理任务
```bash
bash scripts/ops.sh task move --id "SKILL-001" --to "in-progress"
bash scripts/ops.sh task move --id "SKILL-001" --to "review" --output "/path/to/deliverable"
bash scripts/ops.sh task move --id "SKILL-001" --to "done" --approved-by "qa"
bash scripts/ops.sh task move --id "SKILL-001" --to "deployed" --deploy-ref "v2.0.0"
```

### 5. 仪表盘
```bash
bash scripts/ops.sh dashboard
bash scripts/ops.sh dashboard --format html > report.html
```

### 6. 监控（通过 Cron 任务）
```bash
bash scripts/ops.sh monitor --check-stale --check-quota --alert-to /tmp/alerts.log
```

## 任务生命周期

```
BACKLOG → ASSIGNED → IN-PROGRESS → REVIEW → DONE → DEPLOYED
   │          │           │           │        │        │
   │          │           │           ↓        │        │
   │          │           │        REJECTED    │        │
   │          │           │           │        │        │
   │          │           ←───────────┘        │        │
   │          │                                │        │
   └──────────┴────────── CANCELLED ←──────────┘        │
                                                        │
                                              ROLLED-BACK←┘
```

## 质量检查机制

每个任务状态转换阶段都设有质量检查关卡：

| 任务状态转换 | 检查关卡 | 规则 |
|-------------|------------|---------|
| 进行中 → 审查       | 任务成果文件必须存在 |
| 审查 → 完成       | 需要质量保证团队（QA）的批准 |
| 完成 → 部署       | 部署脚本的退出代码必须为 0 |
| 部署 → 回滚       | 需要触发回滚机制（手动或基于警报） |

## 状态存储方案

所有任务状态信息都存储在一个 JSON 文件（`state.json`）中：

```json
{
  "project": "bytesagain-skills",
  "created": "2026-03-12T06:00:00Z",
  "agents": {
    "dev": {"role": "developer", "tasks_completed": 20, "last_active": "..."},
    "qa": {"role": "reviewer", "tasks_completed": 15, "last_active": "..."},
    "deploy": {"role": "deployer", "tasks_completed": 10, "last_active": "..."}
  },
  "tasks": {
    "SKILL-001": {
      "title": "Build chart-generator v2",
      "status": "deployed",
      "assigned": "dev",
      "pipeline": ["dev", "qa", "deploy"],
      "priority": "high",
      "history": [
        {"status": "assigned", "at": "...", "by": "orchestrator"},
        {"status": "in-progress", "at": "...", "by": "dev"},
        {"status": "review", "at": "...", "by": "dev", "output": "/skills/chart-generator/"},
        {"status": "done", "at": "...", "by": "qa", "notes": "All checks pass"},
        {"status": "deployed", "at": "...", "by": "deploy", "ref": "v2.0.0"}
      ]
    }
  },
  "quotas": {
    "publish_daily": {"limit": 100, "used": 45, "reset_at": "2026-03-13T00:00:00Z"},
    "api_hourly": {"limit": 60, "used": 12, "reset_at": "2026-03-12T07:00:00Z"}
  },
  "metrics": {
    "last_check": "2026-03-12T05:17:00Z",
    "total_downloads": 7591,
    "skills_online": 152,
    "alerts": []
  }
}
```

## 命令参考

| 命令            | 描述                        |
|-----------------|-----------------------------|
| `ops.sh init`      | 初始化项目状态                   |
| `ops.sh agent add/list/remove` | 管理代理注册表                   |
| `ops.sh task add/list/move/cancel` | 管理任务                         |
| `ops.sh pipeline define/show` | 定义/显示任务流程线                 |
| `ops.sh gate add/check`     | 管理质量检查关卡                   |
| `ops.sh quota set/check/reset` | 管理任务配额                     |
| `ops.sh dashboard`     | 显示项目状态（文本/HTML格式）                |
| `ops.sh monitor`      | 运行监控检查                     |
| `ops.sh report`      | 生成定期报告                     |
| `ops.sh history`      | 查看任务/代理的历史记录                 |
| `ops.sh rollback`      | 回滚已部署的代理或任务                 |

## 与 OpenClaw 的集成

该框架专为 OpenClaw 的子代理系统设计：

```
Orchestrator (main session)
├── sessions_spawn(task="dev work", label="dev-agent")
├── sessions_spawn(task="qa review", label="qa-agent")  
└── sessions_spawn(task="deploy", label="deploy-agent")
```

每个新创建的代理会从 `state.json` 文件中读取自己的任务，并在任务完成后更新状态。

## 最佳实践

1. **协调者仅负责决策与任务分配**，不直接执行具体操作。
2. **使用统一的状态文件**，避免使用分散的临时文件（如 `/tmp`）。
3. **记录所有任务状态转换过程**，确保有完整的审计追踪。
4. **严格执行质量检查机制**，不允许跳过任何审查环节。
5. **监控任务配额使用情况**，防止超出配额限制。
6. **在出现异常时触发警报**（例如任务超时、部署失败或配额耗尽）。
7. **定期进行回顾与优化**，根据数据反馈调整工作流程。

---
技术支持：BytesAgain | bytesagain.com | hello@bytesagain.com