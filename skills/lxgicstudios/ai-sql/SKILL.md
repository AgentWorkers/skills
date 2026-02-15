---
name: sql-gen
description: 将自然语言转换为SQL查询语句
---

# SQL 生成器

只需描述您的需求，即可获得相应的 SQL 语句。该工具支持任何数据库。

## 快速入门

```bash
npx ai-sql "get all users who signed up this month and made a purchase"
```

## 功能简介

- 将自然语言描述转换为 SQL 语句
- 支持复杂的 JOIN 操作
- 自动添加正确的 WHERE 子句
- 优化查询性能

## 使用示例

```bash
# Generate query
npx ai-sql "top 10 products by revenue last quarter"

# With schema context
npx ai-sql "users without orders" --schema ./schema.sql

# Specific dialect
npx ai-sql "monthly active users" --dialect postgres
```

## 支持的数据库方言

- PostgreSQL
- MySQL
- SQLite
- SQL Server
- Oracle

## 输出示例

```sql
SELECT u.id, u.email, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at >= DATE_TRUNC('month', CURRENT_DATE)
GROUP BY u.id, u.email
HAVING COUNT(o.id) > 0;
```

## 系统要求

- Node.js 18.0 或更高版本
- 需要 OPENAI_API_KEY

## 许可证

MIT 许可证。永久免费使用。

---

**开发团队：LXGIC Studios**

- GitHub: [github.com/lxgicstudios/ai-sql](https://github.com/lxgicstudios/ai-sql)
- Twitter: [@lxgicstudios](https://x.com/lxgicstudios)