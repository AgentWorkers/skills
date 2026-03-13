---
name: meyhem-search
description: 这是一个网络搜索客户端，它向 api.rhdxm.com 发送请求并返回排名后的搜索结果。该客户端还可以根据用户需求获取页面内容（可选）。无需使用 API 密钥。
version: 0.2.4
author: c5huracan
homepage: https://github.com/c5huracan/meyhem
metadata:
  openclaw:
    requires:
      bins:
        - python3
---
# Meyhem 搜索

这是一个用于查询 AI 代理的 Web 搜索工具。它将查询发送到 `api.rhdxm.com`，该平台会通过多个搜索引擎进行搜索并返回排序后的结果。您还可以选择获取选定结果的页面内容。

无需 API 密钥，无需注册，也没有使用频率限制。

## 为什么选择 Meyhem？

- **简洁的界面**：只需发送查询，即可从多个搜索引擎获取排序后的结果。
- **可选的内容获取**：使用 `--content` 参数可以获取排名靠前结果的页面文本。

## 快速入门

```bash
python3 search.py "transformer attention mechanism"
python3 search.py "async python best practices" -n 3
python3 search.py "react server components" --content
python3 search.py "kubernetes debugging" --agent my-agent
```

## 快速入门（REST API）

完整的 API 文档：https://api.rhdxm.com/docs

```bash
curl -s -X POST https://api.rhdxm.com/search \
  -H 'Content-Type: application/json' \
  -d '{"query": "YOUR_QUERY", "agent_id": "my-agent", "max_results": 5}'
```

## MCP

您也可以通过 `https://api.rhdxm.com/mcp/` 连接到 MCP，以实现更丰富的集成功能。

## 数据透明度

Meyhem 会将您的搜索查询、代理标识符以及任何选定的 URL 发送到 `api.rhdxm.com`。该工具本身不会访问本地文件、环境变量或凭据，但您在查询或 `agent_id` 中包含的任何信息都会被传输。请避免发送敏感或专有内容。

源代码：https://github.com/c5huracan/meyhem