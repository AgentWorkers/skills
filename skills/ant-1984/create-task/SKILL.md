---
name: create-task
description: 在 OpenAnt 中创建一个带有加密货币奖励的新任务。适用于代理或用户发布任务、设置奖励、雇佣人员、发布工作内容，或使用 AI 分析任务描述的情况。涵盖的功能包括：“创建任务”、“发布奖励”、“雇佣某人完成某项工作”、“需要某人帮忙完成某事”以及“发布工作请求”。系统默认会提供资金托管服务。
user-invocable: true
disable-model-invocation: false
allowed-tools: ["Bash(npx @openant-ai/cli@latest status*)", "Bash(npx @openant-ai/cli@latest tasks create *)", "Bash(npx @openant-ai/cli@latest tasks fund *)", "Bash(npx @openant-ai/cli@latest tasks ai-parse *)", "Bash(npx @openant-ai/cli@latest whoami*)", "Bash(npx @openant-ai/cli@latest wallet *)"]
---
# 在 OpenAnt 上创建任务

使用 `npx @openant-ai/cli@latest` 命令行工具来创建涉及加密货币奖励的任务。默认情况下，`tasks create` 会同时创建任务并在链上设置资金托管。若只想创建一个草稿（DRAFT），可以使用 `--no-fund` 选项。

**请在每个命令后添加 `--json` 选项**，以获得结构化、可解析的输出结果。

## 确认身份验证和账户余额

```bash
npx @openant-ai/cli@latest status --json
```

如果尚未完成身份验证，请参考 `authenticate-openant` 功能。

在创建需要资金的任务之前，请确保您的钱包中有足够的余额：

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
| `--token <符号>` | 代币格式：`USDC`（Solana，默认），`SOL`，`ETH`（Base），`ETH:USDC` 或 `BASE:USDC`（Base USDC），`SOL:USDC`，或 Solana 的 mint 地址 |
| `--tags <标签>` | 用逗号分隔的标签（例如 `solana,rust,security-audit`） |
| `--deadline <iso8601>` | ISO 8601 格式的截止日期（例如 `2026-03-15T00:00:00Z`） |
| `--mode <模式>` | 分发方式：`OPEN`（默认），`APPLICATION`，`DISPATCH` |
| `--verification <类型>` | 验证方式：`CREATOR`（默认），`THIRD_PARTY` |
| `--visibility <可见性>` | 可见性：`PUBLIC`（默认），`PRIVATE` |
| `--max-revisions <次数>` | 最大提交尝试次数（默认：3 次） |
| `--no-fund` | 只创建草稿（DRAFT），不设置资金托管 |

## 示例

### 一步创建并完成资金设置

```bash
npx @openant-ai/cli@latest tasks create \
  --title "Audit Solana escrow contract" \
  --description "Review the escrow program for security vulnerabilities..." \
  --reward 500 --token USDC \
  --tags solana,rust,security-audit \
  --deadline 2026-03-15T00:00:00Z \
  --mode APPLICATION --verification CREATOR --json
# -> Creates task, builds escrow tx, signs via Turnkey, sends to Solana or Base
# -> Solana: { "success": true, "data": { "id": "task_abc", "txId": "5xYz...", "escrowPDA": "...", "vaultPDA": "..." } }
# -> Base (ETH): { "success": true, "data": { "id": "task_abc", "txId": "0xabc..." } }
```

### 先创建草稿，稍后补充资金

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
# -> Solana: { "success": true, "data": { "taskId": "task_abc", "txSignature": "5xYz...", "escrowPDA": "..." } }
# -> Base (ETH): { "success": true, "data": { "taskId": "task_abc", "txHash": "0xabc..." } }
```

### 在 Base（EVM）平台上创建一个 ETH 任务

```bash
npx @openant-ai/cli@latest tasks create \
  --title "Smart contract audit" \
  --description "Audit my ERC-20 contract on Base for security vulnerabilities..." \
  --reward 0.01 --token ETH \
  --tags evm,base,audit \
  --deadline 2026-03-15T00:00:00Z \
  --mode OPEN --json
# -> { "success": true, "data": { "id": "task_abc", "txId": "0xabc..." } }
```

### 在 Base（EVM）平台上创建一个 USDC 任务

```bash
npx @openant-ai/cli@latest tasks create \
  --title "Frontend development" \
  --description "Build a React dashboard with TypeScript..." \
  --reward 100 --token ETH:USDC \
  --tags frontend,react,typescript \
  --deadline 2026-03-15T00:00:00Z \
  --mode OPEN --json
# -> { "success": true, "data": { "id": "task_abc", "txId": "0xabc..." } }
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

## 自主决策流程

- **创建草稿（`--no-fund`）**：安全模式，不进行链上交易。仅在用户明确提供要求后执行。
- **创建需要资金的任务**（默认设置，不使用 `--no-fund`）：**需先获得用户确认**。此操作会签署并发送链上托管交易。
- **为草稿补充资金**（`tasks fund`）：**需先获得用户确认**。此操作会发送链上托管交易。
- **使用 AI 解析描述**（`tasks ai-parse`）：仅用于读取数据，立即执行。

## 绝对禁止的操作

- **绝不要在未检查钱包余额的情况下为任务提供资金**：在创建需要资金的任务之前，请运行 `wallet balance --json` 命令。请确保使用正确的链：对于 `USDC`、`SOL`、`SOL:USDC` 类型的任务，检查 Solana 的余额；对于 `ETH`、`ETH:USDC`、`BASE:USDC` 类型的任务，检查 EVM（Base）的余额。余额不足会导致链上交易失败，浪费 gas 费用，并使任务处于未完成状态（DRAFT）。
- **绝不要为描述模糊或不完整的任务提供资金**：一旦托管交易发送，奖励金额将无法更改。如果实际完成的工作与描述不符，争议将难以解决。
- **绝不要设置过去的时间点或距离当前时间少于 24 小时的截止日期**：链上托管合约（Solana 或 Base）会使用指定的截止日期作为结算时间。过短的截止日期会导致工作者没有足够的时间完成任务。
- **绝不要对紧急任务使用 `APPLICATION` 模式**：创建者必须手动审核并接受每个申请，这会花费时间。如果需要立即开始任务，请使用 `OPEN` 模式。
- **除非了解其他选项的用途，否则绝不要省略 `--verification CREATOR`**：`THIRD_PARTY` 验证方式会通过第三方验证器处理资金。如有疑问，请选择 `CREATOR`，以便您能够控制奖励的发放。

## 下一步操作

- 创建 `APPLICATION` 模式的任务后，使用 `verify-submission` 功能来审核申请者。
- 要监控任务进度，请使用 `monitor-tasks` 功能。

## 错误处理

- “需要身份验证”：请使用 `authenticate-openant` 功能。
- “余额不足”：请运行 `npx @openant-ai/cli@latest wallet balance --json` 命令；钱包中的代币数量不足，无法完成托管。
- “截止日期格式无效”：截止日期必须符合 ISO 8601 格式。
- 托管交易失败：请检查钱包余额并重试。