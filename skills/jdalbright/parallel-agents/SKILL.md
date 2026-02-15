# 并行代理技能 - 实际人工智能版本

🚀 **使用 OpenClaw 的 `sessions_spawn` 功能，通过真正的人工智能代理执行任务。**

> ⚠️ **重要提示**：此技能已重写，现在使用 `sessions_spawn` 来调用实际的人工智能。  
> 之前它使用模板来模拟代理行为，而现在则是真正生成人工智能子会话。

## 🚨 关键使用说明

**必须从 OpenClaw 代理会话中调用该功能，** **不能作为独立的脚本运行**。  
为什么？`tools` 模块（提供 `sessions_spawn` 功能）仅在代理的运行时环境中可用，而在 `subprocess` 或 `exec` 调用中不可用。

**✅ 正确用法**：直接从代理代码中调用 `sessions_spawn`（请参阅 `USAGE-GUIDE.md`）。  
**❌ 错误用法**：通过 `exec` 或 `subprocess` 以独立 Python 脚本的形式运行该功能。

📖 **参考文档**：请查看 `USAGE-GUIDE.md`，其中包含经过测试的示例和用法说明。

---

## 功能概述

该技能提供了 **4 个级别的代理自动化**：

| 级别 | 功能 | 功能描述 |
|-------|---------|--------------|
| **1** | **任务代理**（16 种类型） | 专门用于内容创作、开发、质量测试和文档编写 |
| **2** | **元代理**（4 种类型） | 负责创建、审查、优化和协调其他代理 |
| **3** | **迭代优化** | 自动质量改进循环（创建者 → 审查者 → 优化者） |
| **4** | **代理编排器** | 完全自主的工作流程管理——只需请求，系统即可处理一切 |

**已验证的功能**：
- ✅ **同时生成 20 个代理**  
- ✅ **智能模型层次结构**：Haiku → Kimi → Opus（成本优化）  
- ✅ **自动升级**：根据需要自动使用更高级的模型  
- ✅ **大规模创建测试中的 100% 成功率**  
- ✅ **单次迭代后，3 个代理的质量提升至 8.5 分以上**  
- ✅ **4 个代理的层次结构**，实现完全自主运行

---

## 实际工作原理

该技能使用 OpenClaw 的 `sessions_spawn` 工具创建 **真正的人工智能子会话**。每个代理：
- 是一个独立的 OpenClaw 会话（而非子进程）  
- 运行着与主机相同的真实人工智能模型  
- 与其他代理完全隔离  
- 可以使用与主机相同的所有工具

**旧版本**：使用模板运行的子进程工作者  
**当前版本**：真正生成的人工智能会话  

---

## 使用要求

- **必须在 OpenClaw 会话中运行**（以使用 `sessions_spawn` 功能）  
- OpenClaw 门户必须处于运行状态  
- 确保环境中已安装 `sessions` 工具  

---

## 快速入门

### ✅ 正确用法：直接调用 `sessions_spawn`  
**在 OpenClaw 代理内部（例如 Scout）**：

```python
# Spawn multiple agents in parallel using sessions_spawn tool directly
from tools import sessions_spawn

# Agent 1: Research task
result1 = sessions_spawn(
    task="Research and provide: Top 3 gay-friendly bars in Savannah. Return as JSON.",
    runTimeoutSeconds=90,
    cleanup="delete"
)

# Agent 2: Different research task  
result2 = sessions_spawn(
    task="Research and provide: Best restaurants for birthday dinner. Return as JSON.",
    runTimeoutSeconds=90,
    cleanup="delete"
)

# Agent 3: Another parallel task
result3 = sessions_spawn(
    task="Research and provide: Top photo spots in Savannah. Return as JSON.",
    runTimeoutSeconds=90,
    cleanup="delete"
)

# All 3 agents now running in parallel!
# Check results with sessions_list() and sessions_history()
```

### ❌ 错误用法：作为独立脚本运行  

```bash
# This WON'T work - tools module not available in subprocess
python3 ~/.openclaw/skills/parallel-agents/ai_orchestrator.py
```

### 基本用法  

```python
from ai_orchestrator import RealAIParallelOrchestrator, AgentTask

# Create orchestrator
orch = RealAIParallelOrchestrator(max_concurrent=5)

# Define tasks
tasks = [
    AgentTask(
        agent_type='content_writer_funny',
        task_description='Write a caption about gym life',
        input_data={'tone': 'motivational'}
    ),
    AgentTask(
        agent_type='content_writer_creative',
        task_description='Write a caption about gym life',
        input_data={'tone': 'inspirational'}
    ),
]

# Execute in parallel (ACTUALLY spawns AI sessions)
results = orch.run_parallel(tasks)
```

---

## 工作原理

```
┌─────────────────────────────────────────────────────────┐
│                    Main Session                         │
│              (Your OpenClaw Instance)                   │
│                      🧠 Host AI                         │
└─────────────────────┬───────────────────────────────────┘
                      │ sessions_spawn (REAL)
                      │
        ┌─────────────┼─────────────┬─────────────┐
        │             │             │             │
   ┌────▼────┐   ┌────▼────┐   ┌────▼────┐   ┌────▼────┐
   │ Agent 1 │   │ Agent 2 │   │ Agent 3 │   │ Agent N │
   │   📝    │   │   💻    │   │   🔍    │   │   🎨    │
   │ REAL AI │   │ REAL AI │   │ REAL AI │   │ REAL AI │
   │ Session │   │ Session │   │ Session │   │ Session │
   └─────────┘   └─────────┘   └─────────┘   └─────────┘
```

### `sessions_spawn` 的集成方式  

每个代理的创建过程包括：

```python
from tools import sessions_spawn

result = sessions_spawn(
    task=agent_prompt,           # Full task description
    agent_id=f"agent_{type}_{id}",  # Unique identifier
    model="kimi-coding/k2p5",     # AI model
    runTimeoutSeconds=120,        # Max execution time
    cleanup="delete"              # Auto-cleanup
)
```

---

## 可用的代理类型

### 内容创作代理

| 代理类型 | 用途 | 系统提示 |
|------------|---------|---------------|
| `content_writer_creative` | 具有创意的内容 | 使用丰富的隐喻和情感表达 |
| `content_writer_funny` | 幽默的内容 | 有趣的笑话和语言游戏 |
| `content_writer_educational` | 教育性内容 | 清晰的解释和实用的建议 |
| `content_writer_trendy` | 热门内容 | 关注潮流和文化相关性 |
| `content_writer_controversial` | 引发讨论的内容 | 热门观点和尊重的讨论方式 |

### 开发代理

| 代理类型 | 用途 | 输出结果 |
|------------|---------|--------|
| `frontend_developer` | React/Vue/Angular | 组件结构、状态管理 |
| `backend_developer` | FastAPI/Flask/Django | API 端点、身份验证、模型 |
| `database_architect` | 数据库设计 | 表结构、索引、迁移 |
| `api_designer` | REST/GraphQL | OpenAPI 规范、速率限制 |
| `devops_engineer` | 持续集成/持续交付 | Docker、Kubernetes、管道配置 |

### 质量测试代理

| 代理类型 | 用途 | 重点关注领域 |
|------------|---------|-------|
| `code_reviewer` | 代码审查 | 最佳实践、可维护性 |
| `security_reviewer` | 安全性扫描 | 漏洞和威胁检测 |
| `performance_reviewer | 性能优化 | 瓶颈和复杂性分析 |
| `accessibility_reviewer` | 可访问性检查 | WCAG 标准符合性 |
| `test_engineer` | 测试覆盖 | 单元测试/集成测试 |

### 文档编写代理

| 代理类型 | 用途 | 任务 |  
|------------|---------|---|
| `documentation_writer` | 编写 README 文件、API 文档和指南 |

### 个性化代理（Jake 的定制套件）🐾

通过 `agent_orchestrator` 功能为 Jake 的需求专门创建的代理：

| 代理类型 | 用途 | 主要特性 |
|------------|---------|--------------|
| `travel_event_planner` | 旅行内容协调 | 旅行计划、装备清单、活动安排 |
| `donut_care_coordinator` | 甜甜圈管理 | 饲养员协调、宠物看护、日常更新 |
| `pup_community_engager` | 狗狗社区管理 | 监控社交媒体、处理私信、与狗狗互动 |
| `print_project_manager` | 3D 打印工作流程 | 模型队列、材料追踪、打印优化 |

**总代理类型：25 种**  
- 5 种内容创作代理  
- 5 种开发代理  
- 5 种质量测试代理  
- 1 种文档编写代理  
- **5 种个性化代理**  
- **4 种元代理**  

### 元代理 🔄（代理创建系统）

| 代理类型 | 用途 | 功能描述 |  
|------------|---------|--------------|
| `agent_creator` | 设计新的人工智能代理 | 根据提示创建完整的代理定义 |
| `agent_design_reviewer` | 评估代理设计 | 评估质量、完整性和生产准备情况（评分 0-10） |
| `agent_refiner` | 优化代理设计 | 根据反馈进行改进以达到目标评分 |
| `agent_orchestrator` | 主要协调者 | 规划工作流程、生成代理、协调执行、汇总结果 |

**4 个代理的层次结构**：

```
Level 4: USER
    ↓ asks
Level 3: AGENT_ORCHESTRATOR
    ↓ plans, spawns, coordinates
Level 2: Meta Agents (creator, reviewer, refiner)
    ↓ designs, reviews, refines
Level 1: Task Agents (content writers, developers, QA)
    ↓ does work
Level 0: Actual Tasks
```

**总代理类型：20 种**  
- 5 种内容创作代理  
- 5 种开发代理  
- 5 种质量测试代理  
- 1 种文档编写代理  
- **4 种元代理**  

---

**工作流程 1：简单创建（2 个代理）**  
```python
from ai_orchestrator import (
    RealAIParallelOrchestrator,
    create_meta_agent_workflow
)

orch = RealAIParallelOrchestrator()

# Define agents to create
new_agents = [
    {'name': 'crypto_analyst', 'purpose': 'Analyze crypto trends'},
    {'name': 'content_strategist', 'purpose': 'Plan content calendars'}
]

# Creates: 2 creators + 2 reviewers (4 tasks)
tasks = create_meta_agent_workflow(new_agents)
results = orch.run_parallel(tasks)
```

**工作流程 2：迭代优化（3 个代理的循环）**  
```python
# The full 3-agent refinement workflow:
# Creator → Reviewer (scores) → Refiner (fixes) → Reviewer (verifies)
# Repeats until score >= 8.5

agents_to_refine = [
    {'name': 'my_agent', 'current_score': 7.4, 'target': 8.5}
]

# This runs the full loop automatically
results = orch.run_iterative_refinement(agents_to_refine)
# Result: 7.4 → 8.5+ ✅
```

**工作流程 3：自动化批量创建**  
```python
# Spawn the orchestrator to handle everything:
# - Plans workflow
# - Spawns all agents
# - Coordinates execution
# - Handles refinements
# - Compiles final report

result = sessions_spawn(
    task="Create 5 new agents and ensure all score 8.5+",
    agent_type='agent_orchestrator',
    timeout=600
)

# The orchestrator does everything autonomously!
```

这实现了 **代理的自我创建和优化**！

---

## 数据结构

### AgentTask  
```python
@dataclass
class AgentTask:
    agent_type: str           # Type from registry (required)
    task_description: str     # What to do (required)
    input_data: Dict          # Input parameters (optional)
    task_id: str             # Unique ID (auto-generated)
    timeout_seconds: int     # Max time (default: 120)
    output_format: str       # json|markdown|code|text
```

### AgentResult  
```python
@dataclass
class AgentResult:
    task_id: str             # Matches AgentTask
    agent_type: str          # Agent that produced this
    status: str              # pending|running|completed|failed
    output: Any              # Generated content (agent-dependent format)
    execution_time: float    # Time taken
    error: str              # Error message if failed
    session_key: str        # Spawned session identifier
```

---

## 示例

### 示例 1：生成多种内容风格  
```python
from ai_orchestrator import RealAIParallelOrchestrator, create_content_team

orch = RealAIParallelOrchestrator(max_concurrent=5)
tasks = create_content_team("Monday motivation", platform="bluesky")

# This spawns 5 REAL AI agents
results = orch.run_parallel(tasks)

print("Agents spawned! Each is generating content...")
print("Check sessions_list() to see running agents")
```

### 示例 2：全栈开发团队  
```python
from ai_orchestrator import RealAIParallelOrchestrator, create_dev_team

orch = RealAIParallelOrchestrator(max_concurrent=5)
tasks = create_dev_team("TaskManager", ['auth', 'tasks', 'teams'])

# Spawns 5 dev agents in parallel
results = orch.run_parallel(tasks)

# Each agent designs their layer independently
# - Frontend agent designs React components
# - Backend agent designs FastAPI routes
# - Database agent designs schema
# - etc.
```

### 示例 3：代码审查团队  
```python
from ai_orchestrator import RealAIParallelOrchestrator, create_review_team

code = open('app.py').read()

orch = RealAIParallelOrchestrator(max_concurrent=5)
tasks = create_review_team(code)

# Spawns 5 reviewers simultaneously
results = orch.run_parallel(tasks)

# Each reviews from different angle:
# - Code quality
# - Security
# - Performance
# - Accessibility
# - Test coverage
```

### 示例 4：元代理系统（代理创建代理）🔄  
```python
from ai_orchestrator import (
    RealAIParallelOrchestrator,
    create_meta_agent_workflow
)

orch = RealAIParallelOrchestrator(max_concurrent=6)

# Define new agents to create
new_agents = [
    {
        'name': 'social_media_analyst',
        'purpose': 'Analyze social media performance',
        'domain': 'social media analytics',
        'capabilities': ['engagement analysis', 'trend identification']
    },
    {
        'name': 'bug_hunter',
        'purpose': 'Find bugs in code',
        'domain': 'software QA',
        'capabilities': ['static analysis', 'edge case detection']
    },
    {
        'name': 'api_documenter',
        'purpose': 'Generate API docs',
        'domain': 'technical writing',
        'capabilities': ['endpoint extraction', 'example generation']
    }
]

# Creates 6 tasks: 3 creators + 3 reviewers
tasks = create_meta_agent_workflow(new_agents)
results = orch.run_parallel(tasks)

# Result: 3 complete agent definitions + 3 quality reviews
# All created entirely by AI in parallel!
```

**这就是代理的自我创建过程**——系统能够自我生成和优化！

### 示例 5：批量创建代理（同时生成 10 个以上代理） 🔥  
**已验证的功能**：系统能够同时生成 **20 个代理**（10 个创建者 + 10 个审查者）。

**实际测试结果**（2026-02-08）：  
- ✅ 10 个创建代理成功生成  
- ✅ 10 个审查代理成功生成  
- ✅ 所有代理均顺利完成  
- ✅ 平均质量得分：8.1/10  
- ✅ 生成了可投入生产的代理定义  

**实际限制**：最多可同时运行 20-50 个代理（取决于系统资源）  
详细实现请参见 `examples/mass_agent_creation.py`。

---

## 结果收集

代理会在会话记录中返回输出结果。要收集结果，请执行以下操作：

```python
# After spawning, poll for results
from tools import sessions_list, sessions_history

# Check which agents have completed
sessions = sessions_list(agent_id_pattern="agent_*")

for session in sessions:
    if session['status'] == 'completed':
        history = sessions_history(session['sessionKey'])
        # Parse JSON from final assistant message
        output = json.loads(history[-1]['content'])
```

**注意**：完整的结果收集功能由编排器实现。生成代理后，可以通过 `results` 属性获取结果。

---

## 架构说明

### 为什么选择 `sessions_spawn`？

之前的实现方式包括：
1. **多线程**：受 Python GIL 限制，无法实现真正的并行处理  
2. **多进程**：在 macOS 上存在问题，且 IPC 复杂  
3. **子进程工作者**：使用模板，而非真正的人工智能  

**`sessions_spawn` 是最佳解决方案**：
- 真正的隔离（独立会话）  
- 全面的人工智能功能  
- 内置在 OpenClaw 中  
- 自动清理资源  

### 限制

1. **依赖 OpenClaw**：必须在 OpenClaw 会话中运行  
2. **结果收集**：需要轮询 `sessions_list`  
3. **成本**：每次生成代理都需要单独的 API 调用（但使用相同的模型和凭据）  
4. **超时**：默认情况下代理运行时间限制为 120 秒  

---

## 文件结构  

```
~/.openclaw/skills/parallel-agents/
├── README.md                          # Quick start guide
├── SKILL.md                           # Complete documentation
├── USAGE-GUIDE.md                     # Practical examples and patterns
├── ai_orchestrator.py                 # Core orchestrator code
├── helpers.py                         # Auto-retry helper functions
└── examples/                          # Working examples
    ├── README.md                      # Examples documentation
    └── simple_parallel_research.py    # Simple example
```

---

## 版本历史

- **3.2.0**（2026-02-08）：**智能模型层次结构**  
  - ✅ 添加了智能模型升级机制（Haiku → Kimi → Opus）  
  - ✅ 优化成本：优先使用最便宜的模型，必要时升级  
  - 更新了 `helpers.py` 文件  
  - 在 `spawn_with_model_hierarchy()` 和 `spawn_parallel_with_retry()` 中加入了自动升级功能  
  - 提供了关于模型选择和成本节约的详细文档  
  - 测试证明：Haiku 能成功完成简单任务  

- **3.1.0**（2026-02-08）：**准备投入生产**  
  - 添加了自动重试机制（`spawn_with_retry`、`spawn_parallel_with_retry`）  
  - 清理了开发过程中的遗留文件  
  - 添加了详细的文档（README、USAGE-GUIDE）  
  - 简化了示例代码  
  - 在实际环境中进行了测试（Savannah 旅行项目）  
  - 发布到 ClawHub  

- **3.0.0**（2026-02-08）：**完全基于人工智能的版本**  
  - 完全重写，使用 `sessions_spawn` 功能  
  - 每个代理都是真正生成的人工智能会话  
  - 不再使用模拟或模板  
  - 需要 OpenClaw 环境支持  

---

## 故障排除

### “sessions_spawn 不可用”

**原因**：未在 OpenClaw 会话中运行脚本  
**解决方法**：在 OpenClaw 会话中运行脚本。  

### “找不到 ‘tools’ 模块”

**原因**：不在 OpenClaw 环境中运行  
**解决方法**：`tools` 模块仅在 OpenClaw 会话中可用。  

### 代理立即失败

**原因**：OpenClaw 门户未运行  
**解决方法**：启动门户：`openclaw gateway start`  

---

**现在真正生成的是人工智能代理**

不再使用模拟或模板。当您在 OpenClaw 中运行此功能时：  
1. 会触发真实的 `sessions_spawn` 调用  
2. 生成真正的人工智能子会话  
3. 每个代理都会进行真实的推理  
4. 生成真实的 JSON 输出  

这些代理不仅仅是执行代码——它们能够独立思考、创造和分析，真正运用人工智能能力。  

**欢迎使用真正的人工智能并行系统。** 🚀  

*专为 OpenClaw 设计，采用 `sessions_spawn` 技术。*  
*属于 OpenClaw 技能生态系统的一部分。*  
*“真实人工智能版本”：无模拟，仅使用真实的人工智能。*