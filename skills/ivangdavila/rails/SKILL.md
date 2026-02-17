---
name: Rails
slug: rails
version: 1.0.1
description: 构建可靠的 Rails 应用程序时，需要避免 ActiveRecord 的陷阱、N+1 查询以及回调相关的错误。
metadata: {"clawdbot":{"emoji":"🛤️","requires":{"bins":["rails"]},"os":["linux","darwin","win32"]}}
---
## 快速参考

| 主题 | 文件 |
|-------|------|
| N+1 问题、回调函数、验证规则、作用域 | `activerecord.md` |
| 强参数、过滤器、渲染逻辑 | `controllers.md` |
| 路由冲突、约束条件 | `routing.md` |
| 部分视图（partials）、辅助函数、缓存机制、XSS 防护 | `views.md` |
| ActiveJob、Sidekiq、重试机制 | `jobs.md` |
| 批量数据操作、CSRF 防护、SQL 注入防护 | `security.md` |

## 重要规则

- `save` 方法在操作失败时会返回 `false`；使用 `save!` 时需要检查返回值或使用 `!` 操作符强制保存。
- `update_all`/`delete_all` 方法会跳过回调函数和验证规则；如果不注意可能会导致数据损坏。
- `find_each` 方法用于批量查询数据，但 `Model.all.each` 会将整个表加载到内存中。
- `redirect_to` 方法不会停止当前操作的执行；在调用 `redirect_to` 后仍需继续执行后续代码，可以使用 `and return` 来实现这一点。
- 如果缺少 `dependent: :destroy` 规则，可能会导致孤儿记录（即没有关联模型的记录）长期存在。
- `default_scope` 会污染所有查询（包括关联查询），这种做法几乎总是错误的。
- 回调函数会默默地执行链式操作；如果需要停止保存操作，应使用 `throw :abort`，但该方法只会返回 `false` 而不会抛出异常。
- 如果在 `where` 字符串中省略了 `references`，仍然可能引发 N+1 问题（即重复插入数据）。
- 对于 `||=` 操作符，应使用 `defined?(@var) ? @var : @var = compute` 来避免缓存 `nil` 或 `false` 值。
- `has_many through:` 与 `has_and_belongs_to_many` 的区别在于：`has_and_belongs_to_many` 不会为关联模型生成额外的关联模型。
- 使用嵌套的 `before_action` 会导致代码逻辑难以阅读；建议避免使用多重继承。
- `render` 方法不会停止当前操作；如果继续执行其他代码，可能会导致重复渲染错误。