---
name: telnyx-account-notifications-go
description: >-
  Configure notification channels and settings for account alerts and events.
  This skill provides Go SDK examples.
metadata:
  author: telnyx
  product: account-notifications
  language: go
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 账户通知 - Go

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

## 列出通知渠道

列出所有通知渠道。

`GET /notification_channels`

```go
	page, err := client.NotificationChannels.List(context.TODO(), telnyx.NotificationChannelListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建通知渠道

创建一个新的通知渠道。

`POST /notification_channels`

```go
	notificationChannel, err := client.NotificationChannels.New(context.TODO(), telnyx.NotificationChannelNewParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", notificationChannel.Data)
```

## 获取通知渠道信息

获取指定通知渠道的详细信息。

`GET /notification_channels/{id}`

```go
	notificationChannel, err := client.NotificationChannels.Get(context.TODO(), "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", notificationChannel.Data)
```

## 更新通知渠道

更新通知渠道的配置。

`PATCH /notification_channels/{id}`

```go
	notificationChannel, err := client.NotificationChannels.Update(
		context.TODO(),
		"182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		telnyx.NotificationChannelUpdateParams{
			NotificationChannel: telnyx.NotificationChannelParam{},
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", notificationChannel.Data)
```

## 删除通知渠道

删除指定的通知渠道。

`DELETE /notification_channels/{id}`

```go
	notificationChannel, err := client.NotificationChannels.Delete(context.TODO(), "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", notificationChannel.Data)
```

## 列出所有通知事件条件

返回所有通知事件的条件设置。

`GET /notification_event_conditions`

```go
	page, err := client.NotificationEventConditions.List(context.TODO(), telnyx.NotificationEventConditionListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 列出所有通知事件

返回所有已发生的通知事件。

`GET /notification_events`

```go
	page, err := client.NotificationEvents.List(context.TODO(), telnyx.NotificationEventListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 列出所有通知配置文件

列出所有通知配置文件。

`GET /notification_profiles`

```go
	page, err := client.NotificationProfiles.List(context.TODO(), telnyx.NotificationProfileListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建通知配置文件

创建一个新的通知配置文件。

`POST /notification_profiles`

```go
	notificationProfile, err := client.NotificationProfiles.New(context.TODO(), telnyx.NotificationProfileNewParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", notificationProfile.Data)
```

## 获取通知配置文件信息

获取指定通知配置文件的详细信息。

`GET /notification_profiles/{id}`

```go
	notificationProfile, err := client.NotificationProfiles.Get(context.TODO(), "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", notificationProfile.Data)
```

## 更新通知配置文件

更新通知配置文件的设置。

`PATCH /notification_profiles/{id}`

```go
	notificationProfile, err := client.NotificationProfiles.Update(
		context.TODO(),
		"182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		telnyx.NotificationProfileUpdateParams{
			NotificationProfile: telnyx.NotificationProfileParam{},
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", notificationProfile.Data)
```

## 删除通知配置文件

删除指定的通知配置文件。

`DELETE /notification_profiles/{id}`

```go
	notificationProfile, err := client.NotificationProfiles.Delete(context.TODO(), "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", notificationProfile.Data)
```

## 查看通知设置

查看所有通知相关的设置。

`GET /notification_settings`

```go
	page, err := client.NotificationSettings.List(context.TODO(), telnyx.NotificationSettingListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 添加通知设置

添加一个新的通知设置。

`POST /notification_settings`

```go
	notificationSetting, err := client.NotificationSettings.New(context.TODO(), telnyx.NotificationSettingNewParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", notificationSetting.Data)
```

## 获取通知设置信息

获取指定通知设置的详细信息。

`GET /notification_settings/{id}`

```go
	notificationSetting, err := client.NotificationSettings.Get(context.TODO(), "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", notificationSetting.Data)
```

## 删除通知设置

删除指定的通知设置。

`DELETE /notification_settings/{id}`

```go
	notificationSetting, err := client.NotificationSettings.Delete(context.TODO(), "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", notificationSetting.Data)
```