---
name: MySQL
slug: mysql
version: 1.0.1
description: 编写正确的 MySQL 查询，确保使用正确的字符集、索引、事务处理以及符合生产环境要求的编程模式。
metadata: {"clawdbot":{"emoji":"🐬","requires":{"bins":["mysql"]},"os":["linux","darwin","win32"]}}
---

## 快速参考

| 主题 | 文件        |
|-------|------------|
| 索引设计详解 | `indexes.md`    |
| 事务与锁定    | `transactions.md`   |
| 查询优化    | `queries.md`    |
| 生产环境配置 | `production.md`   |

## 字符集相关问题

- `utf8` 字符集存在问题：仅支持 3 个字节的数据长度，无法存储表情符号；请始终使用 `utf8mb4` 字符集。
- 使用 `utf8mb4_unicode_ci` 进行不区分大小写的排序；使用 `utf8mb4_bin` 进行精确的字节比较。
- 在 JOIN 操作中，如果字符集不匹配会导致性能下降；请确保所有表的字符集设置一致。
- 连接字符串的字符集必须与数据库的字符集设置相匹配（例如：`SET NAMES utf8mb4`）。
- 如果在 `utf8mb4` 类型的列上创建索引，可能会导致索引大小超出限制；可以考虑使用前缀索引。

## 与 PostgreSQL 的索引差异

- MySQL 不支持部分索引（partial indexes）；在索引定义中无法使用 `WHERE active = true` 条件。
- 在 MySQL 8.0.13 之前，MySQL 不支持表达式索引；必须先创建相应的生成列（generated columns）才能使用索引。
- 对于 `TEXT` 和 `BLOB` 类型的数据，需要指定前缀长度（例如：`INDEX (description(100)`）；如果不指定长度，会引发错误。
- MySQL 不支持使用 `INCLUDE` 子句来包含多个列在同一个索引中；如果需要包含多个列，请分别创建索引（例如：`INDEX (a, b, c)`）。
- 外键在 InnoDB 引擎中会自动被创建索引；在假设某个表使用外键之前，请先确认该引擎是否支持。

## UPSERT 操作模式

- `INSERT ... ON DUPLICATE KEY UPDATE` 并非标准的 SQL 语法；需要确保唯一键存在冲突才会触发更新操作。
- 使用 `LAST_INSERT_ID()` 来获取自增 ID；与 PostgreSQL 不同，MySQL 不支持 `RETURNING` 子句。
- `REPLACE INTO` 语句会先删除现有记录再插入新记录；这会导致自增 ID 的值发生变化，并可能触发级联删除操作。
- 需要检查受影响的行：1 表示记录被插入，2 表示记录被更新（这种行为可能有些反直觉）。

## 锁定相关问题

- `SELECT ... FOR UPDATE` 语句会锁定相关行；但这种锁定方式可能会导致更多的行被锁定（即所谓的“间隙锁定”）。
- InnoDB 引擎使用“下一个键锁定”（next-key locking）机制，可以防止“幻影读”（phantom reads），但也可能引发死锁（deadlocks）。
- 锁定的等待超时时间为 50 秒（默认值）；可以通过 `innodb_lock_wait_timeout` 配置进行调整。
- 从 MySQL 8.0 开始，支持 `FOR UPDATE SKIP LOCKED` 语句，这种机制可以减少锁等待时间。
- InnoDB 的默认隔离级别是 `REPEATABLE READ`，与 PostgreSQL 的 `READ COMMITTED` 不同。
- 死锁是正常现象；代码中应捕获死锁并尝试重新执行操作，而不仅仅是简单地放弃请求。

## `GROUP BY` 的严格性

- 从 MySQL 5.7 开始，`sql_mode` 默认包含了 `ONLY_FULL_GROUP_BY` 选项。
- 非聚合列必须包含在 `GROUP BY` 子句中；这与早期 MySQL 的宽松模式不同。
- 可以使用 `ANY_VALUE(column)` 来忽略重复的值，前提是你知道这些值的实际值是相同的。
- 在使用旧版本的 MySQL 时，请检查 `sql_mode` 的设置，因为其行为可能有所不同。

## InnoDB 与 MyISAM 的区别

- 始终推荐使用 InnoDB 引擎：它支持事务、行级锁定、外键以及崩溃后的数据恢复功能。
- 对于某些系统表，MySQL 仍然默认使用 MyISAM；但不要将其用于存储应用程序数据。
- 可以使用 `SHOW TABLE STATUS` 命令来检查数据库引擎类型，并使用 `ALTER TABLE ... ENGINE=InnoDB` 来转换引擎。
- 在 JOIN 操作中混合使用 InnoDB 和 MyISAM 引擎是可以的，但会失去事务的可靠性。

## 查询相关注意事项

- MySQL 中的 `LIMIT offset, count` 的语法与 PostgreSQL 的 `LIMIT count OFFSET offset` 不同。
- `!=` 和 `<>` 都可以用于比较；为了符合 SQL 标准，建议使用 `<>`。
- MySQL 不支持事务性的数据定义语言（DDL）操作；`ALTER TABLE` 语句会立即提交更改，无法回滚。
- 在 MySQL 中，布尔值用 `TINYINT(1)` 表示；`TRUE` 和 `FALSE` 分别对应 1 和 0。
- 当有两个参数时，应使用 `IFNULL(a, b)` 而不是 `COALESCE`；尽管 `COALESCE` 也可以达到相同的效果。

## 连接管理

- `wait_timeout` 配置用于终止空闲连接；默认值为 8 小时；连接池可能无法自动检测到空闲连接。
- `max_connections` 配置决定了最大连接数；每个连接都会占用内存资源，因此请根据实际需求设置合适的值。
- 在多个应用程序实例中，不要让连接数超过 `max_connections` 的限制。
- 可以使用 `SHOW PROCESSLIST` 命令查看当前活动的连接；对于长时间运行的连接，可以使用 `KILL <id>` 来终止它们。

## 复制相关注意事项

- 基于语句的复制（statement-based replication）在处理非确定性函数（如 `UUID()`、`NOW()`）时可能会出现问题。
- 基于行的复制（row-based replication）更安全，但会消耗更多的带宽；这是 MySQL 8 的默认复制方式。
- 读取复制数据的副本可能存在延迟；在依赖副本数据之前，请检查 `Seconds_Behind_Master` 值。
- 通常情况下，副本数据只能用于读取操作；但在某些情况下也可以用于写入操作，但需要先进行验证。

## 性能优化

- `EXPLAIN ANALYZE` 语句仅适用于 MySQL 8.0.18 及更高版本；在旧版本中，`EXPLAIN` 只能提供查询的执行计划，无法显示实际执行时间。
- MySQL 8 中移除了查询缓存；请在应用程序层面实现缓存机制。
- 对于数据碎片严重的表，可以使用 `OPTIMIZE TABLE` 命令进行优化；但该操作会锁定整个表；对于大型表，建议使用 `pt-online-schema-change` 工具进行优化。
- `innodb_buffer_pool_size` 配置决定了缓冲池的大小；对于专用数据库服务器，建议将其设置为 RAM 容量的 70-80%。