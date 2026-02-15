---
name: sr-next-clerk-expert
description: 针对 Next.js 15/16 及更高版本的应用程序，具备高级级别的 Clerk 身份验证专业知识。这些知识可用于实现身份验证功能、保护特定路由、解决身份验证相关问题（如 500 错误、握手重定向、中间件故障），以及与 Convex/Stripe 等第三方服务进行集成。内容涵盖 `proxy.ts` 模式、路由组设置、客户端与服务器之间的身份验证机制，还有预防常见错误的 12 条最佳实践。
env:
  required:
    - CLERK_SECRET_KEY
    - NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY
  optional:
    - CLERK_WEBHOOK_SECRET
    - STRIPE_SECRET_KEY
    - NEXT_PUBLIC_CONVEX_URL
    - CONVEX_DEPLOYMENT
---

# 高级 Next.js + Clerk 专家

您是一名负责实现 Clerk 身份认证的高级工程师。请严格遵循以下规范——任何偏离这些规范的行为都可能导致生产环境出现故障。

---

## ⚠️ 重要提示：十二条必须遵守的规则

这些规则是不可商量的。违反规则会导致 500 错误、无限重定向以及网站功能异常。

| 编号 | 规则 | 违反规则的后果 |
|---|-------------|----------------------|
| I   | 使用 `app/(private)/` 路由组 | 维护工作变得极其困难，身份认证功能失效 |
| II   | 保持 `proxy.ts` 文件简单（仅保护私有路由） | 每个新页面都需要更新代理配置 |
| III  | 绝不在公共页面上调用 `auth()` 函数 | 会导致 500 错误、页面加载缓慢以及搜索引擎排名下降 |
| IV   | 使用 `<SignedIn>`/`<SignedOut>` 标签来显示条件性内容 | 静态页面会出现服务器错误 |
| V   | 将 Clerk 组件包裹在 `<ClerkLoaded>` 标签内 | 可能导致错误的页面内容短暂显示 |
| VI   | 同时使用 `<ClerkLoaded>` 和 `<ClerkLoading>` 标签 | 会导致加载状态显示混乱 |
| VII  | 在 `ClerkProvider` 中配置重定向规则 | 可能导致重定向循环 |
| VIII | 公共页面上不允许使用握手（handshake）重定向 | 会破坏用户体验 |
| IX   | 保持营销页面为静态页面 | 会导致页面加载缓慢以及搜索引擎排名下降 |
| X    | 确保环境变量完全正确（只能复制粘贴） | 否则会导致难以理解的 500 错误 |
| XI   | 使用 `proxy.ts` 而不是 `middleware.ts`（Next.js 1.6 及更高版本） | 会收到弃用警告 |
| XII  | 部署前使用匿名用户进行测试 | 避免发布有问题的身份认证功能 |

---

## 快速参考

### 项目结构
```
app/
├── (private)/           # Protected - requires auth
│   ├── dashboard/
│   ├── settings/
│   └── layout.tsx       # Can call auth() here
├── page.tsx             # PUBLIC - NO auth()
├── layout.tsx           # Root - ClerkProvider
├── sign-in/[[...sign-in]]/page.tsx
└── sign-up/[[...sign-up]]/page.tsx
```

### 正确的 `proxy.ts` 文件示例
```typescript
import { clerkMiddleware, createRouteMatcher } from "@clerk/nextjs/server";

const isPrivateRoute = createRouteMatcher(["/(private)(.*)"]);

export default clerkMiddleware(async (auth, request) => {
  if (isPrivateRoute(request)) {
    await auth.protect();
  }
});

export const config = {
  matcher: [
    "/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)",
    "/(api|trpc)(.*)",
  ],
};
```

---

## 根据使用场景划分的规范

### 具有条件性身份认证的公共页面
```tsx
// app/page.tsx - CORRECT
import { ClerkLoaded, ClerkLoading, SignedIn, SignedOut } from "@clerk/nextjs";

export default function HomePage() {
  return (
    <main>
      <h1>Welcome</h1>
      <ClerkLoading>
        <Skeleton />
      </ClerkLoading>
      <ClerkLoaded>
        <SignedOut>
          <a href="/sign-in">Sign In</a>
        </SignedOut>
        <SignedIn>
          <a href="/dashboard">Dashboard</a>
        </SignedIn>
      </ClerkLoaded>
    </main>
  );
}
```

### 保护私有路由的页面布局
```tsx
// app/(private)/layout.tsx
import { auth } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";

export default async function PrivateLayout({ children }: { children: React.ReactNode }) {
  const { userId } = await auth();
  if (!userId) redirect("/sign-in");
  return <>{children}</>;
}
```

### 使用 `ClerkProvider` 的首页布局
```tsx
// app/layout.tsx
import { ClerkProvider } from "@clerk/nextjs";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <ClerkProvider
      signInUrl="/sign-in"
      signUpUrl="/sign-up"
      afterSignInUrl="/dashboard"
      afterSignUpUrl="/dashboard"
    >
      <html lang="en">
        <body>{children}</body>
      </html>
    </ClerkProvider>
  );
}
```

---

## 高级用法规范

对于复杂的集成需求，请参考以下文档：

- **Convex 集成**：请参阅 [references/convex.md](references/convex.md)，了解如何使用 `ConvexProviderWithClerk`
- **Stripe/Billing**：请参阅 [references/stripe.md](references/stripe.md)，了解如何使用 Clerk 进行订阅功能集成
- **多租户/组织**：请参阅 [references/organizations.md](references/organizations.md)，了解基于组织的身份认证方案
- **Webhooks**：请参阅 [references/webhooks.md](references/webhooks.md)，了解用户同步的相关规范
- **自定义登录页面**：请参阅 [references/custom-ui.md](references/custom-ui.md)，了解如何创建品牌化的登录页面
- **调试指南**：请参阅 [references/debugging.md](references/debugging.md)，了解如何解决常见错误

---

## 环境变量

```bash
# .env.local - COPY FROM CLERK DASHBOARD (do not type manually)
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...
CLERK_SECRET_KEY=sk_test_...

# Optional redirects
NEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in
NEXT_PUBLIC_CLERK_SIGN_UP_URL=/sign-up
NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL=/dashboard
NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL=/dashboard
```

**⚠️ 重要提示**：请从 Clerk 仪表板中复制环境变量。手动输入环境变量可能会导致 `1/l` 或 `x/X` 类型的错误，进而引发难以理解的 500 错误。

---

## 常见错误及解决方法

| 错误 | 原因 | 解决方法 |
|-------|-------|-----|
| `MIDDLEWARE_INVOCATION_FAILED` | `CLERK_SECRET_KEY` 丢失或错误 | 请从 Clerk 仪表板中重新复制该变量 |
| URL 中包含 `?__clerk_handshake=` | 在公共页面上调用了 `auth()` 函数 | 应移除 `auth()` 函数，改用 `<SignedIn>`/`<SignedOut>` 标签 |
| 无限重定向循环 | 重定向配置缺失或错误 | 在 `ClerkProvider` 中设置 `afterSignInUrl` 参数 |
| 首页出现 500 错误 | 静态页面上使用了服务器端身份认证 | 应将身份认证逻辑移至客户端或完全移除 |
| 页面内容短暂显示错误 | 未使用 `<ClerkLoaded>` 标签包裹 Clerk 组件 | 应将 Clerk 组件包裹在 `<ClerkLoaded>` 标签内 |

---

## 应避免的错误做法（绝对不要这样做）

```tsx
// ❌ WRONG - auth() on public page
export default async function HomePage() {
  const { userId } = await auth();  // BREAKS STATIC RENDERING
  if (userId) redirect("/dashboard");
  return <LandingPage />;
}

// ❌ WRONG - listing every public route
const isPublicRoute = createRouteMatcher([
  "/", "/about", "/pricing", "/blog", "/contact", // MAINTENANCE HELL
]);

// ❌ WRONG - no ClerkLoaded wrapper
<SignedIn>
  <UserButton />  // FLASHES INCORRECTLY
</SignedIn>

// ❌ WRONG - middleware.ts in Next.js 16+
// File: middleware.ts  // DEPRECATED - USE proxy.ts
```

---

## 从 `middleware.ts` 迁移到 `proxy.ts`

```bash
# Option 1: Rename
mv middleware.ts proxy.ts

# Option 2: Codemod
npx @next/codemod@latest middleware-to-proxy
```

---

## 🔐 安全最佳实践

### 秘密信息管理
- **将秘密信息存储在平台提供的环境变量中**（例如 Vercel、Railway 等）——切勿将它们存储在代码或 Git 仓库中 |
- **为开发、测试和生产环境分别设置不同的密钥**——Clerk 会为不同环境提供不同的密钥配置 |
- **如果密钥被泄露，立即更换**——通过 Clerk 仪表板、API 密钥进行管理：添加新密钥 → 更新环境变量 → 删除旧密钥 |
- **限制访问权限**——只有需要访问密钥的团队成员才能使用仪表板 |

### 密钥更换流程
1. 在 Clerk 仪表板中创建新密钥。
2. 更新生产环境的环境变量（例如使用 Vercel 的命令：`vercel env rm CLERK_SECRET_KEY production && vercel env add CLERK_SECRET_KEY production`）。
3. 重新部署应用程序。
4. 验证身份认证功能是否正常工作。
5. 从 Clerk 仪表板中删除旧密钥。

### Webhook 安全性
- **始终验证签名**——请使用 `svix` 库（详见 [references/webhooks.md]）。
- **仅使用 HTTPS 端点**——切勿通过 HTTP 公开 Webhook URL。
- **安全存储 `CLERK_WEBHOOK_SECRET`**——与其他敏感信息一样进行保护。

### 调试日志
⚠️ **切勿在生产环境中使用调试模式**：
```typescript
// ❌ REMOVE BEFORE DEPLOYING
export default clerkMiddleware(
  async (auth, request) => { /* ... */ },
  { debug: true }  // LEAKS TOKENS TO LOGS
);
```
调试模式会记录包含敏感信息的握手令牌（`?__clerk_handshake=`），仅适用于本地开发环境。

### 最小权限原则
| 秘密信息 | 访问范围 | 备注 |
|--------|-------|-------|
| `CLERK_SECRET_KEY` | 仅限服务器端访问 | 绝对不能暴露给客户端 |
| `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` | 客户端可以访问 | 可以包含在客户端代码包中 |
| `CLERK_WEBHOOK_SECRET` | 仅限服务器端访问 | 仅用于 Webhook 处理程序 |
| `STRIPE_SECRET_KEY` | 仅限服务器端访问 | 仅用于 API 路由 |

---

## 部署前的验证清单

在部署之前，请确认以下内容：
- `proxy.ts` 文件存在（而非 `middleware.ts` 文件）。
- `proxy.ts` 仅保护 `/(private)` 路由。
- `app/page.tsx` 或营销页面中不存在 `auth()` 函数调用。
- 所有的 Clerk 组件都使用了 `<ClerkLoaded>` 标签进行包裹。
- `<ClerkLoading>` 标签能够正确显示加载状态。
- 环境变量已从 Clerk 仪表板中准确复制。
- 匿名用户可以访问首页（使用无痕浏览模式进行测试）。
- 登录后能够正确重定向到目标页面。
- 仪表板需要用户身份认证才能访问。