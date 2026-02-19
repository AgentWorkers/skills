---
name: stack-scaffold
description: 使用 Next.js App Router、Supabase、Firebase Auth、Vercel 和 Cloudflare 搭建一个全栈项目
user-invocable: true
---
# Stack Scaffold

作为一名全栈开发专家，当用户请求创建一个新的项目时，您需要按照以下规范来搭建项目的完整结构。在创建文件之前，务必与用户确认项目名称和目标目录。此技能仅会在空目录或新目录中创建文件，绝不会读取或修改现有的 `.env`、`.env.local` 或凭证文件。

## 规划流程（必填——在任何操作之前执行）

在编写任何文件或运行任何命令之前，您必须完成以下规划步骤：

1. **理解用户需求。** 用自己的话重新表述用户的需求，并识别任何模糊不清的地方。如果请求不够明确（例如：“创建一个项目”），请进一步询问具体细节（如项目名称、用途、特殊要求等）。

2. **检查环境。** 查看当前目录的结构及已安装的工具。运行 `ls` 和 `node -v` 以确认目标目录是否为空或尚未存在。切勿读取、打开或查看任何 `.env`、`.env.local` 或凭证文件。此技能仅用于创建新项目；如果目录中已存在项目，请先询问用户是否需要继续。

3. **制定执行计划。** 列出您将执行的步骤（包括要创建或修改的文件路径、要运行的命令以及每个步骤的预期结果）。在执行前，先在心中回顾这个计划。

4. **识别潜在风险。** 注意可能失败或导致数据丢失的步骤（例如覆盖文件、删除数据表、强制推送等）。针对每个风险，制定相应的缓解措施（如备份、预测试、确认等）。

5. **按顺序执行。** 严格按照计划逐步操作。每完成一个步骤后，验证其是否成功再进入下一个步骤。如果某个步骤失败，请诊断问题、更新计划并继续执行。

6. **总结。** 完成所有步骤后，简要总结创建了哪些内容、修改了哪些内容，以及用户还需要手动完成哪些配置。

请务必遵守此流程。不经过规划就直接执行可能会导致错误、系统状态混乱或浪费时间。

## 项目初始化

1. 运行 `npx create-next-app@latest <project-name> --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"` 来创建一个使用 Next.js 框架的项目（包含 App Router）。

2. 进入项目目录。

3. 确保 `.gitignore` 文件存在，并至少包含以下内容：`.env`、`.env.local`、`.env*.local`、`node_modules/`、`.next/`。`create-next-app` 模板中已经包含了这些文件，但在提交之前请再次确认。

4. 初始化 Git：`git init && git add -A && git commit -m "chore: initial Next.js scaffold"`。

## 依赖项安装

使用以下命令一次性安装所有依赖项：

```bash
npm install @supabase/supabase-js @supabase/ssr firebase firebase-admin zod zustand next-themes
npm install -D @types/node vitest @vitejs/plugin-react playwright @playwright/test prettier eslint-config-prettier
```

## 目录结构

在 `src/` 目录下创建以下结构：

```
src/
├── app/
│   ├── (auth)/
│   │   ├── login/page.tsx
│   │   └── signup/page.tsx
│   ├── (dashboard)/
│   │   └── page.tsx
│   ├── api/
│   │   └── health/route.ts
│   ├── layout.tsx
│   ├── page.tsx
│   └── globals.css
├── components/
│   ├── ui/           # Reusable UI primitives
│   └── shared/       # Shared composite components
├── lib/
│   ├── supabase/
│   │   ├── client.ts       # Browser Supabase client
│   │   ├── server.ts       # Server Supabase client (cookies-based)
│   │   ├── middleware.ts    # Auth refresh middleware helper
│   │   └── types.ts        # Generated DB types (placeholder)
│   ├── firebase/
│   │   ├── client.ts       # Firebase client SDK init
│   │   └── admin.ts        # Firebase Admin SDK init (server-only)
│   └── utils.ts
├── hooks/
│   └── use-auth.ts         # Auth state hook
├── stores/
│   └── user-store.ts       # Zustand user store
├── types/
│   └── index.ts
└── middleware.ts            # Next.js middleware for auth
```

## 文件内容

### `src/lib/supabase/client.ts`
```typescript
import { createBrowserClient } from "@supabase/ssr";

export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  );
}
```

### `src/lib/supabase/server.ts`
```typescript
import { createServerClient } from "@supabase/ssr";
import { cookies } from "next/headers";

export async function createClient() {
  const cookieStore = await cookies();
  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return cookieStore.getAll();
        },
        setAll(cookiesToSet) {
          try {
            cookiesToSet.forEach(({ name, value, options }) =>
              cookieStore.set(name, value, options)
            );
          } catch {
            // Called from Server Component — ignore
          }
        },
      },
    }
  );
}
```

### `src/lib/firebase/client.ts`
```typescript
import { initializeApp, getApps } from "firebase/app";
import { getAuth } from "firebase/auth";

const firebaseConfig = {
  apiKey: process.env.NEXT_PUBLIC_FIREBASE_API_KEY,
  authDomain: process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN,
  projectId: process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID,
  storageBucket: process.env.NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: process.env.NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID,
  appId: process.env.NEXT_PUBLIC_FIREBASE_APP_ID,
};

const app = getApps().length === 0 ? initializeApp(firebaseConfig) : getApps()[0];
export const auth = getAuth(app);
```

### `src/lib/firebase/admin.ts`
```typescript
import { initializeApp, getApps, cert } from "firebase-admin/app";
import { getAuth } from "firebase-admin/auth";

if (getApps().length === 0) {
  initializeApp({
    credential: cert({
      projectId: process.env.FIREBASE_PROJECT_ID,
      clientEmail: process.env.FIREBASE_CLIENT_EMAIL,
      privateKey: process.env.FIREBASE_PRIVATE_KEY?.replace(/\\n/g, "\n"),
    }),
  });
}

export const adminAuth = getAuth();
```

### `src/middleware.ts`
```typescript
import { type NextRequest, NextResponse } from "next/server";
import { createServerClient } from "@supabase/ssr";

export async function middleware(request: NextRequest) {
  let response = NextResponse.next({ request });

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return request.cookies.getAll();
        },
        setAll(cookiesToSet) {
          cookiesToSet.forEach(({ name, value }) =>
            request.cookies.set(name, value)
          );
          response = NextResponse.next({ request });
          cookiesToSet.forEach(({ name, value, options }) =>
            response.cookies.set(name, value, options)
          );
        },
      },
    }
  );

  await supabase.auth.getUser();

  return response;
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)"],
};
```

### `src/app/api/health/route.ts`
```typescript
import { NextResponse } from "next/server";

export async function GET() {
  return NextResponse.json({ status: "ok", timestamp: new Date().toISOString() });
}
```

### `.env.example`
```
# Supabase
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=

# Firebase Client
NEXT_PUBLIC_FIREBASE_API_KEY=
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=
NEXT_PUBLIC_FIREBASE_PROJECT_ID=
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=
NEXT_PUBLIC_FIREBASE_APP_ID=

# Firebase Admin (server-only)
FIREBASE_PROJECT_ID=
FIREBASE_CLIENT_EMAIL=
FIREBASE_PRIVATE_KEY=

# App
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

### `vercel.json`
```json
{
  "framework": "nextjs",
  "regions": ["gru1"],
  "headers": [
    {
      "source": "/api/(.*)",
      "headers": [
        { "key": "Cache-Control", "value": "no-store" }
      ]
    }
  ]
}
```

### `vitest.config.ts`
```typescript
import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";
import path from "path";

export default defineConfig({
  plugins: [react()],
  test: {
    environment: "jsdom",
    globals: true,
    setupFiles: ["./src/tests/setup.ts"],
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
});
```

## 搭建完成后需要执行的步骤

1. 将 `.env.example` 复制到 `.env.local` 文件中，并提醒用户填写相应的配置值。

2. 在 `supabase/migrations/00000000000000_init.sql` 文件中创建一个初始的 Supabase 迁移脚本（用于创建 `profiles` 表）：

```sql
create table public.profiles (
  id uuid references auth.users on delete cascade primary key,
  email text not null,
  full_name text,
  avatar_url text,
  created_at timestamptz default now() not null,
  updated_at timestamptz default now() not null
);

alter table public.profiles enable row level security;

create policy "Users can view own profile" on public.profiles
  for select using (auth.uid() = id);

create policy "Users can update own profile" on public.profiles
  for update using (auth.uid() = id);
```

3. 在 `package.json` 中添加相应的脚本：

```json
{
  "scripts": {
    "dev": "next dev --turbopack",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "format": "prettier --write .",
    "test": "vitest",
    "test:e2e": "playwright test",
    "types:supabase": "npx supabase gen types typescript --local > src/lib/supabase/types.ts"
  }
}
```

4. 提交更改：`git add -A && git commit -m "chore: 安装全栈框架（Next.js、Firebase Auth、Vercel）并配置相关设置"。

5. 打印一份总结，列出已创建的内容以及用户需要手动配置的内容（环境变量、Supabase 项目信息、Firebase 项目信息、Vercel 项目链接、Cloudflare DNS 配置等）。