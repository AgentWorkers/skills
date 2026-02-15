---
name: telnyx-numbers-ruby
description: >-
  Search for available phone numbers by location and features, check coverage,
  and place orders. Use when acquiring new phone numbers. This skill provides
  Ruby SDK examples.
metadata:
  author: telnyx
  product: numbers
  language: ruby
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 |

# Telnyx 数字服务 - Ruby

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

## 获取国家覆盖范围

`GET /country_coverage`

```ruby
country_coverage = client.country_coverage.retrieve

puts(country_coverage)
```

## 获取特定国家的覆盖范围

`GET /country_coverage/countries/{country_code}`

```ruby
response = client.country_coverage.retrieve_country("US")

puts(response)
```

## 创建库存覆盖请求

用于创建库存覆盖请求。

`GET /inventory_coverage`

```ruby
inventory_coverages = client.inventory_coverage.list

puts(inventory_coverages)
```

## 列出号码预订信息

获取分页显示的号码预订信息。

`GET /number_reservations`

```ruby
page = client.number_reservations.list

puts(page)
```

## 创建号码预订

为多个号码创建号码预订。

`POST /number_reservations`

```ruby
number_reservation = client.number_reservations.create

puts(number_reservation)
```

## 获取号码预订信息

获取单个号码的预订信息。

`GET /number_reservations/{numberreservation_id}`

```ruby
number_reservation = client.number_reservations.retrieve("number_reservation_id")

puts(number_reservation)
```

## 延长号码预订有效期

延长所有号码的预订有效期。

`POST /number_reservations/{numberreservation_id}/actions/extend`

```ruby
response = client.number_reservations.actions.extend_("number_reservation_id")

puts(response)
```

## 列出号码订单信息

获取分页显示的号码订单信息。

`GET /number_orders`

```ruby
page = client.number_orders.list

puts(page)
```

## 创建号码订单

创建号码订单。

`POST /number_orders`

```ruby
number_order = client.number_orders.create

puts(number_order)
```

## 获取号码订单信息

获取现有的号码订单信息。

`GET /number_orders/{number_order_id}`

```ruby
number_order = client.number_orders.retrieve("number_order_id")

puts(number_order)
```

## 更新号码订单信息

更新号码订单信息。

`PATCH /number_orders/{number_order_id}`

```ruby
number_order = client.number_orders.update("number_order_id")

puts(number_order)
```

## 列出号码块订单信息

获取分页显示的号码块订单信息。

`GET /number_block_orders`

```ruby
page = client.number_block_orders.list

puts(page)
```

## 创建号码块订单

创建号码块订单。

`POST /number_block_orders` — 必需参数：`starting_number`, `range`

```ruby
number_block_order = client.number_block_orders.create(range: 10, starting_number: "+19705555000")

puts(number_block_order)
```

## 获取号码块订单信息

获取现有的号码块订单信息。

`GET /number_block_orders/{number_block_order_id}`

```ruby
number_block_order = client.number_block_orders.retrieve("number_block_order_id")

puts(number_block_order)
```

## 获取与订单关联的号码列表

获取与订单关联的号码列表。

`GET /number_order_phone_numbers`

```ruby
number_order_phone_numbers = client.number_order_phone_numbers.list

puts(number_order_phone_numbers)
```

## 更新号码订单中的需求组

更新号码订单中的需求组。

`POST /number_order_phone_numbers/{id}/requirement_group` — 必需参数：`requirement_group_id`

```ruby
response = client.number_order_phone_numbers.update_requirement_group(
  "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
  requirement_group_id: "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"
)

puts(response)
```

## 获取号码订单中的单个号码信息

获取号码订单中的单个号码信息。

`GET /number_order_phone_numbers/{number_order_phone_number_id}`

```ruby
number_order_phone_number = client.number_order_phone_numbers.retrieve("number_order_phone_number_id")

puts(number_order_phone_number)
```

## 更新号码订单中的单个号码需求

更新号码订单中的单个号码需求。

`PATCH /number_order_phone_numbers/{number_order_phone_number_id}`

```ruby
response = client.number_order_phone_numbers.update_requirements("number_order_phone_number_id")

puts(response)
```

## 列出子号码订单信息

获取分页显示的子号码订单信息。

`GET /sub_number_orders`

```ruby
sub_number_orders = client.sub_number_orders.list

puts(sub_number_orders)
```

## 更新子号码订单的需求组

更新子号码订单的需求组。

`POST /sub_number_orders/{id}/requirement_group` — 必需参数：`requirement_group_id`

```ruby
response = client.sub_number_orders.update_requirement_group(
  "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
  requirement_group_id: "a4b201f9-8646-4e54-a7d2-b2e403eeaf8c"
)

puts(response)
```

## 获取子号码订单信息

获取现有的子号码订单信息。

`GET /sub_number_orders/{sub_number_order_id}`

```ruby
sub_number_order = client.sub_number_orders.retrieve("sub_number_order_id")

puts(sub_number_order)
```

## 更新子号码订单的需求

更新子号码订单的需求。

`PATCH /sub_number_orders/{sub_number_order_id}`

```ruby
sub_number_order = client.sub_number_orders.update("sub_number_order_id")

puts(sub_number_order)
```

## 取消子号码订单

允许取消处于“待处理”状态的子号码订单。

`PATCH /sub_number_orders/{sub_number_order_id}/cancel`

```ruby
response = client.sub_number_orders.cancel("sub_number_order_id")

puts(response)
```

## 创建子号码订单报告

为子号码订单创建 CSV 报告。

`POST /sub_number_orders/report`

```ruby
sub_number_orders_report = client.sub_number_orders_report.create

puts(sub_number_orders_report)
```

## 获取子号码订单报告

获取子号码订单的报告状态和详细信息。

`GET /sub_number_orders/report/{report_id}`

```ruby
sub_number_orders_report = client.sub_number_orders_report.retrieve("12ade33a-21c0-473b-b055-b3c836e1c293")

puts(sub_number_orders_report)
```

## 下载子号码订单报告

下载已完成的子号码订单报告的 CSV 文件。

`GET /sub_number_orders/report/{report_id}/download`

```ruby
response = client.sub_number_orders_report.download("12ade33a-21c0-473b-b055-b3c836e1c293")

puts(response)
```

## 列出高级订单信息

获取高级订单信息。

`GET /advanced_orders`

```ruby
advanced_orders = client.advanced_orders.list

puts(advanced_orders)
```

## 创建高级订单

创建高级订单。

`POST /advanced_orders`

```ruby
advanced_order = client.advanced_orders.create

puts(advanced_order)
```

## 更新高级订单

更新高级订单信息。

`PATCH /advanced_orders/{advanced-order-id}/requirement_group`

```ruby
response = client.advanced_orders.update_requirement_group("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(response)
```

## 获取高级订单信息

获取高级订单信息。

`GET /advanced_orders/{order_id}`

```ruby
advanced_order = client.advanced_orders.retrieve("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(advanced_order)
```

## 列出非明确指定的号码订单

获取分页显示的非明确指定号码订单信息。

`GET /inexplicit_number_orders`

```ruby
page = client.inexplicit_number_orders.list

puts(page)
```

## 创建非明确指定号码订单

创建非明确指定号码订单，以便在无需指定具体号码的情况下程序化购买电话号码。

`POST /inexplicit_number_orders` — 必需参数：`ordering_groups`

```ruby
inexplicit_number_order = client.inexplicit_number_orders.create(
  ordering_groups: [{count_requested: "count_requested", country_iso: :US, phone_number_type: "phone_number_type"}]
)

puts(inexplicit_number_order)
```

## 获取非明确指定号码订单信息

通过 ID 获取现有的非明确指定号码订单。

`GET /inexplicit_number_orders/{id}`

```ruby
inexplicit_number_order = client.inexplicit_number_orders.retrieve("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(inexplicit_number_order)
```

## 获取所有评论信息

获取所有评论信息。

`GET /comments`

```ruby
comments = client.comments.list

puts(comments)
```

## 创建评论

创建评论。

`POST /comments`

```ruby
comment = client.comments.create

puts(comment)
```

## 获取评论信息

获取评论信息。

`GET /comments/{id}`

```ruby
comment = client.comments.retrieve("id")

puts(comment)
```

## 将评论标记为已读

将评论标记为已读。

`PATCH /comments/{id}/read`

```ruby
response = client.comments.mark_as_read("id")

puts(response)
```

## 列出可用的号码块

获取可用的号码块信息。

`GET /available_phone_number_blocks`

```ruby
available_phone_number_blocks = client.available_phone_number_blocks.list

puts(available_phone_number_blocks)
```

## 列出可用的电话号码

获取可用的电话号码信息。

`GET /available_phone_numbers`

```ruby
available_phone_numbers = client.available_phone_numbers.list

puts(available_phone_numbers)
```

## 获取号码列表的功能信息

`POST /numbers_features` — 必需参数：`phone_numbers`

```ruby
numbers_feature = client.numbers_features.create(phone_numbers: ["string"])

puts(numbers_feature)
```

---

## Webhook

以下 Webhook 事件会被发送到您配置的 Webhook URL：
所有 Webhook 都包含 `telnyx-timestamp` 和 `telnyx-signature-ed25519` 标头以进行验证（兼容标准 Webhook）。

| 事件 | 描述 |
|-------|-------------|
| `numberOrderStatusUpdate` | 数字订单状态更新 |
```
```