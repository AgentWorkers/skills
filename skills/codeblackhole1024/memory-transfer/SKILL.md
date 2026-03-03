---
name: memory-transfer
description: 将内存文件从一个 OpenClaw 代理传输到另一个代理。当您需要将内存、配置或上下文从一个代理迁移到另一个代理时，请使用此方法。
metadata:
  {
    "openclaw": { "emoji": "📦" }
  }
---
# 内存传输技能

用于在 OpenClaw 代理之间传输内存文件和上下文信息。

## 使用场景

- 将内存从主代理迁移到子代理
- 将用户偏好设置复制到新代理
- 在代理之间共享项目上下文
- 在重置前备份代理内存

## 工作原理

1. 读取源代理的工作区内存文件
2. 将文件复制到目标代理的工作区
3. （可选）与目标代理现有的内存合并

## 命令

### 列出所有可用代理

```bash
ls /home/node/.openclaw/
```

### 从源代理传输内存到目标代理

```bash
node memory-transfer.js transfer <source-agent-id> <target-agent-id>
```

### 传输特定的内存文件

```bash
node memory-transfer.js transfer <source-agent-id> <target-agent-id> <memory-file>
```

### 列出代理的内存信息

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

### 传输特定的内存文件（例如：日期相关的文件）

```bash
node memory-transfer.js transfer main coder 2026-03-01.md
```

### 预览将要传输的内容

```bash
node memory-transfer.js transfer main coder --dry-run
```

## 代理工作区

OpenClaw 代理的工作区通常位于：
- `/home/node/.openclaw/workspace-<agent-id>/`
- 主代理：`/home/node/.openclaw/workspace-main/`

内存文件格式：
- `MEMORY.md` – 长期存储的内存数据
- `memory/YYYY-MM-DD.md` – 每日生成的内存记录