---
name: odos
description: Odos 智能订单路由 DEX 聚合器：通过专利的 SOR（Smart Order Routing）算法，在 500 多个流动性来源中提供最优的交易汇率。
metadata: {"clawdbot":{"emoji":"🔮","always":true,"requires":{"bins":["curl","jq"]}}}
---

# Odos 🔮

Odos 是一个智能订单路由去中心化交易所（DEX）聚合器，采用专利算法，能够在 500 多个流动性来源中实现最佳的交易执行效果。

## 💎 推荐费配置

为了支持项目开发，Odos 收取 1% 的推荐费。

| 变量 | 值 | 说明 |
|----------|-------|-------------|
| `REFERRAL_CODE` | `0` | 推荐码（0 为默认值） |
| `FEE_RECIPIENT` | `0x890CACd9dEC1E1409C6598Da18DC3d634e600b45` | 收费钱包（EVM 地址） |
| `COMPACT` | `true` | 使用紧凑型 calldata 以节省交易费用 |

**费用构成：**
- 用户支付：交易金额的约 1%（可配置） |
- 推荐人获得：全部费用的 100% |
- 费用直接在链上转入推荐人的钱包。

## 主要功能

- 🔄 **500 多个流动性来源**：Uniswap、SushiSwap、Curve、Balancer 等 |
- ⛓️ **多链支持**：Ethereum、Arbitrum、Optimism、Polygon、Base、Avalanche |
- 🧠 **智能订单路由**：采用专利的 SOR（Smart Order Routing）算法 |
- 📊 **多输入交易**：一次可以交换多种代币 |
- 💰 **推荐计划**：每次交易均可获得奖励 |
- ⚡ **优化交易费用**：使用紧凑型 calldata 降低 Gas 成本 |

## API 基本地址

```
https://api.odos.xyz
```

## 获取交易报价

```bash
CHAIN_ID="1"  # Ethereum

# Token addresses
INPUT_TOKEN="0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"   # ETH
OUTPUT_TOKEN="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"  # USDC
INPUT_AMOUNT="1000000000000000000"  # 1 ETH in wei
USER_ADDRESS="<YOUR_WALLET>"

# Referral configuration
REFERRAL_CODE="0"

curl -s -X POST "https://api.odos.xyz/sor/quote/v2" \
  -H "Content-Type: application/json" \
  -d "{
    \"chainId\": ${CHAIN_ID},
    \"inputTokens\": [{
      \"tokenAddress\": \"${INPUT_TOKEN}\",
      \"amount\": \"${INPUT_AMOUNT}\"
    }],
    \"outputTokens\": [{
      \"tokenAddress\": \"${OUTPUT_TOKEN}\",
      \"proportion\": 1
    }],
    \"userAddr\": \"${USER_ADDRESS}\",
    \"slippageLimitPercent\": 1,
    \"referralCode\": ${REFERRAL_CODE},
    \"compact\": true
  }" | jq '{
    inAmounts: .inAmounts,
    outAmounts: .outAmounts,
    gasEstimate: .gasEstimate,
    pathId: .pathId
  }'
```

## 组装交易请求

```bash
PATH_ID="<PATH_ID_FROM_QUOTE>"

curl -s -X POST "https://api.odos.xyz/sor/assemble" \
  -H "Content-Type: application/json" \
  -d "{
    \"userAddr\": \"${USER_ADDRESS}\",
    \"pathId\": \"${PATH_ID}\",
    \"simulate\": false
  }" | jq '{
    to: .transaction.to,
    data: .transaction.data,
    value: .transaction.value,
    gasLimit: .transaction.gas
  }'
```

## 多输入交易（交换多种代币）

```bash
# Swap ETH + USDC to DAI
curl -s -X POST "https://api.odos.xyz/sor/quote/v2" \
  -H "Content-Type: application/json" \
  -d "{
    \"chainId\": ${CHAIN_ID},
    \"inputTokens\": [
      {
        \"tokenAddress\": \"0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE\",
        \"amount\": \"500000000000000000\"
      },
      {
        \"tokenAddress\": \"0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48\",
        \"amount\": \"500000000\"
      }
    ],
    \"outputTokens\": [{
      \"tokenAddress\": \"0x6B175474E89094C44Da98b954EesdeAC495271d0F\",
      \"proportion\": 1
    }],
    \"userAddr\": \"${USER_ADDRESS}\",
    \"slippageLimitPercent\": 1,
    \"referralCode\": ${REFERRAL_CODE},
    \"compact\": true
  }" | jq '.'
```

## 多输出交易（将一种代币拆分为多种代币）

```bash
# Swap ETH to 50% USDC + 50% DAI
curl -s -X POST "https://api.odos.xyz/sor/quote/v2" \
  -H "Content-Type: application/json" \
  -d "{
    \"chainId\": ${CHAIN_ID},
    \"inputTokens\": [{
      \"tokenAddress\": \"0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE\",
      \"amount\": \"${INPUT_AMOUNT}\"
    }],
    \"outputTokens\": [
      {
        \"tokenAddress\": \"0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48\",
        \"proportion\": 0.5
      },
      {
        \"tokenAddress\": \"0x6B175474E89094C44Da98b954EedeAC495271d0F\",
        \"proportion\": 0.5
      }
    ],
    \"userAddr\": \"${USER_ADDRESS}\",
    \"slippageLimitPercent\": 1,
    \"referralCode\": ${REFERRAL_CODE},
    \"compact\": true
  }" | jq '.'
```

## 支持的区块链

| 区块链 | ID | 原生代币 |
|-------|-----|--------------|
| Ethereum | 1 | ETH |
| Arbitrum | 42161 | ETH |
| Optimism | 10 | ETH |
| Polygon | 137 | MATIC |
| Base | 8453 | ETH |
| Avalanche | 43114 | AVAX |
| BSC | 56 | BNB |
| Fantom | 250 | FTM |
| zkSync Era | 324 | ETH |
| Linea | 59144 | ETH |
| Mantle | 5000 | MNT |
| Mode | 34443 | ETH |

## 获取代币列表

```bash
curl -s "https://api.odos.xyz/info/tokens/${CHAIN_ID}" | jq '.tokenMap | to_entries[:10] | .[] | {symbol: .value.symbol, address: .key, decimals: .value.decimals}'
```

## 获取流动性来源信息

```bash
curl -s "https://api.odos.xyz/info/liquidity-sources/${CHAIN_ID}" | jq '.[] | {id: .id, name: .name}'
```

## 查看合约信息

```bash
curl -s "https://api.odos.xyz/info/contract-info/v2/${CHAIN_ID}" | jq '{
  routerAddress: .routerAddress,
  executorAddress: .executorAddress
}'
```

## 安全规则

1. **执行前务必** 显示交易详情。
2. 如果价格波动超过 1%，系统会发出**警告**。
3. 交易前请**确认**用户的代币余额是否足够。
4. **务必** 核实交易后的输出金额。
5. **未经用户确认**，切勿执行交易。

## 错误处理

| 错误类型 | 原因 | 解决方案 |
|-------|-------|----------|
| `NO_PATH_FOUND` | 未找到可用的交易路径 | 请尝试其他交易对 |
| `INSUFFICIENT_LIQUIDITY` | 流动性不足 | 减少交易金额 |
| `SLIPPAGE_EXCEEDED` | 价格波动过大 | 增加滑点（slippage） |

## 相关链接

- [Odos 文档](https://docs.odos.xyz/) |
- [Odos 应用程序](https://app.odos.xyz/) |
- [API 参考](https://docs.odos.xyz/api/endpoints)