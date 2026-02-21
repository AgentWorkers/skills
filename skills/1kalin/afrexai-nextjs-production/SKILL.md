# Next.js 生产工程

> 一套完整的开发方法论，用于构建、优化和运维生产环境的 Next.js 应用程序。从架构设计到部署策略——涵盖了“hello world”之外的所有内容。

## 快速健康检查（60 秒）

请检查以下 8 项内容，并给出相应的得分（0 表示未通过，2 表示通过）：

| 指标 | 检查内容 | 得分 |
|--------|------------------|-------|
| 🏗️ 架构 | 服务器/客户端组件的边界是经过明确设计的，而非随意设置的 | /2 |
| ⚡ 性能 | 核心 Web Vitals 指标全部达标（LCP <2.5s, INP <200ms, CLS <0.1） | /2 |
| 🔒 安全 | 客户端代码中不存在敏感信息，CSP 头部配置正确 | /2 |
| 📦 包大小 | 客户端 JavaScript 代码中没有不必要的内容，代码压缩（tree-shaking）生效 | /2 |
| 🗄️ 数据 | 缓存策略已定义（非默认设置） | /2 |
| 🧪 测试 | 使用 E2E 和单元测试，关键路径的测试覆盖率超过 70% | /2 |
| 🚀 部署 | 支持预览部署、回滚功能，并具备监控机制 | /2 |
| 📊 可观测性 | 具备错误跟踪、性能监控和结构化的日志记录 | /2 |

**总分：** /16 → 14-16 分：应用程序已具备生产环境所需的条件 | 10-13 分：需要进一步优化 | <10 分：存在严重问题**

---

## 第 1 阶段：架构设计

### App Router 与 Pages Router 的选择

**默认建议：** 对于所有新项目使用 App Router（Next.js 13.4 及以上版本）。

仅在以下情况下使用 Pages Router：
- 正在迁移现有的 Pages Router 应用程序（逐步采用新架构）
- 团队没有任何关于 RSC（React Server Components）的经验，并且项目交付截止日期在 2 周以内
- 项目依赖库要求使用 Pages Router 的设计模式

### 推荐的项目结构

```
src/
├── app/                    # App Router — routes only
│   ├── (auth)/             # Route group — shared auth layout
│   │   ├── login/page.tsx
│   │   └── register/page.tsx
│   ├── (dashboard)/        # Route group — shared dashboard layout
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── settings/page.tsx
│   ├── api/                # Route Handlers (use sparingly)
│   │   └── webhooks/
│   │       └── stripe/route.ts
│   ├── layout.tsx          # Root layout
│   ├── loading.tsx         # Root loading
│   ├── error.tsx           # Root error boundary
│   ├── not-found.tsx       # 404 page
│   └── global-error.tsx    # Global error boundary
├── components/             # Shared components
│   ├── ui/                 # Design system primitives
│   ├── forms/              # Form components
│   └── layouts/            # Layout components
├── lib/                    # Shared utilities
│   ├── db/                 # Database client & queries
│   ├── auth/               # Auth utilities
│   ├── api/                # External API clients
│   └── utils/              # Pure utility functions
├── hooks/                  # Custom React hooks (client-only)
├── actions/                # Server Actions
├── types/                  # TypeScript types
├── styles/                 # Global styles
└── config/                 # App configuration
```

### 结构规则：

1. **路由文件应保持简洁** — `page.tsx` 文件仅用于导入组件，不包含业务逻辑
2. **组件应具备复用性** — 绝不要从 `app/` 目录导入组件到 `components/` 目录
3. **服务器端操作（Server Actions）应单独放在一个目录中** — 按域名进行分类，而不是按页面分类
4. **禁止使用 barrel 文件（如 `index.ts`）** — 因为它们会影响代码压缩（tree-shaking）
5. **特定路由所需的组件应放在对应的文件夹中** — 非共享组件应放在 `_components/` 目录下

### 渲染策略选择矩阵

| 场景 | 渲染策略 | 选择理由 |
|----------|----------|-------------------|
| 静态内容（博客、文档、营销页面） | 使用静态渲染（SSG，Server-Side Generation） | 在构建时生成内容并通过 CDN 缓存 |
| 用户专属的仪表盘 | 动态服务器渲染 | 每次请求时获取最新数据 |
| 带价格的产品列表 | 使用 ISR（异步请求服务，3600 秒后重新验证数据） | 数据更新及时，加载速度快 |
| 实时数据（聊天、股票信息） | 客户端渲染 + WebSocket | 服务器无法主动推送数据 |
| 对 SEO 敏感的内容且需要实时更新 | 动态服务器渲染 + 流式数据加载 | 使用 Suspense 实现快速的首页加载时间（TTFB） |
| 高度交互式的表单/向导 | 使用客户端组件 | 需要复杂的状态管理 |

### 服务器端组件与客户端组件的使用规则

```
DEFAULT: Server Component (every .tsx is server by default)

Add "use client" ONLY when you need:
✅ useState, useEffect, useRef, useContext
✅ Browser APIs (window, document, localStorage)
✅ Event handlers (onClick, onChange, onSubmit)
✅ Third-party client libraries (framer-motion, react-hook-form)

NEVER add "use client" because:
❌ You want to use async/await (Server Components support this natively)
❌ You're fetching data (fetch in Server Components, not useEffect)
❌ You're importing a server-only library
❌ "It's not working" — debug the actual issue first
```

### 边界设计原则

**尽可能将“使用客户端处理”的逻辑推送到代码的底层。** 边界应设置在页面的最底层（叶子节点），而不是根节点。

---

## 第 2 阶段：数据获取与缓存

### 数据获取的优先级（从上到下）

1. **直接由服务器端组件获取数据** — 最简单且性能最佳
2. **通过 Server Actions 处理数据变更和表单提交**
3. **路由处理器** — 用于处理 Webhook 和外部 API 请求
4. **客户端-side 数据获取（使用 SWR/React Query）** — 仅用于实时数据或需要轮询的数据

### 数据获取配置

```tsx
// Static data (cached indefinitely, revalidated on deploy)
const data = await fetch('https://api.example.com/data', {
  cache: 'force-cache'  // Default in App Router
})

// Revalidate every hour
const data = await fetch('https://api.example.com/data', {
  next: { revalidate: 3600 }
})

// Always fresh (no cache)
const data = await fetch('https://api.example.com/data', {
  cache: 'no-store'
})

// Tag-based revalidation
const data = await fetch('https://api.example.com/products', {
  next: { tags: ['products'] }
})
// Then in a Server Action:
import { revalidateTag } from 'next/cache'
revalidateTag('products')
```

### 根据数据类型制定缓存策略

| 数据类型 | 缓存策略 | 重新验证时间 | 缓存标签 |
|-----------|---------------|------------|------|
| CMS 内容 | 使用 ISR（异步请求服务） | 3600 秒（1 小时） | `['cms', 'posts']` |
| 产品目录 | 使用 ISR | 300 秒（5 分钟） | `['products']` |
| 用户资料 | 不使用缓存 | — | — |
| 价格/库存信息 | 不使用缓存 | — | — |
| 静态资源 | 强制缓存 | 部署时自动缓存 | — |
| 分析数据/仪表盘 | 使用 ISR | 60 秒 | `['analytics']` |
| 认证令牌 | 不使用缓存 | — | — |

### 数据库查询（无需使用外部 API）

```tsx
import { unstable_cache } from 'next/cache'
import { db } from '@/lib/db'

// Cache database queries with tags
const getProducts = unstable_cache(
  async (categoryId: string) => {
    return db.query.products.findMany({
      where: eq(products.categoryId, categoryId)
    })
  },
  ['products'],  // Cache key parts
  {
    revalidate: 300,
    tags: ['products']
  }
)
```

### 并行数据获取

```tsx
// ✅ CORRECT: Parallel fetches
export default async function DashboardPage() {
  const [user, stats, notifications] = await Promise.all([
    getUser(),
    getStats(),
    getNotifications()
  ])
  return <Dashboard user={user} stats={stats} notifications={notifications} />
}

// ❌ WRONG: Sequential waterfall
export default async function DashboardPage() {
  const user = await getUser()
  const stats = await getStats(user.id)  // Waits for user
  const notifications = await getNotifications(user.id)  // Waits for stats
}
```

### 使用 Suspense 实现流式数据加载

```tsx
import { Suspense } from 'react'

export default async function Page() {
  return (
    <div>
      <h1>Dashboard</h1>
      {/* Fast: renders immediately */}
      <UserGreeting />
      
      {/* Slow: streams in when ready */}
      <Suspense fallback={<StatsSkeleton />}>
        <StatsPanel />  {/* Async Server Component */}
      </Suspense>
      
      <Suspense fallback={<FeedSkeleton />}>
        <ActivityFeed />
      </Suspense>
    </div>
  )
}
```

---

## 第 3 阶段：服务器端操作与数据变更处理

### 服务器端操作的最佳实践

```tsx
// actions/user.ts
'use server'

import { z } from 'zod'
import { revalidatePath } from 'next/cache'
import { redirect } from 'next/navigation'

const updateProfileSchema = z.object({
  name: z.string().min(1).max(100),
  email: z.string().email(),
  bio: z.string().max(500).optional()
})

export async function updateProfile(formData: FormData) {
  // 1. Authenticate
  const session = await getSession()
  if (!session) throw new Error('Unauthorized')

  // 2. Validate
  const parsed = updateProfileSchema.safeParse({
    name: formData.get('name'),
    email: formData.get('email'),
    bio: formData.get('bio')
  })
  
  if (!parsed.success) {
    return { error: parsed.error.flatten().fieldErrors }
  }

  // 3. Authorize
  if (session.userId !== formData.get('userId')) {
    throw new Error('Forbidden')
  }

  // 4. Mutate
  await db.update(users)
    .set(parsed.data)
    .where(eq(users.id, session.userId))

  // 5. Revalidate
  revalidatePath('/profile')
  
  return { success: true }
}
```

### 服务器端操作规则：

1. **始终验证用户输入** — 数据来自用户输入，切勿直接信任这些数据
2. **始终进行身份验证** — 服务器端操作属于公开接口
3. **始终检查用户权限** — 用户只能修改自己的数据
4. **使用 Zod 进行数据验证** — 提供类型安全的验证机制
5. **返回错误信息，而非直接抛出异常** — 抛出异常会暴露错误位置；返回错误信息可以更清晰地展示问题
6. **在数据变更后重新验证数据** — 使用 `revalidatePath` 或 `revalidateTag` 方法
7. **切勿返回敏感数据** — 仅返回客户端所需的数据

### 使用 `useActionState` 模式（React 19）

```tsx
'use client'
import { useActionState } from 'react'
import { updateProfile } from '@/actions/user'

export function ProfileForm({ user }: { user: User }) {
  const [state, action, pending] = useActionState(updateProfile, null)

  return (
    <form action={action}>
      <input name="name" defaultValue={user.name} />
      {state?.error?.name && <p className="text-red-500">{state.error.name}</p>}
      
      <button type="submit" disabled={pending}>
        {pending ? 'Saving...' : 'Save'}
      </button>
      
      {state?.success && <p className="text-green-500">Saved!</p>}
    </form>
  )
}
```

---

## 第 4 阶段：认证与授权

### 选择合适的认证方式

| 认证方式 | 适用场景 | 推荐库 |
|--------|----------|-----------|
| 基于会话的认证（cookie） | 传统 Web 应用 | NextAuth.js / Auth.js |
| JWT | 首先通过 API 进行认证，适用于移动客户端 | jose, custom |
| 仅使用 OAuth | 适用于社交登录场景，快速集成 | NextAuth.js |
| Passkeys/WebAuthn | 现代化的无密码认证方案 | SimpleWebAuthn |
| 第三方认证服务 | 适用于企业级应用，符合安全规范 | Clerk, Auth0, Supabase Auth |

### 中间件用于实现认证

```tsx
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

const publicRoutes = ['/', '/login', '/register', '/api/webhooks']
const authRoutes = ['/login', '/register']

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl
  const token = request.cookies.get('session')?.value

  // Public routes — allow
  if (publicRoutes.some(route => pathname.startsWith(route))) {
    // Redirect authenticated users away from auth pages
    if (token && authRoutes.some(route => pathname.startsWith(route))) {
      return NextResponse.redirect(new URL('/dashboard', request.url))
    }
    return NextResponse.next()
  }

  // Protected routes — require auth
  if (!token) {
    const loginUrl = new URL('/login', request.url)
    loginUrl.searchParams.set('callbackUrl', pathname)
    return NextResponse.redirect(loginUrl)
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/((?!_next/static|_next/image|favicon.ico|public).*)']
}
```

### 授权机制的设计

```tsx
// lib/auth/permissions.ts
type Permission = 'read' | 'write' | 'admin'
type Resource = 'posts' | 'users' | 'settings'

const rolePermissions: Record<string, Record<Resource, Permission[]>> = {
  admin: {
    posts: ['read', 'write', 'admin'],
    users: ['read', 'write', 'admin'],
    settings: ['read', 'write', 'admin']
  },
  editor: {
    posts: ['read', 'write'],
    users: ['read'],
    settings: ['read']
  },
  viewer: {
    posts: ['read'],
    users: [],
    settings: []
  }
}

export function can(role: string, resource: Resource, permission: Permission): boolean {
  return rolePermissions[role]?.[resource]?.includes(permission) ?? false
}

// Usage in Server Component
export default async function AdminPage() {
  const session = await getSession()
  if (!can(session.role, 'settings', 'admin')) {
    notFound()  // Don't reveal admin pages exist
  }
  return <AdminDashboard />
}
```

### 安全相关头部配置（next.config.ts）

```tsx
const securityHeaders = [
  { key: 'X-DNS-Prefetch-Control', value: 'on' },
  { key: 'Strict-Transport-Security', value: 'max-age=63072000; includeSubDomains; preload' },
  { key: 'X-Frame-Options', value: 'SAMEORIGIN' },
  { key: 'X-Content-Type-Options', value: 'nosniff' },
  { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
  { key: 'Permissions-Policy', value: 'camera=(), microphone=(), geolocation=()' },
  {
    key: 'Content-Security-Policy',
    value: `
      default-src 'self';
      script-src 'self' 'unsafe-eval' 'unsafe-inline';
      style-src 'self' 'unsafe-inline';
      img-src 'self' data: https:;
      font-src 'self';
      connect-src 'self' https://api.example.com;
      frame-ancestors 'none';
    `.replace(/\n/g, '')
  }
]
```

---

## 第 5 阶段：性能优化

### 核心 Web Vitals 指标

| 指标 | 合格标准 | 需要改进 | 表现较差 |
|--------|-------------------|-------------------|------|
| LCP（首屏加载时间） | <2.5 秒 | 2.5-4.0 秒 | >4.0 秒 |
| INP（输入处理时间） | <200 毫秒 | 200-500 毫秒 | >500 毫秒 |
| CLS（内容加载时间） | <0.1 秒 | 0.1-0.25 秒 | >0.25 秒 |
| TTFB（总页加载时间） | <800 毫秒 | 800-1.8 秒 | >1.8 秒 |
| FCP（首次内容绘制时间） | <1.8 秒 | 1.8-3.0 秒 | >3.0 秒 |

### 图像优化

```tsx
import Image from 'next/image'

// ✅ Always use next/image
<Image
  src="/hero.jpg"
  alt="Hero image"
  width={1200}
  height={630}
  priority  // LCP image — load immediately
  sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
  placeholder="blur"
  blurDataURL={shimmer}  // Base64 placeholder
/>

// For dynamic images
<Image
  src={user.avatar}
  alt={user.name}
  width={48}
  height={48}
  loading="lazy"  // Below fold — lazy load
/>
```

### 图像处理规则：

1. **为首页图像设置优先级**（例如 hero 图像）
2. **为所有图像提供正确的尺寸** — 避免加载过大的图像
3. **对大图像使用 `placeholder="blur"` | 防止内容加载时间过长（CLS）
4. 在 `next.config.ts` 中配置外部图像的加载规则
5. **使用 WebP/AVIF 格式** — Next.js 会自动转换图像格式

### 包大小优化

```tsx
// next.config.ts
const nextConfig = {
  // Strict mode for catching bugs
  reactStrictMode: true,
  
  // Optimize packages
  experimental: {
    optimizePackageImports: [
      'lucide-react',
      '@radix-ui/react-icons',
      'date-fns',
      'lodash-es'
    ]
  },
  
  // Bundle analyzer (dev only)
  // npm install @next/bundle-analyzer
  ...(process.env.ANALYZE === 'true' && {
    webpack: (config) => {
      const { BundleAnalyzerPlugin } = require('webpack-bundle-analyzer')
      config.plugins.push(new BundleAnalyzerPlugin({ analyzerMode: 'static' }))
      return config
    }
  })
}
```

### 对于复杂组件的动态导入

```tsx
import dynamic from 'next/dynamic'

// Heavy chart library — only load when needed
const Chart = dynamic(() => import('@/components/chart'), {
  loading: () => <ChartSkeleton />,
  ssr: false  // Client-only component
})

// Code editor — definitely client-only
const CodeEditor = dynamic(() => import('@/components/code-editor'), {
  ssr: false
})
```

### 字体优化

```tsx
// app/layout.tsx
import { Inter, JetBrains_Mono } from 'next/font/google'

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter'
})

const jetbrains = JetBrains_Mono({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-mono'
})

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={`${inter.variable} ${jetbrains.variable}`}>
      <body className="font-sans">{children}</body>
    </html>
  )
}
```

### 性能预算

| 资源类型 | 预算限制 | 使用工具 |
|----------|--------|------|
| 首次加载的 JavaScript 代码 | <100KB | 使用 `next build` 工具生成 |
| 每个页面的 JavaScript 代码 | <50KB | 使用 Bundle Analyzer 工具 |
| 页面总大小 | <500KB | 使用 Lighthouse 工具 |
| 首页图像 | <200KB | Next.js 的 `next/image` 模块负责处理 |
| 第三方脚本 | 总大小 <50KB | 使用 Script Component 工具 |
| Web 字体 | <100KB | 使用 Next.js 的 `next/font` 模块处理 |

---

## 第 6 阶段：数据库与 ORM（对象关系映射）

### 选择合适的 ORM 工具

| ORM | 适用场景 | 优缺点 |
|-----|----------|-----------|
| Drizzle | 类型安全、轻量级、类似 SQL 的接口 | 新兴的开发框架 |
| Prisma | 适用于快速原型设计，支持基于模式的开发 | 重量较大，某些功能有限 |
| Kysely | 类型安全，支持原始 SQL 语法 | 更依赖手动配置，不支持迁移 |
| 原始 SQL（如 PostgreSQL/MySQL2） | 性能最佳，但缺乏类型安全性和迁移支持 |

### 推荐的 Drizzle 配置方式

```tsx
// lib/db/index.ts
import { drizzle } from 'drizzle-orm/node-postgres'
import { Pool } from 'pg'
import * as schema from './schema'

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 20,
  idleTimeoutMillis: 30000
})

export const db = drizzle(pool, { schema })

// lib/db/schema.ts
import { pgTable, text, timestamp, uuid, boolean } from 'drizzle-orm/pg-core'

export const users = pgTable('users', {
  id: uuid('id').defaultRandom().primaryKey(),
  email: text('email').notNull().unique(),
  name: text('name').notNull(),
  role: text('role', { enum: ['admin', 'editor', 'viewer'] }).default('viewer'),
  emailVerified: boolean('email_verified').default(false),
  createdAt: timestamp('created_at').defaultNow(),
  updatedAt: timestamp('updated_at').defaultNow()
})
```

### 无服务器架构（Serverless）下的连接池管理

```tsx
// For Vercel/serverless — use connection pooler
// Neon: use pooler URL (port 5432 → 6543)
// Supabase: use Supavisor URL
// PlanetScale: serverless driver built-in

// lib/db/index.ts (serverless-safe)
import { neon } from '@neondatabase/serverless'
import { drizzle } from 'drizzle-orm/neon-http'

const sql = neon(process.env.DATABASE_URL!)
export const db = drizzle(sql)
```

---

## 第 7 阶段：测试策略

### Next.js 的测试体系

| 测试层级 | 使用工具 | 测试内容 | 目标测试覆盖率 |
|-------|------|-------------|-----------------|
| 单元测试 | Vitest | 测试工具、钩子函数、纯函数 | 覆盖率超过 80% |
| 组件测试 | 使用专门的测试库 + Vitest | UI 组件、表单逻辑 | 覆盖率超过 70% |
| 集成测试 | 使用测试库 | 基于模拟数据的页面级测试 | 关键业务流程 |
| E2E（端到端）测试 | 使用 Playwright | 关键用户流程 | 覆盖率 5-10% |
| 可视化测试 | 使用 Playwright 的截图功能 | 检查 UI 的回归问题 | 关键页面 |

### Vitest 的配置方法

```tsx
// vitest.config.ts
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import tsconfigPaths from 'vite-tsconfig-paths'

export default defineConfig({
  plugins: [react(), tsconfigPaths()],
  test: {
    environment: 'jsdom',
    setupFiles: ['./tests/setup.ts'],
    include: ['**/*.test.{ts,tsx}'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'lcov'],
      exclude: ['**/*.config.*', '**/types/**']
    }
  }
})
```

### 服务器端组件的测试方法

```tsx
// Server Components can be tested as async functions
import { render } from '@testing-library/react'
import Page from '@/app/dashboard/page'

// Mock the data fetching
vi.mock('@/lib/db', () => ({
  getUser: vi.fn().mockResolvedValue({ id: '1', name: 'Test' })
}))

test('dashboard page renders user name', async () => {
  const Component = await Page()  // Call as async function
  const { getByText } = render(Component)
  expect(getByText('Test')).toBeInTheDocument()
})
```

### 使用 Playwright 进行端到端测试的示例

```tsx
// e2e/auth.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Authentication', () => {
  test('login flow', async ({ page }) => {
    await page.goto('/login')
    await page.fill('[name="email"]', 'test@example.com')
    await page.fill('[name="password"]', 'password123')
    await page.click('button[type="submit"]')
    
    await expect(page).toHaveURL('/dashboard')
    await expect(page.getByText('Welcome')).toBeVisible()
  })
  
  test('protected route redirects', async ({ page }) => {
    await page.goto('/dashboard')
    await expect(page).toHaveURL(/\/login/)
  })
})
```

---

## 第 8 阶段：错误处理与监控

### 错误处理的架构设计

```
app/
├── global-error.tsx     # Catches root layout errors (must include <html>)
├── error.tsx            # Catches app-level errors
├── not-found.tsx        # 404 page
├── (dashboard)/
│   ├── error.tsx        # Dashboard-specific errors
│   └── settings/
│       └── error.tsx    # Settings-specific errors
```

### 错误处理组件的实现方式

```tsx
// app/error.tsx
'use client'

import { useEffect } from 'react'

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  useEffect(() => {
    // Log to error tracking service
    console.error('Application error:', error)
    // Sentry.captureException(error)
  }, [error])

  return (
    <div className="flex flex-col items-center justify-center min-h-[400px]">
      <h2 className="text-2xl font-bold">Something went wrong</h2>
      <p className="text-gray-500 mt-2">
        {error.digest ? `Error ID: ${error.digest}` : error.message}
      </p>
      <button
        onClick={reset}
        className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
      >
        Try again
      </button>
    </div>
  )
}
```

### 结构化的日志记录

```tsx
// lib/logger.ts
type LogLevel = 'debug' | 'info' | 'warn' | 'error'

function log(level: LogLevel, message: string, meta?: Record<string, unknown>) {
  const entry = {
    timestamp: new Date().toISOString(),
    level,
    message,
    ...meta,
    // Add request context if available
    ...(meta?.requestId && { requestId: meta.requestId })
  }
  
  if (level === 'error') {
    console.error(JSON.stringify(entry))
  } else {
    console.log(JSON.stringify(entry))
  }
}

export const logger = {
  debug: (msg: string, meta?: Record<string, unknown>) => log('debug', msg, meta),
  info: (msg: string, meta?: Record<string, unknown>) => log('info', msg, meta),
  warn: (msg: string, meta?: Record<string, unknown>) => log('warn', msg, meta),
  error: (msg: string, meta?: Record<string, unknown>) => log('error', msg, meta)
}
```

---

## 第 9 阶段：部署与基础设施

### 平台选择

| 平台 | 适用场景 | 优势 | 数据库选择 | 成本（个人/商业用途） |
|--------|----------|------|-----|---------------|
| Vercel | Next.js 的默认开发工具，最佳集成体验 | ✅ | 支持外部服务 | 免费 → 每月 20 美元 |
| Cloudflare Pages | 优先使用服务器端渲染，支持 Workers | ✅ | 使用 D1 和 KV 存储 | 免费 → 每月 5 美元 |
| AWS Amplify | 与 AWS 生态系统集成 | ✅ | 支持 RDS 和 DynamoDB | 按使用量计费 |
| Railway | 全栈开发框架，支持 Docker | ✌ | 内置 PostgreSQL | 每月 5 美元 |
| Fly.io | 全球范围内可用，支持 Docker | ✅ | 内置 PostgreSQL | 按使用量计费 |
| 自托管（使用 Docker） | 提供最大程度的控制权 | ✌ | 需自行配置服务器 | 需支付服务器费用 |

### Docker 环境下的生产环境搭建

```dockerfile
# Dockerfile
FROM node:20-alpine AS base
RUN corepack enable

FROM base AS deps
WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
ENV NEXT_TELEMETRY_DISABLED=1
RUN pnpm build

FROM base AS runner
WORKDIR /app
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs
EXPOSE 3000
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

CMD ["node", "server.js"]
```

```tsx
// next.config.ts — required for standalone
const nextConfig = {
  output: 'standalone'
}
```

### CI/CD 流程（使用 GitHub Actions）

```yaml
# .github/workflows/ci.yml
name: CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: pnpm
      - run: pnpm install --frozen-lockfile
      - run: pnpm tsc --noEmit
      - run: pnpm lint
      - run: pnpm test -- --coverage
      - run: pnpm build
      
  e2e:
    runs-on: ubuntu-latest
    needs: quality
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: pnpm
      - run: pnpm install --frozen-lockfile
      - run: pnpm exec playwright install --with-deps
      - run: pnpm build
      - run: pnpm exec playwright test
      - uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: playwright-report
          path: playwright-report/
```

### 环境变量的配置

```tsx
// env.ts — runtime validation with t3-env
import { createEnv } from '@t3-oss/env-nextjs'
import { z } from 'zod'

export const env = createEnv({
  server: {
    DATABASE_URL: z.string().url(),
    AUTH_SECRET: z.string().min(32),
    STRIPE_SECRET_KEY: z.string().startsWith('sk_'),
    REDIS_URL: z.string().url().optional(),
  },
  client: {
    NEXT_PUBLIC_APP_URL: z.string().url(),
    NEXT_PUBLIC_STRIPE_KEY: z.string().startsWith('pk_'),
  },
  runtimeEnv: {
    DATABASE_URL: process.env.DATABASE_URL,
    AUTH_SECRET: process.env.AUTH_SECRET,
    STRIPE_SECRET_KEY: process.env.STRIPE_SECRET_KEY,
    REDIS_URL: process.env.REDIS_URL,
    NEXT_PUBLIC_APP_URL: process.env.NEXT_PUBLIC_APP_URL,
    NEXT_PUBLIC_STRIPE_KEY: process.env.NEXT_PUBLIC_STRIPE_KEY,
  },
})
```

---

## 第 10 阶段：常见开发模式与最佳实践

### 优化更新流程

```tsx
'use client'
import { useOptimistic, useTransition } from 'react'
import { toggleTodo } from '@/actions/todos'

export function TodoItem({ todo }: { todo: Todo }) {
  const [optimisticTodo, setOptimisticTodo] = useOptimistic(todo)
  const [, startTransition] = useTransition()

  return (
    <label>
      <input
        type="checkbox"
        checked={optimisticTodo.completed}
        onChange={() => {
          startTransition(async () => {
            setOptimisticTodo({ ...todo, completed: !todo.completed })
            await toggleTodo(todo.id)
          })
        }}
      />
      {optimisticTodo.title}
    </label>
  )
}
```

### 实现无限滚动功能

```tsx
'use client'
import { useInView } from 'react-intersection-observer'
import { useEffect, useState, useTransition } from 'react'
import { loadMore } from '@/actions/feed'

export function InfiniteList({ initialItems }: { initialItems: Item[] }) {
  const [items, setItems] = useState(initialItems)
  const [cursor, setCursor] = useState(initialItems.at(-1)?.id)
  const [hasMore, setHasMore] = useState(true)
  const [isPending, startTransition] = useTransition()
  const { ref, inView } = useInView()

  useEffect(() => {
    if (inView && hasMore && !isPending) {
      startTransition(async () => {
        const newItems = await loadMore(cursor)
        if (newItems.length === 0) {
          setHasMore(false)
        } else {
          setItems(prev => [...prev, ...newItems])
          setCursor(newItems.at(-1)?.id)
        }
      })
    }
  }, [inView, hasMore, isPending, cursor])

  return (
    <div>
      {items.map(item => <ItemCard key={item.id} item={item} />)}
      {hasMore && <div ref={ref}>{isPending ? <Spinner /> : null}</div>}
    </div>
  )
}
```

### 基于 URL 状态实现搜索功能

```tsx
'use client'
import { useRouter, useSearchParams, usePathname } from 'next/navigation'
import { useDebouncedCallback } from 'use-debounce'

export function SearchBar() {
  const router = useRouter()
  const pathname = usePathname()
  const searchParams = useSearchParams()

  const handleSearch = useDebouncedCallback((term: string) => {
    const params = new URLSearchParams(searchParams)
    if (term) {
      params.set('q', term)
      params.set('page', '1')
    } else {
      params.delete('q')
    }
    router.replace(`${pathname}?${params.toString()}`)
  }, 300)

  return (
    <input
      type="search"
      placeholder="Search..."
      defaultValue={searchParams.get('q') ?? ''}
      onChange={e => handleSearch(e.target.value)}
    />
  )
}
```

### 使用 URL 状态实现多步骤表单功能

```tsx
// app/onboarding/page.tsx
export default function OnboardingPage({
  searchParams
}: {
  searchParams: { step?: string }
}) {
  const step = Number(searchParams.step) || 1
  
  return (
    <div>
      <ProgressBar step={step} total={4} />
      {step === 1 && <StepOne />}
      {step === 2 && <StepTwo />}
      {step === 3 && <StepThree />}
      {step === 4 && <StepFour />}
    </div>
  )
}
```

---

## 第 11 阶段：生产环境前的检查清单

### 必须完成的事项：

- [ ] 使用 `next build` 命令构建项目，且没有警告信息
- [ ] 代码中严格使用 TypeScript，避免使用 `any` 类型
- [ ] 所有环境变量都已验证（使用 t3-env 或手动配置）
- [ ] 安全相关头部配置正确（CSP、HSTS、X-Frame-Options）
- [ ] 完成了认证与授权功能的测试（包括关键业务流程）
- [ ] 每个路由层级都设置了错误处理机制
- [ ] 404 和 500 错误页面已自定义
- [ ] 配置了 Favicon、OG 图像和 meta 标签
- [ ] 核心 Web Vitals 指标达标（使用 Lighthouse 工具检测）
- [ ] 在真实设备上测试了移动设备的响应性
- [ ] 完成了无障碍访问性审计（使用 axe、键盘导航、屏幕阅读器等工具）
- [ ] 对 API 路由和服务器端操作进行了速率限制
- [ ] 正确配置了 CORS（跨源资源共享）
- [ ] 为无服务器架构配置了数据库连接池
- [ ] 已连接监控和错误跟踪工具（如 Sentry）

### 建议额外完成的事项：

- [ ] 对关键用户流程进行端到端测试
- [ ] 确保包大小在预算范围内（首次加载时小于 100KB）
- [ ] 图像优化已完成（使用 next/image 工具，确保图像尺寸正确）
- [ ] 配置了 Sitemap.xml 和 robots.txt 文件
- [ ] 安装了分析工具（如 PostHog）
- [ ] 测试了预览版本的部署效果
- [ ] 编写了回滚方案
- [ ] 完成了负载测试
- [ ] 验证了 CDN 的缓存效果
- [ ] 在生产环境中测试了相关的中间件

---

## 第 12 阶段：避免常见错误与故障排除

### Next.js 开发中的 10 个常见错误及解决方法

| 错误编号 | 错误描述 | 解决方法 |
|---|---------|-----|
| 1 | 在每个文件的顶部都写 `use client` | 应将客户端处理逻辑放在代码的底层 |
| 2 | 使用 `useEffect` 来获取数据 | 应在服务器端组件中使用数据获取逻辑，或使用 SWR/React Query |
| 3 | 未使用 `loading.tsx` 文件 | 应添加加载状态提示，避免页面布局混乱 |
| 4 | 忽略了包大小的优化 | 运行 `next build` 命令并检查输出结果，使用动态导入机制 |
| 5 | 未设置错误处理逻辑 | 在每个路由层级添加 `error.tsx` 文件 |
| 6 | 将敏感信息存储在 `NEXT_PUBLIC_*` 变量中 | 敏感信息应仅存储在服务器端环境变量中，并使用 t3-env 进行验证 |
| 7 | 未为图像设置正确的尺寸属性 | 必须为所有图像提供正确的尺寸信息 |
| 8 | 数据获取顺序不合理 | 应使用 `Promise.all()` 来并行获取数据 |
| 9 | 所有数据都缓存或都不缓存 | 应根据数据类型制定明确的缓存策略 |
| 10 | 未使用 `revalidateTag` | 应根据标签来控制数据的缓存策略 |

### 故障排除的参考流程

```
Build error?
├── "Module not found" → Check import paths, tsconfig paths
├── "Server Component error" → Remove "use client" or move hooks to client component
├── "Hydration mismatch" → Check for browser-only code in shared components
│   → Use suppressHydrationWarning for timestamps
│   → Wrap in useEffect or dynamic(ssr: false)
├── "Edge runtime error" → Check node APIs (fs, crypto) not available at edge
└── Slow build → Check for large static generation, reduce ISR pages

Runtime error?
├── 500 on production → Check error.tsx, logs, Sentry
├── Slow TTFB → Check database queries, add caching
├── CLS → Add explicit dimensions to images/embeds
├── High JS bundle → Run bundle analyzer, dynamic import heavy libs
└── Stale data → Check revalidation settings, revalidateTag
```

---

## 推荐的开发栈（2025 年及以后的推荐配置）

| 技术层 | 推荐方案 | 选择理由 |
|-------|---------------|-----|
| 开发框架 | Next.js 15 及以上版本（推荐使用 App Router） | 支持服务器端组件、流式数据加载和服务器端操作 |
| 编程语言 | 使用 TypeScript（严格模式） | 提供类型安全性和更好的开发体验 |
| 样式设计 | 使用 Tailwind CSS 4 | 代码简洁，无需运行时额外开销 |
| UI 组件 | 使用 shadcn/ui | 可复制粘贴，易于定制 |
| 表单处理 | 使用 react-hook-form 和 Zod 库 | 提供类型安全的验证功能 |
| 数据库连接层 | 使用 Drizzle | 类型安全、轻量级，语法类似 SQL |
| 数据库选择 | 使用 PostgreSQL（Neon/Supabase） | 适合无服务器架构，易于使用 |
| 认证机制 | 使用 Auth.js（NextAuth v5） | 专为 Next.js 设计 |
| 支付处理 | 使用 Stripe | 行业标准的支付解决方案 |
| 托管服务 | 使用 Vercel | 最适合 Next.js 的开发环境 |
| 测试工具 | 使用 Vitest 和 Playwright | 提供快速的单元测试和可靠的端到端测试 |
| 监控工具 | 使用 Sentry | 提供错误跟踪和性能监控功能 |
| 分析工具 | 使用 PostHog | 提供详细的分析数据 |

## 质量评估标准（0-100 分）

| 评估维度 | 权重 | 分数 |
|-----------|--------|---------|
| 架构设计（包括组件边界和代码结构） | 20% | 0-20 分 |
| 性能（包括核心 Web Vitals、包大小、首页加载时间） | 20% | 0-20 分 |
| 安全性（包括认证、头部配置、数据验证） | 15% | 0-15 分 |
| 数据处理（包括缓存、数据获取、数据库交互） | 15% | 0-15 分 |
| 测试（包括测试框架、覆盖率和端到端测试） | 10% | 0-10 分 |
| 错误处理（包括错误处理机制和日志记录） | 10% | 0-10 分 |
| 开发流程（包括代码类型检查、持续集成） | 5% | 0-5 分 |
| 部署环境（包括 Docker 使用、监控工具） | 5% | 0-5 分 |

**总分：** 90-100 分：应用程序达到高级水平 | 75-89 分：具备生产环境所需的条件 | 60-74 分：需要进一步优化 | <60 分：尚未达到生产环境标准 |

---

## 常用命令说明：

1. “设置一个新的 Next.js 项目” → 按照第 1 阶段的架构设计和代码结构进行配置 |
2. “添加认证功能” → 按照第 4 阶段的推荐方案进行认证和授权配置 |
3. “优化性能” → 按照第 5 阶段的建议完成所有性能优化工作 |
4. “设置测试环境” → 按照第 7 阶段的步骤搭建完整的测试体系 |
5. “部署到生产环境” → 按照第 9 阶段的建议选择合适的平台并配置 CI/CD 流程 |
6. “修复程序中的错误” | 参考第 12 阶段的故障排除指南 |
7. “添加缓存功能” | 按照第 2 阶段的建议配置缓存策略 |
8. “创建一个服务器端操作” | 按照第 3 阶段的最佳实践进行开发 |
9. “审计我的应用程序” | 执行快速健康检查，并完成第 11 阶段的检查清单 |
10. “添加错误处理机制” | 按照第 8 阶段的建议配置错误处理逻辑 |
11. “实现搜索功能” | 按照第 10 阶段的建议实现基于 URL 状态的搜索功能 |
12. “审查我的应用程序架构” | 根据第 1 阶段的建议重新评估架构设计 |

---

*由 AfrexAI 自动生成。AfrexAI 是一家专注于自动化开发的智能公司。*