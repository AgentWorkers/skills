---
name: telnyx-oauth-ruby
description: >-
  Implement OAuth 2.0 authentication flows for Telnyx API access. This skill
  provides Ruby SDK examples.
metadata:
  author: telnyx
  product: oauth
  language: ruby
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx Oauth - Ruby

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

以下所有示例均假设 `client` 已按照上述方式初始化。

## 授权服务器元数据

OAuth 2.0 授权服务器元数据（RFC 8414）

`GET /.well-known/oauth-authorization-server`

```ruby
response = client.well_known.retrieve_authorization_server_metadata

puts(response)
```

## 受保护资源元数据

用于资源发现的 OAuth 2.0 受保护资源元数据

`GET /.well-known/oauth-protected-resource`

```ruby
response = client.well_known.retrieve_protected_resource_metadata

puts(response)
```

## OAuth 授权端点

用于授权代码流程的 OAuth 2.0 授权端点

`GET /oauth/authorize`

```ruby
result = client.oauth.retrieve_authorize(
  client_id: "client_id",
  redirect_uri: "https://example.com",
  response_type: :code
)

puts(result)
```

## 列出 OAuth 客户端

检索已认证用户的 OAuth 客户端列表（分页显示）

`GET /oauth/clients`

```ruby
page = client.oauth_clients.list

puts(page)
```

## 创建 OAuth 客户端

创建一个新的 OAuth 客户端

`POST /oauth/clients` — 必需参数：`name`、`allowed_scopes`、`client_type`、`allowed_grant_types`

```ruby
oauth_client = client.oauth_clients.create(
  allowed_grant_types: [:client_credentials],
  allowed_scopes: ["admin"],
  client_type: :public,
  name: "My OAuth client"
)

puts(oauth_client)
```

## 获取 OAuth 客户端信息

通过 ID 检索单个 OAuth 客户端的信息

`GET /oauth/clients/{id}`

```ruby
oauth_client = client.oauth_clients.retrieve("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(oauth_client)
```

## 更新 OAuth 客户端

更新现有的 OAuth 客户端

`PUT /oauth/clients/{id}`

```ruby
oauth_client = client.oauth_clients.update("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(oauth_client)
```

## 删除 OAuth 客户端

删除一个 OAuth 客户端

`DELETE /oauth/clients/{id}`

```ruby
result = client.oauth_clients.delete("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(result)
```

## 获取 OAuth 同意令牌

检索 OAuth 同意令牌的详细信息

`GET /oauth/consent/{consent_token}`

```ruby
oauth = client.oauth.retrieve("consent_token")

puts(oauth)
```

## 列出 OAuth 授权令牌

检索已认证用户的 OAuth 授权令牌列表（分页显示）

`GET /oauth/grants`

```ruby
page = client.oauth_grants.list

puts(page)
```

## 获取 OAuth 授权令牌

通过 ID 检索单个 OAuth 授权令牌

`GET /oauth/grants/{id}`

```ruby
oauth_grant = client.oauth_grants.retrieve("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(oauth_grant)
```

## 撤销 OAuth 授权令牌

撤销一个 OAuth 授权令牌

`DELETE /oauth/grants/{id}`

```ruby
oauth_grant = client.oauth_grants.delete("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(oauth_grant)
```

## 令牌验证

验证 OAuth 访问令牌的有效性及元数据

`POST /oauth/introspect` — 必需参数：`token`

```ruby
response = client.oauth.introspect(token: "token")

puts(response)
```

## JSON Web Key Set

检索用于令牌验证的 JSON Web Key Set

`GET /oauth/jwks`

```ruby
response = client.oauth.retrieve_jwks

puts(response)
```

## 动态客户端注册

动态注册一个新的 OAuth 客户端（RFC 7591）

`POST /oauth/register`

```ruby
response = client.oauth.register

puts(response)
```

## OAuth 令牌端点

用于交换授权代码、客户端凭证或刷新访问令牌

`POST /oauth/token` — 必需参数：`grant_type`

```ruby
response = client.oauth.token(grant_type: :client_credentials)

puts(response)
```