---
name: telnyx-numbers-python
description: >-
  Search for available phone numbers by location and features, check coverage,
  and place orders. Use when acquiring new phone numbers. This skill provides
  Python SDK examples.
metadata:
  author: telnyx
  product: numbers
  language: python
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 |

# Telnyx 数字服务 - Python

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

## 获取国家覆盖范围

`GET /country_coverage`

```python
country_coverage = client.country_coverage.retrieve()
print(country_coverage.data)
```

## 获取特定国家的覆盖范围

`GET /country_coverage/countries/{country_code}`

```python
response = client.country_coverage.retrieve_country(
    "US",
)
print(response.data)
```

## 创建库存覆盖请求

创建一个库存覆盖请求。

`GET /inventory_coverage`

```python
inventory_coverages = client.inventory_coverage.list()
print(inventory_coverages.data)
```

## 列出电话号码预订信息

获取分页显示的电话号码预订信息。

`GET /number_reservations`

```python
page = client.number_reservations.list()
page = page.data[0]
print(page.id)
```

## 创建电话号码预订

为多个电话号码创建预订。

`POST /number_reservations`

```python
number_reservation = client.number_reservations.create()
print(number_reservation.data)
```

## 获取电话号码预订信息

获取单个电话号码的预订信息。

`GET /number_reservations/{numberreservation_id}`

```python
number_reservation = client.number_reservations.retrieve(
    "number_reservation_id",
)
print(number_reservation.data)
```

## 延长电话号码预订的有效期

延长所有电话号码的预订有效期。

`POST /number_reservations/{numberreservation_id}/actions/extend`

```python
response = client.number_reservations.actions.extend(
    "number_reservation_id",
)
print(response.data)
```

## 列出电话号码订单信息

获取分页显示的电话号码订单信息。

`GET /number_orders`

```python
page = client.number_orders.list()
page = page.data[0]
print(page.id)
```

## 创建电话号码订单

创建一个电话号码订单。

`POST /number_orders`

```python
number_order = client.number_orders.create()
print(number_order.data)
```

## 获取电话号码订单信息

获取现有的电话号码订单信息。

`GET /number_orders/{number_order_id}`

```python
number_order = client.number_orders.retrieve(
    "number_order_id",
)
print(number_order.data)
```

## 更新电话号码订单信息

更新电话号码订单信息。

`PATCH /number_orders/{number_order_id}`

```python
number_order = client.number_orders.update(
    number_order_id="number_order_id",
)
print(number_order.data)
```

## 列出电话号码块订单信息

获取分页显示的电话号码块订单信息。

`GET /number_block_orders`

```python
page = client.number_block_orders.list()
page = page.data[0]
print(page.id)
```

## 创建电话号码块订单

创建一个电话号码块订单。

`POST /number_block_orders` — 必需参数：`starting_number`, `range`

```python
number_block_order = client.number_block_orders.create(
    range=10,
    starting_number="+19705555000",
)
print(number_block_order.data)
```

## 获取电话号码块订单信息

获取现有的电话号码块订单信息。

`GET /number_block_orders/{number_block_order_id}`

```python
number_block_order = client.number_block_orders.retrieve(
    "number_block_order_id",
)
print(number_block_order.data)
```

## 获取与订单关联的电话号码列表

获取与订单关联的电话号码列表。

`GET /number_order_phone_numbers`

```python
number_order_phone_numbers = client.number_order_phone_numbers.list()
print(number_order_phone_numbers.data)
```

## 更新电话号码订单中的需求组

更新电话号码订单中的需求组。

`POST /number_order_phone_numbers/{id}/requirement_group` — 必需参数：`requirement_group_id`

```python
response = client.number_order_phone_numbers.update_requirement_group(
    id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
    requirement_group_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(response.data)
```

## 获取电话号码订单中的单个电话号码

获取电话号码订单中的单个电话号码信息。

`GET /number_order_phone_numbers/{number_order_phone_number_id}`

```python
number_order_phone_number = client.number_order_phone_numbers.retrieve(
    "number_order_phone_number_id",
)
print(number_order_phone_number.data)
```

## 更新电话号码订单中的单个电话号码的需求

更新电话号码订单中的单个电话号码的需求信息。

`PATCH /number_order_phone_numbers/{number_order_phone_number_id}`

```python
response = client.number_order_phone_numbers.update_requirements(
    number_order_phone_number_id="number_order_phone_number_id",
)
print(response.data)
```

## 列出子号码订单信息

获取分页显示的子号码订单信息。

`GET /sub_number_orders`

```python
sub_number_orders = client.sub_number_orders.list()
print(sub_number_orders.data)
```

## 更新子号码订单的需求组

更新子号码订单的需求组。

`POST /sub_number_orders/{id}/requirement_group` — 必需参数：`requirement_group_id`

```python
response = client.sub_number_orders.update_requirement_group(
    id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
    requirement_group_id="a4b201f9-8646-4e54-a7d2-b2e403eeaf8c",
)
print(response.data)
```

## 获取子号码订单信息

获取现有的子号码订单信息。

`GET /sub_number_orders/{sub_number_order_id}`

```python
sub_number_order = client.sub_number_orders.retrieve(
    sub_number_order_id="sub_number_order_id",
)
print(sub_number_order.data)
```

## 更新子号码订单的需求信息

更新子号码订单的需求信息。

`PATCH /sub_number_orders/{sub_number_order_id}`

```python
sub_number_order = client.sub_number_orders.update(
    sub_number_order_id="sub_number_order_id",
)
print(sub_number_order.data)
```

## 取消子号码订单

允许取消处于“待处理”状态的子号码订单。

`PATCH /sub_number_orders/{sub_number_order_id}/cancel`

```python
response = client.sub_number_orders.cancel(
    "sub_number_order_id",
)
print(response.data)
```

## 创建子号码订单报告

为子号码订单创建 CSV 报告。

`POST /sub_number_orders/report`

```python
sub_number_orders_report = client.sub_number_orders_report.create()
print(sub_number_orders_report.data)
```

## 获取子号码订单报告

获取子号码订单的报告状态和详细信息。

`GET /sub_number_orders/report/{report_id}`

```python
sub_number_orders_report = client.sub_number_orders_report.retrieve(
    "12ade33a-21c0-473b-b055-b3c836e1c293",
)
print(sub_number_orders_report.data)
```

## 下载子号码订单报告

下载已完成的子号码订单的 CSV 文件。

`GET /sub_number_orders/report/{report_id}/download`

```python
response = client.sub_number_orders_report.download(
    "12ade33a-21c0-473b-b055-b3c836e1c293",
)
print(response)
```

## 列出高级订单信息

获取高级订单信息。

`GET /advanced_orders`

```python
advanced_orders = client.advanced_orders.list()
print(advanced_orders.data)
```

## 创建高级订单

创建一个高级订单。

`POST /advanced_orders`

```python
advanced_order = client.advanced_orders.create()
print(advanced_order.id)
```

## 更新高级订单

更新高级订单的信息。

`PATCH /advanced_orders/{advanced-order-id}/requirement_group`

```python
response = client.advanced_orders.update_requirement_group(
    advanced_order_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(response.id)
```

## 获取高级订单信息

获取高级订单的详细信息。

`GET /advanced_orders/{order_id}`

```python
advanced_order = client.advanced_orders.retrieve(
    "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(advanced_order.id)
```

## 获取非明确指定的电话号码订单信息

获取分页显示的非明确指定电话号码订单信息。

`GET /inexplicit_number_orders`

```python
page = client.inexplicit_number_orders.list()
page = page.data[0]
print(page.id)
```

## 创建非明确指定的电话号码订单

创建一个非明确指定的电话号码订单，以便在不指定具体号码的情况下程序化购买电话号码。

`POST /inexplicit_number_orders` — 必需参数：`ordering_groups`

```python
inexplicit_number_order = client.inexplicit_number_orders.create(
    ordering_groups=[{
        "count_requested": "count_requested",
        "country_iso": "US",
        "phone_number_type": "phone_number_type",
    }],
)
print(inexplicit_number_order.data)
```

## 获取非明确指定的电话号码订单信息

通过 ID 获取现有的非明确指定电话号码订单。

`GET /inexplicit_number_orders/{id}`

```python
inexplicit_number_order = client.inexplicit_number_orders.retrieve(
    "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(inexplicit_number_order.data)
```

## 获取所有评论信息

获取所有评论信息。

`GET /comments`

```python
comments = client.comments.list()
print(comments.data)
```

## 创建评论

创建一条评论。

`POST /comments`

```python
comment = client.comments.create()
print(comment.data)
```

## 获取评论信息

获取特定评论的详细信息。

`GET /comments/{id}`

```python
comment = client.comments.retrieve(
    "id",
)
print(comment.data)
```

## 将评论标记为已阅读

将评论标记为已阅读。

`PATCH /comments/{id}/read`

```python
response = client.comments.mark_as_read(
    "id",
)
print(response.data)
```

## 列出可用的电话号码块

获取可用的电话号码块信息。

`GET /available_phone_number_blocks`

```python
available_phone_number_blocks = client.available_phone_number_blocks.list()
print(available_phone_number_blocks.data)
```

## 列出可用的电话号码

获取可用的电话号码信息。

`GET /available_phone_numbers`

```python
available_phone_numbers = client.available_phone_numbers.list()
print(available_phone_numbers.data)
```

## 获取电话号码列表的相关信息

获取电话号码列表的相关信息。

`POST /numbers_features` — 必需参数：`phone_numbers`

```python
numbers_feature = client.numbers_features.create(
    phone_numbers=["string"],
)
print(numbers_feature.data)
```

---

## Webhook

以下 Webhook 事件会被发送到您配置的 Webhook URL。所有 Webhook 都包含 `telnyx-timestamp` 和 `telnyx-signature-ed25519` 标头以进行验证（兼容标准 Webhook）。

| 事件 | 描述 |
|-------|-------------|
| `numberOrderStatusUpdate` | 电话号码订单状态更新 |
```
```