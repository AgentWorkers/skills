# ZeroEx 交易技能

⚠️ **安全警告：** 此技能涉及实际资金，请在执行交易前仔细核对所有参数。

## 安装
```bash
cd skills/zeroex-swap
npm install
```

## 必需的环境变量

| 变量          | 描述                | 是否必需 |
|--------------|------------------|---------|
| `ZEROEX_API_KEY`   | 从 https://dashboard.0x.org/ 获取   | 是       |
| `PRIVATE_KEY`    | 钱包私钥（十六进制格式，不含前缀“0x”） | 是       |
| `RPC_URL`      | 链路的 RPC 端点（可选，提供默认值） | 否       |

**声明为必需的环境变量：`ZEROEX_API_KEY`、`PRIVATE_KEY`**

```bash
export ZEROEX_API_KEY="your-0x-api-key"
export PRIVATE_KEY="your-private-key-hex"
export RPC_URL="https://mainnet.base.org"  # optional
```

## 使用方法

### 获取价格报价
```bash
node quote.js --sell USDC --buy WETH --amount 1 --chain base
```

### 执行交易（卖出 → 买入）
```bash
node swap.js --sell USDC --buy WETH --amount 1 --chain base
```

### 执行交易（买入示例）
```bash
node swap.js --sell WETH --buy USDC --amount 0.01 --chain base
```

## 交易历史记录

### 获取交易记录
```bash
curl -s "https://api.0x.org/trade-analytics/swap?chainId=8453&taker=0xYOUR_WALLET" \
  -H "0x-api-key: $ZEROEX_API_KEY" \
  -H "0x-version: v2"
```

### 获取无需支付 gas 的交易记录
```bash
curl -s "https://api.0x.org/trade-analytics/gasless?chainId=8453&taker=0xYOUR_WALLET" \
  -H "0x-api-key: $ZEROEX_API_KEY" \
  -H "0x-version: v2"
```

## 无需支付 gas 的交易（Meta-transaction）

**操作流程：**
1. 获取无需支付 gas 的交易报价
2. 签署 EIP-712 格式的交易数据
3. 提交 Meta-transaction（元交易）

### 1) 获取无需支付 gas 的交易报价
```bash
curl -s "https://api.0x.org/gasless/quote?sellToken=USDC&buyToken=WETH&sellAmount=1000000&chainId=8453&taker=0xYOUR_WALLET" \
  -H "0x-api-key: $ZEROEX_API_KEY" \
  -H "0x-version: v2"
```

### 2) 签署 EIP-712 格式的交易数据（使用 viem 工具）
```js
// use viem to sign quote.trade.eip712
await client.signTypedData({
  domain: quote.trade.eip712.domain,
  types: quote.trade.eip712.types,
  message: quote.trade.eip712.message,
  primaryType: quote.trade.eip712.primaryType
});
```

### 3) 提交交易请求
```bash
curl -s -X POST "https://api.0x.org/gasless/submit" \
  -H "0x-api-key: $ZEROEX_API_KEY" \
  -H "0x-version: v2" \
  -H "Content-Type: application/json" \
  -d '{"trade": {"type":"settler_metatransaction","eip712": {"domain": {"name": "Settler", "chainId": 8453, "verifyingContract": "0x..."},"types": {...},"message": {...},"primaryType":"..."},"signature": {"v": 27, "r": "0x...", "s": "0x...", "signatureType": 2}}}'
```

## 安全最佳实践：
- 使用专用热钱包
- 设置滑点保护机制
- 仅批准精确的交易金额
- 通过 `RPC_URL` 使用自己的 RPC 服务进行交易