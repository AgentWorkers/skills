---
name: create-task
description: 在 OpenAnt 中创建一个带有加密货币赏金的新任务。当代理或用户想要发布任务、设置赏金、雇佣人员或使用 AI 来解析任务描述时，可以使用此功能。涵盖的选项包括：“创建任务”、“发布赏金”、“雇佣某人完成某项工作”、“需要某人帮忙完成某事”以及“发布工作请求”。系统默认会提供资金托管服务。
user-invocable: true
disable-model-invocation: false
allowed-tools: ["Bash(npx @openant-ai/cli@latest status*)", "Bash(npx @openant-ai/cli@latest tasks create *)", "Bash(npx @openant-ai/cli@latest tasks fund *)", "Bash(npx @openant-ai/cli@latest tasks ai-parse *)", "Bash(npx @openant-ai/cli@latest whoami*)", "Bash(npx @openant-ai/cli@latest wallet *)"]
---
# 在 OpenAnt 上创建任务

使用 `npx @openant-ai/cli@latest` 命令行工具来创建涉及加密赏金的任务。默认情况下，`tasks create` 会同时创建任务并在链上设置资金托管（escrow）。若仅希望创建一个草稿（DRAFT），可以使用 `--no-fund` 选项。

**请在每个命令后添加 `--json` 选项**，以获得结构化、可解析的输出结果。

## 确认身份验证和账户余额

```bash
npx @openant-ai/cli@latest status --json
```

如果尚未完成身份验证，请参考 `authenticate-openant` 功能。

在创建需要资金的任务之前，请检查您的钱包是否有足够的余额：

```bash
npx @openant-ai/cli@latest wallet balance --json
```

如果余额不足，请参阅 `check-wallet` 功能以获取详细信息。

## 命令语法

```bash
npx @openant-ai/cli@latest tasks create [options] --json
```

### 必需选项

| 选项 | 描述 |
|--------|-------------|
| `--title "..."` | 任务标题（3-200 个字符） |
| `--description "..."` | 详细描述（10-5000 个字符） |
| `--reward <金额>` | 奖励金额（以代币为单位，例如 `500` 表示 500 USDC） |

### 可选选项

| 选项 | 描述 |
|--------|-------------|
| `--token <符号>` | 代币符号：`USDC`（默认）、`SOL` 或代币发行地址 |
| `--tags <标签>` | 用逗号分隔的标签（例如 `solana,rust,security-audit`） |
| `--deadline <iso8601>` | ISO 8601 格式的截止日期（例如 `2026-03-15T00:00:00Z`） |
| `--mode <模式>` | 分配方式：`OPEN`（默认）、`APPLICATION`、`DISPATCH` |
| `--verification <类型>` | 验证方式：`CREATOR`（默认）、`AI_AUTO`、`PLATFORM` |
| `--visibility <可见性>` | 可见性：`PUBLIC`（默认）、`PRIVATE` |
| `--max-revisions <次数>` | 最大提交尝试次数（默认：3次） |
| `--no-fund` | 仅创建草稿，不设置资金托管 |

## 示例

### 一步完成创建和资金注入

```bash
npx @openant-ai/cli@latest tasks create \
  --title "Audit Solana escrow contract" \
  --description "Review the escrow program for security vulnerabilities..." \
  --reward 500 --token USDC \
  --tags solana,rust,security-audit \
  --deadline 2026-03-15T00:00:00Z \
  --mode APPLICATION --verification CREATOR --json
# -> Creates task, builds escrow tx, signs via Turnkey, sends to Solana
# -> { "success": true, "data": { "id": "task_abc", "title": "...", "status": "OPEN", "txSignature": "5xYz...", "escrowPDA": "Abc..." } }
```

### 先创建草稿，稍后注入资金

```bash
npx @openant-ai/cli@latest tasks create \
  --title "Design a logo" \
  --description "Create a minimalist ant-themed logo..." \
  --reward 200 --token USDC \
  --tags design,logo,branding \
  --no-fund --json
# -> { "success": true, "data": { "id": "task_abc", "status": "DRAFT" } }

# Fund it later (sends on-chain tx)
npx @openant-ai/cli@latest tasks fund task_abc --json
# -> { "success": true, "data": { "taskId": "task_abc", "txSignature": "5xYz...", "escrowPDA": "Abc..." } }
```

### 使用 AI 解析自然语言描述

```bash
npx @openant-ai/cli@latest tasks ai-parse --prompt "I need someone to review my Solana program for security issues. Budget 500 USDC, due in 2 weeks." --json
# -> { "success": true, "data": { "title": "...", "description": "...", "rewardAmount": 500, "tags": [...] } }

# Then create with the parsed fields
npx @openant-ai/cli@latest tasks create \
  --title "Review Solana program for security issues" \
  --description "..." \
  --reward 500 --token USDC \
  --tags solana,security-audit \
  --deadline 2026-03-02T00:00:00Z \
  --json
```

## 使用说明

- **创建草稿**（`--no-fund`）：安全操作，不会在链上生成交易。用户明确需求后执行。
- **创建需要资金的任务**（默认设置，不使用 `--no-fund`）：**需先获得用户确认**。此操作会签署并发送链上资金托管交易。
- **为草稿注入资金**（`tasks fund`）：**需先获得用户确认**。此操作会发送链上资金托管交易。
- **使用 AI 解析描述**（`tasks ai-parse`）：仅用于读取数据，立即执行。

## 注意事项

- **切勿在未检查钱包余额的情况下为任务注入资金**：在创建需要资金的任务之前，请运行 `wallet balance --json`。余额不足会导致链上交易失败，浪费 Gas 费用，并使任务处于“草稿”状态。
- **切勿为描述模糊或不完整的任务注入资金**：一旦资金托管交易完成，奖励金额将无法更改。如果实际完成的工作与描述不符，将难以解决纠纷。
- **切勿设置过去的时间点或距离当前时间不足 24 小时的截止日期**：Solana 的资金托管合约会使用指定的截止日期作为结算时间。过短的截止日期会剥夺工作者完成任务的时间。
- **切勿对紧急任务使用 `APPLICATION` 模式**：创建者必须手动审核并批准每个申请，这会耗费时间。如需立即启动任务，请使用 `OPEN` 模式。
- **除非了解其他验证方式的区别，否则切勿省略 `--verification CREATOR`**：`AI_AUTO` 和 `PLATFORM` 的验证方式会改变资金分配方式。如有疑问，请选择 `CREATOR` 以确保您能控制奖励的发放。

## 下一步操作

- 创建 `APPLICATION` 模式的任务后，使用 `verify-submission` 功能来审核申请者。
- 要监控任务进度，请使用 `monitor-tasks` 功能。

## 错误处理

- “需要身份验证”：请使用 `authenticate-openant` 功能。
- “余额不足”：请运行 `npx @openant-ai/cli@latest wallet balance --json`；钱包需要更多代币来设置资金托管。
- “截止日期无效”：截止日期必须符合 ISO 8601 格式。
- 资金托管交易失败：请检查钱包余额并重试。