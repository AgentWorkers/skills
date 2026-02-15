---
name: telnyx-account-access-javascript
description: >-
  Configure account addresses, authentication providers, IP access controls,
  billing groups, and integration secrets. This skill provides JavaScript SDK
  examples.
metadata:
  author: telnyx
  product: account-access
  language: javascript
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 账户访问 - JavaScript

## 安装

```bash
npm install telnyx
```

## 设置

```javascript
import Telnyx from 'telnyx';

const client = new Telnyx({
  apiKey: process.env['TELNYX_API_KEY'], // This is the default and can be omitted
});
```

以下所有示例均假设 `client` 已按照上述方式初始化。

## 列出所有地址

返回您的地址列表。

`GET /addresses`

```javascript
// Automatically fetches more pages as needed.
for await (const address of client.addresses.list()) {
  console.log(address.id);
}
```

## 创建地址

创建一个新的地址。

`POST /addresses` — 必需参数：`first_name`（名字）、`last_name`（姓氏）、`business_name`（企业名称）、`street_address`（街道地址）、`locality`（地理位置）、`country_code`（国家代码）

```javascript
const address = await client.addresses.create({
  business_name: "Toy-O'Kon",
  country_code: 'US',
  first_name: 'Alfred',
  last_name: 'Foster',
  locality: 'Austin',
  street_address: '600 Congress Avenue',
});

console.log(address.data);
```

## 查取地址信息

获取现有地址的详细信息。

`GET /addresses/{id}`

```javascript
const address = await client.addresses.retrieve('id');

console.log(address.data);
```

## 删除地址

删除现有的地址。

`DELETE /addresses/{id}`

```javascript
const address = await client.addresses.delete('id');

console.log(address.data);
```

## 接受此地址建议作为新的紧急联系地址，并完成将其相关信息上传至 Microsoft 的操作

`POST /addresses/{id}/actions/accept_suggestions`

```javascript
const response = await client.addresses.actions.acceptSuggestions(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
);

console.log(response.data);
```

## 验证地址

验证地址是否适合用于紧急服务。

`POST /addresses/actions/validate` — 必需参数：`country_code`（国家代码）、`street_address`（街道地址）、`postal_code`（邮政编码）

```javascript
const response = await client.addresses.actions.validate({
  country_code: 'US',
  postal_code: '78701',
  street_address: '600 Congress Avenue',
});

console.log(response.data);
```

## 列出所有 SSO（单点登录）认证提供者

返回您的所有 SSO 认证提供者列表。

`GET /authentication_providers`

```javascript
// Automatically fetches more pages as needed.
for await (const authenticationProvider of client.authenticationProviders.list()) {
  console.log(authenticationProvider.id);
}
```

## 创建认证提供者

创建一个新的认证提供者。

`POST /authentication_providers` — 必需参数：`name`（名称）、`short_name`（简称）、`settings`（设置）

```javascript
const authenticationProvider = await client.authenticationProviders.create({
  name: 'Okta',
  settings: {
    idp_cert_fingerprint: '13:38:C7:BB:C9:FF:4A:70:38:3A:E3:D9:5C:CD:DB:2E:50:1E:80:A7',
    idp_entity_id: 'https://myorg.myidp.com/saml/metadata',
    idp_sso_target_url: 'https://myorg.myidp.com/trust/saml2/http-post/sso',
  },
  short_name: 'myorg',
});

console.log(authenticationProvider.data);
```

## 查取认证提供者信息

获取现有认证提供者的详细信息。

`GET /authentication_providers/{id}`

```javascript
const authenticationProvider = await client.authenticationProviders.retrieve('id');

console.log(authenticationProvider.data);
```

## 更新认证提供者设置

更新现有认证提供者的设置。

`PATCH /authentication_providers/{id}`

```javascript
const authenticationProvider = await client.authenticationProviders.update('id', {
  active: true,
  name: 'Okta',
  settings: {
    idp_entity_id: 'https://myorg.myidp.com/saml/metadata',
    idp_sso_target_url: 'https://myorg.myidp.com/trust/saml2/http-post/sso',
    idp_cert_fingerprint: '13:38:C7:BB:C9:FF:4A:70:38:3A:E3:D9:5C:CD:DB:2E:50:1E:80:A7',
    idp_cert_fingerprint_algorithm: 'sha1',
  },
  short_name: 'myorg',
});

console.log(authenticationProvider.data);
```

## 删除认证提供者

删除现有的认证提供者。

`DELETE /authentication_providers/{id}`

```javascript
const authenticationProvider = await client.authenticationProviders.delete('id');

console.log(authenticationProvider.data);
```

## 列出所有计费组

获取您的所有计费组列表。

`GET /billing_groups`

```javascript
// Automatically fetches more pages as needed.
for await (const billingGroup of client.billingGroups.list()) {
  console.log(billingGroup.id);
}
```

## 创建计费组

创建一个新的计费组。

`POST /billing_groups`

```javascript
const billingGroup = await client.billingGroups.create({ name: 'string' });

console.log(billingGroup.data);
```

## 获取计费组信息

获取特定计费组的详细信息。

`GET /billing_groups/{id}`

```javascript
const billingGroup = await client.billingGroups.retrieve('f5586561-8ff0-4291-a0ac-84fe544797bd');

console.log(billingGroup.data);
```

## 更新计费组设置

更新现有计费组的设置。

`PATCH /billing_groups/{id}`

```javascript
const billingGroup = await client.billingGroups.update('f5586561-8ff0-4291-a0ac-84fe544797bd', {
  name: 'string',
});

console.log(billingGroup.data);
```

## 删除计费组

删除现有的计费组。

`DELETE /billing_groups/{id}`

```javascript
const billingGroup = await client.billingGroups.delete('f5586561-8ff0-4291-a0ac-84fe544797bd');

console.log(billingGroup.data);
```

## 列出所有集成密钥

获取用户配置的所有集成密钥列表。

`GET /integration_secrets`

```javascript
// Automatically fetches more pages as needed.
for await (const integrationSecret of client.integrationSecrets.list()) {
  console.log(integrationSecret.id);
}
```

## 创建集成密钥

创建一个新的集成密钥，并为其指定一个标识符，以便与其他服务安全集成。

`POST /integration_secrets` — 必需参数：`identifier`（标识符）、`type`（类型）

```javascript
const integrationSecret = await client.integrationSecrets.create({
  identifier: 'my_secret',
  type: 'bearer',
  token: 'my_secret_value',
});

console.log(integrationSecret.data);
```

## 删除集成密钥

根据 ID 删除指定的集成密钥。

`DELETE /integration_secrets/{id}`

```javascript
await client.integrationSecrets.delete('id');
```

## 列出所有访问 IP 地址

获取您的所有访问 IP 地址列表。

`GET /access_ip_address`

```javascript
// Automatically fetches more pages as needed.
for await (const accessIPAddressResponse of client.accessIPAddress.list()) {
  console.log(accessIPAddressResponse.id);
}
```

## 创建新的访问 IP 地址

创建一个新的访问 IP 地址。

`POST /access_ip_address` — 必需参数：`ip_address`（IP 地址）

```javascript
const accessIPAddressResponse = await client.accessIPAddress.create({ ip_address: 'ip_address' });

console.log(accessIPAddressResponse.id);
```

## 获取访问 IP 地址信息

获取特定访问 IP 地址的详细信息。

`GET /access_ip_address/{access_ip_address_id}`

```javascript
const accessIPAddressResponse = await client.accessIPAddress.retrieve('access_ip_address_id');

console.log(accessIPAddressResponse.id);
```

## 删除访问 IP 地址

删除指定的访问 IP 地址。

`DELETE /access_ip_address/{access_ip_address_id}`

```javascript
const accessIPAddressResponse = await client.accessIPAddress.delete('access_ip_address_id');

console.log(accessIPAddressResponse.id);
```

## 列出所有访问 IP 范围

获取您的所有访问 IP 范围列表。

`GET /access_ip_ranges`

```javascript
// Automatically fetches more pages as needed.
for await (const accessIPRange of client.accessIPRanges.list()) {
  console.log(accessIPRange.id);
}
```

## 创建新的访问 IP 范围

创建一个新的访问 IP 范围。

`POST /access_ip_ranges` — 必需参数：`cidr_block`（IP 范围）

```javascript
const accessIPRange = await client.accessIPRanges.create({ cidr_block: 'cidr_block' });

console.log(accessIPRange.id);
```

## 删除访问 IP 范围

删除指定的访问 IP 范围。

`DELETE /access_ip_ranges/{access_ip_range_id}`

```javascript
const accessIPRange = await client.accessIPRanges.delete('access_ip_range_id');

console.log(accessIPRange.id);
```