---
name: mcp-finder
description: 为您的任务找到合适的MCP服务器。系统索引了6700多台MCP服务器，并根据社区的信任度对它们进行了排名。无需使用API密钥。如需了解MCP与OpenClaw结合使用的功能，请参阅meyhem-capabilities。
version: 0.2.3
author: c5huracan
homepage: https://github.com/c5huracan/meyhem
metadata:
  openclaw:
    requires:
      bins:
        - python3
---
# MCP Finder

MCP Finder 可帮助您为任何任务找到合适的 MCP（MCP）服务器。该工具索引了来自 MCP 生态系统的 6,700 多台服务器，并根据社区的信任度（GitHub 星标）和相关性对它们进行排序。只需用简单的语言描述您的需求，即可获得最适合您任务的服务器。

无需 API 密钥，无需注册，也没有使用频率限制。

## 为什么选择 MCP Finder？

- **索引了 6,700 多台服务器**：数据来源于 `awesome-mcp-servers` 和官方 MCP 注册表，并通过 GitHub 元数据进行了补充。
- **支持自然语言搜索**：只需描述您的任务，即可获得相关结果。
- **基于信任度排序**：结合了 GitHub 星标和文本相关性进行排序。
- **完全依赖标准 Python 库**：无需额外依赖任何第三方库。

## 快速入门

```bash
python3 finder.py "I need to query a Postgres database"
python3 finder.py "browser automation" -n 3
python3 finder.py "kubernetes monitoring"
python3 finder.py "manage emails"
```

## REST API

```bash
curl -X POST https://api.rhdxm.com/find   -H 'Content-Type: application/json'   -d '{"query": "kubernetes monitoring", "max_results": 5}'
```

完整的 API 文档请访问：https://api.rhdxm.com/docs

## MCP

您可以通过 `streamable HTTP` 协议访问 MCP 服务器，地址为 `https://api.rhdxm.com/mcp/`，并使用 `find_server` 工具进行连接。

## 数据透明度

MCP Finder 会将您的搜索请求发送到 `api.rhdxm.com`。该工具本身不会访问本地文件、环境变量或凭据，但您在查询中输入的任何内容都会被传输。请避免发送敏感或专有信息。

源代码：https://github.com/c5huracan/meyhem