---
name: telnyx-numbers-java
description: >-
  Search for available phone numbers by location and features, check coverage,
  and place orders. Use when acquiring new phone numbers. This skill provides
  Java SDK examples.
metadata:
  author: telnyx
  product: numbers
  language: java
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 |

# Telnyx 数字服务 - Java

## 安装

```text
// See https://github.com/team-telnyx/telnyx-java for Maven/Gradle setup
```

## 设置

```java
import com.telnyx.sdk.client.TelnyxClient;
import com.telnyx.sdk.client.okhttp.TelnyxOkHttpClient;

TelnyxClient client = TelnyxOkHttpClient.fromEnv();
```

以下所有示例均假设 `client` 已按照上述方式初始化。

## 获取国家覆盖范围

`GET /country_coverage`

```java
import com.telnyx.sdk.models.countrycoverage.CountryCoverageRetrieveParams;
import com.telnyx.sdk.models.countrycoverage.CountryCoverageRetrieveResponse;

CountryCoverageRetrieveResponse countryCoverage = client.countryCoverage().retrieve();
```

## 获取特定国家的覆盖范围

`GET /country_coverage/countries/{country_code}`

```java
import com.telnyx.sdk.models.countrycoverage.CountryCoverageRetrieveCountryParams;
import com.telnyx.sdk.models.countrycoverage.CountryCoverageRetrieveCountryResponse;

CountryCoverageRetrieveCountryResponse response = client.countryCoverage().retrieveCountry("US");
```

## 创建库存覆盖请求

创建一个库存覆盖请求。

`GET /inventory_coverage`

```java
import com.telnyx.sdk.models.inventorycoverage.InventoryCoverageListParams;
import com.telnyx.sdk.models.inventorycoverage.InventoryCoverageListResponse;

InventoryCoverageListResponse inventoryCoverages = client.inventoryCoverage().list();
```

## 列出号码预订信息

获取分页显示的电话号码预订信息。

`GET /number_reservations`

```java
import com.telnyx.sdk.models.numberreservations.NumberReservationListPage;
import com.telnyx.sdk.models.numberreservations.NumberReservationListParams;

NumberReservationListPage page = client.numberReservations().list();
```

## 创建号码预订

为多个号码创建电话号码预订。

`POST /number_reservations`

```java
import com.telnyx.sdk.models.numberreservations.NumberReservationCreateParams;
import com.telnyx.sdk.models.numberreservations.NumberReservationCreateResponse;

NumberReservationCreateResponse numberReservation = client.numberReservations().create();
```

## 获取号码预订信息

获取单个电话号码的预订信息。

`GET /number_reservations/{numberreservation_id}`

```java
import com.telnyx.sdk.models.numberreservations.NumberReservationRetrieveParams;
import com.telnyx.sdk.models.numberreservations.NumberReservationRetrieveResponse;

NumberReservationRetrieveResponse numberReservation = client.numberReservations().retrieve("number_reservation_id");
```

## 延长号码预订有效期

延长所有号码的预订有效期。

`POST /number_reservations/{numberreservation_id}/actions/extend`

```java
import com.telnyx.sdk.models.numberreservations.actions.ActionExtendParams;
import com.telnyx.sdk.models.numberreservations.actions.ActionExtendResponse;

ActionExtendResponse response = client.numberReservations().actions().extend("number_reservation_id");
```

## 列出号码订单信息

获取分页显示的号码订单信息。

`GET /number_orders`

```java
import com.telnyx.sdk.models.numberorders.NumberOrderListPage;
import com.telnyx.sdk.models.numberorders.NumberOrderListParams;

NumberOrderListPage page = client.numberOrders().list();
```

## 创建号码订单

创建一个电话号码订单。

`POST /number_orders`

```java
import com.telnyx.sdk.models.numberorders.NumberOrderCreateParams;
import com.telnyx.sdk.models.numberorders.NumberOrderCreateResponse;

NumberOrderCreateResponse numberOrder = client.numberOrders().create();
```

## 获取号码订单信息

获取现有的电话号码订单信息。

`GET /number_orders/{number_order_id}`

```java
import com.telnyx.sdk.models.numberorders.NumberOrderRetrieveParams;
import com.telnyx.sdk.models.numberorders.NumberOrderRetrieveResponse;

NumberOrderRetrieveResponse numberOrder = client.numberOrders().retrieve("number_order_id");
```

## 更新号码订单信息

更新电话号码订单信息。

`PATCH /number_orders/{number_order_id}`

```java
import com.telnyx.sdk.models.numberorders.NumberOrderUpdateParams;
import com.telnyx.sdk.models.numberorders.NumberOrderUpdateResponse;

NumberOrderUpdateResponse numberOrder = client.numberOrders().update("number_order_id");
```

## 列出号码块订单信息

获取分页显示的号码块订单信息。

`GET /number_block_orders`

```java
import com.telnyx.sdk.models.numberblockorders.NumberBlockOrderListPage;
import com.telnyx.sdk.models.numberblockorders.NumberBlockOrderListParams;

NumberBlockOrderListPage page = client.numberBlockOrders().list();
```

## 创建号码块订单

创建一个电话号码块订单。

`POST /number_block_orders` — 必需参数：`starting_number`、`range`

```java
import com.telnyx.sdk.models.numberblockorders.NumberBlockOrderCreateParams;
import com.telnyx.sdk.models.numberblockorders.NumberBlockOrderCreateResponse;

NumberBlockOrderCreateParams params = NumberBlockOrderCreateParams.builder()
    .range(10L)
    .startingNumber("+19705555000")
    .build();
NumberBlockOrderCreateResponse numberBlockOrder = client.numberBlockOrders().create(params);
```

## 获取号码块订单信息

获取现有的电话号码块订单信息。

`GET /number_block_orders/{number_block_order_id}`

```java
import com.telnyx.sdk.models.numberblockorders.NumberBlockOrderRetrieveParams;
import com.telnyx.sdk.models.numberblockorders.NumberBlockOrderRetrieveResponse;

NumberBlockOrderRetrieveResponse numberBlockOrder = client.numberBlockOrders().retrieve("number_block_order_id");
```

## 获取与订单关联的电话号码列表

获取与订单关联的电话号码列表。

`GET /number_order_phone_numbers`

```java
import com.telnyx.sdk.models.numberorderphonenumbers.NumberOrderPhoneNumberListParams;
import com.telnyx.sdk.models.numberorderphonenumbers.NumberOrderPhoneNumberListResponse;

NumberOrderPhoneNumberListResponse numberOrderPhoneNumbers = client.numberOrderPhoneNumbers().list();
```

## 更新号码订单中的需求组

`POST /number_order_phone_numbers/{id}/requirement_group` — 必需参数：`requirement_group_id`

```java
import com.telnyx.sdk.models.numberorderphonenumbers.NumberOrderPhoneNumberUpdateRequirementGroupParams;
import com.telnyx.sdk.models.numberorderphonenumbers.NumberOrderPhoneNumberUpdateRequirementGroupResponse;

NumberOrderPhoneNumberUpdateRequirementGroupParams params = NumberOrderPhoneNumberUpdateRequirementGroupParams.builder()
    .id("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
    .requirementGroupId("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
    .build();
NumberOrderPhoneNumberUpdateRequirementGroupResponse response = client.numberOrderPhoneNumbers().updateRequirementGroup(params);
```

## 获取号码订单中的单个电话号码信息

获取号码订单中的某个电话号码信息。

`GET /number_order_phone_numbers/{number_order_phone_number_id}`

```java
import com.telnyx.sdk.models.numberorderphonenumbers.NumberOrderPhoneNumberRetrieveParams;
import com.telnyx.sdk.models.numberorderphonenumbers.NumberOrderPhoneNumberRetrieveResponse;

NumberOrderPhoneNumberRetrieveResponse numberOrderPhoneNumber = client.numberOrderPhoneNumbers().retrieve("number_order_phone_number_id");
```

## 更新号码订单中的单个电话号码需求

更新号码订单中某个电话号码的需求信息。

`PATCH /number_order_phone_numbers/{number_order_phone_number_id}`

```java
import com.telnyx.sdk.models.numberorderphonenumbers.NumberOrderPhoneNumberUpdateRequirementsParams;
import com.telnyx.sdk.models.numberorderphonenumbers.NumberOrderPhoneNumberUpdateRequirementsResponse;

NumberOrderPhoneNumberUpdateRequirementsResponse response = client.numberOrderPhoneNumbers().updateRequirements("number_order_phone_number_id");
```

## 列出子号码订单信息

获取分页显示的子号码订单信息。

`GET /sub_number_orders`

```java
import com.telnyx.sdk.models.subnumberorders.SubNumberOrderListParams;
import com.telnyx.sdk.models.subnumberorders.SubNumberOrderListResponse;

SubNumberOrderListResponse subNumberOrders = client.subNumberOrders().list();
```

## 更新子号码订单的需求组

`POST /sub_number_orders/{id}/requirement_group` — 必需参数：`requirement_group_id`

```java
import com.telnyx.sdk.models.subnumberorders.SubNumberOrderUpdateRequirementGroupParams;
import com.telnyx.sdk.models.subnumberorders.SubNumberOrderUpdateRequirementGroupResponse;

SubNumberOrderUpdateRequirementGroupParams params = SubNumberOrderUpdateRequirementGroupParams.builder()
    .id("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
    .requirementGroupId("a4b201f9-8646-4e54-a7d2-b2e403eeaf8c")
    .build();
SubNumberOrderUpdateRequirementGroupResponse response = client.subNumberOrders().updateRequirementGroup(params);
```

## 获取子号码订单信息

获取现有的子号码订单信息。

`GET /sub_number_orders/{sub_number_order_id}`

```java
import com.telnyx.sdk.models.subnumberorders.SubNumberOrderRetrieveParams;
import com.telnyx.sdk.models.subnumberorders.SubNumberOrderRetrieveResponse;

SubNumberOrderRetrieveResponse subNumberOrder = client.subNumberOrders().retrieve("sub_number_order_id");
```

## 更新子号码订单的需求信息

更新子号码订单的需求信息。

`PATCH /sub_number_orders/{sub_number_order_id}`

```java
import com.telnyx.sdk.models.subnumberorders.SubNumberOrderUpdateParams;
import com.telnyx.sdk.models.subnumberorders.SubNumberOrderUpdateResponse;

SubNumberOrderUpdateResponse subNumberOrder = client.subNumberOrders().update("sub_number_order_id");
```

## 取消子号码订单

允许取消处于“待处理”状态的子号码订单。

`PATCH /sub_number_orders/{sub_number_order_id}/cancel`

```java
import com.telnyx.sdk.models.subnumberorders.SubNumberOrderCancelParams;
import com.telnyx.sdk.models.subnumberorders.SubNumberOrderCancelResponse;

SubNumberOrderCancelResponse response = client.subNumberOrders().cancel("sub_number_order_id");
```

## 创建子号码订单报告

为子号码订单创建 CSV 报告。

`POST /sub_number_orders/report`

```java
import com.telnyx.sdk.models.subnumberordersreport.SubNumberOrdersReportCreateParams;
import com.telnyx.sdk.models.subnumberordersreport.SubNumberOrdersReportCreateResponse;

SubNumberOrdersReportCreateResponse subNumberOrdersReport = client.subNumberOrdersReport().create();
```

## 获取子号码订单报告

获取子号码订单的报告状态和详细信息。

`GET /sub_number_orders/report/{report_id}`

```java
import com.telnyx.sdk.models.subnumberordersreport.SubNumberOrdersReportRetrieveParams;
import com.telnyx.sdk.models.subnumberordersreport.SubNumberOrdersReportRetrieveResponse;

SubNumberOrdersReportRetrieveResponse subNumberOrdersReport = client.subNumberOrdersReport().retrieve("12ade33a-21c0-473b-b055-b3c836e1c293");
```

## 下载子号码订单报告

下载已完成的子号码订单的 CSV 文件。

`GET /sub_number_orders/report/{report_id}/download`

```java
import com.telnyx.sdk.models.subnumberordersreport.SubNumberOrdersReportDownloadParams;

String response = client.subNumberOrdersReport().download("12ade33a-21c0-473b-b055-b3c836e1c293");
```

## 列出高级订单信息

获取高级订单信息。

`GET /advanced_orders`

```java
import com.telnyx.sdk.models.advancedorders.AdvancedOrderListParams;
import com.telnyx.sdk.models.advancedorders.AdvancedOrderListResponse;

AdvancedOrderListResponse advancedOrders = client.advancedOrders().list();
```

## 创建高级订单

创建一个高级订单。

`POST /advanced_orders`

```java
import com.telnyx.sdk.models.advancedorders.AdvancedOrder;
import com.telnyx.sdk.models.advancedorders.AdvancedOrderCreateParams;
import com.telnyx.sdk.models.advancedorders.AdvancedOrderCreateResponse;

AdvancedOrder params = AdvancedOrder.builder().build();
AdvancedOrderCreateResponse advancedOrder = client.advancedOrders().create(params);
```

## 更新高级订单

更新高级订单的信息。

`PATCH /advanced_orders/{advanced-order-id}/requirement_group`

```java
import com.telnyx.sdk.models.advancedorders.AdvancedOrder;
import com.telnyx.sdk.models.advancedorders.AdvancedOrderUpdateRequirementGroupParams;
import com.telnyx.sdk.models.advancedorders.AdvancedOrderUpdateRequirementGroupResponse;

AdvancedOrderUpdateRequirementGroupParams params = AdvancedOrderUpdateRequirementGroupParams.builder()
    .advancedOrderId("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
    .advancedOrder(AdvancedOrder.builder().build())
    .build();
AdvancedOrderUpdateRequirementGroupResponse response = client.advancedOrders().updateRequirementGroup(params);
```

## 获取高级订单信息

获取高级订单的详细信息。

`GET /advanced_orders/{order_id}`

```java
import com.telnyx.sdk.models.advancedorders.AdvancedOrderRetrieveParams;
import com.telnyx.sdk.models.advancedorders.AdvancedOrderRetrieveResponse;

AdvancedOrderRetrieveResponse advancedOrder = client.advancedOrders().retrieve("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 获取非明确指定的号码订单信息

获取分页显示的非明确指定号码订单信息。

`GET /inexplicit_number_orders`

```java
import com.telnyx.sdk.models.inexplicitnumberorders.InexplicitNumberOrderListPage;
import com.telnyx.sdk.models.inexplicitnumberorders.InexplicitNumberOrderListParams;

InexplicitNumberOrderListPage page = client.inexplicitNumberOrders().list();
```

## 创建非明确指定的号码订单

创建一个非明确指定的号码订单，以便在不指定具体号码的情况下程序化购买电话号码。

`POST /inexplicit_number_orders` — 必需参数：`ordering_groups`

```java
import com.telnyx.sdk.models.inexplicitnumberorders.InexplicitNumberOrderCreateParams;
import com.telnyx.sdk.models.inexplicitnumberorders.InexplicitNumberOrderCreateResponse;

InexplicitNumberOrderCreateParams params = InexplicitNumberOrderCreateParams.builder()
    .addOrderingGroup(InexplicitNumberOrderCreateParams.OrderingGroup.builder()
        .countRequested("count_requested")
        .countryIso(InexplicitNumberOrderCreateParams.OrderingGroup.CountryIso.US)
        .phoneNumberType("phone_number_type")
        .build())
    .build();
InexplicitNumberOrderCreateResponse inexplicitNumberOrder = client.inexplicitNumberOrders().create(params);
```

## 获取非明确指定的号码订单信息

通过 ID 获取现有的非明确指定号码订单。

`GET /inexplicit_number_orders/{id}`

```java
import com.telnyx.sdk.models.inexplicitnumberorders.InexplicitNumberOrderRetrieveParams;
import com.telnyx.sdk.models.inexplicitnumberorders.InexplicitNumberOrderRetrieveResponse;

InexplicitNumberOrderRetrieveResponse inexplicitNumberOrder = client.inexplicitNumberOrders().retrieve("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 获取所有评论信息

获取所有评论信息。

`GET /comments`

```java
import com.telnyx.sdk.models.comments.CommentListParams;
import com.telnyx.sdk.models.comments.CommentListResponse;

CommentListResponse comments = client.comments().list();
```

## 创建评论

创建一条评论。

`POST /comments`

```java
import com.telnyx.sdk.models.comments.CommentCreateParams;
import com.telnyx.sdk.models.comments.CommentCreateResponse;

CommentCreateResponse comment = client.comments().create();
```

## 获取评论信息

获取特定评论的详细信息。

`GET /comments/{id}`

```java
import com.telnyx.sdk.models.comments.CommentRetrieveParams;
import com.telnyx.sdk.models.comments.CommentRetrieveResponse;

CommentRetrieveResponse comment = client.comments().retrieve("id");
```

## 将评论标记为已读

将评论标记为已读。

`PATCH /comments/{id}/read`

```java
import com.telnyx.sdk.models.comments.CommentMarkAsReadParams;
import com.telnyx.sdk.models.comments.CommentMarkAsReadResponse;

CommentMarkAsReadResponse response = client.comments().markAsRead("id");
```

## 列出可用的电话号码块

获取可用的电话号码块信息。

`GET /available_phone_number_blocks`

```java
import com.telnyx.sdk.models.availablephonenumberblocks.AvailablePhoneNumberBlockListParams;
import com.telnyx.sdk.models.availablephonenumberblocks.AvailablePhoneNumberBlockListResponse;

AvailablePhoneNumberBlockListResponse availablePhoneNumberBlocks = client.availablePhoneNumberBlocks().list();
```

## 列出可用的电话号码

获取可用的电话号码信息。

`GET /available_phone_numbers`

```java
import com.telnyx.sdk.models.availablephonenumbers.AvailablePhoneNumberListParams;
import com.telnyx.sdk.models.availablephonenumbers.AvailablePhoneNumberListResponse;

AvailablePhoneNumberListResponse availablePhoneNumbers = client.availablePhoneNumbers().list();
```

## 获取号码列表的功能信息

获取号码列表的功能信息。

`POST /numbers_features` — 必需参数：`phone_numbers`

```java
import com.telnyx.sdk.models.numbersfeatures.NumbersFeatureCreateParams;
import com.telnyx.sdk.models.numbersfeatures.NumbersFeatureCreateResponse;

NumbersFeatureCreateParams params = NumbersFeatureCreateParams.builder()
    .addPhoneNumber("string")
    .build();
NumbersFeatureCreateResponse numbersFeature = client.numbersFeatures().create(params);
```

---

## Webhook

以下 Webhook 事件会发送到您配置的 Webhook URL。所有 Webhook 都包含 `telnyx-timestamp` 和 `telnyx-signature-ed25519` 头部字段以进行验证（兼容标准 Webhook）。

| 事件 | 描述 |
|-------|-------------|
| `numberOrderStatusUpdate` | 数字订单状态更新 |
```
```