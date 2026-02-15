---
name: sql-writer
description: 将自然语言转换为SQL查询。当你需要快速编写SQL语句时，可以使用这个功能。
---

# SQL Writer

没有人能记住所有的SQL语法。你知道自己需要什么数据，但可能记不清应该使用`LEFT JOIN`还是`INNER JOIN`，也不确定`WHERE`子句应该放在`GROUP BY`之前。这个工具可以将你用自然语言描述的需求转换成精确的SQL查询语句。

**只需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-sql "get all users who signed up this month"
```

## 功能介绍

- 将自然语言描述转换为可执行的SQL查询语句
- 支持多种SQL方言，包括PostgreSQL、MySQL和SQLite
- 通过提供表结构信息来生成更准确的查询结果
- 生成格式规范、可直接运行的SQL代码

## 使用示例

```bash
# Simple query
npx ai-sql "get all users who signed up this month"

# Specify dialect
npx ai-sql "top 10 products by revenue" -d MySQL

# With schema context
npx ai-sql "users who ordered in the last 90 days" -s "users(id,name,email) orders(id,user_id,created_at)"
```

## 使用建议

- **提供表结构信息**：使用`--schema`参数传递表名和列名，以获得更准确的结果
- **指定SQL方言**：PostgreSQL和MySQL之间存在细微差异
- **从简单开始，逐步完善**：先确保基础查询的正确性
- **运行前仔细检查**：在生产环境中执行查询前，请务必先查看生成的SQL代码

## 适用场景

- 当你知道所需数据但记不住SQL语法时
- 需要快速生成报告时
- 学习SQL时，想了解查询语句的编写方式
- 在将查询代码写入应用程序之前进行原型设计时

## 作为LXGIC开发工具包的一部分

这是LXGIC Studios开发的110多个免费开发工具之一。免费版本完全开放，无需支付费用或注册账号，也不需要API密钥。这些工具都能正常使用。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgic.dev

## 系统要求

无需安装，只需使用`npx`命令即可运行。建议使用Node.js 18及以上版本。

```bash
npx ai-sql --help
```

## 工作原理

该工具会将你输入的自然语言描述发送给一个能够理解SQL的语音模型，模型会根据你选择的SQL方言生成格式规范的查询语句。

## 许可证

采用MIT许可证，永久免费。你可以自由使用该工具。