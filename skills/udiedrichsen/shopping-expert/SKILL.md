---
name: shopping-expert
description: **在线查找并比较产品（Google Shopping）与本地产品（附近的商店）**  
该功能可根据价格、评分、库存情况以及用户偏好自动选择最佳产品，并生成包含购买链接和商店位置的购物清单。适用于需要购买产品、寻找最优惠的价格、比较价格或定位本地商品的场景。支持预算限制（低/中/高或“$X”）、偏好筛选（品牌、功能、颜色），以及在线与本地商店的双模式搜索。
homepage: https://github.com/clawdbot/clawdbot
metadata: {"clawdbot":{"emoji":"🛒","requires":{"bins":["uv"],"env":["SERPAPI_API_KEY","GOOGLE_PLACES_API_KEY"]},"primaryEnv":"SERPAPI_API_KEY","install":[{"id":"uv-brew","kind":"brew","formula":"uv","bins":["uv"],"label":"Install uv (brew)"}]}}
---

# 购物专家

通过智能推荐，在线上和线下查找并比较产品。

## 快速入门

**在线查找产品：**

```bash
uv run {baseDir}/scripts/shop.py "coffee maker" \
  --budget medium \
  --max-results 5
```

**根据预算进行搜索：**

```bash
uv run {baseDir}/scripts/shop.py "running shoes" \
  --budget "$100" \
  --preferences "Nike, cushioned, waterproof"
```

**查找本地商店：**

```bash
uv run {baseDir}/scripts/shop.py "Bio Gemüse" \
  --mode local \
  --location "Hamburg, Germany"
```

**混合搜索（线上+线下）：**

```bash
uv run {baseDir}/scripts/shop.py "Spiegelreflexkamera" \
  --mode hybrid \
  --location "München, Germany" \
  --budget high \
  --preferences "Canon, 4K Video"
```

**搜索美国商店：**

```bash
uv run {baseDir}/scripts/shop.py "running shoes" \
  --country us \
  --budget "$100"
```

## 搜索模式

- **在线**：通过 Google Shopping 在电子商务网站（如 Amazon、Walmart 等）上搜索
- **本地**：通过 Google Places API 查找附近的商店
- **混合**：合并线上和线下的搜索结果并进行排序
- **自动**：根据查询内容智能选择搜索模式（默认）

## 参数

- `query`：产品搜索查询（必填）
- `--mode`：搜索模式（online|local|hybrid|auto，默认：auto）
- `--budget`：预算范围（"low/medium/high" 或 "€X"/"$X"，默认：medium）
- `--location`：本地/混合搜索的位置
- `--preferences`：用逗号分隔的偏好条件（例如："brand:Sony, wireless, black"）
- `--max-results`：返回的最大产品数量（默认：5，最大值：20）
- `--sort-by`：排序方式（相关性|价格低|价格高|评分）
- `--output`：输出格式（text|json，默认：text）
- `--country`：搜索的国家代码（默认：de）。使用 "us" 表示美国，"uk" 表示英国等）

## 预算等级

- **低**：低于 €50
- **中**：€50-€150
- **高**：超过 €150
- **精确**：特定金额（例如："€75", "€250"；在美国搜索时使用 "$X"）

## 输出格式

**默认（文本）**：包含产品详情、评分、库存情况和购买链接的 Markdown 表格

**JSON**：包含所有产品元数据、评分和链接的结构化数据

## 评分算法

产品排名采用加权评分方式：
- **价格匹配（30%）**：在预算范围内的产品获得满分
- **评分（25%）**：评分越高，排名越靠前
- **库存情况（20%）**：有库存 > 限量供应 > 缺货
- **评论数量（15%）**：评论越多，产品越可信
- **运费/距离（10%）**：免费配送或附近的商店得分更高
- **偏好匹配（加分项）**：产品描述中包含的关键词

## 所需的 API 密钥

- **SERPAPI_API_KEY**：在线购物模式（除仅限本地搜索的模式外）所需
- **GOOGLE_PLACES_API_KEY**：仅限本地和混合搜索模式所需

## 限制

- **API 使用限制**：SerpAPI 和 Google Places 有使用配额
- **实时数据**：价格和库存情况可能会变化
- **库存准确性**：在线库存信息基于最后一次 API 更新
- **本地库存**：通过 Places API 无法保证商店的库存情况

## 错误处理

- 查询无效 → 返回错误信息并提供改进建议
- 未找到结果 → 放宽筛选条件并重试
- API 请求失败 → 采用指数级退避策略进行重试（最多尝试 3 次）
- API 密钥缺失 → 显示错误信息并提供设置指南