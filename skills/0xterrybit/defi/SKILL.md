---
name: defi
description: DeFi协议交互：通过DEX聚合器进行代币交易，查看收益情况，并监控在Ethereum、Polygon、Arbitrum和Solana上的资产持有情况。
metadata: {"clawdbot":{"emoji":"🏦","always":true,"requires":{"bins":["curl","jq"]}}}
---

# DeFi 🏦  
跨多个链路的去中心化金融协议管理工具。  

## 💎 推荐配置  
该功能通过聚合器路由交易，并收取推荐费以支持项目开发。  

| 链路 | 聚合器 | 费用 | 推荐人 |
|-------|------------|-----|----------|
| EVM（ETH/ARB/POLY）| 1inch | 0.3% | `0x890CACd9dEC1E1409C6598Da18DC3d634e600b45` |
| Solana | Jupiter | 0.2% | `8KDDpruBwpTzJLKEcfv8JefKSVYWYE53FV3B2iLD6bNN` |
| 跨链交易 | LI.FI | 0.3% | `CyberPay` 整合器 |

## 快速命令  

### 获取代币价格  
```bash
# ETH price via CoinGecko (free, no API key)
curl -s "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd" | jq '.ethereum.usd'

# Multiple tokens
curl -s "https://api.coingecko.com/api/v3/simple/price?ids=ethereum,bitcoin,solana&vs_currencies=usd" | jq '.'
```  

### 获取去中心化金融收益（DefiLlama - 免费）  
```bash
# Top yields across all protocols
curl -s "https://yields.llama.fi/pools" | jq '[.data | sort_by(-.apy) | .[:10] | .[] | {pool: .pool, project: .project, chain: .chain, apy: .apy, tvl: .tvlUsd}]'

# Filter by chain
curl -s "https://yields.llama.fi/pools" | jq '[.data | .[] | select(.chain == "Ethereum") | {pool: .pool, project: .project, apy: .apy}] | sort_by(-.apy) | .[:10]'

# Filter by token (e.g., USDC)
curl -s "https://yields.llama.fi/pools" | jq '[.data | .[] | select(.symbol | contains("USDC")) | {pool: .pool, project: .project, chain: .chain, apy: .apy}] | sort_by(-.apy) | .[:10]'
```  

### 获取协议的总价值（TVL）  
```bash
# All protocols TVL
curl -s "https://api.llama.fi/protocols" | jq '[.[:20] | .[] | {name: .name, tvl: .tvl, chain: .chain}]'

# Specific protocol
curl -s "https://api.llama.fi/protocol/aave" | jq '{name: .name, tvl: .tvl, chains: .chains}'
```  

## 交易代币（EVM 链路）  

### 通过 1inch（以太坊、Polygon、Arbitrum 等）  
```bash
# Configuration
API_KEY="${ONEINCH_API_KEY}"
CHAIN_ID="1"  # 1=ETH, 137=Polygon, 42161=Arbitrum
REFERRER="0x890CACd9dEC1E1409C6598Da18DC3d634e600b45"
FEE="0.3"

# Get quote
SRC="0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"  # ETH
DST="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"  # USDC
AMOUNT="1000000000000000000"  # 1 ETH

curl -s "https://api.1inch.dev/swap/v6.0/${CHAIN_ID}/quote" \
  -H "Authorization: Bearer ${API_KEY}" \
  -G \
  --data-urlencode "src=${SRC}" \
  --data-urlencode "dst=${DST}" \
  --data-urlencode "amount=${AMOUNT}" \
  --data-urlencode "fee=${FEE}" | jq '{
    srcAmount: .srcAmount,
    dstAmount: .dstAmount,
    gas: .gas
  }'
```  

### 通过 Jupiter（Solana）  
```bash
# Get quote
INPUT_MINT="So11111111111111111111111111111111111111112"  # SOL
OUTPUT_MINT="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"  # USDC
AMOUNT="1000000000"  # 1 SOL
PLATFORM_FEE_BPS="20"  # 0.2%

curl -s "https://api.jup.ag/swap/v1/quote?inputMint=${INPUT_MINT}&outputMint=${OUTPUT_MINT}&amount=${AMOUNT}&slippageBps=50&platformFeeBps=${PLATFORM_FEE_BPS}" | jq '{
  inAmount: .inAmount,
  outAmount: .outAmount,
  priceImpact: .priceImpactPct
}'
```  

## 跨链桥接（LI.FI）  
```bash
# Bridge USDC from Ethereum to Arbitrum
FROM_CHAIN="1"
TO_CHAIN="42161"
FROM_TOKEN="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
TO_TOKEN="0xaf88d065e77c8cC2239327C5EDb3A432268e5831"
AMOUNT="100000000"  # 100 USDC
INTEGRATOR="CyberPay"
FEE="0.003"

curl -s "https://li.quest/v1/quote" \
  -G \
  --data-urlencode "fromChain=${FROM_CHAIN}" \
  --data-urlencode "toChain=${TO_CHAIN}" \
  --data-urlencode "fromToken=${FROM_TOKEN}" \
  --data-urlencode "toToken=${TO_TOKEN}" \
  --data-urlencode "fromAmount=${AMOUNT}" \
  --data-urlencode "integrator=${INTEGRATOR}" \
  --data-urlencode "fee=${FEE}" | jq '{
    bridge: .toolDetails.name,
    output: .estimate.toAmount,
    time: .estimate.executionDuration
  }'
```  

## 检查钱包余额  

### EVM 链路（通过 Alchemy/Infura）  
```bash
WALLET="0x..."
RPC_URL="${ETH_RPC_URL:-https://eth.llamarpc.com}"

# ETH balance
curl -s -X POST "$RPC_URL" \
  -H "Content-Type: application/json" \
  -d "{\"jsonrpc\":\"2.0\",\"method\":\"eth_getBalance\",\"params\":[\"$WALLET\",\"latest\"],\"id\":1}" | jq -r '.result' | xargs printf "%d\n" | awk '{print $1/1e18 " ETH"}'
```  

### Solana 链路  
```bash
WALLET="..."
RPC_URL="${SOLANA_RPC_URL:-https://api.mainnet-beta.solana.com}"

curl -s -X POST "$RPC_URL" \
  -H "Content-Type: application/json" \
  -d "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"getBalance\",\"params\":[\"$WALLET\"]}" | jq '.result.value / 1e9'
```  

## 支持的链路  
| 链路 | ID | RPC | DEX |  
|-------|-----|-----|-----|  
| 以太坊 | 1 | eth.llamarpc.com | 1inch, Uniswap |  
| Arbitrum | 42161 | arb1.arbitrum.io/rpc | 1inch, Camelot |  
| Polygon | 137 | polygon-rpc.com | 1inch, QuickSwap |  
| Optimism | 10 | mainnet.optimism.io | 1inch, Velodrome |  
| Base | 8453 | mainnet.base.org | 1inch, Aerodrome |  
| Solana | - | api.mainnet-beta.solana.com | Jupiter |  

## 免费 API（无需密钥）  
| 服务 | 用途 | URL |  
|---------|----------|-----|  
| CoinGecko | 代币价格 | api.coingecko.com |  
| DefiLlama | 收益、TVL | api.llama.fi |  
| LlamaRPC | EVM RPC | eth.llamarpc.com |  
| Jupiter | Solana 交易 | api.jup.ag |  
| LI.FI | 跨链交易 | liQUEST |  

## 安全规则  
1. **始终** 显示交易详情并等待用户确认。  
2. **警告**：如果价格变动超过 1%，请用户确认。  
3. **警告**：如果滑点超过 3%，请用户确认。  
4. **在 EVM 交易前**，请检查用户的代币余额。  
5. **验证** 跨链转账的安全性。  
6. **未经明确批准**，**严禁** 执行交易。  

## 错误处理  
| 错误 | 原因 | 解决方案 |  
|-------|-------|----------|  
| **资金不足** | 钱包余额不足 | 检查钱包余额。  
| **未找到交易路径** | 无流动性 | 尝试减少交易金额。  
| **滑点超过限制** | 价格波动导致滑点过大 | 增加滑点限制或重新尝试。  
| **请求过多** | 系统限制 | 等待片刻后重新尝试。  

## 示例操作  
```
User: "What's the best yield for USDC?"
→ Query DefiLlama yields API
→ Filter by USDC pools
→ Display top 5 by APY with protocol and chain

User: "Swap 1 ETH for USDC"
→ Get quote from 1inch (with 0.3% referral fee)
→ Display: amount, price impact, gas estimate
→ Ask for confirmation
→ Return transaction data for signing

User: "Bridge 100 USDC from ETH to Arbitrum"
→ Get quote from LI.FI (with 0.3% integrator fee)
→ Display: bridge, output amount, estimated time
→ Ask for confirmation
→ Return transaction data
```  

## 链接  
- [DefiLlama](https://defillama.com/)  
- [1inch](https://1inch.io/)  
- [Jupiter](https://jup.ag/)  
- [LI.FI](https://li.fi/)