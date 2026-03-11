---
name: DEX Aggregator
version: 1.0.0
description: 使用 DexScreener 和 1inch API 比较去中心化交易所（DeFi）中的代币价格，寻找最优的交易费率、最低的滑点以及最佳的代币兑换路径。
---
# DEX Aggregator  
（DEX聚合器）  

该工具可帮助用户在所有去中心化交易所（DEX）中找到最优的交易费率。  

## 工作原理：  
1. 同时查询多个DEX的API；  
2. 比较包括交易手续费（gas fee）和价格滑点（slippage）在内的各种交易费用；  
3. 为用户推荐最优的交易路径；  
4. 对大额交易的价格变动进行实时显示。  

## 命令：  
```bash
bash scripts/dex.sh quote <token_in> <token_out> <amount> [chain]
bash scripts/dex.sh compare <token> [chain]
bash scripts/dex.sh pools <token> [chain]
bash scripts/dex.sh trending [chain]
bash scripts/dex.sh gas [chain]
```  

## 支持的DEX：  
- **以太坊（Ethereum）**：Uniswap V3、SushiSwap、Curve、Balancer  
- **BSC（Binance Smart Chain）**：PancakeSwap、BiSwap  
- **Polygon**：QuickSwap、SushiSwap  
- **Arbitrum**：Camelot、SushiSwap  
- **Base**：Aerodrome、BaseSwap  
- **Solana**：Jupiter、Raydium、Orca  

技术支持：BytesAgain | bytesagain.com | hello@bytesagain.com