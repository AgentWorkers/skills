---
name: amped-openclaw
description: OpenClaw的DeFi操作插件支持通过SODAX进行跨链交易、桥接以及货币市场操作。在构建需要跨链执行的交易机器人、DeFi代理或投资组合管理工具时，请使用该插件。
---

# Amped OpenClaw 插件

这是一个专为 [OpenClaw](https://openclaw.ai) 开发的 DeFi（去中心化金融）插件，通过 [SODAX SDK](https://docs.sodax.com) 支持跨链交易、资产桥接以及货币市场操作。

## 主要功能

- 🔁 **跨链交易** — 在 Ethereum、Arbitrum、Base、Optimism、Avalanche、BSC、Sonic 等链之间执行代币交换。
- 🌉 **资产桥接** — 在各个子链与 Sonic 主链之间实现资产转移。
- 🏦 **跨链货币市场** — 在链 A 上供应代币，然后在链 B 上借款（您的抵押品保持不变！）
- 📊 **统一投资组合视图** — 提供跨链头寸的汇总信息，包括健康状况指标、风险分析及投资建议。
- 📜 **交易历史记录** — 通过 SODAX API 查询完整的交易/桥接历史记录。
- 🔐 **安全优先** — 配备了交易限额、滑点控制以及白名单等安全机制。

## 安装

```bash
openclaw plugins install amped-openclaw
```

安装完成后，请使用以下命令进行验证：
```bash
openclaw plugins list
openclaw tools list | grep amped_oc
```

## 钱包设置

该插件支持 **无钱包** 的使用模式（仅用于查询报价、余额和链信息）。如需执行交易，请安装 [evm-wallet-skill](https://github.com/amped-finance/evm-wallet-skill)：
```bash
git clone https://github.com/amped-finance/evm-wallet-skill.git ~/.openclaw/skills/evm-wallet-skill
cd ~/.openclaw/skills/evm-wallet-skill && npm install
node src/setup.js  # Generate a new wallet
```

或者使用 [Bankr](https://bankr.bot) 来管理您的加密密钥：

```bash
export BANKR_API_KEY=your-bankr-api-key
```

## 可用工具（共 23 个）

### 链信息查询工具
| 工具          | 功能描述                |
|------------------|----------------------|
| `amped_oc_supported_chains` | 显示所有支持的子链            |
| `amped_oc_supported_tokens` | 获取特定模块和链支持的代币列表     |
| `amped_oc_cross_chain_positions` | 提供所有链上的统一投资组合视图       |
| `amped_oc_user_intents` | 通过 SODAX API 查询交易历史记录       |

### 交易与桥接工具
| 工具          | 功能描述                |
|------------------|----------------------|
| `amped_oc_swap_quote` | 获取准确的交易报价             |
| `amped_oc_swap_execute` | 执行交易并遵守相关规则           |
| `amped_oc_bridge_quote` | 检查资产是否可桥接及最大可桥接金额     |
| `amped_oc_bridge_execute` | 执行资产桥接操作             |

### 货币市场工具
| 工具          | 功能描述                |
|------------------|----------------------|
| `amped_oc_mm_supply` | 以代币作为抵押品进行供应          |
| `amped_oc_mm_withdraw` | 提取已供应的代币             |
| `amped_oc_mm_borrow` | 在其他链上借款（支持跨链操作）       |
| `amped_oc_mm_repay` | 归还借款的代币             |

### 钱包管理工具
| 工具          | 功能描述                |
|------------------|----------------------|
| `amped_oc_list_wallets` | 列出所有已配置的钱包             |
| `amped_oc_add_wallet` | 添加新的钱包（带昵称）             |
| `amped_oc_set_default_wallet` | 设置默认钱包                 |

## 示例：跨链交易

```
"Swap 1000 USDC on Ethereum to USDT on Arbitrum"
```

或者通过以下工具完成交易：
```typescript
// Get quote
const quote = await agent.call('amped_oc_swap_quote', {
  walletId: 'main',
  srcChainId: 'ethereum',
  dstChainId: 'arbitrum',
  srcToken: '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48', // USDC
  dstToken: '0xaf88d065e77c8cC2239327C5EDb3A432268e5831', // USDT
  amount: '1000',
  type: 'exact_input'
});

// Execute
const result = await agent.call('amped_oc_swap_execute', {
  walletId: 'main',
  quote: quote,
  maxSlippageBps: 100
});
```

## 示例：跨链货币市场操作

在 Ethereum 上供应代币，然后在 Arbitrum 上借款：

```typescript
// Supply on Ethereum
await agent.call('amped_oc_mm_supply', {
  walletId: 'main',
  chainId: 'ethereum',
  token: '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48', // USDC
  amount: '50000',
  useAsCollateral: true
});

// Borrow to Arbitrum (different chain!)
await agent.call('amped_oc_mm_borrow', {
  walletId: 'main',
  chainId: 'ethereum',        // Collateral source
  dstChainId: 'arbitrum',     // Borrowed tokens destination
  token: '0xaf88d065e77c8cC2239327C5EDb3A432268e5831', // USDT
  amount: '20000'
});
```

## 支持的链

Ethereum、Arbitrum、Base、Optimism、Avalanche、BSC、Polygon、Sonic（主链）、LightLink、HyperEVM、MegaETH

## 资源链接

- **npm:** https://www.npmjs.com/package/amped-openclaw
- **GitHub:** https://github.com/amped-finance/amped-openclaw
- **SODAX 文档:** https://docs.sodax.com
- **Discord:** https://discord.gg/amped