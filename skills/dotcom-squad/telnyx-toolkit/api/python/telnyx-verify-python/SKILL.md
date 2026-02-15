---
name: telnyx-verify-python
description: >-
  Look up phone number information (carrier, type, caller name) and verify users
  via SMS/voice OTP. Use for phone verification and data enrichment. This skill
  provides Python SDK examples.
metadata:
  author: telnyx
  product: verify
  language: python
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx Verify - Python

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

## 查找电话号码信息

返回有关提供的电话号码的信息。

`GET /number_lookup/{phone_number}`

```python
number_lookup = client.number_lookup.retrieve(
    phone_number="+18665552368",
)
print(number_lookup.data)
```

## 触发电话验证

`POST /verifications/call` — 必需参数：`phone_number`、`verify_profile_id`

```python
create_verification_response = client.verifications.trigger_call(
    phone_number="+13035551234",
    verify_profile_id="12ade33a-21c0-473b-b055-b3c836e1c292",
)
print(create_verification_response.data)
```

## 触发闪现式电话验证

`POST /verifications/flashcall` — 必需参数：`phone_number`、`verify_profile_id`

```python
create_verification_response = client.verifications.trigger_flashcall(
    phone_number="+13035551234",
    verify_profile_id="12ade33a-21c0-473b-b055-b3c836e1c292",
)
print(create_verification_response.data)
```

## 触发短信验证

`POST /verifications/sms` — 必需参数：`phone_number`、`verify_profile_id`

```python
create_verification_response = client.verifications.trigger_sms(
    phone_number="+13035551234",
    verify_profile_id="12ade33a-21c0-473b-b055-b3c836e1c292",
)
print(create_verification_response.data)
```

## 获取验证结果

`GET /verifications/{verification_id}`

```python
verification = client.verifications.retrieve(
    "12ade33a-21c0-473b-b055-b3c836e1c292",
)
print(verification.data)
```

## 通过 ID 验证验证码

`POST /verifications/{verification_id}/actions/verify`

```python
verify_verification_code_response = client.verifications.actions.verify(
    verification_id="12ade33a-21c0-473b-b055-b3c836e1c292",
)
print(verify_verification_code_response.data)
```

## 按电话号码列出验证记录

`GET /verifications/by_phone_number/{phone_number}`

```python
by_phone_numbers = client.verifications.by_phone_number.list(
    "+13035551234",
)
print(by_phone_numbers.data)
```

## 通过电话号码验证验证码

`POST /verifications/by_phone_number/{phone_number}/actions/verify` — 必需参数：`code`、`verify_profile_id`

```python
verify_verification_code_response = client.verifications.by_phone_number.actions.verify(
    phone_number="+13035551234",
    code="17686",
    verify_profile_id="12ade33a-21c0-473b-b055-b3c836e1c292",
)
print(verify_verification_code_response.data)
```

## 列出所有验证配置文件

获取分页显示的验证配置文件列表。

`GET /verify_profiles`

```python
page = client.verify_profiles.list()
page = page.data[0]
print(page.id)
```

## 创建验证配置文件

创建一个新的验证配置文件以关联验证操作。

`POST /verify_profiles` — 必需参数：`name`

```python
verify_profile_data = client.verify_profiles.create(
    name="Test Profile",
)
print(verify_profile_data.data)
```

## 获取验证配置文件信息

获取单个验证配置文件的信息。

`GET /verify_profiles/{verify_profile_id}`

```python
verify_profile_data = client.verify_profiles.retrieve(
    "12ade33a-21c0-473b-b055-b3c836e1c292",
)
print(verify_profile_data.data)
```

## 更新验证配置文件

`PATCH /verify_profiles/{verify_profile_id}`

```python
verify_profile_data = client.verify_profiles.update(
    verify_profile_id="12ade33a-21c0-473b-b055-b3c836e1c292",
)
print(verify_profile_data.data)
```

## 删除验证配置文件

`DELETE /verify_profiles/{verify_profile_id}`

```python
verify_profile_data = client.verify_profiles.delete(
    "12ade33a-21c0-473b-b055-b3c836e1c292",
)
print(verify_profile_data.data)
```

## 获取验证配置文件的消息模板

列出所有验证配置文件的消息模板。

`GET /verify_profiles/templates`

```python
response = client.verify_profiles.retrieve_templates()
print(response.data)
```

## 创建消息模板

创建一个新的验证配置文件消息模板。

`POST /verify_profiles/templates` — 必需参数：`text`

```python
message_template = client.verify_profiles.create_template(
    text="Your {{app_name}} verification code is: {{code}}.",
)
print(message_template.data)
```

## 更新消息模板

更新现有的验证配置文件消息模板。

`PATCH /verify_profiles/templates/{template_id}` — 必需参数：`text`

```python
message_template = client.verify_profiles.update_template(
    template_id="12ade33a-21c0-473b-b055-b3c836e1c292",
    text="Your {{app_name}} verification code is: {{code}}.",
)
print(message_template.data)
```