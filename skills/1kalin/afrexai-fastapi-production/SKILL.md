# FastAPI 生产工程

这是一套完整的开发方法论，用于构建、部署和扩展 FastAPI 应用程序。这并非教程，而是一套适用于生产环境的最佳实践。

## 快速健康检查 (/16)

每个项目项需得 2 分。总分低于 8 分表示存在严重问题。

| 项目项 | 健康状态 | 不健康状态 |
|--------|---------|-----------|
| 类型安全 | 所有地方都使用 Pydantic v2 模型 | 使用 `dict` 返回数据，且没有数据验证 |
| 错误处理 | 有结构化的错误层次结构 | 仅使用简单的 `HTTPException` 异常 |
| 身份验证 | 使用 JWT 和依赖注入 | 手动解析令牌 |
| 测试 | 覆盖率超过 80%，包含异步测试 | 没有测试或仅进行同步测试 |
| 数据库 | 使用异步 ORM 和迁移 | 使用原始 SQL，没有数据库迁移 |
| 可观测性 | 有结构化的日志记录和跟踪功能 | 使用 `print()` 进行调试 |
| 部署 | 多阶段 Docker 部署，包含健康检查 | 在裸机上使用 `uvicorn main:app` 启动应用 |
| 文档 | 自动生成的、准确的 OpenAPI 文档 | 默认的 `/docs` 页面未进行任何修改 |

## 第 1 阶段：项目架构

### 推荐的结构

```
src/
├── app/
│   ├── __init__.py
│   ├── main.py              # App factory
│   ├── config.py             # Pydantic Settings
│   ├── dependencies.py       # Shared DI
│   ├── middleware.py          # Custom middleware
│   ├── features/
│   │   ├── users/
│   │   │   ├── __init__.py
│   │   │   ├── router.py     # Endpoints
│   │   │   ├── schemas.py    # Pydantic models
│   │   │   ├── service.py    # Business logic
│   │   │   ├── repository.py # Data access
│   │   │   ├── models.py     # SQLAlchemy/SQLModel
│   │   │   ├── dependencies.py
│   │   │   └── exceptions.py
│   │   ├── auth/
│   │   ├── orders/
│   │   └── ...
│   ├── core/
│   │   ├── database.py       # Engine, session factory
│   │   ├── security.py       # JWT, hashing
│   │   ├── errors.py         # Error hierarchy
│   │   └── logging.py        # Structlog config
│   └── shared/
│       ├── pagination.py
│       ├── filters.py
│       └── responses.py
├── migrations/               # Alembic
├── tests/
│   ├── conftest.py
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── pyproject.toml
├── Dockerfile
└── docker-compose.yml
```

### 7 条架构规则

1. **基于功能的模块** — 按领域分组，而不是按层次结构分组
2. **路由器 → 服务 → 数据库** — 严格遵守层次结构，不得跳过任何环节
3. **处处使用依赖注入** — 使用 `Depends()` 以确保可测试性
4. **在接口边界使用 Pydantic 模型** — 对所有输入和输出数据进行验证
5. **路由器中不包含业务逻辑** — 路由器应保持简洁，服务层负责处理业务逻辑
6. **通过环境变量配置** — 使用支持 `.env` 文件的 Pydantic 设置
7. **默认使用异步编程** — 对所有 I/O 操作使用异步函数

### 框架选择背景

```yaml
# When to choose FastAPI over alternatives
fastapi_is_best_when:
  - "You need auto-generated OpenAPI docs"
  - "Team knows Python type hints"
  - "API-first (no server-rendered HTML as primary)"
  - "High concurrency with async I/O"
  - "Microservice or API gateway"

consider_alternatives:
  django: "Full-featured web app with admin, ORM, auth batteries"
  flask: "Simple app, team prefers explicit over magic"
  litestar: "Need WebSocket-heavy or more opinionated framework"
  hono_or_express: "Team prefers TypeScript"
```

## 第 2 阶段：配置与环境

### Pydantic 设置模式

```python
from pydantic_settings import BaseSettings
from pydantic import SecretStr, field_validator
from functools import lru_cache

class Settings(BaseSettings):
    # App
    app_name: str = "MyAPI"
    debug: bool = False
    environment: str = "production"  # development | staging | production
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 4
    
    # Database
    database_url: SecretStr  # Required — no default
    db_pool_size: int = 20
    db_max_overflow: int = 10
    db_pool_timeout: int = 30
    
    # Auth
    jwt_secret: SecretStr  # Required
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 30
    
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    
    # CORS
    cors_origins: list[str] = ["http://localhost:3000"]
    
    @field_validator("environment")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        allowed = {"development", "staging", "production"}
        if v not in allowed:
            raise ValueError(f"environment must be one of {allowed}")
        return v
    
    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

@lru_cache
def get_settings() -> Settings:
    return Settings()
```

### 5 条配置规则

1. **永远不要硬编码敏感信息** — 对敏感值使用 `SecretStr`
2. **快速失败** — 必需的字段必须有默认值；缺少这些字段时应用无法启动
3. **在启动时进行验证** — 使用 `@field_validator` 进行约束检查
4. **缓存配置** — 使用 `@lru_cache` 确保配置只被解析一次
5. **所有数据都指定类型** — 结构化数据不要使用 `str` 类型；应使用枚举或字面量类型

## 第 3 阶段：精通 Pydantic v2

### 模式设计规则

```python
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from uuid import UUID

# Base with common config
class AppSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,      # ORM mode
        str_strip_whitespace=True,  # Auto-strip
        validate_default=True,      # Validate defaults too
    )

# Input schemas (what the API accepts)
class UserCreate(AppSchema):
    email: str = Field(..., pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    name: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=8, max_length=128)

class UserUpdate(AppSchema):
    name: str | None = Field(None, min_length=1, max_length=100)
    email: str | None = Field(None, pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")

# Output schemas (what the API returns)
class UserResponse(AppSchema):
    id: UUID
    email: str
    name: str
    created_at: datetime
    # Note: password is NEVER in response schema

# List response with pagination
class PaginatedResponse[T](AppSchema):
    items: list[T]
    total: int
    page: int
    page_size: int
    has_next: bool
```

### 8 条 Pydantic 规则

1. **分离创建/更新/响应的schema** — 不要重复使用输入数据作为输出
2. **不要在响应中暴露内部字段** — 响应中不应包含密码、内部 ID 或调试信息
3. **使用 `Field()` 进行约束** — 为字段设置最小/最大长度、正则表达式等限制
4. **启用 `from_attributes=True`** — 以便 ORM 可以正确转换模型
5. **使用泛型包装器** — 如 `PaginatedResponse[T]`, `ApiResponse[T]`
6. **在接口边界进行验证** — 验证请求体、查询参数和路径参数
7. **使用计算字段** — 使用 `@computed_field` 生成派生字段
8. **用示例进行文档说明** — 例如：`model_config = {"json_schema_extra": {"examples": [...]}`

## 第 4 阶段：错误处理架构

### 有结构化的错误层次结构

```python
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.status import (
    HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT, HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_429_TOO_MANY_REQUESTS, HTTP_500_INTERNAL_SERVER_ERROR,
)

class AppError(Exception):
    """Base application error."""
    def __init__(
        self,
        message: str,
        code: str,
        status_code: int = HTTP_500_INTERNAL_SERVER_ERROR,
        details: dict | None = None,
    ):
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)

class NotFoundError(AppError):
    def __init__(self, resource: str, identifier: str | int):
        super().__init__(
            message=f"{resource} not found: {identifier}",
            code="NOT_FOUND",
            status_code=HTTP_404_NOT_FOUND,
            details={"resource": resource, "identifier": str(identifier)},
        )

class ConflictError(AppError):
    def __init__(self, message: str, field: str | None = None):
        super().__init__(
            message=message, code="CONFLICT",
            status_code=HTTP_409_CONFLICT,
            details={"field": field} if field else {},
        )

class AuthenticationError(AppError):
    def __init__(self, message: str = "Invalid credentials"):
        super().__init__(message=message, code="UNAUTHORIZED", status_code=HTTP_401_UNAUTHORIZED)

class AuthorizationError(AppError):
    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(message=message, code="FORBIDDEN", status_code=HTTP_403_FORBIDDEN)

class ValidationError(AppError):
    def __init__(self, message: str, errors: list[dict] | None = None):
        super().__init__(
            message=message, code="VALIDATION_ERROR",
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            details={"errors": errors or []},
        )

class RateLimitError(AppError):
    def __init__(self, retry_after: int = 60):
        super().__init__(
            message="Rate limit exceeded", code="RATE_LIMITED",
            status_code=HTTP_429_TOO_MANY_REQUESTS,
            details={"retry_after": retry_after},
        )

# Global error handler
async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details,
            }
        },
    )

# Register in app factory
# app.add_exception_handler(AppError, app_error_handler)
```

### 6 条错误处理规则

1. **永远不要返回简单的字符串** — 必须返回格式为 `{"error": {"code", "message", "details"}} 的错误信息
2. **使用特定于领域的错误类型** — 例如：`NotFoundError("User", user_id)` 而不是 `HTTPException(404)`
3. **全局错误处理器捕获所有错误** — 在应用工厂中注册 `AppError` 处理器
4. **记录服务器错误，但不要暴露细节** — 5xx 状态码返回通用错误信息，并记录完整的错误堆栈
5. **提供可操作的错误细节** — 显示哪个字段出了问题、允许什么操作、以及是否需要重试
6. **不要泄露内部信息** — 响应中不应包含堆栈跟踪、SQL 查询或文件路径

## 第 5 阶段：身份验证与授权

### JWT + 依赖注入模式

```python
from fastapi import Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

security = HTTPBearer()

def create_access_token(user_id: str, roles: list[str], settings: Settings) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expire_minutes)
    payload = {
        "sub": user_id,
        "roles": roles,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, settings.jwt_secret.get_secret_value(), algorithm=settings.jwt_algorithm)

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security),
    settings: Settings = Depends(get_settings),
    db: AsyncSession = Depends(get_db),
) -> User:
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.jwt_secret.get_secret_value(),
            algorithms=[settings.jwt_algorithm],
        )
        user_id = payload.get("sub")
        if not user_id:
            raise AuthenticationError("Invalid token payload")
    except JWTError:
        raise AuthenticationError("Invalid or expired token")
    
    user = await db.get(User, user_id)
    if not user:
        raise AuthenticationError("User not found")
    return user

# Role-based authorization
def require_role(*roles: str):
    async def checker(user: User = Depends(get_current_user)) -> User:
        if not any(r in user.roles for r in roles):
            raise AuthorizationError(f"Requires one of: {', '.join(roles)}")
        return user
    return checker

# Usage in router
@router.get("/admin/users")
async def list_users(
    admin: User = Depends(require_role("admin", "superadmin")),
    service: UserService = Depends(get_user_service),
):
    return await service.list_all()
```

### 10 条安全检查项

| 序号 | 检查项 | 优先级 |
|---|-------|----------|
| 1 | JWT 密钥长度至少为 256 位，并从环境变量中获取 | P0 |
| 2 | 令牌过期时间：访问时不超过 30 分钟，刷新时不超过 7 天 | P0 |
| 3 | 密码使用 bcrypt/argon2 进行哈希处理 | P0 |
| 4 | 根据环境配置 CORS | P0 |
| 5 | 对身份验证端点实施速率限制 | P0 |
| 6 | 强制使用 HTTPS（并重定向到 HTTPS） | P0 |
| 7 | 设置安全头部（HSTS, CSP, X-Frame-Security） | P1 |
| 8 | 所有端点都进行输入验证 | P1 |
| 9 | 防止 SQL 注入（使用参数化查询） | P0 |
| 10 | 扫描依赖项的安全性（使用 pip-audit） | P1 |

## 第 6 阶段：数据库模式

### 异步 SQLAlchemy + 数据库模式

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import select, func
from uuid import uuid4, UUID
from datetime import datetime, timezone

# Engine setup
engine = create_async_engine(
    settings.database_url.get_secret_value(),
    pool_size=settings.db_pool_size,
    max_overflow=settings.db_max_overflow,
    pool_timeout=settings.db_pool_timeout,
    pool_pre_ping=True,  # Check connection health
    echo=settings.debug,
)

SessionFactory = async_sessionmaker(engine, expire_on_commit=False)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionFactory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

# Base model with common fields
class Base(DeclarativeBase):
    pass

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

# Repository pattern
class BaseRepository[T]:
    def __init__(self, session: AsyncSession, model: type[T]):
        self.session = session
        self.model = model
    
    async def get_by_id(self, id: UUID) -> T | None:
        return await self.session.get(self.model, id)
    
    async def get_or_raise(self, id: UUID) -> T:
        entity = await self.get_by_id(id)
        if not entity:
            raise NotFoundError(self.model.__name__, str(id))
        return entity
    
    async def list(
        self, *, offset: int = 0, limit: int = 20, **filters
    ) -> tuple[list[T], int]:
        query = select(self.model)
        count_query = select(func.count()).select_from(self.model)
        
        for field, value in filters.items():
            if value is not None:
                query = query.where(getattr(self.model, field) == value)
                count_query = count_query.where(getattr(self.model, field) == value)
        
        total = await self.session.scalar(count_query) or 0
        result = await self.session.execute(
            query.offset(offset).limit(limit).order_by(self.model.created_at.desc())
        )
        return list(result.scalars().all()), total
    
    async def create(self, entity: T) -> T:
        self.session.add(entity)
        await self.session.flush()
        return entity
    
    async def delete(self, entity: T) -> None:
        await self.session.delete(entity)
```

### ORM 选择指南

| ORM | 适用场景 | 是否支持异步 | 类型安全性 | 学习难度 |
|-----|----------|-------|-------------|----------------|
| **SQLAlchemy 2.0** | 复杂查询，企业级应用 | ✅ | ✅ | 需要手动映射数据库结构 | 中等难度 |
| **SQLModel** | 简单的 CRUD 操作，适用于同步场景 | ✅ | ✅ | 易于学习 | 低难度 |
| **Tortoise** | 提供类似 Django 的开发体验 | ✅ | 部分支持异步 | 低难度 |
| **Piccolo** | 现代设计，内置迁移功能 | ✅ | ✅ | 低难度 |

**建议：** 生产环境推荐使用 SQLAlchemy 2.0；原型开发可以使用 SQLModel。

### 迁移策略（使用 Alembic）

```bash
# Setup
alembic init migrations
# Edit alembic.ini: sqlalchemy.url = from env

# Generate migration
alembic revision --autogenerate -m "add users table"

# Apply
alembic upgrade head

# Rollback
alembic downgrade -1
```

**迁移规则：**
1. 在应用部署前务必审查自动生成的迁移脚本
2. 不要修改已应用的迁移脚本；如有需要请创建新的迁移文件
3. 在生产环境之前先在测试环境中测试迁移脚本
4. 每个 `upgrade()` 操作都应包含 `downgrade()` 方法
5. 为了兼容 SQLite，使用 `batch_alter_table` 方法

## 第 7 阶段：测试策略

### 测试层次结构

| 测试层次 | 目标覆盖范围 | 使用工具 | 测试重点 |
|-------|----------------|-------|-------|
| 单元测试 | 覆盖 80% 以上的代码 | pytest, unittest.mock | 服务逻辑和数据验证 |
| 集成测试 | 关键业务路径 | pytest-asyncio, testcontainers | 数据库查询和外部 API 的交互 |
| 端到端测试 | 关键业务流程 | httpx.AsyncClient | 完整的请求-响应流程 |
| 合同测试 | API 接口边界 | schemathesis | 确保 API 符合 OpenAPI 标准 |

### 测试模式

```python
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import create_app

@pytest.fixture
async def app():
    app = create_app()
    yield app

@pytest.fixture
async def client(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

@pytest.fixture
async def auth_client(client, test_user):
    token = create_access_token(test_user.id, test_user.roles)
    client.headers["Authorization"] = f"Bearer {token}"
    return client

# E2E test
@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    response = await client.post("/api/users", json={
        "email": "test@example.com",
        "name": "Test User",
        "password": "securepass123",
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "password" not in data  # Never expose

# Unit test (service layer)
@pytest.mark.asyncio
async def test_user_service_duplicate_email(user_service, mock_repo):
    mock_repo.get_by_email.return_value = existing_user
    with pytest.raises(ConflictError, match="Email already registered"):
        await user_service.create(UserCreate(email="taken@example.com", ...))

# Parametrized validation
@pytest.mark.parametrize("email,expected", [
    ("valid@example.com", True),
    ("invalid", False),
    ("", False),
    ("a@b.c", True),
])
def test_email_validation(email, expected):
    if expected:
        UserCreate(email=email, name="Test", password="12345678")
    else:
        with pytest.raises(ValidationError):
            UserCreate(email=email, name="Test", password="12345678")
```

### 7 条测试规则

1. **测试服务逻辑，而不是路由器** — 业务逻辑应放在服务层中
2. **使用测试 fixture 替换真实的数据库 | 通过 `app.dependency_overrides` 功能切换测试数据库 |
3. **每个测试用例只验证一个功能点** — 明确测试失败的原因 |
4. **测试错误路径** — 40% 的测试用例应覆盖错误情况 |
5. **使用测试工厂生成数据 | 使用 `UserFactory.create()` 而不是手动构造数据 |
6. **异步测试需要使用 `@pytest.mark.asyncio` 标注** | 或者在配置中设置 `asyncio_mode = "auto" |
7. **在持续集成（CI）环境中运行测试** — 如果测试失败则阻止代码合并

## 第 8 阶段：结构化日志记录与可观测性

### 结构化日志（Structlog）的配置

```python
import structlog
from uuid import uuid4
from starlette.middleware.base import BaseHTTPMiddleware

structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer(),
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
)

logger = structlog.get_logger()

# Request ID middleware
class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid4()))
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(
            request_id=request_id,
            method=request.method,
            path=request.url.path,
        )
        
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        
        logger.info(
            "request_completed",
            status_code=response.status_code,
        )
        return response
```

### 健康检查端点

```python
@router.get("/health")
async def health():
    """Liveness probe — is the process running?"""
    return {"status": "ok"}

@router.get("/ready")
async def ready(db: AsyncSession = Depends(get_db)):
    """Readiness probe — can we serve traffic?"""
    checks = {}
    try:
        await db.execute(text("SELECT 1"))
        checks["database"] = "ok"
    except Exception:
        checks["database"] = "error"
    
    all_ok = all(v == "ok" for v in checks.values())
    return JSONResponse(
        status_code=200 if all_ok else 503,
        content={"status": "ok" if all_ok else "degraded", "checks": checks},
    )
```

## 第 9 阶段：性能优化

### 优先级排序

| 优化项 | 影响程度 | 需要的努力 |
|---|-----------|--------|--------|
| 1 | 异步数据库查询 | 高 | 较低 |
| 2 | 连接池（优化配置） | 高 | 较低 |
| 3 | 响应缓存（使用 Redis） | 高 | 中等 |
| 4 | 执行后台任务 | 高 | 中等 |
| 5 | 所有列表接口都支持分页 | 中等 | 较低 |
| 6 | 仅选择需要的列 | 中等 | 较低 |
| 7 | 预加载数据（使用 joinedload） | 中等 | 中等 |
| 8 | 实施速率限制 | 中等 | 较低 |

### 后台任务

```python
from fastapi import BackgroundTasks

@router.post("/users", status_code=201)
async def create_user(
    user_in: UserCreate,
    background_tasks: BackgroundTasks,
    service: UserService = Depends(get_user_service),
):
    user = await service.create(user_in)
    background_tasks.add_task(send_welcome_email, user.email, user.name)
    return user
```

### 缓存策略

```python
from redis.asyncio import Redis
import json

class CacheService:
    def __init__(self, redis: Redis):
        self.redis = redis
    
    async def get_or_set(self, key: str, factory, ttl: int = 300):
        cached = await self.redis.get(key)
        if cached:
            return json.loads(cached)
        result = await factory()
        await self.redis.setex(key, ttl, json.dumps(result, default=str))
        return result
    
    async def invalidate(self, pattern: str):
        keys = await self.redis.keys(pattern)
        if keys:
            await self.redis.delete(*keys)
```

## 第 10 阶段：生产环境部署

### 多阶段 Dockerfile 构建

```dockerfile
# Build stage
FROM python:3.12-slim AS builder
WORKDIR /app

RUN pip install --no-cache-dir uv
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-editable

# Production stage
FROM python:3.12-slim
WORKDIR /app

RUN adduser --disabled-password --no-create-home appuser

COPY --from=builder /app/.venv /app/.venv
COPY src/ ./src/
COPY migrations/ ./migrations/
COPY alembic.ini ./

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

USER appuser
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD ["python", "-c", "import httpx; httpx.get('http://localhost:8000/health').raise_for_status()"]

CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### 应用工厂（App Factory）设计

```python
from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("starting_up", environment=settings.environment)
    await init_db()
    yield
    # Shutdown
    logger.info("shutting_down")
    await engine.dispose()

def create_app() -> FastAPI:
    settings = get_settings()
    
    app = FastAPI(
        title=settings.app_name,
        lifespan=lifespan,
        docs_url="/docs" if settings.debug else None,
        redoc_url=None,
    )
    
    # Middleware (order matters — last added = first executed)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(RequestIDMiddleware)
    
    # Error handlers
    app.add_exception_handler(AppError, app_error_handler)
    
    # Routers
    app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
    app.include_router(users_router, prefix="/api/users", tags=["users"])
    app.include_router(health_router, tags=["health"])
    
    return app

app = create_app()
```

### 使用 GitHub Actions 进行持续集成（CI）

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
          POSTGRES_PASSWORD: test
          POSTGRES_DB: testdb
        ports: ["5432:5432"]
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: pip install uv && uv sync
      - run: uv run ruff check .
      - run: uv run mypy src/
      - run: uv run pytest --cov=src --cov-report=xml -x
        env:
          DATABASE_URL: postgresql+asyncpg://postgres:test@localhost:5432/testdb
          JWT_SECRET: test-secret-key-at-least-32-chars
```

### 生产环境检查清单

**必选项：**
- 所有敏感信息都存储在环境变量中（使用 `SecretStr`）
- 强制使用 HTTPS
- 根据环境配置 CORS
- 对身份验证端点实施速率限制
- 所有端点都进行输入验证
- 响应信息采用结构化格式（避免使用堆栈跟踪）
- 提供健康检查和服务就绪状态检查
- 使用数据库连接池
- 在部署前执行数据库迁移
- 使用结构化日志记录（JSON 格式）
- 测试通过持续集成（CI）流程

**推荐项：**
- 使用 OpenTelemetry 进行日志跟踪
- 配置 Prometheus 指标收集
- 使用 Celery 或 ARQ 等工具管理后台任务队列
- 实施 Redis 缓存
- 制定 API 版本管理策略
- 记录请求和响应日志
- 扫描依赖项的安全性
- 进行性能基准测试

## 第 11 阶段：高级开发技巧

### 中间件堆栈的顺序

```python
# Applied bottom-to-top (last added = first executed)
app.add_middleware(GZipMiddleware, minimum_size=1000)    # 5. Compress
app.add_middleware(CORSMiddleware, ...)                  # 4. CORS
app.add_middleware(RequestIDMiddleware)                   # 3. Request ID
app.add_middleware(RateLimitMiddleware)                   # 2. Rate limit
app.add_middleware(TrustedHostMiddleware, allowed=["*"])  # 1. Host check
```

### 基于游标的分页实现

```python
from fastapi import Query

class PaginationParams:
    def __init__(
        self,
        page: int = Query(1, ge=1, description="Page number"),
        page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    ):
        self.offset = (page - 1) * page_size
        self.limit = page_size
        self.page = page
        self.page_size = page_size

@router.get("/users", response_model=PaginatedResponse[UserResponse])
async def list_users(
    pagination: PaginationParams = Depends(),
    service: UserService = Depends(get_user_service),
):
    items, total = await service.list(
        offset=pagination.offset, limit=pagination.limit
    )
    return PaginatedResponse(
        items=items, total=total,
        page=pagination.page, page_size=pagination.page_size,
        has_next=(pagination.offset + pagination.limit) < total,
    )
```

### WebSocket 功能的实现

```python
from fastapi import WebSocket, WebSocketDisconnect

class ConnectionManager:
    def __init__(self):
        self.connections: dict[str, WebSocket] = {}
    
    async def connect(self, user_id: str, ws: WebSocket):
        await ws.accept()
        self.connections[user_id] = ws
    
    def disconnect(self, user_id: str):
        self.connections.pop(user_id, None)
    
    async def send(self, user_id: str, message: dict):
        if ws := self.connections.get(user_id):
            await ws.send_json(message)

manager = ConnectionManager()

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            # Process message
    except WebSocketDisconnect:
        manager.disconnect(user_id)
```

### 文件上传功能的实现

```python
from fastapi import UploadFile, File

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(..., description="File to upload"),
    user: User = Depends(get_current_user),
):
    # Validate
    if file.size and file.size > 10 * 1024 * 1024:  # 10MB
        raise ValidationError("File too large (max 10MB)")
    
    allowed_types = {"image/jpeg", "image/png", "application/pdf"}
    if file.content_type not in allowed_types:
        raise ValidationError(f"File type not allowed: {file.content_type}")
    
    # Save
    contents = await file.read()
    path = f"uploads/{user.id}/{file.filename}"
    # Save to S3/local storage...
    
    return {"filename": file.filename, "size": len(contents)}
```

## 第 12 阶段：常见错误及解决方法

| 错误类型 | 解决方法 |
|---|---------|-----|
| 1 | 在异步应用中使用同步数据库操作 | 使用异步的 SQLAlchemy 或其他异步数据库库 |
| 2 | 将业务逻辑放在路由处理函数中 | 将业务逻辑移至服务层 |
| 3 | 不对输入数据进行验证 | 在所有接口中使用 Pydantic 模型进行数据验证 |
| 4 | 直接返回 ORM 模型 | 使用响应结构（包含字段属性） |
| 5 | 硬编码配置值 | 使用 Pydantic 设置和环境变量进行配置 |
| 6 | 没有错误处理机制 | 自定义错误处理类和全局错误处理器 |
| 7 | 未配置健康检查端点 | 必须提供 `/health` 和 `/ready` 端点 |
| 8 | 使用 `print()` 进行日志记录 | 使用结构化日志（JSON 格式） |
| 9 | 列表接口不支持分页 | 设置默认的分页限制（例如每页 100 条记录） |
| 10 | 在生产环境中测试代码 | 使用与生产环境不同的测试数据库 |

## 质量评分（0–100 分）

| 评估维度 | 权重 | 0–25 | 50 | 75 | 100 |
|-----------|--------|------|----|----|-----|
| 类型安全 | 15% | 未使用类型安全机制 | 部分使用 Pydantic | 完整使用 Pydantic 模型 | 代码通过 mypy 静态类型检查 |
| 错误处理 | 15% | 仅使用简单的 `HTTPException` | 使用自定义错误类型 | 实现完整的错误处理层次结构 | 配置监控工具 |
| 测试 | 15% | 没有进行充分的测试 | 仅测试正常情况 | 覆盖率超过 80% | 包含合同测试 |
| 安全性 | 15% | 未实施身份验证 | 仅使用基本 JWT | 实施基于角色的访问控制（RBAC）和速率限制 | 进行安全扫描和审计 |
| 性能 | 10% | 所有操作都同步执行 | 使用异步数据库 | 使用缓存 | 进行性能分析 |
| 可观测性 | 10% | 使用 `print()` 进行日志记录 | 使用结构化日志 | 配置日志跟踪和指标监控 | |
| 数据库 | 10% | 使用原始 SQL | 使用 ORM 和数据库迁移 | 配置数据库迁移机制 | |
| 部署 | 10% | 部署过程手动操作 | 使用 Dockerfile | 配置持续集成/持续部署（CI/CD） | 配置健康检查机制和回滚功能 |

**评分标准：** 总分 = 各评估维度的得分之和 × 相应权重。**总分低于 40 分表示存在严重问题；40–60 分表示需要改进；60–80 分表示应用达到中等水平；80 分以上表示应用达到生产级标准。**

## FastAPI 生产环境的 10 条黄金法则：

1. **在所有接口边界使用 Pydantic 模型** — 包括请求、响应和配置数据
2. **全程使用异步编程** — 即使是一个同步操作也可能阻塞事件循环
3. **服务层负责处理业务逻辑** — 路由器仅作为轻量级的封装层
4. **使用依赖注入确保代码的可测试性** — `Depends()` 是提高代码可测试性的关键工具
5. **错误信息和日志记录都要结构化** — 所有输出信息都采用 JSON 格式
6. **健康检查是必不可少的** — 必须提供应用的健康状态和就绪状态检查
7. **测试错误情况** — 40% 的测试用例应覆盖错误情况
8. **在部署前执行数据库迁移** — 绝不要手动修改数据库模式
9. **敏感信息存储在环境变量中，切勿硬编码在代码中** — 使用 `SecretStr` 确保敏感信息的安全性
10. **在优化之前先进行性能分析** — 先测量现有性能，再做优化决策

## 常用命令：

- `audit my FastAPI project` → 运行健康检查，识别潜在问题
- `set up a new FastAPI project` → 生成项目结构和配置文件
- `add authentication to my API` → 为 API 实现 JWT 和基于角色的访问控制（RBAC）
- `create a CRUD feature for [resource]` | 为特定资源创建相应的服务、路由、数据库模式和文档
- `optimize my database queries` | 优化数据库查询性能
- `add structured logging` | 配置结构化日志记录
- `write tests for [feature]` | 为相关功能编写异步测试用例
- `prepare for production deployment` | 配置 Dockerfile 和持续集成流程
- `add caching to my API` | 配置 Redis 缓存
- `set up error handling` | 实现自定义错误处理机制和全局错误处理器
- `add WebSocket support` | 配置 WebSocket 支持
- `review my API security` | 进行全面的安全性审计

---

⚡ **提升您的 FastAPI 应用程序水平** → 获取 [AfrexAI SaaS 架构包（价格：47 美元）](https://afrexai-cto.github.io/context-packs/)，获取完整的 SaaS 架构方案、定价策略和市场推广指南。

🔗 **AfrexAI 提供的更多免费技能：**
- [afrexai-python-production](https://clawhub.com/skills/afrexai-python-production) — Python 生产环境开发技巧
- [afrexai-api-architecture](https://clawhub.com/skills/afrexai-api-architecture) — API 设计方法论
- [afrexai-database-engineering](https://clawhub.com/skills/afrexai-database-engineering) — 数据库开发最佳实践
- [afrexai-test-automation-engineering](https://clawhub.com/skills/afrexai-test-automation-engineering) — 自动化测试策略
- [afrexai-cicd-engineering](https://clawhub.com/skills/afrexai-cicd-engineering) — 持续集成/持续部署（CI/CD）流程设计

🛒 浏览所有技能包 → [AfrexAI 商店页面](https://afrexai-cto.github.io/context-packs/)