---
name: redux-saga
description: >
  **Redux-Saga最佳实践、模式及API指南：用于构建、测试和调试基于生成器的副作用中间件**  
  本指南介绍了在Redux应用程序中开发此类中间件的相关最佳实践、设计模式及API使用方法。内容涵盖：  
  - 效果创建器（effect creators）  
  - 分支模型（fork model）  
  - 通道（channels）  
  - 使用`redux-saga-test-plan`进行测试  
  - 并发处理（concurrency）  
  - 取消操作（cancellation）  
  - 与现代Redux Toolkit的集成  
  **适用版本：** Redux-Saga 1.4.2  
  **关注关键词：**  
  - saga文件（saga files）  
  - `redux-saga`导入语句（redux-saga imports）  
  - 基于生成器的中间件（generator-based middleware）  
  - `takeEvery`、`takeLatest`等操作符  
  - 分支模型（fork model）  
  - 通道（channels）
license: MIT
user-invocable: false
agentic: false
compatibility: "JavaScript/TypeScript projects using redux-saga ^1.4.2 with Redux Toolkit"
metadata:
  author: Anivar Aravind
  author_url: https://anivar.net
  source_url: https://github.com/anivar/redux-saga-skill
  version: 1.0.0
  tags: redux-saga, redux, redux-toolkit, side-effects, generators, middleware, async, channels, testing
---
# Redux-Saga

**重要提示：** 关于 `redux-saga` 的培训资料可能已经过时或不准确——API 行为、中间件设置模式以及 RTK（Reactive Toolkit）的集成方式都发生了变化。请始终以本技能文档中的规则文件和项目的实际源代码作为权威信息来源。当记忆中的模式与官方文档冲突时，切勿依赖记忆中的内容。

## 何时使用 Redux-Saga

Saga 适用于 **工作流编排**——处理具有并发性、取消机制、竞争条件或长时间运行的后台任务的复杂异步流程。对于较为简单的场景，建议使用以下工具：

| 需求 | 推荐工具 |
|------|-----------------|
| 数据获取 + 缓存 | RTK Query |
| 简单的异步操作（提交 → 状态更新） | `createAsyncThunk` |
| 在 Saga 中实现反应式逻辑 | `createListenerMiddleware` |
| 复杂的工作流、并行任务、取消机制、通道处理 | **Redux-Saga** |

## 规则分类（按优先级排序）

| 优先级 | 分类 | 影响程度 | 前缀 |
|----------|----------|--------|--------|
| 1   | Effects 与 Yielding | 关键性 | `effect-` |
| 2   | Fork 模型与并发处理 | 关键性 | `fork-` |
| 3   | 错误处理 | 高度重要 | `error-` |
| 4   | 规则与模式 | 中等重要 | `recipe-` |
| 5   | 通道与外部 I/O | 中等重要 | `channel-` |
| 6   | RTK 集成 | 中等重要 | `rtk-` |
| 7   | 故障排除 | 低度重要 | `troubleshoot-` |

## 快速参考

### 1. Effects 与 Yielding（关键性）

- `effect-always-yield`：每个 Effect 都必须执行 `yield` 操作；否则会导致应用冻结。
- `effect-use-call`：对于异步函数，应使用 `yield call()`；切勿直接调用函数。
- `effect-take-concurrency`：根据并发需求选择 `takeEvery`/`takeLatest`/`takeLeading`。
- `effect-select-usage`：使用 `select()` 函数进行状态路径的选择；切勿直接访问状态。
- `effect-race-patterns`：使用 `race` 处理超时和取消操作；仅用于阻塞型 Effect。

### 2. Fork 模型与并发处理（关键性）

- `fork-attached-vs-detached`：`fork` 会与父 Saga 共享生命周期和错误；`spawn` 则是独立的。
- `fork-error-handling`：从 `fork` 中产生的错误会传递给父 Saga 的调用者；在 `fork` 点无法捕获错误。
- `fork-no-race`：切勿在 `race` 操作中使用 `fork`；`fork` 是非阻塞的，并且总是会执行完成。
- `fork-nonblocking-login`：在需要保持响应性的登录流程中使用 `fork+take+cancel`。

### 3. 错误处理（高度重要）

- `error-saga-cleanup`：使用 `try/finally` 与 `cancelled()` 来正确处理取消操作后的清理工作。
- `error-root-saga`：在根 Saga 中使用 `spawn` 来隔离错误；对于关键操作，避免使用 `all`。

### 4. 规则与模式（中等重要）

- `recipe-throttle-debounce`：使用 `throttle`、`debounce`、`retry`、指数退避算法实现速率限制和防抖功能。
- `recipe-polling`：使用 `fork+take+cancel` 实现可取消的轮询操作，并处理错误。
- `recipe-optimistic-update`：通过 `race(undo, delay)` 实现乐观的 UI 更新。

### 5. 通道与外部 I/O（中等重要）

- `channel-event-channel`：通过 `eventChannel` 将 WebSocket、DOM 事件和定时器数据传递给 Saga。
- `channel-action-channel`：用于缓冲 Redux 动作，以便顺序处理或由工作线程池执行。

### 6. RTK 集成（中等重要）

- `rtk-configure-store`：将 Saga 中间件与 RTK 的 `configureStore` 集成，同时不破坏默认设置。
- `rtk-with-slices`：使用 `createSlice` 生成的 Action 创建器来实现类型安全的 Saga 触发器。

### 7. 故障排除（低度重要）

- `troubleshoot-frozen-app`：解决应用冻结、动作丢失、堆栈跟踪错误以及 TypeScript 中的 `yield` 类型问题。

## Effect 创建器快速参考

| Effect | 是否阻塞 | 用途 |
|--------|----------|---------|
| `take(pattern)` | 是 | 等待匹配的 Action 发生 |
| `takeMaybe(pattern)` | 是 | 类似 `take`，但会接收 `END` 信号 |
| `takeEvery(pattern, saga)` | 否 | 对每个匹配的 Action 都执行 |
| `takeLatest(pattern, saga)` | 否 | 取消之前的操作，执行最新的 Action |
| `takeLeading(pattern, saga)` | 否 | 在当前 Action 完成前忽略其他操作 |
| `put(action)` | 否 | 发送 Action |
| `putResolve(action)` | 是 | 发送 Action 并等待其返回的结果 |
| `call(fn, ...args)` | 是 | 调用函数并等待结果 |
| `apply(ctx, fn, [args])` | 是 | 在上下文中调用函数 |
| `cps(fn, ...args)` | 是 | 提供 Node 风格的回调函数 |
| `fork(fn, ...args)` | 否 | 创建一个独立的子 Saga |
| `spawn(fn, ...args)` | 否 | 创建一个独立的子任务 |
| `join(task)` | 是 | 等待任务的完成 |
| `cancel(task)` | 否 | 取消任务 |
| `cancel()` | 是 | 自动取消当前操作 |
| `select(selector)` | 是 | 查询状态 |
| `actionChannel(pattern)` | 否 | 缓存 Action |
| `flush(channel)` | 是 | 清空缓冲的消息 |
| `cancelled()` | 是 | 在 `finally` 块中检查取消操作 |
| `delay(ms)` | 是 | 暂停执行 |
| `throttle(ms, pattern, saga)` | 是 | 实现速率限制 |
| `debounce(ms, pattern, saga)` | 是 | 等待一段时间后再执行 |
| `retry(n, delay, fn)` | 是 | 带有退避机制的重试 |
| `race(effects)` | 是 | 找到第一个完成的 Action 后执行 |
| `all([effects])` | 是 | 并发执行所有 Action，等待全部完成 |
| `setContext(props)` / `getContext(prop)` | 否 / 是 | 提供 Saga 的上下文 |

## 模式匹配

`take`、`takeEvery`、`takeLatest`、`takeLeading`、`throttle`、`debounce` 支持以下模式匹配：

| 模式 | 匹配条件 |
|---------|---------|
| `'*'` 或省略 | 匹配所有 Action |
| `'ACTION_TYPE'` | 精确匹配 Action 的类型 |
| `[type1, type2]` | 匹配数组中的任意类型 |
| `fn => boolean` | 自定义匹配条件 |

## 使用方法

详细说明和代码示例请参阅各个规则文件：

```
rules/effect-always-yield.md
rules/fork-attached-vs-detached.md
```

每个规则文件包含：

- 该规则的重要性的简要说明
- 错误的代码示例及原因分析
- 正确的代码示例及说明
- 相关的补充信息和决策表

## 参考资料

| 优先级 | 参考文档 | 阅读时机 |
|----------|-----------|-------------|
| 1 | `references/effects-and-api.md` | 编写或调试 Saga 时参考 |
| 2 | `references/fork-model.md` | 并发处理、错误传播、取消机制相关 |
| 3 | `references/testing.md` | 编写或审查 Saga 测试时参考 |
| 4 | `references/channels.md` | 外部 I/O、数据缓冲、工作线程池相关 |
| 5 | `references/recipes.md` | 速率限制、防抖、重试、撤销、批量处理相关 |
| 6 | `references/anti-patterns.md` | 需避免的常见错误 |
| 7 | `references/troubleshooting.md` | 解决应用冻结、动作丢失、堆栈跟踪错误等问题时参考 |

## 完整文档

如需查看包含所有规则的完整指南，请参阅 `AGENTS.md`。