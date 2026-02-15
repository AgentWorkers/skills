---
name: telnyx-numbers-go
description: >-
  Search for available phone numbers by location and features, check coverage,
  and place orders. Use when acquiring new phone numbers. This skill provides Go
  SDK examples.
metadata:
  author: telnyx
  product: numbers
  language: go
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 |

# Telnyx Numbers - Go

## 安装

```bash
go get github.com/team-telnyx/telnyx-go
```

## 设置

```go
import (
  "context"
  "fmt"
  "os"

  "github.com/team-telnyx/telnyx-go"
  "github.com/team-telnyx/telnyx-go/option"
)

client := telnyx.NewClient(
  option.WithAPIKey(os.Getenv("TELNYX_API_KEY")),
)
```

以下所有示例均假设 `client` 已按上述方式初始化。

## 获取国家覆盖范围

`GET /country_coverage`

```go
	countryCoverage, err := client.CountryCoverage.Get(context.TODO())
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", countryCoverage.Data)
```

## 获取特定国家的覆盖范围

`GET /country_coverage/countries/{country_code}`

```go
	response, err := client.CountryCoverage.GetCountry(context.TODO(), "US")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 创建库存覆盖请求

创建一个库存覆盖请求。

`GET /inventory_coverage`

```go
	inventoryCoverages, err := client.InventoryCoverage.List(context.TODO(), telnyx.InventoryCoverageListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", inventoryCoverages.Data)
```

## 列出电话号码预订信息

获取分页显示的电话号码预订信息。

`GET /number_reservations`

```go
	page, err := client.NumberReservations.List(context.TODO(), telnyx.NumberReservationListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建电话号码预订

为多个电话号码创建预订。

`POST /number_reservations`

```go
	numberReservation, err := client.NumberReservations.New(context.TODO(), telnyx.NumberReservationNewParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", numberReservation.Data)
```

## 查取电话号码预订信息

获取单个电话号码的预订信息。

`GET /number_reservations/{numberreservation_id}`

```go
	numberReservation, err := client.NumberReservations.Get(context.TODO(), "number_reservation_id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", numberReservation.Data)
```

## 延长电话号码预订的有效期

延长所有电话号码的预订有效期。

`POST /number_reservations/{numberreservation_id}/actions/extend`

```go
	response, err := client.NumberReservations.Actions.Extend(context.TODO(), "number_reservation_id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 列出电话号码订单

获取分页显示的电话号码订单信息。

`GET /number_orders`

```go
	page, err := client.NumberOrders.List(context.TODO(), telnyx.NumberOrderListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建电话号码订单

创建一个电话号码订单。

`POST /number_orders`

```go
	numberOrder, err := client.NumberOrders.New(context.TODO(), telnyx.NumberOrderNewParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", numberOrder.Data)
```

## 查取电话号码订单信息

获取现有的电话号码订单信息。

`GET /number_orders/{number_order_id}`

```go
	numberOrder, err := client.NumberOrders.Get(context.TODO(), "number_order_id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", numberOrder.Data)
```

## 更新电话号码订单信息

更新电话号码订单信息。

`PATCH /number_orders/{number_order_id}`

```go
	numberOrder, err := client.NumberOrders.Update(
		context.TODO(),
		"number_order_id",
		telnyx.NumberOrderUpdateParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", numberOrder.Data)
```

## 列出电话号码块订单

获取分页显示的电话号码块订单信息。

`GET /number_block_orders`

```go
	page, err := client.NumberBlockOrders.List(context.TODO(), telnyx.NumberBlockOrderListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建电话号码块订单

创建一个电话号码块订单。

`POST /number_block_orders` — 必需参数：`starting_number`、`range`

```go
	numberBlockOrder, err := client.NumberBlockOrders.New(context.TODO(), telnyx.NumberBlockOrderNewParams{
		Range:          10,
		StartingNumber: "+19705555000",
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", numberBlockOrder.Data)
```

## 查取电话号码块订单信息

获取现有的电话号码块订单信息。

`GET /number_block_orders/{number_block_order_id}`

```go
	numberBlockOrder, err := client.NumberBlockOrders.Get(context.TODO(), "number_block_order_id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", numberBlockOrder.Data)
```

## 获取与订单关联的电话号码列表

获取与订单关联的电话号码列表。

`GET /number_order_phone_numbers`

```go
	numberOrderPhoneNumbers, err := client.NumberOrderPhoneNumbers.List(context.TODO(), telnyx.NumberOrderPhoneNumberListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", numberOrderPhoneNumbers.Data)
```

## 更新电话号码订单中的需求组

`POST /number_order_phone_numbers/{id}/requirement_group` — 必需参数：`requirement_group_id`

```go
	response, err := client.NumberOrderPhoneNumbers.UpdateRequirementGroup(
		context.TODO(),
		"182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		telnyx.NumberOrderPhoneNumberUpdateRequirementGroupParams{
			RequirementGroupID: "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 查取电话号码订单中的单个电话号码

获取电话号码订单中的某个具体电话号码信息。

`GET /number_order_phone_numbers/{number_order_phone_number_id}`

```go
	numberOrderPhoneNumber, err := client.NumberOrderPhoneNumbers.Get(context.TODO(), "number_order_phone_number_id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", numberOrderPhoneNumber.Data)
```

## 更新电话号码订单中的单个电话号码的需求

更新电话号码订单中某个特定电话号码的需求信息。

`PATCH /number_order_phone_numbers/{number_order_phone_number_id}`

```go
	response, err := client.NumberOrderPhoneNumbers.UpdateRequirements(
		context.TODO(),
		"number_order_phone_number_id",
		telnyx.NumberOrderPhoneNumberUpdateRequirementsParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 列出子号码订单

获取分页显示的子号码订单信息。

`GET /sub_number_orders`

```go
	subNumberOrders, err := client.SubNumberOrders.List(context.TODO(), telnyx.SubNumberOrderListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", subNumberOrders.Data)
```

## 更新子号码订单的需求组

`POST /sub_number_orders/{id}/requirement_group` — 必需参数：`requirement_group_id`

```go
	response, err := client.SubNumberOrders.UpdateRequirementGroup(
		context.TODO(),
		"182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		telnyx.SubNumberOrderUpdateRequirementGroupParams{
			RequirementGroupID: "a4b201f9-8646-4e54-a7d2-b2e403eeaf8c",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 查取子号码订单信息

获取现有的子号码订单信息。

`GET /sub_number_orders/{sub_number_order_id}`

```go
	subNumberOrder, err := client.SubNumberOrders.Get(
		context.TODO(),
		"sub_number_order_id",
		telnyx.SubNumberOrderGetParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", subNumberOrder.Data)
```

## 更新子号码订单的需求信息

更新子号码订单的需求信息。

`PATCH /sub_number_orders/{sub_number_order_id}`

```go
	subNumberOrder, err := client.SubNumberOrders.Update(
		context.TODO(),
		"sub_number_order_id",
		telnyx.SubNumberOrderUpdateParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", subNumberOrder.Data)
```

## 取消子号码订单

允许取消处于“待处理”状态的子号码订单。

`PATCH /sub_number_orders/{sub_number_order_id}/cancel`

```go
	response, err := client.SubNumberOrders.Cancel(context.TODO(), "sub_number_order_id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 创建子号码订单报告

为子号码订单生成 CSV 报告。

`POST /sub_number_orders/report`

```go
	subNumberOrdersReport, err := client.SubNumberOrdersReport.New(context.TODO(), telnyx.SubNumberOrdersReportNewParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", subNumberOrdersReport.Data)
```

## 查取子号码订单报告

获取子号码订单的报告状态和详细信息。

`GET /sub_number_orders/report/{report_id}`

```go
	subNumberOrdersReport, err := client.SubNumberOrdersReport.Get(context.TODO(), "12ade33a-21c0-473b-b055-b3c836e1c293")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", subNumberOrdersReport.Data)
```

## 下载子号码订单报告

下载已完成的子号码订单的 CSV 文件。

`GET /sub_number_orders/report/{report_id}/download`

```go
	response, err := client.SubNumberOrdersReport.Download(context.TODO(), "12ade33a-21c0-473b-b055-b3c836e1c293")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response)
```

## 列出高级订单

获取高级订单信息。

`GET /advanced_orders`

```go
	advancedOrders, err := client.AdvancedOrders.List(context.TODO())
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", advancedOrders.Data)
```

## 创建高级订单

`POST /advanced_orders`

```go
	advancedOrder, err := client.AdvancedOrders.New(context.TODO(), telnyx.AdvancedOrderNewParams{
		AdvancedOrder: telnyx.AdvancedOrderParam{},
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", advancedOrder.ID)
```

## 更新高级订单

`PATCH /advanced_orders/{advanced-order-id}/requirement_group`

```go
	response, err := client.AdvancedOrders.UpdateRequirementGroup(
		context.TODO(),
		"182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		telnyx.AdvancedOrderUpdateRequirementGroupParams{
			AdvancedOrder: telnyx.AdvancedOrderParam{},
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.ID)
```

## 获取高级订单信息

`GET /advanced_orders/{order_id}`

```go
	advancedOrder, err := client.AdvancedOrders.Get(context.TODO(), "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", advancedOrder.ID)
```

## 获取非明确指定的电话号码订单

获取分页显示的非明确指定电话号码订单信息。

`GET /inexplicit_number_orders`

```go
	page, err := client.InexplicitNumberOrders.List(context.TODO(), telnyx.InexplicitNumberOrderListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建非明确指定的电话号码订单

创建一个非明确指定的电话号码订单，以便在不指定具体号码的情况下程序化购买电话号码。

`POST /inexplicit_number_orders` — 必需参数：`ordering_groups`

```go
	inexplicitNumberOrder, err := client.InexplicitNumberOrders.New(context.TODO(), telnyx.InexplicitNumberOrderNewParams{
		OrderingGroups: []telnyx.InexplicitNumberOrderNewParamsOrderingGroup{{
			CountRequested:  "count_requested",
			CountryISO:      "US",
			PhoneNumberType: "phone_number_type",
		}},
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", inexplicitNumberOrder.Data)
```

## 查取非明确指定的电话号码订单信息

根据 ID 获取现有的非明确指定电话号码订单。

`GET /inexplicit_number_orders/{id}`

```go
	inexplicitNumberOrder, err := client.InexplicitNumberOrders.Get(context.TODO(), "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", inexplicitNumberOrder.Data)
```

## 查取所有评论

获取所有评论信息。

`GET /comments`

```go
	comments, err := client.Comments.List(context.TODO(), telnyx.CommentListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", comments.Data)
```

## 创建评论

`POST /comments`

```go
	comment, err := client.Comments.New(context.TODO(), telnyx.CommentNewParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", comment.Data)
```

## 查取评论信息

`GET /comments/{id}`

```go
	comment, err := client.Comments.Get(context.TODO(), "id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", comment.Data)
```

## 将评论标记为已读

`PATCH /comments/{id}/read`

```go
	response, err := client.Comments.MarkAsRead(context.TODO(), "id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 列出可用的电话号码块

获取可用的电话号码块信息。

`GET /available_phone_number_blocks`

```go
	availablePhoneNumberBlocks, err := client.AvailablePhoneNumberBlocks.List(context.TODO(), telnyx.AvailablePhoneNumberBlockListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", availablePhoneNumberBlocks.Data)
```

## 列出可用的电话号码

获取可用的电话号码信息。

`GET /available_phone_numbers`

```go
	availablePhoneNumbers, err := client.AvailablePhoneNumbers.List(context.TODO(), telnyx.AvailablePhoneNumberListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", availablePhoneNumbers.Data)
```

## 获取电话号码列表的相关信息

`POST /numbers_features` — 必需参数：`phone_numbers`

```go
	numbersFeature, err := client.NumbersFeatures.New(context.TODO(), telnyx.NumbersFeatureNewParams{
		PhoneNumbers: []string{"string"},
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", numbersFeature.Data)
```

---

## Webhook

以下 Webhook 事件会被发送到您配置的 Webhook URL。所有 Webhook 都包含 `telnyx-timestamp` 和 `telnyx-signature-ed25519` 标头以进行验证（兼容标准 Webhook）。

| 事件 | 描述 |
|-------|-------------|
| `numberOrderStatusUpdate` | 电话号码订单状态更新 |
```
```