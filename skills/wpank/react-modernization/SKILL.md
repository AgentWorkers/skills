---
name: react-modernization
model: reasoning
---

# React 现代化

将 React 应用程序从类组件升级为函数式组件（使用 Hooks），采用并发处理功能，并在主要版本之间进行迁移。

## 目的

提供系统化的方法来现代化 React 代码库：
- 将类组件迁移到函数式组件，并映射相应的生命周期方法
- 采用 React 18/19 中的并发处理功能
- 为 React 组件添加 TypeScript 类型支持
- 使用自动化代码修改工具（Codemods）进行批量重构
- 利用现代 API 优化应用程序性能

## 适用场景

- 将类组件迁移到使用 Hooks 的函数式组件
- 将 React 16/17 应用程序升级到 React 18/19
- 采用并发处理功能（如 Suspense、Transition 等）
- 将高阶组件（HOCs）和渲染属性（render props）转换为自定义 Hooks
- 为 React 项目添加 TypeScript 类型支持

## 关键词

React 升级、类组件到函数式组件、useEffect、useState、React 18、React 19、并发处理、Suspense、Transition、Codemod、迁移、现代化、函数式组件

## 安装

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install react-modernization
```

---

## 版本升级路径

### React 17 → 18 的重大变更

| 变更 | 影响 | 迁移方法 |
|--------|--------|-----------|
| 新的根 API | 必需 | 将 `ReactDOM.render` 替换为 `createRoot` |
| 自动批量处理 | 行为变化 | 状态更新现在在异步代码中批量执行 |
| 严格模式（Strict Mode） | 仅限开发环境 | Effects 在组件挂载/卸载时会被调用两次 |
| 服务器端的 Suspense | 可选 | 可以启用服务器端渲染（SSR）的流式处理 |

### React 18 → 19 的重大变更

| 变更 | 影响 | 迁移方法 |
|--------|--------|-----------|
| `use()` Hook | 新 API | 在渲染时可以读取 Promise 或上下文信息 |
| `ref` 作为属性 | 简化语法 | 不再需要 `forwardRef` |
| 上下文（Context）的提供方式 | 简化语法 | 使用 `<Context>` 而不是 `<Context.Provider>` |
| 异步操作 | 新模式 | 提供 `useActionState`、`useOptimistic` 等函数 |

---

## 类组件到函数式组件的迁移

### 生命周期方法的映射

```tsx
// componentDidMount → useEffect with empty deps
useEffect(() => {
  fetchData()
}, [])

// componentDidUpdate → useEffect with deps
useEffect(() => {
  updateWhenIdChanges()
}, [id])

// componentWillUnmount → useEffect cleanup
useEffect(() => {
  const subscription = subscribe()
  return () => subscription.unsubscribe()
}, [])

// shouldComponentUpdate → React.memo
const Component = React.memo(({ data }) => <div>{data}</div>)

// getDerivedStateFromProps → useMemo
const derivedValue = useMemo(() => computeFrom(props), [props])
```

### 状态管理的迁移方法

```tsx
// BEFORE: Class with multiple state properties
class UserProfile extends React.Component {
  state = { user: null, loading: true, error: null }
  
  componentDidMount() {
    fetchUser(this.props.id)
      .then(user => this.setState({ user, loading: false }))
      .catch(error => this.setState({ error, loading: false }))
  }
  
  componentDidUpdate(prevProps) {
    if (prevProps.id !== this.props.id) {
      this.setState({ loading: true })
      fetchUser(this.props.id)
        .then(user => this.setState({ user, loading: false }))
    }
  }
  
  render() {
    const { user, loading, error } = this.state
    if (loading) return <Spinner />
    if (error) return <Error message={error.message} />
    return <Profile user={user} />
  }
}

// AFTER: Custom hook + functional component
function useUser(id: string) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<Error | null>(null)

  useEffect(() => {
    let cancelled = false
    setLoading(true)
    
    fetchUser(id)
      .then(data => {
        if (!cancelled) {
          setUser(data)
          setLoading(false)
        }
      })
      .catch(err => {
        if (!cancelled) {
          setError(err)
          setLoading(false)
        }
      })

    return () => { cancelled = true }
  }, [id])

  return { user, loading, error }
}

function UserProfile({ id }: { id: string }) {
  const { user, loading, error } = useUser(id)
  
  if (loading) return <Spinner />
  if (error) return <Error message={error.message} />
  return <Profile user={user} />
}
```

### 高阶组件（HOC）到函数式组件的迁移

```tsx
// BEFORE: Higher-Order Component
function withUser(Component) {
  return function WithUser(props) {
    const [user, setUser] = useState(null)
    useEffect(() => { fetchUser().then(setUser) }, [])
    return <Component {...props} user={user} />
  }
}

const ProfileWithUser = withUser(Profile)

// AFTER: Custom hook (simpler, composable)
function useCurrentUser() {
  const [user, setUser] = useState(null)
  useEffect(() => { fetchUser().then(setUser) }, [])
  return user
}

function Profile() {
  const user = useCurrentUser()
  return user ? <div>{user.name}</div> : null
}
```

---

## React 18 及更高版本的并发处理功能

### 新的根 API（必需）

```tsx
// BEFORE: React 17
import ReactDOM from 'react-dom'
ReactDOM.render(<App />, document.getElementById('root'))

// AFTER: React 18+
import { createRoot } from 'react-dom/client'
const root = createRoot(document.getElementById('root')!)
root.render(<App />)
```

### 使用 `useTransition` 处理非紧急状态更新

```tsx
function SearchResults() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [isPending, startTransition] = useTransition()

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    // Urgent: update input immediately
    setQuery(e.target.value)
    
    // Non-urgent: can be interrupted
    startTransition(() => {
      setResults(searchDatabase(e.target.value))
    })
  }

  return (
    <>
      <input value={query} onChange={handleChange} />
      {isPending ? <Spinner /> : <ResultsList data={results} />}
    </>
  )
}
```

### 使用 Suspense 进行数据获取

```tsx
// With React 19's use() hook
function ProfilePage({ userId }: { userId: string }) {
  return (
    <Suspense fallback={<ProfileSkeleton />}>
      <ProfileDetails userId={userId} />
    </Suspense>
  )
}

function ProfileDetails({ userId }: { userId: string }) {
  // use() suspends until promise resolves
  const user = use(fetchUser(userId))
  return <h1>{user.name}</h1>
}
```

### React 19：`use()` Hook

```tsx
// Read promises directly in render
function Comments({ commentsPromise }) {
  const comments = use(commentsPromise)
  return comments.map(c => <Comment key={c.id} {...c} />)
}

// Read context (simpler than useContext)
function ThemeButton() {
  const theme = use(ThemeContext)
  return <button className={theme}>Click</button>
}
```

### React 19：异步操作（Actions）

```tsx
// useActionState for form submissions
function UpdateName() {
  const [error, submitAction, isPending] = useActionState(
    async (previousState, formData) => {
      const error = await updateName(formData.get('name'))
      if (error) return error
      redirect('/profile')
    },
    null
  )

  return (
    <form action={submitAction}>
      <input name="name" />
      <button disabled={isPending}>Update</button>
      {error && <p>{error}</p>}
    </form>
  )
}
```

---

## 自动化代码修改（Codemods）

### 运行官方提供的 React Codemods

```bash
# Update to new JSX transform (no React import needed)
npx codemod@latest react/19/replace-reactdom-render

# Update deprecated APIs
npx codemod@latest react/19/replace-string-ref

# Class to function components
npx codemod@latest react/19/replace-use-form-state
```

### 手动迁移策略

```bash
# Find class components
rg "class \w+ extends (React\.)?Component" --type tsx

# Find deprecated lifecycle methods
rg "componentWillMount|componentWillReceiveProps|componentWillUpdate" --type tsx

# Find ReactDOM.render (needs migration to createRoot)
rg "ReactDOM\.render" --type tsx
```

---

## TypeScript 的迁移

```tsx
// Add types to functional components
interface ButtonProps {
  onClick: () => void
  children: React.ReactNode
  variant?: 'primary' | 'secondary'
}

function Button({ onClick, children, variant = 'primary' }: ButtonProps) {
  return (
    <button onClick={onClick} className={variant}>
      {children}
    </button>
  )
}

// Type event handlers
function Form() {
  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
  }
  
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    console.log(e.target.value)
  }

  return (
    <form onSubmit={handleSubmit}>
      <input onChange={handleChange} />
    </form>
  )
}

// Generic components
interface ListProps<T> {
  items: T[]
  renderItem: (item: T) => React.ReactNode
}

function List<T>({ items, renderItem }: ListProps<T>) {
  return <>{items.map(renderItem)}</>
}
```

---

## 迁移检查清单

### 迁移前：
- [ ] 逐步升级依赖项
- [ ] 查看发布说明中的重大变更
- [ ] 设置全面的测试覆盖范围
- [ ] 创建特性分支

### 将类组件迁移到函数式组件：
- [ ] 从没有子组件的叶子组件开始迁移
- [ ] 将状态管理转换为 `useState`
- [ ] 将生命周期方法转换为 `useEffect`
- [ ] 将共享逻辑提取到自定义 Hooks 中
- [ ] 尽可能将高阶组件转换为 Hooks

### 升级到 React 18 及更高版本：
- [ ] 使用 `createRoot` API
- [ ] 在严格模式下测试代码，确保没有重复调用 Effects
- [ ] 解决组件 hydrate（渲染）时的问题
- [ ] 在适当的地方使用 Suspense
- [ ] 对于耗时的操作使用 Transition 功能

### 迁移后：
- [ ] 运行完整的测试套件
- [ ] 检查控制台是否有警告
- [ ] 测试迁移前后的性能
- [ ] 为团队记录所有变更

---

## 注意事项：

- **切勿**：
- 迁移后跳过测试
- 在一次提交中迁移多个组件
- 忽略严格模式（Strict Mode）的警告（这些警告可以帮助发现潜在问题）
- 不要盲目使用 `// eslint-disable-next-line react-hooks/exhaustive-deps`，除非你了解其原因
- 不要在同一个组件中混合使用类组件和函数式组件