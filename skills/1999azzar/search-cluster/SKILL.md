---
name: search-cluster
description: 这是一个聚合搜索工具，它整合了 Google CSE、GNews RSS、Wikipedia、Reddit 以及网页抓取（scraping）的数据源来提供统一的搜索结果。
---
# Search Cluster (工业标准版 v3.1)

这是一个专为高可用性和安全性设计的多提供者搜索聚合器。

## 安装
该工具需要一个专用的虚拟环境来运行：
1. 创建一个虚拟环境：`python3 -m venv venv/scrapling`
2. 安装 `scrapling` 模块：`venv/scrapling/bin/pip install scrapling`
3. 将虚拟环境中的 Python 可执行文件路径设置为 `SCRAPLING_PYTHON_PATH`。

## 安全性措施：
- **子进程隔离**：查询参数作为参数传递给 `stealth-fetch.py` 函数。
- **严格的 TLS 协议**：所有提供者都必须使用 SSL 进行身份验证。
- **数据清洗**：内置了数据清洗功能（路径处理机制为中性，即不依赖特定路径格式）。

## 需求与环境配置
请在您的环境或安全存储系统中配置以下变量：

| 变量 | 需求 | 说明 |
|---|---|---|
| GOOGLE_API_KEY | 可选 | 用于 Google 定制搜索的 API 密钥。 |
| GOOGLE_CSE_ID | 可选 | 用于 Google CSE 的搜索引擎 ID。 |
| SCRAPLING_PYTHON_PATH | 可选 | 包含 `scrapling` 模块的虚拟环境中的 Python 可执行文件路径。 |
| REDIS_HOST | 可选 | 用于缓存结果的 Redis 服务器地址。 |
| REDIS_PORT | 可选 | Redis 服务器的端口（默认值：6379）。 |
| SEARCH_USER_AGENT | 可选 | 自定义的用户代理字符串。 |

## 支持的提供者：
- **google**：官方的 Google 定制搜索服务。
- **wiki**：Wikipedia 的 OpenSearch API。
- **reddit**：Reddit 的 JSON 搜索 API。
- **gnews**：Google News 的 RSS 摘要聚合器。
- **scrapling**：通过 DuckDuckGo 进行的无头数据抓取服务。

## 包含的脚本：
- `scripts/search-cluster.py`：程序的入口脚本。
- `scripts/stealth-fetch.py`：用于数据抓取的脚本（对于支持数据抓取的提供者来说是必需的）。

## 工作流程：
1. 运行 `scripts/search-cluster.py`，传入查询参数 `<query>`。
2. 输出结果为结构化的 JSON 格式，包含来源、标题、链接以及经过清洗后的内容片段。