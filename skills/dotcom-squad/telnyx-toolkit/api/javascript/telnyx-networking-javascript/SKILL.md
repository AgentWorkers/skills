---
name: telnyx-networking-javascript
description: >-
  Configure private networks, WireGuard VPN gateways, internet gateways, and
  virtual cross connects. This skill provides JavaScript SDK examples.
metadata:
  author: telnyx
  product: networking
  language: javascript
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 网络服务 - JavaScript

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

以下所有示例均假设 `client` 已按上述方式初始化。

## 列出所有区域

列出所有区域及其支持的接口

`GET /regions`

```javascript
const regions = await client.regions.list();

console.log(regions.data);
```

## 列出所有网络

列出所有网络。

`GET /networks`

```javascript
// Automatically fetches more pages as needed.
for await (const networkListResponse of client.networks.list()) {
  console.log(networkListResponse);
}
```

## 创建网络

创建一个新的网络。

`POST /networks`

```javascript
const network = await client.networks.create({ name: 'test network' });

console.log(network.data);
```

## 获取网络信息

检索网络信息。

`GET /networks/{id}`

```javascript
const network = await client.networks.retrieve('6a09cdc3-8948-47f0-aa62-74ac943d6c58');

console.log(network.data);
```

## 更新网络

更新网络信息。

`PATCH /networks/{id}`

```javascript
const network = await client.networks.update('6a09cdc3-8948-47f0-aa62-74ac943d6c58', {
  name: 'test network',
});

console.log(network.data);
```

## 删除网络

删除网络。

`DELETE /networks/{id}`

```javascript
const network = await client.networks.delete('6a09cdc3-8948-47f0-aa62-74ac943d6c58');

console.log(network.data);
```

## 获取默认网关状态

`GET /networks/{id}/default_gateway`

```javascript
const defaultGateway = await client.networks.defaultGateway.retrieve(
  '6a09cdc3-8948-47f0-aa62-74ac943d6c58',
);

console.log(defaultGateway.data);
```

## 创建默认网关

`POST /networks/{id}/default_gateway`

```javascript
const defaultGateway = await client.networks.defaultGateway.create(
  '6a09cdc3-8948-47f0-aa62-74ac943d6c58',
);

console.log(defaultGateway.data);
```

## 删除默认网关

`DELETE /networks/{id}/default_gateway`

```javascript
const defaultGateway = await client.networks.defaultGateway.delete(
  '6a09cdc3-8948-47f0-aa62-74ac943d6c58',
);

console.log(defaultGateway.data);
```

## 获取网络的所有接口

`GET /networks/{id}/networkInterfaces`

```javascript
// Automatically fetches more pages as needed.
for await (const networkListInterfacesResponse of client.networks.listInterfaces(
  '6a09cdc3-8948-47f0-aa62-74ac943d6c58',
)) {
  console.log(networkListInterfacesResponse);
}
```

## 列出所有 WireGuard 接口

列出所有 WireGuard 接口。

`GET /wireguardInterfaces`

```javascript
// Automatically fetches more pages as needed.
for await (const wireguardInterfaceListResponse of client.wireguardInterfaces.list()) {
  console.log(wireguardInterfaceListResponse);
}
```

## 创建新的 WireGuard 接口

创建一个新的 WireGuard 接口。

`POST /wireguardInterfaces`

```javascript
const wireguardInterface = await client.wireguardInterfaces.create({ region_code: 'ashburn-va' });

console.log(wireguardInterface.data);
```

## 获取 WireGuard 接口信息

检索 WireGuard 接口信息。

`GET /wireguardInterfaces/{id}`

```javascript
const wireguardInterface = await client.wireguardInterfaces.retrieve(
  '6a09cdc3-8948-47f0-aa62-74ac943d6c58',
);

console.log(wireguardInterface.data);
```

## 删除 WireGuard 接口

删除 WireGuard 接口。

`DELETE /wireguardInterfaces/{id}`

```javascript
const wireguardInterface = await client.wireguardInterfaces.delete(
  '6a09cdc3-8948-47f0-aa62-74ac943d6c58',
);

console.log(wireguardInterface.data);
```

## 列出所有 WireGuard 对等体

列出所有 WireGuard 对等体。

`GET /wireguard_peers`

```javascript
// Automatically fetches more pages as needed.
for await (const wireguardPeerListResponse of client.wireguardPeers.list()) {
  console.log(wireguardPeerListResponse);
}
```

## 创建新的 WireGuard 对等体

创建一个新的 WireGuard 对等体。

`POST /wireguard_peers`

```javascript
const wireguardPeer = await client.wireguardPeers.create({
  wireguard_interface_id: '6a09cdc3-8948-47f0-aa62-74ac943d6c58',
});

console.log(wireguardPeer.data);
```

## 获取 WireGuard 对等体信息

检索 WireGuard 对等体信息。

`GET /wireguard_peers/{id}`

```javascript
const wireguardPeer = await client.wireguardPeers.retrieve('6a09cdc3-8948-47f0-aa62-74ac943d6c58');

console.log(wireguardPeer.data);
```

## 更新 WireGuard 对等体信息

更新 WireGuard 对等体信息。

`PATCH /wireguard_peers/{id}`

```javascript
const wireguardPeer = await client.wireguardPeers.update('6a09cdc3-8948-47f0-aa62-74ac943d6c58');

console.log(wireguardPeer.data);
```

## 删除 WireGuard 对等体

删除 WireGuard 对等体。

`DELETE /wireguard_peers/{id}`

```javascript
const wireguardPeer = await client.wireguardPeers.delete('6a09cdc3-8948-47f0-aa62-74ac943d6c58');

console.log(wireguardPeer.data);
```

## 获取 WireGuard 对等体的配置模板

`GET /wireguard_peers/{id}/config`

```javascript
const response = await client.wireguardPeers.retrieveConfig('6a09cdc3-8948-47f0-aa62-74ac943d6c58');

console.log(response);
```

## 获取用户所有的私有无线网关

获取用户所有的私有无线网关。

`GET /private_wireless_gateways`

```javascript
// Automatically fetches more pages as needed.
for await (const privateWirelessGateway of client.privateWirelessGateways.list()) {
  console.log(privateWirelessGateway.id);
}
```

## 为已创建的网络创建私有无线网关

异步地为已创建的网络的 SIM 卡创建私有无线网关。

`POST /private_wireless_gateways` — 必需参数：`network_id`, `name`

```javascript
const privateWirelessGateway = await client.privateWirelessGateways.create({
  name: 'My private wireless gateway',
  network_id: '6a09cdc3-8948-47f0-aa62-74ac943d6c58',
});

console.log(privateWirelessGateway.data);
```

## 获取私有无线网关信息

检索私有无线网关的信息。

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

## 列出所有公共互联网网关

列出所有公共互联网网关。

`GET /public_internet_gateways`

```javascript
// Automatically fetches more pages as needed.
for await (const publicInternetGatewayListResponse of client.publicInternetGateways.list()) {
  console.log(publicInternetGatewayListResponse);
}
```

## 创建公共互联网网关

创建一个新的公共互联网网关。

`POST /public_internet_gateways`

```javascript
const publicInternetGateway = await client.publicInternetGateways.create();

console.log(publicInternetGateway.data);
```

## 获取公共互联网网关信息

检索公共互联网网关的信息。

`GET /public_internet_gateways/{id}`

```javascript
const publicInternetGateway = await client.publicInternetGateways.retrieve(
  '6a09cdc3-8948-47f0-aa62-74ac943d6c58',
);

console.log(publicInternetGateway.data);
```

## 删除公共互联网网关

删除公共互联网网关。

`DELETE /public_internet_gateways/{id}`

```javascript
const publicInternetGateway = await client.publicInternetGateways.delete(
  '6a09cdc3-8948-47f0-aa62-74ac943d6c58',
);

console.log(publicInternetGateway.data);
```

## 列出所有虚拟跨连接

列出所有虚拟跨连接。

`GET /virtual_cross_connects`

```javascript
// Automatically fetches more pages as needed.
for await (const virtualCrossConnectListResponse of client.virtualCrossConnects.list()) {
  console.log(virtualCrossConnectListResponse);
}
```

## 创建虚拟跨连接

创建一个新的虚拟跨连接。<br /><br />对于 AWS 和 GCE，您可以先创建主连接，然后再创建次级连接。

`POST /virtual_cross_connects`

```javascript
const virtualCrossConnect = await client.virtualCrossConnects.create({ region_code: 'ashburn-va' });

console.log(virtualCrossConnect.data);
```

## 获取虚拟跨连接信息

检索虚拟跨连接的信息。

`GET /virtual_cross_connects/{id}`

```javascript
const virtualCrossConnect = await client.virtualCrossConnects.retrieve(
  '6a09cdc3-8948-47f0-aa62-74ac943d6c58',
);

console.log(virtualCrossConnect.data);
```

## 更新虚拟跨连接

更新虚拟跨连接。<br /><br />只有在“创建”状态下才能修改云 IP 地址；因为 GCE 会在连接请求完成后再通知您生成的 IP 地址...

`PATCH /virtual_cross_connects/{id}`

```javascript
const virtualCrossConnect = await client.virtualCrossConnects.update(
  '6a09cdc3-8948-47f0-aa62-74ac943d6c58',
);

console.log(virtualCrossConnect.data);
```

## 删除虚拟跨连接

删除虚拟跨连接。

`DELETE /virtual_cross_connects/{id}`

```javascript
const virtualCrossConnect = await client.virtualCrossConnects.delete(
  '6a09cdc3-8948-47f0-aa62-74ac943d6c58',
);

console.log(virtualCrossConnect.data);
```

## 查看虚拟跨连接的覆盖范围

查看虚拟跨连接的覆盖范围。<br /><br />此端点显示虚拟跨连接将被配置到的云区域。

`GET /virtual_cross_connects/coverage`

```javascript
// Automatically fetches more pages as needed.
for await (const virtualCrossConnectsCoverageListResponse of client.virtualCrossConnectsCoverage.list()) {
  console.log(virtualCrossConnectsCoverageListResponse.available_bandwidth);
}
```

## 列出所有全局 IP 地址

列出所有全局 IP 地址。

`GET /global_ips`

```javascript
// Automatically fetches more pages as needed.
for await (const globalIPListResponse of client.globalIPs.list()) {
  console.log(globalIPListResponse);
}
```

## 创建全局 IP 地址

创建一个新的全局 IP 地址。

`POST /global_ips`

```javascript
const globalIP = await client.globalIPs.create();

console.log(globalIP.data);
```

## 获取全局 IP 地址信息

检索全局 IP 地址的信息。

`GET /global_ips/{id}`

```javascript
const globalIP = await client.globalIPs.retrieve('6a09cdc3-8948-47f0-aa62-74ac943d6c58');

console.log(globalIP.data);
```

## 删除全局 IP 地址

删除全局 IP 地址。

`DELETE /global_ips/{id}`

```javascript
const globalIP = await client.globalIPs.delete('6a09cdc3-8948-47f0-aa62-74ac943d6c58');

console.log(globalIP.data);
```

## 列出所有允许使用的全局 IP 地址端口

列出所有允许使用的全局 IP 地址端口。

`GET /global_ip_allowed_ports`

```javascript
const globalIPAllowedPorts = await client.globalIPAllowedPorts.list();

console.log(globalIPAllowedPorts.data);
```

## 全局 IP 地址分配的健康检查指标

获取全局 IP 地址分配的健康检查指标。

`GET /global_ip_assignment_health`

```javascript
const globalIPAssignmentHealth = await client.globalIPAssignmentHealth.retrieve();

console.log(globalIPAssignmentHealth.data);
```

## 列出所有全局 IP 地址分配记录

列出所有全局 IP 地址的分配记录。

`GET /global_ip_assignments`

```javascript
// Automatically fetches more pages as needed.
for await (const globalIPAssignment of client.globalIPAssignments.list()) {
  console.log(globalIPAssignment.id);
}
```

## 创建全局 IP 地址分配记录

创建一个新的全局 IP 地址分配记录。

`POST /global_ip_assignments`

```javascript
const globalIPAssignment = await client.globalIPAssignments.create();

console.log(globalIPAssignment.data);
```

## 获取全局 IP 地址分配记录

检索全局 IP 地址的分配记录。

`GET /global_ip_assignments/{id}`

```javascript
const globalIPAssignment = await client.globalIPAssignments.retrieve(
  '6a09cdc3-8948-47f0-aa62-74ac943d6c58',
);

console.log(globalIPAssignment.data);
```

## 更新全局 IP 地址分配记录

更新全局 IP 地址的分配记录。

`PATCH /global_ip_assignments/{id}`

```javascript
const globalIPAssignment = await client.globalIPAssignments.update(
  '6a09cdc3-8948-47f0-aa62-74ac943d6c58',
  { globalIpAssignmentUpdateRequest: {} },
);

console.log(globalIPAssignment.data);
```

## 删除全局 IP 地址分配记录

删除全局 IP 地址的分配记录。

`DELETE /global_ip_assignments/{id}`

```javascript
const globalIPAssignment = await client.globalIPAssignments.delete(
  '6a09cdc3-8948-47f0-aa62-74ac943d6c58',
);

console.log(globalIPAssignment.data);
```

## 全局 IP 地址分配的使用情况指标

获取全局 IP 地址分配的使用情况指标。

`GET /global_ip_assignments/usage`

```javascript
const globalIPAssignmentsUsage = await client.globalIPAssignmentsUsage.retrieve();

console.log(globalIPAssignmentsUsage.data);
```

## 列出所有全局 IP 地址的健康检查类型

列出所有全局 IP 地址的健康检查类型。

`GET /global_ip_health_check_types`

```javascript
const globalIPHealthCheckTypes = await client.globalIPHealthCheckTypes.list();

console.log(globalIPHealthCheckTypes.data);
```

## 列出所有全局 IP 地址的健康检查记录

列出所有全局 IP 地址的健康检查记录。

`GET /global_ip_health_checks`

```javascript
// Automatically fetches more pages as needed.
for await (const globalIPHealthCheckListResponse of client.globalIPHealthChecks.list()) {
  console.log(globalIPHealthCheckListResponse);
}
```

## 创建全局 IP 地址的健康检查记录

创建一个新的全局 IP 地址健康检查记录。

`POST /global_ip_health_checks`

```javascript
const globalIPHealthCheck = await client.globalIPHealthChecks.create();

console.log(globalIPHealthCheck.data);
```

## 获取全局 IP 地址的健康检查记录

检索全局 IP 地址的健康检查记录。

`GET /global_ip_health_checks/{id}`

```javascript
const globalIPHealthCheck = await client.globalIPHealthChecks.retrieve(
  '6a09cdc3-8948-47f0-aa62-74ac943d6c58',
);

console.log(globalIPHealthCheck.data);
```

## 删除全局 IP 地址的健康检查记录

删除全局 IP 地址的健康检查记录。

`DELETE /global_ip_health_checks/{id}`

```javascript
const globalIPHealthCheck = await client.globalIPHealthChecks.delete(
  '6a09cdc3-8948-47f0-aa62-74ac943d6c58',
);

console.log(globalIPHealthCheck.data);
```

## 全局 IP 地址的延迟指标

获取全局 IP 地址的延迟指标。

`GET /global_ip_latency`

```javascript
const globalIPLatency = await client.globalIPLatency.retrieve();

console.log(globalIPLatency.data);
```

## 列出所有全局 IP 协议

列出所有全局 IP 协议。

`GET /global_ip_protocols`

```javascript
const globalIPProtocols = await client.globalIPProtocols.list();

console.log(globalIPProtocols.data);
```

## 全局 IP 地址的使用情况指标

获取全局 IP 地址的使用情况指标。

`GET /global_ip_usage`

```javascript
const globalIPUsage = await client.globalIPUsage.retrieve();

console.log(globalIPUsage.data);
```