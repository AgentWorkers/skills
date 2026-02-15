---
name: Ruby
description: 使用代码块、元编程以及惯用的编程模式来编写富有表现力的 Ruby 代码。
metadata: {"clawdbot":{"emoji":"💎","requires":{"bins":["ruby"]},"os":["linux","darwin","win32"]}}
---

# Ruby 开发规范

## 块（Blocks）和过程（Procedures）
- 使用 `do...end` 表示多行代码块，使用 `{}` 表示单行代码块——这是惯例，两种方式都可行。
- `yield` 用于调用一个块；`block_given?` 方法用于检查是否传递了块。
- `&block` 可以将一个块捕获为一个 `Proc` 对象——可以存储、传递或稍后调用。
- Lambda 表达式会检查参数的数量，而 `Proc` 则不会；Lambda 从自身返回结果，而 `Proc` 从包含它的方法返回结果。
- `->` 是 Lambda 表达式的简写语法，例如：`add = ->(a, b) { a + b }`。

## 方法（Methods）
- 方法的最后一个表达式默认会返回结果——除非需要提前退出，否则不需要使用 `return`。
- 布尔值方法通常以 `?` 作为后缀，例如 `empty?`、`valid?`——但这并非强制要求。
- 危险的方法通常以 `!` 作为后缀，因为它们可能会修改原始数据或抛出异常，而不是返回 `nil`。
- 括号是可选的——对于 DSL（Domain-Specific Languages）或没有参数的方法可以省略括号；如果有参数，则使用括号以提高代码的可读性。
- `*args` 用于接收可变数量的参数，`**kwargs` 用于接收关键字参数。

## 真值性（Truthiness）
- 只有 `nil` 和 `false` 被视为假值；`0`、`""`、`[]` 被视为真值。
- `||=` 可用于缓存结果（称为“记忆化”）——例如：`@user ||= fetch_user` 会在第一次调用时缓存结果。
- `&&` 和 `||` 返回实际的值，而不仅仅是布尔值，这在处理默认值时非常有用。
- `nil?` 专门用于检查 `nil`；`blank?` 是 Rails 中的一个方法，用于检查 `nil`、空字符串或空白字符串。

## 符号（Symbols）与字符串（Strings）
- 符号是不可变的，并且在内存中是“interned”的（即符号在内存中只有一个副本）——因此 `:name` 在任何地方都表示同一个对象。
- 使用符号作为键或标识符；使用字符串表示文本内容。
- 在哈希中，可以使用符号作为键，例如：`{ name: "Ruby" }` 是 `{ :name => "Ruby" }` 的简写形式。
- `to_sym` 和 `to_s` 方法可以用来转换字符串和符号，但不要将用户输入直接转换为符号，以防内存泄漏。

## 集合（Collections）
- `each` 用于遍历集合元素，`map` 用于对元素进行转换。
- `select` 和 `reject` 用于过滤元素，返回新的集合。
- `find` 方法返回第一个匹配的元素；如果没有匹配项，则返回 `nil`（而不是抛出异常）。
- `reduce` 和 `inject` 用于对集合元素进行累积操作，例如：`[1, 2, 3].reduce(0) { |sum, n| sum + n }`。
- `compact` 方法会删除集合中的 `nil` 元素；`flatten` 方法会展开嵌套的数组。

## 类（Classes）
- `attr_accessor` 用于定义 getter 和 setter 方法；`attr_reader` 仅用于读取属性值，`attr_writer` 仅用于写入属性值。
- `initialize` 是构造函数，用于初始化对象实例；实例变量以 `@` 开头。
- `self.method` 用于访问类方法；也可以使用 `class << self` 块来定义多个类方法。
- 使用 `<` 进行继承，例如：`class Dog < Animal`。
- 模块（Modules）可用于组合代码片段（mixins）；`include` 用于添加实例方法，`extend` 用于添加类方法。

## 元编程（Metaprogramming）
- `method_missing` 方法用于捕获未定义的方法调用；建议同时定义 `respond_to_missing?` 方法。
- `define_method` 方法用于动态创建方法，接受方法名和代码块作为参数。
- `send` 方法用于按名称调用方法，例如：`obj.send(:method_name, args)`。
- 可以打开类的源代码（Open classes），以便向任何类添加方法——但请谨慎使用，优先考虑使用更优雅的改进方法（refinements）。
- `class_eval` 和 `instance_eval` 可用于在运行时修改类的行为。

## 作用域（Scope）
- `def`、`class`、`module` 等关键字用于定义代码的作用域；在较旧的 Ruby 版本中，块变量可能会泄漏到外部作用域，但在现代 Ruby 中不会再发生这种情况。
- 常量应该使用大写字母开头（UPPERCASE），以便通过字典顺序查找；例如：`Module::Class::CONSTANT`。
- 使用 `::` 来区分不同的命名空间，例如：`Module::Class::CONSTANT`。
- 全局变量（以 `$` 开头）通常是不推荐的做法，因为容易引发代码问题；除非是内置的变量（如 `$stdout`），否则应避免使用。

## 常见错误（Common Mistakes）
- 使用 `==` 比较两个对象的内容，而应该使用 `equal?` 来比较对象的身份（是否相等）——这与 Java 的习惯相反。
- 字符串插值必须使用双引号，例如：`"Hello #{name}"`，而不是 `'Hello #{name}'`。
- 在迭代过程中修改集合元素是允许的，但容易引起混淆；建议使用 `map` 或 `select` 来创建新的集合。
- 范围（Ranges）：`1..5` 包含 1 到 5（包括 5），`1...5` 不包含 5（不包括 5）。
- `require` 用于加载外部库，`require_relative` 用于加载同一项目内的库；`require` 用于加载 Gem 包。

## Gem 和 Bundler
- `Gemfile` 文件用于列出项目依赖的库。
- `bundle install` 命令用于安装这些依赖库。
- `Gemfile.lock` 文件用于固定库的版本，确保构建结果的稳定性。
- `bundle exec` 命令用于运行包含所有依赖库的环境，以避免版本冲突。
- 使用语义版本控制，例如：`~> 2.1` 表示“大于或等于 2.1 且小于 3.0”的版本范围。