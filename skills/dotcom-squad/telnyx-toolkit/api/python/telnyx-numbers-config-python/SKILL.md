---
name: telnyx-numbers-config-python
description: >-
  Configure phone number settings including caller ID, call forwarding,
  messaging enablement, and connection assignments. This skill provides Python
  SDK examples.
metadata:
  author: telnyx
  product: numbers-config
  language: python
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 数字信息配置 - Python

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

## 列出电话号码块的相关任务

`GET /phone_number_blocks/jobs`

```python
page = client.phone_number_blocks.jobs.list()
page = page.data[0]
print(page.id)
```

## 获取某个电话号码块的相关信息

`GET /phone_number_blocks/jobs/{id}`

```python
job = client.phone_number_blocks.jobs.retrieve(
    "id",
)
print(job.data)
```

## 删除与某个电话号码块关联的所有号码

创建一个新的后台任务来删除与该号码块关联的所有号码。

`POST /phone_number_blocks/jobs/delete_phone_number_block` — 必需参数：`phone_number_block_id`

```python
response = client.phone_number_blocks.jobs.delete_phone_number_block(
    phone_number_block_id="f3946371-7199-4261-9c3d-81a0d7935146",
)
print(response.data)
```

## 列出所有电话号码

`GET /phone_numbers`

```python
page = client.phone_numbers.list()
page = page.data[0]
print(page.id)
```

## 获取某个电话号码的信息

`GET /phone_numbers/{id}`

```python
phone_number = client.phone_numbers.retrieve(
    "1293384261075731499",
)
print(phone_number.data)
```

## 更新某个电话号码的信息

`PATCH /phone_numbers/{id}`

```python
phone_number = client.phone_numbers.update(
    phone_number_id="1293384261075731499",
)
print(phone_number.data)
```

## 删除某个电话号码

`DELETE /phone_numbers/{id}`

```python
phone_number = client.phone_numbers.delete(
    "1293384261075731499",
)
print(phone_number.data)
```

## 更改电话号码的捆绑状态（将其添加到捆绑中或从捆绑中移除）

`PATCH /phone_numbers/{id}/actions/bundle_status_change` — 必需参数：`bundle_id`

```python
response = client.phone_numbers.actions.change_bundle_status(
    id="1293384261075731499",
    bundle_id="5194d8fc-87e6-4188-baa9-1c434bbe861b",
)
print(response.data)
```

## 为某个电话号码启用紧急呼叫功能

`POST /phone_numbers/{id}/actions/enable_emergency` — 必需参数：`emergency_enabled`, `emergency_address_id`

```python
response = client.phone_numbers.actions.enable_emergency(
    id="1293384261075731499",
    emergency_address_id="53829456729313",
    emergency_enabled=True,
)
print(response.data)
```

## 获取包含语音设置的电话号码信息

`GET /phone_numbers/{id}/voice`

```python
voice = client.phone_numbers.voice.retrieve(
    "1293384261075731499",
)
print(voice.data)
```

## 更新包含语音设置的电话号码信息

`PATCH /phone_numbers/{id}/voice`

```python
voice = client.phone_numbers.voice.update(
    id="1293384261075731499",
)
print(voice.data)
```

## 验证电话号码的所有权

验证提供的电话号码的所有权，并返回号码与其 ID 的对应关系，以及未在账户中找到的号码列表。

`POST /phone_numbers/actions/verify_ownership` — 必需参数：`phone_numbers`

```python
response = client.phone_numbers.actions.verify_ownership(
    phone_numbers=["+15551234567"],
)
print(response.data)
```

## 查看 CSV 下载记录

`GET /phone_numbers/csv_downloads`

```python
page = client.phone_numbers.csv_downloads.list()
page = page.data[0]
print(page.id)
```

## 创建 CSV 下载文件

`POST /phone_numbers/csv_downloads`

```python
csv_download = client.phone_numbers.csv_downloads.create()
print(csv_download.data)
```

## 获取 CSV 下载文件

`GET /phone_numbers/csv_downloads/{id}`

```python
csv_download = client.phone_numbers.csv_downloads.retrieve(
    "id",
)
print(csv_download.data)
```

## 列出所有电话号码相关的任务

`GET /phone_numbers/jobs`

```python
page = client.phone_numbers.jobs.list()
page = page.data[0]
print(page.id)
```

## 获取某个电话号码任务的相关信息

`GET /phone_numbers/jobs/{id}`

```python
job = client.phone_numbers.jobs.retrieve(
    "id",
)
print(job.data)
```

## 删除一批电话号码

创建一个新的后台任务来删除一批电话号码。

`POST /phone_numbers/jobs/delete_phone_numbers` — 必需参数：`phone_numbers`

```python
response = client.phone_numbers.jobs.delete_batch(
    phone_numbers=["+19705555098", "+19715555098", "32873127836"],
)
print(response.data)
```

## 更新一批电话号码的紧急呼叫设置

创建一个新的后台任务来更新一批电话号码的紧急呼叫设置。

`POST /phone_numbers/jobs/update_emergency_settings` — 必需参数：`emergency_enabled`, `phone_numbers`

```python
response = client.phone_numbers.jobs.update_emergency_settings_batch(
    emergency_enabled=True,
    phone_numbers=["+19705555098", "+19715555098", "32873127836"],
)
print(response.data)
```

## 更新一批电话号码的信息

创建一个新的后台任务来更新一批电话号码的信息。

`POST /phone_numbers/jobs/update_phone_numbers` — 必需参数：`phone_numbers`

```python
response = client.phone_numbers.jobs.update_batch(
    phone_numbers=["1583466971586889004", "+13127367254"],
)
print(response.data)
```

## 获取一批电话号码的监管要求信息

`GET /phone_numbers/regulatory_requirements`

```python
phone_numbers_regulatory_requirement = client.phone_numbers_regulatory_requirements.retrieve()
print(phone_numbers_regulatory_requirement.data)
```

## 简化版电话号码列表

提供性能更高、请求限制更宽松的电话号码列表版本。

`GET /phone_numbers/slim`

```python
page = client.phone_numbers.slim_list()
page = page.data[0]
print(page.id)
```

## 列出包含语音设置的电话号码

`GET /phone_numbers/voice`

```python
page = client.phone_numbers.voice.list()
page = page.data[0]
print(page.id)
```

## 列出手机号码

`GET /v2/mobile_phone_numbers`

```python
page = client.mobile_phone_numbers.list()
page = page.data[0]
print(page.id)
```

## 获取某个手机号码的信息

`GET /v2/mobile_phone_numbers/{id}`

```python
mobile_phone_number = client.mobile_phone_numbers.retrieve(
    "id",
)
print(mobile_phone_number.data)
```

## 更新某个手机号码的信息

`PATCH /v2/mobile_phone_numbers/{id}`

```python
mobile_phone_number = client.mobile_phone_numbers.update(
    id="id",
)
print(mobile_phone_number.data)
```