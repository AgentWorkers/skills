---
name: index-suggester
description: 从查询模式中获取智能的数据库索引建议。当查询速度较慢时，可以使用此方法。
---

# 索引建议器（Index Suggester）

您的查询执行速度较慢，但您不确定应该创建哪些索引。该工具会分析您的查询文件，并告诉您应该创建哪些索引。

**只需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx @lxgicstudios/ai-index ./src/queries/
```

## 功能介绍

- 分析您的查询文件中的模式
- 识别缺失的索引
- 为复杂的查询建议创建复合索引
- 解释每个索引的作用

## 使用示例

```bash
# Analyze all query files
npx @lxgicstudios/ai-index ./src/queries/

# Single file
npx @lxgicstudios/ai-index ./src/queries/users.ts -o indexes.sql

# Prisma queries
npx @lxgicstudios/ai-index ./prisma/
```

## 最佳实践

- **避免过度创建索引**——过多的索引会降低写入速度
- **考虑查询频率**——优先为高频查询创建索引
- **谨慎使用复合索引**——列的排序顺序很重要
- **部署前进行测试**——索引可能会影响查询计划

## 适用场景

- 查询性能下降时
- 向应用程序中添加新查询时
- 数据库审计与优化时
- 学习索引策略时

## 属于 LXGIC 开发工具包（LXGIC Dev Toolkit）的一部分

这是 LXGIC Studios 开发的 110 多个免费开发工具之一。免费版本无需支付费用、无需注册，也不需要 API 密钥。这些工具都能正常使用。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgicstudios.com

## 系统要求

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。需要设置 `OPENAI_API_KEY` 环境变量。

```bash
npx @lxgicstudios/ai-index --help
```

## 工作原理

该工具会读取您的查询文件，提取 `WHERE` 子句和 `JOIN` 条件，然后判断哪些索引能够提升查询性能。AI 会根据查询的选择性和模式来优先推荐合适的索引。

## 许可证

采用 MIT 许可协议，永久免费。您可以自由使用该工具。