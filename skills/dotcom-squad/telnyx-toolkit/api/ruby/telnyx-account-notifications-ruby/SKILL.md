---
name: telnyx-account-notifications-ruby
description: >-
  Configure notification channels and settings for account alerts and events.
  This skill provides Ruby SDK examples.
metadata:
  author: telnyx
  product: account-notifications
  language: ruby
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 账户通知 - Ruby

## 安装

```bash
gem install telnyx
```

## 设置

```ruby
require "telnyx"

client = Telnyx::Client.new(
  api_key: ENV["TELNYX_API_KEY"], # This is the default and can be omitted
)
```

以下所有示例均假设 `client` 已按上述方式初始化。

## 列出通知渠道

列出所有通知渠道。

`GET /notification_channels`

```ruby
page = client.notification_channels.list

puts(page)
```

## 创建通知渠道

创建一个新的通知渠道。

`POST /notification_channels`

```ruby
notification_channel = client.notification_channels.create

puts(notification_channel)
```

## 获取通知渠道信息

获取指定通知渠道的详细信息。

`GET /notification_channels/{id}`

```ruby
notification_channel = client.notification_channels.retrieve("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(notification_channel)
```

## 更新通知渠道

更新通知渠道的配置。

`PATCH /notification_channels/{id}`

```ruby
notification_channel = client.notification_channels.update("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(notification_channel)
```

## 删除通知渠道

删除指定的通知渠道。

`DELETE /notification_channels/{id}`

```ruby
notification_channel = client.notification_channels.delete("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(notification_channel)
```

## 列出所有通知事件条件

返回所有通知事件的条件设置。

`GET /notification_event_conditions`

```ruby
page = client.notification_event_conditions.list

puts(page)
```

## 列出所有通知事件

返回所有已发生的通知事件列表。

`GET /notification_events`

```ruby
page = client.notification_events.list

puts(page)
```

## 列出所有通知配置文件

列出所有通知配置文件的详细信息。

`GET /notification_profiles`

```ruby
page = client.notification_profiles.list

puts(page)
```

## 创建通知配置文件

创建一个新的通知配置文件。

`POST /notification_profiles`

```ruby
notification_profile = client.notification_profiles.create

puts(notification_profile)
```

## 获取通知配置文件信息

获取指定通知配置文件的详细信息。

`GET /notification_profiles/{id}`

```ruby
notification_profile = client.notification_profiles.retrieve("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(notification_profile)
```

## 更新通知配置文件

更新通知配置文件的设置。

`PATCH /notification_profiles/{id}`

```ruby
notification_profile = client.notification_profiles.update("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(notification_profile)
```

## 删除通知配置文件

删除指定的通知配置文件。

`DELETE /notification_profiles/{id}`

```ruby
notification_profile = client.notification_profiles.delete("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(notification_profile)
```

## 查看通知设置

查看所有通知的设置信息。

`GET /notification_settings`

```ruby
page = client.notification_settings.list

puts(page)
```

## 添加通知设置

添加一个新的通知设置。

`POST /notification_settings`

```ruby
notification_setting = client.notification_settings.create

puts(notification_setting)
```

## 获取通知设置信息

获取指定通知设置的详细信息。

`GET /notification_settings/{id}`

```ruby
notification_setting = client.notification_settings.retrieve("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(notification_setting)
```

## 删除通知设置

删除指定的通知设置。

`DELETE /notification_settings/{id}`

```ruby
notification_setting = client.notification_settings.delete("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(notification_setting)
```