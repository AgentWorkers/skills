---
name: Java
slug: java
version: 1.0.1
description: 编写健壮的 Java 代码，避免空指针异常（null traps）、相等性判断错误（equality bugs）以及并发问题（concurrency pitfalls）。
metadata: {"clawdbot":{"emoji":"☕","requires":{"bins":["java","javac"]},"os":["linux","darwin","win32"]}}
---

## 快速参考

| 主题 | 文件 |
|-------|------|
| `null` 值、可选参数、自动装箱 | `nulls.md` |
| 集合与迭代相关的问题 | `collections.md` |
| 泛型与类型擦除 | `generics.md` |
| 并发与同步 | `concurrency.md` |
| 类、继承、内存管理 | `classes.md` |
| 流（Streams）与 `CompletableFuture` | `streams.md` |
| 测试（JUnit、Mockito） | `testing.md` |
| JVM、垃圾回收（GC）、模块系统 | `jvm.md` |

## 重要规则

- `==` 操作符比较的是对象的引用，而非对象的内容——对于字符串，必须使用 `.equals()` 方法进行比较。
- 如果重写了 `equals()` 方法，也必须重写 `hashCode()` 方法，否则 `HashMap` 和 `HashSet` 无法正确工作。
- `Optional.get()` 方法在集合为空时会抛出异常——应使用 `orElse()`、`orElseGet()` 或 `ifPresent()` 来处理这种情况。
- 在迭代过程中修改集合元素会抛出 `ConcurrentModificationException` 异常——应使用 `Iterator.remove()` 方法来安全地删除元素。
- 类型擦除会导致泛型信息在运行时丢失——此时无法使用 `new T()` 或 `instanceof List<String>` 等操作。
- `volatile` 关键字仅用于保证变量的可见性，而非原子性——因此对 `volatile` 变量的操作仍需要同步。
- 将 `null` 值解箱（unboxing）后赋值给非 `null` 变量可能会抛出 `NullPointerException`（NPE）。
- 对于 `Integer` 类型，当数值不在 -128 到 127 的范围内时，`==` 操作符比较的是对象的引用——应使用 `.equals()` 方法进行比较。
- `try-with-resources` 语句可以自动关闭资源——如果资源需要手动关闭，应实现 `AutoCloseable` 接口（Java 7 及更高版本支持）。
- 内部类会持有对外部类的引用——如果不需要，应使用静态内部类。
- 流是一次性使用的资源——在完成操作后不能重复使用。
- `thenApply` 与 `thenCompose` 的区别：`thenCompose` 用于链式调用 `CompletableFutures`。
- `Record` 类是隐式final的——不能被继承，其成员变量也是 final 的。
- 如果 `serialVersionUID` 不匹配，会导致反序列化失败——必须显式声明 `serialVersionUID`。