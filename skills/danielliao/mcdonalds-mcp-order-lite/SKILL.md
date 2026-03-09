---
name: mcdonalds-mcp-order-lite
description: 您可以通过官方的MCP服务器（https://mcp.mcd.cn）使用Bearer MCP令牌，通过Streamable HTTP / JSON-RPC协议来下达麦当劳中国的配送订单。该功能适用于用户浏览麦当劳的配送地址、查询门店菜单项目、查看餐品详情、计算价格、创建配送订单、查询订单状态或查看麦当劳的优惠券/积分等操作。同时，该功能也适用于将MCP集成到诸如Cursor、Cherry Studio、Trae或其他代理程序中。这个轻量级包故意没有嵌入任何令牌，仅包含核心的可重用文件。
---
请使用官方的麦当劳中国（McDonald's China）MCP工具链，切勿使用从网站抓取的API。

## 核心工作流程

1. 确定配送地址。
2. 首先调用 `delivery-query-addresses` 函数。
3. 从返回的地址记录中选取匹配的地址，并获取 `addressId`、`storeCode` 和 `beCode`。
4. 使用 `query-meals` 函数查询该店铺的菜单。
5. 如有需要，使用 `query-meal-detail` 函数查询选定的餐品详情。
6. 在下单前调用 `calculate-price` 函数计算总价。
7. 向用户显示实际需要支付的金额并等待用户确认。
8. 只有在用户确认后，才调用 `create-order` 函数创建订单。
9. 将 `payH5Url` 返回给用户。
10. 在用户完成支付后，调用 `query-order` 函数查询订单状态。

## 重要限制

- 使用服务器地址：`https://mcp.mcd.cn`。
- 发送请求时需附加 `Authorization: Bearer <TOKEN>` 头部信息。
- MCP 协议版本必须为 `2025-06-18` 或更低版本。
- 请尽量减少请求量；文档规定每分钟每个令牌的最大请求量为 600 次。
- 不得自行生成 `storeCode`、`beCode` 或 `addressId`。
- 对于配送订单，始终使用 `delivery-query-addresses` 或 `delivery-create-address` 函数返回的参数。
- 在创建订单前，务必使用 `calculate-price` 函数进行价格核对。
- 文档指出，当前版本不支持修改默认的套餐选项。

## 工具列表

### 配送相关工具
- `delivery-query-addresses`：列出已保存的配送地址
- `delivery-create-address`：添加新的配送地址
- `query-store-coupons`：查询适用于所选店铺的优惠券
- `query-meals`：查询所选店铺的菜单
- `query-meal-detail`：查看餐品/套餐详情
- `calculate-price`：计算最终价格
- `create-order`：创建可支付的配送订单
- `query-order`：查询订单创建/支付后的状态

### 其他实用工具
- `available-coupons`：可使用的优惠券
- `auto-bind-coupons`：一键领取当前优惠券
- `query-my-coupons`：查看优惠券信息
- `list-nutrition-foods`：查询食品的营养信息
- `query-my-account`：查看积分账户信息
- `mall-points-products`、`mall-product-detail`、`mall-create-order`：积分商城相关功能
- `campaign-calendar`：营销日历
- `now-time-info`：获取服务器当前时间

## 推荐的用户操作流程

当用户说“帮我点麦当劳”或类似指令时：

- 首先确认用户的预算或所需商品（如果尚未确定）。
- 从已保存的地址中查找配送地址。
- 通过 `query-meals` 函数查找合适的商品。
- 使用 `calculate-price` 函数计算一个或多个商品组合的总价。
- 向用户展示最便宜或最符合需求的选项，并显示实际需要支付的金额。
- 只有在用户明确确认后，才创建订单。
- 订单创建完成后，发送支付链接。
- 支付完成后，通过 `query-order` 函数查询订单状态，而不是默认认为订单已经成功。

## 本技能相关的文件

- 请参考 `references/api.md` 文件，其中包含简洁的API手册和经过测试的字段名称。
- 在需要确定性测试或通过命令行界面（CLI）操作时，请使用 `scripts/mcd_rpc.py` 文件。
- `client.py` 文件提供了对这些远程MCP接口的Python封装。
- `nlp_processor.py` 文件包含用于解析用户订单意图的简单文本处理功能。
- `tools.py` 文件包含一些高级辅助函数。

## 打包说明

- 保持技能文件夹的结构简洁，仅添加必要的文档。
- 在打包前删除临时文件（如 `__pycache__` 文件）。