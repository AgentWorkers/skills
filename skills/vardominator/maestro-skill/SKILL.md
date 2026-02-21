---
name: maestro-bitcoin
description: >
  **使用 x402 USDC 支付方式，直接通过 HTTP 查询 Maestro Bitcoin API**  
  默认生产环境为以太坊主网（Ethereum Mainnet）。支持使用 `PRIVATE_KEY` 进行签名，或通过 CDP Agent Wallet 进行操作；同时仅要求满足最低限度的钱包使用条件。
---
# Maestro Bitcoin Skill

本技能的设计较为简单：直接使用 x402 协议查询 Maestro 的 API。

## 默认生产模式（优先使用）

- 生产请求的首选网络：`eip155:1`（Ethereum 主网）。
- 备用网络：`eip155:8453`（Base 主网），仅在用户请求使用 Base 主网或同意使用备用网络时使用。
- 默认情况下使用生产环境的服务器。
- 仅在用户明确要求进行测试/预发布环境操作时，才使用 `dev.` 环境的服务器。
- 主网请求不会自动切换到测试网络。

## 请求所需的最小前提条件

请求时只需提供以下最基本的信息：

- 钱包路径 A（原始签名者）：专用 EVM 钱包的 `PRIVATE_KEY`。
- 钱包路径 B（托管签名者）：已在运行时环境中配置好的 CDP Agent 钱包。
- 可选的 `WALLET_NETWORK`（如果省略，则默认为 `eip155:1`）。

**资金要求**（仅限于支付所需）：
- 在所选网络上拥有足够的 `USDC` 以完成当前交易。
- 在同一网络上拥有足够的 `ETH` 作为交易手续费。

**注意**：切勿请求 x402 流程所需的 API 密钥，也切勿请求超出必要范围的钱包信息。

## CDP Agent 钱包选项

当用户/运行时环境支持时，代理可以使用 Coinbase 的 CDP Agent 钱包代替原始的私钥：

- 文档链接：`https://docs.cdp.coinbase.com/agentic-wallet/welcome`
- 使用 CDP 提供的签名者/账户进行 x402 签名操作。
- 保持相同的网络选择规则：优先选择 `eip155:1` 主网。
- 仅在 CDP 相关信息缺失时才请求这些信息；除非用户特别要求，否则不要同时请求 CDP 的秘密信息和 `PRIVATE_KEY`。

## 工作流程

1. 从 `https://docs.gomaestro.org/bitcoin`（或其中的 REST 文档链接）获取端点规范。所有文档页面都可以通过在 URL 后添加 `.md` 扩展名来查看（例如：`https://docs.gomaestro.org/bitcoin/blockchain-indexer-api/addresses/utxos-by-address.md`）。
2. 发送请求时不需要提供 `api-key`。
3. 如果网关返回 `402 Payment Required`（表示需要支付），则解析相应的响应信息。
4. 选择与 `WALLET_NETWORK` 匹配的支付选项（默认为 `eip155:1`）。
5. 根据客户端实现，添加 `PAYMENT-SIGNATURE` 和/或 `X-PAYMENT` 头部信息进行签名并重试请求。
6. 返回 API 响应内容以及支付结算元数据（`PAYMENT-RESPONSE` 或 `X-PAYMENT-RESPONSE`，如果有的话）。

## x402 请求头部信息

- `PAYMENT-REQUIRED`：网关发出的支付请求。
- `PAYMENT-SIGNATURE`：客户端生成的签名支付证明。
- `PAYMENT-RESPONSE`：支付/结算的元数据。
- `X-PAYMENT` / `X-PAYMENT-RESPONSE`：某些客户端使用的替代头部信息。

## 浏览器交易查询

支付成功后，从 `PAYMENT-RESPONSE`（或 `X-PAYMENT-RESPONSE`）中提取 `transaction` 和 `network` 信息，并返回相应的交易查询链接：

- `eip155:1`（Ethereum 主网）：`https://etherscan.io/tx/<transaction_hash>`
- `eip155:8453`（Base 主网）：`https://basescan.org/tx/<transaction_hash>`

如果无法确定对应的浏览器查询链接，仍需返回：
- 原始交易哈希值
- 响应中的网络 ID
- 注意：浏览器链接可能无法自动解析。

## 推荐的客户端库

为了兼容 `eip155:1` 和 `eip155:8453` 等 CAIP-2 网络，建议使用当前的 `@x402/*` 客户端库：

- 推荐使用：`@x402/fetch` + `@x402/evm`。
- 如果交易涉及 CAIP-2 网络 ID，请避免使用旧版本的 `x402-fetch`/`x402`（仅支持 v1 的版本）。

## 通用交易发起方式（不使用 x402 SDK）

如果 `@x402/*` 库不可用，代理可以使用任何 EVM 签名工具手动发起支付：

1. 发送请求并捕获 `402` 请求信息（`PAYMENT-REQUIRED` 头部或 JSON 标签）。
2. 选择与 `WALLET_NETWORK` 匹配的支付选项（默认为 `eip155:1`）。
3. 使用请求中的字段构建 EIP-712 格式的 `TransferWithAuthorization` 消息：
   包括 `asset`、`payTo`、`amount`、`maxTimeoutSeconds` 以及 `extra` 中的令牌元数据。
4. 使用钱包密钥对消息进行签名。
5. 构建支付数据包，包含 `x402Version`、`scheme`、`network` 以及签名后的授权数据。
6. 将数据包进行 Base64 编码，并添加 `PAYMENT-SIGNATURE` 和/或 `X-PAYMENT` 头部信息后重新发送请求。
7. 通过 HTTP 响应码 `200` 以及 `PAYMENT-RESPONSE`/`X-PAYMENT-RESPONSE` 来验证支付是否成功。

**手动流程** 是可行的，但仅作为备用方案，因为协议和编码细节容易出错。

## 对代理的要求

- 不要硬编码支付金额、收款人或网络信息；每次请求都应使用 `PAYMENT-REQUIRED` 头部信息。
- 如果用户请求使用主网，请强制选择 `eip155:1`；除非用户明确要求使用 Base 主网。
- 在使用备用网络（`eip155:8453`）或切换到测试网络之前，请先询问用户。
- 支持两种钱包签名方式：使用 `PRIVATE_KEY` 或 CDP Agent 钱包进行签名。
- 如果用户的意图不明确，在发送第一个主网支付请求之前请先确认。
- 如果支付验证失败或交易详情发生变化，请重新执行整个流程。
- 如果没有可用的已充值钱包，请停止操作并仅请求缺失的必要信息。
- 保持实现方式的简洁性，并确保与特定端点兼容。

## 最基本的错误处理机制

如果支付重试后仍收到 `402` 错误，需提供以下详细诊断信息：
- 选定的支付网络。
- 交易金额和使用的令牌信息。
- 用于签名的钱包地址。
- 用户接下来的操作：在所选的主网上充值 `USDC` 并支付手续费，然后重新尝试。

## 主要参考资料

- `https://docs.gomaestro.org/bitcoin`