---
name: React
slug: react
version: 1.0.4
homepage: https://clawic.com/skills/react
changelog: "Added React 19 coverage, Server Components, AI Mistakes section, Core Rules, state management patterns, setup system"
description: 完整的 React 19 工程实践，包括架构设计、服务器组件、钩子（hooks）、状态管理（Zustand）、TanStack 查询框架、表单处理、性能优化、测试流程以及生产环境的部署。
---
# React

这是一套针对生产环境的React开发技能。这套技能将彻底改变你构建React应用程序的方式——从组件架构到部署流程。

## 使用场景

- 构建React组件、页面或功能模块
- 实现状态管理（使用`useState`、`Context`、`Zustand`或`TanStack Query`）
- 使用React 19的特性（如服务器组件、`use()`钩子、`Actions`）
- 优化应用程序性能（使用`memo`、`lazy`、`Suspense`等机制）
- 调试渲染问题、无限循环或闭包相关问题
- 设计项目架构和文件结构

## 架构决策

在编写代码之前，请先做出以下决策：

| 决策 | 可选方案 | 默认方案 |
|----------|---------|---------|
| 渲染方式 | 单页应用（SPA）/服务器端渲染（SSR）/静态渲染/混合渲染 | 使用Next.js的服务器端渲染（SSR） |
| 服务器端状态管理 | 使用`TanStack Query`或`SWR` | 使用`TanStack Query` |
| 客户端状态管理 | 使用`useState`或`Zustand` | 如果状态需要共享，则使用`Zustand` |
| 样式管理 | 使用Tailwind CSS或CSS模块 | 使用Tailwind CSS |
- 表单处理 | 使用`React Hook Form`结合`Zod`库 | 或使用原生的React表单组件 |

**注意：** 服务器端状态（API数据）和客户端状态（UI状态）是不同的，切勿将它们混在一起使用。

## 组件开发规范

```tsx
// ✅ The correct pattern
export function UserCard({ user, onEdit }: UserCardProps) {
  // 1. Hooks first (always)
  const [isOpen, setIsOpen] = useState(false)
  
  // 2. Derived state (NO useEffect for this)
  const fullName = `${user.firstName} ${user.lastName}`
  
  // 3. Handlers
  const handleEdit = useCallback(() => onEdit(user.id), [onEdit, user.id])
  
  // 4. Early returns
  if (!user) return null
  
  // 5. JSX (max 50 lines)
  return (...)
}
```

| 规范 | 原因 |
|------|-----|
| 仅使用命名导出 | 便于代码重构和IDE支持 |
| 将组件属性作为接口导出 | 便于复用和文档编写 |
| JSX代码长度不超过50行 | 如果代码过长，应将其拆分为多个组件 |
| 文件长度不超过300行 | 超过300行的代码应拆分为多个文件 |
| 将`use()`钩子放在文件开头 | 这是React的推荐做法，有助于代码的可读性 |

## 状态管理

```
Is it from an API?
├─ YES → TanStack Query (NOT Redux, NOT Zustand)
└─ NO → Is it shared across components?
    ├─ YES → Zustand (simple) or Context (if rarely changes)
    └─ NO → useState
```

### TanStack Query（用于管理服务器端状态）

```tsx
// Query key factory — prevents key typos
export const userKeys = {
  all: ['users'] as const,
  detail: (id: string) => [...userKeys.all, id] as const,
}

export function useUser(id: string) {
  return useQuery({
    queryKey: userKeys.detail(id),
    queryFn: () => fetchUser(id),
    staleTime: 5 * 60 * 1000, // 5 min
  })
}
```

### Zustand（用于管理客户端状态）

```tsx
// Thin stores, one concern each
export const useUIStore = create<UIState>()((set) => ({
  sidebarOpen: true,
  toggleSidebar: () => set((s) => ({ sidebarOpen: !s.sidebarOpen })),
}))

// ALWAYS use selectors — prevents unnecessary rerenders
const isOpen = useUIStore((s) => s.sidebarOpen)
```

## React 19

### 服务器组件（Next.js应用中的默认配置）

```tsx
// Server Component — runs on server, zero JS to client
async function ProductList() {
  const products = await db.products.findMany() // Direct DB access
  return <ul>{products.map(p => <ProductCard key={p.id} product={p} />)}</ul>
}

// Client Component — needs 'use client' directive
'use client'
function AddToCartButton({ productId }: { productId: string }) {
  const [loading, setLoading] = useState(false)
  return <button onClick={() => addToCart(productId)}>Add</button>
}
```

| 服务器组件 | 客户端组件 |
|------------------|------------------|
| 支持`async/await` | 支持`useState` |
| 直接访问数据库 | 支持`onClick`事件 |
| 不会增加打包文件大小 | 使用服务器端数据时不需要 |
| 不建议使用`useState` | 服务器端状态不适合使用`useState` |

### `use()`钩子

```tsx
// Read promises in render (with Suspense)
function Comments({ promise }: { promise: Promise<Comment[]> }) {
  const comments = use(promise) // Suspends until resolved
  return <ul>{comments.map(c => <li key={c.id}>{c.text}</li>)}</ul>
}
```

### `useActionState`（用于处理表单状态）

```tsx
'use client'
async function submitAction(prev: State, formData: FormData) {
  'use server'
  // ... server logic
  return { success: true }
}

function Form() {
  const [state, action, pending] = useActionState(submitAction, {})
  return (
    <form action={action}>
      <input name="email" disabled={pending} />
      <button disabled={pending}>{pending ? 'Saving...' : 'Save'}</button>
      {state.error && <p>{state.error}</p>}
    </form>
  )
}
```

## 性能优化

| 优先级 | 优化技巧 | 影响程度 |
|----------|-----------|--------|
| P0 | 基于路由的代码拆分 | 非常重要（提升性能） |
| P0 | 图片优化（使用`next/image`库） | 非常重要（提升性能） |
| P1 | 虚拟化长列表（使用`tanstack-virtual`） | 有一定效果 |
| P1 | 对耗时操作进行去抖动处理 | 有一定效果 |
| P2 | 对耗时计算使用`React.memo` | 有一定效果 |
| P2 | 对耗时计算使用`useMemo` | 有一定效果 |

**React编译器（React 19及以上版本）**：会自动进行代码缓存（memoization）。无需手动使用`memo`、`useMemo`或`useCallback`。

## 常见错误与陷阱

### 渲染相关的问题

```tsx
// ❌ Renders "0" when count is 0
{count && <Component />}

// ✅ Explicit boolean
{count > 0 && <Component />}
```

```tsx
// ❌ Mutating state — React won't detect
array.push(item)
setArray(array)

// ✅ New reference
setArray([...array, item])
```

```tsx
// ❌ New key every render — destroys component
<Item key={Math.random()} />

// ✅ Stable key
<Item key={item.id} />
```

### 使用`Hooks`时可能遇到的问题

```tsx
// ❌ useEffect cannot be async
useEffect(async () => { ... }, [])

// ✅ Define async inside
useEffect(() => {
  async function load() { ... }
  load()
}, [])
```

```tsx
// ❌ Missing cleanup — memory leak
useEffect(() => {
  const sub = subscribe()
}, [])

// ✅ Return cleanup
useEffect(() => {
  const sub = subscribe()
  return () => sub.unsubscribe()
}, [])
```

```tsx
// ❌ Object in deps — triggers every render
useEffect(() => { ... }, [{ id: 1 }])

// ✅ Extract primitives or memoize
useEffect(() => { ... }, [id])
```

### 数据获取相关的问题

```tsx
// ❌ Sequential fetches — slow
const users = await fetchUsers()
const orders = await fetchOrders()

// ✅ Parallel
const [users, orders] = await Promise.all([fetchUsers(), fetchOrders()])
```

### React开发中AI助手可能犯的错误

AI助手在处理React项目时可能会犯以下错误：

| 错误 | 正确的解决方法 |
|---------|-----------------|
| 在`useEffect`中处理派生状态 | 应将相关逻辑直接写在函数内部（例如：`const x = a + b`） |
| 使用Redux处理API数据 | 应使用`TanStack Query`来获取服务器端数据 |
| 使用默认导出方式 | 应使用命名导出（例如：`export function X`） |
| 在动态列表中使用索引作为键 | 应使用稳定的键值对（例如：`key={item.id}`） |
| 在`useEffect`中直接进行数据请求 | 应使用`TanStack Query`或合适的加载器机制 |
| 创建过长的组件（超过500行代码） | 将代码拆分为多个组件（JSX代码不超过50行，文件不超过300行） |
| 未设置错误处理机制 | 应在应用、功能模块或组件级别设置错误处理逻辑 |
| 忽略TypeScript的严格类型检查 | 应将`strict`设置为`true`，并在编译时捕获类型错误 |

## 快速参考

### `Hooks`的使用

| Hook | 用途 |
|------|---------|
| `useState` | 用于管理局部状态 |
| `useEffect` | 用于处理副作用（如数据订阅、DOM操作） |
| ` useCallback` | 用于确保函数引用的稳定性 |
| `useMemo` | 用于缓存耗时的计算结果 |
| `useRef` | 用于引用可变的DOM元素 |
| `use()` | 用于读取Promise或上下文信息（React 19版本） |
| `useActionState` | 用于处理表单相关的状态 |
| `useOptimistic` | 用于实现乐观渲染（React 19版本） |

### 文件结构

```
src/
├── app/                 # Routes (Next.js)
├── features/            # Feature modules
│   └── auth/
│       ├── components/  # Feature components
│       ├── hooks/       # Feature hooks
│       ├── api/         # API calls
│       └── index.ts     # Public exports
├── shared/              # Cross-feature
│   ├── components/ui/   # Button, Input, etc.
│   └── hooks/           # useDebounce, etc.
└── providers/           # Context providers
```

## 配置指南

首次使用请参考`setup.md`文件进行配置。项目跟踪相关内容请参考`memory-template.md`文件。

## 核心开发原则

1. **服务器端状态 ≠ 客户端状态**：API数据应通过`TanStack Query`获取，UI状态应使用`useState`或`Zustand`管理。切勿将它们混用。
2. **仅使用命名导出**：使用`export function X`而非`export default`，以支持安全的代码重构。
3. **先集中编写状态相关的代码，再逐步拆分**：先在需要使用状态的地方编写相关代码，只有在必要时才将其拆分为单独的组件。
4. **不要在`useEffect`中处理派生状态**：对于派生状态，应直接在函数内部进行计算（例如：`const total = items.reduce(...)`）。
5. **使用稳定的键值对**：在动态列表中，应使用`item.id`作为键，而不是`index`。
6. **JSX代码长度限制**：JSX代码长度不超过50行；文件长度不超过300行。
7. **启用TypeScript的严格类型检查**：将`strict`设置为`true`，以在编译时捕获类型错误。

## 相关技能

如果用户需要，可以使用`clawhub install <slug>`命令安装以下相关技能：

- **frontend-design-ultimate**：使用React和Tailwind构建完整的用户界面。
- **typescript**：掌握TypeScript的编程规范和严格类型检查。
- **nextjs**：学习Next.js的应用路由和部署技巧。
- **testing**：学习如何使用测试库来测试React组件。

## 反馈建议

- 如果你觉得这些内容有用，请给项目点赞（`clawhub star react`）。
- 为了保持信息更新，请订阅我们的服务（`clawhub sync`）。