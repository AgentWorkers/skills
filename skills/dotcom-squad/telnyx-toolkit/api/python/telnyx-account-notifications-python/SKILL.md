---
name: telnyx-account-notifications-python
description: >-
  Configure notification channels and settings for account alerts and events.
  This skill provides Python SDK examples.
metadata:
  author: telnyx
  product: account-notifications
  language: python
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 账户通知 - Python

## 安装

```bash
pip install telnyx
```

## 设置

```python
import os
from telnyx import Telnyx

client = Telnyx(
    api_key=os.environ.get("TELNYX_API_KEY"),  # This is the default and can be omitted
)
```

以下所有示例均假设 `client` 已按上述方式初始化。

## 列出通知渠道

列出通知渠道。

`GET /notification_channels`

```python
page = client.notification_channels.list()
page = page.data[0]
print(page.id)
```

## 创建通知渠道

创建一个新的通知渠道。

`POST /notification_channels`

```python
notification_channel = client.notification_channels.create()
print(notification_channel.data)
```

## 获取通知渠道信息

获取指定通知渠道的信息。

`GET /notification_channels/{id}`

```python
notification_channel = client.notification_channels.retrieve(
    "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(notification_channel.data)
```

## 更新通知渠道

更新通知渠道的配置。

`PATCH /notification_channels/{id}`

```python
notification_channel = client.notification_channels.update(
    notification_channel_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(notification_channel.data)
```

## 删除通知渠道

删除指定的通知渠道。

`DELETE /notification_channels/{id}`

```python
notification_channel = client.notification_channels.delete(
    "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(notification_channel.data)
```

## 列出所有通知事件条件

返回所有通知事件的条件列表。

`GET /notification_event_conditions`

```python
page = client.notification_event_conditions.list()
page = page.data[0]
print(page.id)
```

## 列出所有通知事件

返回所有通知事件的列表。

`GET /notification_events`

```python
page = client.notification_events.list()
page = page.data[0]
print(page.id)
```

## 列出所有通知配置文件

返回所有通知配置文件的列表。

`GET /notification_profiles`

```python
page = client.notification_profiles.list()
page = page.data[0]
print(page.id)
```

## 创建通知配置文件

创建一个新的通知配置文件。

`POST /notification_profiles`

```python
notification_profile = client.notification_profiles.create()
print(notification_profile.data)
```

## 获取通知配置文件信息

获取指定通知配置文件的信息。

`GET /notification_profiles/{id}`

```python
notification_profile = client.notification_profiles.retrieve(
    "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(notification_profile.data)
```

## 更新通知配置文件

更新通知配置文件的配置。

`PATCH /notification_profiles/{id}`

```python
notification_profile = client.notification_profiles.update(
    notification_profile_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(notification_profile.data)
```

## 删除通知配置文件

删除指定的通知配置文件。

`DELETE /notification_profiles/{id}`

```python
notification_profile = client.notification_profiles.delete(
    "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(notification_profile.data)
```

## 列出通知设置

列出所有通知设置。

`GET /notification_settings`

```python
page = client.notification_settings.list()
page = page.data[0]
print(page.id)
```

## 添加通知设置

添加一个新的通知设置。

`POST /notification_settings`

```python
notification_setting = client.notification_settings.create()
print(notification_setting.data)
```

## 获取通知设置信息

获取指定通知设置的信息。

`GET /notification_settings/{id}`

```python
notification_setting = client.notification_settings.retrieve(
    "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(notification_setting.data)
```

## 删除通知设置

删除指定的通知设置。

`DELETE /notification_settings/{id}`

```python
notification_setting = client.notification_settings.delete(
    "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(notification_setting.data)
```
```