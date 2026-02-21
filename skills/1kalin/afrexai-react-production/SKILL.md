---
name: afrexai-react-production
description: 一套完整的开发方法论，用于构建生产级的 React 应用程序，涵盖架构设计、组件开发、状态管理、性能优化、测试以及部署等关键环节。
---
# React生产工程

这是一套构建生产级React应用程序的完整方法论，涵盖了架构决策、组件设计、状态管理、性能优化、测试和部署等方面。它不仅提供了API参考，还包含了决策框架、模板和评分系统等工程实践。

## 第1阶段：架构评估

### 快速健康检查（满分16分）
- [ ] 组件树深度小于6层（+2分）
- [ ] 没有超过2层的属性穿透（+2分）
- 压缩后的包大小小于200KB（+2分）
- 在4G网络环境下，LCP（首次绘制时间）小于2.5秒（+2分）
- 业务逻辑的测试覆盖率超过70%（+2分）
- 生产代码中不存在`any`类型（+2分）
- 没有直接操作DOM（+2分）
- 错误处理边界一致（+2分）

### 架构概述

```yaml
project:
  name: ""
  type: "" # spa | ssr | hybrid | static
  framework: "" # next | remix | vite-spa | astro
  scale: "" # small (<20 routes) | medium (20-100) | large (100+)
  team_size: "" # solo | small (2-5) | medium (6-15) | large (15+)
current_state:
  react_version: "" # 18 | 19
  typescript: true
  router: "" # react-router | next-app | tanstack-router
  state_management: "" # useState | zustand | jotai | redux | tanstack-query
  styling: "" # tailwind | css-modules | styled-components | vanilla-extract
  testing: "" # vitest | jest | playwright | cypress
  ci_cd: "" # github-actions | gitlab-ci | vercel
pain_points: []
goals: []
```

### 框架选择决策矩阵

| 因素 | Vite SPA | Next.js | Remix | Astro |
|--------|----------|---------|-------|-------|
| 是否需要SEO | ❌ | ✅（最佳） | ✅（良好） | ✅（最佳） |
| 适用于仪表板/应用程序 | ✅（最佳） | ✅（良好） | ✅（良好） | ❌ |
| 以内容为主的应用 | ❌ | ✅（良好） | ✅（良好） | ✅（最佳） |
| 团队熟悉度 | ✅（简单） | ⚠️（学习曲线较陡） | ⚠️（遵循Web标准） | ⚠️（模块化设计） |
| 部署灵活性 | 任意环境 | Vercel更优 | 任意环境 | 任意环境 |
| 包大小 | 可控 | 框架本身占用的空间较小 | 更小的JS代码量 |

**决策规则：**
1. 如果是用于仪表板或内部工具且不需要SEO，则选择Vite SPA。
2. 如果是营销与应用程序的混合体，则选择Next.js。
3. 如果以内容为主且需要一定交互性，则选择Astro。
4. 如果优先遵循Web标准且布局复杂，则选择Remix。
5. 对于大多数SaaS产品来说，Next.js是默认选择。

---

## 第2阶段：项目结构与规范

### 推荐的基于功能的结构

```
src/
├── app/                    # Routes/pages (framework-specific)
├── features/               # Feature modules (THE core pattern)
│   ├── auth/
│   │   ├── components/     # Feature-specific components
│   │   ├── hooks/          # Feature-specific hooks
│   │   ├── api/            # API calls & types
│   │   ├── utils/          # Feature utilities
│   │   ├── types.ts        # Feature types
│   │   └── index.ts        # Public API (barrel export)
│   ├── dashboard/
│   └── settings/
├── shared/                 # Cross-feature shared code
│   ├── components/         # Generic UI components
│   │   ├── ui/             # Primitives (Button, Input, Card)
│   │   └── layout/         # Layout components
│   ├── hooks/              # Generic hooks
│   ├── lib/                # Utilities, constants
│   └── types/              # Global types
├── providers/              # Context providers
└── styles/                 # Global styles
```

### 7条结构规则
1. **功能隔离**——永远不要直接从其他功能中导入代码；使用共享组件或事件。
2. **模块化导出**——每个功能都有一个`index.ts`文件来定义其公共API。
3. **相关文件放在一起**——测试代码、故事（测试用例）和样式文件应与对应的组件放在同一目录下。
4. **文件大小限制**——每个文件的最大行数为300行；超过这个限制则应拆分文件。
5. **组件大小限制**——每个组件的JSX代码不超过50行；超过这个限制则应提取出可复用的组件。
6. **避免循环依赖**——使用`eslint-plugin-import`来强制检查。
7. **类型管理**——功能相关的类型放在功能文件中，共享类型放在专门的类型文件中。

### 命名规范

```
Components:     PascalCase.tsx       (UserProfile.tsx)
Hooks:          useCamelCase.ts      (useAuth.ts)
Utilities:      camelCase.ts         (formatCurrency.ts)
Types:          PascalCase.ts        (User.ts) or types.ts
Constants:      SCREAMING_SNAKE.ts   (API_ENDPOINTS.ts)
Test files:     *.test.tsx           (UserProfile.test.tsx)
Story files:    *.stories.tsx        (Button.stories.tsx)
```

---

## 第3阶段：组件设计模式

### 组件结构模板

```tsx
// 1. Imports (grouped: react → third-party → internal → types → styles)
import { useState, useCallback, memo } from 'react'
import { clsx } from 'clsx'
import { Button } from '@/shared/components/ui'
import type { User } from '../types'

// 2. Types (exported for reuse)
export interface UserCardProps {
  user: User
  onEdit?: (id: string) => void
  variant?: 'compact' | 'full'
  className?: string
}

// 3. Component (named export, not default)
export const UserCard = memo(function UserCard({
  user,
  onEdit,
  variant = 'full',
  className,
}: UserCardProps) {
  // 4. Hooks first
  const [isExpanded, setIsExpanded] = useState(false)

  // 5. Derived state (no useEffect for derived!)
  const displayName = `${user.firstName} ${user.lastName}`

  // 6. Handlers (useCallback for passed-down refs)
  const handleEdit = useCallback(() => {
    onEdit?.(user.id)
  }, [onEdit, user.id])

  // 7. Early returns for edge cases
  if (!user) return null

  // 8. JSX (max 50 lines)
  return (
    <div className={clsx('rounded-lg border p-4', className)}>
      <h3>{displayName}</h3>
      {variant === 'full' && <p>{user.bio}</p>}
      {onEdit && <Button onClick={handleEdit}>Edit</Button>}
    </div>
  )
})
```

### 组件组合模式

**1. 复合组件（用于相关的UI组件）**
```tsx
// Usage: <Tabs><Tabs.List><Tabs.Tab>A</Tabs.Tab></Tabs.List><Tabs.Panel>...</Tabs.Panel></Tabs>
const TabsContext = createContext<TabsContextType | null>(null)

export function Tabs({ children, defaultValue }: TabsProps) {
  const [activeTab, setActiveTab] = useState(defaultValue)
  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      {children}
    </TabsContext.Provider>
  )
}
Tabs.List = TabsList
Tabs.Tab = TabsTab
Tabs.Panel = TabsPanel
```

**2. 渲染属性（用于灵活的渲染逻辑）**
```tsx
export function DataList<T>({ items, renderItem, renderEmpty }: DataListProps<T>) {
  if (items.length === 0) return renderEmpty?.() ?? <EmptyState />
  return <ul>{items.map((item, i) => <li key={i}>{renderItem(item)}</li>)}</ul>
}
```

**3. 高阶组件（用于处理跨组件的通用逻辑）**
```tsx
export function withAuth<P>(Component: ComponentType<P>) {
  return function AuthenticatedComponent(props: P) {
    const { user, isLoading } = useAuth()
    if (isLoading) return <Spinner />
    if (!user) return <Navigate to="/login" />
    return <Component {...props} />
  }
}
```

### 10条组件设计规则
1. **每个文件只包含一个组件**。
2. **使用命名导出**——避免使用默认导出（以确保代码可维护性）。
3. **明确声明属性接口**——始终明确声明属性，并将其导出。
4. **不要在组件中编写业务逻辑**——将业务逻辑提取到钩子函数中。
5. **不要内联样式**——使用Tailwind CSS或CSS模块。
6. **避免使用字符串引用**——仅使用`useRef`来引用DOM元素。
7. **使用稳定的标识符**——不要使用`index`作为键。
8. **谨慎使用`Memo`缓存**——仅在需要频繁渲染的情况下使用。
9. **优先使用组合式设计**——尽可能使用组合式组件而不是类组件。
10. **默认情况下组件应该是可访问的**——使用语义化的HTML标签，并在需要时添加ARIA属性。

---

## 第4阶段：状态管理决策框架

### 状态类型决策树

```
Is it server data (from API)?
├─ YES → TanStack Query (or SWR) — NEVER Redux/Zustand for server state
│
└─ NO → Is it shared across features?
    ├─ YES → Is it complex with many actions?
    │   ├─ YES → Zustand (or Redux Toolkit if team knows it)
    │   └─ NO → Jotai (atomic) or Zustand (simple store)
    │
    └─ NO → Is it shared within a feature?
        ├─ YES → Context + useReducer (or Zustand feature store)
        └─ NO → useState / useReducer (component-local)
```

### 状态管理工具比较

| 工具 | 适用场景 | 包大小 | 学习难度 | 团队规模 |
|------|----------|--------|----------|-----------|
| `useState` | 适用于组件级别的状态 | 0KB | 易于学习 | 适合任何规模团队 |
| `useReducer` | 适用于复杂的组件状态 | 0KB | 学习难度较低 | 适合任何规模团队 |
| `Context` | 适用于特定功能的、使用频率较低的状态 | 0KB | 学习难度较低 | 适合任何规模团队 |
| `Zustand` | 适用于全局客户端状态 | 1.1KB | 学习难度中等 | 适合中等规模团队 |
| `Jotai` | 适用于原子化的、派生状态 | 3.4KB | 学习难度中等 | 适合中等规模团队 |
| `TanStack Query` | 适用于服务器端状态 | 12KB | 学习难度中等 | 适合任何规模团队 |
| `Redux Toolkit` | 适用于复杂的全局状态和中间件 | 11KB | 学习难度较高 | 适合大型团队 |

### 使用TanStack Query处理服务器端状态

```tsx
// api/users.ts — query key factory pattern
export const userKeys = {
  all: ['users'] as const,
  lists: () => [...userKeys.all, 'list'] as const,
  list: (filters: Filters) => [...userKeys.lists(), filters] as const,
  details: () => [...userKeys.all, 'detail'] as const,
  detail: (id: string) => [...userKeys.details(), id] as const,
}

// hooks/useUsers.ts
export function useUsers(filters: Filters) {
  return useQuery({
    queryKey: userKeys.list(filters),
    queryFn: () => fetchUsers(filters),
    staleTime: 5 * 60 * 1000, // 5 min
    placeholderData: keepPreviousData,
  })
}

export function useUpdateUser() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: updateUser,
    onMutate: async (newUser) => {
      // Optimistic update
      await queryClient.cancelQueries({ queryKey: userKeys.detail(newUser.id) })
      const previous = queryClient.getQueryData(userKeys.detail(newUser.id))
      queryClient.setQueryData(userKeys.detail(newUser.id), newUser)
      return { previous }
    },
    onError: (err, newUser, context) => {
      queryClient.setQueryData(userKeys.detail(newUser.id), context?.previous)
    },
    onSettled: (data, err, variables) => {
      queryClient.invalidateQueries({ queryKey: userKeys.detail(variables.id) })
      queryClient.invalidateQueries({ queryKey: userKeys.lists() })
    },
  })
}
```

### 使用Zustand处理客户端状态

```tsx
// stores/useUIStore.ts — thin, focused stores
interface UIStore {
  sidebarOpen: boolean
  theme: 'light' | 'dark' | 'system'
  toggleSidebar: () => void
  setTheme: (theme: UIStore['theme']) => void
}

export const useUIStore = create<UIStore>()(
  persist(
    (set) => ({
      sidebarOpen: true,
      theme: 'system',
      toggleSidebar: () => set((s) => ({ sidebarOpen: !s.sidebarOpen })),
      setTheme: (theme) => set({ theme }),
    }),
    { name: 'ui-preferences' }
  )
)

// Usage: const theme = useUIStore((s) => s.theme) — always use selectors!
```

### 5条状态管理规则
1. **服务器端状态与客户端状态分开**——永远不要将它们放在同一个状态存储库中。
2. **选择最小范围的状态管理工具**——优先使用`useState`，其次考虑`Context`和`Zustand`，最后考虑`Redux`。
3. **对于派生状态，避免使用`useEffect`**——使用`useMemo`或直接计算。
4. **始终使用选择器来获取状态**——使用`useStore(s => s.field)`而不是`useStore()`。
5. **URL中的参数属于状态的一部分**——搜索参数、筛选条件、分页信息等应存储在URL中，而不是客户端状态中。

---

## 第5阶段：钩子函数工程

### 自定义钩子函数模板

```tsx
// hooks/useDebounce.ts
export function useDebounce<T>(value: T, delayMs: number = 300): T {
  const [debouncedValue, setDebouncedValue] = useState(value)

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delayMs)
    return () => clearTimeout(timer)
  }, [value, delayMs])

  return debouncedValue
}
```

### 必备的自定义钩子函数库

| 钩子函数 | 用途 | 使用场景 |
|------|---------|-------------|
| `useDebounce` | 延迟处理值的变更 | 适用于搜索输入框、窗口大小调整等场景 |
| `useMediaQuery` | 根据屏幕分辨率调整布局 | 适用于响应式布局 |
| `useLocalStorage` | 保存持久化的本地状态 | 适用于保存用户偏好设置、草稿等 |
| `useIntersection` | 检测视口大小 | 适用于懒加载、无限滚动等场景 |
| `usePrevious` | 记录之前的状态值 | 适用于动画、比较等场景 |
| `useClickOutside` | 检测点击事件是否发生在组件外部 | 适用于下拉菜单、模态框等场景 |
| `useEventListener` | 安全地绑定事件监听器 | 适用于键盘输入、滚动、窗口大小调整等场景 |
| `useToggle` | 切换布尔值状态 | 适用于模态框、折叠面板等场景 |

### 钩子函数使用规则（超出React内置规则）
1. **每个钩子函数只处理一个特定的功能**——避免使用通用的`useUserSearch`钩子。
2. **返回元组或对象**——如果返回1-2个值时使用元组，如果返回多个值时使用对象。
3. **接受选项对象**——例如`useDebounce(value, { delay: 300 })`可以更好地控制延迟时间。
4. **确保钩子函数在卸载时进行清理**——在`useEffect`函数中处理所有的订阅和定时器。
5. **避免在条件语句中使用钩子函数**——将条件逻辑提取到钩子函数内部处理。

---

## 第6阶段：TypeScript集成

### 严格的TypeScript配置

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "exactOptionalPropertyTypes": true,
    "forceConsistentCasingInFileNames": true,
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

### 必备的类型声明规范

```tsx
// 1. Discriminated unions for state machines
type AsyncState<T> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: Error }

// 2. Polymorphic components
type ButtonProps<C extends ElementType = 'button'> = {
  as?: C
  variant?: 'primary' | 'secondary'
} & ComponentPropsWithoutRef<C>

export function Button<C extends ElementType = 'button'>({
  as,
  variant = 'primary',
  ...props
}: ButtonProps<C>) {
  const Component = as || 'button'
  return <Component {...props} />
}

// 3. Branded types for IDs
type UserId = string & { __brand: 'UserId' }
type PostId = string & { __brand: 'PostId' }

// 4. Zod for runtime validation
const userSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  role: z.enum(['admin', 'user', 'viewer']),
})
type User = z.infer<typeof userSchema>
```

### 5条TypeScript使用规则
1. **避免使用`any`类型**——使用`unknown`或具体的类型声明。
2. **在数据边界处使用Zod类型检查**——对所有外部数据（API返回的数据、表单输入、URL参数等）进行类型验证。
3. **使用明确的联合类型**——例如`{ status: 'success'; data: T }`而不是`{ data?: T; error?: Error }`。
4. **为ID类型指定明确的类型**——避免错误地传递类型，例如将`userId`当作`postId`使用。
5. **使用`satisfies`操作符进行类型检查**——`config satisfies Config`可以保持类型推断的准确性；`as Config`可能会导致类型推断错误。

---

## 第7阶段：性能优化

### 性能优化目标

| 性能指标 | 目标值 | 测量工具 |
|--------|--------|-------------|
| 首次渲染时间 | < 1.8秒 | Lighthouse |
| 最大渲染时间 | < 2.5秒 | Lighthouse |
| 从交互到下一次渲染的时间 | < 200毫秒 | Lighthouse |
| 累计布局变化量 | < 0.1 | Lighthouse |
| 压缩后的包大小 | < 200KB | webpack-bundle-analyzer |
| JavaScript执行时间（主线程） | < 3秒 | Chrome DevTools |

### 优化优先级

| 优先级 | 优化技术 | 影响程度 | 实施难度 |
|--------|-----------|--------|--------|
| P0 | 基于路由的代码分割 | 非常重要 | 实施难度低 |
| P0 | 图像优化 | 非常重要 | 实施难度低 |
| P1 | 模块化导入（Tree Shaking） | 中等重要 | 实施难度中等 |
| P1 | 长列表的虚拟化处理 | 中等重要 | 实施难度中等 |
| P1 | 对于计算密集型操作使用`useMemo`或`useCallback` | 中等重要 | 实施难度低 |
| P2 | 使用Web Workers进行计算密集型任务 | 低重要性 | 实施难度低 |

### 代码分割技巧

```tsx
// 1. Route-based (automatic with Next.js, manual with React Router)
const Dashboard = lazy(() => import('./features/dashboard'))
const Settings = lazy(() => import('./features/settings'))

// 2. Component-based (heavy components)
const Chart = lazy(() => import('./components/Chart'))
const MarkdownEditor = lazy(() =>
  import('./components/MarkdownEditor').then(m => ({ default: m.MarkdownEditor }))
)

// 3. Library-based (heavy third-party)
const { PDFViewer } = await import('@react-pdf/renderer')
```

### React编译器（React 19及以上版本）

```tsx
// With React Compiler enabled, manual memo/useMemo/useCallback become unnecessary
// The compiler auto-memoizes. Remove manual optimizations:
// ❌ const memoized = useMemo(() => expensiveCalc(data), [data])
// ✅ const memoized = expensiveCalc(data)  // compiler handles it

// Enable in babel config:
// plugins: [['babel-plugin-react-compiler', {}]]
```

### 渲染性能规则
1. **不要在组件内部创建新的组件**——应在模块级别定义组件。
2. **不要在JSX中直接创建对象或数组**——例如`style={{ color: 'red' }}`会导致不必要的重新渲染。
3. **将子组件作为属性传递**——这样可以避免不必要的重新渲染，例如`<Layout><ExpensiveChild /></Layout>`。
4. **键值对必须稳定且唯一**——避免使用`Math.random()`生成的键。
5. **避免频繁更改上下文状态**——使用`memoize`函数或拆分上下文状态。
6. **在优化之前先分析代码性能**——使用React DevTools的Performance Profiler进行性能分析。

---

## 第8阶段：错误处理与容错性

### 错误处理架构

```tsx
// Three levels of error boundaries:
// 1. App-level (catches everything, shows full-page error)
// 2. Feature-level (isolates feature failures)
// 3. Component-level (for risky widgets — charts, third-party)

// Modern error boundary with react-error-boundary
import { ErrorBoundary, FallbackProps } from 'react-error-boundary'

function FeatureErrorFallback({ error, resetErrorBoundary }: FallbackProps) {
  return (
    <div role="alert" className="rounded-lg border-red-200 bg-red-50 p-4">
      <h3>Something went wrong</h3>
      <pre className="text-sm text-red-600">{error.message}</pre>
      <button onClick={resetErrorBoundary}>Try again</button>
    </div>
  )
}

// Usage:
<ErrorBoundary FallbackComponent={FeatureErrorFallback} onReset={() => queryClient.clear()}>
  <DashboardFeature />
</ErrorBoundary>
```

### 错误处理检查清单
- [ ] 应用程序层面有错误处理机制，覆盖整个应用程序。
- [ ] 每个主要功能都有独立的错误处理边界。
- [ ] API错误通过`TanStack Query`的`onError`或错误状态来处理。
- [ ] 表单验证错误以直观的方式显示（而不是弹出警告）。
- [ ] 对于未知的路由，显示404页面。
- [ ] 支持离线状态，并提供优雅的降级体验。
- [ ] 将错误信息发送到监控系统（如Sentry）。
- [ ] 显示用户友好的错误信息（生产环境中不显示堆栈跟踪）。

---

## 第9阶段：表单与验证

### 表单库选择

| 库 | 适用场景 | 包大小 | 渲染性能 |
|---------|----------|--------|---------|
| React Hook Form | 适用于大多数表单 | 9KB | 渲染性能较低 |
| Formik | 适用于简单的表单 | 13KB | 每次按键操作时都会触发渲染 |
| TanStack Form | 适用于类型复杂的表单 | 5KB | 渲染性能可控 |
| Native | 适用于1-2个字段的表单 | 0KB | 包大小可自定义 |

**推荐方案：React Hook Form + Zod类型声明**

### 表单设计模式

```tsx
const schema = z.object({
  email: z.string().email('Invalid email'),
  password: z.string().min(8, 'Min 8 characters'),
  role: z.enum(['admin', 'user']),
})
type FormData = z.infer<typeof schema>

export function LoginForm({ onSubmit }: { onSubmit: (data: FormData) => void }) {
  const form = useForm<FormData>({
    resolver: zodResolver(schema),
    defaultValues: { email: '', password: '', role: 'user' },
  })

  return (
    <form onSubmit={form.handleSubmit(onSubmit)} noValidate>
      <label htmlFor="email">Email</label>
      <input id="email" type="email" {...form.register('email')} aria-invalid={!!form.formState.errors.email} />
      {form.formState.errors.email && (
        <p role="alert">{form.formState.errors.email.message}</p>
      )}
      {/* ... more fields */}
      <button type="submit" disabled={form.formState.isSubmitting}>
        {form.formState.isSubmitting ? 'Signing in...' : 'Sign in'}
      </button>
    </form>
  )
}
```

---

## 第10阶段：测试策略

### React应用的测试策略

| 测试层次 | 使用工具 | 测试目标 | 测试内容 |
|-------|------|-----------------|-------------|
| 单元测试 | Vitest | 80%的业务逻辑 | 钩子函数、辅助函数、状态管理器 |
| 组件测试 | 测试库 | 关键用户流程 | 组件渲染、交互逻辑 |
| 集成测试 | 测试库 | 多组件协同工作流程 |
| 端到端测试 | Playwright | 关键功能路径 | 用户认证、结账流程 |
| 可访问性测试 | Chromatic/Percy | UI组件的可访问性 |

### 7条测试规则
1. **测试组件的行为，而不是实现细节**——不要直接测试状态或`useEffect`函数。
2. **使用适当的查询方法**——优先使用`getByRole`、`getByTestId`、`getByText`等查询方法。
3. **模拟用户操作**——使用`userEvent.click`来模拟真实的用户交互。
4. **每个功能只进行一次断言**——避免每个测试都包含多个断言。
5. **在适当的边界处使用模拟函数**——例如API调用。
6. **避免使用快照测试**——快照测试会在代码变更时失效，无法准确反映实际行为。
7. **遵循“安排-执行-断言”的测试流程**——确保测试逻辑清晰易懂。

---

## 第11阶段：可访问性（符合AA级标准）

### 10项可访问性检查

1. **使用语义化的HTML标签**——例如使用`<button>`而不是`<div onClick>`。
2. **支持键盘导航**——所有可交互的元素都应可以通过Tab键访问，并且可以通过Enter/Space键操作。
3. **正确的焦点管理**——焦点元素应有明显的指示器，标签页的焦点顺序合理。
4. **为图片添加描述性`alt`属性**。
5. **合适的颜色对比度**——普通文本的对比度为4.5:1，大文本的对比度为3:1（WCAG AA标准）。
6. **为图标添加`aria-label`属性**。
7. **动态内容应使用`aria-live`属性**。
8. **减少动画效果**——根据用户偏好启用或禁用动画效果。
9. **使用屏幕阅读器进行测试**——可以使用VoiceOver（Mac）或NVDA（Windows）等工具。
10. **自动化测试**——使用`axe-core`等工具进行自动化测试。

---

## 第12阶段：生产环境部署

### 必须满足的条件（P0级）
- **启用TypeScript的严格模式，确保没有类型错误**。
- **所有测试都通过**。
- **分析压缩后的包大小，确保没有意外的大文件依赖**。
- **在应用程序和功能层面都有明确的错误处理边界**。
- **在构建时验证环境变量**。
- **配置正确的安全头部信息（CSP、HSTS、X-Frame-Options等）。
- **添加SEO相关的元标签（如标题、描述、OG标签）**。
- **集成分析和错误监控功能**。
- **达到性能目标（LCP < 2.5秒）**。

### 推荐的做法（P1级）
- **为组件库使用Storybook**。
- **进行可访问性自动化测试**。
- **为高风险功能启用开关机制**。
- **为拉取请求（PR）提供预览版本**。
- **在构建过程中检查包大小**（如果超过限制则失败）。

### 推荐的开发工具栈（2025年及以上版本）

| 功能 | 推荐工具 | 替代方案 |
|-------|---------------|-------------|
| 框架 | Next.js 15 | Remix、Vite SPA |
| 语言 | TypeScript（严格模式） | |
| 样式框架 | Tailwind CSS v4 | CSS Modules |
| 组件库 | shadcn/ui | Radix、Headless UI |
| 状态管理 | TanStack Query v5 | SWR |
| 客户端状态管理 | Zustand | Jotai |
| 表单库 | React Hook Form + Zod | TanStack Form |
| 测试工具 | Vitest + 测试库 | Jest |
| 端到端测试 | Playwright | Cypress |
| 代码风格检查 | Biome | ESLint + Prettier |
| 身份认证 | Auth.js（NextAuth） | Clerk、Lucia |
| 数据库 | Drizzle ORM | Prisma |
| 部署工具 | Vercel | Cloudflare、Fly.io |
| 监控工具 | Sentry | Datadog |

## 质量评分（0-100分）

| 评估维度 | 权重 | 评分标准 |
|--------|--------|--------------|
| 架构 | 20% | 结构设计、组件分离、设计模式 |
| 类型安全 | 15% | 使用严格的TypeScript类型声明、避免使用`any`类型 |
| 性能 | 15% | 核心Web性能指标、包大小 |
| 测试 | 15% | 测试覆盖率、测试质量 |
| 可访问性 | 10% | 符合WCAG AA标准、支持键盘操作和屏幕阅读器 |
| 状态管理 | 10% | 选择合适的工具、避免不必要的属性穿透 |
| 开发体验 | 5% | 代码风格检查、代码格式化、构建速度 |

**评分标准：**90分以上表示达到世界级水平；75-89分表示适合生产环境；60-74分表示需要改进；60分以下表示代码质量较低。**

## 常见错误及解决方法

| 缺误编号 | 常见错误 | 解决方法 |
|---|---------|-----|
| 1 | 在`useEffect`中处理派生状态 | 应将相关逻辑提取到`useMemo`或`useEffect`中 |
| 2 | 属性穿透超过5层 | 应使用`Context`、`Zustand`或组合式设计 |
| 3 | 在`useEffect`中直接获取数据 | 应使用`TanStack Query`或相应的框架提供的加载器 |
| 4 | 普通情况下使用默认导出 | 应使用命名导出以确保代码可维护性 |
| 5 | 在测试中测试实现细节 | 应使用测试库来测试组件的行为 |
| 6 | 组件代码过于庞大（超过500行） | 应将复杂逻辑提取到钩子函数或子组件中 |
| 7 | 没有设置错误处理边界 | 应在应用程序、功能层和组件层面设置明确的错误处理边界 |
| 8 | 对服务器端状态使用Redux | 应使用`TanStack Query`来处理API数据 |
| 9 | 直到最后才处理可访问性问题 | 从项目开始就应确保代码符合可访问性标准 |
| 10 | 未启用TypeScript的严格模式 | 应启用严格模式，并修复所有类型错误 |

## 常用命令

- “设置一个新的React项目” → 执行第1-2阶段的架构设计和结构配置。
- “审查我的组件” → 检查第3阶段的组件设计规则和代码质量。
- “帮助我选择状态管理方案” → 参考第4阶段的决策流程。
- “优化性能” → 执行第7阶段的性能优化措施。
- “添加错误处理机制” → 实施第8阶段的错误处理方案。
- “构建表单” → 使用第9阶段的表单设计模式。
- “为这个组件编写测试” → 执行第10阶段的测试流程。
- “检查可访问性” | 执行第11阶段的可访问性检查。
- “准备部署到生产环境” | 遵循第12阶段的部署要求。
- “审计我的React应用程序” | 对整个项目进行全面的性能和质量评估。
- “从类组件迁移到现代组件模式” | 采用现代的组件设计模式和钩子函数。

## 提升你的React开发能力

本文档提供了完整的开发方法论。如需针对特定行业的实现方案，可以购买**AfrexAI Context Pack**（价格：47美元）：
- **SaaS Context Pack**：适用于SaaS应用的React开发模式、账单界面、仪表板架构。
- **Fintech Context Pack**：适用于金融行业的React开发模式、实时数据处理、合规性要求。
- **Healthcare Context Pack**：适用于医疗行业的React开发模式、符合HIPAA标准的用户界面设计。

👉 查看所有10个Context Pack：https://afrexai-cto.github.io/context-packs/

### 更多的免费资源
- `afrexai-nextjs-production`：Next.js的生产环境开发指南。
- `afrexai-vibe-coding`：AI辅助的开发方法论。
- `afrexai-technical-seo`：针对React单页应用和服务器端渲染（SSR）的SEO优化方案。
- `afrexai-test-automation-engineering`：全面的测试策略。
- `afrexai-ui-design-system`：用户界面设计系统架构。