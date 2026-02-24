---
name: NextJS
slug: nextjs
version: 1.1.0
homepage: https://clawic.com/skills/nextjs
description: 使用 App Router、服务器组件、缓存、身份验证（auth）以及生产环境（production）的最佳实践来构建 Next.js 15 应用程序。
metadata: {"clawdbot":{"emoji":"⚡","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---
## 设置（Setup）

首次使用时，请阅读 `setup.md` 以了解项目的集成方式。

## 使用场景（When to Use）

当用户需要具备 Next.js 的相关技能（如路由管理、数据获取、缓存处理、身份验证或部署等）时，可以使用该工具。该工具负责处理应用路由模式、服务器与客户端之间的交互以及生产环境的优化工作。

## 架构（Architecture）

项目的核心代码模式存储在 `~/nextjs/` 目录下。有关具体设置方法，请参阅 `memory-template.md`。

```
~/nextjs/
├── memory.md          # Project conventions, patterns
└── projects/          # Per-project learnings
```

## 快速参考（Quick Reference）

| 主题 | 对应文件 |
|-------|------|
| 设置 | `setup.md` |
| 内存模板 | `memory-template.md` |
| 路由管理（并行请求、拦截请求） | `routing.md` |
| 数据获取与流式传输 | `data-fetching.md` |
| 缓存与数据验证 | `caching.md` |
| 身份验证 | `auth.md` |
| 部署 | `deployment.md` |

## 核心规则（Core Rules）

### 1. 默认情况下，所有组件均为服务器组件（Server Components）

在 Next.js 的应用路由（App Router）中，所有组件默认都是服务器组件。只有在使用 `useState`、`useEffect`、事件处理器或浏览器 API 时，才需要添加 `'use client'` 属性。服务器组件不能被导入到客户端组件中；它们只能作为子组件被使用。

### 2. 数据应在服务器端获取（Fetch Data on Server）

数据应在服务器端进行获取，而非在 `useEffect` 中处理。对于并行请求，可以使用 `Promise.all`。具体实现方式请参阅 `data-fetching.md`。

### 3. 有目的地使用缓存（Use Caching Intentionally）

`fetch` 方法会自动缓存数据；对于动态数据，可以使用 `cache: 'no-store` 来禁用缓存。如果需要重新验证数据，可以设置 `revalidate` 属性。相关策略请参阅 `caching.md`。

### 4. 使用服务器端函数处理数据变更（Server Actions for Mutations）

表单提交和数据变更操作应通过服务器端函数来处理。这种方式支持渐进式增强（progressive enhancement），即使不加载 JavaScript 代码也能正常工作。详情请参阅 `data-fetching.md`。

### 5. 环境安全（Environment Security）

`NEXT_PUBLIC_` 变量会暴露给客户端；服务器组件可以访问所有的环境变量。敏感信息应存储在 `.env.local` 文件中。

### 6. 大量数据的流式传输（Streaming for Large Data）

使用 `<Suspense>` 来逐步加载内容；对于加载速度较慢的组件，应单独进行流式传输处理。具体方法请参阅 `data-fetching.md`。

### 7. 身份验证应在中间件层面进行（Auth at Middleware Level）

身份验证逻辑应在中间件中实现，而不是在页面中。中间件运行在服务器端，因此可以进行轻量级的身份验证检查。详情请参阅 `auth.md`。

## 服务器组件与客户端组件（Server vs Client）

| 服务器组件 | 客户端组件 |
|------------------|------------------|
| 在应用路由中默认使用 | 需要添加 `'use client'` 属性 |
| 可以是异步的 | 不能是异步的 |
| 可以访问后端数据和环境变量 | 可以访问浏览器 API 和钩子函数 |
| 不会向客户端发送任何 JavaScript 代码 | 会向客户端发送 JavaScript 代码 |

**建议：** 先启动服务器端代码；仅在需要使用 `useState`、`useEffect`、`onClick` 或浏览器 API 时，才添加 `'use client` 属性。

## 常见问题及解决方法（Common Traps and Fixes）

| 问题 | 解决方案 |
|------|-----|
| 在服务器端使用 `router.push` | 应使用 `redirect()` 方法 |
| `<Link>` 组件会预加载所有内容 | 应设置 `prefetch={false}` |
| `next/image` 组件无法显示图片尺寸 | 应设置 `width`、`height` 或 `fill` 属性 |
| 客户端处理元数据 | 应将元数据处理逻辑移至服务器端或使用 `generateMetadata` 函数 |
| 在 `useEffect` 中处理数据获取 | 应在服务器端组件中获取数据 |
| 从服务器组件导入代码到客户端组件 | 应将代码作为子组件或属性传递给客户端组件 |
| 中间件中调用数据库操作 | 应通过 API 路由来调用数据库 |
| Next.js 15 版本中缺少 `await` 参数 | 在 Next.js 15 中，参数获取是异步的 |

## Next.js 15 的变化（Changes in Next.js 15）

- `params` 和 `searchParams` 现在都是 `Promise` 类型，必须使用 `await` 来处理它们。
- `fetch` 方法默认不会缓存数据；如需缓存，需使用 `cache: 'force-cache`。
- 推荐使用 React 19 的新钩子：`useActionState`、`useFormStatus`。

## 相关技能（Related Skills）

如果用户需要，可以使用以下命令安装相关工具：

```bash
clawhub install <slug>
```

- **React**：React 的基础知识与开发模式。
- **TypeScript**：提高代码的可维护性和类型安全性。
- **Prisma**：Next.js 应用的数据库 ORM 工具。
- **Tailwind CSS**：使用实用类进行样式设计。
- **Node.js**：服务器端运行时所需的知识。

## 反馈（Feedback）

- 如果觉得本文档有用，请给 `clawhub` 项目点赞（star）。
- 如需保持信息更新，请使用 `clawhub sync` 命令。