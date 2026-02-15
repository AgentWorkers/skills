---
name: prisma-gen
description: 从纯文本描述生成 Prisma 数据库模式。适用于开始设计数据库架构时使用。
---

# Prisma Generator

设计数据库模式意味着需要考虑数据之间的关系、索引以及约束条件。通过描述你的数据，Prisma 会自动生成完整的数据库模式。

**只需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-prisma-gen "e-commerce with users, products, and orders"
```

## 功能介绍

- 根据用户提供的数据描述生成完整的 Prisma 模式
- 自动设置正确的数据关系和约束条件
- 包含常见的字段（如 `createdAt`、`updatedAt`）
- 支持枚举类型和索引的创建

## 使用示例

```bash
# E-commerce schema
npx ai-prisma-gen "e-commerce with users, products, orders"

# SaaS schema
npx ai-prisma-gen "SaaS with organizations, users, and subscriptions"

# Social app
npx ai-prisma-gen "social app with users, posts, likes, and follows"
```

## 最佳实践

- **合理使用数据关系**：让 Prisma 自动处理数据之间的连接操作
- **为频繁查询的字段添加索引**  
- **采用“软删除”机制**：使用 `deletedAt` 而不是直接删除数据  
- **持续审查和优化**：AI 可生成 80% 的代码，其余部分由用户自行完成

## 适用场景

- 开始新的数据库设计时  
- 学习 Prisma 模式的语法  
- 快速原型开发  
- 获取可供进一步定制的数据库基础结构  

## Prisma Generator 是 LXGIC Dev Toolkit 的一部分

Prisma Generator 是 LXGIC Studios 开发的 110 多款免费开发工具之一。所有功能均免费提供，无需支付费用、注册账号或使用 API 密钥。  

**了解更多：**  
- GitHub: https://github.com/LXGIC-Studios  
- Twitter: https://x.com/lxgicstudios  
- Substack: https://lxgicstudios.substack.com  
- 官网: https://lxgicstudios.com  

## 使用要求

无需安装任何软件，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。运行时需要设置 `OPENAI_API_KEY` 环境变量。  

```bash
npx ai-prisma-gen --help
```

## 工作原理

Prisma Generator 会解析用户用自然语言描述的数据模型和关系结构，然后生成符合 Prisma 标准的数据库模式语法，其中包含正确的字段类型、数据关系和索引设置。

## 许可证

Prisma Generator 使用 MIT 许可证，永久免费。你可以随心所欲地使用它。