---
name: escrow-agent
description: 在 Solana 和 Base 上构建一种无需信任的第三方托管机制，用于代理之间的交易。当一个 AI 代理需要向另一个代理付款时，该机制可以代为持有资金，直到交易完成并得到验证；或者在链上解决支付纠纷时发挥作用。
---
# EscrowAgent

这是一个用于实现代理间自动交易的去中心化托管协议。代理们可以将资金锁定在链上的托管账户中，定义交易成功的标准，并根据可验证的结果自动完成交易。该协议支持Solana（使用SPL代币）和Base（使用ERC-20代币），并且使用相同的API。

## 适用场景

在以下情况下使用EscrowAgent：

- 一个代理需要向另一个代理支付费用（例如：交换、数据获取、计算服务、API调用）；
- 需要实现去中心化的交易结算——资金在满足条件之前会被锁定，无需中间人；
- 构建代理间的商业合作模式——一个代理雇佣另一个代理并在任务完成后支付费用；
- 需要解决争议——由AI仲裁者自动处理分歧；
- 用户对Solana或Base上的托管服务、代理支付或去中心化交易有疑问。

**不适用场景**：

- 无需任何条件的简单钱包间转账（请使用常规转账方式）；
- 人与人之间的支付（该协议专为自动化代理设计）；
- 不支持Solana或Base以外的区块链。

## 安装

```bash
# Install escrow skills into your AI agent (Cursor, Claude Code, Codex, Copilot, ...)
npx skills add cruellacodes/escrowagent

# TypeScript SDK (core)
npm install escrowagent-sdk@latest

# Agent tools (LangChain, Vercel AI, MCP adapters)
npm install escrowagent-agent-tools@latest

# Or scaffold everything into the project
npx escrowagent@latest init

# Start MCP server for Claude / Cursor
npx escrowagent@latest mcp
```

```bash
# Python SDK
pip install escrowagent-sdk
pip install escrowagent-sdk[base]  # with Base chain support
```

## 核心概念

### 托管流程

所有托管交易都会遵循以下状态机流程（在两个区块链上均相同）：

```
CREATE -> AwaitingProvider
  |-- [cancel]  -> Cancelled (full refund)
  |-- [timeout] -> Expired (full refund)
  +-- [accept]  -> Active
                    |-- [dispute] -> Disputed -> [resolve] -> Resolved
                    |-- [timeout] -> Expired (full refund)
                    +-- [submit_proof] -> ProofSubmitted
                                          |-- [confirm] -> Completed (funds released)
                                          |-- [dispute] -> Disputed
                                          +-- [timeout] -> Expired
```

### 角色

- **客户端（代理A）**：创建托管合约，存入资金，并定义交易任务；
- **提供者（代理B）**：接受任务，执行相关操作，并提交任务完成的证明；
- **仲裁者**（可选）：解决争议。仲裁者可以是AI，也可以是任何地址。

### 费用结构

| 事件 | 协议费用 | 仲裁者费用 | 退款情况 |
|-------|-------------|----------------|--------|
| 任务成功完成 | 0.5% | -- | 提供者获得99.5%的费用 |
| 争议解决 | 0.5% | 1.0% | 按每项裁决结果收费 |
| 取消托管 | 0% | -- | 全额退款 |
| 托管期限到期 | 0% | -- | 全额退款 |

## SDK使用方法

### 初始化客户端

`AgentVault`类为两个区块链提供了统一的API接口：

**Solana：**

```typescript
import { AgentVault, USDC_DEVNET_MINT } from "escrowagent-sdk";
import { Connection, Keypair } from "@solana/web3.js";

const vault = new AgentVault({
  chain: "solana",
  connection: new Connection("https://api.devnet.solana.com"),
  wallet: Keypair.fromSecretKey(Uint8Array.from(JSON.parse(process.env.AGENT_PRIVATE_KEY!))),
  programId: "8rXSN62qT7hb3DkcYrMmi6osPxak7nhXi2cBGDNbh7Py",
});
```

**Base：**

```typescript
import { AgentVault, USDC_BASE } from "escrowagent-sdk";

const vault = new AgentVault({
  chain: "base",
  privateKey: process.env.BASE_PRIVATE_KEY!,       // 0x...
  contractAddress: "0xddBC03546BcFDf55c550F5982BaAEB37202fEB11",
  rpcUrl: "https://mainnet.base.org",
  chainId: 8453,
});
```

**Python：**

```python
from escrowagent import AgentVault

# Solana
vault = AgentVault(chain="solana", rpc_url="https://api.devnet.solana.com", keypair=kp)

# Base
vault = AgentVault(chain="base", rpc_url="https://mainnet.base.org",
                   private_key="0x...", contract_address="0x...")
```

### 完整的托管流程

```typescript
// 1. Client creates escrow
const { escrowAddress } = await vault.createEscrow({
  provider: "ProviderAgentAddress",
  amount: 50_000_000,             // 50 USDC (6 decimals)
  tokenMint: USDC_DEVNET_MINT,   // or USDC_BASE for Base chain
  deadline: Date.now() + 600_000, // 10 minutes
  task: {
    description: "Swap 10 USDC to SOL on Jupiter at best price",
    criteria: [
      { type: "TransactionExecuted", description: "Swap tx confirmed on-chain" },
    ],
  },
  verification: "OnChain",       // or "MultiSigConfirm", "OracleCallback", "AutoRelease"
  arbitrator: "ArbitratorAddress", // optional
});

// 2. Provider accepts the escrow
await vault.acceptEscrow(escrowAddress);

// 3. Provider does the work, then submits proof
await vault.submitProof(escrowAddress, {
  type: "TransactionSignature",  // or "OracleAttestation", "SignedConfirmation"
  data: swapTxSignature,
});

// 4. Client confirms completion -> funds release to provider
await vault.confirmCompletion(escrowAddress);
```

## 其他操作

```typescript
// Cancel (only before provider accepts)
await vault.cancelEscrow(escrowAddress);

// Raise a dispute (freezes funds)
await vault.raiseDispute(escrowAddress, { reason: "Work not completed as specified" });

// Resolve a dispute (arbitrator only)
await vault.resolveDispute(escrowAddress, { type: "PayProvider" });
// or: { type: "PayClient" }
// or: { type: "Split", clientBps: 5000, providerBps: 5000 }

// Query
const info = await vault.getEscrow(escrowAddress);
const escrows = await vault.listEscrows({ status: "AwaitingProvider", limit: 10 });
const stats = await vault.getAgentStats("AgentAddress");
```

## 与代理框架的集成

### LangChain

```typescript
import { createLangChainTools } from "escrowagent-agent-tools";

const tools = createLangChainTools(vault);
const agent = createReactAgent({ llm, tools });
// Agent now has 9 escrow tools it can use autonomously
```

### Vercel AI SDK

```typescript
import { createVercelAITools } from "escrowagent-agent-tools";

const tools = createVercelAITools(vault);
const { text } = await generateText({ model, tools, prompt });
```

### MCP（Claude Desktop / Cursor）

### 配置Claude Desktop（`claude_desktop_config.json`）：

```json
{
  "mcpServers": {
    "escrowagent": {
      "command": "npx",
      "args": ["escrowagent@latest", "mcp"],
      "env": {
        "SOLANA_RPC_URL": "https://api.devnet.solana.com",
        "AGENT_PRIVATE_KEY": "[your,keypair,bytes]"
      }
    }
  }
}
```

## 可用的工具（所有集成方案）

所有代理集成方案都提供以下9种工具：

| 工具 | 功能描述 |
|------|-------------|
| `create_escrow` | 为特定任务创建托管合约，并设置截止日期和成功标准 |
| `accept_escrow` | 作为提供者接受待处理的托管请求 |
| `submit_proof` | 提交任务完成的证明 |
| `confirm_completion` | 确认任务完成并释放资金给提供者 |
| `cancel_escrow` | 在提供者接受之前取消托管（全额退款） |
| `raise_dispute` | 冻结资金，并将争议提交给仲裁者 |
| `get_escrow` | 根据地址查询托管详情 |
| `list_escrows` | 按状态、客户端或提供者筛选托管记录 |
| `get_agent_stats` | 查看代理的信誉、成功率及交易量 |

## 部署地址

### Solana

| 资源 | 地址 |
|----------|---------|
| 程序合约 | `8rXSN62qT7hb3DkcYrMmi6osPxak7nhXi2cBGDNbh7Py`（Devnet） |
| AI仲裁者地址 | `C8xn3TXJXxaKijq3AMMY1k1Su3qdA4cG9z3AMBjfRnfr` |
| USDC（Devnet） | 使用SDK中的`USDC_DEVNET_MINT`地址 |

### Base

| 资源 | 地址 |
|----------|---------|
| 合同地址 | `0xddBC03546BcFDf55c550F5982BaAEB37202fEB11`（[Basescan](https://basescan.org/address/0xddbc03546bcfdf55c550f5982baaeb37202feb11)） |
| AI仲裁者地址 | `0xacB84e5fB127E9B411e8E4Aeb5D59EaE1BF5592e` |
| USDC | 使用SDK中的`USDC_BASE`（Mainnet）或`USDC_BASE_SEPOLIA`（Testnet） |

## 基础设施

| 资源 | 链接地址 |
|----------|-----|
| 官方网站 | https://escrowagent.vercel.app |
| API接口 | https://escrowagent.onrender.com |
| GitHub仓库 | https://github.com/cruellacodes/escrowagent |

## 环境变量设置

| 变量 | 是否必填 | 是否敏感 | 说明 |
|----------|----------|-----------|-------------|
| `BASE_PRIVATE_KEY` | 是（仅针对Base链） | 是 | 用于签署Base链交易的EVM私钥（格式为0x...），请使用专用代理钱包存储 |
| `BASE_RPC_URL` | 否 | 否 | Base链的RPC接口地址，默认为`https://mainnet.base.org` |
| `AGENT_PRIVATE_KEY` | 仅针对Solana链 | 是 | Solana链的私钥字节数组（JSON格式），Base链使用时无需设置 |
| `SOLANA_RPC_URL` | 否 | 否 | Solana链的RPC接口地址，默认为Devnet |
| `BASE_CONTRACT_ADDRESS` | 否 | 否 | Base链合约地址，默认为`0xddBC03546BcFDf55c550F5982BaAEB37202fEB11` |
| `ESCROWAGENT_INDEXER_URL` | 否 | 否 | 用于存储链外数据的索引器API地址 |

**安全提示：**

- 请使用专用代理钱包存储资金（切勿使用主钱包或热钱包）；
- 将私钥存储在环境变量或密钥管理工具中（如AWS Secrets Manager、Vault），切勿直接编码到源代码中；
- 在使用主网和真实资金之前，请先在测试网/Devnet环境中进行测试；
- 为代理钱包设置资金限额，仅投入你能承受的风险金额；
- 对于高价值交易，建议使用硬件钱包或多签名方案；
- 尽可能在隔离环境中（如Docker容器或沙箱环境）运行程序；
- **切勿在日志、错误信息或监控数据中泄露**私钥。

## 代码中的关键类型

在编写与SDK相关的代码时，请注意以下关键类型：

```typescript
type ChainType = "solana" | "base";

type EscrowStatus =
  | "AwaitingProvider" | "Active" | "ProofSubmitted"
  | "Completed" | "Disputed" | "Resolved"
  | "Expired" | "Cancelled";

type VerificationType = "OnChain" | "OracleCallback" | "MultiSigConfirm" | "AutoRelease";
type CriterionType = "TransactionExecuted" | "TokenTransferred" | "PriceThreshold" | "TimeBound" | "Custom";
type ProofType = "TransactionSignature" | "OracleAttestation" | "SignedConfirmation";

type DisputeRuling =
  | { type: "PayClient" }
  | { type: "PayProvider" }
  | { type: "Split"; clientBps: number; providerBps: number };
```

## 重要说明

- 所有金额均以代币的最小单位表示（例如：`50_000_000`表示50个USDC）；
- 两个链上的SDK接口完全相同，仅配置参数有所不同；
- 资金由智能合约管理，不会被任何个人或服务器控制；
- AI仲裁者会以超过70%的置信度自动解决争议；置信度较低的争议会提交给人工审核；
- 该协议尚未经过外部审计，处理大额资金时请谨慎操作；
- 协议费用为0.5%，仲裁者费用为1.0%（仅针对有争议的交易）。