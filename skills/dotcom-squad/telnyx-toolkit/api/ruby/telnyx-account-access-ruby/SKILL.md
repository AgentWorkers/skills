---
name: telnyx-account-access-ruby
description: >-
  Configure account addresses, authentication providers, IP access controls,
  billing groups, and integration secrets. This skill provides Ruby SDK
  examples.
metadata:
  author: telnyx
  product: account-access
  language: ruby
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 账户访问 - Ruby

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

## 列出所有地址

返回您的地址列表。

`GET /addresses`

```ruby
page = client.addresses.list

puts(page)
```

## 创建地址

创建一个新的地址。

`POST /addresses` — 必需参数：`first_name`（名字）、`last_name`（姓氏）、`business_name`（公司名称）、`street_address`（街道地址）、`locality`（地区）、`country_code`（国家代码）

```ruby
address = client.addresses.create(
  business_name: "Toy-O'Kon",
  country_code: "US",
  first_name: "Alfred",
  last_name: "Foster",
  locality: "Austin",
  street_address: "600 Congress Avenue"
)

puts(address)
```

## 获取地址详情

获取现有地址的详细信息。

`GET /addresses/{id}`

```ruby
address = client.addresses.retrieve("id")

puts(address)
```

## 删除地址

删除现有的地址。

`DELETE /addresses/{id}`

```ruby
address = client.addresses.delete("id")

puts(address)
```

## 接受此地址建议作为 Operator Connect 的新紧急联系人地址，并完成将其相关号码上传至 Microsoft 的操作。

`POST /addresses/{id}/actions/accept_suggestions`

```ruby
response = client.addresses.actions.accept_suggestions("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(response)
```

## 验证地址

验证地址是否适合用于紧急服务。

`POST /addresses/actions/validate` — 必需参数：`country_code`（国家代码）、`street_address`（街道地址）、`postal_code`（邮政编码）

```ruby
response = client.addresses.actions.validate(
  country_code: "US",
  postal_code: "78701",
  street_address: "600 Congress Avenue"
)

puts(response)
```

## 列出所有 SSO（单点登录）认证提供者

返回您的 SSO 认证提供者列表。

`GET /authentication_providers`

```ruby
page = client.authentication_providers.list

puts(page)
```

## 创建认证提供者

创建一个新的认证提供者。

`POST /authentication_providers` — 必需参数：`name`（名称）、`short_name`（简称）、`settings`（设置）

```ruby
authentication_provider = client.authentication_providers.create(
  name: "Okta",
  settings: {
    idp_cert_fingerprint: "13:38:C7:BB:C9:FF:4A:70:38:3A:E3:D9:5C:CD:DB:2E:50:1E:80:A7",
    idp_entity_id: "https://myorg.myidp.com/saml/metadata",
    idp_sso_target_url: "https://myorg.myidp.com/trust/saml2/http-post/sso"
  },
  short_name: "myorg"
)

puts(authentication_provider)
```

## 获取认证提供者详情

获取现有认证提供者的详细信息。

`GET /authentication_providers/{id}`

```ruby
authentication_provider = client.authentication_providers.retrieve("id")

puts(authentication_provider)
```

## 更新认证提供者设置

更新现有认证提供者的设置。

`PATCH /authentication_providers/{id}`

```ruby
authentication_provider = client.authentication_providers.update("id")

puts(authentication_provider)
```

## 删除认证提供者

删除现有的认证提供者。

`DELETE /authentication_providers/{id}`

```ruby
authentication_provider = client.authentication_providers.delete("id")

puts(authentication_provider)
```

## 列出所有计费组

获取您的计费组列表。

`GET /billing_groups`

```ruby
page = client.billing_groups.list

puts(page)
```

## 创建计费组

创建一个新的计费组。

`POST /billing_groups`

```ruby
billing_group = client.billing_groups.create

puts(billing_group)
```

## 获取计费组详情

获取特定计费组的详细信息。

`GET /billing_groups/{id}`

```ruby
billing_group = client.billing_groups.retrieve("f5586561-8ff0-4291-a0ac-84fe544797bd")

puts(billing_group)
```

## 更新计费组设置

更新现有计费组的设置。

`PATCH /billing_groups/{id}`

```ruby
billing_group = client.billing_groups.update("f5586561-8ff0-4291-a0ac-84fe544797bd")

puts(billing_group)
```

## 删除计费组

删除现有的计费组。

`DELETE /billing_groups/{id}`

```ruby
billing_group = client.billing_groups.delete("f5586561-8ff0-4291-a0ac-84fe544797bd")

puts(billing_group)
```

## 列出所有集成密钥

获取用户配置的所有集成密钥列表。

`GET /integration_secrets`

```ruby
page = client.integration_secrets.list

puts(page)
```

## 创建集成密钥

创建一个新的集成密钥，并为其指定一个标识符，以便与其他服务安全地集成。

`POST /integration_secrets` — 必需参数：`identifier`（标识符）、`type`（类型）

```ruby
integration_secret = client.integration_secrets.create(identifier: "my_secret", type: :bearer)

puts(integration_secret)
```

## 删除集成密钥

根据 ID 删除指定的集成密钥。

`DELETE /integration_secrets/{id}`

```ruby
result = client.integration_secrets.delete("id")

puts(result)
```

## 列出所有访问 IP 地址

获取您的访问 IP 地址列表。

`GET /access_ip_address`

```ruby
page = client.access_ip_address.list

puts(page)
```

## 创建新的访问 IP 地址

创建一个新的访问 IP 地址。

`POST /access_ip_address` — 必需参数：`ip_address`（IP 地址）

```ruby
access_ip_address_response = client.access_ip_address.create(ip_address: "ip_address")

puts(access_ip_address_response)
```

## 获取访问 IP 地址详情

获取特定访问 IP 地址的详细信息。

`GET /access_ip_address/{access_ip_address_id}`

```ruby
access_ip_address_response = client.access_ip_address.retrieve("access_ip_address_id")

puts(access_ip_address_response)
```

## 删除访问 IP 地址

删除指定的访问 IP 地址。

`DELETE /access_ip_address/{access_ip_address_id}`

```ruby
access_ip_address_response = client.access_ip_address.delete("access_ip_address_id")

puts(access_ip_address_response)
```

## 列出所有访问 IP 范围

获取您的访问 IP 范围列表。

`GET /access_ip_ranges`

```ruby
page = client.access_ip_ranges.list

puts(page)
```

## 创建新的访问 IP 范围

创建一个新的访问 IP 范围。

`POST /access_ip_ranges` — 必需参数：`cidr_block`（IP 范围）

```ruby
access_ip_range = client.access_ip_ranges.create(cidr_block: "cidr_block")

puts(access_ip_range)
```

## 删除访问 IP 范围

删除指定的访问 IP 范围。

`DELETE /access_ip_ranges/{access_ip_range_id}`

```ruby
access_ip_range = client.access_ip_ranges.delete("access_ip_range_id")

puts(access_ip_range)
```