---
name: telnyx-iot-ruby
description: >-
  Manage IoT SIM cards, eSIMs, data plans, and wireless connectivity. Use when
  building IoT/M2M solutions. This skill provides Ruby SDK examples.
metadata:
  author: telnyx
  product: iot
  language: ruby
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx Iot - Ruby

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

以下所有示例均假设 `client` 已按上述方式初始化。

## 获取所有无线区域

检索指定产品的所有无线区域。

`GET /wireless/regions`

```ruby
response = client.wireless.retrieve_regions(product: "public_ips")

puts(response)
```

## 获取所有 SIM 卡

获取符合给定过滤条件的用户拥有的所有 SIM 卡。

`GET /sim_cards`

```ruby
page = client.sim_cards.list

puts(page)
```

## 获取 SIM 卡信息

返回特定 SIM 卡的详细信息。

`GET /sim_cards/{id}`

```ruby
sim_card = client.sim_cards.retrieve("6a09cdc3-8948-47f0-aa62-74ac943d6c58")

puts(sim_card)
```

## 更新 SIM 卡信息

更新 SIM 卡数据

`PATCH /sim_cards/{id}`

```ruby
sim_card = client.sim_cards.update("6a09cdc3-8948-47f0-aa62-74ac943d6c58")

puts(sim_card)
```

## 删除 SIM 卡

SIM 卡将被停用，从您的账户中移除，您将不再被收取费用。<br />删除完成后，SIM 卡将无法连接到网络。

`DELETE /sim_cards/{id}`

```ruby
sim_card = client.sim_cards.delete("6a09cdc3-8948-47f0-aa62-74ac943d6c58")

puts(sim_card)
```

## 获取 eSIM 的激活码

返回 eSIM 的激活码。<br/><br/>
此 API 仅适用于 eSIM。

`GET /sim_cards/{id}/activation_code`

```ruby
response = client.sim_cards.get_activation_code("6a09cdc3-8948-47f0-aa62-74ac943d6c58")

puts(response)
```

## 获取 SIM 卡设备详情

返回当前正在使用该 SIM 卡的设备详情。

`GET /sim_cards/{id}/device_details`

```ruby
response = client.sim_cards.get_device_details("6a09cdc3-8948-47f0-aa62-74ac943d6c58")

puts(response)
```

## 获取 SIM 卡的公共 IP 地址

返回 SIM 卡的公共 IP 地址。

`GET /sim_cards/{id}/public_ip`

```ruby
response = client.sim_cards.get_public_ip("6a09cdc3-8948-47f0-aa62-74ac943d6c58")

puts(response)
```

## 列出无线连接日志

此 API 允许分页列出与 SIM 卡关联的无线连接日志，用于故障排查。

`GET /sim_cards/{id}/wireless_connectivity_logs`

```ruby
page = client.sim_cards.list_wireless_connectivity_logs("6a09cdc3-8948-47f0-aa62-74ac943d6c58")

puts(page)
```

## 请求禁用 SIM 卡

此 API 会禁用 SIM 卡，使其无法连接到网络并无法使用数据。<br/>
该 API 将触发一个异步操作（称为 SIM 卡操作）。

`POST /sim_cards/{id}/actions/disable`

```ruby
response = client.sim_cards.actions.disable("6a09cdc3-8948-47f0-aa62-74ac943d6c58")

puts(response)
```

## 请求启用 SIM 卡

此 API 会启用 SIM 卡，使其能够连接到网络并可以使用数据。<br/>
要启用 SIM 卡，必须先将其关联到一个 SIM 卡组。<br/>
该 API 将触发一个异步操作...

`POST /sim_cards/{id}/actions/enable`

```ruby
response = client.sim_cards.actions.enable("6a09cdc3-8948-47f0-aa62-74ac943d6c58")

puts(response)
```

## 请求删除 SIM 卡的公共 IP 地址

此 API 会删除 SIM 卡的现有公共 IP 地址。

`POST /sim_cards/{id}/actions/remove_public_ip`

```ruby
response = client.sim_cards.actions.remove_public_ip("6a09cdc3-8948-47f0-aa62-74ac943d6c58")

puts(response)
```

## 请求设置 SIM 卡的公共 IP 地址

此 API 会为 SIM 卡分配一个随机公共 IP 地址，使其可以在公共互联网上使用。

`POST /sim_cards/{id}/actions/set_public_ip`

```ruby
response = client.sim_cards.actions.set_public_ip("6a09cdc3-8948-47f0-aa62-74ac943d6c58")

puts(response)
```

## 请求将 SIM 卡设置为待机状态

设置 SIM 卡为待机状态后，它将能够重新连接到网络并可以使用数据。<br/>
要设置 SIM 卡为待机状态，必须先...

`POST /sim_cards/{id}/actions/set_standby`

```ruby
response = client.sim_cards.actions.set_standby("6a09cdc3-8948-47f0-aa62-74ac943d6c58")

puts(response)
```

## 请求批量设置 SIM 卡的公共 IP 地址

此 API 会为每个指定的 SIM 卡异步设置公共 IP 地址。<br/>
对于每个 SIM 卡，都将触发一个 SIM 卡操作。

`POST /sim_cards/actions/bulk_set_public_ips` — 必需参数：`sim_card_ids`

```ruby
response = client.sim_cards.actions.bulk_set_public_ips(sim_card_ids: ["6b14e151-8493-4fa1-8664-1cc4e6d14158"])

puts(response)
```

## 验证 SIM 卡注册码

验证 SIM 卡注册码是否有效。

`POST /sim_cards/actions/validate_registration_codes`

```ruby
response = client.sim_cards.actions.validate_registration_codes

puts(response)
```

## 列出 SIM 卡操作

此 API 允许分页列出所有 SIM 卡操作。

`GET /sim_card_actions`

```ruby
page = client.sim_cards.actions.list

puts(page)
```

## 获取 SIM 卡操作详情

此 API 可以获取有关特定 SIM 卡操作的详细信息，以便跟进已进行的异步操作。

`GET /sim_card_actions/{id}`

```ruby
action = client.sim_cards.actions.retrieve("6a09cdc3-8948-47f0-aa62-74ac943d6c58")

puts(action)
```

## 列出批量 SIM 卡操作

此 API 允许分页列出所有批量 SIM 卡操作。

`GET /bulk_sim_card_actions`

```ruby
page = client.bulk_sim_card_actions.list

puts(page)
```

## 获取批量 SIM 卡操作详情

此 API 可以获取批量 SIM 卡操作的详细信息。

`GET /bulk_sim_card_actions/{id}`

```ruby
bulk_sim_card_action = client.bulk_sim_card_actions.retrieve("6a09cdc3-8948-47f0-aa62-74ac943d6c58")

puts(bulk_sim_card_action)
```

## 获取所有 SIM 卡组

获取符合给定过滤条件的用户拥有的所有 SIM 卡组。

`GET /sim_card_groups`

```ruby
page = client.sim_card_groups.list

puts(page)
```

## 创建 SIM 卡组

创建一个新的 SIM 卡组对象。

`POST /sim_card_groups` — 必需参数：`name`

```ruby
sim_card_group = client.sim_card_groups.create(name: "My Test Group")

puts(sim_card_group)
```

## 获取 SIM 卡组信息

返回特定 SIM 卡组的详细信息。

`GET /sim_card_groups/{id}`

```ruby
sim_card_group = client.sim_card_groups.retrieve("6a09cdc3-8948-47f0-aa62-74ac943d6c58")

puts(sim_card_group)
```

## 更新 SIM 卡组

更新 SIM 卡组。

`PATCH /sim_card_groups/{id}`

```ruby
sim_card_group = client.sim_card_groups.update("6a09cdc3-8948-47f0-aa62-74ac943d6c58")

puts(sim_card_group)
```

## 删除 SIM 卡组

永久删除一个 SIM 卡组。

`DELETE /sim_card_groups/{id}`

```ruby
sim_card_group = client.sim_card_groups.delete("6a09cdc3-8948-47f0-aa62-74ac943d6c58")

puts(sim_card_group)
```

## 从 SIM 卡组中删除私有无线网关

此操作将异步删除 SIM 卡组中现有的私有无线网关。

`POST /sim_card_groups/{id}/actions/remove_private_wireless_gateway`

```ruby
response = client.sim_card_groups.actions.remove_private_wireless_gateway("6a09cdc3-8948-47f0-aa62-74ac943d6c58")

puts(response)
```

## 从 SIM 卡组中删除无线阻止列表

此操作将异步删除 SIM 卡组中所有 SIM 卡的现有无线阻止列表。

`POST /sim_card_groups/{id}/actions/remove_wireless_blocklist`

```ruby
response = client.sim_card_groups.actions.remove_wireless_blocklist("6a09cdc3-8948-47f0-aa62-74ac943d6c58")

puts(response)
```

## 为 SIM 卡组分配私有无线网关

此操作将异步为 SIM 卡组分配一个私有无线网关。

`POST /sim_card_groups/{id}/actions/set_private_wireless_gateway` — 必需参数：`private_wireless_gateway_id`

```ruby
response = client.sim_card_groups.actions.set_private_wireless_gateway(
  "6a09cdc3-8948-47f0-aa62-74ac943d6c58",
  private_wireless_gateway_id: "6a09cdc3-8948-47f0-aa62-74ac943d6c58"
)

puts(response)
```

## 为 SIM 卡组分配无线阻止列表

此操作将异步为 SIM 卡组中的所有 SIM 卡分配一个无线阻止列表。

`POST /sim_card_groups/{id}/actions/set_wireless_blocklist` — 必需参数：`wireless_blocklist_id`

```ruby
response = client.sim_card_groups.actions.set_wireless_blocklist(
  "6a09cdc3-8948-47f0-aa62-74ac943d6c58",
  wireless_blocklist_id: "6a09cdc3-8948-47f0-aa62-74ac943d6c58"
)

puts(response)
```

## 列出 SIM 卡组操作

此 API 允许分页列出所有 SIM 卡组操作。

`GET /sim_card_group_actions`

```ruby
page = client.sim_card_groups.actions.list

puts(page)
```

## 获取 SIM 卡组操作详情

此 API 可以获取有关 SIM 卡组操作的详细信息，以便跟进已进行的异步操作。

`GET /sim_card_group_actions/{id}`

```ruby
action = client.sim_card_groups.actions.retrieve("6a09cdc3-8948-47f0-aa62-74ac943d6c58")

puts(action)
```

## 获取所有 SIM 卡订单

根据过滤条件获取所有 SIM 卡订单。

`GET /sim_card_orders`

```ruby
page = client.sim_card_orders.list

puts(page)
```

## 创建 SIM 卡订单

创建新的 SIM 卡订单。

`POST /sim_card_orders` — 必需参数：`address_id`, `quantity`

```ruby
sim_card_order = client.sim_card_orders.create(address_id: "1293384261075731499", quantity: 23)

puts(sim_card_order)
```

## 获取单个 SIM 卡订单

根据 ID 获取单个 SIM 卡订单。

`GET /sim_card_orders/{id}`

```ruby
sim_card_order = client.sim_card_orders.retrieve("6a09cdc3-8948-47f0-aa62-74ac943d6c58")

puts(sim_card_order)
```

## 预览 SIM 卡订单

预览 SIM 卡订单信息。

`POST /sim_card_order_preview` — 必需参数：`quantity`, `address_id`

```ruby
response = client.sim_card_order_preview.preview(address_id: "1293384261075731499", quantity: 21)

puts(response)
```

## 列出 SIM 卡数据使用通知

分页列出所有 SIM 卡数据使用通知。

`GET /sim_card_data_usage_notifications`

```ruby
page = client.sim_card_data_usage_notifications.list

puts(page)
```

## 创建新的 SIM 卡数据使用通知

创建新的 SIM 卡数据使用通知。

`POST /sim_card_data_usage_notifications` — 必需参数：`sim_card_id`, `threshold`

```ruby
sim_card_data_usage_notification = client.sim_card_data_usage_notifications.create(
  sim_card_id: "6a09cdc3-8948-47f0-aa62-74ac943d6c58",
  threshold: {}
)

puts(sim_card_data_usage_notification)
```

## 获取单个 SIM 卡数据使用通知

获取单个 SIM 卡的数据使用通知。

`GET /sim_card_data_usage_notifications/{id}`

```ruby
sim_card_data_usage_notification = client.sim_card_data_usage_notifications.retrieve("6a09cdc3-8948-47f0-aa62-74ac943d6c58")

puts(sim_card_data_usage_notification)
```

## 更新 SIM 卡数据使用通知信息

更新 SIM 卡数据使用通知的信息。

`PATCH /sim_card_data_usage_notifications/{id}`

```ruby
sim_card_data_usage_notification = client.sim_card_data_usage_notifications.update("6a09cdc3-8948-47f0-aa62-74ac943d6c58")

puts(sim_card_data_usage_notification)
```

## 删除 SIM 卡数据使用通知

删除 SIM 卡数据使用通知。

`DELETE /sim_card_data_usage_notifications/{id}`

```ruby
sim_card_data_usage_notification = client.sim_card_data_usage_notifications.delete("6a09cdc3-8948-47f0-aa62-74ac943d6c58")

puts(sim_card_data_usage_notification)
```

## 购买 eSIM

购买并将指定数量的 eSIM 注册到当前用户的账户。<br/><br/>
如果提供了 `sim_card_group_id`，这些 eSIM 将与该组关联。

`POST /actions/purchase/esims` — 必需参数：`amount`

```ruby
purchase = client.actions.purchase.create(amount: 10)

puts(purchase)
```

## 注册 SIM 卡

将提供的注册码关联到的 SIM 卡注册到当前用户的账户。<br/><br/>
如果提供了 `sim_card_group_id`，这些 SIM 卡将与该组关联...

`POST /actions/register/sim_cards` — 必需参数：`registration_codes`

```ruby
register = client.actions.register.create(registration_codes: ["0000000001", "0000000002", "0000000003"])

puts(register)
```

## 列出 OTA 更新

`GET /ota_updates`

```ruby
page = client.ota_updates.list

puts(page)
```

## 获取 OTA 更新

此 API 返回 OTA（Over the Air）更新的详细信息。

`GET /ota_updates/{id}`

```ruby
ota_update = client.ota_updates.retrieve("6a09cdc3-8948-47f0-aa62-74ac943d6c58")

puts(ota_update)
```

## 获取所有私有无线网关

获取用户拥有的所有私有无线网关。

`GET /private_wireless_gateways`

```ruby
page = client.private_wireless_gateways.list

puts(page)
```

## 创建私有无线网关

为之前创建的网络异步创建一个私有无线网关。

`POST /private_wireless_gateways` — 必需参数：`network_id`, `name`

```ruby
private_wireless_gateway = client.private_wireless_gateways.create(
  name: "My private wireless gateway",
  network_id: "6a09cdc3-8948-47f0-aa62-74ac943d6c58"
)

puts(private_wireless_gateway)
```

## 获取私有无线网关信息

检索私有无线网关的详细信息。

`GET /private_wireless_gateways/{id}`

```ruby
private_wireless_gateway = client.private_wireless_gateways.retrieve("6a09cdc3-8948-47f0-aa62-74ac943d6c58")

puts(private_wireless_gateway)
```

## 删除私有无线网关

删除私有无线网关。

`DELETE /private_wireless_gateways/{id}`

```ruby
private_wireless_gateway = client.private_wireless_gateways.delete("6a09cdc3-8948-47f0-aa62-74ac943d6c58")

puts(private_wireless_gateway)
```

## 获取所有无线阻止列表

获取用户拥有的所有无线阻止列表。

`GET /wireless_blocklists`

```ruby
page = client.wireless_blocklists.list

puts(page)
```

## 创建无线阻止列表

创建一个无线阻止列表，以防止 SIM 卡连接到某些网络。

`POST /wireless_blocklists` — 必需参数：`name`, `type`, `values`

```ruby
wireless_blocklist = client.wireless_blocklists.create(name: "My Wireless Blocklist", type: :country, values: ["CA", "US"])

puts(wireless_blocklist)
```

## 更新无线阻止列表

更新无线阻止列表。

`PATCH /wireless_blocklists`

```ruby
wireless_blocklist = client.wireless_blocklists.update

puts(wireless_blocklist)
```

## 获取无线阻止列表信息

检索无线阻止列表的详细信息。

`GET /wireless_blocklists/{id}`

```ruby
wireless_blocklist = client.wireless_blocklists.retrieve("6a09cdc3-8948-47f0-aa62-74ac943d6c58")

puts(wireless_blocklist)
```

## 删除无线阻止列表

删除无线阻止列表。

`DELETE /wireless_blocklists/{id}`

```ruby
wireless_blocklist = client.wireless_blocklists.delete("6a09cdc3-8948-47f0-aa62-74ac943d6c58")

puts(wireless_blocklist)
```

## 获取所有可能的无线阻止列表值

检索给定类型的所有无线阻止列表值。

`GET /wireless_blocklist_values`

```ruby
wireless_blocklist_values = client.wireless_blocklist_values.list(type: :country)

puts(wireless_blocklist_values)
```