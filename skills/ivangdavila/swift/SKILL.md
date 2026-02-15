---
name: Swift
slug: swift
version: 1.0.1
description: 编写安全的 Swift 代码，避免内存泄漏、可选陷阱（optional traps）以及并发错误。
metadata: {"clawdbot":{"emoji":"🦅","requires":{"bins":["swift"]},"os":["darwin","linux"]}}
---

## 快速参考

| 主题        | 文件        |
|------------|------------|
| 可选参数、nil 安全性、强制解包 | `optionals.md`   |
| 保留循环引用、弱引用、闭包    | `memory.md`   |
| 异步/await、Actor、Sendable 类型 | `concurrency.md`  |
| JSON 编码/解码问题    | `codable.md`   |
| 协议、集合、字符串、错误处理、构建    | `types.md`   |
| SwiftUI 状态（@State、@Binding、Combine）| `swiftui.md`   |
| 属性包装器、Actor、结果构建器、宏    | `advanced.md`   |
| XCTest 测试技巧、SPM 使用注意事项 | `testing.md`   |

## 重要规则

### 内存与安全性
- 强制解包（`!`）操作在 `nil` 上会引发崩溃——请使用 `guard let` 或 `if let` 代替。
- 闭包中捕获 `self` 会导致循环引用——在需要逃逸的闭包中使用 `[weak self]`。
- 代理（delegate）必须是弱引用（`weak`）——否则对象将永远不会被释放。
- `try!` 操作在遇到任何错误时都会引发崩溃——切勿在生产代码中使用。
- `removeFirst()` 在集合为空时会导致崩溃——为安全起见，请使用 `popFirst()`。

### 并发
- `async let` 会立即执行——而不是在 `await` 之后执行。
- 每次调用 `await` 时，Actor 都会重新进入执行状态——状态可能在暂停点之间发生变化。
- `@MainActor` 并不保证会立即在主线程上执行——它会被放入队列中执行。
- 违反 `Sendable` 协议规范会导致运行时崩溃——编译器警告会被视为错误。

### 类型与集合
- 协议扩展不会覆盖原有类型的方法——静态调用会忽略子类的实现。
- 在集合中修改结构体成员需要重新赋值——`array[0].mutate()` 是无效的。
- 一个字符串中的 `String.Index` 在另一个字符串中可能无效——即使内容相同也是如此。

### SwiftUI
- `@StateObject` 拥有数据，`@ObservedObject` 只是读取数据——重新创建视图会丢失 `ObservedObject` 的状态。
- 如果未注入 `@EnvironmentObject`，使用它会导致程序崩溃——编译时没有进行检查。
- 视图的标识符发生变化会重置所有 `@State` 的状态——更改标识符会导致状态丢失。

### 构建
- `print()` 无论在开发模式还是发布模式下都会生成字符串输出——请移除该函数或使用 `os_log` 替代。
- 泛型代码会导致二进制文件体积增大——应为每种类型编写专门的代码。