---
name: autonomous-agent
description: CreditNexus x402代理：适用于用户需要股票预测、回测、银行账户关联或代理/借款人评分的场景。该代理提供了受支付保护的MCP工具（包括`run_prediction`、`run_backtest`、`link_bank_account`、`get_agent_reputation_score`、`get_borrower_score`等），这些工具均基于x402流程（Aptos + Base）进行操作。代理能够自动处理支付、重试等流程，并支持钱包认证（签名）以完成用户注册流程。
metadata: {"openclaw":{"emoji":"📈","homepage":"https://github.com/FinTechTonic/autonomous-agent","requires":{"bins":["node","npm"]},"primaryEnv":"MCP_SERVER_URL","skillKey":"autonomous-agent"},"clawdbot":{"emoji":"📈","homepage":"https://github.com/FinTechTonic/autonomous-agent","requires":{"bins":["node","npm"]}}}
---

# CreditNexus x402 代理技能

这是一个自主代理，用于调用受 x402 保护的 MCP 工具：股票预测、回测、银行账户关联以及代理/借款人的信用评分。该代理负责处理支付流程（从 x402 到支付，然后使用 `payment_payload` 重新尝试支付），并与 Aptos（用于预测/回测）和 Base（用于银行相关操作）进行交互。此外，该代理还支持 **钱包认证**（签名）功能，以完成用户注册流程（通过 POST 请求发送到 `/attest/aptos` 或 `/attest/evm`）。

## 安装

当从 **autonomous-agent** 仓库加载此技能时，仓库的根目录将成为技能文件夹 `{baseDir}` 的父目录。请从仓库根目录克隆并安装该技能：

```bash
# From repository root (parent of {baseDir} when using this repo)
git clone https://github.com/FinTechTonic/autonomous-agent.git && cd autonomous-agent
npm install
```

请将 `MCP_SERVER_URL` 设置为您的 MCP 服务器地址（例如 `https://borrower.replit.app`）。将 `.env.example` 文件复制到 `.env` 文件，并设置以下参数：
- `MCP_SERVER_URL` – MCP 服务器的基地址（MCP 协议位于 `/mcp`）
- `X402_FACILITATOR_URL` – x402 代理的地址（用于验证/结算）
- `LLM_BASE_URL`、`HUGGINGFACE_API_KEY` 或 `HF_TOKEN`、`LLM_MODEL` – 用于推理
- `APTOS_WALLET_PATH`、`EVM_WALLET_PATH`（或 `EVM_PRIVATE_KEY`） – 用于支付操作

## 运行代理

从 **仓库根目录**（包含 `package.json` 和 `src/` 文件的目录）开始运行代理：

```bash
npx cornerstone-agent "Run a 30-day prediction for AAPL"
# Or interactive
npx cornerstone-agent
# Or from repo: npm run agent -- "..." or node src/run-agent.js "..."
```

**x402 流程：** 代理在没有 `payment_payload` 的情况下调用相关工具 → 服务器返回 402 错误代码及支付要求 → 代理进行签名，随后由 x402 代理的验证/结算机构进行处理 → 代理再次尝试支付，并接收支付结果及 `paymentReceipt`。

## 钱包认证（签名）

为了在用户注册过程中证明钱包的所有权，请从仓库根目录运行以下命令：
- 对于 Aptos：`npm run attest:aptos` 或 `npx cornerstone-agent-attest-aptos` — 结果将发送到 POST 请求 `/attest/aptos`
- 对于 EVM：`npm run attest:evm` 或 `npx cornerstone-agent-attest-evm` — 结果将发送到 POST 请求 `/attest/evm`

## MCP 工具

所有相关工具均位于 MCP 服务器的 `/mcp` 目录下。有关资源和使用费用的信息，请参阅 [MCP_INTEGRATION_REFERENCE.md](https://github.com/FinTechTonic/autonomous-agent/blob/main/MCP_INTEGRATION_REFERENCE.md) 文档。

| 工具          | 资源路径        | 描述                                      | 费用                |
|----------------|------------------|-----------------------------------------|-------------------|
| `run_prediction`    | `/mcp/prediction/{symbol}`    | 股票预测（股票代码、预测时间范围）                        | 约 6 美分            |
| `run_backtest`    | `/mcp/backtest/{symbol}`    | 回测（股票代码、开始/结束时间、策略）                        | 约 6 美分            |
| `link_bank_account`    | `/mcp/banking/link`     | 关联银行账户（使用 CornerStone/Plaid 服务）                   | 约 5 美分（根据配置而定）       |
| `get_agent_reputation_score` | `/mcp/scores/reputation` | 代理信用评分（基于 100 分；可能涉及 x402 或贷款机构的信用评分）      | 约 6 美分            |
| `get_borrower_score`    | `/mcp/scores/borrower`    | 借款人信用评分（基于 100 分或 Plaid 服务的评分）                  | 约 6 美分            |
| `get_agent_reputation_score_by_email` | `/mcp/scores/reputation-by-email` | 根据电子邮件地址获取代理信用评分（需启用 SCORE_BY_EMAIL 功能）       | 基础费用 + 额外费用        |
| `get_borrower_score_by_email` | `/mcp/scores/borrower-by-email` | 根据电子邮件地址获取借款人信用评分（需启用 SCORE_BY_EMAIL 功能）       | 基础费用 + 额外费用        |

请在用户注册流程中将您的代理添加到白名单中（例如通过访问 `MCP_SERVER_URL/flow.html`），以便服务器允许您的钱包进行支付操作。