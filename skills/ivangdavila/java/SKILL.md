---
name: Java
description: 编写健壮的 Java 代码，避免出现空指针异常（null traps）、相等性判断错误（equality bugs）以及并发问题（concurrency pitfalls）。
metadata: {"clawdbot":{"emoji":"☕","requires":{"bins":["java","javac"]},"os":["linux","darwin","win32"]}}
---

## 字符串使用中的常见陷阱  
- `==` 比较的是对象的引用，而不是字符串的内容——处理字符串时务必使用 `.equals()` 方法。  
- 字符串池：字符串字面量会被缓存（intern），而 `new String()` 创建的字符串则不会被缓存——因此 `"a" == "a"` 的结果是 `true`，但 `new String("a") == "a"` 的结果是 `false`。  
- 字符串是不可变的——在循环中直接连接字符串会生成垃圾对象，应使用 `StringBuilder` 进行操作。  
- `null.equals(x)` 会抛出 `NullPointerException`（NPE）——应使用 `"literal".equals(variable)` 或 `Objects.equals()` 来进行比较。  

## 空值处理  
- `NullPointerException` 是最常见的异常——务必检查变量是否为 `null`，或者使用 `Optional<T>` 来处理空值。  
- `Optional.get()` 在集合为空时会抛出异常——应使用 `orElse()`、`orElseGet()` 或 `ifPresent()` 来处理空值。  
- 不要将 `Optional` 用于字段或参数——它主要用于返回类型。  
- `@Nullable` 和 `@NonNull` 注解有助于静态代码分析，但在运行时不会强制执行。  
- 原始类型不能为 `null`——但其包装类（如 `Integer`）可以，不过自动装箱会掩盖这一特性。  

## 等价性规则  
- 如果重写了 `equals()`，就必须同时重写 `hashCode()`——否则 `HashMap` 和 `HashSet` 无法正确使用该对象。  
- `equals()` 方法必须满足对称性、传递性和一致性——即 `a.equals(b)` 时，`b.equals(a)` 也应返回 `true`。  
- 比较对象是否相等时，应使用 `getClass()` 方法，而不是 `instanceof`——除非明确需要继承关系。  
- `hashCode()` 对于相等的对象必须返回相同的值——否则不同的对象可能会被错误地视为相同。  
- 对于数组，应使用 `Arrays.equals()` 方法来比较内容，而 `array.equals(other)` 则比较引用。  

## 泛型使用中的注意事项  
- 泛型信息在运行时会被擦除——因此无法执行 `new T()` 或 `instanceof List<String>` 等操作。  
- 原始类型不能作为泛型参数或返回类型使用——因为它们不能为 `null`（但它们的包装类可以）。  
- 使用通配符 `List<? extends Animal>` 可以避免类型错误。  
- `<?>` 并不等同于 `<Object>`——`<?>` 可以接受任何类型，而 `<Object>` 只接受 `Object` 类型。  
- Java 不允许创建泛型数组——应使用 `ArrayList<T>` 等容器类。  

## 集合操作中的陷阱  
- 在迭代过程中修改集合会抛出 `ConcurrentModificationException`——应使用 `Iterator.remove()` 或复制集合内容。  
- `Arrays.asList()` 返回的是固定大小的列表——无法添加或删除元素，因为它基于数组实现。  
- `List.of()` 和 `Set.of()` 返回的是不可变的集合——尝试修改这些集合会抛出异常。  
- `HashMap` 允许使用 `null` 作为键或值，而 `Hashtable` 和 `ConcurrentHashMap` 不允许。  
- 对集合进行排序时需要实现 `Comparable` 或提供 `Comparator`——否则会抛出 `ClassCastException`。  

## 自动装箱的潜在风险  
- 对于 `Integer` 类型，`==` 比较的是引用（-128 到 127 之间的值），因此应使用 `.equals()` 方法进行比较。  
- 将 `null` 自动装箱后解箱会抛出 `NullPointerException`。  
- 在循环中频繁进行自动装箱/拆箱操作会生成垃圾对象——应尽量使用原始类型。  
- `Integer.valueOf()` 会缓存一些较小的数值，但 `new Integer()` 从不进行缓存（已被弃用）。  

## 并发编程  
- `volatile` 关键字仅确保变量的可见性，并不保证操作的原子性——因此对 `count++` 这样的操作仍需要同步。  
- 使用 `synchronized` 语句锁定 `this` 对象，而静态方法应使用类级别的同步锁。  
- 如果不使用 `volatile` 关键字，双重检查锁定机制可能失效——应使用 `holder` 模式或枚举来实现单例模式。  
- `ConcurrentHashMap` 在处理复合操作时并不保证原子性——应使用 `computeIfAbsent()` 方法来保证操作的原子性。  
- 不要手动创建线程池——应使用 `ExecutorService` 来管理线程。  

## 异常处理  
- 检查型异常（Checked Exceptions）必须被捕获或声明——未检查型异常（RuntimeException）则不需要捕获。  
- `try-with-resources` 语句可以自动关闭资源——建议从 Java 7 开始使用。  
- 应先捕获特定的异常，再捕获通用的异常；对于无法到达的代码区域，可以使用 `Error` 来捕获异常。  
- `finally` 代码块总是会被执行——即使在 `return` 语句之后，但 `finally` 中的 `return` 语句会覆盖 `try` 块中的 `return` 语句。  

## 继承相关的问题  
- `private` 方法不能被覆盖——子类中不能定义同名但内容不同的方法。  
- `static` 方法会被隐藏，不能被覆盖——它们是根据引用类型调用的，而不是根据对象类型。  
- 构造函数中的第一条语句必须是 `super()`——构造函数中不能有其他逻辑。  
- `final` 方法不能被覆盖；`final` 类也不能被继承。  
- `final` 字段不能参与多态性——它们只能通过引用类型来访问。  

## 内存管理  
- 未释放的监听器或回调函数会导致垃圾回收器（GC）无法正常工作——使用完这些对象后应立即释放引用。  
- 对于缓存数据，可以使用 `WeakReference` 来允许垃圾回收器在内存不足时回收对象。  
- `static` 类型的集合可能会无限增长——应定期清理这些集合，或者使用 `WeakReference` 或 `SoftReference` 来控制内存使用。  
- 内部类会持有对外部类的引用——如果不需要，可以使用静态内部类。  
- `finalize()` 方法已被弃用——应使用 ` Cleaner` 或 `try-with-resources` 来释放资源。  

## 现代 Java 的新特性  
- **Records**（Java 16 及以上版本）：不可变的数据结构，会自动生成 `equals()`、`hashCode()` 和 `toString()` 方法。  
- **Sealed` 类（Java 17 及以上版本）：限制类的继承，通过 `permits` 子类列表来指定允许的子类。  
- **模式匹配**（Java 21 及以上版本）：支持类型模式和条件判断，比传统的 `instanceof` 链式判断更简洁。  
- **虚拟线程**（Java 21 及以上版本）：轻量级的并发模型，可以自由创建线程。  
- **var` 关键字**（Java 10 及以上版本）：用于声明局部变量，类型会自动推断，但仍保持强类型特性。