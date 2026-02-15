---
name: Nuxt
description: 使用Vue 3构建支持服务器端渲染（SSR/SSG）的应用程序，并确保数据获取、组件渲染以及服务器端处理逻辑的正确实现。
metadata: {"clawdbot":{"emoji":"💚","requires":{"bins":["node"]},"os":["linux","darwin","win32"]}}
---

# Nuxt 3 开发模式

## 数据获取
- `useFetch` 可以在服务器端（SSR）重复请求并缓存结果——请在组件中使用它，而不是使用 `$fetch`（因为它会在服务器端和客户端都进行请求）。
- `$fetch` 仅用于事件处理器和服务器端路由——在 `<script setup>` 中使用它可能会导致数据不一致的问题。
- `useFetch` 仅在服务器端执行请求——如果需要仅在客户端获取的数据，请检查 `process.server`。
- 当 URL 参数发生变化但路径保持不变时，为 `useFetch` 添加 `key` 选项——否则缓存会返回旧数据。
- `useLazyFetch` 不会阻塞页面导航——适用于非关键数据，但需要处理请求的待处理状态。

## 数据渲染问题
- 在模板中使用 `Date.now()` 或 `Math.random()` 可能会导致数据渲染不一致——请在 `setup` 中计算一次数据，或者使用 `<ClientOnly>` 组件来避免这个问题。
- 仅适用于浏览器的 API（如 `localStorage`、`window`）可能会导致 SSR 失败——请将相关代码放在 `onMounted` 中执行，或者通过 `process.client` 来判断是否在客户端操作。
- 基于仅在客户端可用的状态进行条件渲染时，请使用带有回退逻辑的 `<ClientOnly>` 组件。
- 使用 `v-if` 与异步数据时可能会出现错误内容——此时应使用 `v-show` 或显示占位内容。

## 自动导入
- 存放在 `components/` 目录下的组件会自动导入——例如 `components/UI/Button.vue` 会被导入为 `<UIButton>`。
- 存放在 `composables/` 目录下的可组合函数（composables）必须以 `use*` 为前缀才能被自动导入——`utils.ts` 中导出的内容不会被自动导入。
- 服务器端工具函数（位于 `server/utils/`）仅在服务器端路由中被自动导入——在客户端代码中无法使用。
- 可以通过 `// @ts-nocheck` 注解禁用文件的自动导入，或者显式导入以避免命名冲突。

## 服务器端路由
- 存放在 `server/api/` 目录下的文件会被视为 API 路由——例如 `server/api/users.get.ts` 用于处理 `/api/users` 的 GET 请求。
- 方法名需要加上后缀（如 `.get.ts`、`.post.ts`）以区分不同的方法——否则所有请求都会被同一个方法处理。
- 使用 `query(event)` 获取查询参数，`readBody(event)` 获取 POST 请求的 body 数据——不要直接访问 `event.req`。
- 返回的值会自动序列化为 JSON 格式；如果发生错误，应抛出 `createError({ statusCode: 404 })`。

## 状态管理
- `useState` 是安全的，可以在页面切换后保持状态——普通的 `ref()` 在每次页面加载时都会被重置。
- `useState` 的键在整个应用中必须是唯一的——否则不同组件之间会共享状态。
- 使用 Pinia 时，需要使用 `storeToRefs()` 来保持状态的响应式——否则状态会失去响应性。
- 不要使用浏览器 API 来初始化 `useState` 中的状态——因为这些操作也会在服务器端执行。

## 中间件
- 全局中间件（以 `.global.ts` 为后缀）会在所有路由上执行——中间件的执行顺序是按字母顺序的。
- 在 `definePageMeta` 中定义的路由中间件会在全局中间件之后执行——可用于特定页面的授权检查。
- 中间件中的 `navigateTo()` 方法必须返回结果——如果忘记返回，页面会继续导航到原始路由。
- 服务器端中间件（位于 `server/middleware/`）会在所有服务器请求（包括 API 路由）上执行。

## 配置
- `runtimeConfig` 用于存储服务器端的配置信息；`runtimeConfig.public` 用于存储客户端可访问的值——环境变量可以通过 `NUXT_` 前缀进行覆盖。
- `app.config.ts` 用于存储构建时的配置信息，这些配置不需要环境变量——它们会被打包到应用中。
- 修改 `nuxt.config.ts` 需要重启应用；修改 `app.config.ts` 可以通过热加载实现。

## SEO 和元数据
- `useSeoMeta` 用于生成标准的元标签——它支持类型安全，并能自动处理 og:/twitter: 前缀。
- `useHead` 用于生成自定义的头部标签、脚本和链接——虽然更灵活，但不支持元标签名称的类型安全检查。
- 在 `definePageMeta` 中定义的元数据是静态的——可以使用 `useSeoMeta` 在 `setup` 中动态生成元数据。
- `nuxt.config` 中的 `titleTemplate` 用于统一页面标题——例如使用 `%s - My Site` 的格式。

## 插件
- 插件在应用创建之前执行——可以使用 `nuxtApp.hook('app:created')` 来执行创建后的逻辑。
- 使用 `provide` 可以通过 `useNuxtApp()` 访问插件提供的值——不过使用可组合函数（composables）会更加简洁。
- 插件的加载顺序：以数字为前缀的插件（如 `01.plugin.ts`）会先被加载，然后是按字母顺序加载的插件——依赖关系需要明确指定。
- 仅适用于客户端的插件以 `.client.ts` 为后缀；仅适用于服务器端的插件以 `.server.ts` 为后缀。

## 构建和部署
- `nuxt generate` 用于生成静态文件——但没有服务器，API 路由将无法正常工作。
- `nuxt build` 用于生成服务器端代码包——部署时需要使用 `.output` 目录。
- 可以使用 `routeRules` 来配置缓存策略——例如：`/blog/**` 路由的缓存时间为 1 小时。
- 可以指定某些路由需要预渲染——例如：`routeRules: { '/about': { prerender: true }` 表示该路由在构建时会生成静态 HTML。