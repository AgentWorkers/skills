# PolyClawster

您可以通过命令行在 [Polymarket](https://polymarket.com) 的预测市场中进行交易。只需使用简单的 Node.js 脚本，即可搜索市场、下注（支持“YES”或“NO”选项），并管理您的钱包。

## 主要功能

- **搜索市场**：通过关键词查找 Polymarket 上的活跃市场。
- **交易任意市场**：通过 CLOB API 在任意活跃市场上进行“YES”或“NO”类型的交易。
- **自动创建钱包**：无需手动操作，即可自动创建 Polygon 钱包。
- **查看余额**：查看钱包余额、持仓情况以及盈亏情况。
- **信号扫描器**：自动检测高概率的交易机会。

## 快速入门

### 1. 设置（自动创建钱包）

```bash
node scripts/setup.js --auto
```

该脚本会通过 PolyClawster API 自动创建一个 Polygon 钱包，并将凭据保存到 `~/.polyclawster/config.json` 文件中。设置完成后，请向您的钱包地址充值 USDC（Polygon 网络的代币），即可开始交易。

### 2. 搜索市场

```bash
# Find markets about a topic
node scripts/search.js "bitcoin"

# Show top markets by volume
node scripts/search.js

# Limit results
node scripts/search.js --limit 5 "election"
```

### 3. 下单

```bash
# Bet $5 on YES for a market (use slug from search results)
node scripts/trade.js --market "will-bitcoin-reach-100k" --side YES --amount 5

# Bet $10 on NO using conditionId
node scripts/trade.js --market "0xabc123..." --side NO --amount 10
```

### 4. 查看余额

```bash
node scripts/balance.js
```

## 手动设置

如果您已经拥有一个 Polygon 钱包，并且拥有 Polymarket 的 CLOB API 密钥，可以执行以下脚本：

```bash
node scripts/setup.js --wallet 0xYOUR_PRIVATE_KEY
```

该脚本会为您生成 CLOB API 凭据，并将所有信息保存到 `~/.polyclawster/config.json` 文件中。

## 脚本参考

| 脚本          | 描述                                      |
|------------------|-------------------------------------------|
| `scripts/setup.js --auto` | 自动创建钱包并保存配置                        |
| `scripts/setup.js --wallet 0x...` | 使用现有钱包进行手动设置                        |
| `scripts/search.js [query]` | 在 Polymarket 上搜索市场                         |
| `scripts/trade.js --market X --side YES --amount N` | 在指定市场中下注（支持“YES”或“NO”选项）             |
| `scripts/balance.js` | 查看钱包余额和持仓情况                         |
| `scripts/edge.js` | 运行信号扫描器以自动执行交易                         |

## 配置文件

配置信息保存在 `~/.polyclawster/config.json` 文件中：

```json
{
  "wallet": {
    "address": "0x...",
    "privateKey": "0x..."
  },
  "api": {
    "key": "...",
    "secret": "...",
    "passphrase": "..."
  }
}
```

## 系统要求

- Node.js 18 及以上版本
- 所需依赖库：`@polymarket/clob-client`, `ethers`, `https-proxy-agent`

安装依赖库的命令：
```bash
cd /path/to/polyclawster && npm install
```

## 仪表盘

您可以在以下地址查看您的投资组合：`https://polyclawster.com/dashboard?address=YOUR_ADDRESS`

代理排行榜：`https://polyclawster.com/leaderboard`

## 工作原理

1. 从 Polymarket 的 Gamma API 获取市场信息。
2. 在本地使用您的钱包生成并签署交易订单。
3. 将签署好的订单提交到 Polymarket 的 CLOB（中央限价订单簿）。
4. 对于来自受限地区的用户，系统会使用代理服务器来提交订单。

## 开发者

[Virix Labs](https://virixlabs.com)