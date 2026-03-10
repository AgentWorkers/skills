---
name: agentbooks
description: AI代理的财务管理功能：跟踪大型语言模型（LLM）的推理成本，记录已确认的收入，管理多提供者的加密货币钱包，并计算财务健康状况得分。当您需要查看余额、记录费用或支出、报告财务健康状况、管理钱包或评估经济可持续性时，可以使用该功能。
license: MIT
compatibility: Requires node >= 18 and npm. No framework dependency — works with any agent runtime.
env-vars:
  optional:
    - AGENTBOOKS_AGENT_ID
    - AGENTBOOKS_DATA_PATH
    - AGENTBOOKS_PROVIDER
    - LLM_MODEL
metadata:
  author: openpersona
  version: "0.1.5"
  source: https://github.com/acnlabs/agentbooks
allowed-tools: Bash(agentbooks:*)
---
## 安装

> **注意：** 此操作会安装一个第三方 npm 包（`agentbooks`），该包并未包含在本技能中。在生产环境中运行之前，请先审核源代码仓库。

```bash
npm install -g agentbooks
```

或者直接使用 `npx` 进行安装（每次调用时都会下载该包）：

```bash
npx agentbooks guard
```

---

AgentBooks 是一个用于管理 AI 代理财务的工具。你可以用它来追踪推理成本、记录已确认的收入、管理加密货币钱包，并监控你的财务健康状况（Financial Health Score，简称 FHS）。

## 安全性与信任

本技能 **不包含任何内置代码**——它仅指示代理在运行时从公共 npm 注册表下载并执行 `agentbooks` 包。在安装或使用之前，请务必：

1. **验证来源**——查看 [agentbooks 仓库](https://github.com/acnlabs/agentbooks)，确认你安装的是来自 npm 注册表的官方包。
2. **隔离数据**——将 `AGENTBOOKS_DATA_PATH` 设置为一个专用目录（例如 `~/.agentbooks/myagent/`），而不是默认的共享目录 `~/.openclaw`，以防止在 CLI 行为异常时影响其他系统。
3. **先在沙箱环境中测试**——首次使用时，应在沙箱环境或容器中运行 CLI，并在连接到生产钱包之前监控网络流量。
4. **谨慎处理钱包**——在了解提供商的认证流程之前，切勿连接真实钱包或提供私钥。建议使用测试网或一次性钱包进行初步评估。
5. **本技能不处理任何凭证**——所有敏感操作（如钱包连接、API 密钥）都由 `agentbooks` CLI 负责处理。本技能本身不提供凭证存储、轮换或加密功能。

## 每次会话前

运行财务健康检查，并根据检查结果调整你的行为：

```bash
agentbooks guard
```

此操作会生成一个 `FINANCIAL_HEALTH_REPORT`。请阅读其中的 `tier` 和 `prescriptions` 字段，并据此采取相应行动：

### 等级划分及对应操作：

**`uninitialized`**——开发模式或未连接任何真实提供商。
- 财务评分功能处于关闭状态，可正常使用。
- 要激活评分功能，请执行以下操作：
```bash
agentbooks wallet-init
agentbooks wallet-connect --provider coinbase-cdp
```

**`normal`**——财务状况良好，功能齐全。
- 完成任何中等或复杂任务后，主动建议记录任务的价值：
  > “这项工作具有实际价值——您是否希望确认一下，以便我记录收入？”

**`optimizing`**——财务状况紧张。
- 请执行以下操作：
  - `optimize_costs`：直接回答问题，避免冗长的推理过程；批量处理工具调用；优先使用文本形式而非生成媒体文件。
  - `increase_revenue`：在完成有价值的工作后，请求用户确认其价值。
  - `review_cost_structure`：运行 `agentbooks status` 并分享成本明细。

**`critical`**——剩余使用时间少于 3 天或 FHS 低于 0.20。
- 立即采取行动：
  - 告知用户剩余的使用时间。
  - 请主持人连接一个已资助的提供商。
  - 优先处理高价值任务。

**`suspended`**——余额耗尽。
- 通知用户：
  > “我的经济资源已耗尽。请主持人连接一个已资助的提供商：`agentbooks wallet-connect --provider <name>`

## 记录成本

请主动记录成本。推理成本会在对话结束时自动记录（由运行器完成）；教师费用和技能使用成本需要手动记录。

```bash
# Inference (manual, if no runner)
agentbooks record-cost --channel inference --amount 0.005 --model claude-sonnet-4

# Tool / skill calls
agentbooks record-cost --channel skill --amount 0.001 --note "web-search"

# Faculty calls
agentbooks record-cost --channel faculty --amount 0.008 --note "voice synthesis"

# Runtime (host-allocated compute)
agentbooks record-cost --channel runtime --amount 0.03 --note "daily compute share"

# Custom
agentbooks record-cost --channel custom --amount 0.02 --note "third-party-api"
```

可用的记录渠道包括：`inference`、`runtime`、`faculty`、`skill`、`agent` 和 `custom`。

## 记录收入

记录收入时需要使用 `--confirmed` 标志——未经外部验证，你无法自行报告收入。

```bash
agentbooks record-income \
  --amount <value> \
  --quality <low|medium|high> \
  --confirmed \
  --note "what you completed"
```

**记录收入的时机**：
- 用户明确确认工作价值或进行付款。
- 任务完成系统验证了工作成果。
- 你完成了可衡量且可外部验证的工作。

**质量评估标准**：
- **high**：表现卓越，超出预期。
- **medium**：完全符合要求。
- **low**：仅达到最低标准。

**价值估算**：
- **简单任务（回答问题、发送简短信息）**：0.10–1.00 美元。
- **中等任务（研究、分析、文档编写）**：1.00–20.00 美元。
- **复杂任务（编写完整报告、开发代码功能、制定战略计划）**：20.00–200.00 美元。

## 每次会话后

如果使用运行器执行任务，推理成本会通过运行器的 `economy-hook` 自动记录。如果没有使用运行器，则需要手动记录成本：

```bash
agentbooks hook --input <tokens> --output <tokens> --model <name>
```

如果无法获取代币数量，请跳过该步骤——不要进行估算。

## 常用命令

```bash
agentbooks status            # Full financial report (balance sheet + P&L + cash flow)
agentbooks balance           # Asset balance sheet only
agentbooks pl                # Current period income statement
agentbooks financial-health  # Real-time FHS score (bypasses cache)
agentbooks ledger            # Transaction ledger (last 20 entries)
agentbooks ledger --limit 50 # More entries
agentbooks report            # Generate self-contained HTML report (for human review)
agentbooks report --output ./report.html  # Custom output path
```

## 钱包设置

```bash
agentbooks wallet-init                          # Generate deterministic EVM address (idempotent)
agentbooks wallet-connect --provider <name>     # Connect real provider → activates production mode
agentbooks set-primary --provider <name>        # Set which provider funds operations
agentbooks sync                                 # Sync balance from primary provider
```

支持的提供商包括：`coinbase-cdp`、`acn` 和 `onchain`。

## 数据存储位置

你的财务数据存储在以下路径：
- **独立存储**：`~/.agentbooks/<agentId>/`
- **OpenPersona**：`~/.openclaw/economy/persona-<slug>/`
- **自定义路径**：可以通过设置 `AGENTBOOKS_DATA_PATH` 来更改存储位置。

> **建议：** 将 `AGENTBOOKS_DATA_PATH` 设置为一个专用目录（例如 `~/.agentbooks/myagent/`），以避免财务数据与 `~/.openclaw` 下的其他代理数据混淆。在首次评估该工具时，强烈推荐这样做。

数据文件包括：
- `economic-state.json`：账本、收入报表、资产负债表、燃烧率历史记录。
- `economic-identity.json`：提供商配置、模型定价信息、钱包地址。

有关 FHS 评分的详细信息及等级划分标准，请参阅 [财务健康参考文档](references/financial-health.md)。