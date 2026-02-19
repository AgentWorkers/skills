---
name: mcporter
description: 使用 `mcporter` CLI 直接列出、配置、认证以及调用 MCP 服务器/工具（支持 HTTP 或标准输入/输出方式），包括自定义服务器的配置修改以及 CLI 代码的生成。
homepage: http://mcporter.dev
metadata: {"clawdbot":{"emoji":"📦","requires":{"bins":["mcporter"]},"install":[{"id":"node","kind":"node","package":"mcporter","bins":["mcporter"],"label":"Install mcporter (node)"}]}}
---

# mcporter

使用 `mcporter` 可以直接与 MCP 服务器进行交互。

**快速入门：**
- `mcporter list`：列出所有可用的 MCP 服务器。
- `mcporter list <server> --schema`：列出指定服务器的可用协议/模式。
- `mcporter call <server.tool> key=value`：调用服务器上的指定工具，并传递参数。

**工具调用示例：**
- **问题查询：** `mcporter call linear.list_issues team=ENG limit:5`  
- **创建问题：** `mcporter call "linear.create_issue(title="Bug")`  
- **数据获取：** `mcporter call https://api.example.com/mcp.fetch url="https://example.com"`  
- **脚本执行：** `mcporter call --stdio "bun run ./server.ts scrape url=https://example.com"`  
- **JSON 数据传递：** `mcporter call <server.tool> --args '{"limit":5}'`  

**身份验证与配置：**
- **OAuth：** `mcporter auth <server | url> [--reset]`  
- **配置管理：** `mcporter config list|get|add|remove|import|login|logout`  

**守护进程管理：**
- `mcporter daemon start`：启动守护进程  
- `mcporter daemon status`：查看守护进程状态  
- `mcporter daemon stop`：停止守护进程  
- `mcporter daemon restart`：重启守护进程  

**代码生成：**
- **命令行工具：** `mcporter generate-cli --server <name>` 或 `--command <url>`  
- **代码检查：** `mcporter inspect-cli <path> [--json]`  
- **类型转换：** `mcporter emit-ts <server> --mode client|types`  

**注意事项：**
- **默认配置文件：** `./config/mcporter.json`（可通过 `--config` 参数覆盖）。  
- **输出格式：** 使用 `--output json` 可获得机器可读的格式化结果。