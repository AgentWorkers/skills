---
name: telnyx-numbers-services-go
description: >-
  Configure voicemail, voice channels, and emergency (E911) services for your
  phone numbers. This skill provides Go SDK examples.
metadata:
  author: telnyx
  product: numbers-services
  language: go
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 数字服务 - Go

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

## 列出动态紧急地址

根据筛选条件返回动态紧急地址

`GET /dynamic_emergency_addresses`

```go
	page, err := client.DynamicEmergencyAddresses.List(context.TODO(), telnyx.DynamicEmergencyAddressListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建动态紧急地址

创建一个动态紧急地址。

`POST /dynamic_emergency_addresses` — 必需参数：`house_number`、`street_name`、`locality`、`administrative_area`、`postal_code`、`country_code`

```go
	dynamicEmergencyAddress, err := client.DynamicEmergencyAddresses.New(context.TODO(), telnyx.DynamicEmergencyAddressNewParams{
		DynamicEmergencyAddress: telnyx.DynamicEmergencyAddressParam{
			AdministrativeArea: "TX",
			CountryCode:        telnyx.DynamicEmergencyAddressCountryCodeUs,
			HouseNumber:        "600",
			Locality:           "Austin",
			PostalCode:         "78701",
			StreetName:         "Congress",
		},
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", dynamicEmergencyAddress.Data)
```

## 获取动态紧急地址

根据提供的 ID 返回动态紧急地址

`GET /dynamic_emergency_addresses/{id}`

```go
	dynamicEmergencyAddress, err := client.DynamicEmergencyAddresses.Get(context.TODO(), "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", dynamicEmergencyAddress.Data)
```

## 删除动态紧急地址

根据提供的 ID 删除动态紧急地址

`DELETE /dynamic_emergency_addresses/{id}`

```go
	dynamicEmergencyAddress, err := client.DynamicEmergencyAddresses.Delete(context.TODO(), "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", dynamicEmergencyAddress.Data)
```

## 列出动态紧急终端点

根据筛选条件返回动态紧急终端点

`GET /dynamic_emergency_endpoints`

```go
	page, err := client.DynamicEmergencyEndpoints.List(context.TODO(), telnyx.DynamicEmergencyEndpointListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建动态紧急终端点

创建一个动态紧急终端点。

`POST /dynamic_emergency_endpoints` — 必需参数：`dynamic_emergency_address_id`、`callback_number`、`caller_name`

```go
	dynamicEmergencyEndpoint, err := client.DynamicEmergencyEndpoints.New(context.TODO(), telnyx.DynamicEmergencyEndpointNewParams{
		DynamicEmergencyEndpoint: telnyx.DynamicEmergencyEndpointParam{
			CallbackNumber:            "+13125550000",
			CallerName:                "Jane Doe Desk Phone",
			DynamicEmergencyAddressID: "0ccc7b54-4df3-4bca-a65a-3da1ecc777f0",
		},
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", dynamicEmergencyEndpoint.Data)
```

## 获取动态紧急终端点

根据提供的 ID 返回动态紧急终端点

`GET /dynamic_emergency_endpoints/{id}`

```go
	dynamicEmergencyEndpoint, err := client.DynamicEmergencyEndpoints.Get(context.TODO(), "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", dynamicEmergencyEndpoint.Data)
```

## 删除动态紧急终端点

根据提供的 ID 删除动态紧急终端点

`DELETE /dynamic_emergency_endpoints/{id}`

```go
	dynamicEmergencyEndpoint, err := client.DynamicEmergencyEndpoints.Delete(context.TODO(), "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", dynamicEmergencyEndpoint.Data)
```

## 列出非美国区域的语音通道

返回您账户中的非美国区域语音通道。

`GET /channel_zones`

```go
	page, err := client.ChannelZones.List(context.TODO(), telnyx.ChannelZoneListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 更新非美国区域的语音通道

更新非美国区域的语音通道数量。

`PUT /channel_zones/{channel_zone_id}` — 必需参数：`channels`

```go
	channelZone, err := client.ChannelZones.Update(
		context.TODO(),
		"channel_zone_id",
		telnyx.ChannelZoneUpdateParams{
			Channels: 0,
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", channelZone.ID)
```

## 列出美国区域的语音通道

返回您账户中的美国区域语音通道。

`GET /inbound_channels`

```go
	inboundChannels, err := client.InboundChannels.List(context.TODO())
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", inboundChannels.Data)
```

## 更新美国区域的语音通道

更新美国区域的语音通道数量。

`PATCH /inbound_channels` — 必需参数：`channels`

```go
	inboundChannel, err := client.InboundChannels.Update(context.TODO(), telnyx.InboundChannelUpdateParams{
		Channels: 7,
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", inboundChannel.Data)
```

## 列出使用通道计费的电话号码

检索按区域分组的所有使用通道计费的电话号码列表。

`GET /list`

```go
	response, err := client.List.GetAll(context.TODO())
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 列出特定区域的使用通道计费的电话号码

检索特定区域使用通道计费的电话号码列表。

`GET /list/{channel_zone_id}`

```go
	response, err := client.List.GetByZone(context.TODO(), "channel_zone_id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 获取语音信箱

返回电话号码的语音信箱设置

`GET /phone_numbers/{phone_number_id}/voicemail`

```go
	voicemail, err := client.PhoneNumbers.Voicemail.Get(context.TODO(), "123455678900")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", voicemail.Data)
```

## 创建语音信箱

为电话号码创建语音信箱设置

`POST /phone_numbers/{phone_number_id}/voicemail`

```go
	voicemail, err := client.PhoneNumbers.Voicemail.New(
		context.TODO(),
		"123455678900",
		telnyx.PhoneNumberVoicemailNewParams{
			VoicemailRequest: telnyx.VoicemailRequestParam{},
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", voicemail.Data)
```

## 更新语音信箱

更新电话号码的语音信箱设置

`PATCH /phone_numbers/{phone_number_id}/voicemail`

```go
	voicemail, err := client.PhoneNumbers.Voicemail.Update(
		context.TODO(),
		"123455678900",
		telnyx.PhoneNumberVoicemailUpdateParams{
			VoicemailRequest: telnyx.VoicemailRequestParam{},
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", voicemail.Data)
```
```