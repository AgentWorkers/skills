---
name: bricklink
description: "BrickLink商店API辅助工具/命令行界面（OAuth 1.0请求签名）：支持处理订单、查询/更新商店库存、管理产品目录、类别、颜色信息、接收用户反馈以及发送推送通知等功能。"
summary: "BrickLink Store API CLI: orders, inventory, catalog, pricing, feedback."
version: 1.3.3
homepage: https://github.com/odrobnik/bricklink-skill
metadata:
  openclaw:
    emoji: "🧱"
    requires:
      bins: ["python3"]
      env: ["BRICKLINK_CONSUMER_KEY", "BRICKLINK_CONSUMER_SECRET", "BRICKLINK_TOKEN_VALUE", "BRICKLINK_TOKEN_SECRET"]
---

# BrickLink

请使用 `scripts/bricklink.py` 命令。

## 设置

有关先决条件和设置说明，请参阅 [SETUP.md](SETUP.md)。

## 命令

### 仅读操作

- `bricklink.py get-orders [--direction in|out] [--status ...] [--include-status ...] [--exclude-status ...] [--filed true|false]` - 列出您收到或下的订单。
- `bricklink.py get-order <order_id>` - 获取特定订单的详细信息。
- `bricklink.py get-order-items <order_id>` - 获取特定订单中的商品批次信息。
- `bricklink.py get-order-messages <order_id>` - 获取与特定订单相关的消息。
- `bricklink.py get-order-feedback <order_id>` - 获取与特定订单相关的反馈信息。
- `bricklink.py get-feedback [--direction in|out]` - 列出您收到的反馈（`in`）或发布的反馈（`out`）。
- `bricklink.py get-feedback-item <feedback_id>` - 根据 ID 获取单条反馈信息。
- `bricklink.py get-notifications` - 列出未读的推送通知（位于 `/notifications` 目录下）。
- `bricklink.py get-categories` - 列出所有商品类别。
- `bricklink.py get-category <category_id>` - 根据 ID 获取单个类别信息。
- `bricklink.py get-colors` - 列出所有商品颜色。
- `bricklink.py get-color <color_id>` - 根据 ID 获取单个颜色信息。
- `bricklink.py get-inventories [--item-type ...] [--status ...] [--category-id ...] [--color-id ...]` - 列出您店铺的库存信息（支持筛选条件）。
- `bricklink.py get-inventory <inventory_id>` - 根据 ID 获取单个库存记录。
- `bricklink.py get-item <type> <no>` - 获取商品信息（如 PART/SET/MINIFIG 等）。
- `bricklink.py get-supersets <type> <no> [--color-id N]` - 列出包含指定商品的其他商品。
- `bricklink.py get-subsets <type> <no> [--color-id N] [--box true|false] [--instruction true|false] [--break-minifigs true|false] [--break-subsets true|false]` - 将商品拆分为其包含的子商品。
- `bricklink.py get-price-guide <type> <no> [--color-id N] [--guide-type stock|sold] [--new-or-used N|U] [--country-code XX] [--region ...] [--currency-code XXX] [--vat N|Y|O]` - 获取价格指南统计信息。
- `bricklink.py get-known-colors <type> <no>` - 列出商品已知的颜色信息。

### 修改操作（需要使用 `--yes` 参数）

> **注意：** 修改订单状态（如 `update-order`、`update-order-status`、`update-payment-status`）仅适用于 **店铺订单**（方向为 `out`，即您作为卖方的订单）。购买订单（方向为 `in`）会返回 404 错误——BrickLink API 不允许买家修改订单状态或删除/归档收到的订单。请使用 BrickLink 网站进行这些操作。

- `bricklink.py update-order <order_id> --yes [--json body.json] [--remarks ...] [--is-filed true|false] [--shipping-...] [--cost-...]` - 更新订单字段（如追踪信息、备注、运输/费用信息）。仅适用于店铺订单。
- `bricklink.py update-order-status <order_id> <status> --yes` - 更新订单状态。仅适用于店铺订单。
- `bricklink.py update-payment-status <order_id> <payment_status> --yes` - 更新订单的支付状态。仅适用于店铺订单。
- `bricklink.py send-drive-thru <order_id> --yes` - 为订单发送“Drive Thru”通知邮件。
- `bricklink.py post-feedback --yes [--json body.json] [--order-id N --rating 0|1|2 --comment ...]` - 为订单发布新的反馈信息。
- `bricklink.py reply-feedback <feedback_id> --yes [--json body.json] --reply ...` - 回复收到的反馈信息。
- `bricklink.py create-inventory --yes [--json body.json] [--item-type ... --item-no ... --color-id N --quantity N --unit-price ... --new-or-used N|U ...]` - 创建单个库存记录。
- `bricklink.py create-inventories --yes [--json body.json] [--item-type ... --item-no ... --color-id N --quantity N --unit-price ... --new-or-used N|U ...]` - 一次性创建多个库存记录。
- `bricklink.py update-inventory <inventory_id> --yes [--json body.json] --quantity N --unit-price ... --new-or-used N|U --remarks ...]` - 更新库存记录。
- `bricklink.py delete-inventory <inventory_id> --yes` - 删除库存记录。

### 其他实用命令

- `bricklink.py order-detail-html <order_id> [--out path] [--inline-images]` - 获取订单及商品信息，并生成简洁的 HTML 页面（类似于 BrickLink 的 orderDetail.asp 页面）。