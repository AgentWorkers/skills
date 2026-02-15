---
name: telnyx-account-access-java
description: >-
  Configure account addresses, authentication providers, IP access controls,
  billing groups, and integration secrets. This skill provides Java SDK
  examples.
metadata:
  author: telnyx
  product: account-access
  language: java
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 账户访问 - Java

## 安装

```text
// See https://github.com/team-telnyx/telnyx-java for Maven/Gradle setup
```

## 设置

```java
import com.telnyx.sdk.client.TelnyxClient;
import com.telnyx.sdk.client.okhttp.TelnyxOkHttpClient;

TelnyxClient client = TelnyxOkHttpClient.fromEnv();
```

以下所有示例均假设 `client` 已按照上述方式初始化。

## 列出所有地址

返回您的地址列表。

`GET /addresses`

```java
import com.telnyx.sdk.models.addresses.AddressListPage;
import com.telnyx.sdk.models.addresses.AddressListParams;

AddressListPage page = client.addresses().list();
```

## 创建地址

创建一个新的地址。

`POST /addresses` — 必需参数：`first_name`、`last_name`、`business_name`、`street_address`、`locality`、`country_code`

```java
import com.telnyx.sdk.models.addresses.AddressCreateParams;
import com.telnyx.sdk.models.addresses.AddressCreateResponse;

AddressCreateParams params = AddressCreateParams.builder()
    .businessName("Toy-O'Kon")
    .countryCode("US")
    .firstName("Alfred")
    .lastName("Foster")
    .locality("Austin")
    .streetAddress("600 Congress Avenue")
    .build();
AddressCreateResponse address = client.addresses().create(params);
```

## 获取地址详情

获取现有地址的详细信息。

`GET /addresses/{id}`

```java
import com.telnyx.sdk.models.addresses.AddressRetrieveParams;
import com.telnyx.sdk.models.addresses.AddressRetrieveResponse;

AddressRetrieveResponse address = client.addresses().retrieve("id");
```

## 删除地址

删除现有的地址。

`DELETE /addresses/{id}`

```java
import com.telnyx.sdk.models.addresses.AddressDeleteParams;
import com.telnyx.sdk.models.addresses.AddressDeleteResponse;

AddressDeleteResponse address = client.addresses().delete("id");
```

## 接受此地址建议作为新的紧急联系方式，并完成将其相关信息上传至 Microsoft 的操作。

`POST /addresses/{id}/actions/accept_suggestions`

```java
import com.telnyx.sdk.models.addresses.actions.ActionAcceptSuggestionsParams;
import com.telnyx.sdk.models.addresses.actions.ActionAcceptSuggestionsResponse;

ActionAcceptSuggestionsResponse response = client.addresses().actions().acceptSuggestions("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 验证地址

验证地址是否适用于紧急服务。

`POST /addresses/actions/validate` — 必需参数：`country_code`、`street_address`、`postal_code`

```java
import com.telnyx.sdk.models.addresses.actions.ActionValidateParams;
import com.telnyx.sdk.models.addresses.actions.ActionValidateResponse;

ActionValidateParams params = ActionValidateParams.builder()
    .countryCode("US")
    .postalCode("78701")
    .streetAddress("600 Congress Avenue")
    .build();
ActionValidateResponse response = client.addresses().actions().validate(params);
```

## 列出所有 SSO（单点登录）认证提供者

返回您的 SSO 认证提供者列表。

`GET /authentication_providers`

```java
import com.telnyx.sdk.models.authenticationproviders.AuthenticationProviderListPage;
import com.telnyx.sdk.models.authenticationproviders.AuthenticationProviderListParams;

AuthenticationProviderListPage page = client.authenticationProviders().list();
```

## 创建认证提供者

创建一个新的认证提供者。

`POST /authentication_providers` — 必需参数：`name`、`short_name`、`settings`

```java
import com.telnyx.sdk.models.authenticationproviders.AuthenticationProviderCreateParams;
import com.telnyx.sdk.models.authenticationproviders.AuthenticationProviderCreateResponse;
import com.telnyx.sdk.models.authenticationproviders.Settings;

AuthenticationProviderCreateParams params = AuthenticationProviderCreateParams.builder()
    .name("Okta")
    .settings(Settings.builder()
        .idpCertFingerprint("13:38:C7:BB:C9:FF:4A:70:38:3A:E3:D9:5C:CD:DB:2E:50:1E:80:A7")
        .idpEntityId("https://myorg.myidp.com/saml/metadata")
        .idpSsoTargetUrl("https://myorg.myidp.com/trust/saml2/http-post/sso")
        .build())
    .shortName("myorg")
    .build();
AuthenticationProviderCreateResponse authenticationProvider = client.authenticationProviders().create(params);
```

## 获取认证提供者详情

获取现有认证提供者的详细信息。

`GET /authentication_providers/{id}`

```java
import com.telnyx.sdk.models.authenticationproviders.AuthenticationProviderRetrieveParams;
import com.telnyx.sdk.models.authenticationproviders.AuthenticationProviderRetrieveResponse;

AuthenticationProviderRetrieveResponse authenticationProvider = client.authenticationProviders().retrieve("id");
```

## 更新认证提供者

更新现有认证提供者的设置。

`PATCH /authentication_providers/{id}`

```java
import com.telnyx.sdk.models.authenticationproviders.AuthenticationProviderUpdateParams;
import com.telnyx.sdk.models.authenticationproviders.AuthenticationProviderUpdateResponse;

AuthenticationProviderUpdateResponse authenticationProvider = client.authenticationProviders().update("id");
```

## 删除认证提供者

删除现有的认证提供者。

`DELETE /authentication_providers/{id}`

```java
import com.telnyx.sdk.models.authenticationproviders.AuthenticationProviderDeleteParams;
import com.telnyx.sdk.models.authenticationproviders.AuthenticationProviderDeleteResponse;

AuthenticationProviderDeleteResponse authenticationProvider = client.authenticationProviders().delete("id");
```

## 列出所有计费组

获取您的计费组列表。

`GET /billing_groups`

```java
import com.telnyx.sdk.models.billinggroups.BillingGroupListPage;
import com.telnyx.sdk.models.billinggroups.BillingGroupListParams;

BillingGroupListPage page = client.billingGroups().list();
```

## 创建计费组

创建一个新的计费组。

`POST /billing_groups`

```java
import com.telnyx.sdk.models.billinggroups.BillingGroupCreateParams;
import com.telnyx.sdk.models.billinggroups.BillingGroupCreateResponse;

BillingGroupCreateResponse billingGroup = client.billingGroups().create();
```

## 获取计费组详情

获取特定计费组的详细信息。

`GET /billing_groups/{id}`

```java
import com.telnyx.sdk.models.billinggroups.BillingGroupRetrieveParams;
import com.telnyx.sdk.models.billinggroups.BillingGroupRetrieveResponse;

BillingGroupRetrieveResponse billingGroup = client.billingGroups().retrieve("f5586561-8ff0-4291-a0ac-84fe544797bd");
```

## 更新计费组

更新现有计费组的设置。

`PATCH /billing_groups/{id}`

```java
import com.telnyx.sdk.models.billinggroups.BillingGroupUpdateParams;
import com.telnyx.sdk.models.billinggroups.BillingGroupUpdateResponse;

BillingGroupUpdateResponse billingGroup = client.billingGroups().update("f5586561-8ff0-4291-a0ac-84fe544797bd");
```

## 删除计费组

删除现有的计费组。

`DELETE /billing_groups/{id}`

```java
import com.telnyx.sdk.models.billinggroups.BillingGroupDeleteParams;
import com.telnyx.sdk.models.billinggroups.BillingGroupDeleteResponse;

BillingGroupDeleteResponse billingGroup = client.billingGroups().delete("f5586561-8ff0-4291-a0ac-84fe544797bd");
```

## 列出所有集成密钥

获取用户配置的所有集成密钥列表。

`GET /integration_secrets`

```java
import com.telnyx.sdk.models.integrationsecrets.IntegrationSecretListPage;
import com.telnyx.sdk.models.integrationsecrets.IntegrationSecretListParams;

IntegrationSecretListPage page = client.integrationSecrets().list();
```

## 创建集成密钥

创建一个新的集成密钥，并为其指定一个标识符，以便与其他服务安全地集成。

`POST /integration_secrets` — 必需参数：`identifier`、`type`

```java
import com.telnyx.sdk.models.integrationsecrets.IntegrationSecretCreateParams;
import com.telnyx.sdk.models.integrationsecrets.IntegrationSecretCreateResponse;

IntegrationSecretCreateParams params = IntegrationSecretCreateParams.builder()
    .identifier("my_secret")
    .type(IntegrationSecretCreateParams.Type.BEARER)
    .build();
IntegrationSecretCreateResponse integrationSecret = client.integrationSecrets().create(params);
```

## 删除集成密钥

根据密钥 ID 删除相应的集成密钥。

`DELETE /integration_secrets/{id}`

```java
import com.telnyx.sdk.models.integrationsecrets.IntegrationSecretDeleteParams;

client.integrationSecrets().delete("id");
```

## 列出所有访问 IP 地址

获取您的访问 IP 地址列表。

`GET /access_ip_address`

```java
import com.telnyx.sdk.models.accessipaddress.AccessIpAddressListPage;
import com.telnyx.sdk.models.accessipaddress.AccessIpAddressListParams;

AccessIpAddressListPage page = client.accessIpAddress().list();
```

## 创建新的访问 IP 地址

创建一个新的访问 IP 地址。

`POST /access_ip_address` — 必需参数：`ip_address`

```java
import com.telnyx.sdk.models.accessipaddress.AccessIpAddressCreateParams;
import com.telnyx.sdk.models.accessipaddress.AccessIpAddressResponse;

AccessIpAddressCreateParams params = AccessIpAddressCreateParams.builder()
    .ipAddress("ip_address")
    .build();
AccessIpAddressResponse accessIpAddressResponse = client.accessIpAddress().create(params);
```

## 获取访问 IP 地址详情

获取特定访问 IP 地址的详细信息。

`GET /access_ip_address/{access_ip_address_id}`

```java
import com.telnyx.sdk.models.accessipaddress.AccessIpAddressResponse;
import com.telnyx.sdk.models.accessipaddress.AccessIpAddressRetrieveParams;

AccessIpAddressResponse accessIpAddressResponse = client.accessIpAddress().retrieve("access_ip_address_id");
```

## 删除访问 IP 地址

删除指定的访问 IP 地址。

`DELETE /access_ip_address/{access_ip_address_id}`

```java
import com.telnyx.sdk.models.accessipaddress.AccessIpAddressDeleteParams;
import com.telnyx.sdk.models.accessipaddress.AccessIpAddressResponse;

AccessIpAddressResponse accessIpAddressResponse = client.accessIpAddress().delete("access_ip_address_id");
```

## 列出所有访问 IP 范围

获取您的访问 IP 范围列表。

`GET /access_ip_ranges`

```java
import com.telnyx.sdk.models.accessipranges.AccessIpRangeListPage;
import com.telnyx.sdk.models.accessipranges.AccessIpRangeListParams;

AccessIpRangeListPage page = client.accessIpRanges().list();
```

## 创建新的访问 IP 范围

创建一个新的访问 IP 范围。

`POST /access_ipRanges` — 必需参数：`cidr_block`

```java
import com.telnyx.sdk.models.accessipranges.AccessIpRange;
import com.telnyx.sdk.models.accessipranges.AccessIpRangeCreateParams;

AccessIpRangeCreateParams params = AccessIpRangeCreateParams.builder()
    .cidrBlock("cidr_block")
    .build();
AccessIpRange accessIpRange = client.accessIpRanges().create(params);
```

## 删除访问 IP 范围

删除指定的访问 IP 范围。

`DELETE /access_ip_ranges/{access_ip_range_id}`

```java
import com.telnyx.sdk.models.accessipranges.AccessIpRange;
import com.telnyx.sdk.models.accessipranges.AccessIpRangeDeleteParams;

AccessIpRange accessIpRange = client.accessIpRanges().delete("access_ip_range_id");
```