---
name: telnyx-oauth-go
description: >-
  Implement OAuth 2.0 authentication flows for Telnyx API access. This skill
  provides Go SDK examples.
metadata:
  author: telnyx
  product: oauth
  language: go
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx Oauth - Go

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

以下所有示例均假设 `client` 已经按照上述方式初始化。

## 授权服务器元数据

OAuth 2.0 授权服务器元数据（RFC 8414）

`GET /.well-known/oauth-authorization-server`

```go
	response, err := client.WellKnown.GetAuthorizationServerMetadata(context.TODO())
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.AuthorizationEndpoint)
```

## 受保护资源元数据

用于资源发现的 OAuth 2.0 受保护资源元数据

`GET /.well-known/oauth-protected-resource`

```go
	response, err := client.WellKnown.GetProtectedResourceMetadata(context.TODO())
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.AuthorizationServers)
```

## OAuth 授权端点

用于授权码流程的 OAuth 2.0 授权端点

`GET /oauth/authorize`

```go
	err := client.OAuth.GetAuthorize(context.TODO(), telnyx.OAuthGetAuthorizeParams{
		ClientID:     "client_id",
		RedirectUri:  "https://example.com",
		ResponseType: telnyx.OAuthGetAuthorizeParamsResponseTypeCode,
	})
	if err != nil {
		panic(err.Error())
	}
```

## 列出 OAuth 客户端

获取已认证用户的 OAuth 客户端列表（分页显示）

`GET /oauth/clients`

```go
	page, err := client.OAuthClients.List(context.TODO(), telnyx.OAuthClientListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建 OAuth 客户端

创建一个新的 OAuth 客户端

`POST /oauth/clients` — 必需参数：`name`、`allowed_scopes`、`client_type`、`allowed_grant_types`

```go
	oauthClient, err := client.OAuthClients.New(context.TODO(), telnyx.OAuthClientNewParams{
		AllowedGrantTypes: []string{"client_credentials"},
		AllowedScopes:     []string{"admin"},
		ClientType:        telnyx.OAuthClientNewParamsClientTypePublic,
		Name:              "My OAuth client",
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", oauthClient.Data)
```

## 获取 OAuth 客户端信息

通过 ID 获取单个 OAuth 客户端的信息

`GET /oauth/clients/{id}`

```go
	oauthClient, err := client.OAuthClients.Get(context.TODO(), "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", oauthClient.Data)
```

## 更新 OAuth 客户端

更新现有的 OAuth 客户端

`PUT /oauth/clients/{id}`

```go
	oauthClient, err := client.OAuthClients.Update(
		context.TODO(),
		"182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		telnyx.OAuthClientUpdateParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", oauthClient.Data)
```

## 删除 OAuth 客户端

删除一个 OAuth 客户端

`DELETE /oauth/clients/{id}`

```go
	err := client.OAuthClients.Delete(context.TODO(), "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
	if err != nil {
		panic(err.Error())
	}
```

## 获取 OAuth 同意令牌

获取 OAuth 同意令牌的详细信息

`GET /oauth/consent/{consent_token}`

```go
	oauth, err := client.OAuth.Get(context.TODO(), "consent_token")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", oauth.Data)
```

## 列出 OAuth 授权权限

获取已认证用户的 OAuth 授权权限列表（分页显示）

`GET /oauth/grants`

```go
	page, err := client.OAuthGrants.List(context.TODO(), telnyx.OAuthGrantListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 获取 OAuth 授权权限

通过 ID 获取单个 OAuth 授权权限

`GET /oauth/grants/{id}`

```go
	oauthGrant, err := client.OAuthGrants.Get(context.TODO(), "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", oauthGrant.Data)
```

## 撤销 OAuth 授权权限

撤销一个 OAuth 授权权限

`DELETE /oauth/grants/{id}`

```go
	oauthGrant, err := client.OAuthGrants.Delete(context.TODO(), "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", oauthGrant.Data)
```

## 令牌检查

检查 OAuth 访问令牌的有效性及其元数据

`POST /oauth/introspect` — 必需参数：`token`

```go
	response, err := client.OAuth.Introspect(context.TODO(), telnyx.OAuthIntrospectParams{
		Token: "token",
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.ClientID)
```

## JSON Web Key Set

获取用于令牌验证的 JSON Web Key Set

`GET /oauth/jwks`

```go
	response, err := client.OAuth.GetJwks(context.TODO())
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Keys)
```

## 动态客户端注册

动态注册一个新的 OAuth 客户端（RFC 7591）

`POST /oauth/register`

```go
	response, err := client.OAuth.Register(context.TODO(), telnyx.OAuthRegisterParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.ClientID)
```

## OAuth 令牌端点

用于交换授权码、客户端凭据或刷新访问令牌

`POST /oauth/token` — 必需参数：`grant_type`

```go
	response, err := client.OAuth.Token(context.TODO(), telnyx.OAuthTokenParams{
		GrantType: telnyx.OAuthTokenParamsGrantTypeClientCredentials,
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.AccessToken)
```