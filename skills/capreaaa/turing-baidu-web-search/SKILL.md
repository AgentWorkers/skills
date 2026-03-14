---
name: turing-baidu-web-search
version: "1.0.0"
description: "通过 Turing Baidu 代理来搜索网页。当用户需要用中文搜索网页、从中文来源获取实时信息、研究中国的时事新闻，或需要使用百度搜索获取最新数据时，请使用该代理。请通过 bash 命令运行捆绑好的脚本——切勿手动构造 HTTP 请求。"
homepage: https://docs.turing.cn
metadata:
  openclaw:
    emoji: "🔍"
    requires:
      credentials: "TURING_API_KEY, TURING_CLIENT, TURING_ENVIRONMENT"
---
# 百度网页搜索

通过Turing Baidu代理API进行网页搜索。

## 使用方法

```bash
python3 ~/.openclaw/skills/turing-baidu-web-search/scripts.py '<JSON>'
```

## 请求参数

| 参数 | 类型 | 是否必填 | 默认值 | 描述 |
| --- | --- | --- | --- |
| `q` | `str` | 是 | 搜索查询 |
| `count` | `int` | 否 | 返回的结果数量（默认值：10） |
| `search_recency_filter` | `str` | 否 | 新近性过滤：`week`（7天）、`month`（30天）、`semiyear`（180天）、`year`（365天） |

## 响应字段

| 字段 | 类型 | 描述 |
| --- | --- | --- |
| `results[].id` | `int` | 结果的排名 |
| `results[].title` | `str` | 页面标题 |
| `results[].url` | `str` | 页面URL |
| `results[].website` | `str` | 来源网站名称 |
| `results[].content` | `str` | 内容片段 |
| `results[].date` | `str` | 发布日期 |
| `results[].type` | `str` | 内容类型（例如：`web`、`news`） |

## 示例

```bash
# Basic search
python3 ~/.openclaw/skills/turing-baidu-web-search/scripts.py '{"q": "今日A股行情"}'

# Limit results
python3 ~/.openclaw/skills/turing-baidu-web-search/scripts.py '{"q": "今日A股行情", "count": 5}'

# Recent results only (last 7 days)
python3 ~/.openclaw/skills/turing-baidu-web-search/scripts.py '{"q": "中证A50最新消息", "count": 10, "search_recency_filter": "week"}'
```

## 配置

在`openclaw.json`文件中的`skills.entries.turing-skills.env`部分进行配置：

| 变量 | 是否必填 | 描述 |
| --- | --- | --- |
| `TURING_API_KEY` | 是 | Bearer令牌（格式为`sk-...`） |
| `TURING_CLIENT` | 是 | 客户端标识符 |
| `TURING_ENVIRONMENT` | 是 | 环境名称 |
| `TURING_API_BASE` | 否 | API基础URL（默认值：`https://live-turing.cn.llm.tcljd.com`） |