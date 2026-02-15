---
name: marktplaats
description: 支持在 Marktplaats.nl 的所有分类中搜索分类广告，并提供过滤功能。
homepage: https://www.marktplaats.nl
metadata: {"clawdbot":{"emoji":"🇳🇱","requires":{"bins":["node"]}}}
---

# Marktplaats Skill

您可以搜索 Marktplaats 上的任何类别，根据条件或配送方式筛选结果，查看类别列表，并获取商品详情。

## 命令行界面 (CLI)

```bash
npm install -g {baseDir}

# Search
marktplaats-search "<query>" [options]
  -n, --limit <num>         Number of results (default: 10, max: 100)
  -c, --category <id>       Category ID (top-level)
  --min-price <cents>       Minimum price in euro cents
  --max-price <cents>       Maximum price in euro cents
  --sort <relevance|date|price-asc|price-desc>
  --param key=value         Filter by attribute (repeatable)
  --details [target]        Fetch details for "first" result or URL/ID
  --json                    Output raw JSON

# Categories
marktplaats-categories            # main categories
marktplaats-categories <id>       # sub-categories for a category
  --json                          Output raw JSON
```

## 过滤器

常见的过滤器可以通过 `--param` 参数进行设置：

| 过滤器 | 可能的值 |
|--------|--------|
| `condition` | 新品 (New), 二手 (Refurbished), 几乎全新 (Zo goed als nieuw), 二手商品 (Gebruikt), 不可用 (Niet werkend) |
| `delivery` | 自取 (Ophalen), 邮寄 (Verzenden) |
| `buyitnow` | true (仅限直接购买) |

英文别名也可以使用：`new`, `used`, `like-new`, `pickup`, `shipping`

## 示例

```bash
# New laptops only
marktplaats-search "laptop" --param condition=Nieuw

# Used cameras with shipping
marktplaats-search "camera" --param condition=Gebruikt --param delivery=Verzenden

# Cars under €15k
marktplaats-search "bmw 330d" --category 96 --max-price 1500000

# Furniture, pickup only
marktplaats-search "eettafel" --param delivery=Ophalen --sort price-asc

# Get details for first result
marktplaats-search "iphone" -n 1 --details first

# List all categories
marktplaats-categories

# BMW sub-categories
marktplaats-categories 96
```

## 程序化 API (ESM)

```js
import { searchListings, fetchCategories, getListingDetails } from '{baseDir}';

// Search with filters
const results = await searchListings({
  query: 'espresso machine',
  params: { condition: 'Nieuw', delivery: 'Verzenden' },
  limit: 10,
});

// Get categories
const categories = await fetchCategories();  // top-level
const bmw = await fetchCategories(96);       // BMW sub-categories

// Fetch listing details
const details = await getListingDetails(results.listings[0].vipUrl);
```

## 注意事项：

- 价格以 **欧分** 为单位（例如：€15,000 表示 150,000 欧分）。
- 搜索结果包含商品的完整网址。
- 使用 `--json` 参数可以查看所有可用的筛选选项和字段。
- 搜索结果后会显示筛选提示信息。