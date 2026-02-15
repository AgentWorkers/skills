---
name: lemonsqueezy-admin
version: 1.0.0
description: Lemon Squeezy商店的管理员命令行界面（Admin CLI）：用于查看订单、订阅信息以及客户资料。
author: abakermi
metadata:
  openclaw:
    emoji: "🍋"
    requires:
      env: ["LEMONSQUEEZY_API_KEY"]
---

# Lemon Squeezy Admin 🍋

通过命令行管理您的 Lemon Squeezy 商店。

## 设置

1. 从 [Lemon Squeezy 设置 > API](https://app.lemonsqueezy.com/settings/api) 获取 API 密钥。
2. 将其设置为：`export LEMONSQUEEZY_API_KEY="your_key"`

## 命令

### 订单
```bash
ls-admin orders --limit 10
# Output: #1234 - $49.00 - john@example.com (Paid)
```

### 订阅
```bash
ls-admin subscriptions
# Output: Active: 15 | MMR: $450
```

### 商店
```bash
ls-admin stores
```