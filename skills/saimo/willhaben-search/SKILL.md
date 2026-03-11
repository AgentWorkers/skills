---
name: willhaben-search
description: Willhaben市场搜索API：用于在奥地利最大的分类广告平台上查找房源信息、浏览分类目录以及获取房源详情。
homepage: https://api.nochda.at
metadata: {"clawdbot":{"emoji":"🔍"}}
---
# willhaben-search

使用基于人工智能的语义搜索功能，在 willhaben.at（奥地利最大的在线市场）上搜索和浏览商品列表。

## API 基础信息

基础 URL：`https://api.nochda.at`

无需身份验证。所有接口返回 JSON 格式的数据。

```bash
curl "https://api.nochda.at/api/health"
```

**请求速率限制：**
- 全局请求速率限制为每分钟 50 次；
- 搜索和推荐功能的请求速率限制为每分钟 10 次。

## 典型工作流程

1. 使用 `GET /api/categories/suggest?q=...` 查找合适的分类。
2. 使用 `GET /api/search?categoryId=...&query=...` 搜索商品列表。
3. 使用 `GET /api/listings/:id` 获取商品详情。

## 接口说明

### 建议分类（语义搜索）

`GET /api/categories/suggest?q=<query>`

利用人工智能为用户推荐最合适的分类。当不知道从哪个分类开始搜索时，可以从这里开始。

**响应格式：**
```json
{
  "suggestions": [
    {"id": 4552, "label": "Fahrräder", "parentLabel": "Sport/Sportgeräte", "score": 1.0},
    {"id": 2145, "label": "Mountainbikes", "parentLabel": "Fahrräder", "score": 0.82}
  ]
}
```

在搜索时，使用匹配度最高的分类的 `id` 作为 `categoryId` 参数。最多返回 5 个按相关性排序的分类建议（相关性评分范围为 0–1）。

---

### 搜索商品列表

`GET /api/search?categoryId=<id>&query=<query>`

在指定分类内进行语义搜索。该接口能够理解自然语言查询。

**查询参数：**

| 参数 | 是否必填 | 说明 |
|---------|---------|-------------|
| `categoryId` | 是 | 分类 ID（来自 `suggest` 或 `browse` 接口） |
| `query` | 是 | 自然语言搜索关键词（最多 500 个字符） |
| `maxPrice` | 否 | 最高价格（单位：EUR） |
| `recentDays` | 否 | 仅显示过去 N 天内的商品列表 |

**响应格式：**
```json
{
  "results": [
    {
      "id": 12345,
      "title": "Giant Trance X 29 2024",
      "description": "Full suspension trail bike, excellent condition...",
      "price": 1800,
      "location": "Wien",
      "url": "https://willhaben.at/iad/kaufen-und-verkaufen/d/...",
      "images": ["https://cache.willhaben.at/...jpg"],
      "publishedAt": "2026-03-08T10:30:00Z",
      "similarity": 0.87
    }
  ],
  "totalCandidates": 85
}
```

搜索结果按语义相关性排序。每个结果都包含指向原始 willhaben 商品页面的直接链接。最多返回 40 个结果。

---

### 获取商品详情

`GET /api/listings/:id`

获取特定商品的详细信息，包括价格对比数据。

**响应格式：**
```bash
curl "https://api.nochda.at/api/listings/12345"
```

`compAnalysis` 参数用于将当前商品的价格与同一类别中其他 30 个类似商品的价格进行比较。如果数据不足，该字段可能为空。

---

### 浏览分类

- **根分类：**  
```bash
curl "https://api.nochda.at/api/categories"
```

- **所有分类（扁平列表）：**  
```bash
curl "https://api.nochda.at/api/categories/all"
```

- **分类的子分类：**  
```bash
curl "https://api.nochda.at/api/categories/123/children"
```

返回的响应格式为：`{"parent": {...}, "children": [...] }`。

- **按名称搜索分类：**  
```bash
curl "https://api.nochda.at/api/categories/search?q=auto"
```

名称重复的分类会附带一个 `disambiguatedLabel`（例如：“PKW (Auto/Motorrad)”）。

所有分类对象包含以下字段：`id`、`label`、`parentCategoryId`、`image`。

## 错误处理

错误信息以 JSON 格式返回：`{"error": "错误描述"}`。

| 状态码 | 含义 |
|--------|---------|
| 400 | 参数无效或缺失 |
| 404 | 资源未找到 |
| 429 | 请求速率限制——请在 `Retry-After` 头部字段指定的时间后重试 |
| 500 | 服务器错误 |

## 注意事项：

- 所有价格均以欧元（EUR）显示。
- 搜索功能基于人工智能，支持自然语言查询（例如：“cozy armchair for reading”）。
- 分类之间存在层级结构（根分类 → 子分类）；搜索时会包含所有子分类。
- 系统会始终提供商品的完整链接（`url`），以便用户可以查看 willhaben 上的商品详情页面。