---
name: telnyx-messaging-go
description: >-
  Send and receive SMS/MMS messages, manage messaging-enabled phone numbers, and
  handle opt-outs. Use when building messaging applications, implementing 2FA,
  or sending notifications. This skill provides Go SDK examples.
metadata:
  author: telnyx
  product: messaging
  language: go
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 |

# Telnyx 消息服务 - Go 语言版本

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

以下所有示例均假设 `client` 已按照上述方式初始化完成。

## 发送消息

可以使用电话号码、字母数字发送者 ID、短代码或号码池来发送消息。

`POST /messages` — 必需参数：`to`

```go
	response, err := client.Messages.Send(context.TODO(), telnyx.MessageSendParams{
		To: "+18445550001",
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 查取消息

注意：此 API 端点仅能检索创建时间不超过 10 天的消息。

`GET /messages/{id}`

```go
	message, err := client.Messages.Get(context.TODO(), "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", message.Data)
```

## 取消已安排的消息

取消尚未发送的已安排消息。

`DELETE /messages/{id}`

```go
	response, err := client.Messages.CancelScheduled(context.TODO(), "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.ID)
```

## 发送 Whatsapp 消息

`POST /messages/whatsapp` — 必需参数：`from`, `to`, `whatsapp_message`

```go
	response, err := client.Messages.SendWhatsapp(context.TODO(), telnyx.MessageSendWhatsappParams{
		From:            "+13125551234",
		To:              "+13125551234",
		WhatsappMessage: telnyx.MessageSendWhatsappParamsWhatsappMessage{},
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 发送群组 MMS 消息

`POST /messages/group_mms` — 必需参数：`from`, `to`

```go
	response, err := client.Messages.SendGroupMms(context.TODO(), telnyx.MessageSendGroupMmsParams{
		From: "+13125551234",
		To:   []string{"+18655551234", "+14155551234"},
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 发送长码消息

`POST /messages/long_code` — 必需参数：`from`, `to`

```go
	response, err := client.Messages.SendLongCode(context.TODO(), telnyx.MessageSendLongCodeParams{
		From: "+18445550001",
		To:   "+13125550002",
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 使用号码池发送消息

`POST /messages/number_pool` — 必需参数：`to`, `messaging_profile_id`

```go
	response, err := client.Messages.SendNumberPool(context.TODO(), telnyx.MessageSendNumberPoolParams{
		MessagingProfileID: "abc85f64-5717-4562-b3fc-2c9600000000",
		To:                 "+13125550002",
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 安排消息

可以使用电话号码、字母数字发送者 ID、短代码或号码池来安排消息的发送。

`POST /messages/schedule` — 必需参数：`to`

```go
	response, err := client.Messages.Schedule(context.TODO(), telnyx.MessageScheduleParams{
		To: "+18445550001",
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 发送短代码消息

`POST /messages/short_code` — 必需参数：`from`, `to`

```go
	response, err := client.Messages.SendShortCode(context.TODO(), telnyx.MessageSendShortCodeParams{
		From: "+18445550001",
		To:   "+18445550001",
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 查取用户退订信息

检索用户的退订信息。

`GET /messaging_optouts`

```go
	page, err := client.MessagingOptouts.List(context.TODO(), telnyx.MessagingOptoutListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 获取带有消息功能的电话号码信息

`GET /phone_numbers/{id}/messaging`

```go
	messaging, err := client.PhoneNumbers.Messaging.Get(context.TODO(), "id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", messaging.Data)
```

## 更新电话号码的消息功能设置

`PATCH /phone_numbers/{id}/messaging`

```go
	messaging, err := client.PhoneNumbers.Messaging.Update(
		context.TODO(),
		"id",
		telnyx.PhoneNumberMessagingUpdateParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", messaging.Data)
```

## 查取带有消息功能的电话号码列表

`GET /phone_numbers/messaging`

```go
	page, err := client.PhoneNumbers.Messaging.List(context.TODO(), telnyx.PhoneNumberMessagingListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 获取带有消息功能的手机号码信息

`GET /mobile_phone_numbers/{id}/messaging`

```go
	messaging, err := client.MobilePhoneNumbers.Messaging.Get(context.TODO(), "id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", messaging.Data)
```

## 查取带有消息功能的手机号码列表

`GET /mobile_phone_numbers/messaging`

```go
	page, err := client.MobilePhoneNumbers.Messaging.List(context.TODO(), telnyx.MobilePhoneNumberMessagingListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 批量更新电话号码信息

`POST /messaging_numbers/bulk_updates` — 必需参数：`messaging_profile_id`, `numbers`

```go
	messagingNumbersBulkUpdate, err := client.MessagingNumbersBulkUpdates.New(context.TODO(), telnyx.MessagingNumbersBulkUpdateNewParams{
		MessagingProfileID: "00000000-0000-0000-0000-000000000000",
		Numbers:            []string{"+18880000000", "+18880000001", "+18880000002"},
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", messagingNumbersBulkUpdate.Data)
```

## 查取批量更新状态

`GET /messaging_numbers/bulk_updates/{order_id}`

---

## Webhook

以下 Webhook 事件会被发送到您配置的 Webhook URL。所有 Webhook 都包含 `telnyx-timestamp` 和 `telnyx-signature-ed25519` 标头以进行验证（兼容标准 Webhook）。

| 事件 | 描述 |
|-------|-------------|
| `deliveryUpdate` | 消息送达更新 |
| `inboundMessage` | 收到的消息 |
| `replacedLinkClick` | 被替换的链接被点击 |
```
```