---
name: openclaw-docs
description: OpenClaw功能、配置选项及最佳实践的参考文档。当用户需要了解OpenClaw的特性、配置方案、定时任务（cron jobs）、多代理路由（multi-agent routing）或故障排除（troubleshooting）相关信息时，请参考本文档。
metadata:
  {"openclaw": {"always": true, "emoji": "📚"}}
---

# OpenClaw 文档参考

OpenClaw 功能的快速参考。

## 配置路径（agentsdefaults）

| 功能 | 配置路径 |
|---------|-------------|
| 内存刷新 | `compaction.memoryFlush.enabled` |
| 会话内存 | `memorySearch.experimental.sessionMemory` |
| 网页搜索 | `tools.web.search.{enabled,provider,apiKey}` |
| Cron 任务 | `cron.{enabled,store,maxConcurrentRuns}` |
| 技能目录 | `skills.load.extraDirs[]` |
| 多代理 | `agents.list[], bindings[]` |
| 沙箱环境 | `agentsdefaults.sandbox.{mode,scope,workspaceAccess}` |

## Cron 任务类型

**主会话**（使用心跳机制）：
```json
{
  "schedule": {"kind": "at", "atMs": 1234567890000},
  "sessionTarget": "main",
  "payload": {"kind": "systemEvent", "text": "Check calendar"}
}
```

**隔离会话**（专用代理执行）：
```json
{
  "schedule": {"kind": "cron", "expr": "0 7 * * *", "tz": "UTC"},
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "Morning brief",
    "deliver": true,
    "channel": "telegram"
  }
}
```

## 工具类别

- **核心工具**：read、write、edit、apply_patch
- **Shell 工具**：exec、process
- **Web 工具**：web_search、web_fetch、browser
- **会话管理工具**：sessions_list、sessions_history、sessions_send、sessions_spawn
- **调度工具**：cron、system event
- **系统管理工具**：gateway、nodes、canvas
- **内存管理工具**：memory_search、memory_get

## 安全策略

- `requires.bins`：必须在 PATH 环境变量中存在的二进制文件
- `requires.env`：必需的环境变量
- `requires.config`：必须为真值的配置路径
- `os`：操作系统类型（darwin、linux、win32）

详情请参阅相关参考资料。