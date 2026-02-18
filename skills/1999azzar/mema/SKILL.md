---
name: mema
description: Mema的个人大脑：基于SQLite的元数据索引用于存储文档信息，同时结合Redis作为短期上下文缓存。该系统用于整理工作区的知识路径以及管理临时会话状态。
metadata: {"openclaw":{"requires":{"bins":["python3"],"env":["REDIS_HOST","REDIS_PORT"]},"install":[{"id":"pip-deps","kind":"exec","command":"pip install -r requirements.txt"}]}}
---# Mema Brain（集中式记忆系统）

这是一个标准化的记忆系统，提供元数据索引（SQLite）和短期存储功能（Redis）。

## 核心组件

### 1. 文档索引（SQLite）
- **主路径：** `~/.openclaw/memory/main.sqlite`
- **功能：** 存储文件路径、标题和标签。
- **注意：** 这只是一个元数据索引，不支持文件内容的导入或全文搜索。

### 2. 短期记忆（Redis）
- **键前缀：** `mema:mental:*
- **用途：** 管理临时状态和跨会话的数据传递。
- **过期时间（TTL）：** 默认为6小时（21600秒）。

## 核心工作流程

### 索引知识
将文件的位置和标签记录到本地数据库中。
- **用法：** `python3 $WORKSPACE/skills/mema/scripts/mema.py index <path> [--tag <tag>]`

### 搜索索引
根据标签或最近访问时间列出被索引的文件路径。
- **用法：** `python3 $WORKSPACE/skills/mema/scripts/mema.py list [--tag <tag>]`

### 心理状态（Redis）
在 `mema:mental` 命名空间中管理键值对。
- **设置：** `python3 $WORKSPACE/skills/mema/scripts/mema.py mental set <key> <value> [--ttl N]`
- **获取：** `python3 $WORKSPACE/skills/mema/scripts/mema.py mental get <key>`

## 设置
1. 将 `env.example.txt` 复制到 `.env` 文件中。
2. 配置 `REDIS_HOST` 和 `REDIS_PORT`（默认值：localhost:6379）。
3. 初始化 SQLite 数据库模式：
   `python3 $WORKSPACE/skills/mema/scripts/mema.py init`

## 可靠性与安全性
- **数据隐私：** 所有数据都存储在本地。
- **网络安全：** 仅将 `REDIS_HOST` 指向可信的服务器。
- **路径隔离：** 数据库操作仅限于 `~/.openclaw/memory` 目录内进行。