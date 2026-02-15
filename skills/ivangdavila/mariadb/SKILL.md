---
name: MariaDB
description: 使用适当的索引、时间表（temporal tables）和集群（clustering）来编写高效的 MariaDB 查询。
metadata: {"clawdbot":{"emoji":"🦭","requires":{"bins":["mariadb"]},"os":["linux","darwin","win32"]}}
---

## 字符集

- 对于表格和数据库连接，始终使用 `utf8mb4` 字符集——该字符集支持完整的 Unicode 字符集，包括表情符号；
- 使用 `utf8mb4_unicode_ci` 可以确保正确的语言排序；使用 `utf8mb4_bin` 可以进行字节级比较；
- 设置数据库连接的字符集：可以通过 `SET NAMES utf8mb4` 或在连接字符串中指定；
- 如果 `JOIN` 操作中的字符集不匹配，系统会强制进行转换，这可能会导致索引无法正常使用。

## 索引

- 对于 `TEXT` 和 `BLOB` 类型的列，需要指定索引前缀的长度（例如：`INDEX (description(100)`）；
- 复合索引的排序顺序很重要：`(a, b)` 可以用于 `WHERE a=?` 的查询，但不适用于 `WHERE b=?` 的查询；
- 外键会在子表上自动创建索引，但需要使用 `SHOW INDEX` 命令来确认索引的存在；
- 为了提高查询效率，应该创建覆盖所有相关列的索引，以避免频繁访问表。

## 序列

- 使用 `CREATE SEQUENCE seq_name` 可以生成跨表的唯一标识符；
- `NEXT VALUE FOR seq_name` 可以获取序列中的下一个值；即使在事务回滚后，该值仍然有效；
- 当需要在插入数据之前确定标识符的值时，使用序列比使用自动递增更合适；
- 可以使用 `SETVAL(seq_name, n)` 来重置序列的值，这对于数据迁移非常有用。

## 系统版本控制（时间序列表）

- 使用 `ALTER TABLE t ADD SYSTEM VERSIONING` 可以跟踪表的所有历史更改；
- `FOR SYSTEM_TIME AS OF '2024-01-01 00:00:00'` 可以查询表在指定时间点之前的状态；
- `FOR SYSTEM_TIME BETWEEN start AND end` 可以查询指定时间范围内的更改历史；
- 表中存在两个隐藏列 `row_start` 和 `row_end`，用于存储数据的有效期。

## JSON 处理

- `JSON_VALUE(col, '$.key')` 可以提取 JSON 字符串中的指定键对应的值，如果键不存在则返回 `NULL`；
- `JSON_QUERY(col, '$.obj')` 可以提取 JSON 对象或数组的内容，并保留原有的引号；
- `JSON_TABLE()` 可以将 JSON 数组转换为数据库表格式，便于进一步处理；
- 在插入数据之前，可以使用 `JSON_VALID()` 方法检查 JSON 数据的格式是否正确。

## Galera 集群

- 所有节点都可以写入数据，但同一行上的并发写操作可能导致数据冲突，从而引发事务回滚；
- 在执行关键读操作之前，应将 `wsrep_sync_wait` 设置为 1，以确保节点之间的数据同步；
- 应尽量减少事务的大小，因为大型事务会增加数据冲突的概率；
- `wsrep_cluster_size` 应该设置为奇数，以避免集群出现脑裂（即部分节点数据不一致的情况）。

## 窗口函数

- `ROW_NUMBER() OVER (PARTITION BY x ORDER BY y)` 可以对分组内的数据进行排名；
- `LAG(col, 1) OVER (ORDER BY date)` 可以获取当前行之前的数据值；
- `SUM(amount) OVER (ORDER BY date ROWS UNBOUNDED PRECEDING)` 可以计算指定时间范围内的累计值；
- 使用 `WITH cte AS (...)` 可以创建公共表表达式（CTE），使复杂的查询更加易于理解。

## 线程池

- 通过 `thread_handling=pool-of-threads` 启用线程池，这比为每个连接分配单独的线程更高效；
- 根据系统的 CPU 资源情况设置 `thread_pool_size`：对于 CPU 密集型任务，设置较大的值；对于 I/O 密集型任务，设置较小的值；
- 线程池可以减少并发连接时的上下文切换开销；
- 可以使用 `SHOW STATUS LIKE 'Threadpool%'` 命令来监控线程池的运行状态。

## 存储引擎

- `InnoDB` 是 MySQL 的默认存储引擎，支持 ACID 事务、行级锁定和崩溃后的数据恢复；
- `Aria` 适用于临时表，是 `MyISAM` 的安全替代方案；
- `MEMORY` 存储引擎用于缓存数据，重启时会丢失数据，但查询速度较快；
- 可以使用 `SHOW TABLE STATUS WHERE Name='table'` 命令来查看表的存储引擎信息。

## 锁定机制

- `SELECT ... FOR UPDATE` 会锁定相关行，直到事务提交；
- `LOCK TABLES t WRITE` 会锁定整个表，提供类似于 DDL 操作的独占访问权限，阻止其他会话的访问；
- 系统会自动检测死锁情况，发生死锁时事务会被回滚，需要重新执行；
- `innodb_lock_wait_timeout` 的默认值为 50 秒，对于交互式应用程序来说，可以适当降低这个值。

## 查询优化

- 使用 `EXPLAIN ANALYZE` 可以了解查询的实际执行时间（从 MySQL 10.1 版本开始支持）；
- 通过 `SET optimizer_trace='enabled=on` 可以启用查询优化器的调试功能；
- 如果查询优化器选择了错误的索引，可以使用 `FORCE INDEX (idx)` 强制使用指定的索引；
- `STRAIGHT_JOIN` 可以强制指定连接的顺序，但这是最后的解决方案。

## 备份与恢复

- `mariadb-dump --single-transaction` 可以生成不涉及锁操作的备份文件；
- `mariadb-backup` 可以生成 InnoDB 表的增量备份；
- 二进制日志（binlog）可用于精确的恢复操作：`mysqlbinlog binlog.000001 | mariadb`；
- 应定期测试恢复操作，因为无法成功恢复的备份实际上是没有用的备份。

## 常见错误

- “连接数过多”：可以增加 `max_connections` 的值或使用连接池；
- “锁等待超时”：可以使用 `SHOW ENGINE INNODB STATUS` 命令找出导致锁等待的查询；
- “行长度过大”：`TEXT` 和 `BLOB` 类型的列可能会存储在磁盘的外部页面，但行指针的长度是有限的；
- “键重复”：需要检查表的唯一性约束，并使用 `ON DUPLICATE KEY UPDATE` 语句来处理重复数据。