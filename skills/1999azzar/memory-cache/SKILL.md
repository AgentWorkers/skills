---
name: memory-cache
description: High-performance temporary storage system using Redis. Supports namespaced keys (mema:*), TTL management, and session context caching. Use for: (1) Saving agent state, (2) Caching API results, (3) Sharing data between sub-agents.
metadata: {"openclaw":{"requires":{"bins":["python3"],"env":["REDIS_URL"]},"install":[{"id":"pip-dependencies","kind":"exec","command":"pip install -r requirements.txt"}]}}
---

# 内存缓存

这是一个为 OpenClaw 代理设计的、基于 Redis 的标准化缓存系统。

## 先决条件
- **系统要求**：主机上必须安装 `python3`。
- **配置信息**：需要设置 `REDIS_URL` 环境变量（例如：`redis://localhost:6379/0`）。

## 设置流程
1. 将 `env.example.txt` 文件复制到 `.env` 文件中。
2. 在 `.env` 文件中配置数据库连接信息。
3. 所需依赖项列在 `requirements.txt` 文件中。

## 核心工作流程

### 1. 存储和检索数据
- **存储数据**：使用命令 `python3 $WORKSPACE/skills/memory-cache/scripts/cache_manager.py set mema:cache:<名称> <值> [--ttl 3600]`。
- **获取数据**：使用命令 `python3 $WORKSPACE/skills/memory-cache/scripts/cache_manager.py get mema:cache:<名称>`。

### 2. 数据搜索与维护
- **扫描数据**：使用命令 `python3 $WORKSPACE/skills/memory-cache/scripts/cache_manager.py scan [模式]`。
- **检查数据状态**：使用命令 `python3 $WORKSPACE/skills/memory-cache/scripts/cache_manager.py ping`。

## 键命名规范
必须严格遵循以下前缀规则：
- `mema:context:*` – 用于存储会话状态。
- `mema:cache:*` – 用于存储临时数据。
- `mema:state:*` – 用于存储持久化数据。