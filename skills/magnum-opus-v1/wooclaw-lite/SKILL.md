---
name: openclaw-connector
description: 通过 OpenClaw Connector Lite 插件连接到 WooCommerce 商店，以获取订单和商品信息。
user-invocable: true
---

# OpenClaw 连接器

此技能允许您与 WooCommerce 商店进行交互。您可以查看订单状态、搜索产品以及验证商店的连接是否正常。

## 配置

需要以下环境变量：
*   `OPENCLAW_STORE_URL`：您的 WordPress 网站的完整 URL（例如：https://example.com）。
*   `OPENCLAW_STORE_SECRET`：来自 OpenClaw Connector Lite 插件设置的密钥。

## 工具

### `check_order`
使用此工具获取特定订单的详细信息。
*   **输入：** `id`（整数） - 订单 ID。
*   **输出：** 包含订单状态、总金额、客户信息和商品信息的格式化字符串。

### `find_product`
使用此工具按名称或 SKU 搜索产品。
*   **输入：** `query`（字符串） - 搜索关键词。
*   **输出：** 匹配产品的列表，其中包含产品 ID、库存情况和价格。

### `store_status`
使用此工具检查商店是否可访问以及插件是否处于激活状态。
*   **输入：** （无）
*   **输出：** 连接状态信息。