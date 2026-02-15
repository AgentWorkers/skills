---
name: autonomous-agent
description: CornerStone MCP x402技能专为代理人设计，提供股票预测、回测、银行账户关联以及代理人/借款人信用评分等功能。该技能包含支付保护机制（如`run_prediction`、`run_backtest`、`link_bank_account`、`get_agent_reputation_score`、`get_borrower_score`等），并支持通过电子邮件发送结果。其核心流程基于Aptos和Base平台实现，能够处理从“402”状态到“支付”状态再到“重试”状态的整个流程。此外，该技能还支持钱包认证功能，便于代理人在市场上自主下载和使用。
metadata: {"clawdbot":{"emoji":"📈","homepage":"https://github.com/FinTechTonic/autonomous-agent","requires":{"bins":["node","npm"]}}}
---

# CornerStone MCP x402 技能（适用于代理）

此技能为代理提供了一组工具，用于：创建和管理 Aptos 与 EVM 钱包、查询余额，以及调用 x402 支付的费用型 MCP 工具（如股票预测、回测、银行链接、代理/借款者评分）。**支付过程是自动完成的**——当付费工具返回 402 状态码时，该技能会自动完成签名、验证、结算并重新尝试。用户只需调用相应的工具，即可获取结果。

---

## 快速入门工作流程

首次使用时，请按照以下顺序操作，之后可以直接使用所需的工具：

1. **查询钱包地址** → 调用 `get_wallet_addresses`（无需参数）。
2. **如果钱包为空** → 先调用 `create_aptos_wallet`，再调用 `create_evm_wallet`。
3. **充值** → 调用 `credit_aptos_wallet`（Aptos 水龙头）和 `fund_evm_wallet`（EVM 水龙头）。
4. **告知用户将返回的地址添加到白名单**：[https://arnstein.ch/flow.html](https://arnstein.ch/flow.html)。
5. **查询余额** → 调用 `balance_aptos`（进行股票预测/回测时需要 USDC）和/或 `balance_evm`（进行银行链接时需要 ETH）。
6. **使用付费工具** → 调用 `run_prediction`、`run_backtest`、`link_bank_account` 或评分工具。

> **重要提示：** 如果地址尚未充值或未添加到白名单，付费工具会失败。请务必先验证钱包余额。

---

## 工具参考

### 钱包管理工具（本地）

#### `get_wallet_addresses`
- **参数：** 无
- **返回值：** `{ aptos: [{ address, network }], evm: [{ address, network }] }` — 可能为空数组。
- **使用场景：** 在执行任何钱包或付费工具操作之前必须先调用此函数。用于确定钱包是否存在及类型。
- **处理方式：** 如果两个数组都为空 → 创建新的钱包；如果只有一个数组为空 → 创建缺失的类型；如果两个数组都有记录 → 继续进行余额查询或使用付费工具。

#### `create_aptos_wallet`
- **参数：** `{ force?: boolean, network?: "testnet" | "mainnet" }` — 默认值：force=false, network=testnet。
- **返回值：** `{ success, address, network, message }` 或 `{ success: false, message, addresses }`（如果钱包已存在且 force 为 false）。
- **使用场景：** 当 `get_wallet_addresses` 返回空的 aptos 数组时，或用户请求创建新钱包时。
- **错误处理：** 如果 `success` 为 false 且钱包已存在，可以选择使用现有钱包，或设置 `force: true` 重新尝试创建。

#### `create_evm_wallet`
- **参数：** `{ force?: boolean, network?: "testnet" | "mainnet" }` — 默认值：force=false, network=testnet。
- **返回值：** `{ success, address, network, message }` 或 `{ success: false, message, addresses }`。
- **与 create_aptos_wallet 的用法相同。**

#### `credit_aptos_wallet`
- **参数：** `{ amount_octas?: number }` — 默认值：100,000,000（等于 1 APT）。
- **在 devnet 上的返回值：** `{ success: true, address }`（表示钱包已通过编程方式充值）。
- **在 testnet 上的返回值：** `{ success: true, address, faucet_url }`（仅提供充值链接，无编程充值功能）。
- **前提条件：** 必须先创建 Aptos 钱包（使用 `create_aptos_wallet`）。
- **注意：** 充值的 APT 用于支付交易手续费；工具费用为 USDC（约 6 美分）。用户可能需要单独获取 testnet 的 USDC。

#### `fund_evm_wallet`
- **参数：** 无
- **返回值：** `{ success: true, address, faucet_url, message }`（提供手动充值说明）。
- **前提条件：** 必须先创建 EVM 钱包（使用 `create_evm_wallet`）。
- **注意：** 返回的是 Base Sepolia 水龙头的充值链接；用户需手动充值。

### 余额查询工具（本地）

#### `balance_aptos`
- **参数：** 无
- **返回值：** `{ address, balances: { usdc, apt } }` 或 `{ error }`。
- **使用场景：** 在调用 `run_prediction`、`run_backtest` 或评分工具之前，确认钱包中有足够的 USDC。

#### `balance_evm`
- **参数：** `{ chain?: string }` — 默认值：`base`。支持的链包括：`base`, `baseSepolia`, `ethereum`, `polygon`, `arbitrum`, `optimism`。
- **返回值：** `{ address, chain, balance, symbol }` 或 `{ error }`。
- **使用场景：** 在调用 `link_bank_account` 之前，确认钱包中有足够的 ETH（用于 Base Sepolia 链）。
- **注意：** 对于 testnet 工具，使用 `chain: "baseSepolia"`。

### 支付型 MCP 工具（x402 — 支付自动处理）

> 所有付费工具都支持 Aptos 和 EVM 两种支付方式。该技能会自动选择最佳支付方式，或按照预设的 `PREFERRED_payment_ORDER` 进行支付。用户不会收到 402 错误信息，只需调用工具即可获取结果或错误提示。

#### `run_prediction`
- **参数：** `{ symbol: string, horizon?: number }` — `symbol` 表示股票代码（例如 "AAPL"），`horizon` 表示预测周期（默认为 30 天）。
- **返回值：** 预测结果对象（包含预测数据、置信区间等）或 `{ error }`。
- **费用：** 约 6 美分（Aptos 或 EVM 钱包）。
- **前提条件：** 钱包已充值且添加到白名单。

#### `run_backtest`
- **参数：** `{ symbol: string, startDate?: string, endDate?: string, strategy?: string }` — 日期格式为 "YYYY-MM-DD"，默认策略为 "chronos"。
- **返回值：** 回测结果（包括回报、回撤率等）或 `{ error }`。
- **费用：** 约 6 美分。
- **示例调用：** `run_backtest({ symbol: "TSLA", startDate: "2024-01-01", endDate: "2024-12-31", strategy: "chronos" }`

#### `link_bank_account`
- **参数：** 无
- **返回值：** `{ link_token }`（用于 Plaid 银行链接的令牌）或 `{ error }`。
- **费用：** 约 5 美分（EVM/Base 链）。
- **前提条件：** 钱包已充值且添加到白名单（testnet 使用 Base Sepolia 链）。

#### `get_agent_reputation_score`
- **参数：** `{ agent_address?: string, payer_wallet?: string }` — 两个参数均为可选；如省略则使用配置的默认钱包。
- **返回值：** `{ reputation_score: number }`（例如 100 分）；如果地址未添加到白名单则返回 403；或 `{ error }`。
- **费用：** 通过 x402 收费约 6 美分，或使用借款者信用额度免费获取。

#### `get_borrower_score`
- **参数：** `{ agent_address?: string, payer_wallet?: string }` — 参数相同。
- **返回值：** `{ score: number }`（基础分为 100 分；银行链接后分数更高）或 `{ error }`。
- **费用：** 通过 x402 收费约 6 美分，或使用借款者信用额度免费获取。

#### `get_agent_reputation_score_by_email`
- **参数：** `{ email: string, payer_wallet?: string }` — 根据邮箱地址查找对应的代理。
- **返回值：** `{ reputation_score: number }` 或 `{ error }`。
- **前提条件：** 服务器必须启用 `SCORE_BY_EMAIL_ENABLED` 功能。此功能费用较高。

#### `get_borrower_score_by_email`
- **参数：** `{ email: string, payer_wallet?: string }` — 参数相同。
- **返回值：** `{ score: number }` 或 `{ error }`。
- **前提条件：** 服务器必须启用 `SCORE_BY_EMAIL_ENABLED` 功能。此功能费用较高。

---

## 常见任务的处理流程

### “为 X 运行预测”
```
get_wallet_addresses
  → aptos empty? → create_aptos_wallet → credit_aptos_wallet → tell user to whitelist
  → aptos exists? → balance_aptos
    → has USDC? → run_prediction({ symbol: "X", horizon: 30 })
    → no USDC? → tell user to fund USDC, provide address
```

### “链接银行账户”
```
get_wallet_addresses
  → evm empty? → create_evm_wallet → fund_evm_wallet → tell user to whitelist
  → evm exists? → balance_evm({ chain: "baseSepolia" })
    → has ETH? → link_bank_account
    → no ETH? → fund_evm_wallet (returns faucet URL)
```

### “获取我的评分”
```
get_wallet_addresses
  → has aptos or evm? → get_agent_reputation_score + get_borrower_score
  → neither? → create wallets first, whitelist, then query
```

---

## 错误处理

| 错误类型 | 原因 | 处理方法 |
|--------------|---------|------------|
| “没有 Aptos 钱包” | 缺少 Aptos 钱包文件 | 调用 `create_aptos_wallet` |
| “没有 EVM 钱包” | 缺少 EVM 钱包文件 | 调用 `create_evm_wallet` |
| “钱包已存在。使用 force: true” | 钱包存在但无需覆盖 | 使用现有钱包，或设置 `force: true` 重新创建 |
| “支付验证失败” | 账户余额不足或资产类型错误 | 检查余额；提示用户充值钱包 |
| “未配置 Aptos 钱包” / “未配置 EVM 钱包” | 需要的钱包类型不存在 | 创建缺失的钱包 |
| “不支持的链” | `balance_evm` 使用的链名无效 | 使用 `base`, `baseSepolia`, `ethereum`, `polygon`, `arbitrum`, `optimism` 其中的一种 |
| “超时（300 秒后）” | MCP 调用耗时过长 | 重试一次；可能是服务器负载过高 |
| “403” 或 “未添加到白名单” | 钱包未添加到白名单 | 提示用户将地址添加到白名单：[https://arnstein.ch/flow.html](https://arnstein.ch/flow.html) |

---

## 安装说明（适用于手动安装此技能的用户）

1. **安装：** 从仓库根目录执行 `npm install`。将 `.env.example` 文件复制到 `.env` 文件中。
2. **配置：** 设置钱包路径（`APTOS_WALLET_PATH`, `EVM_WALLET_PATH` 或 `EVM_PRIVATE_KEY`）。
3. **创建钱包：** 使用工具（`create_aptos_wallet`, `create_evm_wallet`）或 CLI（`node src/setup-aptos.js`, `node src/setup.js`）进行操作。完成后，将所有地址添加到白名单：[https://arnstein.ch/flow.html](https://arnstein.ch/flow.html)。

---

## CLI 命令（从仓库根目录执行）

| 功能 | 命令 |
|------|--------|
| 生成 Aptos 钱包 | `npm run setup:aptos` |
| 生成 EVM 钱包 | `npm run setup` |
| 显示钱包地址 | `npm run addresses` |
- **在 devnet 上充值 Aptos 钱包** | `npm run credit:aptos`（设置 `APTOS_FAUCET_NETWORK=devnet`） |
- **查询 EVM 钱包余额** | `npm run balance -- <chain>` |
- **转账 ETH/代币** | `npm run transfer -- <chain> <to> <amount> [tokenAddress]` |
- **交换代币（Odos）** | `npm run swap -- <chain> <fromToken> <toToken> <amount>` |
- **运行技能演示** | `npx cornerstone-agent "Run a 30-day prediction for AAPL"` |
- **验证 Aptos 钱包** | `npm run attest:aptos` |
- **验证 EVM 钱包** | `npm run attest:evm` |

---

**来源：** [FinTechTonic/autonomous-agent](https://github.com/FinTechTonic/autonomous-agent)