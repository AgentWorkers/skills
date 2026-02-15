---
name: mcp-hub
description: 通过模型上下文协议（Model Context Protocol, MCP）访问1200多种AI代理工具
author: claude-office-skills
version: "1.0"
tags: ['mcp', 'ai-agent', 'tools', 'integration']
models: [claude-sonnet-4, claude-opus-4]
tools: [computer, code_execution, file_operations]
library:
  name: MCP Servers
  url: https://github.com/modelcontextprotocol/servers
  stars: 40k+
---

# Mcp Hub 技能

## 概述

该技能提供了对 1200 多个 MCP（Model Context Protocol）服务器的访问权限，这些服务器是用于扩展 AI 功能的标准化工具。可以将 Claude 与文件系统、数据库、API 和文档处理工具连接起来。

## 使用方法

1. 说明您想要完成的任务。
2. 提供所需的输入数据或文件。
3. 我将执行相应的操作。

**示例提示：**
- “访问本地文件系统以读写文档”
- “查询数据库以进行分析”
- “与 GitHub、Slack、Google Drive 集成”
- “运行文档处理工具”

## 领域知识


### MCP 架构

```
Claude ←→ MCP Server ←→ External Resource
        (Protocol)      (Files, APIs, DBs)
```

### 常用的 MCP 服务器

| 服务器 | 功能 | 星级 |
|--------|----------|-------|
| **filesystem** | 读写本地文件 | 官方提供 |
| **google-drive** | 访问 Google Docs/Sheets | 5000 多个评分 |
| **puppeteer** | 浏览器自动化、PDF 生成 | 10000 多个评分 |
| **sqlite** | 数据库查询 | 官方提供 |

### 配置示例

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/path/to/documents"
      ]
    },
    "google-drive": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-google-drive"]
    }
  }
}
```

### 查找 MCP 工具

可以浏览可用的服务器：
- [mcp.run](https://mcp.run) - MCP 市场平台
- [awesome-mcp-servers](https://github.com/wong2/awesome-mcp-servers)
- [mcp-awesome.com](https://mcp-awesome.com)

### 在技能中使用 MCP

```python
# MCP tools become available to Claude automatically
# Example: filesystem MCP provides these tools:

# read_file(path) - Read file contents
# write_file(path, content) - Write to file
# list_directory(path) - List directory contents
# search_files(query) - Search for files
```


## 最佳实践

1. **仅启用所需的 MCP 服务器（出于安全考虑）**
2. **在可能的情况下使用官方服务器**
3. **在启用之前检查服务器权限**
4. **结合多个服务器以完成复杂的工作流程**

## 安装

```bash
# Install required dependencies
pip install python-docx openpyxl python-pptx reportlab jinja2
```

## 资源

- [MCP 服务器仓库](https://github.com/modelcontextprotocol/servers)
- [Claude Office 技能中心](https://github.com/claude-office-skills/skills)