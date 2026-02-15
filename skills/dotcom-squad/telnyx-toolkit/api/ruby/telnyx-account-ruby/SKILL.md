---
name: telnyx-account-ruby
description: >-
  Manage account balance, payments, invoices, webhooks, and view audit logs and
  detail records. This skill provides Ruby SDK examples.
metadata:
  author: telnyx
  product: account
  language: ruby
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 账户 - Ruby

## 安装

```bash
gem install telnyx
```

## 设置

```ruby
require "telnyx"

client = Telnyx::Client.new(
  api_key: ENV["TELNYX_API_KEY"], # This is the default and can be omitted
)
```

以下所有示例均假设 `client` 已按照上述方式初始化。

## 列出审计日志

检索审计日志条目的列表。

`GET /audit_events`

```ruby
page = client.audit_events.list

puts(page)
```

## 获取用户余额详情

`GET /balance`

```ruby
balance = client.balance.retrieve

puts(balance)
```

## 搜索详细记录

在 Telnyx 平台上搜索任何详细记录。

`GET /detail_records`

```ruby
page = client.detail_records.list

puts(page)
```

## 列出发票

检索分页显示的发票列表。

`GET /invoices`

```ruby
page = client.invoices.list

puts(page)
```

## 根据 ID 获取发票

根据唯一标识符检索单张发票。

`GET /invoices/{id}`

```ruby
invoice = client.invoices.retrieve("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(invoice)
```

## 列出自动充值偏好设置

返回支付自动充值偏好设置。

`GET /payments/auto_recharge_prefs`

```ruby
auto_recharge_prefs = client.payment.auto_recharge_prefs.list

puts(auto_recharge_prefs)
```

## 更新自动充值偏好设置

更新支付自动充值偏好设置。

`PATCH /payments/auto_recharge_prefs`

```ruby
auto_recharge_pref = client.payment.auto_recharge_prefs.update

puts(auto_recharge_pref)
```

## 列出用户标签

列出所有用户标签。

`GET /user_tags`

```ruby
user_tags = client.user_tags.list

puts(user_tags)
```

## 列出 Webhook 交付记录

列出已认证用户的 Webhook 交付记录。

`GET /webhook_deliveries`

```ruby
page = client.webhook_deliveries.list

puts(page)
```

## 根据 ID 查找 Webhook 交付详情

提供 Webhook 交付的调试数据，如时间戳、交付状态和尝试次数。

`GET /webhook_deliveries/{id}`

```ruby
webhook_delivery = client.webhook_deliveries.retrieve("C9C0797E-901D-4349-A33C-C2C8F31A92C2")

puts(webhook_delivery)
```