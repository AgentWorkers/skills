---
name: telnyx-account-python
description: >-
  Manage account balance, payments, invoices, webhooks, and view audit logs and
  detail records. This skill provides Python SDK examples.
metadata:
  author: telnyx
  product: account
  language: python
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 账户 - Python

## 安装

```bash
pip install telnyx
```

## 设置

```python
import os
from telnyx import Telnyx

client = Telnyx(
    api_key=os.environ.get("TELNYX_API_KEY"),  # This is the default and can be omitted
)
```

以下所有示例均假设 `client` 已按上述方式初始化。

## 列出审计日志

检索审计日志条目的列表。

`GET /audit_events`

```python
page = client.audit_events.list()
page = page.data[0]
print(page.id)
```

## 获取用户余额详情

`GET /balance`

```python
balance = client.balance.retrieve()
print(balance.data)
```

## 搜索详细记录

在 Telnyx 平台上搜索任何详细记录。

`GET /detail_records`

```python
page = client.detail_records.list()
page = page.data[0]
print(page)
```

## 列出发票

检索分页显示的发票列表。

`GET /invoices`

```python
page = client.invoices.list()
page = page.data[0]
print(page.file_id)
```

## 根据 ID 获取发票

根据唯一的标识符检索单张发票。

`GET /invoices/{id}`

```python
invoice = client.invoices.retrieve(
    id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(invoice.data)
```

## 列出自动充值偏好设置

返回支付自动充值偏好设置。

`GET /payments/auto_recharge_prefs`

```python
auto_recharge_prefs = client.payment.auto_recharge_prefs.list()
print(auto_recharge_prefs.data)
```

## 更新自动充值偏好设置

更新支付自动充值偏好设置。

`PATCH /payments/auto_recharge_prefs`

```python
auto_recharge_pref = client.payment.auto_recharge_prefs.update()
print(auto_recharge_pref.data)
```

## 列出用户标签

列出所有用户标签。

`GET /user_tags`

```python
user_tags = client.user_tags.list()
print(user_tags.data)
```

## 列出 Webhook 交付记录

列出已认证用户的 Webhook 交付记录。

`GET /webhook_deliveries`

```python
page = client.webhook_deliveries.list()
page = page.data[0]
print(page.id)
```

## 根据 ID 查找 Webhook 交付详情

提供 Webhook 交付的调试数据，如时间戳、交付状态和尝试次数。

`GET /webhook_deliveries/{id}`

```python
webhook_delivery = client.webhook_deliveries.retrieve(
    "C9C0797E-901D-4349-A33C-C2C8F31A92C2",
)
print(webhook_delivery.data)
```