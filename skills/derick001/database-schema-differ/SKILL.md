---
name: database-schema-differ
description: 比较不同环境下的数据库架构，生成迁移脚本，并跟踪数据库架构的演变过程。
version: 1.0.0
author: skill-factory
metadata:
  openclaw:
    requires:
      bins:
        - python3
      python:
        - sqlalchemy
        - alembic
---
# 数据库架构差异检测工具

## 功能概述

这是一个命令行（CLI）工具，用于比较不同环境（开发、测试、生产环境）下的数据库架构，生成迁移脚本，并跟踪架构随时间的变化。支持通过 SQLAlchemy 连接 PostgreSQL、MySQL、SQLite 等数据库。

**主要功能：**
- **架构比较**：可以比较不同数据库、分支或不同时间点的架构差异。
- **迁移脚本生成**：根据架构变化自动生成 SQL 迁移脚本（用于升级或降级数据库架构）。
- **架构快照**：捕获并存储架构快照以供历史对比。
- **架构差异检测**：识别不同环境（如开发环境与生产环境）之间的架构差异。
- **支持多种数据库**：通过 SQLAlchemy 支持 PostgreSQL、MySQL、SQLite、SQL Server、Oracle 等数据库。
- **输出格式**：支持生成 SQL、JSON 或可视化差异报告。
- **易于集成**：可与 Alembic、Django 迁移工具或独立使用。
- **变更跟踪**：通过版本控制机制跟踪架构演变过程。
- **适合持续集成/持续部署（CI/CD）**：输出机器可读的格式，便于自动化流程使用。

## 使用场景

- 需要比较开发环境和生产环境之间的数据库架构。
- 需要为架构变更生成迁移脚本。
- 管理多个数据库环境并确保架构一致性。
- 需要检测生产环境中的架构差异。
- 在进行数据库重构时需要跟踪变更。
- 希望在 CI/CD 流程中自动化架构验证。
- 需要记录架构变更以供合规性检查或团队协作使用。
- 新团队成员入职时需要了解架构演变情况。
- 希望可视化不同分支或版本之间的架构差异。

## 使用方法

基本命令如下：
```bash
# Compare two database connections
python3 scripts/main.py compare postgresql://user:pass@host1/db postgresql://user:pass@host2/db

# Generate migration script from schema differences
python3 scripts/main.py diff dev_db.sql prod_db.sql --output migration.sql

# Create schema snapshot for future comparison
python3 scripts/main.py snapshot postgresql://user:pass@host/db --save snapshot.json

# Compare current schema with saved snapshot
python3 scripts/main.py compare-snapshot postgresql://user:pass@host/db snapshot.json

# Generate visual diff between schemas
python3 scripts/main.py visual-diff schema1.sql schema2.sql --html diff.html

# Check for schema drift in CI pipeline
python3 scripts/main.py check-drift --expected expected_schema.json --actual actual_schema.json

# Track schema evolution over time
python3 scripts/main.py history postgresql://user:pass@host/db --days 30
```

## 示例

### 示例 1：比较开发环境和生产环境的数据库架构

```bash
python3 scripts/main.py compare \
  postgresql://dev_user:dev_pass@localhost/dev_db \
  postgresql://prod_user:prod_pass@prod-host/prod_db \
  --output diff-report.json
```

**输出结果：**
```
🔍 Comparing schemas: dev_db (localhost) vs prod_db (prod-host)

📊 Summary:
- Tables: 42 vs 45 (3 missing in dev)
- Columns: 287 vs 295 (8 differences)
- Indexes: 67 vs 72 (5 differences)
- Constraints: 34 vs 38 (4 differences)

⚠️  Differences found (15):
1. Table `audit_logs` missing in dev
   → CREATE TABLE audit_logs (...)
   
2. Column `users.email_verified` missing in dev
   → ALTER TABLE users ADD COLUMN email_verified BOOLEAN DEFAULT FALSE
   
3. Index `idx_users_email` missing in prod
   → CREATE INDEX idx_users_email ON users(email)
   
4. Constraint `fk_orders_customer_id` differs
   → ALTER TABLE orders DROP CONSTRAINT fk_orders_customer_id_old;
   → ALTER TABLE orders ADD CONSTRAINT fk_orders_customer_id FOREIGN KEY ...

✅ Generated migration: diff-report.json
✅ SQL migration script: migration_20240306_143022.sql
```

### 示例 2：生成迁移脚本

```bash
python3 scripts/main.py diff old_schema.sql new_schema.sql --format sql --output migration.sql
```

**输出结果（migration.sql）：**
```sql
-- Generated: 2024-03-06 14:30:22
-- Database: PostgreSQL

-- UP Migration
CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    action VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);

ALTER TABLE users ADD COLUMN email_verified BOOLEAN DEFAULT FALSE;

CREATE INDEX idx_users_email ON users(email);

ALTER TABLE orders 
    DROP CONSTRAINT fk_orders_customer_id_old,
    ADD CONSTRAINT fk_orders_customer_id 
    FOREIGN KEY (customer_id) REFERENCES customers(id) 
    ON DELETE CASCADE;

-- DOWN Migration (rollback)
DROP TABLE IF EXISTS audit_logs;

ALTER TABLE users DROP COLUMN IF EXISTS email_verified;

DROP INDEX IF EXISTS idx_users_email;

ALTER TABLE orders 
    DROP CONSTRAINT fk_orders_customer_id,
    ADD CONSTRAINT fk_orders_customer_id_old 
    FOREIGN KEY (customer_id) REFERENCES customers(id);
```

### 示例 3：在 CI 流程中检测架构差异

```bash
python3 scripts/main.py check-drift \
  --expected schemas/expected/prod.json \
  --actual schemas/actual/prod.json \
  --fail-on-drift
```

**输出结果（CI 失败）：**
```
❌ Schema drift detected!

Differences:
1. Unexpected table `temp_backup` in production
2. Missing index `idx_orders_status` in production
3. Column `users.last_login` has different type (TIMESTAMP vs TIMESTAMPTZ)

Exit code: 1 (failed due to --fail-on-drift)
```

### 示例 4：跟踪架构演变

```bash
python3 scripts/main.py history postgresql://user:pass@host/db --days 90 --format timeline
```

**输出结果：**
```
📅 Schema Evolution Timeline (last 90 days)

2024-03-05: Added audit_logs table (v4.2.0 release)
2024-02-28: Added email_verified column to users table
2024-02-15: Created indexes for performance optimization  
2024-02-01: Added foreign key constraints for data integrity
2024-01-20: Initial schema snapshot (v4.0.0)

📈 Change Statistics:
- Tables: +3 (42 → 45)
- Columns: +23 (272 → 295)
- Indexes: +8 (64 → 72)
- Avg changes per week: 2.1
```

### 示例 5：可视化架构差异

```bash
python3 scripts/main.py visual-diff schema_v1.sql schema_v2.sql --html schema_diff.html
```

**输出结果：**
```
✨ Generated visual diff: schema_diff.html

Open in browser to see:
- Side-by-side schema comparison
- Color-coded differences (added/removed/changed)
- Interactive expand/collapse for tables
- Export options for documentation

Differences highlighted:
✅ 5 tables added (green)
❌ 2 tables removed (red)  
🔄 12 columns modified (yellow)
```

## 系统要求

- Python 3.x
- SQLAlchemy（用于数据库连接）
- Alembic（可选，用于生成迁移脚本）
- 数据库驱动程序：psycopg2（PostgreSQL）、pymysql（MySQL）等

**安装依赖项：**
```bash
pip3 install sqlalchemy alembic psycopg2-binary pymysql
```

## 限制

- 需要数据库凭据和网络访问权限来比较实时数据库。
- 复杂的架构变更可能需要手动审核生成的迁移脚本。
- 对 SQLAlchemy 未覆盖的数据库特定功能支持有限。
- 当数据库表数量超过 1000 张时，性能可能会受到影响。
- 不支持 NoSQL 数据库（如 MongoDB、Redis 等）。
- 无法比较加密或压缩的数据库转储文件。
- 对连接问题或权限问题的错误处理能力有限。
- 不支持跨所有数据库类型比较 Materialized Views 或数据库函数。
- 生成的迁移脚本可能无法处理数据迁移或复杂的数据转换。
- 不支持分布式数据库的比较。
- 仅比较架构结构，不优化数据或索引。
- 对于具有自定义类型或扩展的数据库，可能无法检测所有架构差异。
- 不支持跨所有数据库类型比较数据库触发器或存储过程。
- 当表数量非常多或关系复杂时，性能可能会下降。
- 不支持内置的架构版本控制系统（如 Liquibase 或 Flyway）。
- 对于格式错误的 SQL 文件或损坏的架构文件，错误处理能力有限。
- 不支持实时监控架构变化。
- 无法比较不同类型的数据库（例如 PostgreSQL 和 MySQL）。
- 对数据库特定的优化或扩展支持有限。
- 没有内置的架构差异警报通知系统。
- 生成的迁移脚本可能需要手动调整才能在生产环境中使用。

## 目录结构

该工具使用数据库连接字符串、SQL 文件或架构快照文件进行工作，无需额外的配置目录。

## 错误处理

- 如果数据库连接无效，会显示包含连接详细信息的错误信息。
- 权限错误提示检查数据库凭据和访问权限。
- 架构解析错误会显示具体出错的 SQL 语句及其所在行号。
- 比较错误提示检查数据库架构的兼容性或版本信息。
- 文件未找到错误提示检查文件路径和权限设置。
- 输出生成错误提示检查磁盘空间和写入权限。

## 贡献方式

该工具由 Skill Factory 开发。如有问题或改进建议，请通过 OpenClaw 项目进行反馈。