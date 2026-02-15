---
name: Next.js
slug: nextjs
version: 1.0.2
description: 使用 App Router、服务器组件、缓存策略以及部署模式来构建 Next.js 应用程序。
---

## 使用场景

当用户需要具备 Next.js 的专业技能时（从路由配置到生产环境部署），代理（Agent）会处理应用程序路由（App Router）的模式、服务器与客户端之间的交互、缓存机制以及数据获取流程。

## 快速参考

| 主题 | 文件名 |
|-------|------|
| 路由模式 | `routing.md` |
| 数据获取 | `data-fetching.md` |
| 缓存策略 | `caching.md` |
| 部署 | `deployment.md` |

## 服务器组件与客户端组件

- 在应用程序路由（App Router）中，默认使用的是服务器组件（Server Component）——不支持 `useState`、`useEffect` 或浏览器 API。
- 如果希望某个组件及其子组件成为客户端组件（Client Component），需要在文件顶部添加 `use client`。
- 服务器组件不能被导入到客户端组件中，只能作为子组件或属性传递给客户端组件。
- 客户端组件不能使用异步操作（async），只有服务器组件可以直接使用 `await`。

## 缓存相关注意事项

- 在服务器组件中，`fetch` 请求默认会被缓存；如果需要防止缓存，可以使用 `cache: 'no-store'`。
- 可以通过 `revalidate` 属性设置缓存验证的时间间隔（例如：`next: { revalidate: 60 }`）。
- 路由处理函数（Route Handlers）默认不会被缓存，除非请求的数据是动态生成的。
- 如果需要按需缓存某个路由，可以使用 `revalidatePath('/path')` 或 `revalidateTag('tag')`。

## 数据获取

- 数据获取应在服务器组件中完成，而非使用 `useEffect`，这样可以避免不必要的请求并提升性能。
- 可以使用 `Promise.all` 来并行获取多个数据源。
- 使用 `loading.tsx` 来处理加载过程中的状态变化（Suspense）。
- 使用 `error.tsx` 来处理数据获取过程中的错误。

## 环境变量

- 以 `NEXT_PUBLIC_` 为前缀的环境变量仅适用于客户端；其他环境变量仅在服务器端可用。
- 服务器组件可以访问所有的环境变量，无需添加前缀。
- 用于存储敏感信息的变量应放在 `.env.local` 文件中；`.env` 文件会被提交到代码仓库，而 `.env.local` 文件会被 Git 忽略。
- 运行时的环境变量可以通过 `process.env` 获取；构建时的环境变量可以通过 `next.config.js` 配置。

## 路由处理函数（API 路由）

- 路由处理函数应放在 `route.ts` 文件中；`pages/api` 文件用于管理页面路由。
- 应该为路由函数指定具体的方法名称（如 `GET`、`POST` 等）。
- `NextRequest` 和 `NextResponse` 是用于处理请求和响应的对象类型。
- 默认情况下，路由处理函数是动态的；如果需要静态路由，可以使用 `export const dynamic = 'force-static` 来强制缓存。

## 服务器动作（Server Actions）

- 在函数或文件顶部添加 `use server` 可以将该函数标记为服务器动作。
- 客户端组件可以调用服务器动作，实现服务器与客户端之间的交互。
- 可以通过 `action={serverAction}` 在表单中触发服务器动作，实现渐进式增强（progressive enhancement）功能。
- 在数据发生变更后，需要使用 `revalidatePath` 或 `revalidateTag` 来重新验证缓存。

## 中间件（Middleware）

- 中间件在 Edge 环境中运行，而非 Node.js 环境；因此其可用的 API 和功能受到限制（例如：无法访问文件系统 `fs`，也无法使用 npm 包）。
- 可以使用 `matcher` 配置来限制中间件处理的路由范围（例如：避免处理静态资源）。
- 中间件不能抛出错误，必须返回 `redirect()` 或 `next()` 来继续处理请求。
- 中间件可以访问 cookie 和请求头信息，但不能直接访问数据库。

## 动态路由

- 使用 `[slug]` 作为参数路径；`page.tsx` 组件会接收到 `paramsslug` 参数。
- 使用 `[...slug]` 来处理通配路由；`generateStaticParams` 可以生成参数对象数组。
- 将 `dynamicParams` 设置为 `false` 可以避免 404 错误（表示参数未知）；否则会按需渲染页面。

## 常见错误

- 不要在服务器组件中使用 `router.push` 方法——该方法仅在客户端有效，应使用 `redirect()` 方法进行重定向。
- 使用 `<Link>` 标签进行预加载（prefetch）可能会导致过多的请求，可以通过 `prefetch={false}` 来禁用该功能。
- 使用 `next/image` 时必须指定图片的宽度和高度；如果没有 `fill` 属性，图片可能会填充整个视图区域。
- 客户端组件中不应设置元数据（metadata），元数据应在服务器组件中生成。
- 使用 `cookies()` 会使路由变得动态，因此无法在服务器端静态生成元数据。