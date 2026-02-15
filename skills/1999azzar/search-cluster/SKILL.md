---
name: search-cluster
description: 这是一个统一的搜索工具，可以同时搜索 Google、Wikipedia、Reddit 以及 RSS 源中的内容，并利用 Redis 进行缓存。当用户输入诸如“搜索 X”、“Y 是谁”或“Z 的最新消息”等查询时，该工具能够提供相应的结果。
---

# 搜索集群

## 概述
这是一个统一的搜索聚合器，能够并行查询多个数据源（Google、Wikipedia、Reddit、RSS、NewsAPI）。它将搜索结果缓存到 Redis 中，以优化性能并减少对 API 的调用次数。

## 设置
1. 将 `.env.example` 文件复制到 `.env` 文件中。
2. 设置 `GOOGLE_CSE_KEY`（或 `GOOGLE_API_KEY`）和 `GOOGLE_CSE_ID`。
3. 确保 Redis 可以被访问（主机/端口或 Docker 容器）。

## 配置
此功能需要在 `.env` 文件中配置以下环境变量：

| 变量 | 描述 | 是否必需？ |
| :--- | :--- | :--- |
| `GOOGLE_CSE_KEY` | Google 自定义搜索 JSON API 密钥 | 是（针对 Google） |
| `GOOGLE_CSE_ID` | Google 自定义搜索引擎 ID (cx) | 是（针对 Google） |
| `NEWSAPI_KEY` | NewsAPI.org API 密钥（免费 tier：每天 100 次请求） | 是（针对 NewsAPI） |
| `REDIS_HOST` | Redis 主机名（默认：localhost） | 否 |
| `REDIS_PORT` | Redis 端口（默认：6379） | 否 |
| `REDDIT_USER_AGENT` | Reddit API 的自定义 User-Agent | 否 |

## 使用方法
- **角色**：信息收集工具。
- **触发语句**：例如：“搜索...”、“查找关于...的信息”、“在 Reddit 上查找...”。
- **输出**：结果的 JSON 列表（包含标题、链接、摘要和来源）。

### 命令
#### `scripts/search-cluster.py`
主要的聚合器脚本。

**语法：**
```bash
python3 scripts/search-cluster.py <SOURCE> <QUERY>
```

**可查询的数据源**：`google`、`wiki`、`reddit`、`rss`、`all`。

**示例**：
```bash
# Search Google
python3 scripts/search-cluster.py google "query"

# Search NewsAPI (Latest News)
python3 scripts/search-cluster.py newsapi "artificial intelligence"

# Search All Sources (Parallel)
python3 scripts/search-cluster.py all "query"

# Fetch RSS Feed
python3 scripts/search-cluster.py rss "https://rss-url.com/feed"
```

## 功能特点
1. **多引擎集群**：可以并行查询 Google、Wikipedia 和 Reddit（使用 `all` 模式）。
2. **强大的缓存机制**：将搜索结果保存到 Redis 中（缓存有效期为 24 小时），以节省 API 带宽。
3. **稳定的解析能力**：能够正确解析 RSS 数据，并优雅地处理 API 错误。

## 隐私与数据流
- **Redis**：仅用于缓存搜索结果（缓存有效期为 24 小时），以减少 API 调用次数和延迟。可以连接到本地实例或 Docker 容器。不会将数据发送到外部 Redis 服务器。
- **API 调用**：
  - Google：直接发送到 `googleapis.com`。
  - Reddit：发送到 `reddit.com`。
  - Wikipedia：发送到 `wikipedia.org`。
  - RSS：直接从源 URL 获取。
- **日志记录**：不进行外部日志记录或跟踪。

## 参考资料
- [搜索 API 与缓存](references/search-apis.md)