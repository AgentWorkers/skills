---
name: mema
description: Mema的个人大脑系统：基于SQLite的文档索引机制与Redis的临时存储功能。该系统用于对MD格式的文件进行索引管理、存储用户的短期思维状态，并在不同会话之间协调记忆信息。
---
# Mema Brain（集中式记忆系统）

该功能为代理提供了**长期记忆**（存储在 SQLite 数据库中）和**短期上下文数据**（存储在 Redis 数据库中）。这些数据直接集成到了代理的核心数据库中。

## 架构

### 1. 长期记忆（SQLite）

- **存储路径：** `~/.openclaw/memory/main.sqlite`
- **数据库表：**
  - `documents`：知识文件的索引（包含文件的路径、标题和标签）。
  - `skills`：记录技能的使用情况及其成功率。
- **作用：** 提供持久化的存储空间，数据在代理重启后仍可保留，并会与代理的状态一起被备份。

### 2. 短期记忆（Redis）

- **键前缀：** `mema:mental:*`
- **用途：** 在不同会话之间传递上下文信息、缓存临时数据以及作为临时工作区。
- **过期时间：** 6 小时（与代理会话的生命周期相同）。

## 使用方法

### 索引知识

当你学习新内容或创建文档时：

```bash
scripts/mema.py index "docs/NEW_FEATURE.md" --tag "feature"
```

### 搜索记忆

查找相关的文档：

```bash
scripts/mema.py list --tag "iot"
```

### 保存当前状态（上下文）

为下一次会话保存当前的处理状态：

```bash
scripts/mema.py mental set context:summary "Working on Hub Redesign..."
```

### 检索状态

在需要时重新获取之前保存的状态：

```bash
scripts/mema.py mental get context:summary
```

## 设置步骤

1. 将 `.env.example` 文件复制到 `.env` 文件中，并根据需要配置 Redis 连接信息。
2. 安装依赖项：`pip install -r requirements.txt`（或使用虚拟环境）。
3. **初始化：** 运行 `scripts/mema.py init` 命令，以在 `main.sqlite` 中创建所需的数据库表。