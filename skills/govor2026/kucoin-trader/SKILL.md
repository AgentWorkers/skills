---
name: kucoin-trader
description: 专业 KuCoin (KC) 交易系统——支持多账户操作，提供现货/保证金/期货交易功能，以及资产转账服务。该系统可用于查询账户余额、转移资产、开仓/平仓，并帮助您管理 KuCoin 投资组合。
metadata: {"openclaw":{"emoji":"🟢","always":true,"requires":{"bins":["node"]}}}
---
# KuCoin Trader 🟢

这是一个专为 KuCoin（KC）设计的专业自动化交易系统，KuCoin 是一家全球性的加密货币交易所。

## 🚀 快速入门

### 设置凭据

将凭据保存到 `~/.openclaw/credentials/kucoin.json` 文件中：
```json
{
  "apiKey": "YOUR_API_KEY",
  "secretKey": "YOUR_SECRET_KEY",
  "passphrase": "YOUR_PASSPHRASE"
}
```

### 环境变量（可选）
```bash
export KUCOIN_API_KEY="your_api_key"
export KUCOIN_SECRET_KEY="your_secret_key"
export KUCOIN_PASSPHRASE="your_passphrase"
```

## 📊 基本查询

| 命令 | 描述 |
|---------|-------------|
| `node scripts/accounts.js` | 列出所有账户余额 |
| `node scripts/market.js --symbol BTC-USDT` | 获取当前价格 |
| `node scripts/query.js` | 查询所有活跃订单 |

## 💰 资产转移

支持的资产类型：`main`、`trade`、`margin`、`isolated`、`futures`

```bash
# Main to Trade
node scripts/transfer.js --from main --to trade --currency USDT --amount 100

# Trade to Futures
node scripts/transfer.js --from trade --to futures --currency USDT --amount 100

# Any account transfer
node scripts/transfer.js --from <FROM> --to <TO> --currency <CURRENCY> --amount <AMOUNT>
```

## ⚡ 现货交易

```bash
# Market Buy
node scripts/spot.js trade --symbol BTC-USDT --side buy --type market --size 0.001

# Limit Buy
node scripts/spot.js trade --symbol ETH-USDT --side buy --type limit --price 2500 --size 0.1

# Market Sell
node scripts/spot.js trade --symbol BTC-USDT --side sell --type market --size 0.001

# Limit Sell
node scripts/spot.js trade --symbol ETH-USDT --side sell --type limit --price 3000 --size 0.1

# Query orders
node scripts/spot.js orders --symbol BTC-USDT

# Cancel order
node scripts/spot.js cancel --orderId xxx
```

## 🏦 保证金交易（跨保证金与隔离保证金）

```bash
# --- Cross Margin (全仓杠杆) ---
# Check borrowable
node scripts/margin.js borrowable --currency USDT

# Borrow
node scripts/margin.js borrow --currency USDT --amount 100

# Repay
node scripts/margin.js repay --currency USDT --amount 50

# Trade with leverage (5x)
node scripts/margin.js trade --symbol BTC-USDT --side buy --size 0.01 --leverage 5

# Query orders
node scripts/margin.js orders --symbol BTC-USDT
node scripts/margin.js all-orders

# --- Isolated Margin (逐仓杠杆) ---
# Check isolated account info
node scripts/margin.js info-isolated --symbol BTC-USDT

# Check borrowable
node scripts/margin.js borrowable-isolated --symbol BTC-USDT

# Borrow/Repay
node scripts/margin.js borrow-isolated --symbol BTC-USDT --amount 0.01
node scripts/margin.js repay-isolated --symbol BTC-USDT --amount 0.01

# Trade with leverage (3x)
node scripts/margin.js trade-isolated --symbol BTC-USDT --side buy --size 0.01 --leverage 3

# Enable/Disable isolated margin
node scripts/margin.js enable
node scripts/margin.js disable

# Query isolated orders
node scripts/margin.js orders-isolated --symbol BTC-USDT
```

## 📈 期货交易

```bash
# Long
node scripts/futures.js trade --symbol BTC-USDT --side buy --size 0.001 --leverage 10

# Short
node scripts/futures.js trade --symbol BTC-USDT --side sell --size 0.001 --leverage 10

# Set leverage
node scripts/futures.js leverage --symbol BTC-USDT --leverage 20
```

## 📈 支持的交易对

| 交易对 | 描述 |
|------|-------------|
| BTC-USDT | 比特币 |
| ETH-USDT | 以太坊 |
| SOL-USDT | Solana |
| XRP-USDT | XRP |
| DOGE-USDT | Dogecoin |
| ADA-USDT | Cardano |
| AVAX-USDT | Avalanche |
| KCS-USDT | KuCoin Token |

## 🏦 账户类型

| 账户类型 | 描述 |
|------|-------------|
| `main` | 资金账户 - 用于存储资产 |
| `trade` | 现货交易账户 - 用于交易 |
| `margin` | 跨保证金账户 - 支持杠杆交易（最高 5 倍） |
| `isolated` | 隔离保证金账户 |
| `futures` | 期货账户 - 用于交易期货合约 |

## ⚠️ 安全规则

1. **在平仓前** 必须确认持仓情况。
2. **在杠杆交易中** 必须设置止损。
3. **没有交易经验时** **切勿** 使用超过 10 倍的杠杆。
4. **在执行交易前** **务必** 核对交易对和交易数量。
5. **在执行大额订单前** **务必** 与用户确认。

## 🔗 链接

- [API 文档](https://docs.kucoin.com/)
- [创建账户](https://www.kucoin.com/r/rf/QBSYNXQD)

---
*支持多账户的 KuCoin 交易工具*