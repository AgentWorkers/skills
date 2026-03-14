---
name: turing-tavily-web-search
version: "1.0.0"
description: "通过 Turing Tavily 代理来搜索网页。当用户请求搜索网页、查询实时信息、研究时事事件或需要训练数据之外的最新数据时，可以使用该代理。请通过 bash 运行捆绑好的脚本——切勿手动构建 HTTP 请求。"
homepage: https://docs.turing.cn
metadata:
  openclaw:
    emoji: "🔍"
    requires:
      credentials: "TURING_API_KEY, TURING_CLIENT, TURING_ENVIRONMENT"
---
# Tavily 网页搜索

通过 Turing Tavily 代理 API 进行网页搜索。

## 使用方法

```bash
python3 ~/.openclaw/skills/turing-tavily-web-search/scripts.py '<JSON>'
```

## 请求参数

| 参数 | 类型 | 是否必填 | 默认值 | 描述 |
|---|---|---|---|
| `query` | `str` 或 `list[str]` | 是 | 搜索查询；或用于批量搜索的查询列表 |
| `max_results` | `int` | 否 | 每次查询的最大结果数量（1–20） |
| `max_tokens_per_page` | `int` | 否 | 每页提取的最大字符数（1024） |
| `search_domain_filter` | `list[str]` | 否 | 将结果限制在特定域名内（最多 20 个域名） |

## 响应字段

| 字段 | 类型 | 描述 |
|---|---|---|
| `answer` | `str` | 由 AI 生成的摘要（如可用） |
| `results[].title` | `str` | 页面标题 |
| `results[].url` | `str` | 页面 URL |
| `results[].content` | `str` | 页面内容片段 |
| `results[].publishedDate` | `str` | 发布日期（如可用） |

## 示例

```bash
# Basic search
python3 ~/.openclaw/skills/turing-tavily-web-search/scripts.py '{"query": "latest AI news"}'

# Limit results
python3 ~/.openclaw/skills/turing-tavily-web-search/scripts.py '{"query": "latest AI news", "max_results": 5}'

# Domain filter
python3 ~/.openclaw/skills/turing-tavily-web-search/scripts.py '{"query": "transformer architecture", "search_domain_filter": ["arxiv.org", "github.com"]}'
```

## 配置

在 `openclaw.json` 文件的 `skills.entries.turing-skills.env` 下进行配置：

| 变量 | 是否必填 | 描述 |
|---|---|---|
| `TURING_API_KEY` | 是 | 承载令牌（格式为 `sk-...`） |
| `TURING_CLIENT` | 是 | 客户端标识符 |
| `TURING_ENVIRONMENT` | 是 | 环境名称 |
| `TURING_API_BASE` | 否 | API 基础 URL（默认：`https://live-turing.cn.llm.tcljd.com`） |