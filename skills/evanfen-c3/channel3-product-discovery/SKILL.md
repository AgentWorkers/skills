---
name: product-discovery
description: >
  当您需要真实的产品数据来回答用户的问题时（例如：查找产品、比较价格、推荐商品或检查零售商的库存情况），请使用这项技能。该技能为您提供了一个搜索脚本，该脚本可以查询包含数百万产品的目录，并返回结构化的数据结果。
  适用场景包括：
  - “帮我找到X产品”；
  - “Y产品哪个最好？”；
  - “比较Z产品的优劣”；
  - “价格在N美元以下的最佳X产品”；
  - 产品推荐；
  - 价格查询；
  - “这个商品划算吗？”；
  - “在哪里可以购买X产品”；
  - 产品对比；
  - 以及任何需要通过真实产品目录数据来回答用户问题的场景。
---
# 产品发现

您可以使用一个产品搜索脚本，该脚本能够查询来自数千家零售商的数百万种产品信息。每当您需要真实的产品数据来回答用户的问题时，都可以使用这个脚本。

## 先决条件

- **API密钥：** 此技能需要一个名为 `CHANNEL3_API_KEY` 的环境变量。您可以在 [trychannel3.com](https://trychannel3.com) 获取免费的 API 密钥。
- **依赖软件：** 必须安装 `curl` 和 `jq`。

## 搜索脚本

**位置：** `product-discovery/scripts/search.sh`（相对于技能根目录）

通过 shell 运行该脚本。脚本需要 `curl` 和 `jq` 的支持。

### 使用方法

```
search.sh [OPTIONS] "query text"
```

### 参数选项

| 参数 | 说明 | 示例 |
|------|-------------|---------|
| `-n 数量` | 显示的结果数量（默认值：5，最大值：30） | `-n 10` |
| `-p 最高价格` | 产品的最高价格（美元） | `-p 100` |
| `--最低价格` | 产品的最低价格（美元） | `--最低价格 50` |
| `-g 性别` | 产品性别筛选（男/女/中性） | `-g 男` |
| `-c 状态` | 产品状态（新/翻新/二手） | `-c 新` |
| `-a 年龄段` | 以逗号分隔的年龄段（新生儿/婴儿/幼儿/儿童/成人） | `-a "儿童,幼儿"` |
| `--库存状态` | 以逗号分隔的库存状态（有货/缺货/预购/待发货/限量供应/售罄/已停产） | `--库存状态 "有货"` |
| `-i 图片链接` | 通过图片进行搜索（基于视觉相似度） | `-i "https://example.com/photo.jpg"` |
| `-b 品牌ID` | 以逗号分隔的包含的品牌ID | `-b "brand_abc,brand_def"` |
| `-w 网站ID` | 以逗号分隔的包含的网站ID | `-w "website_abc"` |
| `--类别ID` | 以逗号分隔的包含的类别ID | `--类别 "cat_abc"` |
| `--排除品牌ID` | 以逗号分隔的排除的品牌ID | `--排除品牌 "brand_xyz"` |
| `--排除网站ID` | 以逗号分隔的排除的网站ID | `--排除网站 "website_xyz"` |
| `--排除类别ID` | 以逗号分隔的排除的类别ID | `--排除类别 "cat_xyz"` |
| `--仅使用关键词` | 使用精确匹配关键词，而非语义搜索 | `--仅使用关键词` |
| `--next 令牌` | 上次搜索的分页令牌 | `--next "tok_abc..."` |

当使用 `-i` 仅通过图片进行搜索时，查询参数是可选的。您也可以同时使用文本和图片进行搜索。

### 示例

```bash
# Basic text search
search.sh "wireless noise cancelling headphones"

# Price-filtered search
search.sh -p 100 -n 10 "running shoes"

# Price range search
search.sh --min-price 50 -p 200 "winter boots"

# Gendered search
search.sh -g female -p 200 "winter jacket"

# Condition filter
search.sh -c used "macbook pro"

# Kids products
search.sh -a kids -p 50 "sneakers"

# Only in-stock products
search.sh --availability "InStock" "yoga mat"

# Image-based visual similarity search
search.sh -i "https://example.com/dress.jpg"

# Combined text + image search
search.sh -i "https://example.com/jacket.jpg" "similar but in blue"

# Keyword-only (exact match, no semantic search)
search.sh --keyword-only "Nike Air Max 90"

# Paginate for more results
search.sh --next "tok_abc123..." "running shoes"
```

### 输出格式

脚本输出的是结构化的文本，而不是原始的 JSON 数据。每个产品信息包括其 ID、所属品牌以及所有商家的报价和购买链接：

```
Found 5 products (next_page: tok_abc123)

1. Nike Air Zoom Pegasus 41
   ID: prod_abc123
   Brands: Nike
   Offers:
     - nordstrom.com: $89.99 (InStock) https://buy.trychannel3.com/...
     - nike.com: $94.99 (InStock) https://buy.trychannel3.com/...

2. Adidas Ultraboost Light
   ID: prod_def456
   Brands: Adidas
   Offers:
     - adidas.com: $97.00 (InStock) https://buy.trychannel3.com/...
```

如果未找到任何产品，输出内容为：`未找到产品。`

如果 API 密钥缺失或无效，脚本会提示您如何获取密钥。

## 工作流程示例

### 查找产品

用户提问：“帮我找价格在 100 美元以下的跑鞋：”

1. 运行：`search.sh -p 100 "跑鞋"`
2. 以列表形式展示结果，包括产品名称、价格、商家名称和购买链接。

### 比较产品

用户提问：“比较 AirPods Pro 和 Sony WF-1000XM5：”

1. 分别运行两次搜索：`search.sh -n 3 "AirPods Pro"` 和 `search.sh -n 3 "Sony WF-1000XM5"`
2. 使用 Markdown 格式创建一个对比表，列出产品名称、价格、商家名称和库存状态。

### 在预算范围内选择最佳产品

用户提问：“价格在 800 美元以下的最佳笔记本电脑是什么？”

1. 运行：`search.sh -p 800 -n 10 "笔记本电脑"`
2. 查看结果后，根据产品详情推荐最佳选项，并说明原因。

### 基于图片的搜索

用户分享一张图片链接并请求：“帮我找类似这样的产品：”

1. 运行：`search.sh -i "IMAGE_URL"`
2. 显示与图片相似的产品列表，包括价格和购买链接。

### 获取更多结果

如果用户希望在初次搜索后获取更多结果：

1. 复制上次搜索得到的 `next_page` 令牌。
2. 运行：`search.sh --next "TOKEN" "原始查询"`
3. 显示额外的搜索结果。

## 如何向用户展示结果

- 将脚本的输出内容整理成简洁的回答形式，不要直接粘贴原始的脚本输出。
- 以列表或 Markdown 表格的形式展示产品信息，根据实际情况选择更合适的展示方式。
- 必须包含以下信息：产品名称、价格、商家名称和购买链接。
- 在进行产品对比时，使用包含“产品”、“价格”、“商家”和“链接”等列的 Markdown 表格。
- 如果同一产品有多个商家销售且价格不同，应突出显示最便宜的选项。
- 保持回答的简洁性——用户需要的是推荐建议，而不是大量数据。

## 关于此技能

此技能通过 [Channel3](https://trychannel3.com) 的产品目录 API (`api.trychannel3.com`) 进行查询。您提供的搜索查询和图片链接都会发送给这个第三方 API。产品的购买链接会指向 `buy.trychannel3.com`，该链接会重定向到带有联盟营销跟踪功能的商家网站。请避免在搜索查询中发送敏感或私密信息。

- **API 文档：** [docs.trychannel3.com](https://docs.trychannel3.com)
- **来源：** [github.com/channel3-ai/skills](https://github.com/channel3-ai/skills)
- **提供者：** Channel3 ([trychannel3.com](https://trychannel3.com))