---
name: "saas-scaffolder"
description: "使用 Next.js 14 及更高版本的应用路由（App Router）、TypeScript、Tailwind CSS、shadcn/ui、Drizzle ORM 和 Stripe，生成一套完整的、可用于生产环境的 SaaS 项目模板。该模板包括认证机制、数据库架构、账单集成功能、API 路由以及一个可正常使用的仪表板。适用于用户需要创建新的 SaaS 应用程序、启动基于订阅模式的 Web 项目，或搭建 Next.js 应用程序的场景；同时也可用于描述“启动模板”（starter template）、“项目模板”（boilerplate）、“新项目”（new project）等概念，以及与认证和支付系统相关的配置工作。"
---
# SaaS 搭建工具（SaaS Scaffolder）

**级别：** 高级（Powerful）  
**类别：** 产品团队（Product Team）  
**领域：** 全栈开发（Full-Stack Development）/ 项目启动（Project Bootstrapping）  

---

## 输入格式  
（输入格式的具体内容在文档中未提供，此处保留空白。）

---

## 文件结构输出  
（文件结构的具体内容在文档中未提供，此处保留空白。）

---

## 关键组件模式  

### 身份认证配置（NextAuth）  
（相关代码块内容在文档中未提供，此处保留空白。）

### 数据库架构（Drizzle + NeonDB）  
（相关代码块内容在文档中未提供，此处保留空白。）

### Stripe 结账功能  
（相关代码块内容在文档中未提供，此处保留空白。）

### 中间件（Middleware）  
（相关代码块内容在文档中未提供，此处保留空白。）

### 环境变量模板  
（相关代码块内容在文档中未提供，此处保留空白。）

---

## 搭建检查清单  
以下阶段必须按顺序完成。**每个阶段完成后请进行验证。**  

### 第1阶段 — 基础建设（Foundation）  
- [ ] 1. 使用 TypeScript 和 App Router 初始化 Next.js  
- [ ] 配置 Tailwind CSS 并使用自定义主题样式  
- 安装并配置 shadcn/ui  
- 配置 ESLint 和 Prettier  
- 创建 `.env.example` 文件并设置所有必要的环境变量  

✅ **验证方法：** 运行 `npm run build` — 不应出现 TypeScript 或代码格式错误。  
🔧 **如果构建失败：** 检查 `tsconfig.json` 中的路径设置，以及是否已安装所有 shadcn/ui 的依赖项。  

### 第2阶段 — 数据库（Database）  
- [ ] 安装并配置 Drizzle ORM  
- 设计数据库架构（用户、账户、会话、验证令牌）  
- 生成并应用初始数据库迁移  
- 从 `lib/db.ts` 中导出数据库客户端（单例模式）  
- 在本地环境中测试数据库连接  

✅ **验证方法：** 在测试脚本中运行 `db.select().from(users)` — 应返回空数组且不抛出错误。  
🔧 **如果数据库连接失败：** 确保 `DATABASE_URL` 的格式包含 `?sslmode(require)`（适用于 NeonDB/Supabase）。使用 `drizzle-kit push`（开发环境）或 `drizzle-kit migrate`（生产环境）验证迁移是否成功应用。  

### 第3阶段 — 身份认证（Authentication）  
- 安装身份认证提供者（NextAuth / Clerk / Supabase）  
- 配置 OAuth 提供者（Google / GitHub）  
- 创建身份认证 API 路由  
- 会话回调中包含用户 ID 和订阅状态  
- 中间件保护仪表板路由  
- 构建登录和注册页面，并显示错误状态  

✅ **验证方法：** 通过 OAuth 登录，确认用户具有 `id` 和 `subscriptionStatus`。尝试在没有会话的情况下访问 `/dashboard` — 应被重定向到 `/login`。  
🔧 **如果在生产环境中出现登录循环问题：** 确保 `NEXTAUTH_SECRET` 已设置且在所有环境中保持一致。如果出现 TypeScript 错误，添加 `declare module "next-auth"` 以扩展会话类型。  

### 第4阶段 — 支付（Payments）  
- 使用 TypeScript 类型初始化 Stripe 客户端  
- 创建结账会话路由  
- 创建客户门户页面  
- 实现 Stripe Webhook 处理逻辑（包括签名验证）  
- Webhook 动作应原子性地更新数据库中的用户订阅状态  

✅ **验证方法：** 使用测试卡号（`4242 4242 4242 4242`）完成Stripe 结账测试。确认 `stripeSubscriptionId` 已写入数据库。重新触发 `checkout.session_completed` Webhook 事件，验证操作的原子性（避免数据库重复写入）。  
🔧 **如果 Webhook 签名验证失败：** 在本地运行 `stripe listen --forward-to localhost:3000/api/webhooks/stripe`；切勿硬编码 Webhook 密钥。确认 `STRIPE_WEBHOOK_SECRET` 与监听器的输出匹配。  

### 第5阶段 — 用户界面（UI）  
- 创建包含首页、功能介绍和价格信息的页面  
- 设计带有侧边栏和响应式页头的仪表板  
- 创建显示当前套餐和升级选项的账单页面  
- 创建包含个人资料更新表单和成功状态提示的设置页面  

✅ **验证方法：** 运行 `npm run build` 进行最终的生产环境构建检查。手动浏览所有页面，确认布局无误、会话数据完整且无加载错误。  

---

## 参考文件  
为获得更多指导，请生成以下配套参考文件：  
- **`CUSTOMIZATION.md`**：身份认证提供者、数据库选项、ORM 替代方案、支付方式、UI 主题以及计费模式（按用户计费、固定费率、按使用量计费）。  
- **`PITFALLS.md`**：常见故障原因：`NEXTAUTH_SECRET` 未设置、Webhook 密钥不匹配、Edge 运行时与 Drizzle 的冲突、会话类型未正确扩展、开发环境与生产环境之间的迁移策略差异。  
- **`BEST_PRACTICES.md`**：Stripe 单例模式的使用、表单变更时的服务器处理逻辑、异步数据加载时的 `Suspense` 机制、通过 `stripeCurrentPeriodEnd` 控制服务器端功能启用/禁用、以及在身份认证路由上使用 Upstash Redis 和 `@upstash/ratelimit` 实现的速率限制。