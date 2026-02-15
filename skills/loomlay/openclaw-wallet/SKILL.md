---
name: openclaw-wallet
description: |
  Multi-chain wallet and trading tools for AI agents. Provides 27 tools for: wallet management (create, balance, export keys), token swaps with flexible amounts ($100, 50%, max), cross-chain bridges, DEX market data (trending, volume, gainers/losers), token launches with tiered market caps, and fee management. Supports Solana and EVM chains. Use when agents need to interact with wallets, execute trades, research tokens, or launch tokens.
homepage: https://github.com/loomlay/openclaw-wallet
metadata: {"openclaw":{"requires":{"env":["LOOMLAY_API_KEY"]},"primaryEnv":"LOOMLAY_API_KEY","optionalEnv":["LOOMLAY_BASE_URL"],"install":"npm install @loomlay/openclaw-wallet-plugin"}}
---

# OpenClaw 钱包插件

这是一个专为 AI 代理设计的多链钱包和交易工具包，包含 27 个实用工具。

## 安装

**在使用任何工具之前，必须先安装 npm 包：**

```bash
npm install @loomlay/openclaw-wallet-plugin
```

此操作将安装该插件及其所有依赖项。无需额外安装其他包。

**身份验证是自动完成的。** 首次使用时，插件会自动注册 API 密钥，并将其保存到 `~/.loomlay/credentials.json` 文件中。无需手动配置。

**如需使用特定的 API 密钥而非自动注册，请执行以下操作：**
```bash
export LOOMLAY_API_KEY=agent_your_key_here
```

## 首次设置

**重要提示：** 安装插件后，必须先设置钱包才能使用交易/钱包工具。

首次与用户交互时（或技能首次加载时），请按照以下顺序执行设置步骤：
```javascript
const { wallet_get, wallet_create } = require('@loomlay/openclaw-wallet-plugin');

// 1. Check if a wallet already exists
const existing = await wallet_get();

if (!existing.success) {
  // 2. No wallet yet — create one
  const created = await wallet_create();
  if (created.success) {
    // 3. Show the user their new wallet
    // IMPORTANT: The seed phrase is shown ONCE. Tell the user to save it.
    // "Your wallet has been created:"
    // "  Solana: <solanaAddress>"
    // "  EVM: <evmAddress>"
    // "  Seed phrase: <seedPhrase> (save this securely — it won't be shown again)"
  }
} else {
  // Wallet exists — show addresses
  // "Your wallet:"
  // "  Solana: <solanaAddress>"
  // "  SOL balance: <balance>"
}
```

**在任何钱包或交易操作之前，请务必执行此检查。** 如果 `wallet_get()` 函数返回 `UNAUTHORIZED` 错误，可能需要重新注册 API 密钥——请删除 `~/.loomlay/credentials.json` 文件后重新尝试。

## 如何使用这些工具

所有 27 个工具都以 **扁平的异步函数** 的形式从插件包中导出。可以在 Node.js 中这样使用它们：
```javascript
const { wallet_get, swap_quote, swap, dex_trending, token_search } = require('@loomlay/openclaw-wallet-plugin');

// Check wallet balance
const wallet = await wallet_get();
// wallet.data.balances.solana.sol

// Get trending tokens
const trending = await dex_trending({ chain: 'solana', limit: 10 });
// trending.data.pairs[...]
```

每个工具都会返回一个标准化的响应结果：
```javascript
{
  success: true,       // or false
  data: { ... },       // result data (when success is true)
  error: {             // error info (when success is false)
    message: "...",
    code: "RATE_LIMITED",
    retryAfter: 30     // seconds (for rate limits)
  }
}
```

**在使用 `result.data` 之前，请务必检查 `result.success` 的值。**

## 重要提示：执行操作前请务必进行验证

对于任何涉及资金的操作：
1. **先获取报价**——向用户展示操作结果。
2. **获取用户确认**——未经用户同意切勿执行操作。
3. **执行操作**——运行交易。
4. **验证结果**——检查交易结果和新的账户余额。

```javascript
const { swap_quote, swap } = require('@loomlay/openclaw-wallet-plugin');

// Step 1: Quote
const quote = await swap_quote({ inputToken: 'SOL', outputToken: 'USDC', amount: '$100' });
// Tell user: "You'll swap ~1.2 SOL for ~$99.50 USDC"

// Step 2: User confirms → Step 3: Execute
const result = await swap({ inputToken: 'SOL', outputToken: 'USDC', amount: '$100' });
if (result.success) {
  // Show txHash and new balance
}
```

## 安全规则

- **切勿泄露助记词**——`wallet_create()` 函数仅会返回助记词一次，请告知用户将其保存到安全位置。
- **未经用户确认切勿执行操作**——务必先获取用户确认。
- **切勿猜测代币地址**——使用 `token_search()` 功能来查找代币地址。
- **切勿将 API 密钥硬编码**——请使用环境变量来存储密钥。

## 金额格式

交易工具支持多种金额格式：

| 格式 | 例子 | 含义 |
|--------|---------|---------|
| 小数 | `"1.5"` | 精确的代币数量 |
| USD | `"$100"` | 美元金额（会自动转换） |
| 百分比 | `"50%"` | 账户余额的 50% |
| 最大值 | `"max"` | 账户余额的全部 |

## 所有 27 个工具的参考文档

### 钱包（3 个工具）

```javascript
const { wallet_create, wallet_get, wallet_export_keys } = require('@loomlay/openclaw-wallet-plugin');

// Create new wallet (returns seed phrase ONCE)
await wallet_create()
// → { wallet: { solanaAddress, evmAddress }, seedPhrase, message }

// Get wallet addresses and balances
await wallet_get()
// → { wallet: { solanaAddress, evmAddress }, balances: { solana, evm } }

// Export private keys (requires seed phrase)
await wallet_export_keys({ seedPhrase: '12 word phrase here' })
// → { solanaPrivateKey, evmPrivateKey }
```

### 交易（5 个工具）

```javascript
const { swap, swap_quote, transfer, bridge, bridge_quote } = require('@loomlay/openclaw-wallet-plugin');

// Swap tokens
await swap({ inputToken: 'SOL', outputToken: 'USDC', amount: '$100', chain: 'solana', slippage: 1 })
// → { success, txHash, inputAmount, outputAmount }

// Get swap quote (no execution)
await swap_quote({ inputToken: 'SOL', outputToken: 'USDC', amount: '$100' })
// → { inputAmount, outputAmount, minOutputAmount, priceImpact, route }

// Transfer tokens
await transfer({ token: 'SOL', amount: '1.5', to: 'recipient_address' })
// → { success, txHash, amount, token, to }

// Bridge cross-chain
await bridge({ inputToken: 'SOL', amount: '1', sourceChain: 'solana', destinationChain: 'base' })
// → { success, sourceTxHash, destinationTxHash, status }

// Bridge quote
await bridge_quote({ inputToken: 'SOL', amount: '1', sourceChain: 'solana', destinationChain: 'base' })
// → { inputAmount, outputAmount, fee, estimatedTime }
```

### 代币（4 个工具）

```javascript
const { token_search, token_price, token_details, token_chart } = require('@loomlay/openclaw-wallet-plugin');

// Search tokens by name/symbol
await token_search({ query: 'BONK' })
// → { tokens: [{ address, symbol, name, price, safetyScore }] }

// Get token price
await token_price({ token: 'SOL', chain: 'solana' })
// → { token, price, chain }

// Get detailed token info
await token_details({ address: 'token_mint_address' })
// → { token, market, safety }

// Get OHLCV chart data
await token_chart({ address: 'token_mint_address' })
// → { data: [...] }
```

### 投资组合（2 个工具）

```javascript
const { portfolio_get, portfolio_history } = require('@loomlay/openclaw-wallet-plugin');

// Get combined portfolio across all chains
await portfolio_get()
// → { positions: [...], totalUsdValue: number }

// Get transaction history
await portfolio_history({ chain: 'solana', limit: 50 })
// → { transactions: [...] }
```

### DEX 市场数据（7 个工具）

```javascript
const { dex_trending, dex_volume, dex_gainers, dex_losers, dex_new, dex_pumpfun, dex_query } = require('@loomlay/openclaw-wallet-plugin');

// Trending pairs
await dex_trending({ chain: 'solana', minLiquidity: 10000, limit: 10 })
// → { pairs: [...], pagination }

// Top volume pairs
await dex_volume({ chain: 'solana', minLiquidity: 10000, limit: 10 })

// Top gainers (24h)
await dex_gainers({ chain: 'solana', minLiquidity: 10000, limit: 10 })

// Top losers (24h)
await dex_losers({ chain: 'solana', minLiquidity: 10000, limit: 10 })

// Newly created pairs (< 24h)
await dex_new({ chain: 'solana', minLiquidity: 5000, limit: 10 })

// Pumpfun trending (Solana only)
await dex_pumpfun({ maxAge: 6, maxProgress: 80, limit: 10 })

// Advanced query with custom filters
await dex_query({
  chain: 'solana',
  timeframe: 'h24',
  rankBy: 'volume',
  order: 'desc',
  minSafetyScore: 80,
  limit: 10
})
```

### 代币发行（2 个工具）

```javascript
const { tokenize_launch, tokenize_info } = require('@loomlay/openclaw-wallet-plugin');

// Launch a token (one per account)
await tokenize_launch({
  name: 'My Token',
  symbol: 'MYT',
  tier: '100k',        // 10k, 100k, 1m, 10m
  imageUrl: 'https://...'
})
// → { success, launchId, tokenMint, poolAddress, dexscreenerUrl }

// Get your launched token info
await tokenize_info()
// → { hasToken, launchId, tokenMint, poolAddress, dexscreenerUrl }
```

### 费用（2 个工具）

```javascript
const { fees_status, fees_claim } = require('@loomlay/openclaw-wallet-plugin');

// Check fee status
await fees_status()
// → { totalFeesGeneratedSol, beneficiaryFeesUnclaimedSol, canClaim, feeForfeitsAt }

// Claim fees (platform pays gas)
await fees_claim()
// → { success, amountSol, txSignature }
```

### RPC（2 个工具）

```javascript
const { rpc_call, rpc_chains } = require('@loomlay/openclaw-wallet-plugin');

// Direct RPC call
await rpc_call({ chain: 'solana', method: 'getBalance', params: ['address'] })
// → { result, error }

// List supported chains
await rpc_chains()
// → { chains: [...] }
```

## 支持的区块链

| 区块链 | 交易对 | 桥接器 | RPC 支持 |
|-------|-------|---------|-----|
| Solana | 是 | 是 | 是 |
| Ethereum | 是 | 是 | 是 |
| Base | 是 | 是 | 是 |
| Arbitrum | 是 | 是 | 是 |
| Optimism | 是 | 是 | 是 |
| Polygon | 是 | 是 | 是 |
| BSC | 是 | 是 | 是 |

## 错误处理

```javascript
const result = await swap({ inputToken: 'SOL', outputToken: 'USDC', amount: '1' });

if (!result.success) {
  switch (result.error?.code) {
    case 'RATE_LIMITED':
      // Wait result.error.retryAfter seconds and retry
      break;
    case 'BAD_REQUEST':
      // Invalid parameters
      break;
    case 'UNAUTHORIZED':
      // API key issue — check LOOMLAY_API_KEY or ~/.loomlay/credentials.json
      break;
    case 'INSUFFICIENT_BALANCE':
      // Not enough funds
      break;
    default:
      // General error
      break;
  }
}
```

## 参考文档

- `references/wallet-operations.md` - 钱包创建、安全设置、密钥导出
- `references/trading-guide.md` - 交易对、转账、支持多种金额格式的桥梁功能
- `references/market-analysis.md` - DEX 数据、市场趋势分析、筛选功能
- `references/token-launch.md` - 代币发行流程、费用结构
- `references/error-handling.md` - 错误类型、恢复策略、重试机制
- `references/amount-formats.md` - 金额格式的详细说明
- `references/chain-reference.md` - 支持的区块链及其特性

## 工作流程

- `workflows/first-time-setup.md` - 安装 → 创建钱包 → 进行首次交易
- `workflows/token-launch-playbook.md` - 完整的代币发行指南