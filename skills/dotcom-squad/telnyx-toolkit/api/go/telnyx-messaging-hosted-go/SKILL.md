---
name: telnyx-messaging-hosted-go
description: >-
  Set up hosted SMS numbers, toll-free verification, and RCS messaging. Use when
  migrating numbers or enabling rich messaging features. This skill provides Go
  SDK examples.
metadata:
  author: telnyx
  product: messaging-hosted
  language: go
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx Messaging Hosted - Go

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

## 列出托管消息服务的号码订单

`GET /messaging_hosted_number_orders`

```go
	page, err := client.MessagingHostedNumberOrders.List(context.TODO(), telnyx.MessagingHostedNumberOrderListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建托管消息服务的号码订单

`POST /messaging_hosted_number_orders`

```go
	messagingHostedNumberOrder, err := client.MessagingHostedNumberOrders.New(context.TODO(), telnyx.MessagingHostedNumberOrderNewParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", messagingHostedNumberOrder.Data)
```

## 获取托管消息服务的号码订单信息

`GET /messaging_hosted_number_orders/{id}`

```go
	messagingHostedNumberOrder, err := client.MessagingHostedNumberOrders.Get(context.TODO(), "id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", messagingHostedNumberOrder.Data)
```

## 删除托管消息服务的号码订单

删除托管消息服务的号码订单及其所有关联的电话号码。

`DELETE /messaging_hosted_number_orders/{id}`

```go
	messagingHostedNumberOrder, err := client.MessagingHostedNumberOrders.Delete(context.TODO(), "id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", messagingHostedNumberOrder.Data)
```

## 上传托管号码文档

`POST /messaging_hosted_number_orders/{id}/actions/file_upload`

```go
	response, err := client.MessagingHostedNumberOrders.Actions.UploadFile(
		context.TODO(),
		"id",
		telnyx.MessagingHostedNumberOrderActionUploadFileParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 验证托管号码的验证码

验证发送到托管号码的验证码。

`POST /messaging_hosted_number_orders/{id}/validation_codes` — 必需参数：`verification_codes`

```go
	response, err := client.MessagingHostedNumberOrders.ValidateCodes(
		context.TODO(),
		"id",
		telnyx.MessagingHostedNumberOrderValidateCodesParams{
			VerificationCodes: []telnyx.MessagingHostedNumberOrderValidateCodesParamsVerificationCode{{
				Code:        "code",
				PhoneNumber: "phone_number",
			}},
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 生成托管号码的验证码

为托管号码生成验证码。

`POST /messaging_hosted_number_orders/{id}/verification_codes` — 必需参数：`phone_numbers`, `verification_method`

```go
	response, err := client.MessagingHostedNumberOrders.NewVerificationCodes(
		context.TODO(),
		"id",
		telnyx.MessagingHostedNumberOrderNewVerificationCodesParams{
			PhoneNumbers:       []string{"string"},
			VerificationMethod: telnyx.MessagingHostedNumberOrderNewVerificationCodesParamsVerificationMethodSMS,
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 检查托管号码的适用性

`POST /messaging_hosted_number_orders/eligibility_numbers_check` — 必需参数：`phone_numbers`

```go
	response, err := client.MessagingHostedNumberOrders.CheckEligibility(context.TODO(), telnyx.MessagingHostedNumberOrderCheckEligibilityParams{
		PhoneNumbers: []string{"string"},
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.PhoneNumbers)
```

## 删除托管消息服务的号码

`DELETE /messaging_hosted_numbers/{id}`

```go
	messagingHostedNumber, err := client.MessagingHostedNumbers.Delete(context.TODO(), "id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", messagingHostedNumber.Data)
```

## 发送 RCS 消息

`POST /messages/rcs` — 必需参数：`agent_id`, `to`, `messaging_profile_id`, `agent_message`

```go
	response, err := client.Messages.Rcs.Send(context.TODO(), telnyx.MessageRcSendParams{
		AgentID:            "Agent007",
		AgentMessage:       telnyx.RcsAgentMessageParam{},
		MessagingProfileID: "messaging_profile_id",
		To:                 "+13125551234",
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 列出所有 RCS 代理

`GET /messaging/rcs/agents`

```go
	page, err := client.Messaging.Rcs.Agents.List(context.TODO(), telnyx.MessagingRcAgentListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 获取 RCS 代理信息

`GET /messaging/rcs/agents/{id}`

```go
	rcsAgentResponse, err := client.Messaging.Rcs.Agents.Get(context.TODO(), "id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", rcsAgentResponse.Data)
```

## 修改 RCS 代理

`PATCH /messaging/rcs/agents/{id}`

```go
	rcsAgentResponse, err := client.Messaging.Rcs.Agents.Update(
		context.TODO(),
		"id",
		telnyx.MessagingRcAgentUpdateParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", rcsAgentResponse.Data)
```

## 检查 RCS 功能（批量）

`POST /messaging/rcs/bulk_capabilities` — 必需参数：`agent_id`, `phone_numbers`

```go
	response, err := client.Messaging.Rcs.ListBulkCapabilities(context.TODO(), telnyx.MessagingRcListBulkCapabilitiesParams{
		AgentID:      "TestAgent",
		PhoneNumbers: []string{"+13125551234"},
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 检查 RCS 功能

`GET /messaging/rcs/capabilities/{agent_id}/{phone_number}`

```go
	response, err := client.Messaging.Rcs.GetCapabilities(
		context.TODO(),
		"phone_number",
		telnyx.MessagingRcGetCapabilitiesParams{
			AgentID: "agent_id",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 添加 RCS 测试号码

为 RCS 代理添加测试电话号码以供测试使用。

`PUT /messages/rcs/test_numberInvite/{id}/{phone_number}`

```go
	response, err := client.Messaging.Rcs.InviteTestNumber(
		context.TODO(),
		"phone_number",
		telnyx.MessagingRcInviteTestNumberParams{
			ID: "id",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 生成 RCS 深链接

生成一个深链接，用于与特定代理启动 RCS 对话。

`GET /messages/rcs_deeplinks/{agent_id}`

```go
	response, err := client.Messages.Rcs.GenerateDeeplink(
		context.TODO(),
		"agent_id",
		telnyx.MessageRcGenerateDeeplinkParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 列出验证请求

获取之前提交的免费电话验证请求列表

`GET /messaging_tollfree/verification/requests`

```go
	page, err := client.MessagingTollfree.Verification.Requests.List(context.TODO(), telnyx.MessagingTollfreeVerificationRequestListParams{
		Page:     1,
		PageSize: 1,
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 提交验证请求

提交新的免费电话验证请求

`POST /messaging_tollfree/verification/requests` — 必需参数：`businessName`, `corporateWebsite`, `businessAddr1`, `businessCity`, `businessState`, `businessZip`, `businessContactFirstName`, `businessContactLastName`, `businessContactEmail`, `businessContactPhone`, `messageVolume`, `phoneNumbers`, `useCase`, `useCaseSummary`, `productionMessageContent`, `optInWorkflow`, `optInWorkflowImageURLs`, `additionalInformation`, `isvReseller`

```go
	verificationRequestEgress, err := client.MessagingTollfree.Verification.Requests.New(context.TODO(), telnyx.MessagingTollfreeVerificationRequestNewParams{
		TfVerificationRequest: telnyx.TfVerificationRequestParam{
			AdditionalInformation:    "additionalInformation",
			BusinessAddr1:            "600 Congress Avenue",
			BusinessCity:             "Austin",
			BusinessContactEmail:     "email@example.com",
			BusinessContactFirstName: "John",
			BusinessContactLastName:  "Doe",
			BusinessContactPhone:     "+18005550100",
			BusinessName:             "Telnyx LLC",
			BusinessState:            "Texas",
			BusinessZip:              "78701",
			CorporateWebsite:         "http://example.com",
			IsvReseller:              "isvReseller",
			MessageVolume:            telnyx.VolumeV100000,
			OptInWorkflow:            "User signs into the Telnyx portal, enters a number and is prompted to select whether they want to use 2FA verification for security purposes. If they've opted in a confirmation message is sent out to the handset",
			OptInWorkflowImageURLs: []telnyx.URLParam{{
				URL: "https://telnyx.com/sign-up",
			}, {
				URL: "https://telnyx.com/company/data-privacy",
			}},
			PhoneNumbers: []telnyx.TfPhoneNumberParam{{
				PhoneNumber: "+18773554398",
			}, {
				PhoneNumber: "+18773554399",
			}},
			ProductionMessageContent: "Your Telnyx OTP is XXXX",
			UseCase:                  telnyx.UseCaseCategoriesTwoFa,
			UseCaseSummary:           "This is a use case where Telnyx sends out 2FA codes to portal users to verify their identity in order to sign into the portal",
		},
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", verificationRequestEgress.ID)
```

## 获取验证请求信息

通过 ID 获取单个验证请求的详细信息。

`GET /messaging_tollfree/verification/requests/{id}`

```go
	verificationRequestStatus, err := client.MessagingTollfree.Verification.Requests.Get(context.TODO(), "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", verificationRequestStatus.ID)
```

## 更新验证请求

更新现有的免费电话验证请求。

`PATCH /messaging_tollfree/verification/requests/{id}` — 必需参数：`businessName`, `corporateWebsite`, `businessAddr1`, `businessCity`, `businessState`, `businessZip`, `businessContactFirstName`, `businessContactLastName`, `businessContactEmail`, `businessContactPhone`, `messageVolume`, `phoneNumbers`, `useCase`, `useCaseSummary`, `productionMessageContent`, `optInWorkflow`, `optInWorkflowImageURLs`, `additionalInformation`, `isvReseller`

```go
	verificationRequestEgress, err := client.MessagingTollfree.Verification.Requests.Update(
		context.TODO(),
		"182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		telnyx.MessagingTollfreeVerificationRequestUpdateParams{
			TfVerificationRequest: telnyx.TfVerificationRequestParam{
				AdditionalInformation:    "additionalInformation",
				BusinessAddr1:            "600 Congress Avenue",
				BusinessCity:             "Austin",
				BusinessContactEmail:     "email@example.com",
				BusinessContactFirstName: "John",
				BusinessContactLastName:  "Doe",
				BusinessContactPhone:     "+18005550100",
				BusinessName:             "Telnyx LLC",
				BusinessState:            "Texas",
				BusinessZip:              "78701",
				CorporateWebsite:         "http://example.com",
				IsvReseller:              "isvReseller",
				MessageVolume:            telnyx.VolumeV100000,
				OptInWorkflow:            "User signs into the Telnyx portal, enters a number and is prompted to select whether they want to use 2FA verification for security purposes. If they've opted in a confirmation message is sent out to the handset",
				OptInWorkflowImageURLs: []telnyx.URLParam{{
					URL: "https://telnyx.com/sign-up",
				}, {
					URL: "https://telnyx.com/company/data-privacy",
				}},
				PhoneNumbers: []telnyx.TfPhoneNumberParam{{
					PhoneNumber: "+18773554398",
				}, {
					PhoneNumber: "+18773554399",
				}},
				ProductionMessageContent: "Your Telnyx OTP is XXXX",
				UseCase:                  telnyx.UseCaseCategoriesTwoFa,
				UseCaseSummary:           "This is a use case where Telnyx sends out 2FA codes to portal users to verify their identity in order to sign into the portal",
			},
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", verificationRequestEgress.ID)
```

## 删除验证请求

只有在请求处于“被拒绝”状态时，才能删除该请求。

`DELETE /messaging_tollfree/verification/requests/{id}`

```go
	err := client.MessagingTollfree.Verification.Requests.Delete(context.TODO(), "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
	if err != nil {
		panic(err.Error())
	}
```