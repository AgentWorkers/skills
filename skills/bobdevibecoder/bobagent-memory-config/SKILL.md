---
name: memory-config
description: 配置 Clawdbot 的内存设置，包括在数据压缩前的内存刷新以及会话内存搜索功能。当用户需要启用或配置诸如 `compaction.memoryFlush`、`sessionMemorySearch` 或 `memorySearchSources` 等内存相关功能时，请使用此设置。
---

# 内存配置技巧

此技巧用于配置代理的高级内存设置。

## 配置选项

### 1. 压缩前刷新内存
在内存压缩之前，将上下文数据保存到内存文件中。

**配置路径：** `agentsdefaults.compaction.memoryFlush.enabled`
**值：** `true` 或 `false`

### 2. 会话内存搜索
允许搜索过去的会话记录（而不仅仅是 `MEMORY.md` 文件）。

**配置路径：** `agentsdefaults.memorySearchexperimental.sessionMemory`
**值：** `true` 或 `false`

### 3. 内存搜索源
指定包含在内存搜索中的数据来源。

**配置路径：** `agentsdefaults.memorySearch.sources`
**值：** `["memory"]` 或 `["memory", "sessions"]`

## 使用方法

通过 `gateway config.patch` 应用配置更改：

```json
{
  "agents": {
    "defaults": {
      "compaction": {
        "memoryFlush": {
          "enabled": true
        }
      },
      "memorySearch": {
        "experimental": {
          "sessionMemory": true
        },
        "sources": ["memory", "sessions"]
      }
    }
  }
}
```

应用配置更改后，代理将自动重启。