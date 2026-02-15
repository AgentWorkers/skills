---
name: foreseek
description: 通过 Foreseek，您可以使用自然语言在交易预测市场中进行操作。
  Matches your beliefs to Kalshi contracts and executes trades. Use when 
  user wants to bet on or trade predictions about elections, politics, 
  sports outcomes, economic data (Fed rates, CPI, GDP), crypto prices, 
  weather events, or any real-world event outcomes. Supports viewing 
  positions, parsing predictions, executing market/limit orders, managing
  orders, and checking account status.
metadata:
  clawdbot:
    requires:
      env:
        - FORESEEK_API_KEY
---

# Foreseek - 预测市场交易

通过自然语言在预测市场中进行交易。说出你的预测，系统会为你匹配合适的合约在 Kalshi 平台上执行交易。

## 设置

从 [foreseek.ai/dashboard](https://foreseek.ai/dashboard) 的“API Keys”页面获取你的 API 密钥。

```bash
export FORESEEK_API_KEY="fsk_your_api_key_here"
```

## 快速命令

### 解析预测结果（查找匹配的市场）

将自然语言输入转换为 Kalshi 平台上的相应合约。

```bash
curl -X POST https://jxvtetqmzduvhgiyldgp.supabase.co/functions/v1/foreseek-cli \
  -H "Authorization: Bearer $FORESEEK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"operation": "parse", "prediction": "Fed will cut rates in March"}'
```

**响应：**
```json
{
  "matched": true,
  "confidence": 0.92,
  "direction": "yes",
  "market": {
    "ticker": "KXFED-25MAR-T475",
    "title": "Fed funds rate below 4.75% on March 19",
    "price": 0.35,
    "event_ticker": "KXFED-25MAR",
    "kalshi_url": "https://kalshi.com/markets/kxfed/fed-funds-rate-below-475-on-march-19/kxfed-25mar#market=KXFED-25MAR-T475"
  },
  "insight": "Currently trading at 35¢, implying 35% probability"
}
```

### 执行交易

通过你的账户在 Kalshi 平台上下达交易订单。

```bash
curl -X POST https://jxvtetqmzduvhgiyldgp.supabase.co/functions/v1/foreseek-cli \
  -H "Authorization: Bearer $FORESEEK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "trade",
    "ticker": "KXFED-25MAR-T475",
    "side": "yes",
    "action": "buy",
    "count": 10,
    "type": "market"
  }'
```

**响应：**
```json
{
  "success": true,
  "order": {
    "order_id": "abc123",
    "status": "filled",
    "filled_count": 10,
    "avg_price": 35
  },
  "message": "BUY 10 YES contracts on KXFED-25MAR-T475"
}
```

### 查看持仓

显示你在 Kalshi 平台上的当前未平仓合约。

```bash
curl -X POST https://jxvtetqmzduvhgiyldgp.supabase.co/functions/v1/foreseek-cli \
  -H "Authorization: Bearer $FORESEEK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"operation": "positions"}'
```

**响应：**
```json
{
  "count": 2,
  "positions": [
    {
      "ticker": "KXBTC-120K-JAN",
      "title": "Bitcoin above $120,000",
      "side": "yes",
      "contracts": 25,
      "avg_price": 42,
      "current_price": 48,
      "pnl": 150
    }
  ],
  "is_demo": false
}
```

### 搜索市场

通过关键词或类别浏览可用的市场。

```bash
curl -X POST https://jxvtetqmzduvhgiyldgp.supabase.co/functions/v1/foreseek-cli \
  -H "Authorization: Bearer $FORESEEK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"operation": "markets", "query": "bitcoin", "limit": 5}'
```

### 查看待定订单

显示你在 Kalshi 平台上的待定订单和最近的交易记录。

```bash
curl -X POST https://jxvtetqmzduvhgiyldgp.supabase.co/functions/v1/foreseek-cli \
  -H "Authorization: Bearer $FORESEEK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"operation": "orders"}'
```

**响应：**
```json
{
  "count": 3,
  "orders": [
    {
      "order_id": "abc123",
      "ticker": "KXBTC-120K",
      "side": "yes",
      "action": "buy",
      "status": "pending",
      "count": 10,
      "filled": 5,
      "price": 42,
      "created_at": "2026-01-31T10:00:00Z"
    }
  ],
  "is_demo": false
}
```

### 取消订单

通过订单 ID 取消待定订单。

```bash
curl -X POST https://jxvtetqmzduvhgiyldgp.supabase.co/functions/v1/foreseek-cli \
  -H "Authorization: Bearer $FORESEEK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"operation": "cancel", "order_id": "abc123"}'
```

**响应：**
```json
{
  "success": true,
  "order_id": "abc123",
  "message": "Order abc123 cancelled successfully"
}
```

### 检查账户状态

查看你的订阅等级、使用限制和连接状态。

```bash
curl -X POST https://jxvtetqmzduvhgiyldgp.supabase.co/functions/v1/foreseek-cli \
  -H "Authorization: Bearer $FORESEEK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"operation": "status"}'
```

**响应：**
```json
{
  "tier": "pro",
  "daily_used": 5000,
  "daily_limit": 150000,
  "daily_percent": 3.3,
  "monthly_used": 25000,
  "monthly_limit": 3000000,
  "monthly_percent": 0.8,
  "predictions_used": 2,
  "predictions_limit": 75,
  "is_limited": false,
  "kalshi_connected": true,
  "is_demo": false
}
```

### 查看账户余额

查看你的 Kalshi 账户余额和投资组合价值。

```bash
curl -X POST https://jxvtetqmzduvhgiyldgp.supabase.co/functions/v1/foreseek-cli \
  -H "Authorization: Bearer $FORESEEK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"operation": "balance"}'
```

**响应：**
```json
{
  "balance": 1000.00,
  "available": 850.00,
  "portfolio_value": 150.00,
  "is_demo": false
}
```

### 查看关注列表

查看你保存的市场列表及其当前价格。

```bash
curl -X POST https://jxvtetqmzduvhgiyldgp.supabase.co/functions/v1/foreseek-cli \
  -H "Authorization: Bearer $FORESEEK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"operation": "watchlist"}'
```

**响应：**
```json
{
  "count": 2,
  "watchlist": [
    {
      "ticker": "KXBTC-120K-JAN",
      "title": "Bitcoin above $120,000",
      "price": 48,
      "volume": 125000,
      "status": "open",
      "added_at": "2026-01-15T08:00:00Z"
    }
  ]
}
```

## 预测示例

| 你的预测 | 匹配的市场 |
|--------------|----------------|
| “特朗普在 2028 年获胜” | KXPRES-2028-REP |
| “比特币在月底前涨到 10 万美元以上” | KXBTC-100K-JAN |
| “老鹰队赢得超级碗” | KXNFLSB-PHI |
| “美联储在 3 月降息” | KXFED-25MAR-T475 |
| “下个月 CPI 超过 3%” | KXCPI-FEB-3PCT |
| “英伟达股价达到 200 美元” | KXNVDA-200 |

## 操作参考

| 操作 | 描述 | 范围 | 所需资源 |
|-----------|-------------|-------|-----------------|
| parse   | 解析预测结果   | 是       | 需要 API 密钥       |
| trade    | 执行交易     | 是       | 需要 API 密钥       |
| positions | 查看持仓     | 是       | 需要 API 密钥       |
| markets  | 搜索市场     | 是       | 需要 API 密钥       |
| orders   | 查看待定订单   | 是       | 需要 API 密钥       |
| cancel   | 取消订单     | 是       | 需要 API 密钥       |
| status   | 检查账户状态   | 是       | 需要 API 密钥       |
| balance | 查看账户余额   | 是       | 需要 API 密钥       |
| watchlist | 查看关注列表   | 是       | 需要 API 密钥       |

## 交易参数

| 参数        | 类型        | 是否必填 | 描述                        |
|-----------|-----------|---------|-----------------------------------------|
| operation    | string     | 是       | 操作类型（parse, trade, positions, markets, orders, cancel, status, balance, watchlist） |
| prediction | string     | 是       | 预测内容（自然语言）                 |
| ticker     | string     | 是       | 市场代码（例如：KXBTC-120K-JAN）             |
| side       | string     | 是       | 交易方向（“yes” 或 “no”）                |
| action      | string     | 是       | 交易类型（“buy” 或 “sell”，默认：buy）           |
| count      | number     | 是       | 要交易的合约数量                   |
| type       | string     | 是       | 交易类型（“market” 或 “limit”，默认：market）        |
| yes_price   | number     | 是       | 限价单的买入价格（单位：美分）             |
| no_price   | number     | 是       | 限价单的卖出价格（单位：美分）             |
| query      | string     | 是       | 搜索关键词                     |
| category    | string     | 是       | 过滤市场类别                     |
| limit      | number     | 是       | 每页显示的结果数量（默认：10，最大：50）           |
| order_id    | string     | 是       | 要取消的订单 ID                   |

## 错误处理

**401 - 未经授权**  
→ 请确认你的 API 密钥正确且未被撤销。

**403 - 禁止操作**  
→ 你的 API 密钥权限不允许执行此操作。

**429 - 日使用量限制**  
→ 当日token使用量已达到上限。升级账户以获得更多使用权限：
  - 免费账户：每天约 5 次预测
  - Pro 账户（每月 29 美元）：每天约 75 次预测
  - Ultra 账户（每月 79 美元）：每天约 200 次预测

**400 - 请求错误**  
→ 请在控制台中重新连接你的 Kalshi API 认证信息。

## 市场类别

可用的市场类别（用于过滤）：
- 政治（选举、立法）
- 经济（美联储利率、CPI、GDP、失业率）
- 加密货币（比特币、以太坊价格）
- 体育（NFL、NBA、MLB、足球）
- 娱乐（奥斯卡奖项、流媒体服务）
- 天气（温度、飓风）
- 科技（产品发布、财报）

## 使用要求

1. **注册 Foreseek 账户**：访问 [foreseek.ai](https://foreseek.ai) 进行注册。
2. **连接 Kalshi 平台**：在控制台中配置你的 Kalshi API 密钥。
3. **获取 API 密钥**：在控制台的“API Keys”页面生成 API 密钥。

## 链接

- 网站：https://foreseek.ai
- 控制台：https://foreseek.ai/dashboard
- 文档：https://foreseek.ai/docs