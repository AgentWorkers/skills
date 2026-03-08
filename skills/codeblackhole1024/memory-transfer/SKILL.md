---
name: memory-transfer
description: Transfer memory between OpenClaw agents with advanced features: topic-specific filtering, user info privacy protection, and intelligent agent identity adaptation. Use when: (1) Migrating context between agents, (2) Sharing knowledge without leaking user personal info, (3) Backing up agent memory. Supports share mode (filters user data + adapts to target agent) and clone mode (verbatim copy).
metadata:
  {
    "openclaw": { "emoji": "📦" }
  }
---

# 内存传输功能

用于在 OpenClaw 代理之间传输内存文件和上下文数据。

## 使用场景

- 将内存从主代理迁移到子代理
- 将用户偏好设置复制到新代理
- 在代理之间共享项目上下文
- 在重置之前备份代理内存

## 工作原理

1. 读取源代理的工作区内存文件
2. 将文件复制到目标代理的工作区
3. （可选）将文件与目标代理现有的内存合并

## 命令

### 列出所有可用代理

```bash
ls /home/node/.openclaw/
```

### 从源代理向目标代理传输内存

```bash
node memory-transfer.js transfer <source-agent-id> <target-agent-id>
```

### 传输特定的内存文件

```bash
node memory-transfer.js transfer <source-agent-id> <target-agent-id> <memory-file>
```

### 列出代理的内存文件

```bash
node memory-transfer.js list <agent-id>
```

### 预览传输内容（模拟传输）

```bash
node memory-transfer.js transfer <source> <target> --dry-run
```

## 示例

### 将主代理的内存传输到编码代理

```bash
node memory-transfer.js transfer main coder
```

### 传输特定的内存文件（例如：特定日期的数据）

```bash
node memory-transfer.js transfer main coder 2026-03-01.md
```

### 预览即将传输的内容

```bash
node memory-transfer.js transfer main coder --dry-run
```

## 代理工作区

OpenClaw 代理的工作区通常位于：
- `/home/node/.openclaw/workspace-<agent-id>/`
- 主代理：`/home/node/.openclaw/workspace-main/`

内存文件格式：
- `MEMORY.md`：长期存储的内存数据
- `memory/YYYY-MM-DD.md`：每日生成的内存记录