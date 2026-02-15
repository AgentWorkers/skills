---
name: C#
slug: csharp
version: 1.0.1
description: 编写健壮的 C# 代码时，需要避免以下常见问题：空指针异常（null traps）、异步死锁（async deadlocks）以及 LINQ 使用中的陷阱（LINQ pitfalls）。
metadata: {"clawdbot":{"emoji":"💜","requires":{"bins":["dotnet"]},"os":["linux","darwin","win32"]}}
---

## 快速参考

| 主题 | 文件 |
|-------|------|
| `null` 引用、可空类型 | `nulls.md` |
| 异步/`await`、死锁 | `async.md` |
| 延迟执行、闭包 | `linq.md` |
| 值类型与引用类型、装箱与拆箱 | `types.md` |
| 迭代、相等性判断 | `collections.md` |
`IDisposable`、使用方式及终结器 | `dispose.md` |

## 重要规则

- `?.` 和 `??` 可防止运行时异常（NRE），但 `!` 只能覆盖警告，如果变量仍为 `null`，程序仍会崩溃。
- 在 UI 线程上使用 `.Result` 或 `.Wait()` 会导致死锁，应使用 `await` 或 `ConfigureAwait(false)`。
- LINQ 是惰性计算的：`query.Where(...)` 仅在遍历时才会执行。
- 对 `IEnumerable` 进行多次遍历时，可能会重新查询数据库，建议先调用 `.ToList()`。
- 闭包捕获的是变量的引用，而非变量的值；Lambda 表达式中的循环变量会捕获最后一个值。
- 在异步方法中使用结构体时，结构体会被复制，因此在 `await` 后对结构体的修改会丢失。
- 字符串比较时，代码中应使用 `StringComparisonOrdinal`，UI 中使用 `CurrentCulture`。
- `GetHashCode()` 方法必须保持稳定，否则可变字段会导致字典查找失败。
- 在遍历集合时修改集合会导致异常，建议使用 `.ToList()` 来获取集合的副本进行遍历。
- 表示货币时应使用 `decimal` 类型，`float`/`double` 类型会导致精度损失。
- `readonly` 结构体可以防止不必要的复制操作，从而提高性能。
- `sealed` 关键字可以防止继承，有助于实现虚拟方法调用的优化。