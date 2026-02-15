---
name: C#
description: 避免常见的 C# 错误：空指针异常（null traps）、异步编程中的陷阱（async pitfalls）、LINQ 使用中的误区（LINQ gotchas），以及资源释放问题（disposal leaks）。
metadata: {"clawdbot":{"emoji":"🟣","requires":{"bins":["dotnet"]},"os":["linux","darwin","win32"]}}
---

## 空值处理  
- 启用可为空的引用类型 `<Nullable>enable` — 在编译时捕获空值问题  
- `?.`：如果左侧值为 `null`，则返回 `null` — 可安全地链式调用：`obj?.Property?.Method()`  
- `??`：用于获取默认值：`value ?? fallback` — `??=` 用于在值为 `null` 时进行赋值  
- `!`：忽略空值 — 优先使用正确的空值检查或模式  

## 异步编程的陷阱  
- `async void` 仅适用于事件处理程序 — 无法使用 `await`，异常会导致应用程序崩溃  
- 对于 CPU 密集型操作，使用 `await Task.Run()` — 不要包装已经异步的 I/O 方法  
- 在库中设置 `ConfigureAwait(false)` — 可避免死锁，但在应用程序代码中通常不需要  
- 在 UI/ASP.NET 中，使用 `.Result` 或 `.Wait()` 会导致死锁 — 应始终使用 `await`  
- 返回类型应为 `Task` 而不是 `void` — 否则调用者无法使用 `await`  

## LINQ 的常见错误  
- `IEnumerable` 是惰性的 — 多次遍历会重新执行查询  
- 使用 `.ToList()` 或 `.ToArray()` 可将集合转换为数组 — 如果需要多次遍历，请使用这些方法  
- 对 `IEnumerable` 使用 `.Count()` 会遍历所有元素 — 使用 `.Any()` 来检查是否存在元素  
- `FirstOrDefault()` 可返回 `null` 或默认值 — 使用前请先进行检查；如果可以保证元素存在，可使用 `First()`  
- LINQ to SQL 会在遍历时执行数据库操作 — 使用 `.ToList()` 会触发数据库调用  

## 等价性判断  
- 对于引用类型，使用 `==` 检查引用关系 — 对于值类型，需要重写 `Equals()` 方法  
- `string` 使用 `==` 进行值比较 — 这是一个特殊情况，行为是正确的  
- 记录（Record）默认使用值相等性进行比较 — 对于数据传输对象（DTO），建议使用记录类型  
- 为字典键重写 `GetHashCode()` 和 `Equals()` 方法  

## 值类型与引用类型的区别  
- 结构体（struct）在赋值时会被复制 — 修改副本不会影响原对象  
- 可变的结构体很危险 — 建议使用只读的结构体或类  
- 将结构体装箱（boxing）为接口会浪费性能  
- `ref` 和 `out` 参数按引用传递 — `in` 参数用于只读的引用类型（不会复制也不会修改原对象）  

## 资源释放  
- `using` 语句会自动释放资源 — 在现代 C# 中可以使用 `using var x = new Resource();`  
- 如果需要异步清理资源，应实现 `IAsyncDisposable` 并使用 `await using`  
- 最终析构函数（Finalizer）会消耗较多资源 — 仅在管理非托管资源时实现  
- 事件处理程序会阻止垃圾回收器（GC）回收资源 — 为避免资源泄漏，请取消订阅：`-=`  

## 集合操作  
- 在 `foreach` 循环中修改集合元素会抛出异常 — 可将集合复制到列表中，或使用带索引的循环  
- `Dictionary` 在查找不存在的键时会抛出异常 — 使用 `TryGetValue()` 或 `GetValueOrDefault()`  
- `List<T>` 不是线程安全的 — 如果集合大小可能变化，请使用 `ConcurrentBag<T>` 或加锁  
- 数组的大小是固定的 — 如果数组大小可能变化，请使用 `List<T>`  

## 字符串操作中的注意事项  
- 字符串是不可变的 — 在循环中拼接字符串会创建不必要的垃圾对象  
- 对于多次字符串拼接，使用 `StringBuilder`；对于少量拼接，可以使用 `string.Join()` 或字符串插值  
- `string.IsNullOrEmpty()` 与 `IsNullOrWhiteSpace()` 的区别：`IsNullOrWhiteSpace()` 会检查字符串是否包含空格  
- 为了提高性能，使用 `StringComparisonOrdinal` 进行比较；`OrdinalIgnoreCase` 可忽略大小写  

## 模式匹配  
- `is` 模式：`if (obj is string s)` — 一次完成声明和赋值  
- `switch` 表达式：`x switch { 1 => "one", _ => "other" }` — 可以全面覆盖所有情况  
- 属性模式：`obj is { Name: "test" }` — 简洁且安全的空值检查方式  
- `not`、`and`、`or` 模式：可以组合使用，例如 `is not null and { Length: > 0 }`