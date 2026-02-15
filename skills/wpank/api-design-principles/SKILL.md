---
name: api-design-principles
model: reasoning
---

# API 设计原则

## 目标
设计直观、可扩展的 REST 和 GraphQL API，让开发人员满意。涵盖资源建模、HTTP 半义、分页、错误处理、版本控制以及 GraphQL 模式设计。

## 适用场景
- 设计新的 REST 或 GraphQL API
- 在实现前审查 API 规范
- 为团队建立统一的 API 设计标准
- 重构 API 以提高可用性
- 在不同的 API 架构之间进行迁移

## 关键词
REST、GraphQL、API 设计、HTTP 方法、分页、错误处理、版本控制、OpenAPI、HATEOAS、模式设计

---

## REST 与 GraphQL 的选择框架

| 选择 REST 的情况 | 选择 GraphQL 的情况 |
|-------------------|------------------------|
| 简单的 CRUD 操作 | 需要处理复杂嵌套数据的情况 |
| 面向广大用户的公共 API | 需要优化带宽使用的移动应用 |
| 需要大量缓存的情况 | 客户端需要指定数据的具体结构 |
| 团队不熟悉 GraphQL | 需要聚合多个数据源的情况 |
| 响应结构简单的情况 | 前端需求变化迅速的情况 |

---

## REST API 设计

### 资源命名规则

```
✓ Plural nouns for collections
  GET /api/users
  GET /api/orders
  GET /api/products

✗ Avoid verbs (let HTTP methods be the verb)
  POST /api/createUser     ← Wrong
  POST /api/users          ← Correct

✓ Nested resources (max 2 levels)
  GET /api/users/{id}/orders
  
✗ Avoid deep nesting
  GET /api/users/{id}/orders/{orderId}/items/{itemId}/reviews  ← Too deep
  GET /api/order-items/{id}/reviews                            ← Better
```

### HTTP 方法与状态码

| 方法 | 功能 | 成功 | 常见错误 |
|--------|---------|---------|---------------|
| GET | 获取资源 | 200 OK | 404 未找到 |
| POST | 创建资源 | 201 创建成功 | 400/422 验证失败 |
| PUT | 更新资源 | 200 更新成功 | 404 未找到 |
| PATCH | 部分更新资源 | 200 部分更新成功 | 404 未找到 |
| DELETE | 删除资源 | 204 无内容 | 404/409 冲突 |

### 完整的状态码参考

```python
SUCCESS = {
    200: "OK",           # GET, PUT, PATCH success
    201: "Created",      # POST success
    204: "No Content",   # DELETE success
}

CLIENT_ERROR = {
    400: "Bad Request",           # Malformed syntax
    401: "Unauthorized",          # Missing/invalid auth
    403: "Forbidden",             # Valid auth, no permission
    404: "Not Found",             # Resource doesn't exist
    409: "Conflict",              # State conflict (duplicate email)
    422: "Unprocessable Entity",  # Validation errors
    429: "Too Many Requests",     # Rate limited
}

SERVER_ERROR = {
    500: "Internal Server Error",
    503: "Service Unavailable",   # Temporary downtime
}
```

### 分页

#### 基于偏移量的分页（简单情况）

```python
GET /api/users?page=2&page_size=20

{
  "items": [...],
  "page": 2,
  "page_size": 20,
  "total": 150,
  "pages": 8
}
```

#### 基于游标的分页（适用于大数据集）

```python
GET /api/users?limit=20&cursor=eyJpZCI6MTIzfQ

{
  "items": [...],
  "next_cursor": "eyJpZCI6MTQzfQ",
  "has_more": true
}
```

### 过滤与排序

```
# Filtering
GET /api/users?status=active&role=admin

# Sorting (- prefix for descending)
GET /api/users?sort=-created_at,name

# Search
GET /api/users?search=john

# Field selection
GET /api/users?fields=id,name,email
```

### 错误响应格式
始终使用一致的结构进行错误响应：

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [
      {"field": "email", "message": "Invalid email format"}
    ],
    "timestamp": "2025-10-16T12:00:00Z"
  }
}
```

### FastAPI 实现

```python
from fastapi import FastAPI, Query, Path, HTTPException, status
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime

app = FastAPI(title="API", version="1.0.0")

# Models
class UserCreate(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)

class User(BaseModel):
    id: str
    email: str
    name: str
    created_at: datetime

class PaginatedResponse(BaseModel):
    items: List[User]
    total: int
    page: int
    page_size: int
    pages: int

# Endpoints
@app.get("/api/users", response_model=PaginatedResponse)
async def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None)
):
    """List users with pagination and filtering."""
    total = await count_users(status=status, search=search)
    offset = (page - 1) * page_size
    users = await fetch_users(limit=page_size, offset=offset, status=status, search=search)
    
    return PaginatedResponse(
        items=users,
        total=total,
        page=page,
        page_size=page_size,
        pages=(total + page_size - 1) // page_size
    )

@app.post("/api/users", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    """Create new user."""
    if await user_exists(user.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"code": "EMAIL_EXISTS", "message": "Email already registered"}
        )
    return await save_user(user)

@app.get("/api/users/{user_id}", response_model=User)
async def get_user(user_id: str = Path(...)):
    """Get user by ID."""
    user = await fetch_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.delete("/api/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str):
    """Delete user."""
    if not await fetch_user(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    await remove_user(user_id)
```

---

## GraphQL API 设计

### 模式设计

```graphql
# Types
type User {
  id: ID!
  email: String!
  name: String!
  createdAt: DateTime!
  orders(first: Int = 20, after: String): OrderConnection!
}

# Pagination (Relay-style)
type OrderConnection {
  edges: [OrderEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type OrderEdge {
  node: Order!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

# Queries
type Query {
  user(id: ID!): User
  users(first: Int = 20, after: String, search: String): UserConnection!
}

# Mutations with Input/Payload pattern
input CreateUserInput {
  email: String!
  name: String!
  password: String!
}

type CreateUserPayload {
  user: User
  errors: [Error!]
}

type Error {
  field: String
  message: String!
  code: String!
}

type Mutation {
  createUser(input: CreateUserInput!): CreateUserPayload!
}
```

### 数据加载器（防止 N+1 问题）

```python
from aiodataloader import DataLoader

class UserLoader(DataLoader):
    async def batch_load_fn(self, user_ids: List[str]) -> List[Optional[dict]]:
        """Load multiple users in single query."""
        users = await fetch_users_by_ids(user_ids)
        user_map = {user["id"]: user for user in users}
        return [user_map.get(uid) for uid in user_ids]

# In resolver
@user_type.field("orders")
async def resolve_orders(user: dict, info):
    loader = info.context["loaders"]["orders_by_user"]
    return await loader.load(user["id"])
```

### 查询保护机制

```python
# Depth limiting
MAX_QUERY_DEPTH = 5

# Complexity limiting
MAX_QUERY_COMPLEXITY = 100

# Timeout
QUERY_TIMEOUT_SECONDS = 10
```

---

## 版本控制策略

### URL 版本控制（推荐方案）

```
/api/v1/users
/api/v2/users
```

**优点**：清晰易懂、易于路由、支持缓存
**缺点**：同一资源可能有多个 URL

### 标头版本控制

```
GET /api/users
Accept: application/vnd.api+json; version=2
```

**优点**：URL 更简洁
**缺点**：不太直观、测试难度较大

### 废弃策略
1. 添加废弃标记：`Deprecation: true`
2. 文档化迁移路径
3. 提前 6-12 个月通知
4. 在删除前监控使用情况

---

## 速率限制

### 使用的头部信息

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 742
X-RateLimit-Reset: 1640000000

# When limited:
429 Too Many Requests
Retry-After: 3600
```

### 实现方式

```python
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, calls: int, period: int):
        self.calls = calls
        self.period = period
        self.cache = {}
    
    def check(self, key: str) -> tuple[bool, dict]:
        now = datetime.now()
        if key not in self.cache:
            self.cache[key] = []
        
        # Remove old requests
        cutoff = now - timedelta(seconds=self.period)
        self.cache[key] = [ts for ts in self.cache[key] if ts > cutoff]
        
        remaining = self.calls - len(self.cache[key])
        
        if remaining <= 0:
            return False, {"limit": self.calls, "remaining": 0}
        
        self.cache[key].append(now)
        return True, {"limit": self.calls, "remaining": remaining - 1}
```

---

## 实施前的检查清单

### 资源相关
- 使用名词而非动词作为接口名称
- 集合类使用复数形式
- 最多允许两层嵌套

### HTTP 相关
- 每个操作使用正确的 HTTP 方法
- 使用正确的状态码
- 幂等操作必须保持幂等性

### 数据相关
- 所有集合数据都支持分页
- 支持过滤和排序
- 错误格式统一

### 安全相关
- 定义了身份验证机制
- 配置了速率限制
- 对所有输入字段进行验证
- 强制使用 HTTPS 协议

### 文档相关
- 生成 OpenAPI 规范
- 所有接口点都有文档说明
- 提供示例代码

---

## 绝对禁止的做法
- **在 URL 中使用动词**：例如 `/api/getUser` 应改为 `/api/users/{id}` 并使用 GET 方法
- **使用 POST 方法进行获取操作**：对于安全的、幂等性的读取操作，应使用 GET 方法
- **错误信息不一致**：错误信息格式必须统一
- **列表没有上限**：所有集合数据都应支持分页
- **在 URL 中包含敏感信息**：查询参数会被记录下来
- **在没有版本控制的情况下进行重大更改**：从项目开始就应规划好系统的演进方向
- **将数据库模式直接作为 API 的结构**：即使数据库模式发生变化，API 也应保持稳定
- **忽略 HTTP 半义**：HTTP 状态码和方法都有其特定的含义