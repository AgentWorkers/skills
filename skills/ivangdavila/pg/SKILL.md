---
name: PostgreSQL
description: 编写高效的 PostgreSQL 查询，并设计具有适当索引和模式的数据库模式。
metadata: {"clawdbot":{"emoji":"🐘","requires":{"anyBins":["psql","pgcli"]},"os":["linux","darwin","win32"]}}
---

## 我经常忘记创建的索引

- **部分索引（Partial Indexes）**：当大多数记录处于非活动状态时，这种索引的大小可以缩小80%；建议用于状态相关的列。
- **表达式索引（Expression Indexes）**：必须与查询完全匹配；如果没有这种索引，`WHERE lower(email)` 会进行全表扫描。
- **覆盖索引（Covering Indexes）**：允许仅通过索引进行查询；可以通过 `EXPLAIN` 命令查看是否使用了覆盖索引。
- **外键列（Foreign Key Columns）**：在 PostgreSQL 中不会自动创建索引；在 JOIN 操作或 `ON DELETE CASCADE` 语句中需要索引。
- **复合索引（Composite Indexes）**：索引的创建顺序很重要；例如，`(a, b)` 对于 `WHERE a = ?` 有优化效果，但对 `WHERE b = ?` 则没有。

## 索引使用中的常见陷阱

- **未使用的索引（Unused Indexes）**：会降低 INSERT 和 UPDATE 操作的性能；可以使用 `pg_stat_user_indexes` 命令检查索引的使用情况（如果 `idx_scan` 值为 0，则表示该索引未被使用，应删除）。
- **索引过多（Too Many Indexes）**：在写入操作频繁的表上创建过多索引会降低性能；需要谨慎平衡。
- **在低基数列（Low-Cardinality Columns）** 上创建索引通常没有效果；PostgreSQL 通常会优先使用顺序扫描（seq scan）。
- **`LIKE '%suffix'` 查询**：如果列类型不是 B-tree 类型，无法使用索引加速查询；需要使用 `pg_trgm` 或 `GIN` 索引，或者使用 `reverse()` 表达式索引。

## 我经常未充分利用的查询模式

- `SELECT FOR UPDATE SKIP LOCKED`：可以在没有外部工具的情况下优化查询队列的执行效率，跳过正在处理的行。
- `pg_advisory_lock(key)`：在应用程序层面提供锁管理功能；需要显式释放锁或在连接断开时释放锁。
- `IS NOT DISTINCT FROM`：比 `(a = b OR (a IS NULL AND b IS NULL))` 更简洁且更安全。
- `DISTINCT ON (x) ORDER BY x, y`：可以快速获取每个组的第一个记录，无需子查询；这是 PostgreSQL 的特性，但非常实用。

## 连接管理（经常被忽视的设置）

- 当连接数超过50个时，使用 `PgBouncer` 是必要的；每个 PostgreSQL 连接会占用约10MB的内存；建议在事务级别管理连接池。
- 设置 `statement_timeout = '30s` 可以防止某些查询长时间占用资源导致数据库崩溃。
- `idle_in_transaction_session_timeout = '5min`：可以释放长时间未使用的、仍持有锁的事务。
- 默认的最大连接数（100）对于生产环境来说可能太低，过高则会浪费内存；应根据实际内存情况进行调整。

## 我经常误解的数据类型

- `SERIAL` 数据类型已被弃用；建议使用 `GENERATED ALWAYS AS IDENTITY` 代替。
- `TIMESTAMP` 数据类型如果不指定时区，可能会导致时间计算错误；应使用 `TIMESTAMPTZ` 并确保存储为 UTC 格式。
- 对于货币数据，应使用 `NUMERIC(12,2)` 或整数类型（例如表示分）；使用浮点数会导致计算错误（例如 0.1 + 0.2 ≠ 0.3）。
- 在 PostgreSQL 中，`VARCHAR(n)` 和 `TEXT` 在性能上没有区别；除非有特殊需求，否则建议使用 `TEXT` 类型。

## 数据清理与优化（务必关注）

- **数据膨胀（Data Bloat）**：频繁更新的数据表容易产生大量无效数据；可以使用 `pg_repack` 命令进行优化，无需锁定数据库。
- 在批量插入数据后执行 `VACUUM ANALYZE` 可以更新统计信息，帮助查询优化器做出更好的决策。
- 大型表的自动真空清理（Autovacuum）可能会延迟；可以通过调整 `autovacuum_vacuum_cost_delay` 参数来优化清理频率，或者手动执行真空操作。
- 如果事务 ID（`xid`）用完，数据库会停止工作；需要通过自动真空功能来避免这种情况，但也需要定期监控。

## 对 `EXPLAIN` 结果的误解

- 总是使用 `EXPLAIN (ANALYZE, BUFFERS)` 命令；它显示的是实际执行时间和 I/O 操作情况，仅基于估计的结果可能会产生误导。
- 如果查询中出现了 “Heap Fetches: 1000” 的提示，说明缺少相关索引；需要为相关列添加 `INCLUDE` 到索引中。
- 对于某些表，顺序扫描（seq scan）可能比使用索引更快；需要根据实际情况判断是否适合使用顺序扫描。
- `Rows` 的估计值可能不准确；可以通过执行 `ANALYZE` 命令或检查统计信息来修正估计值。

## 全文搜索（Full-Text Search）的常见错误

- 应提前计算用户输入的文本数据，并将其存储为带有 `GIN` 索引的 `tsvector` 类型。
- 使用 `plainto_tsquery` 可以正确处理包含空格的输入，而 `to_tsquery` 则会出错。
- 使用 `english` 作为语言参数时，查询会匹配以 “english” 开头的所有单词；如果需要精确匹配，则应使用 `simple` 选项。
- 全文搜索是基于单词的；对于子字符串匹配，仍然需要使用 `LIKE '%exact phrase%'`。

## 事务隔离级别（Transaction Isolation Levels）

- 默认的 `READ COMMITTED` 级别可能会导致幻影读取（phantom reads）；为了数据一致性，建议使用 `REPEATABLE READ` 级别。
- `SERIALIZABLE` 级别可以避免数据冲突，但需要处理 `40001` 错误，并通过重试机制来恢复。
- 长时间运行的事务会阻塞真空清理操作并持有锁；应尽量将事务持续时间控制在几秒以内。