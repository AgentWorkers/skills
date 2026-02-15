---
name: find-products
version: 1.0.0
description: 使用 ProductHunt 提供的结构化分析数据，搜索并发现热门产品。当用户询问产品推荐、工具比较或热门应用程序时，可以使用这些数据。
homepage: https://github.com/xiazhefengzhi/find-products-skill
---

# find-products

该技能用于从 trend-hunt.com 获取 ProductHunt 中的产品信息，并进行结构化分析。

## 使用场景

当用户执行以下操作时，可触发此技能：
- 请求产品或工具推荐（例如：“哪些是最佳的人工智能视频工具？”）
- 希望比较某个类别中的产品
- 询问热门产品或应用程序
- 需要寻找特定产品的替代品
- 询问“有哪些工具可用于 X”

## 搜索方法

向搜索 API 发送 GET 请求：

```bash
curl -s "https://trend-hunt.com/api/search?q=QUERY&locale=LOCALE&limit=LIMIT&category=CATEGORY"
```

### 参数

| 参数          | 是否必填 | 默认值     | 说明                          |
|---------------|---------|-----------|-----------------------------------|
| `q`           | 是       |          | 搜索关键词（支持英文和中文）                   |
| `locale`       | 否       | `en`       | 语言：`en` 或 `zh`                     |
| `limit`        | 否       | `10`       | 结果数量（1–20个）                     |
| `category`     | 否       |          | 按类别过滤                        |

### 常见类别

`AI`, `Productivity`, `Developer Tools`, `Design`, `Marketing`, `Analytics`, `Writing`, `Video`, `Audio`, `Education`, `Finance`, `Social`, `Health`, `E-commerce`

## 响应格式

API 返回 JSON 数据：

```json
{
  "success": true,
  "query": "video editor",
  "locale": "en",
  "count": 5,
  "products": [
    {
      "slug": "product-slug",
      "name": "Product Name",
      "tagline": "Short description",
      "category": "AI",
      "upvotes": 523,
      "hypeScore": 85,
      "utilityScore": 78,
      "metaphor": "It's like Canva but for video editing",
      "phUrl": "https://www.producthunt.com/posts/product-slug",
      "websiteUrl": "https://product.com",
      "positiveReviews": ["Great UI", "Fast rendering"],
      "negativeReviews": ["Limited free tier"],
      "newbieQA": [...],
      "translations": [...]
    }
  ]
}
```

## 结果展示方式

每个产品的展示格式如下：

```
### Product Name
⭐ Upvotes: 523 | Hype: 85 | Utility: 78
> Metaphor: "It's like Canva but for video editing"

**Tagline**: Short description
**Category**: AI
**Pros**: Great UI, Fast rendering
**Cons**: Limited free tier

🔗 [ProductHunt](phUrl) | [Website](websiteUrl)
```

## 示例

### 示例 1：查找人工智能写作工具
```bash
curl -s "https://trend-hunt.com/api/search?q=AI+writing&locale=en&limit=5"
```

### 示例 2：使用中文进行搜索
```bash
curl -s "https://trend-hunt.com/api/search?q=视频编辑&locale=zh&limit=5"
```

### 示例 3：按类别过滤结果
```bash
curl -s "https://trend-hunt.com/api/search?q=automation&category=Productivity&limit=10"
```

## 使用提示

- 使用英文关键词可获得更广泛的结果（数据库中英文内容较多）；
- 当 `locale=zh` 时，翻译后的字段会显示在 `translations` 数组中；
- 产品按点赞数排序（最受欢迎的产品排在前面）；
- `hypeScore` 表示社区的关注度，`utilityScore` 表示产品的实际用途；
- `metaphor` 字段提供了“这个工具就像 Y 对于 X 一样”的简洁描述；
- 如果未找到结果，请尝试使用更宽泛的关键词或替代关键词。