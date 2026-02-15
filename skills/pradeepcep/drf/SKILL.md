---
name: drf
description: Django REST Framework的搭建最佳实践及需要注意的事项。
homepage: "https://github.com/pradeepcep/openclaw-drf"
metadata: {"clawdbot":{"emoji":"🔥","requires":{"bins":["python3"]},"os":["linux","darwin","win32"]}}

---

# Django REST Framework

本技能详细介绍了如何使用 **Django + Django REST Framework (DRF)** 生成、配置和优化 REST API。内容包括项目设置、API 结构、序列化器（serializers）、视图集（viewsets）、路由（routing）、认证（authentication）、性能优化、测试以及常见问题的解决方法。

## 概述

在以下情况下，请使用本技能：
- 开始一个新的 Django + Django REST Framework (DRF) 项目
- 在使用 Django REST Framework (DRF) 的 Django 项目中工作
- 在 `requirements.txt` 或 `pyproject.toml` 中列出了 `djangorestframework` 的 Python 项目中工作
- 在 Django 项目中创建 REST API 端点
- 在 Django 项目中添加、修改或应用序列化器、视图集、权限控制、认证、分页和过滤的最佳实践
- 在 Django 项目中优化数据库查询和 API 性能

## 启动项目

### 1. 创建并激活虚拟环境

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install django djangorestframework
django-admin startproject project .
```

### 2. Create an App

```
python manage.py startapp [appname or "api"]
```

### 3. Configure Django REST Framework

Add to `settings.py`:

```
INSTALLED_APPS = [
    "rest_framework",
    appname or "api",
]

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULTRenderer_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 10,
}
```


## Core Principles

### Serializers

-   Prefer `ModelSerializer` to reduce boilerplate.
-   Keep serializers focused on **validation and representation**.
-   Use separate serializers for:
    -   list vs detail
    -   read vs write
    -   public vs internal APIs
-   Add serializers to a `serializers.py` file inside the appropriate Django app

Example:

```
# 文件：accounts/serializers.py
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]
```

### Views & ViewSets

-   Use `ViewSet` or `ModelViewSet` for standard CRUD APIs.
-   Override `get_queryset()` instead of filtering in the serializer.
-   Keep views thin, and use features from DRF parent classes as much as possible
-   Always return responses in the configured format (fallback to json)
-   Always put views in the `views.py` file inside the appropriate Django app

Example:

```
# 文件：accounts/views.py
class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(is_active=True)
```

### Routing

-   Use DRF routers for consistency and discoverability.
-   Avoid deeply nested URLs unless strictly necessary.
-   Put routers in a `urls.py` file inside the appropriate Django app
-   Make sure the `urls.py` inside the Django app is included in the main `urls.py`

Example:

```
# 文件：accounts/urls.py
router = DefaultRouter()
router.register("users", UserViewSet)
urlpatterns = router.urls
```

Example:
```
# 文件：project/urls.py
urlpatterns = [
    path("", include("accounts.urls"))
]
```

## Authentication & Permissions

### Authentication

-   Prefer stateless authentication for APIs.
-   Token-based or JWT authentication is recommended.
-   Never rely on session authentication for public APIs unless
    explicitly required.

### Permissions

-   Always define explicit permissions.
-   Default to secure (`IsAuthenticated`) rather than open.
-   Use custom permission classes for fine-grained control.
-   Create custom permissions inside a `permissions.py` file inside the appropriate Django app.

Example:

```
python
permission_classes = [IsAuthenticated]
```


## Pagination, Filtering & Throttling

### Pagination

-   Always paginate list endpoints.
-   Avoid returning unbounded querysets.

### Filtering

-   Filter in `get_queryset()` using request parameters.
-   Validate query params explicitly.

### Throttling

Protect APIs from abuse:

```
REST_FRAMEWORK = {
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "100/day",
        "user": "1000/day",
    },
}
```


## Performance Best Practices

### Query Optimization

-   Always inspect query counts in list views.
-   Use `select_related()` for foreign keys.
-   Use `prefetch_related()` for many-to-many and reverse relations.

Example:

```
# 文件：orders/views.py
def get_queryset(self):
    return Order.objects.select_related("customer").prefetch_related("items")
```


### Caching

-   Cache expensive read-heavy endpoints.
-   Use Redis or Memcached.
-   Never cache user-specific responses globally.


## Testing

-   Write tests for:
    -   serializers
    -   permissions
    -   edge cases
-   Use `APITestCase` and `APIClient`.
-   Test both success and failure paths.


## Common Gotchas & Pitfalls

### Bulky Views / Bulky Serializers

Avoid putting business logic inside:
    - serializers
    - views
    - permission classes

Instead, use:
    - service modules
    - domain logic in models
    - reusable helper functions

### N+1 Query Problems

DRF does **not** optimize queries automatically. Missing
`select_related()` or `prefetch_related()` will silently destroy
performance.

### Silent Security Bugs

Common mistakes:
    - Forgetting permission classes
    - Allowing unauthenticated access by default
    - Exposing writeable fields unintentionally
    - Exposing passwords or secret fields in response

Always audit:
    - serializer `fields`
    - permission classes
    - allowed HTTP methods


### Assuming Async Behavior

Django REST Framework is **primarily synchronous**.

Do not assume:
    - async views improve performance automatically
    - background tasks belong in request/response cycles

Use task queues (Celery etc.) for long-running work.


## Example Commands

```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## 参考资料

- Django 文档
- Django REST Framework 文档
- 实际生产环境中的 Django REST Framework 模式（最佳实践）