---
name: clicky-analytics
description: 通过 Clicky（clicky.com）的 REST API 获取网站分析数据。当用户询问网站流量、访问者数量、页面浏览量、热门页面、跳出率、搜索排名、流量来源、国家等信息时，可以使用此 API。此外，该 API 还可用于生成定期分析报告或比较不同时间段的网站流量数据。
metadata: {"openclaw":{"emoji":"📊"}}
---
# Clicky Analytics

从 Clicky API 获取分析数据。支持多个网站。

## 网站注册表

网站信息存储在 `references/sites.json` 文件中。可以通过名称查询 `site_id` 和 `sitekey`。

## 使用方法

```bash
# By site name (looks up from sites.json)
scripts/clicky.sh envelopebudget visitors,actions-pageviews

# By explicit credentials
scripts/clicky.sh --id 101427673 --key c287a01cc00f70cb visitors,actions-pageviews

# With options
scripts/clicky.sh envelopebudget pages --date last-7-days --limit 20
scripts/clicky.sh envelopebudget visitors --date 2026-03-01,2026-03-13 --daily
```

### 参数选项
- `--date DATE` — 当前日期、昨天、过去7天、过去30天、YYYY-MM-DD 或日期范围 YYYY-MM-DD,YYYY-MM-DD
- `--limit N` — 最大结果数量（默认为50，最大值为1000）
- `--daily` — 按天划分结果
- `--page N` — 分页显示结果

### 在一个请求中组合多种数据类型
使用逗号分隔来批量获取数据：`visitors,visitors-unique,actions-pageviews,bounce-rate,time-average-pretty`

## 常见报告类型

| 报告名称 | 收集的数据类型 |
|--------|-------|
| 概览 | `visitors,visitors-unique,actions-pageviews,bounce-rate,time-average-pretty` |
| 内容 | `pages,pages-entrance,pages-exit` |
| 流量 | `traffic-sources,links-domains,searches,countries` |
| SEO | `searches,searches-rankings,searches-keywords` |

## 添加网站

编辑 `references/sites.json` 文件以添加新网站：
```json
{"name": "mysite", "site_id": "12345", "sitekey": "abc123def456", "domain": "mysite.com"}
```

## API 参考

请参阅 `references/api-types.md` 以获取所有可用的数据类型、日期格式和请求限制信息。