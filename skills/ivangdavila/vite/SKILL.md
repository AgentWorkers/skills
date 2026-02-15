---
name: Vite
description: 配置并优化 Vite，以适应开发环境、生产环境的构建需求以及库的打包过程。
metadata: {"clawdbot":{"emoji":"⚡","requires":{"bins":["node"]},"os":["linux","darwin","win32"]}}
---

# Vite 开发模式与最佳实践

## 环境变量
- 仅以 `VITE_` 为前缀的环境变量会暴露给客户端代码；`DB_PASSWORD` 保留在服务器端，`VITE_API_URL` 会被打包进最终生成的文件中。
- 应通过 `import.meta.env.VITE_*` 来访问这些变量，而不是 `process.env`（`process.env` 仅在 Node.js 环境中可用，在浏览器中可能未定义）。
- 文件 `*.env.local` 会覆盖 `*.env` 的配置，且默认情况下会被 Git 忽略——适用于存储本地敏感信息。
- `import.meta.env.MODE` 的值为 `development` 或 `production`，用于条件逻辑判断，而非 `NODE_ENV`。

## 兼容 CommonJS
- Vite 默认使用 ESM（ECMAScript Module Standard）格式；CommonJS 包需要通过 `optimizeDeps/include` 配置项才能被预打包到项目中。
- `require()` 在 Vite 中不可用，应使用 `import` 或 `createRequire` 来动态加载依赖。
- 有些 CommonJS 包的 ESM 导出可能存在问题——可以将这些包添加到 `ssr.noExternal` 或 `optimizeDeps.exclude` 列表中，让 Vite 自动处理。
- CommonJS 中的命名导出可能会导致导入失败——建议使用默认的导入方式并解构导入内容：`import pkg from 'pkg'; const { method } = pkg;`。

## 依赖项的预打包
- Vite 会在首次运行时预打包所有依赖项；修改依赖后需要删除 `node_modules/.vite` 文件以强制重新构建。
- 大型依赖项会降低开发服务器的启动速度——可以将不经常变化的依赖项添加到 `optimizeDeps.include` 列表中以实现缓存。
- 通过 `npm link` 创建的本地链接依赖项不会被自动预打包——需要手动将其添加到 `optimizeDeps.include` 列表中。
- 设置 `optimizeDeps.force: true` 会强制每次构建时重新打包所有依赖项——但这会降低开发效率。

## 路径别名
- 路径别名需要在 `vite.config.ts` 和 `tsconfig.json` 中同时配置——Vite 使用它自己的配置规则，而 TypeScript 使用 `tsconfig` 的配置。
- 应使用 `path.resolve(__dirname, './src')` 来构建路径，避免使用相对路径（因为相对路径会随工作目录的变化而变化）。
- `@/` 这样的路径别名不是 Vite 的内置功能，需要手动配置。

### 开发服务器代理
- 代理功能仅在开发模式下生效；生产环境需要使用真正的 CORS（跨源资源共享）配置或反向代理。
- `changeOrigin: true` 用于重写请求的 `Host` 头信息——大多数检查请求来源的 API 需要这个设置。
- WebSocket 代理需要设置 `ws: true`——HTTP 代理默认不会转发 WebSocket 请求。
- 路径末尾的斜杠很重要：`/api` 会代理到 `/api/users`，而 `/api/` 只会代理到 `/api//users`。

### 静态资源处理
- 放在 `public/` 目录下的文件会被直接 served（不经过处理），适用于图标、`robots.txt` 等文件，以及需要固定路径的资源。
- `src/assets/` 目录下的文件会被处理并添加哈希值，以便在代码中引用——适用于图片、字体等资源。
- 导入静态资源时使用 `import logo from './logo.png'`；硬编码的路径在构建后会失效。
- 动态路径可以使用 `new URL('./img.png', import.meta.url)` 来生成——模板字面量中的变量在构建后不再有效。

## 构建优化
- 使用 `build.rollupOptions.output/manualChunks` 来分割代码文件——否则生成的文件会非常庞大。
- 可使用 `rollup-plugin-visualizer` 来分析构建后的文件，找出意外的大型依赖项。
- `build.target` 默认设置为支持现代浏览器；如果需要兼容旧版本浏览器，可以设置为 `'es2015'`，但这会增加文件大小。
- `build.cssCodeSplit: true`（默认值）——每个异步代码块都会生成独立的 CSS 文件。

## 库模式
- 使用 `build.lib` 模式处理 npm 包——这与普通应用模式的配置不同。
- 对于第三方依赖（peer dependencies），应设置 `external` 属性，避免将 React/Vue 等库打包到库文件中。
- 需要使用 `tsc` 来生成类型声明文件（`.d.ts`）——Vite 本身不生成这些文件。
- 支持 ESM 和 CJS 两种格式的输出：`formats: ['es', 'cjs']`——某些客户端可能仍然需要 `require()` 来加载依赖。

## HMR（Hot Module Replacement）相关问题
- 循环导入会导致 HMR 功能失效——需要重构代码以打破循环，或者强制重新加载页面。
- 如果在 HMR 模式下状态丢失，组件可能无法接收更新——需要检查 `import.meta.hot.accept()` 的返回值。
- 如果 CSS 变更被导入到不支持 HMR 的 JavaScript 文件中，可能会导致页面完全重新加载——应在支持 HMR 的组件中导入 CSS。
- `server.hmr.overlay: false` 可以隐藏错误提示框——有助于自定义错误处理，但可能会掩盖问题。

## 静态服务器（SSR）配置
- 对于仅适用于 Node.js 的包，应使用 `ssr.external` 配置——避免将 `node_modules` 目录中的文件打包到 SSR 构建结果中。
- `ssr.noExternal` 可以强制所有依赖项都被打包——这对于包含浏览器特定导入的包是必要的。
- 在 SSR 模式下，CSS 导入可能会失败——可以使用 `?inline` 后缀或配置 `css.postcss` 来解决这个问题。