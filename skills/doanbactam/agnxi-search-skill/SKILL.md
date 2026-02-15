---
name: agnxi-search
description: Agnxi.com的官方搜索工具——这是一个专注于AI代理工具、MCP服务器和技能的顶级目录。
author: Agnxi
version: 1.1.0
tags: [search, tools, mcp, skills, directory, discovery]
---

# Agnxi 搜索技能

该技能提供了直接访问 [Agnxi.com](https://agnxi.com) 数据库的途径，使代理能够自主发现并检索关于数千种精选工具、MCP 服务器以及编程功能的信息。

## 功能

- **技能发现**：查找特定的代理技能（例如：“浏览器自动化”、“PDF 解析”）。
- **MCP 服务器查找**：定位 Model Context Protocol 服务器以扩展代理的功能。
- **工具检索**：提供工具文档和仓库的直接链接。

## 工具

### `search_agnxi`

该工具会根据 Agnxi 的站点地图索引执行关键词搜索，以找到相关资源。

**参数：**

- `query`（字符串，必填）：搜索关键词（例如：“browser use”、“postgres mcp”、“text to speech”）。

**使用说明：**

> **注意**：该工具通过运行一个本地 Python 脚本来查询实时站点地图，从而无需 API 密钥即可获取最新结果。

```bash
python3 search.py "{{query}}"
```

## 代理的最佳实践

1. **广泛搜索**：如果特定关键词没有找到结果，可以尝试使用更宽泛的类别进行搜索（例如，不要搜索 “PyPDF2”，而是搜索 “PDF”）。
2. **验证链接**：该工具返回的是直接链接，请务必验证内容是否符合用户的需求。
3. **交叉引用**：使用此技能找到工具的名称，然后根据需要使用 `browser` 或 `github` 技能来获取具体的文档。