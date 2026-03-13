---
name: card-news
description: 以下是过去3个月内关于美国主要信用卡品牌的最新资讯汇总，包括信用卡的直接变更、发卡机构的更新以及相关新闻报道。涵盖的信用卡品牌包括：American Express（美国运通）、Chase（大通银行）、Capital One（资本一号银行）、Citi（花旗银行）、Bank of America（美国银行）、Discover（发现银行）和Wells Fargo（富国银行）。
metadata:
  openclaw:
    requires:
      env:
        - BRAVE_API_KEY
      bins:
        - curl
    primaryEnv: BRAVE_API_KEY
---
# 卡片新闻

以简洁的格式返回某一张特定卡片在过去3个月内的新闻内容。

## 使用场景

当用户询问信用卡的最新变更、新闻或更新时使用。触发短语包括：“card-news”、“any changes”、“recent news”、“what’s new with”、“updates for”。

## 工作流程

1. **确定卡片类型** — 将输入信息标准化并匹配到具体的卡片类型。如果信息不明确，则返回一个编号列表并停止处理。
2. **搜索** — 使用Brave Search API进行搜索，并设置新鲜度过滤器以获取最新结果。
3. **筛选** — 应用3个月的回顾时间窗口和筛选规则。
4. **整理** — 汇总新闻内容。
5. **确认信息的准确性** — 标记出不确定或相互矛盾的信息。

## 第一步：确定卡片类型

### 常见缩写

| 输入 | 对应的卡片类型 |
|---|---|
| CSP | Chase Sapphire Preferred |
| CSR | Chase Sapphire Reserve |
| CFU | Chase Freedom Unlimited |
| CFF | Chase Freedom Flex |
| Amex Gold | American Express Gold Card |
| Amex Plat | American Express Platinum Card |
| Venture X | Capital One Venture X Rewards Credit Card |
| Savor | Capital One SavorOne / Savor（信息不明确时需进一步确认） |
| Double Cash | Citi Double Cash Card |
| Custom Cash | Citi Custom Cash Card |

### 支持的发卡机构

American Express、Bank of America、Capital One、Chase、Citi、Discover、Wells Fargo。

## 第二步：搜索

使用Brave Search API进行搜索，并设置`freshness=pm`参数以限制结果为过去一个月内的内容。请将`CURRENT_YEAR`替换为实际的当前年份。

### 信息来源规则

- **优先考虑发卡机构的官方新闻来源**：查看发卡机构的博客和新闻稿页面。
- **最多使用5个次要信息来源**：Doctor of Credit（推荐）、The Points Guy（推荐）、One Mile at a Time（推荐）、NerdWallet（推荐）、Bankrate（推荐）、Upgraded Points。
- **禁止使用的来源**：Reddit、Facebook、Instagram、TikTok、X、YouTube、推荐链接以及用户论坛。

## 新闻时效性规则

- 仅使用3个月的回顾时间窗口。
- **包含的内容**：直接与卡片相关的变更、对卡片有重大影响的发卡机构更新、以及能够改变人们对卡片认知的重大媒体报道。
- **排除的内容**：泛泛而谈的发卡机构讨论、以及不涉及近期变更的“最佳卡片”类文章。

## 必需的输出部分

### `## 📅 新闻时间范围`
3个月回顾时间窗口的开始和结束日期。

### `## 📰 最新更新**
按日期排序的变更列表，每条更新包含日期和简短摘要。

### `## 📝 总结**
用2-3句话概括发生了哪些变化以及哪些内容保持不变。

### `## 📋 信息准确性说明`
标记出任何不确定、未经确认或相互矛盾的信息。

## 输出规则

- 每个部分标题使用一个表情符号，并使用编号列表来展示更新内容。
- 保持内容简洁明了，避免冗长的描述。
- 如果卡片类型已经确定，则省略“卡片类型”部分。
- 输出中不包含内联链接、来源信息或YAML格式的代码块。

## 信息准确性定义

- **已确认**：有发卡机构的官方声明或多个权威来源支持的信息。
- **未经确认**：虽然看似合理但尚未得到完全证实。
- **相互矛盾**：不同来源对关键事实存在分歧。