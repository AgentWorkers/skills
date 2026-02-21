---
name: forage-shopping
description: 在多个商家之间搜索和比较产品。通过价格对比和购物推荐找到最划算的交易。
homepage: https://forageshopping.com
user-invocable: true
metadata: {"openclaw":{"requires":{},"emoji":"🌿"}}
---
您可以使用 Forage Shopping MCP 服务器来搜索产品并进行价格比较。

## 设置

将 Forage MCP 服务器添加到您的 `openclaw.json` 文件中：

```json
{
  "mcpServers": {
    "forage-shopping": {
      "url": "https://forageshopping.com/mcp"
    }
  }
}
```

无需 API 密钥——远程服务器会处理所有操作。

## 可用工具

- **search_products**：在多个商家中搜索产品。可以输入自然语言查询，例如 “价格低于 120 英镑的跑鞋” 或 “最佳降噪耳机”。
- **compare_prices**：比较多个零售商中特定产品的价格。需要提供产品的确切名称，例如 “Sony WH-1000XM5”。
- **find_deals**：在指定类别中查找当前最优惠的交易（可选设置预算）。需要提供类别名称（例如 “咖啡机”），并可选设置预算（例如 “200 英镑”）。

## 使用方法

当用户询问购买商品、查找产品、比较价格或寻找优惠时，请按照以下步骤操作：

1. 使用 `search_products` 来查找符合查询条件的产品选项。
2. 如果用户对某个特定产品感兴趣，使用 `compare_prices` 来找到价格最优惠的零售商。
3. 如果用户希望在某个类别中寻找优惠交易，使用 `find_deals`。

结果应清晰地显示产品名称、价格、零售商以及购买链接。推荐时请基于产品的性价比（而不仅仅是最低价格），并在可能的情况下说明配送费用和退换货政策。