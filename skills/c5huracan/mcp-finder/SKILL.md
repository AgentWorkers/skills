---
name: mcp-finder
description: 为您的任务找到合适的MCP服务器。系统收录了4,500多台服务器，并根据社区的信任度对它们进行了排名。无需使用API密钥。
version: 0.2.0
author: c5huracan
homepage: https://github.com/c5huracan/meyhem
metadata:
  openclaw:
    requires:
      bins:
        - python3
---
# MCP Finder

MCP Finder 可帮助您为任何任务找到合适的 MCP（MCP）服务器。该工具索引了来自 MCP 生态系统的 4,500 多台服务器，并根据社区的信任度（GitHub 星级）和相关性对它们进行排序。只需用简单的语言描述您的需求，MCP Finder 便会为您推荐最适合的服务器。

无需 API 密钥，无需注册，也没有使用限制。

## 为什么选择 MCP Finder？

- **索引了 4,500 多台服务器**：这些服务器信息来自 `awesome-mcp-servers`，并补充了 GitHub 的元数据。
- **支持自然语言搜索**：您只需描述任务需求，系统便会返回相关结果。
- **基于信任度排序**：评分标准结合了 GitHub 星级和内容的相关性。
- **完全依赖标准 Python 库**：无需额外的依赖库。

## 快速入门

```bash
python3 finder.py "I need to query a Postgres database"
python3 finder.py "browser automation" -n 3
python3 finder.py "kubernetes monitoring"
python3 finder.py "manage emails"
```

## REST API

```bash
curl -X POST https://api.rhdxm.com/find \
  -H 'Content-Type: application/json' \
  -d '{"query": "kubernetes monitoring", "max_results": 5}'
```

完整的 API 文档请访问：https://api.rhdxm.com/docs

## MCP

您可以通过 `streamable HTTP` 协议访问 MCP 服务器，地址为 `https://api.rhdxm.com/mcp/`，使用工具 `find_server` 进行连接。

## 数据透明度

- **发送的数据**：仅限于您的搜索查询内容。
- **不发送的数据**：个人信息、凭证、本地文件或系统数据。
- **无需 API 密钥或账户**。源代码链接：https://github.com/c5huracan/meyhem