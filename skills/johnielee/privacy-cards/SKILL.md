---
name: privacy-cards
description: "创建和管理 Privacy.com 虚拟卡片。这些卡片可用于生成一次性使用的卡片、由商家管理的卡片、用于商品展示的卡片、设置消费限额、暂停或关闭卡片，以及通过 Privacy.com API 查看交易记录。"
---

# 隐私卡管理

通过 Privacy.com 的 API 来管理虚拟卡。

## 设置

### 获取 API 访问权限

1. 在 [Privacy.com](https://privacy.com) 注册一个账户。
2. 发送电子邮件至 **support@privacy.com** 以申请 API 访问权限。
3. 一旦获得批准，您将收到 API 密钥。

### 配置

```bash
export PRIVACY_API_KEY="your-api-key"
```

**环境：**
- 生产环境：`https://api.privacy.com/v1`
- 沙盒环境：`https://sandbox.privacy.com/v1`

所有请求均需包含以下授权头：`Authorization: api-key $PRIVACY_API_KEY`

---

## 创建卡片

```bash
curl -s -X POST "https://api.privacy.com/v1/cards" \
  -H "Authorization: api-key $PRIVACY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "SINGLE_USE",
    "memo": "One-time purchase",
    "spend_limit": 5000,
    "spend_limit_duration": "TRANSACTION"
  }' | jq
```

### 卡片类型
| 类型 | 行为 |
|------|----------|
| `SINGLE_USE` | 在首次交易后关闭 |
| `MERCHANT_LOCKED` | 锁定到指定的商家，仅可在该商家处使用 |
| `UNLOCKED` | 可在任何商家处使用（需要重新授权） |

### 创建参数
| 参数 | 是否必填 | 说明 |
|-----------|----------|-------------|
| `type` | 是 | `SINGLE_USE`, `MERCHANT_LOCKED`, `UNLOCKED` |
| `memo` | 否 | 卡片标签/描述 |
| `spend_limit` | 否 | 消费限额（单位：分） |
| `spend_limit_duration` | 否 | 消费限额的有效期限：一次性、每月、每年或永久 |
| `state` | 否 | 状态：`OPEN`（默认）或 `PAUSED` |
| `funding_token` | 否 | 特定资金来源的 UUID |

### 响应数据
```json
{
  "token": "card-uuid",
  "type": "SINGLE_USE",
  "state": "OPEN",
  "memo": "One-time purchase",
  "last_four": "1234",
  "pan": "4111111111111234",
  "cvv": "123",
  "exp_month": "12",
  "exp_year": "2027",
  "spend_limit": 5000,
  "spend_limit_duration": "TRANSACTION",
  "created": "2024-01-15T10:30:00Z"
}
```

> **注意：** 在生产环境中，`pan`, `cvv`, `exp_month`, `exp_year` 等字段需要企业级访问权限。这些字段在沙盒环境中始终可用。

---

## 查看交易记录

### 查看卡片的全部交易记录
```bash
curl -s "https://api.privacy.com/v1/transactions?card_token={card_token}" \
  -H "Authorization: api-key $PRIVACY_API_KEY" | jq
```

### 按日期范围过滤交易记录
```bash
curl -s "https://api.privacy.com/v1/transactions?card_token={card_token}&begin=2024-01-01&end=2024-01-31" \
  -H "Authorization: api-key $PRIVACY_API_KEY" | jq
```

### 按交易结果过滤交易记录
```bash
# Only approved
curl -s "https://api.privacy.com/v1/transactions?result=APPROVED" \
  -H "Authorization: api-key $PRIVACY_API_KEY" | jq

# Only declined
curl -s "https://api.privacy.com/v1/transactions?result=DECLINED" \
  -H "Authorization: api-key $PRIVACY_API_KEY" | jq
```

### 查询参数
| 参数 | 说明 |
|-----------|-------------|
| `card_token` | 通过卡片 UUID 过滤交易记录 |
| `result` | 交易状态：`APPROVED` 或 `DECLINED` |
| `begin` | 交易开始的日期（格式：YYYY-MM-DD） |
| `end` | 交易结束的日期（格式：YYYY-MM-DD） |
| `page` | 页码（默认值：1） |
| `page_size` | 每页显示的交易记录数量（1-1000，默认值：50） |

### 交易响应数据
```json
{
  "token": "txn-uuid",
  "card_token": "card-uuid",
  "amount": -2500,
  "status": "SETTLED",
  "result": "APPROVED",
  "merchant": {
    "descriptor": "NETFLIX.COM",
    "mcc": "4899",
    "city": "LOS GATOS",
    "state": "CA",
    "country": "USA"
  },
  "created": "2024-01-15T14:22:00Z"
}
```

### 交易状态
`PENDING` → `SETTLING` → `SETTLED`

其他状态：`VOIDED`, `BOUNCED`, `DECLINED`

---

## 快速参考

### 列出所有卡片
```bash
curl -s "https://api.privacy.com/v1/cards" \
  -H "Authorization: api-key $PRIVACY_API_KEY" | jq
```

### 获取单张卡片的详细信息
```bash
curl -s "https://api.privacy.com/v1/cards/{card_token}" \
  -H "Authorization: api-key $PRIVACY_API_KEY" | jq
```

### 暂停卡片的使用
```bash
curl -s -X PATCH "https://api.privacy.com/v1/cards/{card_token}" \
  -H "Authorization: api-key $PRIVACY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"state": "PAUSED"}' | jq
```

### 永久关闭卡片
```bash
curl -s -X PATCH "https://api.privacy.com/v1/cards/{card_token}" \
  -H "Authorization: api-key $PRIVACY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"state": "CLOSED"}' | jq
```

### 更新消费限额
```bash
curl -s -X PATCH "https://api.privacy.com/v1/cards/{card_token}" \
  -H "Authorization: api-key $PRIVACY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"spend_limit": 10000, "spend_limit_duration": "MONTHLY"}' | jq
```

---

## 常见交易拒绝原因

| 代码 | 含义 |
|------|---------|
| `CARD_PAUSED` | 卡片被暂停使用 |
| `CARD_CLOSED` | 卡片已被关闭 |
| `SINGLE_USE_RECHARGED` | 单次使用的卡片已被再次使用 |
| `UNAUTHORIZED_MERCHANT` | 该卡片无法用于指定的商家 |
| `USER_TRANSACTION_LIMIT` | 消费限额已超出 |
| `INSUFFICIENT_FUNDS` | 资金来源出现问题 |

有关所有字段的详细信息，请参阅 [references/api.md](references/api.md)。