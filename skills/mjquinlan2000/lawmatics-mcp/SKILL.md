---
name: lawmatics-mcp
description: MCP服务器用于Lawmatics的法律CRM API。它将Lawmatics的REST API作为只读的MCP工具提供给用户使用。
metadata: { "openclaw": { "requires": { "bins": ["mcporter", "lawmatics-mcp"], "env": ["NODE_MCP_SECRET_KEY"] } } }
---
# Lawmatics MCP 服务器

这是一个仅用于读取数据的 MCP 服务器，用于 Lawmatics 法律客户关系管理（CRM）API。

## 使用方法

使用 `mcporter` 通过标准输入（stdio）与该服务器进行交互：

- **列出可用工具：** `mcporter list --stdio lawmatics-mcp`
- **调用某个工具：** `mcporter call --stdio lawmatics-mcp <tool_name> [args]`

## 链接

- **npm：** https://www.npmjs.com/package/@mjquinlan2000/lawmatics-mcp