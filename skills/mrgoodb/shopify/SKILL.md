---
name: shopify
description: 通过 Admin API 管理 Shopify 店铺中的产品、订单、客户和库存信息。
metadata: {"clawdbot":{"emoji":"🛒","requires":{"env":["SHOPIFY_STORE","SHOPIFY_ACCESS_TOKEN"]}}}
---

# Shopify

用于管理电子商务店铺。

## 环境配置

```bash
export SHOPIFY_STORE="your-store.myshopify.com"
export SHOPIFY_ACCESS_TOKEN="shpat_xxxxxxxxxx"
```

## 列出产品

```bash
curl "https://$SHOPIFY_STORE/admin/api/2024-01/products.json" \
  -H "X-Shopify-Access-Token: $SHOPIFY_ACCESS_TOKEN"
```

## 创建产品

```bash
curl -X POST "https://$SHOPIFY_STORE/admin/api/2024-01/products.json" \
  -H "X-Shopify-Access-Token: $SHOPIFY_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "product": {
      "title": "New Product",
      "body_html": "<p>Description</p>",
      "vendor": "My Brand",
      "product_type": "Clothing",
      "variants": [{"price": "29.99", "sku": "SKU123"}]
    }
  }'
```

## 列出订单

```bash
curl "https://$SHOPIFY_STORE/admin/api/2024-01/orders.json?status=any" \
  -H "X-Shopify-Access-Token: $SHOPIFY_ACCESS_TOKEN"
```

## 获取订单详情

```bash
curl "https://$SHOPIFY_STORE/admin/api/2024-01/orders/{order_id}.json" \
  -H "X-Shopify-Access-Token: $SHOPIFY_ACCESS_TOKEN"
```

## 更新库存

```bash
curl -X POST "https://$SHOPIFY_STORE/admin/api/2024-01/inventory_levels/set.json" \
  -H "X-Shopify-Access-Token: $SHOPIFY_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"location_id": 123, "inventory_item_id": 456, "available": 100}'
```

## 链接：
- 管理后台：https://admin.shopify.com
- 文档：https://shopify.dev/docs/api/admin-rest