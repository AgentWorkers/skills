---
name: claude-local-bridge
version: 0.1.0
summary: Access local repos from Claude on your phone via approval-gated MCP bridge
tags:
  - mcp
  - file-access
  - remote-development
  - code-bridge
  - approval-gating
  - developer-tools
author: suhteevah
repository: https://github.com/suhteevah/claude-local-bridge
license: MIT
install:
  - pip install -r requirements.txt
env: []
---

# Claude 本地桥接器 (Claude Local Bridge)

通过手机上的 Claude 应用程序访问您的本地仓库。MCP 桥接服务器采用审批机制来确保安全性。

## 功能介绍

该工具运行一个基于 SSE 协议的本地 MCP 服务器，允许 Claude 访问您的文件——但只有在您通过实时控制面板明确批准每个请求后，Claude 才能执行文件操作。

## 提供的工具

- **browse_files**：列出工作区的文件结构（无需审批）
- **request_file_access**：请求读取/写入文件的权限（在您批准之前，相关操作将被阻止）
- **read_file**：读取已获批准文件的内容
- **write_file**：向已获批准的文件写入内容
- **list_approvals**：查看所有当前的审批记录
- **revoke_approval**：撤销访问权限
- **view_audit_log**：查看访问历史记录

## 快速入门

```bash
git clone https://github.com/suhteevah/claude-local-bridge.git
cd claude-local-bridge
pip install -r requirements.txt
python -m app.main --roots ~/projects
```

接下来，将 Claude 应用程序连接到 `http://localhost:9120/mcp/sse` 协议地址。

## 安全性特性

- 仅允许访问白名单中的目录
- 禁用某些扩展名（如 `.env`、`.pem`、`.key` 等）
- 防止路径遍历攻击
- 采用令牌认证机制
- 所有文件访问操作均需人工审批
- 提供完整的审计记录

## 远程访问方式

您可以使用 Tailscale（免费）、Cloudflare Tunnel（免费）或 NetBird（开源软件）从手机上访问本地仓库。详情请参阅 [tunnel.md](https://github.com/suhteevah/claude-local-bridge/blob/main/tunnel.md)。