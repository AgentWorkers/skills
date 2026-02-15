---
name: mcps
description: MCP CLI Manager – 用于管理MCP服务器并调用相关工具
homepage: https://github.com/maplezzk/mcps
metadata: {"clawdbot":{"emoji":"🔌","requires":{"bins":["mcps"]},"install":[{"id":"npm","kind":"node","package":"@maplezzk/mcps","bins":["mcps"],"label":"Install mcps"}]}}
---

# mcps - MCP CLI Manager

这是一个功能强大的命令行工具，用于管理和调用MCP（Model Context Protocol）服务器。

## 安装

```bash
npm install -g @maplezzk/mcps
```

## 配置示例

### 添加多种MCP服务器

```bash
# Add fetch server (web scraping)
mcps add fetch --command uvx --args mcp-server-fetch

# Add PostgreSQL server
mcps add postgres --command npx --args @modelcontextprotocol/server-postgres --env POSTGRES_CONNECTION_STRING="${DATABASE_URL}"

# Add GitLab server
mcps add gitlab --command npx --args gitlab-mcp-server

# Add SSE server
mcps add remote --type sse --url http://localhost:8000/sse

# Add HTTP server
mcps add http-server --type http --url http://localhost:8000/mcp
```

### 配置文件示例（`~/.mcps/mcp.json`）

```json
{
  "servers": [
    {
      "name": "fetch",
      "type": "stdio",
      "command": "uvx",
      "args": ["mcp-server-fetch"]
    },
    {
      "name": "postgres",
      "type": "stdio",
      "command": "npx",
      "args": ["@modelcontextprotocol/server-postgres"],
      "env": {
        "POSTGRES_CONNECTION_STRING": "${DATABASE_URL}"
      }
    },
    {
      "name": "gitlab",
      "type": "stdio",
      "command": "npx",
      "args": ["gitlab-mcp-server"],
      "env": {
        "GITLAB_PERSONAL_ACCESS_TOKEN": "${GITLAB_TOKEN}",
        "GITLAB_API_URL": "https://gitlab.com/api/v4"
      }
    }
  ]
}
```

**注意**：对于敏感数据，请使用环境变量（格式为`${VAR_NAME}`）。

## 快速入门

```bash
# 1. Add an MCP server
mcps add fetch --command uvx --args mcp-server-fetch

# 2. Start the daemon
mcps start

# 3. Check status
mcps status

# 4. List available tools
mcps tools fetch

# 5. Call a tool
mcps call fetch fetch url="https://example.com"
```

## 命令参考

### 服务器管理

| 命令 | 描述 |
|---------|-------------|
| `mcps ls` | 列出所有已配置的服务器 |
| `mcps add <名称> --command <命令> --args <参数>` | 添加新的服务器 |
| `mcps rm <名称>` | 删除服务器 |
| `mcps update [名称]` | 更新服务器配置 |
| `mcps update <名称> --disabled true` | 禁用服务器 |

### 守护进程控制

| 命令 | 描述 |
|---------|-------------|
| `mcps start [--verbose]` | 启动守护进程（详细日志模式，便于调试） |
| `mcps stop` | 停止守护进程 |
| `mcps restart [服务器名称]` | 重启守护进程或特定服务器 |
| `mcps status` | 检查守护进程的状态 |

### 工具调用

| 命令 | 描述 |
|---------|-------------|
| `mcps tools <服务器名称> [--simple]` | 列出可用的工具 |
| `mcps call <服务器名称> <工具名称> [参数...]` | 调用指定的工具 |

## 参数传递方式

### 默认模式（自动解析JSON）

```bash
# String values are sent as-is
mcps call fetch fetch url="https://example.com"

# Numbers and booleans are auto-parsed
mcps call fetch fetch max_length=5000 follow_redirects=true
# Sends: { "max_length": 5000, "follow_redirects": true }

# JSON objects (use single quotes outside)
mcps call my-server createUser user='{"name": "Alice", "age": 30}'
```

### --raw模式（将参数保持为字符串）

```bash
# Use --raw for SQL IDs, codes, or strings that should not be parsed
mcps call my-db createOrder --raw order_id="12345" sku="ABC-001"
# Sends: { "order_id": "12345", "sku": "ABC-001" }

# SQL with special characters
mcps call alibaba-dms createDataChangeOrder --raw \
  database_id="123" \
  script="DELETE FROM table WHERE id = 'xxx';" \
  logic="true"
```

### --json模式（处理复杂参数）

```bash
# From JSON string
mcps call my-server createUser --json '{"name": "Alice", "age": 30}'

# From file
mcps call my-server createUser --json params.json
```

## 实际使用示例

### 场景1：网页抓取与搜索

```bash
# Fetch webpage content
mcps call fetch fetch url="https://example.com" max_length=5000

# Deep fetch (follow links)
mcps call fetch fetch url="https://example.com" follow_redirects=true max_depth=2

# Filtered fetch
mcps call fetch fetch url="https://news.example.com" include_tags='["article", "p"]' exclude_tags='["script", "style"]'
```

### 场景2：数据库查询

```bash
# Query data (auto-parsed parameters)
mcps call postgres query sql="SELECT * FROM users WHERE active = true LIMIT 10"

# Keep parameters as strings (use --raw)
mcps call postgres query --raw sql="SELECT * FROM orders WHERE id = '12345'"
```

### 场景3：传递复杂参数

```bash
# JSON object parameters
mcps call my-server createUser user='{"name": "Alice", "age": 30, "tags": ["admin", "user"]}'

# Load JSON from file
mcps call my-server createUser --json user.json

# Mixed parameters (some auto-parsed, some raw)
mcps call my-server update --raw id="123" data='{"name": "Updated"}'
```

### 场景4：服务器管理

```bash
# View all server configurations
mcps ls

# Check active connections
mcps status

# Restart a single server
mcps restart postgres

# Restart all servers
mcps restart

# Disable a server (without removing config)
mcps update my-server --disabled true

# Remove a server
mcps rm my-server
```

### 场景5：工具过滤与搜索

```bash
# Show only tool names (simple mode)
mcps tools postgres --simple

# Filter tools by keyword
mcps tools postgres --tool query --tool describe

# Find tools containing "create"
mcps tools postgres --tool create
```

## 配置文件

- **配置文件**：`~/.mcps/mcp.json`
- **环境变量**：
  - `MCPS_CONFIG_DIR`：配置目录
  - `MCPS_PORT`：守护进程端口（默认：4100）
  - `MCPS_VERBOSE`：详细日志模式

## 常见问题解答

**问：如何检查服务器状态？**
```bash
mcps status  # Check active connections
mcps ls      # Check all configurations (including disabled)
```

**问：服务器连接失败了？**
```bash
mcps start --verbose  # View detailed logs
mcps restart my-server  # Restart specific server
```

**问：如何快速查找工具？**
```bash
mcps tools my-server --tool keyword  # Filter by keyword
mcps tools my-server --simple        # Show names only
```

**问：参数中包含特殊字符（例如SQL字符）怎么办？**
```bash
# Use --raw to keep string format
mcps call alibaba-dms createDataChangeOrder --raw \
  database_id="123" \
  script="DELETE FROM table WHERE id = 'xxx';" \
  logic="true"
```

**问：守护进程启动缓慢？**
- 首次启动时会加载所有服务器，这需要10-15秒，属于正常现象。
- 之后的启动速度会更快（约2秒）。
- 可以使用`mcps ls`命令在不启动守护进程的情况下查看配置信息。