---
name: ui-development
description: 生成具备生产环境准备度的 Next.js 项目，这些项目将使用 TypeScript、Tailwind CSS、shadcn/ui 以及 API 集成。当用户需要构建、创建、开发或搭建 Next.js 应用程序、Web 应用程序、全栈项目或具有后端集成功能的前端应用时，可以使用此服务。优先采用现代技术栈（Next.js 14 及以上版本、TypeScript、shadcn/ui、axios、react-query）及最佳实践。此外，该服务还会在用户请求添加新功能、集成 API 或扩展现有 Next.js 项目时自动启动相关流程。
---

## UI 开发

我们可以从自然语言生成适用于生产环境的 Next.js 项目，该项目将使用 `shadcn/ui` 组件、API 集成、类型安全性和现代开发工具。

### 快速入门（简而言之）

**简单项目的快速路径：**
1. 创建 Next.js 应用程序 → 2. 安装 `shadcn/ui` → 3. 构建用户界面 → 4. 使用 PM2 启动服务器 → 5. 截取屏幕截图进行审查 → 6. 完成

**实时预览：** 项目在 PM2 上运行（端口 3002），可以通过 `http://localhost:3002` 访问，或者如果配置了 Nginx 代理，则可以通过该代理访问。

**默认工作流程：** 所有项目都使用 PM2 来管理开发服务器（防止端口冲突，确保只有一个实例运行）。

### 需求与可选功能

#### 必需依赖项
- **Node.js 18+** 以及 **npm/yarn/pnpm**
- **Git**（用于项目初始化）

#### 可选功能（用户可以选择不使用）

#### 1. 带有视觉审查的自动修订功能（需要 Chromium）
- **功能：** 在开发过程中截取屏幕截图以进行视觉审查并自动修复问题
- **安装方法：** `sudo apt-get install chromium-browser`（Debian/Ubuntu）
- **权限：** 对项目文件有读写权限，并能在无头模式下运行 Chromium
- **如果选择不使用：** 仅进行手动审查（由用户描述，用户确认）

#### 2. 实时预览服务器（需要 Nginx）
- **功能：** 在外部端口上提供项目实时预览（适用于移动设备测试或远程访问）
- **安装方法：** `sudo apt-get install nginx`
- **工作原理：** PM2 在端口 3002 上运行开发服务器，Nginx 将其代理到选定的外部端口
- **Nginx 配置模板：**
  ```nginx
  # /etc/nginx/sites-available/<project-name>
  server {
    listen <external-port>;  # e.g., 3001, 8081, etc.
    server_name _;
    
    location / {
      proxy_pass http://localhost:3002;  # PM2 dev server
      proxy_http_version 1.1;
      proxy_set_header Upgrade $http_upgrade;
      proxy_set_header Connection 'upgrade';
      proxy_set_header Host $host;
      proxy_cache_bypass $http_upgrade;
    }
  }
  ```
- **启用方法：** `sudo ln -s /etc/nginx/sites-available/<project-name> /etc/nginx/sites-enabled/ && sudo systemctl reload nginx`
- **如果选择不使用：** 直接通过 `http://localhost:3002` 访问（使用 PM2 的端口）

**在开始之前，请询问用户是否希望启用这些可选功能。**

### 常见项目类型

**常见请求的快速参考：**

- **仪表板/管理面板** → 使用 `(dashboard)` 路由组、`shadcn` 数据表和图表
- **首页** → 单个 `app/page.tsx` 文件，包含标题部分、功能网格和用户评价
- **待办事项/任务应用** → 使用 `shadcn` 的复选框、输入框和按钮；可以使用本地状态或 API
- **博客/内容管理系统** → 动态路由 `app/blog/[slug]/page.tsx`，支持 Markdown
- **电子商务** → 产品目录、购物车状态（使用 Zustand）
- **SaaS 应用** → 认证（使用 `(auth)` 组件）、受保护的路由和订阅逻辑
- **作品集** → 项目网格、联系表单和图片库
- **表单较多的应用** → 使用 React Hook Form 和 Zod 进行表单验证，以及 `shadcn` 的表单组件

**询问用户：** 您正在构建哪种类型的项目？（这有助于确定结构和所需组件）

### 技术栈

**核心组件：**
- Next.js 14+（应用路由）
- TypeScript
- Tailwind CSS v3
- **shadcn/ui**（推荐的 UI 组件库）
- ESLint + Prettier

**API 集成（默认）：**
- axios（HTTP 客户端）
- @tanstack/react-query（用于数据获取、缓存和状态管理）

**可选组件（根据需求选择）：**
- Zustand（客户端状态管理）
- Zod（运行时验证）
- next-auth（认证）
- Prisma（数据库对象关系映射）

### 项目结构

**符合行业标准的 Next.js 14+ 应用程序结构，采用基于功能的组织方式：**

```
<project-name>/
├── app/                                # Next.js 14 App Router
│   ├── (auth)/                         # Route group (auth pages)
│   │   ├── login/
│   │   │   └── page.tsx
│   │   ├── register/
│   │   │   └── page.tsx
│   │   └── layout.tsx                  # Auth-specific layout
│   ├── (dashboard)/                    # Route group (protected pages)
│   │   ├── dashboard/
│   │   │   ├── page.tsx
│   │   │   └── loading.tsx
│   │   ├── profile/
│   │   │   └── page.tsx
│   │   ├── settings/
│   │   │   └── page.tsx
│   │   └── layout.tsx                  # Dashboard layout with sidebar
│   ├── api/                            # API routes
│   │   ├── auth/
│   │   │   └── [...nextauth]/route.ts
│   │   └── users/
│   │       └── route.ts
│   ├── layout.tsx                      # Root layout
│   ├── page.tsx                        # Home page
│   ├── loading.tsx                     # Root loading UI
│   ├── error.tsx                       # Root error boundary
│   ├── not-found.tsx                   # 404 page
│   └── providers.tsx                   # Client providers (React Query, etc.)
│
├── components/
│   ├── ui/                             # shadcn/ui components (auto-generated)
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── input.tsx
│   │   ├── form.tsx
│   │   └── ...
│   ├── layout/                         # Layout components
│   │   ├── header.tsx
│   │   ├── footer.tsx
│   │   ├── sidebar.tsx
│   │   └── mobile-nav.tsx
│   ├── features/                       # Feature-specific components
│   │   ├── auth/
│   │   │   ├── login-form.tsx
│   │   │   └── register-form.tsx
│   │   ├── dashboard/
│   │   │   ├── stats-card.tsx
│   │   │   └── recent-activity.tsx
│   │   └── profile/
│   │       ├── profile-header.tsx
│   │       └── edit-profile-form.tsx
│   └── shared/                         # Shared/common components
│       ├── data-table.tsx
│       ├── search-bar.tsx
│       └── pagination.tsx
│
├── lib/                                # Utility functions & configurations
│   ├── api.ts                          # Axios instance + interceptors
│   ├── react-query.ts                  # React Query client config
│   ├── utils.ts                        # Utility functions (cn, formatters)
│   ├── validations.ts                  # Zod schemas
│   ├── constants.ts                    # App constants
│   └── auth.ts                         # Auth utilities (if using next-auth)
│
├── hooks/                              # Custom React hooks
│   ├── use-auth.ts                     # Authentication hook
│   ├── use-user.ts                     # User data hook (React Query)
│   ├── use-posts.ts                    # Posts data hook (React Query)
│   ├── use-media-query.ts              # Responsive design hook
│   └── use-toast.ts                    # Toast notifications (shadcn)
│
├── types/                              # TypeScript type definitions
│   ├── index.ts                        # Common types
│   ├── api.ts                          # API response types
│   ├── user.ts                         # User-related types
│   └── database.ts                     # Database types (Prisma generated)
│
├── actions/                            # Server Actions (Next.js 14+)
│   ├── auth.ts                         # Auth actions
│   ├── user.ts                         # User actions
│   └── posts.ts                        # Posts actions
│
├── config/                             # Configuration files
│   ├── site.ts                         # Site metadata (name, description, etc.)
│   └── navigation.ts                   # Navigation menu config
│
├── prisma/                             # Prisma ORM (if using database)
│   ├── schema.prisma                   # Database schema
│   └── migrations/                     # Database migrations
│
├── public/                             # Static assets
│   ├── images/
│   ├── icons/
│   └── fonts/
│
├── styles/                             # Global styles
│   └── globals.css                     # Tailwind imports + custom styles
│
├── .env.local                          # Environment variables (gitignored)
├── .env.example                        # Environment variables template
├── .eslintrc.json                      # ESLint config
├── .prettierrc                         # Prettier config
├── components.json                     # shadcn/ui config
├── next.config.js                      # Next.js config
├── tailwind.config.ts                  # Tailwind config
├── tsconfig.json                       # TypeScript config
├── package.json                        # Dependencies
└── README.md                           # Project documentation
```

### 目录用途

**`app/`** - Next.js 14 应用程序的页面和布局。使用路由组 `(name)` 进行逻辑分组，不会影响 URL。

**`components/`** - 所有的 React 组件，按类型分类：
- `ui/` - `shadcn/ui` 组件（可以直接复制粘贴并自定义）
- `layout/` - 公共布局组件（页眉、页脚、侧边栏）
- `features/` - 与特定功能相关的组件
- `shared/` - 在多个功能中可重用的组件

**`lib/`** - 实用函数、配置文件和第三方库的设置

**`hooks/`** - 自定义 React 钩子，特别是用于 API 调用的 React Query 钩子

**`types/`** - TypeScript 类型定义和接口

**`actions/`** - 用于处理表单和服务器端操作的服务器端函数（Next.js 14+）

**`config/`** - 应用程序配置（站点元数据、导航菜单、常量）

**`prisma/`** - 数据库模式和迁移文件（如果使用 Prisma）

**`public/`** - 静态文件，从根 URL 提供

**`styles/`** - 全局 CSS（包含 Tailwind CSS 和自定义样式）

### 工作流程

**在每个步骤中都向用户提供反馈——这是一个实时的构建日志。**

**⚠️ 重要提示：** 所有项目都使用 PM2 来管理开发服务器（默认端口为 3002）。这样可以确保：**
- 同时只运行一个实例（避免端口冲突）
- 简化进程管理（列出/重启/停止服务器）
- 在不同的终端会话中保持开发服务器的持续运行
- 提高错误日志记录和调试的效率

### 第 1 步：项目设置
- 询问用户：
  - 项目名称
  - 项目描述/用途
  - 是否需要可选功能（如 Chromium 视觉审查、Nginx 预览）

- 创建 Next.js 项目：
  ```bash
npx create-next-app@latest <project-name> \
  --typescript \
  --tailwind \
  --app \
  --no-src-dir \
  --import-alias "@/*"
```

**→ 向用户发送消息：“Next.js 项目已初始化 ✓”**

### 第 2 步：创建目录结构

按照行业最佳实践创建所有必要的目录：

```bash
cd <project-name>

# Create app route groups
mkdir -p app/\(auth\)/login app/\(auth\)/register
mkdir -p app/\(dashboard\)/dashboard app/\(dashboard\)/profile app/\(dashboard\)/settings
mkdir -p app/api/auth app/api/users

# Create component directories
mkdir -p components/ui components/layout components/features components/shared
mkdir -p components/features/auth components/features/dashboard components/features/profile

# Create utility directories
mkdir -p lib hooks types actions config

# Create static asset directories
mkdir -p public/images public/icons public/fonts

# Create styles directory
mkdir styles

# Create Prisma directory (if using database)
# mkdir -p prisma
```

**创建必要的配置文件：**

**`config/site.ts`** - 站点元数据
```typescript
export const siteConfig = {
  name: '<Project Name>',
  description: '<Project Description>',
  url: process.env.NEXT_PUBLIC_APP_URL || 'http://localhost:3000',
  links: {
    github: 'https://github.com/...',
  },
};
```

**`config/navigation.ts`** - 导航菜单
```typescript
export const mainNav = [
  { title: 'Home', href: '/' },
  { title: 'Dashboard', href: '/dashboard' },
  { title: 'Profile', href: '/profile' },
];

export const dashboardNav = [
  { title: 'Overview', href: '/dashboard' },
  { title: 'Profile', href: '/profile' },
  { title: 'Settings', href: '/settings' },
];
```

**`.env.example`** - 环境变量模板
```
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXT_PUBLIC_API_BASE_URL=http://localhost:3000/api
DATABASE_URL=postgresql://...
NEXTAUTH_SECRET=...
NEXTAUTH_URL=http://localhost:3000
```

**→ 向用户发送消息：“目录结构已创建 ✓”**

### 第 3 步：安装依赖项

**核心依赖项：**
```bash
cd <project-name>
npm install axios @tanstack/react-query
npm install -D @types/node
```

**推荐安装 `shadcn/ui`：**
```bash
npx shadcn-ui@latest init
```

系统会提示进行配置。推荐设置：
- 样式：默认样式
- 基本颜色：Slate
- CSS 变量：启用

**安装必要的 `shadcn` 组件：**
```bash
npx shadcn-ui@latest add button card input label select textarea
npx shadcn-ui@latest add dropdown-menu dialog sheet tabs
npx shadcn-ui@latest add table form avatar badge separator toast
```

**安装表单相关的依赖项（用于 `shadcn/ui` 表单）：**
```bash
npm install react-hook-form @hookform/resolvers zod
```

**根据用户需求选择是否安装其他可选依赖项：**
```bash
npm install zustand  # State management
npm install next-auth  # Authentication
npm install prisma @prisma/client  # Database ORM
```

**→ 向用户发送消息：“依赖项和 `shadcn/ui` 已安装 ✓”**

### 第 4 步：配置基础文件

#### `lib/api.ts`（axios 实例）
```typescript
import axios from 'axios';

export const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:3000/api',
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' }
});

// Request interceptor (add auth tokens, etc.)
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) config.headers.Authorization = `Bearer ${token}`;
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor (handle errors globally)
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized
    }
    return Promise.reject(error);
  }
);
```

#### `lib/react-query.ts`（查询客户端）
```typescript
import { QueryClient } from '@tanstack/react-query';

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60 * 1000, // 1 minute
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});
```

#### `app/providers.tsx`（为应用程序添加提供者）
```typescript
'use client';

import { QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { queryClient } from '@/lib/react-query';

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <QueryClientProvider client={queryClient}>
      {children}
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}
```

**更新 `app/layout.tsx` 以使用这些提供者。**

**→ 向用户发送消息：“基础配置已完成 ✓”**

### 第 5 步：生成功能

询问用户需要构建哪些功能/页面。对于每个功能：
1. **创建路由**（`app/<feature>/page.tsx`）
2. **创建组件**（`components/features/<feature>/`）
3. **创建 API 钩子**（使用 `react-query` 的 `use<Feature>.ts`）
4. **创建类型定义**（`types/<feature>.ts`）
5. **可选：创建 API 路由**（`app/api/<feature>/route.ts`）

**示例：用户个人资料功能**

```typescript
// types/user.ts
export interface User {
  id: string;
  name: string;
  email: string;
}

// hooks/useUser.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/lib/api';
import type { User } from '@/types/user';

export const useUser = (id: string) => {
  return useQuery({
    queryKey: ['user', id],
    queryFn: async () => {
      const { data } = await api.get<User>(`/users/${id}`);
      return data;
    },
  });
};

export const useUpdateUser = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async (user: Partial<User>) => {
      const { data } = await api.patch<User>(`/users/${user.id}`, user);
      return data;
    },
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['user', data.id] });
    },
  });
};

// app/profile/[id]/page.tsx
'use client';

import { useUser, useUpdateUser } from '@/hooks/useUser';

export default function ProfilePage({ params }: { params: { id: string } }) {
  const { data: user, isLoading, error } = useUser(params.id);
  const updateUser = useUpdateUser();

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div>
      <h1>{user?.name}</h1>
      <p>{user?.email}</p>
    </div>
  );
}
```

**→ 在每个功能完成后向用户发送消息：“个人资料页面已完成 ✓”**

### 第 6 步：使用 `shadcn/ui` 组件构建用户界面**

使用已安装的 `shadcn/ui` 组件来构建一致且易于使用的用户界面。遵循以下设计原则：

**示例：使用 `shadcn/ui` 的个人资料页面**
```typescript
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';

export default function ProfilePage({ params }: { params: { id: string } }) {
  const { data: user, isLoading } = useUser(params.id);

  if (isLoading) return <Card className="w-full max-w-2xl mx-auto"><CardContent>Loading...</CardContent></Card>;

  return (
    <Card className="w-full max-w-2xl mx-auto">
      <CardHeader>
        <div className="flex items-center gap-4">
          <Avatar className="h-20 w-20">
            <AvatarImage src={user?.avatar} />
            <AvatarFallback>{user?.name[0]}</AvatarFallback>
          </Avatar>
          <div>
            <CardTitle>{user?.name}</CardTitle>
            <p className="text-sm text-muted-foreground">{user?.email}</p>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <Button>Edit Profile</Button>
      </CardContent>
    </Card>
  );
}
```

**何时添加更多组件：**
- 表单 → `npx shadcn-ui@latest add form input label`
- 数据表 → `npx shadcn-ui@latest add table`
- 导航 → `npx shadcn-ui@latest add navigation-menu`
- 反馈 → `npx shadcn-ui@latest add toast alert`

**→ 向用户发送消息：“使用 `shadcn/ui` 构建的用户界面已完成 ✓`**

### 第 7 步：视觉审查（如果启用了 Chromium）

**重要提示：** 使用 PM2 来管理开发服务器（确保只运行一个实例，防止端口冲突）**

使用 PM2 启动开发服务器：
```bash
# Stop any existing instance of this project
pm2 delete <project-name> 2>/dev/null || true

# Start with PM2 (port 3002 for nginx proxy)
PORT=3002 pm2 start npm --name "<project-name>" --cwd "$(pwd)" -- run dev

# Give PM2 a moment to start
sleep 2
```

**等待服务器完全准备好**（这一步很关键——避免截图显示空白屏幕）：
```bash
# Wait for "Ready in" message in PM2 logs (usually 5-15 seconds)
timeout=30
elapsed=0
while [ $elapsed -lt $timeout ]; do
  if pm2 logs <project-name> --nostream --lines 50 2>/dev/null | grep -q "Ready in"; then
    echo "Server ready!"
    sleep 3  # Extra buffer for module loading
    break
  fi
  sleep 1
  elapsed=$((elapsed + 1))
done

# Verify server is responding
if ! curl -s http://localhost:3002 > /dev/null; then
  echo "Warning: Server not responding on port 3002"
  pm2 logs <project-name> --nostream --lines 20
fi
```

**截取屏幕截图（需要 Chromium）：**
```bash
bash scripts/screenshot.sh "http://localhost:3002" /tmp/review-desktop.png 1400 900
bash scripts/screenshot.sh "http://localhost:3002" /tmp/review-mobile.png 390 844
```

**审查检查清单**（使用 `image` 工具进行分析）：
- ✅ **桌面（1400px）**：内容居中，间距合适
- ✅ **移动设备（390px）**：
  - 没有水平滚动条（内容能完全显示在屏幕上）
  - 文本可读（不会太小）
  - 内容间距合适（使用 `p-4` 而不是 `p-24`）
  - 触控目标足够大（至少 44x44px）
  - 内容不会超出屏幕边界

**如果发现问题：** 修复响应式样式，然后重新截图。

**常见的修复方法：**
- 如果间距过大：将 `p-4` 更改为 `p-8 lg:p-12`
- 如果文本过大：将 `text-2xl` 更改为 `text-4xl`
- 如果内容太宽：添加 `max-w-full` 或 `px-4`

**→ 向用户发送消息：“审查完成，正在发送预览...”**

### 第 8 步：环境设置

创建 `.env.local` 文件：
```
NEXT_PUBLIC_API_BASE_URL=https://api.example.com
DATABASE_URL=postgresql://...
NEXTAUTH_SECRET=...
```

创建 `.env.example` 文件（供用户参考）。

**→ 向用户发送消息：“环境配置文件已创建 ✓****

### 第 9 步：脚本和文档

更新 `package.json` 中的脚本：
```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "type-check": "tsc --noEmit"
  }
}
```

创建 `README.md` 文件，内容包括：
- 设置说明
- 所需的环境变量
- 开发命令
- API 集成指南

**→ 向用户发送消息：“文档已完成 ✓****

### 第 10 步：导出和部署指导

**如果开发服务器正在运行，请停止它：**
```bash
pm2 delete <project-name> 2>/dev/null || true
pm2 save  # Persist PM2 process list
```

将项目压缩：
```bash
cd .. && zip -r /tmp/<project-name>.zip <project-name>/
```

通过消息工具将压缩后的项目文件发送给用户。

提供部署选项：
- **Vercel**（推荐）：`npx vercel`
- **Netlify**：`npm run build && netlify deploy`
- **Docker**：提供 Dockerfile
- **自托管**：提供 systemd 服务和相关 Nginx 配置

**→ 向用户发送消息：“项目已准备好！🚀****

## 测试和实时预览

### 开发过程中的快速测试

**1. PM2 开发服务器（在步骤 7 之后始终运行）：**
```bash
# Check status
pm2 list

# View logs
pm2 logs <project-name>

# Access locally
curl http://localhost:3002
```

**2. 实时预览地址：**
- **本地访问：** `http://localhost:3002`
- **Nginx 代理**（如果配置了代理）：`http://<server-ip>:<external-port>`
- **移动设备测试：** 使用 Nginx 代理或 ngrok 代理服务

**3. 如果启用了 Chromium，进行屏幕截图审查：**
```bash
# Desktop (1400x900)
bash scripts/screenshot.sh "http://localhost:3002" /tmp/desktop.png 1400 900

# Mobile (390x844)
bash scripts/screenshot.sh "http://localhost:3002" /tmp/mobile.png 390 844
```

### 全端测试工作流程

**完整的测试顺序：**
```bash
# 1. Check PM2 status
pm2 list | grep <project-name>

# 2. Verify dev server responding
curl -I http://localhost:3002

# 3. Take screenshots for visual verification
bash scripts/screenshot.sh "http://localhost:3002" /tmp/test-desktop.png 1400 900
bash scripts/screenshot.sh "http://localhost:3002" /tmp/test-mobile.png 390 844

# 4. Check logs for errors
pm2 logs <project-name> --lines 50 | grep -i error

# 5. Test API endpoints (if using API routes)
curl http://localhost:3002/api/health  # Example health check

# 6. Production build test
npm run build && npm run start  # Test production build

# 7. Type check
npm run type-check
```

### 常见测试场景

**场景 1：测试响应式设计**
```bash
# Mobile, tablet, desktop
for width in 390 768 1400; do
  bash scripts/screenshot.sh "http://localhost:3002" /tmp/screen-${width}.png $width 900
done
```

**场景 2：测试特定页面/路由**
```bash
# Take screenshot of specific route
bash scripts/screenshot.sh "http://localhost:3002/dashboard" /tmp/dashboard.png 1400 900
```

**场景 3：在做出更改后进行测试**
```bash
# PM2 auto-reloads on file changes, verify in logs
pm2 logs <project-name> --lines 20

# Wait for "compiled successfully" then take new screenshot
bash scripts/screenshot.sh "http://localhost:3002" /tmp/updated.png 1400 900
```

### 与用户共享预览

**选项 1：截图**
- 通过消息工具发送桌面和移动设备的截图
- 用户提供反馈，然后根据反馈进行迭代

**选项 2：使用 Nginx 代理和外部访问**
- 配置 Nginx 代理（参见可选功能）
- 分享地址：`http://<server-ip>:<port>`
- 用户可以在浏览器中直接测试

**选项 3：导出和部署**
- 将项目压缩后发送给用户
- 用户可以使用 Vercel 或 Netlify 进行部署
- 在生产环境中测试项目

## API 集成模式

### 模式 1：REST API（默认）

使用 axios 和 `react-query**：
```typescript
// hooks/usePosts.ts
import { useQuery, useMutation } from '@tanstack/react-query';
import { api } from '@/lib/api';

export const usePosts = () => {
  return useQuery({
    queryKey: ['posts'],
    queryFn: async () => {
      const { data } = await api.get('/posts');
      return data;
    },
  });
};

export const useCreatePost = () => {
  return useMutation({
    mutationFn: async (post: { title: string; body: string }) => {
      const { data } = await api.post('/posts', post);
      return data;
    },
  });
};
```

### 模式 2：GraphQL（可选）

安装相关依赖项：
```bash
npm install @apollo/client graphql
```

设置 Apollo 客户端，并使用 `useQuery` 和 `useMutation`。

### 模式 3：tRPC（可选）

对于需要类型安全的 Next.js API 路由：
```bash
npm install @trpc/server @trpc/client @trpc/react-query @trpc/next
```

### 模式 4：服务器端操作（Next.js 14+）

对于不需要 API 路由的表单处理：
```typescript
// app/actions.ts
'use server';

export async function createPost(formData: FormData) {
  const title = formData.get('title');
  // ...
}
```

**始终询问用户他们希望使用哪种模式。**

## 设计原则

请始终遵循这些设计原则，以确保项目质量。

### 布局和间距
- 保持一致的 Tailwind 布局间距（4, 6, 8, 12, 16, 20, 24）
- 内容的最大宽度：`max-w-5xl` 或 `max-w-6xl`
- 垂直布局比例：部分使用 `py-16`，子部分使用 `py-8`
- 移动设备：最小间距为 `px-4`

### 字体排版
- 清晰的层次结构（h1 → h2 → h3，最多使用 3-4 个级别）
- 行长度：最多 65-75 个字符
- 字体颜色对比度（粗体标题 → 正常文本）
- 文本颜色层次：`slate-900` → `slate-700` → `slate-500`

### 颜色和对比度
- 符合 WCAG AA 标准（对比度至少为 4.5:1）
- 限制颜色调色板（1 个主色调 + 1 个强调色 + 中性色）
- 一致地使用强调色（例如按钮、链接和活动状态）

### 响应式设计（非常重要）
- **以移动设备为先**（390px → 768px → 1024px）——始终优先考虑移动设备的显示效果
- **响应式间距**：使用 Tailwind 的响应式样式：
  - 移动设备：`p-4` 或 `px-4 py-6`（移动设备上禁止使用 `p-24`）
  - 平板设备：`md:p-8` 或 `md:px-6 md:py-8`
  - 桌面设备：`lg:p-12 xl:p-24`
  - 例如：`<main className="p-4 md:p-8 lg:p-12">`
- **响应式文本大小**：在移动设备上缩小标题大小：
  - 移动设备：`text-2xl` → 桌面设备：`md:text-4xl`
  - 移动设备：`text-lg` → 桌面设备：`md:text-2xl`
- **避免内容超出屏幕边界**：确保内容在 390px 宽度内显示
- **测试移动设备的屏幕截图**：检查内容是否超出屏幕边界
- 对于容器使用 `max-w-full`
- 对于较长的单词使用断字功能：`break-words`
- **触控目标**：按钮/链接的尺寸至少为 44x44px
- **在移动设备上使用网格布局**：当屏幕宽度较窄时，网格应缩放到单列：`grid-cols-1 md:grid-cols-2 lg:grid-cols-3`

### 组件（使用 `shadcn/ui`）
- **图标**：使用 `Lucide React` 图标（`shadcn/ui` 自带），避免使用 emoji
- **按钮**：使用 `<Button>` 组件，并提供不同的样式（默认、破坏性按钮、轮廓按钮、透明按钮）
- **表单**：使用 `shadcn` 的 `<Form>` 组件，并结合 `react-hook-form` 进行表单验证
- **卡片**：使用 `<Card>` 组件来展示内容
- **对话框/模态框**：使用 `<Dialog>` 或 `<Sheet>` 组件
- **加载状态**：使用 `shadcn` 的 `<Skeleton>` 组件来显示加载中的界面
- **错误处理**：使用 `<Alert>` 组件来显示错误信息
- **数据展示**：使用 `<Table>` 组件来展示表格数据

**`shadcn/ui` 的优点：** 易于使用、可定制、便于复制粘贴，且与 Tailwind CSS 兼容

### TypeScript 的最佳实践
- 启用严格模式
- 为函数指定明确的返回类型
- 对对象使用接口而不是 `any`
- 如果需要，使用 `unknown` 而不是 `any`
- 对不同的组件类型使用明确的联合类型

### 性能优化
- 使用 Next.js 的 `Image` 组件
- 对折叠后的内容使用懒加载
- 代码分割（动态导入）
- 对计算量较大的操作使用 `memoize` 和 `useMemo` 进行优化

### 常见的使用技巧

### 表单处理（使用 `shadcn/ui`）
```typescript
'use client';

import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';
import * as z from 'zod';
import { useMutation } from '@tanstack/react-query';
import { Button } from '@/components/ui/button';
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { useToast } from '@/components/ui/use-toast';

const formSchema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters'),
  email: z.string().email('Invalid email address'),
});

export default function ContactForm() {
  const { toast } = useToast();
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: { name: '', email: '' },
  });

  const mutation = useMutation({
    mutationFn: async (data: z.infer<typeof formSchema>) => {
      const res = await api.post('/contact', data);
      return res.data;
    },
    onSuccess: () => {
      toast({ title: 'Success', description: 'Message sent!' });
      form.reset();
    },
    onError: (error) => {
      toast({ title: 'Error', description: error.message, variant: 'destructive' });
    },
  });

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit((data) => mutation.mutate(data))} className="space-y-4">
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
        <Button type="submit" disabled={mutation.isPending}>
          {mutation.isPending ? 'Sending...' : 'Send Message'}
        </Button>
      </form>
    </Form>
  );
}
```

**注意：** 运行 `npx shadcn-ui@latest add form toast`，并安装 `npm install react-hook-form @hookform/resolvers zod` 以实现这些功能。

### 分页
```typescript
const usePaginatedPosts = (page: number) => {
  return useQuery({
    queryKey: ['posts', page],
    queryFn: async () => {
      const { data } = await api.get(`/posts?page=${page}`);
      return data;
    },
    keepPreviousData: true, // Smooth transitions
  });
};
```

### 无限滚动
```typescript
import { useInfiniteQuery } from '@tanstack/react-query';

const useInfinitePosts = () => {
  return useInfiniteQuery({
    queryKey: ['posts'],
    queryFn: async ({ pageParam = 1 }) => {
      const { data } = await api.get(`/posts?page=${pageParam}`);
      return data;
    },
    getNextPageParam: (lastPage, pages) => lastPage.nextPage,
  });
};
```

### 常见错误及避免方法

- ❌ 未使用 `QueryClientProvider` 包装应用程序
- ❌ 使用 axios 时未添加拦截器（无法处理错误）
- ❌ 在组件中未处理加载/错误状态
- ❌ 在进行数据更新后未取消之前的查询
- ❌ 使用 `any` 而不是适当的 TypeScript 类型
- 在可以使用服务器端组件的情况下使用客户端组件
- ❌ 未使用 Next.js 的 `Image` 组件（会导致性能损失）
- ❌ 未添加错误边界
- ❌ 未设置错误提示
- ❌ 在截图之前未等待开发服务器完全准备好
- ❌ 在截图之前未等待模块加载完成

### 故障排除

### 屏幕显示空白的问题
**问题：** 截图显示空白页面
**原因：** 开发服务器在截图之前未完全启动
**解决方法：**
- 等待开发服务器日志中显示“Ready in”的提示
- 在显示“Ready in”提示后等待 3-5 秒
- 在截图之前确认 `localhost:3000` 是否能在浏览器中正常加载

### 模块未找到错误
**问题：** React 报错“Module not found: Can't resolve @tanstack/react-query”
**原因：** 开发服务器在所有包加载完成之前就启动了
**解决方法：**
- 重启开发服务器：`pkill -f "next dev" && npm run dev`
- 检查 `node_modules` 目录中的包：`ls node_modules/@tanstack/`
- 在运行开发服务器之前等待 10-15 秒

### 开发服务器无法启动
**问题：** 端口已被占用（EADDRINUSE 错误）
**解决方法（使用 PM2）：**
```bash
# Check what's running
pm2 list

# Stop the conflicting process
pm2 delete <project-name>

# Or check port directly
lsof -ti:3002

# Kill process on port (if not PM2-managed)
kill -9 $(lsof -ti:3002)

# Restart with PM2
PORT=3002 pm2 start npm --name "<project-name>" --cwd "$(pwd)" -- run dev
```

### PM2 进程管理
- 列出所有 PM2 进程：**
```bash
pm2 list
```

**查看日志：**
```bash
pm2 logs <project-name> --lines 50
```

**重启一个进程：**
```bash
pm2 restart <project-name>
```

**停止一个进程：**
```bash
pm2 stop <project-name>
```

**删除一个进程：**
```bash
pm2 delete <project-name>
```

**确保只有一个实例运行：**
```bash
# Always delete before starting
pm2 delete <project-name> 2>/dev/null || true
PORT=3002 pm2 start npm --name "<project-name>" --cwd "$(pwd)" -- run dev
```

**常见的 PM2 使用场景：**

1. **项目无法启动** → 查看日志：`pm2 logs <project-name>`
2. **进程不断重启** → 检查是否有模块缺失或端口冲突
3. **更改未反映** → PM2 会自动重启，查看日志：`pm2 logs <project-name> | grep compiled`
4. **多个实例同时运行** → 删除所有进程：`pm2 delete all && pm2 list`
5. **监控进程使用情况**：`pm2 monit`（实时监控）
6. **保存 PM2 进程列表**：`pm2 save`（重启后列表仍然保留）

### 迭代和更新

当用户请求更改时：
1. 确定受影响的文件
2. 进行更改
3. PM2 会自动重启（文件更改后无需手动重启）
4. 运行类型检查：`npm run type-check`
5. 查看日志：`pm2 logs <project-name> --lines 20`
6. 如果启用了 Chromium，重新截图
7. 向用户报告更改内容及原因

### 快速参考卡片

### 常用命令
```bash
# Start dev server
pm2 delete <project-name> 2>/dev/null || true
PORT=3002 pm2 start npm --name "<project-name>" --cwd "$(pwd)" -- run dev

# Check status
pm2 list
pm2 logs <project-name>

# Take screenshots
bash scripts/screenshot.sh "http://localhost:3002" /tmp/desktop.png 1400 900
bash scripts/screenshot.sh "http://localhost:3002" /tmp/mobile.png 390 844

# Test production build
npm run build && npm run start

# Type check
npm run type-check
```

### 文件位置
- **组件：** `components/ui/`（`shadcn` 组件），`components/features/`（自定义组件）
- **页面：** `app/*/page.tsx`
- **API 路由：** `app/api/*/route.ts`
- **样式：** `app/globals.css`, `tailwind.config.ts`
- **配置：** `next.config.ts`, `.env.local`

### 常用的 `shadcn` 组件
```bash
npx shadcn-ui@latest add button input form card table dialog toast
```

### 实时预览地址
- **本地：** `http://localhost:3002`
- **Nginx 代理：** `http://<server-ip>:<external-port>`
- **移动设备测试：** 使用 Nginx 代理或 ngrok

### 故障排除方法：
1. **端口冲突** → 使用 `pm2 delete <name>` 后重新启动
2. **屏幕显示空白** → 等待“Ready in”的提示
3. **模块错误** → 安装依赖项后重新启动 PM2
4. **类型错误**：运行 `npm run type-check`
5. **布局问题** **检查响应式样式（使用 `p-4 md:p-8 lg:p-12`）**