---
name: keywords-everywhere
description: 通过 Keywords Everywhere API 进行 SEO 关键词研究及竞争对手分析。当您需要获取关键词的搜索量、点击成本（CPC）、竞争数据、查找相关关键词（PASF）、分析某个域名/URL 的排名情况，或检索反向链接数据时，可以使用该工具。
---

# Keywords Everywhere API

这是一个用于SEO关键词研究、竞争对手分析以及反向链接指标的命令行工具（CLI）。

## 设置

需要API密钥。请在`clawdbot config`文件中的`skills.entries_keywords-everywhere.apiKey`字段进行配置，或通过环境变量设置：
```bash
export KEYWORDS_EVERYWHERE_API_KEY="your_api_key"
```

## 使用方法

```bash
python3 scripts/kwe.py <command> [arguments] [options]
```

或者，您可以为其设置一个别名：
```bash
alias kwe="python3 /path/to/skills/keywords-everywhere/scripts/kwe.py"
```

## 命令

### 关键词研究

- **获取关键词数据**（搜索量、点击成本、竞争程度、趋势）：
```bash
kwe keywords "seo tools" "keyword research" --country us --currency usd
```

- **相关关键词**（发现相关术语）：
```bash
kwe related "content marketing" --num 20
```

- **用户也搜索的内容**：
```bash
kwe pasf "best crm software" --num 15
```

### 域名/URL分析

- **某个域名在搜索结果中的排名及预估流量**：
```bash
kwe domain-keywords example.com --country us --num 100
```

- **特定URL在搜索结果中的排名**：
```bash
kwe url-keywords "https://example.com/blog/post" --num 50
```

### 反向链接分析

- **域名的反向链接**：
```bash
kwe domain-backlinks example.com --num 50
```

- **每个引用域名的唯一反向链接**：
```bash
kwe unique-domain-backlinks example.com --num 30
```

- **特定URL的反向链接**：
```bash
kwe page-backlinks "https://example.com/page" --num 20
```

- **每个页面的唯一反向链接**：
```bash
kwe unique-page-backlinks "https://example.com/page"
```

### 账户信息

- **查看剩余信用额度**：
```bash
kwe credits
```

- **支持的国家列表**：
```bash
kwe countries
```

- **支持的货币列表**：
```bash
kwe currencies
```

## 选项

| 选项          | 描述                        | 默认值       |
|----------------|----------------------------------|------------|
| `--country`     | 国家代码（空表示全球；`us`、`uk`、`in`等）        | global       |
| `--currency`     | 货币代码（`usd`、`gbp`、`inr`等）           | usd         |
| `--num`       | 结果数量（银级计划最多2000条）                | 10          |
| `--output`     | 输出格式：`table`、`json`、`csv`                 | table       |

## 输出数据

### 关键词数据（`keywords`命令）

- `vol`：每月搜索量
- `cpc`：每次点击的成本（广告商出价）
- `competition`：竞争程度（0-1）
- `trend`：过去12个月的搜索趋势数据

### 域名/URL关键词数据

- `keyword`：排名关键词
- `estimated_monthly_traffic`：预估的每月自然流量
- `serp_position`：当前在搜索引擎结果页（SERP）中的排名

### 反向链接数据

- `domain_source`：引用域名
- `anchor_text`：链接的锚文本
- `url_source` / `url_target`：来源/目标URL

## 信用额度使用规则

1个信用额度对应1个关键词。银级计划：每年400,000个信用额度，每个网站最多可查询2,000个关键词/反向链接。

## 示例

- **竞争对手关键词研究**：
```bash
# What keywords does competitor rank for?
kwe domain-keywords competitor.com --num 200 --output json > keywords.json

# Get detailed metrics for specific keywords
kwe keywords "keyword1" "keyword2" "keyword3" --country us
```

- **内容缺口分析**：
```bash
# Find keywords competitor ranks for
kwe domain-keywords competitor.com --num 500

# Get related keywords for your topic
kwe related "your topic" --num 100
kwe pasf "your topic" --num 100
```

- **反向链接挖掘**：
```bash
# Find who links to competitor
kwe unique-domain-backlinks competitor.com --num 100 --output json
```