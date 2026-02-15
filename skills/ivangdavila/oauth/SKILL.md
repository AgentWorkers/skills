---
name: OAuth
description: 安全地实现 OAuth 2.0 和 OpenID Connect 流程。
metadata: {"clawdbot":{"emoji":"🔑","os":["linux","darwin","win32"]}}
---

## 流程选择

- **授权码（Authorization Code）+ PKCE**：适用于所有客户端——包括Web应用、移动应用和单页应用程序（SPAs）。
- **客户端凭据（Client Credentials）**：仅用于服务之间的通信，不涉及用户上下文。
- **隐式流程（Implicit Flow）**：已被弃用，请勿使用；它曾在PKCE出现之前用于SPAs。
- **设备代码（Device Code）**：适用于没有浏览器的设备（如电视、命令行界面等）——用户需要在单独的设备上进行授权。

## PKCE（Proof Key for Code Exchange）

- **强制要求**：适用于公共客户端（如SPAs和移动应用），建议所有客户端都使用。
- **生成`code_verifier`**：一个43到128个字符的随机字符串，存储在客户端端。
- **发送`code_challenge`**：`code_verifier`的SHA256哈希值，随授权请求一起发送。
- **令牌交换**：需要包含`code_verifier`，服务器会将其与存储的`code_challenge`进行比对。
- **防止授权码被截获**：攻击者无法在没有`code_verifier`的情况下使用被盗的授权码。

## **状态参数（State Parameter）**

- **授权请求中必须包含`state`**：以防止CSRF攻击。
- **生成一个随机且无法猜测的值**，在重定向之前将其存储在会话中。
- **在处理回调之前**，验证返回的`state`是否与存储的值匹配。
- **也可以对返回的URL或其他上下文进行编码（加密或签名）**。

## **重定向URI安全（Redirect URI Security）**

- **注册精确的重定向URI**：不允许使用通配符或开放重定向。
- **在授权端点和令牌端点上都验证`redirect_uri`**。
- **始终使用HTTPS**——开发环境除外（仅限localhost）。
- **路径匹配必须精确**：例如`/callback`不应与`/callback/`混淆。

## **令牌（Tokens）**

- **访问令牌（Access Token）**：生命周期较短（几分钟到一小时），用于API访问。
- **刷新令牌（Refresh Token）**：生命周期较长，仅在令牌端点用于获取新的访问令牌。
- **ID令牌（ID Token, OIDC）**：是一种包含用户身份信息的JWT令牌，不应用于API授权。
- **不要将刷新令牌发送到资源服务器**，只能发送到授权服务器。

## **权限范围（Scopes）**

- **仅请求所需的最低权限范围**——用户更信任这种细粒度的权限控制。
- **权限范围格式各不相同**：例如`openid profile email`（OIDC格式）、`repo:read`（GitHub风格）。
- **服务器可能会授予比请求更少的权限范围**——请检查令牌响应。
- **使用`openid`权限范围是获取ID令牌的必要条件**。

## **OpenID Connect**

- **OpenID Connect** = **OAuth 2.0** + 身份认证层——增加了ID令牌和UserInfo端点。
- **ID令牌**是一种包含`sub`、`iss`、`aud`、`exp`以及用户信息声明的JWT令牌。
- **在信任令牌中的声明之前**，必须验证其签名。
- **`nonce`参数用于防止重放攻击**——需在授权请求中包含，并在ID令牌中进行验证。

## **安全检查清单（Security Checklist）**

- **所有接口都必须使用HTTPS**——令牌在传输过程中必须受到保护。
- **验证令牌中的`iss`和`aud`字段**——防止不同服务之间出现令牌混淆。
- **将授权码与特定客户端绑定**——确保授权码只能由发起请求的客户端使用。
- **授权码的生命周期应尽可能短（最长10分钟）**——仅允许一次性使用。
- **实现令牌撤销机制**，以应对登出或安全事件。

## **常见错误**

- **将访问令牌用作身份验证依据**：应使用ID令牌进行身份验证。
- **将令牌存储在`localStorage`中**：这容易受到XSS攻击；建议使用`httpOnly`属性的cookie或内存存储方式。
- **不验证`redirect_uri**：可能导致开放重定向攻击。
- **在后端接受来自URL片段的令牌**：这些片段可能无法到达服务器。
- **使用长期有效的访问令牌**：应采用“短期访问令牌+刷新令牌”的模式。

## **令牌端点（Token Endpoints）**

- `/authorize`：面向用户的接口，通过重定向返回授权码。
- `/token`：用于客户端与服务器之间的令牌交换；对于需要身份验证的客户端，此接口是必需的。
- `/userinfo`（OIDC）：返回用户信息声明；需要访问令牌。
- `/revoke`：用于撤销令牌；可以接受访问令牌或刷新令牌。

## **客户端类型（Client Types）**

- **机密客户端（Confidential Clients）**：可以存储敏感信息（例如后端应用程序），因此可以使用`client_secret`。
- **公共客户端（Public Clients）**：无法存储敏感信息（例如SPAs和移动应用），因此只能使用PKCE。
- **切勿在移动应用或SPAs中嵌入`client_secret`——否则可能会被窃取。