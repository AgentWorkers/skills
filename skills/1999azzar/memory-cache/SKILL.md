---
name: memory-cache
description: 使用 Redis 实现高性能的临时存储。可用于保存上下文信息、缓存昂贵的 API 返回结果，或在代理会话之间共享状态。遵循严格的键命名规范。
metadata: {"openclaw":{"requires":{"env":["REDIS_URL"]},"install":[{"id":"node","kind":"exec","command":"scripts/cache.py ping"}]}}
---
# 内存缓存

## 设置
1. 将 `.env.example` 复制到 `.env` 文件中。
2. 设置 `REDIS_URL`（例如：`redis://localhost:6379/0`）或具体的主机/端口变量。
3. 在首次运行时，`scripts/cache.py` 会创建一个虚拟环境（venv）并安装所需的依赖项。

## 核心工作流程

### 1. 关键操作
在缓存中设置、获取或删除数据。所有键都必须以 `mema:` 为前缀。
- **用法**：`bash $WORKSPACE/skills/memory-cache/scripts/cache.py set mema:<category>:<name> <value> [--ttl N]`
- **用法**：`bash $WORKSPACE/skills/memory-cache/scripts/cache.py get mema:<category>:<name>`

### 2. 搜索与扫描
使用 Redis 的 `SCAN` 命令安全地列出所有键。
- **用法**：`bash $WORKSPACE/skills/memory-cache/scripts/cache.py scan [pattern]`

## 键命名规范
**要求**：所有键都必须遵循 `mema:<category>:<name>` 的格式。
- `mema:context:*` – 用于存储短期会话状态的数据。
- `mema:cache:*` – 用于存储易变数据或 API 的返回结果。
- `mema:state:*` – 用于存储跨会话的持久化数据。

## 安全性与可靠性
- **命名空间隔离**：严格使用 `mema:` 作为前缀，以避免与其他 Redis 数据库发生冲突。
- **连接安全性**：通过环境配置优雅地处理连接重试和超时问题。