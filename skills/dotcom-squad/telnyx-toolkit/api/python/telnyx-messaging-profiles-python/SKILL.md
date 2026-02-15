---
name: telnyx-messaging-profiles-python
description: >-
  Create and manage messaging profiles with number pools, sticky sender, and
  geomatch features. Configure short codes for high-volume messaging. This skill
  provides Python SDK examples.
metadata:
  author: telnyx
  product: messaging-profiles
  language: python
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 消息传递配置文件 - Python

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

## 列出消息传递配置文件

`GET /messagingprofiles`

```python
page = client.messaging_profiles.list()
page = page.data[0]
print(page.id)
```

## 创建消息传递配置文件

`POST /messagingprofiles` — 必需参数：`name`, `whitelisted_destinations`

```python
messaging_profile = client.messaging_profiles.create(
    name="My name",
    whitelisted_destinations=["US"],
)
print(messaging_profile.data)
```

## 获取消息传递配置文件

`GET /messagingprofiles/{id}`

```python
messaging_profile = client.messaging_profiles.retrieve(
    "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(messaging_profile.data)
```

## 更新消息传递配置文件

`PATCH /messagingprofiles/{id}`

```python
messaging_profile = client.messaging_profiles.update(
    messaging_profile_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(messaging_profile.data)
```

## 删除消息传递配置文件

`DELETE /messagingprofiles/{id}`

```python
messaging_profile = client.messaging_profiles.delete(
    "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(messaging_profile.data)
```

## 列出与消息传递配置文件关联的电话号码

`GET /messagingprofiles/{id}/phone_numbers`

```python
page = client.messaging_profiles.list_phone_numbers(
    messaging_profile_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
page = page.data[0]
print(page.id)
```

## 列出与消息传递配置文件关联的短代码

`GET /messagingprofiles/{id}/short_codes`

```python
page = client.messaging_profiles.list_short_codes(
    messaging_profile_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
page = page.data[0]
print(page.messaging_profile_id)
```

## 列出自动应答设置

`GET /messagingprofiles/{profile_id}/autoresp_configs`

```python
autoresp_configs = client.messaging_profiles.autoresp_configs.list(
    profile_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(autoresp_configs.data)
```

## 创建自动应答设置

`POST /messagingprofiles/{profile_id}/autoresp_configs` — 必需参数：`op`, `keywords`, `country_code`

```python
auto_resp_config_response = client.messaging_profiles.autoresp_configs.create(
    profile_id="profile_id",
    country_code="US",
    keywords=["keyword1", "keyword2"],
    op="start",
)
print(auto_resp_config_response.data)
```

## 获取自动应答设置

`GET /messagingprofiles/{profile_id}/autoresp_configs/{autoresp_cfg_id}`

```python
auto_resp_config_response = client.messaging_profiles.autoresp_configs.retrieve(
    autoresp_cfg_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
    profile_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(auto_resp_config_response.data)
```

## 更新自动应答设置

`PUT /messagingprofiles/{profile_id}/autoresp_configs/{autoresp_cfg_id}` — 必需参数：`op`, `keywords`, `country_code`

```python
auto_resp_config_response = client.messaging_profiles.autoresp_configs.update(
    autoresp_cfg_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
    profile_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
    country_code="US",
    keywords=["keyword1", "keyword2"],
    op="start",
)
print(auto_resp_config_response.data)
```

## 删除自动应答设置

`DELETE /messagingprofiles/{profile_id}/autoresp_configs/{autoresp_cfg_id}`

```python
autoresp_config = client.messaging_profiles.autoresp_configs.delete(
    autoresp_cfg_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
    profile_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(autoresp_config)
```

## 列出所有短代码

`GET /short_codes`

```python
page = client.short_codes.list()
page = page.data[0]
print(page.messaging_profile_id)
```

## 获取特定短代码的信息

`GET /short_codes/{id}`

```python
short_code = client.short_codes.retrieve(
    "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(short_code.data)
```

## 更新短代码的设置

`PATCH /short_codes/{id}` — 必需参数：`messaging_profile_id`

```python
short_code = client.short_codes.update(
    id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
    messaging_profile_id="abc85f64-5717-4562-b3fc-2c9600000000",
)
print(short_code.data)
```