---
name: Laravel
slug: laravel
version: 1.0.1
description: 构建健壮的 Laravel 应用程序时，需要避免 Eloquent 模型的陷阱、队列执行失败以及认证相关的问题。
metadata: {"clawdbot":{"emoji":"🔴","requires":{"bins":["php","composer"]},"os":["linux","darwin","win32"]}}
---

## 快速参考

| 主题 | 文件 |
|-------|------|
| N+1次查询、即时加载、访问器、观察者 | `eloquent.md` |
| 验证、中间件顺序、依赖注入 | `controllers.md` |
| 作业序列化、重试、失败作业 | `queues.md` |
| 安全策略、门控机制、Sanctum令牌 | `auth.md` |
| XSS转义、组件、插槽 | `blade.md` |
| 命令、调度、工具 | `artisan.md` |

## 重要规则

- 在循环中使用 `with('posts')` 进行即时加载，而不是使用懒加载的 `->posts`（这会导致N+1次查询问题）  
- 在开发环境的 `AppServiceProvider` 中启用 `preventLazyLoading()` 可以避免N+1次查询的问题，并提前捕获错误  
- `env()` 只应在配置文件中使用；在 `config:cache` 后调用会返回 `null`  
- 使用 `$fillable` 列表来指定可填充的字段；否则可能导致批量赋值攻击  
- `find()` 方法可能返回 `null`，请使用 `findOrFail()` 来避免空值检查  
- 作业属性在序列化时会转换为ID；在后续处理过程中可能需要重新获取数据（数据可能已经过时或被删除）  
- `route:cache` 需要控制器路由；否则会破坏缓存机制  
- `DB::transaction()` 无法捕获 `exit` 或超时异常，只有异常发生时才会回滚事务  
- `RefreshDatabase` 使用事务处理，比 `DatabaseMigrations` 更快  
- `{!! $html !!}` 会跳过HTML转义；默认应使用 `{{ }}` 进行转义  
- 中间件的执行顺序很重要：前面的中间件会覆盖后面的中间件  
- `required` 验证规则允许空字符串通过；对于必填字段，请使用 `required|filled`  
- `firstOrCreate` 方法会立即保存数据；`firstOrNew` 方法返回未保存的模型  
- 路由模型绑定时使用 `id`；请覆盖 `getRouteKeyName()` 方法以自定义路由名称