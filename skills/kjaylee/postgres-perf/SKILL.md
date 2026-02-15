---
name: postgres-perf
description: PostgreSQL性能优化及最佳实践：在编写SQL查询、设计数据库架构、实现索引或调试数据库性能时参考这些内容。涵盖查询优化、连接管理、数据库架构设计以及规则基安全性（Rule-Based Security, RLS）等相关内容。
metadata:
  author: misskim
  version: "1.0"
  origin: Concept from Supabase postgres-best-practices, distilled for our use
---

# PostgreSQL 性能优化指南

在编写数据库查询和数据库模式时，以下是一些性能优化的建议。

## 按优先级划分的关键规则

### 🔴 关键性：查询性能

```sql
-- ❌ 인덱스 없는 WHERE
SELECT * FROM orders WHERE customer_email = 'user@example.com';

-- ✅ 인덱스 생성
CREATE INDEX idx_orders_email ON orders(customer_email);
```

- **养成使用 `EXPLAIN ANALYZE` 的习惯** —— 始终检查查询的执行计划。
- 如果在大型表上出现顺序扫描（Seq Scan），则需要创建索引。
- 禁止使用 `SELECT *` —— 应仅选择所需的列。
- 对于复杂的查询（N+1 查询），应考虑使用 JOIN 或批量查询来替代。

### 🔴 关键性：连接管理

- 使用连接池（禁止直接建立连接）。
- 在 Supabase 环境中，建议使用 `pgBouncer` 并设置为事务模式（transaction mode）。
- 在服务器less 环境中，连接池是必不可少的。
- 定期清理闲置的连接。

### 🟡 高度重要：数据库模式设计

```sql
-- ❌ 무분별한 인덱스
CREATE INDEX idx_everything ON orders(a, b, c, d, e);

-- ✅ 부분 인덱스 (자주 쓰는 조건)
CREATE INDEX idx_active_orders ON orders(created_at)
WHERE status = 'active';
```

- 在规范化（Normalization）与非规范化（Denormalization）之间做出选择 —— 根据读取模式来决定。
- 在分布式环境中，UUID 更适合使用，但会导致索引体积增大。
- 对于无法结构化的数据，如果需要查询，可以考虑将其存储为 JSONB 类型。

### 🟢 中等重要性：并发与锁定

- 对于大量的 UPDATE/DELETE 操作，应采用批量处理的方式。
- 使用 `SELECT ... FOR UPDATE` 语句，仅锁定所需的行。
- 尽量减少事务的使用，并保持事务的时长尽可能短。
- 防止死锁（Deadlock）的发生，确保锁定的顺序一致。

### 🔵 重要性较低：行级安全性（Row Level Security, RLS）

```sql
-- 보안 정책 예시
CREATE POLICY user_data ON user_profiles
  FOR SELECT USING (auth.uid() = user_id);
```

- RLS 策略的制定应与索引设计相结合（这会对性能产生显著影响！）
- 尽量减少对 `auth.uid()` 的调用。
- 对于复杂的 RLS 策略，应通过 `EXPLAIN` 来评估其对性能的影响。

## 实际开发中的建议

- **开发阶段：** 使用 `EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)` 来分析查询性能。
- **生产环境：** 启用慢查询日志功能。
- **数据迁移时：** 对大型表进行修改时，应采用异步操作。
- **备份：** 可以自动化使用 `pg_dump` 将数据库备份到 NAS 中。