---
name: telnyx-sip-go
description: >-
  Configure SIP trunking connections and outbound voice profiles. Use when
  connecting PBX systems or managing SIP infrastructure. This skill provides Go
  SDK examples.
metadata:
  author: telnyx
  product: sip
  language: go
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx Sip - Go

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

## 获取所有出站语音配置文件

获取符合指定筛选条件的用户的所有出站语音配置文件。

`GET /outbound_voice_profiles`

```go
	page, err := client.OutboundVoiceProfiles.List(context.TODO(), telnyx.OutboundVoiceProfileListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建出站语音配置文件

创建一个新的出站语音配置文件。

`POST /outbound_voice_profiles` — 必需参数：`name`

```go
	outboundVoiceProfile, err := client.OutboundVoiceProfiles.New(context.TODO(), telnyx.OutboundVoiceProfileNewParams{
		Name: "office",
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", outboundVoiceProfile.Data)
```

## 查询出站语音配置文件

查询现有出站语音配置文件的详细信息。

`GET /outbound_voice_profiles/{id}`

```go
	outboundVoiceProfile, err := client.OutboundVoiceProfiles.Get(context.TODO(), "1293384261075731499")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", outboundVoiceProfile.Data)
```

## 更新出站语音配置文件

更新现有出站语音配置文件的详细信息。

`PATCH /outbound_voice_profiles/{id}` — 必需参数：`name`

```go
	outboundVoiceProfile, err := client.OutboundVoiceProfiles.Update(
		context.TODO(),
		"1293384261075731499",
		telnyx.OutboundVoiceProfileUpdateParams{
			Name: "office",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", outboundVoiceProfile.Data)
```

## 删除出站语音配置文件

删除现有的出站语音配置文件。

`DELETE /outbound_voice_profiles/{id}`

```go
	outboundVoiceProfile, err := client.OutboundVoiceProfiles.Delete(context.TODO(), "1293384261075731499")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", outboundVoiceProfile.Data)
```

## 列出所有连接

返回所有类型的连接列表。

`GET /connections`

```go
	page, err := client.Connections.List(context.TODO(), telnyx.ConnectionListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 查询连接信息

获取现有连接的详细信息。

`GET /connections/{id}`

```go
	connection, err := client.Connections.Get(context.TODO(), "id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", connection.Data)
```

## 列出凭证连接

返回所有凭证连接的列表。

`GET /credential_connections`

```go
	page, err := client.CredentialConnections.List(context.TODO(), telnyx.CredentialConnectionListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建凭证连接

创建一个新的凭证连接。

`POST /credential_connections` — 必需参数：`user_name`, `password`, `connection_name`

```go
	credentialConnection, err := client.CredentialConnections.New(context.TODO(), telnyx.CredentialConnectionNewParams{
		ConnectionName: "my name",
		Password:       "my123secure456password789",
		UserName:       "myusername123",
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", credentialConnection.Data)
```

## 查询凭证连接信息

获取现有凭证连接的详细信息。

`GET /credential_connections/{id}`

```go
	credentialConnection, err := client.CredentialConnections.Get(context.TODO(), "id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", credentialConnection.Data)
```

## 更新凭证连接信息

更新现有凭证连接的设置。

`PATCH /credential_connections/{id}`

```go
	credentialConnection, err := client.CredentialConnections.Update(
		context.TODO(),
		"id",
		telnyx.CredentialConnectionUpdateParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", credentialConnection.Data)
```

## 删除凭证连接

删除现有的凭证连接。

`DELETE /credential_connections/{id}`

```go
	credentialConnection, err := client.CredentialConnections.Delete(context.TODO(), "id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", credentialConnection.Data)
```

## 检查凭证连接的注册状态

检查凭证连接的注册状态（`registration_status`）以及最后一次 SIP 注册事件的时间戳（`registration_status_updated_at`）。

`POST /credential_connections/{id}/actions/check_registration_status`

```go
	response, err := client.CredentialConnections.Actions.CheckRegistrationStatus(context.TODO(), "id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 列出 IP 地址

获取符合指定筛选条件的用户的所有 IP 地址。

`GET /ips`

```go
	page, err := client.IPs.List(context.TODO(), telnyx.IPListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建 IP 地址

创建一个新的 IP 对象。

`POST /ips` — 必需参数：`ip_address`

```go
	ip, err := client.IPs.New(context.TODO(), telnyx.IPNewParams{
		IPAddress: "192.168.0.0",
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", ip.Data)
```

## 查询 IP 地址信息

获取特定 IP 地址的详细信息。

`GET /ips/{id}`

```go
	ip, err := client.IPs.Get(context.TODO(), "6a09cdc3-8948-47f0-aa62-74ac943d6c58")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", ip.Data)
```

## 更新 IP 地址信息

更新特定 IP 地址的详细信息。

`PATCH /ips/{id}` — 必需参数：`ip_address`

```go
	ip, err := client.IPs.Update(
		context.TODO(),
		"6a09cdc3-8948-47f0-aa62-74ac943d6c58",
		telnyx.IPUpdateParams{
			IPAddress: "192.168.0.0",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", ip.Data)
```

## 删除 IP 地址

删除指定的 IP 地址。

`DELETE /ips/{id}`

```go
	ip, err := client.IPs.Delete(context.TODO(), "6a09cdc3-8948-47f0-aa62-74ac943d6c58")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", ip.Data)
```

## 列出 IP 连接

返回所有 IP 连接的列表。

`GET /ip_connections`

```go
	page, err := client.IPConnections.List(context.TODO(), telnyx.IPConnectionListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建 IP 连接

创建一个新的 IP 连接。

`POST /ip_connections`

```go
	ipConnection, err := client.IPConnections.New(context.TODO(), telnyx.IPConnectionNewParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", ipConnection.Data)
```

## 查询 IP 连接信息

获取现有 IP 连接的详细信息。

`GET /ip_connections/{id}`

```go
	ipConnection, err := client.IPConnections.Get(context.TODO(), "id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", ipConnection.Data)
```

## 更新 IP 连接信息

更新现有 IP 连接的设置。

`PATCH /ip_connections/{id}`

```go
	ipConnection, err := client.IPConnections.Update(
		context.TODO(),
		"id",
		telnyx.IPConnectionUpdateParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", ipConnection.Data)
```

## 删除 IP 连接

删除现有的 IP 连接。

`DELETE /ip_connections/{id}`

```go
	ipConnection, err := client.IPConnections.Delete(context.TODO(), "id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", ipConnection.Data)
```

## 列出 FQDN（完全 Qualified Domain Name）

获取符合指定筛选条件的用户的所有 FQDN。

`GET /fqdns`

```go
	page, err := client.Fqdns.List(context.TODO(), telnyx.FqdnListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建 FQDN

创建一个新的 FQDN 对象。

`POST /fqdns` — 必需参数：`fqdn`, `dns_record_type`, `connection_id`

```go
	fqdn, err := client.Fqdns.New(context.TODO(), telnyx.FqdnNewParams{
		ConnectionID:  "1516447646313612565",
		DNSRecordType: "a",
		Fqdn:          "example.com",
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", fqdn.Data)
```

## 查询 FQDN 信息

获取特定 FQDN 的详细信息。

`GET /fqdns/{id}`

```go
	fqdn, err := client.Fqdns.Get(context.TODO(), "id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", fqdn.Data)
```

## 更新 FQDN 信息

更新特定 FQDN 的详细信息。

`PATCH /fqdns/{id}`

```go
	fqdn, err := client.Fqdns.Update(
		context.TODO(),
		"id",
		telnyx.FqdnUpdateParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", fqdn.Data)
```

## 删除 FQDN

删除指定的 FQDN。

`DELETE /fqdns/{id}`

```go
	fqdn, err := client.Fqdns.Delete(context.TODO(), "id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", fqdn.Data)
```

## 列出 FQDN 连接

返回所有 FQDN 连接的列表。

`GET /fqdn_connections`

```go
	page, err := client.FqdnConnections.List(context.TODO(), telnyx.FqdnConnectionListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建 FQDN 连接

创建一个新的 FQDN 连接。

`POST /fqdn_connections` — 必需参数：`connection_name`

```go
	fqdnConnection, err := client.FqdnConnections.New(context.TODO(), telnyx.FqdnConnectionNewParams{
		ConnectionName: "string",
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", fqdnConnection.Data)
```

## 查询 FQDN 连接信息

获取现有 FQDN 连接的详细信息。

`GET /fqdn_connections/{id}`

```go
	fqdnConnection, err := client.FqdnConnections.Get(context.TODO(), "id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", fqdnConnection.Data)
```

## 更新 FQDN 连接信息

更新现有 FQDN 连接的设置。

`PATCH /fqdn_connections/{id}`

```go
	fqdnConnection, err := client.FqdnConnections.Update(
		context.TODO(),
		"id",
		telnyx.FqdnConnectionUpdateParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", fqdnConnection.Data)
```

## 删除 FQDN 连接

删除现有的 FQDN 连接。

`DELETE /fqdn_connections/{id}`

```go
	fqdnConnection, err := client.FqdnConnections.Delete(context.TODO(), "id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", fqdnConnection.Data)
```

## 列出移动语音连接

获取所有移动语音连接的列表。

`GET /v2/mobile_voice_connections`

```go
	page, err := client.MobileVoiceConnections.List(context.TODO(), telnyx.MobileVoiceConnectionListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建移动语音连接

创建一个新的移动语音连接。

`POST /v2/mobile_voice_connections`

```go
	mobileVoiceConnection, err := client.MobileVoiceConnections.New(context.TODO(), telnyx.MobileVoiceConnectionNewParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", mobileVoiceConnection.Data)
```

## 查询移动语音连接信息

获取特定移动语音连接的详细信息。

`GET /v2/mobile_voice_connections/{id}`

```go
	mobileVoiceConnection, err := client.MobileVoiceConnections.Get(context.TODO(), "id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", mobileVoiceConnection.Data)
```

## 更新移动语音连接信息

更新现有移动语音连接的设置。

`PATCH /v2/mobile_voice_connections/{id}`

```go
	mobileVoiceConnection, err := client.MobileVoiceConnections.Update(
		context.TODO(),
		"id",
		telnyx.MobileVoiceConnectionUpdateParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", mobileVoiceConnection.Data)
```

## 删除移动语音连接

删除现有的移动语音连接。

`DELETE /v2/mobile_voice_connections/{id}`

```go
	mobileVoiceConnection, err := client.MobileVoiceConnections.Delete(context.TODO(), "id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", mobileVoiceConnection.Data)
```
```