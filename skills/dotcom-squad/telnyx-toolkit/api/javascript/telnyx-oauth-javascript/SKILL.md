---
name: telnyx-oauth-javascript
description: >-
  Implement OAuth 2.0 authentication flows for Telnyx API access. This skill
  provides JavaScript SDK examples.
metadata:
  author: telnyx
  product: oauth
  language: javascript
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx Oauth - JavaScript

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

## 授权服务器元数据

OAuth 2.0 授权服务器元数据（RFC 8414）

`GET /.well-known/oauth-authorization-server`

```javascript
const response = await client.wellKnown.retrieveAuthorizationServerMetadata();

console.log(response.authorization_endpoint);
```

## 受保护资源元数据

用于资源发现的 OAuth 2.0 受保护资源元数据

`GET /.well-known/oauth-protected-resource`

```javascript
const response = await client.wellKnown.retrieveProtectedResourceMetadata();

console.log(response.authorization_servers);
```

## OAuth 授权端点

用于授权码流程的 OAuth 2.0 授权端点

`GET /oauth/authorize`

```javascript
await client.oauth.retrieveAuthorize({
  client_id: 'client_id',
  redirect_uri: 'https://example.com',
  response_type: 'code',
});
```

## 列出 OAuth 客户端

检索已认证用户的 OAuth 客户端列表（分页显示）

`GET /oauth/clients`

```javascript
// Automatically fetches more pages as needed.
for await (const oauthClient of client.oauthClients.list()) {
  console.log(oauthClient.client_id);
}
```

## 创建 OAuth 客户端

创建一个新的 OAuth 客户端

`POST /oauth/clients` — 必需参数：`name`、`allowed_scopes`、`client_type`、`allowed_grant_types`

```javascript
const oauthClient = await client.oauthClients.create({
  allowed_grant_types: ['client_credentials'],
  allowed_scopes: ['admin'],
  client_type: 'public',
  name: 'My OAuth client',
});

console.log(oauthClient.data);
```

## 获取 OAuth 客户端信息

通过 ID 检索单个 OAuth 客户端的信息

`GET /oauth/clients/{id}`

```javascript
const oauthClient = await client.oauthClients.retrieve('182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e');

console.log(oauthClient.data);
```

## 更新 OAuth 客户端

更新现有的 OAuth 客户端

`PUT /oauth/clients/{id}`

```javascript
const oauthClient = await client.oauthClients.update('182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e');

console.log(oauthClient.data);
```

## 删除 OAuth 客户端

删除一个 OAuth 客户端

`DELETE /oauth/clients/{id}`

```javascript
await client.oauthClients.delete('182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e');
```

## 获取 OAuth 同意令牌

检索关于 OAuth 同意令牌的详细信息

`GET /oauth/consent/{consent_token}`

```javascript
const oauth = await client.oauth.retrieve('consent_token');

console.log(oauth.data);
```

## 列出 OAuth 授权令牌

检索已认证用户的 OAuth 授权令牌列表（分页显示）

`GET /oauth/grants`

```javascript
// Automatically fetches more pages as needed.
for await (const oauthGrant of client.oauthGrants.list()) {
  console.log(oauthGrant.id);
}
```

## 获取 OAuth 授权令牌

通过 ID 检索单个 OAuth 授权令牌的信息

`GET /oauth/grants/{id}`

```javascript
const oauthGrant = await client.oauthGrants.retrieve('182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e');

console.log(oauthGrant.data);
```

## 撤销 OAuth 授权令牌

撤销一个 OAuth 授权令牌

`DELETE /oauth/grants/{id}`

```javascript
const oauthGrant = await client.oauthGrants.delete('182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e');

console.log(oauthGrant.data);
```

## 令牌验证

验证 OAuth 访问令牌的有效性及元数据

`POST /oauth/introspect` — 必需参数：`token`

```javascript
const response = await client.oauth.introspect({ token: 'token' });

console.log(response.client_id);
```

## JSON Web Key Set

检索用于令牌验证的 JSON Web Key Set

`GET /oauth/jwks`

```javascript
const response = await client.oauth.retrieveJwks();

console.log(response.keys);
```

## 动态客户端注册

动态注册一个新的 OAuth 客户端（RFC 7591）

`POST /oauth/register`

```javascript
const response = await client.oauth.register();

console.log(response.client_id);
```

## OAuth 令牌端点

交换授权码、客户端凭据或刷新令牌以获取访问令牌

`POST /oauth/token` — 必需参数：`grant_type`

```javascript
const response = await client.oauth.token({ grant_type: 'client_credentials' });

console.log(response.access_token);
```