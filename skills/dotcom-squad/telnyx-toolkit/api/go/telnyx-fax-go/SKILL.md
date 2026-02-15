---
name: telnyx-fax-go
description: >-
  Send and receive faxes programmatically. Manage fax applications and media.
  This skill provides Go SDK examples.
metadata:
  author: telnyx
  product: fax
  language: go
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 传真 - Go

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

## 列出所有传真应用程序

此端点会在响应的 `data` 属性中返回您的传真应用程序列表。

`GET /fax_applications`

```go
	page, err := client.FaxApplications.List(context.TODO(), telnyx.FaxApplicationListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建传真应用程序

根据请求中发送的参数创建一个新的传真应用程序。

`POST /fax_applications` — 必需参数：`application_name`、`webhook_event_url`

```go
	faxApplication, err := client.FaxApplications.New(context.TODO(), telnyx.FaxApplicationNewParams{
		ApplicationName: "fax-router",
		WebhookEventURL: "https://example.com",
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", faxApplication.Data)
```

## 获取传真应用程序的详细信息

在响应的 `data` 属性中返回现有传真应用程序的详细信息。

`GET /fax_applications/{id}`

```go
	faxApplication, err := client.FaxApplications.Get(context.TODO(), "1293384261075731499")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", faxApplication.Data)
```

## 更新传真应用程序

根据请求的参数更新现有传真应用程序的设置。

`PATCH /fax_applications/{id}` — 必需参数：`application_name`、`webhook_event_url`

```go
	faxApplication, err := client.FaxApplications.Update(
		context.TODO(),
		"1293384261075731499",
		telnyx.FaxApplicationUpdateParams{
			ApplicationName: "fax-router",
			WebhookEventURL: "https://example.com",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", faxApplication.Data)
```

## 删除传真应用程序

永久删除一个传真应用程序。

`DELETE /fax_applications/{id}`

```go
	faxApplication, err := client.FaxApplications.Delete(context.TODO(), "1293384261075731499")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", faxApplication.Data)
```

## 查看传真列表

`GET /faxes`

```go
	page, err := client.Faxes.List(context.TODO(), telnyx.FaxListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 发送传真

发送传真。

`POST /faxes` — 必需参数：`connection_id`、`from`、`to`

```go
	fax, err := client.Faxes.New(context.TODO(), telnyx.FaxNewParams{
		ConnectionID: "234423",
		From:         "+13125790015",
		To:           "+13127367276",
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", fax.Data)
```

## 查看传真详情

`GET /faxes/{id}`

```go
	fax, err := client.Faxes.Get(context.TODO(), "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", fax.Data)
```

## 删除传真

`DELETE /faxes/{id}`

```go
	err := client.Faxes.Delete(context.TODO(), "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
	if err != nil {
		panic(err.Error())
	}
```

## 取消传真

取消处于以下状态之一的传出传真：`queued`、`media.processed`、`originated` 或 `sending`

`POST /faxes/{id}/actions/cancel`

```go
	response, err := client.Faxes.Actions.Cancel(context.TODO(), "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 刷新传真信息

当传入的传真信息过期时，刷新其媒体链接。

`POST /faxes/{id}/actions/refresh`

```go
	response, err := client.Faxes.Actions.Refresh(context.TODO(), "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

---

## Webhook

以下 Webhook 事件会被发送到您配置的 Webhook URL：
所有 Webhook 都包含 `telnyx-timestamp` 和 `telnyx-signature-ed25519` 标头以进行验证（兼容标准 Webhook）。

| 事件 | 描述 |
|-------|-------------|
| `fax.delivered` | 传真已送达 |
| `fax_failed` | 传真发送失败 |
| `fax.media.processed` | 传真媒体文件已处理 |
| `fax.queued` | 传真已排队 |
| `fax.sendingstarted` | 传真发送开始 |
```