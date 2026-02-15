---
name: duckdb-en
description: DuckDB CLI 是一个专门用于 SQL 分析、数据处理和文件转换的工具。它可以执行 SQL 查询、CSV/Parquet/JSON 文件的解析与处理，以及数据库操作。相关的命令包括：`duckdb`、`sql`、`query`、`data analysis`、`parquet` 和 `convert data`。
---

# DuckDB CLI 专业指南

DuckDB CLI 提供了数据分析、SQL 查询以及文件转换的功能。

## 快速入门

### 直接使用 SQL 读取数据文件
```bash
# CSV
duckdb -c "SELECT * FROM 'data.csv' LIMIT 10"

# Parquet
duckdb -c "SELECT * FROM 'data.parquet'"

# Multiple files with glob
duckdb -c "SELECT * FROM read_parquet('logs/*.parquet')"

# JSON
duckdb -c "SELECT * FROM read_json_auto('data.json')"
```

### 打开持久化数据库
```bash
# Create/open database
duckdb my_database.duckdb

# Read-only mode
duckdb -readonly existing.duckdb
```

## 命令行参数

### 输出格式（以标志形式表示）
| 标志 | 格式 |
|------|--------|
| `-csv` | 逗号分隔 |
| `-json` | JSON 数组 |
| `-table` | ASCII 表格 |
| `-markdown` | Markdown 表格 |
| `-html` | HTML 表格 |
| `-line` | 每行一个值 |

### 执行参数
| 参数 | 描述 |
|----------|-------------|
| `-c COMMAND` | 运行 SQL 语句后退出 |
| `-f FILENAME` | 从文件中运行脚本 |
| `-init FILE` | 使用替代配置文件（`.duckdbrc`） |
| `-readonly` | 以只读模式打开数据库 |
| `-echo` | 在执行前显示命令 |
| `-bail` | 遇到错误时立即停止 |
| `-header` / `-noheader` | 显示/隐藏列标题 |
| `-nullvalue TEXT` | NULL 值的显示文本 |
| `-separator SEP` | 列分隔符 |

## 数据转换

### 将 CSV 转换为 Parquet
```bash
duckdb -c "COPY (SELECT * FROM 'input.csv') TO 'output.parquet' (FORMAT PARQUET)"
```

### 将 Parquet 转换为 CSV
```bash
duckdb -c "COPY (SELECT * FROM 'input.parquet') TO 'output.csv' (HEADER, DELIMITER ',')"
```

### 将 JSON 转换为 Parquet
```bash
duckdb -c "COPY (SELECT * FROM read_json_auto('input.json')) TO 'output.parquet' (FORMAT PARQUET)"
```

### 带过滤条件的转换
```bash
duckdb -c "COPY (SELECT * FROM 'data.csv' WHERE amount > 1000) TO 'filtered.parquet' (FORMAT PARQUET)"
```

## 常用命令

### 检查数据库模式
| 命令 | 描述 |
|---------|-------------|
| `.tables [pattern]` | 显示符合指定模式的表 |
| `.schema [table]` | 显示表的创建语句 |
| `.databases` | 显示所有连接的数据库 |

### 输出控制
| 命令 | 描述 |
|---------|-------------|
| `.mode FORMAT` | 更改输出格式 |
| `.output file` | 将输出结果保存到文件 |
| `.once file` | 将后续输出结果保存到同一文件 |
| `.headers on/off` | 显示/隐藏列标题 |
| `.separator COL ROW` | 设置列分隔符和行分隔符 |

### 查询
| 命令 | 描述 |
|---------|-------------|
| `.timer on/off` | 显示执行时间 |
| `.echo on/off` | 在执行前显示命令 |
| `.bail on/off` | 遇到错误时立即停止 |
| `.read file.sql` | 从文件中运行 SQL 语句 |

### 编辑
| 命令 | 描述 |
|---------|-------------|
| `.edit` 或 `\e` | 在外部编辑器中打开查询内容 |
| `.help [pattern]` | 显示帮助信息 |

## 可用的输出格式（共 18 种）

### 数据导出格式
- **csv** - 逗号分隔，适用于电子表格 |
- **tabs** - 制表符分隔 |
- **json** - JSON 数组 |
- **jsonlines** - 每行一个 JSON 值（流式格式）

### 可读性强的输出格式
- **duckbox**（默认） - 带有 Unicode 标签的美观 ASCII 格式 |
- **table** - 简单的 ASCII 表格 |
- **markdown** - 适用于文档编写 |
- **html** - HTML 表格格式 |
- **latex** - 适用于学术论文

### 特殊功能
- **insert TABLE** - 执行 SQL 插入操作 |
- **column** - 设置列宽 |
- **line** - 每行一个值 |
- **list** - 以管道符分隔的列表 |
- **trash** - 删除所有输出结果

## 键盘快捷键（macOS/Linux）

### 导航
| 快捷键 | 功能 |
|----------|--------|
| `Home` / `End` | 移动到行首/行尾 |
| `Ctrl+Left/Right` | 跳转到单词的开始/结束位置 |
| `Ctrl+A` / `Ctrl+E` | 移动到缓冲区的开始/结束位置 |

### 命令历史记录
| 快捷键 | 功能 |
|----------|--------|
| `Ctrl+P` / `Ctrl+N` | 查看上一次/下一次执行的命令 |
| `Ctrl+R` | 查找命令历史记录 |
| `Alt+<` / `Alt+>` | 查看历史记录中的第一个/最后一个命令 |

### 编辑功能
| 快捷键 | 功能 |
|----------|--------|
| `Ctrl+W` | 向后删除一个单词 |
| `Alt+D` | 向前删除一个单词 |
| `Alt+U` / `Alt+L` | 将单词转换为大写/小写 |
| `Ctrl+K` | 删除到行尾 |

### 自动完成功能
通过 `Tab` 键激活自动完成功能：
- **关键词** - 自动完成 SQL 命令 |
- **表名** - 自动完成数据库对象名称 |
- **列名** - 自动完成字段和函数名称 |
- **文件名** - 自动完成文件路径

## 数据库操作

### 从文件创建表格
```sql
CREATE TABLE sales AS SELECT * FROM 'sales_2024.csv';
```

### 插入数据
```sql
INSERT INTO sales SELECT * FROM 'sales_2025.csv';
```

### 导出表格
```sql
COPY sales TO 'backup.parquet' (FORMAT PARQUET);
```

## 分析示例

### 快速统计
```sql
SELECT
    COUNT(*) as count,
    AVG(amount) as average,
    SUM(amount) as total
FROM 'transactions.csv';
```

### 数据分组
```sql
SELECT
    category,
    COUNT(*) as count,
    SUM(amount) as total
FROM 'data.csv'
GROUP BY category
ORDER BY total DESC;
```

### 在多个文件之间进行连接操作
```sql
SELECT a.*, b.name
FROM 'orders.csv' a
JOIN 'customers.parquet' b ON a.customer_id = b.id;
```

### 描述数据结构
```sql
DESCRIBE SELECT * FROM 'data.csv';
```

## 使用管道和标准输入（stdin）

```bash
# Read from stdin
cat data.csv | duckdb -c "SELECT * FROM read_csv('/dev/stdin')"

# Pipe to another command
duckdb -csv -c "SELECT * FROM 'data.parquet'" | head -20

# Write to stdout
duckdb -c "COPY (SELECT * FROM 'data.csv') TO '/dev/stdout' (FORMAT CSV)"
```

## 配置设置

将常用配置保存在 `~/.duckdbrc` 文件中：
```sql
.timer on
.mode duckbox
.maxrows 50
.highlight on
```

### 语法高亮显示颜色设置
```sql
.keyword green
.constant yellow
.comment brightblack
.error red
```

## 外部编辑器

您可以在外部编辑器中打开复杂的 SQL 查询：
```sql
.edit
```

可选编辑器包括：`DUCKDB_EDITOR`、`EDITOR`、`VISUAL` 或 `vi`。

## 安全模式

启用安全模式后，会限制对文件的访问：
- 禁止访问外部文件 |
- 关闭 `.read`、`.output`、`.import` 等相关功能 |
- 在同一会话中无法关闭安全模式

## 使用技巧

- 对于大型文件，使用 `LIMIT` 语句可快速预览数据 |
- 对于重复查询，Parquet 格式比 CSV 更高效 |
- `read_csv_auto` 和 `read_json_auto` 会自动推断列类型 |
- 命令参数按顺序处理（类似于 SQLite CLI 的处理方式） |
- 在某些 Ubuntu 版本中，WSL2 可能会显示错误的 `memory_limit` 值