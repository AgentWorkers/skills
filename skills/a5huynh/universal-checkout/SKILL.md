---
name: zinc-orders
description: 通过 Zinc API (zinc.com) 来放置、列出和检索订单。当用户想要从在线零售商购买产品、查看订单状态、列出最近的交易记录，或执行任何与 Zinc 电子商务订单 API 相关的操作时，可以使用此功能。需要设置 ZINC_API_KEY 环境变量。
---

# 使用 Zinc API 下单与管理订单

您可以通过 Zinc API (`https://api.zinc.com`) 在在线零售商上下单和管理订单。

## 先决条件

- 必须设置环境变量 `ZINC_API_KEY`。您可以从 <https://app.zinc.com> 获取该密钥。

## 认证

所有请求均使用 Bearer Token 进行认证：

```
Authorization: Bearer $ZINC_API_KEY
```

## API 端点

### 创建订单 — `POST /orders`

提交新订单。订单处理是异步进行的。

**必填字段：**

- `products` — 一个包含 `{ url, quantity?, variant? }` 对象的数组
  - `url`：支持零售商上的产品页面直接链接
  - `quantity`：整数（默认值为 1）
  - `variant`：一个包含 `{ label, value }` 的数组，用于表示尺寸/颜色等信息
- `shipping_address` — 一个对象，包含 `first_name`、`last_name`、`address_line1`、`address_line2`、`city`、`state`（两位字母的州名）、`postal_code`、`phone_number`、`country`（ISO 2 位国家代码，例如 "US"）等字段
- `max_price` — 整数，表示订单的最高价格（单位：分）

**可选字段：**

- `idempotency_key` — 一个字符串（最长 36 个字符），用于防止重复下单
- `retailer_credentials_id` — 一个简短的 ID，例如 `zn_acct_XXXXXXXX`
- `metadata` — 随意的键值对对象
- `po_number` — 采购订单编号字符串

**响应：** 包含订单信息的对象，包括 `id`（UUID）、`status`、`items`、`shipping_address`、`created_at`、`tracking_numbers` 等字段

**订单状态：** `pending` → `in_progress` → `order_placed` | `order_failed` | `cancelled`

### 列出订单 — `GET /orders`

返回一个包含订单对象的数组 `{ orders: [...] }`。

### 获取订单详情 — `GET /orders/{id}`

根据订单的 UUID 获取单个订单的详细信息。

## 示例：下单

```bash
curl -X POST https://api.zinc.com/orders \
  -H "Authorization: Bearer $ZINC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "products": [{ "url": "https://example.com/product", "quantity": 1 }],
    "max_price": 5000,
    "shipping_address": {
      "first_name": "Jane",
      "last_name": "Doe",
      "address_line1": "123 Main St",
      "city": "San Francisco",
      "state": "CA",
      "postal_code": "94105",
      "phone_number": "5551234567",
      "country": "US"
    }
  }'
```

## 错误处理

有关完整的错误代码参考，请参阅 [references/errors.md](references/errors.md)。

**关键点：**

- HTTP 错误会返回 `{ code, message, details }` 的格式
- 订单处理失败会在 Webhook 的订单响应中以 `error_type` 的形式显示
- 常见错误原因包括：`max_price_exceeded`（价格超出限制）、`product_out_of_stock`（商品缺货）、`invalid_shipping_address`（地址无效）

## 订单状态跟踪

订单处理是异步进行的，通常需要 **5–10 分钟**。下单后：

1. 在订单创建后约 7 分钟，安排一个 cron 作业来检查订单状态。
2. 使用 `GET /orders/{id}` 来查询订单状态。
3. 将查询结果通过相同的方式反馈给用户。
4. 如果订单仍处于 `pending` 或 `in_progress` 状态，再次安排检查（间隔 5 分钟）。

**终端状态：** `order_placed`、`order_failed`、`cancelled` — 停止检查。
**非终端状态：** `pending`、`in_progress` — 间隔 3–5 分钟再次检查。

**示例 cron 作业（用于通知用户）：**

```json
{
  "name": "zinc-order-check-<short_id>",
  "schedule": { "kind": "at", "at": "<ISO-8601 ~7min from now>" },
  "payload": {
    "kind": "agentTurn",
    "message": "Check Zinc order <order_id> via GET https://api.zinc.com/orders/<order_id>"
  },
  "sessionTarget": "isolated",
  "delivery": {
    "mode": "announce",
    "channel": "<channel>",
    "to": "<channel_id>"
  }
}
```

## 安全性注意事项**

- 在提交订单（`POST /orders`）之前，务必先与用户确认。
- 查看订单信息（`GET` 请求）是安全的。
- 在提交订单前，请确保 `max_price` 的设置合理。