---
name: sage-system
description: Sage系统操作：同步状态、版本信息、数据库统计数据以及系统维护相关内容。
---

# Sage系统

系统状态与维护操作

## 端点（Endpoints）

### 状态（Status）

| 端点 | 数据内容（Payload） | 描述（Description） |
|----------|------------------|-------------------------|
| `get_sync_status` | `{}` | 获取同步进度 |
| `get_version` | `{}` | 获取钱包版本 |

### 数据库（Database）

| 端点 | 数据内容（Payload） | 描述（Description） |
|----------|------------------|-------------------------|
| `get_database_stats` | `{}` | 获取数据库统计信息 |
| `perform_database_maintenance` | `{"force_vacuum": false}` | 优化数据库 |

## 同步状态响应（Sync Status Response）

```json
{
  "balance": "1000000000000",
  "unit": {"decimals": 12, "ticker": "XCH"},
  "synced_coins": 150,
  "total_coins": 150,
  "receive_address": "xch1...",
  "burn_address": "xch1...",
  "unhardened_derivation_index": 100,
  "hardened_derivation_index": 50,
  "checked_files": 25,
  "total_files": 25,
  "database_size": 52428800
}
```

## 版本响应（Version Response）

```json
{
  "version": "0.12.7"
}
```

## 数据库统计信息响应（Database Stats Response）

```json
{
  "total_pages": 10000,
  "free_pages": 500,
  "free_percentage": 5.0,
  "page_size": 4096,
  "database_size_bytes": 40960000,
  "free_space_bytes": 2048000,
  "wal_pages": 100
}
```

## 维护操作响应（Maintenance Response）

```json
{
  "vacuum_duration_ms": 1500,
  "analyze_duration_ms": 200,
  "wal_checkpoint_duration_ms": 50,
  "total_duration_ms": 1750,
  "pages_vacuumed": 250,
  "wal_pages_checkpointed": 100
}
```

## 示例（Examples）

```bash
# Check sync status
sage_rpc get_sync_status '{}'

# Get version
sage_rpc get_version '{}'

# Database stats
sage_rpc get_database_stats '{}'

# Run maintenance
sage_rpc perform_database_maintenance '{"force_vacuum": false}'

# Force full vacuum (slower)
sage_rpc perform_database_maintenance '{"force_vacuum": true}'
```

## 同步进度（Sync Progress）

- 计算同步进度：  
  ```
progress = (synced_coins / total_coins) * 100
```

- 检查是否已同步：  
  ```
synced = (synced_coins == total_coins)
```

## 注意事项（Notes）

- 定期运行维护操作以释放存储空间。
- `force_vacuum` 会执行完整的数据库压缩（速度较慢，但更彻底）。
- 如果存在大量未写入的数据页（`wal_pages`），检查点会自动清除这些数据页。