---
name: bloomfilter
description: 通过 Bloomfilter x402 API 搜索、注册和管理域名——使用 Base 平台以 USDC 进行支付
homepage: https://bloomfilter.xyz
metadata:
  clawdbot:
    emoji: 🌐
    requires:
      env:
        - EVM_PRIVATE_KEY
    primaryEnv: EVM_PRIVATE_KEY
---
# Bloomfilter - 域名注册 API

基础 URL：`https://api.bloomfilter.xyz`

付费接口使用 x402 支付协议。API 会返回 HTTP 402 错误码，并附带支付详情；您的 x402 兼容 HTTP 客户端会自动处理支付。

`EVM_PRIVATE_KEY` 由代理的 x402 HTTP 客户端（`@x402/axios` 或 `@x402/fetch`）在本地使用，用于签署 EIP-3009 `TransferWithAuthorization` 消息（用于 USDC 支付）以及 EIP-4361 `SIWE` 消息（用于身份验证）。该私钥永远不会离开本地机器，也不会被发送到任何服务器。所有的加密签名操作都在代理的运行时环境中完成。

DNS 和账户相关的接口需要通过 SIWE（使用以太坊进行身份验证）进行访问。完成身份验证后，您可以将生成的 JWT 作为承载令牌（Bearer token）传递给这些接口。

## 身份验证（SIWE）

- **GET /auth/nonce**  
  -> 返回：`{ nonce, domain, uri, chainId, version, expiresIn }`

- **POST /auth/verify**  
  `Body`: `{"message": "<EIP-4361 SIWE message>", "signature": "0x..."}`  
  -> 返回：`{ accessToken, refreshToken, walletAddress }`

- **POST /auth/refresh**  
  `Body`: `{"refreshToken": "..."}`  
  -> 返回：新的 `accessToken` 和 `refreshToken`

- **POST /auth/revoke**  
  （需要承载令牌）  
  -> 取消已认证钱包的所有会话。

## 域名搜索与价格查询（免费，无需身份验证）  

- **GET /domains/search?query=example&tlds=com,io,xyz**  
  -> 返回每个顶级域名（TLD）的可用性和价格信息。`tlds` 参数是可选的。

- **GET /domains/pricing**  
  -> 返回所有支持的顶级域名的价格信息。

- **GET /domains/pricing/:tld**  
  -> 返回特定顶级域名（例如：`/domains/pricing/com`）的价格信息。

## 域名注册（x402 - 动态定价）  

- **POST /domains/register**  
  `Body`: `{"domain": "example.com", "years": 1}`  
  如果省略 `years`，默认值为 1 年。  
  可选参数：`"dns_records": [{ "type": "A", "host": "@", "value": "1.2.3.4" }`  
  支持的 DNS 记录类型：A、AAAA、CNAME、MX、TXT、SRV、CAA  
  每条记录还可以设置 `ttl`（300-86400，默认为 3600）和 `priority`（针对 MX/SRV）。  
  - 首次请求会返回 402 错误码，提示需要使用 x402 协议完成支付；成功后返回 201 状态码；异步处理时返回 202 状态码并附带作业 ID。  

- **POST /domains/renew**  
  `Body`: `{"domain": "example.com", "years": 1}`  
  如果省略 `years`，默认值为 1 年。  
  注：注册过程与上述相同，同样采用两阶段 x402 支付流程。

## 域名信息（免费，无需身份验证）  

- **GET /domains/:domain**  
  -> 返回域名的状态、到期时间、名称服务器以及锁定/隐私设置。  
  **注意**：仅适用于通过 Bloomfilter 注册的域名。

## 作业状态查询（免费，无需身份验证）  

- **GET /domains/status/:jobId**  
  -> 查询异步注册的作业状态。返回 200（已完成）、202（待处理）或 500（失败）。

## DNS 管理（需要承载令牌）  

- 每条 DNS 记录的修改费用为 0.10 USDC（通过 x402 协议支付）。  
  添加 DNS 记录是免费的。

**重要提示：**  
  请始终一次只添加、更新或删除一条 DNS 记录（按顺序操作，不要同时进行）。注册新域名后，请至少等待 30 秒再添加 DNS 记录，因为 DNS 区可能尚未准备好。  

- **GET /dns/:domain**  
  -> 列出所有 DNS 记录。

- **POST /dns/:domain**  
  `Body`: `{"type": "A", "host": "@", "value": "1.2.3.4"}`  
  可选参数：`ttl`（300-86400，默认为 3600）、`priority`（针对 MX/SRV）。  
  支持的类型：A、AAAA、CNAME、MX、TXT、NS、SRV、CAA。

- **PUT /dns/:domain/:recordId**  
  `Body`: `{"host": "@", "value": "5.6.7.8"}`  
  至少需要填写一个字段。可选参数：`host`、`value`、`ttl`、`priority`。

- **DELETE /dns/:domain/:recordId**  
  -> 删除指定的 DNS 记录。

## 账户信息（需要承载令牌，免费）  

- **GET /account**  
  -> 账户概览（钱包信息、拥有的域名数量、总花费金额）。  

- **GET /account/domains?limit=50&offset=0**  
  -> 分页显示拥有的域名列表。

- **GET /account/transactions?limit=50&offset=0**  
  -> 分页显示交易历史记录。

## 注意事项：**  
  - 所有付费请求都需要使用支持 x402 协议的 HTTP 客户端，并且必须使用基于 Base 链路的 USDC 进行支付（链 ID 为 8453）。  
  - 所有域名注册默认启用 WHOIS 隐私设置，您的身份信息不会公开显示在 WHOIS 记录中。  
  - 所有 API 请求均通过 HTTPS 协议传输。

## 安全与隐私：**  
  - `EVM_PRIVATE_KEY` 仅在本机使用，用于签署 x402 支付授权和 SIWE 消息。  
  - API 会接收您的钱包地址（从私钥派生而来），但不会获取私钥本身。  
  - 所有 API 操作均通过 HTTPS 进行。  

## 信任说明：**  
  该服务通过 `api.bloomfilter.xyz` 接口帮助您注册 ICANN 域名并管理 DNS 记录。支付使用基于 Base 链路的 USDC 和 x402 协议完成。您的私钥始终保留在本地。  
  仅当您信任 Bloomfilter（https://bloomfilter.xyz）作为域名注册服务提供商时，才建议安装该服务。