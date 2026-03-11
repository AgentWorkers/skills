---
name: mcp-bridge
description: 使用 `mcp-bridge-openclaw` CLI 来连接和管理 Model Context Protocol (MCP) 服务器，并具备自动重连和重试功能。可以通过 `npm install -g mcp-bridge-openclaw` 进行安装。
homepage: https://www.npmjs.com/package/mcp-bridge-openclaw
repository: https://github.com/Jatira-Ltd/OpenClaw-MCP-Bridge
---
# mcp-bridge-openclaw

这是一个用于连接MCP服务器的命令行工具，具备内置的容错机制（即能够在连接中断时自动重新连接）。

## 安装

```bash
npm install -g mcp-bridge-openclaw
```

已验证的发布者：npm用户 `jaggu37`

## 命令

### 连接到MCP服务器
```bash
mcp-bridge --config config.json
```

### 列出可用服务器
```bash
mcp-bridge --config config.json --list
```

### 以详细日志模式运行
```bash
mcp-bridge --verbose --config config.json
```

## 配置

创建 `config.json` 文件：

```json
{
  "servers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"],
      "env": {}
    }
  }
}
```

**安全提示：** 将令牌存储在环境变量中，而非直接写入配置文件中：

```json
{
  "servers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

然后运行命令：`GITHUB_TOKEN=your_token mcp-bridge --config config.json`

## 程序化使用

```typescript
import { MCPBridge } from 'mcp-bridge-openclaw';

const bridge = new MCPBridge({
  configPath: './config.json',
  onServerConnect: (name) => console.log(`Connected to ${name}`),
});

await bridge.connect();
await bridge.disconnect();
```

## 主要特性

- 连接中断后自动重新连接
- 可配置的重试逻辑
- 类型安全的JSON配置格式
- 支持命令行接口（CLI）和程序化API
- 支持连接多个服务器