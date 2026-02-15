---
name: supabase-rls-gen
description: 根据 Prisma 的模式生成 Supabase 的 RLS（Row Level Security）策略。这些策略用于保护数据库的安全性。
---

# Supabase RLS 生成器

行级安全（Row Level Security, RLS）功能非常强大，但其策略语法较为复杂。该工具会读取您的数据库架构（schema），并自动生成相应的 RLS 策略。

**仅需一个命令，无需任何配置，即可使用。**

## 快速入门

```bash
npx ai-supabase-gen ./prisma/schema.prisma
```

## 功能介绍

- 读取您的 Prisma 数据库架构
- 生成适用于 Supabase 的 RLS 策略
- 支持常见的访问模式（如访问用户自己的数据、团队访问权限等）
- 包含用于启用 RLS 策略的指令

## 使用示例

```bash
# Generate from Prisma
npx ai-supabase-gen ./prisma/schema.prisma
```

## 最佳实践

- **启用 RLS**：默认情况下 RLS 是关闭的，请务必先启用它。
- **测试策略**：确保策略按预期工作。
- **使用辅助函数**：如 `auth.uid()`、`auth.role()` 等。
- **考虑所有数据操作**：包括 SELECT、INSERT、UPDATE、DELETE 等操作。

## 适用场景

- 设置 Supabase 的安全机制
- 为现有表添加 RLS 保护
- 学习 RLS 的使用方法
- 保护多租户应用程序的安全

## 该工具属于 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多个免费开发工具之一。免费版本无需支付费用、无需注册账号，也不需要 API 密钥，直接可以使用这些工具。

**了解更多信息：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgicstudios.com

## 使用要求

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。运行时需要设置 `OPENAI_API_KEY` 环境变量。

```bash
npx ai-supabase-gen --help
```

## 工作原理

该工具会解析您的 Prisma 数据库架构，以理解数据模型和数据之间的关系，然后根据常见的访问模式生成相应的 RLS 策略。

## 许可证

采用 MIT 许可协议，永久免费。您可以自由使用该工具。

---

**由 LXGIC Studios 开发**

- GitHub: [github.com/lxgicstudios/supabase-schema-gen](https://github.com/lxgicstudios/supabase-schema-gen)
- Twitter: [@lxgicstudios](https://x.com/lxgicstudios)