---
name: telnyx-account-access-python
description: >-
  Configure account addresses, authentication providers, IP access controls,
  billing groups, and integration secrets. This skill provides Python SDK
  examples.
metadata:
  author: telnyx
  product: account-access
  language: python
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 账户访问 - Python

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

## 列出所有地址

返回您的地址列表。

`GET /addresses`

```python
page = client.addresses.list()
page = page.data[0]
print(page.id)
```

## 创建地址

创建一个新的地址。

`POST /addresses` — 必需参数：`first_name`（名字）、`last_name`（姓氏）、`business_name`（公司名称）、`street_address`（街道地址）、`locality`（地区）、`country_code`（国家代码）

```python
address = client.addresses.create(
    business_name="Toy-O'Kon",
    country_code="US",
    first_name="Alfred",
    last_name="Foster",
    locality="Austin",
    street_address="600 Congress Avenue",
)
print(address.data)
```

## 查取地址信息

获取现有地址的详细信息。

`GET /addresses/{id}`

```python
address = client.addresses.retrieve(
    "id",
)
print(address.data)
```

## 删除地址

删除现有的地址。

`DELETE /addresses/{id}`

```python
address = client.addresses.delete(
    "id",
)
print(address.data)
```

## 接受此地址建议作为新的紧急联系地址，并完成将其相关号码上传至 Microsoft 的操作。

`POST /addresses/{id}/actions/accept_suggestions`

```python
response = client.addresses.actions.accept_suggestions(
    address_uuid="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(response.data)
```

## 验证地址

验证地址是否适合用于紧急服务。

`POST /addresses/actions/validate` — 必需参数：`country_code`（国家代码）、`street_address`（街道地址）、`postal_code`（邮政编码）

```python
response = client.addresses.actions.validate(
    country_code="US",
    postal_code="78701",
    street_address="600 Congress Avenue",
)
print(response.data)
```

## 列出所有 SSO（单点登录）认证提供者

返回您的所有 SSO 认证提供者列表。

`GET /authentication_providers`

```python
page = client.authentication_providers.list()
page = page.data[0]
print(page.id)
```

## 创建认证提供者

创建一个新的认证提供者。

`POST /authentication_providers` — 必需参数：`name`（名称）、`short_name`（简称）、`settings`（设置）

```python
authentication_provider = client.authentication_providers.create(
    name="Okta",
    settings={
        "idp_cert_fingerprint": "13:38:C7:BB:C9:FF:4A:70:38:3A:E3:D9:5C:CD:DB:2E:50:1E:80:A7",
        "idp_entity_id": "https://myorg.myidp.com/saml/metadata",
        "idp_sso_target_url": "https://myorg.myidp.com/trust/saml2/http-post/sso",
    },
    short_name="myorg",
)
print(authentication_provider.data)
```

## 查取认证提供者信息

获取现有认证提供者的详细信息。

`GET /authentication_providers/{id}`

```python
authentication_provider = client.authentication_providers.retrieve(
    "id",
)
print(authentication_provider.data)
```

## 更新认证提供者设置

更新现有认证提供者的设置。

`PATCH /authentication_providers/{id}`

```python
authentication_provider = client.authentication_providers.update(
    id="id",
    active=True,
    name="Okta",
    settings={
        "idp_entity_id": "https://myorg.myidp.com/saml/metadata",
        "idp_sso_target_url": "https://myorg.myidp.com/trust/saml2/http-post/sso",
        "idp_cert_fingerprint": "13:38:C7:BB:C9:FF:4A:70:38:3A:E3:D9:5C:CD:DB:2E:50:1E:80:A7",
        "idp_cert_fingerprint_algorithm": "sha1",
    },
    short_name="myorg",
)
print(authentication_provider.data)
```

## 删除认证提供者

删除现有的认证提供者。

`DELETE /authentication_providers/{id}`

```python
authentication_provider = client.authentication_providers.delete(
    "id",
)
print(authentication_provider.data)
```

## 列出所有计费组

获取您的所有计费组列表。

`GET /billing_groups`

```python
page = client.billing_groups.list()
page = page.data[0]
print(page.id)
```

## 创建计费组

创建一个新的计费组。

`POST /billing_groups`

```python
billing_group = client.billing_groups.create(
    name="string",
)
print(billing_group.data)
```

## 获取计费组信息

获取指定计费组的详细信息。

`GET /billing_groups/{id}`

```python
billing_group = client.billing_groups.retrieve(
    "f5586561-8ff0-4291-a0ac-84fe544797bd",
)
print(billing_group.data)
```

## 更新计费组设置

更新现有计费组的设置。

`PATCH /billing_groups/{id}`

```python
billing_group = client.billing_groups.update(
    id="f5586561-8ff0-4291-a0ac-84fe544797bd",
    name="string",
)
print(billing_group.data)
```

## 删除计费组

删除现有的计费组。

`DELETE /billing_groups/{id}`

```python
billing_group = client.billing_groups.delete(
    "f5586561-8ff0-4291-a0ac-84fe544797bd",
)
print(billing_group.data)
```

## 列出所有集成密钥

获取用户配置的所有集成密钥列表。

`GET /integration_secrets`

```python
page = client.integration_secrets.list()
page = page.data[0]
print(page.id)
```

## 创建集成密钥

创建一个新的集成密钥，并为其指定一个标识符，以便与其他服务安全地集成。

`POST /integration_secrets` — 必需参数：`identifier`（标识符）、`type`（类型）

```python
integration_secret = client.integration_secrets.create(
    identifier="my_secret",
    type="bearer",
    token="my_secret_value",
)
print(integration_secret.data)
```

## 删除集成密钥

根据 ID 删除指定的集成密钥。

`DELETE /integration_secrets/{id}`

```python
client.integration_secrets.delete(
    "id",
)
```

## 列出所有访问 IP 地址

获取您的所有访问 IP 地址列表。

`GET /access_ip_address`

```python
page = client.access_ip_address.list()
page = page.data[0]
print(page.id)
```

## 创建新的访问 IP 地址

创建一个新的访问 IP 地址。

`POST /access_ip_address` — 必需参数：`ip_address`（IP 地址）

```python
access_ip_address_response = client.access_ip_address.create(
    ip_address="ip_address",
)
print(access_ip_address_response.id)
```

## 查取访问 IP 地址信息

获取指定访问 IP 地址的详细信息。

`GET /access_ip_address/{access_ip_address_id}`

```python
access_ip_address_response = client.access_ip_address.retrieve(
    "access_ip_address_id",
)
print(access_ip_address_response.id)
```

## 删除访问 IP 地址

删除指定的访问 IP 地址。

`DELETE /access_ip_address/{access_ip_address_id}`

```python
access_ip_address_response = client.access_ip_address.delete(
    "access_ip_address_id",
)
print(access_ip_address_response.id)
```

## 列出所有访问 IP 范围

获取您的所有访问 IP 范围列表。

`GET /access_ip_ranges`

```python
page = client.access_ip_ranges.list()
page = page.data[0]
print(page.id)
```

## 创建新的访问 IP 范围

创建一个新的访问 IP 范围。

`POST /access_ip_ranges` — 必需参数：`cidr_block`（IP 范围）

```python
access_ip_range = client.access_ip_ranges.create(
    cidr_block="cidr_block",
)
print(access_ip_range.id)
```

## 删除访问 IP 范围

删除指定的访问 IP 范围。

`DELETE /access_ip_ranges/{access_ip_range_id}`

```python
access_ip_range = client.access_ip_ranges.delete(
    "access_ip_range_id",
)
print(access_ip_range.id)
```