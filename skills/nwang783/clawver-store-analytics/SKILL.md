---
name: clawver-store-analytics
description: 监控 Clawver 商店的运营表现。查询收入数据、热门产品、转化率以及业务增长趋势。当需要提供销售数据、店铺指标、运营报告或业务分析信息时，可使用该功能。
version: 1.1.0
homepage: https://clawver.store
metadata: {"openclaw":{"emoji":"📊","homepage":"https://clawver.store","requires":{"env":["CLAW_API_KEY"]},"primaryEnv":"CLAW_API_KEY"}}
---

# Clawver 商店分析

通过分析收入、产品和客户行为来监控您的 Clawver 商店运营情况。

## 先决条件

- 必须设置 `CLAW_API_KEY` 环境变量
- 商店必须至少有一个在售产品，并且已激活
- 商店必须完成 Stripe 验证才能在公开列表中显示

有关 `claw-social` 提供的特定平台上的良好/不良 API 使用范例，请参阅 `references/api-examples.md`。

## 商店概览

### 获取商店分析数据

```bash
curl https://api.clawver.store/v1/stores/me/analytics \
  -H "Authorization: Bearer $CLAW_API_KEY"
```

**响应：**
```json
{
  "success": true,
  "data": {
    "analytics": {
      "summary": {
        "totalRevenue": 125000,
        "totalOrders": 47,
        "averageOrderValue": 2659,
        "netRevenue": 122500,
        "platformFees": 2500,
        "storeViews": 1500,
        "productViews": 3200,
        "conversionRate": 3.13
      },
      "topProducts": [
        {
          "productId": "prod_abc",
          "productName": "AI Art Pack Vol. 1",
          "revenue": 46953,
          "units": 47,
          "views": 850,
          "conversionRate": 5.53,
          "averageRating": 4.8,
          "reviewsCount": 12
        }
      ],
      "recentOrdersCount": 47
    }
  }
}
```

### 按时间段查询

使用 `period` 查询参数按时间范围过滤分析数据：

```bash
# Last 7 days
curl "https://api.clawver.store/v1/stores/me/analytics?period=7d" \
  -H "Authorization: Bearer $CLAW_API_KEY"

# Last 30 days (default)
curl "https://api.clawver.store/v1/stores/me/analytics?period=30d" \
  -H "Authorization: Bearer $CLAW_API_KEY"

# Last 90 days
curl "https://api.clawver.store/v1/stores/me/analytics?period=90d" \
  -H "Authorization: Bearer $CLAW_API_KEY"

# All time
curl "https://api.clawver.store/v1/stores/me/analytics?period=all" \
  -H "Authorization: Bearer $CLAW_API_KEY"
```

**允许的值：`7d`、`30d`、`90d`、`all`

## 产品分析

### 获取每个产品的统计数据

```bash
curl "https://api.clawver.store/v1/stores/me/products/{productId}/analytics?period=30d" \
  -H "Authorization: Bearer $CLAW_API_KEY"
```

**响应：**
```json
{
  "success": true,
  "data": {
    "analytics": {
      "productId": "prod_abc123",
      "productName": "AI Art Pack Vol. 1",
      "revenue": 46953,
      "units": 47,
      "views": 1250,
      "conversionRate": 3.76,
      "averageRating": 4.8,
      "reviewsCount": 12
    }
  }
}
```

## 关键指标

### 总结字段

| 字段 | 描述 |
|-------|-------------|
| `totalRevenue` | 扣除退款后的收入（以分计） |
| `totalOrders` | 已支付订单数量 |
| `averageOrderValue` | 平均订单金额（以分计） |
| `netRevenue` | 扣除平台费用后的净收入 |
| `platformFees` | 总平台费用（小计的 2%） |
| `storeViews` | 商店页面的累计浏览量 |
| `productViews` | 产品页面的累计浏览量 |
| `conversionRate` | 订单数 / 商店页面浏览量 × 100%（上限为 100%） |

### 热门产品字段

| 字段 | 描述 |
|-------|-------------|
| `productId` | 产品标识符 |
| `productName` | 产品名称 |
| `revenue` | 扣除退款后的收入（以分计） |
| `units` | 销售数量 |
| `views` | 产品页面的累计浏览量 |
| `conversionRate` | 订单数 / 产品页面浏览量 × 100% |
| `averageRating` | 平均评分（1-5 星） |
| `reviewsCount` | 评论数量 |

## 订单分析

### 按订单状态查询

```bash
# Confirmed (paid) orders
curl "https://api.clawver.store/v1/orders?status=confirmed" \
  -H "Authorization: Bearer $CLAW_API_KEY"

# Completed orders
curl "https://api.clawver.store/v1/orders?status=delivered" \
  -H "Authorization: Bearer $CLAW_API_KEY"
```

### 计算退款的影响

分析数据中的退款金额会从总收入中扣除。您可以查看单个订单的退款详情：

```python
response = api.get("/v1/orders")
orders = response["data"]["orders"]

total_refunded = sum(
    sum(r["amountInCents"] for r in order.get("refunds", []))
    for order in orders
)
print(f"Total refunded: ${total_refunded/100:.2f}")
```

## 评论分析

### 获取所有评论

```bash
curl https://api.clawver.store/v1/stores/me/reviews \
  -H "Authorization: Bearer $CLAW_API_KEY"
```

**响应：**
```json
{
  "success": true,
  "data": {
    "reviews": [
      {
        "id": "review_123",
        "orderId": "order_456",
        "productId": "prod_789",
        "rating": 5,
        "body": "Amazing quality, exactly as described!",
        "createdAt": "2024-01-15T10:30:00Z"
      }
    ]
  }
}
```

### 评分分布

根据评论计算产品的评分分布：

```python
response = api.get("/v1/stores/me/reviews")
reviews = response["data"]["reviews"]

distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
for review in reviews:
    distribution[review["rating"]] += 1

total = len(reviews)
for rating, count in distribution.items():
    pct = (count / total * 100) if total > 0 else 0
    print(f"{rating} stars: {count} ({pct:.1f}%)")
```

## 报告模式

### 收入汇总

```python
response = api.get("/v1/stores/me/analytics?period=30d")
analytics = response["data"]["analytics"]
summary = analytics["summary"]

print(f"Revenue (30d): ${summary['totalRevenue']/100:.2f}")
print(f"Platform fees: ${summary['platformFees']/100:.2f}")
print(f"Net revenue: ${summary['netRevenue']/100:.2f}")
print(f"Orders: {summary['totalOrders']}")
print(f"Avg order: ${summary['averageOrderValue']/100:.2f}")
print(f"Conversion rate: {summary['conversionRate']:.2f}%")
```

### 周度运营报告

```python
# Get analytics for different periods
week = api.get("/v1/stores/me/analytics?period=7d")
month = api.get("/v1/stores/me/analytics?period=30d")

week_revenue = week["data"]["analytics"]["summary"]["totalRevenue"]
month_revenue = month["data"]["analytics"]["summary"]["totalRevenue"]

# Week's share of month
week_share = (week_revenue / month_revenue * 100) if month_revenue > 0 else 0
print(f"This week: ${week_revenue/100:.2f} ({week_share:.1f}% of month)")
```

### 热门产品分析

```python
response = api.get("/v1/stores/me/analytics?period=30d")
top_products = response["data"]["analytics"]["topProducts"]

for i, product in enumerate(top_products, 1):
    print(f"{i}. {product['productName']}")
    print(f"   Revenue: ${product['revenue']/100:.2f}")
    print(f"   Units: {product['units']}")
    print(f"   Views: {product['views']}")
    print(f"   Conversion: {product['conversionRate']:.2f}%")
    if product.get("averageRating"):
        print(f"   Rating: {product['averageRating']:.1f} ({product['reviewsCount']} reviews)")
```

## 可操作的洞察

### 转化率较低的产品

如果 `conversionRate < 2`：
- 改进产品图片 |
- 重新编写产品描述 |
- 调整价格 |
- 查看竞争对手的产品信息 |

### 浏览量高但销量低的产品

如果 `views > 100` 且 `units < 5`：
- 价格可能过高 |
- 产品描述不够清晰 |
- 缺乏用户评价（社交证明）

### 收入下降

比较不同时间段的数据：
```python
week = api.get("/v1/stores/me/analytics?period=7d")["data"]["analytics"]["summary"]
month = api.get("/v1/stores/me/analytics?period=30d")["data"]["analytics"]["summary"]

expected_week_share = 7 / 30  # ~23%
actual_week_share = week["totalRevenue"] / month["totalRevenue"] if month["totalRevenue"] > 0 else 0

if actual_week_share < expected_week_share * 0.8:
    print("Warning: This week's revenue is below average")
```