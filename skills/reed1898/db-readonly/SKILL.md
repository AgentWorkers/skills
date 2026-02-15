---
name: db-readonly
description: 可以安全地执行只读查询，以用于 MySQL 或 PostgreSQL 数据库中的数据检查、报告生成和故障排除。当用户需要读取表格内容、检查数据库架构、统计行数、抽取数据样本或导出查询结果（且不修改数据）时，可以使用此功能。
---

# db-readonly

此技能仅用于数据库的读取操作。

## 功能说明

- 使用连接环境变量（connection env vars）连接到 **PostgreSQL** 或 **MySQL** 数据库。
- 仅执行 **SELECT**、**WITH** 和 **EXPLAIN** 类型的查询。
- 可选地将查询结果保存为 CSV、TSV 或 JSON 格式。
- 禁止执行具有风险的操作（如 `INSERT`、`UPDATE`、`DELETE`、`DROP`、`ALTER` 等）。

## 连接环境变量

### PostgreSQL

- `PGHOST`
- `PGPORT`（可选，默认值 5432）
- `PGDATABASE`
- `PGUSER`
- `PGPASSWORD`

### MySQL

- `MYSQL_HOST`
- `MYSQL_PORT`（可选，默认值 3306）
- `MYSQL DATABASE`
- `MYSQL_USER`
- `MYSQL_PASSWORD`

## 使用方法

运行以下脚本：

- `scripts/db_readonly.sh postgres "SELECT now();"`
- `scripts/db_readonly.sh mysql "SELECT NOW();"`

**导出示例**：

- `scripts/db_readonly.sh postgres "SELECT * FROM users LIMIT 100" --format csv --out /tmp/users.csv`

## 安全规则

1. 拒绝执行任何非读取操作的 SQL 语句。
2. 在进行探索性查询时，建议使用 `LIMIT` 限制查询结果的数量。
3. 当用户请求执行更新、删除或修改数据库结构的操作时，必须获得明确确认后才能使用此技能。
4. 避免输出环境变量中包含的敏感信息。

## 参考资料

- 查询操作指南：`references/query-cookbook.md`