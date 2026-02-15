---
name: Django
description: 避免常见的 Django 错误：QuerySet 评估问题、N+1 查询、迁移冲突以及 ORM 相关的陷阱。
metadata: {"clawdbot":{"emoji":"🌿","requires":{"bins":["python3"]},"os":["linux","darwin","win32"]}}
---

## QuerySet 的使用与评估  
- QuerySet 是惰性的：只有在迭代、切片或进行布尔值判断时才会访问数据库。  
- 如果需要重复使用 QuerySet，应先将其转换为列表（`list(queryset)`），因为重复迭代会再次访问数据库。  
- `exists()` 的执行速度比 `bool(queryset)` 更快，因为它不会获取所有数据行。  
- `count()` 和 `len()` 的区别在于：`count()` 使用 SQL 的 `COUNT` 函数，而 `len()` 会获取所有数据行。  

## N+1 查询模式  
- 对于 `ForeignKey` 或 `OneToOne` 关系，使用 `select_related` 可以通过单次 JOIN 查询获取相关对象；  
- 对于 `ManyToMany` 或反向 `FK` 关系，使用 `prefetch_related` 可以预先获取相关对象并缓存。  
- 如果在循环中直接访问相关对象而不使用 `prefetch`，会导致 N+1 次数据库查询（即每次迭代都会触发一次查询）。可以使用 `django-debug-toolbar` 来检查这种情况。  
- 对于自定义的 QuerySet，可以使用 `prefetch` 方法来预获取数据，并对预获取的数据进行过滤或添加注释。  

## ORM 使用中的注意事项  
- `update()` 方法不会自动调用 `save()` 方法，因此不会触发信号或更新 `auto_now` 属性。  
- 使用 `F()` 方法可以进行数据库级别的操作（例如 `F('count') + 1` 可以避免竞态条件）。  
- `exclude(field=None)` 会排除值为 `NULL` 的记录，但这可能不符合实际需求。  
- 在某些情况下，需要在使用 `values()` 方法后使用 `distinct()` 来去除重复记录。  

## 数据库迁移  
- 当模型发生变化时，需要手动运行 `makemigrations` 命令。  
- 如果迁移文件存在冲突，应通过重命名文件来避免冲突（例如使用 `git merge` 合并冲突的迁移文件），或者使用 `rebase` 命令来处理。  
- 可以使用 `squashmigrations` 命令来合并多个迁移文件，但请确保在完全部署之前保持迁移文件的原始状态。  
- 如果表已经存在，可以使用 `migrate --fake appname 0001` 命令来创建虚拟迁移文件（仅用于测试）。  

## 设置配置中的注意事项  
- 当 `DEBUG=False` 时，必须设置 `ALLOWED_HOSTS`；否则程序会崩溃。  
- `SECRET_KEY` 必须是保密的，不应包含在代码仓库中，而应作为环境变量进行配置。  
- 在生产环境中，需要使用 `collectstatic` 命令来收集静态文件；如果 `DEBUG=True`，静态文件的加载方式会有所不同。  
- `STATIC_ROOT` 和 `STATICFILES_DIRS` 的作用分别是指定静态文件的存储路径和来源目录。  

## CSRF 防护  
- 表单中需要添加 `{% csrf_token %}` 标签，否则 POST 请求会收到 403 错误。  
- AJAX 请求需要设置 `X-CSRFToken` 头部字段，该字段可以从 cookie 中获取。  
- `@csrf_exempt` 注解会带来安全风险，仅应用于与其他认证机制结合使用的 Webhook。  

## 测试相关注意事项  
- `TestCase` 类会自动在测试过程中创建事务，这可以提高测试效率，但无法模拟事务的具体行为。  
- `TransactionTestCase` 类会实际执行事务操作，虽然效率较低，但适用于需要测试事务逻辑的场景。  
- 对于视图函数，可以使用 `Client` 类；对于中间件或直接处理请求的视图函数，可以使用 `RequestFactory` 类。  
- 使用 `override_settings` 装饰器可以针对不同的配置环境进行测试。  

## 常见错误  
- 使用 `get()` 方法获取对象时，可能会遇到 `DoesNotExist` 或 `MultipleObjectsReturned` 错误，此时应使用 `filter().first()` 来获取第一个符合条件的对象。  
- `auto_now` 属性不能被直接覆盖，如果需要手动设置时间戳，可以使用 `default=timezone.now`。  
- 模型中的循环导入可能导致问题，应使用字符串引用（例如 `ForeignKey('app.Model')`）。  
- `related_name` 属性可能会与其他字段冲突，应设置唯一值，或者使用 `related_name='+'` 来避免冲突。