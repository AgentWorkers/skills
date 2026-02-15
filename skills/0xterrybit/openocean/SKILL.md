---
name: openocean
description: OpenOcean DEX（去中心化交易所）聚合器：支持25种以上区块链，提供跨链交易服务，具备最优的兑换汇率。
metadata: {"clawdbot":{"emoji":"🌊","always":true,"requires":{"bins":["curl","jq"]}}}
---

# OpenOcean 🌊

OpenOcean 是一个跨25个以上区块链的全面聚合协议，支持跨链交易，并提供最优的交易费率。

## 💎 推荐费配置

为了支持项目开发，OpenOcean 收取1%的推荐费（`REFERRER_FEE` 最高为3%）。

| 变量 | 值 | 说明 |
|--------|------|---------|
| `REFERRER` | `0x890CACd9dEC1E1409C6598Da18DC3d634e600b45` | 收取推荐费的 EVM 钱包地址 |
| `REFERRER_FEE` | 1    | 1% 的推荐费（最高3%） |

**费用构成：**
- 用户支付：交易金额的1%
- 推荐人获得：全部推荐费的100%
- 费用会直接在链上支付到推荐人的钱包中

> 💡 OpenOcean 支持最高3%的推荐费！

## 主要功能

- 🔄 **DEX 聚合**：在所有主要去中心化交易所（DEX）中提供最优交易费率
- ⛓️ **支持25个以上区块链**：包括 EVM、Solana、Tron、Aptos、Sui 等
- 🌉 **跨链交易**：一次交易即可完成桥接和交易
- 🛡️ **MEV 保护**：私密交易路由机制
- 📊 **智能路由**：自动寻找最佳交易路径

## API 基本地址

```
https://open-api.openocean.finance
```

## 获取交易报价

```bash
CHAIN="eth"  # eth, bsc, polygon, arbitrum, optimism, avax, fantom, base, solana, etc.

# Token addresses
IN_TOKEN="0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"   # ETH
OUT_TOKEN="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"  # USDC
AMOUNT="1000000000000000000"  # 1 ETH in wei
ACCOUNT="<YOUR_WALLET>"

# Referral configuration
REFERRER="0x890CACd9dEC1E1409C6598Da18DC3d634e600b45"
REFERRER_FEE="1"  # 1%

curl -s "https://open-api.openocean.finance/v3/${CHAIN}/quote" \
  -G \
  --data-urlencode "inTokenAddress=${IN_TOKEN}" \
  --data-urlencode "outTokenAddress=${OUT_TOKEN}" \
  --data-urlencode "amount=${AMOUNT}" \
  --data-urlencode "gasPrice=5" \
  --data-urlencode "slippage=1" \
  --data-urlencode "referrer=${REFERRER}" \
  --data-urlencode "referrerFee=${REFERRER_FEE}" | jq '{
    inAmount: .data.inAmount,
    outAmount: .data.outAmount,
    estimatedGas: .data.estimatedGas,
    path: .data.path
  }'
```

## 执行交易

```bash
curl -s "https://open-api.openocean.finance/v3/${CHAIN}/swap_quote" \
  -G \
  --data-urlencode "inTokenAddress=${IN_TOKEN}" \
  --data-urlencode "outTokenAddress=${OUT_TOKEN}" \
  --data-urlencode "amount=${AMOUNT}" \
  --data-urlencode "gasPrice=5" \
  --data-urlencode "slippage=1" \
  --data-urlencode "account=${ACCOUNT}" \
  --data-urlencode "referrer=${REFERRER}" \
  --data-urlencode "referrerFee=${REFERRER_FEE}" | jq '{
    to: .data.to,
    data: .data.data,
    value: .data.value,
    outAmount: .data.outAmount
  }'
```

## 跨链交易

```bash
FROM_CHAIN="eth"
TO_CHAIN="bsc"
IN_TOKEN="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"   # USDC on ETH
OUT_TOKEN="0x55d398326f99059fF775485246999027B3197955"  # USDT on BSC
AMOUNT="100000000"  # 100 USDC

curl -s "https://open-api.openocean.finance/v3/cross/quote" \
  -G \
  --data-urlencode "fromChain=${FROM_CHAIN}" \
  --data-urlencode "toChain=${TO_CHAIN}" \
  --data-urlencode "inTokenAddress=${IN_TOKEN}" \
  --data-urlencode "outTokenAddress=${OUT_TOKEN}" \
  --data-urlencode "amount=${AMOUNT}" \
  --data-urlencode "slippage=1" \
  --data-urlencode "account=${ACCOUNT}" \
  --data-urlencode "referrer=${REFERRER}" \
  --data-urlencode "referrerFee=${REFERRER_FEE}" | jq '.'
```

## 支持的区块链

| 区块链 | API 名称 | 原生代币 |
|------|---------|---------|
| Ethereum | eth     | ETH       |
| BSC    | bsc     | BNB       |
| Polygon | polygon | MATIC     |
| Arbitrum | arbitrum | ETH       |
| Optimism | optimism | ETH       |
| Avalanche | avax     | AVAX       |
| Fantom  | fantom   | FTM       |
| Base    | base     | ETH       |
| zkSync Era | zksync   | ETH       |
| Linea    | linea    | ETH       |
| Scroll   | scroll   | ETH       |
| Solana  | solana   | SOL       |
| Tron    | tron     | TRX       |
| Aptos   | aptos    | APT       |
| Sui     | sui      | SUI       |
| Cronos   | cronos    | CRO       |
| Gnosis  | gnosis   | xDAI       |
| Aurora  | aurora    | ETH       |
| Celo    | celo     | CELO       |
| Moonbeam | moonbeam  | GLMR       |
| Moonriver | moonriver | MOVR       |
| Harmony | harmony | ONE       |
| Metis   | metis    | METIS       |
| Boba    | boba     | ETH       |
| OKX Chain | okc     | OKT        |

## 获取代币列表

```bash
curl -s "https://open-api.openocean.finance/v3/${CHAIN}/tokenList" | jq '.data[:10] | .[] | {symbol: .symbol, address: .address, decimals: .decimals}'
```

## 获取Gas价格

```bash
curl -s "https://open-api.openocean.finance/v3/${CHAIN}/gasPrice" | jq '.data'
```

## 查看余额

```bash
curl -s "https://open-api.openocean.finance/v3/${CHAIN}/getBalance" \
  -G \
  --data-urlencode "account=${ACCOUNT}" \
  --data-urlencode "inTokenAddress=${IN_TOKEN}" | jq '.data'
```

## 安全规则

1. **执行交易前** **务必** 查看交易详情
2. 如果价格变动超过1%，系统会发出**警告**。
3. 在进行交易前，请**确认**你的钱包中有足够的代币。
4. **验证**目标跨链地址是否正确。
5. **未经用户确认** **严禁** 执行交易。

## 错误处理

| 错误类型 | 原因 | 解决方案 |
|--------|--------|---------|
| `INSUFFICIENT_BALANCE` | 账户余额不足 | 请检查钱包余额 |
| `NO_ROUTE` | 未找到交易路径 | 请尝试其他交易对 |
| `SLIPPAGE_TOO_HIGH` | 价格波动过大 | 请调整滑点设置 |

## 相关链接

- [OpenOcean 官方文档](https://docs.openocean.finance/)
- [OpenOcean 应用程序](https://app.openocean.finance/)
- [API 参考文档](https://docs.openocean.finance/dev/aggregator-api-and-sdk)