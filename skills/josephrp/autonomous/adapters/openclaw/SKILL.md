---
name: autonomous-agent
description: CreditNexus x402 代理：适用于用户需要股票预测、回测、银行账户关联或代理/借款人评分的场景。该代理提供了受支付保护的功能（如 `run_prediction`、`run_backtest`、`link_bank_account`、`get_agent_reputation_score`、`get_borrower_score` 等），并支持通过电子邮件发送结果。它遵循 x402 流程（Aptos + Base）进行操作。代理能够自动处理支付请求并重试失败的操作。此外，还支持钱包认证（签名）功能，以便用户顺利完成账户注册流程。
metadata: {"openclaw":{"emoji":"📈","homepage":"https://github.com/FinTechTonic/autonomous-agent","requires":{"bins":["node","npm"]},"primaryEnv":"MCP_SERVER_URL","skillKey":"autonomous-agent"},"clawdbot":{"emoji":"📈","homepage":"https://github.com/FinTechTonic/autonomous-agent","requires":{"bins":["node","npm"]}}}
---

# CreditNexus x402 代理技能

这是一个自主运行的代理，用于调用受 x402 协议保护的 MCP 工具，这些工具包括股票预测、回测、银行账户关联以及代理/借款人的信用评分服务。该代理负责处理支付流程（从用户到支付系统的交互），并与 Aptos（用于预测和回测）和 Base（用于银行相关操作）系统进行交互。此外，该代理还支持 **钱包认证**（签名）功能，以完成用户注册流程（通过 POST 请求发送到 `/attest/aptos` 或 `/attest/evm`）。

## 安装

克隆或复制该仓库。当从 OpenClaw/MoltBook 中加载该代理技能时，技能文件所在的文件夹为 `{baseDir}`；请在仓库的 **根目录**（`adapters/openclaw` 或 `skills/autonomous-agent` 的上级目录）下执行相关命令。

```bash
# From repository root
git clone https://github.com/FinTechTonic/autonomous-agent.git && cd autonomous-agent
npm install
```

请将 `MCP_SERVER_URL` 设置为您的 MCP 服务器地址（例如：`https://borrower.replit.app`）。将 `.env.example` 文件复制到 `.env` 文件，并设置以下参数：
- `MCP_SERVER_URL`：MCP 服务器的基地址（MCP 协议接口位于 `/mcp`）
- `X402_FACILITATOR_URL`：x402 服务的协调/结算接口
- `LLM_BASE_URL`、`HUGGINGFACE_API_KEY` 或 `HF_TOKEN`、`LLM_MODEL`：用于智能合约推理的参数
- `APTOS_WALLET_PATH`、`EVM_WALLET_PATH`（或 `EVM_PRIVATE_KEY`）：用于支付操作的参数

## 运行代理

请从仓库的 **根目录**（包含 `package.json` 和 `src/` 文件的目录）开始执行以下命令：

```bash
npx cornerstone-agent "Run a 30-day prediction for AAPL"
# Or interactive
npx cornerstone-agent
# Or from repo: npm run agent -- "..." or node src/run-agent.js "..."
```

**x402 流程：**
- 代理在没有 `payment_payload` 的情况下调用相关工具 → 服务器返回错误代码 402 以及支付所需的详细信息 → 代理进行签名操作 → 协调方进行验证/结算 → 代理再次尝试调用工具并附带 `payment_payload` → 接收到处理结果及支付确认信息（`paymentReceipt`）

## 钱包认证（签名）

为了在用户注册过程中证明钱包的所有权，请在仓库根目录下执行以下命令：
- 对于 Aptos 系统：`npm run attest:aptos` 或 `npx cornerstone-agent-attest-aptos` — 结果将发送到 POST 请求地址 `/attest/aptos`
- 对于 EVM 系统：`npm run attest:evm` 或 `npx cornerstone-agent-attest-evm` — 结果将发送到 POST 请求地址 `/attest/evm`

## MCP 工具

所有相关工具均位于 MCP 服务器的 `/mcp` 目录下。有关详细信息及费用标准，请参考仓库中的 [MCP_INTEGRATION_REFERENCE.md](https://github.com/FinTechTonic/autonomous-agent/blob/main/MCP_INTEGRATION_REFERENCE.md) 文件。

| 工具          | 所需资源            | 功能描述                                      | 费用                |
|-----------------|------------------|----------------------------------|-------------------|
| `run_prediction`    | `/mcp/prediction/{symbol}`    | 股票预测（股票代码、预测周期）                        | 约 6 美分            |
| `run_backtest`    | `/mcp/backtest/{symbol}`    | 股票回测（股票代码、开始时间/结束时间、策略）                | 约 6 美分            |
| `link_bank_account`    | `/mcp/banking/link`      | 银行账户关联服务                              | 约 5 美分（根据配置而定）       |
| `get_agent_reputation_score` | `/mcp/scores/reputation`    | 代理信用评分（基于 100 分的评分标准；涉及 x402 或贷款机构信用评估） | 约 6 美分            |
| `get_borrower_score`    | `/mcp/scores/borrower`    | 借款人信用评分（基于 100 分或 Plaid 评分标准；涉及 x402 或贷款机构信用评估） | 约 6 美分            |
| `get_agent_reputation_score_by_email` | `/mcp/scores/reputation-by-email` | 基于电子邮件地址的代理信用评分（需启用 `SCORE_BY_EMAIL` 功能） | 基础费用 + 额外费用        |
| `get_borrower_score_by_email` | `/mcp/scores/borrower-by-email` | 基于电子邮件地址的借款人信用评分（需启用 `SCORE_BY_EMAIL` 功能） | 基础费用 + 额外费用        |

请在用户注册流程中将该代理添加到白名单中（例如：`MCP_SERVER_URL/flow.html`），以便服务器允许使用您的钱包进行支付操作。