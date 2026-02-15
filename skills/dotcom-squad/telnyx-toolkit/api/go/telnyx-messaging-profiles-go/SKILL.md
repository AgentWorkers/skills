---
name: telnyx-messaging-profiles-go
description: >-
  Create and manage messaging profiles with number pools, sticky sender, and
  geomatch features. Configure short codes for high-volume messaging. This skill
  provides Go SDK examples.
metadata:
  author: telnyx
  product: messaging-profiles
  language: go
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 消息传递配置文件 - Go 语言实现

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

## 列出消息传递配置文件

`GET /messaging_profiles`

```go
	page, err := client.MessagingProfiles.List(context.TODO(), telnyx.MessagingProfileListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建消息传递配置文件

`POST /messagingprofiles` — 必需参数：`name`、`whitelisted_destinations`

```go
	messagingProfile, err := client.MessagingProfiles.New(context.TODO(), telnyx.MessagingProfileNewParams{
		Name:                    "My name",
		WhitelistedDestinations: []string{"US"},
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", messagingProfile.Data)
```

## 获取消息传递配置文件

`GET /messagingprofiles/{id}`

```go
	messagingProfile, err := client.MessagingProfiles.Get(context.TODO(), "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", messagingProfile.Data)
```

## 更新消息传递配置文件

`PATCH /messagingprofiles/{id}`

```go
	messagingProfile, err := client.MessagingProfiles.Update(
		context.TODO(),
		"182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		telnyx.MessagingProfileUpdateParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", messagingProfile.Data)
```

## 删除消息传递配置文件

`DELETE /messagingprofiles/{id}`

```go
	messagingProfile, err := client.MessagingProfiles.Delete(context.TODO(), "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", messagingProfile.Data)
```

## 获取与消息传递配置文件关联的电话号码

`GET /messagingprofiles/{id}/phone_numbers`

```go
	page, err := client.MessagingProfiles.ListPhoneNumbers(
		context.TODO(),
		"182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		telnyx.MessagingProfileListPhoneNumbersParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 获取与消息传递配置文件关联的短代码

`GET /messagingprofiles/{id}/short_codes`

```go
	page, err := client.MessagingProfiles.ListShortCodes(
		context.TODO(),
		"182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		telnyx.MessagingProfileListShortCodesParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 查看自动应答设置

`GET /messagingprofiles/{profile_id}/autoresp_configs`

```go
	autorespConfigs, err := client.MessagingProfiles.AutorespConfigs.List(
		context.TODO(),
		"182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		telnyx.MessagingProfileAutorespConfigListParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", autorespConfigs.Data)
```

## 创建自动应答设置

`POST /messagingprofiles/{profile_id}/autoresp_configs` — 必需参数：`op`、`keywords`、`country_code`

```go
	autoRespConfigResponse, err := client.MessagingProfiles.AutorespConfigs.New(
		context.TODO(),
		"profile_id",
		telnyx.MessagingProfileAutorespConfigNewParams{
			AutoRespConfigCreate: telnyx.AutoRespConfigCreateParam{
				CountryCode: "US",
				Keywords:    []string{"keyword1", "keyword2"},
				Op:          telnyx.AutoRespConfigCreateOpStart,
			},
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", autoRespConfigResponse.Data)
```

## 获取自动应答设置

`GET /messagingprofiles/{profile_id}/autoresp_configs/{autoresp_cfg_id}`

```go
	autoRespConfigResponse, err := client.MessagingProfiles.AutorespConfigs.Get(
		context.TODO(),
		"182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		telnyx.MessagingProfileAutorespConfigGetParams{
			ProfileID: "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", autoRespConfigResponse.Data)
```

## 更新自动应答设置

`PUT /messagingprofiles/{profile_id}/autoresp_configs/{autoresp_cfg_id}` — 必需参数：`op`、`keywords`、`country_code`

```go
	autoRespConfigResponse, err := client.MessagingProfiles.AutorespConfigs.Update(
		context.TODO(),
		"182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		telnyx.MessagingProfileAutorespConfigUpdateParams{
			ProfileID: "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
			AutoRespConfigCreate: telnyx.AutoRespConfigCreateParam{
				CountryCode: "US",
				Keywords:    []string{"keyword1", "keyword2"},
				Op:          telnyx.AutoRespConfigCreateOpStart,
			},
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", autoRespConfigResponse.Data)
```

## 删除自动应答设置

`DELETE /messagingprofiles/{profile_id}/autoresp_configs/{autoresp_cfg_id}`

```go
	autorespConfig, err := client.MessagingProfiles.AutorespConfigs.Delete(
		context.TODO(),
		"182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		telnyx.MessagingProfileAutorespConfigDeleteParams{
			ProfileID: "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", autorespConfig)
```

## 列出所有短代码

`GET /short_codes`

```go
	page, err := client.ShortCodes.List(context.TODO(), telnyx.ShortCodeListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 获取特定短代码的信息

`GET /short_codes/{id}`

```go
	shortCode, err := client.ShortCodes.Get(context.TODO(), "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", shortCode.Data)
```

## 更新短代码的设置

`PATCH /short_codes/{id}` — 必需参数：`messaging_profile_id`

```go
	shortCode, err := client.ShortCodes.Update(
		context.TODO(),
		"182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		telnyx.ShortCodeUpdateParams{
			MessagingProfileID: "abc85f64-5717-4562-b3fc-2c9600000000",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", shortCode.Data)
```