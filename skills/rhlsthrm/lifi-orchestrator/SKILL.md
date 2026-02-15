---
name: lifi-orchestrator
description: 通过 LI.FI 实现跨链桥接与交换——这是一款领先的桥接聚合器，能够连接 30 多个跨链桥接服务和去中心化交易所（DEX），以提供最优的交易费率。您可以在以下情况下使用它：  
1. 获取在不同区块链之间转移代币的报价；  
2. 以最优惠的价格执行跨链交易；  
3. 查看桥接交易的实时状态；  
4. 比较 Stargate、Across、Hop、Celer 等协议的交易路径。  

LI.FI 支持以太坊（Ethereum）、Polygon、Arbitrum、Optimism、Base、BSC、Avalanche、Solana 以及 15 种以上的其他区块链。它能够处理原生代币和 ERC-20 标准的代币，并提供自动滑点保护（即防止交易价格因网络波动而产生意外损失）。
---

# LI.FI Orchestrator

使用 LI.FI 的聚合桥接/去中心化交易所（DEX）路由功能，在不同区块链之间传输代币。

## 快速入门

```bash
# Get a quote (ETH on Ethereum → MATIC on Polygon)
python3 scripts/quote.py --from-chain 1 --to-chain 137 \
  --from-token ETH --to-token MATIC --amount 0.1

# Execute a bridge (requires private key)
python3 scripts/bridge.py --from-chain 1 --to-chain 137 \
  --from-token ETH --to-token USDC --amount 0.1

# Check transaction status
python3 scripts/status.py <txHash>
```

## API 基础信息

- **端点**: `https://liQUEST/v1`
- **认证**: 可通过 `x-lifi-api-key` 头部字段提供 API 密钥（可提升请求速率限制）
- **请求速率限制**: 无密钥时为每分钟 10 次请求；使用密钥后限制会提高

## 常见区块链 ID

| 区块链 | ID | 原生代币 |
|-------|-----|--------------|
| Ethereum | 1 | ETH |
| Polygon | 137 | MATIC |
| Arbitrum | 42161 | ETH |
| Optimism | 10 | ETH |
| Base | 8453 | ETH |
| BSC | 56 | BNB |
| Avalanche | 43114 | AVAX |
| Solana | 1151111081099710 | SOL |

## 主要 API 端点

### 获取报价
```bash
curl "https://li.quest/v1/quote?fromChain=1&toChain=137&fromToken=ETH&toToken=USDC&fromAmount=1000000000000000000&fromAddress=<wallet>"
```

### 获取区块链信息
```bash
curl "https://li.quest/v1/chains"
```

### 获取代币信息
```bash
curl "https://li.quest/v1/tokens?chains=1,137"
```

### 检查交易状态
```bash
curl "https://li.quest/v1/status?txHash=<hash>"
```

## 代币地址

- 原生代币（如 ETH、MATIC 等）的地址为 `0x0000000000000000000000000000000000000000`；
- ERC-20 代币的地址为对应的合约地址。

常见稳定币地址：
- **USDC (Ethereum)**: `0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48`
- **USDC (Polygon)**: `0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359`
- **USDT (Ethereum)**: `0xdAC17F958D2ee523a2206206994597C13D831ec7`

## 工作流程

1. **获取报价** → 返回最佳交易路径及所需 gas 费用估算
2. **检查交易批准情况** → 对于 ERC-20 代币，如有需要需进行交易批准
3. **执行交易** → 根据报价中的信息签署并发送 `transactionRequest`
4. **跟踪交易状态** → 定期查询 `/status` 状态直到交易完成

## 脚本

- `scripts/quote.py` — 获取可读的桥接报价信息
- `scripts/bridge.py` — 执行跨链交易（需要钱包）
- `scripts/status.py` — 监控交易状态

## 注意事项

- LI.FI 集中了 30 多个桥接服务与去中心化交易所以提供最优交易费率
- 默认滑点为 0.5%（可配置）
- 部分交易路径有最低交易金额要求
- 跨链交易通常需要 1-20 分钟完成