---
name: Next.js
slug: nextjs
version: 1.0.1
description: 使用 App Router、服务器组件、缓存策略以及部署模式来构建 Next.js 应用程序。
---

## 适用场景

当用户需要 Next.js 的专业知识时（从路由配置到生产环境部署），Agent 负责处理 App Router 的相关逻辑，包括服务器与客户端之间的交互、缓存机制以及数据获取等。

## 快速参考

| 主题 | 对应文件 |
|-------|------|
| 路由模式 | `routing.md` |
| 数据获取 | `data-fetching.md` |
| 缓存策略 | `caching.md` |
| 部署 | `deployment.md` |

## 服务器组件与客户端组件

- 在 App Router 中，默认使用的是服务器组件（Server Component）——不支持 `useState`、`useEffect` 以及浏览器 API。
- 如果希望某个组件及其子组件成为客户端组件（Client Component），需在文件顶部添加 `use client`。
- 服务器组件不能被导入到客户端组件中，只能作为子组件或属性传递给客户端组件。
- 客户端组件不能使用异步操作（async），只有服务器组件可以直接使用 `await`。

## 缓存相关注意事项

- 在服务器组件中，`fetch` 请求默认会被缓存；如需避免缓存动态数据，需添加 `cache: 'no-store'`。
- 可通过 `revalidate` 配置来控制缓存更新频率（例如：`next: { revalidate: 60 }`）。
- 路由处理函数（Route Handlers）默认不会被缓存，除非请求的 URL 不包含动态参数。
- 可通过 `revalidatePath('/path')` 或 `revalidateTag('tag')` 来按需更新缓存。

## 数据获取

- 数据应通过服务器组件进行获取，而非使用 `useEffect`；这样可以避免不必要的请求并提升性能。
- 可使用 `Promise.all` 来并行获取多个数据源。
- 使用 `loading.tsx` 来处理加载状态；`error.tsx` 用于处理请求错误。

## 环境变量

- 以 `NEXT_PUBLIC_` 为前缀的变量仅适用于客户端；其他环境变量仅在服务器端可用。
- 服务器组件可以访问所有环境变量，无需添加前缀。
- 用于存储敏感信息的变量应放在 `.env.local` 文件中（该文件不会被提交到代码仓库）。
- 运行时环境变量可通过 `process.env` 获取；构建时环境变量可通过 `next.config.js` 进行配置。

## 路由处理函数（API 路由）

- 路由处理函数通常位于 `route.ts` 文件中；`pages/api` 文件用于定义 API 路由。
- 可通过导出函数来处理特定类型的请求（如 `GET`、`POST` 等）。
- `NextRequest` 和 `NextResponse` 是用于处理请求和响应的对象类型。
- 默认情况下，路由处理函数是动态的；如需强制缓存结果，可设置 `export const dynamic = 'force-static'`。

## 服务器动作（Server Actions）

- 在函数或文件顶部添加 `use server` 标签，即可将其标记为服务器动作。
- 客户端组件可以调用服务器动作；这种机制支持渐进式增强（progressive enhancement）。
- 可通过 `action={serverAction}` 在表单中触发服务器动作。
- 数据变更后需重新验证缓存（使用 `revalidatePath` 或 `revalidateTag`）。

## 中间件（Middleware）

- 中间件在 Edge 环境中运行，而非 Node.js 环境；因此其可用的 API 和 npm 包有限。
- 可通过 `matcher` 配置来限制中间件的执行范围（例如：避免处理静态资源）。
- 中间件不能抛出错误，否则应返回重定向（`redirect()`）或继续执行下一个请求（`next()`）。
- 中间件可以访问 Cookie 和请求头信息，但不能直接访问数据库。

## 动态路由

- 动态路由的路径名通常以 `[slug]` 的形式表示；`page.tsx` 组件会接收 `paramsslug` 参数。
- 使用 `[...slug]` 可处理通配路由；`generateStaticParams` 可用于生成静态路由参数。
- 将 `dynamicParams` 设置为 `false` 可避免 404 错误；否则页面会按需渲染。

## 常见错误

- 不要在服务器组件中使用 `router.push` 方法——该方法仅在客户端有效，应使用 `redirect()` 进行重定向。
- `<Link>` 标签的 `prefetch` 属性可能导致不必要的请求；建议将其设置为 `prefetch={false}` 以禁用预加载。
- 使用 `next/image` 时必须指定宽度（width）和高度（height）；如果父元素使用了定位（positioning），还需设置 `fill` 属性。
- 客户端组件中不应设置元数据（metadata）；元数据应在服务器组件中生成。
- 使用 `cookies()` 可使路由变得动态；但动态路由无法被静态生成。