---
name: shadcn-ui
model: fast
description: 使用 `shadcn/ui`、`Radix UI` 和 `Tailwind CSS` 构建可访问且可定制的用户界面（UI）。这些工具适用于配置 `shadcn/ui`、安装组件、使用 `React Hook Form` 和 `Zod` 构建表单、自定义主题，以及实现组件模式。
keywords: [shadcn, shadcn/ui, radix ui, tailwind, react components, forms, react hook form, zod, dialog, sheet, button, card, toast, select, dropdown, table, accessible components]
---

# shadcn/ui 组件模式

本指南旨在帮助您使用 shadcn/ui 构建可访问且可定制的 UI 组件。

## 安装

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install shadcn-ui
```

## 适用场景

- 使用 shadcn/ui 设置新项目
- 安装或配置单个组件
- 使用 React Hook Form 和 Zod 验证来构建表单
- 创建可访问的 UI 组件（按钮、对话框、下拉菜单、表格等）
- 使用 Tailwind CSS 自定义组件样式
- 使用 shadcn/ui 实现设计系统
- 使用 TypeScript 构建 Next.js 应用程序

## 什么是 shadcn/ui？

shadcn/ui 是一组可重用的组件，您可以直接将其复制到您的项目中——它不是一个 npm 包。您拥有这些组件的代码。它基于 **Radix UI**（可访问性框架）和 **Tailwind CSS**（样式系统）构建。

## 快速入门

```bash
# New Next.js project
npx create-next-app@latest my-app --typescript --tailwind --eslint --app
cd my-app
npx shadcn@latest init

# Install components
npx shadcn@latest add button input form card dialog select toast
npx shadcn@latest add --all  # or install everything
```

## 核心概念

### `cn` 工具

该工具用于合并 Tailwind 类并解决冲突，所有组件都会使用这个工具：

```tsx
import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

### 类型变体管理（Class Variance Authority, CVA）

该机制用于管理组件的不同变体，这是 shadcn/ui 组件背后的核心设计模式：

```tsx
import { cva, type VariantProps } from "class-variance-authority"

const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90",
        outline: "border border-input bg-background hover:bg-accent",
        secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/90",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 rounded-md px-3",
        lg: "h-11 rounded-md px-8",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: { variant: "default", size: "default" },
  }
)
```

## 核心组件

### 按钮（Button）

```tsx
import { Button } from "@/components/ui/button"
import { Loader2 } from "lucide-react"

// Variants: default | destructive | outline | secondary | ghost | link
// Sizes: default | sm | lg | icon
<Button variant="outline" size="sm">Click me</Button>

// Loading state
<Button disabled>
  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
  Please wait
</Button>

// As link (uses Radix Slot)
<Button asChild>
  <a href="/dashboard">Go to Dashboard</a>
</Button>
```

### 带验证功能的表单（Forms with Validation）

标准实现方式：使用 Zod 架构、React Hook Form 和 shadcn 提供的表单组件：

```bash
npx shadcn@latest add form input select checkbox textarea
```

```tsx
"use client"

import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import * as z from "zod"
import { Button } from "@/components/ui/button"
import {
  Form, FormControl, FormDescription,
  FormField, FormItem, FormLabel, FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

const formSchema = z.object({
  username: z.string().min(2, "Username must be at least 2 characters."),
  email: z.string().email("Please enter a valid email."),
  role: z.enum(["admin", "user", "guest"]),
})

export function ProfileForm() {
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: { username: "", email: "", role: "user" },
  })

  function onSubmit(values: z.infer<typeof formSchema>) {
    console.log(values)
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
        <FormField control={form.control} name="username" render={({ field }) => (
          <FormItem>
            <FormLabel>Username</FormLabel>
            <FormControl><Input placeholder="shadcn" {...field} /></FormControl>
            <FormDescription>Your public display name.</FormDescription>
            <FormMessage />
          </FormItem>
        )} />

        <FormField control={form.control} name="email" render={({ field }) => (
          <FormItem>
            <FormLabel>Email</FormLabel>
            <FormControl><Input type="email" {...field} /></FormControl>
            <FormMessage />
          </FormItem>
        )} />

        <FormField control={form.control} name="role" render={({ field }) => (
          <FormItem>
            <FormLabel>Role</FormLabel>
            <Select onValueChange={field.onChange} defaultValue={field.value}>
              <FormControl>
                <SelectTrigger><SelectValue placeholder="Select a role" /></SelectTrigger>
              </FormControl>
              <SelectContent>
                <SelectItem value="admin">Admin</SelectItem>
                <SelectItem value="user">User</SelectItem>
                <SelectItem value="guest">Guest</SelectItem>
              </SelectContent>
            </Select>
            <FormMessage />
          </FormItem>
        )} />

        <Button type="submit">Submit</Button>
      </form>
    </Form>
  )
}
```

### 对话框（Dialog）与表格（Sheet）

```tsx
import {
  Dialog, DialogContent, DialogDescription,
  DialogFooter, DialogHeader, DialogTitle, DialogTrigger,
} from "@/components/ui/dialog"
import {
  Sheet, SheetContent, SheetHeader, SheetTitle, SheetTrigger,
} from "@/components/ui/sheet"

// Modal dialog
<Dialog>
  <DialogTrigger asChild><Button variant="outline">Edit profile</Button></DialogTrigger>
  <DialogContent className="sm:max-w-[425px]">
    <DialogHeader>
      <DialogTitle>Edit profile</DialogTitle>
      <DialogDescription>Make changes here. Click save when done.</DialogDescription>
    </DialogHeader>
    <div className="grid gap-4 py-4">{/* form fields */}</div>
    <DialogFooter><Button type="submit">Save changes</Button></DialogFooter>
  </DialogContent>
</Dialog>

// Slide-over panel (side: "left" | "right" | "top" | "bottom")
<Sheet>
  <SheetTrigger asChild><Button variant="outline">Open</Button></SheetTrigger>
  <SheetContent side="right">
    <SheetHeader><SheetTitle>Settings</SheetTitle></SheetHeader>
    {/* content */}
  </SheetContent>
</Sheet>
```

### 卡片（Card）

```tsx
import {
  Card, CardContent, CardDescription,
  CardFooter, CardHeader, CardTitle,
} from "@/components/ui/card"

<Card className="w-[350px]">
  <CardHeader>
    <CardTitle>Create project</CardTitle>
    <CardDescription>Deploy your new project in one-click.</CardDescription>
  </CardHeader>
  <CardContent>
    <div className="grid w-full items-center gap-4">
      <div className="flex flex-col space-y-1.5">
        <Label htmlFor="name">Name</Label>
        <Input id="name" placeholder="Project name" />
      </div>
    </div>
  </CardContent>
  <CardFooter className="flex justify-between">
    <Button variant="outline">Cancel</Button>
    <Button>Deploy</Button>
  </CardFooter>
</Card>
```

### 通知弹窗（Toast Notifications）

```tsx
// 1. Add Toaster to root layout
import { Toaster } from "@/components/ui/toaster"

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}<Toaster /></body>
    </html>
  )
}

// 2. Use toast in components
import { useToast } from "@/components/ui/use-toast"
import { ToastAction } from "@/components/ui/toast"

const { toast } = useToast()

toast({ title: "Success", description: "Changes saved." })

toast({
  variant: "destructive",
  title: "Error",
  description: "Something went wrong.",
  action: <ToastAction altText="Try again">Try again</ToastAction>,
})
```

### 表格（Table）

```tsx
import {
  Table, TableBody, TableCaption, TableCell,
  TableHead, TableHeader, TableRow,
} from "@/components/ui/table"

const invoices = [
  { invoice: "INV001", status: "Paid", method: "Credit Card", amount: "$250.00" },
  { invoice: "INV002", status: "Pending", method: "PayPal", amount: "$150.00" },
]

<Table>
  <TableCaption>A list of your recent invoices.</TableCaption>
  <TableHeader>
    <TableRow>
      <TableHead>Invoice</TableHead>
      <TableHead>Status</TableHead>
      <TableHead>Method</TableHead>
      <TableHead className="text-right">Amount</TableHead>
    </TableRow>
  </TableHeader>
  <TableBody>
    {invoices.map((invoice) => (
      <TableRow key={invoice.invoice}>
        <TableCell className="font-medium">{invoice.invoice}</TableCell>
        <TableCell>{invoice.status}</TableCell>
        <TableCell>{invoice.method}</TableCell>
        <TableCell className="text-right">{invoice.amount}</TableCell>
      </TableRow>
    ))}
  </TableBody>
</Table>
```

## 主题设置（Theming）

shadcn/ui 使用 HSL 格式的 CSS 变量进行主题设置，具体配置在 `globals.css` 文件中：

```css
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --primary: 222.2 47.4% 11.2%;
    --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96.1%;
    --muted: 210 40% 96.1%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --destructive: 0 84.2% 60.2%;
    --border: 214.3 31.8% 91.4%;
    --ring: 222.2 84% 4.9%;
    --radius: 0.5rem;
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    --primary: 210 40% 98%;
    --primary-foreground: 222.2 47.4% 11.2%;
    /* ... mirror all variables for dark mode */
  }
}
```

在 Tailwind 配置中，颜色可以通过 `hsl(var(--primary))` 来引用。通过修改 CSS 变量即可重新设置整个应用程序的主题。

## 自定义组件

由于您拥有组件的代码，因此可以直接对其进行修改：

```tsx
// Add a custom variant to button.tsx
const buttonVariants = cva("...", {
  variants: {
    variant: {
      // ... existing variants
      gradient: "bg-gradient-to-r from-purple-500 to-pink-500 text-white",
    },
    size: {
      // ... existing sizes
      xl: "h-14 rounded-md px-10 text-lg",
    },
  },
})
```

## 组件参考

| 组件 | 安装方法 | 关键属性 |
|---------|-------------|------------|
| 按钮（Button） | `add button` | `variant`, `size`, `asChild` |
| 输入框（Input） | `add input` | 标准的 HTML 输入属性 |
| 表单（Form） | `add form` | 结合 React Hook Form 和 Zod 验证 |
| 卡片（Card） | `add card` | 包含标题、内容和底部元素 |
| 对话框（Dialog） | `add dialog` | 带有触发机制的模态框 |
| 表格（Sheet） | `add sheet` | 可滑动的面板，支持 `side` 属性 |
| 下拉菜单（Select） | `add select` | 可访问的下拉菜单 |
| 通知弹窗（Toast） | `add toast` | `variant: "default" \| "destructive"` |
| 表格（Table） | `add table` | 包含标题、行和单元格 |
| 标签页（Tabs） | `add tabs` | 提供默认值和触发/内容对 |
| 折叠菜单（Accordion） | `add accordion` | `type: "single" \| "multiple"` |
| 命令面板（Command） | `add command` | 提供命令面板或搜索功能 |
| 下拉菜单（Dropdown Menu） | `add dropdown-menu` | 提供上下文菜单或动作菜单 |
| 侧边栏（Menubar） | `add menubar` | 包含应用程序菜单和快捷方式 |

## 与 Next.js 的集成

### Next.js 路由器设置

对于 Next.js 13 及更高版本，确保交互式组件使用了 `use client`：

```tsx
// src/components/ui/button.tsx
"use client"

import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
// ... rest of component
```

### 布局集成

将通知弹窗（Toaster）添加到应用程序的根布局中：

```tsx
// app/layout.tsx
import { Toaster } from "@/components/ui/toaster"
import "./globals.css"

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="min-h-screen bg-background font-sans antialiased">
        {children}
        <Toaster />
      </body>
    </html>
  )
}
```

### 服务器端组件

大多数 shadcn/ui 组件需要使用 `use client`。对于服务器端组件，需要将它们包裹在客户端组件中或在客户端组件的子元素中使用。

## 命令行工具参考

```bash
npx shadcn@latest init              # Initialize project
npx shadcn@latest add [component]   # Add specific component
npx shadcn@latest add --all         # Add all components
npx shadcn@latest diff              # Show upstream changes
```

## 最佳实践

| 实践 | 说明 |
|---------|---------|
| **使用 TypeScript** | 所有组件都附带完整的类型定义 |
| **使用 Zod 进行验证** | 结合 React Hook Form 以创建类型安全的表单 |
| **`asChild` 模式** | 使用 Radix 的 Slot 功能将组件渲染为不同的元素 |
| **服务器端组件** | 大多数 shadcn/ui 组件需要使用 `use client` |
| **保持一致性** | 在自定义组件时遵循现有的设计模式 |
| **可访问性** | Radix 的基础组件已经处理了 ARIA 标签；除非必要，否则不要自行覆盖这些属性 |
| **使用 CSS 变量** | 通过变量来设置主题，而不是直接修改组件类 |
| **按需安装组件** | 只安装实际需要的组件，因为它们是独立的 |

## 绝对不要做的事情

| 绝对不要 | 原因 | 替代方法 |
|---------|---------|-----------|
| 将 shadcn 作为 npm 包安装 | 它不是普通的包，而是您可以自由使用的源代码 | 使用命令行工具：`npx shadcn@latest add` |
| 直接覆盖 ARIA 属性 | Radix 已经正确处理了可访问性相关的问题 | 请依赖 Radix 提供的基础组件 |
| 使用内联样式进行主题设置 | 这会破坏设计系统的一致性 | 应该通过修改 CSS 变量来设置主题 |
| 手动从文档中复制组件代码 | 可能会遗漏依赖关系 | 使用命令行工具进行正确的安装 |
| 混合组件的样式 | 这会导致样式不一致 | 应遵循组件设计模式（如 CVA） |

## 参考资源

- [学习指南](references/learn.md) — 从基础到高级模式的逐步学习指南
- [扩展组件](references/extended-components.md) — 包括终端界面、侧边栏、图表、动画和自定义钩子等功能
- [官方文档](https://ui.shadcn.com) | [Radix UI](https://www.radix-ui.com) | [React Hook Form](https://react-hook-form.com) | [Zod](https://zod.dev)