---
name: nextjs
model: standard
description: Next.js 应用程序路由器的最佳实践 —— 服务器组件、数据获取、缓存、路由、中间件、元数据、错误处理、流式传输、服务器动作以及针对 Next.js 14-16+ 版本的性能优化。
keywords: [next.js, nextjs, app router, server components, rsc, server actions, streaming, suspense, parallel routes, intercepting routes, metadata, middleware, caching, revalidation, image optimization, font optimization]
user-invocable: false
---

# Next.js 应用程序路由器

在构建、审查或调试 Next.js 应用程序的路由器时，请遵循以下模式。

## 安装

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install nextjs
```

## 适用场景

- 构建使用路由器（Router）的 Next.js 应用程序
- 从 Pages Router 迁移到 App Router
- 实现服务器组件（Server Components）和流式数据传输（streaming）
- 设置并行路由（parallel routes）和拦截路由（intercepting routes）
- 优化数据获取和缓存（data fetching and caching）
- 使用服务器动作（Server Actions）构建全栈功能
- 调试数据加载错误（hydration errors）或 RSC（React Server Components）边界问题

## 渲染模式

| 模式 | 渲染位置 | 适用场景 |
|------|-------|-------------|
| **服务器组件** | 仅在服务器端 | 数据获取、敏感信息处理、复杂计算 |
| **客户端组件** | 浏览器端 | 交互性、钩子（hooks）、浏览器 API |
| **静态渲染（SSG, Static Site Generation）** | 构建时 | 假设内容很少变化 |
| **动态渲染（SSR, Server-Side Rendering）** | 请求时 | 需要个性化或实时更新的数据 |
| **流式渲染** | 逐步加载（progressive loading） | 大型页面、数据源加载缓慢 |

### 服务器与客户端决策树

```
Does it need...?
├── useState, useEffect, event handlers, browser APIs
│   └── Client Component ('use client')
├── Direct data fetching, no interactivity
│   └── Server Component (default)
└── Both?
    └── Split: Server parent fetches data → Client child handles UI
```

## 文件规范

有关完整规范，请参阅 [file-conventions.md](references/file-conventions.md)。

```
app/
├── layout.tsx          # Shared UI wrapper (persists across navigations)
├── page.tsx            # Route UI
├── loading.tsx         # Suspense fallback (automatic)
├── error.tsx           # Error boundary (must be 'use client')
├── not-found.tsx       # 404 UI
├── route.ts            # API endpoint (cannot coexist with page.tsx)
├── template.tsx        # Like layout but re-mounts on navigation
├── default.tsx         # Parallel route fallback
└── opengraph-image.tsx # OG image generation
```

路由段说明：
- `[slug]`：动态路由
- `[...slug]`：通用路由
- `[[...slug]]`：可选的通用路由
- `(group)`：路由组
- `@slot`：并行路由
- `_folder`：私有文件夹（不参与路由处理）

## 数据获取模式

为每种使用场景选择合适的模式。有关详细信息，请参阅 [data-patterns.md](references/data-patterns.md)。

| 模式 | 适用场景 | 缓存策略 |
|---------|----------|---------|
| 服务器组件获取数据 | 内部数据读取（推荐） | 全部使用 Next.js 的缓存机制 |
| 服务器动作（Server Action） | 数据更新、表单提交 | 仅使用 POST 请求，不缓存 |
- 路由处理器（Route Handler） | 外部 API、Webhook、公共 REST 请求 | GET 请求可以缓存 |
- 客户端获取数据 → API | 客户端读取（最后手段） | 使用 HTTP 缓存头（HTTP cache headers）

### 服务器组件数据获取（推荐）

```tsx
// app/products/page.tsx — Server Component by default
export default async function ProductsPage() {
  const products = await db.product.findMany() // Direct DB access, no API layer
  return <ProductGrid products={products} />
}
```

## 避免数据瀑布效应（Avoiding Data Waterfalls）

```tsx
// BAD: Sequential — each awaits before the next starts
const user = await getUser()
const posts = await getPosts()

// GOOD: Parallel fetching
const [user, posts] = await Promise.all([getUser(), getPosts()])

// GOOD: Streaming with Suspense — each section loads independently
<Suspense fallback={<UserSkeleton />}><UserSection /></Suspense>
<Suspense fallback={<PostsSkeleton />}><PostsSection /></Suspense>
```

## 服务器动作（Server Actions）

```tsx
// app/actions.ts
'use server'
import { revalidateTag } from 'next/cache'

export async function addToCart(productId: string) {
  const cookieStore = await cookies()
  const sessionId = cookieStore.get('session')?.value
  if (!sessionId) redirect('/login')

  await db.cart.upsert({
    where: { sessionId_productId: { sessionId, productId } },
    update: { quantity: { increment: 1 } },
    create: { sessionId, productId, quantity: 1 },
  })
  revalidateTag('cart')
  return { success: true }
}
```

## 缓存策略

| 方法 | 语法 | 适用场景 |
|--------|--------|----------|
| 不缓存 | `fetch(url, { cache: 'no-store' })` | 始终获取最新数据 |
| 静态数据 | `fetch(url, { cache: 'force-cache' })` | 数据很少变化 |
- 基于时间的更新 | `fetch(url, { next: { revalidate: 60 } })` | 定期更新数据 |
- 基于标签的更新 | `fetch(url, { next: { tags: ['products'] } })` | 根据标签动态更新数据 |

**注意：** 从服务器动作（Server Actions）发起的数据更新必须能够被序列化为 JSON 格式（JSON-serializable）。

**关键规则：** 客户端组件（Client Components）不能是异步的（async）。应在服务器组件中获取数据，然后将其传递给客户端组件。

## 异步 API（Next.js 15 及以上版本）

`params`、`searchParams`、`cookies()` 和 `headers()` 都是异步操作。有关详细信息，请参阅 [async-patterns.md](references/async-patterns.md)。

```tsx
// Pages and layouts — always await params
type Props = { params: Promise<{ slug: string }> }

export default async function Page({ params }: Props) {
  const { slug } = await params
}

// Server functions
const cookieStore = await cookies()
const headersList = await headers()

// Non-async components — use React.use()
import { use } from 'react'
export default function Page({ params }: Props) {
  const { slug } = use(params)
}
```

## 路由模式

### 路由组织结构

| 模式 | 语法 | 用途 |
|---------|--------|---------|
| 路由组 | `(marketing)/` | 逻辑组织路由，不影响 URL 结构 |
| 并行路由 | `@analytics/` | 在同一布局中展示多个独立的部分 |
- 拦截路由 | `(.)photos/[id]` | 在导航操作时显示模态框 |
- 私有文件夹 | `_components/` | 不参与路由处理 |

### 并行路由与模态框

有关模态框的详细信息，请参阅 [parallel-routes.md](references/parallel-routes.md)。

**重要规则：**
- 每个 `@slot` 文件夹必须包含一个 `default.tsx` 文件（该文件应返回 `null`），否则页面在刷新时会显示 404 错误。
- 使用 `router.back()` 关闭模态框，**禁止** 使用 `router.push()` 或 `<Link>`。
- 拦截路由的匹配器：`(.)` 表示同一层级路由，`(..)` 表示上一层级路由，`(...)` 表示从根目录开始的路由。

## 元数据与 SEO

有关元数据（Metadata）的详细信息，请参阅 [metadata.md](references/metadata.md)，包括原始图片（OG images）、站点地图（sitemaps）和文件规范。

**注意：** 元数据仅适用于服务器组件（Metadata is Server Components）。如果页面使用了 `use client`，请将元数据提取到父布局中。

## 错误处理

有关错误处理的详细信息，请参阅 [error-handling.md](references/error-handling.md)，包括身份验证错误（auth errors）的处理方式。

**重要提示：** `redirect()`、`notFound()`、`forbidden()` 和 `unauthorized()` 会抛出特殊的错误。切勿在 `try/catch` 块中捕获这些错误。

```tsx
// BAD: redirect throw is caught — navigation fails!
try {
  await db.post.create({ data })
  redirect(`/posts/${post.id}`)
} catch (error) {
  return { error: 'Failed' } // Catches the redirect too!
}

// GOOD: Call redirect outside try-catch
let post
try { post = await db.post.create({ data }) }
catch (error) { return { error: 'Failed' } }
redirect(`/posts/${post.id}`)
```

## 使用 Suspense 实现流式渲染

```tsx
export default async function ProductPage({ params }: Props) {
  const { id } = await params
  const product = await getProduct(id) // Blocking — loads first

  return (
    <div>
      <ProductHeader product={product} />
      <Suspense fallback={<ReviewsSkeleton />}>
        <Reviews productId={id} />       {/* Streams in independently */}
      </Suspense>
      <Suspense fallback={<RecommendationsSkeleton />}>
        <Recommendations productId={id} /> {/* Streams in independently */}
      </Suspense>
    </div>
  )
}
```

### 需要 Suspense 的钩子

| 需要 Suspense 的钩子 | 说明 |
|------|-------------------|
| `useSearchParams()` | 总是需要 Suspense，否则整个页面会变成客户端渲染（CSR） |
| `usePathname()` | 在动态路由中需要 Suspense |
| `useParams()` | 不需要 Suspense |
| `useRouter()` | 不需要 Suspense |

## 性能优化

- **始终使用 `next/image` 而不是 `<img>` — 详见 [image-optimization.md](references/image-optimization.md) |
- **始终使用 `next/link` 而不是 `<a>` — 实现客户端导航并预加载资源 |
- **始终使用 `next/font` — 详见 [font-optimization.md](references/font-optimization.md) |
- **始终使用 `next/script` — 详见 [scripts.md](references/scripts.md) |
- 为重要的图片设置 `priority` 属性（LCP, Loading Critical Pictures） |
- 使用 `sizes` 属性来控制图片大小 — 不设置此属性会导致下载最大的图片版本 |
- 对于复杂的客户端组件，使用动态导入：`const Chart = dynamic(() => import('./Chart'))`
- 使用 `generateStaticParams` 在构建时预渲染动态路由

## 路由处理器（Route Handlers）

有关 API 端点的详细信息，请参阅 [route-handlers.md](references/route-handlers.md)。

## 打包（Bundling）

有关解决第三方包问题、服务器不兼容包以及 ESM（ESM）/CommonJS 相关问题的方法，请参阅 [bundling.md](references/bundling.md)。

## 数据加载错误（Hydration Errors）

有关数据加载错误的成因及解决方法，请参阅 [hydration-errors.md](references/hydration-errors.md)。

| 原因 | 解决方法 |
|-------|-----|
- 浏览器 API（如 `window`、`localStorage`） | 客户端组件中需要使用 `useEffect` 进行渲染检查 |
- `new Date().toLocaleString()` | 在客户端使用 `useEffect` 进行渲染 |
- 使用 `Math.random()` 生成 ID 时 | 使用 `useId()` 钩子 |
- 错误的 HTML 结构（如 `<p><div>...</div></p>` | 修复无效的 HTML 标签嵌套 |
- 第三方脚本修改 DOM 时 | 使用 `next/script` 并设置 `afterInteractive` 属性

## 自托管（Self-Hosting）

有关 Docker、PM2、缓存处理以及部署的详细信息，请参阅 [self-hosting.md](references/self-hosting.md)。

**关键点：**
- 使用 `output: 'standalone'` 选项进行 Docker 托管 — 生成最小的生产版本包 |
- 分别复制 `public/` 和 `.next/static/` 文件夹（它们不包含在独立版本包中） |
- 为容器设置 `HOSTNAME="0.0.0.0"` |
- 多实例场景需要自定义缓存处理（如 Redis/S3） — 文件系统缓存可能导致问题 |
- 设置健康检查端点为 `/api/health`

## 绝对不要做的事情

| 绝对不要 | 原因 | 替代方案 |
|-------|-----|---------|
- 默认启用 `use client` | 会导致客户端包体积增大，失去服务器组件的优势 | 服务器组件是默认设置——仅在需要交互性时启用 `use client` |
- 将客户端组件设置为异步（async） | 不被支持，可能导致程序崩溃 | 应在服务器组件中获取数据，并将其作为属性传递给客户端组件 |
- 将 `Date`、`Map` 或函数传递给客户端 | 这些数据无法在 RSC 边界之间进行序列化 | 应将它们序列化为字符串或普通对象 |
- 在服务器组件中直接从自己的 API 获取数据 | 不必要地增加网络请求 | 直接访问数据库或服务 |
- 在 `try-catch` 块中捕获 `redirect()`、`notFound()`、`forbidden()` 等错误 | 这些错误会隐藏在异常处理中 | 应在 `try-catch` 之外处理这些错误 |
- 跳过 `loading.tsx` 或 Suspense 备用方案 | 用户在数据加载时可能会看到空白页面 | 必须提供加载状态提示 |
- 在没有 Suspense 的情况下使用 `useSearchParams` | 会导致整个页面变成客户端渲染 | 应使用 `<Suspense>` 来处理加载状态 |
- 使用 `router.push()` 关闭模态框 | 会破坏浏览历史记录，导致模态框突然关闭 | 应使用 `router.back()` |
- 使用 `@vercel/og` 生成原始图片 | Next.js 已经内置了相关功能 | 应从 `next/og` 导入图片 |
- 在并行路由中省略 `default.tsx` 文件 | 这会导致页面刷新时显示 404 错误 | 应添加返回 `null` 的 `default.tsx` 文件 |
- 除非必要，否则不使用 Edge 运行时环境 | 大多数 npm 包在 Edge 环境中无法正常工作 | 默认的 Node.js 运行时环境已经可以满足大部分需求 |
- 跳过 `sizes` 属性 | 会导致下载最大的图片版本 | 应设置 `sizes="100vw"` 或适当的尺寸属性 |
- 在多个组件中重复导入字体 | 会导致重复加载 | 应在布局文件中统一导入字体 |
- 使用 `<link>` 标签加载 Google 字体 | 无法优化渲染效果 | 应使用 `next/font` |

## 参考文件

| 文件 | 主题 |
|------|-------|
| [rsc-boundaries.md](references/rsc-boundaries.md) | 服务器/客户端边界规则、数据序列化 |
| [data-patterns.md](references/data-patterns.md) | 数据获取策略、避免数据瀑布效应 |
| [error-handling.md](references/error-handling.md) | 错误处理、重定向相关问题、身份验证错误 |
| [async-patterns.md](references/async-patterns.md) | Next.js 15 及以上版本中的异步参数、cookies、headers 的使用 |
| [metadata.md](references/metadata.md) | SEO、原始图片、站点地图、文件规范 |
| [parallel-routes.md](references/parallel-routes.md) | 模态框模式、拦截路由的相关注意事项 |
| [hydration-errors.md](references/hydration-errors.md) | 数据加载错误的成因及解决方法 |
| [self-hosting.md](references/self-hosting.md) | Docker 托管、PM2、缓存处理、部署相关内容 |
| [file-conventions.md](references/file-conventions.md) | 项目结构、特殊文件、中间件（middleware） |
| [bundling.md](references/bundling.md) | 第三方包、服务器渲染问题、Turbopack 打包工具 |
| [image-optimization.md](references/image-optimization.md) | `next/image` 的最佳实践 |
| [font-optimization.md](references/font-optimization.md) | `next/font` 的最佳实践 |
| [scripts.md](references/scripts.md) | `next/script` 的使用、第三方脚本的加载 |
| [route-handlers.md](references/route-handlers.md) | API 端点、请求/响应处理相关内容 |