---
name: factory-ai
description: 使用 Factory AI 的 droid CLI 来执行软件工程任务。该工具支持交互式模式、执行模式（exec mode）、MCP 服务器以及插件功能。
metadata: {"clawdbot":{"emoji":"🤖","requires":{"bins":["droid"]}}
---

# Factory AI Droid CLI

使用 `droid` 命令来构建功能、调试代码、重构代码以及部署应用程序。

## 安装

`droid` 已安装在以下路径：`/Users/mitchellbernstein/.local/bin/droid`

## 认证

```bash
droid login
# or set FACTORY_API_KEY env var
export FACTORY_API_KEY=your-api-key
```

## 命令

### 交互式模式
```bash
droid                           # Start fresh session
droid "fix the login bug"       # Start with prompt
droid -r                        # Resume last session
droid -r session-id             # Resume specific session
```

### 非交互式（执行模式）
```bash
droid exec "analyze this file"
droid exec "commit my changes with a good message"
droid exec "deploy to fly.io"
droid exec --help               # Show exec options
```

### 执行命令的选项
```bash
droid exec --force "fix lint errors"    # Auto-apply without confirmation
droid exec --json "analyze code"        # JSON output
droid exec --model claude "task"        # Specify model
```

### MCP 服务器
```bash
droid mcp list                    # List installed MCP servers
droid mcp add server-name         # Add MCP server
droid mcp remove server-name      # Remove MCP server
```

### 插件
```bash
droid plugin list                 # List plugins
droid plugin add name             # Add plugin
```

## 使用场景

### 功能开发
```bash
droid exec "add a user settings page with dark mode toggle"
```

### 调试
```bash
droid exec "fix this error: [paste error]"
```

### 代码审查
```bash
droid exec "review the PR for security issues"
```

### Git 操作
```bash
droid exec "create a PR for my changes"
droid exec "write a good commit message for the staged changes"
```

### 部署
```bash
droid exec "deploy to fly.io"
```

### 多文件修改
```bash
droid
# Then in interactive mode:
@src/components/
@src/api/
Implement authentication flow
```

## 注意事项

- `droid` 能够深入理解整个组织内的代码库结构。
- 支持多种模型框架（如 OpenAI、Anthropic、xAI 等）。
- 提供 MCP 服务器以扩展应用程序的功能。
- 采用基于会话的内存管理机制，确保代码执行的上下文连续性。