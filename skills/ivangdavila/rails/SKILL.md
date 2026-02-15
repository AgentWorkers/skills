---
name: Rails
description: 使用正确的规范、性能最佳实践以及安全措施来构建 Rails 应用程序。
metadata: {"clawdbot":{"emoji":"💎","requires":{"bins":["rails"]},"os":["linux","darwin","win32"]}}
---

# Rails 开发规范

## Active Record（活动记录）
- **N+1 查询** 是性能问题的主要根源——使用 `includes`、`preload` 或 `eager_load` 来优化。
- 对于大型数据集，使用 `find_each`；`all.each` 会将所有数据加载到内存中。
- 使用 `where.not(field: nil)` 而不是 `where("field IS NOT NULL)`，这样更通用。
- `update_all` 和 `delete_all` 会跳过回调函数——请谨慎使用，避免误操作。
- 当只需要获取数据时，使用 `pluck(:id)`，避免创建完整的模型实例。

## 关联关系（Associations）
- 使用 `dependent: :destroy` 可以实现级联删除——否则可能会导致孤儿记录（即没有关联关系的记录）。
- 对于多对多关系，使用 `has_many :through`；`has_and_belongs_to_many` 没有这种功能。
- `inverse_of` 可以帮助 Rails 重用已加载的对象——在处理嵌套表单时尤为重要。
- 使用 `touch: true` 可以更新父模型的时间戳——有助于缓存失效的处理。

## 迁移（Migrations）
- **切勿编辑已提交的迁移文件**——需要修改时请创建新的迁移文件，否则回滚操作可能会影响其他开发人员。
- 对于大型表，建议在单独的迁移文件中添加 `add_index` 操作——否则可能会锁定数据库表，导致长时间延迟。
- 在迁移文件中设置 `null: false` 和 `default:` 属性——不要仅依赖模型自身的验证规则。
- `change` 方法必须是可逆的——对于复杂的更改，请使用 `up`/`down` 方法。
- 使用 `add_foreign_key` 来设置外键——这可以确保数据库层面的数据完整性，而不仅仅是模型层面的验证。

## 控制器（Controllers）
- 使用 `params.require(:model).permit(:fields)` 来明确指定允许的参数。
- 使用 `before_action` 来处理通用逻辑——但不要嵌套太多层，否则会导致逻辑难以追踪。
- 使用 `respond_to` 块来处理不同的响应格式（JSON 或 HTML）。
- 避免在控制器中编写业务逻辑——将其提取到模型或服务对象中处理。
- `redirect_to` 用于结束请求——但请求之后的代码仍然会执行，可以使用 `return` 或 `and return` 来终止请求。

## 视图（Views）和部分视图（Partial Views）
- 使用 `render collection:` 比使用循环和 `render partial:` 更快——一次渲染多个部分视图比多次单独渲染更快。
- 使用 `cache` 辅助方法来缓存数据——`cache @post do` 可以在数据更新后自动失效。
- 使用 `content_for` 和 `yield` 来生成布局内容——不要使用实例变量。
- 使用 `turbo_frame` 和 `turbo_stream` 可以加速页面加载。

## 安全性（Security）
- 默认情况下，`protect_from_forgery` 是启用的——在没有充分理解其作用之前不要禁用它。
- **避免 SQL 注入**：永远不要在查询中直接使用用户输入——始终使用 `?` 占位符或哈希值。
- 对于批量赋值操作，使用强参数（strong parameters）来防止属性注入——这应该在控制器层面进行验证，而不是模型层面。
- `html_safe` 和 `raw` 方法可以绕过 HTML 转义——但仅适用于可信的内容。
- 生产环境中，默认启用 `secure` 和 `httponly` cookie 标志。

## 后台任务（Background Jobs）
- 使用 Sidekiq 或 Solid Queue 来处理异步任务——不要在请求周期中使用 `delay` 方法。
- 后台任务应该是幂等的（idempotent）——在重试时可能会被多次执行。
- 传递对象的 ID 而不是对象本身——序列化的对象在类发生变化时可能会出问题。
- 使用 `perform_later` 来安排任务的执行时间，`perform_now` 用于立即执行任务——除非在测试环境中，否则建议使用 `perform_later`。

## 缓存（Caching）
- 使用多层缓存（Russian doll caching）——内部更改只会影响对应的缓存层。
- 使用 `cache_key_with_version` 来为缓存片段设置版本号——这样可以实现自动失效。
- 使用 `Rails.cache.fetch` 来缓存计算结果。
- 对于低级别的缓存，需要明确设置失效时间——缓存片段会在模型发生变化时自动失效。

## 测试（Testing）
- 在大多数情况下，使用 `FactoryBot` 而不是固定的测试数据（fixtures）——这样更灵活，也更不容易出错。
- `let` 是惰性加载的，`let!` 是立即加载的——当需要立即执行操作时使用 `let!`。
- 使用 `freeze_time` 来模拟时间依赖的测试环境——`travel_to` 块可以自动恢复测试状态。
- 使用 `assert_difference` 来检查数据的变化——这比使用 `before/after` 更直观。
- 使用 Capybara 进行系统测试——虽然速度较慢，但可以测试整个应用程序（包括 JavaScript 部分）。

## 性能（Performance）
- `bullet` 插件可以帮助检测 N+1 查询问题——对于任何 Rails 应用程序来说都非常重要。
- `rack-mini-profiler` 可以显示查询的执行时间——在开发环境中非常有用。
- 在控制台中将 `ActiveRecord::Base.logger` 设置为 `nil` 可以减少不必要的日志输出。
- 为外键和经常被查询的列创建数据库索引——查看 `explain` 的输出结果以优化查询性能。

## 常见错误（Common Mistakes）
- `save` 和 `save!` 的区别：`save` 先返回布尔值，`save!` 在失败时会抛出异常。
- `update` 方法在失败时返回 `false`——请检查返回值，或者使用 `update!` 来确保数据被成功保存。
- `||=` 操作会缓存 `nil` 和 `false` 的值——对于这种情况，可以使用 `defined?` 来判断值是否存在。
- 使用回调函数可能会导致复杂的逻辑链——可以考虑使用服务对象来处理这些逻辑。
- `default_scope` 会影响所有查询，包括关联查询——这几乎总是一个错误。