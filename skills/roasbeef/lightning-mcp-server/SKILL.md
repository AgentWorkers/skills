---
name: lightning-mcp-server
description: 构建并配置用于 Lightning Node Connect (LNC) 的 MCP 服务器。该服务器通过加密的 WebSocket 隧道将 AI 助手连接到 lnd 节点，无需直接的网络访问或 TLS 证书。默认情况下，MCP 服务器仅提供读取权限（支持 18 种工具，用于查询节点状态、通道信息、支付记录、发票数据以及链上信息）。
---

# MCP LNC 服务器

构建并配置 MCP 服务器，该服务器通过 **Lightning Node Connect (LNC)** 将 AI 助手连接到 Lightning 节点。LNC 使用加密的 WebSocket 隧道，因此代理程序无需直接访问 gRPC、TLS 证书或 macaroons——只需提供来自 Lightning Terminal 的 10 个单词组成的配对短语即可。

MCP 服务器默认为 **只读** 模式——它提供了 18 个工具用于查询节点状态，但无法发送支付或修改通道。

## 快速入门

```bash
# 1. Build the MCP server binary
skills/lightning-mcp-server/scripts/install.sh

# 2. Configure environment (mailbox server, dev mode, etc.)
skills/lightning-mcp-server/scripts/configure.sh

# 3. Add to Claude Code as an MCP server
skills/lightning-mcp-server/scripts/setup-claude-config.sh
```

然后重启 Claude Code。此时 `lnc_connect` 工具将可用，可以使用配对短语连接到任何 lnd 节点。

## 工作原理

```
Claude Code  <--stdio-->  lightning-mcp-server  <--LNC WebSocket-->  Mailbox  <-->  lnd
```

1. Claude Code 以子进程的形式启动 `lightning-mcp-server`（使用 stdio 传输方式）。
2. 代理程序使用配对短语和密码调用 `lnc_connect`。
3. 服务器生成一个临时的 ECDSA 密钥对，并通过 mailbox 中继打开一个加密的 WebSocket 隧道。
4. 连接成功后，代理程序可以调用这 18 个只读工具中的任意一个。
5. `lncdisconnect` 用于关闭隧道。

所有密钥、证书或 macaroons 都不会存储在磁盘上——配对短语是唯一的凭证，并且仅在内存中处理。

## 安装

```bash
# Build from source (requires Go 1.24+)
skills/lightning-mcp-server/scripts/install.sh

# Verify
lightning-mcp-server -version
```

安装脚本从本仓库的 `lightning-mcp-server/` 目录构建。

## 配置

```bash
# Generate .env with defaults
skills/lightning-mcp-server/scripts/configure.sh

# Production (mainnet via Lightning Terminal)
skills/lightning-mcp-server/scripts/configure.sh --production

# Development (local regtest)
skills/lightning-mcp-server/scripts/configure.sh --dev --mailbox aperture:11110
```

配置信息存储在 `lightning-mcp-server/.env` 文件中。关键配置参数如下：

| 变量 | 默认值 | 说明 |
|----------|---------|-------------|
| `LNC_MAILBOX_SERVER` | `mailbox.terminal.lightning.today:443` | Mailbox 中继服务器地址 |
| `LNC_DEV_MODE` | `false` | 启用开发模式 |
| `LNC_INSECURE` | `false` | 跳过 TLS 验证（仅限开发环境） |
| `LNC_CONNECT_TIMEOUT` | `30` | 连接超时时间（以秒为单位） |

## Claude Code 集成

### 方式 1：`claude mcp add`（推荐）

通过一条命令注册 MCP 服务器——无需构建步骤：

```bash
# Zero-install via npx (downloads pre-built binary)
claude mcp add --transport stdio lnc -- npx -y @lightninglabs/lightning-mcp-server

# With environment variables for production
claude mcp add --transport stdio \
  --env LNC_MAILBOX_SERVER=mailbox.terminal.lightning.today:443 \
  lnc -- npx -y @lightninglabs/lightning-mcp-server

# For development/regtest
claude mcp add --transport stdio \
  --env LNC_MAILBOX_SERVER=localhost:11110 \
  --env LNC_DEV_MODE=true \
  --env LNC_INSECURE=true \
  lnc -- npx -y @lightninglabs/lightning-mcp-server
```

可选范围：`--scope local`（默认，仅限当前用户），`--scope project`（通过 `.mcp.json` 共享），`--scope user`（所有项目）。

### 方式 2：使用设置脚本（从源代码安装）

```bash
# Add lightning-mcp-server to Claude Code's MCP config
skills/lightning-mcp-server/scripts/setup-claude-config.sh

# Project-level config (current project only)
skills/lightning-mcp-server/scripts/setup-claude-config.sh --scope project

# Global config (all projects)
skills/lightning-mcp-server/scripts/setup-claude-config.sh --scope global
```

此方法会将服务器添加到 Claude Code 的 `.mcp.json`（项目配置文件）或 `~/.claude.json`（全局配置文件）中。重启 Claude Code 后，LNC 工具即可使用。

### 方式 3：手动配置

在项目根目录下的 `.mcp.json` 文件中进行配置：

```json
{
  "mcpServers": {
    "lnc": {
      "command": "npx",
      "args": ["-y", "@lightninglabs/lightning-mcp-server"],
      "env": {
        "LNC_MAILBOX_SERVER": "mailbox.terminal.lightning.today:443"
      }
    }
  }
}
```

或者使用本地构建的二进制文件进行配置：

```json
{
  "mcpServers": {
    "lnc": {
      "command": "lightning-mcp-server",
      "env": {
        "LNC_MAILBOX_SERVER": "mailbox.terminal.lightning.today:443"
      }
    }
  }
}
```

也可以通过 Docker 运行服务器：

```json
{
  "mcpServers": {
    "lnc": {
      "command": "docker",
      "args": [
        "run", "--rm", "-i", "--network", "host",
        "--env", "LNC_MAILBOX_SERVER",
        "--env", "LNC_DEV_MODE",
        "--env", "LNC_INSECURE",
        "lightning-mcp-server"
      ]
    }
  }
}
```

## 可用的工具（共 18 个）

### 连接相关工具

| 工具 | 说明 |
|------|-------------|
| `lnc_connect` | 通过 LNC 配对短语连接到 lnd 节点 |
| `lncdisconnect` | 关闭当前的 LNC 连接 |

### 节点相关工具

| 工具 | 说明 |
|------|-------------|
| `lnc_get_info` | 节点别名、版本、同步状态、区块高度 |
| `lnc_get_balance` | 钱包余额（链上余额）和通道余额 |

### 通道相关工具

| 工具 | 说明 |
|------|-------------|
| `lnc_list_channels` | 活动/非活动通道及其容量、余额 |
| `lnc_pending_channels` | 正在打开或关闭的通道 |

### 发票相关工具

| 工具 | 说明 |
|------|-------------|
| `lnc_decodeinvoice` | 解码 BOLT11 发票 |
| `lnc_list_invoices` | 分页显示发票列表 |
| `lnc_lookupinvoice` | 根据支付哈希查找发票 |

### 支付相关工具

| 工具 | 说明 |
|------|-------------|
| `lnc_list_payments` | 分页显示支付历史记录 |
| `lnc_track_payment` | 根据哈希追踪特定支付记录 |

### 对等节点及网络相关工具

| 工具 | 说明 |
|------|-------------|
| `lnc_list_peers` | 连接的对等节点及其统计信息 |
| `lnc_describe_graph` | Lightning Network 的拓扑结构示例 |
| `lnc_get_node_info` | 特定节点的详细信息 |

### 链上相关工具

| 工具 | 说明 |
|------|-------------|
| `lnc_list_unspent` | 未花费的交易输出（UTXOs）及其确认状态 |
| `lnc_get_transactions` | 链上交易历史记录 |
| `lnc_estimate_fee` | 预计的确认费用 |

## 安全模型

- **无需存储凭证：** 配对短语仅在内存中处理。每次会话都会生成临时的 ECDSA 密钥对。
- **只读权限：** 不支持任何支付、通道或状态修改操作。代理程序只能查看数据，无法进行修改。
- **加密隧道：** 所有流量都通过 mailbox 中继进行端到端加密。mailbox 无法读取传输的数据。
- **无直接访问：** 代理程序不会直接连接到 lnd 节点的 gRPC 端口——所有流量都通过 mailbox 中继传输。

### 与直接使用 gRPC 的比较

| | MCP LNC 服务器 | 直接使用 lncli/gRPC |
|---|---|---|
| **凭证要求：** 配对短语（仅存储在内存中） | TLS 证书 + macaroons（存储在磁盘上） |
| **网络连接：** 通过 mailbox 中继的 WebSocket | 直接通过 TCP 连接到 gRPC 端口 |
| **防火墙要求：** 无需开放额外的端口 | 必须能访问端口 10009 |
| **权限控制：** 仅限读取（硬编码） | 权限取决于 macaroons 的使用范围 |
| **配置方式：** 通过 Lightning Terminal 提供配对短语 | 需要导出证书和 macaroons 文件 |

## 先决条件

- 需要 Go 1.24 或更高版本的编程语言来从源代码构建服务器。
- 目标节点上需要安装 Lightning Terminal (litd) 以生成配对短语。
- 需要安装 Claude Code 以便集成 MCP 服务器。

## 故障排除

### “配对短语必须由 10 个单词组成”
配对短语由 Lightning Terminal 生成，必须由 10 个单词组成，单词之间用空格分隔。

### “连接超时”
请检查 mailbox 中继服务器是否可访问。在生产环境中，请确保 `mailbox.terminal.lightning.today:443` 端口未被防火墙阻止。

### “TLS 握手失败”
如果使用本地测试环境（regtest），请启用开发模式（`LNC_DEV_MODE`）和不安全模式（`LNC_INSECURE`）：

```bash
skills/lightning-mcp-server/scripts/configure.sh --dev --insecure
```

### 工具在 Claude Code 中未显示
运行 `setup-claude-config.sh` 后重启 Claude Code。确认 `lightning-mcp-server` 是否已添加到 `$PATH` 环境变量中：

```bash
which lightning-mcp-server
```