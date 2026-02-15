---
name: C++
slug: cpp
version: 1.0.1
description: 编写安全的 C++ 代码，避免内存泄漏、悬空指针、未定义行为以及所有权混淆。
metadata: {"clawdbot":{"emoji":"⚡","requires":{"bins":["g++"]},"os":["linux","darwin","win32"]}}
---

## 快速参考

| 主题 | 文件 |
|-------|------|
| RAII、智能指针、new/delete | `memory.md` |
| 原始指针、引用、nullptr | `pointers.md` |
| 3/5/0 规则、继承、虚函数 | `classes.md` |
| 容器、迭代器、算法 | `stl.md` |
| 模板、SFINAE、概念 | `templates.md` |
| 线程、互斥锁、原子操作 | `concurrency.md` |
| C++11/14/17/20、移动语义 | `modern.md` |
| 未定义行为陷阱 | `ub.md` |

## 重要规则

- 不使用 `delete` 的 `new` 会导致内存泄漏——请使用 `std::unique_ptr` 或 `std::make_unique`  
- 将局部变量的引用作为函数返回会导致未定义行为：对象会在返回时被销毁  
- 使用 `==` 比较 C 字符串时实际上是在比较指针——请使用 `std::string` 或 `strcmp()`  
- 有符号整数溢出属于未定义行为（UB）：与无符号整数不同，有符号整数不会自动回绕  
- 基类中必须声明虚析构函数——否则派生类的析构函数可能不会被调用  
- `std::move` 实际上并不会移动对象，而是将其转换为右值类型以支持移动语义  
- 被移动的对象仍然是有效的，但状态可能不确定——请在重新赋值之前谨慎使用  
- 非原子操作可能导致数据竞争（UB）——请使用 `std::mutex` 或 `std::atomic` 来避免  
- `vector<bool>` 并不是一个真正的容器，它返回的是一个代理对象——请使用 `deque<bool>`  
- 当 `map[key]` 中的键不存在时，会插入默认值——请使用 `find()` 或 `contains()` 来检查键是否存在  
- 使用大括号 `{}` 进行初始化可以避免类型转换错误（例如 `int x{3.5}` 会导致错误，而 `int x(3.5)` 会截断小数部分）  
- 在 `push_back` 操作后迭代器可能会失效——因为向量可能会重新分配内存，导致迭代器失效  
- `string_view` 不拥有底层字符串的数据——底层字符串必须比 `string_view` 的生命周期更长