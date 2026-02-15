---
name: csfloat
description: 向 csfloat.com 查询关于皮肤的数据
homepage: https://docs.csfloat.com/#introduction
metadata: {"clawdbot":{"emoji":"𝒇","requires":{"bins":["jq"],"env":["CSFLOAT_API_KEY"]}}}
---


# CSFloat 技能

直接从 Clawdbot 查询 CSFloat 皮肤数据。

## 设置

1. 获取您的 API 密钥：[https://csfloat.com/profile](https://csfloat.com/profile)，在“开发者”（Developer）选项卡下。
2. 点击“新建密钥”（New Key）生成 API 密钥。
3. 设置环境变量：
   ```bash
   export CSFLOAT_API_KEY="your-api-key"
   ```

## 使用方法

所有命令均使用 `curl` 来调用 Trello REST API。在请求头中添加 `Authorization: ` 以使用 API 密钥。

### 获取所有列表（Get all listings）
```bash
curl -s "https://csfloat.com/api/v1/listings" --header "Authorization: $CSFLOAT_API_KEY" --header "Content-Type: application/json" | jq '.data.[] | { "id", "item", "price" }'
```

### 获取特定列表（Get specific listing）
```bash
curl -s https://csfloat.com/api/v1/listings/$LISTING_ID --header "Authorization: $CSFLOAT_API_KEY" --header "Content-Type: application/json"
```

### 创建列表（Create a listing）
```bash
curl -X POST "https://csfloat.com/api/v1/listings" \
-H "Authorization: $LISTING_ID; Content-Type: application/json" \
-d '{"asset_id": 21078095468, "type": "buy_now", "price": 8900, "description": "Just for show", "private": false}'
```

创建列表时需要使用以下参数：

| 参数            | 默认值    | 描述                | 是否可选     |
|-----------------|---------|------------------|-----------|
| type           | buy_now   | `buy_now` 或 `auction`       | 是         |
| asset_id        |         | 要发布的物品 ID           | 否         |
| price          |         | `buy_now` 价格；或拍卖中的当前出价/保留价 | 否（仅限 `buy_now`） |
| max_offer_discount | （在用户配置中设置）| `buy_now` 时的最高折扣。会覆盖您配置中的默认值 | 是         |
| reserve_price     |         | 拍卖的起拍价           | 否（仅限 `auction`） |
| duration_days    |         | 拍卖持续时间（以天计）：1、3、5、7 或 14 | 否（仅限 `auction`） |
| description     |         | 用户自定义的描述（最多 180 个字符）   | 是         |
| private         | false     | 如果设置为 `true`，列表将隐藏于公开搜索结果中 | 是         |

## 注意事项

- 资产 ID 来自 Steam。