---
name: telnyx-networking-python
description: >-
  Configure private networks, WireGuard VPN gateways, internet gateways, and
  virtual cross connects. This skill provides Python SDK examples.
metadata:
  author: telnyx
  product: networking
  language: python
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 网络服务 - Python

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

以下所有示例均假设 `client` 已按照上述方式初始化。

## 列出所有区域

列出所有区域及其支持的接口

`GET /regions`

```python
regions = client.regions.list()
print(regions.data)
```

## 列出所有网络

列出所有网络。

`GET /networks`

```python
page = client.networks.list()
page = page.data[0]
print(page)
```

## 创建网络

创建一个新的网络。

`POST /networks`

```python
network = client.networks.create(
    name="test network",
)
print(network.data)
```

## 获取网络信息

检索网络信息。

`GET /networks/{id}`

```python
network = client.networks.retrieve(
    "6a09cdc3-8948-47f0-aa62-74ac943d6c58",
)
print(network.data)
```

## 更新网络

更新网络信息。

`PATCH /networks/{id}`

```python
network = client.networks.update(
    network_id="6a09cdc3-8948-47f0-aa62-74ac943d6c58",
    name="test network",
)
print(network.data)
```

## 删除网络

删除网络。

`DELETE /networks/{id}`

```python
network = client.networks.delete(
    "6a09cdc3-8948-47f0-aa62-74ac943d6c58",
)
print(network.data)
```

## 获取默认网关状态

`GET /networks/{id}/default_gateway`

```python
default_gateway = client.networks.default_gateway.retrieve(
    "6a09cdc3-8948-47f0-aa62-74ac943d6c58",
)
print(default_gateway.data)
```

## 创建默认网关

`POST /networks/{id}/default_gateway`

```python
default_gateway = client.networks.default_gateway.create(
    network_identifier="6a09cdc3-8948-47f0-aa62-74ac943d6c58",
)
print(default_gateway.data)
```

## 删除默认网关

`DELETE /networks/{id}/default_gateway`

```python
default_gateway = client.networks.default_gateway.delete(
    "6a09cdc3-8948-47f0-aa62-74ac943d6c58",
)
print(default_gateway.data)
```

## 列出网络的所有接口

`GET /networks/{id}/networkInterfaces`

```python
page = client.networks.list_interfaces(
    id="6a09cdc3-8948-47f0-aa62-74ac943d6c58",
)
page = page.data[0]
print(page)
```

## 列出所有 WireGuard 接口

列出所有 WireGuard 接口。

`GET /wireguard_interfaces`

```python
page = client.wireguard_interfaces.list()
page = page.data[0]
print(page)
```

## 创建新的 WireGuard 接口

创建一个新的 WireGuard 接口。

`POST /wireguard_interfaces`

```python
wireguard_interface = client.wireguard_interfaces.create(
    region_code="ashburn-va",
)
print(wireguard_interface.data)
```

## 获取 WireGuard 接口信息

检索 WireGuard 接口信息。

`GET /wireguardinterfaces/{id}`

```python
wireguard_interface = client.wireguard_interfaces.retrieve(
    "6a09cdc3-8948-47f0-aa62-74ac943d6c58",
)
print(wireguard_interface.data)
```

## 删除 WireGuard 接口

删除 WireGuard 接口。

`DELETE /wireguardinterfaces/{id}`

```python
wireguard_interface = client.wireguard_interfaces.delete(
    "6a09cdc3-8948-47f0-aa62-74ac943d6c58",
)
print(wireguard_interface.data)
```

## 列出所有 WireGuard 对等方

列出所有 WireGuard 对等方。

`GET /wireguard_peers`

```python
page = client.wireguard_peers.list()
page = page.data[0]
print(page)
```

## 创建新的 WireGuard 对等方

创建一个新的 WireGuard 对等方。

`POST /wireguard_peers`

```python
wireguard_peer = client.wireguard_peers.create(
    wireguard_interface_id="6a09cdc3-8948-47f0-aa62-74ac943d6c58",
)
print(wireguard_peer.data)
```

## 获取 WireGuard 对等方信息

检索 WireGuard 对等方信息。

`GET /wireguard_peers/{id}`

```python
wireguard_peer = client.wireguard_peers.retrieve(
    "6a09cdc3-8948-47f0-aa62-74ac943d6c58",
)
print(wireguard_peer.data)
```

## 更新 WireGuard 对等方信息

更新 WireGuard 对等方信息。

`PATCH /wireguard_peers/{id}`

```python
wireguard_peer = client.wireguard_peers.update(
    id="6a09cdc3-8948-47f0-aa62-74ac943d6c58",
)
print(wireguard_peer.data)
```

## 删除 WireGuard 对等方

删除 WireGuard 对等方。

`DELETE /wireguard_peers/{id}`

```python
wireguard_peer = client.wireguard_peers.delete(
    "6a09cdc3-8948-47f0-aa62-74ac943d6c58",
)
print(wireguard_peer.data)
```

## 获取 WireGuard 对等方的配置模板

`GET /wireguard_peers/{id}/config`

```python
response = client.wireguard_peers.retrieve_config(
    "6a09cdc3-8948-47f0-aa62-74ac943d6c58",
)
print(response)
```

## 获取用户所有的私有无线网关

获取用户所有的私有无线网关。

`GET /private_wireless_gateways`

```python
page = client.private_wireless_gateways.list()
page = page.data[0]
print(page.id)
```

## 创建私有无线网关

为已创建的网络中的 SIM 卡异步创建私有无线网关。

`POST /private_wireless_gateways` — 必需参数：`network_id`, `name`

```python
private_wireless_gateway = client.private_wireless_gateways.create(
    name="My private wireless gateway",
    network_id="6a09cdc3-8948-47f0-aa62-74ac943d6c58",
)
print(private_wireless_gateway.data)
```

## 获取私有无线网关信息

检索私有无线网关的详细信息。

`GET /private_wireless_gateways/{id}`

```python
private_wireless_gateway = client.private_wireless_gateways.retrieve(
    "6a09cdc3-8948-47f0-aa62-74ac943d6c58",
)
print(private_wireless_gateway.data)
```

## 删除私有无线网关

删除私有无线网关。

`DELETE /private_wireless_gateways/{id}`

```python
private_wireless_gateway = client.private_wireless_gateways.delete(
    "6a09cdc3-8948-47f0-aa62-74ac943d6c58",
)
print(private_wireless_gateway.data)
```

## 列出所有公共互联网网关

列出所有公共互联网网关。

`GET /public_internet_gateways`

```python
page = client.public_internet_gateways.list()
page = page.data[0]
print(page)
```

## 创建公共互联网网关

创建一个新的公共互联网网关。

`POST /public_internet_gateways`

```python
public_internet_gateway = client.public_internet_gateways.create()
print(public_internet_gateway.data)
```

## 获取公共互联网网关信息

检索公共互联网网关的详细信息。

`GET /public_internet_gateways/{id}`

```python
public_internet_gateway = client.public_internet_gateways.retrieve(
    "6a09cdc3-8948-47f0-aa62-74ac943d6c58",
)
print(public_internet_gateway.data)
```

## 删除公共互联网网关

删除公共互联网网关。

`DELETE /public_internet_gateways/{id}`

```python
public_internet_gateway = client.public_internet_gateways.delete(
    "6a09cdc3-8948-47f0-aa62-74ac943d6c58",
)
print(public_internet_gateway.data)
```

## 列出所有虚拟跨连接

列出所有虚拟跨连接。

`GET /virtual_cross_connects`

```python
page = client.virtual_cross_connects.list()
page = page.data[0]
print(page)
```

## 创建虚拟跨连接

创建一个新的虚拟跨连接。<br /><br />对于 AWS 和 GCE，您可以先创建主连接，再创建次级连接。

`POST /virtual_cross_connects`

```python
virtual_cross_connect = client.virtual_cross_connects.create(
    region_code="ashburn-va",
)
print(virtual_cross_connect.data)
```

## 获取虚拟跨连接信息

检索虚拟跨连接的详细信息。

`GET /virtual_cross_connects/{id}`

```python
virtual_cross_connect = client.virtual_cross_connects.retrieve(
    "6a09cdc3-8948-47f0-aa62-74ac943d6c58",
)
print(virtual_cross_connect.data)
```

## 更新虚拟跨连接

更新虚拟跨连接的信息。<br /><br />只有在“创建”状态下才能修改云 IP 地址；因为 GCE 会在连接请求处理完成后才会通知您生成的 IP 地址...

`PATCH /virtual_cross_connects/{id}`

```python
virtual_cross_connect = client.virtual_cross_connects.update(
    id="6a09cdc3-8948-47f0-aa62-74ac943d6c58",
)
print(virtual_cross_connect.data)
```

## 删除虚拟跨连接

删除虚拟跨连接。

`DELETE /virtual_cross_connects/{id}`

```python
virtual_cross_connect = client.virtual_cross_connects.delete(
    "6a09cdc3-8948-47f0-aa62-74ac943d6c58",
)
print(virtual_cross_connect.data)
```

## 查看虚拟跨连接的覆盖范围

查看虚拟跨连接可使用的云区域。

`GET /virtual_cross_connects/coverage`

```python
page = client.virtual_cross_connects_coverage.list()
page = page.data[0]
print(page.available_bandwidth)
```

## 列出所有全局 IP 地址

列出所有全局 IP 地址。

`GET /global_ips`

```python
page = client.global_ips.list()
page = page.data[0]
print(page)
```

## 创建全局 IP 地址

创建一个新的全局 IP 地址。

`POST /global_ips`

```python
global_ip = client.global_ips.create()
print(global_ip.data)
```

## 获取全局 IP 地址信息

检索全局 IP 地址的详细信息。

`GET /global_ips/{id}`

```python
global_ip = client.global_ips.retrieve(
    "6a09cdc3-8948-47f0-aa62-74ac943d6c58",
)
print(global_ip.data)
```

## 删除全局 IP 地址

删除全局 IP 地址。

`DELETE /global_ips/{id}`

```python
global_ip = client.global_ips.delete(
    "6a09cdc3-8948-47f0-aa62-74ac943d6c58",
)
print(global_ip.data)
```

## 列出所有允许使用的全局 IP 地址端口

列出所有允许使用的全局 IP 地址端口。

`GET /global_ip_allowed_ports`

```python
global_ip_allowed_ports = client.global_ip_allowed_ports.list()
print(global_ip_allowed_ports.data)
```

## 全局 IP 地址分配健康检查指标

获取全局 IP 地址分配的健康检查指标。

`GET /global_ip_assignment_health`

```python
global_ip_assignment_health = client.global_ip_assignment_health.retrieve()
print(global_ip_assignment_health.data)
```

## 列出所有全局 IP 地址分配记录

列出所有全局 IP 地址的分配记录。

`GET /global_ip_assignments`

```python
page = client.global_ip_assignments.list()
page = page.data[0]
print(page.id)
```

## 创建全局 IP 地址分配记录

创建一个新的全局 IP 地址分配记录。

`POST /global_ip_assignments`

```python
global_ip_assignment = client.global_ip_assignments.create()
print(global_ip_assignment.data)
```

## 获取全局 IP 地址分配记录

检索全局 IP 地址的分配记录。

`GET /global_ip_assignments/{id}`

```python
global_ip_assignment = client.global_ip_assignments.retrieve(
    "6a09cdc3-8948-47f0-aa62-74ac943d6c58",
)
print(global_ip_assignment.data)
```

## 更新全局 IP 地址分配记录

更新全局 IP 地址的分配记录。

`PATCH /global_ip_assignments/{id}`

```python
global_ip_assignment = client.global_ip_assignments.update(
    global_ip_assignment_id="6a09cdc3-8948-47f0-aa62-74ac943d6c58",
    global_ip_assignment_update_request={},
)
print(global_ip_assignment.data)
```

## 删除全局 IP 地址分配记录

删除全局 IP 地址的分配记录。

`DELETE /global_ip_assignments/{id}`

```python
global_ip_assignment = client.global_ip_assignments.delete(
    "6a09cdc3-8948-47f0-aa62-74ac943d6c58",
)
print(global_ip_assignment.data)
```

## 全局 IP 地址分配使用情况指标

获取全局 IP 地址分配的使用情况指标。

`GET /global_ip_assignments/usage`

```python
global_ip_assignments_usage = client.global_ip_assignments_usage.retrieve()
print(global_ip_assignments_usage.data)
```

## 列出所有全局 IP 地址的健康检查类型

列出所有全局 IP 地址的健康检查类型。

`GET /global_ip_health_check_types`

```python
global_ip_health_check_types = client.global_ip_health_check_types.list()
print(global_ip_health_check_types.data)
```

## 列出所有全局 IP 地址的健康检查记录

列出所有全局 IP 地址的健康检查记录。

`GET /global_ip_health_checks`

```python
page = client.global_ip_health_checks.list()
page = page.data[0]
print(page)
```

## 创建全局 IP 地址的健康检查记录

创建一个新的全局 IP 地址健康检查记录。

`POST /global_ip_health_checks`

```python
global_ip_health_check = client.global_ip_health_checks.create()
print(global_ip_health_check.data)
```

## 获取全局 IP 地址的健康检查记录

检索全局 IP 地址的健康检查记录。

`GET /global_ip_health_checks/{id}`

```python
global_ip_health_check = client.global_ip_health_checks.retrieve(
    "6a09cdc3-8948-47f0-aa62-74ac943d6c58",
)
print(global_ip_health_check.data)
```

## 删除全局 IP 地址的健康检查记录

删除全局 IP 地址的健康检查记录。

`DELETE /global_ip_health_checks/{id}`

```python
global_ip_health_check = client.global_ip_health_checks.delete(
    "6a09cdc3-8948-47f0-aa62-74ac943d6c58",
)
print(global_ip_health_check.data)
```

## 全局 IP 地址的延迟指标

获取全局 IP 地址的延迟指标。

`GET /global_ip_latency`

```python
global_ip_latency = client.global_ip_latency.retrieve()
print(global_ip_latency.data)
```

## 列出所有全局 IP 协议

列出所有全局 IP 地址支持的协议。

`GET /global_ip_protocols`

```python
global_ip_protocols = client.global_ip_protocols.list()
print(global_ip_protocols.data)
```

## 全局 IP 地址的使用情况指标

获取全局 IP 地址的使用情况指标。

`GET /global_ip_usage`

```python
global_ip_usage = client.global_ip_usage.retrieve()
print(global_ip_usage.data)
```
```