---
name: maestro-bitcoin
description: >
  **直接通过 HTTP 查询 Maestro Bitcoin API，并使用 x402 USDC 在 Ethereum 或 Base 上进行支付**  
  当代理需要从 `docs.gomaestro.org` 阅读 API 规范并直接调用 API（而无需使用本地封装脚本）时，可以使用此技能。
---
# Maestro Bitcoin 技能

该技能的设计非常简单：直接使用 x402 协议查询 Maestro 的 API。

## 核心要求

- 拥有一个能够在以太坊（Ethereum）或 Base 网络上使用 USDC 进行支付/签名的钱包。
- 具备发送 HTTP 请求的能力。
- 以 Maestro 的官方文档作为 API 端点规范的来源。

## 钱包设置（必需）

在使用 x402 调用 Maestro API 之前，必须使用已充值 USDC 的钱包。如果没有这样的钱包，请求会返回 `402 Payment Required` 的错误，导致请求无法完成。

1. 创建或导入一个能够签署 x402 支付请求的 EVM（以太坊虚拟机）钱包。
2. 选择用于支付的网络（以太坊或 Base）。
3. 为该钱包充值：
   - 所选网络上的 USDC（用于支付 API）。
   - 该网络上的少量原生以太坊（ETH）作为交易手续费（gas）。
4. 将钱包的认证信息提供给运行时环境（例如，通过安全的 `PRIVATE_KEY` 环境变量或钱包提供商的配置文件）。
5. 绝不要将任何敏感信息硬编码到代码库中。
6. 在调用 Maestro 的 API 端点之前，确保钱包中的 USDC 数量和手续费（gas）足够完成支付。

## 工作流程

1. 从 `https://docs.gomaestro.org/bitcoin`（或其中的 REST 参考链接）获取 API 端点规范。
2. 发送 API 请求时不要包含 `api-key`。
3. 如果网关返回 `402 Payment Required`，则解析该响应并执行相应的处理逻辑。
4. 选择一个有效的 USDC 支付方式（以太坊或 Base），使用钱包进行签名，然后再次发送请求（带有 `PAYMENT-SIGNATURE` 参数）。
5. 使用 API 的响应内容（以及可能存在的 `PAYMENT-RESPONSE` 参数）进行后续处理。

## x402 请求头

- `PAYMENT-REQUIRED`：来自网关的支付验证请求。
- `PAYMENT-SIGNATURE`：客户端生成的签名后的支付证明。
- `PAYMENT-RESPONSE`：支付/结算的元数据（仅在支付成功时返回）。

## 对代理程序（Agents）的要求

- 不要硬编码支付金额、收款人或网络信息；每次请求都应使用 `PAYMENT-REQUIRED` 参数。
- 如果支付验证失败或验证细节发生变化，重新执行支付验证流程。
- 如果没有可用的已充值钱包，应停止尝试并报告缺失的必要条件，而不是盲目重试。
- 实现应保持直接且针对特定 API 端点设计；不需要额外的本地封装脚本。

## 主要参考资料

- `https://docs.gomaestro.org/bitcoin`