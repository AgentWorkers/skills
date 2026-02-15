---
emoji: 📈
name: maxxit-lazy-trading
version: 1.0.0
author: Maxxit
description: 通过 Maxxit 的懒惰交易（Lazy Trading）API，在 Ostium 平台上执行永久性交易（即长期有效的交易）。
homepage: https://maxxit.ai
repository: https://github.com/Maxxit-ai/maxxit-latest
disableModelInvocation: true
requires:
  env:
    - MAXXIT_API_KEY
    - MAXXIT_API_URL
metadata:
  openclaw:
    requiredEnv:
      - MAXXIT_API_KEY
      - MAXXIT_API_URL
    bins:
      - curl
    primaryCredential: MAXXIT_API_KEY
---

# Maxxit 懒人交易（Lazy Trading）

通过 Maxxit 的懒人交易 API，在 Ostium 协议上执行永续期货交易。该功能支持基于您编程发送的交易信号进行自动化交易。

## 适用场景

- 用户希望在 Ostium 上执行交易
- 用户希望编程方式发送交易信号
- 用户询问懒人交易账户的详细信息
- 用户想查看自己的 USDC/ETH 余额
- 用户想查看未平仓头寸或投资组合
- 用户想查看已平仓头寸的历史记录或盈亏情况
- 用户提到“懒人交易”、“永续合约”或“期货交易”
- 用户希望自动化自己的交易流程

## 认证

所有请求都需要一个以 `lt_` 为前缀的 API 密钥。可以通过以下方式传递该密钥：
- 在请求头中添加：`X-API-KEY: lt_你的_api_key`
- 或者：`Authorization: Bearer lt_你的_api_key`

## API 端点

### 获取账户详情

检索懒人交易账户信息，包括代理状态、Telegram 连接状态和交易偏好设置。

```bash
curl -L -X GET "${MAXXIT_API_URL}/api/lazy-trading/programmatic/club-details" \
  -H "X-API-KEY: ${MAXXIT_API_KEY}"
```

**响应：**
```json
{
  "success": true,
  "user_wallet": "0x...",
  "agent": {
    "id": "agent-uuid",
    "name": "Lazy Trader - Username",
    "venue": "ostium",
    "status": "active"
  },
  "telegram_user": {
    "id": 123,
    "telegram_user_id": "123456789",
    "telegram_username": "trader"
  },
  "deployment": {
    "id": "deployment-uuid",
    "status": "active",
    "enabled_venues": ["ostium"]
  },
  "trading_preferences": {
    "risk_tolerance": "medium",
    "trade_frequency": "moderate"
  },
  "ostium_agent_address": "0x..."
}
```

### 发送交易信号

发送一个交易信号，该信号将由您的懒人交易代理进行处理。

```bash
curl -L -X POST "${MAXXIT_API_URL}/api/lazy-trading/programmatic/send-message" \
  -H "X-API-KEY: ${MAXXIT_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"message": "Long BTC 10x leverage, entry 65000, TP 70000, SL 62000"}'
```

**请求体：**
```json
{
  "message": "Your trading signal text"
}
```

**响应：**
```json
{
  "success": true,
  "message_id": "api_0x..._1234567890_abc123",
  "post_id": 456
}
```

### 获取账户余额

检索用户 Ostium 钱包地址的 USDC 和 ETH 余额。

**注意：** 用户的 Ostium 钱包地址（`user_wallet`）可以通过 `/api/lazy-trading/programmatic/club-details` 端点获取。

```bash
curl -L -X POST "${MAXXIT_API_URL}/api/lazy-trading/programmatic/balance" \
  -H "X-API-KEY: ${MAXXIT_API_KEY}" \
  -H "Content-Type: application/json" \
  -d "{"address": "0x..."}"
```

**响应：**
```json
{
  "success": true,
  "address": "0x...",
  "usdcBalance": "1000.50",
  "ethBalance": "0.045"
}
```

### 获取投资组合头寸

获取用户 Ostium 交易账户的所有未平仓头寸。

**注意：** 用户的 Ostium 钱包地址可以通过 `/api/lazy-trading/programmatic/club-details` 端点获取。

```bash
curl -L -X POST "${MAXXIT_API_URL}/api/lazy-trading/programmatic/positions" \
  -H "X-API-KEY: ${MAXXIT_API_KEY}" \
  -H "Content-Type: application/json" \
  -d "{"address": "0x..."}"
```

**请求体：**
```json
{
  "address": "0x..."  // User's Ostium wallet address (required)
}
```

**响应：**
```json
{
  "success": true,
  "positions": [
    {
      "market": "BTC",
      "marketFull": "BTC/USD",
      "side": "long",
      "collateral": 100.0,
      "entryPrice": 95000.0,
      "leverage": 10.0,
      "tradeId": "12345",
      "notionalUsd": 1000.0,
      "totalFees": 2.50,
      "stopLossPrice": 85500.0,
      "takeProfitPrice": 0.0
    }
  ],
  "totalPositions": 1
}
```

### 获取头寸历史记录

获取某个地址的原始交易历史记录（包括已开仓、已平仓、已取消的订单等）。

**注意：** 用户的 Ostium 钱包地址可以通过 `/api/lazy-trading/programmatic/club-details` 端点获取（参见上述“获取账户余额”部分）。

```bash
curl -L -X POST "${MAXXIT_API_URL}/api/lazy-trading/programmatic/history" \
  -H "X-API-KEY: ${MAXXIT_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"address": "0x...", "count": 50}'
```

**请求体：**
```json
{
  "address": "0x...",  // User's Ostium wallet address (required)
  "count": 50           // Number of recent orders to retrieve (default: 50)
}
```

**响应：**
```json
{
  "success": true,
  "history": [
    {
      "market": "ETH",
      "side": "long",
      "collateral": 50.0,
      "leverage": 5,
      "price": 3200.0,
      "pnlUsdc": 15.50,
      "profitPercent": 31.0,
      "totalProfitPercent": 31.0,
      "rolloverFee": 0.05,
      "fundingFee": 0.10,
      "executedAt": "2025-02-10T15:30:00Z",
      "tradeId": "trade_123"
    }
  ],
  "count": 25
}
```

## 信号格式示例

懒人交易系统支持处理自然语言形式的交易信号。以下是一些示例：

### 开仓指令
- `"以 5 倍杠杆买入 ETH，入场价格为 3200"`
- `"以 10 倍杠杆卖出 BTC，止盈价格为 60000，止损价格为 68000"`
- `"买入价值 100 USDC 的 ETH 永续合约"`

### 带有风险管理的指令
- `"以 3 倍杠杆买入 SOL，入场价格为 150，盈利目标为 180，止损价格为 140"`
- `"以 5 倍杠杆卖出 AVAX，风险控制在投资组合的 2% 内"`

### 平仓指令
- `"平仓 ETH 多头头寸"`
- `"卖出 BTC 空头头寸并获利"`

## 环境变量

| 变量 | 描述 | 示例 |
|----------|-------------|---------|
| `MAXXIT_API_KEY` | 懒人交易 API 密钥（以 `lt_` 开头） | `lt_abc123...` |
| `MAXXIT_API_URL` | Maxxit API 基本地址 | `https://maxxit.ai` |

## 错误处理

| 状态码 | 含义 |
|-------------|---------|
| 401 | API 密钥无效或缺失 |
| 404 | 未找到懒人交易代理（请先完成设置） |
| 400 | 信号内容缺失或无效 |
| 405 | HTTP 方法错误 |
| 500 | 服务器错误 |

## 入门步骤

1. **设置懒人交易**：访问 https://maxxit.ai/lazy-trading，连接您的钱包并配置代理设置。
2. **生成 API 密钥**：进入您的仪表板并创建 API 密钥。
3. **配置环境变量**：设置 `MAXXIT_API_KEY` 和 `MAXXIT_API_URL`。
4. **开始交易**：使用此功能发送交易信号！

## 安全提示

- 请勿泄露您的 API 密钥。
- API 密钥可以在仪表板上随时撤销和重新生成。
- 所有交易都在链上执行，并使用您委托的钱包权限进行操作。