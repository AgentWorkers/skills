---
name: sql-assistant
description: 这是一个全面的SQL查询辅助工具，用于数据库操作、优化和故障排除。当Codex需要编写、调试、优化或解释SQL查询时，或者需要分析数据库架构，或者需要处理与SQL相关的任务（如连接（joins）、子查询（subqueries）、聚合操作（aggregations）和性能调优（performance tuning）时，都可以使用该工具。该工具支持MySQL、PostgreSQL、SQLite等SQL方言。
---

# SQL Assistant

## 概述

该技能为 Codex 用户提供深厚的 SQL 专业知识，帮助用户完成所有与数据库相关的任务：编写高效的查询语句、调试错误、优化查询性能、解释复杂查询以及设计数据库架构。这些内容基于数据库管理员和 SQL 优化专家的最佳实践。

## 核心能力

### 1. 查询编写

根据用户需求编写清晰、高效的 SQL 查询语句：

**基本查询构建：**
```
User: "Show me all users who signed up in the last 7 days"
Codex: SELECT * FROM users WHERE created_at >= DATE('now', '-7 days');
```

**复杂查询：**
- **连接（Joins）**：内连接（Inner Join）、左连接（Left Join）、右连接（Right Join）、全外连接（Full Outer Join）
- **子查询（Subqueries）**：嵌套子查询、相关子查询（Correlated Subqueries）
- **聚合操作（Aggregations）**：GROUP BY、HAVING、窗口函数（Window Functions）
- **公共表表达式（CTEs）**：用于处理复杂逻辑
- **联合查询（Unions）**：合并多个查询的结果

**示例：多表连接查询：**
```sql
SELECT
    u.name,
    COUNT(o.id) AS order_count,
    SUM(o.total) AS total_spent
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at >= '2024-01-01'
GROUP BY u.id, u.name
HAVING COUNT(o.id) > 0
ORDER BY total_spent DESC
LIMIT 10;
```

### 2. 查询调试

识别并修复常见的 SQL 错误：

**需要修复的常见错误：**
- 语法错误（缺少逗号、括号不匹配）
- 列名/表名拼写错误
- 使用了无效的数据类型
- 缺少 FROM 子句
- GROUP BY 子句使用不当
- 字符串字面量未加引号

**调试流程：**
1. 分析错误信息
2. 找出根本原因
3. 解释错误发生的原因
4. 提供修正后的查询语句
5. 向用户解释修正方法

**示例：**
```
User: SELECT * FROM users WHERE created_at = '2024-01-01' AND status = active
Error: column "active" does not exist

Codex: The issue is that 'active' should be quoted as a string literal:

SELECT * FROM users WHERE created_at = '2024-01-01' AND status = 'active';

Without quotes, SQL treats 'active' as a column name rather than a string value.
```

### 3. 查询优化

通过索引和查询重构来提升查询性能：

**优化策略：**
- **索引（Indexing）**：在经常被查询的列上创建索引
- **查询重构（Query Rewriting）**：使用更高效的查询模式（例如使用 EXISTS 替代 IN）
- **子查询优化（Subquery Optimization）**：在合适的情况下将子查询转换为连接操作
- **限制查询结果数量（Limit Results）**：使用 LIMIT/OFFSET 或分页功能
- **选择必要的列（Select Relevant Columns）**：仅选择需要的列
- **正确的连接顺序（Proper Join Order）**：先连接较小的表

**优化前：**
```sql
SELECT * FROM orders o
WHERE user_id IN (SELECT id FROM users WHERE status = 'active');
```

**优化后：**
```sql
SELECT o.* FROM orders o
JOIN users u ON o.user_id = u.id
WHERE u.status = 'active';

-- Better performance because:
-- 1. Uses indexed join instead of subquery
-- 2. Database can optimize the join execution plan
-- 3. Potentially uses existing indexes on both tables
```

### 4. 查询解释

用简单的语言解释复杂的查询语句：

**解释模板：**
1. **查询目的（Purpose）**：查询的整体功能
2. **步骤说明（Step-by-Step）**：逐个解释查询的每个部分
3. **查询结果（Result）**：最终输出的结果是什么
4. **性能考虑（Performance Notes）**：任何相关的优化建议

**示例解释：**
```
Query: SELECT u.name, COUNT(o.id) FROM users u LEFT JOIN orders o ON u.id = o.user_id GROUP BY u.id;

Explanation:
1. FROM users u: Start with the users table (alias 'u')
2. LEFT JOIN orders o: For each user, include matching orders (or NULL if none)
3. ON u.id = o.user_id: Match records where user IDs are equal
4. GROUP BY u.id: Group results by each user
5. COUNT(o.id): Count orders for each user (NULL counts as 0 with LEFT JOIN)
6. Result: List of users with their order count, including users with 0 orders
```

### 5. 数据库架构设计

帮助设计高效的数据库架构：

**架构设计原则：**
- **规范化（Normalization）**：减少数据冗余（1NF、2NF、3NF）
- **数据类型选择（Data Types）**：使用合适的数据类型（VARCHAR、INT、DECIMAL 等）
- **主键（Primary Key）**：每个表都必须有主键
- **外键（Foreign Keys）**：确保引用完整性
- **索引（Indexes）**：在经常被查询的列上创建索引
- **命名规范（Naming Conventions）**：使用一致且具有描述性的列名

**示例数据库架构：**
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    total DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id),
    INDEX idx_status (status)
);

-- Create index on email for fast lookups
CREATE INDEX idx_users_email ON users(email);
```

## 快速入门

**场景 1：编写查询语句**
```
User: "Find the top 5 customers by total spending"
Codex: [Writes efficient query with JOIN and aggregation]
```

**场景 2：修复错误的查询**
```
User: [Posts query with error]
Codex: [Explains error and provides corrected version]
```

**场景 3：优化性能低下的查询**
```
User: "This query takes too long: [query]"
Codex: [Analyzes and provides optimized version with index recommendations]
```

## SQL 方言支持

该技能支持多种 SQL 方言：

### MySQL / MariaDB
- 使用反引号（```）作为标识符
- LIMIT 语法：LIMIT offset, count
- 字符串函数：CONCAT()、SUBSTRING() 等
- 日期函数：NOW()、DATE_ADD() 等

### PostgreSQL
- 使用双引号（""）作为标识符
- LIMIT 语法：LIMIT count OFFSET offset
- 字符串函数：|| 用于字符串连接、SUBSTR() 等
- 日期函数：NOW()、DATE_TRUNC() 等

### SQLite
- 使用双引号（""）或方括号（[]）作为标识符
- LIMIT 语法：LIMIT count OFFSET offset
- 字符串函数：|| 用于字符串连接、SUBSTR() 等
- 日期函数：date()、datetime() 等

### SQL Server (T-SQL)
- 使用双引号（""）或方括号（[]）作为标识符
- LIMIT 语法：TOP count 或 OFFSET-FETCH
- 字符串函数：+ 用于字符串连接、SUBSTRING() 等
- 日期函数：GETDATE()、DATEADD() 等

**提示：**始终询问用户使用的是哪种数据库系统，以便提供准确的语法。

## 常见查询模式

### 分页（Pagination）
```sql
-- MySQL
SELECT * FROM users LIMIT 10 OFFSET 20;

-- PostgreSQL / SQLite
SELECT * FROM users LIMIT 10 OFFSET 20;

-- SQL Server
SELECT * FROM users ORDER BY id OFFSET 20 ROWS FETCH NEXT 10 ROWS ONLY;
```

### 排名（Ranking）
```sql
-- Row numbers
SELECT name, score,
    ROW_NUMBER() OVER (ORDER BY score DESC) as rank
FROM scores;

-- Percentiles
SELECT name, score,
    PERCENT_RANK() OVER (ORDER BY score) as percentile
FROM scores;
```

### 条件聚合（Conditional Aggregation）
```sql
SELECT
    DATE(created_at) as day,
    SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed,
    SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending,
    COUNT(*) as total
FROM orders
GROUP BY DATE(created_at);
```

## 适用场景

当用户需要：
- 编写或创建 SQL 查询
- 调试 SQL 错误
- 了解 SQL 查询、数据库相关操作或查询性能优化
- 设计数据库架构
- 理解复杂查询的工作原理时，可以使用该技能。

## 最佳实践

1. **详细解释（Always Explain）**：不要只给出答案，要讲解背后的原理。
2. **优先考虑性能（Performance First）**：始终关注查询性能。
3. **使用示例（Use Examples）**：为每个概念提供具体的示例。
4. **确认数据库方言（Check Dialect）**：在编写查询前确认用户使用的数据库系统。
5. **建议创建索引（Suggest Indexes）**：为经常被查询的列创建索引。
6. **注意安全性（Security Awareness）**：提醒用户注意 SQL 注入风险，并使用参数化查询。
7. **共享前测试（Test Before Sharing）**：在正式使用前先在测试数据集上验证查询语句的正确性。

## 高级功能

### 性能分析（Performance Analysis）

分析性能低下的查询时：
- 检查 WHERE/JOIN 列上是否缺少索引
- 查找全表扫描（Full Table Scans）
- 分析查询执行计划（EXPLAIN）
- 考虑重构查询语句
- 建议创建合适的索引

**示例：EXPLAIN 分析：**
```
EXPLAIN SELECT * FROM orders WHERE user_id = 123;

-- Look for:
-- Index Scan (good) vs Sequential Scan (bad)
-- Cost estimates
-- Number of rows examined
```

### 窗口函数（Window Functions）

使用窗口函数的复杂查询：
- ROW_NUMBER()：生成唯一行号
- RANK() / DENSE_RANK()：进行排名（包括并列情况）
- LAG() / LEAD()：获取当前行之前/之后的行
- SUM() OVER()：对指定列进行求和
- FIRST_VALUE() / LAST_VALUE()：获取窗口中的第一个/最后一个值

**示例：**
```sql
SELECT
    user_id,
    created_at,
    amount,
    SUM(amount) OVER (
        PARTITION BY user_id
        ORDER BY created_at
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) as running_total
FROM orders;
```

### 数据透视表（Pivot Tables）

将数据从行转换为列：

```sql
-- Standard SQL approach
SELECT
    user_id,
    SUM(CASE WHEN month = 'Jan' THEN amount ELSE 0 END) as jan,
    SUM(CASE WHEN month = 'Feb' THEN amount ELSE 0 END) as feb,
    SUM(CASE WHEN month = 'Mar' THEN amount ELSE 0 END) as mar
FROM monthly_sales
GROUP BY user_id;
```

## 资源

### references/examples.md
包含按以下分类整理的 SQL 查询示例：
- 查询类型（SELECT、INSERT、UPDATE、DELETE）
- 复杂度（基础、中级、高级）
- 使用场景（数据分析、报表生成、事务处理）
- 数据库系统（MySQL、PostgreSQL、SQLite、SQL Server）

### references/optimization.md
包含 SQL 优化技巧：
- 索引创建策略
- 查询重构方法
- 查询执行计划分析
- 常见的性能优化问题及解决方法

### references/common-errors.md
常见 SQL 错误及其解决方法：
- 语法错误及修复方法
- 数据类型不匹配问题
- 约束条件违反
- 死锁（Deadlock）问题

## 对 Codex 的建议

- 在提供查询语句前务必验证其语法正确性。
- 如果不确定用户使用的数据库系统，请先询问用户。
- 根据需要提供简单和高级版本的查询示例。
- 在复杂的查询中添加注释以解释各部分的功能。
- 建议用户先在小型数据集上测试查询语句。
- 在执行 DELETE/DROP 操作前提醒用户备份数据库。