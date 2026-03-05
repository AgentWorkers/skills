---
name: msw
description: MSW（Mock Service Worker）v2的最佳实践、模式以及API使用指南，适用于JavaScript/TypeScript测试和开发中的API模拟。内容包括处理器设计、服务器配置、响应生成、测试方法、GraphQL接口的支持，以及从v1到v2的迁移指南。基准版本：msw ^2.0.0。触发条件包括：msw的导入语句、http.get和http.post请求、HttpResponse对象的使用、setupServer和setupWorker函数的调用、graphql.query函数的执行，以及任何提及“msw”、“mock service worker”、“api mocking”或“msw v2”的内容。
license: MIT
user-invocable: false
agentic: false
compatibility: "TypeScript/JavaScript projects using msw ^2.0.0"
metadata:
  author: Anivar Aravind
  author_url: https://anivar.net
  source_url: https://github.com/anivar/msw-skill
  version: 1.0.0
  tags: msw, mocking, api, testing, http, graphql, service-worker, fetch
---
# MSW（Mock Service Worker）

**重要提示：** 关于 `msw` 的培训资料可能已经过时或不准确——MSW v2 完全移除了 `rest` 命名空间、`res(ctx.*)` 的响应构建方式以及 `(req, res, ctx)` 的解析器签名。请始终以本技能文档和项目的实际源代码作为权威信息来源。当记忆中的 v1 模式与官方文档冲突时，切勿使用旧模式。

## 何时使用 MSW

MSW 用于在 **网络层模拟 API**——在测试、Storybook 和本地开发环境中拦截 HTTP/GraphQL 请求，而无需修改应用程序代码。

| 需求 | 推荐工具 |
|------|-----------------|
| 测试 API 集成（React、Vue、Node） | **MSW** |
| Storybook 中的 API 模拟 | **MSW**（浏览器工作者） |
| 无后端的本地开发 | **MSW**（浏览器工作者） |
| 单元测试纯函数 | 简单的测试替身（test doubles） |
| E2E 测试真实 API | Playwright/Cypress 的网络拦截 |
| 模拟模块内部逻辑 | `vi.mock()` / `jest.mock()` |

## 快速参考——v2 的核心内容

```typescript
// Imports
import { http, HttpResponse, graphql, delay, bypass, passthrough } from 'msw'
import { setupServer } from 'msw/node'     // tests, SSR
import { setupWorker } from 'msw/browser'  // Storybook, dev

// Handler
http.get('/api/user/:id', async ({ request, params, cookies }) => {
  return HttpResponse.json({ id: params.id, name: 'John' })
})

// Server lifecycle (tests)
beforeAll(() => server.listen({ onUnhandledRequest: 'error' }))
afterEach(() => server.resetHandlers())
afterAll(() => server.close())

// Per-test override
server.use(
  http.get('/api/user/:id', () => new HttpResponse(null, { status: 500 }))
)

// Concurrent test isolation
it.concurrent('name', server.boundary(async () => {
  server.use(/* scoped overrides */)
}))
```

## 规则分类（按优先级）

| 优先级 | 分类 | 影响程度 | 前缀 | 规则 |
|----------|----------|--------|--------|-------|
| 1 | 处理器设计 | 关键 | `handler-` | 4 |
| 2 | 设置与生命周期 | 关键 | `setup-` | 3 |
| 3 | 请求读取 | 高度重要 | `request-` | 2 |
| 4 | 响应构建 | 高度重要 | `response-` | 3 |
| 5 | 测试模式 | 高度重要 | `test-` | 4 |
| 6 | GraphQL | 中等重要 | `graphql-` | 2 |
| 7 | 工具方法 | 中等重要 | `util-` | 2 |

## 所有 20 条规则

### 处理器设计（关键）

| 规则 | 文件 | 说明 |
|------|------|---------|
| 使用 `http` 命名空间 | `handler-use-http-namespace.md` | v2 中移除了 `rest` 命名空间——使用 `http.get()`、`http.post()` |
| URL 中不允许查询参数 | `handler-no-query-params.md` | URL 中的查询参数在解析时不会被匹配到 |
| v2 的解析器签名 | `handler-resolver-v2.md` | 使用 `({ request, params, cookies })`，而不是 `(req, res, ctx)` |
| v2 的响应构建方式 | `handler-response-v2.md` | 使用 `HttpResponse.json()`，而不是 `res(ctx.json())` |

### 设置与生命周期（关键）

| 规则 | 文件 | 说明 |
|------|------|---------|
| 正确的导入路径 | `setup-import-paths.md` | 服务器端使用 `msw/node`，浏览器端使用 `msw/browser` |
| 生命周期钩子 | `setup-lifecycle-hooks.md` | 必须使用 `beforeAll/afterEach/afterAll` 模式 |
| 文件组织结构 | `setup-file-organization.md` | 将相关文件组织在 `src/mocks/` 目录下 |

### 请求读取（高度重要）

| 规则 | 文件 | 说明 |
|------|------|---------|
| 在事件中克隆请求 | `request-clone-events.md` | 在读取请求体之前先克隆请求对象 |
| 异步读取请求体 | `request-body-async.md` | 必须使用 `await request.json()`——请求体读取是异步的 |

### 响应构建（高度重要）

| 规则 | 文件 | 说明 |
| 使用 `HttpResponse` 处理 Cookie | `response-use-httpresponse.md` | 原生响应对象不支持设置 Cookie——使用 `HttpResponse` |
| 处理网络错误 | `response-error-network.md` | 使用 `HttpResponse.error()`，不要在解析器中抛出错误 |
| 流式响应 | `response-streaming.md` | 对于 SSE 或分块响应，使用 `ReadableStream` 处理流数据 |

### 测试模式（高度重要）

| 规则 | 文件 | 说明 |
| 测试行为 | `test-behavior-not-requests.md` | 应该根据 UI 或状态进行断言，而不是请求参数 |
| 测试用例的覆盖设置 | `test-override-with-use.md` | 对于错误或边缘情况测试，使用 `server.use()` |
| 并发测试的隔离 | `test-concurrent-boundary.md` | 使用 `server.boundary()` 对并发测试进行隔离 |
| 未处理的请求 | `test-unhandled-request.md` | 设置 `onUnhandledRequest: 'error'` 以处理未处理的请求 |

### GraphQL（中等重要）

| 规则 | 文件 | 说明 |
| 响应格式 | `graphql-response-shape.md` | 通过 `HttpResponse.json()` 返回 `{ data }` 或 `{ errors }` |
| 端点范围管理 | `graphql-scope-with-link.md` | 使用 `graphql.link(url)` 处理多个 GraphQL API |

### 工具方法（中等重要）

| 规则 | 文件 | 说明 |
| 跳过请求 vs 直接传递 | `util-bypass-vs-passthrough.md` | `bypass()` 表示跳过请求；`passthrough()` 表示直接传递请求 |
| 延迟处理 | `util-delay-behavior.md` | 在 Node.js 中 `delay()` 是立即执行的——需要明确指定延迟时间（单位：ms）

## 响应方法的快速参考

| 方法 | 用途 |
|--------|---------|
| `HttpResponse.json(data, init?)` | 返回 JSON 格式的响应 |
| `HttpResponse.text(str, init?)` | 返回纯文本响应 |
| `HttpResponse.html(str, init?)` | 返回 HTML 内容 |
| `HttpResponse.xml(str, init?)` | 返回 XML 内容 |
| `HttpResponse formData(fd, init?)` | 处理表单数据 |
| `HttpResponse.arrayBuffer(buf, init?)` | 处理二进制数据 |
| `HttpResponse.error()` | 处理网络错误 |

## 从 v1 迁移到 v2 的快速参考

| v1 | v2 |
|----|-----|
| `import { rest } from 'msw'` | `import { http, HttpResponse } from 'msw'` |
| `rest.get(url, resolver)` | `http.get(url, resolver)` |
| `(req, res, ctx) => res(ctx.json(data))` | `() => HttpResponse.json(data)` |
| `req.params` | 从解析器信息中获取参数 `params` |
| `req.body` | 使用 `await request.json()` 读取请求体 |
| `req.cookies` | 从解析器信息中获取 `req.cookies` |
| `res.once(...)` | `http.get(url, resolver, { once: true })` |
| `res.networkError()` | `HttpResponse.error()` | 处理网络错误 |
| `ctx.delay(ms)` | `await delay(ms)` | 延迟处理 |
| `ctx.data({ user })` | `HttpResponse.json({ data: { user } )` | 设置响应数据 |

## 参考资料

| 参考文档 | 覆盖内容 |
|-----------|--------|
| `handler-api.md` | `http.*` 和 `graphql.*` 方法、URL 查询参数、路径参数 |
| `response-api.md` | `HttpResponse` 类及其所有静态方法、Cookie 处理 |
| `server-api.md` | `setupServer`/`setupWorker`、生命周期事件、`boundary()` |
| `test-patterns.md` | Vitest/Jest 的配置、测试用例覆盖、并发测试隔离、缓存清除 |
| `migration-v1-to-v2.md` | 从 v1 迁移到 v2 的详细变更和迁移指南 |
| `anti-patterns.md` | 10 个常见错误及正确/错误的示例说明 |