---
name: autonomous-agent
description: CornerStone MCP x402：专为代理人设计的工具。该工具支持股票预测、回测、银行数据对接以及代理人/借款人的信用评分功能。它采用了支付保护机制（基于Aptos和Base技术），能够处理从“402”状态到“支付”状态再到“重试”状态的整个流程。此外，该工具还支持钱包认证功能，便于新代理人的入职流程。适用于代理人能够自主下载并使用这些工具的市场平台。
metadata: {"openclaw":{"emoji":"📈","homepage":"https://github.com/FinTechTonic/autonomous-agent","requires":{"bins":["node","npm"]},"primaryEnv":"MCP_SERVER_URL","skillKey":"autonomous-agent"},"clawdbot":{"emoji":"📈","homepage":"https://github.com/FinTechTonic/autonomous-agent","requires":{"bins":["node","npm"]}}}
---

# CornerStone MCP x402 技能（适用于代理）

该技能为代理提供了调用受 x402 保护的 MCP 端点的工具，包括股票预测、回测、银行账户关联以及代理/借款人的信用评分等功能。支付过程是自动完成的——该技能会透明地处理从请求到验证、结算再到重试的整个流程。同时，该技能支持钱包认证（signing）功能，用于新用户注册（通过 POST 请求发送到 `/attest/aptos` 或 `/attest/evm`）。

## 安装

当从 `autonomous-agent` 仓库加载此技能时，仓库的根目录即为技能文件夹 `{baseDir}` 的父目录。请从仓库根目录进行克隆和安装：

```bash
git clone https://github.com/FinTechTonic/autonomous-agent.git && cd autonomous-agent
npm install
```

将 `.env.example` 文件复制到 `.env` 文件，并设置以下参数：
- `X402_FACILITATOR_URL`
- `LLM_BASE_URL`、`HUGGINGFACE_API_KEY` 或 `HF_TOKEN`、`LLM_MODEL`（用于推理）
- `APTOS_WALLET_PATH`、`EVM_WALLET_PATH`（或 `EVM_PRIVATE_KEY`）（用于支付）

## 快速启动工作流程

1. `get_wallet_addresses()`：检查现有的钱包地址。
2. 如果钱包地址为空：执行 `create_aptos_wallet()` 和 `create_evm_wallet()`。
3. 充值钱包：执行 `credit_aptos_wallet()` 和 `fund_evm_wallet()`。
4. 将地址添加到白名单中（地址列表请参考：https://arnstein.ch/sse/flow.html）。
5. 查看钱包余额：执行 `balance_aptos()` 和 `balance_evm({ chain: "baseSepolia" })`。
6. 调用相应的工具：`run_prediction`、`run_backtest`、`link_bank_account` 或 `score`。

## 运行该技能（演示）

```bash
npx cornerstone-agent "Run a 30-day prediction for AAPL"
npx cornerstone-agent
npm run agent -- "..."
node src/run-agent.js "..."
```

## 钱包认证（signing）

- Aptos：`npm run attest:aptos` 或 `npx cornerstone-agent-attest-aptos` — 输出结果发送到 POST /attest/aptos
- EVM：`npm run attest:evm` 或 `npx cornerstone-agent-attest-evm` — 输出结果发送到 POST /attest/evm

## 工具参考

### 本地钱包工具

| 工具 | 参数 | 返回值 |
|------|------|---------|
| `get_wallet_addresses` | 无 | `{ aptos: [{ address, network }], evm: [...] }` |
| `create_aptos_wallet` | `{ force?, network? }` | `{ success, address, network }` |
| `create_evm_wallet` | `{ force?, network? }` | `{ success, address, network }` |
| `credit_aptos_wallet` | `{ amount_octas? }` | 在 devnet 上直接充值；在 testnet 上：返回 faucet_url 和地址 |
| `fund_evm_wallet` | 无 | `{ faucet_url, address, message }` |
| `balance_aptos` | 无 | `{ address, balances: { usdc, apt } }` |
| `balance_evm` | `{ chain? }` | `{ address, chain, balance, symbol }` |

### 支付型 MCP 工具（x402 — 支付自动完成）

| 工具 | 参数 | 返回值 | 费用 |
|------|------|---------|------|
| `run_prediction` | `{ symbol, horizon? }` | 预测数据 | 约 6 美分 |
| `run_backtest` | `{ symbol, startDate?, endDate?, strategy? }` | 性能指标 | 约 6 美分 |
| `link_bank_account` | 无 | `{ link_token }` | 约 5 美分 |
| `get_agent_reputation_score` | `{ agent_address?, payer_wallet? }` | `{ reputation_score }` | 约 6 美分或相应金额的信用 |
| `get_borrower_score` | `{ agent_address?, payer_wallet? }` | `{ score }` | 约 6 美分或相应金额的信用 |
| `get_agent_reputation_score_by_email` | `{ email, payer_wallet? }` | `{ reputation_score }` | 约 6 美分 |
| `get_borrower_score_by_email` | `{ email, payer_wallet? }` | `{ score }` | 约 6 美分 |

请将代理使用的钱包地址添加到白名单（地址列表请参考：https://arnstein.ch/sse/flow.html），以便服务器允许这些钱包进行操作。