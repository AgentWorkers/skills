# Django生产环境工程

这是一套完整的开发方法论，涵盖了Django应用程序的构建、扩展和运维过程。从项目结构到部署，从安全性到性能优化——涵盖了Django团队所需的所有决策框架。

## 快速健康检查

对任何Django项目执行以下8项检查：

| 序号 | 检查项 | 是否合格 |
|---|---|---|
| 1 | 设置文件分离 | 存在`settings/base.py`、`local.py`、`production.py` | ✅ 按环境分隔设置文件 |
| 2 | 秘密密钥管理 | `SECRET_KEY`未硬编码在代码中，生产环境中`DEBUG`设置为`False` | ✅ 使用环境变量或安全存储库管理密钥 |
| 3 | 数据库连接池 | 使用连接池（如pgbouncer或django-db-conn-pool） | ✅ 配置了连接池 |
| 4 | 数据库迁移 | `python manage.py showmigrations`显示所有已应用的迁移 | ✅ 所有迁移都已应用 |
| 5 | 静态文件处理 | 配置了`collectstatic`和CDN/whitenoise | ✅ 静态文件正确部署 |
| 6 | 异步任务 | 使用Celery、django-q或Huey处理后台任务 | ✅ 后台任务不会阻塞用户请求 |
| 7 | 缓存机制 | 配置了缓存后端（如Redis或Memcached） | ✅ 使用非模拟缓存（DummyCache） |
| 8 | 安全性 | `python manage.py check --deploy`检查通过 | ✅ 所有安全检查都通过 |

**得分：合格项数量 / 8项** —— 得分低于6分时，应先修复基础问题。

---

## 第1阶段：项目架构

### 推荐的项目结构

```
myproject/
├── config/                    # Project config (was myproject/)
│   ├── __init__.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py           # Shared settings
│   │   ├── local.py          # Development
│   │   ├── staging.py        # Staging
│   │   └── production.py     # Production
│   ├── urls.py               # Root URL conf
│   ├── wsgi.py
│   ├── asgi.py
│   └── celery.py             # Celery app
├── apps/
│   ├── users/                # Custom user model (ALWAYS)
│   │   ├── models.py
│   │   ├── managers.py
│   │   ├── admin.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── services.py       # Business logic
│   │   ├── selectors.py      # Complex queries
│   │   ├── tests/
│   │   │   ├── test_models.py
│   │   │   ├── test_views.py
│   │   │   └── test_services.py
│   │   └── migrations/
│   ├── core/                 # Shared utilities
│   │   ├── models.py         # Abstract base models
│   │   ├── permissions.py
│   │   ├── pagination.py
│   │   ├── exceptions.py
│   │   └── middleware.py
│   └── <domain>/             # Feature apps
├── templates/
├── static/
├── media/
├── requirements/
│   ├── base.txt
│   ├── local.txt
│   └── production.txt
├── docker/
├── scripts/
├── manage.py
├── pyproject.toml
├── Makefile
└── .env.example
```

### 7条架构规则

1. **从项目开始就使用自定义用户模型** —— 将`AUTH_USER_MODEL`设置为`users.User`。后期更改会非常麻烦。
2. **分离业务逻辑和服务层** —— 视图处理HTTP请求；`services.py`处理业务逻辑；`selectors.py`处理复杂查询。
3. **每个业务领域对应一个应用** —— 不要按模型划分应用，而是将相关模型放在同一个应用中。
4. **按环境分隔设置文件** —— 不要在同一个文件中使用`if DEBUG`条件判断。
5. **在核心代码中定义抽象基模型** —— 如`TimeStampedModel`、`UUIDModel`可在多个应用中复用。
6. **分离配置文件** —— 有`base.txt`（通用配置）、`local.txt`（开发工具配置）、`production.txt`（生产环境配置）。
7. **保持应用之间的解耦** —— 应用之间通过服务层通信，而不是直接导入彼此的模型。谨慎使用信号（signals）。

### 抽象基模型

```python
# apps/core/models.py
import uuid
from django.db import models

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True

class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False, db_index=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def soft_delete(self):
        from django.utils import timezone
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=["is_deleted", "deleted_at"])
```

---

## 第2阶段：ORM（对象关系映射）掌握与查询优化

### 避免N+1查询

```python
# ❌ N+1 — fires 1 + N queries
for order in Order.objects.all():
    print(order.customer.name)        # Each access = new query
    for item in order.items.all():    # Each access = new query
        print(item.product.name)      # Each access = new query

# ✅ Optimized — fires 3 queries total
orders = (
    Order.objects
    .select_related("customer")              # FK/OneToOne — JOIN
    .prefetch_related(
        Prefetch(
            "items",
            queryset=OrderItem.objects
                .select_related("product")   # Nested FK
                .only("id", "quantity", "product__name")  # Only needed fields
        )
    )
)
```

### `select_related`与`prefetch_related`的选择

| 关系类型 | 使用方法 | 原因 |
|---|---|---|
| 外键关系（正向） | 使用`select_related` | 通过SQL JOIN完成，一次查询 |
| 一对一关系 | 使用`select_related` | 通过SQL JOIN完成，一次查询 |
| 多对多关系 | 使用`prefetch_related` | 分别执行查询，然后通过Python代码连接结果 |
| 反向外键关系 | 使用`prefetch_related` | 分别执行查询，然后通过Python代码连接结果 |
| 过滤后的数据预取 | 使用`Prefetch()`方法 | 使用自定义查询集 |

### QuerySet评估规则

```python
# QuerySets are LAZY — no database hit until evaluated
qs = Order.objects.filter(status="pending")  # No query yet

# These EVALUATE the queryset (trigger SQL):
list(qs)           # Iteration
len(qs)            # Use qs.count() instead
bool(qs)           # Use qs.exists() instead
qs[0]              # Indexing
repr(qs)           # In shell/debugger
for obj in qs:     # Iteration
if qs:             # Use qs.exists()
```

### 批量操作

```python
# ❌ N queries
for item in items:
    Product.objects.create(name=item["name"], price=item["price"])

# ✅ 1 query
Product.objects.bulk_create(
    [Product(name=i["name"], price=i["price"]) for i in items],
    batch_size=1000,
    ignore_conflicts=True,  # Skip duplicates
)

# ✅ Bulk update
Product.objects.filter(category="sale").update(
    price=F("price") * 0.9  # 10% discount — single query, no race conditions
)

# ✅ Bulk update with different values
products = Product.objects.filter(id__in=ids)
for p in products:
    p.price = new_prices[p.id]
Product.objects.bulk_update(products, ["price"], batch_size=1000)
```

### 数据库函数与表达式

```python
from django.db.models import F, Q, Value, Count, Avg, Sum, Case, When
from django.db.models.functions import Coalesce, Lower, TruncMonth

# Conditional aggregation
Order.objects.aggregate(
    total_revenue=Sum("amount"),
    paid_revenue=Sum("amount", filter=Q(status="paid")),
    refund_count=Count("id", filter=Q(status="refunded")),
    avg_order_value=Avg("amount", filter=Q(status="paid")),
)

# Annotate with computed fields
customers = (
    Customer.objects
    .annotate(
        order_count=Count("orders"),
        total_spent=Coalesce(Sum("orders__amount"), Value(0)),
        last_order=Max("orders__created_at"),
    )
    .filter(order_count__gte=5)
    .order_by("-total_spent")
)

# Monthly revenue report
monthly = (
    Order.objects
    .filter(status="paid")
    .annotate(month=TruncMonth("created_at"))
    .values("month")
    .annotate(
        revenue=Sum("amount"),
        count=Count("id"),
        avg=Avg("amount"),
    )
    .order_by("month")
)

# Case/When for computed status
users = User.objects.annotate(
    tier=Case(
        When(total_spent__gte=10000, then=Value("platinum")),
        When(total_spent__gte=5000, then=Value("gold")),
        When(total_spent__gte=1000, then=Value("silver")),
        default=Value("bronze"),
    )
)
```

### 索引策略

```python
class Order(TimeStampedModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, db_index=True)  # Single column
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        indexes = [
            # Composite index — for queries filtering both
            models.Index(fields=["status", "created_at"], name="idx_order_status_created"),
            # Partial index — only index what you query
            models.Index(
                fields=["customer"],
                condition=Q(status="pending"),
                name="idx_order_pending_customer",
            ),
            # Covering index (Postgres) — avoid table lookup
            models.Index(
                fields=["status"],
                include=["amount", "created_at"],
                name="idx_order_status_covering",
            ),
        ]
        # Default ordering impacts ALL queries — be intentional
        ordering = ["-created_at"]
```

### 8条ORM使用规则

1. **始终使用`select_related`或`prefetch_related`** —— 安装`django-debug-toolbar`并监控查询次数。
2. **永远不要同时使用`.count()`和`.all()`** —— 使用`.exists()`进行布尔判断。
3. **使用`F()`表达式进行原子更新** —— 避免竞争条件。
4. **对于不需要显示的文本或JSON字段，使用`.only()`或`.defer()`**。
5. **当不需要模型实例时，使用`.values()`或`.values_list()`**。
6. **处理大量数据时，使用`iterator(chunk_size=2000)`** —— 减少内存消耗。
7. **使用`django-silk`或`django-debug-toolbar`进行性能分析** —— 不要猜测代码的性能表现。
8. **对于大型数据列表，使用`Exists()`子查询代替`__in`操作符**。

---

## 第3阶段：Django REST框架（DRF）

### 序列化器设计模式

```python
# apps/orders/serializers.py
from rest_framework import serializers

class OrderListSerializer(serializers.ModelSerializer):
    """Lightweight for list views — minimal fields."""
    customer_name = serializers.CharField(source="customer.name", read_only=True)
    
    class Meta:
        model = Order
        fields = ["id", "customer_name", "status", "amount", "created_at"]
        read_only_fields = ["id", "created_at"]

class OrderDetailSerializer(serializers.ModelSerializer):
    """Full detail with nested items."""
    items = OrderItemSerializer(many=True, read_only=True)
    customer = CustomerSerializer(read_only=True)
    
    class Meta:
        model = Order
        fields = "__all__"

class OrderCreateSerializer(serializers.Serializer):
    """Explicit create — don't use ModelSerializer for writes."""
    customer_id = serializers.UUIDField()
    items = OrderItemInputSerializer(many=True)
    notes = serializers.CharField(required=False, allow_blank=True)
    
    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("At least one item required.")
        return value
    
    def create(self, validated_data):
        # Delegate to service layer
        from apps.orders.services import create_order
        return create_order(**validated_data)
```

### 服务层设计模式

```python
# apps/orders/services.py
from django.db import transaction
from django.core.exceptions import ValidationError

def create_order(*, customer_id: str, items: list[dict], notes: str = "") -> Order:
    """
    Create order with items atomically.
    
    Raises:
        ValidationError: If customer not found or insufficient stock.
    """
    customer = Customer.objects.filter(id=customer_id).first()
    if not customer:
        raise ValidationError("Customer not found.")
    
    with transaction.atomic():
        order = Order.objects.create(customer=customer, notes=notes)
        
        order_items = []
        for item_data in items:
            product = Product.objects.select_for_update().get(id=item_data["product_id"])
            if product.stock < item_data["quantity"]:
                raise ValidationError(f"Insufficient stock for {product.name}")
            
            product.stock -= item_data["quantity"]
            product.save(update_fields=["stock"])
            
            order_items.append(
                OrderItem(order=order, product=product, quantity=item_data["quantity"], unit_price=product.price)
            )
        
        OrderItem.objects.bulk_create(order_items)
        order.amount = sum(i.unit_price * i.quantity for i in order_items)
        order.save(update_fields=["amount"])
    
    # Side effects OUTSIDE transaction
    send_order_confirmation.delay(order.id)
    return order
```

### ViewSet最佳实践

```python
# apps/orders/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Always scope to current user. Never return all objects."""
        return (
            Order.objects
            .filter(customer__user=self.request.user)
            .select_related("customer")
            .prefetch_related("items__product")
        )
    
    def get_serializer_class(self):
        """Different serializers for different actions."""
        if self.action == "list":
            return OrderListSerializer
        if self.action in ("create",):
            return OrderCreateSerializer
        return OrderDetailSerializer
    
    def perform_create(self, serializer):
        serializer.save()
    
    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        order = self.get_object()
        from apps.orders.services import cancel_order
        try:
            cancel_order(order=order, cancelled_by=request.user)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": "cancelled"})
    
    @action(detail=False, methods=["get"])
    def summary(self, request):
        from apps.orders.selectors import get_order_summary
        data = get_order_summary(user=request.user)
        return Response(data)
```

### 分页功能

```python
# apps/core/pagination.py
from rest_framework.pagination import CursorPagination

class StandardCursorPagination(CursorPagination):
    """Cursor pagination — O(1) performance regardless of offset."""
    page_size = 25
    page_size_query_param = "page_size"
    max_page_size = 100
    ordering = "-created_at"

# settings/base.py
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "apps.core.pagination.StandardCursorPagination",
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {"anon": "100/hour", "user": "1000/hour"},
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "EXCEPTION_HANDLER": "apps.core.exceptions.custom_exception_handler",
}
```

---

## 第4阶段：认证与安全

### JWT认证（简单JWT实现）

```python
# config/settings/base.py
from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# Custom user model
# apps/users/models.py
from django.contrib.auth.models import AbstractUser
from apps.users.managers import UserManager

class User(AbstractUser):
    username = None  # Remove username field
    email = models.EmailField(unique=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    objects = UserManager()
```

### 生产环境下的安全设置

```python
# config/settings/production.py
import os

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
DEBUG = False
ALLOWED_HOSTS = os.environ["ALLOWED_HOSTS"].split(",")

# HTTPS
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Content security
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"

# CORS (django-cors-headers)
CORS_ALLOWED_ORIGINS = os.environ.get("CORS_ORIGINS", "").split(",")
CORS_ALLOW_CREDENTIALS = True

# CSP (django-csp)
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'",)
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")
CSP_IMG_SRC = ("'self'", "data:", "https:")
```

### 权限管理

```python
# apps/core/permissions.py
from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """Object-level: only the owner can access."""
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True
        return request.user.is_staff

class HasRole(BasePermission):
    """Role-based access control."""
    required_role = None
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.roles.filter(name=self.required_role).exists()

class IsManager(HasRole):
    required_role = "manager"
```

### 10项安全检查清单

| 序号 | 检查项 | 检查方法 | 优先级 |
|---|---|-----|----------|
| 1 | `manage.py check --deploy`检查 | 所有警告都应解决 | P0 |
| 2 | 秘密密钥来自环境变量或安全存储库 | 不要硬编码在源代码中 | P0 |
| 3 | 生产环境中`DEBUG`设置为`False` | 根据环境配置 | P0 |
| 4 | 强制使用HTTPS | 设置`SECURE_SSL_REDIRECT` | P0 |
| 5 | 启用CSRF保护 | 默认设置，切勿禁用 | P0 |
| 6 | 防止SQL注入 | 使用ORM，避免使用f-string直接操作数据库 | P0 |
| 7 | 输入验证 | 所有输入都需通过序列化器进行验证 | P1 |
| 8 | 实施速率限制 | 配置DRF的速率限制机制 | P1 |
| 9 | 更改管理员URL | 不要使用`/admin/`，使用随机路径 | P1 |
| 10 | 依赖项审计 | 使用`pip-audit`或CI工具进行安全检查 | P1 |

---

## 第5阶段：迁移与数据库管理

### 迁移安全规则

1. **在生产环境中应用迁移后，切勿修改迁移文件** —— 应创建新的迁移文件。
2. **务必审查自动生成的迁移脚本** —— `makemigrations`可能会产生破坏性变更。
3. **先添加可为空的列** —— 先添加列，部署后设置`null=True`，之后再将其设置为非空。
4. **切勿直接重命名列** —— 先添加新列，迁移数据，再删除旧列（分三次部署）。
5. **使用`RunPython`命令时指定`reverse_code`参数** —— 确保迁移操作可逆。
6. **定期合并迁移文件** —— 使用`squashmigrations app_name 0001 0050`命令压缩迁移文件以提高性能。
7. **注意数据库锁定** —— 在Postgres 11以下版本中，`ALTER TABLE ADD COLUMN NOT NULL DEFAULT`操作会锁定数据库。

### 零停机时间迁移策略

```python
# Step 1: Add nullable column (safe, no lock)
# migrations/0042_add_new_field.py
class Migration(migrations.Migration):
    operations = [
        migrations.AddField(
            model_name="order",
            name="tracking_number",
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]

# Step 2: Backfill data (separate migration)
# migrations/0043_backfill_tracking.py
def backfill_tracking(apps, schema_editor):
    Order = apps.get_model("orders", "Order")
    batch_size = 1000
    while True:
        ids = list(
            Order.objects.filter(tracking_number__isnull=True)
            .values_list("id", flat=True)[:batch_size]
        )
        if not ids:
            break
        Order.objects.filter(id__in=ids).update(tracking_number="LEGACY")

class Migration(migrations.Migration):
    operations = [
        migrations.RunPython(backfill_tracking, migrations.RunPython.noop),
    ]

# Step 3: Make non-null (after backfill verified)
# migrations/0044_tracking_not_null.py
```

### 迁移冲突解决

```bash
# When two developers create migrations from same parent:
python manage.py makemigrations --merge  # Creates merge migration

# To detect conflicts in CI:
python manage.py makemigrations --check --dry-run
```

---

## 第6阶段：缓存策略

### 缓存层次结构

```python
# config/settings/base.py
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get("REDIS_URL", "redis://localhost:6379/0"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "SERIALIZER": "django_redis.serializers.json.JSONSerializer",
        },
        "KEY_PREFIX": "myapp",
        "TIMEOUT": 300,  # 5 min default
    }
}

# Session storage in Redis (faster than DB)
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
```

### 缓存使用模式

```python
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

# View-level caching
@cache_page(60 * 15)  # 15 minutes
def product_list(request):
    ...

# Manual cache with invalidation
def get_product_stats(product_id: str) -> dict:
    cache_key = f"product_stats:{product_id}"
    stats = cache.get(cache_key)
    if stats is None:
        stats = _compute_product_stats(product_id)
        cache.set(cache_key, stats, timeout=600)
    return stats

def invalidate_product_cache(product_id: str):
    cache.delete(f"product_stats:{product_id}")

# Signal-based cache invalidation
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

@receiver([post_save, post_delete], sender=Product)
def clear_product_cache(sender, instance, **kwargs):
    invalidate_product_cache(str(instance.id))
    cache.delete("product_list")

# Template fragment caching
# {% load cache %}
# {% cache 600 sidebar request.user.id %}
#   ... expensive template fragment ...
# {% endcache %}
```

### 缓存决策指南

| 数据类型 | 缓存策略 | 缓存有效期 | 验证时机 |
|---|---|---|---|
| 用户会话 | 使用Redis作为缓存后端 | 2周 | 用户登出时清除 |
| API列表 | 使用`cache_page` | 5分钟 | 基于时间触发 |
| 计算结果 | 手动设置缓存 | 10-30分钟 | 数据更新时触发 |
| 用户个性化数据 | 使用用户ID进行缓存 | 5分钟 | 用户操作时触发 |
| 静态配置文件 | 手动设置缓存 | 1小时 | 管理员修改配置时触发 |
| 全页面内容（匿名用户） | 使用Nginx或CDN | 1-60分钟 | 根据需要清除 |

---

## 第7阶段：后台任务（Celery）

### Celery配置

```python
# config/celery.py
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
app = Celery("myapp")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

# config/settings/base.py
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/1")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/2")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 300  # 5 min hard limit
CELERY_TASK_SOFT_TIME_LIMIT = 240  # 4 min soft limit
CELERY_TASK_ACKS_LATE = True  # Re-deliver if worker crashes
CELERY_WORKER_PREFETCH_MULTIPLIER = 1  # Fair scheduling
```

### 任务设计模式

```python
# apps/orders/tasks.py
from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    autoretry_for=(ConnectionError, TimeoutError),
    retry_backoff=True,
    retry_backoff_max=600,
    acks_late=True,
)
def send_order_confirmation(self, order_id: str):
    """Send confirmation email with exponential backoff retry."""
    try:
        order = Order.objects.select_related("customer__user").get(id=order_id)
        send_email(
            to=order.customer.user.email,
            template="order_confirmation",
            context={"order": order},
        )
        logger.info("Confirmation sent", extra={"order_id": order_id})
    except Order.DoesNotExist:
        logger.error("Order not found", extra={"order_id": order_id})
        # Don't retry — order doesn't exist

@shared_task
def generate_daily_report():
    """Periodic task — scheduled via beat."""
    from apps.reports.services import build_daily_report
    report = build_daily_report()
    notify_admins(report)

# Celery Beat schedule
CELERY_BEAT_SCHEDULE = {
    "daily-report": {
        "task": "apps.orders.tasks.generate_daily_report",
        "schedule": crontab(hour=6, minute=0),
    },
    "cleanup-expired-sessions": {
        "task": "apps.users.tasks.cleanup_sessions",
        "schedule": crontab(hour=3, minute=0),
    },
}
```

### 6条Celery使用规则

1. **始终传递ID而不是对象** —— 使用`task.delay(order.id)`而不是`task.delay(order)`，因为对象可能无法正确序列化且可能已过期。
2. **为每个任务设置时间限制** —— 避免任务重复执行。
3. **确保任务具有幂等性** —— 对于可能重复执行的任务，使用`autoretry_for`进行重试。
4. **区分不同类型的任务队列** —— 重要任务（如支付处理）使用单独的队列，批量任务（如邮件发送）使用另一个队列。
5. **使用Flower工具监控任务执行情况** —— 通过`celery -A config flower`实时监控任务状态。

---

## 第8阶段：测试策略

### 测试层次结构

| 测试类型 | 工具 | 测试目标 | 测试速度 |
|---|---|---|---|
| 单元测试 | pytest | 服务层、工具类、模型 | 每个测试用时<1秒 |
| 集成测试 | pytest + Django测试客户端 | 视图、序列化器、数据库 | 每个测试用时<5秒 |
| 终端到端测试 | Playwright/Selenium | 完整的用户流程 | 每个测试用时<30秒 |
| 合规性测试 | schemathesis/dredd | 检查API接口是否符合规范 | 每个测试用时<10秒 |

### 7条测试规则

1. **使用`pytest-django`进行测试** —— 不要使用Django自带的`TestCase`，它更快且更易于使用。
2. **使用工厂模式** —— 使用`factory_boy`或自定义测试工厂。避免手动填充测试数据库。
3. **测试业务逻辑** —— 业务逻辑应在服务层中实现，便于独立测试。
4. **使用`@pytest.mark.django_db`标记需要数据库的测试 | 只有需要数据库操作的测试才使用该标记。
5. **使用`freezegun`模拟时间依赖逻辑 | 对于时间相关的逻辑，使用`freezegun`工具。
6. **模拟外部服务** —— 使用`responses`模拟HTTP响应，`unittest.mock`模拟其他外部服务。
7. **持续集成（CI）执行`pytest --cov --cov-fail-under=80` | 确保代码覆盖率达到最低要求。

---

## 第9阶段：性能与监控

### Gunicorn配置

```python
# config/gunicorn.conf.py
import multiprocessing

bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "gthread"  # or "uvicorn.workers.UvicornWorker" for async
threads = 4
max_requests = 1000
max_requests_jitter = 50
timeout = 30
graceful_timeout = 30
keepalive = 5
accesslog = "-"
errorlog = "-"
loglevel = "info"
```

### Django中间件顺序（影响性能）

```python
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",     # Static files (before everything)
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",           # CORS (before CommonMiddleware)
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "apps.core.middleware.RequestIDMiddleware",         # Custom: attach request ID
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
```

### 结构化日志记录

```python
# config/settings/base.py
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(name)s %(levelname)s %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json",
        },
    },
    "root": {"handlers": ["console"], "level": "INFO"},
    "loggers": {
        "django.db.backends": {"level": "WARNING"},  # Quiet SQL logs
        "apps": {"level": "INFO", "propagate": True},
    },
}
```

### 性能指标与目标

| 指标 | 目标值 | 监测方法 |
|---|---|---|
| p50响应时间 | <100毫秒 | 使用`django-silk`或APM工具 |
| p99响应时间 | <500毫秒 | 使用APM（如Sentry、Datadog） |
| 每个请求的数据库查询次数 | <10次 | 使用`django-debug-toolbar` |
| 每个工作进程的内存使用量 | <256MB | 使用Gunicorn和监控工具 |
| Celery任务执行延迟 | <5秒 | 使用Flower或Prometheus工具 |

## 第10阶段：部署

### 生产环境Dockerfile

```dockerfile
# Multi-stage build
FROM python:3.12-slim AS builder
RUN pip install --no-cache-dir uv
WORKDIR /app
COPY requirements/production.txt .
RUN uv pip install --system --no-cache -r production.txt

FROM python:3.12-slim
RUN adduser --disabled-password --no-create-home app
WORKDIR /app

COPY --from=builder /usr/local/lib/python3.12 /usr/local/lib/python3.12
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . .

RUN python manage.py collectstatic --noinput
USER app
EXPOSE 8000
CMD ["gunicorn", "config.wsgi:application", "-c", "config/gunicorn.conf.py"]
```

### GitHub Actions与持续集成/持续部署（CI/CD）

```yaml
name: CI
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_DB: test_db
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
        ports: ["5432:5432"]
      redis:
        image: redis:7
        ports: ["6379:6379"]
    
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: pip install -r requirements/local.txt
      - run: python manage.py check --deploy
        env:
          DJANGO_SETTINGS_MODULE: config.settings.local
      - run: python manage.py makemigrations --check --dry-run
      - run: pytest --cov --cov-fail-under=80 -n auto
        env:
          DATABASE_URL: postgres://test:test@localhost:5432/test_db
          REDIS_URL: redis://localhost:6379/0
      - run: ruff check .
      - run: ruff format --check .
      - run: mypy apps/
```

### 生产环境部署前必检项

**P0级要求：**
- `manage.py check --deploy`检查通过，且无警告 |
- `SECRET_KEY`来自环境变量 |
- `DEBUG`设置为`False` |
- `ALLOWED_HOSTS`配置正确 |
- 强制使用HTTPS |
- 配置了数据库连接池 |
- 静态文件通过WhiteNoise或CDN服务提供 |
- 配置了错误跟踪系统（如Sentry） |
- 定期执行数据备份

**P1级要求（应在第一周内完成）：**
- 所有接口都实施了速率限制 |
- 管理员URL已更改（非`/admin/`） |
- 配置了缓存后端（如Redis） |
- 使用Celery处理后台任务 |
- 实现了结构化日志记录 |
- 配置了持续集成/持续部署流程 |
- 配置了健康检查接口 |
- 在CI过程中执行`pip-audit`安全审计。

---

## 其他常见实践与库

### 软删除机制

```python
class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class Order(SoftDeleteModel):
    objects = ActiveManager()      # Default: excludes deleted
    all_objects = models.Manager() # Include deleted
```

### 多租户架构设计

```python
# Middleware: set tenant from request
class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        tenant_id = request.headers.get("X-Tenant-ID")
        if tenant_id:
            request.tenant = Tenant.objects.get(id=tenant_id)
        return self.get_response(request)

# Auto-filter all queries by tenant
class TenantManager(models.Manager):
    def get_queryset(self):
        from threading import local
        _thread_local = local()
        qs = super().get_queryset()
        tenant = getattr(_thread_local, "tenant", None)
        if tenant:
            qs = qs.filter(tenant=tenant)
        return qs
```

### Webhook处理机制

```python
import hashlib, hmac
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

@csrf_exempt
@require_POST
def stripe_webhook(request):
    payload = request.body
    sig = request.headers.get("Stripe-Signature")
    
    try:
        event = stripe.Webhook.construct_event(payload, sig, settings.STRIPE_WEBHOOK_SECRET)
    except (ValueError, stripe.error.SignatureVerificationError):
        return JsonResponse({"error": "Invalid signature"}, status=400)
    
    handlers = {
        "checkout.session.completed": handle_checkout,
        "invoice.paid": handle_invoice_paid,
        "customer.subscription.deleted": handle_cancellation,
    }
    
    handler = handlers.get(event["type"])
    if handler:
        handler(event["data"]["object"])
    
    return JsonResponse({"status": "ok"})
```

---

## Django 5.x的新特性

### Django 5.0及更高版本中的`GeneratedField`功能

```python
class Product(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    tax_rate = models.DecimalField(max_digits=4, decimal_places=2, default=0.20)
    
    total_price = models.GeneratedField(
        expression=F("price") * (1 + F("tax_rate")),
        output_field=models.DecimalField(max_digits=10, decimal_places=2),
        db_persist=True,  # Stored column, not virtual
    )
```

### 表单中的字段分组功能（Django 5.0及更高版本）

```python
class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    
    # Template: {{ form.as_field_group }}
```

### 数据库计算属性（Django 5.0及更高版本）

```python
from django.db.models.functions import Now

class Event(models.Model):
    starts_at = models.DateTimeField(db_default=Now())
```

---

## 10个常见错误及解决方法

| 错误 | 解决方法 |
|---|---------|-----|
| 1 | 未使用自定义用户模型 | 从项目开始就使用`AbstractUser`模型 |
| 2 | 每处都使用N+1查询 | 使用`select_related`或`prefetch_related` |
| 3 | 业务逻辑写在视图函数中 | 将业务逻辑移至`services.py` |
| 4 | 所有配置文件集中在一个文件中 | 将配置文件分为`base.py`、`local.py`、`production.py` |
| 5 | 不审查迁移脚本 | 必须阅读自动生成的迁移脚本 |
| 6 | 生产环境中`DEBUG`设置为`True` | 根据环境配置，切勿条件化设置 |
| 7 | 同步发送邮件 | 使用Celery任务处理邮件发送 |
| 8 | 未使用连接池 | 使用pgbouncer或django-db-conn-pool |
| 9 | 使用f-string直接操作数据库 | 仅使用ORM或参数化查询 |
| 10 | 未设置请求超时 | 为Gunicorn和数据库设置合适的超时参数 |

---

## 质量评估标准（0-100分）

| 评估维度 | 权重 | 评估标准 |
|---|---|---|
| 架构设计 | 15% | 设置文件分离、服务层设计、应用结构 |
| ORM使用 | 15% | 避免N+1查询、使用批量操作、正确设置索引 |
| 安全性 | 15% | 安全检查、HTTPS、认证机制、CSRF保护 |
| 测试 | 15% | 代码覆盖率超过80%，使用pytest和工厂模式 |
| 性能 | 10% | 有效使用缓存、连接池、合理设计查询 |
| 错误处理 | 10% | 有完善的错误处理机制、日志记录系统 |
| 迁移管理 | 10% | 迁移操作可逆、无停机时间、定期审查 |
| 部署流程 | 10% | 使用Docker、持续集成/持续部署流程、定期进行健康检查 |

**90-100分**：达到生产级标准，适合企业级应用 |
**70-89分**：功能基本完善，但需要进一步优化 |
**50-69分**：功能可用，但在扩展时存在风险 |
**低于50分**：存在严重的技术问题，需要立即修复基础架构 |

## Django生产环境的10条准则

1. 从第一次创建迁移文件时就开始使用自定义用户模型。
2. 始终分离业务逻辑和服务层。
3. 对所有涉及关联关系的查询都使用`select_related`或`prefetch_related`。
4. 按环境分隔设置文件，避免使用`if DEBUG`条件判断。
5. 每个迁移脚本在合并前都应由人工审核。
6. 对耗时超过200毫秒的任务使用Celery处理。
7. 在持续集成过程中执行`manage.py check --deploy`检查，确保无警告。
8. 必须使用连接池。
9. 测试业务逻辑，而非具体的实现细节。
10. 如果某个功能不在`requirements.txt`中，那么它就不存在。

---

## 常用命令

- “检查这个Django项目” → 执行快速健康检查，得分评估。
- “优化这些查询” → 应用N+1查询优化策略，建议设置合适的索引。
- “为这个模型设置DRF接口” → 生成序列化器、视图、URL和测试用例。
- “为某个功能添加Celery任务” → 为任务设置重试机制、时间限制和幂等性。
- “审查这个迁移脚本” → 检查安全规则，确保无停机风险。
- “设置认证机制” → 实现JWT认证、自定义用户模型和权限管理。
- “执行全面的安全检查” —— 完成所有P0级和P1级检查。
- “为某个功能配置缓存” —— 根据缓存策略选择合适的缓存方式。
- “设置持续集成/持续部署流程” —— 使用GitHub Actions、pytest等工具。
- “为某个功能创建服务” —— 设计服务层并实现数据验证和事务处理。
- “配置日志系统” —— 使用结构化日志格式和请求ID处理。
- “部署这个Django应用” —— 使用Dockerfile、Gunicorn和完整部署流程。