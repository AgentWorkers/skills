---
name: prisma-gen
description: **从普通文本生成 Prisma 数据模型**  
当您需要快速创建数据库模型而不想编写繁琐的样板代码时，可以使用此方法。
---

# Prisma Gen

再也不用手动编写 Prisma 模式了。只需用简单的英语描述你的数据模型，几秒钟内就能得到一个完整、可直接用于生产的 `schema.prisma` 文件。再也不用去搜索关系的语法，也不用担心忘记使用 `@unique` 等装饰器了。

**一个命令，无需任何配置，即可使用。**

## 快速入门

```bash
npx ai-prisma-gen "a blog with users, posts, comments, and tags"
```

## 功能介绍

- 从自然语言描述生成完整的 Prisma 模式
- 自动处理各种关系（一对一、多对多、自引用）
- 为字段添加适当的索引、约束和默认值
- 支持所有 Prisma 字段类型和装饰器
- 输出格式规范、易于使用的模式文件

## 使用示例

```bash
# E-commerce database
npx ai-prisma-gen "e-commerce with products, categories, orders, and user reviews"

# SaaS multi-tenant
npx ai-prisma-gen "multi-tenant saas with organizations, teams, users, and role-based permissions"

# Social app
npx ai-prisma-gen "social network with users, friendships, posts, likes, and direct messages"

# Save to file
npx ai-prisma-gen "task management with projects and assignees" > prisma/schema.prisma
```

## 最佳实践

- **明确描述关系** - 例如，应写 “用户有很多帖子” 而不是简单地写 “用户和帖子”
- **提及唯一字段** - 如果需要，要说明 “电子邮件应该是唯一的”
- **考虑边缘情况** - 如软删除、时间戳、状态枚举等，务必提前说明
- **迁移前进行审查** - 模式文件只是一个起点，务必确认输出内容符合你的需求

## 适用场景

- 开始新项目时需要快速生成数据库模式
- 原型设计时不想浪费时间在重复性工作上
- 学习 Prisma 时想了解复杂关系的实现方式
- 将思维模型转换为实际的模式代码

## 属于 LXGIC 开发工具包

这是 LXGIC Studios 开发的 110 多个免费开发工具之一。免费版本无付费门槛、无需注册，也不需要 API 密钥。这些工具都能直接使用。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgic.dev

## 使用要求

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。需要设置 `OPENAI_API_KEY` 环境变量。

```bash
export OPENAI_API_KEY=sk-...
npx ai-prisma-gen --help
```

## 工作原理

将你的自然语言描述发送给 GPT，并提供 Prisma 特定的提示，GPT 会生成格式规范的 `schema.prisma` 文件。AI 能理解 Prisma 的约定（如 `@@index`、`@relation`），以及常见的模式元素（如软删除、时间戳等）。

## 许可证

MIT 许可证。永久免费，可随意使用。