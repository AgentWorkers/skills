---
name: agents-manager
description: 管理 Clawdbot 代理：发现代理、生成代理配置文件、追踪代理的功能、定义路由层次结构，并分配任务。
homepage: https://www.clawhub.com/skills/agents-manager
metadata: {"openclaw":{"emoji":"🕵️","requires":{"bins":["node"]}}}
---

# 代理管理器

集中管理所有 Clawdbot 代理：发现可用的代理，了解它们的功能，定义路由层次结构（谁可以分配任务给谁，谁需要向谁汇报），并智能地通过升级流程来路由新任务。

## 🤖 用于代理

### 系统提示（复制粘贴）
将此提示提供给任何代理，以教授它们使用该技能：
> “您可以使用 `agents-manager` 技能。使用它来发现其他代理（`scanAgents`）、检查权限（`can_assign.js`）以及路由任务。请始终遵循握手协议：在分配任务之前，请先检查 `requires_approval` 的值。如果值为 `true`，请先咨询我。”

### 核心规则
1. **发现：** 在假设代理存在之前，务必先检查 `scanAgents.js`。
2. **权限：** 在不检查 `can_assign.js` 或 `agent-registry.md` 的情况下，切勿分配任务。
3. **协议：**
   - 如果 `requires_approval` 的值为 `FALSE` -> 直接分配任务。
   - 如果 `requires_approval` 的值为 `TRUE` -> 请请求主管（人类或代理）的批准。

## 👤 用于人类

### 快速入门
| 目标 | 命令 |
|------|---------|
| **设置** | `node scripts/setup_wizard.js`（请先运行此脚本！） |
| **列表** | `node scripts/scanAgents.js` |
| **健康检查** | `node scripts/health_check.js` |
| **统计信息** | `node scripts/log_analyzer.js` |

### 1. 代理发现与配置
列出并分析所有代理的信息，以了解它们的功能和路由配置。

```bash
# List all agents
node {baseDir}/scripts/scan_agents.js

# Profile specific agent
node {baseDir}/scripts/generate_card.js <agent_id>
```

### 2. 验证与健康检查
确保您的代理生态系统处于正常运行状态且配置有效。

```bash
# Validate registry integrity
node {baseDir}/scripts/validate_registry.js

# Check permissions (Agent A -> Agent B)
node {baseDir}/scripts/can_assign.js <source_id> <target_id>

# Visualize hierarchy
node {baseDir}/scripts/visualize_agents.js
```

### 3. 任务路由与升级
使用 `references/task-routing-rules.md` 来定义任务在代理之间的流动方式：
- **直接分配：** 代理 → 代理（如果 `can_assign_to` 允许的话）
- **请求批准：** 如果 `requires_approval` 的值为 `TRUE`，则需要请求批准。
- **升级流程：** 助手 → 监督者 → 人类

## 资源
- **[agent-profile-schema.md](references/agent-profile-schema.md)**：包含路由信息和卡片字段的标准代理配置文件。
- **[agent-registry.md](references/agent-registry.md)**：所有代理的实时注册表。
- **[task-routing-rules.md](references/task-routing-rules.md)**：任务路由规则和握手协议。

## 脚本
- `scanAgents.js`：代理发现工具
- `validate_registry.js`：配置文件验证工具
- `can_assign.js`：权限检查工具
- `generate_card.js`：代理信息卡片生成工具
- `visualize_agents.js`：代理层次结构可视化工具
- `scan_agents.js`：代理发现工具
- `validate_registry.js`：配置文件验证工具
- `can_assign.js`：权限检查工具
- `generate_card.js`：代理信息卡片生成工具
- `visualize_agents.js`：代理层次结构可视化工具
- `health_check.js`：状态监控工具（正常/运行缓慢/离线）
- `log_analyzer.js`：性能统计信息（任务数量/成功率）
- `setup_wizard.js`：交互式配置工具