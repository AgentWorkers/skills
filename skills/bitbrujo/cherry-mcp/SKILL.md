---
name: cherry-mcp
description: 这是一个HTTP桥接器，用于保持MCP服务器的正常运行，并通过REST接口将这些服务器暴露出来。它专为那些需要使用MCP工具但缺乏原生MCP支持的OpenClaw代理程序而设计。
tags: mcp, bridge, rest, api, openclaw, http, tools, automation, stdio
---

# Cherry MCP 🍒

## 起源故事

这个项目诞生于一个深夜的编程时光，当时我尝试使用 OpenClaw 来操作 MCP 服务器。然而，这些服务器总是会意外终止——因为 MCP 依赖于标准输入/输出（stdio）接口，如果没有一个持续运行的客户端来维持连接，进程就会自动结束。

OpenClaw 本身并不支持 MCP 服务器，而通过 `exec` 命令来运行它们的话，一旦服务器停止响应，它们也会被立即终止。为了解决这个问题，我开发了一个中间代理：这个代理负责创建 MCP 服务器，保持它们的运行状态，并通过 HTTP REST 接口暴露它们的功能。

项目名称取自我常用的表情符号 🍒。

*— EULOxGOS, 2026年2月*

## 为什么需要 Cherry MCP？

MCP 服务器依赖于 stdio 接口，因此在没有持续运行的客户端的情况下会自动关闭。Cherry MCP 的主要功能包括：
- 以子进程的形式启动 MCP 服务器；
- 在服务器崩溃时自动重启它们；
- 为每个服务器提供 HTTP 接口。

## 快速入门

```bash
# Add a server
node cli.js add-server github npx @anthropic/mcp-github

# Set env vars for the server
node cli.js set-env github GITHUB_TOKEN ghp_xxx

# Start
pm2 start bridge.js --name cherry-mcp
```

## 命令行界面（CLI）

```bash
# Servers
node cli.js add-server <name> <command> [args...]
node cli.js remove-server <name>
node cli.js list-servers

# Environment variables
node cli.js set-env <server> <KEY> <value>
node cli.js remove-env <server> <KEY>

# Security
node cli.js set-rate-limit <rpm>      # requests per minute
node cli.js set-allowed-ips <ip>...   # IP allowlist
node cli.js enable-audit-log          # log requests

# Other
node cli.js show-config
node cli.js restart
```

## HTTP API

```bash
# List servers
curl http://localhost:3456/

# List tools
curl http://localhost:3456/<server>/tools

# Call a tool
curl -X POST http://localhost:3456/<server>/call \
  -H "Content-Type: application/json" \
  -d '{"tool": "search", "arguments": {"query": "test"}}'

# Restart server
curl -X POST http://localhost:3456/<server>/restart
```

## 安全性设置

- 仅绑定到本地地址 `127.0.0.1`（不对外部网络开放）；
- 支持可选的速率限制功能；
- 提供可选的 IP 白名单功能；
- 支持审计日志记录功能；
- 每次请求的最大数据传输量限制为 1MB。

### ⚠️ 重要提示

- 所有命令都需要用户自行配置。代理程序仅执行 `config.json` 文件中指定的命令，不会接受通过 HTTP 发送的任意命令。你可以完全控制哪些命令会被执行。
- **请勿在代码中存储敏感信息！** 如果你通过 `set-env` 命令设置了 API 密钥，这些密钥会以明文形式保存在 `config.json` 文件中。为了避免安全风险，请将这些密钥添加到 `.gitignore` 文件中，或者使用环境变量来管理它们：
  ```bash
# Alternative: set env vars before starting
export GITHUB_TOKEN=ghp_xxx
pm2 start bridge.js --name cherry-mcp
```

 之后在配置文件中引用这些环境变量时，只需提供变量名即可：
  ```json
{
  "servers": {
    "github": {
      "command": "npx",
      "args": ["@anthropic/mcp-github"],
      "env": {}
    }
  }
}
```

- 服务器会继承用户的 shell 环境设置。

## 运行方式

```bash
# pm2 (recommended)
pm2 start bridge.js --name cherry-mcp
pm2 save

# Auto-start on boot
pm2 startup
```