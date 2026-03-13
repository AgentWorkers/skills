---
name: clicky-analytics
description: 通过 Clicky（clicky.com）的 REST API 获取网站分析数据。当用户询问关于网站流量、访问者数量、页面浏览量、热门页面、跳出率、搜索排名、流量来源、国家等信息时，可以使用此功能。此外，该 API 还可用于生成定期分析报告或比较不同时间段的网站流量数据。
metadata: {"openclaw":{"emoji":"📊","primaryEnv":"CLICKY_SITEKEY","requires":{"bins":["curl"],"env":["CLICKY_SITE_ID","CLICKY_SITEKEY"]}}}
---
# Clicky Analytics

从 Clicky API 获取分析数据。支持通过环境变量配置多个网站。

## 设置

将网站凭据存储为环境变量。使用以下命名规范：`CLICKY_<名称>_SITE_ID` 和 `CLICKY_<名称>_SITEKEY`：

```bash
# In ~/.openclaw/.env or your shell profile
CLICKY_ENVELOPEBUDGET_SITE_ID=101427673
CLICKY_ENVELOPEBUDGET_SITEKEY=c287a01cc00f70cb
CLICKY_ZAPYETI_SITE_ID=99999999
CLICKY_ZAPYETI_SITEKEY=abc123def456
```

对于单个默认网站，使用以下命令：
```bash
CLICKY_SITE_ID=101427673
CLICKY_SITEKEY=c287a01cc00f70cb
```

## 使用方法

```bash
# Named site (reads CLICKY_<NAME>_SITE_ID and CLICKY_<NAME>_SITEKEY env vars)
scripts/clicky.sh envelopebudget visitors,actions-pageviews

# Default site (reads CLICKY_SITE_ID and CLICKY_SITEKEY env vars)
scripts/clicky.sh default visitors,actions-pageviews

# With options
scripts/clicky.sh envelopebudget pages --date last-7-days --limit 20
scripts/clicky.sh envelopebudget visitors --date 2026-03-01,2026-03-13 --daily
```

### 参数选项
- `--date DATE` — 当前日期、昨天、过去7天、过去30天、YYYY-MM-DD，或日期范围 YYYY-MM-DD,YYYY-MM-DD
- `--limit N` — 最大结果数量（默认为50，最大值为1000）
- `--daily` — 按天划分结果
- `--page N` — 对结果进行分页显示

### 在一个请求中组合数据类型
使用逗号分隔：`visitors,visitors-unique,actions-pageviews,bounce-rate,time-average-pretty`

## 常见报告类型

| 报告类型 | 收集的数据类型 |
|--------|-------|
| 概览 | `visitors,visitors-unique,actions-pageviews,bounce-rate,time-average-pretty` |
| 内容分析 | `pages,pages-entrance,pages-exit` |
| 流量分析 | `traffic-sources,links-domains,searches,countries` |
| SEO 分析 | `searches,searches-rankings,searches-keywords` |

## API 参考

请参阅 `references/api-types.md` 以获取所有可用的数据类型、日期格式和请求限制信息。