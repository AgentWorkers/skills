---
summary: Query crypto wallet portfolios, transactions, DeFi positions, and token prices across EVM chains and Solana using Zerion's MCP server.
---

# Zerion API 技能

使用 Zerion API MCP 服务器查询加密钱包数据。

## 概述

该技能允许通过 MCP 工具访问 Zerion 提供的加密钱包数据。支持 **EVM 链路**（以太坊、Polygon、Arbitrum、Optimism、Base、BSC 等）和 **Solana**。

**注意**：需要 API 密钥进行身份验证 - 请在 [https://developers.zerion.io](https://developers.zerion.io) 获取您的 API 密钥。

## 可用数据

| 数据类型 | 描述 |
|-----------|-------------|
| 财产组合 | 钱包总价值，按链条细分 |
| 交易记录 | 包含详细操作信息的完整交易历史 |
| 盈亏情况 | 盈利/亏损计算 |
| DeFi 位置 | DeFi 交易、质押、借贷情况 |
| 代币价格 | 实时价格及历史图表 |
| NFT 数据 | NFT 收藏及单个 NFT 的详细信息 |
| 燃气价格 | 各链路的当前燃气价格 |

## 常见查询

### 财产组合分析
```
Get the portfolio for wallet 0x1234...
Show total value and breakdown by chain for 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045
```

### 交易历史
```
Show recent transactions for 0x1234...
Get transaction history for 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045 in the last 30 days
```

### DeFi 位置
```
Show all DeFi positions for 0x1234...
What protocols is 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045 using?
```

### 代币分析
```
Get current price of ETH
Show price chart for USDC over the last 7 days
Compare ETH price to SOL
```

### NFT 数据
```
Show NFT collections owned by 0x1234...
Get details for Bored Ape #1234
List all NFTs in wallet 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045
```

### 燃气价格
```
What are current gas prices on Ethereum?
Compare gas prices across all EVM chains
Show Solana transaction fees
```

## 提示

1. **地址格式**：仅使用 0x 格式的地址（例如：0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045）
2. **多链支持**：支持 EVM 链路（以太坊、Polygon、Arbitrum、Optimism、Base、BSC 等）和 Solana
3. **实时数据**：所有数据均来自 Zerion 的实时索引
4. **需要身份验证**：必须配置 API 密钥

## 示例工作流程

### 客户研究
```
Analyze the portfolio composition of 0x1234...
What DeFi protocols are they using?
Show their transaction patterns over the last month
Calculate their PnL across all positions
```

### 代币分析
```
Get the current price of our governance token
Compare it to historical prices
Show top holders by wallet address
```

### 竞争分析
```
What wallets are using Protocol X?
What's the average portfolio size?
What other protocols do they use?
Show cross-chain activity patterns
```

### 多链分析
```
Compare wallet activity on Ethereum vs Solana
Show portfolio breakdown across all EVM chains
Which chains have the most DeFi activity?
```

## MCP 服务器详情

**URL**：`https://developers.zerion.io/mcp`
**类型**：远程 HTTP MCP 服务器
**身份验证**：需要 API 密钥（在 MCP 设置中配置）
**文档**：[https://developers.zerion.io/reference/building-with-ai](https://developers.zerion.io/reference/building-with-ai)

## 设置步骤

1. 在 [https://developers.zerion.io](https://developers.zerion.io) 获取您的 API 密钥。
2. 将 API 密钥添加到您的 MCP 配置中：
   ```json
   {
     "zerion": {
       "url": "https://developers.zerion.io/mcp",
       "headers": {
         "Authorization": "Bearer YOUR_API_KEY"
       }
     }
   }
   ```

## 相关资源

- API 文档：[https://developers.zerion.io](https://developers.zerion.io)
- Zerion 仪表板：[https://dashboard.zerion.io](https://dashboard.zerion.io)
- llms.txt：[https://developers.zerion.io/llms.txt](https://developers.zerion.io/llms.txt)（用于保持 AI 工具的更新）

## 适用场景

- 研究钱包地址（0x 格式）
- 分析 DeFi 交易和协议
- 获取各链路的实时代币价格
- 调查交易模式
- 查看 NFT 持有情况
- 查阅 EVM 链路和 Solana 的燃气价格
- 验证客户或竞争对手的数据
- 计算资产组合的盈亏情况