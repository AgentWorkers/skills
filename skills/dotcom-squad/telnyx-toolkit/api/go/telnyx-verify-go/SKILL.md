---
name: telnyx-verify-go
description: >-
  Look up phone number information (carrier, type, caller name) and verify users
  via SMS/voice OTP. Use for phone verification and data enrichment. This skill
  provides Go SDK examples.
metadata:
  author: telnyx
  product: verify
  language: go
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx Verify - Go

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

以下所有示例均假设 `client` 已经按照上述方式初始化。

## 查找电话号码信息

返回有关提供的电话号码的信息。

`GET /number_lookup/{phone_number}`

```go
	numberLookup, err := client.NumberLookup.Get(
		context.TODO(),
		"+18665552368",
		telnyx.NumberLookupGetParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", numberLookup.Data)
```

## 触发电话验证

`POST /verifications/call` — 必需参数：`phone_number`、`verify_profile_id`

```go
	createVerificationResponse, err := client.Verifications.TriggerCall(context.TODO(), telnyx.VerificationTriggerCallParams{
		PhoneNumber:     "+13035551234",
		VerifyProfileID: "12ade33a-21c0-473b-b055-b3c836e1c292",
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", createVerificationResponse.Data)
```

## 触发闪现式电话验证

`POST /verifications/flashcall` — 必需参数：`phone_number`、`verify_profile_id`

```go
	createVerificationResponse, err := client.Verifications.TriggerFlashcall(context.TODO(), telnyx.VerificationTriggerFlashcallParams{
		PhoneNumber:     "+13035551234",
		VerifyProfileID: "12ade33a-21c0-473b-b055-b3c836e1c292",
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", createVerificationResponse.Data)
```

## 触发短信验证

`POST /verifications/sms` — 必需参数：`phone_number`、`verify_profile_id`

```go
	createVerificationResponse, err := client.Verifications.TriggerSMS(context.TODO(), telnyx.VerificationTriggerSMSParams{
		PhoneNumber:     "+13035551234",
		VerifyProfileID: "12ade33a-21c0-473b-b055-b3c836e1c292",
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", createVerificationResponse.Data)
```

## 获取验证结果

`GET /verifications/{verification_id}`

```go
	verification, err := client.Verifications.Get(context.TODO(), "12ade33a-21c0-473b-b055-b3c836e1c292")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", verification.Data)
```

## 通过 ID 验证验证码

`POST /verifications/{verification_id}/actions/verify`

```go
	verifyVerificationCodeResponse, err := client.Verifications.Actions.Verify(
		context.TODO(),
		"12ade33a-21c0-473b-b055-b3c836e1c292",
		telnyx.VerificationActionVerifyParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", verifyVerificationCodeResponse.Data)
```

## 按电话号码列出验证记录

`GET /verifications/by_phone_number/{phone_number}`

```go
	byPhoneNumbers, err := client.Verifications.ByPhoneNumber.List(context.TODO(), "+13035551234")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", byPhoneNumbers.Data)
```

## 通过电话号码验证验证码

`POST /verifications/by_phone_number/{phone_number}/actions/verify` — 必需参数：`code`、`verify_profile_id`

```go
	verifyVerificationCodeResponse, err := client.Verifications.ByPhoneNumber.Actions.Verify(
		context.TODO(),
		"+13035551234",
		telnyx.VerificationByPhoneNumberActionVerifyParams{
			Code:            "17686",
			VerifyProfileID: "12ade33a-21c0-473b-b055-b3c836e1c292",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", verifyVerificationCodeResponse.Data)
```

## 列出所有验证配置文件

获取分页显示的验证配置文件列表。

`GET /verify_profiles`

```go
	page, err := client.VerifyProfiles.List(context.TODO(), telnyx.VerifyProfileListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建验证配置文件

创建一个新的验证配置文件，用于关联验证操作。

`POST /verify_profiles` — 必需参数：`name`

```go
	verifyProfileData, err := client.VerifyProfiles.New(context.TODO(), telnyx.VerifyProfileNewParams{
		Name: "Test Profile",
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", verifyProfileData.Data)
```

## 获取验证配置文件信息

获取单个验证配置文件的信息。

`GET /verify_profiles/{verify_profile_id}`

```go
	verifyProfileData, err := client.VerifyProfiles.Get(context.TODO(), "12ade33a-21c0-473b-b055-b3c836e1c292")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", verifyProfileData.Data)
```

## 更新验证配置文件

`PATCH /verify_profiles/{verify_profile_id}`

```go
	verifyProfileData, err := client.VerifyProfiles.Update(
		context.TODO(),
		"12ade33a-21c0-473b-b055-b3c836e1c292",
		telnyx.VerifyProfileUpdateParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", verifyProfileData.Data)
```

## 删除验证配置文件

`DELETE /verify_profiles/{verify_profile_id}`

```go
	verifyProfileData, err := client.VerifyProfiles.Delete(context.TODO(), "12ade33a-21c0-473b-b055-b3c836e1c292")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", verifyProfileData.Data)
```

## 获取验证配置文件的消息模板

列出所有验证配置文件的消息模板。

`GET /verify_profiles/templates`

```go
	response, err := client.VerifyProfiles.GetTemplates(context.TODO())
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 创建消息模板

创建一个新的验证配置文件消息模板。

`POST /verify_profiles/templates` — 必需参数：`text`

```go
	messageTemplate, err := client.VerifyProfiles.NewTemplate(context.TODO(), telnyx.VerifyProfileNewTemplateParams{
		Text: "Your {{app_name}} verification code is: {{code}}.",
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", messageTemplate.Data)
```

## 更新消息模板

更新现有的验证配置文件消息模板。

`PATCH /verify_profiles/templates/{template_id}` — 必需参数：`text`

```go
	messageTemplate, err := client.VerifyProfiles.UpdateTemplate(
		context.TODO(),
		"12ade33a-21c0-473b-b055-b3c836e1c292",
		telnyx.VerifyProfileUpdateTemplateParams{
			Text: "Your {{app_name}} verification code is: {{code}}.",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", messageTemplate.Data)
```