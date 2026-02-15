---
name: amped-defi
version: 1.0.0
description: OpenClaw的DeFi操作插件支持通过SODAX进行跨链交易、桥接以及货币市场操作。在构建需要跨链执行的交易机器人、DeFi代理或投资组合管理工具时，可使用该插件。
---

# Amped DeFi 插件

这是一个专为 [OpenClaw](https://openclaw.ai) 设计的 DeFi 操作插件，通过 [SODAX SDK](https://docs.sodax.com) 支持跨链交易、资产桥接以及货币市场操作。

## 主要功能

- 🔁 **跨链交易** — 在 Ethereum、Arbitrum、Base、Optimism、Avalanche、BSC、Sonic 之间执行代币交换。
- 🌉 **资产桥接** — 在子链（spoke chains）与 Sonic 主链之间进行资产转移。
- 🏦 **跨链货币市场** — 在链 A 上供应代币，在链 B 上借款（你的抵押品保持不变！）
- 📊 **统一投资组合视图** — 提供跨链头寸的汇总信息，包括健康状况指标、风险分析和建议。
- 📜 **操作历史记录** — 通过 SODAX API 查询完整的交易/桥接历史记录。
- 🔐 **安全优先** — 具有交易限额、滑点上限和白名单等安全机制。

## 安装

```bash
openclaw plugins install amped-defi
```

安装完成后，请使用以下命令进行验证：
```bash
openclaw plugins list
openclaw tools list | grep amped_oc
```

## 钱包设置

该插件支持 **无钱包** 的只读操作（如查询报价、余额和链信息）。如需执行交易，请安装 [evm-wallet-skill](https://github.com/amped-finance/evm-wallet-skill)：
```bash
git clone https://github.com/amped-finance/evm-wallet-skill.git ~/.openclaw/skills/evm-wallet-skill
cd ~/.openclaw/skills/evm-wallet-skill && npm install
node src/setup.js  # Generate a new wallet
```

或者使用 [Bankr](https://bankr.bot) 来管理你的密钥：

```bash
export BANKR_API_KEY=your-bankr-api-key
```

## 可用工具（共 24 个）

### 信息查询工具
| 工具 | 功能描述 |
|------|-------------|
| `amped_supported_chains` | 列出所有支持的子链 |
| `amped_supported_tokens` | 查看特定模块和链支持的代币 |
| `amped_cross_chain_positions` | 提供所有链上的统一投资组合视图 |
| `amped_money_market_positions` | 查看单链的头寸详情 |
| `amped_money_market_reserves` | 查看市场储备、年化收益率（APY）和流动性 |
| `amped_user_intents` | 通过 SODAX API 查询操作历史记录 |
| `amped_portfolio_summary` | 结合钱包余额和货币市场头寸的汇总信息 |

### 交易与桥接工具
| 工具 | 功能描述 |
|------|-------------|
| `amped_swap_quote` | 获取准确的交易报价 |
| `amped_swap_execute` | 执行交易并执行相关策略 |
| `amped_swap_status` | 检查交易/桥接的状态 |
| `amped_swap_cancel` | 取消待定的交易 |
| `amped_bridge_discover` | 查找可用的桥接路径 |
| `amped_bridge_quote` | 检查桥接的可行性及最大可转移金额 |
| `amped_bridge_execute` | 执行资产桥接操作 |

### 货币市场工具
| 工具 | 功能描述 |
|------|-------------|
| `amped_mm_supply` | 以代币作为抵押品进行供应 |
| `amped_mm_withdraw` | 提取已供应的代币 |
| `amped_mm_borrow` | 借入代币（支持跨链操作） |
| `amped_mm_repay` | 偿还借入的代币 |

### 钱包管理工具
| 工具 | 功能描述 |
|------|-------------|
| `amped_list_wallets` | 列出所有配置的钱包 |
| `amped_add_wallet` | 添加新的钱包并设置昵称 |
| `amped_rename_wallet` | 重命名现有钱包 |
| `amped_remove_wallet` | 从配置中删除钱包 |
| `amped_set_default_wallet` | 设置默认钱包 |
| `amped_wallet_address` | 根据昵称获取钱包地址 |

---

## ⚠️ 重要提示：货币市场架构

### 中心-子链模型

SODAX 采用 **中心-子链架构**：
- **中心链**：Sonic（链 ID：146）—— 存储所有市场储备。
- **子链**：Base、Arbitrum、Ethereum、Optimism 等—— 用户交互的节点。

**规则**：货币市场操作（供应、借款、提取、偿还）必须从 **子链** 发起，**不能** 从中心链（Sonic）发起。

### 各链的健康状况

🚨 **每个子链都维护自己的独立健康状况指标。**
- 在 Base 上的抵押品 **不能** 保护在 Arbitrum 上的头寸。
- 每个链的头寸在清算时是 **独立处理的**。
- 必须 **按链** 显示健康状况指标，不能进行汇总。

**示例说明：**
在使用 `amped_cross_chain_positions` 时，请务必检查 `chainBreakdown` 数组：
```json
{
  "chainBreakdown": [
    { "chainId": "base", "healthFactor": "4.11", "supplyUsd": "17.25", "borrowUsd": "4.20" },
    { "chainId": "arbitrum", "healthFactor": "1.20", "supplyUsd": "100.00", "borrowUsd": "83.00" }
  ]
}
```

**切勿** 显示汇总的健康状况指标—— 这可能会让用户误以为所有链都是安全的（即使其中某个链处于清算风险中）。

---

## 示例：跨链交易

```
"Swap 1000 USDC on Ethereum to USDT on Arbitrum"
```

或者通过以下工具进行操作：
```typescript
// Get quote
const quote = await agent.call('amped_swap_quote', {
  walletId: 'main',
  srcChainId: 'ethereum',
  dstChainId: 'arbitrum',
  srcToken: 'USDC',
  dstToken: 'USDT',
  amount: '1000',
  type: 'exact_input',
  slippageBps: 50
});

// Execute
const result = await agent.call('amped_swap_execute', {
  walletId: 'main',
  quote: quote
});
```

## 示例：跨链货币市场

在 Base 上供应代币，在 Arbitrum 上借款：

```typescript
// Supply on Base
await agent.call('amped_mm_supply', {
  walletId: 'main',
  chainId: 'base',
  token: 'USDC',
  amount: '1000',
  useAsCollateral: true
});

// Borrow to Arbitrum (different chain!)
await agent.call('amped_mm_borrow', {
  walletId: 'main',
  chainId: 'base',          // Where collateral lives
  dstChainId: 'arbitrum',   // Where borrowed tokens go
  token: 'USDT',
  amount: '500'
});
```

## 投资组合显示规则

在显示投资组合数据时，请务必：
1. **按链** 显示余额。
2. **按链** 显示健康状况指标。
3. **标记风险较高的头寸**（健康状况指标 < 1.5）。

```typescript
const positions = await agent.call('amped_cross_chain_positions', {
  walletId: 'main'
});

// Good display:
positions.chainBreakdown.forEach(chain => {
  console.log(`${chain.chainId}: Supply $${chain.supplyUsd} | Borrow $${chain.borrowUsd} | HF: ${chain.healthFactor}`);
});
```

## 支持的链

Ethereum、Arbitrum、Base、Optimism、Avalanche、BSC、Polygon、Sonic（中心链）、LightLink、HyperEVM、Kaia

## 资源链接

- **npm**：https://www.npmjs.com/package/amped-defi
- **GitHub**：https://github.com/amped-finance/amped-defi
- **SODAX 文档**：https://docs.sodax.com
- **Discord**：https://discord.gg/amped

---

## 🧠 注意事项

### Bankr 钱包的限制

**Bankr 钱包的链支持情况如下：**

| 链 | 作为来源链 | 作为目标链 |
|-------|-----------|----------------|
| Ethereum | ✅ | ✅ |
| Base | ✅ | ✅ |
| Polygon | ✅ | ✅ |
| Solana | ❌ | ✅（仅支持接收） |
| Arbitrum | ❌ | ❌ |
| Optimism | ❌ | ❌ |
| 其他链 | ❌ | ❌ |

**示例**：可以使用 Bankr 在 Base 和 Solana 之间进行跨链交易：
```typescript
await agent.call('amped_swap_execute', {
  walletId: 'bankr',
  srcChainId: 'base',      // ✅ Bankr supports as source
  dstChainId: 'solana',    // ✅ Solana OK as destination
  recipient: '8qguBqM4UHQ...',  // Solana base58 address
  ...
});
```

**注意**：不能使用 Bankr 在 Arbitrum 上发起跨链交易。

### 基于操作的结算方式

所有交易和桥接操作都是 **基于操作意图** 来执行的：
- 交易不是即时完成的。
- 结算通常需要 **30-60 秒**。
- 使用 `amped_swap_status` 来确认交易是否完成。
- 响应中的 `sodaxScanUrl` 可以查看完整的操作流程。

**注意**：即使工具显示操作成功，也不代表交易已经完成—— 只表示操作已被提交，尚未实际结算。

### Solana 地址格式

Solana 地址使用 **base58 编码**，而非十六进制格式：
- ✅ 正确格式：`8qguBqM4UHQNHgBm18NLPeonSSFEB3RWBdbih6FXhwZu`
- ❌ 错误格式：`0x8qguBqM4UHQ...`

在指定 Solana 收件人地址时，请使用 base58 格式。

### 高波动市场中的滑点问题

在波动较大的市场中，默认的滑点（50 bps / 0.5%）可能导致交易失败：
- 在正常情况下，50 bps 是可接受的。
- 在高波动市场中，建议使用 100-200 bps。
- 在极端波动市场中，滑点可能高达 300 bps。

```typescript
await agent.call('amped_swap_quote', {
  ...
  slippageBps: 150  // 1.5% for volatile conditions
});
```

### 代币的小数位数

该插件会自动处理代币的小数位数，但请注意：
- **USDC、USDT**：6 位小数。
- **大多数 ERC20 标准代币**：18 位小数。
- **原生代币（如 ETH、MATIC）**：18 位小数。

在显示金额时，插件会以人类可读的形式呈现（例如：“100.5” 而不是 “100500000”）。

---

## 🎨 链路标识表情符号

在投资组合界面中使用以下表情符号来区分不同的链：

| 链路 | 表情符号 | 十六进制代码 |
|-------|-------|----------|
| LightLink | ⚡ | U+26A1 |
| Base | 🟦 | U+1F7E6 |
| Sonic | ⚪ | U+26AA |
| Arbitrum | 🔽 | U+1F53D |
| Optimism | 🔴 | U+1F534 |
| Polygon | ♾️ | U+267E |
| BSC | 🔶 | U+1F536 |
| Ethereum | 💎 | U+1F48E |
| Avalanche | 🔺 | U+1F53A |
| HyperEVM | 🌀 | U+1F300 |
| Kaia | 🟢 | U+1F7E2 |

**使用示例：**
```
⚡ LightLink    │ 0.002 ETH + 5.49 USDC       │   $9.78
🟦 Base         │ 0.002 ETH + 0.39 USDC       │   $4.55
                │ 💰 Supply $21.93 Borrow $5.00
                │ 🏥 HF: 3.51 🟢
```