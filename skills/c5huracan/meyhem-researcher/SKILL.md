---
name: meyhem-researcher
description: 多查询研究工具：可将一个主题拆分为多个具体的查询，预览最相关的结果。无需使用API密钥。
version: 0.1.9
author: c5huracan
homepage: https://github.com/c5huracan/meyhem
metadata:
  openclaw:
    requires:
      bins:
        - python3
---
# Meyhem 深度研究工具

这是一个多查询研究工具，可将一个主题拆分为多个具体的查询，通过 api.rhdxm.com 进行搜索，并预览搜索结果中的顶级条目。

无需 API 密钥，无需注册，也没有使用频率限制。

## 为什么选择 Meyhem Researcher？

- **多查询工作流程**：能够将一个主题拆分为多个查询，分别进行搜索，并预览每个查询的顶级结果。
- **每个查询可返回多个结果**：通过 api.rhdxm.com 进行搜索，并显示所有搜索结果中的顶级条目。

## 快速入门

```bash
python3 researcher.py "transformer attention mechanism"
python3 researcher.py "kubernetes networking" -n 3 -q 5
```

## 快速入门（REST API）

完整的 API 文档：https://api.rhdxm.com/docs

```bash
curl -s -X POST https://api.rhdxm.com/search \
  -H 'Content-Type: application/json' \
  -d '{"query": "YOUR_QUERY", "agent_id": "my-researcher", "max_results": 10}'
```

## MCP（管理控制面板）

您还可以通过 `https://api.rhdxm.com/mcp/` 连接到 MCP，以实现更丰富的集成功能。

## 数据透明度

该工具会将您的搜索查询、代理标识符以及您选择的任何 URL 发送到 `api.rhdxm.com`。该工具本身不会访问本地文件、环境变量或凭据，但您在查询或代理标识符中包含的任何内容都会被传输。请避免发送敏感或专有信息。

源代码：https://github.com/c5huracan/meyhem