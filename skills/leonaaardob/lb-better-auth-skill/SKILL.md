---
name: better-auth
description: 完善 `Better Auth` 的文档（采用 Markdown 格式）。该文档适用于在 TypeScript 项目中实现身份验证功能，内容涵盖 OAuth 提供商（如 Google、GitHub 等）、电子邮件/密码认证方式、Passkey 认证、双因素认证（2FA）、会话管理、数据库适配器（如 Prisma、Drizzle）以及框架集成（如 Next.js、SvelteKit 等）。
---

# 更好的认证（Better Auth）文档

所有关于“Better Auth”的文档都采用Markdown格式编写。您可以通过访问`references/`目录来获取有关认证实现、OAuth配置、数据库设置以及框架集成等方面的信息。

## 文档结构

所有文档都存储在`references/`目录中，并按主题进行分类：

### 核心文档

#### 入门
- `references/introduction.mdx` - 什么是Better Auth
- `references/installation.mdx` - 设置指南
- `references/basic-usage.mdx` - 认证基础
- `references/comparison.mdx` - 与其他认证库的比较

#### 认证方法（`references/authentication/`）
- OAuth提供者和认证策略：
  - `google.mdx` - Google OAuth
  - `github.mdx` - GitHub OAuth
  - `microsoft.mdx` - Microsoft/Azure AD
  - `apple.mdx` - Apple Sign In
  - `discord.mdx`, `facebook.mdx`, `twitter.mdx` 等
  - `email-password.mdx` - 邮箱和密码认证
  - `magic-link.mdx` - 无密码的魔法链接（Magic Links）
  - `passkey.mdx` - WebAuthn令牌

#### 数据库适配器（`references/adapters/`）
  - `prisma.mdx` - Prisma ORM
  - `drizzle.mdx` - Drizzle ORM
  - `kysely.mdx` - Kysely
  - `mongodb.mdx` - MongoDB
  - `pg.mdx` - node-postgres

#### 概念（`references/concepts/`）
  - 认证核心概念：
    - `session.mdx` - 会话管理
    - `oauth.mdx` - OAuth流程
    - `database.mdx` - 数据库架构
    - `rate-limit.mdx` - 速率限制
    - `middleware.mdx` - 认证中间件
    - `cookies.mdx` - Cookie处理

#### 插件（`references/plugins/`）
  - 扩展功能：
    - `two-factor.mdx` - 双因素认证（2FA/TOTP）
    - `passkey.mdx` - WebAuthn令牌
    - `email-verification.mdx` - 邮箱验证
    - `magic-link.mdx` - 魔法链接认证
    - `organization.mdx` - 组织和团队
    - `multi-session.mdx` - 多会话管理
    - `anonymous.mdx` - 匿名用户

#### 集成（`references/integrations/`）
  - 框架特定的集成指南：
    - `next-js.mdx` - Next.js集成
    - `sveltekit.mdx` - SvelteKit集成
    - `astro.mdx` - Astro集成
    - `solid-start.mdx` - SolidStart集成

#### 示例（`references/examples/`）
  - 实际使用示例：
    - `next-js.mdx` - 完整的Next.js示例
    - `sveltekit.mdx` - SvelteKit示例

#### 教程（`references/guides/`）
  - 操作指南：
    - `custom-session.mdx` - 自定义会话处理
    - `testing.mdx` - 认证流程测试
    - `deployment.mdx` - 生产环境部署

#### API参考（`references/reference/`）
  - 完整的API文档

## 快速参考

### 常见任务

| 任务 | 需要阅读的文件 |
|------|--------------|
| 初始设置 | `references/installation.mdx` |
| 邮箱和密码认证 | `references/authentication/email-password.mdx` |
| Google OAuth | `references/authentication/google.mdx` |
| GitHub OAuth | `references/authentication/github.mdx` |
| 使用Prisma进行设置 | `references/adapters/prisma.mdx` |
| 使用Drizzle进行设置 | `references/adapters/drizzle.mdx` |
| 会话管理 | `references/concepts/session.mdx` |
| 添加双因素认证 | `references/plugins/two-factor.mdx` |
| 添加WebAuthn令牌 | `references/plugins/passkey.mdx` |
| Next.js集成 | `references/integrations/next-js.mdx` |
| 组织和团队 | `references/plugins/organization.mdx` |
| 速率限制 | `references/concepts/rate-limit.mdx` |

### 何时使用此技能

- 在TypeScript项目中实现认证功能
- 设置OAuth提供者（如Google、GitHub、Microsoft等）
- 配置数据库适配器（如Prisma、Drizzle等）
- 添加双因素认证、WebAuthn令牌或魔法链接
- 管理会话和Cookie
- 与Next.js、SvelteKit或其他框架集成
- 有关认证模式和最佳实践的问题

### 如何导航

1. **从`references/introduction.mdx`开始阅读以获取概述**
2. **关于设置：**阅读`references/installation.mdx`
3. **关于认证方法：**浏览`references/authentication/`
4. **关于数据库：**查看`references/adapters/`
5. **关于高级功能：**查看`references/plugins/`
6. **关于框架集成：**使用`references/integrations/`

所有文件均为`.mdx`格式（Markdown + JSX），但也可以直接作为纯Markdown文本阅读。