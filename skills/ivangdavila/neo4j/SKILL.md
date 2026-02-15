---
name: Neo4j
description: 编写具有适当模式的 Cypher 查询，以实现数据合并、遍历和优化性能的功能。
metadata: {"clawdbot":{"emoji":"🕸️","requires":{"anyBins":["cypher-shell","neo4j"]},"os":["linux","darwin","win32"]}}
---

## 合并陷阱（Merge Traps）

- `MERGE` 操作会匹配完整的模式，例如 `MERGE (a)-[:KNOWS]->(b)`；如果相关关系缺失，则会创建重复的节点。
- 安全的插入操作（upsert）：先分别插入节点，再合并它们之间的关系。
- 对于具有条件属性的情况，需要使用 `ON CREATE SET` 和 `ON MATCH SET` —— 如果不使用这些选项，匹配操作将不会更新任何数据。
- 对于简单的节点插入操作，可以使用 `MERGE (n:User {id: $id})`，其中 `id` 需要满足唯一性约束。

## 索引（Indexes）

- 如果某个属性没有索引，则系统会扫描所有标签来查找匹配的节点，这会导致性能下降。因此，应始终为在 `WHERE` 子句中使用的属性创建索引。
- 当存在唯一性约束时，系统会自动为该属性创建索引；在可能的情况下，优先使用唯一性约束而非普通的索引。
- 在正式生产环境使用之前，可以使用 `EXPLAIN` 命令检查查询计划，确保没有“NodeByLabelScan”操作（这通常意味着查询没有利用索引进行优化）。
- 对于文本搜索，需要为 `n.title` 和 `n.body` 创建全文索引：`CREATE FULLTEXT INDEX FOR (n:Post) ON EACH [n.title, n.body]`。

## 变长路径（Variable-Length Paths）

- 在连接的图中，使用通配符 `[*]` 可能会导致查询结果数量无限增长；因此应始终为其设置上限，例如 `[*1..5]`。
- `[*0..]` 包括起始节点，但这通常不是预期的行为，建议使用 `[*1..]`。
- `shortestPath()` 只返回最短的一条路径；如果需要获取所有长度相同的路径，应使用 `allShortestPaths()`。
- 在路径内部进行过滤操作会降低查询效率：例如 `[r:KNOWS* WHERE r.active]` 先进行扫描再过滤，这种情况下可能需要考虑数据模型的优化。

## 笛卡尔积（Cartesian Product）

- 当两个查询模式不相关时，执行它们会导致大量的结果行（即笛卡尔积）。为了避免这种情况，可以使用 `WITH` 语句将它们连接起来。
- 如果两个模式中包含相同的变量，系统会隐式地执行连接操作，而不会生成笛卡尔积。
- 当查询计划中包含 `CartesianProduct` 操作符时，可以使用 `PROFILE` 命令来查看具体的执行情况。

## `WITH` 作用域的更新（WITH Scope Updates）

- 只有在 `WITH` 语句中声明的变量才能在后续的查询中继续使用；例如 `MATCH (a)--(b) WITH a` 中的 `a` 变量在后续查询中将不可用。
- 聚合操作会影响到 `WITH` 语句中的变量：例如 `MATCH (u:User) WITH u.country AS c, count(*) AS n`。
- 常见的错误是在聚合操作后再次使用 `WITH` 语句进行过滤，这会导致重复计算。
- 分页操作：`WITH n ORDER BY n.created SKIP 10 LIMIT 10` 可用于分页查询。

## NULL 值的传播（NULL Value Propagation）

- `OPTIONAL MATCH` 语句对于缺失的模式会返回 `NULL` 值；`NULL` 值会在表达式中被传递并继续被使用。
- `WHERE` 子句可以在 `OPTIONAL MATCH` 之后过滤掉 `NULL` 值；可以使用 `COALESCE()` 函数来保留非 `NULL` 的值。
- `count(NULL)` 的结果总是 0；例如 `OPTIONAL MATCH (u)-[:REVIEWED]->(p) RETURN count(p)` 可以用来统计被查看过的记录数量。
- 如果尝试访问 `NULL` 值的属性，系统不会报错，但会返回 `NULL`，这可能导致数据丢失。

## 查询方向（Query Direction）

- 如果查询语句中没有使用箭头符号 `->`，则查询的方向是双向的（即 `a)-[:KNOWS]-(b)` 既可以从 `a` 查找 `b`，也可以从 `b` 查找 `a`。
- 创建关系时需要指定方向；无法创建无向的关系。
- 如果方向指定错误，查询结果将为空；例如，如果关系是 `(a)-[:OWNS]->(b)`，那么查询 `(b)-[:OWNS]->(a)` 将返回空结果。

## 批量操作（Batch Operations）

- 大量的数据插入操作可能会导致内存不足；可以使用 `CALL {} IN TRANSACTIONS OF 1000 ROWS` 来分批执行。
- 对于批量插入操作，可以使用 `UNWIND $list AS item CREATE (n:Node {id: item.id})` 来构建节点对象。
- `apoc.periodic.iterate()` 可用于处理复杂的批量逻辑，并提供查询进度。
- 删除操作也可以分批进行：例如 `MATCH (n:Old) WITH n LIMIT 10000 DETACH DELETE n`。

## 参数注入（Parameter Injection）

- 应始终使用参数 `$param` 而不是字符串拼接来传递值，这样可以防止 Cypher 注入攻击。
- 使用参数还可以缓存查询计划；如果使用字面值，每次查询时都需要重新编译查询计划。
- 参数可以通过映射传递，例如在驱动程序中使用 `{param: value}`，在浏览器中使用 `:param {param: value}`。
- 对于 `IN` 操作，可以使用列表参数，例如 `WHERE n.id IN $ids`。