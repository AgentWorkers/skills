---
name: query-optimizer
description: 使用人工智能优化 SQL 和 Prisma 查询。当你的查询执行速度较慢且需要提升性能时，可以尝试这种方法。
---

# 查询优化器

查询速度过慢，导致应用程序性能下降？只需粘贴您的 SQL 语句或 Prisma 代码，即可获得优化建议。包括索引创建建议、查询重写方案以及 N+1 错误的检测结果。这些优化工作通常需要花费数小时才能手动完成。

**只需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-query-optimize "SELECT * FROM users WHERE email LIKE '%@gmail.com'"
```

## 功能介绍

- 分析 SQL 和 Prisma 查询中的性能问题
- 建议添加缺失的索引（使用 `CREATE INDEX` 语句）
- 重写查询语句，以避免常见的性能瓶颈
- 检测 ORM 代码中的 N+1 错误
- 解释优化措施为何能提升查询性能

## 使用示例

```bash
# Optimize a SQL query
npx ai-query-optimize "SELECT * FROM orders WHERE created_at > NOW() - INTERVAL '30 days'"

# Analyze a Prisma query file
npx ai-query-optimize queries.ts

# Check for N+1 issues
npx ai-query-optimize src/api/users.ts --check-n-plus-one

# Get index recommendations
npx ai-query-optimize schema.sql --suggest-indexes
```

## 最佳实践

- **提供数据库模式信息**：了解表格结构和现有索引有助于优化过程
- **进行前后性能对比**：`EXPLAIN ANALYZE` 命令能提供准确的性能数据
- **使用真实数据测试优化效果**：在少量数据上有效的优化方案可能在大量数据下失效
- **避免过早进行优化**：先修复实际存在的性能问题，而非假设性的问题

## 适用场景

- 数据库查询在 APM（应用性能监控工具）中被标记为“慢”
- 用户对应用程序的加载时间表示不满
- 继承了包含不良查询模式的代码库
- 希望学习 SQL 优化技巧并理解其背后的原理

## 作为 LXGIC 开发工具包的一部分

LXGIC Studios 开发了 110 多款免费开发者工具，这款工具便是其中之一。免费版本无需支付费用、无需注册账号，也无需使用 API 密钥。这些工具都能直接使用。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgic.dev

## 使用要求

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。运行该工具需要设置 `OPENAI_API_KEY` 环境变量。

```bash
export OPENAI_API_KEY=sk-...
npx ai-query-optimize --help
```

## 工作原理

该工具会解析您的查询语句或代码文件，以了解数据访问模式。然后运用数据库优化知识，识别诸如缺失索引、效率低下的操作（如使用通配符的 `LIKE` 操作）以及 ORM 中的常见性能问题，并提供具体的优化建议。

## 许可证

采用 MIT 许可协议，永久免费。您可以随意使用该工具。