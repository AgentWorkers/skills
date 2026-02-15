---
name: sql-check
description: 分析 SQL 查询以检测性能问题和安全漏洞
---

# SQL检查工具

只需粘贴您的SQL代码，即可获得性能优化建议和安全警告。该工具能够检测到N+1查询错误和SQL注入风险。

## 快速入门

```bash
npx ai-sql-check "SELECT * FROM users WHERE name LIKE '%john%'"
```

## 功能介绍

- 识别性能问题
- 标记SQL注入风险
- 建议添加缺失的索引
- 警告N+1查询错误

## 使用示例

```bash
# Check a query
npx ai-sql-check "SELECT * FROM orders WHERE status = 'pending'"

# Check from file
npx ai-sql-check --file ./queries/report.sql

# With schema for better analysis
npx ai-sql-check --file query.sql --schema ./schema.sql
```

## 可检测的问题

- 错误的SELECT语句（反模式）
- WHERE子句缺失
- WHERE子句中使用了未索引的列
- LIKE操作符前使用了通配符
- 使用笛卡尔连接（Cartesian joins）
- SQL注入攻击的常见模式

## 输出示例

```
⚠️ Performance Issues:
- SELECT * returns unnecessary columns
- LIKE '%john%' can't use index

🔒 Security Issues:
- None detected

💡 Suggestions:
- Add index on users(name)
- Select only needed columns
```

## 系统要求

- 必需安装Node.js 18.0及以上版本
- 需要OPENAI_API_KEY

## 许可证

采用MIT许可证，永久免费使用。

---

**开发团队：LXGIC Studios**

- GitHub仓库：[github.com/lxgicstudios/ai-sql-check](https://github.com/lxgicstudios/ai-sql-check)
- Twitter账号：[@lxgicstudios](https://x.com/lxgicstudios)