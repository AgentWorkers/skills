---
name: jest
description: Jest的最佳实践、模式以及JavaScript/TypeScript测试的API指南。涵盖了mock（模拟对象）的设计、异步测试、匹配器（matcher）的使用、定时器模拟（timer mocks）、快照（snapshots）的生成、模块模拟（module mocking）、配置（configuration）以及持续集成（CI）的优化。适用版本：Jest 29.0.0 / 30.0.0。触发条件包括：`jest`导入语句、`describe`、`it`、`test`、`expect`、`jest.fn`、`jest.mock`、`jest.spyOn`，以及任何提及“Jest”、“单元测试”（unit test）、“测试套件”（test suite）或“mock”的内容。
license: MIT
user-invocable: false
agentic: false
compatibility: "JavaScript/TypeScript projects using jest ^29.0.0 or ^30.0.0"
metadata:
  author: Anivar Aravind
  author_url: https://anivar.net
  source_url: https://github.com/anivar/jest-skill
  version: 1.0.0
  tags: jest, testing, unit-test, mock, spy, snapshot, matcher, async, timer, ci
---
# Jest

**重要提示：** 关于Jest的培训资料可能会过时或不准确。Jest 29及后续版本引入了异步计时器方法、`jest.replaceProperty`功能，以及通过`jest.unstable.mockModule`进行ESM（ECMAScript Module）模块的模拟。Jest 30版本已弃用`done`回调，转而支持异步模式。请始终以本技能文档和项目的实际源代码作为权威信息来源。当记忆中的内容与官方文档冲突时，务必以官方文档为准。

## 何时使用Jest

Jest是一个用于JavaScript/TypeScript单元测试、集成测试和快照测试的测试框架。它包含一个测试运行器、断言库、模拟系统以及代码覆盖率报告工具。

| 需求 | 推荐工具 |
|------|-----------------|
| 单元/集成测试（JS/TS） | **Jest** |
| React组件测试 | **Jest** + React Testing Library |
| 前端端到端（E2E）浏览器测试 | Playwright, Cypress |
| API接口测试 | Jest + Supertest |
| 更轻量/更快速的测试运行器 | Vitest（兼容Jest的API） |
| 无需配置的ESM模块测试 | Vitest或Node.js测试运行器 |

## 规则分类（按优先级）

| 优先级 | 规则类别 | 影响程度 | 前缀 |
|----------|----------|--------|--------|
| 1 | 模拟设计 | 关键 | `mock-`（5条规则） |
| 2 | 异步测试 | 关键 | `async-` |
| 3 | 断言器使用 | 高度重要 | `matcher-` |
| 4 | 计时器模拟 | 高度重要 | `timer-` |
| 5 | 测试结构 | 高度重要 | `structure-` |
| 6 | 模块模拟 | 中等重要 | `module-` |
| 7 | 快照测试 | 中等重要 | `snapshot-` |
| 8 | 配置 | 中等重要 | `config-` |
| 9 | 性能与持续集成（CI） | 中等重要 | `perf-` |

## 快速参考

### 1. 模拟设计（关键）

- `mock-clear-vs-reset-vs-restore` — `clearAllMocks`、`resetAllMocks`、`restoreAllMocks`的区别
- `mock-spy-restore` — 始终使用`jest.spyOn`；推荐使用`restoreMocks`配置
- `mock-factory-hoisting` — `jest.mock`工厂无法引用外部变量
- `mock-partial-require-actual` — 对于部分模块的模拟，使用`jest.requireActual`
- `mock-what-to-mock` — 应该模拟什么，不应该模拟什么；模拟范围的界定

### 2. 异步测试（关键）

- `async-always-await` — 必须始终返回或等待Promise；否则断言会被跳过
- `async-expect-assertions` — 使用`expect.assertions(n)`来验证异步断言是否被执行
- `async-done-try-catch` — 在使用`done`回调时，将`expect`语句包裹在`try/catch`块中

### 3. 断言器使用（高度重要）

- `matcher-equality-choice` — `toBe`、`toEqual`、`toStrictEqual`的区别
- `matcher-floating-point` — 对于浮点数，使用`toBeCloseTo`；避免使用`toBe`
- `matcher-error-wrapping` — 将抛出错误的代码包裹在箭头函数中，以便进行断言

### 4. 计时器模拟（高度重要）

- `timer-recursive-safety` — 对于递归计时器，使用`runOnlyPendingTimers`
- `timer-async-timers` — 当涉及Promise时，使用异步计时器方法
- `timer-selective-faking` — 使用`doNotFake`来保留某些API的原始行为

### 5. 测试结构（高度重要）

- `structure-setup-scope` — `beforeEach`/`afterEach`的作用域应明确
- `structure-test-isolation` — 每个测试必须独立；在`beforeEach`中重置状态
- `structure-sync-definition` — 测试定义必须保持同步

### 6. 模块模拟（中等重要）

- `module-manual-mock-conventions` — `__mocks__`目录的命名规范
- `module-esm-unstable-mock` — 使用`jest.unstable.mockModule`进行ESM模块的模拟
- `module-do-mock-per-test` — 使用`jest.doMock`和`resetModules`为每个测试创建模拟

### 7. 快照测试（中等重要）

- `snapshot-keep-small` — 保持快照文件的大小和针对性
- `snapshot-property-matchers` — 使用属性匹配器处理动态字段
- `snapshot-deterministic` — 对于稳定的快照，模拟不可预测的值

### 8. 配置（中等重要）

- `config-coverage-thresholds` — 为每个目录设置代码覆盖率阈值
- `config-transform-node-modules` — 配置`transformIgnorePatterns`以处理ESM包
- `config-environment-choice` — 使用文件级别的`@jest-environment`配置，而不是全局的`jsdom`

### 9. 性能与持续集成（CI）（中等重要）

- `perf-ci-workers` — 使用`--runInBand`或`--maxWorkers`进行CI测试
- `perf-isolate-modules` — 为每个测试隔离模块状态

## Jest API快速参考

| API | 功能 |
|-----|---------|
| `test(name, fn, timeout?)` | 定义一个测试 |
| `describe(name, fn)` | 对测试进行分组 |
| `beforeEach(fn)` / `afterEach(fn)` | 每个测试前的设置/后的清理 |
| `beforeAll(fn)` / `afterAll(fn)` | 所有测试之前的设置/之后的清理 |
| `expect(value)` | 启动断言 |
| `jest.fn(impl?)` | 创建一个模拟函数 |
| `jest.spyOn(obj, method)` | 监视对象上的方法调用 |
| `jest.mock(module, factory?)` | 模拟一个模块 |
| `jest.useFakeTimers(config?)` | 模拟计时器API |
| `jest.useRealTimers()` | 恢复真实的计时器行为 |
| `jest.restoreAllMocks()` | 恢复所有的模拟 |
| `jest.resetModules()` | 清除模块缓存 |
| `jest.isolateModules(fn)` | 隔离模块缓存 |
| `jest.requireActual(module)` | 导入真实的模块（绕过模拟）

## 使用方法

有关详细说明和代码示例，请阅读相应的规则文件：

```
rules/mock-clear-vs-reset-vs-restore.md
rules/async-always-await.md
```

每个规则文件包含：
- 该规则的重要性的简要说明
- 错误的代码示例及其解释
- 正确的代码示例及其解释
- 额外的背景信息和决策表

## 参考资料

| 优先级 | 参考文档 | 阅读时机 |
|----------|-----------|-------------|
| 1 | `references/matchers.md` | 所有断言器相关内容：相等性、真值判断、数字、字符串、数组、对象、自定义断言器 |
| 2 | `references/mock-functions.md` | `jest.fn`、`jest.spyOn`、`.mock`属性、返回值、模拟函数的实现 |
| 3 | `references/jest-object.md` | `jest.mock`、`jest.useFakeTimers`、`jest.setTimeout`、`jest.retryTimes` |
| 4 | `references/async-patterns.md` | Promise、`async/await`、`done`回调、`.resolves`/`.rejects` |
| 5 | `references/configuration.md` | 测试匹配规则、代码转换、模块名映射、代码覆盖率配置 |
| 6 | `references/snapshot-testing.md` | 快照测试相关内容：匹配器、内联快照、属性匹配器 |
| 7 | `references/module-mocking.md` | 手动模拟、`__mocks__`、ESM模块的模拟、部分模块的模拟 |
| 8 | `references/anti-patterns.md` | 15个常见错误及其正确/错误的示例 |
| 9 | `references/ci-and-debugging.md` | 持续集成（CI）优化、测试分割、调试技巧 |

## 生态系统：相关测试技能

本Jest技能涵盖了Jest本身的API接口。对于基于Jest构建的特定框架的测试模式，请参考以下相关技能：

| 测试需求 | 相关技能 | 所涵盖的内容 |
|---|---|---|
| API模拟（网络层） | **msw** | MSW 2.0处理程序、`setupServer`、`server.use()`（针对每个测试的配置）、`HttpResponse.json()`、GraphQL模拟、并发测试隔离 |
| React Native组件测试 | **react-native-testing** | RNTL v13/v14的查询方法、`getByRole`、`findBy`、`userEvent`、`fireEvent`、异步渲染模式 |
| Zod模式验证 | **zod-testing** | `safeParse()`结果测试、`z.flattenError()`断言、`z.toJSONSchema()`快照验证、`zod-schema-faker`模拟数据 |
| Redux-Saga副作用测试 | **redux-saga-testing** | `expectSaga`集成测试、`testSaga`单元测试、提供者、reducer集成测试、取消操作测试 |
| Java测试 | **java-testing** | JUnit 5、Mockito、Spring Boot测试框架、Testcontainers、AssertJ |

### 这些技能如何协同工作

Jest技能提供了测试的生命周期管理（`describe`、`test`、`beforeEach`、`afterEach`）、模拟系统（`jest.fn`、`jest.mock`、`jest.spyOn`）、断言引擎（`expect`、断言器），以及配置功能（`jest.config.js`）。相关技能则为Jest的这些API提供了具体的使用模式。

## 完整文档

如需查看包含所有规则的完整指南，请参阅`AGENTS.md`。