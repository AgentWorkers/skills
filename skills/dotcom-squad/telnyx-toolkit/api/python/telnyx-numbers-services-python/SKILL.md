---
name: telnyx-numbers-services-python
description: >-
  Configure voicemail, voice channels, and emergency (E911) services for your
  phone numbers. This skill provides Python SDK examples.
metadata:
  author: telnyx
  product: numbers-services
  language: python
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 数字服务 - Python

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

## 列出动态紧急地址

根据筛选条件返回动态紧急地址

`GET /dynamic_emergency_addresses`

```python
page = client.dynamic_emergency_addresses.list()
page = page.data[0]
print(page.id)
```

## 创建动态紧急地址

创建一个动态紧急地址。

`POST /dynamic_emergency_addresses` — 必需参数：`house_number`、`street_name`、`locality`、`administrative_area`、`postal_code`、`country_code`

```python
dynamic_emergency_address = client.dynamic_emergency_addresses.create(
    administrative_area="TX",
    country_code="US",
    house_number="600",
    locality="Austin",
    postal_code="78701",
    street_name="Congress",
)
print(dynamic_emergency_address.data)
```

## 获取动态紧急地址

根据提供的 ID 返回动态紧急地址

`GET /dynamic_emergency_addresses/{id}`

```python
dynamic_emergency_address = client.dynamic_emergency_addresses.retrieve(
    "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(dynamic_emergency_address.data)
```

## 删除动态紧急地址

根据提供的 ID 删除动态紧急地址

`DELETE /dynamic_emergency_addresses/{id}`

```python
dynamic_emergency_address = client.dynamic_emergency_addresses.delete(
    "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(dynamic_emergency_address.data)
```

## 列出动态紧急端点

根据筛选条件返回动态紧急端点

`GET /dynamic_emergency_endpoints`

```python
page = client.dynamic_emergency_endpoints.list()
page = page.data[0]
print(page.dynamic_emergency_address_id)
```

## 创建动态紧急端点

创建一个动态紧急端点。

`POST /dynamic_emergency_endpoints` — 必需参数：`dynamic_emergency_address_id`、`callback_number`、`caller_name`

```python
dynamic_emergency_endpoint = client.dynamic_emergency_endpoints.create(
    callback_number="+13125550000",
    caller_name="Jane Doe Desk Phone",
    dynamic_emergency_address_id="0ccc7b54-4df3-4bca-a65a-3da1ecc777f0",
)
print(dynamic_emergency_endpoint.data)
```

## 获取动态紧急端点

根据提供的 ID 返回动态紧急端点

`GET /dynamic_emergency_endpoints/{id}`

```python
dynamic_emergency_endpoint = client.dynamic_emergency_endpoints.retrieve(
    "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(dynamic_emergency_endpoint.data)
```

## 删除动态紧急端点

根据提供的 ID 删除动态紧急端点

`DELETE /dynamic_emergency_endpoints/{id}`

```python
dynamic_emergency_endpoint = client.dynamic_emergency_endpoints.delete(
    "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(dynamic_emergency_endpoint.data)
```

## 列出非美国地区的语音通道

列出您账户中的非美国地区语音通道。

`GET /channel_zones`

```python
page = client.channel_zones.list()
page = page.data[0]
print(page.id)
```

## 更新非美国地区的语音通道

更新非美国地区的语音通道数量。

`PUT /channel_zones/{channel_zone_id}` — 必需参数：`channels`

```python
channel_zone = client.channel_zones.update(
    channel_zone_id="channel_zone_id",
    channels=0,
)
print(channel_zone.id)
```

## 列出美国地区的语音通道

列出您账户中的美国地区语音通道。

`GET /inbound_channels`

```python
inbound_channels = client.inbound_channels.list()
print(inbound_channels.data)
```

## 更新美国地区的语音通道

更新美国地区的语音通道数量。

`PATCH /inbound_channels` — 必需参数：`channels`

```python
inbound_channel = client.inbound_channels.update(
    channels=7,
)
print(inbound_channel.data)
```

## 列出使用通道计费的电话号码

检索按地区分组的所有使用通道计费的电话号码列表。

`GET /list`

```python
response = client.list.retrieve_all()
print(response.data)
```

## 列出特定地区的使用通道计费的电话号码

检索特定地区使用通道计费的电话号码列表。

`GET /list/{channel_zone_id}`

```python
response = client.list.retrieve_by_zone(
    "channel_zone_id",
)
print(response.data)
```

## 获取语音信箱

获取电话号码的语音信箱设置

`GET /phone_numbers/{phone_number_id}/voicemail`

```python
voicemail = client.phone_numbers.voicemail.retrieve(
    "123455678900",
)
print(voicemail.data)
```

## 创建语音信箱

为电话号码创建语音信箱设置

`POST /phone_numbers/{phone_number_id}/voicemail`

```python
voicemail = client.phone_numbers.voicemail.create(
    phone_number_id="123455678900",
)
print(voicemail.data)
```

## 更新语音信箱

更新电话号码的语音信箱设置

`PATCH /phone_numbers/{phone_number_id}/voicemail`

```python
voicemail = client.phone_numbers.voicemail.update(
    phone_number_id="123455678900",
)
print(voicemail.data)
```