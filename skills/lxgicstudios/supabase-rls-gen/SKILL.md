---
name: supabase-rls-gen
description: 根据 Prisma 的数据库模式生成 Supabase 的 RLS（Row Level Security，行级安全）策略。这些策略用于保护数据库的安全性。
---

# Supabase RLS 生成器

行级安全（Row Level Security, RLS）功能非常强大，但其策略语法较为复杂。该工具会读取您的 Prisma 数据模型并自动生成相应的 RLS 策略。

**仅需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-supabase-gen ./prisma/schema.prisma
```

## 功能介绍

- 读取您的 Prisma 数据模型
- 生成适用于 Supabase 的 RLS 策略
- 支持常见的访问控制模式（如对自有数据的访问、团队访问权限等）
- 自动包含策略启用语句

## 使用示例

```bash
# Generate from Prisma
npx ai-supabase-gen ./prisma/schema.prisma
```

## 最佳实践

- **启用 RLS**：默认情况下 RLS 是关闭的，请务必启用它。
- **测试策略**：确保策略按预期工作。
- **使用辅助函数**：如 `auth.uid()`、`auth.role()` 等。
- **考虑所有数据操作**：包括 SELECT、INSERT、UPDATE、DELETE 等操作。

## 适用场景

- 设置 Supabase 的安全机制
- 为现有表添加 RLS 功能
- 学习 RLS 的使用方法
- 保护多租户应用程序的安全性

## 属于 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多个免费开发工具之一。免费版本完全无限制使用，无需支付费用、注册账号或获取 API 密钥。这些工具都能正常运行。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgic.dev

## 使用要求

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。运行时需要设置 `OPENAI_API_KEY` 环境变量。

```bash
npx ai-supabase-gen --help
```

## 工作原理

该工具会解析您的 Prisma 数据模型，以理解其中的数据结构和关系。随后根据常见的访问控制模式生成相应的 RLS 策略。

## 许可证

采用 MIT 许可协议，永久免费。您可以随心所欲地使用该工具。