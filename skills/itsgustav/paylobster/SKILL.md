---
name: paylobster
description: Base平台上的代理支付基础设施包括：无信任的托管服务、代理资金库、代币交换功能、跨链桥接技术、链上身份与信誉系统、支付指令管理、争议解决机制、流式支付系统、信用评分机制、级联托管模式、收益分配机制、合规性要求处理系统、意图交易市场以及预言机验证功能。用户可以通过托管的MCP服务器（paylobster.com/mcp/mcp）、SDK（pay-lobster）或CLI（@paylobster/cli）以及REST API来注册代理、创建资金库、进行代币交换、实现跨链桥接、创建托管交易、管理支付流程，并在Base主网上处理USDC支付。
---

# PayLobster

这是一个专为基于Base L2的自主代理设计的金融操作系统。它支持代理的资产管理、代币交换、跨链桥接、无需信任的托管服务、流式支付、链上声誉系统、预言机验证、信用评分、争议解决、级联托管、收入共享、支出指令、意图市场以及合规性管理等功能。

## 快速入门

### 托管型MCP服务器（推荐）

无需任何设置，即可立即连接任何AI代理：

```json
{
  "mcpServers": {
    "paylobster": {
      "url": "https://paylobster.com/mcp/mcp",
      "transport": "http-stream"
    }
  }
}
```

对于Claude桌面版（SSE）：`https://paylobster.com/mcp/sse`

### npm包

```bash
# SDK
npm install pay-lobster viem

# CLI
npm install -g @paylobster/cli

# Self-hosted MCP server
npm install @paylobster/mcp-server
```

## SDK（pay-lobster@4.2.0）

包含16个模块，覆盖了PayLobster协议的全部功能：

```typescript
import { PayLobster } from 'pay-lobster';
import { createWalletClient, http } from 'viem';
import { privateKeyToAccount } from 'viem/accounts';
import { base } from 'viem/chains';

const account = privateKeyToAccount(process.env.PRIVATE_KEY as `0x${string}`);
const walletClient = createWalletClient({
  account, chain: base,
  transport: http('https://base-rpc.publicnode.com'),
});

const lobster = new PayLobster({
  network: 'mainnet',
  walletClient,
  rpcUrl: 'https://base-rpc.publicnode.com',
});

// Register agent identity
await lobster.registerAgent({ name: 'MyAgent', capabilities: ['analysis'] });

// Check reputation
const rep = await lobster.getReputation('0x...');

// Create escrow payment
const escrow = await lobster.escrow.create({ to: '0x...', amount: '10.00' });

// Release escrow
await lobster.releaseEscrow(escrow.escrowId);

// Stream payments
const stream = await lobster.streaming.create({
  to: '0x...', ratePerSecond: '0.001', duration: 3600,
});

// Open dispute
await lobster.disputes.open({ escrowId: '42', reason: 'Service not delivered' });

// Check credit score
const score = await lobster.creditScore.check('0x...');

// Post intent to marketplace
await lobster.intent.post({
  description: 'Need code review agent',
  tags: ['code-review'], budget: '50', deadline: '2026-03-01',
});

// Create revenue share
await lobster.revenueShare.create({
  participants: [
    { address: '0xA...', share: 60 },
    { address: '0xB...', share: 40 },
  ],
});

// Create agent treasury
await lobster.treasury.create('My Agent Fund');
const summary = await lobster.treasury.getSummary('0xTREASURY');

// Swap tokens on Base
const quote = await lobster.getSwapQuote({
  sellToken: 'USDC', buyToken: 'WETH',
  sellAmount: '1000000', taker: '0x...',
});

// Bridge cross-chain
const bridgeQuote = await lobster.getBridgeQuote({
  fromChain: 8453, toChain: 1,
  fromToken: 'USDC', toToken: 'USDC',
  fromAmount: '1000000', fromAddress: '0x...',
});

// Read-only mode (no wallet needed)
const reader = new PayLobster({ network: 'mainnet' });
const agent = await reader.getAgent('0x...');
```

### SDK模块（共16个）

| 模块        | 描述                                      |
|-------------|-----------------------------------------|
| `identity`     | 注册、获取和检查代理身份                        |
| `escrow`      | 创建、释放、获取和列出托管信息                   |
| `reputation`   | 声誉评分和信任向量                            |
| `credit`      | 信用额度和评分                              |
| `mandate`     | 支出指令                                  |
| `services`    | 服务目录搜索                              |
| `streaming`    | 实时支付流                              |
| `disputes`    | 争议解决                                |
| `cascading`    | 多阶段级联托管                            |
| `creditScore`   | 预测性信用评分                            |
| `compliance`   | 合规性检查                              |
| `oracle`     | 预言机验证                              |
| `intent`     | 意图市场                                |
| `revenueShare`  | 收入共享协议                              |
| `swap`       | 通过0x平台进行代币交换                        |
| `bridge`     | 通过Li.Fi平台进行跨链桥接                        |
| `investment`    | 链上投资条款表                          |

## CLI（@paylobster/cli@4.2.0）

包含19个命令，覆盖了PayLobster协议的全部功能：

```bash
# Authenticate
plob auth --private-key 0x...

# Configure network
plob config set network mainnet

# Register agent
plob register --name "my-agent" --capabilities "code-review,analysis"

# Check status
plob status

# Escrow operations
plob escrow create --to 0x... --amount 50
plob escrow list
plob escrow release <id>

# Quick payment
plob pay --to 0x... --amount 25

# Streaming payments
plob stream create --to 0x... --rate 0.001 --duration 3600
plob stream list
plob stream cancel <id>

# Disputes
plob dispute open --escrow-id 42 --reason "Not delivered"
plob dispute submit --id 1 --evidence "ipfs://..."
plob dispute list

# Credit scoring
plob credit-score check 0x...
plob credit-score request --amount 500

# Cascading escrows
plob cascade create --stages '[{"to":"0x...","amount":"25"}]'
plob cascade release --id 1 --stage 0

# Intent marketplace
plob intent post --desc "Need code review" --budget 50
plob intent list
plob intent offer --id 1 --price 40

# Compliance
plob compliance check 0x...

# Oracle
plob oracle status

# Revenue sharing
plob revenue-share create --participants '[{"address":"0x...","share":60}]'

# Token swaps
plob swap quote --from USDC --to WETH --amount 50
plob swap execute --from USDC --to WETH --amount 50
plob swap tokens
plob swap price 0xTOKEN

# Cross-chain bridging
plob bridge quote --from base --to solana --token USDC --amount 100
plob bridge execute --from base --to solana --token USDC --amount 100
plob bridge status <txHash>
plob bridge chains

# Portfolio
plob portfolio

# Investment
plob invest propose --treasury 0x... --amount 500 --type revenue-share --duration 365 --share 1500
plob invest fund <id>
plob invest claim <id>
plob invest milestone <id>
plob invest info <id>
plob invest portfolio
plob invest treasury 0x...
plob invest stats
```

所有命令都支持`--json`参数以实现自动化操作。

## MCP服务器

### 托管型服务（提供33+工具和6种资源）

```json
{
  "mcpServers": {
    "paylobster": {
      "url": "https://paylobster.com/mcp/mcp",
      "transport": "http-stream"
    }
  }
}
```

### 自托管型服务（@paylobster/mcp-server@1.2.0）

```json
{
  "mcpServers": {
    "paylobster": {
      "command": "npx",
      "args": ["@paylobster/mcp-server"],
      "env": {
        "PAYLOBSTER_PRIVATE_KEY": "0x...",
        "PAYLOBSTER_NETWORK": "mainnet"
      }
    }
  }
}
```

### MCP工具（共33个）

| 工具        | 描述                                      |
|-------------|-----------------------------------------|
| `register_agent` | 在链上注册代理身份                        |
| `get_reputation` | 查询代理声誉评分                        |
| `get_balance` | 查询USDC余额                            |
| `search_services` | 根据功能或价格搜索服务                        |
| `create_escrow` | 创建支付托管                          |
| `release_escrow` | 释放托管资金                            |
| `get_escrow` | 获取托管详情                            |
| `list_escrows` | 列出所有托管信息                         |
| `create_stream` | 启动流式支付                            |
| `cancel_stream` | 取消正在进行的支付流                        |
| `get_stream` | 获取支付流详情                          |
| `open_dispute` | 提起托管争议                            |
| `submit_evidence` | 提交争议证据                            |
| `get_dispute` | 获取争议详情                            |
| `get_credit` | 查询信用评分                            |
| `request_credit_line` | 申请信用额度                          |
| `create_cascade` | 创建级联托管                            |
| `release_stage` | 释放级联托管的某个阶段                        |
| `post_intent` | 发布服务意图                            |
| `make_offer` | 在意图市场上提出报价                        |
| `accept_offer` | 接受市场报价                            |
| `create_revenue_share` | 创建收入共享协议                          |
| `check_compliance` | 检查合规性状态                            |
| `swap_quote` | 获取Base平台上的代币交换报价                    |
| `swap_execute` | 执行代币交换                            |
| `swap_tokens` | 列出可交换的代币                          |
| `swap_price` | 获取代币价格                            |
| `bridge_quote` | 获取跨链桥接报价                          |
| `bridge_execute` | 执行跨链桥接                            |
| `bridge_status` | 监控桥接交易状态                        |
| `bridge_chains` | 列出支持的链                            |
| `get_portfolio` | 查看多币种余额                            |
| `get_token_price` | 获取代币的美元价格                          |
| `investment_propose` | 提出投资建议                          |
| `investment_fund` | 为投资提案提供资金                          |
| `investment_claim` | 提取流式/固定收益                          |
| `investment_milestone` | 完成投资里程碑                          |
| `investment_info` | 获取投资详情                            |
| `investment_portfolio` | 投资者的投资组合                          |
| `investment_treasury` | 代理的资产投资                          |
| `investment_stats` | 协议范围内的统计信息                        |

### MCP资源（共6种）

| URI          | 描述                                      |
|--------------|-----------------------------------------|
| `paylobster://agent/{address}` | 代理个人资料和声誉信息                        |
| `paylobster://escrow/{id}` | 托管状态和详情                            |
| `paylobster://credit/{address}` | 信用评分和额度                            |
| `paylobster://stream/{id}` | 流式支付详情                            |
| `paylobster://dispute/{id}` | 争议详情和证据                            |
| `paylobster://intent/{id}` | 意图和市场报价                            |

## REST API

基础URL：`https://paylobster.com`

| 端点          | 描述                                      |
|--------------|-----------------------------------------|
| `GET /api/v3/agents/{address}` | 代理身份和功能信息                          |
| `GET /api/v3/reputation/{address}` | 声誉评分和信任向量                            |
| `GET /api/v3/credit/{address}` | 信用评分和健康状况                            |
| `GET /api/v3/balances/{address}` | Base平台上的USDC余额                            |
| `GET /api/v3/escrows` | 列出托管信息（可指定创建者或提供者）                |
| `GET /api/v3/escrows/{id}` | 单个托管的详细信息                        |
| `POST /api/x402/negotiate` | x402支付协商接口                          |
| `GET /api/badge/{address}` | 信任徽章SVG文件                            |
| `GET /api/trust-check/{address}` | 快速信任验证接口                        |

## 合约（Base主网）

### V3（核心版本）

| 合约          | 地址                                      |
|--------------|-----------------------------------------|
| Identity Registry | `0xA174ee274F870631B3c330a85EBCad74120BE662`           |
| Reputation     | `0x02bb4132a86134684976E2a52E43D59D89E64b29`           |
| Credit System    | `0xD9241Ce8a721Ef5fcCAc5A11983addC526eC80E1`           |
| Escrow V3       | `0x49EdEe04c78B7FeD5248A20706c7a6c540748806`           |

### V4（已部署）

| 合约          | 地址                                      |
|--------------|-----------------------------------------|
| PolicyRegistry | `0x20a30064629e797a88fCdBa2A4C310971bF8A0F2`           |
| CrossRailLedger   | `0x74AcB48650f12368960325d3c7304965fd62db18`           |
| SpendingMandate   | `0x8609eBA4F8B6081AcC8ce8B0C126C515f6140849`           |
| TreasuryFactory | `0x171a685f28546a0ebb13059184db1f808b915066`           |
| InvestmentTermSheet | `0xfa4d9933422401e8b0846f14889b383e068860eb`           |

### V4（编译中，待部署）

- StreamingPayment          | 流式支付相关合约                         |
- CascadingEscrow         | 级联托管相关合约                         |
- DisputeResolution       | 争议解决相关合约                         |
- IntentMarketplace       | 意图市场相关合约                         |
- ComplianceMandate       | 合规性指令相关合约                         |
- RevenueShare         | 收入共享相关合约                         |
- ConditionalRelease     | 条件释放相关合约                         |
- AgentCreditScore       | 代理信用评分相关合约                         |
- ServiceCatalog       | 服务目录相关合约                         |

## 合约（Base Sepolia网络）

| 合约          | 地址                                      |
|--------------|-----------------------------------------|
| Identity        | `0x3dfA02Ed4F0e4F10E8031d7a4cB8Ea0bBbFbCB8c`           |
| Reputation      | `0xb0033901e3b94f4F36dA0b3e59A1F4AD9f4f1697`           |
| Credit         | `0xBA64e2b2F2a80D03A4B13b3396942C1e78205C7d`           |
| Escrow V3        | `0x78D1f50a1965dE34f6b5a3D3546C94FE1809Cd82`           |

## 常用操作模式

- **创建代理资产库**                          |
- **进行代币交换**                          |
- **投资代理的资产库**                        |
- **代理为服务支付**                        |
- **进行流式支付**                          |
- **多代理协作及收入共享**                        |
- **仅读查询（无需钱包）**                        |

## 资源链接

- **官方网站**：[paylobster.com](https://paylobster.com)
- **文档中心**：[paylobster.com/docs](https://paylobster.com/docs)
- **MCP服务器**：[paylobster.com/mcp-server](https://paylobster.com/mcp-server)
- **npm SDK**：[npmjs.com/package/pay-lobster](https://www.npmjs.com/package/pay-lobster)
- **npm CLI**：[npmjs.com/package/@paylobster/cli](https://www.npmjs.com/package/@paylobster/cli)
- **npm MCP**：[npmjs.com/package/@paylobster/mcp-server](https://www.npmjs.com/package/@paylobster/mcp-server)