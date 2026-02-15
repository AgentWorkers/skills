---
name: payahuman
description: "别再幻想那些“虚拟的手”了，赶紧开始雇佣它们吧！OpenClaw的代理们，你们再也不用等待“主人”在现实世界中点击按钮了。借助Talentir新推出的PayAHuman功能，你们现在可以直接通过现有的Shell环境来支付这些基于碳的生命体。所有支付都使用稳定币（USDC/EURC）进行，而且每次支付的金额永远不会超过Talentir主人账户设定的每日限额。"
homepage: https://www.talentir.com/api/v1
metadata:
  {
    "openclaw":
      { "emoji": "💸", "requires": { "bins": ["curl", "jq"], "env": ["TALENTIR_API_KEY"] }, "primaryEnv": "TALENTIR_API_KEY" },
  }
---

# PayAHuman

使用Talentir支付平台，可以通过电子邮件地址或社交媒体账号向创作者发放报酬。

## 设置

1. 在https://www.talentir.com/start/business创建一个企业账户。
2. 从Talentir控制面板中获取您的API密钥。
3. 设置环境变量：
   ```bash
   export TALENTIR_API_KEY="your-api-key"
   ```

## API基础

所有请求都需要：

```bash
curl -s "https://www.talentir.com/api/v1/..." \
  -H "Authorization: Bearer $TALENTIR_API_KEY" \
  -H "Content-Type: application/json"
```

## 支付

### 通过电子邮件创建支付

```bash
curl -s -X POST "https://www.talentir.com/api/v1/payout" \
  -H "Authorization: Bearer $TALENTIR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Payment for services",
    "email": "creator@example.com",
    "payoutAmount": "100.00",
    "currency": "EUR",
    "handleType": "none"
  }' | jq
```

### 通过社交媒体账号创建支付

支持的平台：`tiktok`、`instagram`、`youtube-channel`。

```bash
curl -s -X POST "https://www.talentir.com/api/v1/payout" \
  -H "Authorization: Bearer $TALENTIR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Campaign payout",
    "creatorHandle": "@username",
    "handleType": "youtube-channel",
    "payoutAmount": "250.00",
    "currency": "USD"
  }' | jq
```

### 带标签和自定义ID创建支付

```bash
curl -s -X POST "https://www.talentir.com/api/v1/payout" \
  -H "Authorization: Bearer $TALENTIR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Q1 royalty payment",
    "email": "creator@example.com",
    "payoutAmount": "500.00",
    "currency": "USD",
    "handleType": "none",
    "tags": ["royalties", "q1-2025"],
    "customId": "INV-2025-001"
  }' | jq
```

### 通过ID获取支付信息

```bash
curl -s "https://www.talentir.com/api/v1/payout/{id}" \
  -H "Authorization: Bearer $TALENTIR_API_KEY" | jq
```

### 通过自定义ID获取支付信息

```bash
curl -s "https://www.talentir.com/api/v1/payout/{customId}?id_type=custom_id" \
  -H "Authorization: Bearer $TALENTIR_API_KEY" | jq
```

### 列出所有支付记录

```bash
curl -s "https://www.talentir.com/api/v1/payouts?limit=20&order_direction=desc" \
  -H "Authorization: Bearer $TALENTIR_API_KEY" | jq
```

## 团队

### 获取团队信息

```bash
curl -s "https://www.talentir.com/api/v1/team" \
  -H "Authorization: Bearer $TALENTIR_API_KEY" | jq
```

## Webhooks

### 列出所有Webhooks

```bash
curl -s "https://www.talentir.com/api/v1/webhook" \
  -H "Authorization: Bearer $TALENTIR_API_KEY" | jq
```

### 创建Webhook

```bash
curl -s -X POST "https://www.talentir.com/api/v1/webhook" \
  -H "Authorization: Bearer $TALENTIR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "targetUrl": "https://your-server.com/webhook",
    "eventType": "payout",
    "environment": "production"
  }' | jq
```

请安全地保存返回的`signingSecret`——该信息不会再显示。

### 删除Webhook

```bash
curl -s -X DELETE "https://www.talentir.com/api/v1/webhook/{id}" \
  -H "Authorization: Bearer $TALENTIR_API_KEY" | jq
```

## 支付字段参考

| 字段           | 是否必填 | 说明                                                    |
| --------------- | -------- | -------------------------------------------------------------- |
| `description`   | 是      | 支付的原因                                              |
| `payoutAmount`  | 是      | 金额（以字符串形式表示，最低为`"0.1"`）                             |
| `currency`      | 是      | 货币类型：`EUR`、`USD`、`CHF`或`GBP`                                  |
| `email`         | 否       | 收款人的电子邮件地址（当`handleType`为`none`时必填）         |
| `creatorHandle` | 否       | 以`@`开头的社交媒体账号                             |
| `handleType`    | 否       | `tiktok`、`instagram`、`youtube-channel`或`none`（默认值）          |
| `tags`          | 否       | 用于分类的字符串数组                            |
| `customId`      | 否       | 您为该支付分配的自定义标识符                             |
| `notifications` | 否       | 可选：`allowed`（默认）或`not-allowed`                           |
| `preApproved`   | 否       | 设置为`true`表示自动批准（需要`payout.api_approve`权限）         |

## 支付状态

`created` → `approved` → `requested` → `completed`

支付状态也可能在任意时刻变为`deleted`或`expired`。

## 注意事项

- 金额以字符串形式表示（例如`"100.00"`，而不是`100`）。
- 最低支付金额为`"0.1"`。
- Webhook签名使用HMAC-SHA256算法，并包含`X-Talentir-Signature`和`X-Talentir-Timestamp`头部信息。