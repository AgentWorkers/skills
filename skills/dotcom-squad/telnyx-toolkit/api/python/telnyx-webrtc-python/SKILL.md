---
name: telnyx-webrtc-python
description: >-
  Manage WebRTC credentials and mobile push notification settings. Use when
  building browser-based or mobile softphone applications. This skill provides
  Python SDK examples.
metadata:
  author: telnyx
  product: webrtc
  language: python
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx Webrtc - Python

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

## 列出移动推送凭据

`GET /mobile_push_credentials`

```python
page = client.mobile_push_credentials.list()
page = page.data[0]
print(page.id)
```

## 创建新的移动推送凭据

`POST /mobile_push_credentials`

```python
push_credential_response = client.mobile_push_credentials.create(
    create_mobile_push_credential_request={
        "alias": "LucyIosCredential",
        "certificate": "-----BEGIN CERTIFICATE----- MIIGVDCCBTKCAQEAsNlRJVZn9ZvXcECQm65czs... -----END CERTIFICATE-----",
        "private_key": "-----BEGIN RSA PRIVATE KEY----- MIIEpQIBAAKCAQEAsNlRJVZn9ZvXcECQm65czs... -----END RSA PRIVATE KEY-----",
        "type": "ios",
    },
)
print(push_credential_response.data)
```

## 获取移动推送凭据

根据给定的 `push_credential_id` 获取移动推送凭据

`GET /mobile_push_credentials/{push_credential_id}`

```python
push_credential_response = client.mobile_push_credentials.retrieve(
    "0ccc7b76-4df3-4bca-a05a-3da1ecc389f0",
)
print(push_credential_response.data)
```

## 删除移动推送凭据

根据给定的 `push_credential_id` 删除移动推送凭据

`DELETE /mobile_push_credentials/{push_credential_id}`

```python
client.mobile_push_credentials.delete(
    "0ccc7b76-4df3-4bca-a05a-3da1ecc389f0",
)
```

## 列出所有凭据

列出所有的按需凭据。

`GET /telephony_credentials`

```python
page = client.telephony_credentials.list()
page = page.data[0]
print(page.id)
```

## 创建凭据

创建一个新的凭据。

`POST /telephony_credentials` — 必需参数：`connection_id`

```python
telephony_credential = client.telephony_credentials.create(
    connection_id="1234567890",
)
print(telephony_credential.data)
```

## 获取凭据详情

获取现有按需凭据的详细信息。

`GET /telephony_credentials/{id}`

```python
telephony_credential = client.telephony_credentials.retrieve(
    "id",
)
print(telephony_credential.data)
```

## 更新凭据

更新现有的凭据。

`PATCH /telephony_credentials/{id}`

```python
telephony_credential = client.telephony_credentials.update(
    id="id",
)
print(telephony_credential.data)
```

## 删除凭据

删除现有的凭据。

`DELETE /telephony_credentials/{id}`

```python
telephony_credential = client.telephony_credentials.delete(
    "id",
)
print(telephony_credential.data)
```

## 创建访问令牌

为该凭据创建一个访问令牌（JWT）。

`POST /telephony_credentials/{id}/token`

```python
response = client.telephony_credentials.create_token(
    "id",
)
print(response)
```