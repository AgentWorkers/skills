---
name: serpapi
description: 统一搜索API，支持谷歌（Google）、亚马逊（Amazon）、Yelp、OpenTable、沃尔玛（Walmart）等众多平台。无论您是在搜索产品、本地商家、餐厅、购物信息、图片、新闻，还是进行任何网页搜索，都可以使用该API。只需一个API密钥，即可访问多个搜索引擎。
homepage: https://serpapi.com
metadata: {"clawdbot":{"emoji":"🔍","requires":{"env":["SERPAPI_API_KEY"]}}}
---

# SerpAPI - 统一搜索平台

SerpAPI 通过一个统一的 API 提供来自 Google、Amazon、Yelp、OpenTable 以及 20 多个其他搜索引擎的结构化数据。

## 设置

1. 从 [https://serpapi.com](https://serpapi.com) 获取 API 密钥（免费 tier：每月 100 次搜索）。
2. 设置环境变量：`export SERPAPI_API_KEY=your-key-here`。
3. （可选）在 `<workspace>/TOOLS.md` 中设置默认搜索位置：
   ```markdown
   ## SerpAPI
   Default location: Pittsburgh, PA
   ```

## 使用方法

```bash
# General syntax
<skill>/scripts/serp.py <engine> "<query>" [options]

# Examples
serp.py google "best coffee shops"
serp.py google_maps "restaurants near me" --location "15238"
serp.py amazon "mechanical keyboard" --num 10
serp.py yelp "pizza" --location "New York, NY"
serp.py google_shopping "standing desk"
```

## 可用的搜索引擎

| 搜索引擎 | 适用场景 | 主要功能 |
|--------|---------|--------------|
| `google` | 通用网页搜索 | 自然搜索结果、知识图谱、本地商家信息 |
| `google_maps` | 本地地点/商家信息 | 评分、评论、营业时间、GPS 坐标 |
| `google_shopping` | 产品搜索 | 价格、商家信息、评论 |
| `google_images` | 图片搜索 | 图片缩略图、图片来源 |
| `google_news` | 新闻文章 | 标题、来源、发布日期 |
| `amazon` | 亚马逊产品信息 | 价格、评分、评论、Prime 会员状态 |
| `yelp` | 本地商家信息 | 评论、评分、分类 |
| `opentable` | 餐厅评论 | 餐厅评价、评分 |
| `walmart` | 沃尔玛产品信息 | 价格、库存情况 |
| `ebay` | eBay 商品信息 | 价格、出价、交易条件 |
| `tripadvisor` | 旅行/景点信息 | 酒店、餐厅、活动推荐 |

## 参数选项

| 参数 | 说明 |
|--------|-------------|
| `--location`, `-l` | 本地搜索的位置（城市、邮政编码、地址） |
| `--num`, `-n` | 搜索结果数量（默认：10 条） |
| `--format`, `-f` | 输出格式：`json`（默认）或 `text` |
| `--type`, `-t` | 搜索类型：`shop`（产品）、`isch`（图片）、`nws`（新闻）、`vid`（视频） |
| `--page`, `-p` | 分页页码 |
| `--gl` | 国家代码（例如：`us`、`uk`、`de`） |
| `--hl` | 语言代码（例如：`en`、`es`、`fr`） |

## 如何选择合适的搜索引擎

**查找本地商家/餐厅：**
- `google_maps`：适合查找地点、营业时间、餐厅评价。
- `yelp`：提供详细的餐厅评价和评分。
- `opentable`：专注于餐厅的用餐评价。

**购物/产品搜索：**
- `google_shopping`：跨商家比较产品价格。
- `amazon`：提供亚马逊产品的详细信息及 Prime 会员相关内容。
- `walmart`：查询 Walmart 的商品库存和价格。
- `ebay`：查看 eBay 上的商品信息、出价和交易条件。

**通用搜索：**
- `google`：获取网页内容、新闻文章等通用信息。
- `google_news`：获取最新新闻文章。
- `google_images`：搜索图片。

## 使用示例

### 查找指定地点附近的餐厅
```bash
serp.py google_maps "italian restaurants" --location "Pittsburgh, PA" --num 5
```

### 比较产品价格
```bash
serp.py google_shopping "sony wh-1000xm5" --num 10
```

### 查看亚马逊产品的评论和价格
```bash
serp.py amazon "standing desk" --num 10
```

### 获取 Yelp 上的本地服务评价
```bash
serp.py yelp "plumber" --location "15238"
```

### 搜索特定主题的新闻
```bash
serp.py google_news "AI regulation" --num 5
```

## 输出格式

**JSON（默认格式）：** SerpAPI 返回的完整结构化数据，适合程序化调用或需要详细信息的情况。

**文本格式（`--format text`）：** 以人类可读的形式呈现搜索结果，适合快速获取信息。

## 集成说明

- 返回的结果为结构化的 JSON 数据，可方便地解析和提取所需信息。
- 本地搜索结果包含用于地图显示的 GPS 坐标。
- 购物结果会显示可比较的产品价格。
- 当可用时，知识图谱会提供相关实体的详细信息。
- 免费 tier 的月搜索次数限制为 100 次，请在 [serpapi.com/dashboard](https://serpapi.com/dashboard) 查看您的使用计划。