---
name: telnyx-account-go
description: >-
  Manage account balance, payments, invoices, webhooks, and view audit logs and
  detail records. This skill provides Go SDK examples.
metadata:
  author: telnyx
  product: account
  language: go
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 账户 - Go

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

## 列出审计日志

检索审计日志条目的列表。

`GET /audit_events`

```go
	page, err := client.AuditEvents.List(context.TODO(), telnyx.AuditEventListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 获取用户余额详情

`GET /balance`

```go
	balance, err := client.Balance.Get(context.TODO())
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", balance.Data)
```

## 搜索详细记录

在 Telnyx 平台上搜索任何详细记录。

`GET /detail_records`

```go
	page, err := client.DetailRecords.List(context.TODO(), telnyx.DetailRecordListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 列出发票

检索分页显示的发票列表。

`GET /invoices`

```go
	page, err := client.Invoices.List(context.TODO(), telnyx.InvoiceListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 根据 ID 获取发票

根据唯一的标识符检索单张发票。

`GET /invoices/{id}`

```go
	invoice, err := client.Invoices.Get(
		context.TODO(),
		"182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		telnyx.InvoiceGetParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", invoice.Data)
```

## 列出自动充值偏好设置

返回支付自动充值偏好设置。

`GET /payments/auto_recharge_prefs`

```go
	autoRechargePrefs, err := client.Payment.AutoRechargePrefs.List(context.TODO())
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", autoRechargePrefs.Data)
```

## 更新自动充值偏好设置

更新支付自动充值偏好设置。

`PATCH /payments/auto_recharge_prefs`

```go
	autoRechargePref, err := client.Payment.AutoRechargePrefs.Update(context.TODO(), telnyx.PaymentAutoRechargePrefUpdateParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", autoRechargePref.Data)
```

## 列出用户标签

列出所有用户标签。

`GET /user_tags`

```go
	userTags, err := client.UserTags.List(context.TODO(), telnyx.UserTagListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", userTags.Data)
```

## 列出 Webhook 交付记录

列出已认证用户的 Webhook 交付记录。

`GET /webhook_deliveries`

```go
	page, err := client.WebhookDeliveries.List(context.TODO(), telnyx.WebhookDeliveryListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 根据 ID 查找 Webhook 交付详情

提供 Webhook 交付的调试数据，如时间戳、交付状态和尝试次数。

`GET /webhook_deliveries/{id}`

```go
	webhookDelivery, err := client.WebhookDeliveries.Get(context.TODO(), "C9C0797E-901D-4349-A33C-C2C8F31A92C2")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", webhookDelivery.Data)
```