---
name: warehouse-ui
description: 通用数据库集成开发环境（IDE）命令行工具（CLI）——支持查询 PostgreSQL、MySQL、SQLite、BigQuery 和 MongoDB，并提供成本预测功能
version: 0.10.0
homepage: https://github.com/olegnazarov23/warehouse-ui
metadata: {"openclaw": {"emoji": "db", "requires": {"bins": ["warehouse-ui"]}, "primaryEnv": "DATABASE_URL", "os": ["darwin", "linux", "win32"], "install": [{"kind": "github-release", "repo": "olegnazarov23/warehouse-ui", "bins": ["warehouse-ui"], "label": "Download from GitHub Releases"}]}}
---
# 仓库 UI — 数据库查询工具

使用此工具可以连接数据库、浏览数据库架构、运行查询、估算费用，并从自然语言生成 SQL 语句。

## 安装

从 GitHub 的 Releases 页面下载：https://github.com/olegnazarov23/warehouse-ui/releases

- **macOS**：下载 DMG 文件，将其拖放到“应用程序”文件夹中，然后将其添加到系统的 PATH 环境变量中：
  `ln -s /Applications/warehouse-ui.app/Contents/MacOS/warehouse-ui /usr/local/bin/warehouse-ui`
- **Windows**：运行安装程序（EXE 文件），它会自动将工具添加到 PATH 环境变量中。

## 支持的数据库

- PostgreSQL
- MySQL
- SQLite
- BigQuery（支持费用估算）
- MongoDB

## 连接到数据库

在运行查询之前，请先建立连接：

```bash
# From a connection URL
warehouse-ui connect --url "postgres://user:pass@localhost:5432/mydb"

# With explicit parameters
warehouse-ui connect --type postgres --host localhost:5432 --database mydb --user admin --password secret

# SQLite (local file)
warehouse-ui connect --type sqlite --database /path/to/data.db

# BigQuery (service account)
warehouse-ui connect --type bigquery --database my-gcp-project --option sa_json_path=/path/to/sa.json

# MySQL
warehouse-ui connect --url "mysql://user:pass@localhost:3306/mydb"
```

## 检查连接状态

```bash
warehouse-ui status
```

## 浏览数据库架构

```bash
# List all databases
warehouse-ui schema list-databases

# List tables in a database
warehouse-ui schema list-tables --database mydb

# Describe a table (columns, types, nullability)
warehouse-ui schema describe users --database mydb
```

## 运行查询

```bash
# SQL as argument
warehouse-ui query "SELECT * FROM users LIMIT 10"

# With explicit limit
warehouse-ui query --sql "SELECT count(*) FROM orders WHERE created_at > '2024-01-01'" --limit 1000

# From a SQL file
warehouse-ui query --file path/to/report.sql
```

查询结果将以 JSON 格式输出，其中包含列信息、行数、查询耗时，以及（针对 BigQuery）处理的数据字节数和费用。

## 费用估算（预测试）

在执行查询之前先检查费用估算结果——这对 BigQuery 非常有用：

```bash
warehouse-ui dry-run "SELECT * FROM big_dataset.events WHERE date > '2024-01-01'"
```

输出内容包括：预估处理的数据字节数、预估费用（美元）、查询语句类型、引用的表以及任何警告信息。

## 基于 AI 的查询

使用配置好的 AI 服务（设置 `OPENAI_API_KEY` 或 `ANTHROPIC_API_KEY`）从自然语言生成 SQL 语句：

```bash
# Generate SQL only
warehouse-ui ai "show me the top 10 customers by total revenue"

# Generate and execute
warehouse-ui ai "find all orders from last week that were cancelled" --execute
```

## 列出已保存的连接信息

```bash
warehouse-ui connections
```

## 查询历史记录

```bash
warehouse-ui history --limit 10
warehouse-ui history --search "SELECT"
```

## 断开连接

```bash
warehouse-ui disconnect
```

## 输出格式

所有命令默认将结果以 JSON 格式输出到标准输出（stdout）。若需以人类可读的格式查看结果，可添加 `--format table` 参数。错误信息将以 JSON 格式输出到标准错误输出（stderr），并返回退出码 1。

## 环境变量

- `DATABASE_URL`：无需手动执行 `connect` 操作即可自动连接数据库（支持以下格式：postgres://、mysql://、sqlite://、mongodb://）
- `OPENAI_API_KEY`：使用 OpenAI 服务时必须设置此变量。
- `ANTHROPIC_API_KEY`：使用 Anthropic 服务时必须设置此变量。

## 提示

- 设置 `DATABASE_URL` 可以完全跳过连接步骤。
- 使用 `schema describe <table>` 命令在查询前了解表的结构。
- 对于 BigQuery，使用 `dry-run` 功能在执行复杂查询前先检查费用。
- 使用 `--limit` 参数控制大型查询的结果集大小。
- 使用 `connections` 命令查看桌面应用中已配置的数据库连接信息。