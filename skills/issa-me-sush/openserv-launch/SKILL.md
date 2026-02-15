---
name: openserv-launch
description: 通过 OpenServ Launch API 在 Base 区块链上发布代币。该 API 可用于创建基于 ERC-20 标准的代币，并利用 Aerodrome 平台提供的集中流动性池（liquidity pools）进行代币发行。这些代币可用于后续的部署、交易或其他业务场景（如 memecoins 的发行，或构建能够生成代币的代理程序）。如需完整的 API 参考信息，请参阅 reference.md 文件。如需了解如何构建和运行用于管理这些代币的代理程序，请查阅 openserv-agent-sdk 和 openserv-client 文档。您可以使用这些工具为自己的 OpenServ 代理程序生成代币。
---

# OpenServ 发布 API

在 Aerodrome Slipstream 上，利用单边集中流动性池即时发布代币。

**参考文件：**

- `reference.md` - 所有端点的完整 API 参考
- `troubleshooting.md` - 常见问题及解决方案
- `examples/` - 完整的代码示例

**基础 URL：`https://instant-launch.openserv.ai`

---

## 该 API 的功能

- **部署 ERC-20 代币** - 总供应量为 10 亿枚，采用标准代币合约
- **创建 Aerodrome CL 池** - 单边流动性池，价格波动范围为 2,000,000 倍
- **锁定流动性池 1 年** - 提供自动防止资金抽逃的保护机制
- **交易费用平分** - 创建者钱包获得 50% 的所有交易费用

---

## 快速入门

### 所需依赖项

```bash
npm install axios
```

### 发布代币

```typescript
import axios from 'axios'

const response = await axios.post('https://instant-launch.openserv.ai/api/launch', {
  name: 'My Token',
  symbol: 'MTK',
  wallet: '0x1234567890abcdef1234567890abcdef12345678',
  description: 'A cool memecoin',
  imageUrl: 'https://example.com/logo.png',
  website: 'https://mytoken.com',
  twitter: '@mytoken'
})

console.log(response.data)
// {
//   success: true,
//   token: { address: '0x...', name: 'My Token', symbol: 'MTK', supply: '1000000000' },
//   pool: { address: '0x...', tickSpacing: 500, fee: '2%' },
//   locker: { address: '0x...', lpTokenId: '12345', lockedUntil: '2027-02-03T...' },
//   txHashes: { tokenDeploy: '0x...', lpMint: '0x...', lock: '0x...', buy: '0x...' },
//   links: { explorer: '...', aerodrome: '...', dexscreener: '...' }
// }
```

---

## 端点概述

| 端点              | 方法    | 描述                                      |
| --------------------- | ------ | -------------------------------- |
| `/api/launch`         | POST   | 创建带有流动性池的新代币                         |
| `/api/tokens`         | GET    | 列出已发布的代币                             |
| `/api/tokens/:address`| GET    | 根据地址获取代币详情                         |

---

## 发布请求字段

| 字段            | 类型     | 是否必填 | 描述                                      |
| --------------------------- | -------- | ----------------------------- |
| `name`      | string | 是      | 代币名称（1-64 个字符）                         |
| `symbol`    | string | 是      | 代币符号（1-10 个字符，大写，字母数字混合）                 |
| `wallet`    | string | 是      | 创建者钱包地址（获得 50% 的费用）                     |
| `description` | string | 否      | 代币描述（最多 500 个字符）                         |
| `imageUrl`  | string | 否      | 图片文件链接（jpg、png、gif、webp、svg 格式）                |
| `website`   | string | 否      | 网站地址（必须以 http/https 开头）                     |
| `twitter`   | string | 否      | Twitter 账号（可带 @）                         |

---

## 发布响应

```typescript
interface LaunchResponse {
  success: true
  internalId: string           // Database record ID
  creator: string              // Creator wallet address
  token: {
    address: string            // Deployed token contract
    name: string
    symbol: string
    supply: string             // Always "1000000000"
  }
  pool: {
    address: string            // Aerodrome CL pool
    tickSpacing: number        // 500
    fee: string                // "2%"
  }
  locker: {
    address: string            // LP locker contract
    lpTokenId: string          // NFT position ID
    lockedUntil: string        // ISO date (1 year from launch)
  }
  txHashes: {
    tokenDeploy: string        // Token deployment tx
    stakingTransfer: string    // 5% staking allocation tx
    lpMint: string             // LP position mint tx
    lock: string               // LP lock tx
    buy: string                // Initial buy tx
  }
  links: {
    explorer: string           // Basescan token page
    aerodrome: string          // Aerodrome swap page
    dexscreener: string        // DEXScreener chart
    defillama: string          // DefiLlama swap
  }
}
```

---

## 代币默认参数

| 参数              | 值                                      |
| --------------------------- | -------------------------------------- |
| 代币总量       | 10 亿枚                              |
| 初始市值        | 15,000 美元                              |
| 价格波动范围     | 2,000,000 倍（约 300 亿美元）                     |
| 流动性池费用     | 2%                                    |
| 价格更新间隔     | 500 毫秒                               |
| 费用分配        | 50/50（创建者/平台）                          |
| 锁定期限        | 1 年                                   |
| 投资奖励        | 5%                                    |
| 最小购买金额     | 0.0005 ETH                              |

---

## 示例：具备代币发布功能的代理

```typescript
import { Agent, run } from '@openserv-labs/sdk'
import { provision, triggers } from '@openserv-labs/client'
import { z } from 'zod'
import axios from 'axios'

const agent = new Agent({
  systemPrompt: 'You help users launch tokens on Base blockchain.'
})

agent.addCapability({
  name: 'launch_token',
  description: 'Launch a new ERC-20 token with LP pool on Aerodrome',
  schema: z.object({
    name: z.string().describe('Token name (1-64 chars)'),
    symbol: z.string().describe('Token symbol (1-10 chars, uppercase)'),
    wallet: z.string().describe('Creator wallet address'),
    description: z.string().optional().describe('Token description'),
    imageUrl: z.string().optional().describe('Logo image URL'),
    website: z.string().optional().describe('Website URL'),
    twitter: z.string().optional().describe('Twitter handle')
  }),
  async run({ args }) {
    const response = await axios.post('https://instant-launch.openserv.ai/api/launch', args)
    const { token, pool, links } = response.data
    return `Token launched! Address: ${token.address}, Pool: ${pool.address}, Trade: ${links.aerodrome}`
  }
})

async function main() {
  await provision({
    agent: {
      instance: agent,
      name: 'token-launcher',
      description: 'Launch tokens on Base with Aerodrome LP'
    },
    workflow: {
      name: 'Token Launcher',
      goal: 'Launch ERC-20 tokens on Base blockchain with Aerodrome concentrated liquidity pools',
      trigger: triggers.webhook({ waitForCompletion: true, timeout: 600 })
    }
  })
  await run(agent)
}

main().catch(console.error)
```

---

## 限制规则

- **每个钱包 24 小时内只能发布 1 个代币**（防止垃圾信息）
- 创建者钱包必须在链上具有活跃交易记录（账户不得为空）

---

## 网络信息

所有代币均部署在 **Base Mainnet** 上（链 ID：8453）。

---

## 更新本技能

本技能可能会过时。OpenServ 团队会定期发布更新——新的功能、API 变更和漏洞修复内容将在更新后才会在此显示。**如果某些功能无法正常使用，或您希望确保拥有最新信息，请在继续使用前更新本技能。**

```bash
# Check if updates are available
npx skills check

# Update all installed skills to latest versions
npx skills update
```

或者直接重新安装 OpenServ 技能：

```bash
npx skills add openserv-labs/skills
```

---

## 相关技能

- **openserv-agent-sdk** - 用于构建具备代币发布功能的代理
- **openserv-client** - 用于在平台上配置和部署代理
- **openserv-multi-agent-workflows** - 多代理协作模式
- **openserv-ideaboard-api** - 用于查找创意并发布与代币相关的服务