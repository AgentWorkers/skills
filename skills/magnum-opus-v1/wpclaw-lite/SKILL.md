---
name: wpclaw-connector
description: 通过 WPClaw Connector 插件连接到 WooCommerce 商店，以获取订单和商品信息。
user-invocable: true
---

# WPClaw Connector

该技能允许您与WooCommerce商店进行交互。您可以查看订单状态、搜索产品以及验证商店的连接是否正常。

## 配置

需要以下环境变量：
*   `WPCLAW_STORE_URL`：您的WordPress网站的完整URL（例如：https://example.com）。
*   `WPCLAW_STORE_SECRET`：来自WPClaw Connector插件设置的密钥。

## 工具

### `check_order`
使用此工具获取特定订单的详细信息。
*   **输入：** `id`（整数） - 订单ID。
*   **输出：** 包含订单状态、总金额、客户信息和商品信息的格式化字符串。

### `find_product`
使用此工具按名称或SKU搜索产品。
*   **输入：** `query`（字符串） - 搜索词。
*   **输出：** 匹配的产品列表，包含产品ID、库存数量和价格。

### `store_status`
使用此工具检查商店是否可访问以及插件是否处于激活状态。
*   **输入：** （无）
*   **输出：** 连接状态信息。