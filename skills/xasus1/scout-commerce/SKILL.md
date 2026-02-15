---
name: scout-commerce
version: 1.1.0
description: 在 Amazon 或 Shopify 上搜索产品，并使用 Solana 中的 USDC 进行购买。通过 Jupiter 来交换代币。
homepage: https://scout.trustra.xyz
metadata: {"emoji":"🛒","category":"shopping","api_base":"https://scout-api.trustra.xyz/api/v2"}
---

# Scout 🛒

您可以使用 USDC 在 Amazon 和 Shopify 上进行购物，并通过 Jupiter 进行代币兑换。仅支持美国境内配送。

## 产品展示（重要！）

**搜索结果：** 对于每个推荐的产品，请将产品图片作为实际媒体文件发送（而非 Markdown 链接），并将产品详情作为图片的说明文字。每条消息中只包含一个产品信息，以确保图片能够正确显示。

**产品详情：** 在展示产品详情时，应将产品图片作为媒体附件随文字一起发送。API 会返回产品的图片，请立即使用这些图片，无需让用户另行请求。

**原因：** Markdown 中的图片链接（`![](url)`）在 Telegram 或其他消息平台上无法正常显示。请始终使用带有 `media` 参数的消息工具发送图片，或者如果支持的话，也可以使用内联图片格式。

## 快速参考

**首次设置：** `python get_api_key.py --email ... --address "..."`

**查找产品：** `python search.py "价格低于 $50 的游戏鼠标"`

**获取产品详情：** `python product.py amazon:B07GBZ4Q68`

**查看钱包余额：** `python balance.py`（显示所有代币）

**购买产品：** `python buy.py amazon:B07GBZ4Q68`

**查看订单状态：** `python order_status.py ord_abc123`

**列出订单：** `python order_status.py --list`

**兑换代币：** `python swap.py SOL USDC 5`（最低交易金额为 $5）

**获取兑换报价：** `python swap.py --quote SOL USDC 5`

**列出钱包中的代币：** `python swap.py --list`

所有命令均需在 `scripts/` 目录下执行。API 密钥会自动从 `credentials.json` 文件中加载。

## 首次设置

```bash
python get_api_key.py --email <EMAIL> --address "<NAME>,<STREET>,<CITY>,<STATE>,<ZIP>,<COUNTRY>"
```

此步骤会创建一个 **Crossmint 钱包** 并生成一个 **API 密钥**，并将它们保存在 `credentials.json` 文件中。请使用 USDC 为钱包充值以便进行购物。

**请妥善保管 API 密钥**——它用于授权您的钱包进行交易。

## 命令说明

| 命令 | 用法 |
|---------|-------|
| 搜索 | `python search.py "查询"` |
| 产品详情 | `python product.py amazon:B07GBZ4Q68` |
| 查看余额 | `python balance.py`（显示所有代币）或 `balance.py --usdc` |
| 购买 | `python buy.py amazon:B07GBZ4Q68` |
| 查看订单 | `python order_status.py --list` 或 `order_status.py <orderId>` |
| 兑换代币 | `python swap.py SOL USDC 5`（最低交易金额为 $5） |
| 获取兑换报价 | `python swap.py --quote SOL USDC 5` |
| 查看代币 | `python swap.py --list` |

**支持的代币：** SOL、USDC、USDT、BONK、TRUST —— 或者可以直接使用任何代币的地址。

## 工作流程

1. **没有 API 密钥？** 执行 `get_api_key.py`（创建钱包和 API 密钥）。
2. **钱包余额不足？** 使用 `balance.py` 查看钱包地址并进行充值。
3. **准备购买？** 执行 `buy.py <产品链接>`。

## 错误处理

| 错误类型 | 处理方法 |
|---------|-------|
| **余额不足** | 使用 `balance.py` 为钱包充值 |
| **找不到 API 密钥** | 运行 `get_api_key.py` |
| **商品缺货** | 查找其他商品 |
| **交易金额超出限制** | 每单交易的最大金额为 $1,500 |

## 凭据文件（`credentials.json`）

```json
{
  "api_key": "scout_sk_...",
  "wallet_address": "FtbC9x5...",
  "shipping_profile": { "email": "...", "address": "..." }
}
```

请勿泄露 API 密钥。