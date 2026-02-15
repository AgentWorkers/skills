# K-Trendz荧光棒交易技巧

在K-Trendz的绑定曲线市场上交易K-pop艺术家的荧光棒代币。

## 概述

K-Trendz荧光棒是一种与K-pop艺术家绑定的数字粉丝代币。与套利市场不同，这里采用的是**绑定曲线**系统：
- **每次购买后价格会上涨**（遵循√供应公式）
- **艺术家的受欢迎程度直接影响需求**
- **早期购买者可以从价格上涨中获益**

## 交易策略

这并非套利市场。主要原则如下：
1. **在趋势上升时购买**——`trending_score`上升以及近期新闻表明需求在增加
2. **尽早购买**——`total_supply`较低意味着在曲线上的位置更靠前
3. **关注外部信号**——新闻头条通常会先于平台上的活动出现
4. **在价格上涨期间持有**——绑定曲线机制会奖励耐心持有的用户

## 可用工具

### get_token_price

获取代币的当前价格和受欢迎程度信息。

**接口地址**：`POST /functions/v1/bot-get-token-price`

**请求头**：
```
x-bot-api-key: YOUR_API_KEY
Content-Type: application/json
```

**请求参数**：
```json
{
  "token_id": "7963681970480434413",
  // OR
  "artist_name": "RIIZE"
}
```

**响应内容**：
```json
{
  "success": true,
  "data": {
    "token_id": "7963681970480434413",
    "artist_name": "RIIZE",
    "current_price_usdc": 1.85,
    "buy_cost_usdc": 1.91,
    "sell_refund_usdc": 1.78,
    "price_change_24h": "+5.2",
    "total_supply": 42,
    "trending_score": 1250,
    "votes": 89,
    "follower_count": 156,
    "view_count": 2340,
    "external_signals": {
      "article_count_24h": 3,
      "headlines": [
        {"title": "RIIZE announces world tour dates", "url": "..."},
        {"title": "New single breaks records", "url": "..."}
      ],
      "has_recent_news": true
    },
    "trading_context": {
      "contract_address": "0xfe7791e3078FD183FD1c08dE2F1e4ab732024489",
      "fee_structure": {
        "buy_fee_percent": 3,
        "sell_fee_percent": 2
      }
    }
  }
}
```

**决策依据**：
| 字段 | 含义 | 买入信号 |
|-------|---------|------------|
| `trending_score` | 平台上的互动情况 | 上升 = 市场看涨 |
| `price_change_24h` | 最近的价格波动 | 正面趋势 = 价格将继续上涨 |
| `total_supply` | 持有者数量 | 较低 = 早期买入机会 |
| `externalsignals.article_count_24h` | 新闻报道量 | 高 = 关注度增加 |
| `externalsignals.has_recent_news` | 最近是否有新闻报道 | true = 可能的催化剂 |

---

### buy_fanz_token

购买1个荧光棒代币。

**接口地址**：`POST /functions/v1/bot-buy-token`

**请求头**：
```
x-bot-api-key: YOUR_API_KEY
Content-Type: application/json
```

**请求参数**：
```json
{
  "token_id": "7963681970480434413",
  "max_slippage_percent": 5
}
```

**响应内容**：
```json
{
  "success": true,
  "data": {
    "transaction_id": "abc123",
    "tx_hash": "0x...",
    "token_id": "7963681970480434413",
    "artist_name": "RIIZE",
    "amount": 1,
    "total_cost_usdc": 1.91,
    "remaining_daily_limit": 98.09
  }
}
```

**限制条件**：
- 每笔交易最多购买1个代币（保护绑定曲线机制）
- 每个代理每天最多交易100美元
- 同一区块内的交易会被阻止（防止市场操纵）

---

### sell_fanz_token

出售1个荧光棒代币。

**接口地址**：`POST /functions/v1/bot-sell-token`

**请求头**：
```
x-bot-api-key: YOUR_API_KEY
Content-Type: application/json
```

**请求参数**：
```json
{
  "token_id": "7963681970480434413",
  "min_slippage_percent": 5
}
```

**响应内容**：
```json
{
  "success": true,
  "data": {
    "transaction_id": "def456",
    "tx_hash": "0x...",
    "token_id": "7963681970480434413",
    "artist_name": "RIIZE",
    "amount": 1,
    "net_refund_usdc": 1.78,
    "fee_usdc": 0.04
  }
}
```

---

## 可用代币

| 艺术家 | 代币ID |
|--------|----------|
| K-Trendz Supporters | 12666454296509763493 |
| RIIZE | 7963681970480434413 |
| IVE | 4607865675402095874 |
| Cortis | 13766662462343366758 |
| BTS | 9138265216282739420 |
| All Day Project | 18115915419890895215 |

---

## 费用结构

| 操作 | 费用 | 分配方式 |
|--------|-----|--------------|
| 买入 | 3% | 2% 支付给艺术家，1% 归平台 |
| 卖出 | 2% | 归平台 |

**往返费用**：5%

---

## 交易逻辑示例

```python
# Pseudocode for news-driven trading

def should_buy(token_data):
    signals = token_data['external_signals']
    
    # Strong buy: Recent news + rising trend
    if signals['has_recent_news'] and signals['article_count_24h'] >= 2:
        if token_data['price_change_24h'] and float(token_data['price_change_24h']) > 0:
            return True
    
    # Moderate buy: High trending score, low supply
    if token_data['trending_score'] > 1000 and token_data['total_supply'] < 50:
        return True
    
    return False

def should_sell(token_data, purchase_price):
    current_price = token_data['current_price_usdc']
    
    # Take profit at 10%+
    if current_price > purchase_price * 1.10:
        return True
    
    # Cut loss if no news and price dropping
    signals = token_data['external_signals']
    if not signals['has_recent_news']:
        if token_data['price_change_24h'] and float(token_data['price_change_24h']) < -5:
            return True
    
    return False
```

---

## 交易限制

- **每日交易额**：每个代理每天最多100美元
- **交易频率**：每个代理每天最多100笔交易
- **价格限制**：如果价格在10个时间块内上涨超过20%，交易将暂停

---

## 基础URL

```
https://jguylowswwgjvotdcsfj.supabase.co/functions/v1/
```

---

## 认证

在所有请求中，需要在`x-bot-api-key`头部字段中包含您的API密钥。

如需获取API密钥，请联系K-Trendz团队。