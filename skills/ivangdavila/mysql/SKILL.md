---
name: MySQL
description: 编写正确的 MySQL 查询，避免在字符集、索引和锁定方面常见的错误。
metadata: {"clawdbot":{"emoji":"🐬","requires":{"bins":["mysql"]},"os":["linux","darwin","win32"]}}
---

## 字符集相关问题

- `utf8` 字符集存在问题：它只能存储 3 个字节的数据，因此无法存储emoji符号，应始终使用 `utf8mb4` 字符集。
- 对于不区分大小写的排序，使用 `utf8mb4_unicode_ci`；对于精确的字节比较，则使用 `utf8mb4_bin`。
- 在 JOIN 操作中，如果字符集不一致，会导致性能下降。因此，请确保所有表的字符集设置一致。
- 连接字符串的字符集必须与数据库的字符集匹配。可以通过 `SET NAMES utf8mb4` 或在连接字符串中指定字符集来实现。

## 索引相关差异（与 PostgreSQL 相比）

- MySQL 不支持部分索引（partial indexes），因此无法在索引定义中使用 `WHERE active = true` 条件。
- 在 MySQL 8.0.13 之前，MySQL 不支持表达式索引，必须使用生成的列作为索引键。
- 对于 TEXT/BLOB 类型的数据，索引需要指定前缀长度（例如：`INDEX (description(100)`）。如果不指定长度，会引发错误。
- MySQL 不支持使用 `INCLUDE` 子句来包含多个列在同一个索引中。如果需要包含多个列，需要分别为它们创建索引（例如：`INDEX (a, b, c)`）。
- 外键在 InnoDB 引擎中会自动创建索引，但在使用前请确认数据库引擎是否支持该功能。

## UPSERT 操作模式

- `INSERT ... ON DUPLICATE KEY UPDATE` 并非标准的 SQL 语法，需要确保唯一键不存在才会执行更新操作。
- MySQL 使用 `LAST_INSERT_ID()` 来生成自增 ID，与 PostgreSQL 不同，MySQL 不支持 `RETURNING` 子句。
- `REPLACE INTO` 语句会先删除原有记录再插入新记录，这会导致自增 ID 的更新，并可能触发级联删除操作。
- 可以通过检查受影响的行数来判断操作结果：1 表示插入了新记录，2 表示更新了现有记录（这个逻辑可能有些反直觉）。

## 锁机制相关问题

- `SELECT ... FOR UPDATE` 语句会锁定相关行，但可能会导致意外地锁定更多行。
- InnoDB 使用“下一个键”（next-key）锁定机制，可以防止“幻影读”（phantom reads），但也可能导致死锁。
- InnoDB 的锁等待超时默认值为 50 秒，可以通过 `innodb_lock_wait_timeout` 配置进行调整。
- 从 MySQL 8.0 开始，支持 `FOR UPDATE SKIP LOCKED` 选项，其锁等待机制与 PostgreSQL 类似。

## GROUP BY 的严格性

- 在 MySQL 5.7 及更高版本中，`sql_mode` 默认包含了 `ONLY_FULL_GROUP_BY` 选项，这意味着非聚合列必须包含在 `GROUP BY` 子句中。
- 如果知道某些列的值始终相同，可以使用 `ANY_VALUE(column)` 来避免错误提示。
- 在使用旧版本的 MySQL 时，请检查 `sql_mode` 的设置，因为其行为可能有所不同。

## InnoDB 与 MyISAM 的区别

- 建议始终使用 InnoDB 引擎，因为它支持事务、行级锁定和外键功能，并且具有更好的崩溃恢复能力。
- 对于某些系统表，MySQL 仍然默认使用 MyISAM，但不要将其用于存储应用程序数据。
- 可以通过 `SHOW TABLE STATUS` 命令查看表的状态，并使用 `ALTER TABLE ... ENGINE=InnoDB` 来转换表引擎。
- 在 JOIN 操作中混合使用 InnoDB 和 MyISAM 引擎可能会导致事务保障机制失效。

## 查询相关特性

- MySQL 中的 `LIMIT offset, count` 的语法顺序与 PostgreSQL 的 `LIMIT count OFFSET offset` 不同。
- `!=` 和 `<>` 都是有效的比较运算符，但按照 SQL 标准，推荐使用 `<>`。
- 在 MySQL 中，布尔值用 `TINYINT(1)` 表示，`TRUE` 和 `FALSE` 分别对应 1 和 0。
- 当有两个参数时，建议使用 `IFNULL(a, b)` 而不是 `COALESCE`，尽管 `COALESCE` 也可以达到相同的效果。

## 连接管理

- `wait_timeout` 参数用于终止空闲连接，默认值为 8 小时，但连接池可能会忽略这个设置。
- `max_connections` 参数限制了同时连接的的最大数量，这个值通常设置得较低（默认为 151），每个连接都会占用内存资源。
- 在使用连接池时，确保所有应用程序实例的连接数不超过 `max_connections` 的限制。
- 可以使用 `SHOW PROCESSLIST` 命令查看当前活跃的连接，对于长时间运行的连接，可以使用 `KILL <id>` 来终止它们。

## 复制相关注意事项

- 基于语句的复制（statement-based replication）在处理非确定性函数（如 `UUID()`、`NOW()`）时可能会出现问题。
- 基于行的复制（row-based replication）更可靠，但会消耗更多带宽，是 MySQL 8 的默认复制方式。
- 读取复制数据的副本可能存在延迟，因此在依赖副本数据之前，请检查 `Seconds_Behind_Master` 值。
- 通常情况下，复制副本只能用于读取数据，但有时也可以用于写入操作，请确保了解其限制。

## 性能优化

- `EXPLAIN ANALYZE` 语句仅存在于 MySQL 8.0.18 及更高版本中，较低版本只能执行 `EXPLAIN` 而无法获取实际执行时间。
- MySQL 8 中移除了查询缓存机制，因此性能优化需要在应用程序层面进行。
- 对于数据碎片严重的表，可以使用 `OPTIMIZE TABLE` 命令进行优化；对于大型表，建议使用 `pt-online-schema-change` 命令进行在线表结构修改。
- 对于专用数据库服务器，建议将 `innodb_buffer_pool_size` 设置为 RAM 容量的 70-80%。