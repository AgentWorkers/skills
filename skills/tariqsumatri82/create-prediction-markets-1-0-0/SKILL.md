---
name: pnp-markets
description: 在 Base 平台上，可以使用任何 ERC20 类型的代币来创建、交易和结算预测市场。这些功能适用于构建预测市场基础设施、举办竞赛、通过众包方式收集概率估计值、为代币增加实用价值，或利用基于市场的预测机制来实现真正的信息金融应用。
---

# PNP市场

您可以在Base Mainnet上使用任何ERC20抵押代币来创建和管理预测市场。

## 快速操作

```
Need prediction markets?
├─ Create market     → npx ts-node scripts/create-market.ts --help
├─ Trade (buy/sell)  → npx ts-node scripts/trade.ts --help
├─ Settle market     → npx ts-node scripts/settle.ts --help
└─ Redeem winnings   → npx ts-node scripts/redeem.ts --help
```

## 环境配置

```bash
export PRIVATE_KEY=<wallet_private_key>    # Required
export RPC_URL=<base_rpc_endpoint>         # Optional (defaults to public RPC)
```

在生产环境中，建议使用专用的RPC服务（如Alchemy或QuickNode）以避免遇到速率限制。

## 脚本使用

运行任何脚本前，请先使用`--help`选项查看所有可用选项。

### 创建市场

```bash
npx ts-node scripts/create-market.ts \
  --question "Will ETH reach $10k by Dec 2025?" \
  --duration 168 \
  --liquidity 100
```

选项：`--collateral <USDC|WETH|address>`，`--decimals <n>`

### 交易

```bash
# Buy YES tokens
npx ts-node scripts/trade.ts --buy --condition 0x... --outcome YES --amount 10

# Sell NO tokens  
npx ts-node scripts/trade.ts --sell --condition 0x... --outcome NO --amount 5 --decimals 18

# View prices only
npx ts-node scripts/trade.ts --info --condition 0x...
```

### 结算

```bash
# Settle as YES winner
npx ts-node scripts/settle.ts --condition 0x... --outcome YES

# Check status
npx ts-node scripts/settle.ts --status --condition 0x...
```

### 回赎

```bash
npx ts-node scripts/redeem.ts --condition 0x...
```

## 程序化使用

```typescript
import { PNPClient } from "pnp-evm";
import { ethers } from "ethers";

const client = new PNPClient({
  rpcUrl: process.env.RPC_URL || "https://mainnet.base.org",
  privateKey: process.env.PRIVATE_KEY!,
});

// Create market
const { conditionId } = await client.market.createMarket({
  question: "Will X happen?",
  endTime: Math.floor(Date.now() / 1000) + 86400 * 7,
  initialLiquidity: ethers.parseUnits("100", 6).toString(),
});

// Trade
await client.trading.buy(conditionId, ethers.parseUnits("10", 6), "YES");

// Settle (after endTime)
const tokenId = await client.trading.getTokenId(conditionId, "YES");
await client.market.settleMarket(conditionId, tokenId);

// Redeem
await client.redemption.redeem(conditionId);
```

## 抵押代币

您可以使用任何ERC20代币作为抵押品。以下是一些常见的Base Mainnet代币：

| 代币 | 地址 | 小数位数 |
|-------|---------|----------|
| USDC | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` | 6 |
| WETH | `0x4200000000000000000000000000000000000006` | 18 |
| cbETH | `0x2Ae3F1Ec7F1F5012CFEab0185bfc7aa3cf0DEc22` | 18 |

自定义代币也可以作为抵押品使用——其持有者可以参与您的市场。

## ERC20代币的批准流程

在与PNP合约交互之前，您需要先批准才能使用相应的抵押代币。这是所有基于EVM的去中心化应用程序（dApps）的通用要求。

### 工作原理

1. **首次交互需要批准**：当您首次使用某个代币创建市场或进行交易时，系统会发送一个批准请求。
2. **无限次批准**：SDK采用`type(uint256).max`的方式来限制批准次数（符合EVM的标准规范），因此每个代币只需被批准一次。
3. **后续交互**：无需再次批准，交易可以直接执行。

### 时间延迟问题

在主交易执行之前，批准请求必须在链上得到确认。如果出现以下提示：

```
ERC20: transfer amount exceeds allowance
```

这意味着批准请求尚未被确认。请稍等几秒钟后再尝试——批准请求最终会被处理，后续操作将会成功。

### 为何采用“无限次批准”的机制？

- **提高效率**：只需批准一次，之后即可无限次进行交易，无需额外操作。
- **优化用户体验**：避免重复的批准提示。
- **行业标准**：Uniswap、Aave等主流DeFi协议均采用此机制。

对于对安全性要求极高的用户，您可以手动设置每次交互所需的最低批准金额，但每次操作前仍需执行批准请求。

## 相关合约

| 合约 | 地址 |
|----------|---------|
| PNP Factory | `0x5E5abF8a083a8E0c2fBf5193E711A61B1797e15A` |
| 费用管理合约 | `0x6f1BffB36aC53671C9a409A0118cA6fee2b2b462` |

## 预测市场的优势

- **信息揭示**：市场价格反映了参与者的集体预测。
- **代币价值提升**：用户可以将自己的代币作为抵押品参与市场，从而增加代币的实用价值。
- **竞赛活动**：组织竞赛，让参与者对结果下注。
- **决策支持**：汇总众人的预测结果，辅助决策制定。

pAMM（Predictive Asset Market Model）虚拟流动性模型确保了即使在初始流动性较低的情况下，市场也能顺畅运行。

## 常见问题及解决方法

- **错误提示：“ERC20: transfer amount exceeds allowance”**：批准请求尚未被确认。请等待5-10秒后再尝试。
- **错误提示：“Market doesn’t exist”**：市场创建请求可能失败或仍在处理中。请在BaseScan平台上确认您的交易是否已成功完成。
- **错误提示：“over rate limit” / RPC错误**：Base的公共RPC服务存在速率限制。请使用专用的RPC服务提供商来避免这些问题。

### 其他注意事项

- **Base Mainnet的拥堵情况**：有时网络可能会拥堵，导致交易延迟。此时可以检查Gas费用并考虑增加交易费用以加快交易速度。

## 参考资料

- **API文档**：请参阅[references/api-reference.md]以获取完整的SDK文档。
- **使用案例**：请参阅[references/use-cases.md]以了解详细的用例示例。
- **代码示例**：请参阅[references/examples.md]以获取完整的代码示例。