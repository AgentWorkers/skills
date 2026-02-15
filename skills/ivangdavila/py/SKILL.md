---
name: Python
slug: python
version: 1.0.1
description: 编写可靠的 Python 代码时，应避免使用可变的默认值、导入陷阱（import errors）以及常见的运行时问题。
metadata: {"clawdbot":{"emoji":"🐍","requires":{"bins":["python3"]},"os":["linux","darwin","win32"]}}
---

## 快速参考

| 主题 | 文件 |
|-------|------|
| 动态类型、类型提示、鸭子类型（Duck Typing） | `types.md` |
| 列表/字典/集合的使用技巧及注意事项、列表推导式 | `collections.md` |
| 参数（args/kwargs）、闭包、装饰器、生成器（Closures, Decorators, Generators） | `functions.md` |
| 继承、描述符、元类（Inheritance, Descriptors, Metaclasses） | `classes.md` |
| 全局解释器锁（GIL）、多线程、异步IO（Asynchronous I/O, asyncio）、多进程（Concurrency） | `concurrency.md` |
| 循环导入（Circular Imports）、包（Packages）、`__init__.py`文件 | `imports.md` |
| Pytest测试框架、模拟（Mocking）、测试 fixture | `testing.md` |

## 重要规则

- 函数`def f(items=[])`会在所有调用中共享列表中的元素——应使用`items=None`，然后通过`items = items or []`来处理空列表的情况。
- `is`用于检查对象的身份，`==`用于检查对象是否相等——“a” * 100和“a” * 100的结果可能不同（即`False`）。
- 在迭代列表时修改列表会导致元素丢失——应使用列表的副本进行迭代：`for x in list(items):`。
- 全局解释器锁（GIL）限制了Python的多线程并行执行能力——对于CPU密集型任务，请使用多进程（multiprocessing）。
- 单纯的`except:`语句会捕获`SystemExit`和`KeyboardInterrupt`异常——应使用`except Exception:`来捕获所有异常。
- 当尝试为外部作用域的变量赋值时可能会引发`UnboundLocalError`错误——此时应使用`nonlocal`或`global`关键字。
- 不使用上下文管理器的`open()`函数会导致文件句柄泄漏——务必使用`with open():`来打开文件。
- 循环导入可能导致程序无声失败或部分失败——应在函数内部进行导入以打破循环。
- `0.1 + 0.2`的结果不等于`0.3`——这是浮点数的特性，处理货币计算时应使用`decimal.Decimal`。
- 生成器在仅执行一次迭代后会被耗尽——无法重新使用，可以使用`itertools.tee`来创建多个生成器实例。
- 如果类属性包含可变对象，这些属性会在所有实例之间共享——应将这些属性定义在`__init__`方法中。
- `__init__`方法并非构造函数（Constructor）——`__new__`方法负责创建实例，`__init__`方法负责初始化实例。
- Python的默认编码方式依赖于操作系统——始终指定`encoding='utf-8'`。