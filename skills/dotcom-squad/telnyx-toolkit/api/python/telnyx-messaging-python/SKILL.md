---
name: telnyx-messaging-python
description: >-
  Send and receive SMS/MMS messages, manage messaging-enabled phone numbers, and
  handle opt-outs. Use when building messaging applications, implementing 2FA,
  or sending notifications. This skill provides Python SDK examples.
metadata:
  author: telnyx
  product: messaging
  language: python
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 消息服务 - Python

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

以下所有示例均假设 `client` 已按照上述方式初始化。

## 发送消息

可以使用电话号码、字母数字发送者 ID、短代码或号码池来发送消息。

`POST /messages` — 必需参数：`to`

```python
response = client.messages.send(
    to="+18445550001",
)
print(response.data)
```

## 获取消息

注意：此 API 端点仅能获取创建时间不超过 10 天的消息。

`GET /messages/{id}`

```python
message = client.messages.retrieve(
    "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(message.data)
```

## 取消已安排的消息

取消尚未发送的已安排消息。

`DELETE /messages/{id}`

```python
response = client.messages.cancel_scheduled(
    "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(response.id)
```

## 发送 Whatsapp 消息

`POST /messages/whatsapp` — 必需参数：`from`, `to`, `whatsapp_message`

```python
response = client.messages.send_whatsapp(
    from_="+13125551234",
    to="+13125551234",
    whatsapp_message={},
)
print(response.data)
```

## 发送群组 MMS 消息

`POST /messages/group_mms` — 必需参数：`from`, `to`

```python
response = client.messages.send_group_mms(
    from_="+13125551234",
    to=["+18655551234", "+14155551234"],
)
print(response.data)
```

## 发送长码消息

`POST /messages/long_code` — 必需参数：`from`, `to`

```python
response = client.messages.send_long_code(
    from_="+18445550001",
    to="+13125550002",
)
print(response.data)
```

## 使用号码池发送消息

`POST /messages/number_pool` — 必需参数：`to`, `messaging_profile_id`

```python
response = client.messages.send_number_pool(
    messaging_profile_id="abc85f64-5717-4562-b3fc-2c9600000000",
    to="+13125550002",
)
print(response.data)
```

## 安排消息

可以使用电话号码、字母数字发送者 ID、短代码或号码池来安排消息的发送。

`POST /messages/schedule` — 必需参数：`to`

```python
response = client.messages.schedule(
    to="+18445550001",
)
print(response.data)
```

## 发送短代码消息

`POST /messages/short_code` — 必需参数：`from`, `to`

```python
response = client.messages.send_short_code(
    from_="+18445550001",
    to="+18445550001",
)
print(response.data)
```

## 获取用户退订信息

获取用户的退订信息列表。

`GET /messaging_optouts`

```python
page = client.messaging_optouts.list()
page = page.data[0]
print(page.messaging_profile_id)
```

## 获取带有消息功能的电话号码信息

`GET /phone_numbers/{id}/messaging`

```python
messaging = client.phone_numbers.messaging.retrieve(
    "id",
)
print(messaging.data)
```

## 更新电话号码的消息功能设置

`PATCH /phone_numbers/{id}/messaging`

```python
messaging = client.phone_numbers.messaging.update(
    id="id",
)
print(messaging.data)
```

## 获取带有消息功能的电话号码列表

`GET /phone_numbers/messaging`

```python
page = client.phone_numbers.messaging.list()
page = page.data[0]
print(page.id)
```

## 获取带有消息功能的手机号码信息

`GET /mobile_phone_numbers/{id}/messaging`

```python
messaging = client.mobile_phone_numbers.messaging.retrieve(
    "id",
)
print(messaging.data)
```

## 获取带有消息功能的手机号码列表

`GET /mobile_phone_numbers/messaging`

```python
page = client.mobile_phone_numbers.messaging.list()
page = page.data[0]
print(page.id)
```

## 批量更新电话号码信息

`POST /messaging_numbers/bulk_updates` — 必需参数：`messaging_profile_id`, `numbers`

```python
messaging_numbers_bulk_update = client.messaging_numbers_bulk_updates.create(
    messaging_profile_id="00000000-0000-0000-0000-000000000000",
    numbers=["+18880000000", "+18880000001", "+18880000002"],
)
print(messaging_numbers_bulk_update.data)
```

## 获取批量更新状态

`GET /messaging_numbers/bulk_updates/{order_id}`

---

## Webhook

以下 Webhook 事件会发送到您配置的 Webhook URL。所有 Webhook 都包含 `telnyx-timestamp` 和 `telnyx-signature-ed25519` 标头以进行验证（兼容标准 Webhook）。

| 事件 | 描述 |
|-------|-------------|
| `deliveryUpdate` | 消息发送状态更新 |
| `inboundMessage` | 收到的消息 |
| `replacedLinkClick` | 替换的链接被点击 |