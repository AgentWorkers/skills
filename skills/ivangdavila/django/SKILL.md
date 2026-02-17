---
name: Django
slug: django
version: 1.0.1
description: 构建安全的 Django 应用程序时，需要避免 ORM（对象关系映射）中的陷阱、N+1 查询以及常见的安全漏洞。
metadata: {"clawdbot":{"emoji":"🌿","requires":{"bins":["python3"]},"os":["linux","darwin","win32"]}}
---
## 快速参考

| 主题 | 文件 |
|-------|------|
| QuerySet 的惰性求值、N+1 查询、事务处理 | `orm.md` |
| 请求处理、中间件、上下文 | `views.md` |
| 数据验证、CSRF 防御、文件上传 | `forms.md` |
| 数据迁移、信号（signals）、模型管理器 | `models.md` |
| XSS 防御、CSRF 防御、SQL 注入、身份验证 | `security.md` |
| 异步视图、异步环境下的 ORM 操作、通道（channels） | `async.md` |

## 重要规则

- QuerySet 是惰性求值的：多次迭代会多次访问数据库，使用 `list()` 方法进行缓存。
- 对于外键关联（FK）或双向关联（O2O）关系，使用 `select_related`；对于多对多（M2M）关系，使用 `prefetch_related` 以避免 N+1 查询。
- `update()` 方法会跳过 `save()` 操作，因此不会触发信号（signals），也不会自动更新字段的 `auto_now` 属性。
- 使用 `F()` 方法进行原子性更新：`F('count') + 1` 可以避免竞态条件。
- `get()` 方法会返回 `DoesNotExist` 或 `MultipleObjectsReturned` 异常，使用 `filter().first()` 可以确保获取到正确的结果。
- 当 `DEBUG` 设置为 `False` 时，必须配置 `ALLOWED_HOSTS`；否则请求会返回 400 错误。
- 表单需要包含 `{% csrf_token %}` 防御代码，否则 POST 请求会返回 403 禁止访问错误。
- `auto_now` 属性不能被覆盖，如果需要手动设置时间戳，请使用 `default=timezone.now`。
- `exclude(field=None)` 方法用于排除 NULL 值；如果需要排除所有 NULL 值，可以使用 `filter(field__isnull=True)`。
- 在模型中遇到循环导入时，使用字符串引用（例如：`ForeignKey('app.Model')`）。
- `transaction.atomic()` 方法不会捕获异常，错误仍然会继续传播。
- 在异步视图中使用 `sync_to_async` 方法时，ORM 操作仍然是同步的。