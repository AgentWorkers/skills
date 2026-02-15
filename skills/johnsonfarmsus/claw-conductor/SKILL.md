---
name: claw-conductor
description: 这款开发工具具备始终在线的自主运行能力，同时具备智能的请求分类与处理功能：它能自动检测 Discord 频道，将相关请求路由到对应的项目工作区；区分简单请求与开发请求，并对复杂任务进行拆分处理；将任务分配给最合适的 AI 模型进行并行执行；最后汇总所有执行结果。
version: 2.1.0
---

# Claw Conductor v2.1

**您的随时待命的开发助手——从快速解答问题到完成整个项目构建，一切皆可处理。**

Claw Conductor 是一个智能的编排层，具备以下特点：

- 🎯 **随时待命**：自动处理所有消息（无需手动调用）
- 🤖 **智能分类**：区分简单问题和开发任务
- 💬 **兼容 Discord**：自动将频道映射到项目工作区
- 🔀 **多模型支持**：根据模型能力将任务分配给最合适的 AI
- ⚡ **并行执行**：高效地构建完整项目

## 🚀 工作原理

**自动流程：**
1. 消息到达 Discord 频道（例如 #scientific-calculator）
2. Claw Conductor 检测到该频道 → 将其映射到 `/root/projects/scientific-calculator`
3. 对请求进行分类：是简单问题还是开发任务？
4. **如果是简单问题**：由快速响应的模型在项目上下文中给出答案
5. **如果是开发任务**：则进行完整的任务编排——分解任务、分配路径、执行任务并整合结果

**您无需手动调用它**——它会自动处理一切！

## 🎯 使用示例

**简单问题**（快速响应）：
```
User: What files are in this project?
Conductor: 📋 Simple response mode
          [Lists files from /root/projects/scientific-calculator]

User: How does the calculator work?
Conductor: 📋 Simple response mode
          [Explains architecture with project context]
```

**开发任务**（完整编排）：
```
User: Build a scientific calculator with trig functions
Conductor: 🔧 Development mode - full orchestration
          [Decomposes into tasks, routes to models, executes in parallel]

User: Fix the bug in the calculation logic
Conductor: 🔧 Development mode - full orchestration
          [Analyzes code, creates fix, tests, commits]
```

**用户自定义设置**：
```
User: !simple Build a calculator
Conductor: 📋 Simple response mode
          [Gives advice/explanation instead of building]

User: !dev What files exist?
Conductor: 🔧 Development mode - full orchestration
          [Treats as development task - maybe creates file listing tool]
```

## 🚀 技能调用（针对 OpenClaw 代理）

**新功能：始终待命模式（推荐使用）**

将此技能配置为“Active Projects”类别中 Discord 频道的默认处理程序：
```python
# In OpenClaw agent configuration
from orchestrator import Orchestrator

orchestrator = Orchestrator()

# Handle ALL messages through conductor
result = orchestrator.handle_message(
    request=user_message,
    channel_id=discord_channel_id,
    channel_name=discord_channel_name
)
```

**旧版：手动调用**

当通过此技能发起开发请求时，执行以下步骤：
1. 从用户消息中提取请求内容（“use claw-conductor to”之后的所有内容）
2. 从请求中确定项目名称，或根据关键词生成项目名称
3. 使用 Python 执行任务编排：
   ```bash
   cd ~/.openclaw/skills/claw-conductor/scripts
   python3 -c "
   from orchestrator import Orchestrator
   import sys

   orchestrator = Orchestrator()

   request = '''[USER'S REQUEST HERE]'''
   project_name = '[PROJECT-NAME]'  # e.g., 'calculator-app', 'todo-app', 'blog-site'

   # Get GitHub user from config
   github_user = orchestrator.config.get('github_user')

   result = orchestrator.execute_request(
       request=request,
       project_name=project_name,
       github_user=github_user
   )

   # Report results back to Discord
   if result['success']:
       print(f\"✅ Project '{project_name}' completed successfully!\")
       print(f\"📦 {result['tasks_completed']} tasks completed\")
       if github_user:
           print(f\"🔗 GitHub: https://github.com/{github_user}/{project_name}\")
       print(f\"📁 Workspace: {result.get('workspace', '/root/projects/' + project_name)}\")
   else:
       print(f\"❌ Project failed: {result.get('error', 'Unknown error')}\")
       sys.exit(1)
   "
   ```

4. 在执行过程中向 Discord 报告进度：
   - 公布任务分解结果
   - 报告任务分配情况
   - 更新并行执行进度
   - 通过 GitHub 链接分享最终结果

**示例调用：**
用户输入：`@OpenClaw use claw-conductor to build a calculator app`

系统执行步骤：
- 请求：构建一个计算器应用程序
- 项目名称：`calculator-app`
- 使用相应参数运行任务编排程序

---

## v2.1 的新功能

- 🤖 **AI 驱动的任务分解**：使用最佳 AI 模型（自动选择或手动配置）智能分析复杂请求
- 🎯 **完整任务编排**：分解复杂任务 → 分配子任务 → 并行执行 → 整合结果
- ⚡ **并行执行**：最多支持 5 个任务同时在多个项目中运行
- 📁 **项目管理**：自动创建工作区、初始化 Git 仓库并集成 GitHub
- 🔗 **依赖关系处理**：自动处理任务依赖关系和文件冲突
- 📦 **自动整合**：合并结果、运行测试、提交到 Git 仓库并推送至 GitHub

---

## 快速入门

### 安装

在 OpenClaw 中安装：
```bash
cd ~/.openclaw/skills
git clone https://github.com/johnsonfarmsus/claw-conductor.git
cd claw-conductor
./scripts/setup.sh
```

### 首次设置

按照说明完成首次配置：
```bash
./scripts/setup.sh
```

此过程会生成您的个性化 `agent-registry.json` 文件，其中包含：
- AI 模型配置
- 成本信息（免费/付费选项）
- 模型的能力评分
- 任务分配偏好设置

### 使用方法

- **简单请求**：
```
@OpenClaw use claw-conductor to build a calculator app
```

- **复杂请求**：
```
@OpenClaw use claw-conductor to build a towing dispatch system with:
- Customer portal for requesting service
- Driver dashboard for accepting jobs
- Admin panel for managing users
- Real-time location tracking
- Payment integration
```

---

## 完整工作流程

### 示例：任务调度系统

**请求：**
```
Build a towing dispatch system with customer portal,
driver dashboard, admin panel, and real-time tracking
```

**任务分解：**
```
Task 1: Database schema (database-operations, complexity: 4)
Task 2: Authentication system (security-fixes, complexity: 4)
Task 3: Customer portal UI (frontend-development, complexity: 3)
Task 4: Driver dashboard UI (frontend-development, complexity: 3)
Task 5: Admin panel UI (frontend-development, complexity: 3)
Task 6: REST API endpoints (api-development, complexity: 3)
Task 7: Real-time tracking (performance-optimization, complexity: 5)
Task 8: Unit tests (unit-test-generation, complexity: 2)
```

**任务分配：**
```
Task 1 → Mistral Devstral (score: 92, best for database)
Task 2 → Mistral Devstral (score: 88, security expert)
Task 3 → Mistral Devstral (score: 95, frontend expert)
Task 4 → Mistral Devstral (score: 95, frontend expert)
Task 5 → Mistral Devstral (score: 95, frontend expert)
Task 6 → Llama 3.3 70B (score: 87, API specialist)
Task 7 → Mistral Devstral (score: 78, fallback - needs Claude ideally)
Task 8 → Llama 3.3 70B (score: 95, test generation expert)
```

**任务执行：**
```
Parallel execution plan:
Worker 1: Task 1 (Database) → Mistral
Worker 2: Task 3 (Customer UI) → Devstral
Worker 3: Task 4 (Driver UI) → Devstral
Worker 4: Task 5 (Admin UI) → Devstral
Worker 5: Task 6 (API) → Llama

After Task 1 completes:
Worker 1: Task 2 (Auth - depends on DB) → Mistral

After all code complete:
Worker 1: Task 8 (Tests) → Llama
```

**最终结果：**
```
✅ All 8 tasks completed in 47 minutes
📦 Committed to git with 8 changes
🔗 Pushed to GitHub repository
🎉 Project ready for deployment
```

---

## 评分机制

每个模型针对每个任务会被评分 0-100 分：

```python
score = (
    (rating / 5.0) * 50 +              # Model capability (0-50 pts)
    (1 - complexity/5.0) * 40 +        # Complexity fit (0-40 pts)
    (experience / 100) * 10 +          # Experience (0-10 pts)
    cost_factor * 10                   # Cost (0-10 pts)
)
```

**限制条件：**模型无法处理超出其 `max_complexity` 评分能力的任务。

**评分示例**

**任务：后端 API 开发（复杂度：4）**

| 模型 | 能力评分 | 任务复杂度匹配度 | 经验值 | 成本 | 总分 |
|-------|------------|----------------|------------|------|-------|
| Mistral Devstral | 4★（40 分） | 可处理该任务（40 分） | 0 分（无经验） | 免费（10 分） | **90/100** |
| Llama 3.3 70B | 4★（40 分） | 可处理该任务（40 分） | 可处理 2 个子任务（2 分） | 免费（10 分） | **92/100** ✅ |
| Perplexity | 不适用 | 无法处理后端开发任务 | - | - | **0/100** |

**胜出者：**Llama 3.3 70B**（经验值更高）

---

## 配置设置

### 代理注册表结构

`config/agent-registry.json` 文件的内容：
```json
{
  "version": "1.0.0",
  "user_config": {
    "cost_tracking_enabled": true,
    "prefer_free_when_equal": true,
    "max_parallel_tasks": 5,
    "default_complexity_if_unknown": 3,
    "fallback": {
      "enabled": true,
      "retry_delay_seconds": 2,
      "track_failures": true,
      "penalize_failures": true,
      "failure_penalty_points": 5
    }
  },
  "agents": {
    "mistral-devstral-2512": {
      "model_id": "mistral/devstral-2512",
      "provider": "mistral",
      "context_window": 256000,
      "enabled": true,
      "user_cost": {
        "type": "free-tier",
        "input_cost_per_million": 0,
        "output_cost_per_million": 0
      },
      "capabilities": {
        "frontend-development": {
          "rating": 5,
          "max_complexity": 5,
          "notes": "Expert - near-parity with Claude"
        },
        "multi-file-refactoring": {
          "rating": 5,
          "max_complexity": 5,
          "notes": "Expert - designed for 50+ file changes"
        }
      }
    }
  }
}
```

### 回退策略

（用户可配置的保守策略）：
1. 尝试首选模型（第 1 次尝试）
2. 再次尝试首选模型（第 2 次尝试）
3. 如果两次尝试均失败 → 尝试第二名模型（第 3 次尝试）
4. 如果所有尝试均失败 → 放弃并通知 Discord

**为何采用保守策略？**
防止使用不合适的模型导致任务无法完成。

---

## 任务类别（23 个标准类别）：
- 代码生成（新增功能）
- 错误检测与修复
- 多文件重构
- 单元测试生成
- 复杂问题调试
- API 开发
- 安全漏洞检测
- 安全修复
- 文档生成
- 代码审查
- 前端开发
- 后端开发
- 数据库操作
- 代码库探索
- 依赖管理
- 旧代码现代化
- 错误修正
- 性能优化
- 测试覆盖率分析
- 算法实现
- 通用代码生成

---

## 高级功能

- **多项目支持**：支持在不同项目中同时处理多个请求：
```
Project A: Dispatch System (3 tasks running)
Project B: Calculator App (2 tasks running)
────────────────────────────────────────────
Total: 5 concurrent tasks (at global limit)
```

- **文件冲突检测**：
  触及相同文件的任务会按顺序执行：
```
Task 1: Modify src/api/users.js → Running
Task 2: Modify src/api/users.js → Queued (waits for Task 1)
Task 3: Modify src/ui/dashboard.js → Running (independent)
```

- **依赖关系驱动的调度**：
  自动考虑任务之间的依赖关系进行调度：
```
Task 1: Database schema → No deps, starts immediately
Task 2: Auth system → Depends on Task 1, waits
Task 3: Frontend UI → Depends on Task 2, waits
Task 4: Tests → Depends on all, runs last
```

- **自动整合**：
  任务完成后：
  1. 检查 Git 仓库中的冲突
  2. 运行测试（如 pytest、npm test 等）
  3. 使用常规提交信息提交代码
  4. （如果配置了）将结果推送到 GitHub
  5. 向 Discord 报告进度

---

## 示例

- **简单计算器项目**：
  **结果：**3 个子任务（用户界面、逻辑实现、测试）  
  **完成时间：**约 8 分钟  
  **提交至 GitHub：**已完成

- **调度系统项目**：
  **结果：**3 个模型同时处理 8 个子任务  
  **完成时间：**约 45 分钟  
  **最终成果：**一个可运行的应用程序

- **带文档的 API 项目**：
  **结果：**5 个子任务（数据模型设计、认证机制、API 接口、文档编写、测试）  
  **完成时间：**约 20 分钟  
  **设计原则：**API 首先完成构建

---

## 故障排除

- **任务分解问题**：
  **问题：**请求未被正确分解  
  **解决方法：**请在请求中明确指定任务类型（例如：数据库、API、前端、测试）

- **模型选择问题**：
  **问题：**选择了不合适的模型  
  **解决方法：**调整 `agent-registry.json` 中的模型能力评分

- **执行失败**：
  **问题：**任务执行失败  
  **解决方法：**优先尝试首选模型两次，其次尝试第二名模型两次；查看 `.claw-conductor/execution-log.json` 文件中的错误日志

- **Git 冲突问题**：
  **问题：**整合过程中出现冲突  
  **解决方法：**目前需要手动解决；未来计划实现 AI 驱动的冲突解决机制

---

## 开发计划

- [x] 任务分解功能（v2.0）
- [x] 并行执行功能（v2.0）
- [x] 多项目支持功能（v2.0）
- [x] 自动整合功能（v2.0）
- [ ] AI 驱动的任务分解功能（v2.1）
- [ ] 实时任务进度更新功能（v2.2）
- [ ] 实时任务流处理功能（v2.2）
- [ ] Web 界面管理功能（v3.0）

---

## 许可证

采用 GNU AGPL v3 许可证——详情请参阅 LICENSE 文件。

**许可证要求：**服务器端代码必须公开可用。

---

## 贡献指南

有关贡献方式，请参阅 [CONTRIBUTING.md](CONTRIBUTING.md)。

发布平台：ClawHub.ai：https://clawhub.ai/skills/claw-conductor

---

*由 Claw Conductor 团队精心制作*