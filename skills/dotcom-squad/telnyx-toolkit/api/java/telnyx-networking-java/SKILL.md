---
name: telnyx-networking-java
description: >-
  Configure private networks, WireGuard VPN gateways, internet gateways, and
  virtual cross connects. This skill provides Java SDK examples.
metadata:
  author: telnyx
  product: networking
  language: java
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 网络服务 - Java

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

## 列出所有区域

列出所有区域及其支持的接口

`GET /regions`

```java
import com.telnyx.sdk.models.regions.RegionListParams;
import com.telnyx.sdk.models.regions.RegionListResponse;

RegionListResponse regions = client.regions().list();
```

## 列出所有网络

列出所有网络。

`GET /networks`

```java
import com.telnyx.sdk.models.networks.NetworkListPage;
import com.telnyx.sdk.models.networks.NetworkListParams;

NetworkListPage page = client.networks().list();
```

## 创建网络

创建一个新的网络。

`POST /networks`

```java
import com.telnyx.sdk.models.networks.NetworkCreate;
import com.telnyx.sdk.models.networks.NetworkCreateParams;
import com.telnyx.sdk.models.networks.NetworkCreateResponse;

NetworkCreate params = NetworkCreate.builder()
    .name("test network")
    .build();
NetworkCreateResponse network = client.networks().create(params);
```

## 查取网络信息

获取网络信息。

`GET /networks/{id}`

```java
import com.telnyx.sdk.models.networks.NetworkRetrieveParams;
import com.telnyx.sdk.models.networks.NetworkRetrieveResponse;

NetworkRetrieveResponse network = client.networks().retrieve("6a09cdc3-8948-47f0-aa62-74ac943d6c58");
```

## 更新网络信息

更新网络信息。

`PATCH /networks/{id}`

```java
import com.telnyx.sdk.models.networks.NetworkCreate;
import com.telnyx.sdk.models.networks.NetworkUpdateParams;
import com.telnyx.sdk.models.networks.NetworkUpdateResponse;

NetworkUpdateParams params = NetworkUpdateParams.builder()
    .networkId("6a09cdc3-8948-47f0-aa62-74ac943d6c58")
    .networkCreate(NetworkCreate.builder()
        .name("test network")
        .build())
    .build();
NetworkUpdateResponse network = client.networks().update(params);
```

## 删除网络

删除网络。

`DELETE /networks/{id}`

```java
import com.telnyx.sdk.models.networks.NetworkDeleteParams;
import com.telnyx.sdk.models.networks.NetworkDeleteResponse;

NetworkDeleteResponse network = client.networks().delete("6a09cdc3-8948-47f0-aa62-74ac943d6c58");
```

## 获取默认网关状态

`GET /networks/{id}/default_gateway`

```java
import com.telnyx.sdk.models.networks.defaultgateway.DefaultGatewayRetrieveParams;
import com.telnyx.sdk.models.networks.defaultgateway.DefaultGatewayRetrieveResponse;

DefaultGatewayRetrieveResponse defaultGateway = client.networks().defaultGateway().retrieve("6a09cdc3-8948-47f0-aa62-74ac943d6c58");
```

## 创建默认网关

`POST /networks/{id}/default_gateway`

```java
import com.telnyx.sdk.models.networks.defaultgateway.DefaultGatewayCreateParams;
import com.telnyx.sdk.models.networks.defaultgateway.DefaultGatewayCreateResponse;

DefaultGatewayCreateResponse defaultGateway = client.networks().defaultGateway().create("6a09cdc3-8948-47f0-aa62-74ac943d6c58");
```

## 删除默认网关

`DELETE /networks/{id}/default_gateway`

```java
import com.telnyx.sdk.models.networks.defaultgateway.DefaultGatewayDeleteParams;
import com.telnyx.sdk.models.networks.defaultgateway.DefaultGatewayDeleteResponse;

DefaultGatewayDeleteResponse defaultGateway = client.networks().defaultGateway().delete("6a09cdc3-8948-47f0-aa62-74ac943d6c58");
```

## 列出网络的所有接口

`GET /networks/{id}/networkInterfaces`

```java
import com.telnyx.sdk.models.networks.NetworkListInterfacesPage;
import com.telnyx.sdk.models.networks.NetworkListInterfacesParams;

NetworkListInterfacesPage page = client.networks().listInterfaces("6a09cdc3-8948-47f0-aa62-74ac943d6c58");
```

## 列出所有 WireGuard 接口

列出所有 WireGuard 接口。

`GET /wireguardInterfaces`

```java
import com.telnyx.sdk.models.wireguardinterfaces.WireguardInterfaceListPage;
import com.telnyx.sdk.models.wireguardinterfaces.WireguardInterfaceListParams;

WireguardInterfaceListPage page = client.wireguardInterfaces().list();
```

## 创建新的 WireGuard 接口

创建一个新的 WireGuard 接口。

`POST /wireguardInterfaces`

```java
import com.telnyx.sdk.models.wireguardinterfaces.WireguardInterfaceCreateParams;
import com.telnyx.sdk.models.wireguardinterfaces.WireguardInterfaceCreateResponse;

WireguardInterfaceCreateResponse wireguardInterface = client.wireguardInterfaces().create();
```

## 查取 WireGuard 接口信息

获取 WireGuard 接口信息。

`GET /wireguardInterfaces/{id}`

```java
import com.telnyx.sdk.models.wireguardinterfaces.WireguardInterfaceRetrieveParams;
import com.telnyx.sdk.models.wireguardinterfaces.WireguardInterfaceRetrieveResponse;

WireguardInterfaceRetrieveResponse wireguardInterface = client.wireguardInterfaces().retrieve("6a09cdc3-8948-47f0-aa62-74ac943d6c58");
```

## 删除 WireGuard 接口

删除 WireGuard 接口。

`DELETE /wireguardInterfaces/{id}`

```java
import com.telnyx.sdk.models.wireguardinterfaces.WireguardInterfaceDeleteParams;
import com.telnyx.sdk.models.wireguardinterfaces.WireguardInterfaceDeleteResponse;

WireguardInterfaceDeleteResponse wireguardInterface = client.wireguardInterfaces().delete("6a09cdc3-8948-47f0-aa62-74ac943d6c58");
```

## 列出所有 WireGuard 对等方

列出所有 WireGuard 对等方。

`GET /wireguard_peers`

```java
import com.telnyx.sdk.models.wireguardpeers.WireguardPeerListPage;
import com.telnyx.sdk.models.wireguardpeers.WireguardPeerListParams;

WireguardPeerListPage page = client.wireguardPeers().list();
```

## 创建新的 WireGuard 对等方

创建一个新的 WireGuard 对等方。

`POST /wireguard_peers`

```java
import com.telnyx.sdk.models.wireguardpeers.WireguardPeerCreateParams;
import com.telnyx.sdk.models.wireguardpeers.WireguardPeerCreateResponse;

WireguardPeerCreateParams params = WireguardPeerCreateParams.builder()
    .wireguardInterfaceId("6a09cdc3-8948-47f0-aa62-74ac943d6c58")
    .build();
WireguardPeerCreateResponse wireguardPeer = client.wireguardPeers().create(params);
```

## 查取 WireGuard 对等方信息

获取 WireGuard 对等方信息。

`GET /wireguard_peers/{id}`

```java
import com.telnyx.sdk.models.wireguardpeers.WireguardPeerRetrieveParams;
import com.telnyx.sdk.models.wireguardpeers.WireguardPeerRetrieveResponse;

WireguardPeerRetrieveResponse wireguardPeer = client.wireguardPeers().retrieve("6a09cdc3-8948-47f0-aa62-74ac943d6c58");
```

## 更新 WireGuard 对等方信息

更新 WireGuard 对等方信息。

`PATCH /wireguard_peers/{id}`

```java
import com.telnyx.sdk.models.wireguardpeers.WireguardPeerPatch;
import com.telnyx.sdk.models.wireguardpeers.WireguardPeerUpdateParams;
import com.telnyx.sdk.models.wireguardpeers.WireguardPeerUpdateResponse;

WireguardPeerUpdateParams params = WireguardPeerUpdateParams.builder()
    .id("6a09cdc3-8948-47f0-aa62-74ac943d6c58")
    .wireguardPeerPatch(WireguardPeerPatch.builder().build())
    .build();
WireguardPeerUpdateResponse wireguardPeer = client.wireguardPeers().update(params);
```

## 删除 WireGuard 对等方

删除 WireGuard 对等方。

`DELETE /wireguard_peers/{id}`

```java
import com.telnyx.sdk.models.wireguardpeers.WireguardPeerDeleteParams;
import com.telnyx.sdk.models.wireguardpeers.WireguardPeerDeleteResponse;

WireguardPeerDeleteResponse wireguardPeer = client.wireguardPeers().delete("6a09cdc3-8948-47f0-aa62-74ac943d6c58");
```

## 获取 WireGuard 对等方的配置模板

`GET /wireguard_peers/{id}/config`

```java
import com.telnyx.sdk.models.wireguardpeers.WireguardPeerRetrieveConfigParams;

String response = client.wireguardPeers().retrieveConfig("6a09cdc3-8948-47f0-aa62-74ac943d6c58");
```

## 获取用户所有的私有无线网关

获取用户所有的私有无线网关。

`GET /private_wireless_gateways`

```java
import com.telnyx.sdk.models.privatewirelessgateways.PrivateWirelessGatewayListPage;
import com.telnyx.sdk.models.privatewirelessgateways.PrivateWirelessGatewayListParams;

PrivateWirelessGatewayListPage page = client.privateWirelessGateways().list();
```

## 为已创建的网络创建私有无线网关

异步地为已创建的网络中的 SIM 卡创建私有无线网关。

`POST /private_wireless_gateways` — 必需参数：`network_id`、`name`

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

获取私有无线网关的详细信息。

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

## 列出所有公共互联网网关

列出所有公共互联网网关。

`GET /public_internet_gateways`

```java
import com.telnyx.sdk.models.publicinternetgateways.PublicInternetGatewayListPage;
import com.telnyx.sdk.models.publicinternetgateways.PublicInternetGatewayListParams;

PublicInternetGatewayListPage page = client.publicInternetGateways().list();
```

## 创建公共互联网网关

创建一个新的公共互联网网关。

`POST /public_internet_gateways`

```java
import com.telnyx.sdk.models.publicinternetgateways.PublicInternetGatewayCreateParams;
import com.telnyx.sdk.models.publicinternetgateways.PublicInternetGatewayCreateResponse;

PublicInternetGatewayCreateResponse publicInternetGateway = client.publicInternetGateways().create();
```

## 获取公共互联网网关信息

获取公共互联网网关的详细信息。

`GET /public_internet_gateways/{id}`

```java
import com.telnyx.sdk.models.publicinternetgateways.PublicInternetGatewayRetrieveParams;
import com.telnyx.sdk.models.publicinternetgateways.PublicInternetGatewayRetrieveResponse;

PublicInternetGatewayRetrieveResponse publicInternetGateway = client.publicInternetGateways().retrieve("6a09cdc3-8948-47f0-aa62-74ac943d6c58");
```

## 删除公共互联网网关

删除公共互联网网关。

`DELETE /public_internet_gateways/{id}`

```java
import com.telnyx.sdk.models.publicinternetgateways.PublicInternetGatewayDeleteParams;
import com.telnyx.sdk.models.publicinternetgateways.PublicInternetGatewayDeleteResponse;

PublicInternetGatewayDeleteResponse publicInternetGateway = client.publicInternetGateways().delete("6a09cdc3-8948-47f0-aa62-74ac943d6c58");
```

## 列出所有虚拟交叉连接

列出所有虚拟交叉连接。

`GET /virtual_cross_connects`

```java
import com.telnyx.sdk.models.virtualcrossconnects.VirtualCrossConnectListPage;
import com.telnyx.sdk.models.virtualcrossconnects.VirtualCrossConnectListParams;

VirtualCrossConnectListPage page = client.virtualCrossConnects().list();
```

## 创建虚拟交叉连接

创建一个新的虚拟交叉连接。<br /><br />对于 AWS 和 GCE，您可以先创建主连接，然后再创建次级连接。

`POST /virtual_cross_connects`

```java
import com.telnyx.sdk.models.virtualcrossconnects.VirtualCrossConnectCreateParams;
import com.telnyx.sdk.models.virtualcrossconnects.VirtualCrossConnectCreateResponse;

VirtualCrossConnectCreateResponse virtualCrossConnect = client.virtualCrossConnects().create();
```

## 查取虚拟交叉连接信息

获取虚拟交叉连接的详细信息。

`GET /virtual_cross_connects/{id}`

```java
import com.telnyx.sdk.models.virtualcrossconnects.VirtualCrossConnectRetrieveParams;
import com.telnyx.sdk.models.virtualcrossconnects.VirtualCrossConnectRetrieveResponse;

VirtualCrossConnectRetrieveResponse virtualCrossConnect = client.virtualCrossConnects().retrieve("6a09cdc3-8948-47f0-aa62-74ac943d6c58");
```

## 更新虚拟交叉连接信息

更新虚拟交叉连接信息。<br /><br />只有在“创建”状态下才能修改云 IP 地址；GCE 会在连接请求处理完成后通知您生成的 IP 地址...

`PATCH /virtual_cross_connects/{id}`

```java
import com.telnyx.sdk.models.virtualcrossconnects.VirtualCrossConnectUpdateParams;
import com.telnyx.sdk.models.virtualcrossconnects.VirtualCrossConnectUpdateResponse;

VirtualCrossConnectUpdateResponse virtualCrossConnect = client.virtualCrossConnects().update("6a09cdc3-8948-47f0-aa62-74ac943d6c58");
```

## 删除虚拟交叉连接

删除虚拟交叉连接。

`DELETE /virtual_cross_connects/{id}`

```java
import com.telnyx.sdk.models.virtualcrossconnects.VirtualCrossConnectDeleteParams;
import com.telnyx.sdk.models.virtualcrossconnects.VirtualCrossConnectDeleteResponse;

VirtualCrossConnectDeleteResponse virtualCrossConnect = client.virtualCrossConnects().delete("6a09cdc3-8948-47f0-aa62-74ac943d6c58");
```

## 查看虚拟交叉连接的覆盖范围

查看虚拟交叉连接的覆盖范围。<br /><br />此端点显示虚拟交叉连接将被配置到的云区域。

`GET /virtual_cross_connects/coverage`

```java
import com.telnyx.sdk.models.virtualcrossconnectscoverage.VirtualCrossConnectsCoverageListPage;
import com.telnyx.sdk.models.virtualcrossconnectscoverage.VirtualCrossConnectsCoverageListParams;

VirtualCrossConnectsCoverageListPage page = client.virtualCrossConnectsCoverage().list();
```

## 列出所有全局 IP 地址

列出所有全局 IP 地址。

`GET /global_ips`

```java
import com.telnyx.sdk.models.globalips.GlobalIpListPage;
import com.telnyx.sdk.models.globalips.GlobalIpListParams;

GlobalIpListPage page = client.globalIps().list();
```

## 创建全局 IP 地址

创建一个新的全局 IP 地址。

`POST /global_ips`

```java
import com.telnyx.sdk.models.globalips.GlobalIpCreateParams;
import com.telnyx.sdk.models.globalips.GlobalIpCreateResponse;

GlobalIpCreateResponse globalIp = client.globalIps().create();
```

## 获取全局 IP 地址信息

获取全局 IP 地址的详细信息。

`GET /global_ips/{id}`

```java
import com.telnyx.sdk.models.globalips.GlobalIpRetrieveParams;
import com.telnyx.sdk.models.globalips.GlobalIpRetrieveResponse;

GlobalIpRetrieveResponse globalIp = client.globalIps().retrieve("6a09cdc3-8948-47f0-aa62-74ac943d6c58");
```

## 删除全局 IP 地址

删除全局 IP 地址。

`DELETE /global_ips/{id}`

```java
import com.telnyx.sdk.models.globalips.GlobalIpDeleteParams;
import com.telnyx.sdk.models.globalips.GlobalIpDeleteResponse;

GlobalIpDeleteResponse globalIp = client.globalIps().delete("6a09cdc3-8948-47f0-aa62-74ac943d6c58");
```

## 列出所有允许使用的全球 IP 端口

列出所有允许使用的全球 IP 端口。

`GET /global_ip_allowed_ports`

```java
import com.telnyx.sdk.models.globalipallowedports.GlobalIpAllowedPortListParams;
import com.telnyx.sdk.models.globalipallowedports.GlobalIpAllowedPortListResponse;

GlobalIpAllowedPortListResponse globalIpAllowedPorts = client.globalIpAllowedPorts().list();
```

## 全局 IP 地址分配的健康检查指标

获取全局 IP 地址分配的健康检查指标。

`GET /global_ip_assignment_health`

```java
import com.telnyx.sdk.models.globalipassignmenthealth.GlobalIpAssignmentHealthRetrieveParams;
import com.telnyx.sdk.models.globalipassignmenthealth.GlobalIpAssignmentHealthRetrieveResponse;

GlobalIpAssignmentHealthRetrieveResponse globalIpAssignmentHealth = client.globalIpAssignmentHealth().retrieve();
```

## 列出所有全局 IP 地址分配记录

列出所有全局 IP 地址的分配记录。

`GET /global_ip_assignments`

```java
import com.telnyx.sdk.models.globalipassignments.GlobalIpAssignmentListPage;
import com.telnyx.sdk.models.globalipassignments.GlobalIpAssignmentListParams;

GlobalIpAssignmentListPage page = client.globalIpAssignments().list();
```

## 创建全局 IP 地址分配记录

创建一个新的全局 IP 地址分配记录。

`POST /global_ip_assignments`

```java
import com.telnyx.sdk.models.globalipassignments.GlobalIpAssignment;
import com.telnyx.sdk.models.globalipassignments.GlobalIpAssignmentCreateParams;
import com.telnyx.sdk.models.globalipassignments.GlobalIpAssignmentCreateResponse;

GlobalIpAssignment params = GlobalIpAssignment.builder().build();
GlobalIpAssignmentCreateResponse globalIpAssignment = client.globalIpAssignments().create(params);
```

## 获取全局 IP 地址分配记录

获取全局 IP 地址分配的详细信息。

`GET /global_ip_assignments/{id}`

```java
import com.telnyx.sdk.models.globalipassignments.GlobalIpAssignmentRetrieveParams;
import com.telnyx.sdk.models.globalipassignments.GlobalIpAssignmentRetrieveResponse;

GlobalIpAssignmentRetrieveResponse globalIpAssignment = client.globalIpAssignments().retrieve("6a09cdc3-8948-47f0-aa62-74ac943d6c58");
```

## 更新全局 IP 地址分配记录

更新全局 IP 地址分配记录。

`PATCH /global_ip_assignments/{id}`

```java
import com.telnyx.sdk.models.globalipassignments.GlobalIpAssignmentUpdateParams;
import com.telnyx.sdk.models.globalipassignments.GlobalIpAssignmentUpdateResponse;

GlobalIpAssignmentUpdateResponse globalIpAssignment = client.globalIpAssignments().update("6a09cdc3-8948-47f0-aa62-74ac943d6c58");
```

## 删除全局 IP 地址分配记录

删除全局 IP 地址分配记录。

`DELETE /global_ip_assignments/{id}`

```java
import com.telnyx.sdk.models.globalipassignments.GlobalIpAssignmentDeleteParams;
import com.telnyx.sdk.models.globalipassignments.GlobalIpAssignmentDeleteResponse;

GlobalIpAssignmentDeleteResponse globalIpAssignment = client.globalIpAssignments().delete("6a09cdc3-8948-47f0-aa62-74ac943d6c58");
```

## 全局 IP 地址分配的使用情况指标

获取全局 IP 地址分配的使用情况指标。

`GET /global_ip_assignments/usage`

```java
import com.telnyx.sdk.models.globalipassignmentsusage.GlobalIpAssignmentsUsageRetrieveParams;
import com.telnyx.sdk.models.globalipassignmentsusage.GlobalIpAssignmentsUsageRetrieveResponse;

GlobalIpAssignmentsUsageRetrieveResponse globalIpAssignmentsUsage = client.globalIpAssignmentsUsage().retrieve();
```

## 列出所有全局 IP 地址的健康检查类型

列出所有全局 IP 地址的健康检查类型。

`GET /global_ip_health_check_types`

```java
import com.telnyx.sdk.models.globaliphealthchecktypes.GlobalIpHealthCheckTypeListParams;
import com.telnyx.sdk.models.globaliphealthchecktypes.GlobalIpHealthCheckTypeListResponse;

GlobalIpHealthCheckTypeListResponse globalIpHealthCheckTypes = client.globalIpHealthCheckTypes().list();
```

## 查看所有全局 IP 地址的健康检查记录

列出所有全局 IP 地址的健康检查记录。

`GET /global_ip_health_checks`

```java
import com.telnyx.sdk.models.globaliphealthchecks.GlobalIpHealthCheckListPage;
import com.telnyx.sdk.models.globaliphealthchecks.GlobalIpHealthCheckListParams;

GlobalIpHealthCheckListPage page = client.globalIpHealthChecks().list();
```

## 创建全局 IP 地址的健康检查

创建一个新的全局 IP 地址健康检查。

`POST /global_ip_health_checks`

```java
import com.telnyx.sdk.models.globaliphealthchecks.GlobalIpHealthCheckCreateParams;
import com.telnyx.sdk.models.globaliphealthchecks.GlobalIpHealthCheckCreateResponse;

GlobalIpHealthCheckCreateResponse globalIpHealthCheck = client.globalIpHealthChecks().create();
```

## 获取全局 IP 地址的健康检查记录

获取全局 IP 地址的健康检查记录的详细信息。

`GET /global_ip_health_checks/{id}`

```java
import com.telnyx.sdk.models.globaliphealthchecks.GlobalIpHealthCheckRetrieveParams;
import com.telnyx.sdk.models.globaliphealthchecks.GlobalIpHealthCheckRetrieveResponse;

GlobalIpHealthCheckRetrieveResponse globalIpHealthCheck = client.globalIpHealthChecks().retrieve("6a09cdc3-8948-47f0-aa62-74ac943d6c58");
```

## 删除全局 IP 地址的健康检查记录

删除全局 IP 地址的健康检查记录。

`DELETE /global_ip_health_checks/{id}`

```java
import com.telnyx.sdk.models.globaliphealthchecks.GlobalIpHealthCheckDeleteParams;
import com.telnyx.sdk.models.globaliphealthchecks.GlobalIpHealthCheckDeleteResponse;

GlobalIpHealthCheckDeleteResponse globalIpHealthCheck = client.globalIpHealthChecks().delete("6a09cdc3-8948-47f0-aa62-74ac943d6c58");
```

## 全局 IP 地址的延迟指标

获取全局 IP 地址的延迟指标。

`GET /global_ip_latency`

```java
import com.telnyx.sdk.models.globaliplatency.GlobalIpLatencyRetrieveParams;
import com.telnyx.sdk.models.globaliplatency.GlobalIpLatencyRetrieveResponse;

GlobalIpLatencyRetrieveResponse globalIpLatency = client.globalIpLatency().retrieve();
```

## 列出所有全局 IP 协议

列出所有全局 IP 协议。

`GET /global_ip_protocols`

```java
import com.telnyx.sdk.models.globalipprotocols.GlobalIpProtocolListParams;
import com.telnyx.sdk.models.globalipprotocols.GlobalIpProtocolListResponse;

GlobalIpProtocolListResponse globalIpProtocols = client.globalIpProtocols().list();
```

## 全局 IP 地址的使用情况指标

获取全局 IP 地址的使用情况指标。

`GET /global_ip_usage`

```java
import com.telnyx.sdk.models.globalipusage.GlobalIpUsageRetrieveParams;
import com.telnyx.sdk.models.globalipusage.GlobalIpUsageRetrieveResponse;

GlobalIpUsageRetrieveResponse globalIpUsage = client.globalIpUsage().retrieve();
```