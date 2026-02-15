---
name: telnyx-oauth-python
description: >-
  Implement OAuth 2.0 authentication flows for Telnyx API access. This skill
  provides Python SDK examples.
metadata:
  author: telnyx
  product: oauth
  language: python
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx Oauth - Python

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

## 授权服务器元数据

OAuth 2.0 授权服务器元数据 (RFC 8414)

`GET /.well-known/oauth-authorization-server`

```python
response = client.well_known.retrieve_authorization_server_metadata()
print(response.authorization_endpoint)
```

## 受保护资源元数据

用于资源发现的 OAuth 2.0 受保护资源元数据

`GET /.well-known/oauth-protected-resource`

```python
response = client.well_known.retrieve_protected_resource_metadata()
print(response.authorization_servers)
```

## OAuth 授权端点

用于授权码流程的 OAuth 2.0 授权端点

`GET /oauth/authorize`

```python
client.oauth.retrieve_authorize(
    client_id="client_id",
    redirect_uri="https://example.com",
    response_type="code",
)
```

## 列出 OAuth 客户端

获取已认证用户的 OAuth 客户端列表（分页显示）

`GET /oauth/clients`

```python
page = client.oauth_clients.list()
page = page.data[0]
print(page.client_id)
```

## 创建 OAuth 客户端

创建一个新的 OAuth 客户端

`POST /oauth/clients` — 必需参数：`name`, `allowed_scopes`, `client_type`, `allowed_grant_types`

```python
oauth_client = client.oauth_clients.create(
    allowed_grant_types=["client_credentials"],
    allowed_scopes=["admin"],
    client_type="public",
    name="My OAuth client",
)
print(oauth_client.data)
```

## 获取 OAuth 客户端信息

通过 ID 获取单个 OAuth 客户端的信息

`GET /oauth/clients/{id}`

```python
oauth_client = client.oauth_clients.retrieve(
    "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(oauth_client.data)
```

## 更新 OAuth 客户端

更新现有的 OAuth 客户端

`PUT /oauth/clients/{id}`

```python
oauth_client = client.oauth_clients.update(
    id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(oauth_client.data)
```

## 删除 OAuth 客户端

删除一个 OAuth 客户端

`DELETE /oauth/clients/{id}`

```python
client.oauth_clients.delete(
    "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
```

## 获取 OAuth 同意令牌

获取 OAuth 同意令牌的详细信息

`GET /oauth/consent/{consent_token}`

```python
oauth = client.oauth.retrieve(
    "consent_token",
)
print(oauth.data)
```

## 列出 OAuth 授权令牌

获取已认证用户的 OAuth 授权令牌列表（分页显示）

`GET /oauth/grants`

```python
page = client.oauth_grants.list()
page = page.data[0]
print(page.id)
```

## 获取 OAuth 授权令牌

通过 ID 获取单个 OAuth 授权令牌的信息

`GET /oauth/grants/{id}`

```python
oauth_grant = client.oauth_grants.retrieve(
    "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(oauth_grant.data)
```

## 撤销 OAuth 授权令牌

撤销一个 OAuth 授权令牌

`DELETE /oauth/grants/{id}`

```python
oauth_grant = client.oauth_grants.delete(
    "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(oauth_grant.data)
```

## 令牌检查

检查 OAuth 访问令牌的有效性和元数据

`POST /oauth/introspect` — 必需参数：`token`

```python
response = client.oauth.introspect(
    token="token",
)
print(response.client_id)
```

## JSON Web Key Set

获取用于令牌验证的 JSON Web Key Set

`GET /oauth/jwks`

```python
response = client.oauth.retrieve_jwks()
print(response.keys)
```

## 动态客户端注册

动态注册一个新的 OAuth 客户端 (RFC 7591)

`POST /oauth/register`

```python
response = client.oauth.register()
print(response.client_id)
```

## OAuth 令牌端点

交换授权码、客户端凭据或刷新令牌以获取访问令牌

`POST /oauth/token` — 必需参数：`grant_type`

```python
response = client.oauth.token(
    grant_type="client_credentials",
)
print(response.access_token)
```
```