---
name: SQLite
description: 正确使用 SQLite，确保其具备适当的并发处理能力、使用正确的编译指示（pragmas），并妥善处理数据类型。
metadata: {"clawdbot":{"emoji":"🪶","requires":{"bins":["sqlite3"]},"os":["linux","darwin","win32"]}}
---

## 并发（最容易犯的错误）

- 同时只能有一个写入操作：如果有多个写入操作，将会导致队列堵塞或系统崩溃；因此不适用于高写入负载的场景。
- 启用 WAL（Write-Ahead Logging）模式：`PRAGMA journal_mode=WAL`——允许在写入过程中进行读取操作，显著提升性能。
- 设置繁忙等待超时：`PRAGMA busy_timeout=5000`——在遇到 `SQLite_BUSY` 错误时等待 5 秒后再尝试，而不是立即失败。
- WAL 模式需要 `-wal` 和 `-shm` 文件——请确保这些文件与主数据库文件一起被备份。
- 使用 `BEGIN IMMEDIATE` 语句提前获取写入锁——可以避免在读取后进行写入操作时发生死锁。

## 外键（默认是关闭的！）

- 每个连接都需要启用 `PRAGMA foreign_keys=ON`；外键约束不会被持久化到数据库中。
- 如果不启用外键约束，数据库将默默忽略外键关系，从而导致数据完整性问题。
- 在使用外键约束之前，请先检查 `PRAGMA foreign_keys` 的返回值（0 或 1）。
- `ON DELETE CASCADE` 仅在外键约束为 `ON` 的情况下才有效。

## 类型系统

- SQLite 支持类型“亲和性”，而不是严格的类型检查：例如，`INTEGER` 列可以接受 “hello” 这样的字符串而不会报错。
- `STRICT` 表格会强制类型检查，但仅支持 SQLite 3.37 及更高版本（2021 年发布）。
- SQLite 没有原生的 `DATE/TIME` 类型——可以使用 `TEXT` 表示 ISO861 格式的日期时间，或者使用 `INTEGER` 表示 Unix 时间戳。
- `BOOLEAN` 类型并不存在——实际上使用 `INTEGER` 的 0/1 来表示布尔值；`TRUE/FALSE` 只是 `INTEGER` 的别名。
- `REAL` 类型实际上是 8 字节的浮点数，与其他浮点数类型一样存在精度问题。

## 数据库模式修改

- `ALTER TABLE` 的功能非常有限：只能添加列、重命名表或列；基本上只能做这些操作。
- 在 SQLite 3.35 之前，无法修改列类型、添加约束或删除列。
- 解决方法：创建新表，复制数据，删除旧表，然后重命名表——整个过程需要在一个事务中完成。
- 使用 `ALTER TABLE ADD COLUMN` 语句时，如果列没有默认值，则不能设置 `PRIMARY KEY`、`UNIQUE` 或 `NOT NULL` 约束。

## 性能优化参数

- 在关闭长时间运行的连接之前，使用 `PRAGMA optimize` 语句更新查询规划器的统计信息。
- 使用 `PRAGMA cache_size=-64000` 设置 64MB 的缓存大小（负数表示 KB）；默认值非常小。
- 使用 `PRAGMA synchronous=NORMAL` 可以在保证安全性的同时提升性能。
- 使用 `PRAGMA temp_store=MEMORY` 可以将临时表存储在 RAM 中，从而加快排序和临时结果的生成速度。

## 数据库清理与维护

- 被删除的数据不会自动释放磁盘空间——需要使用 `VACUUM` 命令来重新写入数据库并释放空间。
- `VACUUM` 操作会暂时占用双倍的磁盘空间——请确保有足够的磁盘空间。
- 使用 `PRAGMA auto_vacuum=INCREMENTAL` 和 `PRAGMA incremental_vacuum` 可以实现部分数据清理，而无需完全重写数据库。
- 在进行大量数据删除后，务必执行 `VACUUM` 操作，否则文件会持续占用大量磁盘空间。

## 备份安全

- 在数据库文件打开期间切勿尝试复制它——如果正在写入数据，复制操作可能会导致文件损坏。
- 可以使用 `sqlite3` 中的 `.backup` 命令或 `sqlite3_backup_*` API 来备份数据库。
- 在使用 WAL 模式时，必须将 `-wal` 和 `-shm` 文件与主数据库文件一起备份。
- 使用 `VACUUM INTO 'backup.db'` 可以创建独立的备份文件（从 SQLite 3.27 版本开始支持）。

## 索引

- 覆盖索引（Covering indexes）可以提高查询效率——通过添加额外的列来避免频繁的表查找操作。
- SQLite 3.8 及更高版本支持部分索引：`CREATE INDEX ... WHERE condition`。
- 表达式索引（Expression indexes）从 SQLite 3.9 开始支持：`CREATE INDEX ON t(lower(name))`。
- `EXPLAIN QUERY PLAN` 可以显示索引的使用情况——比 PostgreSQL 的 `EXPLAIN` 更易于理解。

## 事务

- 默认情况下，每个 SQL 语句都会自动提交；这对于批量插入操作来说效率较低。
- 使用 `BEGIN; INSERT...; INSERT...; COMMIT` 可以批量插入数据，速度可以提高 10 到 100 倍。
- 使用 `BEGIN EXCLUSIVE` 可以获得独占锁，从而阻止其他连接同时进行写入操作。
- 可以通过 `SAVEPOINT name`、`RELEASE name` 和 `ROLLBACK TO name` 来创建和回滚嵌套事务。

## 常见错误

- 将 SQLite 用于需要处理大量并发用户的 Web 应用程序——单个写入操作会阻塞所有连接；建议使用 PostgreSQL。
- 假设 `ROWID` 是稳定的——实际上 `VACUUM` 操作可能会改变 `ROWID` 值；应使用显式的 `INTEGER PRIMARY KEY` 来确保数据唯一性。
- 不设置 `busy_timeout` 会导致在并发环境下随机出现 `SQLite_BUSY` 错误。
- 使用内存数据库（`':memory:'`）时，每个连接都会使用不同的数据库实例；如果需要共享数据库，请使用 `file::memory:?cache=shared`。