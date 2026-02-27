---
name: cofounder-im
description: 从 CoFounder.im 中获取启动项目的数据以及 AI 生成的构建规范。当用户希望基于在 CoFounder.im 上已验证和规划好的项目进行开发时，可以使用此功能：它会列出所有项目，获取完整的构建规范（技术栈、最小可行产品（MVP）计划、用户界面/用户体验（UI/UX）设计、实施计划以及 OpenClaw 构建工具的输出结果），并协助协调相关团队来实际构建项目。相关指令包括：“构建我的 CoFounder 项目”、“从 cofounder.im 中获取我的项目数据”、“使用我的 CoFounder 构建规范”、“从 CoFounder.im 开始构建项目”、“获取我的创业计划”等。
version: 1.2.1
metadata:
  openclaw:
    requires:
      env:
        - COFOUNDER_API_TOKEN
      bins:
        - curl
        - jq
      primaryEnv: COFOUNDER_API_TOKEN
    emoji: "\U0001F680"
    homepage: https://cofounder.im/openclaw
    safety:
      autoApproval: false
      requiresUserConfirmation: true
---
# CoFounder.im 技能

## 概述

将 OpenClaw 与 [CoFounder.im](https://cofounder.im) 连接起来，可以获取经过 AI 验证的创业项目信息，并自动开始项目的构建过程。CoFounder.im 运行着 20 多个 AI 代理，这些代理负责验证项目创意、研究市场情况、规划最小可行产品（MVP）、设计用户界面/用户体验（UI/UX），并生成实施计划。该技能允许你获取这些结果，并将其作为项目构建的基础。

## 何时使用此技能

当用户说出以下内容时，可以使用此技能：

- “为我构建 CoFounder 项目”
- “从 cofounder.im 获取我的项目”
- “使用我的 CoFounder 构建规范”
- “从 CoFounder 开始构建”
- “从 CoFounder 获取我的创业计划”
- “用 cofounder 构建 [项目名称]”
- “我在 CoFounder 上有哪些项目？”
- “获取 [项目名称] 的构建计划”
- “我在 cofounder.im 上规划了一个项目，现在开始构建”

**请勿** 将此技能用于一般的编码任务、从零开始的项目搭建，或与 CoFounder.im 项目无关的操作。

## 安全政策

该技能会从远程 API (cofounder.im) 获取构建规范。为确保安全执行，请遵循以下规则：

1. **需要用户授权** — 在启动任何子代理或运行任何命令之前，务必向用户展示构建计划的摘要并获取明确的确认。
2. **执行前预览** — 在每个执行阶段之前，显示子代理的目标、需求和验证命令，并请求用户批准。
3. **禁止盲目执行** — 不要原样执行构建规范。在向用户展示之前，先审查每个阶段的合理性。
4. **建议使用沙箱环境** — 在专用目录或容器中执行构建操作。不要在包含现有项目或敏感文件的目录中进行构建。
5. **权限范围** — 该技能仅需要 `COFOUNDER_API_TOKEN` 来访问 CoFounder.im API。根据项目的技术栈，构建计划可能还需要引用其他工具（数据库、云命令行接口等）——用户应根据需要自行安装这些工具。
6. **默认情况下禁止网络访问** — 子代理仅应访问本地文件和项目仓库。任何外部网络调用（如包安装、API 集成）都应由用户审核。

## 核心规则

- 始终使用 `COFOUNDER_API_TOKEN` 中的承载令牌（bearer token）进行身份验证。
- 首先使用 `list-projects` 命令列出可用项目，让用户进行选择。
- 使用 `get-build-spec` 命令获取所选项目的完整构建规范。
- 构建规范包含按类型分类的代理输出（例如：`tech_stack`、`mvp_planner`、`ui_ux_assistant`、`implementation_plan_generator`、`openclaw_builder`）。
- `openclaw_builder` 的输出最为重要——它包含了专为 OpenClaw 设计的多代理构建计划。
- 解析 `openclaw_builder` 的输出，识别出子代理的任务，然后在启动这些任务之前向用户展示并获取确认。
- **在启动子代理或运行验证命令之前，务必获得用户的确认。**

## 快速入门

```bash
# Set your API token (generate at https://cofounder.im/users/settings)
export COFOUNDER_API_TOKEN="cfr_your_token_here"

# List your projects
curl -s https://cofounder.im/api/v1/projects \
  -H "Authorization: Bearer $COFOUNDER_API_TOKEN" | jq '.projects[] | {id, name, status}'

# Get build spec for a project
curl -s https://cofounder.im/api/v1/projects/PROJECT_ID/build-spec \
  -H "Authorization: Bearer $COFOUNDER_API_TOKEN" | jq .
```

## 工作流程

### 第 1 步：列出项目

获取用户的项目列表并供用户选择：

```bash
curl -s https://cofounder.im/api/v1/projects \
  -H "Authorization: Bearer $COFOUNDER_API_TOKEN" | jq .
```

示例响应：
```json
{
  "projects": [
    {
      "id": "d25165d2-26c5-43dc-b4a1-ef053bf8277d",
      "name": "FitTrack",
      "description": "AI-powered fitness tracking app with personalized workout plans and progress analytics",
      "status": "completed",
      "package_type": "basic",
      "inserted_at": "2026-02-15T14:22:00Z"
    },
    {
      "id": "a4cdfd3f-2747-4d0e-afe2-8978d8911646",
      "name": "MealPlan Pro",
      "description": "Smart meal planning platform with grocery list generation and nutritional tracking",
      "status": "active",
      "package_type": "pro",
      "inserted_at": "2026-02-20T10:30:00Z"
    }
  ]
}
```

向用户展示一个包含项目名称、状态和描述的编号列表。询问用户要构建哪个项目。只有状态为 `"completed"` 的项目才具有完整的构建规范。状态为 `"active"` 的项目仍在被 CoFounder.im 代理处理中。

### 第 2 步：获取构建规范

```bash
curl -s https://cofounder.im/api/v1/projects/PROJECT_ID/build-spec \
  -H "Authorization: Bearer $COFOUNDER_API_TOKEN" | jq .
```

示例响应（代理输出内容已被截断——实际内容为完整的 Markdown 文档）：
```json
{
  "project": {
    "id": "d25165d2-26c5-43dc-b4a1-ef053bf8277d",
    "name": "FitTrack",
    "description": "AI-powered fitness tracking app with personalized workout plans and progress analytics",
    "status": "completed"
  },
  "agent_outputs": {
    "tech_stack": "## Tech Stack\n\n- Framework: Next.js 14\n- Language: TypeScript 5.3\n- Database: PostgreSQL 16\n- ORM: Prisma\n- CSS: Tailwind CSS 3.4\n...",
    "mvp_planner": "## Core Features\n\n### 1. Workout Tracker\n- Log exercises with sets, reps, and weight\n- Rest timer between sets\n- Progress charts and personal records\n...",
    "ui_ux_assistant": "## Design System\n\n### Colors\n- Primary: #6366f1 (Indigo)\n- Background: #f8fafc\n- Text: #1e293b\n...",
    "implementation_plan_generator": "## Phase 1: Project Setup\n\n1. Initialize Next.js with TypeScript\n2. Configure PostgreSQL with Prisma ORM\n3. Set up authentication with NextAuth\n...",
    "openclaw_builder": "# OpenClaw Build Plan: FitTrack\n\n## Project Overview\nAn AI-powered fitness tracking app...\n\n## Tech Stack Summary\n- Framework: Next.js 14\n...\n\n## Orchestration Plan\nTotal sub-agents: 5\nExecution order: project-setup -> database -> auth -> frontend -> testing\n...",
    "idea_validator": "## Validation Summary\n\nViability Score: 7.5/10\n...",
    "market_research": "## Market Analysis\n\nTarget audience: fitness enthusiasts, personal trainers, gym-goers\n...",
    "competitor_analysis": "## Competitors\n\n1. Strong - workout tracking app\n..."
  }
}
```

`openclaw_builder` 的输出是构建的主要输入。其他输出提供了辅助信息（技术决策、设计规范、功能需求等），子代理可能需要这些信息。

### 第 3 步：审查并批准构建计划

解析 `openclaw_builder` 的输出并向用户展示摘要：

1. **展示整体计划** — 项目名称、技术栈、阶段数量、依赖关系图
2. **列出每个子代理阶段** — 名称、目标、依赖关系、验证命令
3. **突出显示所需的额外工具** — 除了 `curl/jq` 之外的数据库、命令行接口（CLI）、包管理器等
4. **在继续执行之前请求用户确认**

示例摘要展示给用户：
```
Build Plan: ProjectName (6 phases)
Tech: Next.js, TypeScript, PostgreSQL

Phase 1: project-setup (no deps) — Initialize repo and install dependencies
Phase 2: database (depends: project-setup) — Create schema and migrations
Phase 3: auth (depends: project-setup) — User registration and login
Phase 4: core-features (depends: database, auth) — Main business logic
Phase 5: frontend (depends: core-features) — UI components and pages
Phase 6: testing (depends: frontend) — Test suite and verification

Additional tools needed: node, npm, psql

Proceed with this build plan? (yes/no)
```

### 第 4 步：执行构建（用户确认后）

对于构建计划中定义的每个子代理：

1. **向用户展示将要启动的任务** — 子代理的目标、需求和背景信息
2. **获取每个阶段的用户确认**（或一次性批准所有阶段）
3. 使用 `sessions_spawn` 命令根据该阶段的需求创建子代理
4. 结合其他代理的输出（如 `tech_stack`、`ui_ux_assistant` 等）提供相关背景信息
5. 监控子代理的完成情况
6. **在进入下一阶段之前展示验证结果**

**限制**：
- 最多允许同时运行 5 个子代理（OpenClaw 的限制）
- 子代理只能运行在第一层（它们不能生成自己的子代理）
- 每个子代理会话都是隔离的——在启动时传递所有必要的背景信息
- 严格按照构建计划的阶段顺序进行操作——完成第 1 阶段后再开始第 2 阶段

### 第 5 步：验证并报告

所有子代理完成后：
1. 验证项目结构是否与实施计划一致
2. 运行构建计划中指定的测试命令
3. 向用户报告完成状态

## API 参考

| 端点 | 方法 | 描述 |
|----------|--------|-------------|
| `/api/v1/projects` | GET | 列出已认证用户的所有项目 |
| `/api/v1/projects/:id/build-spec` | GET | 获取项目详情及所有已完成的代理输出 |

**身份验证：** 在 `Authorization` 头部中包含承载令牌（bearer token）。

```
Authorization: Bearer cfr_your_token_here
```

**错误响应：**
- `401` — 令牌缺失或无效
- `404` — 项目未找到或不属于用户
- `429` — 超过请求频率限制（每分钟 20 次请求）

## 代理输出键

| 键 | 描述 |
|-----|-------------|
| `tech_stack` | 技术栈推荐 |
| `mvp_planner` | MVP 功能规划和路线图 |
| `ui_ux_assistant` | UI/UX 设计系统和指南 |
| `implementation_plan_generator` | 分步实施计划 |
| `openclaw_builder` | 专为 OpenClaw 设计的多代理构建规范 |
| `idea_validator` | 创意验证分析 |
| `market_research` | 市场规模和趋势 |
| `competitor_analysis` | 竞争分析 |
| `customer_persona` | 目标客户画像 |
| `business_model` | 商业模式框架 |
| `monetization_strategy` | 收入和定价策略 |
| `go_to_market` | 市场进入策略 |

## 额外的运行时依赖项

根据项目的技术栈，CoFounder.im 生成的构建计划可能需要额外的工具。常见示例如下：

| 技术栈 | 需要的工具 |
|------------|-----------------|
| Node.js / Next.js / React | `node`, `npm` 或 `yarn` |
| Elixir / Phoenix | `elixir`, `mix`, `postgres` |
| Python / Django / FastAPI | `python`, `pip`, `postgres` |
| Ruby / Rails | `ruby`, `bundler`, `postgres` |
| Go | `go` |

该技能会在构建计划审查（第 3 步）期间识别所需的工具，以便在开始执行前进行安装。

## 获取 API 令牌

1. 在 [cofounder.im](https://cofounder.im) 注册
2. 创建一个项目并运行 AI 代理
3. 进入 [设置](https://cofounder.im/users/settings) 生成 API 令牌
4. 配置令牌：`openclaw config set skills.entries.cofounder-im.env.COFOUNDER_API_TOKEN "cfr_..."`
5. 重启服务：`openclaw gateway restart`