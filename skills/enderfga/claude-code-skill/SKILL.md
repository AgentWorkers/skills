# OpenClaw Claude 代码技能

## 描述

本技能实现了 OpenClaw/Clawdbot 与 MCP（Model Context Protocol）的集成。适用于以下场景：
- 连接并协调 MCP 工具服务器（如文件系统、GitHub 等）；
- 使用 IndexedDB 或 localStorage 在会话之间持久化数据；
- 在多个设备之间同步会话状态。

触发条件：`MCP`、`tool server`、`sub-agent orchestration`、`session sync`、`state persistence`、`Claude Code integration`。

## 安装

```bash
npm install openclaw-claude-code-skill
```

## 核心 API

### MCP 服务器管理

```typescript
import { 
  initializeMcpSystem, 
  addMcpServer, 
  executeMcpAction, 
  getAllTools 
} from "openclaw-claude-code-skill";

// 1. Initialize all configured servers
await initializeMcpSystem();

// 2. Add a new MCP server
await addMcpServer("fs", {
  command: "npx",
  args: ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]
});

// 3. Get available tools
const tools = await getAllTools();

// 4. Call a tool
const result = await executeMcpAction("fs", {
  method: "tools/call",
  params: { name: "read_file", arguments: { path: "/tmp/test.txt" } }
});
```

### 状态持久化

```typescript
import { createPersistStore, indexedDBStorage } from "openclaw-claude-code-skill";

const useStore = createPersistStore(
  { count: 0, items: [] },
  (set, get) => ({
    increment: () => set({ count: get().count + 1 }),
    addItem: (item: string) => set({ items: [...get().items, item] })
  }),
  { name: "my-store" },
  indexedDBStorage  // or omit for localStorage
);

// Check hydration status
if (useStore.getState()._hasHydrated) {
  console.log("State restored!");
}
```

### 会话同步

```typescript
import { mergeSessions, mergeWithUpdate, mergeKeyValueStore } from "openclaw-claude-code-skill";

// Merge chat sessions from multiple sources
const mergedSessions = mergeSessions(localSessions, remoteSessions);

// Merge configs with timestamp-based resolution
const mergedConfig = mergeWithUpdate(localConfig, remoteConfig);
```

## 主要功能

| 功能          | 用途                                      |
|-----------------|-----------------------------------------|
| `initializeMcpSystem()` | 根据配置启动所有 MCP 服务器                         |
| `addMcpServer(id, config)` | 动态添加新的 MCP 服务器                         |
| `removeMcpServer(id)` | 删除指定的 MCP 服务器                         |
| `pauseMcpServer(id)` | 暂停指定的 MCP 服务器                         |
| `resumeMcpServer(id)` | 恢复暂停的 MCP 服务器                         |
| `executeMcpAction(id, req)` | 在指定服务器上执行工具命令                         |
| `getAllTools()` | 获取所有可用的工具列表                         |
| `getClientsStatus()` | 获取所有 MCP 客户端的状态                         |
| `setConfigPath(path)` | 设置自定义配置文件路径                         |
| `createPersistStore()` | 创建具有持久化功能的存储系统                         |
| `mergeSessions()` | 合并多个会话数据                         |
| `mergeWithUpdate()` | 合并会话数据并处理时间戳差异                   |
| `mergeKeyValueStore()` | 合并键值对存储数据                         |

## 配置

创建 `mcp_config.json` 文件：

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"],
      "status": "active"
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_TOKEN": "your-token" },
      "status": "active"
    }
  }
}
```

设置自定义配置文件路径：

```typescript
import { setConfigPath } from "openclaw-claude-code-skill";
setConfigPath("/path/to/mcp_config.json");
```

## 系统要求

- Node.js 18 及以上版本                     |
- TypeScript（推荐使用，但非必需）                     |

## 链接

- [GitHub](https://github.com/Enderfga/openclaw-claude-code-skill)       |
- [npm](https://www.npmjs.com/package/openclaw-claude-code-skill)     |
- [MCP 规范文档](https://spec.modelcontextprotocol.io/)       |