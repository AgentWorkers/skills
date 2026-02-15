---
name: telnyx-iot-javascript
description: >-
  Manage IoT SIM cards, eSIMs, data plans, and wireless connectivity. Use when
  building IoT/M2M solutions. This skill provides JavaScript SDK examples.
metadata:
  author: telnyx
  product: iot
  language: javascript
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx Iot - JavaScript

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

## 获取所有无线区域

检索指定产品的所有无线区域。

`GET /wireless/regions`

```javascript
const response = await client.wireless.retrieveRegions({ product: 'public_ips' });

console.log(response.data);
```

## 获取所有 SIM 卡

获取符合给定过滤条件的用户所属的所有 SIM 卡。

`GET /sim_cards`

```javascript
// Automatically fetches more pages as needed.
for await (const simpleSimCard of client.simCards.list()) {
  console.log(simpleSimCard.id);
}
```

## 获取 SIM 卡详情

返回特定 SIM 卡的详细信息。

`GET /sim_cards/{id}`

```javascript
const simCard = await client.simCards.retrieve('6a09cdc3-8948-47f0-aa62-74ac943d6c58');

console.log(simCard.data);
```

## 更新 SIM 卡

更新 SIM 卡数据

`PATCH /sim_cards/{id}`

```javascript
const simCard = await client.simCards.update('6a09cdc3-8948-47f0-aa62-74ac943d6c58');

console.log(simCard.data);
```

## 删除 SIM 卡

SIM 卡将被停用，从您的账户中移除，且您将不再被收费。<br />删除完成后，SIM 卡将无法连接网络。

`DELETE /sim_cards/{id}`

```javascript
const simCard = await client.simCards.delete('6a09cdc3-8948-47f0-aa62-74ac943d6c58');

console.log(simCard.data);
```

## 获取 eSIM 的激活码

返回 eSIM 的激活码。<br/>
此 API 仅适用于 eSIM。

`GET /sim_cards/{id}/activation_code`

```javascript
const response = await client.simCards.getActivationCode('6a09cdc3-8948-47f0-aa62-74ac943d6c58');

console.log(response.data);
```

## 获取 SIM 卡设备详情

返回当前正在使用 SIM 卡的设备详情。

`GET /sim_cards/{id}/device_details`

```javascript
const response = await client.simCards.getDeviceDetails('6a09cdc3-8948-47f0-aa62-74ac943d6c58');

console.log(response.data);
```

## 获取 SIM 卡的公共 IP 地址

返回 SIM 卡的公共 IP 地址。

`GET /sim_cards/{id}/public_ip`

```javascript
const response = await client.simCards.getPublicIP('6a09cdc3-8948-47f0-aa62-74ac943d6c58');

console.log(response.data);
```

## 列出无线连接日志

此 API 可用于列出与 SIM 卡关联的无线连接日志（分页显示），以便进行故障排查。

`GET /sim_cards/{id}/wireless_connectivity_logs`

```javascript
// Automatically fetches more pages as needed.
for await (const simCardListWirelessConnectivityLogsResponse of client.simCards.listWirelessConnectivityLogs(
  '6a09cdc3-8948-47f0-aa62-74ac943d6c58',
)) {
  console.log(simCardListWirelessConnectivityLogsResponse.id);
}
```

## 请求禁用 SIM 卡

此 API 会禁用 SIM 卡，使其无法连接网络并无法使用数据。<br/>
该 API 会触发一个异步操作（称为 SIM 卡操作）。

`POST /sim_cards/{id}/actions/disable`

```javascript
const response = await client.simCards.actions.disable('6a09cdc3-8948-47f0-aa62-74ac943d6c58');

console.log(response.data);
```

## 请求启用 SIM 卡

此 API 会启用 SIM 卡，使其能够连接网络并可以使用数据。<br/>
要启用 SIM 卡，必须先将其关联到一个 SIM 卡组。<br/>
该 API 会触发一个异步操作。

`POST /sim_cards/{id}/actions/enable`

```javascript
const response = await client.simCards.actions.enable('6a09cdc3-8948-47f0-aa62-74ac943d6c58');

console.log(response.data);
```

## 请求删除 SIM 卡的公共 IP 地址

此 API 会删除 SIM 卡的现有公共 IP 地址。

`POST /sim_cards/{id}/actions/remove_public_ip`

```javascript
const response = await client.simCards.actions.removePublicIP(
  '6a09cdc3-8948-47f0-aa62-74ac943d6c58',
);

console.log(response.data);
```

## 请求设置 SIM 卡的公共 IP 地址

此 API 会为 SIM 卡分配一个随机公共 IP 地址，使其可以在公共互联网上使用。

`POST /sim_cards/{id}/actions/set_public_ip`

```javascript
const response = await client.simCards.actions.setPublicIP('6a09cdc3-8948-47f0-aa62-74ac943d6c58');

console.log(response.data);
```

## 请求将 SIM 卡设置为待机状态

设置 SIM 卡为待机状态后，它将能够重新连接网络并可以使用数据。<br/>
要设置 SIM 卡为待机状态，必须先...

`POST /sim_cards/{id}/actions/set_standby`

```javascript
const response = await client.simCards.actions.setStandby('6a09cdc3-8948-47f0-aa62-74ac943d6c58');

console.log(response.data);
```

## 批量设置 SIM 卡的公共 IP 地址

此 API 会为指定的每个 SIM 卡设置公共 IP 地址（异步操作）。

`POST /sim_cards/actions/bulk_set_public_ips` — 必需参数：`sim_card_ids`

```javascript
const response = await client.simCards.actions.bulkSetPublicIPs({
  sim_card_ids: ['6b14e151-8493-4fa1-8664-1cc4e6d14158'],
});

console.log(response.data);
```

## 验证 SIM 卡注册码

验证 SIM 卡注册码是否有效。

`POST /sim_cards/actions/validate_registration_codes`

```javascript
const response = await client.simCards.actions.validateRegistrationCodes();

console.log(response.data);
```

## 列出 SIM 卡操作

此 API 可列出 SIM 卡操作的列表（分页显示）。

`GET /sim_card_actions`

```javascript
// Automatically fetches more pages as needed.
for await (const simCardAction of client.simCards.actions.list()) {
  console.log(simCardAction.id);
}
```

## 获取 SIM 卡操作详情

此 API 可获取特定 SIM 卡操作的详细信息，以便跟进已进行的异步操作。

`GET /sim_card_actions/{id}`

```javascript
const action = await client.simCards.actions.retrieve('6a09cdc3-8948-47f0-aa62-74ac943d6c58');

console.log(action.data);
```

## 列出批量 SIM 卡操作

此 API 可列出批量 SIM 卡操作的列表（分页显示）。

`GET /bulk_sim_card_actions`

```javascript
// Automatically fetches more pages as needed.
for await (const bulkSimCardActionListResponse of client.bulkSimCardActions.list()) {
  console.log(bulkSimCardActionListResponse.id);
}
```

## 获取批量 SIM 卡操作详情

此 API 可获取批量 SIM 卡操作的详细信息。

`GET /bulk_sim_card_actions/{id}`

```javascript
const bulkSimCardAction = await client.bulkSimCardActions.retrieve(
  '6a09cdc3-8948-47f0-aa62-74ac943d6c58',
);

console.log(bulkSimCardAction.data);
```

## 获取所有 SIM 卡组

获取符合给定过滤条件的用户所属的所有 SIM 卡组。

`GET /sim_card_groups`

```javascript
// Automatically fetches more pages as needed.
for await (const simCardGroupListResponse of client.simCardGroups.list()) {
  console.log(simCardGroupListResponse.id);
}
```

## 创建 SIM 卡组

创建一个新的 SIM 卡组。

`POST /sim_card_groups` — 必需参数：`name`

```javascript
const simCardGroup = await client.simCardGroups.create({ name: 'My Test Group' });

console.log(simCardGroup.data);
```

## 获取 SIM 卡组详情

返回特定 SIM 卡组的详细信息。

`GET /sim_card_groups/{id}`

```javascript
const simCardGroup = await client.simCardGroups.retrieve('6a09cdc3-8948-47f0-aa62-74ac943d6c58');

console.log(simCardGroup.data);
```

## 更新 SIM 卡组

更新 SIM 卡组。

`PATCH /sim_card_groups/{id}`

```javascript
const simCardGroup = await client.simCardGroups.update('6a09cdc3-8948-47f0-aa62-74ac943d6c58');

console.log(simCardGroup.data);
```

## 删除 SIM 卡组

永久删除一个 SIM 卡组。

`DELETE /sim_card_groups/{id}`

```javascript
const simCardGroup = await client.simCardGroups.delete('6a09cdc3-8948-47f0-aa62-74ac943d6c58');

console.log(simCardGroup.data);
```

## 从 SIM 卡组中移除私有无线网关

此操作会异步地从 SIM 卡组中移除现有的私有无线网关。

`POST /sim_card_groups/{id}/actions/remove_private_wireless_gateway`

```javascript
const response = await client.simCardGroups.actions.removePrivateWirelessGateway(
  '6a09cdc3-8948-47f0-aa62-74ac943d6c58',
);

console.log(response.data);
```

## 从 SIM 卡组中移除无线阻止列表

此操作会异步地从 SIM 卡组中的所有 SIM 卡中移除现有的无线阻止列表。

`POST /sim_card_groups/{id}/actions/remove_wireless_blocklist`

```javascript
const response = await client.simCardGroups.actions.removeWirelessBlocklist(
  '6a09cdc3-8948-47f0-aa62-74ac943d6c58',
);

console.log(response.data);
```

## 为 SIM 卡组分配私有无线网关

此操作会异步地为 SIM 卡组分配一个私有无线网关。

`POST /sim_card_groups/{id}/actions/set_private_wireless_gateway` — 必需参数：`private_wireless_gateway_id`

```javascript
const response = await client.simCardGroups.actions.setPrivateWirelessGateway(
  '6a09cdc3-8948-47f0-aa62-74ac943d6c58',
  { private_wireless_gateway_id: '6a09cdc3-8948-47f0-aa62-74ac943d6c58' },
);

console.log(response.data);
```

## 为 SIM 卡组分配无线阻止列表

此操作会异步地为 SIM 卡组中的所有 SIM 卡分配一个无线阻止列表。

`POST /sim_card_groups/{id}/actions/set_wireless_blocklist` — 必需参数：`wireless_blocklist_id`

```javascript
const response = await client.simCardGroups.actions.setWirelessBlocklist(
  '6a09cdc3-8948-47f0-aa62-74ac943d6c58',
  { wireless_blocklist_id: '6a09cdc3-8948-47f0-aa62-74ac943d6c58' },
);

console.log(response.data);
```

## 列出 SIM 卡组操作

此 API 可列出 SIM 卡组的操作列表（分页显示）。

`GET /sim_card_group_actions`

```javascript
// Automatically fetches more pages as needed.
for await (const simCardGroupAction of client.simCardGroups.actions.list()) {
  console.log(simCardGroupAction.id);
}
```

## 获取 SIM 卡组操作详情

此 API 可获取 SIM 卡组操作的详细信息，以便跟进已进行的异步操作。

`GET /sim_card_group_actions/{id}`

```javascript
const action = await client.simCardGroups.actions.retrieve('6a09cdc3-8948-47f0-aa62-74ac943d6c58');

console.log(action.data);
```

## 获取所有 SIM 卡订单

根据过滤条件获取所有 SIM 卡订单。

`GET /sim_card_orders`

```javascript
// Automatically fetches more pages as needed.
for await (const simCardOrder of client.simCardOrders.list()) {
  console.log(simCardOrder.id);
}
```

## 创建 SIM 卡订单

创建新的 SIM 卡订单。

`POST /sim_card_orders` — 必需参数：`address_id`, `quantity`

```javascript
const simCardOrder = await client.simCardOrders.create({
  address_id: '1293384261075731499',
  quantity: 23,
});

console.log(simCardOrder.data);
```

## 获取单个 SIM 卡订单

根据 ID 获取单个 SIM 卡订单。

`GET /sim_card_orders/{id}`

```javascript
const simCardOrder = await client.simCardOrders.retrieve('6a09cdc3-8948-47f0-aa62-74ac943d6c58');

console.log(simCardOrder.data);
```

## 预览 SIM 卡订单

预览 SIM 卡订单信息。

`POST /sim_card_order_preview` — 必需参数：`quantity`, `address_id`

```javascript
const response = await client.simCardOrderPreview.preview({
  address_id: '1293384261075731499',
  quantity: 21,
});

console.log(response.data);
```

## 列出 SIM 卡数据使用通知

列出 SIM 卡数据使用通知的列表（分页显示）。

`GET /sim_card_data_usage_notifications`

```javascript
// Automatically fetches more pages as needed.
for await (const simCardDataUsageNotification of client.simCardDataUsageNotifications.list()) {
  console.log(simCardDataUsageNotification.id);
}
```

## 创建新的 SIM 卡数据使用通知

创建新的 SIM 卡数据使用通知。

`POST /sim_card_data_usage_notifications` — 必需参数：`sim_card_id`, `threshold`

```javascript
const simCardDataUsageNotification = await client.simCardDataUsageNotifications.create({
  sim_card_id: '6a09cdc3-8948-47f0-aa62-74ac943d6c58',
  threshold: {},
});

console.log(simCardDataUsageNotification.data);
```

## 获取单个 SIM 卡数据使用通知

获取单个 SIM 卡的数据使用通知。

`GET /sim_card_data_usage_notifications/{id}`

```javascript
const simCardDataUsageNotification = await client.simCardDataUsageNotifications.retrieve(
  '6a09cdc3-8948-47f0-aa62-74ac943d6c58',
);

console.log(simCardDataUsageNotification.data);
```

## 更新 SIM 卡数据使用通知的信息

更新 SIM 卡数据使用通知的信息。

`PATCH /sim_card_data_usage_notifications/{id}`

```javascript
const simCardDataUsageNotification = await client.simCardDataUsageNotifications.update(
  '6a09cdc3-8948-47f0-aa62-74ac943d6c58',
);

console.log(simCardDataUsageNotification.data);
```

## 删除 SIM 卡数据使用通知

删除 SIM 卡数据使用通知。

`DELETE /sim_card_data_usage_notifications/{id}`

```javascript
const simCardDataUsageNotification = await client.simCardDataUsageNotifications.delete(
  '6a09cdc3-8948-47f0-aa62-74ac943d6c58',
);

console.log(simCardDataUsageNotification.data);
```

## 购买 eSIM

购买并注册指定数量的 eSIM 到当前用户的账户。<br/>
如果提供了 `sim_card_group_id`，这些 eSIM 将与该组关联。

`POST /actions/purchase/esims` — 必需参数：`amount`

```javascript
const purchase = await client.actions.purchase.create({ amount: 10 });

console.log(purchase.data);
```

## 注册 SIM 卡

将提供的注册码关联到的 SIM 卡注册到当前用户的账户。<br/>
如果提供了 `sim_card_group_id`，这些 SIM 卡将与该组关联...

`POST /actions/register/sim_cards` — 必需参数：`registration_codes`

```javascript
const register = await client.actions.register.create({
  registration_codes: ['0000000001', '0000000002', '0000000003'],
});

console.log(register.data);
```

## 列出 OTA 更新

`GET /ota_updates`

```javascript
// Automatically fetches more pages as needed.
for await (const otaUpdateListResponse of client.otaUpdates.list()) {
  console.log(otaUpdateListResponse.id);
}
```

## 获取 OTA 更新

此 API 返回 OTA（Over the Air）更新的详细信息。

`GET /ota_updates/{id}`

```javascript
const otaUpdate = await client.otaUpdates.retrieve('6a09cdc3-8948-47f0-aa62-74ac943d6c58');

console.log(otaUpdate.data);
```

## 获取所有私有无线网关

获取用户所属的所有私有无线网关。

`GET /private_wireless_gateways`

```javascript
// Automatically fetches more pages as needed.
for await (const privateWirelessGateway of client.privateWirelessGateways.list()) {
  console.log(privateWirelessGateway.id);
}
```

## 创建私有无线网关

为先前创建的网络异步创建一个私有无线网关。

`POST /private_wireless_gateways` — 必需参数：`network_id`, `name`

```javascript
const privateWirelessGateway = await client.privateWirelessGateways.create({
  name: 'My private wireless gateway',
  network_id: '6a09cdc3-8948-47f0-aa62-74ac943d6c58',
});

console.log(privateWirelessGateway.data);
```

## 获取私有无线网关详情

检索私有无线网关的详细信息。

`GET /private_wireless_gateways/{id}`

```javascript
const privateWirelessGateway = await client.privateWirelessGateways.retrieve(
  '6a09cdc3-8948-47f0-aa62-74ac943d6c58',
);

console.log(privateWirelessGateway.data);
```

## 删除私有无线网关

删除私有无线网关。

`DELETE /private_wireless_gateways/{id}`

```javascript
const privateWirelessGateway = await client.privateWirelessGateways.delete(
  '6a09cdc3-8948-47f0-aa62-74ac943d6c58',
);

console.log(privateWirelessGateway.data);
```

## 获取所有无线阻止列表

获取用户所属的所有无线阻止列表。

`GET /wireless_blocklists`

```javascript
// Automatically fetches more pages as needed.
for await (const wirelessBlocklist of client.wirelessBlocklists.list()) {
  console.log(wirelessBlocklist.id);
}
```

## 创建无线阻止列表

创建一个无线阻止列表，以防止 SIM 卡连接到某些网络。

`POST /wireless_blocklists` — 必需参数：`name`, `type`, `values`

```javascript
const wirelessBlocklist = await client.wirelessBlocklists.create({
  name: 'My Wireless Blocklist',
  type: 'country',
  values: ['CA', 'US'],
});

console.log(wirelessBlocklist.data);
```

## 更新无线阻止列表

更新无线阻止列表。

`PATCH /wireless_blocklists`

```javascript
const wirelessBlocklist = await client.wirelessBlocklists.update();

console.log(wirelessBlocklist.data);
```

## 获取无线阻止列表详情

检索无线阻止列表的详细信息。

`GET /wireless_blocklists/{id}`

```javascript
const wirelessBlocklist = await client.wirelessBlocklists.retrieve(
  '6a09cdc3-8948-47f0-aa62-74ac943d6c58',
);

console.log(wirelessBlocklist.data);
```

## 删除无线阻止列表

删除无线阻止列表。

`DELETE /wireless_blocklists/{id}`

```javascript
const wirelessBlocklist = await client.wirelessBlocklists.delete(
  '6a09cdc3-8948-47f0-aa62-74ac943d6c58',
);

console.log(wirelessBlocklist.data);
```

## 获取所有可能的无线阻止列表值

检索给定类型的无线阻止列表的所有值。

`GET /wireless_blocklist_values`

```javascript
const wirelessBlocklistValues = await client.wirelessBlocklistValues.list({ type: 'country' });

console.log(wirelessBlocklistValues.data);
```