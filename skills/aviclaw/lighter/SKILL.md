---
name: lighter
description: 与 Lighter 协议进行交互——这是一个基于 ZK（Zcash-Kernel）技术的订单簿去中心化交易所（DEX）。当您需要在 Lighter 上进行交易、查看价格、管理持仓或查询账户数据时，可以使用该功能。
---
# Lighter 协议

Lighter 是一个基于零知识证明（Zero-Knowledge Proof, ZK）技术的去中心化交易所（DEX），专为零售交易者设计。它提供零费用的交易服务，并且订单执行延迟仅为毫秒级。

## 快速入门

```bash
# Set environment variables
export PRIVATE_KEY="your-private-key"
export LIGHTER_API_KEY="your-api-key"
export LIGHTER_ACCOUNT_INDEX="0"

# Check account
node scripts/account.js

# Get markets
node scripts/markets.js

# Place order
node scripts/order.js --market ETH-USDC --side buy --amount 0.1 --price 3000
```

## 获取凭证

### `PRIVATE_KEY`

您的以太坊钱包私钥（以 `0x` 开头）。

**获取方法：**
1. 打开 MetaMask → 账户详情
2. 点击“导出私钥”
3. 输入密码
4. 复制私钥（私钥以 `0x...` 开头）

**⚠️ 请勿泄露此密钥！** 将私钥存储在环境变量中，切勿将其写入代码中。

### `LIGHTER_API_KEY`

用于访问 Lighter 协议的 API 密钥。

**获取方法：**
1. 访问 https://dashboard.zklighter.io
2. 连接您的钱包
3. 转到“API 密钥”部分
4. 创建新的 API 密钥
5. 复制密钥

**注意：** 某些操作无需 API 密钥即可执行，但会受到速率限制。

### `LIGHTER_ACCOUNT_INDEX`

您的 Lighter 账户索引。

**获取方法：**
1. 访问 https://dashboard.zklighter.io
2. 连接您的钱包
3. 账户索引会显示在仪表板上（通常第一个账户的索引为 `0`）
4. 或者在设置 `PRIVATE_KEY` 后，通过 `node scripts/account.js` 文件查询账户索引。

## Lighter 是什么？

Lighter 是一个完全可验证的去中心化交易所，它基于自定义的零知识证明基础设施构建：
- **零费用**：对零售交易者而言，所有交易均免费
- **毫秒级延迟**：每秒可处理数以万计的订单
- **所有操作均需经过零知识证明**  
- **以太坊安全架构**：基于以太坊的安全性
- **得到支持**：来自 a16z、Dragonfly 和 Coatue 的技术支持

## 主要功能

- **市场数据**：查看市场列表、获取价格信息、查看订单簿
- **交易**：下单/取消订单、管理持仓
- **账户**：查询余额、进行存款和取款
- **WebSocket**：实时市场数据流

## 安装

```bash
cd ~/.openclaw/workspace/skills/lighter
npm install
```

## 使用方法

### 账户操作

```bash
# Check account balance
node scripts/account.js

# Deposit
node scripts/deposit.js --token USDC --amount 1000

# Withdraw  
node scripts/withdraw.js --token USDC --amount 1000 --to 0x...
```

### 市场数据

```bash
# List all markets
node scripts/markets.js

# Get market data for ETH-USDC
node scripts/market.js --market ETH-USDC

# Get order book
node scripts/orderbook.js --market ETH-USDC

# Get recent trades
node scripts/trades.js --market ETH-USDC --limit 50
```

### 订单

```bash
# Place limit order
node scripts/order.js --market ETH-USDC --side buy --amount 0.1 --price 3000 --type limit

# Place market order
node scripts/order.js --market ETH-USDC --side buy --amount 0.1 --type market

# Cancel order
node scripts/cancel.js --order-id 12345

# List open orders
node scripts/orders.js
```

### 持仓

```bash
# Get positions
node scripts/positions.js

# Get position history
node scripts/position-history.js --market ETH-USDC
```

## 架构

```
lighter/
├── SKILL.md              # This file
├── package.json
├── scripts/
│   ├── account.js       # Account info
│   ├── markets.js       # List markets
│   ├── market.js        # Market details
│   ├── orderbook.js     # Order book
│   ├── order.js         # Place/cancel orders
│   ├── orders.js        # List open orders
│   ├── positions.js     # Positions
│   └── trades.js        # Recent trades
└── references/
    └── api.md           # API docs
```

## 环境变量

| 变量 | 说明 | 是否必需 | 获取方法 |
|--------|--------|---------|---------|
| `PRIVATE_KEY` | 钱包私钥（格式为 `0x...`） | 是 | 通过 MetaMask → 账户 → 导出私钥 |
| `LIGHTER_API_KEY` | Lighter 的 API 密钥 | 否 | 访问 https://dashboard.zklighter.io → API 密钥部分 |
| `LIGHTER_ACCOUNT_INDEX` | 账户索引 | 否 | 在 https://dashboard.zklighter.io 上查看（通常为 `0`） |

## 注意事项

- 主网 RPC 地址：https://mainnet.zklighter.elliot.ai
- 链路 ID：300
- 在 Lighter 上进行交易需要支付以太坊作为 gas 费用
- 订单按照价格和时间优先级匹配
- 所有操作都会生成零知识证明
- **测试网**：使用链路 ID 111 或测试网 RPC 进行测试