---
name: apiosk-publish
description: 发布和管理 Apiosk 网关列表，支持签名钱包认证、基于列表组的分类功能，以及更新/删除操作。
---
# apiosk-publish

使用此技能可在 `https://gateway.apiosk.com` 上进行 API 的发布和生命周期管理。

## 使用场景

- 需要在 Apiosk 上注册一个新的付费 API。
- 需要更新、列出或停用已发布的 API。
- 需要将 API 映射到最新的列表组（`api`、`datasets`、`compute`）。
- 需要为管理端点发送正确签名的钱包认证信息。

## 所需工具和文件

- `curl`
- `jq`
- `cast`（Foundry 提供的工具）
- 钱包文件：
  - `~/.apiosk/wallet.json`（推荐使用，包含 `address` 和 `private_key`）
  - 或使用环境变量 `APIOSK_PRIVATE_KEY`
  - 或使用命令行参数 `--private-key`

## 管理端点

- `POST /v1/apis/register`
- `GET /v1/apis/mine?wallet=0x...`
- `POST /v1/apis/:slug`
- `DELETE /v1/apis/:slug?wallet=0x...`

## 签名的钱包认证信息

所有管理请求都需要提供以下字段：

- `x-wallet-address`
- `x-wallet-signature`
- `x-wallet-timestamp`
- `x-wallet-nonce`

用于签名的标准消息格式如下：

```text
Apiosk auth
action:<action>
wallet:<lowercase_wallet>
resource:<resource>
timestamp:<unix_seconds>
nonce:<nonce>
```

**操作与资源映射**：

- 注册：`action=register_api`, `resource=register:<slug>`
- 更新：`action=update_api`, `resource=update:<slug>`
- 列出：`action=my_apis`, `resource=mine:<wallet>`
- 删除：`action=delete_api`, `resource=delete:<slug>`

## 列表组和分类

Gateway 中的列表组包括：

- `api`
- `datasets`
- `compute`

注册请求的 JSON 格式目前使用 `category` 字段（而非显式的 `listing_type`）。请按照以下规则进行映射：

- `api` -> `data`
- `datasets` -> `dataset`
- `compute` -> `compute`

## 注册请求的 JSON 格式

发送请求到 `POST /v1/apis/register`：

```json
{
  "name": "My API",
  "slug": "my-api",
  "endpoint_url": "https://example.com",
  "price_usd": 0.01,
  "description": "My paid API",
  "owner_wallet": "0x...",
  "category": "dataset"
}
```

## 代理行为要求

- 所有管理请求都必须经过签名；未签名的请求将被视为无效。
- 确保签名消息中的钱包地址（`wallet-address`）为小写形式，即使请求头中使用的地址可能是大写形式。
- 如果收到 `Unauthorized` 错误，应重新生成时间戳和随机数（nonce），然后重新签名请求。
- 在执行注册或更新操作之前，请验证请求的 HTTPS 端点是否合法。
- 请使用上述的列表组映射规则，以确保新发布的 API 能正确显示在相应的发现页面上。