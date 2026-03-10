---
name: bitrefill-website
description: "浏览并探索 Bitrefill（bitrefill.com）：您可以在这里找到礼品卡、手机充值服务以及 eSIM 卡；可以通过品牌、类别或国家进行搜索；比较不同产品和面额；了解产品的价格、可用性以及每种产品的使用方式。当用户提到 Bitrefill、礼品卡、手机充值或旅行相关的 eSIM 服务时，可以参考此信息。"
compatibility: "No credentials or API access required. Instruction-only skill for navigating bitrefill.com."
metadata:
  author: bitrefill
  version: "1.2.1"
  homepage: "https://www.bitrefill.com"
---
# Bitrefill网站使用技巧

当用户想要**探索**Bitrefill（bitrefill.com）时，可以使用此技巧：了解产品信息、进行搜索、比较产品，或了解价格和库存情况。Bitrefill销售数字商品（礼品卡、手机充值卡、eSIM卡），并提供比特币/Lightning支付服务。所有产品均以数字形式交付。

> **程序化访问与购买：**如需通过API进行搜索、购买产品、管理订单或执行任何自动化流程，请使用**bitrefill-cli**技巧。此技巧仅用于浏览——它帮助用户导航和了解网站内容。

## 何时使用此技巧

在以下情况下激活此技巧：
- 用户提到**Bitrefill**或bitrefill.com；
- 用户询问如何在Bitrefill上**搜索**、**查找**或**比较**产品；
- 用户需要了解**产品信息**（如价格、库存情况、国家限制、面额等）；
- 用户想了解Bitrefill提供的服务或某种产品类型的工作原理。

当用户希望：
- **购买**产品、使用加密货币进行支付；
- 以程序化方式使用Bitrefill的**API**或**MCP端点**；
- 管理**订单**或**发票**；
- 执行任何**自动化**或**基于CLI**的流程时，请引导用户使用**bitrefill-cli**技巧。

如果用户的需求不够明确（例如：“我需要一份礼物”），请询问用户需要哪种类型的产品以及购买对象（国家/偏好）。

## 快速判断：用户想要做什么？

```
User intent?
├─ Learn what Bitrefill offers / product types     → See "Product types at a glance" below; details in references/product-types.md
├─ Search or browse for a product                 → references/search-and-browse.md
└─ Get detailed info (price, country, how it works)→ references/search-and-browse.md
```

## 产品类型概览

| 产品类型 | 产品说明 | 主要URL | 需要时加载详细信息 |
|--------------|------------|----------|---------------------------|
| **礼品卡** | 数字礼品卡（可用于购物、流媒体、游戏、餐饮、旅行等） | bitrefill.com/{country}/{lang}/gift-cards/ | references/product-types.md, references/supported-categories.md |
| **手机充值卡** | 预付费电话话费/数据（支持200多个国家） | bitrefill.com/refill/ | references/product-types.md |
| **eSIM卡** | 旅行数据套餐（仅数据功能，支持二维码激活，覆盖190多个国家） | bitrefill.com/esim/all-destinations 或 bitrefill.com/{country}/{lang}/esims/ | references/product-types.md |
| **比特币 / Lightning** | 提供比特币交易渠道、流动性服务及支付工具 | bitrefill.com（相关页面） | references/product-types.md（简要说明） |
| **账户与认证** | 注册、登录、密码重置、推荐计划 | bitrefill.com/signup, /login | references/account-and-auth.md |

**重要提示：**许多产品具有**国家或地区限制**。在推荐产品或流程之前，请务必确认或推断用户的所在国家（对于充值卡，还需确认运营商）。  

- **URL中的国家信息：**URL的第一部分表示国家，第二部分表示语言（例如：`/us/en/gift-cards/`、`/mx/es/gift-cards/`）。国家部分会过滤显示在该国家可使用的礼品卡。如需查看特定国家的商品列表，请在URL中指定相应国家。  
- **地域限制：**产品的购买权限由用户的IP地址决定，而非URL中的国家信息。如果某个产品无法购买，可能是由于用户的IP地址或地理位置导致的，而非URL设置的问题。  

## 任务流程（概述）

### 浏览或搜索

1. 确定**产品类型**（礼品卡/充值卡/eSIM卡）和**国家**（如果已知充值卡的具体运营商信息）。
2. 为了快速查找礼品卡，直接将用户引导至搜索页面：`https://www.bitrefill.com/{country}/{lang}/gift-cards/?q={query}`（例如：`https://www.bitrefill.com/us/en/gift-cards/?q=amazon`）——无需从首页开始导航。
3. 如需按目的地查找eSIM卡，将用户引导至`bitrefill.com/esim/all-destinations`页面，浏览190多个国家/地区的商品。
4. 其他情况下，直接引导用户至相应页面或使用网站搜索功能；可根据类别、品牌或金额进行筛选。
5. 有关详细信息（类别、品牌、面额等），请参考**references/search-and-browse.md**和**references/supported-categories.md**。
6. **路径与类别的关系：**要列出某个类别（或其子类别），请使用`/{country}/{lang}/gift-cards/{category-slug}/`。
7. **子类别：**某些类别下包含子类别（例如：旅行 → 航班、火车、巴士）。路径模式相同；子类别名称用于区分不同子类别。
8. **列表筛选与排序：**礼品卡列表支持以下查询参数：`filters`（`redemptionMethod`：在线/店内兑换、`minRating`：评分2–5分、`minRewards`：返现比例1–10%）；`sort`：`s=2`（按字母顺序）、`s=3`（按添加时间排序）、`s=4`（按返现比例排序）；默认排序方式为按受欢迎程度排序。详情请参阅references/search-and-browse.md。  

## 提示与常见误区

- **优先考虑国家信息：**使用URL中的国家信息来显示该国家可使用的商品。地区限制的产品（例如美国版与英国版的Amazon礼品卡）是导致错误的主要原因——请确保所显示的商品符合用户的实际需求。
- **地域限制与URL的关系：**产品是否可购买由用户的IP地址决定，而非URL中的国家信息。URL仅用于控制显示的商品列表。
- **退款政策：**数字商品一旦交付通常不可退款；请在购买前明确相关规则。

## 限制事项

- **禁止抓取数据：**Cloudflare会阻止对www.bitrefill.com的自动化访问。请勿使用firecrawl或直接抓取数据，否则会收到403错误。
- **禁止API访问：**此技巧不使用Bitrefill的API或MCP端点。如需进行程序化操作（搜索、购买、订单管理），请使用**bitrefill-cli**技巧。

## 参考资料

仅在代理需要更多详细信息时加载相关文档：

| 参考资料 | 使用场景 |
|-----------|----------|
| [product-types](references/product-types.md) | 介绍礼品卡、充值卡和eSIM卡的区别及其在网站上的使用方式 |
| [search-and-browse](references/search-and-browse.md) | 用户需要查找或筛选产品时使用 |
| [supported-categories](references/supported-categories.md) | 列出产品类别或热门品牌信息（如礼品卡等） |