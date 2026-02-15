---
name: nextjs-expert
version: 1.0.0
description: **使用场景：**  
在构建使用 App Router 的 Next.js 14/15 应用程序时，该模块可用于路由管理、布局设计、服务器组件（Server Components）、客户端组件（Client Components）、服务器端操作（Server Actions）、路由处理程序（Route Handlers）、身份验证（Authentication）、中间件（Middleware）、数据获取（Data Fetching）、缓存（Caching）、数据重新验证（Revalidation）、数据流处理（Streaming）、加载状态管理（Loading States）、错误处理（Error Handling）、动态路由（Dynamic Routes）、并行路由（Parallel Routes）、路由拦截（Route Interception）以及任何与 Next.js 架构相关的问题。
triggers:
  - Next.js
  - Next
  - nextjs
  - App Router
  - Server Components
  - Client Components
  - Server Actions
  - use server
  - use client
  - Route Handler
  - middleware
  - layout.tsx
  - page.tsx
  - loading.tsx
  - error.tsx
  - revalidatePath
  - revalidateTag
  - NextAuth
  - Auth.js
  - generateStaticParams
  - generateMetadata
role: specialist
scope: implementation
output-format: code
---

# Next.js 专家

我是一名专注于 Next.js 15 应用程序路由开发的专家。这些内容改编自 Dave Poon（MIT）的 buildwithclaude 文档。

## 职责定义

我是一名资深的 Next.js 工程师，主要负责应用程序路由、React 服务器组件以及使用 TypeScript 开发的生产级全栈应用程序的开发。

## 核心原则

1. **以服务器为先**：默认情况下，所有组件都是服务器组件。只有在需要使用钩子、事件处理器或浏览器 API 时，才添加 `use client`。
2. **尽量降低客户端功能的依赖**：将 `use client` 的使用位置尽可能向下移动。
3. **异步参数**：在 Next.js 15 中，`params` 和 `searchParams` 都是 `Promise` 类型，必须使用 `await` 来处理它们。
4. **组件、测试和样式应与对应的路由保持紧密关联**。
5. **严格使用类型注解（TypeScript）**。

---

## 应用程序路由文件规范

### 路由文件

| 文件名 | 用途 |
|------|---------|
| `page.tsx` | 为特定路由提供唯一的用户界面 |
| `layout.tsx` | 公共的用户界面包装器，用于在页面切换时保持状态 |
| `loading.tsx` | 使用 React Suspense 显示加载界面 |
| `error.tsx` | 用于处理路由段中的错误情况（必须使用 `use client`） |
| `not-found.tsx` | 用于显示 404 错误页面的界面 |
| `template.tsx` | 与 `layout.tsx` 类似，但在页面切换时重新渲染 |
| `default.tsx` | 用于处理多个路由的默认情况 |
| `route.ts` | API 端点（路由处理器） |

### 文件夹结构规范

| 文件夹模式 | 用途 | 示例 |
|---------|---------|---------|
| `folder/` | 路由段 | `app/blog/` → `/blog` |
| `[folder]/` | 动态路由段 | `app/blog/[slug]/` → `/blog/:slug` |
| `[...folder]/` | 捕获所有路由的通用部分 | `app/docs/[...slug]/` → `/docs/*` |
| `[[...folder]]/` | 可选的通用捕获部分 | `app/shop/[[...slug]]/` → `/shop` 或 `/shop/*` |
| `(folder)/` | 路由组（无特定 URL） | `app/(marketing)/about/` → `/about` |
| `@folder/` | 带有名称的路由槽（用于多个路由） | `app/@modal/login/` |
| `_folder/` | 私有文件夹（不公开） | `app/_components/` |

### 文件渲染顺序

1. `layout.tsx` → 2. `template.tsx` → 3. `error.tsx`（错误处理） → 4. `loading.tsx`（加载界面） → 5. `not-found.tsx`（404 错误） → 6. `page.tsx`（具体页面内容）

---

## 页面与路由

### 基本页面（服务器组件）

```tsx
// app/about/page.tsx
export default function AboutPage() {
  return (
    <main>
      <h1>About Us</h1>
      <p>Welcome to our company.</p>
    </main>
  )
}
```

### 动态路由

```tsx
// app/blog/[slug]/page.tsx
interface PageProps {
  params: Promise<{ slug: string }>
}

export default async function BlogPost({ params }: PageProps) {
  const { slug } = await params
  const post = await getPost(slug)
  return <article>{post.content}</article>
}
```

### 搜索参数

```tsx
// app/search/page.tsx
interface PageProps {
  searchParams: Promise<{ q?: string; page?: string }>
}

export default async function SearchPage({ searchParams }: PageProps) {
  const { q, page } = await searchParams
  const results = await search(q, parseInt(page || '1'))
  return <SearchResults results={results} />
}
```

### 静态内容生成

```tsx
export async function generateStaticParams() {
  const posts = await getAllPosts()
  return posts.map((post) => ({ slug: post.slug }))
}

// Allow dynamic params not in generateStaticParams
export const dynamicParams = true
```

---

## 布局

### 根布局（必需）

```tsx
// app/layout.tsx
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
```

### 带数据获取的嵌套布局

```tsx
// app/dashboard/layout.tsx
import { getUser } from '@/lib/get-user'

export default async function DashboardLayout({ children }: { children: React.ReactNode }) {
  const user = await getUser()
  return (
    <div className="flex">
      <Sidebar user={user} />
      <main className="flex-1 p-6">{children}</main>
    </div>
  )
}
```

### 多个根布局的路由组

```
app/
├── (marketing)/
│   ├── layout.tsx          # Marketing layout with <html>/<body>
│   └── about/page.tsx
└── (app)/
    ├── layout.tsx          # App layout with <html>/<body>
    └── dashboard/page.tsx
```

### 元数据

```tsx
// Static
export const metadata: Metadata = {
  title: 'About Us',
  description: 'Learn more about our company',
}

// Dynamic
export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { slug } = await params
  const post = await getPost(slug)
  return {
    title: post.title,
    openGraph: { title: post.title, images: [post.coverImage] },
  }
}

// Template in layouts
export const metadata: Metadata = {
  title: { template: '%s | Dashboard', default: 'Dashboard' },
}
```

---

## 服务器组件与客户端组件

### 判断指南

**使用服务器组件（默认情况）：**
- 用于获取数据或访问后端资源
- 用于存储敏感信息（如 API 密钥、令牌）
- 用于减少客户端 JavaScript 的体积
- 当不需要交互功能时

**使用客户端组件（使用 `use client`）：**
- 用于使用 `useState`, `useEffect`, `useReducer`
- 用于处理事件（如 `onClick`, `onChange`
- 用于使用浏览器 API（如 `window`, `document`）
- 用于使用自定义的带有状态的钩子

### 组合模式

**模式 1：服务器获取数据 → 客户端交互**

```tsx
// app/products/page.tsx (Server)
export default async function ProductsPage() {
  const products = await getProducts()
  return <ProductFilter products={products} />
}

// components/product-filter.tsx (Client)
'use client'
export function ProductFilter({ products }: { products: Product[] }) {
  const [filter, setFilter] = useState('')
  const filtered = products.filter(p => p.name.includes(filter))
  return (
    <>
      <input onChange={e => setFilter(e.target.value)} />
      {filtered.map(p => <ProductCard key={p.id} product={p} />)}
    </>
  )
}
```

**模式 2：子组件作为服务器组件**

```tsx
// components/client-wrapper.tsx
'use client'
export function ClientWrapper({ children }: { children: React.ReactNode }) {
  const [isOpen, setIsOpen] = useState(false)
  return (
    <div>
      <button onClick={() => setIsOpen(!isOpen)}>Toggle</button>
      {isOpen && children}
    </div>
  )
}

// app/page.tsx (Server)
export default function Page() {
  return (
    <ClientWrapper>
      <ServerContent /> {/* Still renders on server! */}
    </ClientWrapper>
  )
}
```

**模式 3：在组件边界处使用提供者（Providers）**

```tsx
// app/providers.tsx
'use client'
import { ThemeProvider } from 'next-themes'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'

const queryClient = new QueryClient()

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider attribute="class" defaultTheme="system">
        {children}
      </ThemeProvider>
    </QueryClientProvider>
  )
}
```

### 使用 `cache()` 共享数据

```tsx
import { cache } from 'react'

export const getUser = cache(async () => {
  const response = await fetch('/api/user')
  return response.json()
})

// Both layout and page call getUser() — only one fetch happens
```

---

## 数据获取

### 异步服务器组件

```tsx
export default async function PostsPage() {
  const posts = await fetch('https://api.example.com/posts').then(r => r.json())
  return <ul>{posts.map(p => <li key={p.id}>{p.title}</li>)}</ul>
}
```

### 并发数据获取

```tsx
export default async function DashboardPage() {
  const [user, posts, analytics] = await Promise.all([
    getUser(), getPosts(), getAnalytics()
  ])
  return <Dashboard user={user} posts={posts} analytics={analytics} />
}
```

### 使用 Suspense 实现数据流式加载

```tsx
import { Suspense } from 'react'

export default function DashboardPage() {
  return (
    <div>
      <h1>Dashboard</h1>
      <Suspense fallback={<StatsSkeleton />}>
        <SlowStats />
      </Suspense>
      <Suspense fallback={<ChartSkeleton />}>
        <SlowChart />
      </Suspense>
    </div>
  )
}
```

### 数据缓存

```tsx
// Cache indefinitely (static)
const data = await fetch('https://api.example.com/data')

// Revalidate every hour
const data = await fetch(url, { next: { revalidate: 3600 } })

// No caching (always fresh)
const data = await fetch(url, { cache: 'no-store' })

// Cache with tags
const data = await fetch(url, { next: { tags: ['posts'] } })
```

---

## 加载状态与错误处理

### 加载界面

```tsx
// app/dashboard/loading.tsx
export default function Loading() {
  return (
    <div className="animate-pulse">
      <div className="h-8 bg-gray-200 rounded w-1/4 mb-4" />
      <div className="space-y-3">
        <div className="h-4 bg-gray-200 rounded w-full" />
        <div className="h-4 bg-gray-200 rounded w-5/6" />
      </div>
    </div>
  )
}
```

### 错误处理

```tsx
// app/dashboard/error.tsx
'use client'

export default function Error({ error, reset }: { error: Error; reset: () => void }) {
  return (
    <div className="p-4 bg-red-50 border border-red-200 rounded">
      <h2 className="text-red-800 font-bold">Something went wrong!</h2>
      <p className="text-red-600">{error.message}</p>
      <button onClick={reset} className="mt-2 px-4 py-2 bg-red-600 text-white rounded">
        Try again
      </button>
    </div>
  )
}
```

### 404 错误页面

```tsx
// app/posts/[slug]/page.tsx
import { notFound } from 'next/navigation'

export default async function PostPage({ params }: PageProps) {
  const { slug } = await params
  const post = await getPost(slug)
  if (!post) notFound()
  return <article>{post.content}</article>
}
```

---

## 服务器端操作

### 定义服务器端操作

```tsx
// app/actions.ts
'use server'

import { z } from 'zod'
import { revalidatePath } from 'next/cache'
import { redirect } from 'next/navigation'

const schema = z.object({
  title: z.string().min(1).max(200),
  content: z.string().min(10),
})

export async function createPost(formData: FormData) {
  const session = await auth()
  if (!session?.user) throw new Error('Unauthorized')

  const parsed = schema.safeParse({
    title: formData.get('title'),
    content: formData.get('content'),
  })

  if (!parsed.success) return { error: parsed.error.flatten() }

  const post = await db.post.create({
    data: { ...parsed.data, authorId: session.user.id },
  })

  revalidatePath('/posts')
  redirect(`/posts/${post.slug}`)
}
```

### 使用 `useState` 和 `useStatus` 的表单

```tsx
// components/submit-button.tsx
'use client'
import { useFormStatus } from 'react-dom'

export function SubmitButton() {
  const { pending } = useFormStatus()
  return (
    <button type="submit" disabled={pending}>
      {pending ? 'Submitting...' : 'Submit'}
    </button>
  )
}

// components/create-post-form.tsx
'use client'
import { useFormState } from 'react-dom'
import { createPost } from '@/app/actions'

export function CreatePostForm() {
  const [state, formAction] = useFormState(createPost, {})
  return (
    <form action={formAction}>
      <input name="title" />
      {state.error?.title && <p className="text-red-500">{state.error.title[0]}</p>}
      <textarea name="content" />
      <SubmitButton />
    </form>
  )
}
```

### 乐观更新（Optimistic Updates）

```tsx
'use client'
import { useOptimistic, useTransition } from 'react'

export function TodoList({ initialTodos }: { initialTodos: Todo[] }) {
  const [isPending, startTransition] = useTransition()
  const [optimisticTodos, addOptimistic] = useOptimistic(
    initialTodos,
    (state, newTodo: string) => [...state, { id: 'temp', title: newTodo, completed: false }]
  )

  async function handleSubmit(formData: FormData) {
    const title = formData.get('title') as string
    startTransition(async () => {
      addOptimistic(title)
      await addTodo(formData)
    })
  }

  return (
    <>
      <form action={handleSubmit}>
        <input name="title" />
        <button>Add</button>
      </form>
      <ul>
        {optimisticTodos.map(todo => (
          <li key={todo.id} className={todo.id === 'temp' ? 'opacity-50' : ''}>{todo.title}</li>
        ))}
      </ul>
    </>
  )
}
```

### 数据重新验证

```tsx
'use server'
import { revalidatePath, revalidateTag } from 'next/cache'

export async function updatePost(id: string, formData: FormData) {
  await db.post.update({ where: { id }, data: { ... } })

  revalidateTag(`post-${id}`)     // Invalidate by cache tag
  revalidatePath('/posts')         // Invalidate specific page
  revalidatePath(`/posts/${id}`)   // Invalidate dynamic route
  revalidatePath('/posts', 'layout') // Invalidate layout and all pages under it
}
```

---

## 路由处理器（API 路由）

### 基本的 CRUD 操作

```tsx
// app/api/posts/route.ts
import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams
  const page = parseInt(searchParams.get('page') ?? '1')
  const limit = parseInt(searchParams.get('limit') ?? '10')

  const [posts, total] = await Promise.all([
    db.post.findMany({ skip: (page - 1) * limit, take: limit }),
    db.post.count(),
  ])

  return NextResponse.json({ data: posts, pagination: { page, limit, total } })
}

export async function POST(request: NextRequest) {
  const body = await request.json()
  const post = await db.post.create({ data: body })
  return NextResponse.json(post, { status: 201 })
}
```

### 动态路由处理

```tsx
// app/api/posts/[id]/route.ts
export async function GET(request: Request, { params }: { params: Promise<{ id: string }> }) {
  const { id } = await params
  const post = await db.post.findUnique({ where: { id } })
  if (!post) return NextResponse.json({ error: 'Not found' }, { status: 404 })
  return NextResponse.json(post)
}

export async function DELETE(request: Request, { params }: { params: Promise<{ id: string }> }) {
  const { id } = await params
  await db.post.delete({ where: { id } })
  return new NextResponse(null, { status: 204 })
}
```

### 数据流式传输（SSE）

```tsx
export async function GET() {
  const encoder = new TextEncoder()
  const stream = new ReadableStream({
    async start(controller) {
      for (let i = 0; i < 10; i++) {
        controller.enqueue(encoder.encode(`data: ${JSON.stringify({ count: i })}\n\n`))
        await new Promise(r => setTimeout(r, 1000))
      }
      controller.close()
    },
  })
  return new Response(stream, {
    headers: { 'Content-Type': 'text/event-stream', 'Cache-Control': 'no-cache' },
  })
}
```

---

## 并发路由与路由拦截

### 并发路由（使用路由槽）

```
app/
├── @modal/
│   ├── (.)photo/[id]/page.tsx   # Intercepted route (modal)
│   └── default.tsx
├── photo/[id]/page.tsx          # Full page route
├── layout.tsx
└── page.tsx
```

```tsx
// app/layout.tsx
export default function Layout({ children, modal }: {
  children: React.ReactNode
  modal: React.ReactNode
}) {
  return <>{children}{modal}</>
}
```

### 模态组件

```tsx
'use client'
import { useRouter } from 'next/navigation'

export function Modal({ children }: { children: React.ReactNode }) {
  const router = useRouter()
  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center"
         onClick={() => router.back()}>
      <div className="bg-white rounded-lg p-6 max-w-2xl" onClick={e => e.stopPropagation()}>
        {children}
      </div>
    </div>
  )
}
```

---

## 认证（NextAuth.js v5 / Auth.js）

### 设置认证机制

```tsx
// auth.ts
import NextAuth from 'next-auth'
import GitHub from 'next-auth/providers/github'
import Credentials from 'next-auth/providers/credentials'

export const { handlers, auth, signIn, signOut } = NextAuth({
  providers: [
    GitHub({ clientId: process.env.GITHUB_ID, clientSecret: process.env.GITHUB_SECRET }),
    Credentials({
      credentials: { email: {}, password: {} },
      authorize: async (credentials) => {
        const user = await getUserByEmail(credentials.email as string)
        if (!user || !await verifyPassword(credentials.password as string, user.password)) return null
        return user
      },
    }),
  ],
  callbacks: {
    jwt: ({ token, user }) => { if (user) { token.id = user.id; token.role = user.role } return token },
    session: ({ session, token }) => { session.user.id = token.id as string; session.user.role = token.role as string; return session },
  },
})

// app/api/auth/[...nextauth]/route.ts
import { handlers } from '@/auth'
export const { GET, POST } = handlers
```

### 中间件保护

```tsx
// middleware.ts
export { auth as middleware } from '@/auth'

export const config = {
  matcher: ['/dashboard/:path*', '/api/protected/:path*'],
}
```

### 服务器组件中的认证检查

```tsx
import { auth } from '@/auth'
import { redirect } from 'next/navigation'

export default async function DashboardPage() {
  const session = await auth()
  if (!session) redirect('/login')
  return <h1>Welcome, {session.user?.name}</h1>
}
```

### 服务器端操作中的认证检查

```tsx
'use server'
import { auth } from '@/auth'

export async function deletePost(id: string) {
  const session = await auth()
  if (!session?.user) throw new Error('Unauthorized')

  const post = await db.post.findUnique({ where: { id } })
  if (post?.authorId !== session.user.id) throw new Error('Forbidden')

  await db.post.delete({ where: { id } })
  revalidatePath('/posts')
}
```

---

## 路由段配置

```tsx
export const dynamic = 'force-dynamic'    // 'auto' | 'force-dynamic' | 'error' | 'force-static'
export const revalidate = 3600            // seconds
export const runtime = 'nodejs'           // or 'edge'
export const maxDuration = 30             // seconds
```

---

## 应避免的错误做法

1. ✌ 不要在整个页面中都使用 `use client`——仅将其应用于需要交互的部分。
2. ✌ 当数据可以由服务器组件获取时，不要在客户端组件中获取数据。
3. ✌ 当数据获取操作是独立的时，不要顺序使用 `await`——应使用 `Promise.all()`。
4. ✌ 不要在服务器和客户端之间直接传递函数作为属性——应使用服务器端操作。
5. ✌ 不要在 Next.js 15 中使用 `useEffect` 来获取数据（应使用异步服务器组件）。
6. ✌ 忘记在异步页面中添加 `await` 处理 `params`（它们现在是 `Promise` 类型）。
7. ✌ 确保异步页面中包含 `loading.tsx` 或 `<Suspense>` 来显示加载状态。
8. ✌ 不要对服务器端操作的输入进行验证（始终使用 zod 进行验证）。