---
name: telnyx-iot-java
description: >-
  Manage IoT SIM cards, eSIMs, data plans, and wireless connectivity. Use when
  building IoT/M2M solutions. This skill provides Java SDK examples.
metadata:
  author: telnyx
  product: iot
  language: java
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx Iot - Java

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

## 获取所有无线区域

检索指定产品的所有无线区域。

`GET /wireless/regions`

```java
import com.telnyx.sdk.models.wireless.WirelessRetrieveRegionsParams;
import com.telnyx.sdk.models.wireless.WirelessRetrieveRegionsResponse;

WirelessRetrieveRegionsParams params = WirelessRetrieveRegionsParams.builder()
    .product("public_ips")
    .build();
WirelessRetrieveRegionsResponse response = client.wireless().retrieveRegions(params);
```

## 获取所有 SIM 卡

获取符合给定过滤条件的用户拥有的所有 SIM 卡。

`GET /sim_cards`

```java
import com.telnyx.sdk.models.simcards.SimCardListPage;
import com.telnyx.sdk.models.simcards.SimCardListParams;

SimCardListPage page = client.simCards().list();
```

## 获取 SIM 卡详情

返回特定 SIM 卡的详细信息。

`GET /sim_cards/{id}`

```java
import com.telnyx.sdk.models.simcards.SimCardRetrieveParams;
import com.telnyx.sdk.models.simcards.SimCardRetrieveResponse;

SimCardRetrieveResponse simCard = client.simCards().retrieve("6a09cdc3-8948-47f0-aa62-74ac943d6c58");
```

## 更新 SIM 卡

更新 SIM 卡数据

`PATCH /sim_cards/{id}`

```java
import com.telnyx.sdk.models.simcards.SimCard;
import com.telnyx.sdk.models.simcards.SimCardUpdateParams;
import com.telnyx.sdk.models.simcards.SimCardUpdateResponse;

SimCardUpdateParams params = SimCardUpdateParams.builder()
    .simCardId("6a09cdc3-8948-47f0-aa62-74ac943d6c58")
    .simCard(SimCard.builder().build())
    .build();
SimCardUpdateResponse simCard = client.simCards().update(params);
```

## 删除 SIM 卡

SIM 卡将被停用，从您的账户中移除，您将不再被收取费用。<br />删除完成后，SIM 卡将无法连接到网络。

`DELETE /sim_cards/{id}`

```java
import com.telnyx.sdk.models.simcards.SimCardDeleteParams;
import com.telnyx.sdk.models.simcards.SimCardDeleteResponse;

SimCardDeleteResponse simCard = client.simCards().delete("6a09cdc3-8948-47f0-aa62-74ac943d6c58");
```

## 获取 eSIM 的激活码

返回 eSIM 的激活码。<br/>
此 API 仅适用于 eSIM。

`GET /sim_cards/{id}/activation_code`

```java
import com.telnyx.sdk.models.simcards.SimCardGetActivationCodeParams;
import com.telnyx.sdk.models.simcards.SimCardGetActivationCodeResponse;

SimCardGetActivationCodeResponse response = client.simCards().getActivationCode("6a09cdc3-8948-47f0-aa62-74ac943d6c58");
```

## 获取 SIM 卡设备详情

返回当前正在使用该 SIM 卡的设备详情。

`GET /sim_cards/{id}/device_details`

```java
import com.telnyx.sdk.models.simcards.SimCardGetDeviceDetailsParams;
import com.telnyx.sdk.models.simcards.SimCardGetDeviceDetailsResponse;

SimCardGetDeviceDetailsResponse response = client.simCards().getDeviceDetails("6a09cdc3-8948-47f0-aa62-74ac943d6c58");
```

## 获取 SIM 卡的公共 IP 地址

返回 SIM 卡的公共 IP 地址。

`GET /sim_cards/{id}/public_ip`

```java
import com.telnyx.sdk.models.simcards.SimCardGetPublicIpParams;
import com.telnyx.sdk.models.simcards.SimCardGetPublicIpResponse;

SimCardGetPublicIpResponse response = client.simCards().getPublicIp("6a09cdc3-8948-47f0-aa62-74ac943d6c58");
```

## 列出无线连接日志

此 API 可用于列出与 SIM 卡关联的无线连接日志（分页显示），以便进行故障排除。

`GET /sim_cards/{id}/wireless_connectivity_logs`

```java
import com.telnyx.sdk.models.simcards.SimCardListWirelessConnectivityLogsPage;
import com.telnyx.sdk.models.simcards.SimCardListWirelessConnectivityLogsParams;

SimCardListWirelessConnectivityLogsPage page = client.simCards().listWirelessConnectivityLogs("6a09cdc3-8948-47f0-aa62-74ac943d6c58");
```

## 请求禁用 SIM 卡

此 API 会禁用 SIM 卡，使其无法连接到网络并无法使用数据。<br/>
该 API 将触发一个异步操作（称为 SIM 卡操作）。

`POST /sim_cards/{id}/actions/disable`

```java
import com.telnyx.sdk.models.simcards.actions.ActionDisableParams;
import com.telnyx.sdk.models.simcards.actions.ActionDisableResponse;

ActionDisableResponse response = client.simCards().actions().disable("6a09cdc3-8948-47f0-aa62-74ac943d6c58");
```

## 请求启用 SIM 卡

此 API 会启用 SIM 卡，使其能够连接到网络并可以使用数据。<br/>
要启用 SIM 卡，必须先将其关联到一个 SIM 卡组。<br/>
该 API 将触发一个异步操作...

`POST /sim_cards/{id}/actions/enable`

```java
import com.telnyx.sdk.models.simcards.actions.ActionEnableParams;
import com.telnyx.sdk.models.simcards.actions.ActionEnableResponse;

ActionEnableResponse response = client.simCards().actions().enable("6a09cdc3-8948-47f0-aa62-74ac943d6c58");
```

## 请求删除 SIM 卡的公共 IP 地址

此 API 会删除 SIM 卡的现有公共 IP 地址。

`POST /sim_cards/{id}/actions/remove_public_ip`

```java
import com.telnyx.sdk.models.simcards.actions.ActionRemovePublicIpParams;
import com.telnyx.sdk.models.simcards.actions.ActionRemovePublicIpResponse;

ActionRemovePublicIpResponse response = client.simCards().actions().removePublicIp("6a09cdc3-8948-47f0-aa62-74ac943d6c58");
```

## 请求设置 SIM 卡的公共 IP 地址

此 API 会为 SIM 卡分配一个随机公共 IP 地址，使其可以在公共互联网上使用。

`POST /sim_cards/{id}/actions/set_public_ip`

```java
import com.telnyx.sdk.models.simcards.actions.ActionSetPublicIpParams;
import com.telnyx.sdk.models.simcards.actions.ActionSetPublicIpResponse;

ActionSetPublicIpResponse response = client.simCards().actions().setPublicIp("6a09cdc3-8948-47f0-aa62-74ac943d6c58");
```

## 请求将 SIM 卡设置为待机状态

设置 SIM 卡为待机状态后，它将能够重新连接到网络并可以使用数据。<br/>
要设置 SIM 卡为待机状态，必须先...

`POST /sim_cards/{id}/actions/set_standby`

```java
import com.telnyx.sdk.models.simcards.actions.ActionSetStandbyParams;
import com.telnyx.sdk.models.simcards.actions.ActionSetStandbyResponse;

ActionSetStandbyResponse response = client.simCards().actions().setStandby("6a09cdc3-8948-47f0-aa62-74ac943d6c58");
```

## 批量设置 SIM 卡的公共 IP 地址

此 API 会为指定的每个 SIM 卡设置公共 IP 地址（异步操作）。

`POST /sim_cards/actions/bulk_set_public_ips` — 必需参数：`sim_card_ids`

```java
import com.telnyx.sdk.models.simcards.actions.ActionBulkSetPublicIpsParams;
import com.telnyx.sdk.models.simcards.actions.ActionBulkSetPublicIpsResponse;

ActionBulkSetPublicIpsParams params = ActionBulkSetPublicIpsParams.builder()
    .addSimCardId("6b14e151-8493-4fa1-8664-1cc4e6d14158")
    .build();
ActionBulkSetPublicIpsResponse response = client.simCards().actions().bulkSetPublicIps(params);
```

## 验证 SIM 卡注册码

验证 SIM 卡注册码是否有效。

`POST /sim_cards/actions/validate_registration_codes`

```java
import com.telnyx.sdk.models.simcards.actions.ActionValidateRegistrationCodesParams;
import com.telnyx.sdk.models.simcards.actions.ActionValidateRegistrationCodesResponse;

ActionValidateRegistrationCodesResponse response = client.simCards().actions().validateRegistrationCodes();
```

## 列出 SIM 卡操作

此 API 可用于列出 SIM 卡操作的列表（分页显示）。

`GET /sim_card_actions`

```java
import com.telnyx.sdk.models.simcards.actions.ActionListPage;
import com.telnyx.sdk.models.simcards.actions.ActionListParams;

ActionListPage page = client.simCards().actions().list();
```

## 获取 SIM 卡操作详情

此 API 可用于获取特定 SIM 卡操作的详细信息（用于跟进已进行的异步操作）。

`GET /sim_card_actions/{id}`

```java
import com.telnyx.sdk.models.simcards.actions.ActionRetrieveParams;
import com.telnyx.sdk.models.simcards.actions.ActionRetrieveResponse;

ActionRetrieveResponse action = client.simCards().actions().retrieve("6a09cdc3-8948-47f0-aa62-74ac943d6c58");
```

## 列出批量 SIM 卡操作

此 API 可用于列出批量 SIM 卡操作的列表（分页显示）。

`GET /bulk_sim_card_actions`

```java
import com.telnyx.sdk.models.bulksimcardactions.BulkSimCardActionListPage;
import com.telnyx.sdk.models.bulksimcardactions.BulkSimCardActionListParams;

BulkSimCardActionListPage page = client.bulkSimCardActions().list();
```

## 获取批量 SIM 卡操作详情

此 API 可用于获取批量 SIM 卡操作的详细信息。

`GET /bulk_sim_card_actions/{id}`

```java
import com.telnyx.sdk.models.bulksimcardactions.BulkSimCardActionRetrieveParams;
import com.telnyx.sdk.models.bulksimcardactions.BulkSimCardActionRetrieveResponse;

BulkSimCardActionRetrieveResponse bulkSimCardAction = client.bulkSimCardActions().retrieve("6a09cdc3-8948-47f0-aa62-74ac943d6c58");
```

## 获取所有 SIM 卡组

检索符合给定过滤条件的用户拥有的所有 SIM 卡组。

`GET /sim_card_groups`

```java
import com.telnyx.sdk.models.simcardgroups.SimCardGroupListPage;
import com.telnyx.sdk.models.simcardgroups.SimCardGroupListParams;

SimCardGroupListPage page = client.simCardGroups().list();
```

## 创建 SIM 卡组

创建一个新的 SIM 卡组。

`POST /sim_card_groups` — 必需参数：`name`

```java
import com.telnyx.sdk.models.simcardgroups.SimCardGroupCreateParams;
import com.telnyx.sdk.models.simcardgroups.SimCardGroupCreateResponse;

SimCardGroupCreateParams params = SimCardGroupCreateParams.builder()
    .name("My Test Group")
    .build();
SimCardGroupCreateResponse simCardGroup = client.simCardGroups().create(params);
```

## 获取 SIM 卡组详情

返回特定 SIM 卡组的详细信息。

`GET /sim_card_groups/{id}`

```java
import com.telnyx.sdk.models.simcardgroups.SimCardGroupRetrieveParams;
import com.telnyx.sdk.models.simcardgroups.SimCardGroupRetrieveResponse;

SimCardGroupRetrieveResponse simCardGroup = client.simCardGroups().retrieve("6a09cdc3-8948-47f0-aa62-74ac943d6c58");
```

## 更新 SIM 卡组

更新 SIM 卡组。

`PATCH /sim_card_groups/{id}`

```java
import com.telnyx.sdk.models.simcardgroups.SimCardGroupUpdateParams;
import com.telnyx.sdk.models.simcardgroups.SimCardGroupUpdateResponse;

SimCardGroupUpdateResponse simCardGroup = client.simCardGroups().update("6a09cdc3-8948-47f0-aa62-74ac943d6c58");
```

## 删除 SIM 卡组

永久删除 SIM 卡组。

`DELETE /sim_card_groups/{id}`

```java
import com.telnyx.sdk.models.simcardgroups.SimCardGroupDeleteParams;
import com.telnyx.sdk.models.simcardgroups.SimCardGroupDeleteResponse;

SimCardGroupDeleteResponse simCardGroup = client.simCardGroups().delete("6a09cdc3-8948-47f0-aa62-74ac943d6c58");
```

## 从 SIM 卡组中删除私有无线网关

此操作会异步地从 SIM 卡组中删除现有的私有无线网关。

`POST /sim_card_groups/{id}/actions/remove_private_wireless_gateway`

```java
import com.telnyx.sdk.models.simcardgroups.actions.ActionRemovePrivateWirelessGatewayParams;
import com.telnyx.sdk.models.simcardgroups.actions.ActionRemovePrivateWirelessGatewayResponse;

ActionRemovePrivateWirelessGatewayResponse response = client.simCardGroups().actions().removePrivateWirelessGateway("6a09cdc3-8948-47f0-aa62-74ac943d6c58");
```

## 从 SIM 卡组中删除无线阻止列表

此操作会异步地从 SIM 卡组中的所有 SIM 卡中删除现有的无线阻止列表。

`POST /sim_card_groups/{id}/actions/remove_wireless_blocklist`

```java
import com.telnyx.sdk.models.simcardgroups.actions.ActionRemoveWirelessBlocklistParams;
import com.telnyx.sdk.models.simcardgroups.actions.ActionRemoveWirelessBlocklistResponse;

ActionRemoveWirelessBlocklistResponse response = client.simCardGroups().actions().removeWirelessBlocklist("6a09cdc3-8948-47f0-aa62-74ac943d6c58");
```

## 为 SIM 卡组分配私有无线网关

此操作会异步地为 SIM 卡组分配一个私有无线网关。

`POST /sim_card_groups/{id}/actions/set_private_wireless_gateway` — 必需参数：`private_wireless_gateway_id`

```java
import com.telnyx.sdk.models.simcardgroups.actions.ActionSetPrivateWirelessGatewayParams;
import com.telnyx.sdk.models.simcardgroups.actions.ActionSetPrivateWirelessGatewayResponse;

ActionSetPrivateWirelessGatewayParams params = ActionSetPrivateWirelessGatewayParams.builder()
    .id("6a09cdc3-8948-47f0-aa62-74ac943d6c58")
    .privateWirelessGatewayId("6a09cdc3-8948-47f0-aa62-74ac943d6c58")
    .build();
ActionSetPrivateWirelessGatewayResponse response = client.simCardGroups().actions().setPrivateWirelessGateway(params);
```

## 为 SIM 卡组分配无线阻止列表

此操作会异步地为 SIM 卡组中的所有 SIM 卡分配一个无线阻止列表。

`POST /sim_card_groups/{id}/actions/set_wireless_blocklist` — 必需参数：`wireless_blocklist_id`

```java
import com.telnyx.sdk.models.simcardgroups.actions.ActionSetWirelessBlocklistParams;
import com.telnyx.sdk.models.simcardgroups.actions.ActionSetWirelessBlocklistResponse;

ActionSetWirelessBlocklistParams params = ActionSetWirelessBlocklistParams.builder()
    .id("6a09cdc3-8948-47f0-aa62-74ac943d6c58")
    .wirelessBlocklistId("6a09cdc3-8948-47f0-aa62-74ac943d6c58")
    .build();
ActionSetWirelessBlocklistResponse response = client.simCardGroups().actions().setWirelessBlocklist(params);
```

## 列出 SIM 卡组操作

此 API 可用于列出 SIM 卡组的操作列表（分页显示）。

`GET /sim_card_group_actions`

```java
import com.telnyx.sdk.models.simcardgroups.actions.ActionListPage;
import com.telnyx.sdk.models.simcardgroups.actions.ActionListParams;

ActionListPage page = client.simCardGroups().actions().list();
```

## 获取 SIM 卡组操作详情

此 API 可用于获取 SIM 卡组操作的详细信息（用于跟进已进行的异步操作）。

`GET /sim_card_group_actions/{id}`

```java
import com.telnyx.sdk.models.simcardgroups.actions.ActionRetrieveParams;
import com.telnyx.sdk.models.simcardgroups.actions.ActionRetrieveResponse;

ActionRetrieveResponse action = client.simCardGroups().actions().retrieve("6a09cdc3-8948-47f0-aa62-74ac943d6c58");
```

## 获取所有 SIM 卡订单

根据过滤条件获取所有 SIM 卡订单。

`GET /sim_card_orders`

```java
import com.telnyx.sdk.models.simcardorders.SimCardOrderListPage;
import com.telnyx.sdk.models.simcardorders.SimCardOrderListParams;

SimCardOrderListPage page = client.simCardOrders().list();
```

## 创建 SIM 卡订单

创建新的 SIM 卡订单。

`POST /sim_card_orders` — 必需参数：`address_id`, `quantity`

```java
import com.telnyx.sdk.models.simcardorders.SimCardOrderCreateParams;
import com.telnyx.sdk.models.simcardorders.SimCardOrderCreateResponse;

SimCardOrderCreateParams params = SimCardOrderCreateParams.builder()
    .addressId("1293384261075731499")
    .quantity(23L)
    .build();
SimCardOrderCreateResponse simCardOrder = client.simCardOrders().create(params);
```

## 获取单个 SIM 卡订单

根据 ID 获取单个 SIM 卡订单。

`GET /sim_card_orders/{id}`

```java
import com.telnyx.sdk.models.simcardorders.SimCardOrderRetrieveParams;
import com.telnyx.sdk.models.simcardorders.SimCardOrderRetrieveResponse;

SimCardOrderRetrieveResponse simCardOrder = client.simCardOrders().retrieve("6a09cdc3-8948-47f0-aa62-74ac943d6c58");
```

## 预览 SIM 卡订单

预览 SIM 卡订单信息。

`POST /sim_card_order_preview` — 必需参数：`quantity`, `address_id`

```java
import com.telnyx.sdk.models.simcardorderpreview.SimCardOrderPreviewPreviewParams;
import com.telnyx.sdk.models.simcardorderpreview.SimCardOrderPreviewPreviewResponse;

SimCardOrderPreviewPreviewParams params = SimCardOrderPreviewPreviewParams.builder()
    .addressId("1293384261075731499")
    .quantity(21L)
    .build();
SimCardOrderPreviewPreviewResponse response = client.simCardOrderPreview().preview(params);
```

## 列出 SIM 卡数据使用通知

列出 SIM 卡数据使用通知的列表（分页显示）。

`GET /sim_card_data_usage_notifications`

```java
import com.telnyx.sdk.models.simcarddatausagenotifications.SimCardDataUsageNotificationListPage;
import com.telnyx.sdk.models.simcarddatausagenotifications.SimCardDataUsageNotificationListParams;

SimCardDataUsageNotificationListPage page = client.simCardDataUsageNotifications().list();
```

## 创建新的 SIM 卡数据使用通知

创建新的 SIM 卡数据使用通知。

`POST /sim_card_data_usage_notifications` — 必需参数：`sim_card_id`, `threshold`

```java
import com.telnyx.sdk.models.simcarddatausagenotifications.SimCardDataUsageNotificationCreateParams;
import com.telnyx.sdk.models.simcarddatausagenotifications.SimCardDataUsageNotificationCreateResponse;

SimCardDataUsageNotificationCreateParams params = SimCardDataUsageNotificationCreateParams.builder()
    .simCardId("6a09cdc3-8948-47f0-aa62-74ac943d6c58")
    .threshold(SimCardDataUsageNotificationCreateParams.Threshold.builder().build())
    .build();
SimCardDataUsageNotificationCreateResponse simCardDataUsageNotification = client.simCardDataUsageNotifications().create(params);
```

## 获取单个 SIM 卡数据使用通知

获取单个 SIM 卡的数据使用通知。

`GET /sim_card_data_usage_notifications/{id}`

```java
import com.telnyx.sdk.models.simcarddatausagenotifications.SimCardDataUsageNotificationRetrieveParams;
import com.telnyx.sdk.models.simcarddatausagenotifications.SimCardDataUsageNotificationRetrieveResponse;

SimCardDataUsageNotificationRetrieveResponse simCardDataUsageNotification = client.simCardDataUsageNotifications().retrieve("6a09cdc3-8948-47f0-aa62-74ac943d6c58");
```

## 更新 SIM 卡数据使用通知的信息

更新 SIM 卡数据使用通知的信息。

`PATCH /sim_card_data_usage_notifications/{id}`

```java
import com.telnyx.sdk.models.simcarddatausagenotifications.SimCardDataUsageNotification;
import com.telnyx.sdk.models.simcarddatausagenotifications.SimCardDataUsageNotificationUpdateParams;
import com.telnyx.sdk.models.simcarddatausagenotifications.SimCardDataUsageNotificationUpdateResponse;

SimCardDataUsageNotificationUpdateParams params = SimCardDataUsageNotificationUpdateParams.builder()
    .simCardDataUsageNotificationId("6a09cdc3-8948-47f0-aa62-74ac943d6c58")
    .simCardDataUsageNotification(SimCardDataUsageNotification.builder().build())
    .build();
SimCardDataUsageNotificationUpdateResponse simCardDataUsageNotification = client.simCardDataUsageNotifications().update(params);
```

## 删除 SIM 卡数据使用通知

删除 SIM 卡数据使用通知。

`DELETE /sim_card_data_usage_notifications/{id}`

```java
import com.telnyx.sdk.models.simcarddatausagenotifications.SimCardDataUsageNotificationDeleteParams;
import com.telnyx.sdk.models.simcarddatausagenotifications.SimCardDataUsageNotificationDeleteResponse;

SimCardDataUsageNotificationDeleteResponse simCardDataUsageNotification = client.simCardDataUsageNotifications().delete("6a09cdc3-8948-47f0-aa62-74ac943d6c58");
```

## 购买 eSIM

购买并注册指定数量的 eSIM 到当前用户的账户。<br/>
如果提供了 `sim_card_group_id`，这些 eSIM 将与该组关联。

`POST /actions/purchase/esims` — 必需参数：`amount`

```java
import com.telnyx.sdk.models.actions.purchase.PurchaseCreateParams;
import com.telnyx.sdk.models.actions.purchase.PurchaseCreateResponse;

PurchaseCreateParams params = PurchaseCreateParams.builder()
    .amount(10L)
    .build();
PurchaseCreateResponse purchase = client.actions().purchase().create(params);
```

## 注册 SIM 卡

将提供的注册码关联到当前用户的账户中的 SIM 卡。<br/>
如果提供了 `sim_card_group_id`，这些 SIM 卡将与该组关联...

`POST /actions/register/sim_cards` — 必需参数：`registration_codes`

```java
import com.telnyx.sdk.models.actions.register.RegisterCreateParams;
import com.telnyx.sdk.models.actions.register.RegisterCreateResponse;
import java.util.List;

RegisterCreateParams params = RegisterCreateParams.builder()
    .registrationCodes(List.of(
      "0000000001",
      "0000000002",
      "0000000003"
    ))
    .build();
RegisterCreateResponse register = client.actions().register().create(params);
```

## 列出 OTA 更新

`GET /ota_updates`

```java
import com.telnyx.sdk.models.otaupdates.OtaUpdateListPage;
import com.telnyx.sdk.models.otaupdates.OtaUpdateListParams;

OtaUpdateListPage page = client.otaUpdates().list();
```

## 获取 OTA 更新信息

此 API 返回 OTA（Over the Air）更新的详细信息。

`GET /ota_updates/{id}`

```java
import com.telnyx.sdk.models.otaupdates.OtaUpdateRetrieveParams;
import com.telnyx.sdk.models.otaupdates.OtaUpdateRetrieveResponse;

OtaUpdateRetrieveResponse otaUpdate = client.otaUpdates().retrieve("6a09cdc3-8948-47f0-aa62-74ac943d6c58");
```

## 获取所有私有无线网关

获取用户拥有的所有私有无线网关。

`GET /private_wireless_gateways`

```java
import com.telnyx.sdk.models.privatewirelessgateways.PrivateWirelessGatewayListPage;
import com.telnyx.sdk.models.privatewirelessgateways.PrivateWirelessGatewayListParams;

PrivateWirelessGatewayListPage page = client.privateWirelessGateways().list();
```

## 创建私有无线网关

为先前创建的网络异步创建一个私有无线网关。

`POST /private_wireless_gateways` — 必需参数：`network_id`, `name`

```java
import com.telnyx.sdk.models.privatewirelessgateways.PrivateWirelessGatewayCreateParams;
import com.telnyx.sdk.models.privatewirelessgateways.PrivateWirelessGatewayCreateResponse;

PrivateWirelessGatewayCreateParams params = PrivateWirelessGatewayCreateParams.builder()
    .name("My private wireless gateway")
    .networkId("6a09cdc3-8948-47f0-aa62-74ac943d6c58")
    .build();
PrivateWirelessGatewayCreateResponse privateWirelessGateway = client.privateWirelessGateways().create(params);
```

## 获取私有无线网关信息

检索私有无线网关的详细信息。

`GET /private_wireless_gateways/{id}`

```java
import com.telnyx.sdk.models.privatewirelessgateways.PrivateWirelessGatewayRetrieveParams;
import com.telnyx.sdk.models.privatewirelessgateways.PrivateWirelessGatewayRetrieveResponse;

PrivateWirelessGatewayRetrieveResponse privateWirelessGateway = client.privateWirelessGateways().retrieve("6a09cdc3-8948-47f0-aa62-74ac943d6c58");
```

## 删除私有无线网关

删除私有无线网关。

`DELETE /private_wireless_gateways/{id}`

```java
import com.telnyx.sdk.models.privatewirelessgateways.PrivateWirelessGatewayDeleteParams;
import com.telnyx.sdk.models.privatewirelessgateways.PrivateWirelessGatewayDeleteResponse;

PrivateWirelessGatewayDeleteResponse privateWirelessGateway = client.privateWirelessGateways().delete("6a09cdc3-8948-47f0-aa62-74ac943d6c58");
```

## 获取所有无线阻止列表

获取用户拥有的所有无线阻止列表。

`GET /wireless_blocklists`

```java
import com.telnyx.sdk.models.wirelessblocklists.WirelessBlocklistListPage;
import com.telnyx.sdk.models.wirelessblocklists.WirelessBlocklistListParams;

WirelessBlocklistListPage page = client.wirelessBlocklists().list();
```

## 创建无线阻止列表

创建一个无线阻止列表，以防止 SIM 卡连接到某些网络。

`POST /wireless_blocklists` — 必需参数：`name`, `type`, `values`

```java
import com.telnyx.sdk.models.wirelessblocklists.WirelessBlocklistCreateParams;
import com.telnyx.sdk.models.wirelessblocklists.WirelessBlocklistCreateResponse;

WirelessBlocklistCreateParams params = WirelessBlocklistCreateParams.builder()
    .name("My Wireless Blocklist")
    .type(WirelessBlocklistCreateParams.Type.COUNTRY)
    .addValue("CA")
    .addValue("US")
    .build();
WirelessBlocklistCreateResponse wirelessBlocklist = client.wirelessBlocklists().create(params);
```

## 更新无线阻止列表

更新无线阻止列表。

`PATCH /wireless_blocklists`

```java
import com.telnyx.sdk.models.wirelessblocklists.WirelessBlocklistUpdateParams;
import com.telnyx.sdk.models.wirelessblocklists.WirelessBlocklistUpdateResponse;

WirelessBlocklistUpdateResponse wirelessBlocklist = client.wirelessBlocklists().update();
```

## 获取无线阻止列表信息

检索无线阻止列表的详细信息。

`GET /wireless_blocklists/{id}`

```java
import com.telnyx.sdk.models.wirelessblocklists.WirelessBlocklistRetrieveParams;
import com.telnyx.sdk.models.wirelessblocklists.WirelessBlocklistRetrieveResponse;

WirelessBlocklistRetrieveResponse wirelessBlocklist = client.wirelessBlocklists().retrieve("6a09cdc3-8948-47f0-aa62-74ac943d6c58");
```

## 删除无线阻止列表

删除无线阻止列表。

`DELETE /wireless_blocklists/{id}`

```java
import com.telnyx.sdk.models.wirelessblocklists.WirelessBlocklistDeleteParams;
import com.telnyx.sdk.models.wirelessblocklists.WirelessBlocklistDeleteResponse;

WirelessBlocklistDeleteResponse wirelessBlocklist = client.wirelessBlocklists().delete("6a09cdc3-8948-47f0-aa62-74ac943d6c58");
```

## 获取所有可能的无线阻止列表值

检索给定类型的所有无线阻止列表值。

`GET /wireless_blocklist_values`

```java
import com.telnyx.sdk.models.wirelessblocklistvalues.WirelessBlocklistValueListParams;
import com.telnyx.sdk.models.wirelessblocklistvalues.WirelessBlocklistValueListResponse;

WirelessBlocklistValueListParams params = WirelessBlocklistValueListParams.builder()
    .type(WirelessBlocklistValueListParams.Type.COUNTRY)
    .build();
WirelessBlocklistValueListResponse wirelessBlocklistValues = client.wirelessBlocklistValues().list(params);
```
```