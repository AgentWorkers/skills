---
name: telnyx-iot-go
description: >-
  Manage IoT SIM cards, eSIMs, data plans, and wireless connectivity. Use when
  building IoT/M2M solutions. This skill provides Go SDK examples.
metadata:
  author: telnyx
  product: iot
  language: go
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx Iot - Go

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

以下所有示例均假设 `client` 已按照上述方式初始化。

## 获取所有无线区域

检索指定产品的所有无线区域。

`GET /wireless/regions`

```go
	response, err := client.Wireless.GetRegions(context.TODO(), telnyx.WirelessGetRegionsParams{
		Product: "public_ips",
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 获取所有 SIM 卡

获取符合指定过滤条件的用户拥有的所有 SIM 卡。

`GET /sim_cards`

```go
	page, err := client.SimCards.List(context.TODO(), telnyx.SimCardListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 获取 SIM 卡详情

返回特定 SIM 卡的详细信息。

`GET /sim_cards/{id}`

```go
	simCard, err := client.SimCards.Get(
		context.TODO(),
		"6a09cdc3-8948-47f0-aa62-74ac943d6c58",
		telnyx.SimCardGetParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", simCard.Data)
```

## 更新 SIM 卡

更新 SIM 卡的数据

`PATCH /sim_cards/{id}`

```go
	simCard, err := client.SimCards.Update(
		context.TODO(),
		"6a09cdc3-8948-47f0-aa62-74ac943d6c58",
		telnyx.SimCardUpdateParams{
			SimCard: telnyx.SimCardParam{},
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", simCard.Data)
```

## 删除 SIM 卡

SIM 卡将被停用，从您的账户中移除，且您将不再被收取费用。<br />删除完成后，SIM 卡将无法连接到网络。

`DELETE /sim_cards/{id}`

```go
	simCard, err := client.SimCards.Delete(
		context.TODO(),
		"6a09cdc3-8948-47f0-aa62-74ac943d6c58",
		telnyx.SimCardDeleteParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", simCard.Data)
```

## 获取 eSIM 的激活码

返回 eSIM 的激活码。<br/>
此 API 仅适用于 eSIM。

`GET /sim_cards/{id}/activation_code`

```go
	response, err := client.SimCards.GetActivationCode(context.TODO(), "6a09cdc3-8948-47f0-aa62-74ac943d6c58")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 获取 SIM 卡设备详情

返回当前正在使用该 SIM 卡的设备详情。

`GET /sim_cards/{id}/device_details`

```go
	response, err := client.SimCards.GetDeviceDetails(context.TODO(), "6a09cdc3-8948-47f0-aa62-74ac943d6c58")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 获取 SIM 卡的公共 IP 地址

返回 SIM 卡的公共 IP 地址。

`GET /sim_cards/{id}/public_ip`

```go
	response, err := client.SimCards.GetPublicIP(context.TODO(), "6a09cdc3-8948-47f0-aa62-74ac943d6c58")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 列出无线连接日志

此 API 可用于列出与 SIM 卡关联的无线连接日志（分页显示），以便进行故障排查。

`GET /sim_cards/{id}/wireless_connectivity_logs`

```go
	page, err := client.SimCards.ListWirelessConnectivityLogs(
		context.TODO(),
		"6a09cdc3-8948-47f0-aa62-74ac943d6c58",
		telnyx.SimCardListWirelessConnectivityLogsParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 请求禁用 SIM 卡

此 API 会禁用 SIM 卡，使其无法连接到网络。

`POST /sim_cards/{id}/actions/disable`

```go
	response, err := client.SimCards.Actions.Disable(context.TODO(), "6a09cdc3-8948-47f0-aa62-74ac943d6c58")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 请求启用 SIM 卡

此 API 会启用 SIM 卡，使其能够连接到网络。<br/>要启用 SIM 卡，必须先将其关联到一个 SIM 卡组。

`POST /sim_cards/{id}/actions/enable`

```go
	response, err := client.SimCards.Actions.Enable(context.TODO(), "6a09cdc3-8948-47f0-aa62-74ac943d6c58")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 请求删除 SIM 卡的公共 IP 地址

此 API 会删除 SIM 卡的公共 IP 地址。

`POST /sim_cards/{id}/actions/remove_public_ip`

```go
	response, err := client.SimCards.Actions.RemovePublicIP(context.TODO(), "6a09cdc3-8948-47f0-aa62-74ac943d6c58")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 请求设置 SIM 卡的公共 IP 地址

此 API 会为 SIM 卡分配一个随机公共 IP 地址，使其能够在公共互联网上使用。

`POST /sim_cards/{id}/actions/set_public_ip`

```go
	response, err := client.SimCards.Actions.SetPublicIP(
		context.TODO(),
		"6a09cdc3-8948-47f0-aa62-74ac943d6c58",
		telnyx.SimCardActionSetPublicIPParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 请求将 SIM 卡设置为待机状态

设置 SIM 卡为待机状态后，它将能够重新连接到网络。

`POST /sim_cards/{id}/actions/set_standby`

```go
	response, err := client.SimCards.Actions.SetStandby(context.TODO(), "6a09cdc3-8948-47f0-aa62-74ac943d6c58")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 请求批量设置 SIM 卡的公共 IP 地址

此 API 会为指定的每个 SIM 卡批量设置公共 IP 地址。<br/>每个 SIM 卡都会触发一个异步操作。

`POST /sim_cards/actions/bulk_set_public_ips` — 必需参数：`sim_card_ids`

```go
	response, err := client.SimCards.Actions.BulkSetPublicIPs(context.TODO(), telnyx.SimCardActionBulkSetPublicIPsParams{
		SimCardIDs: []string{"6b14e151-8493-4fa1-8664-1cc4e6d14158"},
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 验证 SIM 卡注册码

验证 SIM 卡注册码是否有效。

`POST /sim_cards/actions/validate_registration_codes`

```go
	response, err := client.SimCards.Actions.ValidateRegistrationCodes(context.TODO(), telnyx.SimCardActionValidateRegistrationCodesParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 列出 SIM 卡操作记录

此 API 可列出 SIM 卡的操作记录（分页显示）。

`GET /sim_card_actions`

```go
	page, err := client.SimCards.Actions.List(context.TODO(), telnyx.SimCardActionListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 获取 SIM 卡操作详情

此 API 可获取特定 SIM 卡操作的详细信息，以便跟进已进行的异步操作。

`GET /sim_card_actions/{id}`

```go
	action, err := client.SimCards.Actions.Get(context.TODO(), "6a09cdc3-8948-47f0-aa62-74ac943d6c58")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", action.Data)
```

## 列出批量 SIM 卡操作记录

此 API 可列出批量 SIM 卡的操作记录（分页显示）。

`GET /bulk_sim_card_actions`

```go
	page, err := client.BulkSimCardActions.List(context.TODO(), telnyx.BulkSimCardActionListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 获取批量 SIM 卡操作详情

此 API 可获取批量 SIM 卡操作的详细信息。

`GET /bulk_sim_card_actions/{id}`

```go
	bulkSimCardAction, err := client.BulkSimCardActions.Get(context.TODO(), "6a09cdc3-8948-47f0-aa62-74ac943d6c58")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", bulkSimCardAction.Data)
```

## 获取所有 SIM 卡组

检索符合指定过滤条件的用户拥有的所有 SIM 卡组。

`GET /sim_card_groups`

```go
	page, err := client.SimCardGroups.List(context.TODO(), telnyx.SimCardGroupListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建 SIM 卡组

创建一个新的 SIM 卡组。

`POST /sim_card_groups` — 必需参数：`name`

```go
	simCardGroup, err := client.SimCardGroups.New(context.TODO(), telnyx.SimCardGroupNewParams{
		Name: "My Test Group",
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", simCardGroup.Data)
```

## 获取 SIM 卡组详情

返回特定 SIM 卡组的详细信息。

`GET /sim_card_groups/{id}`

```go
	simCardGroup, err := client.SimCardGroups.Get(
		context.TODO(),
		"6a09cdc3-8948-47f0-aa62-74ac943d6c58",
		telnyx.SimCardGroupGetParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", simCardGroup.Data)
```

## 更新 SIM 卡组

更新 SIM 卡组。

`PATCH /sim_card_groups/{id}`

```go
	simCardGroup, err := client.SimCardGroups.Update(
		context.TODO(),
		"6a09cdc3-8948-47f0-aa62-74ac943d6c58",
		telnyx.SimCardGroupUpdateParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", simCardGroup.Data)
```

## 删除 SIM 卡组

永久删除 SIM 卡组。

`DELETE /sim_card_groups/{id}`

```go
	simCardGroup, err := client.SimCardGroups.Delete(context.TODO(), "6a09cdc3-8948-47f0-aa62-74ac943d6c58")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", simCardGroup.Data)
```

## 从 SIM 卡组中移除私有无线网关

此操作会异步地从 SIM 卡组中移除现有的私有无线网关。

`POST /sim_card_groups/{id}/actions/remove_private_wireless_gateway`

```go
	response, err := client.SimCardGroups.Actions.RemovePrivateWirelessGateway(context.TODO(), "6a09cdc3-8948-47f0-aa62-74ac943d6c58")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 从 SIM 卡组中移除无线阻止列表

此操作会异步地从 SIM 卡组中的所有 SIM 卡中移除现有的无线阻止列表。

`POST /sim_card_groups/{id}/actions/remove_wireless_blocklist`

```go
	response, err := client.SimCardGroups.Actions.RemoveWirelessBlocklist(context.TODO(), "6a09cdc3-8948-47f0-aa62-74ac943d6c58")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 为 SIM 卡组分配私有无线网关

此操作会异步地为 SIM 卡组分配一个私有无线网关。

`POST /sim_card_groups/{id}/actions/set_private_wireless_gateway` — 必需参数：`private_wireless_gateway_id`

```go
	response, err := client.SimCardGroups.Actions.SetPrivateWirelessGateway(
		context.TODO(),
		"6a09cdc3-8948-47f0-aa62-74ac943d6c58",
		telnyx.SimCardGroupActionSetPrivateWirelessGatewayParams{
			PrivateWirelessGatewayID: "6a09cdc3-8948-47f0-aa62-74ac943d6c58",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 为 SIM 卡组分配无线阻止列表

此操作会异步地为 SIM 卡组中的所有 SIM 卡分配一个无线阻止列表。

`POST /sim_card_groups/{id}/actions/set_wireless_blocklist` — 必需参数：`wireless_blocklist_id`

```go
	response, err := client.SimCardGroups.Actions.SetWirelessBlocklist(
		context.TODO(),
		"6a09cdc3-8948-47f0-aa62-74ac943d6c58",
		telnyx.SimCardGroupActionSetWirelessBlocklistParams{
			WirelessBlocklistID: "6a09cdc3-8948-47f0-aa62-74ac943d6c58",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 列出 SIM 卡组操作记录

此 API 可列出 SIM 卡组的操作记录（分页显示）。

`GET /sim_card_group_actions`

```go
	page, err := client.SimCardGroups.Actions.List(context.TODO(), telnyx.SimCardGroupActionListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 获取 SIM 卡组操作详情

此 API 可获取 SIM 卡组操作的详细信息，以便跟进已进行的异步操作。

`GET /sim_card_group_actions/{id}`

```go
	action, err := client.SimCardGroups.Actions.Get(context.TODO(), "6a09cdc3-8948-47f0-aa62-74ac943d6c58")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", action.Data)
```

## 获取所有 SIM 卡订单

根据过滤条件获取所有 SIM 卡的订单信息。

`GET /sim_card_orders`

```go
	page, err := client.SimCardOrders.List(context.TODO(), telnyx.SimCardOrderListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建 SIM 卡订单

创建新的 SIM 卡订单。

`POST /sim_card_orders` — 必需参数：`address_id`, `quantity`

```go
	simCardOrder, err := client.SimCardOrders.New(context.TODO(), telnyx.SimCardOrderNewParams{
		AddressID: "1293384261075731499",
		Quantity:  23,
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", simCardOrder.Data)
```

## 获取单个 SIM 卡订单

根据订单 ID 获取单个 SIM 卡的订单信息。

`GET /sim_card_orders/{id}`

```go
	simCardOrder, err := client.SimCardOrders.Get(context.TODO(), "6a09cdc3-8948-47f0-aa62-74ac943d6c58")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", simCardOrder.Data)
```

## 预览 SIM 卡订单

预览 SIM 卡的购买信息。

`POST /sim_card_order_preview` — 必需参数：`quantity`, `address_id`

```go
	response, err := client.SimCardOrderPreview.Preview(context.TODO(), telnyx.SimCardOrderPreviewPreviewParams{
		AddressID: "1293384261075731499",
		Quantity:  21,
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 列出 SIM 卡数据使用通知

列出 SIM 卡的数据使用通知记录（分页显示）。

`GET /sim_card_data_usage_notifications`

```go
	page, err := client.SimCardDataUsageNotifications.List(context.TODO(), telnyx.SimCardDataUsageNotificationListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建新的 SIM 卡数据使用通知

创建新的 SIM 卡数据使用通知。

`POST /sim_card_data_usage_notifications` — 必需参数：`sim_card_id`, `threshold`

```go
	simCardDataUsageNotification, err := client.SimCardDataUsageNotifications.New(context.TODO(), telnyx.SimCardDataUsageNotificationNewParams{
		SimCardID: "6a09cdc3-8948-47f0-aa62-74ac943d6c58",
		Threshold: telnyx.SimCardDataUsageNotificationNewParamsThreshold{},
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", simCardDataUsageNotification.Data)
```

## 获取单个 SIM 卡数据使用通知

获取单个 SIM 卡的数据使用通知。

`GET /sim_card_data_usage_notifications/{id}`

```go
	simCardDataUsageNotification, err := client.SimCardDataUsageNotifications.Get(context.TODO(), "6a09cdc3-8948-47f0-aa62-74ac943d6c58")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", simCardDataUsageNotification.Data)
```

## 更新 SIM 卡数据使用通知信息

更新 SIM 卡数据使用通知的信息。

`PATCH /sim_card_data_usage_notifications/{id}`

```go
	simCardDataUsageNotification, err := client.SimCardDataUsageNotifications.Update(
		context.TODO(),
		"6a09cdc3-8948-47f0-aa62-74ac943d6c58",
		telnyx.SimCardDataUsageNotificationUpdateParams{
			SimCardDataUsageNotification: telnyx.SimCardDataUsageNotificationParam{},
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", simCardDataUsageNotification.Data)
```

## 删除 SIM 卡数据使用通知

删除 SIM 卡的数据使用通知。

`DELETE /sim_card_data_usage_notifications/{id}`

```go
	simCardDataUsageNotification, err := client.SimCardDataUsageNotifications.Delete(context.TODO(), "6a09cdc3-8948-47f0-aa62-74ac943d6c58")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", simCardDataUsageNotification.Data)
```

## 购买 eSIM

购买指定数量的 eSIM 并将其注册到当前用户的账户。<br/>
如果提供了 `sim_card_group_id`，这些 eSIM 将与该组关联。

`POST /actions/purchase/esims` — 必需参数：`amount`

```go
	purchase, err := client.Actions.Purchase.New(context.TODO(), telnyx.ActionPurchaseNewParams{
		Amount: 10,
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", purchase.Data)
```

## 注册 SIM 卡

将提供的注册码对应的 SIM 卡注册到当前用户的账户。<br/>
如果提供了 `sim_card_group_id`，这些 SIM 卡将与该组关联。

`POST /actions/register/sim_cards` — 必需参数：`registration_codes`

```go
	register, err := client.Actions.Register.New(context.TODO(), telnyx.ActionRegisterNewParams{
		RegistrationCodes: []string{"0000000001", "0000000002", "0000000003"},
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", register.Data)
```

## 获取 OTA 更新信息

获取所有 OTA（Over the Air）更新信息。

`GET /ota_updates`

```go
	page, err := client.OtaUpdates.List(context.TODO(), telnyx.OtaUpdateListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 获取 OTA 更新详情

此 API 返回 OTA 更新的详细信息。

`GET /ota_updates/{id}`

```go
	otaUpdate, err := client.OtaUpdates.Get(context.TODO(), "6a09cdc3-8948-47f0-aa62-74ac943d6c58")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", otaUpdate.Data)
```

## 获取所有私有无线网关

获取用户拥有的所有私有无线网关。

`GET /private_wireless_gateways`

```go
	page, err := client.PrivateWirelessGateways.List(context.TODO(), telnyx.PrivateWirelessGatewayListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建私有无线网关

为已创建的网络异步创建一个私有无线网关。

`POST /private_wireless_gateways` — 必需参数：`network_id`, `name`

```go
	privateWirelessGateway, err := client.PrivateWirelessGateways.New(context.TODO(), telnyx.PrivateWirelessGatewayNewParams{
		Name:      "My private wireless gateway",
		NetworkID: "6a09cdc3-8948-47f0-aa62-74ac943d6c58",
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", privateWirelessGateway.Data)
```

## 获取私有无线网关详情

检索私有无线网关的详细信息。

`GET /private_wireless_gateways/{id}`

```go
	privateWirelessGateway, err := client.PrivateWirelessGateways.Get(context.TODO(), "6a09cdc3-8948-47f0-aa62-74ac943d6c58")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", privateWirelessGateway.Data)
```

## 删除私有无线网关

删除私有无线网关。

`DELETE /private_wireless_gateways/{id}`

```go
	privateWirelessGateway, err := client.PrivateWirelessGateways.Delete(context.TODO(), "6a09cdc3-8948-47f0-aa62-74ac943d6c58")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", privateWirelessGateway.Data)
```

## 获取所有无线阻止列表

获取用户拥有的所有无线阻止列表。

`GET /wireless_blocklists`

```go
	page, err := client.WirelessBlocklists.List(context.TODO(), telnyx.WirelessBlocklistListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建无线阻止列表

创建一个无线阻止列表，以防止 SIM 卡连接到特定网络。

`POST /wireless_blocklists` — 必需参数：`name`, `type`, `values`

```go
	wirelessBlocklist, err := client.WirelessBlocklists.New(context.TODO(), telnyx.WirelessBlocklistNewParams{
		Name:   "My Wireless Blocklist",
		Type:   telnyx.WirelessBlocklistNewParamsTypeCountry,
		Values: []string{"CA", "US"},
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", wirelessBlocklist.Data)
```

## 更新无线阻止列表

更新无线阻止列表。

`PATCH /wireless_blocklists`

```go
	wirelessBlocklist, err := client.WirelessBlocklists.Update(context.TODO(), telnyx.WirelessBlocklistUpdateParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", wirelessBlocklist.Data)
```

## 获取无线阻止列表详情

检索无线阻止列表的详细信息。

`GET /wireless_blocklists/{id}`

```go
	wirelessBlocklist, err := client.WirelessBlocklists.Get(context.TODO(), "6a09cdc3-8948-47f0-aa62-74ac943d6c58")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", wirelessBlocklist.Data)
```

## 删除无线阻止列表

删除无线阻止列表。

`DELETE /wireless_blocklists/{id}`

```go
	wirelessBlocklist, err := client.WirelessBlocklists.Delete(context.TODO(), "6a09cdc3-8948-47f0-aa62-74ac943d6c58")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", wirelessBlocklist.Data)
```

## 获取所有无线阻止列表的值

检索指定类型的无线阻止列表的所有值。

`GET /wireless_blocklist_values`

```go
	wirelessBlocklistValues, err := client.WirelessBlocklistValues.List(context.TODO(), telnyx.WirelessBlocklistValueListParams{
		Type: telnyx.WirelessBlocklistValueListParamsTypeCountry,
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", wirelessBlocklistValues.Data)
```
```