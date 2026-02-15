---
name: shadcn-ui
version: 1.0.0
description: **使用场景：**  
适用于使用 `shadcn/ui` 组件构建用户界面（UI）、`Tailwind CSS` 布局、结合 `react-hook-form` 和 `zod` 创建表单结构、实现主题切换（theming）、暗黑模式（dark mode）、侧边栏布局（sidebar layouts）、移动端导航（mobile navigation），或任何与 `shadcn` 组件相关的问题或需求。
triggers:
  - shadcn
  - shadcn/ui
  - radix
  - component library
  - UI components
  - form pattern
  - react-hook-form
  - dark mode
  - theming
  - sidebar layout
  - dialog
  - sheet
  - toast
  - dropdown menu
  - command palette
  - data table
role: specialist
scope: implementation
output-format: code
---

# shadcn/ui 专家指南

本指南详细介绍了如何使用 shadcn/ui、Tailwind CSS、react-hook-form 和 zod 来构建高质量的生产级用户界面（UI）。

## 核心概念

shadcn/ui 并不是一个组件库，而是一组基于 Radix UI 原语构建的、可以直接复用的组件。这些组件的代码所有权属于您，您可以将它们直接添加到您的项目中，而无需将其作为依赖项进行安装。

## 安装

```bash
# Initialize shadcn/ui in a Next.js project
npx shadcn@latest init

# Add individual components
npx shadcn@latest add button
npx shadcn@latest add card
npx shadcn@latest add dialog
npx shadcn@latest add form
npx shadcn@latest add input
npx shadcn@latest add select
npx shadcn@latest add table
npx shadcn@latest add toast
npx shadcn@latest add dropdown-menu
npx shadcn@latest add sheet
npx shadcn@latest add tabs
npx shadcn@latest add sidebar

# Add multiple at once
npx shadcn@latest add button card input label textarea select checkbox
```

---

## 组件分类及使用场景

### 布局与导航
| 组件 | 使用场景 |
|---------|---------|
| `sidebar` | 具有可折叠部分的 app 级导航 |
| `navigation-menu` | 带有下拉菜单的顶级站点导航 |
| `breadcrumb` | 显示页面层次结构/位置 |
| `tabs` | 在同一上下文中切换相关视图 |
| `separator` | 用于分隔内容区域的视觉分隔符 |
| `sheet` | 可滑出的面板（用于移动导航、筛选器、详细信息显示） |
| `resizable` | 可调整大小的面板布局 |

### 表单与输入
| 组件 | 使用场景 |
|---------|---------|
| `form` | 需要验证的表单（用于包裹 react-hook-form） |
| `input` | 文本、电子邮件、密码、数字输入框 |
| `textarea` | 多行文本输入框 |
| `select` | 从列表中选择（类似原生选择框） |
| `combobox` | 可搜索的选择框（结合了 `command` 和 `popover` 功能） |
| `checkbox` | 布尔值或多选状态的切换 |
| `radio-group` | 从少量选项中选择单个选项 |
| `switch` | 开/关状态的切换（用于设置或偏好设置） |
| `slider` | 数值范围选择器 |
| `date-picker` | 日期选择器（结合了 `calendar` 和 `popover` 功能） |
| `toggle` | 表示按钮被按下/释放的状态 |

### 反馈与提示
| 组件 | 使用场景 |
|---------|---------|
| `dialog` | 弹出式确认框、表单或详细信息显示 |
| `alert-dialog` | 表示破坏性操作的确认提示（“你确定吗？”） |
| `sheet` | 用于显示表单、筛选器或移动导航的侧边面板 |
| `toast` | 短暂的非阻塞通知（通过 `sonner` 实现） |
| `alert` | 表示状态的消息（信息、警告、错误） |
| `tooltip` | 图标/按钮上的悬停提示 |
| `popover` | 点击时显示的丰富内容（如颜色选择器、日期选择器） |
| `hover-card` | 鼠标悬停时显示的内容预览（如用户资料、链接） |
| `skeleton` | 加载中的占位符 |
| `progress` | 任务完成进度指示器 |

### 数据显示
| 组件 | 使用场景 |
|---------|---------|
| `table` | 表格形式的数据展示 |
| `data-table` | 具有排序、筛选和分页功能的表格（基于 `@tanstack/react-table` 实现） |
| `card` | 包含标题、正文和脚注的内容容器 |
| `badge` | 表示状态、标签或计数的标签 |
| `avatar` | 用户资料图片 |
| `accordion` | 可折叠的常见问题解答或设置部分 |
| `carousel` | 图片/内容的轮播展示 |
| `scroll-area` | 可自定义滚动的容器 |

### 动作组件
| 组件 | 使用场景 |
|---------|---------|
| `button` | 主要操作按钮、表单提交 |
| `dropdown-menu` | 上下文菜单、动作菜单 |
| `context-menu` | 右键菜单 |
| `menubar` | 应用程序菜单栏 |
| `command` | 命令面板/搜索功能（使用 ⌘K 键调用）

---

## 表单设计模式（react-hook-form + zod）

### 完整的表单示例

```bash
npx shadcn@latest add form input select textarea checkbox button
```

```tsx
'use client'

import { zodResolver } from '@hookform/resolvers/zod'
import { useForm } from 'react-hook-form'
import { z } from 'zod'
import { Button } from '@/components/ui/button'
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Checkbox } from '@/components/ui/checkbox'
import { toast } from 'sonner'

const formSchema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters'),
  email: z.string().email('Invalid email address'),
  role: z.enum(['admin', 'user', 'editor'], { required_error: 'Select a role' }),
  bio: z.string().max(500).optional(),
  notifications: z.boolean().default(false),
})

type FormValues = z.infer<typeof formSchema>

export function UserForm() {
  const form = useForm<FormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      name: '',
      email: '',
      bio: '',
      notifications: false,
    },
  })

  async function onSubmit(values: FormValues) {
    try {
      await createUser(values)
      toast.success('User created successfully')
      form.reset()
    } catch (error) {
      toast.error('Failed to create user')
    }
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
        <FormField
          control={form.control}
          name="name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Name</FormLabel>
              <FormControl>
                <Input placeholder="John Doe" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl>
                <Input type="email" placeholder="john@example.com" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="role"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Role</FormLabel>
              <Select onValueChange={field.onChange} defaultValue={field.value}>
                <FormControl>
                  <SelectTrigger>
                    <SelectValue placeholder="Select a role" />
                  </SelectTrigger>
                </FormControl>
                <SelectContent>
                  <SelectItem value="admin">Admin</SelectItem>
                  <SelectItem value="editor">Editor</SelectItem>
                  <SelectItem value="user">User</SelectItem>
                </SelectContent>
              </Select>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="bio"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Bio</FormLabel>
              <FormControl>
                <Textarea placeholder="Tell us about yourself..." {...field} />
              </FormControl>
              <FormDescription>Max 500 characters</FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="notifications"
          render={({ field }) => (
            <FormItem className="flex flex-row items-start space-x-3 space-y-0">
              <FormControl>
                <Checkbox checked={field.value} onCheckedChange={field.onChange} />
              </FormControl>
              <div className="space-y-1 leading-none">
                <FormLabel>Email notifications</FormLabel>
                <FormDescription>Receive emails about account activity</FormDescription>
              </div>
            </FormItem>
          )}
        />

        <Button type="submit" disabled={form.formState.isSubmitting}>
          {form.formState.isSubmitting ? 'Creating...' : 'Create User'}
        </Button>
      </form>
    </Form>
  )
}
```

### 带有服务器处理的表单

```tsx
'use client'

import { useFormState } from 'react-dom'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'

export function ContactForm() {
  const form = useForm<FormValues>({
    resolver: zodResolver(schema),
  })

  async function onSubmit(values: FormValues) {
    const formData = new FormData()
    Object.entries(values).forEach(([key, value]) => formData.append(key, String(value)))
    await submitContact(formData)
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        {/* fields */}
      </form>
    </Form>
  )
}
```

---

## 主题设置与暗模式

### 使用 next-themes 进行主题配置

```bash
npm install next-themes
npx shadcn@latest add dropdown-menu
```

```tsx
// app/providers.tsx
'use client'
import { ThemeProvider } from 'next-themes'

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <ThemeProvider attribute="class" defaultTheme="system" enableSystem disableTransitionOnChange>
      {children}
    </ThemeProvider>
  )
}
```

```tsx
// components/theme-toggle.tsx
'use client'
import { Moon, Sun } from 'lucide-react'
import { useTheme } from 'next-themes'
import { Button } from '@/components/ui/button'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'

export function ThemeToggle() {
  const { setTheme } = useTheme()
  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="outline" size="icon">
          <Sun className="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
          <Moon className="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
          <span className="sr-only">Toggle theme</span>
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        <DropdownMenuItem onClick={() => setTheme('light')}>Light</DropdownMenuItem>
        <DropdownMenuItem onClick={() => setTheme('dark')}>Dark</DropdownMenuItem>
        <DropdownMenuItem onClick={() => setTheme('system')}>System</DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  )
}
```

### 在 `globals.css` 中自定义颜色

```css
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --primary: 222.2 47.4% 11.2%;
    --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96.1%;
    --secondary-foreground: 222.2 47.4% 11.2%;
    --muted: 210 40% 96.1%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --accent: 210 40% 96.1%;
    --accent-foreground: 222.2 47.4% 11.2%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;
    --border: 214.3 31.8% 91.4%;
    --ring: 222.2 84% 4.9%;
    --radius: 0.5rem;
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    --primary: 210 40% 98%;
    --primary-foreground: 222.2 47.4% 11.2%;
    /* ... etc */
  }
}
```

---

## 常见布局

### 带侧边栏的应用界面

```tsx
import { SidebarProvider, SidebarTrigger } from '@/components/ui/sidebar'
import { AppSidebar } from '@/components/app-sidebar'

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <SidebarProvider>
      <AppSidebar />
      <main className="flex-1">
        <header className="flex h-14 items-center gap-4 border-b px-6">
          <SidebarTrigger />
          <h1 className="text-lg font-semibold">Dashboard</h1>
        </header>
        <div className="p-6">{children}</div>
      </main>
    </SidebarProvider>
  )
}
```

### 具有移动导航的响应式页眉

```tsx
import { Sheet, SheetContent, SheetTrigger } from '@/components/ui/sheet'
import { Button } from '@/components/ui/button'
import { Menu } from 'lucide-react'

export function Header() {
  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur">
      <div className="container flex h-14 items-center">
        <div className="mr-4 hidden md:flex">
          <Logo />
          <nav className="flex items-center gap-6 text-sm ml-6">
            <Link href="/dashboard">Dashboard</Link>
            <Link href="/settings">Settings</Link>
          </nav>
        </div>

        {/* Mobile hamburger */}
        <Sheet>
          <SheetTrigger asChild>
            <Button variant="outline" size="icon" className="md:hidden">
              <Menu className="h-5 w-5" />
            </Button>
          </SheetTrigger>
          <SheetContent side="left" className="w-[300px]">
            <nav className="flex flex-col gap-4 mt-8">
              <Link href="/dashboard">Dashboard</Link>
              <Link href="/settings">Settings</Link>
            </nav>
          </SheetContent>
        </Sheet>

        <div className="flex flex-1 items-center justify-end gap-2">
          <ThemeToggle />
          <UserMenu />
        </div>
      </div>
    </header>
  )
}
```

### 卡片网格布局

```tsx
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

export function StatsGrid({ stats }: { stats: Stat[] }) {
  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      {stats.map((stat) => (
        <Card key={stat.label}>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">{stat.label}</CardTitle>
            <stat.icon className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stat.value}</div>
            <p className="text-xs text-muted-foreground">{stat.description}</p>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}
```

---

## Tailwind CSS 设计模式

### 常用实用组件

```tsx
// Centering
<div className="flex items-center justify-center min-h-screen">

// Container with max-width
<div className="container mx-auto px-4">

// Responsive grid
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">

// Sticky header
<header className="sticky top-0 z-50 border-b bg-background/95 backdrop-blur">

// Truncated text
<p className="truncate">Very long text...</p>

// Line clamp
<p className="line-clamp-3">Multi-line truncation...</p>

// Aspect ratio
<div className="aspect-video rounded-lg overflow-hidden">

// Animations
<div className="animate-pulse">    {/* Loading skeleton */}
<div className="animate-spin">     {/* Spinner */}
<div className="transition-all duration-200 hover:scale-105">
```

### 按钮样式变体

```tsx
<Button>Default</Button>
<Button variant="secondary">Secondary</Button>
<Button variant="outline">Outline</Button>
<Button variant="ghost">Ghost</Button>
<Button variant="link">Link</Button>
<Button variant="destructive">Delete</Button>
<Button size="sm">Small</Button>
<Button size="lg">Large</Button>
<Button size="icon"><Plus className="h-4 w-4" /></Button>
<Button disabled>Disabled</Button>
<Button asChild><Link href="/page">As Link</Link></Button>
```

---

## 通知提示

```bash
npx shadcn@latest add sonner
```

```tsx
// app/layout.tsx
import { Toaster } from '@/components/ui/sonner'

export default function RootLayout({ children }) {
  return (
    <html><body>{children}<Toaster /></body></html>
  )
}

// Usage anywhere
import { toast } from 'sonner'

toast.success('User created')
toast.error('Something went wrong')
toast.info('New update available')
toast.warning('This action cannot be undone')
toast.promise(asyncAction(), {
  loading: 'Creating...',
  success: 'Created!',
  error: 'Failed to create',
})
```

---

## 命令面板（⌘K）

```tsx
'use client'
import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import {
  CommandDialog,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from '@/components/ui/command'

export function CommandPalette() {
  const [open, setOpen] = useState(false)
  const router = useRouter()

  useEffect(() => {
    const down = (e: KeyboardEvent) => {
      if (e.key === 'k' && (e.metaKey || e.ctrlKey)) {
        e.preventDefault()
        setOpen((open) => !open)
      }
    }
    document.addEventListener('keydown', down)
    return () => document.removeEventListener('keydown', down)
  }, [])

  return (
    <CommandDialog open={open} onOpenChange={setOpen}>
      <CommandInput placeholder="Type a command or search..." />
      <CommandList>
        <CommandEmpty>No results found.</CommandEmpty>
        <CommandGroup heading="Navigation">
          <CommandItem onSelect={() => { router.push('/dashboard'); setOpen(false) }}>
            Dashboard
          </CommandItem>
          <CommandItem onSelect={() => { router.push('/settings'); setOpen(false) }}>
            Settings
          </CommandItem>
        </CommandGroup>
      </CommandList>
    </CommandDialog>
  )
}
```