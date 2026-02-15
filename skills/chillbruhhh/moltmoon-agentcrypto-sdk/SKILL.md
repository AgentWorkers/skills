---
name: moltmoon-sdk
description: 完整的 OpenClaw 支持的操作技能，适用于 @moltmoon/sdk V2。当代理需要在 Base 主网上端到端地安装、配置和操作 MoltMoon SDK 或 CLI 时，可使用这些技能，包括启动测试运行、验证元数据和图像、进行实时代币发行、报价检查、买卖交易、领取奖励、数据迁移、故障排除以及执行安全的生产运行流程。
---

# MoltMoon SDK 技能（OpenClaw）- V2

使用此技能可以在 Base 主网上将 MoltMoon SDK/CLI 作为完整的代理工作流程来操作。

## V2 经济系统概述

MoltMoon V2 使用 **MoltTokenV2**（类似 SafeMoon 的反射型代币）以及 **BondingCurveMarketV2** 债券曲线机制：

| 参数 | 值 |
|-----------|-------|
| 总供应量 | 每次发布时为 10 亿枚代币 |
| 买入费用 | 0% |
| 卖出费用 | 5%（1% 归持有人，2% 归创作者，2% 归储备金） |
| 债券曲线分配 | 80% 用于债券曲线，20% 保留给流动性提供者（LP） |
| 虚拟基础价值 | 3,000 美元（USDC） |
| 最低种子资金（普通情况） | 20 美元（USDC） |
| 平台手续费 | 种子资金的 10% 归储备金 |
| 成熟条件 | 当债券曲线上的代币售出达到 95% 时（避免价格无限上涨） |
| 流动性提供者锁定期 | 成熟后，在 Aerodrome 平台上锁定 180 天 |
| 创作者前期收益 | 从债券曲线中获得的收益（上限为 20%） |

**反射机制**：每次卖出操作会触发 1% 的收益重新分配给所有代币持有者（根据 rOwned/tOwned 比例）。4% 的收益会自动转换为 USDC，并在创作者和储备金之间平分。买入操作以及钱包间的转账均免征税费。

**成熟后的操作**：代币在 Aerodrome DEX 上交易后，卖出仍需缴纳税费（通过多 DEX 对接机制进行计算）。流动性提供者的资金将在锁定期内无法取出。

## 安装

请使用以下方法之一进行安装：

```bash
npm install @moltmoon/sdk
```

或者选择不安装直接使用：

```bash
npx -y @moltmoon/sdk moltlaunch --help
```

## 运行时配置

在执行任何写入操作之前，请设置环境变量：

```env
MOLTMOON_API_URL=https://api.moltmoon.ai
MOLTMOON_NETWORK=base
MOLTMOON_PRIVATE_KEY=0x...   # 32-byte hex key with 0x prefix
```

**注意**：
- `MOLTMOON_NETWORK` 仅支持 `base` 网络。
- 发布、买入、卖出和领取操作都需要 `MOLTMOON_PRIVATE_KEY`（或 `PRIVATE_KEY`）。

## 支持的 CLI 命令

**全局选项**：
- `--api-url <url>`  
- `--network base`  
- `--private-key <0x...>`

**命令**：
- `launch`：发布代币（包含元数据、图片和社交信息，包括审批流程）  
- `tokens`：列出所有代币  
- `buy`：审批 USDC 并一次性购买代币  
- `sell`：审批代币并一次性卖出  
- `quote-buy`：仅获取买入报价（免手续费）  
- `quote-sell`：仅获取卖出报价（显示已扣除的 5% 手续费）  
- `rewards-earned`：检查钱包中未领取的 USDC 奖励  
- `rewards-claim`：领取未领取的 USDC 奖励（需要签名者权限）  
- `migration-status`：检查从 V1 到 V2 的迁移状态  
- `migrate`：将 V1 代币迁移到 V2（包括审批和迁移流程）

## 标准的 CLI 运行脚本

### 1) 先进行模拟发布（不进行链上交易）

```bash
npx -y @moltmoon/sdk mltl launch \
  --name "Agent Token" \
  --symbol "AGT" \
  --description "Agent launch token on MoltMoon" \
  --website "https://example.com" \
  --twitter "https://x.com/example" \
  --discord "https://discord.gg/example" \
  --image "./logo.png" \
  --seed 20 \
  --dry-run \
  --json
```

### 2) 正式发布

```bash
npx -y @moltmoon/sdk mltl launch \
  --name "Agent Token" \
  --symbol "AGT" \
  --description "Agent launch token on MoltMoon" \
  --seed 20 \
  --json
```

### 3) 交易流程

```bash
# Buy (0% fee)
npx -y @moltmoon/sdk mltl quote-buy --market 0xMARKET --usdc 1 --json
npx -y @moltmoon/sdk mltl buy --market 0xMARKET --usdc 1 --slippage 500 --json

# Sell (5% fee: 1% reflection + 2% creator + 2% treasury)
npx -y @moltmoon/sdk mltl quote-sell --market 0xMARKET --tokens 100 --json
npx -y @moltmoon/sdk mltl sell --market 0xMARKET --token 0xTOKEN --amount 100 --slippage 500 --json
```

### 4) 奖励流程（$MOLTM 持有者）

```bash
# Check earned USDC rewards
npx -y @moltmoon/sdk mltl rewards-earned --pool 0xPOOL --account 0xWALLET --json

# Claim rewards
npx -y @moltmoon/sdk mltl rewards-claim --pool 0xPOOL --json
```

### 5) 从 V1 迁移到 V2

```bash
# Check migration status
npx -y @moltmoon/sdk mltl migration-status --json

# Migrate tokens (approve + swap)
npx -y @moltmoon/sdk mltl migrate --amount 1000 --json
```

## SDK API 接口

**初始化方法**：
```ts
import { MoltmoonSDK } from '@moltmoon/sdk';

const sdk = new MoltmoonSDK({
  baseUrl: process.env.MOLTMOON_API_URL || 'https://api.moltmoon.ai',
  network: 'base',
  privateKey: process.env.MOLTMOON_PRIVATE_KEY as `0x${string}`,
});
```

**读取方法**：
- `getTokens()`：列出所有已发布的代币  
- `getMarket(marketAddress)`：获取完整市场信息（V2 版本包含 `holderRewardsPool`、`aerodromePool`、`virtualBase`、`liquidityTokens`、`creator`、`usdc`）  
- `getQuoteBuy(marketAddress, usdcIn)`：获取买入报价（免手续费）  
- `getQuoteSell(marketAddress, tokensIn)`：获取卖出报价（已扣除 5% 手续费）  

**发布方法**：
- `prepareLaunchToken(params)`：准备发布所需的元数据和意图（仅用于模拟）  
- `launchToken(params)`：执行审批和发布操作  

**交易方法**：
- `buy(marketAddress, usdcIn, slippageBps?)`：审批 USDC 并买入代币  
- `sell(marketAddress, tokensIn, tokenAddress, slippageBps?)`：审批代币并卖出  

**奖励方法**：
- `getRewardsEarned(poolAddress, account)`：检查钱包中未领取的 USDC 奖励  
- `claimRewards(poolAddress)`：领取 USDC 奖励  

**迁移方法**：
- `getMigrationStatus()`：检查从 V1 到 V2 的迁移状态  
- `migrate(v1Amount)`：审批 V1 代币并迁移到 V2  

**辅助方法**：
- `calculateProgress(marketDetails)`：计算迁移进度百分比  
- `calculateMarketCap(marketDetails)`：计算市场市值（以 USDC 计算）  

## V2 版本的市场信息字段

`getMarket()` 方法的响应现在包含以下字段：

```ts
interface MarketDetails {
  market: string;
  token: string;
  usdc: string;                  // USDC contract address
  graduated: boolean;            // true after 95% sold
  curveTokensRemaining: string;
  baseReserveReal: string;       // real USDC in curve
  totalBaseReserve: string;      // virtual + real
  virtualBase: string;           // $3,000 USDC virtual
  liquidityTokens: string;       // reserved for Aerodrome LP
  sellFeeBps: number;            // 500 (5%)
  creator: string;               // token creator address
  holderRewardsPool: string;     // $MOLTM rewards pool
  aerodromePool: string | null;  // DEX pool after graduation
  progressPercent: number;       // 0-95 (graduates at 95)
}
```

## 发布前的元数据和图片要求

发布前请遵守以下规则：
- 图片格式必须为 PNG 或 JPEG  
- 最大文件大小不超过 500KB（建议不超过 100KB）  
- 图片尺寸必须为正方形，最小为 512x512，最大为 2048x2048  
- 社交媒体链接必须是有效的 URL  
- 普通发布的种子资金至少为 20 美元（USDC）  

## 故障诊断**

- **缺少私钥**：请设置 `MOLTMOON_PRIVATE_KEY` 或使用 `--private-key` 参数。  
- **不支持的网络**：仅支持 `base` 网络。  
- **转账金额超出限制**：重新运行买入/卖出/发布流程以完成审批。  
- **转账金额超出账户余额**：请使用 Base 网络的 ETH（作为 gas）或 USDC/代币进行转账。  
- **已成熟**：市场已迁移到 Aerodrome，交易在 DEX 上进行。  
- **滑点问题**：增加 `--slippage` 参数的值或调整交易金额。  
- **债券曲线问题**：债券曲线上剩余的代币不足，无法完成购买操作。  
- **未达到成熟条件**：债券曲线上的代币售出比例未达到 95%。  
- **错误信息**：检查 `MOLTMOON_API_URL` 的 DNS 设置和 API 的运行状态。  
- **图片验证问题**：请确保图片格式、大小和尺寸符合要求。  

## 操作者政策

- 每次发布新代币前，请先进行模拟测试。  
- 在执行写入操作前确认签名者地址和链上网络信息。  
- 将敏感信息存储在 `.env` 文件中，切勿直接提交密钥。  
- 发布/买入/卖出/领取操作完成后记录交易哈希值以备审计。  
- 当债券曲线上的代币售出达到 95% 时，系统会自动完成迁移，无需手动触发。  
- 成熟后的代币在 Aerodrome 平台上交易，仍需缴纳 5% 的卖出税费。  
- $MOLTM 持有者可通过 `HolderRewardsPool` 从所有平台交易活动中获得被动收益。