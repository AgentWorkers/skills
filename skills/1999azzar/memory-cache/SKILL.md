---
name: memory-cache
description: 使用 Redis 实现高性能的临时存储。可用于保存上下文信息、缓存耗时的 API 返回结果，或在代理会话之间共享状态。遵循严格的键命名规范。
---

# 内存缓存

## 设置
1. 将 `.env.example` 复制到 `.env`。
2. 设置 `REDIS_URL`（例如 `redis://localhost:6379/0`）或 `REDIS_HOST`、`REDIS_PORT`、`REDIS_DB`、`REDIS_PASSWORD`。
3. 确保 Redis 正在运行。可选的超时设置：`REDIS SOCKET_TIMEOUT`、`REDIS SOCKET_CONNECT_TIMEOUT`。
4. 在首次运行时，`scripts/cache` 会创建一个虚拟环境（venv）并安装所需依赖项。

## 使用方法
- **功能**：内存管理器。
- **触发条件**：“稍后保存这些数据”、“缓存这些结果”、“上次搜索的内容是什么？”。
- **输出**：存储或检索到的值的确认信息。

## 命令（命令行接口 CLI）
推荐使用 `scripts/cache`，或者直接运行 `python3 scripts/cache_manager.py`。

| 命令 | 描述 |
|---------|-------------|
| `set <key> <value> [--ttl N] [--json]` | 设置键值对；可选设置过期时间（秒）并使用 JSON 格式编码 |
| `get <key> [--json]` | 获取键值对；可选使用 JSON 解码并以美观的格式显示结果 |
| `del <key>` | 删除键 |
| `exists <key>` | 如果键存在则返回 1，否则返回 0 |
| `ttl <key>` | 获取键的过期时间（以秒为单位）；-1 表示无过期时间，-2 表示键不存在 |
| `expire <key> <seconds>` | 为现有键设置过期时间 |
| `scan [pattern] [--count N]` | 根据模式列出所有键（安全操作，适用于生产环境） |
| `keys [pattern]` | `scan` 的别名 |
| `ping` | 检查与 Redis 的连接状态 |

所有键的命名格式必须遵循 `mema:<category>:<name>`。无效的键会导致程序退出，并返回错误代码 2。

## 键命名规范
**必须** 使用 `mema:<category>:<name>` 的命名结构。类别包括：`context`（上下文）、`cache`（缓存）、`state`（状态）、`queue`（队列）。命名规则：可以使用字母、数字、`_`、`:`、`.`、`-`。

- `mema:context:*` – 会话上下文（过期时间：24 小时）。
- `mema:cache:*` – API 数据缓存（过期时间：7 天）。
- `mema:state:*` – 应用程序的持久化状态数据。
- `mema:queue:*` – 任务队列（用于存储列表或流式数据）。

详细规范请参阅 [键命名标准](references/key-standards.md)。

## 示例

```bash
# Cache a search result for 1 hour
./scripts/cache set mema:cache:search:123 "search result json" --ttl 3600

# Store and retrieve JSON
./scripts/cache set mema:cache:config '{"theme":"dark"}' --ttl 86400 --json
./scripts/cache get mema:cache:config --json

# Retrieve context
./scripts/cache get mema:context:summary

# List keys (SCAN; safe on large datasets)
./scripts/cache scan mema:cache:*
./scripts/cache keys

# Check connection
./scripts/cache ping
```

## 错误代码
- 0：操作成功
- 1：Redis/缓存系统出现错误
- 2：键名验证失败