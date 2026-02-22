# 性能工程

## 瓶颈检测

```typescript
// Simple profiling
const timers = new Map<string, number>()

export function startTimer(name: string) {
  timers.set(name, Date.now())
}

export function endTimer(name: string) {
  const start = timers.get(name)
  if (!start) return
  console.log(`${name}: ${Date.now() - start}ms`)
  timers.delete(name)
}

// Usage
startTimer('db-query')
const users = await db.query('SELECT * FROM users')
endTimer('db-query')
```

## 查询优化

```sql
-- Use EXPLAIN ANALYZE
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';

-- Add indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_orders_user_id ON orders(user_id, created_at DESC);
```

## 缓存策略

| 数据类型 | 过期时间（TTL） | 缓存策略 |
|-----------|-----------|---------|
| 用户会话 | 24小时 | Redis |
| 配置信息 | 1小时 | 内存 |
| 产品目录 | 1小时 | Redis + CDN |
| API响应 | 1分钟 | 使用缓存旁路（Cache-aside） |

## 检查清单

- [ ] 分析关键路径的性能
- [ ] 优化数据库查询
- [ ] 添加适当的索引
- [ ] 实施缓存机制
- [ ] 设置负载测试
- [ ] 监控前端的核心性能指标（Core Web Vitals）