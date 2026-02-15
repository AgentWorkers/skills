---
name: clerk-auth
description: |
  Clerk auth with API Keys beta (Dec 2025), Next.js 16 proxy.ts (March 2025 CVE context), API version 2025-11-10 breaking changes, clerkMiddleware() options, webhooks, production considerations (GCP outages), and component reference. Prevents 15 documented errors. Use when: API keys for users/orgs, Next.js 16 middleware filename, troubleshooting JWKS/CSRF/JWT/token-type-mismatch errors, webhook verification, user type inconsistencies, or testing with 424242 OTP.
user-invocable: true
---

# Clerk Auth - 变更说明与错误预防指南

## 包版本：
@clerk/nextjs@6.36.7, @clerk/backend@2.29.2, @clerk/clerk-react@5.59.2, @clerk/testing@1.13.26

### 变更说明：
- 2025年11月：API版本更新至2025-11-10
- 2024年10月：Next.js v6中的`async auth()`方法引入

## 最后更新时间：2026年1月9日

---

## 2025年12月至2026年1月的新增功能

### 1. API密钥（测试版）（2025年12月11日） - 新功能 ✨
- 为应用程序提供用户级和组织级API密钥
- 支持零代码UI组件

### 后端验证：
### clerkMiddleware的令牌类型：
### 定价（测试版 = 免费）：
- 创建密钥：0.001美元/个
- 验证：0.0001美元/次

### 2. Next.js 16：`proxy.ts`中间件文件名变更（2025年12月）
**⚠️ 重要变更**：由于2025年3月发现的安全漏洞，Next.js 16的中间件文件名已更改

### Next.js 16的正确配置：
### 最低版本要求：
@clerk/nextjs@6.35.0或更高版本（修复Turbopack构建错误和登出时的缓存失效问题）

### 3. 强制密码重置（2025年12月19日）
管理员可以标记密码为已泄露，并强制用户重置密码

### 4. 组织报告与筛选功能（2025年12月15日至17日）
- 仪表板新增组织创建指标，并支持按名称/slug/日期进行筛选

---

## API版本2025-11-10的变更说明

### 1. API版本2025-11-10（2025年11月10日） - 重要变更 ⚠️
- 影响使用Clerk Billing/Commerce API的应用程序
- **端点URL**：`/commerce/` → `/billing/`（30多个端点）
- **字段术语**：`payment_source` → `payment_method`
- **移除的字段**：`amount`, `amountformatted`（使用`fee.amount`代替）
- **移除的端点**：`invoices`端点，`Products`端点
- **空值处理**：`null`表示“不存在”，省略表示“未声明存在”

### 迁移说明：
- 需将SDK更新至v6.35.0或更高版本，以支持API版本2025-11-10

### Next.js v6中的`async auth()`方法（2024年10月） - 重要变更 ⚠️
- 影响所有使用`auth()`方法的Next.js服务器组件

### Next.js 16的支持（2025年11月）
@clerk/nextjs v6.35.2或更高版本为Next.js 16提供了缓存失效的改进功能

---

## 关键模式与错误预防

### Next.js v6：`async auth()`辅助函数
### Cloudflare Workers：`authorizedParties`（防止CSRF攻击）
**务必设置`authorizedParties`以防止CSRF攻击**

### clerkMiddleware()配置
### 路由保护模式
### 所有中间件选项：
| 选项 | 类型 | 描述 |
|--------|------|-------------|
| `debug` | `boolean` | 启用调试日志记录 |
| `jwtKey` | `string` | 用于无网络验证的JWKS公钥 |
| `clockSkewInMs` | `number` | 令牌时间偏差（默认值：5000毫秒） |
| `organizationSyncOptions` | `object` | 基于URL的组织激活 |
| `signInUrl` | `string` | 自定义登录URL |
| `signUpUrl` | `string` | 自定义注册URL |

### 组织同步（基于URL的组织激活）
**仅适用于Next.js**：此功能目前仅与`clerkMiddleware()`配合使用。由于`Sec-Fetch-Dest`头的检查，它不适用于其他运行时环境（如Cloudflare Workers、Express等）。

---

## Webhook验证
### 常见事件类型：
| 事件 | 触发条件 |
|-------|---------|
| `user-created` | 新用户注册 |
| `user.updated` | 用户资料更新 |
| `userdeleted` | 用户账户删除 |
| `session-created` | 新会话创建 |
| `session.ended` | 登出 |
| `organization-created` | 新组织创建 |
| `organization-membership-created` | 用户加入组织 |

### Webhook路由注意事项：
- Webhook路由必须设置为公共访问（无需身份验证）

---

## UI组件快速参考
| 组件 | 用途 |
|-----------|---------|
| `<SignIn />` | 完整的登录流程 |
| `<SignUp />` | 完整的注册流程 |
| `<SignInButton />` | 触发登录弹窗 |
| `<SignUpButton />` | 触发注册弹窗 |
| `<SignedIn>` | 仅在用户登录时显示 |
| `<SignedOut>` | 仅在用户未登录时显示 |
| `<UserButton />` | 用户菜单，包含登出选项 |
| `<UserProfile />` | 完整的用户资料管理 |
| `<OrganizationSwitcher />` | 在不同组织间切换 |
| `<OrganizationProfile />` | 组织设置 |
| `<CreateOrganization />` | 创建新组织 |
| `<APIKeys />` | API密钥管理（新功能） |

### React Hooks
| Hook | 返回值 |
|------|---------|
| `useAuth()` | `{userId, sessionId, isLoaded, isSignedIn, getToken }` |
| `useUser()` | `{ user, isLoaded, isSignedIn }` |
| `useClerk()` | 提供Clerk实例及相关方法 |
| `useSession()` | 当前会话对象 |
| `useOrganization()` | 当前组织上下文 |
| `useOrganizationList()` | 用户所属的所有组织 |

---

## JWT模板 - 大小限制与简写代码

### JWT大小限制：
- 自定义声明的最大大小为1.2KB

### 开发注意事项：
- 在Vite开发模式下测试自定义JWT声明时，可能会遇到“431 Request Header Fields Too Large”错误。这是由于Clerk的握手令牌在URL中的长度超过了Vite的8KB限制。请参考[问题#11](#issue-11-431-request-header-fields-too-large-vite-dev-mode)获取解决方案。

### 最佳实践：
- 将大型数据存储在数据库中，仅在JWT中包含标识符/角色信息。

### 可用的简写代码：
| 类别 | 简写代码 | 例子 |
|----------|-----------|---------|
| **用户ID与姓名** | `{{user.id}}`, `{{user.first_name}}`, `{{user.last_name}}`, `{{user.full_name}}` | `"John Doe"` |
| **联系方式** | `{{user.primary_email_address}}`, `{{user.primary_phone_address}}` | `"john@example.com"` |
| **个人资料** | `{{user.image_url}}`, `{{user.username}}`, `{{user.created_at}}` | `"https://..."` |
| **验证状态** | `{{user.email_verified}}`, `{{user.phone_number_verified}}` | `true` |
| **元数据** | `{{user.public_metadata}}`, `{{user.public_metadata.field}}` | `{"role": "admin"}` |
| **组织信息** | `org_id`, `org_slug`, `org_role` | `"org:admin"` |

---

## 使用Clerk进行测试

- 测试凭据（已修复OTP问题）
- 测试电话号码（已修复短信发送问题）
- 生成的会话令牌有效期为60秒

### 使用Playwright进行端到端测试：
- 安装`@clerk/testing`以自动管理测试令牌

## 已知问题的预防措施

本文档预防了15个已记录的问题：

### 问题#1：Clerk密钥缺失
- **错误**：“缺少Clerk密钥或API密钥”
- **预防措施**：务必在`.env.local`文件中设置密钥，或通过`wrangler secret put`配置

### 问题#2：API密钥与Secret Key的替换
- **错误**：“apiKey已过时，请使用secretKey”
- **预防措施**：在所有调用中将`apiKey`替换为`secretKey`

### 问题#3：JWKS缓存竞争条件
- **错误**：“无法获取JWK”
- **预防措施**：使用@clerk/backend@2.17.2或更高版本的SDK

### 问题#4：`authorizedParties`缺失（CSRF攻击）
- **错误**：虽然没有显示错误，但存在CSRF风险
- **预防措施**：始终设置`authorizedParties: ['https://yourdomain.com']`

### 问题#5：导入路径变更
- **错误**：“无法找到模块”
- **预防措施**：更新Core 2的导入路径

### 问题#6：JWT大小超出限制
- **错误**：令牌大小超过限制
- **预防措施**：确保自定义声明的大小在1.2KB以内

### 问题#7：API版本v1已过时
- **错误**：“API版本v1已过时”
- **预防措施**：使用最新版本的SDK（API版本2025-11-10）

### 问题#8：ClerkProvider JSX组件使用错误
- **错误**：“无法作为JSX组件使用”
- **预防措施**：确保使用与React 19兼容的@clerk/clerk-react@5.59.2+

### 问题#9：`async auth()`辅助函数的混淆
- **错误**：“auth()不是一个函数”
- **预防措施**：始终使用`await`：`const { userId } = await auth()`

### 问题#10：环境变量配置错误
- **错误**：“缺少可发布的密钥”或密钥泄露
- **预防措施**：使用正确的前缀（`NEXT_PUBLIC_`, `VITE_`），切勿直接提交密钥

### 问题#11：Vite开发模式下的请求头字段过大
- **错误**：在登录时出现“431 Request Header Fields Too Large”错误
- **原因**：Clerk的`__clerk_handshake`令牌在URL中的长度超过了Vite的8KB限制
- **预防措施**：
  - 在`package.json`中添加相关配置
  - 清除浏览器缓存，重新登录

### 问题#12：用户类型不匹配
- **原因**：`useUser()`和`currentUser()`返回的对象属性不同
- **预防措施**：仅使用共享的属性，或为客户端和服务器环境分别编写辅助函数

### 问题#13：使用多种`acceptsToken`类型导致的错误
- **原因**：使用`authenticateRequest()`时，如果同时指定多种`acceptsToken`类型，可能会引发错误
- **预防措施**：升级至@clerk/backend@2.29.2或更高版本

### 问题#14：`deriveUrlFromHeaders`在格式错误的URL下导致服务器崩溃
- **原因**：内部`deriveUrlFromHeaders()`函数在处理格式错误的URL时会导致服务器崩溃
- **预防措施**：升级至@clerk/backend@2.29.0或更高版本

### 问题#15：`treatPendingAsSignedOut`选项的用途
- **说明**：此选项用于处理特殊情况
- **用法**：设置`treatPendingAsSignedOut: false`以将待处理的会话视为已登录状态

---

## 生产环境注意事项

- **服务可用性与可靠性**：
- 2025年5月至6月期间，Clerk因Google Cloud Platform（GCP）故障导致三次重大服务中断。2025年6月26日的故障持续了45分钟（UTC时间6:16-7:01），影响了所有Clerk用户。
- **缓解策略**：
  - 监控[Clerk状态](https://status.clerk.com)以获取实时更新
  - 在Clerk API不可用时实现优雅降级
  - 尽可能在本地缓存认证令牌
  - 对于现有会话，使用`jwtKey`进行无网络验证

---

## 官方文档：
- **Clerk文档**：https://clerk.com/docs
- **Next.js指南**：https://clerk.com/docs/references/nextjs/overview
- **React指南**：https://clerk.com/docs/references/react/overview
- **后端SDK**：https://clerk.com/docs/reference/backend/overview
- **JWT模板**：https://clerk.com/docs/guides/sessions/jwt-templates
- **API版本2025-11-10升级指南**：https://clerk.com/docs/guides/development/upgrading/upgrade-guides/2025-11-10
- **测试指南**：https://clerk.com/docs/guides/development/testing/overview

---

## 包版本（2025年11月22日最新版本）：
---

## 令牌效率：
- 未使用本文档中的优化措施时：约6,500个令牌
- 使用本文档中的优化措施后：约3,200个令牌
- **节省的令牌数量**：约51%（约3,300个令牌）

## 预防的错误：
- 15个已记录的问题及其对应的解决方案
- **关键价值**：API密钥（测试版）、Next.js 16的`proxy.ts`（包含2025年3月的安全漏洞修复）、`clerkMiddleware()`选项、Webhook功能、组件参考、API版本2025-11-10的变更说明、JWT大小限制、用户类型不匹配问题以及生产环境注意事项

---

**最后验证时间**：2026年1月20日
**技能版本**：3.1.0
**变更内容**：
- 新增了4个已知问题（问题#12-15）
- 扩展了`proxy.ts`部分的描述，包括2025年3月的安全漏洞信息
- 添加了生产环境注意事项（包括GCP故障的应对策略）

---

通过遵循这些指南和最佳实践，您可以确保Clerk服务的稳定性和安全性。