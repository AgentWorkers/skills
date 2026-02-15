---
name: Next.js
description: 避免常见的 Next.js 错误：服务器与客户端之间的边界问题、缓存相关的问题，以及 App Router 的使用陷阱。
metadata: {"clawdbot":{"emoji":"▲","requires":{"bins":["node"]},"os":["linux","darwin","win32"]}}
---

## 服务器组件与客户端组件  
- 在 App Router 中，默认使用的是服务器组件；这些组件不支持 `useState`、`useEffect`，也无法访问浏览器 API。  
- 如果需要在组件中使用客户端功能，需在文件顶部添加 ``use client`；这样该组件及其子组件将被标记为客户端组件。  
- 服务器组件不能被导入到客户端组件中，只能作为子组件或属性传递给客户端组件。  
- 客户端组件不能包含异步操作；只有服务器组件才能直接使用 `await`。  

## 缓存相关注意事项  
- `fetch` 请求在服务器组件中默认会被缓存；如果需要避免缓存动态数据，需添加 `cache: 'no-store'`。  
- 可使用 `revalidate` 方法来控制数据更新的频率（例如：`next: { revalidate: 60 }`）。  
- 路由处理函数默认不会被缓存（除非请求的是不包含动态数据的 `GET` 请求）。  
- 可通过 `revalidatePath('/path')` 或 `revalidateTag('tag')` 来按需刷新缓存。  

## 数据获取  
- 数据应从服务器组件中获取，而非使用 `useEffect`；这样可以避免不必要的数据请求，提升性能。  
- 可使用 `Promise.all` 并发获取多个数据源。  
- 使用 `loading.tsx` 来处理加载过程中的状态显示；`error.tsx` 用于处理加载错误。  

## 环境变量  
- 以 `NEXT_PUBLIC_` 为前缀的环境变量仅适用于客户端；服务器组件可以直接访问所有环境变量（无需前缀）。  
- 保密信息应存储在 `.env.local` 文件中（该文件不会被提交到代码仓库，但在 Git 中会被忽略）。  
- 运行时环境变量可以通过 `process.env` 获取；构建时的环境变量配置需在 `next.config.js` 中设置。  

## 路由处理函数（API 路由）  
- 路由处理函数应放在 `route.ts` 文件中；`pages/api` 文件用于管理 API 路由。  
- 需要导出的路由处理函数应明确指定方法名（如 `GET`、`POST` 等）。  
- `NextRequest` 和 `NextResponse` 是用于处理请求和响应的类型化对象。  
- 路由默认是动态的；如果需要强制使用静态路由，可设置 `export const dynamic = 'force-static'`。  

## 服务器端操作  
- 在函数或文件顶部添加 ``use server` 可将其标记为服务器端操作。  
- 客户端组件可以调用服务器端操作（实现远程过程调用，RPC）。  
- 可通过 `action={serverAction}` 在表单中触发服务器端操作（实现渐进式增强功能）。  
- 数据更新后需使用 `revalidatePath` 或 `revalidateTag` 来刷新缓存。  

## 中间件  
- 中间件在 Edge 环境中运行，而非 Node.js 环境；因此其可用的 API 和 npm 包有限。  
- 可使用 `matcher` 配置来限制中间件处理的路由范围（避免处理静态资源）。  
- 中间件不能抛出错误，否则应返回 `redirect()` 或 `next()` 来处理错误。  
- 可访问 Cookie 和请求头信息，但不能直接访问数据库。  

## 动态路由  
- 动态路由的路径名应为 `[slug]` 格式；`page.tsx` 组件会接收 `paramsslug` 参数。  
- 使用 `[...slug]` 可处理通配路由。  
- 使用 `generateStaticParams` 方法为静态渲染生成参数对象。  
- 将 `dynamicParams` 设置为 `false` 可实现 404 错误处理（表示路由不存在）；否则页面会按需渲染。  

## 常见错误  
- 不要在服务器组件中使用 `router.push`——该方法仅在客户端有效，应使用 `redirect()` 来重定向。  
- 使用 `<Link>` 标签进行预加载可能导致过多请求；可通过 `prefetch={false}` 来禁用预加载功能。  
- 使用 `next/image` 时必须指定图片的宽度和高度；如果没有 `fill` 属性，图片会填充整个视口。  
- 客户端组件中不应设置元数据；元数据应在服务器组件中生成。  
- 使用 `cookies()` 可使路由变得动态；但元数据无法在服务器端静态生成。