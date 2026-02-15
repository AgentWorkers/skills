---
name: telnyx-networking-go
description: >-
  Configure private networks, WireGuard VPN gateways, internet gateways, and
  virtual cross connects. This skill provides Go SDK examples.
metadata:
  author: telnyx
  product: networking
  language: go
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 网络服务 - Go 语言接口

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

## 列出所有区域

列出所有区域及其支持的接口：

`GET /regions`

```go
	regions, err := client.Regions.List(context.TODO())
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", regions.Data)
```

## 列出所有网络

列出所有网络：

`GET /networks`

```go
	page, err := client.Networks.List(context.TODO(), telnyx.NetworkListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建网络

创建一个新的网络：

`POST /networks`

```go
	network, err := client.Networks.New(context.TODO(), telnyx.NetworkNewParams{
		NetworkCreate: telnyx.NetworkCreateParam{
			RecordParam: telnyx.RecordParam{},
			Name:        "test network",
		},
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", network.Data)
```

## 查取网络信息

获取网络信息：

`GET /networks/{id}`

```go
	network, err := client.Networks.Get(context.TODO(), "6a09cdc3-8948-47f0-aa62-74ac943d6c58")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", network.Data)
```

## 更新网络信息

更新网络信息：

`PATCH /networks/{id}`

```go
	network, err := client.Networks.Update(
		context.TODO(),
		"6a09cdc3-8948-47f0-aa62-74ac943d6c58",
		telnyx.NetworkUpdateParams{
			NetworkCreate: telnyx.NetworkCreateParam{
				RecordParam: telnyx.RecordParam{},
				Name:        "test network",
			},
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", network.Data)
```

## 删除网络

删除网络：

`DELETE /networks/{id}`

```go
	network, err := client.Networks.Delete(context.TODO(), "6a09cdc3-8948-47f0-aa62-74ac943d6c58")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", network.Data)
```

## 获取默认网关状态

`GET /networks/{id}/default_gateway`

```go
	defaultGateway, err := client.Networks.DefaultGateway.Get(context.TODO(), "6a09cdc3-8948-47f0-aa62-74ac943d6c58")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", defaultGateway.Data)
```

## 创建默认网关

创建默认网关：

`POST /networks/{id}/default_gateway`

```go
	defaultGateway, err := client.Networks.DefaultGateway.New(
		context.TODO(),
		"6a09cdc3-8948-47f0-aa62-74ac943d6c58",
		telnyx.NetworkDefaultGatewayNewParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", defaultGateway.Data)
```

## 删除默认网关

删除默认网关：

`DELETE /networks/{id}/default_gateway`

```go
	defaultGateway, err := client.Networks.DefaultGateway.Delete(context.TODO(), "6a09cdc3-8948-47f0-aa62-74ac943d6c58")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", defaultGateway.Data)
```

## 列出网络的所有接口

`GET /networks/{id}/networkInterfaces`

```go
	page, err := client.Networks.ListInterfaces(
		context.TODO(),
		"6a09cdc3-8948-47f0-aa62-74ac943d6c58",
		telnyx.NetworkListInterfacesParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 列出所有 WireGuard 接口

列出所有 WireGuard 接口：

`GET /wireguard_interfaces`

```go
	page, err := client.WireguardInterfaces.List(context.TODO(), telnyx.WireguardInterfaceListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建新的 WireGuard 接口

创建一个新的 WireGuard 接口：

`POST /wireguardInterfaces`

```go
	wireguardInterface, err := client.WireguardInterfaces.New(context.TODO(), telnyx.WireguardInterfaceNewParams{
		RegionCode: "ashburn-va",
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", wireguardInterface.Data)
```

## 查取 WireGuard 接口信息

获取 WireGuard 接口信息：

`GET /wireguardinterfaces/{id}`

```go
	wireguardInterface, err := client.WireguardInterfaces.Get(context.TODO(), "6a09cdc3-8948-47f0-aa62-74ac943d6c58")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", wireguardInterface.Data)
```

## 删除 WireGuard 接口

删除 WireGuard 接口：

`DELETE /wireguardinterfaces/{id}`

```go
	wireguardInterface, err := client.WireguardInterfaces.Delete(context.TODO(), "6a09cdc3-8948-47f0-aa62-74ac943d6c58")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", wireguardInterface.Data)
```

## 列出所有 WireGuard 对等体

列出所有 WireGuard 对等体：

`GET /wireguard_peers`

```go
	page, err := client.WireguardPeers.List(context.TODO(), telnyx.WireguardPeerListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建新的 WireGuard 对等体

创建一个新的 WireGuard 对等体：

`POST /wireguard_peers`

```go
	wireguardPeer, err := client.WireguardPeers.New(context.TODO(), telnyx.WireguardPeerNewParams{
		WireguardInterfaceID: "6a09cdc3-8948-47f0-aa62-74ac943d6c58",
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", wireguardPeer.Data)
```

## 查取 WireGuard 对等体信息

获取 WireGuard 对等体信息：

`GET /wireguard_peers/{id}`

```go
	wireguardPeer, err := client.WireguardPeers.Get(context.TODO(), "6a09cdc3-8948-47f0-aa62-74ac943d6c58")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", wireguardPeer.Data)
```

## 更新 WireGuard 对等体信息

更新 WireGuard 对等体信息：

`PATCH /wireguard_peers/{id}`

```go
	wireguardPeer, err := client.WireguardPeers.Update(
		context.TODO(),
		"6a09cdc3-8948-47f0-aa62-74ac943d6c58",
		telnyx.WireguardPeerUpdateParams{
			WireguardPeerPatch: telnyx.WireguardPeerPatchParam{},
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", wireguardPeer.Data)
```

## 删除 WireGuard 对等体

删除 WireGuard 对等体：

`DELETE /wireguard_peers/{id}`

```go
	wireguardPeer, err := client.WireguardPeers.Delete(context.TODO(), "6a09cdc3-8948-47f0-aa62-74ac943d6c58")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", wireguardPeer.Data)
```

## 获取 WireGuard 对等体的配置模板

`GET /wireguard_peers/{id}/config`

```go
	response, err := client.WireguardPeers.GetConfig(context.TODO(), "6a09cdc3-8948-47f0-aa62-74ac943d6c58")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response)
```

## 获取用户所有的私有无线网关

获取用户所有的私有无线网关：

`GET /private_wireless_gateways`

```go
	page, err := client.PrivateWirelessGateways.List(context.TODO(), telnyx.PrivateWirelessGatewayListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 为已创建的网络创建私有无线网关

异步地为已创建的网络创建私有无线网关：

`POST /private_wireless_gateways` — 必需参数：`network_id`、`name`

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

## 获取私有无线网关信息

获取私有无线网关的信息：

`GET /private_wireless_gateways/{id}`

```go
	privateWirelessGateway, err := client.PrivateWirelessGateways.Get(context.TODO(), "6a09cdc3-8948-47f0-aa62-74ac943d6c58")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", privateWirelessGateway.Data)
```

## 删除私有无线网关

删除私有无线网关：

`DELETE /private_wireless_gateways/{id}`

```go
	privateWirelessGateway, err := client.PrivateWirelessGateways.Delete(context.TODO(), "6a09cdc3-8948-47f0-aa62-74ac943d6c58")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", privateWirelessGateway.Data)
```

## 列出所有公共互联网网关

列出所有公共互联网网关：

`GET /public_internet_gateways`

```go
	page, err := client.PublicInternetGateways.List(context.TODO(), telnyx.PublicInternetGatewayListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建公共互联网网关

创建一个新的公共互联网网关：

`POST /public_internet_gateways`

```go
	publicInternetGateway, err := client.PublicInternetGateways.New(context.TODO(), telnyx.PublicInternetGatewayNewParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", publicInternetGateway.Data)
```

## 查取公共互联网网关信息

获取公共互联网网关的信息：

`GET /public_internet_gateways/{id}`

```go
	publicInternetGateway, err := client.PublicInternetGateways.Get(context.TODO(), "6a09cdc3-8948-47f0-aa62-74ac943d6c58")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", publicInternetGateway.Data)
```

## 删除公共互联网网关

删除公共互联网网关：

`DELETE /public_internet_gateways/{id}`

```go
	publicInternetGateway, err := client.PublicInternetGateways.Delete(context.TODO(), "6a09cdc3-8948-47f0-aa62-74ac943d6c58")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", publicInternetGateway.Data)
```

## 列出所有虚拟跨连接

列出所有虚拟跨连接：

`GET /virtual_cross_connects`

```go
	page, err := client.VirtualCrossConnects.List(context.TODO(), telnyx.VirtualCrossConnectListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建虚拟跨连接

创建一个新的虚拟跨连接。<br /><br />对于 AWS 和 GCE，您可以先创建主连接，再创建次级连接：

`POST /virtual_cross_connects`

```go
	virtualCrossConnect, err := client.VirtualCrossConnects.New(context.TODO(), telnyx.VirtualCrossConnectNewParams{
		RegionCode: "ashburn-va",
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", virtualCrossConnect.Data)
```

## 查取虚拟跨连接信息

获取虚拟跨连接的信息：

`GET /virtual_cross_connects/{id}`

```go
	virtualCrossConnect, err := client.VirtualCrossConnects.Get(context.TODO(), "6a09cdc3-8948-47f0-aa62-74ac943d6c58")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", virtualCrossConnect.Data)
```

## 更新虚拟跨连接信息

更新虚拟跨连接的信息。<br /><br />云 IP 只能在“创建”状态时进行修改，因为 GCE 会在待处理的连接请求完成之后才会通知您生成的 IP 地址...

`PATCH /virtual_cross_connects/{id}`

```go
	virtualCrossConnect, err := client.VirtualCrossConnects.Update(
		context.TODO(),
		"6a09cdc3-8948-47f0-aa62-74ac943d6c58",
		telnyx.VirtualCrossConnectUpdateParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", virtualCrossConnect.Data)
```

## 删除虚拟跨连接

删除虚拟跨连接：

`DELETE /virtual_cross_connects/{id}`

```go
	virtualCrossConnect, err := client.VirtualCrossConnects.Delete(context.TODO(), "6a09cdc3-8948-47f0-aa62-74ac943d6c58")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", virtualCrossConnect.Data)
```

## 查看虚拟跨连接的覆盖范围

查看虚拟跨连接的覆盖范围。<br /><br />此接口显示虚拟跨连接将被配置到的云区域：

`GET /virtual_cross_connects/coverage`

```go
	page, err := client.VirtualCrossConnectsCoverage.List(context.TODO(), telnyx.VirtualCrossConnectsCoverageListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 列出所有全局 IP 地址

列出所有全局 IP 地址：

`GET /global_ips`

```go
	page, err := client.GlobalIPs.List(context.TODO(), telnyx.GlobalIPListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建全局 IP 地址

创建一个新的全局 IP 地址：

`POST /global_ips`

```go
	globalIP, err := client.GlobalIPs.New(context.TODO(), telnyx.GlobalIPNewParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", globalIP.Data)
```

## 获取全局 IP 地址信息

获取全局 IP 地址的信息：

`GET /global_ips/{id}`

```go
	globalIP, err := client.GlobalIPs.Get(context.TODO(), "6a09cdc3-8948-47f0-aa62-74ac943d6c58")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", globalIP.Data)
```

## 删除全局 IP 地址

删除全局 IP 地址：

`DELETE /global_ips/{id}`

```go
	globalIP, err := client.GlobalIPs.Delete(context.TODO(), "6a09cdc3-8948-47f0-aa62-74ac943d6c58")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", globalIP.Data)
```

## 列出所有允许使用的全局 IP 地址端口

列出所有允许使用的全局 IP 地址端口：

`GET /global_ip_allowed_ports`

```go
	globalIPAllowedPorts, err := client.GlobalIPAllowedPorts.List(context.TODO())
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", globalIPAllowedPorts.Data)
```

## 全局 IP 地址分配的健康检查指标

获取全局 IP 地址分配的健康检查指标：

`GET /global_ip_assignment_health`

```go
	globalIPAssignmentHealth, err := client.GlobalIPAssignmentHealth.Get(context.TODO(), telnyx.GlobalIPAssignmentHealthGetParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", globalIPAssignmentHealth.Data)
```

## 列出所有全局 IP 地址分配记录

列出所有全局 IP 地址的分配记录：

`GET /global_ip_assignments`

```go
	page, err := client.GlobalIPAssignments.List(context.TODO(), telnyx.GlobalIPAssignmentListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建全局 IP 地址分配记录

创建一个新的全局 IP 地址分配记录：

`POST /global_ip_assignments`

```go
	globalIPAssignment, err := client.GlobalIPAssignments.New(context.TODO(), telnyx.GlobalIPAssignmentNewParams{
		GlobalIPAssignment: telnyx.GlobalIPAssignmentParam{},
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", globalIPAssignment.Data)
```

## 获取全局 IP 地址分配记录

获取全局 IP 地址的分配记录：

`GET /global_ip_assignments/{id}`

```go
	globalIPAssignment, err := client.GlobalIPAssignments.Get(context.TODO(), "6a09cdc3-8948-47f0-aa62-74ac943d6c58")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", globalIPAssignment.Data)
```

## 更新全局 IP 地址分配记录

更新全局 IP 地址的分配记录：

`PATCH /global_ip_assignments/{id}`

```go
	globalIPAssignment, err := client.GlobalIPAssignments.Update(
		context.TODO(),
		"6a09cdc3-8948-47f0-aa62-74ac943d6c58",
		telnyx.GlobalIPAssignmentUpdateParams{
			GlobalIPAssignmentUpdateRequest: telnyx.GlobalIPAssignmentUpdateParamsGlobalIPAssignmentUpdateRequest{
				GlobalIPAssignmentParam: telnyx.GlobalIPAssignmentParam{},
			},
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", globalIPAssignment.Data)
```

## 删除全局 IP 地址分配记录

删除全局 IP 地址的分配记录：

`DELETE /global_ip_assignments/{id}`

```go
	globalIPAssignment, err := client.GlobalIPAssignments.Delete(context.TODO(), "6a09cdc3-8948-47f0-aa62-74ac943d6c58")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", globalIPAssignment.Data)
```

## 全局 IP 地址分配的使用情况指标

获取全局 IP 地址分配的使用情况指标：

`GET /global_ip_assignments/usage`

```go
	globalIPAssignmentsUsage, err := client.GlobalIPAssignmentsUsage.Get(context.TODO(), telnyx.GlobalIPAssignmentsUsageGetParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", globalIPAssignmentsUsage.Data)
```

## 列出所有全局 IP 地址的健康检查类型

列出所有全局 IP 地址的健康检查类型：

`GET /global_ip_health_check_types`

```go
	globalIPHealthCheckTypes, err := client.GlobalIPHealthCheckTypes.List(context.TODO())
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", globalIPHealthCheckTypes.Data)
```

## 列出所有全局 IP 地址的健康检查记录

列出所有全局 IP 地址的健康检查记录：

`GET /global_ip_health_checks`

```go
	page, err := client.GlobalIPHealthChecks.List(context.TODO(), telnyx.GlobalIPHealthCheckListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建全局 IP 地址的健康检查记录

创建一个新的全局 IP 地址的健康检查记录：

`POST /global_ip_health_checks`

```go
	globalIPHealthCheck, err := client.GlobalIPHealthChecks.New(context.TODO(), telnyx.GlobalIPHealthCheckNewParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", globalIPHealthCheck.Data)
```

## 获取全局 IP 地址的健康检查记录

获取全局 IP 地址的健康检查记录：

`GET /global_ip_health_checks/{id}`

```go
	globalIPHealthCheck, err := client.GlobalIPHealthChecks.Get(context.TODO(), "6a09cdc3-8948-47f0-aa62-74ac943d6c58")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", globalIPHealthCheck.Data)
```

## 删除全局 IP 地址的健康检查记录

删除全局 IP 地址的健康检查记录：

`DELETE /global_ip_health_checks/{id}`

```go
	globalIPHealthCheck, err := client.GlobalIPHealthChecks.Delete(context.TODO(), "6a09cdc3-8948-47f0-aa62-74ac943d6c58")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", globalIPHealthCheck.Data)
```

## 全局 IP 地址的延迟指标

获取全局 IP 地址的延迟指标：

`GET /global_ip_latency`

```go
	globalIPLatency, err := client.GlobalIPLatency.Get(context.TODO(), telnyx.GlobalIPLatencyGetParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", globalIPLatency.Data)
```

## 列出所有全局 IP 协议

列出所有全局 IP 协议：

`GET /global_ip_protocols`

```go
	globalIPProtocols, err := client.GlobalIPProtocols.List(context.TODO())
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", globalIPProtocols.Data)
```

## 全局 IP 地址的使用情况指标

获取全局 IP 地址的使用情况指标：

`GET /global_ip_usage`

```go
	globalIPUsage, err := client.GlobalIPUsage.Get(context.TODO(), telnyx.GlobalIPUsageGetParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", globalIPUsage.Data)
```