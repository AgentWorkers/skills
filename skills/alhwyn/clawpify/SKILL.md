---
name: clawpify
description: 通过 GraphQL Admin API 查询和管理 Shopify 商店。该 API 可用于处理产品、订单、客户、库存、折扣以及所有与 Shopify 相关的数据操作。
dependencies:
  - Tool: shopify_graphql (from MCP server or custom function)
---

# Shopify GraphQL Admin API

这是一项用于与Shopify的GraphQL Admin API进行交互的综合性技能。通过该技能，Claude能够查询和管理Shopify商店数据的所有方面。

## 何时使用此技能

当用户需要执行以下操作时，请使用此技能：
- 产品（列出、搜索、创建、更新、删除）
- 订单（查看、取消、发货）
- 客户（列出、创建、更新）
- 库存（检查库存水平、调整数量）
- 优惠券（创建优惠券代码、管理促销活动）
- 任何其他Shopify商店相关操作

## 需要权限的关键操作

重要提示：在执行以下任何操作之前，必须先获得用户的明确许可：
- 退款：创建退款（涉及永久性的财务交易）
- 订单取消：取消订单（可能会触发退款）
- 礼品卡停用：永久禁用礼品卡
- 库存调整：修改库存水平
- 产品删除：永久删除产品
- 优惠券激活：更改客户的价格

请始终向用户说明将要进行的更改，并等待用户的确认。

## 使用方法

1. 使用`shopify_graphql`工具来执行查询。
2. 检查`errors`（GraphQL错误）和`userErrors`（验证错误）。
3. 对于大量数据，使用`first`/`after`进行分页处理。
4. 将所有ID格式化为：`gid://shopify/Resource/123`。

## 可参考的文档

有关详细模式和示例，请参阅以下文档：
- products.md - 产品及变体管理
- orders.md - 订单操作
- customers.md - 客户管理
- inventory.md - 库存管理
- discounts.md - 优惠券代码及促销活动
- collections.md - 产品系列
- fulfillments.md - 订单发货
- refunds.md - 退款处理
- draft-orders.md - 草稿订单创建
- gift-cards.md - 礼品卡管理
- webhooks.md - 事件订阅
- locations.md - 商店位置信息
- marketing.md - 营销活动
- markets.md - 多市场设置
- menus.md - 导航菜单
- metafields.md - 自定义数据字段
- pages.md - 商店页面
- blogs.md - 博文管理
- files.md - 文件上传
- shipping.md - 运输配置
- shop.md - 商店信息
- subscriptions.md - 订阅管理
- translations.md - 内容翻译
- segments.md - 客户分组
- bulk-operations.md - 批量数据操作

## 快速示例

### 列出最近的交易记录
```graphql
query {
  orders(first: 10, sortKey: CREATED_AT, reverse: true) {
    nodes {
      id
      name
      totalPriceSet {
        shopMoney { amount currencyCode }
      }
      customer { displayName }
    }
  }
}
```

### 搜索产品
```graphql
query {
  products(first: 10, query: "title:*shirt* AND status:ACTIVE") {
    nodes {
      id
      title
      status
    }
  }
}
```

### 检查库存情况
```graphql
query GetInventory($id: ID!) {
  inventoryItem(id: $id) {
    id
    inventoryLevels(first: 5) {
      nodes {
        quantities(names: ["available"]) {
          name
          quantity
        }
        location { name }
      }
    }
  }
}
```

## 错误处理

务必检查响应中的内容：
- `errors`数组：表示GraphQL语法错误
- `userErrors`：表示验证问题

## 最佳实践

1. 仅请求所需的字段以优化响应大小。
2. 对于可能包含大量数据的列表，使用分页功能。
3. 在所有mutation响应中检查`userErrors`。
4. 在执行危险操作前先获取用户许可。
5. 以清晰的方式向用户展示查询结果。
6. 对于大量数据的导出/导入操作，使用批量处理功能。
7. 采用指数级退避策略来处理请求速率限制。