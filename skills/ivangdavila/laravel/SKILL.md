---
name: Laravel
description: 避免常见的 Laravel 错误：N+1 查询、批量赋值、缓存相关的问题以及队列序列化错误。
metadata: {"clawdbot":{"emoji":"🔴","requires":{"bins":["php"]},"os":["linux","darwin","win32"]}}
---

## Eloquent N+1 问题  
- 在循环中访问关联关系时，应避免使用 `User::all()` 后再调用 `->posts()`，而应直接使用 `User::with('posts')->get()`。  
- 嵌套关联关系需要使用点表示法（例如：`with('posts_comments')`）来进行关联数据的预加载（eager loading）。  
- 使用 `withCount('posts')` 可以在不加载关联数据的情况下统计关联记录的数量，并在模型中添加 `posts_count` 属性。  
- 在 `AppServiceProvider` 中启用 `preventLazyLoading()` 可以防止在开发环境中出现 N+1 查询问题，从而提前发现潜在错误。  

## 批量赋值  
- 应选择 `$fillable` 白名单或 `$guarded` 黑名单之一，切勿同时使用两者。  
- 将 `$guarded` 设置为 `[]` 会允许所有字段被赋值，但这很危险，建议明确指定可赋值的字段（使用 `$fillable`）。  
- `create()` 和 `update()` 方法会自动处理批量赋值；直接使用 `$model->field = x` 会绕过批量赋值机制。  
- 请求中经过验证的数据并不会自动被视为安全的数据，仍会经过 `$fillable` 和 `$guarded` 的过滤。  

## 缓存相关问题  
- `config:cache` 会缓存 `.env` 文件中的配置值；`env()` 只能在缓存后的配置文件中生效。  
- `route:cache` 要求所有路由都必须基于控制器实现；不允许使用闭包。  
- `php artisan optimize` 会同时清理配置、路由和视图缓存，建议在部署后执行该命令。  
- 本地对配置的修改不会立即反映到缓存中，需要执行 `php artisan cache:clear && config:clear && route:clear` 来清除缓存。  

## 队列作业  
- 队列作业的属性会被序列化；模型在队列中仅保存其 ID，实际处理时需要重新获取数据。  
- 闭包不能被直接放入队列中，必须使用可调用的类作为队列作业。  
- 失败的作业会被保存到 `failed_jobs` 表中，可以通过该表查看错误信息。  
- `tries`、`timeout` 和 `backoff` 等属性可以在作业类中设置，也可以在配置文件中配置。  
- `connection` 和 `queue` 的概念不同：`connection` 指的是数据库连接，而 `queue` 指的是用于传输作业的通道（在特定的数据库驱动程序中）。  

## 中间件  
- 中间件的执行顺序很重要：位于前面的中间件会先于后面的中间件执行。  
- `$middleware` 是全局中间件，适用于所有请求；`$middlewareGroups` 可用于区分 Web 和 API 请求。  
- 中间件会在响应发送后执行，可用于日志记录或资源清理等操作。  
- 路由中间件可以接受参数；例如：`role:admin` 会将 “admin” 传递给相应的中间件。  

## 数据库操作  
- `migrate:fresh` 会删除所有表；`migrate:refresh` 会先回滚再执行新的迁移操作。  
- `DB::transaction()` 会在遇到异常时自动回滚事务，但在手动退出或超时时不会回滚。  
- 默认情况下，数据库操作会进行软删除（仅删除记录的引用，不删除数据本身；使用 `withTrashed()` 可以强制删除数据）。  
- `firstOrCreate` 会尝试创建新记录（如果不存在则创建），而 `firstOrNew` 会尝试更新现有记录（如果不存在则创建新记录）。  

## 测试  
- `RefreshDatabase` 比 `DatabaseMigrations` 更快，因为它使用了事务机制。  
- 数据库工厂方法中，`create()` 会保存数据，`make()` 不会保存数据；单元测试应使用 `make()` 方法。  
- `this->withoutExceptionHandling()` 可以显示实际的错误信息，有助于调试。  
- 可以使用 `Queue::assertPushed()` 来验证作业是否已被正确放入队列，而无需实际执行该作业。  

## 常见错误  
- `find()` 方法可能返回 `null`，`findOrFail()` 方法会抛出 404 错误；建议使用 `OrFail` 方法来避免空值检查。  
- 在已缓存的配置文件中使用 `env()` 时，`env()` 可能返回 `null`；请仅在配置文件内部使用 `env()`。  
- 验证规则中的 `required` 并不意味着字段必须非空；对于字符串字段，应使用 `required|filled`。  
- 路由模型绑定默认使用 `id` 作为键；可以使用 `getRouteKeyName()` 来自定义键名。