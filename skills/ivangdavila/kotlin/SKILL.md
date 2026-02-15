---
name: Kotlin
description: 使用 Kotlin 的特性（如协程和空值安全机制），构建健壮的 Android 应用程序以及跨平台应用程序。
metadata: {"clawdbot":{"emoji":"🟠","requires":{"bins":["kotlin"]},"os":["linux","darwin","win32"]}}
---

# Kotlin 开发规范

## 空值安全性（Null Safety）
- 使用 `?.` 进行安全调用：`user?.address?.city` 会在任何参数为 `null` 时返回 `null`。
- 使用 `?:` 来设置默认值：`name ?: "Unknown"` 比使用 `if-else` 更简洁。
- 使用 `!!` 来断言值非 `null`：如果值是 `null`，会抛出异常，仅在使用前进行判断。
- 使用 `let` 进行空值检查：`user?.let { doSomething(it) }` 仅当参数非 `null` 时才会执行代码。

## 协程（Coroutines）
- `suspend` 函数只能在协程中调用，不要阻塞主线程；使用 `withContext(Dispatchers.IO)` 处理 I/O 操作。
- 使用 `launch` 来启动协程并忽略其结果：当需要获取结果时使用 `async/await`。
- `viewModelScope` 会在 `ViewModel` 被清除时自动取消协程；在 Android 中不要使用 `GlobalScope`。
- 使用 `flow` 来处理响应式数据流；使用 `repeatOnLifecycle` 在生命周期敏感的范围内处理数据流。
- 结构化并发：子协程失败会取消父协程；使用 `supervisorScope` 来隔离失败。

## 集合（Collections）
- `listOf` 是不可变的；如果需要修改集合，请使用 `mutableListOf`。
- `map`, `filter`, `reduce` 对于序列（Sequences）是惰性的；对于较长的操作链，请使用 `.asSequence()`。
- `first()` 在集合为空时会抛出异常；使用 `firstOrNull()` 可以安全地获取第一个元素。
- `associate` 和 `groupBy` 可以替代手动构建映射；比使用 `forEach` 和 `mutableMap` 更简洁。
- 解构赋值：`for ((key, value) in map)` 也适用于数据类。

## 数据类（Data Classes）
- `data class` 会自动生成 `equals`, `hashCode`, `copy`, `toString` 方法；无需手动编写。
- `equals` 和 `hashCode` 方法中只包含构造函数中的属性；其他属性会被忽略。
- 使用 `copy()` 方法进行不可变对象的更新：`user.copy(name = "New")` 会保留其他字段的值。
- 对于数据传输对象（DTO）和状态管理，优先使用数据类；但对于具有唯一标识的实体，则不适用。

## 作用域函数（Scope Functions）
- 使用 `let` 进行空值检查和转换：`value?.let { use(it) }`。
- 使用 `apply` 进行对象配置：`MyObject().apply { prop = value }` 会返回配置后的对象。
- 使用 `run` 进行作用域内的计算：`val result = obj.run { compute() }` 会返回计算结果。
- 使用 `also` 处理副作用：`value.also { log(it) }` 会返回原始对象。
- 不要嵌套作用域函数，否则代码可读性会降低；建议将相关功能提取到单独的函数中。

## 扩展函数（Extension Functions）
- 可以在不继承的情况下扩展现有类：`fun String.isEmail(): Boolean`。
- 将扩展函数放在靠近使用它们的地方；避免分散在代码库中。
- 对于可空类型（nullable）的扩展函数：`fun String?.orEmpty()` 可以在 `null` 对象上调用。
- 扩展函数是静态解析的；接收者类型在编译时确定。

## 密封类（Sealed Classes）
- 使用 `when` 来处理所有可能的情况；编译器会确保所有子类都被处理。
- `sealed class` 非常适合状态机和结果类：`sealed class Result<T> { Success, Error }`。
- 子类必须在同一个文件中（或在 Kotlin 1.5 及更高版本中位于同一个包中）；这是有意的设计限制。
- 使用 `sealed interface` 来实现多重继承。

## 常见错误（Common Mistakes）
- 在 Kotlin 中，`==` 表示结构相等；`===` 表示引用相等（与 Java 相反）。
- 字符串模板：使用 `"$var"` 或 `"${expr}"`，无需手动连接字符串。
- `lateinit` 不能用于基本数据类型；使用 `by lazy` 进行延迟初始化。
- `object` 是单例；使用 `companion object` 来定义类似静态成员的代码，而不是创建实例。
- SAM（Single Abstract Method）转换仅适用于 Java 接口；Kotlin 接口需要明确指定 `fun` 关键字。

## 与 Java 的互操作（Interop with Java）
- 使用 `@JvmStatic` 为伴生方法添加静态调用权限；否则需要使用 `Companion.method()`。
- 使用 `@JvmOverloads` 为默认参数生成重载版本；Java 否则无法识别默认参数。
- 使用 `@JvmField` 将属性暴露为 Java 可访问的字段；Java 调用者可以直接访问该字段。
- 空值注解（nullability annotations）可以传递给 Java 代码，以确保 Kotlin 代码的安全性。