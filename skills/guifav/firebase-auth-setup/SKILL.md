---
name: firebase-auth-setup
description: 配置 Firebase 认证：提供者（Providers）、安全规则（Security Rules）、自定义声明（Custom Claims）以及 React 认证钩子（React Auth Hooks）
user-invocable: true
---
# Firebase 认证设置

作为一名专注于安全的工程师，您的职责是在 Next.js 应用程序中配置 Firebase 认证。您需要设置认证提供者、创建 React 钩子、配置中间件，并将 Firebase 用户信息与 Supabase 用户资料进行同步。

## 规划流程（必读——在任何操作之前执行）

在创建或修改任何认证配置之前，您必须完成以下规划步骤：

1. **理解需求。** 明确：(a) 需要哪些认证提供者；(b) 这是初次设置还是对现有配置的补充；(c) 是否有基于角色的访问需求（自定义声明）；(d) 是否已经配置了 Firebase 与 Supabase 之间的数据同步。

2. **检查现有的认证设置。** 查看：(a) `src/lib/firebase/` 目录中是否存在客户端和管理员 SDK 的初始化代码；(b) `src/hooks/use-auth.ts` 文件中是否存在现有的认证钩子；(c) `src/middleware.ts` 文件中是否存在现有的认证中间件；(d) `src/app/api/auth/` 目录中是否存在用于数据同步的路由；(e) `.env.example` 文件（而非 `.env.local`）中列出了所需的 Firebase 环境变量。请勿读取 `.env.local` 或任何包含实际凭证值的文件。

3. **制定执行计划。** 明确：(a) 需要创建或修改哪些文件；(b) 文件的依赖顺序（先初始化 SDK，再编写钩子，然后是组件，最后是同步路由）；(c) 用户需要在 Firebase 控制台手动配置哪些设置。

4. **识别潜在风险。** 标记出可能的问题：(a) 对认证中间件的修改可能导致现有用户无法登录；(b) 数据同步路由的变更可能破坏 Firebase 与 Supabase 之间的用户映射关系；(c) 缺失的环境变量可能导致运行时错误。针对每个风险，制定相应的缓解措施。

5. **按步骤执行。** 按照依赖顺序创建或修改文件。修改每个文件后，验证其是否能正常编译。如果可能的话，对整个认证流程进行端到端的测试。

6. **总结。** 报告已配置的内容、新增或修改的文件，以及用户需要在 Firebase 控制台完成的操作（例如启用认证提供者、添加授权域名等）。

请务必遵守此流程。错误的认证配置可能会导致用户无法登录或产生安全漏洞。

## 架构概述

该系统使用 Firebase 进行用户认证，使用 Supabase 进行数据存储。具体流程如下：

1. 用户通过 Firebase（Google、Apple、电子邮件/密码等方式）进行身份验证。
2. Firebase 生成一个 JWT（身份令牌）。
3. Next.js 的中间件或服务器组件通过 Firebase Admin SDK 验证该令牌。
4. 在 Supabase 中创建或更新相应的用户资料（通过触发器或 API 路由实现数据同步）。
5. Supabase 的 RLS（Role-Based Security）策略会使用存储在 `profiles.id` 列中的 Firebase 用户 ID。

## 认证钩子

请在 `src/hooks/use-auth.ts` 文件中创建或修改相关代码：

```typescript
"use client";

import { useEffect, useState, useCallback } from "react";
import {
  onAuthStateChanged,
  signInWithPopup,
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  signOut as firebaseSignOut,
  GoogleAuthProvider,
  OAuthProvider,
  type User,
} from "firebase/auth";
import { auth } from "@/lib/firebase/client";

interface AuthState {
  user: User | null;
  loading: boolean;
  error: string | null;
}

export function useAuth() {
  const [state, setState] = useState<AuthState>({
    user: null,
    loading: true,
    error: null,
  });

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      setState({ user, loading: false, error: null });
    });
    return unsubscribe;
  }, []);

  const signInWithGoogle = useCallback(async () => {
    try {
      setState((prev) => ({ ...prev, loading: true, error: null }));
      const provider = new GoogleAuthProvider();
      await signInWithPopup(auth, provider);
    } catch (error: any) {
      setState((prev) => ({ ...prev, loading: false, error: error.message }));
    }
  }, []);

  const signInWithApple = useCallback(async () => {
    try {
      setState((prev) => ({ ...prev, loading: true, error: null }));
      const provider = new OAuthProvider("apple.com");
      provider.addScope("email");
      provider.addScope("name");
      await signInWithPopup(auth, provider);
    } catch (error: any) {
      setState((prev) => ({ ...prev, loading: false, error: error.message }));
    }
  }, []);

  const signInWithEmail = useCallback(
    async (email: string, password: string) => {
      try {
        setState((prev) => ({ ...prev, loading: true, error: null }));
        await signInWithEmailAndPassword(auth, email, password);
      } catch (error: any) {
        setState((prev) => ({ ...prev, loading: false, error: error.message }));
      }
    },
    []
  );

  const signUpWithEmail = useCallback(
    async (email: string, password: string) => {
      try {
        setState((prev) => ({ ...prev, loading: true, error: null }));
        await createUserWithEmailAndPassword(auth, email, password);
      } catch (error: any) {
        setState((prev) => ({ ...prev, loading: false, error: error.message }));
      }
    },
    []
  );

  const signOut = useCallback(async () => {
    try {
      await firebaseSignOut(auth);
    } catch (error: any) {
      setState((prev) => ({ ...prev, error: error.message }));
    }
  }, []);

  return {
    ...state,
    signInWithGoogle,
    signInWithApple,
    signInWithEmail,
    signUpWithEmail,
    signOut,
  };
}
```

## 认证提供者组件

请在 `src/components/shared/auth-provider.tsx` 文件中创建相关代码：

```typescript
"use client";

import { createContext, useContext } from "react";
import { useAuth } from "@/hooks/use-auth";
import type { User } from "firebase/auth";

interface AuthContextType {
  user: User | null;
  loading: boolean;
  error: string | null;
  signInWithGoogle: () => Promise<void>;
  signInWithApple: () => Promise<void>;
  signInWithEmail: (email: string, password: string) => Promise<void>;
  signUpWithEmail: (email: string, password: string) => Promise<void>;
  signOut: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const auth = useAuth();
  return <AuthContext.Provider value={auth}>{children}</AuthContext.Provider>;
}

export function useAuthContext() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuthContext must be used within an AuthProvider");
  }
  return context;
}
```

## 服务器端令牌验证

请在 `src/lib/firebase/verify-token.ts` 文件中创建或修改相关代码：

```typescript
import { adminAuth } from "@/lib/firebase/admin";

export async function verifyFirebaseToken(token: string) {
  try {
    const decodedToken = await adminAuth.verifyIdToken(token);
    return { uid: decodedToken.uid, email: decodedToken.email };
  } catch {
    return null;
  }
}
```

## Firebase 与 Supabase 用户同步

请在 `src/app/api/auth/sync/route.ts` 文件中创建代码，以实现 Firebase 用户信息与 Supabase 用户资料的同步：

```typescript
import { NextRequest, NextResponse } from "next/server";
import { adminAuth } from "@/lib/firebase/admin";
import { createClient } from "@supabase/supabase-js";

// Use service role for admin operations
const supabaseAdmin = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!
);

export async function POST(request: NextRequest) {
  const authHeader = request.headers.get("Authorization");
  if (!authHeader?.startsWith("Bearer ")) {
    return NextResponse.json({ error: "Missing token" }, { status: 401 });
  }

  try {
    const token = authHeader.split("Bearer ")[1];
    const decoded = await adminAuth.verifyIdToken(token);

    // Upsert profile in Supabase
    const { error } = await supabaseAdmin
      .from("profiles")
      .upsert(
        {
          id: decoded.uid,
          email: decoded.email || "",
          full_name: decoded.name || null,
          avatar_url: decoded.picture || null,
          updated_at: new Date().toISOString(),
        },
        { onConflict: "id" }
      );

    if (error) throw error;

    return NextResponse.json({ success: true });
  } catch (error: any) {
    return NextResponse.json(
      { error: error.message },
      { status: 401 }
    );
  }
}
```

## 登录页面模板

请在 `src/app/(auth)/login/page.tsx` 文件中创建登录页面的模板：

```typescript
"use client";

import { useAuthContext } from "@/components/shared/auth-provider";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

export default function LoginPage() {
  const { user, loading, error, signInWithGoogle, signInWithApple } =
    useAuthContext();
  const router = useRouter();

  useEffect(() => {
    if (user && !loading) {
      // Sync with Supabase on login
      user.getIdToken().then((token) => {
        fetch("/api/auth/sync", {
          method: "POST",
          headers: { Authorization: `Bearer ${token}` },
        }).then(() => router.push("/dashboard"));
      });
    }
  }, [user, loading, router]);

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <p className="text-muted-foreground">Loading...</p>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen items-center justify-center px-4">
      <div className="w-full max-w-sm space-y-6">
        <div className="text-center">
          <h1 className="text-2xl font-bold">Sign In</h1>
          <p className="mt-2 text-sm text-gray-500">
            Choose your preferred sign-in method
          </p>
        </div>

        {error && (
          <p className="rounded-md bg-red-50 p-3 text-sm text-red-600">
            {error}
          </p>
        )}

        <div className="space-y-3">
          <button
            onClick={signInWithGoogle}
            className="flex w-full items-center justify-center gap-2 rounded-lg border px-4 py-3 text-sm font-medium hover:bg-gray-50 transition-colors"
          >
            Continue with Google
          </button>
          <button
            onClick={signInWithApple}
            className="flex w-full items-center justify-center gap-2 rounded-lg border bg-black text-white px-4 py-3 text-sm font-medium hover:bg-gray-900 transition-colors"
          >
            Continue with Apple
          </button>
        </div>
      </div>
    </div>
  );
}
```

## 自定义声明

为实现基于角色的访问（管理员、编辑者、查看者等权限），请在相应文件中添加相关代码：

```typescript
// Set custom claims (run from a secure server context or admin script)
import { adminAuth } from "@/lib/firebase/admin";

export async function setUserRole(uid: string, role: "admin" | "editor" | "viewer") {
  await adminAuth.setCustomUserClaims(uid, { role });
}

// Verify role in API routes
export async function getUserRole(token: string): Promise<string | null> {
  try {
    const decoded = await adminAuth.verifyIdToken(token);
    return (decoded.role as string) || null;
  } catch {
    return null;
  }
}
```

## 添加新的认证提供者

当用户请求添加新的认证提供者时，请按照以下步骤操作：

1. 使用新的登录方式更新 `useAuth` 钩子。
2. 在登录页面上添加新的认证提供者按钮。
3. 在本地环境中测试整个登录流程。
4. 提醒用户在 Firebase 控制台（Settings > Authentication > Sign-in method）中启用新的认证提供者。
5. 提交代码更改：`feat: add <provider> authentication`。

## 安全检查清单

- [ ] Firebase API 密钥应存储在 `.env.local` 文件中（切勿将其提交到代码仓库）。
- [ ] Firebase 管理员凭证应通过环境变量进行管理。
- [ ] 所有受保护的路由都需要在服务器端验证 JWT 令牌。
- [ ] 自定义声明必须通过服务器端的管理员 SDK 进行设置。
- [ ] 数据同步接口需要使用 Firebase Admin 来验证令牌的有效性。
- [ ] 确保认证域的 CORS（跨源资源共享）配置正确。
- [ ] 对认证接口应用速率限制（通过 Cloudflare Guard 实现）。