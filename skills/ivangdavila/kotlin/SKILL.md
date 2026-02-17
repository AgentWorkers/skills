---
name: Kotlin
slug: kotlin
version: 1.0.1
description: 使用 Kotlin 的特性（如协程和空值安全机制），构建健壮的 Android 应用程序以及跨平台应用。
metadata: {"clawdbot":{"emoji":"🟠","requires":{"bins":["kotlin"]},"os":["linux","darwin","win32"]}}
---
## 快速参考

| 主题 | 文件 |
|-------|------|
| 空值安全操作符和模式 | `nullsafety.md` |
| 协程、流程、结构化并发 | `coroutines.md` |
| 集合、序列、数据类 | `collections.md` |
| 作用域函数、扩展、密封类 | `idioms.md` |
| Java 互操作性与常见的 Kotlin 错误 | `interop.md` |
| Android 生命周期、Compose 状态管理 | `android.md` |
| 委托模式、内联代码、多平台支持 | `advanced.md` |

## 重要规则

### 空值安全
- `!!` 用于断言变量非空；如果变量为 `null`，程序会崩溃。请仅在已经进行过空值检查后使用该操作符。
- 来自 Java 的平台类型可能存在风险，请添加空值检查或使用 `@Nullable`/`@NonNull` 注解。
- 使用 `return`/`throw` 与 `Elvis` 语法实现提前退出：`val name = user?.name ?: return`

### 协程
- 当 `ViewModel` 被清除时，`viewModelScope` 会自动取消协程的执行。在 Android 中请避免使用 `GlobalScope`。
- 结构化并发中，子协程的失败会触发父协程的取消。请使用 `supervisorScope` 来隔离不同协程的执行。
- `StateFlow` 需要一个初始值，并且永远不会完成执行；对于一次性事件，请使用 `SharedFlow`。
- 为了便于测试，请为协程注入相应的调度器（dispatcher），不要硬编码 `Dispatchers.IO`。

### 集合与数据类
- `first()` 方法在集合为空时会抛出异常；请使用 `firstOrNull()` 来安全地获取第一个元素。
- 在 `equals`/`hashCode` 方法中，只有构造函数中声明的属性才会被考虑；其他属性会被忽略。
- 对于 Compose 环境，建议使用 `mutableStateListOf`；直接使用 `mutableListOf` 无法跟踪状态的变化。

### 作用域函数与扩展
- 不要嵌套作用域函数，否则代码的可读性会大大降低；请将嵌套的功能提取为独立的函数。
- 扩展函数在编译时会被静态解析，不具备多态性；因此接收器的类型在编译时就已经确定了。

### Android/Compose
- 使用 `repeatOnLifecycle(STARTED)` 来处理与生命周期相关的操作；`launchWhenStarted` 已被弃用。
- `remember` 方法仅在组件重新组合时保留数据；对于配置变更，建议使用 `rememberSaveable`。
- `collectAsStateWithLifecycle` 是处理生命周期相关操作的最佳方式，它结合了 Compose 的状态管理机制。

### Java 互操作性
- 在 Kotlin 中，`==` 表示结构相等；`===` 表示引用相等，这与 Java 的规则相反。
- 只有 Java 接口才能进行 SAM（Single Abstract Method）转换；Kotlin 接口需要明确指定 `fun interface`。
- 使用 `@JvmStatic`、`@JvmOverloads`、`@JvmField` 等注解来适配 Java 的 API。