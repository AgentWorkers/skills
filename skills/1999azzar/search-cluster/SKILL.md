---
name: search-cluster
description: 这是一个统一的搜索聚合器，可以同时查询 Google、Wikipedia、Reddit、NewsAPI 以及 RSS 源。该工具支持 Redis 缓存功能（可选），并能够返回结构化的 JSON 数据。此外，它还支持并行查询。
metadata: {"openclaw":{"requires":{"bins":["python3"],"env":["GOOGLE_CSE_KEY","GOOGLE_CSE_ID","NEWSAPI_KEY"]},"install":[{"id":"pip-deps","kind":"exec","command":"pip install redis"}]}}
---
# 搜索集群

这是一个用于多源信息收集的统一搜索系统。

## 先决条件
- **系统要求**：必须安装 `python3`。
- **Google Search**：需要 `GOOGLE_CSE_KEY` 和 `GOOGLE_CSE_ID`。
- **NewsAPI**：需要 `NEWSAPI_KEY`。
- **缓存（可选）**：需要一个运行中的 Redis 实例（默认使用 `localhost:6379`）。

## 设置
1. 在环境变量或本地 `.env` 文件中定义 API 密钥。
2. （可选）安装 Redis 客户端：`pip install redis`。

## 核心工作流程

### 1. 单源搜索
针对特定来源查询目标结果。
- **使用方法**：`python3 $WORKSPACE/skills/search-cluster/scripts/search-cluster.py <source> "<query>"`
- **支持的来源**：`google`、`wiki`、`reddit`、`newsapi`。

### 2. 聚合搜索
并行查询所有支持的来源并汇总结果。
- **使用方法**：`python3 $WORKSPACE/skills/search-cluster/scripts/search-cluster.py all "<query>"`

### 3. RSS/Feed 获取
检索并解析标准的 RSS 或 Atom 源。
- **使用方法**：`python3 $WORKSPACE/skills/search-cluster/scripts/search-cluster.py rss "<url>"`

## 可靠性与安全性
- **安全网络**：对所有 API 和 Feed 请求强制执行严格的 SSL/TLS 验证，不允许使用未经验证的替代方案。
- **命名空间隔离**：缓存键前缀为 `search:` 以避免冲突。
- **本地偏好设置**：Redis 连接默认使用 `localhost`；用户需要明确设置 `REDIS_HOST` 以连接远程实例。
- **用户代理**：使用标准化的 `SearchClusterBot` 代理来遵守网站政策。

## 参考资料
- **API 设置**：请参阅 [references/search-apis.md](references/search-apis.md)。