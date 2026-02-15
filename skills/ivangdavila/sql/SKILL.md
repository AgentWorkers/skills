---
name: SQL
description: 编写高效的查询语句，避免常见的性能问题以及容易被忽视的错误。
metadata: {"clawdbot":{"emoji":"🗄️","os":["linux","darwin","win32"]}}
---

# SQL 使用中的常见陷阱

## NULL 相关的问题
- 当子查询中包含 NULL 值时，`NOT IN (subquery)` 会返回空结果集——应使用 `NOT EXISTS` 代替。
- `NULL = NULL` 的结果仍然是 NULL，而不是 true——应使用 `IS NULL` 来判断。
- `COUNT(column)` 会排除 NULL 值，而 `COUNT(*)` 会计算所有行——这两种行为虽然看似相同，但实际上存在差异。
- 对 NULL 进行算术运算会得到 NULL 结果——例如 `5 + NULL` 的结果是 NULL，而不是 5。
- 在 `WHERE` 子句中使用 `COALESCE(col, 0)` 会阻止数据库使用该列的索引——需要单独处理 NULL 值。

## 影响索引性能的问题
- 对已建立索引的列使用函数会使得索引失效——例如 `WHERE YEAR(date_col) = 2024` 会扫描整个表。
- 隐式的类型转换会阻止索引被使用——例如 `WHERE varchar_col = 123` 无法利用索引加速查询。
- `LIKE '%term'` 语句无法使用索引进行查询加速——只有 `LIKE 'term%'` 才能利用索引。
- `OR` 条件可能导致查询不使用索引——在性能关键的情况下，应将其重写为 `UNION`。
- 复合索引 `(a, b)` 在仅基于 `b` 进行查询时无法提供加速效果——查询中必须包含最左边的列。

## 影响查询性能的问题
- 在子查询中使用 `SELECT *` 会强制数据库检索不必要的数据——应仅选择所需的列。
- 对大型结果集使用 `ORDER BY` 会降低查询效率——应添加 `LIMIT` 限制结果数量，或者确保索引能够覆盖排序的列。
- 使用 `DISTINCT` 通常意味着查询设计有误——应修复查询逻辑，而不是尝试去重数据。
- 相关子查询会在每一行外部查询结果上执行一次——如果可能的话，应将其重写为 `JOIN` 操作。

## 连接操作中的问题
- 当在右表上使用 `WHERE` 条件进行 `LEFT JOIN` 时，可能会导致查询使用内连接（INNER JOIN）——应将条件放在 `ON` 子句中。
- 自连接（self-join）如果没有为表指定别名，可能会导致列名冲突的错误——必须为两个表都指定别名。
- 如果连接条件缺失，可能会导致笛卡尔积（Cartesian product），从而增加数据量——这通常是编程错误，而非有意为之。
- 多个 `LEFT JOIN` 操作可能会导致数据量意外增加——在连接之前应先进行数据聚合，或者使用子查询来优化查询。

## 聚合操作中的问题
- 在 MySQL 中，选择未分组列可能会导致随机结果被选中；在其他数据库中，这种行为会引发错误。
- `HAVING` 子句在没有 `GROUP BY` 的情况下也是有效的，但容易引起混淆——它会对整个结果集进行聚合操作。
- 窗口函数（window functions）会在 `WHERE` 子句之后执行——因此无法直接对窗口函数的结果进行过滤。
- 在某些数据库中，`AVG(integer_column)` 的计算结果可能会被截断——在使用前应先将数值转换为十进制。

## 数据修改操作中的风险
- 不使用 `WHERE` 子句的 `UPDATE` 或 `DELETE` 操作会修改所有行——这种操作没有确认机制，可能会导致不可预见的后果。
- 当子查询返回空结果时，`UPDATE ... SET col = (SELECT ...)` 会将该列设置为 NULL——应使用 `COALESCE` 来避免这种情况，或者对数据进行验证。
- 通过外键进行的级联删除操作可能会删除更多数据——在批量删除之前应检查相关约束。
- `TRUNCATE` 操作在大多数数据库中不是原子性的（不可回滚）。

## 数据库间的兼容性问题
- `LIMIT` 的语法因数据库而异：MySQL 和 Postgres 使用 `LIMIT`，SQL Server 使用 `TOP`，Oracle 使用 `FETCH FIRST`。
- `ILIKE`（不区分大小写）是 Postgres 的特性——为了跨数据库兼容，应使用 `LOWER()` 函数。
- 布尔值的处理方式也有所不同：MySQL 使用 1/0 表示布尔值，Postgres 使用 true/false，而 SQL Server 没有专门的布尔类型。
- `UPSERT` 操作的语法也因数据库而异：Postgres 使用 `ON CONFLICT`，MySQL 使用 `ON DUPLICATE KEY`，SQL Server 使用 `MERGE`。
- 字符串连接的操作方式也有所不同：Postgres 和 Oracle 使用 `||`，SQL Server 使用 `+`，而其他数据库通常使用 `CONCAT()`。