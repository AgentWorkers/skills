---
name: baidu-search
description: 使用百度AI搜索引擎（BDSE）在互联网上搜索信息。该搜索引擎适用于获取实时数据、查阅文档或进行相关研究。
metadata: { "openclaw": { "emoji": "🔍︎",  "requires": { "bins": ["python3"], "env":["BAIDU_API_KEY"]},"primaryEnv":"BAIDU_API_KEY" } }
---
# 百度搜索

通过百度AI搜索API在网络上进行搜索。

## 使用方法

```bash
python3 skills/baidu-search/scripts/search.py '<JSON>'
```

## 请求参数

| 参数 | 类型 | 是否必填 | 默认值 | 描述 |
|-------|------|----------|---------|-------------|
| query | str | 是 | - | 搜索查询内容 |
| count | int | 否 | 10 | 返回的结果数量，范围为1-50 |
| freshness | str | 否 | Null | 时间范围，有两种格式：第一种格式为“YYYY-MM-DD to YYYY-MM-DD”；第二种格式包含“pd”、“pw”、“pm”和“py”，分别表示过去24小时、过去7天、过去31天和过去365天 |

## 示例

```bash
# Basic search
python3 scripts/search.py '{"query":"人工智能"}'

# Freshness first format "YYYY-MM-DDtoYYYY-MM-DD" example
python3 scripts/search.py '{
  "query":"最新新闻",
  "freshness":"2025-09-01to2025-09-08"
}'

# Freshness second format pd、pw、pm、py example
python3 scripts/search.py '{
  "query":"最新新闻",
  "freshness":"pd"
}'

# set count, the number of results to return
python3 scripts/search.py '{
  "query":"旅游景点",
  "count": 20,
}'
```

## 当前状态

功能完备。