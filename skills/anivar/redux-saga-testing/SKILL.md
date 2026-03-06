---
name: redux-saga-testing
description: 使用 `redux-saga-test-plan`、`runSaga` 以及手动测试工具为 Redux Saga 编写测试用例。测试内容包括：`expectSaga`（集成测试）、`testSaga`（单元测试）、Saga 提供者（provider）的测试、部分匹配器（partial matchers）的验证、 reducer 的集成测试、错误模拟（error simulation）以及 Saga 的取消（cancellation）功能。这些测试工具兼容 Jest 和 Vitest 测试框架。触发测试的条件包括： Saga 相关的测试文件、`redux-saga-test-plan` 的导入语句，以及任何提及“test saga”、“saga test”、“expectSaga”、“testSaga”或“redux-saga-test-plan”的内容。
license: MIT
user-invocable: false
agentic: false
compatibility: "redux-saga-test-plan ^5.x, Jest or Vitest, redux-saga ^1.4.2"
metadata:
  author: Anivar Aravind
  author_url: https://anivar.net
  source_url: https://github.com/anivar/redux-saga-testing
  version: 1.0.0
  tags: redux-saga, testing, redux-saga-test-plan, expectSaga, testSaga, jest, vitest, providers
---
# Redux-Saga 测试指南

**重要提示：** 关于 `redux-saga-test-plan` 的培训资料可能会过时——不同版本的 API 签名、提供者模式和断言方法可能存在差异。请始终以本文档中的参考文件和项目的实际源代码作为权威依据。当记忆中的模式与参考资料冲突时，切勿依赖记忆中的内容。

## 测试方法优先级

1. **`expectSaga`（集成测试）**——推荐使用；这种测试方法不会将测试结果与效果执行顺序绑定在一起。
2. **`testSaga`（单元测试）**——仅当效果执行顺序是测试需求的一部分时使用。
3. **`runSaga`（无依赖库）**——轻量级测试方法；直接使用 Jest/Vitest 的间谍函数（spy）进行测试。
4. **手动调用 `.next()`**——最后的手段；这种方法最容易出错。

## 核心模式

```javascript
import { expectSaga } from 'redux-saga-test-plan'
import * as matchers from 'redux-saga-test-plan/matchers'
import { throwError } from 'redux-saga-test-plan/providers'

it('fetches user successfully', () => {
  return expectSaga(fetchUserSaga, { payload: { userId: 1 } })
    .provide([
      [matchers.call.fn(api.fetchUser), { id: 1, name: 'Alice' }],
    ])
    .put(fetchUserSuccess({ id: 1, name: 'Alice' }))
    .run()
})

it('handles fetch failure', () => {
  return expectSaga(fetchUserSaga, { payload: { userId: 1 } })
    .provide([
      [matchers.call.fn(api.fetchUser), throwError(new Error('500'))],
    ])
    .put(fetchUserFailure('500'))
    .run()
})
```

## 断言方法

| 方法 | 用途 |
|--------|---------|
| `.put(action)` | 派发该动作 |
| `.put_like({ action: { type } })` | 部分匹配动作类型 |
| `.call(fn, ...args)` | 使用指定的参数调用该函数 |
| `.call(fn)` | 调用该函数（参数可任意） |
| `.fork(fn, ...args)` | 分支执行该函数 |
| `.select(selector)` | 使用指定的选择器 |
| `.take(pattern)` | 使用指定的模式 |
| `.dispatch(action)` | 模拟接收到的动作 |
| `.not.put(action)` | 不发送该动作 |
| `.returns(value)` | 获取 Saga 返回的值 |
| `.run()` | 执行 Saga（返回 Promise） |
| `.run({ timeout })` | 带有自定义超时时间的执行 |
| `.silentRun()` | 执行 Saga 时抑制超时警告 |

## 提供者类型

### 静态提供者（推荐使用）

```javascript
.provide([
  [matchers.call.fn(api.fetchUser), mockUser],        // match by function
  [call(api.fetchUser, 1), mockUser],                  // match by function + exact args
  [matchers.select.selector(getToken), 'mock-token'],  // mock selector
  [matchers.call.fn(api.save), throwError(error)],     // simulate error
])
```

### 动态提供者

```javascript
.provide({
  call(effect, next) {
    if (effect.fn === api.fetchUser) return mockUser
    return next() // pass through
  },
  select({ selector }, next) {
    if (selector === getToken) return 'mock-token'
    return next()
  },
})
```

## 测试规则

1. **优先使用 `expectSaga` 而不是 `testSaga`——集成测试不会因代码重构而失效。
2. **使用 `matchers.call(fn())` 进行部分匹配**——除非必要，否则不要严格依赖具体的参数。
3. **在提供者中使用 `throwError()` 进行错误处理**——而不是直接使用 `throw new Error()`。
4. **使用 `.withReducer()` 和 `.hasFinalState()` 与 reducer 一起进行测试，以验证状态变化。
5. **使用 `.dispatch()` 派发动作，以模拟用户操作流程**。
6. **返回 Promise（Jest）或使用 `await`（Vitest）处理异步操作**——不要忽略异步性。
7. **使用 `.not.put()` 来断言动作是否被发送**（用于负向测试）。
8. **通过发送取消动作并验证清理操作来测试 Saga 的取消机制**。
9. **当 Saga 无限期运行时（例如在观察器中），使用 `.silentRun()` 抑制超时警告**。
10. **不要测试 Saga 的实现细节**——只需测试其行为（例如发送了哪些动作、最终状态如何）。

## 避免的错误模式

有关错误模式的详细信息，请参阅 [references/anti-patterns.md]，其中包含以下示例：

- 因动作执行顺序改变而导致测试失败的逐步测试。
- 测试中缺少必要的提供者（例如缺少真实的 API 调用）。
- 仅测试效果的执行顺序而非 Saga 的实际行为。
- 忽视异步操作（Jest/Vitest）。
- 直接使用内联模拟（而非依赖提供者）。
- 不测试错误处理路径。
- 不测试 Saga 的取消和清理机制。

## 参考资料

- [API 参考](references/api-reference.md) — 完整的 `expectSaga`、`testSaga`、提供者及匹配器的相关信息。
- [错误模式](references/anti-patterns.md) — 常见的测试错误及避免方法。