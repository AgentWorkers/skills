# SQL数据库精通

## 数据库架构设计

```sql
-- Users table
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  name VARCHAR(255),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_users_email ON users(email);
```

## 索引策略

| 查询模式 | 索引类型 |
|--------------|-------------|
| WHERE email = ? | 单列索引 |
| WHERE status = ? AND created > ? | 复合索引 |
| ORDER BY created_at DESC | B树索引（默认） |
| 全文搜索 | GIN索引 |

## 数据库迁移安全

```sql
-- Always add columns as nullable first
ALTER TABLE users ADD COLUMN phone VARCHAR(20);

-- Backfill data
UPDATE users SET phone = 'unknown' WHERE phone IS NULL;

-- Make not nullable
ALTER TABLE users ALTER COLUMN phone SET NOT NULL;
```

## 检查清单

- [ ] 使用UUID作为主键 |
- [ ] 添加时间戳（created_at, updated_at） |
- [ ] 为常见的查询模式创建索引 |
- [ ] 编写安全的数据库迁移脚本（包括回滚机制，优先处理可为空的字段） |
- [ ] 使用EXPLAIN ANALYZE分析查询性能 |
- [ ] 配置连接池以提高数据库访问效率 |