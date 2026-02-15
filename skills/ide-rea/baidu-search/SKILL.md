---
name: baidu-search
description: 使用百度AI搜索引擎（BDSE）在互联网上搜索信息。该搜索引擎适用于获取实时数据、查阅文档或进行相关研究。
metadata: { "openclaw": { "emoji": "🔍︎",  "requires": { "bins": ["python3"], "env":["BAIDU_API_KEY"]},"primaryEnv":"BAIDU_API_KEY" } }
---

# 百度搜索

通过百度AI搜索API在网页上进行搜索。

## 使用方法

```bash
python3 skills/baidu-search/scripts/search.py '<JSON>'
```

## 请求参数

| 参数 | 类型 | 是否必填 | 默认值 | 描述 |
|-------|------|----------|---------|-------------|
| query | str | 是 | - | 搜索查询内容 |
| edition | str | 否 | standard | `standard`（完整版）或 `lite`（简化版） |
| resource_type_filter | list[obj] | 否 | web:20, others:0 | 资源类型：网页（最多50个）、视频（最多10个）、图片（最多30个）、其他（最多5个） |
| search_filter | obj | 否 | - | 高级过滤条件（见下文） |
| block_websites | list[str] | 否 | - | 需要屏蔽的网站列表，例如 ["tieba.baidu.com"] |
| search_recency_filter | str | 否 | - | 时间过滤条件：`week`（周）、`month`（月）、`semiyear`（半年）、`year`（年） |
| safe_search | bool | 否 | false | 是否启用严格的内容过滤 |

## SearchFilter（高级过滤条件）

| 参数 | 类型 | 描述 |
|-------|------|-------------|
| match.site | list[str] | 将搜索范围限制在特定网站内，例如 ["baike.baidu.com"] |
| range.pageTime | obj | `page_time` 字段的日期范围（见下文） |

### 日期范围格式

固定日期：`YYYY-MM-DD`
相对时间（从当前日期起）：`now-1w/d`（过去1周）、`now-1M/d`（过去1个月）、`now-1y/d`（过去1年）

| 运算符 | 含义 |
|----------|---------|
| gte | 大于或等于（开始时间） |
| lte | 小于或等于（结束时间） |

## 示例

```bash
# Basic search
python3 skills/baidu-search/scripts/search.py '{"query":"人工智能"}'

# Filter by time and site
python3 skills/baidu-search/scripts/search.py '{
  "query":"最新新闻",
  "search_recency_filter":"week",
  "search_filter":{"match":{"site":["news.baidu.com"]}}
}'

# Resource type filter
python3 skills/baidu-search/scripts/search.py '{
  "query":"旅游景点",
  "resource_type_filter":[{"type":"web","top_k":20},{"type":"video","top_k":5}]
}'
```

## 当前状态

该功能已完全实现。