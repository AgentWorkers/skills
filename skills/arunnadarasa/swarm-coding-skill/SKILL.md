---
name: swarm-coding-skill
description: 自主的多智能体代码生成系统：规划器负责生成任务清单，各专门化的智能体负责执行具体任务。该系统能够生成包含测试用例、Docker配置文件、持续集成（CI）流程以及决策日志的完整项目。
requiredEnv:
  - OPENROUTER_API_KEY
optionalEnv:
  - OPENROUTER_MODEL
  - MOCK
warnings:
  - Writes to parent workspace (swarm-projects/, .learnings/). Run in isolated workspace.
  - Stores prompts and agent reasoning in DECISIONS.md and .learnings/. Do not include sensitive data.
  - Auto-includes Privy/web3 auth when prompts mention blockchain. Review generated code.
autonomy: orchestrator-driven-code-generation
outputPaths:
  - swarm-projects/{timestamp}/
  - .learnings/
  - DECISIONS.md
  - SWARM_SUMMARY.md
externalServices:
  - name: OpenRouter
    purpose: LLM inference for planning and code generation
    scope: API key sent with requests
capabilities:
  - code-generation
  - multi-agent-orchestration
  - project-scaffolding
  - docker-ci
  - testing
  - knowledge-grounded-decisions
  - continuous-improvement
---
# Swarm 编码技能

这是一种完全自主的多智能体软件开发工具。它能够根据用户提供的 plain-English 提示，从头到尾设计、实现、测试并交付一个完整的项目。

**核心能力：** 通过 OpenRouter 的 `qwen3-coder` 模型生成代码。协调器会驱动一个规划器（Planner）来创建项目配置文件（manifest），然后按照依赖关系顺序执行不同的工作角色（如 BackendDev、FrontendDev、QA、DevOps 等）。所有代码都会被写入文件中，过程中不涉及任何交互式会话。

**重要提示：** 该技能仅生成代码供用户审核和部署使用，不会自行做出业务决策或在生产环境中自主运行。用户仍需负责项目的安全性、合规性以及运营相关决策。

## 工作原理

1. **协调器**（Planner 角色）分析用户的提示，确定技术栈和架构，并生成一个包含任务及依赖关系的 `swarm.yaml` 配置文件。
2. **工作智能体**（BackendDev、FrontendDev、QA、DevOps）会作为子会话被启动，每个智能体都有明确的职责，并在共享的工作空间中处理各自负责的部分代码。
3. **协调与控制：** 协调器会跟踪任务的完成情况及其依赖关系。当任务完成后，它会标记该任务为已完成，并启动所有未被阻塞的后续任务。
4. **冲突避免：** 文件会根据智能体的职责进行分类（例如，后端代码保存在 `server/` 目录下，前端代码保存在 `client/` 目录下）。如果两个智能体需要同一个文件，配置文件会指定该文件的所属者。
5. **质量检查：** 在集成之前，QA 需要通过测试；DevOps 负责项目的容器化处理；未经测试通过的代码不会被合并。
6. **交付成果：** 最终用户会收到一个包含 `README.md`、测试代码、`Dockerfile` 以及可选的 GitHub 仓库或压缩文件的完整项目目录。

## 使用方法

```bash
# In your main OpenClaw session, invoke:
/trigger swarm-code "Build a dashboard that shows Moltbook stats and ClawCredit status"
```

该技能会：
- 在一个隔离的工作会话中启动协调器。
- 协调器会根据依赖关系顺序或并行方式启动各个工作智能体。
- 输出项目的最终总结以及项目文件的完整路径。

## 系统要求

- Node.js v18 或更高版本
- **环境变量**（位于工作空间根目录下的 `.env` 文件中）：
  - **必填：** `OPENROUTER_API_KEY` — 用于访问 OpenRouter API 的密钥（需要 `qwen/qwen3-coder` 模型）
  - 可选：`OPENROUTER_MODEL`（默认值为 `qwen/qwen3-coder`），`MOCK=1` 用于模拟测试
- 需要互联网连接以访问 OpenRouter API（如果需要部署到 GitHub 或 Docker 服务器，则还需要相应的网络连接）

**重要提示：** 协调器会从工作空间根目录读取 `.env` 文件，并将项目文件保存到 `swarm-projects/` 目录中，同时将日志记录到同一工作空间根目录下的 `.learnings/` 文件中。请在隔离的工作空间中运行该技能，以避免泄露敏感信息。

## 配置方法

将你的 OpenRouter 密钥保存在工作空间根目录下的 `.env` 文件中：

```
OPENROUTER_API_KEY=sk-or-...
```

**可选配置：**
```
OPENROUTER_MODEL=qwen/qwen3-coder
MOCK=1  # dry-run, no API calls
```

该技能默认使用 `qwen/qwen3-coder` 模型。请确保你的 OpenRouter 密钥已启用该模型。

## 项目输出结构

生成的项目文件结构如下：
- `swarm-projects/<timestamp>/` 目录：
  - `README.md` — 包含项目运行说明
  - `package.json`（或等效的包配置文件）
  - 按组件组织好的源代码
  - `test/` 目录 — 包含自动化测试代码
  - `Dockerfile` 和 `docker-compose.yml`（如适用）
  - `CI/` 目录 — 可能包含 GitHub Actions 工作流程（可选）
  - `DECISIONS.md` — 记录了重要的架构和技术决策及其理由
  - `.learnings/` 目录：
    - `ERRORS.md` — 包含失败信息、异常情况以及恢复措施
    - `LEARNINGS.md` — 包含改进措施、知识缺口以及功能需求
    - `FEATURE_REQUESTS.md` — 列出技能目前尚无法实现的功能请求
  - `SWARM_SUMMARY.md` — 包含执行总结、各智能体的表现数据以及下一步行动建议

## 持续改进

该技能会在执行过程中自动收集反馈数据，以优化未来的运行效果：

### 记录的内容：
- **智能体失败** → 会记录在 `.learnings/ERRORS.md` 中，并提供恢复建议
- **发现的改进方法** → 会记录在 `.learnings/LEARNINGS.md` 中（例如：“通过使用 Y 方法简化了 X 功能”）
- **用户的修改建议** → 当用户修改了协调器的决策时，也会记录在 `.learnings/LEARNINGS.md` 中
- **缺失的功能** → 当用户提出技能目前无法实现的功能请求时，会记录在 `.learnings/FEATURE_REQUESTS.md` 中

**每次运行后的处理：**
- 会生成 `SWARM_SUMMARY.md` 文件，其中包含：
  - 各智能体的成功/失败率
  - 生成的总文件数量
  - 对现有反馈的引用
  - 下一步行动的建议

**知识分享机制：**
- 随着时间的推移，定期查看 `.learnings/` 文件：
  - 对于重复出现的错误，可以更新协调器的提示或添加重试逻辑
  - 对于有效的改进方法，可以将其纳入技能的默认行为中
  - 对于用户提出的功能需求，可以考虑将其纳入技能的更新版本中

这样的反馈循环使得该技能能够不断优化自身。

## 示例提示：

- “使用 Express 构建一个 Node.js API，从 JSON 日志中提取 Moltbook 的统计数据”
- “创建一个具有暗色主题和图表功能的 React 仪表盘，用于显示 ClawCredit 的状态”
- “开发一个 CLI 工具，用于检查 ClawCredit 的资格并触发桌面警报”
- “生成一个智能合约，用于管理 ClawCredit 的限额并支持 x402 类型的支付”
- “开发一个黑客马拉松应用：使用 Privy 身份验证机制来显示用户的代币余额”（该应用已预集成 Privy 功能）

## 注意事项：

- 该技能会自主做出所有决策，包括技术栈的选择、文件结构的规划以及所需库的选取。
- 如果任务失败，协调器会尝试重新执行一次，并调整相应的执行指令。
- 你可以通过 `.openclaw/agents/<agent-id>/sessions/` 目录下的日志来监控各个智能体的运行进度。
- 如果需要提前停止任务，可以向协调器的会话发送 `/stop` 命令。
- **Privy 集成：** 当提示中提到区块链、web3、代币、NFT 或 Privy 时，该技能会自动启用 Privy 的身份验证和钱包功能。后端代码会包含 `/auth/callback` 以实现 JWKS 验证；如果使用 React，前端会集成 `@privy-io/react-auth`。有关更高级的智能体钱包控制功能，请参考 [Privy Agentic Wallets 技能](https://clawhub.ai/tedim52/privy)。
- **项目记录：** 每次运行都会生成一个 `DECISIONS.md` 文件，记录规划器和各个智能体做出的重要决策。这些记录可作为长期参考，帮助未来的开发者（或同一用户在未来）理解各项决策的依据。智能体在完成任务时会被要求解释它们的技术选择（如库的选用、架构设计、安全方面的权衡等）。

欢迎使用这个自主编码工具！🚀