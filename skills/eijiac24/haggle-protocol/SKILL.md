---
name: haggle-protocol
description: 用于AI代理的链上谈判协议：该协议支持在Base Mainnet上使用真实的USDC进行交易创建、谈判和结算；同时，也支持在Solana/Monad/Arbitrum测试网络上使用测试代币进行交易操作。
homepage: https://haggle.dev
user-invocable: true
metadata: {"clawdbot": {"category": "crypto", "tags": ["negotiation", "defi", "base", "solana", "ai-agents", "usdc"]}, "requires": {"env": ["HAGGLE_PRIVATE_KEY"]}, "credentials": ["HAGGLE_PRIVATE_KEY"]}
files: ["scripts/*"]
---

# Haggle 协议

> 这是首个用于自主 AI 代理的链上谈判协议。

Haggle 协议允许两个 AI 代理通过多轮交替报价以及基于时间衰减的机制来协商出一个公平的价格。与固定价格不同，代理们通过动态议价来发现公平的价格。

**适用场景：** 当你需要从另一个代理那里购买或出售服务，但不知道公平价格时。

## 部署环境

| 链路 | 网络 | 合同地址 | 代币 |
|-------|---------|----------|-------|
| Base | **主网** | `0xB77B5E932de5e5c6Ad34CB4862E33CD634045514` | USDC (`0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`) |
| Solana | 开发网 | `DRXGcVHj1GZSc7wD4LTnrM8RJ1shWH93s1zKCXtJtGbq` | SPL 代币 |
| Monad | 测试网 | `0x30FD25bAB859D8D68de6A0719983bb75200b1CeC` | MockERC20 |
| Base | Sepolia | `0x30FD25bAB859D8D68de6A0719983bb75200b1CeC` | MockERC20 |
| Arbitrum | Sepolia | `0x30FD25bAB859D8D68de6A0719983bb75200b1CeC` | MockERC20 |

你可以在各自的区块链浏览器中独立验证这些合同地址：
- Base 主网：https://basescan.org/address/0xB77B5E932de5e5c6Ad34CB4862E33CD634045514
- Solana 开发网：https://explorer.solana.com/address/DRXGcVHj1GZSc7wD4LTnrM8RJ1shWH93s1zKCXtJtGbq?cluster=devnet

## 工作原理

```
1. Buyer deposits escrow (USDC) into protocol-controlled vault
2. Seller accepts the negotiation invitation
3. Both parties submit alternating offers (turn-based, enforced on-chain)
4. Each round, escrow decays by a configurable rate, creating time pressure
5. Either party accepts the counterparty's offer -> settlement and payout
```

## 设置

### 选项 1：MCP 服务器（推荐）

安装 MCP 服务器以实现代理的全面集成：

```bash
npm install -g @haggle-protocol/mcp@0.2.0
```

使用你的私钥进行配置（详见下方的“私钥安全”部分）：

```bash
export HAGGLE_PRIVATE_KEY="0x..."   # EVM private key
```

运行：

```bash
npx @haggle-protocol/mcp@0.2.0
```

### 选项 2：TypeScript SDK

```bash
npm install @haggle-protocol/evm@0.1.0    # For Base/Monad/Arbitrum
npm install @haggle-protocol/solana@0.1.0  # For Solana
npm install @haggle-protocol/core@0.1.0    # Shared types
```

### 选项 3：REST API

```bash
npx @haggle-protocol/api@0.1.0
```

## 私钥安全

使用此功能需要 `HAGGLE_PRIVATE_KEY` 来签署链上交易。这是一个敏感的凭证，请遵循以下安全建议：

1. **使用专用钱包** - 为代理操作创建一个单独的钱包，切勿使用你的主钱包。
2. **仅存入最低所需金额** - 只存入你计划用于谈判的金额（例如，几枚 USDC 加上交易手续费）。
3. **仅批准所需金额** - 调用 `approve()` 函数时，仅批准实际需要的托管金额，不要批准无限额。
4. **先在测试网上测试** - 在使用主网之前，使用 `base_sepolia` 或 `monad_testnet` 和 MockERC20 代币进行测试。
5. **监控钱包** - 定期检查你的代理钱包在 https://basescan.org 上是否有异常交易。
6. **定期更换密钥** - 如果怀疑账户被入侵，立即转移资金并生成新密钥。

私钥从环境变量中加载，不会被该功能记录、传输或存储。所有签名操作都在本地通过 ethers.js 完成。你可以在 https://github.com/haggle-protocol 查看源代码。

## 买家流程（Base 主网）

```typescript
import { HaggleEVM } from "@haggle-protocol/evm";
import { ethers } from "ethers";

const provider = new ethers.JsonRpcProvider("https://mainnet.base.org");
const wallet = new ethers.Wallet(process.env.HAGGLE_PRIVATE_KEY, provider);
const haggle = new HaggleEVM("base_mainnet", wallet);

// 1. Approve USDC (approve only what you need)
const USDC = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913";
const usdc = new ethers.Contract(USDC, [
  "function approve(address,uint256) returns (bool)"
], wallet);
await (await usdc.approve(haggle.contractAddress, 1000000n)).wait(); // 1 USDC

// 2. Create negotiation
const negId = await haggle.createNegotiation({
  seller: "0xSELLER_ADDRESS",
  escrowAmount: 1000000n,      // 1 USDC (6 decimals)
  tokenAddress: USDC,
  serviceHash: ethers.keccak256(ethers.toUtf8Bytes("data analysis")),
  maxRounds: 6,
  decayRateBps: 200,           // 2% decay per round
  responseWindow: 300,         // 5 min per turn
  globalDeadlineSeconds: 1800, // 30 min total
  minOfferBps: 1000,           // min 10% of escrow
});

// 3. Submit offer
await haggle.submitOffer(negId, 500000n); // Offer 0.5 USDC
```

## 卖家流程

```typescript
// 1. Accept invitation
await haggle.acceptInvitation(negId);

// 2. Counter-offer
await haggle.submitOffer(negId, 800000n); // Counter at 0.8 USDC

// 3. Accept buyer's offer (triggers settlement)
await haggle.acceptOffer(negId);
```

## 查看谈判状态

```typescript
const neg = await haggle.getNegotiation(negId);

console.log("Status:", neg.status);
console.log("Round:", neg.currentRound);
console.log("Current Offer:", ethers.formatUnits(neg.currentOfferAmount, 6), "USDC");
console.log("Effective Escrow:", ethers.formatUnits(neg.effectiveEscrow, 6), "USDC");
```

## MCP 服务器工具

使用 MCP 服务器时，可以使用以下工具：

| 工具 | 功能描述 |
|------|-------------|
| `create_negotiation` | 创建一个新的带有托管存款的谈判 |
| `get_negotiation` | 通过 ID 查看谈判状态 |
| `submit_offer` | 提交报价（遵循轮流顺序） |
| `accept_offer` | 接受对方的报价，触发结算 |
| `reject_negotiation` | 放弃谈判，将托管资金退还给买家 |
| `get_protocol_config` | 查看协议配置 |
| `list_chains` | 列出所有支持的链路 |

## 关键参数

| 参数 | 描述 |
|-----------|-------------|
| `escrowAmount` | 买家存入的托管总额（以最小单位计） |
| `maxRounds` | 谈判的最大轮数 |
| `decayRateBps` | 每轮托管资金的衰减率（以基点计算，200 = 2%） |
| `responseWindow` | 双方每轮的响应时间（秒） |
| `globalDeadlineSeconds` | 谈判的总截止时间（秒） |
| `minOfferBps` | 最低报价比例（以有效托管资金的百分比计算，1000 = 10%） |

## 结算计算公式

```
protocolFee    = settledAmount * 50 / 10000  (0.5%)
sellerReceives = settledAmount - protocolFee
buyerRefund    = effectiveEscrow - settledAmount
```

## 谈判策略建议

1. **从合理的报价开始** - 以一个积极但合理的初始报价开始谈判。
2. **逐步让步** - 小幅让步可以显示你的诚意。
3. **关注托管资金的衰减** - 每轮谈判都会消耗托管资金。
4. **监控有效托管金额** - 随着托管资金减少，可接受的报价范围也会缩小。

## 外部端点

该功能通过以下 RPC 端点发送和读取区块链交易数据：

| 端点 | 发送的数据 | 功能 |
|----------|-----------|---------|
| `https://mainnet.base.org` | 签名的交易记录 | Base 主网 RPC |
| `https://sepolia.base.org` | 签名的交易记录 | Base Sepolia RPC |
| `https://api.devnet.solana.com` | 签名的交易记录 | Solana 开发网 RPC |
| `https://monad-testnet.drpc.org` | 签名的交易记录 | Monad 测试网 RPC |
| `https://sepolia-rollup.arbitrum.io/rpc` | 签名的交易记录 | Arbitrum Sepolia RPC |
| `https://registry.npmjs.org` | 包元数据 | 仅用于安装（设置阶段） |

不会向其他任何端点发送数据。该功能不进行任何数据分析、跟踪或监控。

## 安全性与隐私

- **仅本地签名** - 所有交易都在本地使用 ethers.js 进行签名，私钥不会离开你的设备。
- **无数据传输** - 不会向第三方分析、跟踪或日志服务发送任何数据。
- **开源代码** - 所有智能合约和 SDK 代码均可在 https://github.com/haggle-protocol 公开审计。
- **仅接受数值报价** - 所有报价均为 uint256 类型，避免输入文本带来的安全风险。
- **托管资金由合约控制** - 资金存储在链上合约的托管账户中，任何一方都无法恶意撤资。
- **轮流报价机制** | 链上逻辑确保报价按顺序进行，不允许提前提交。
- **自动终止** - 谈判到期后任何人都可以进行结算，避免资金滞留。
- **协议所有者可暂停** | 协议所有者可在紧急情况下暂停合约。
- **未经审计** - 智能合约尚未经过正式审计，使用前请自行承担风险，并建议从小额金额开始测试。

## 链接

- 官网：https://haggle.dev
- GitHub 仓库：https://github.com/haggle-protocol
- Base 仪表板：https://haggle.dev/base
- npm：https://www.npmjs.com/org/haggle-protocol
- BaseScan：https://basescan.org/address/0xB77B5E932de5e5c6Ad34CB4862E33CD634045514