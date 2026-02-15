---
name: bluepages
description: >
  Look up wallet address <> Twitter/Farcaster identity mappings via Bluepages.fyi.
  Use when asked who owns a wallet, finding addresses for a Twitter/Farcaster handle,
  looking up 0x addresses, or any wallet identity and address attribution queries.
compatibility: >
  Requires MCP server (npx github:bluepagesdoteth/bluepages-mcp) and one of:
  BLUEPAGES_API_KEY or PRIVATE_KEY (Ethereum, for x402 payments).
metadata:
  author: bluepages
  version: "1.0.1"
---

# Bluepages

Bluepages 支持查询超过 80 万个经过验证的以太坊地址及其对应的 Twitter 账号信息（包括 Farcaster 账号），并提供相应的 API 功能。

## 设置

使用 Bluepages 需要安装 Bluepages MCP 服务器：`npx -y github:bluepagesdoteth/bluepages-mcp`，或者直接使用 API 调用（详见下文）。MCP 服务器是推荐的使用方式。

## 认证

需要设置以下环境变量之一：

- **`BLUEPAGES_API_KEY`**（推荐）：使用此密钥可节省 20% 的费用，并且每分钟的请求次数限制更高。
- **`PRIVATE_KEY`**：使用以太坊私钥通过 x402 方式支付请求费用（费用以 USDC 计算）。

> **安全提示**：切勿使用主钱包的私钥。如果使用 `PRIVATE_KEY`，请使用专门用于支付的代理钱包。

**使用私钥**时，可以选择通过 x402 方式按请求付费，或者使用 `get_api_key` 和 `purchase_credits` 工具购买 `BLUEPAGES_API_KEY`。

**不使用私钥**时，用户需要从 [bluepages.fyi/api-keys](https://bluepages.fyi/api-keys.html) 获取 API 密钥，并将其设置为 `BLUEPAGES_API_KEY`。

## 工具（快速参考）

| 工具                        | 费用                   | 描述                                        |
| -------------------------- | ---------------------- | -------------------------------------------------- |
| `check_address`            | 1 信用点（0.001 美元）      | 检查地址是否包含相关数据                          |
| `check_twitter`            | 1 信用点（0.001 美元）      | 检查 Twitter 账号是否包含相关数据                   |
| `get_data_for_address`     | 50 信用点（0.05 美元）     | 获取地址的完整身份信息（未找到时免费）             |
| `get_data_for_twitter`     | 50 信用点（0.05 美元）     | 获取 Twitter 账号的完整身份信息（未找到时免费）             |
| `batch_check`              | 40 信用点（0.04 美元）     | 一次检查最多 50 个条目                       |
| `batch_get_data`           | 40 信用点/每个找到的条目  | 获取最多 50 个条目的数据（x402 方式：每次批量请求 2.00 美元）   |
| `batch_check_streaming`    | 与 `batch_check` 相同    | 适用于大量条目（100 个以上），可显示处理进度             |
| `batch_get_data_streaming` | 与 `batch_get_data` 相同 | 适用于大量条目（100 个以上），可显示处理进度             |
| `check_credits`            | 免费                   | 查看剩余信用点数（仅限使用 API 密钥的情况）             |
| `set_credit_alert`         | 免费                   | 设置低信用点数警告阈值（仅限使用 API 密钥的情况）    |
| `get_api_key`              | 免费                   | 通过钱包签名获取/创建 API 密钥            |
| `purchase_credits`         | 5–600 美元             | 通过 x402 方式购买信用点（仅限使用 `PRIVATE_KEY`）            |

## 输入格式

- **地址**：以 `0x` 开头的 42 位十六进制字符串，大小写不敏感。
- **Twitter 账号**：可包含或不包含 `@` 符号。

## 节省费用的方法

- **单次查询**：先使用 `check_address`/`check_twitter`（1 信用点），只有在找到相关数据后才使用 `get_data_*`（50 信用点）。跳过这些步骤会在未找到数据时浪费信用点。
- **批量查询**：始终分两步进行——先使用 `batch_check`，然后在找到相关数据后使用 `batch_get_data`。这种方式比一次性获取所有数据节省约 90% 的费用。
- **处理大量条目（100 个以上）**：使用 `_streaming` 系列工具来获取处理进度。

## 请求限制

- API 密钥：每分钟 60 次请求。
- x402 方式：每分钟 30 次请求。
- 批量请求：每次请求最多处理 50 个条目。

## 替代方案：直接使用 HTTP API

如果 MCP 服务器不可用，可以直接调用 API。认证方式取决于您的设置：

- **API 密钥**：在请求头中添加 `X-API-KEY`。
- **使用私钥（x402 方式）**：API 端点会返回 402 错误代码并提示支付详情；需要使用 `X-PAYMENT` 请求头进行签名并重新发送请求。

```bash
# With API key
curl "https://bluepages.fyi/check?address=0x..." -H "X-API-KEY: your-key"
curl "https://bluepages.fyi/data?address=0x..." -H "X-API-KEY: your-key"

# Batch check
curl -X POST "https://bluepages.fyi/batch/check" \
  -H "X-API-KEY: your-key" -H "Content-Type: application/json" \
  -d '{"addresses": ["0x...", "0x..."]}'
```

完整 API 文档：[bluepages.fyi/docs](https://bluepages.fyi/docs.html)