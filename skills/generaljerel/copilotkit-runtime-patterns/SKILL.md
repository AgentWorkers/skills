---
name: copilotkit-runtime-patterns
description: CopilotKit的服务器端运行时模式：适用于配置CopilotKit的运行时端点（如Express、Hono、Next.js）、远程代理端点、添加中间件以及保护运行时的安全。这些模式会在涉及`@copilotkit/runtime`、`CopilotRuntime`、代理注册或API端点配置的后端任务中被触发。
license: MIT
metadata:
  author: copilotkit
  version: "2.0.0"
---
# CopilotKit 运行时配置模式

本文档介绍了服务器端的运行时配置模式，共包含 15 条规则，分为 5 个类别。

## 适用场景

在以下情况下请参考这些指南：
- 设置 CopilotKit 的运行时端点（Express、Hono、Next.js API 路由）
- 使用服务适配器（如 OpenAIAdapter）配置 CopilotRuntime
- 通过远程端点注册代理（LangGraph、CrewAI）
- 添加用于日志记录、身份验证或请求修改的中间件
- 保护运行时的安全性（CORS、身份验证、速率限制）
- 优化运行时性能

## 规则分类及优先级

| 优先级 | 分类 | 影响程度 | 前缀 |
|---------|---------|-----------|---------|
| 1      | 端点配置 | 关键（CRITICAL） | `endpoint-` |
| 2      | 代理配置 | 高（HIGH）    | `runner-`   |
| 3      | 中间件     | 中等（MEDIUM）  | `middleware-`  |
| 4      | 安全性    | 高（HIGH）    | `security-`  |
| 5      | 性能     | 中等（MEDIUM）  | `perf-`    |

## 快速参考

### 1. 端点配置（关键）

- `endpoint-express-setup`：配置使用 CopilotRuntime 的 Express 端点及 CORS
- `endpoint-hono-setup`：配置用于边缘运行的 Hono 端点
- `endpoint-nextjs-route`：使用 `copilotRuntimeNextJSAppRouterEndpoint` 设置 Next.js API 路由

### 2. 代理配置（高）

- `runner-inmemory-vs-sqlite`：为生产环境中的线程管理选择持久化存储方式
- `runner-agent-registration`：通过远程端点注册代理
- `runner-multiple-agents`：配置多代理环境的路由规则

### 3. 中间件

- `middleware-before-request`：在请求处理前执行中间件，用于身份验证、日志记录等
- `middleware-after-request`：在请求处理后执行中间件，用于日志记录和资源清理
- `middleware-error-handling`：在中间件中处理错误，避免影响运行时进程

### 4. 安全性（高）

- `security-cors-config`：为特定前端来源配置 CORS
- `security-auth-middleware`：在代理执行前验证请求
- `security-rate-limiting`：根据用户或 API 密钥实施速率限制

### 5. 性能（中等）

- `perf-streaming-response`：确保响应流不被代理服务器缓存

## 完整文档

如需查看包含所有详细规则的完整指南，请参阅 `AGENTS.md`。