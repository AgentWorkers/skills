---
name: maestro-api
description: 使用 SIWX + JWT + x402 认证机制通过 HTTP 查询 Maestro API。在请求或支付之前，请先从 docs.gomaestro.org 获取正确的 API 端点信息。
---
# Maestro API

当用户需要直接通过 HTTP 调用 Maestro 的端点时，请使用此技能。所需的路径非常简洁：确定具体的操作页面，发送请求，完成 SIWX 验证流程，只有当服务器返回 `402` 状态码时才购买信用点数。

## 快速操作流程

1. 在 `docs.gomaestro.org` 上找到具体的操作页面。
2. 读取该页面的 `.md` 文件，并将其中的 `OpenAPI` 部分作为请求的依据。
3. 根据 `servers:` 和操作路径构建请求 URL。
4. 发送请求时不要包含任何身份验证或支付相关的头部信息。
5. 如果响应状态码为 `200`，则返回数据。
6. 如果响应状态码为 `402` 且包含 `extensions.sign-in-with-x`，则需要完成 SIWX 验证流程，然后使用 `sign-in-with-x` 重新发送相同的请求。
7. 如果再次尝试后响应状态码仍为 `200`，则返回数据。
8. 如果再次尝试后响应状态码为 `402` 且包含 `Authorization: Bearer <jwt>`，则需要从最新的 `accepts[]` 列表中获取信用点数，并使用 `Authorization` 和 `X-PAYMENT` 头部信息重新发送相同的请求。
9. 在 JWT 有效期内或 Maestro 要求更多信用点数之前，可重复使用该 JWT 进行后续请求。

## 从文档中获取端点信息

仅使用文档来查找具体的操作页面。找到页面后请避免进行广泛的浏览。

- 仅在操作页面不明确的情况下，从 `https://docs.gomaestro.org/llms.txt` 开始查找。
- 优先选择操作页面而非快速入门页面。
- 阅读 `.md` 文件并提取以下信息：
  - 操作相关的路径（`path`）
  - 选定网络的基 URL（`servers:`）
  - 请求参数和数据格式（`parameters` 和 `body schema`）
- 将 `server.url` 与 `path` 组合起来形成完整的请求 URL。
- 不要从 SIWX 的 `domain` 或 `URI` 中推导出 REST 主机地址。
- 一些常用的比特币路由快捷方式：
  - 已确认的交易数据 -> Blockchain Indexer API
  - 与内存池相关的数据 -> Mempool Monitoring API
  - 与内存池相关的路由 -> Esplora API
  - 钱包余额或活动信息 -> Wallet API

## 最低要求

仅获取进行签名和支付所需的资源：
- `PRIVATE_KEY`，或运行时的 CDP 钱包签名器
- 根据最新的 `402` 响应结果，在某个网络中拥有足够的 `USDC` 和原生气体（gas）
- 不需要 API 密钥

## 请求规则

- 在未经身份验证的请求、尝试完成 SIWX 验证后的请求以及已付费的请求中，方法（method）、路径（path）、查询参数（query parameters）和请求体（body）必须保持不变。
- 始终使用最新的 `402` 响应结果来获取 `supported_chains`、`accepts[]`、`asset`、`pay_to` 和价格限制（price limits）等信息。
- 在进行首次付费请求之前，请确保所有信息都是正确的。
- 如果付费请求仍然失败，请记录以下信息：
  - 使用的文档页面
  - 选定的网络
  - 选择的金额
  - 签名器地址
  - 下一步应采取的措施

## 仅在需要时阅读相关文档

仅在需要了解具体的签名或头部信息时，才阅读 [SIWX + x402 参考文档](references/siwx-x402.md)：
- `sign-in-with-x` 的请求格式
- `X-PAYMENT` 的请求格式
- EIP-4361 和 EIP-712 相关的 SIWX 消息模板
- ERC-3009 和 ERC-712 相关的域名及消息字段
- 响应头部的含义
- 失败情况以及常见的错误点