---
name: telnyx-webrtc-go
description: >-
  Manage WebRTC credentials and mobile push notification settings. Use when
  building browser-based or mobile softphone applications. This skill provides
  Go SDK examples.
metadata:
  author: telnyx
  product: webrtc
  language: go
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿修改。 -->

# Telnyx Webrtc - Go

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

## 列出移动推送凭据

`GET /mobile_push_credentials`

```go
	page, err := client.MobilePushCredentials.List(context.TODO(), telnyx.MobilePushCredentialListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建新的移动推送凭据

`POST /mobile_push_credentials`

```go
	pushCredentialResponse, err := client.MobilePushCredentials.New(context.TODO(), telnyx.MobilePushCredentialNewParams{
		OfIos: &telnyx.MobilePushCredentialNewParamsCreateMobilePushCredentialRequestIos{
			Alias:       "LucyIosCredential",
			Certificate: "-----BEGIN CERTIFICATE----- MIIGVDCCBTKCAQEAsNlRJVZn9ZvXcECQm65czs... -----END CERTIFICATE-----",
			PrivateKey:  "-----BEGIN RSA PRIVATE KEY----- MIIEpQIBAAKCAQEAsNlRJVZn9ZvXcECQm65czs... -----END RSA PRIVATE KEY-----",
		},
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", pushCredentialResponse.Data)
```

## 获取移动推送凭据

根据给定的 `push_credential_id` 获取移动推送凭据

`GET /mobile_push_credentials/{push_credential_id}`

```go
	pushCredentialResponse, err := client.MobilePushCredentials.Get(context.TODO(), "0ccc7b76-4df3-4bca-a05a-3da1ecc389f0")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", pushCredentialResponse.Data)
```

## 删除移动推送凭据

根据给定的 `push_credential_id` 删除移动推送凭据

`DELETE /mobile_push_credentials/{push_credential_id}`

```go
	err := client.MobilePushCredentials.Delete(context.TODO(), "0ccc7b76-4df3-4bca-a05a-3da1ecc389f0")
	if err != nil {
		panic(err.Error())
	}
```

## 列出所有凭据

列出所有的按需生成的凭据。

`GET /telephony_credentials`

```go
	page, err := client.TelephonyCredentials.List(context.TODO(), telnyx.TelephonyCredentialListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建凭据

创建一个新的凭据。

`POST /telephony_credentials` — 必需参数：`connection_id`

```go
	telephonyCredential, err := client.TelephonyCredentials.New(context.TODO(), telnyx.TelephonyCredentialNewParams{
		ConnectionID: "1234567890",
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", telephonyCredential.Data)
```

## 获取凭据详情

获取现有按需生成凭据的详细信息。

`GET /telephony_credentials/{id}`

```go
	telephonyCredential, err := client.TelephonyCredentials.Get(context.TODO(), "id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", telephonyCredential.Data)
```

## 更新凭据

更新现有的凭据。

`PATCH /telephony_credentials/{id}`

```go
	telephonyCredential, err := client.TelephonyCredentials.Update(
		context.TODO(),
		"id",
		telnyx.TelephonyCredentialUpdateParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", telephonyCredential.Data)
```

## 删除凭据

删除现有的凭据。

`DELETE /telephony_credentials/{id}`

```go
	telephonyCredential, err := client.TelephonyCredentials.Delete(context.TODO(), "id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", telephonyCredential.Data)
```

## 创建访问令牌

为该凭据创建一个访问令牌（JWT）。

`POST /telephony_credentials/{id}/token`

```go
	response, err := client.TelephonyCredentials.NewToken(context.TODO(), "id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response)
```