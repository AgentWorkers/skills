# 0x Swap API 技能

⚠️ **安全警告：** 该技能涉及实际资金操作。在执行任何交易前，请仔细核对所有参数。

## 安装

```bash
cd skills/0x-swap
npm install
```

## 设置

```bash
# Get API key from https://dashboard.0x.org/
# Your key must have "Full Trading" access (not just prices)
export ZEROEX_API_KEY="your-api-key"

# Set your wallet private key (for signing swaps)
# Pass via PRIVATE_KEY environment variable
export PRIVATE_KEY="your-private-key-hex"
```

## API 密钥要求

⚠️ **重要提示：** 您的 API 密钥必须具有完整的交易权限：
- 仅提供价格信息的密钥会返回 `transaction.to: null`；
- 具有完整交易权限的密钥会返回完整的交易对象；
- 对于无需支付 gas 的交易，请在仪表板应用设置中启用 “Gasless API” 功能。

## 使用方法

### 获取价格报价
```bash
node quote.js --sell USDC --buy WETH --amount 1 --chain base
```

### 执行交易（使用 “AllowanceHolder” 模式）
```bash
node swap.js --sell USDC --buy WETH --amount 1 --chain base --wallet 0x...
```

### 执行无需支付 gas 的交易（使用 “Meta-transaction” 模式）
```bash
node gasless.js --sell USDC --buy WETH --amount 1 --chain base --wallet 0x...
```

## API 参考

### 端点

| 端点 | 描述 |
|----------|-------------|
| `/swap/allowance-holder/quote` | 需要链上批准的交换交易 |
| `/gasless/quote` | 无需支付 gas 的交换交易（Meta-transaction 模式） |
| `/gasless/submit` | 提交已签名的无需支付 gas 的交易请求 |
| `/gasless/status/{tradeHash}` | 查询交易状态 |
| `/trade-analytics/swap` | 获取已完成的交换交易记录 |
| `/trade-analytics/gasless` | 获取已完成的无需支付 gas 的交易记录 |

### 所有请求所需的头部信息
```
0x-api-key: YOUR_API_KEY
0x-version: v2
```

### 必需参数
- `sellToken`：用于出售的代币地址 |
- `buyToken`：用于购买的代币地址 |
- `sellAmount`：交易金额（以基础单位计，USDC 保留 6 位小数，WETH 保留 18 位小数） |
- `chainId`：链 ID（1=ETH，8453=Base 等） |
- `taker`：执行交易的钱包地址（必填） |
- `slippagePercentage`：最大滑点率（例如，“1” 表示 1%）——建议使用此参数 |

## 交易类型

### 1. 使用 “AllowanceHolder” 模式（最可靠的方式）

1. 获取报价：`GET /swap/allowance-holder/quote`
2. 将代币授权给 `quote.allowanceTarget`
3. 执行交易：`wallet.sendTransaction({ to: tx.to, data: tx.data })`

### 2. 无需支付 gas 的交易（Meta-transaction 模式）

**注意：** 需要在仪表板应用设置中启用 “Gasless API” 功能：

1. 获取报价：`GET /gasless/quote`
2. 检查 `quote.approval` 是否不为空；如果为空，则签署授权许可。
3. 签署交易数据：`wallet.signTypedData(quote.trade.eip712)`
4. 将签名拆分为 {v, r, s} 格式。
5. 提交交易请求：`POST /gasless/submit`
6. 查询交易状态：`GET /gasless/status/{tradeHash}`

```javascript
// Sign trade
const tradeSig = hexToSignature(signature);
const submitBody = {
  trade: {
    type: quote.trade.type,  // "settler_metatransaction"
    eip712: quote.trade.eip712,
    signature: {
      v: Number(tradeSig.v),
      r: tradeSig.r,
      s: tradeSig.s,
      signatureType: 2
    }
  }
};

// Submit
const res = await fetch('https://api.0x.org/gasless/submit', {
  method: 'POST',
  headers: { '0x-api-key': API_KEY, '0x-version': 'v2', 'Content-Type': 'application/json' },
  body: JSON.stringify(submitBody)
});
const { tradeHash } = await res.json();
```

### 3. 使用 EIP-712 许可的交换方式（更高级）

与 “AllowanceHolder” 模式类似，但使用 EIP-712 来进行交易授权。签名过程更为复杂。

## 交易历史记录

### 获取交易记录

```
GET https://api.0x.org/trade-analytics/swap?chainId=8453&taker=0x...
Headers: 0x-api-key: KEY, 0x-version: v2
```

### 获取无需支付 gas 的交易记录

```
GET https://api.0x.org/trade-analytics/gasless?chainId=8453&taker=0x...
Headers: 0x-api-key: KEY, 0x-version: v2
```

最多返回 200 条交易记录。可以使用 `nextCursor` 进行分页查询。

## 支持的链

| 链 | chainId |
|-------|---------|
| Ethereum | 1 |
| Base | 8453 |
| Polygon | 137 |
| Arbitrum | 42161 |
| Optimism | 10 |

## 常见代币地址（Base 链）

| 代币 | 地址 |
|-------|---------|
| WETH | 0x4200000000000000000000000000000000000006 |
| USDC | 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913 |
| DAI | 0x50c5725949A6F0C72E6C4a641F24049A917DB0Cb |

## 相关文件

- `quote.js`：用于获取价格报价
- `swap.js`：用于执行交易（使用 “AllowanceHolder” 模式）
- `gasless.js`：用于执行无需支付 gas 的交易（Meta-transaction 模式）
- `package.json`：项目依赖项

## 注意事项：

- 报价信息在大约 30 秒后失效，请定期刷新。
- 无需支付 gas 的交易需要在仪表板中启用相关功能。
- 不能直接出售原生 ETH，需先将其转换为 WETH。
- 交易历史记录的索引可能需要一些时间。

## 安全最佳实践

### 1. 私钥管理
- ⚠️ **切勿** 将私钥硬编码到代码或环境变量中。
- 使用加密密钥存储工具或硬件安全模块（HSM）来保管私钥。
- 考虑使用热钱包和冷钱包的组合方式（热钱包中存放少量资金）。

### 2. 防止滑点
```javascript
// Always set slippage to protect against MEV/price impact
const quote = await fetch(`/swap/allowance-holder/quote?${new URLSearchParams({
  sellToken, buyToken, sellAmount,
  slippagePercentage: '1',  // 1% max slippage
  chainId: '8453'
})}`);

// Verify received amount meets minimum
const minBuyAmount = quote.buyAmount * 0.99;
```

### 3. 授权安全性
```javascript
// ⚠️ NEVER approve unlimited amounts
// Approve only what you need

// Good: Exact amount
await token.approve(allowanceTarget, sellAmount);

// Bad: Unlimited (vulnerable to token contract hacks)
// await token.approve(allowanceTarget, ethers.MaxUint256);
```

### 4. 交易结果验证
```javascript
// Always verify swap output after execution
const balanceBefore = await token.balanceOf(wallet);
await wallet.sendTransaction({ to: tx.to, data: tx.data, value: tx.value });
const balanceAfter = await token.balanceOf(wallet);

const received = balanceAfter - balanceBefore;
if (received < minBuyAmount) {
  throw new Error('Swap failed: received less than minimum');
}
```

### 5. gas 安全性
```javascript
// Set reasonable gas limits to prevent overpayment
const gasLimit = Math.ceil(quote.gas * 1.2); // 20% buffer

await wallet.sendTransaction({
  to: tx.to,
  data: tx.data,
  gasLimit: gasLimit,
  maxFeePerGas: tx.maxFeePerGas,
  maxPriorityFeePerGas: tx.maxPriorityFeePerGas
});
```

### 6. 报价有效期
- ⚠️ 报价信息在大约 30 秒后失效，请在获取报价后立即执行交易。
- 如果报价失效，请监控交易是否会被撤销。

### 7. 代币授权
- 在执行交易前请检查现有的代币授权情况。
- 取消未使用的授权以减少攻击风险。
- 使用 Etherscan 等工具验证交易授权目标地址的合法性。