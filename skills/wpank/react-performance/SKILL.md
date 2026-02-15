---
name: react-performance
model: standard
description:
  React and Next.js performance optimization patterns. Use when writing,
  reviewing, or refactoring React/Next.js code to ensure optimal performance.
  Triggers on tasks involving components, data fetching, bundle optimization,
  re-render reduction, or server component architecture.
version: "1.0"
---

# React 性能优化模式

本文档为 React 和 Next.js 应用程序的性能优化指南，涵盖了 7 个方面的优化策略，并根据其影响程度进行了优先级排序。详细示例请参见 `references/` 目录。

## 适用场景

- 编写新的 React 组件或 Next.js 页面
- 实现数据获取（客户端或服务器端）
- 优化性能或进行代码重构
- 减小打包大小或提升加载速度

## 按优先级分类的优化策略

| 优先级 | 分类                | 影响程度    |
|-------|------------------|-----------|
| 1     | 异步处理 / 流式操作        | 关键        |
| 2     | 打包大小              | 关键        |
| 3     | 服务器端组件            | 高度重要    |
| 4     | 重新渲染              | 中等程度    |
| 5     | 绘制性能              | 中等程度    |
| 6     | 客户端数据获取          | 中等程度    |
| 7     | JavaScript 性能          | 低至中等程度 |

## 安装工具

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install react-performance
```


---

## 1. 异步处理 — 消除流式操作（关键）

### 并行执行独立操作

在 React 应用中，顺序执行 `await` 语句是导致性能问题的主要原因。

```typescript
// BAD — sequential, 3 round trips
const user = await fetchUser()
const posts = await fetchPosts()
const comments = await fetchComments()

// GOOD — parallel, 1 round trip
const [user, posts, comments] = await Promise.all([
  fetchUser(), fetchPosts(), fetchComments(),
])
```

### 将 `await` 语句放在实际使用数据的地方

将 `await` 语句移到需要使用数据的地方。

```typescript
// BAD — blocks both branches
async function handle(userId: string, skip: boolean) {
  const data = await fetchUserData(userId)
  if (skip) return { skipped: true }    // Still waited
  return process(data)
}

// GOOD — only blocks when needed
async function handle(userId: string, skip: boolean) {
  if (skip) return { skipped: true }    // Returns immediately
  return process(await fetchUserData(userId))
}
```

### 战略性地控制渲染时机

在数据依赖的部分加载完成之前，先显示页面布局。

```tsx
// BAD — entire page blocked
async function Page() {
  const data = await fetchData()
  return <div><Sidebar /><Header /><DataDisplay data={data} /><Footer /></div>
}

// GOOD — layout renders immediately, data streams in
function Page() {
  return (
    <div>
      <Sidebar /><Header />
      <Suspense fallback={<Skeleton />}><DataDisplay /></Suspense>
      <Footer />
    </div>
  )
}
async function DataDisplay() {
  const data = await fetchData()
  return <div>{data.content}</div>
}
```

使用 `use()` 在多个组件之间共享 Promise，避免重复请求数据。

---

## 2. 打包大小（关键）

### 避免使用“桶式”导入（barrel imports）

“桶式”导入会加载大量未使用的模块，导致打包体积过大。直接导入可以节省 200–800 毫秒的加载时间。

```tsx
// BAD — loads 1,583 modules
import { Check, X, Menu } from 'lucide-react'

// GOOD — loads only 3 modules
import Check from 'lucide-react/dist/esm/icons/check'
import X from 'lucide-react/dist/esm/icons/x'
import Menu from 'lucide-react/dist/esm/icons/menu'
```

在 Next.js 13.5 及更高版本中，可以在配置文件中启用 `experimental.optimizePackageImports` 选项。受影响的常用库包括：`lucide-react`、`@mui/material`、`react-icons`、`@radix-ui`、`lodash`、`date-fns`。

### 对于大型组件，使用动态导入

```tsx
import dynamic from 'next/dynamic'
const MonacoEditor = dynamic(
  () => import('./monaco-editor').then((m) => m.MonacoEditor),
  { ssr: false }
)
```

### 延迟加载非必要的第三方库

分析工具、日志记录、错误跟踪等功能可以在页面加载完成后（使用 `dynamic()` 和 `{ ssr: false }`）再加载。

### 根据用户操作预加载相关内容

```tsx
const preload = () => { void import('./monaco-editor') }
<button onMouseEnter={preload} onFocus={preload} onClick={onClick}>Open Editor</button>
```

---

## 3. 服务器端组件（高度重要）

### 在服务器与客户端之间仅传递实际需要的数据

只传递客户端真正需要的数据。

```tsx
// BAD — serializes all 50 user fields
return <Profile user={user} />

// GOOD — serializes 1 field
return <Profile name={user.name} />
```

### 使用组合式编程并行处理数据获取

在服务器端，数据获取操作通常是顺序执行的；可以通过重构代码实现并行处理。

```tsx
// BAD — Sidebar waits for header fetch
export default async function Page() {
  const header = await fetchHeader()
  return <div><div>{header}</div><Sidebar /></div>
}

// GOOD — sibling async components fetch simultaneously
async function Header() { return <div>{await fetchHeader()}</div> }
async function Sidebar() { return <nav>{(await fetchSidebarItems()).map(renderItem)}</nav> }
export default function Page() { return <div><Header /><Sidebar /></div> }
```

### 使用 `React.cache()` 避免重复计算

`React.cache()` 可以根据请求内容避免重复计算。

### 使用基本类型参数（而非对象）

`React.cache()` 会通过 `Object.is()` 来判断参数是否已经缓存过。

Next.js 会自动处理 `fetch` 请求的重复计算，但对于数据库查询、身份验证和计算操作，仍需要手动使用 `React.cache()`。

### 使用 `after()` 实现非阻塞操作

```tsx
import { after } from 'next/server'
export async function POST(request: Request) {
  await updateDatabase(request)
  after(async () => { logUserAction({ userAgent: request.headers.get('user-agent') }) })
  return Response.json({ status: 'success' })
}
```

---

## 4. 重新渲染优化（中等程度）

### 在渲染过程中计算状态，而非在副作用中计算

```tsx
// BAD — redundant state + effect
const [fullName, setFullName] = useState('')
useEffect(() => { setFullName(first + ' ' + last) }, [first, last])

// GOOD — derive inline
const fullName = first + ' ' + last
```

### 对于稳定的回调函数，使用函数式 `setState`

```tsx
// BAD — recreated on every items change
const addItem = useCallback((item: Item) => {
  setItems([...items, item])
}, [items])

// GOOD — stable, always latest state
const addItem = useCallback((item: Item) => {
  setItems((curr) => [...curr, item])
}, [])
```

### 将状态读取操作延迟到实际使用的时候

如果只在回调函数中读取状态，就不要订阅状态变化。

```tsx
// BAD — re-renders on every searchParams change
const searchParams = useSearchParams()
const handleShare = () => shareChat(chatId, { ref: searchParams.get('ref') })

// GOOD — reads on demand
const handleShare = () => {
  const ref = new URLSearchParams(window.location.search).get('ref')
  shareChat(chatId, { ref })
}
```

### 拖动式初始化状态

```tsx
// BAD — JSON.parse runs every render
const [settings] = useState(JSON.parse(localStorage.getItem('s') || '{}'))

// GOOD — runs only once
const [settings] = useState(() => JSON.parse(localStorage.getItem('s') || '{}'))
```

### 对于非紧急的更新，使用条件渲染

```tsx
// BAD — re-renders on every pixel
const width = useWindowWidth(); const isMobile = width < 768

// GOOD — re-renders only when boolean flips
const isMobile = useMediaQuery('(max-width: 767px)')
```

### 将耗时的操作提取到缓存组件中

```tsx
const UserAvatar = memo(function UserAvatar({ user }: { user: User }) {
  const id = useMemo(() => computeAvatarId(user), [user])
  return <Avatar id={id} />
})
function Profile({ user, loading }: Props) {
  if (loading) return <Skeleton />
  return <div><UserAvatar user={user} /></div>
}
```

注意：React 编译器会自动处理部分缓存逻辑，因此通常不需要手动使用 `memo()` 或 `useMemo()`。

---

## 5. 绘制性能（中等程度）

### 对于长列表，利用 CSS 的内容可见性优化

对于包含 1000 个元素的列表，浏览器会自动省略屏幕外的 990 个元素，从而显著提升初始渲染速度。

```css
.list-item { content-visibility: auto; contain-intrinsic-size: 0 80px; }
```

### 将静态 JSX 提前提取到组件外部

这样可以避免不必要的重新渲染，尤其是对于大型 SVG 元素。React 编译器会自动处理这部分优化。

```tsx
const skeleton = <div className="skeleton" />
function Container() { return <div>{loading && skeleton}</div> }
```

---

## 6. 客户端数据获取（中等程度）

### 使用 SWR（Server-side Rendering）进行数据去重和缓存

```tsx
// BAD — each instance fetches independently
useEffect(() => { fetch('/api/users').then(r => r.json()).then(setUsers) }, [])

// GOOD — multiple instances share one request
const { data: users } = useSWR('/api/users', fetcher)
```

---

## 7. JavaScript 性能（低至中等程度）

### 使用 `Set` 或 `Map` 数据结构以实现 O(1) 的查找效率

```typescript
// BAD — O(n)
items.filter(i => allowed.includes(i.id))
// GOOD — O(1)
const allowedSet = new Set(allowed)
items.filter(i => allowedSet.has(i.id))
```

### 合并数组遍历操作

```typescript
// BAD — 3 passes
const a = users.filter(u => u.isAdmin)
const t = users.filter(u => u.isTester)
// GOOD — 1 pass
const a: User[] = [], t: User[] = []
for (const u of users) { if (u.isAdmin) a.push(u); if (u.isTester) t.push(u) }
```

**另外：** 尽量提前返回结果，循环中缓存属性访问，将正则表达式提取到循环外部，对于高频访问的部分优先使用 `for...of` 循环。

---

## 快速决策指南

- **页面加载缓慢？** → 首先检查打包大小（2），然后优化异步处理（1）
- **交互响应迟缓？** → 优化重新渲染（4），接着优化 JavaScript 性能（7）
- **服务器端页面响应慢？** → 优化服务器端数据序列化和并行数据获取（3）
- **客户端数据更新不及时或速度慢？** → 使用 SWR（6）
- **长列表显示效果不佳？** → 优化 CSS 的内容可见性（5）