---
name: telnyx-networking-ruby
description: >-
  Configure private networks, WireGuard VPN gateways, internet gateways, and
  virtual cross connects. This skill provides Ruby SDK examples.
metadata:
  author: telnyx
  product: networking
  language: ruby
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿修改。 -->

# Telnyx 网络服务 - Ruby

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

以下所有示例均假设 `client` 已经按照上述方式初始化。

## 列出所有区域

列出所有区域及其支持的接口

`GET /regions`

```ruby
regions = client.regions.list

puts(regions)
```

## 列出所有网络

列出所有网络。

`GET /networks`

```ruby
page = client.networks.list

puts(page)
```

## 创建网络

创建一个新的网络。

`POST /networks`

```ruby
network = client.networks.create(name: "test network")

puts(network)
```

## 获取网络信息

获取网络信息。

`GET /networks/{id}`

```ruby
network = client.networks.retrieve("6a09cdc3-8948-47f0-aa62-74ac943d6c58")

puts(network)
```

## 更新网络

更新网络信息。

`PATCH /networks/{id}`

```ruby
network = client.networks.update("6a09cdc3-8948-47f0-aa62-74ac943d6c58", name: "test network")

puts(network)
```

## 删除网络

删除网络。

`DELETE /networks/{id}`

```ruby
network = client.networks.delete("6a09cdc3-8948-47f0-aa62-74ac943d6c58")

puts(network)
```

## 获取默认网关状态

`GET /networks/{id}/default_gateway`

```ruby
default_gateway = client.networks.default_gateway.retrieve("6a09cdc3-8948-47f0-aa62-74ac943d6c58")

puts(default_gateway)
```

## 创建默认网关

`POST /networks/{id}/default_gateway`

```ruby
default_gateway = client.networks.default_gateway.create("6a09cdc3-8948-47f0-aa62-74ac943d6c58")

puts(default_gateway)
```

## 删除默认网关

`DELETE /networks/{id}/default_gateway`

```ruby
default_gateway = client.networks.default_gateway.delete("6a09cdc3-8948-47f0-aa62-74ac943d6c58")

puts(default_gateway)
```

## 列出网络的所有接口

`GET /networks/{id}/networkInterfaces`

```ruby
page = client.networks.list_interfaces("6a09cdc3-8948-47f0-aa62-74ac943d6c58")

puts(page)
```

## 列出所有 WireGuard 接口

列出所有 WireGuard 接口。

`GET /wireguardInterfaces`

```ruby
page = client.wireguard_interfaces.list

puts(page)
```

## 创建 WireGuard 接口

创建一个新的 WireGuard 接口。

`POST /wireguardInterfaces`

```ruby
wireguard_interface = client.wireguard_interfaces.create(region_code: "ashburn-va")

puts(wireguard_interface)
```

## 获取 WireGuard 接口信息

获取 WireGuard 接口信息。

`GET /wireguardInterfaces/{id}`

```ruby
wireguard_interface = client.wireguard_interfaces.retrieve("6a09cdc3-8948-47f0-aa62-74ac943d6c58")

puts(wireguard_interface)
```

## 删除 WireGuard 接口

删除 WireGuard 接口。

`DELETE /wireguardInterfaces/{id}`

```ruby
wireguard_interface = client.wireguard_interfaces.delete("6a09cdc3-8948-47f0-aa62-74ac943d6c58")

puts(wireguard_interface)
```

## 列出所有 WireGuard 对等体

列出所有 WireGuard 对等体。

`GET /wireguard_peers`

```ruby
page = client.wireguard_peers.list

puts(page)
```

## 创建 WireGuard 对等体

创建一个新的 WireGuard 对等体。

`POST /wireguard_peers`

```ruby
wireguard_peer = client.wireguard_peers.create(wireguard_interface_id: "6a09cdc3-8948-47f0-aa62-74ac943d6c58")

puts(wireguard_peer)
```

## 获取 WireGuard 对等体信息

获取 WireGuard 对等体信息。

`GET /wireguard_peers/{id}`

```ruby
wireguard_peer = client.wireguard_peers.retrieve("6a09cdc3-8948-47f0-aa62-74ac943d6c58")

puts(wireguard_peer)
```

## 更新 WireGuard 对等体信息

更新 WireGuard 对等体信息。

`PATCH /wireguard_peers/{id}`

```ruby
wireguard_peer = client.wireguard_peers.update("6a09cdc3-8948-47f0-aa62-74ac943d6c58")

puts(wireguard_peer)
```

## 删除 WireGuard 对等体

删除 WireGuard 对等体。

`DELETE /wireguard_peers/{id}`

```ruby
wireguard_peer = client.wireguard_peers.delete("6a09cdc3-8948-47f0-aa62-74ac943d6c58")

puts(wireguard_peer)
```

## 获取 WireGuard 对等体的配置模板

`GET /wireguard_peers/{id}/config`

```ruby
response = client.wireguard_peers.retrieve_config("6a09cdc3-8948-47f0-aa62-74ac943d6c58")

puts(response)
```

## 获取用户所有的私有无线网关

获取用户所有的私有无线网关。

`GET /private_wireless_gateways`

```ruby
page = client.private_wireless_gateways.list

puts(page)
```

## 创建私有无线网关

为已创建的网络的 SIM 卡异步创建私有无线网关。

`POST /private_wireless_gateways` — 必需参数：`network_id`、`name`

```ruby
private_wireless_gateway = client.private_wireless_gateways.create(
  name: "My private wireless gateway",
  network_id: "6a09cdc3-8948-47f0-aa62-74ac943d6c58"
)

puts(private_wireless_gateway)
```

## 获取私有无线网关信息

获取私有无线网关的信息。

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

## 列出所有公共互联网网关

列出所有公共互联网网关。

`GET /public_internet_gateways`

```ruby
page = client.public_internet_gateways.list

puts(page)
```

## 创建公共互联网网关

创建一个新的公共互联网网关。

`POST /public_internet_gateways`

```ruby
public_internet_gateway = client.public_internet_gateways.create

puts(public_internet_gateway)
```

## 获取公共互联网网关信息

获取公共互联网网关的信息。

`GET /public_internet_gateways/{id}`

```ruby
public_internet_gateway = client.public_internet_gateways.retrieve("6a09cdc3-8948-47f0-aa62-74ac943d6c58")

puts(public_internet_gateway)
```

## 删除公共互联网网关

删除公共互联网网关。

`DELETE /public_internet_gateways/{id}`

```ruby
public_internet_gateway = client.public_internet_gateways.delete("6a09cdc3-8948-47f0-aa62-74ac943d6c58")

puts(public_internet_gateway)
```

## 列出所有虚拟交叉连接

列出所有虚拟交叉连接。

`GET /virtual_cross_connects`

```ruby
page = client.virtual_cross_connects.list

puts(page)
```

## 创建虚拟交叉连接

创建一个新的虚拟交叉连接。<br /><br />对于 AWS 和 GCE，您可以先创建主连接，再创建次级连接。

`POST /virtual_cross_connects`

```ruby
virtual_cross_connect = client.virtual_cross_connects.create(region_code: "ashburn-va")

puts(virtual_cross_connect)
```

## 获取虚拟交叉连接信息

获取虚拟交叉连接的信息。

`GET /virtual_cross_connects/{id}`

```ruby
virtual_cross_connect = client.virtual_cross_connects.retrieve("6a09cdc3-8948-47f0-aa62-74ac943d6c58")

puts(virtual_cross_connect)
```

## 更新虚拟交叉连接

更新虚拟交叉连接。<br /><br />只有在“创建”状态下才能修改云 IP 地址；因为 GCE 会在连接请求完成之后才会通知您生成的 IP 地址...

`PATCH /virtual_cross_connects/{id}`

```ruby
virtual_cross_connect = client.virtual_cross_connects.update("6a09cdc3-8948-47f0-aa62-74ac943d6c58")

puts(virtual_cross_connect)
```

## 删除虚拟交叉连接

删除虚拟交叉连接。

`DELETE /virtual_cross_connects/{id}`

```ruby
virtual_cross_connect = client.virtual_cross_connects.delete("6a09cdc3-8948-47f0-aa62-74ac943d6c58")

puts(virtual_cross_connect)
```

## 查看虚拟交叉连接的覆盖范围

查看虚拟交叉连接的覆盖范围。<br /><br />此端点会显示虚拟交叉连接将被配置到的云区域。

`GET /virtual_cross_connects/coverage`

```ruby
page = client.virtual_cross_connects_coverage.list

puts(page)
```

## 列出所有全局 IP 地址

列出所有全局 IP 地址。

`GET /global_ips`

```ruby
page = client.global_ips.list

puts(page)
```

## 创建全局 IP 地址

创建一个新的全局 IP 地址。

`POST /global_ips`

```ruby
global_ip = client.global_ips.create

puts(global_ip)
```

## 获取全局 IP 地址信息

获取全局 IP 地址的信息。

`GET /global_ips/{id}`

```ruby
global_ip = client.global_ips.retrieve("6a09cdc3-8948-47f0-aa62-74ac943d6c58")

puts(global_ip)
```

## 删除全局 IP 地址

删除全局 IP 地址。

`DELETE /global_ips/{id}`

```ruby
global_ip = client.global_ips.delete("6a09cdc3-8948-47f0-aa62-74ac943d6c58")

puts(global_ip)
```

## 列出所有允许使用的全局 IP 地址端口

列出所有允许使用的全局 IP 地址端口。

`GET /global_ip_allowed_ports`

```ruby
global_ip_allowed_ports = client.global_ip_allowed_ports.list

puts(global_ip_allowed_ports)
```

## 全局 IP 地址分配的健康检查指标

获取全局 IP 地址分配的健康检查指标。

`GET /global_ip_assignment_health`

```ruby
global_ip_assignment_health = client.global_ip_assignment_health.retrieve

puts(global_ip_assignment_health)
```

## 列出所有全局 IP 地址分配记录

列出所有全局 IP 地址的分配记录。

`GET /global_ip_assignments`

```ruby
page = client.global_ip_assignments.list

puts(page)
```

## 创建全局 IP 地址分配记录

创建一个新的全局 IP 地址分配记录。

`POST /global_ip_assignments`

```ruby
global_ip_assignment = client.global_ip_assignments.create

puts(global_ip_assignment)
```

## 获取全局 IP 地址分配记录

获取全局 IP 地址的分配记录。

`GET /global_ip_assignments/{id}`

```ruby
global_ip_assignment = client.global_ip_assignments.retrieve("6a09cdc3-8948-47f0-aa62-74ac943d6c58")

puts(global_ip_assignment)
```

## 更新全局 IP 地址分配记录

更新全局 IP 地址的分配记录。

`PATCH /global_ip_assignments/{id}`

```ruby
global_ip_assignment = client.global_ip_assignments.update(
  "6a09cdc3-8948-47f0-aa62-74ac943d6c58",
  global_ip_assignment_update_request: {}
)

puts(global_ip_assignment)
```

## 删除全局 IP 地址分配记录

删除全局 IP 地址的分配记录。

`DELETE /global_ip_assignments/{id}`

```ruby
global_ip_assignment = client.global_ip_assignments.delete("6a09cdc3-8948-47f0-aa62-74ac943d6c58")

puts(global_ip_assignment)
```

## 全局 IP 地址分配的使用情况指标

获取全局 IP 地址分配的使用情况指标。

`GET /global_ip_assignments/usage`

```ruby
global_ip_assignments_usage = client.global_ip_assignments_usage.retrieve

puts(global_ip_assignments_usage)
```

## 列出所有全局 IP 地址的健康检查类型

列出所有全局 IP 地址的健康检查类型。

`GET /global_ip_health_check_types`

```ruby
global_ip_health_check_types = client.global_ip_health_check_types.list

puts(global_ip_health_check_types)
```

## 列出所有全局 IP 地址的健康检查记录

列出所有全局 IP 地址的健康检查记录。

`GET /global_ip_health_checks`

```ruby
page = client.global_ip_health_checks.list

puts(page)
```

## 创建全局 IP 地址的健康检查

创建一个新的全局 IP 地址健康检查。

`POST /global_ip_health_checks`

```ruby
global_ip_health_check = client.global_ip_health_checks.create

puts(global_ip_health_check)
```

## 获取全局 IP 地址的健康检查记录

获取全局 IP 地址的健康检查记录。

`GET /global_ip_health_checks/{id}`

```ruby
global_ip_health_check = client.global_ip_health_checks.retrieve("6a09cdc3-8948-47f0-aa62-74ac943d6c58")

puts(global_ip_health_check)
```

## 删除全局 IP 地址的健康检查记录

删除全局 IP 地址的健康检查记录。

`DELETE /global_ip_health_checks/{id}`

```ruby
global_ip_health_check = client.global_ip_health_checks.delete("6a09cdc3-8948-47f0-aa62-74ac943d6c58")

puts(global_ip_health_check)
```

## 全局 IP 地址的延迟指标

获取全局 IP 地址的延迟指标。

`GET /global_ip_latency`

```ruby
global_ip_latency = client.global_ip_latency.retrieve

puts(global_ip_latency)
```

## 列出所有全局 IP 协议

列出所有全局 IP 协议。

`GET /global_ip_protocols`

```ruby
global_ip_protocols = client.global_ip_protocols.list

puts(global_ip_protocols)
```

## 全局 IP 地址的使用情况指标

获取全局 IP 地址的使用情况指标。

`GET /global_ip_usage`

```ruby
global_ip_usage = client.global_ip_usage.retrieve

puts(global_ip_usage)
```
```