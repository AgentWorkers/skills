---
name: supabase-gen
description: 根据 Prisma 的模式生成 Supabase 的 RLS（Row-Level Security）策略。这些策略可用于为您的表设置行级安全性。
---

# Supabase Gen

在实现行级安全（Row-level security）时，编写相关代码往往非常繁琐。这款工具会读取您的 Prisma 模式（schema），并自动生成适用于 Supabase 的 RLS（Row-Level Security）策略。它能够根据您的数据模型提供安全且合理的默认设置。

**只需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-supabase-gen prisma/schema.prisma
```

## 功能介绍

- 读取您的 Prisma 模式并理解数据模型结构
- 为 SELECT、INSERT、UPDATE、DELETE 操作生成相应的 RLS 策略
- 实现对用户拥有资源的访问控制（通过 `auth.uid()` 函数）
- 支持多租户模式，并根据组织层级进行权限管理
- 生成可直接在 Supabase SQL 编辑器中运行的 SQL 语句

## 使用示例

```bash
# Generate RLS from your schema
npx ai-supabase-gen prisma/schema.prisma

# Save to migration file
npx ai-supabase-gen prisma/schema.prisma > supabase/migrations/001_rls.sql

# Specify output format
npx ai-supabase-gen prisma/schema.prisma --format sql
```

## 最佳实践

- **仔细审查每条策略**：虽然 AI 可以提供帮助，但您最了解自己的访问需求
- **用不同用户进行测试**：RLS 策略中的漏洞可能难以发现，因此需要以不同角色进行读写操作测试
- **初始设置时应采取严格的访问控制**：阻止合法访问总比数据泄露要好；后续可以根据实际情况逐步放宽限制
- **谨慎使用服务角色（service roles）**：服务角色可以绕过 RLS 策略，这既方便又可能带来安全隐患

## 适用场景

- 为已有 Prisma 模式的 Supabase 项目配置 RLS 安全性
- 为尚未启用 RLS 安全性的表格添加该功能
- 对现有安全设置进行审计，并希望获得新的策略以供对比
- 学习 RLS 的实现方式，了解其最佳实践

## 属于 LXGIC 开发工具包（LXGIC Dev Toolkit）

这是 LXGIC Studios 开发的 110 多款免费开发者工具之一。所有工具均免费提供，无需支付费用或注册账号，免费版本也不需要 API 密钥。只需使用 `npx` 命令即可运行。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgic.dev

## 使用要求

无需安装任何软件，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。运行该工具需要设置 `OPENAI_API_KEY` 环境变量。

```bash
export OPENAI_API_KEY=sk-...
npx ai-supabase-gen --help
```

## 工作原理

该工具会解析您的 Prisma 模式，识别模型结构、字段类型及字段之间的关系，然后根据用户所有权、组织成员资格以及数据的公共/私有访问权限等常见规则生成相应的 RLS 策略。同时，它会利用 GPT（Generative Pre-trained Transformer）模型智能地处理一些复杂情况。

## 许可证

采用 MIT 许可协议，永久免费。您可以随意使用该工具。