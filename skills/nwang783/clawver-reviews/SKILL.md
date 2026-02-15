---
name: clawver-reviews
description: 处理 Clawver 客户评价：监控评分，撰写回复，跟踪用户情绪趋势。在需要了解客户反馈、评价或声誉管理相关情况时使用这些数据。
version: 1.1.0
homepage: https://clawver.store
metadata: {"openclaw":{"emoji":"⭐","homepage":"https://clawver.store","requires":{"env":["CLAW_API_KEY"]},"primaryEnv":"CLAW_API_KEY"}}
---

# Clawver 评论管理

在您的 Clawver 商店中管理客户评论，监控评分，回应反馈，并维护商店的声誉。

## 先决条件

- `CLAW_API_KEY` 环境变量
- 已有活跃的商店且订单已完成

有关 `claw-social` 提供的特定平台上的优秀和不良 API 模式的详细信息，请参阅 `references/api-examples.md`。

## 查看评论

### 查看所有评论

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
        "id": "review_abc123",
        "orderId": "order_xyz789",
        "productId": "prod_456",
        "rating": 5,
        "title": "Amazing quality!",
        "body": "The wallpapers are stunning.",
        "reviewerName": "John D.",
        "reviewerEmail": "john@example.com",
        "createdAt": "2024-01-15T10:30:00Z",
        "updatedAt": "2024-01-15T10:30:00Z"
      },
      {
        "id": "review_def456",
        "orderId": "order_abc123",
        "productId": "prod_789",
        "rating": 3,
        "body": "Good quality but shipping took longer than expected.",
        "reviewerName": "Jane S.",
        "reviewerEmail": "jane@example.com",
        "createdAt": "2024-01-14T08:15:00Z",
        "updatedAt": "2024-01-14T09:00:00Z",
        "response": {
          "body": "Thank you for your feedback! We're working with our shipping partner to improve delivery times.",
          "createdAt": "2024-01-14T09:00:00Z"
        }
      }
    ]
  },
  "pagination": {
    "cursor": "next_page_id",
    "hasMore": false,
    "limit": 20
  }
}
```

### 分页

```bash
curl "https://api.clawver.store/v1/stores/me/reviews?limit=20&cursor=abc123" \
  -H "Authorization: Bearer $CLAW_API_KEY"
```

### 过滤未回复的评论

```python
response = api.get("/v1/stores/me/reviews")
reviews = response["data"]["reviews"]
unanswered = [r for r in reviews if not r.get("response")]
print(f"Unanswered reviews: {len(unanswered)}")
```

## 回复评论

```bash
curl -X POST https://api.clawver.store/v1/reviews/{reviewId}/respond \
  -H "Authorization: Bearer $CLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "body": "Thank you for your kind review! We appreciate your support."
  }'
```

**响应要求：**
- 回复内容长度不超过 1000 个字符
- 重新回复会替换原有的评论内容
- 建议使用专业的语气

## 评论 Webhook

当有新评论发布时收到通知：

```bash
curl -X POST https://api.clawver.store/v1/webhooks \
  -H "Authorization: Bearer $CLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://your-server.com/webhook",
    "events": ["review.received"],
    "secret": "your-secret-min-16-chars"
  }'
```

**Webhook 数据包：**
```json
{
  "event": "review.received",
  "timestamp": "2024-01-15T10:30:00Z",
  "data": {
    "reviewId": "review_abc123",
    "orderId": "order_xyz789",
    "rating": 5
  }
}
```

**签名格式：**
```
X-Claw-Signature: sha256=abc123...
```

**验证（Node.js）：**
```javascript
const crypto = require('crypto');

function verifyWebhook(body, signature, secret) {
  const expected = 'sha256=' + crypto
    .createHmac('sha256', secret)
    .update(body)
    .digest('hex');
  return crypto.timingSafeEqual(
    Buffer.from(signature),
    Buffer.from(expected)
  );
}
```

## 回复模板

### 正面评论（4-5 星）

**通用感谢语：**
```
Thank you for your wonderful review! We're thrilled you love the product. Your support means everything to us!
```

**针对重复购买的客户：**
```
Thank you for another great review! We truly appreciate your continued support.
```

**针对详细评论：**
```
Thank you for taking the time to write such a thoughtful review! Feedback like yours helps other customers and motivates us to keep creating.
```

### 中立评论（3 星）

**表示感谢并承诺改进：**
```
Thank you for your honest feedback! We're always looking to improve. If there's anything specific we can do better, please reach out—we'd love to hear from you.
```

### 负面评论（1-2 星）

**道歉并提供解决方案：**
```
We're sorry to hear about your experience. This isn't the standard we aim for. Please contact us at [email] so we can make this right.
```

**针对配送问题（POD）：**
```
We apologize for the shipping delay. We're working with our fulfillment partner to improve delivery times. Thank you for your patience and feedback.
```

**针对产品问题：**
```
We're sorry the product didn't meet your expectations. We'd like to understand more about what went wrong. Please reach out to us so we can resolve this for you.
```

## 分析

### 来自商店分析的总体评分

```bash
curl https://api.clawver.store/v1/stores/me/analytics \
  -H "Authorization: Bearer $CLAW_API_KEY"
```

回复中会显示产品的 `averageRating` 和 `reviewsCount`。

### 评分分布

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

## 自动化评论管理

### 每日评论检查

```python
def check_and_respond_to_reviews():
    response = api.get("/v1/stores/me/reviews")
    reviews = response["data"]["reviews"]
    
    for review in reviews:
        # Skip if already responded
        if review.get("response"):
            continue
        
        # Auto-respond based on rating
        if review["rating"] >= 4:
            response_text = "Thank you for your wonderful review! We're thrilled you love the product."
        elif review["rating"] == 3:
            response_text = "Thank you for your feedback! We're always looking to improve."
        else:
            # Flag for manual review
            print(f"Negative review needs attention: {review['id']}")
            continue
        
        api.post(f"/v1/reviews/{review['id']}/respond", {
            "body": response_text
        })
        print(f"Responded to review {review['id']}")
```

### 情感分析

```python
def check_sentiment_trend():
    response = api.get("/v1/stores/me/reviews")
    reviews = response["data"]["reviews"]
    
    # Get last 10 reviews (already sorted by date)
    recent = reviews[:10]
    
    if not recent:
        return
    
    avg_rating = sum(r["rating"] for r in recent) / len(recent)
    negative_count = sum(1 for r in recent if r["rating"] <= 2)
    
    if avg_rating < 3.5:
        print("Warning: Recent review sentiment is declining")
    
    if negative_count >= 3:
        print("Warning: Multiple negative reviews in recent batch")
```

## 最佳实践

1. **快速回复** - 尽量在 24 小时内回复
2. **保持专业** - 避免 defensive 或争论性的回复
3. **将复杂问题转交给客服** - 对于复杂问题，邀请客户通过电子邮件联系
4. **感谢每一位评论者** - 即使是负面评论，也值得感谢
5. **从反馈中学习** - 利用反馈中的共同问题来改进产品
6. **不要激励评论** - 绝不要为正面评论提供折扣

## 评论对商店的影响

- 评论会显示在产品页面上
- 平均评分会显示在商店简介中
- 更高的评分有助于提高商店在市场上的可见度
- 回复评论有助于建立与未来买家的信任