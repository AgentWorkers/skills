---
name: autonomous-agent
description: **CreditNexus x402 代理**  
适用于用户需要股票预测、回测、银行账户关联或代理/借款人评分的场景。该代理提供了受支付保护的 MCP 工具（`run_prediction`、`run_backtest`、`link_bank_account`、`get_agent_reputation_score`、`get_borrower_score` 等），并支持通过电子邮件发送结果（`by-email` 变体）。整个流程基于 Aptos 和 Base 平台实现。代理能够自动处理用户请求（如提交预测、执行回测、关联银行账户等），并在遇到问题时自动重试。此外，该代理还支持钱包认证（signing）功能，以完成用户注册流程。
metadata: {"clawdbot":{"emoji":"📈","homepage":"https://github.com/FinTechTonic/autonomous-agent","requires":{"bins":["node","npm"]}}}
---

# CreditNexus x402 代理技能

该代理能够自动创建、充值并使用 Aptos 和 EVM 钱包，并调用由 x402 支付的 MCP 工具（如股票预测、回测、银行账户链接、代理/借款人评分等）。它负责处理支付流程（从 x402 支付到完成支付），并使用 Aptos 和 Base 平台进行操作。此外，该代理还支持钱包的认证（签名）功能，以便用户完成注册流程。适用于需要设置钱包、充值、查看余额、进行股票预测、回测、链接银行账户、获取评分或执行代币操作的场景。

## 安装

从仓库根目录克隆并安装相关依赖：

```bash
git clone https://github.com/FinTechTonic/autonomous-agent.git && cd autonomous-agent
npm install
```

将 `MCP_SERVER_URL` 设置为您的 x402 MCP 服务器地址（例如 `https://borrower.replit.app` 或 `https://arnstein.ch`），然后将 `.env.example` 文件复制到 `.env` 文件中，并配置 LLM（大型语言模型）和钱包的路径。

---

## 可执行的任务

### 钱包管理

- **创建 Aptos 钱包**：`create_aptos_wallet`（可选参数 `network: "testnet"` 或 `"mainnet"`）。代理可以拥有多个 Aptos 钱包。
- **创建 EVM 钱包**：`create_evm_wallet`（可选参数 `network: "testnet"` 或 `"mainnet"`）。代理可以拥有多个 EVM 钱包。
- **列出钱包地址**：`get_wallet_addresses` 可返回所有 Aptos 和 EVM 钱包地址（附带网络标签），用于白名单管理和充值操作。

### 充值钱包

- **为 Aptos 钱包充值**：`credit_aptos_wallet`（在 devnet 上使用程序化充值方式；在 testnet 上返回充值指令和 Aptos 充值地址）。此操作用于 `run_prediction` 和 `run_backtest` 等功能（费用约为 6 美分）。
- **为 EVM 钱包充值**：`fund_evm_wallet`（返回充值地址和所需信息；例如使用 Base Sepolia 充值平台，费用约为 3.65 美元）。

用户必须在注册流程中为每个代理地址添加到白名单中（例如通过 `http://localhost:4024/flow.html` 或您的 MCP 服务器的注册页面），才能成功使用付费工具。

### 查看余额

- **Aptos 钱包余额**：`balance_aptos`（以 USDC 为单位）。
- **EVM 钱包余额**：`balance_evm`（以链上的原生代币为单位，如 base、baseSepolia、ethereum 等）。

### 支付型 MCP 工具（x402）

- **股票预测**：`run_prediction`（输入股票代码和预测期限，费用约为 6 美分）。
- **回测**：`run_backtest`（输入交易策略，费用约为 6 美分）。
- **银行账户链接**：`link_bank_account`（使用 CornerStone/Plaid 平台，费用约为 5 美元，具体价格可配置）。
- **评分**：`get_agent_reputation_score`、`get_borrower_score`（按钱包或电子邮件查询）；`get_agent_reputation_score_by_email`、`get_borrower_score_by_email`（在启用 SCORE_BY_EMAIL 功能时可用）。

该代理会自动处理 x402 支付请求：验证 → 结算 → 如需重试则再次发起支付（并附带签名信息）。

### 命令行接口（CLI）

| 任务 | 命令                |
|------|-------------------|
| 创建 Aptos 钱包 | `npm run setup:aptos`       |
| 创建 EVM 钱包 | `npm run setup`         |
| 查看白名单地址 | `npm run addresses`        |
| 为 Aptos 钱包充值（devnet） | `npm run credit:aptos`       |
| 查看 EVM 余额 | `npm run balance -- <chain>`       |
| 转移 ETH/代币 | `npm run transfer -- <chain> <to> <amount> [tokenAddress]` |
| 交换代币（Odos） | `npm run swap -- <chain> <fromToken> <toToken> <amount>` |
| 运行代理 | `npx cornerstone-agent "Run a 30-day prediction for AAPL"` | 或 `npx cornerstone-agent`（交互式命令）；也可以通过 `npm run agent -- "..."` 运行代理 |
| 验证 Aptos 钱包 | `npm run attest:aptos`       | 或 `npx cornerstone-agent-attest-aptos` |
| 验证 EVM 钱包 | `npm run attest:evm`       | 或 `npx cornerstone-agent-attest-evm` |

---

## 使用场景

当用户需要执行以下操作时，请使用此代理技能：

- 创建或使用 Aptos 或 EVM 钱包（测试网或主网）。
- 为代理钱包充值（使用充值指令或程序化方式）。
- 查看 Aptos 或 EVM 钱包余额。
- 运行股票预测或回测（费用通过 Aptos 支付）。
- 链接银行账户（费用通过 Base 平台支付）。
- 获取代理/借款人的评分（按钱包或电子邮件查询）。
- 为注册流程生成钱包认证文件（使用 `attest:aptos` 或 `attest:evm`）。
- 通过 CLI 或其他方式从代理钱包转移或交换代币。

---

## 设置步骤

1. **安装依赖**：从仓库根目录执行 `npm install`，并将 `.env.example` 文件复制到 `.env` 文件中。
2. **配置参数**：设置 `MCP_SERVER_URL`、`X402_FACILITATOR_URL`、`HUGGINGFACE_API_KEY`（或 `HF_TOKEN`）、LLM 模型以及钱包路径（`APTOS_WALLET_PATH`、`EVM_WALLET_PATH` 或 `EVM_PRIVATE_KEY`）。
3. **创建钱包**：通过代理工具（`create_aptos_wallet`、`create_evm_wallet`）或 CLI（`node src/setup-aptos.js`、`node src/setup.js`）来创建钱包，并在 MCP 服务器的注册页面（如 `/flow.html`）完成所有地址的充值和白名单设置。

---

## 运行代理

从仓库根目录（包含 `package.json` 和 `src/` 目录的位置）运行代理：

```bash
npx cornerstone-agent "Create an Aptos wallet, then run a 30-day prediction for AAPL"
# Or interactive
npx cornerstone-agent
# Or from repo: npm run agent -- "..." or node src/run-agent.js "..."
```

**来源代码链接：** [FinTechTonic/autonomous-agent](https://github.com/FinTechTonic/autonomous-agent)