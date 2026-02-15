---
name: telnyx-account-access-go
description: >-
  Configure account addresses, authentication providers, IP access controls,
  billing groups, and integration secrets. This skill provides Go SDK examples.
metadata:
  author: telnyx
  product: account-access
  language: go
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 账户访问 - Go

## 安装

```bash
go get github.com/team-telnyx/telnyx-go
```

## 设置

```go
import (
  "context"
  "fmt"
  "os"

  "github.com/team-telnyx/telnyx-go"
  "github.com/team-telnyx/telnyx-go/option"
)

client := telnyx.NewClient(
  option.WithAPIKey(os.Getenv("TELNYX_API_KEY")),
)
```

以下所有示例均假设 `client` 已按照上述方式初始化。

## 列出所有地址

返回您的地址列表。

`GET /addresses`

```go
	page, err := client.Addresses.List(context.TODO(), telnyx.AddressListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建地址

创建一个新的地址。

`POST /addresses` — 必需参数：`first_name`、`last_name`、`business_name`、`street_address`、`locality`、`country_code`

```go
	address, err := client.Addresses.New(context.TODO(), telnyx.AddressNewParams{
		BusinessName:  "Toy-O'Kon",
		CountryCode:   "US",
		FirstName:     "Alfred",
		LastName:      "Foster",
		Locality:      "Austin",
		StreetAddress: "600 Congress Avenue",
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", address.Data)
```

## 查询地址信息

查询现有地址的详细信息。

`GET /addresses/{id}`

```go
	address, err := client.Addresses.Get(context.TODO(), "id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", address.Data)
```

## 删除地址

删除现有的地址。

`DELETE /addresses/{id}`

```go
	address, err := client.Addresses.Delete(context.TODO(), "id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", address.Data)
```

## 接受此地址建议作为新的紧急联系地址，并完成将其关联的号码上传至 Microsoft 的操作。

`POST /addresses/{id}/actions/accept_suggestions`

```go
	response, err := client.Addresses.Actions.AcceptSuggestions(
		context.TODO(),
		"182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		telnyx.AddressActionAcceptSuggestionsParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 验证地址

验证地址是否适合用于紧急服务。

`POST /addresses/actions/validate` — 必需参数：`country_code`、`street_address`、`postal_code`

```go
	response, err := client.Addresses.Actions.Validate(context.TODO(), telnyx.AddressActionValidateParams{
		CountryCode:   "US",
		PostalCode:    "78701",
		StreetAddress: "600 Congress Avenue",
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 列出所有 SSO（单点登录）认证提供者

返回您的所有 SSO 认证提供者列表。

`GET /authentication_providers`

```go
	page, err := client.AuthenticationProviders.List(context.TODO(), telnyx.AuthenticationProviderListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建认证提供者

创建一个新的认证提供者。

`POST /authentication_providers` — 必需参数：`name`、`short_name`、`settings`

```go
	authenticationProvider, err := client.AuthenticationProviders.New(context.TODO(), telnyx.AuthenticationProviderNewParams{
		Name: "Okta",
		Settings: telnyx.SettingsParam{
			IdpCertFingerprint: "13:38:C7:BB:C9:FF:4A:70:38:3A:E3:D9:5C:CD:DB:2E:50:1E:80:A7",
			IdpEntityID:        "https://myorg.myidp.com/saml/metadata",
			IdpSSOTargetURL:    "https://myorg.myidp.com/trust/saml2/http-post/sso",
		},
		ShortName: "myorg",
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", authenticationProvider.Data)
```

## 查询认证提供者信息

查询现有认证提供者的详细信息。

`GET /authentication_providers/{id}`

```go
	authenticationProvider, err := client.AuthenticationProviders.Get(context.TODO(), "id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", authenticationProvider.Data)
```

## 更新认证提供者设置

更新现有认证提供者的设置。

`PATCH /authentication_providers/{id}`

```go
	authenticationProvider, err := client.AuthenticationProviders.Update(
		context.TODO(),
		"id",
		telnyx.AuthenticationProviderUpdateParams{
			Active: telnyx.Bool(true),
			Name:   telnyx.String("Okta"),
			Settings: telnyx.SettingsParam{
				IdpEntityID:                 "https://myorg.myidp.com/saml/metadata",
				IdpSSOTargetURL:             "https://myorg.myidp.com/trust/saml2/http-post/sso",
				IdpCertFingerprint:          "13:38:C7:BB:C9:FF:4A:70:38:3A:E3:D9:5C:CD:DB:2E:50:1E:80:A7",
				IdpCertFingerprintAlgorithm: telnyx.SettingsIdpCertFingerprintAlgorithmSha1,
			},
			ShortName: telnyx.String("myorg"),
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", authenticationProvider.Data)
```

## 删除认证提供者

删除现有的认证提供者。

`DELETE /authentication_providers/{id}`

```go
	authenticationProvider, err := client.AuthenticationProviders.Delete(context.TODO(), "id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", authenticationProvider.Data)
```

## 列出所有计费组

返回您的所有计费组列表。

`GET /billing_groups`

```go
	page, err := client.BillingGroups.List(context.TODO(), telnyx.BillingGroupListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建计费组

创建一个新的计费组。

`POST /billing_groups`

```go
	billingGroup, err := client.BillingGroups.New(context.TODO(), telnyx.BillingGroupNewParams{
		Name: telnyx.String("string"),
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", billingGroup.Data)
```

## 获取计费组信息

查询特定计费组的详细信息。

`GET /billing_groups/{id}`

```go
	billingGroup, err := client.BillingGroups.Get(context.TODO(), "f5586561-8ff0-4291-a0ac-84fe544797bd")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", billingGroup.Data)
```

## 更新计费组设置

更新现有计费组的设置。

`PATCH /billing_groups/{id}`

```go
	billingGroup, err := client.BillingGroups.Update(
		context.TODO(),
		"f5586561-8ff0-4291-a0ac-84fe544797bd",
		telnyx.BillingGroupUpdateParams{
			Name: telnyx.String("string"),
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", billingGroup.Data)
```

## 删除计费组

删除现有的计费组。

`DELETE /billing_groups/{id}`

```go
	billingGroup, err := client.BillingGroups.Delete(context.TODO(), "f5586561-8ff0-4291-a0ac-84fe544797bd")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", billingGroup.Data)
```

## 列出所有集成密钥

获取用户配置的所有集成密钥列表。

`GET /integration_secrets`

```go
	page, err := client.IntegrationSecrets.List(context.TODO(), telnyx.IntegrationSecretListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建集成密钥

创建一个新的集成密钥，并为其指定一个标识符，以便与其他服务安全地集成。

`POST /integration_secrets` — 必需参数：`identifier`、`type`

```go
	integrationSecret, err := client.IntegrationSecrets.New(context.TODO(), telnyx.IntegrationSecretNewParams{
		Identifier: "my_secret",
		Type:       telnyx.IntegrationSecretNewParamsTypeBearer,
		Token:      telnyx.String("my_secret_value"),
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", integrationSecret.Data)
```

## 删除集成密钥

根据 ID 删除指定的集成密钥。

`DELETE /integration_secrets/{id}`

```go
	err := client.IntegrationSecrets.Delete(context.TODO(), "id")
	if err != nil {
		panic(err.Error())
	}
```

## 列出所有访问 IP 地址

获取您的所有访问 IP 地址列表。

`GET /access_ip_address`

```go
	page, err := client.AccessIPAddress.List(context.TODO(), telnyx.AccessIPAddressListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建新的访问 IP 地址

创建一个新的访问 IP 地址。

`POST /access_ip_address` — 必需参数：`ip_address`

```go
	accessIPAddressResponse, err := client.AccessIPAddress.New(context.TODO(), telnyx.AccessIPAddressNewParams{
		IPAddress: "ip_address",
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", accessIPAddressResponse.ID)
```

## 查询访问 IP 地址信息

查询特定访问 IP 地址的详细信息。

`GET /access_ip_address/{access_ip_address_id}`

```go
	accessIPAddressResponse, err := client.AccessIPAddress.Get(context.TODO(), "access_ip_address_id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", accessIPAddressResponse.ID)
```

## 删除访问 IP 地址

删除指定的访问 IP 地址。

`DELETE /access_ip_address/{access_ip_address_id}`

```go
	accessIPAddressResponse, err := client.AccessIPAddress.Delete(context.TODO(), "access_ip_address_id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", accessIPAddressResponse.ID)
```

## 列出所有访问 IP 范围

获取您的所有访问 IP 范围列表。

`GET /access_ip_ranges`

```go
	page, err := client.AccessIPRanges.List(context.TODO(), telnyx.AccessIPRangeListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建新的访问 IP 范围

创建一个新的访问 IP 范围。

`POST /access_ip_ranges` — 必需参数：`cidr_block`

```go
	accessIPRange, err := client.AccessIPRanges.New(context.TODO(), telnyx.AccessIPRangeNewParams{
		CidrBlock: "cidr_block",
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", accessIPRange.ID)
```

## 删除访问 IP 范围

删除指定的访问 IP 范围。

`DELETE /access_ip_ranges/{access_ip_range_id}`

```go
	accessIPRange, err := client.AccessIPRanges.Delete(context.TODO(), "access_ip_range_id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", accessIPRange.ID)
```