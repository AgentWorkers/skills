---
name: autonomous-agent
description: CornerStone MCP x402技能专为代理人设计，提供股票预测、回测、银行数据对接以及代理人/借款人信用评分等功能。该技能基于Aptos和Base平台，采用了x402支付流程，具备支付保护机制。它能够处理从“402”状态到“支付”状态再到“重试”状态的整个流程，并支持钱包认证以完成新代理人的入职流程。适用于代理人能够自主下载和使用此类技能的市场平台。
metadata: {"openclaw":{"emoji":"📈","homepage":"https://github.com/FinTechTonic/autonomous-agent","requires":{"bins":["node","npm"]},"primaryEnv":"MCP_SERVER_URL","skillKey":"autonomous-agent"},"clawdbot":{"emoji":"📈","homepage":"https://github.com/FinTechTonic/autonomous-agent","requires":{"bins":["node","npm"]}}}
---

# CornerStone MCP x402 技能（适用于代理）

该技能为代理提供了调用受 x402 保护的 MCP 端点的工具，包括股票预测、回测、银行账户关联以及代理/借款人的信用评分等功能。**支付过程是自动化的**——该技能会透明地处理从请求到验证、结算再到重试的整个流程。同时，该技能还支持 **钱包认证**（签名）功能，用于新用户的注册（使用 POST 请求到 `/attest/aptos` 或 `/attest/evm`）。

## 安装

克隆或复制该代码仓库。当从 OpenClaw/MoltBook 加载该技能时，技能文件所在的文件夹位于 `{baseDir}`；请在代码仓库的根目录下执行相关命令（即 `adapters/openclaw` 或 `skills/autonomous-agent` 的父目录）。

```bash
git clone https://github.com/FinTechTonic/autonomous-agent.git && cd autonomous-agent
npm install
```

将 `.env.example` 文件复制到 `.env` 文件，并设置以下参数：

- `X402_FACILITATOR_URL`：x402 服务的验证/结算接口地址
- `LLM_BASE_URL`、`HUGGINGFACE_API_KEY` 或 `HF_TOKEN`、`LLM_MODEL`：用于推理的 LLM 服务相关信息
- `APTOS_WALLET_PATH`、`EVM_WALLET_PATH`（或 `EVM_PRIVATE_KEY`）：用于支付的钱包地址

## 快速启动工作流程

1. `get_wallet_addresses()`：查询现有的钱包地址。
2. 如果钱包为空：执行 `create_aptos_wallet()` 和 `create_evm_wallet()`。
3. 为钱包充值：执行 `credit_aptos_wallet()` 和 `fund_evm_wallet()`。
4. 将地址添加到白名单中（地址列表请参考：https://arnstein.ch/flow.html）。
5. 查询钱包余额：执行 `balance_aptos()` 和 `balance_evm({ chain: "baseSepolia" })`。
6. 调用相应的工具：`run_prediction`、`run_backtest`、`link_bank_account` 或其他评分工具。

## 运行该技能（演示）

```bash
npx cornerstone-agent "Run a 30-day prediction for AAPL"
npx cornerstone-agent
npm run agent -- "..."
node src/run-agent.js "..."
```

## 钱包认证（签名）

- Aptos：使用 `npm run attest:aptos` 或 `npx cornerstone-agent-attest-aptos` 命令进行认证；认证结果将发送到 POST 请求地址 `/attest/aptos`。
- EVM：使用 `npm run attest:evm` 或 `npx cornerstone-agent-attest-evm` 命令进行认证；认证结果将发送到 POST 请求地址 `/attest/evm`。

## 工具参考

### 本地钱包相关工具

| 工具 | 参数 | 返回值 |
|------|------|---------|
| `get_wallet_addresses` | 无 | `[{ aptos: [{ address, network }], evm: [...] }]` |
| `create_aptos_wallet` | `{ force?, network? }` | `{ success, address, network }` |
| `create_evm_wallet` | `{ force?, network? }` | `{ success, address, network }` |
| `credit_aptos_wallet` | `{ amount_octas? }` | 在 devnet 网络中直接充值；在 testnet 网络中返回 faucet_url 和地址 |
| `fund_evm_wallet` | 无 | `{ faucet_url, address, message }` |
| `balance_aptos` | 无 | `{ address, balances: { usdc, apt } }` |
| `balance_evm` | `{ chain? }` | `{ address, chain, balance, symbol }` |

### 支付型 MCP 工具（x402，支付过程自动化）

| 工具 | 参数 | 返回值 | 费用 |
|------|------|---------|------|
| `run_prediction` | `{ symbol, horizon? }` | 预测数据 | 约 6 美分 |
| `run_backtest` | `{ symbol, startDate?, endDate?, strategy? }` | 性能指标 | 约 6 美分 |
| `link_bank_account` | 无 | `{ link_token }` | 约 5 美分 |
| `get_agent_reputation_score` | `{ agent_address?, payer_wallet? }` | 代理的信用评分 | 约 6 美分或相应数量的代币 |
| `get_borrower_score` | `{ agent_address?, payer_wallet? }` | 借款人的信用评分 | 约 6 美分或相应数量的代币 |
| `get_agent_reputation_score_by_email` | `{ email, payer_wallet? }` | 通过电子邮件查询代理的信用评分 | 更高费用 |
| `get_borrower_score_by_email` | `{ email, payer_wallet? }` | 通过电子邮件查询借款人的信用评分 | 更高费用 |

请将代理使用的钱包地址添加到白名单（地址列表请参考：https://arnstein.ch/flow.html），以便服务器允许这些钱包进行交易。