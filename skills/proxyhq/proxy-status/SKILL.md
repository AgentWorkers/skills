---
name: proxy-status
description: 检查代理支付意图（Proxy payment intents）和交易（transactions）的状态。使用方法：`/proxy-status [intent-id]` 或 `/proxy-status` 可查看所有最近的记录。
disable-model-invocation: true
argument-hint: "[intent-id or blank for all]"
---

# 检查支付状态

查看支付请求（payment intents）和交易（transactions）的状态。

## 使用方法

```
/proxy-status              # Show all recent intents
/proxy-status int_abc123   # Show specific intent
```

## 使用说明

### 如果 `$ARGUMENTS` 包含请求 ID（intent ID）：
```
Call: proxy.intents.get { intentId: "$ARGUMENTS" }
Show: status, merchant, amount, created time
If card issued: proxy.transactions.list_for_card
```

### 如果 `$ARGUMENTS` 为空：
```
Call: proxy.intents.list
Group by status and display:
```

## 输出格式

```
📊 Payment Status
─────────────────

⏳ Pending Approval (2)
  • $500.00 - Adobe Creative Cloud
  • $299.00 - Apple Store

✅ Active Cards (3)
  • $49.99 - Amazon (card ready)
  • $25.00 - Uber Eats (card ready)
  • $150.00 - Best Buy (used, $147.32 charged)

✓ Completed (5 this week)
  • $29.99 - Netflix - matched
  • $12.50 - Spotify - matched
  ...
```

## 状态说明

| 状态 | 图标 | 含义 |
|--------|------|---------|
| 待处理 | 🟢 | 卡片已准备好（Card ready） |
| 待审批 | ⏳ | 需要审批 |
| 卡片已发放 | 💳 | 卡片已激活（Card active） |
| 交易成功 | ✅ | 交易已完成 |
| 信息不匹配 | ⚠️ | 金额或商家信息不一致 |
| 被拒绝 | ❌ | 审批被拒绝 |
| 已过期 | ⏰ | 请求已过期 |