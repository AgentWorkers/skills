---
name: schema-gen
description: 根据描述生成数据库模式
---

# 数据模式生成器

通过描述您的数据，可以自动生成合适的数据库模式。支持 SQL、Prisma 和 Drizzle 数据库。

## 快速入门

```bash
npx ai-schema "e-commerce with users, products, orders, reviews"
```

## 功能介绍

- 生成完整的数据库模式
- 自动建立字段之间的关系
- 为常用查询创建索引
- 支持时间戳和软删除（即数据的逻辑删除）

## 使用示例

```bash
# Generate SQL schema
npx ai-schema "blog with posts, authors, comments, tags"

# Prisma format
npx ai-schema "saas with teams and members" --format prisma

# Drizzle format
npx ai-schema "inventory system" --format drizzle
```

## 输出格式

- 原始 SQL 语句（适用于 PostgreSQL、MySQL）
- Prisma 模式文件
- Drizzle 模式文件
- TypeORM 实体类文件
- Mongoose 模型文件

## 包含的内容

- 主键
- 外键关系
- 常用字段的索引
- 时间戳（创建时间/更新时间）
- 软删除功能
- 在适用的情况下支持枚举类型

## 系统要求

- Node.js 18.0 及以上版本
- 需要 OPENAI_API_KEY

## 许可证

MIT 许可证。永久免费使用。

---

**开发团队：LXGIC Studios**

- GitHub 仓库：[github.com/lxgicstudios/ai-schema](https://github.com/lxgicstudios/ai-schema)
- Twitter 账号：[@lxgicstudios](https://x.com/lxgicstudios)