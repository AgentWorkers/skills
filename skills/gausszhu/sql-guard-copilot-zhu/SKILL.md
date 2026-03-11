---
name: sql-query-copilot
description: 简化 MySQL、PostgreSQL 和 SQLite 的 SQL 查询及故障排除流程。适用于用户需要查看数据库架构、将自然语言转换为 SQL 语句、调试 SQL 错误、运行查询执行计划（explain plan）、检查存在风险的 SQL 代码，或通过安全的只读方式验证数据的情况。
---
# SQL 查询助手（SQL Query Copilot）

## 概述

使用此工具可将自然语言请求转换为可执行的 SQL 语句，确保工作流程具有可预测性且风险较低。系统默认以只读模式执行查询，并在运行前根据数据库模式验证每个查询语句的合法性。

## 快速入门

首先设置 `SQL_DSN`（或每次执行时通过 `--dsn` 参数传递该值）。

```bash
# PowerShell
$env:SQL_DSN="mysql://user:password@127.0.0.1:3306/stock_monitor"
$env:SQL_DSN="postgres://user:password@127.0.0.1:5432/stock_monitor"
$env:SQL_DSN="sqlite:///d:/data/demo.db"

# Windows CMD
set SQL_DSN=mysql://user:password@127.0.0.1:3306/stock_monitor
set SQL_DSN=postgres://user:password@127.0.0.1:5432/stock_monitor
set SQL_DSN=sqlite:///d:/data/demo.db

# Bash / Zsh
export SQL_DSN="mysql://user:password@127.0.0.1:3306/stock_monitor"
export SQL_DSN="postgres://user:password@127.0.0.1:5432/stock_monitor"
export SQL_DSN="sqlite:///d:/data/demo.db"
```

**核心命令：**

```bash
python scripts/sql_easy.py tables
python scripts/sql_easy.py describe daily_kline
python scripts/sql_easy.py lint --sql "SELECT * FROM daily_kline"
python scripts/sql_easy.py explain --sql "SELECT code, close FROM daily_kline WHERE trade_date >= '2026-01-01'"
python scripts/sql_easy.py query --sql "SELECT code, close FROM daily_kline ORDER BY trade_date DESC" --limit 50
python scripts/sql_easy.py query --sql "SELECT code, close FROM daily_kline" --summary
python scripts/sql_easy.py ask --q "show symbols with old sell signals older than 20 days" --summary
python scripts/sql_easy.py profile
```

请设置 `OPENAI_API_KEY`（或通过 `--api-key` 参数传递），以便使用 `ask` 功能。

## v0.2 的主要功能：

- **多数据库引擎支持**：支持 MySQL、PostgreSQL 和 SQLite。
- **SQL 代码检查功能**：在执行前能检测出高风险代码模式。
- **查询计划解释功能**：可快速查看查询的执行计划（使用 `EXPLAIN` 或 `EXPLAIN QUERY PLAN`）。
- **自然语言交互模式**：用户可以通过自然语言描述需求，系统会自动生成相应的 SQL 语句。
- **查询结果汇总**：会自动统计返回列的统计信息（如空值比例、唯一值数量、最小值/最大值/平均值）。
- **慢速查询提示**：通过 `--slow-ms` 参数可标记执行时间较长的查询。
- **审计日志功能**：可通过 `--audit-log` 或 `SQL_EASY_AUDIT_LOG` 将命令元数据写入 JSONL 格式文件。

## 工作流程：

1. 明确查询需求：在编写 SQL 语句之前，需要确定查询的时间范围、数据维度以及所需的输出列。
2. 首先了解数据库结构：在执行复杂查询之前，先运行 `tables`、`describe <table>` 和 `profile` 命令来查看数据库表结构。
3. 以只读模式草拟 SQL 语句：使用 `SELECT` 或 `WITH` 语句来构建查询，并明确指定所需的列以及时间过滤条件。
4. 在安全机制的保护下执行查询：通过 `scripts/sql_easy.py query` 命令执行查询，除非需要完整导出数据，否则请使用 `--limit` 选项限制查询结果的数量。
5. 验证查询结果：检查返回数据的行数、空值比例以及异常值情况；根据需要调整查询语句后重新执行。

## 安全机制：

- 系统默认以只读模式执行 SQL 语句，禁止执行破坏性操作（如 `INSERT`、`UPDATE`、`DELETE`、`DROP`、`ALTER`、`TRUNCATE` 等）。
- 对于生产环境或报告用途的查询，建议明确指定需要查询的列，而非使用 `SELECT *`。
- 在执行复杂查询或计划性查询之前，先运行代码检查（`lint`）。
- 当表名或列名不确定时，务必为这些标识符加上引号。
- 对于业务决策，需同时提供 SQL 语句以及返回数据的简要解释。

## 常用查询模式：

在创建相关查询时，请参考 `references/query_patterns.md` 文件中的示例：
- 获取排名前 N 条记录的查询
- 按时间窗口进行数据聚合
- 使用窗口函数去除重复数据
- 进行条件统计（例如计算符合特定条件的数据数量）
- 进行数据质量检查（如检测空值、重复值或异常值）

如需使用 Chanquant 的特定查询模板，请参考 `references/chanquant_templates.md` 文件。