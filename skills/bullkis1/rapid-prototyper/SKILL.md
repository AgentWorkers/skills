---
name: rapid-prototyper
description: 超快速的概念验证（Proof-of-Concept, PoC）和最小可行产品（Minimum Viable Product, MVP）开发工具。适用于从零开始构建新的Web应用程序、原型或MVP的场景，其中速度比完美度更为重要。该工具专门针对Next.js 14、Supabase、Clerk、shadcn/ui和Prisma等快速开发技术栈进行优化。当用户需要“构建”新项目、“制作原型”、“快速开发一个应用程序”或“快速搭建一个可运行的MVP”时，该工具能够发挥重要作用。但不适用于对现有代码库进行的小规模修改或修复。
  Ultra-fast proof-of-concept and MVP development. Use when building new web apps,
  prototypes, or MVPs from scratch where speed matters over perfection. Specializes
  in the canonical fast-stack: Next.js 14 + Supabase + Clerk + shadcn/ui + Prisma.
  Triggers when user asks to "build", "prototype", "create a quick app", "spin up an MVP",
  or wants a working thing fast. NOT for small one-liner fixes or edits to existing codebases.
---
# 快速原型工具（Rapid Prototyper）

在几天内构建可用的最小可行产品（MVP），而非几周。优先考虑速度，避免过度设计。

## 思维方式

- 首先发布可运行的代码，而非追求完美的架构；
- 使用现成的组件和基于云的基础设施（BaaS）而非自定义基础设施；
- 先验证想法，再优化细节；
- 从一开始就集成分析和反馈功能。

## 技术栈

**除非有特殊原因，否则始终使用以下默认配置：**

| 层次 | 工具 | 原因 |
|---|---|---|
| 框架 | Next.js 14（App Router） | 全栈开发，快速搭建 |
| 数据库 | Supabase（PostgreSQL） | 即时数据库支持、实时数据处理和存储功能 |
| 身份验证 | Clerk | 几分钟内即可完成身份验证功能的集成 |
| 用户界面 | shadcn/ui + Tailwind CSS | 高质量的组件库，无需额外设计 |
| 对象关系映射（ORM） | Prisma | 类型安全的数据库访问层 |
| 状态管理 | Zustand | 简单易用的状态管理库，无样板代码 |
| 表单处理 | React Hook Form + Zod | 内置验证功能 |
| 动画效果 | Framer Motion | 根据需要添加动画效果 |

完整的搭建命令和样板代码请参阅 `references/stack-setup.md`。

## 工作流程

### 第1阶段 — 定义核心功能（5分钟）
1. 用户使用这个应用程序时，最常执行的操作是什么？
2. 成功的标准是什么？（现在就定义好评估标准，不要等到后期）
3. 测试假设所需的最少功能是什么？

### 第2阶段 — 构建基础框架（15–30分钟）
```bash
npx create-next-app@latest my-app --typescript --tailwind --eslint --app
cd my-app
npx shadcn@latest init
```
之后：添加 Prisma 数据库驱动程序、Supabase 客户端以及 Clerk 身份验证服务。具体步骤请参考 `references/stack-setup.md`。

### 第3阶段 — 仅构建核心用户流程
- 先实现一个基本的、能正常运行的用户路径；
- 在核心功能完善之前，可以暂时忽略边缘情况、错误状态和加载状态；
- 使用 shadcn 提供的组件进行开发，无需从头开始设计界面样式。

### 第4阶段 — 添加反馈收集功能
- 始终添加一个简单的反馈机制（例如文本输入框和提交按钮）；
- 从一开始就启用 Vercel Analytics 或 PostHog 等分析工具；
- 记录关键的用户操作。

### 第5阶段 — 部署
```bash
npx vercel --prod
# or: push to GitHub → auto-deploy on Vercel
```

## 重要规则

- **身份验证功能的开发时间不得超过1小时**——优先使用 Clerk；
- **在确认 Supabase 的默认配置无法满足需求之前，**切勿自定义数据库架构；
- **在认为项目完成之前，**务必将代码部署到实际网址上（即使是开发预览版本）；
- **始终要问自己：**“这个功能对于验证核心假设是否必要？”

## 成功标准

- 应用程序已成功部署到网址上：✅ 完成；
- 核心用户流程能够端到端正常运行：✅ 完成；
- 至少有一名真实用户能够使用该应用程序进行测试：✅ 完成；
- 反馈收集机制已建立：✅ 完成。

## 参考资料

- `references/stack-setup.md` — 完整的搭建命令、环境变量配置和样板代码；
- `references/patterns.md` — 常见的设计模式：身份验证路由、数据库查询、API 路由、表单处理等。