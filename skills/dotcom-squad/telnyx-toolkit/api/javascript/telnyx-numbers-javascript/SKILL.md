---
name: telnyx-numbers-javascript
description: >-
  Search for available phone numbers by location and features, check coverage,
  and place orders. Use when acquiring new phone numbers. This skill provides
  JavaScript SDK examples.
metadata:
  author: telnyx
  product: numbers
  language: javascript
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 |

# Telnyx 数字服务 - JavaScript

## 安装

```bash
npm install telnyx
```

## 设置

```javascript
import Telnyx from 'telnyx';

const client = new Telnyx({
  apiKey: process.env['TELNYX_API_KEY'], // This is the default and can be omitted
});
```

以下所有示例均假设 `client` 已按照上述方式初始化。

## 获取国家覆盖范围

`GET /country_coverage`

```javascript
const countryCoverage = await client.countryCoverage.retrieve();

console.log(countryCoverage.data);
```

## 获取特定国家的覆盖范围

`GET /country_coverage/countries/{country_code}`

```javascript
const response = await client.countryCoverage.retrieveCountry('US');

console.log(response.data);
```

## 创建库存覆盖请求

创建一个库存覆盖请求。

`GET /inventory_coverage`

```javascript
const inventoryCoverages = await client.inventoryCoverage.list();

console.log(inventoryCoverages.data);
```

## 列出号码预订信息

获取分页显示的号码预订信息。

`GET /number_reservations`

```javascript
// Automatically fetches more pages as needed.
for await (const numberReservation of client.numberReservations.list()) {
  console.log(numberReservation.id);
}
```

## 创建号码预订

为多个号码创建号码预订。

`POST /number_reservations`

```javascript
const numberReservation = await client.numberReservations.create();

console.log(numberReservation.data);
```

## 获取号码预订信息

获取单个号码的预订信息。

`GET /number_reservations/{numberreservation_id}`

```javascript
const numberReservation = await client.numberReservations.retrieve('number_reservation_id');

console.log(numberReservation.data);
```

## 延长号码预订有效期

延长所有号码的预订有效期。

`POST /number_reservations/{numberreservation_id}/actions/extend`

```javascript
const response = await client.numberReservations.actions.extend('number_reservation_id');

console.log(response.data);
```

## 列出号码订单信息

获取分页显示的号码订单信息。

`GET /number_orders`

```javascript
// Automatically fetches more pages as needed.
for await (const numberOrderListResponse of client.numberOrders.list()) {
  console.log(numberOrderListResponse.id);
}
```

## 创建号码订单

创建一个号码订单。

`POST /number_orders`

```javascript
const numberOrder = await client.numberOrders.create();

console.log(numberOrder.data);
```

## 获取号码订单信息

获取现有的号码订单信息。

`GET /number_orders/{number_order_id}`

```javascript
const numberOrder = await client.numberOrders.retrieve('number_order_id');

console.log(numberOrder.data);
```

## 更新号码订单信息

更新号码订单信息。

`PATCH /number_orders/{number_order_id}`

```javascript
const numberOrder = await client.numberOrders.update('number_order_id');

console.log(numberOrder.data);
```

## 列出号码块订单信息

获取分页显示的号码块订单信息。

`GET /number_block_orders`

```javascript
// Automatically fetches more pages as needed.
for await (const numberBlockOrder of client.numberBlockOrders.list()) {
  console.log(numberBlockOrder.id);
}
```

## 创建号码块订单

创建一个号码块订单。

`POST /number_block_orders` — 必需参数：`starting_number`, `range`

```javascript
const numberBlockOrder = await client.numberBlockOrders.create({
  range: 10,
  starting_number: '+19705555000',
});

console.log(numberBlockOrder.data);
```

## 获取号码块订单信息

获取现有的号码块订单信息。

`GET /number_block_orders/{number_block_order_id}`

```javascript
const numberBlockOrder = await client.numberBlockOrders.retrieve('number_block_order_id');

console.log(numberBlockOrder.data);
```

## 获取与订单关联的号码列表

获取与订单关联的号码列表。

`GET /number_order_phone_numbers`

```javascript
const numberOrderPhoneNumbers = await client.numberOrderPhoneNumbers.list();

console.log(numberOrderPhoneNumbers.data);
```

## 更新号码订单中的需求组

更新号码订单中的需求组。

`POST /number_order_phone_numbers/{id}/requirement_group` — 必需参数：`requirement_group_id`

```javascript
const response = await client.numberOrderPhoneNumbers.updateRequirementGroup(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
  { requirement_group_id: '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e' },
);

console.log(response.data);
```

## 获取号码订单中的单个号码信息

获取号码订单中的单个号码信息。

`GET /number_order_phone_numbers/{number_order_phone_number_id}`

```javascript
const numberOrderPhoneNumber = await client.numberOrderPhoneNumbers.retrieve(
  'number_order_phone_number_id',
);

console.log(numberOrderPhoneNumber.data);
```

## 更新号码订单中的单个号码需求

更新号码订单中的单个号码需求。

`PATCH /number_order_phone_numbers/{number_order_phone_number_id}`

```javascript
const response = await client.numberOrderPhoneNumbers.updateRequirements(
  'number_order_phone_number_id',
);

console.log(response.data);
```

## 列出子号码订单信息

获取分页显示的子号码订单信息。

`GET /sub_number_orders`

```javascript
const subNumberOrders = await client.subNumberOrders.list();

console.log(subNumberOrders.data);
```

## 更新子号码订单的需求组

更新子号码订单的需求组。

`POST /sub_number_orders/{id}/requirement_group` — 必需参数：`requirement_group_id`

```javascript
const response = await client.subNumberOrders.updateRequirementGroup(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
  { requirement_group_id: 'a4b201f9-8646-4e54-a7d2-b2e403eeaf8c' },
);

console.log(response.data);
```

## 获取子号码订单信息

获取现有的子号码订单信息。

`GET /sub_number_orders/{sub_number_order_id}`

```javascript
const subNumberOrder = await client.subNumberOrders.retrieve('sub_number_order_id');

console.log(subNumberOrder.data);
```

## 更新子号码订单的需求

更新子号码订单的需求。

`PATCH /sub_number_orders/{sub_number_order_id}`

```javascript
const subNumberOrder = await client.subNumberOrders.update('sub_number_order_id');

console.log(subNumberOrder.data);
```

## 取消子号码订单

允许取消处于“待处理”状态的子号码订单。

`PATCH /sub_number_orders/{sub_number_order_id}/cancel`

```javascript
const response = await client.subNumberOrders.cancel('sub_number_order_id');

console.log(response.data);
```

## 创建子号码订单报告

创建子号码订单的 CSV 报告。

`POST /sub_number_orders/report`

```javascript
const subNumberOrdersReport = await client.subNumberOrdersReport.create();

console.log(subNumberOrdersReport.data);
```

## 获取子号码订单报告

获取子号码订单的报告状态和详细信息。

`GET /sub_number_orders/report/{report_id}`

```javascript
const subNumberOrdersReport = await client.subNumberOrdersReport.retrieve(
  '12ade33a-21c0-473b-b055-b3c836e1c293',
);

console.log(subNumberOrdersReport.data);
```

## 下载子号码订单报告

下载已完成的子号码订单的 CSV 文件。

`GET /sub_number_orders/report/{report_id}/download`

```javascript
const response = await client.subNumberOrdersReport.download(
  '12ade33a-21c0-473b-b055-b3c836e1c293',
);

console.log(response);
```

## 列出高级订单信息

获取高级订单信息。

`GET /advanced_orders`

```javascript
const advancedOrders = await client.advancedOrders.list();

console.log(advancedOrders.data);
```

## 创建高级订单

创建一个高级订单。

`POST /advanced_orders`

```javascript
const advancedOrder = await client.advancedOrders.create();

console.log(advancedOrder.id);
```

## 更新高级订单

更新高级订单的信息。

`PATCH /advanced_orders/{advanced-order-id}/requirement_group`

```javascript
const response = await client.advancedOrders.updateRequirementGroup(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
);

console.log(response.id);
```

## 获取高级订单信息

获取高级订单的详细信息。

`GET /advanced_orders/{order_id}`

```javascript
const advancedOrder = await client.advancedOrders.retrieve('182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e');

console.log(advancedOrder.id);
```

## 获取非明确指定的号码订单信息

获取分页显示的非明确指定号码订单信息。

`GET /inexplicit_number_orders`

```javascript
// Automatically fetches more pages as needed.
for await (const inexplicitNumberOrderResponse of client.inexplicitNumberOrders.list()) {
  console.log(inexplicitNumberOrderResponse.id);
}
```

## 创建非明确指定的号码订单

创建一个非明确指定的号码订单，以便在不指定具体号码的情况下批量购买电话号码。

`POST /inexplicit_number_orders` — 必需参数：`ordering_groups`

```javascript
const inexplicitNumberOrder = await client.inexplicitNumberOrders.create({
  ordering_groups: [
    {
      count_requested: 'count_requested',
      country_iso: 'US',
      phone_number_type: 'phone_number_type',
    },
  ],
});

console.log(inexplicitNumberOrder.data);
```

## 获取非明确指定的号码订单信息

通过 ID 获取现有的非明确指定号码订单。

`GET /inexplicit_number_orders/{id}`

```javascript
const inexplicitNumberOrder = await client.inexplicitNumberOrders.retrieve(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
);

console.log(inexplicitNumberOrder.data);
```

## 获取所有评论信息

获取所有评论信息。

`GET /comments`

```javascript
const comments = await client.comments.list();

console.log(comments.data);
```

## 创建评论

创建一条评论。

`POST /comments`

```javascript
const comment = await client.comments.create();

console.log(comment.data);
```

## 获取评论信息

获取特定评论的详细信息。

`GET /comments/{id}`

```javascript
const comment = await client.comments.retrieve('id');

console.log(comment.data);
```

## 将评论标记为已读

将评论标记为已读。

`PATCH /comments/{id}/read`

```javascript
const response = await client.comments.markAsRead('id');

console.log(response.data);
```

## 列出可用的号码块

获取可用的号码块信息。

`GET /available_phone_number_blocks`

```javascript
const availablePhoneNumberBlocks = await client.availablePhoneNumberBlocks.list();

console.log(availablePhoneNumberBlocks.data);
```

## 列出可用的电话号码

获取可用的电话号码信息。

`GET /available_phone_numbers`

```javascript
const availablePhoneNumbers = await client.availablePhoneNumbers.list();

console.log(availablePhoneNumbers.data);
```

## 获取号码列表的相关信息

获取号码列表的相关信息。

`POST /numbers_features` — 必需参数：`phone_numbers`

```javascript
const numbersFeature = await client.numbersFeatures.create({ phone_numbers: ['string'] });

console.log(numbersFeature.data);
```

---

## Webhook

以下 Webhook 事件会被发送到您配置的 Webhook URL。所有 Webhook 都包含 `telnyx-timestamp` 和 `telnyx-signature-ed25519` 标头以进行验证（兼容标准 Webhook）。

| 事件 | 描述 |
|-------|-------------|
| `numberOrderStatusUpdate` | 数字订单状态更新 |
```
```