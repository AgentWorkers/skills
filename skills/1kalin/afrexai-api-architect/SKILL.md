---
name: afrexai-api-architect
description: 设计、开发、测试、文档编写以及保护生产级API的安全性。涵盖了从架构设计到部署、监控以及版本控制的整个生命周期。适用于新API的设计、现有API的审查、OpenAPI规范的生成、测试套件的构建，或生产环境问题的调试等场景。
metadata: {"openclaw":{"os":["linux","darwin","win32"]}}
---
# API架构师——全生命周期API开发

设计、构建、测试、文档化、保护并监控生产级别的API。这不仅仅是一系列curl命令的集合，而是一种完整的工程方法论。

## 适用场景

- 设计新的API（REST、GraphQL或gRPC）
- 评估现有API的质量、一致性和安全性
- 生成或验证OpenAPI/Swagger规范
- 构建全面的测试套件（单元测试、集成测试、契约测试、负载测试）
- 调试生产环境中的API问题
- 规划API的版本控制及淘汰策略
- 设置监控机制、速率限制和错误处理

---

## 第1阶段：API设计

### 首先设计

在编码之前，务必先进行设计。API规范本身就是契约。

#### 资源建模

使用以下模板将你的业务领域映射到具体的资源：

```yaml
# api-design.yaml
service: order-management
base_path: /api/v1
resources:
  - name: orders
    path: /orders
    description: Customer purchase orders
    identifier: order_id (UUID)
    parent: null
    operations: [list, create, get, update, cancel]
    sub_resources:
      - name: line_items
        path: /orders/{order_id}/items
        operations: [list, add, update, remove]
      - name: payments
        path: /orders/{order_id}/payments
        operations: [list, create, get, refund]
    states: [draft, confirmed, processing, shipped, delivered, cancelled]
    transitions:
      - from: draft → to: confirmed (action: confirm)
      - from: confirmed → to: processing (action: process)
      - from: processing → to: shipped (action: ship)
      - from: shipped → to: delivered (action: deliver)
      - from: [draft, confirmed] → to: cancelled (action: cancel)
```

#### 命名规范检查表

| 规则 | 合适 | 不合适 |
|------|------|-----|
| 集合使用复数名词 | `/users` | `/user`, `/getUsers` |
| 多词使用驼峰式命名法 | `/line-items` | `/lineItems`, `/line_items` |
| URL中不使用动词 | `POST /orders` | `/createOrder` |
| 通过路径表示所有权关系 | `/users/123/orders` | `/orders?user=123` （表示主键关系） |
| 最多3层嵌套 | `/users/123/orders` | `/users/123/orders/456/items/789/options` |
| 通过查询参数过滤 | `/orders?status=active` | `/active-orders` |
| 动作作为子资源 | `POST /orders/123/cancel` | `PATCH /orders/123 {cancelled:true}` |

#### HTTP方法选择矩阵

```
Need to...                          → Method   Idempotent?  Safe?
Get a resource or collection        → GET      Yes          Yes
Create a new resource               → POST     No           No
Full replace of a resource          → PUT      Yes          No
Partial update of a resource        → PATCH    No*          No
Remove a resource                   → DELETE   Yes          No
Check if resource exists            → HEAD     Yes          Yes
List allowed methods                → OPTIONS  Yes          Yes

* PATCH can be idempotent if using JSON Merge Patch
```

#### 状态码决策树

```
Success?
├── Created something new? → 201 Created (Location header)
├── Accepted for async processing? → 202 Accepted (include status URL)
├── No body to return? → 204 No Content
└── Returning data? → 200 OK

Client error?
├── Malformed request syntax? → 400 Bad Request
├── No/invalid credentials? → 401 Unauthorized
├── Valid credentials but insufficient permissions? → 403 Forbidden
├── Resource doesn't exist? → 404 Not Found
├── Method not allowed on resource? → 405 Method Not Allowed
├── Conflict with current state? → 409 Conflict
├── Resource permanently gone? → 410 Gone
├── Validation failed? → 422 Unprocessable Entity
├── Too many requests? → 429 Too Many Requests (Retry-After header)
└── Precondition failed (etag mismatch)? → 412 Precondition Failed

Server error?
├── Unexpected failure? → 500 Internal Server Error
├── Upstream dependency failed? → 502 Bad Gateway
├── Temporarily overloaded? → 503 Service Unavailable (Retry-After)
└── Upstream timeout? → 504 Gateway Timeout
```

### 请求/响应设计

#### 标准响应格式

```json
// Success (single resource)
{
  "data": { "id": "ord_abc123", "status": "confirmed", ... },
  "meta": { "request_id": "req_xyz789" }
}

// Success (collection)
{
  "data": [ ... ],
  "meta": { "request_id": "req_xyz789" },
  "pagination": {
    "total": 142,
    "page": 2,
    "per_page": 20,
    "total_pages": 8,
    "next": "/api/v1/orders?page=3&per_page=20",
    "prev": "/api/v1/orders?page=1&per_page=20"
  }
}

// Error
{
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "Request validation failed",
    "details": [
      { "field": "email", "message": "Must be a valid email address", "code": "INVALID_FORMAT" },
      { "field": "age", "message": "Must be at least 18", "code": "MIN_VALUE", "min": 18 }
    ]
  },
  "meta": { "request_id": "req_xyz789" }
}
```

#### 分页模式及适用场景

| 模式 | 适用场景 | 优点 | 缺点 |
|---------|----------|------|------|
| **Offset** `?page=2&per_page=20` | 简单的UI分页，适用于小型数据集 | 实现容易，但插入操作时可能导致数据偏移 |
| **Cursor** `?after=eyJ...&limit=20` | 无限滚动，适用于实时数据流和大型数据集 | 一致性高，性能良好 | 无法直接跳转页面 |
| **Keyset** `?created_after=2024-01-01&limit=20` | 适用于时间序列数据或日志 | 快速响应，但需要可排序的字段 |

#### 过滤、排序和字段选择

```
# Filtering
GET /orders?status=active&created_after=2024-01-01&total_min=100

# Sorting (prefix - for descending)
GET /orders?sort=-created_at,total

# Field selection (reduce payload)
GET /orders?fields=id,status,total,customer.name

# Search
GET /products?q=wireless+headphones

# Combined
GET /orders?status=active&sort=-created_at&fields=id,status,total&page=1&per_page=10
```

---

## 第2阶段：OpenAPI规范

### 生成OpenAPI 3.1规范

为设计中的每个资源生成完整的规范文档：

```yaml
openapi: 3.1.0
info:
  title: Order Management API
  version: 1.0.0
  description: |
    Order lifecycle management.
    
    ## Authentication
    All endpoints require Bearer token authentication.
    
    ## Rate Limits
    - Standard: 100 req/min
    - Bulk operations: 10 req/min
  contact:
    name: API Support
    email: api@example.com
  license:
    name: MIT
servers:
  - url: https://api.example.com/v1
    description: Production
  - url: https://staging-api.example.com/v1
    description: Staging

paths:
  /orders:
    get:
      operationId: listOrders
      summary: List orders
      tags: [Orders]
      parameters:
        - $ref: '#/components/parameters/PageParam'
        - $ref: '#/components/parameters/PerPageParam'
        - name: status
          in: query
          schema:
            $ref: '#/components/schemas/OrderStatus'
        - name: created_after
          in: query
          schema:
            type: string
            format: date-time
      responses:
        '200':
          description: Order list
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/OrderListResponse'
        '401':
          $ref: '#/components/responses/Unauthorized'

    post:
      operationId: createOrder
      summary: Create an order
      tags: [Orders]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateOrderRequest'
            examples:
              basic:
                summary: Basic order
                value:
                  customer_id: "cust_abc"
                  items:
                    - product_id: "prod_xyz"
                      quantity: 2
      responses:
        '201':
          description: Order created
          headers:
            Location:
              schema:
                type: string
              description: URL of created order
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/OrderResponse'
        '422':
          $ref: '#/components/responses/ValidationError'

components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

  parameters:
    PageParam:
      name: page
      in: query
      schema: { type: integer, minimum: 1, default: 1 }
    PerPageParam:
      name: per_page
      in: query
      schema: { type: integer, minimum: 1, maximum: 100, default: 20 }

  responses:
    Unauthorized:
      description: Missing or invalid authentication
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ErrorResponse'
    ValidationError:
      description: Request validation failed
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ErrorResponse'

security:
  - BearerAuth: []
```

### 规范质量检查表（每项0-2分）

| 编号 | 检查项 | 分数 |
|---|-------|-------|
| 1 | 每个端点都有操作ID | /2 |
| 2 | 所有参数都带有类型和约束 | /2 |
| 3 | 请求体包含示例数据 | /2 |
| 4 | 所有错误响应都有文档说明（400, 401, 403, 404, 422, 429, 500） | /2 |
| 5 | 共享的schema使用 `$ref`（DRY原则） | /2 |
| 6 | 分页参数标准化 | /2 |
| 7 | 定义了安全策略并全局应用 | /2 |
| 8 | 描述中包含认证、速率限制和版本信息 | /2 |
| 9 | 响应头有明确的文档说明 | /2 |
| 10 | 使用枚举来表示固定值集合 | /2 |

**总分：___/20**（目标分数：16分以上）

---

## 第3阶段：实现模式

### 请求验证层

每个端点在处理请求之前都必须进行验证：

```
Validation Order:
1. Content-Type header (reject non-JSON early)
2. Authentication (401 before wasting cycles)
3. Authorization (403 - does this user have access?)
4. Path parameters (404 - does the resource exist?)
5. Query parameters (400 - valid types/ranges?)
6. Request body schema (422 - valid structure?)
7. Business rules (422 - valid state transition?)
```

### 错误处理——标准错误代码

为API定义一套统一的错误代码：

```
# Authentication & Authorization
AUTH_REQUIRED          — No credentials provided
AUTH_INVALID           — Invalid/expired credentials
AUTH_INSUFFICIENT      — Valid credentials, wrong permissions
AUTH_RATE_LIMITED       — Too many auth attempts

# Validation
VALIDATION_FAILED      — Generic validation error (see details array)
INVALID_FORMAT         — Field format wrong (email, UUID, etc.)
REQUIRED_FIELD         — Required field missing
OUT_OF_RANGE           — Value outside allowed range
INVALID_ENUM           — Value not in allowed set

# Resource
NOT_FOUND              — Resource doesn't exist
ALREADY_EXISTS         — Duplicate (unique constraint)
CONFLICT               — State conflict (e.g., already cancelled)
GONE                   — Resource permanently deleted

# Business Logic
INSUFFICIENT_FUNDS     — Payment-related
QUOTA_EXCEEDED         — Usage limit reached
FEATURE_DISABLED       — Feature flag off
DEPENDENCY_FAILED      — Upstream service error

# System
INTERNAL_ERROR         — Unexpected server error
SERVICE_UNAVAILABLE    — Temporarily down
TIMEOUT                — Request took too long
```

### 幂等性

对于非幂等操作（如POST请求），需要添加幂等性标识：

```
Request:
POST /orders
Idempotency-Key: ord_req_abc123

Server behavior:
1. Check if Idempotency-Key was seen before
2. If yes → return cached response (same status, same body)
3. If no → process request, cache response for 24h
4. Key format: client-generated UUID or meaningful string
```

### 速率限制

需要包含的标准响应头：

```
X-RateLimit-Limit: 100          # Max requests per window
X-RateLimit-Remaining: 67       # Remaining in current window
X-RateLimit-Reset: 1706886400   # Unix timestamp when window resets
Retry-After: 30                 # Seconds to wait (on 429)
```

### 速率限制等级

| 等级 | 限制频率 | 适用场景 |
|------|-------|--------|----------|
| 标准 | 每分钟100次 | 常规API调用 |
| 批量操作 | 每分钟10次 | 批量处理操作 |
| 搜索 | 每分钟30次 | 全文搜索 |
| 登录尝试 | 每分钟5次 | 固定频率 |

---

## 第4阶段：测试策略

### API的测试层次结构

```
        /  E2E  \          — 5-10 critical user flows
       / Contract \        — Schema validation, backward compat
      / Integration \      — Database, external services, auth
     /    Unit Tests  \    — Business logic, validation, transforms
    ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
```

### 每个端点的测试检查项

对于每个端点，都需要测试以下场景：

```yaml
endpoint: POST /orders
tests:
  happy_path:
    - Creates order with valid data → 201
    - Returns created resource with ID
    - Location header points to new resource
    - Timestamps are set (created_at, updated_at)
  
  validation:
    - Missing required fields → 422 with field-level errors
    - Invalid field types (string where int expected) → 422
    - Empty body → 400
    - Invalid Content-Type → 415
    - Extra unknown fields → ignored or 422 (pick one, be consistent)
    - Boundary values (min/max length, 0, negative, empty string vs null)
  
  authentication:
    - No token → 401
    - Expired token → 401
    - Invalid token → 401
    - Valid token, wrong scope → 403
  
  authorization:
    - User accessing own resource → 200
    - User accessing other's resource → 403 or 404 (security choice)
    - Admin accessing any resource → 200
  
  edge_cases:
    - Duplicate creation (same idempotency key) → same 201 response
    - Concurrent creation race condition → one wins, one gets 409
    - Resource at max relationships → 422
    - Unicode in text fields → handled correctly
    - Very long strings → 422 with max length error
    - SQL injection in params → no effect (parameterized queries)
    - XSS in text fields → stored safely, escaped on output
  
  performance:
    - Response time < 200ms (p95)
    - List endpoint with 10K records → paginated, < 500ms
    - Bulk operation timeout handling
```

### curl测试示例

```bash
# === Setup ===
BASE="https://api.example.com/v1"
TOKEN="your_bearer_token"
alias api='curl -s -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json"'

# === CRUD Lifecycle Test ===
# Create
ORDER=$(api -X POST "$BASE/orders" -d '{"customer_id":"cust_1","items":[{"product_id":"prod_1","qty":2}]}')
ORDER_ID=$(echo "$ORDER" | jq -r '.data.id')
echo "Created: $ORDER_ID"

# Read
api "$BASE/orders/$ORDER_ID" | jq .

# Update
api -X PATCH "$BASE/orders/$ORDER_ID" -d '{"notes":"Rush order"}' | jq .

# List with filters
api "$BASE/orders?status=draft&sort=-created_at&per_page=5" | jq .

# Action (state transition)
api -X POST "$BASE/orders/$ORDER_ID/confirm" | jq .

# Delete
curl -s -o /dev/null -w "%{http_code}" -X DELETE -H "Authorization: Bearer $TOKEN" "$BASE/orders/$ORDER_ID"

# === Error Testing ===
# No auth
curl -s "$BASE/orders" | jq .error

# Invalid body
api -X POST "$BASE/orders" -d '{"invalid": true}' | jq .error

# Not found
api "$BASE/orders/nonexistent" | jq .error

# === Performance ===
# Timing breakdown
curl -s -o /dev/null -w "DNS:%{time_namelookup} TCP:%{time_connect} TLS:%{time_appconnect} TTFB:%{time_starttransfer} Total:%{time_total}\n" -H "Authorization: Bearer $TOKEN" "$BASE/orders"

# Quick load test (50 requests, 10 concurrent)
seq 50 | xargs -P10 -I{} curl -s -o /dev/null -w "%{http_code} %{time_total}s\n" -H "Authorization: Bearer $TOKEN" "$BASE/orders"
```

### 契约测试

验证API的向后兼容性是否受损：

```yaml
# contract-tests.yaml
contract:
  name: Order API Contract
  version: 1.0.0
  
  rules:
    # These changes are SAFE (non-breaking)
    safe:
      - Adding new optional fields to responses
      - Adding new endpoints
      - Adding new optional query parameters
      - Adding new enum values (if clients handle unknown)
      - Widening a constraint (min: 5 → min: 1)
    
    # These changes are BREAKING
    breaking:
      - Removing a response field
      - Renaming a response field
      - Changing a field type
      - Adding a new required request field
      - Removing an endpoint
      - Narrowing a constraint (max: 100 → max: 50)
      - Changing error response format
      - Removing an enum value
    
    # Verify after every change
    checks:
      - All existing fields still present in responses
      - All existing field types unchanged
      - All existing required fields still required (no more, no fewer)
      - Default values unchanged
      - Error format unchanged
```

---

## 第5阶段：安全防护

### 安全检查表（对每个API进行审计）

```yaml
authentication:
  - [ ] All endpoints require auth (except /health, /docs, public webhooks)
  - [ ] Tokens expire (short-lived access + long-lived refresh)
  - [ ] Token rotation supported
  - [ ] Failed auth returns 401 with no info leakage
  - [ ] API keys are hashed in storage (never plain text)

authorization:
  - [ ] Resource-level checks (user can only access their data)
  - [ ] Endpoint-level checks (role-based access)
  - [ ] No IDOR vulnerabilities (can't guess other users' resource IDs)
  - [ ] Admin endpoints separately protected
  - [ ] Webhook endpoints verify signatures

input_validation:
  - [ ] All inputs validated server-side (never trust client)
  - [ ] SQL injection prevented (parameterized queries only)
  - [ ] NoSQL injection prevented
  - [ ] Path traversal prevented
  - [ ] Request size limited (body, headers, URL length)
  - [ ] File upload types restricted and scanned

output_security:
  - [ ] No sensitive data in responses (passwords, tokens, internal IDs)
  - [ ] No stack traces in production errors
  - [ ] Consistent error format (no info leakage in different error types)
  - [ ] PII redacted in logs

transport:
  - [ ] HTTPS only (HTTP redirects to HTTPS)
  - [ ] HSTS header set
  - [ ] TLS 1.2+ required
  - [ ] CORS configured restrictively (specific origins, not *)
  
headers:
  - [ ] X-Content-Type-Options: nosniff
  - [ ] X-Frame-Options: DENY
  - [ ] Content-Security-Policy set
  - [ ] No Server version header
  - [ ] Cache-Control: no-store for sensitive endpoints
```

### CORS配置

```yaml
# Restrictive (recommended)
cors:
  origins:
    - https://app.example.com
    - https://admin.example.com
  methods: [GET, POST, PUT, PATCH, DELETE]
  headers: [Authorization, Content-Type, X-Request-ID]
  credentials: true
  max_age: 3600

# Common mistakes to avoid:
# ❌ Access-Control-Allow-Origin: *  (with credentials)
# ❌ Reflecting Origin header without validation
# ❌ Allowing all methods/headers
```

---

## 第6阶段：版本控制与淘汰策略

### 版本控制策略选择

| 策略 | 例子 | 优点 | 缺点 | 适用场景 |
|----------|---------|------|------|----------|
| **URL路径** | `/v1/orders` | 明确的版本标识，易于路由 | 可能导致URL混乱 | 适用于公开API和多个主要版本 |
| **请求头** | `API-Version: 2024-01` | URL更简洁 | 隐藏版本信息，测试难度增加 | 适用于内部API |
| **查询参数** | `?version=2` | 测试方便 | 但可能污染参数 | 适用于快速原型开发 |
| **基于日期** | `2024-01-15` | 明确的版本时间线 | 适用于多个版本 | 例如Stripe风格的API |

**建议**：使用URL路径来标识主要版本，使用请求头来标识次要版本变更。

### 淘汰策略

```
Timeline:
1. T+0: Announce deprecation (docs, changelog, email)
2. T+0: Add Deprecation + Sunset headers to old endpoints
3. T+30d: Log warnings for old endpoint usage
4. T+60d: Email heavy users of old endpoint directly
5. T+90d: Return 299 warning header
6. T+180d: Shut down old endpoint (410 Gone)

Headers:
Deprecation: true
Sunset: Sat, 01 Jun 2025 00:00:00 GMT
Link: <https://api.example.com/v2/orders>; rel="successor-version"
```

### 迁移指南模板

```markdown
# Migrating from v1 to v2

## Breaking Changes
1. `user.name` split into `user.first_name` + `user.last_name`
2. Pagination changed from offset to cursor-based
3. Error format updated (see new schema)

## Step-by-Step Migration
1. Update your client SDK to v2 (`npm install @example/sdk@2`)
2. Update response parsing for split name fields
3. Replace `?page=N` with `?after=cursor` pagination
4. Update error handling for new error format

## Compatibility Mode
Set `X-Compat-Mode: v1` header to get v1-style responses from v2 endpoints.
Available until 2025-06-01.
```

---

## 第7阶段：监控与可观测性

### 关键指标仪表盘

```yaml
availability:
  - Uptime percentage (target: 99.9% = 8.7h downtime/year)
  - Health check status (/health endpoint)
  - Error rate (5xx / total requests)

performance:
  - p50 latency (target: < 100ms)
  - p95 latency (target: < 500ms)
  - p99 latency (target: < 1000ms)
  - Throughput (requests/second)
  - Time to first byte (TTFB)

business:
  - Requests per endpoint (usage patterns)
  - Unique API consumers/day
  - Error rate by endpoint
  - Rate limit hits/day
  - Authentication failures/day

infrastructure:
  - Database query time (p95)
  - Connection pool utilization
  - Memory/CPU per instance
  - Queue depth (async operations)
```

### 结构化日志记录

所有请求都应被记录下来：

```json
{
  "timestamp": "2024-01-15T10:30:00.000Z",
  "level": "info",
  "request_id": "req_abc123",
  "method": "POST",
  "path": "/api/v1/orders",
  "status": 201,
  "duration_ms": 45,
  "user_id": "usr_xyz",
  "ip": "203.0.113.1",
  "user_agent": "MyApp/2.0",
  "request_size": 256,
  "response_size": 1024
}
```

### 健康检查端点

```json
// GET /health — for load balancers (simple)
{ "status": "ok" }

// GET /health/detailed — for monitoring (authenticated)
{
  "status": "degraded",
  "version": "1.5.2",
  "uptime_seconds": 86400,
  "checks": {
    "database": { "status": "ok", "latency_ms": 5 },
    "redis": { "status": "ok", "latency_ms": 2 },
    "external_payment_api": { "status": "degraded", "latency_ms": 2500, "error": "timeout" },
    "disk": { "status": "ok", "free_gb": 45.2 }
  }
}
```

---

## 第8阶段：API评审

在评估现有API时，从以下维度进行评分：

### API质量评分标准（0-100分）

| 维度 | 权重 | 评估标准 | 分数 |
|-----------|--------|----------|-------|
| **设计一致性** | 20% | 命名规范、HTTP方法、状态码、URL结构 | /20 |
| **文档质量** | 15% | OpenAPI规范、示例代码、错误处理文档、变更日志 | /15 |
| **错误处理** | 15% | 一致的错误处理格式、有用的错误信息、正确的错误代码 | /15 |
| **安全性** | 20% | 认证机制、输入验证、CORS配置、安全头设置 | /20 |
| **性能** | 15% | 达到延迟目标、支持分页、使用缓存机制 | /15 |
| **开发者体验** | 15% | SDK质量、提供沙箱环境、易用性、速率限制说明 | /15 |

**总分：___/100**

| 评分 | 分数 | 推荐措施 |
|--------|-------|--------|
| 🟢 优秀 | 85-100 | 需要少量改进 |
| 🟡 良好 | 70-84 | 在下一次重大发布前解决存在的问题 |
| 🟠 需改进 | 50-69 | 优先处理改进事项，创建技术债务工单 |
| 🔴 危急 | <50 | 停止当前功能开发，先修复基础问题 |

### 评审输出模板

```markdown
## API Review: [Service Name]

**Date:** YYYY-MM-DD
**Reviewer:** [Agent]
**Score:** XX/100 (Rating)

### Summary
[2-3 sentence overview of API quality]

### Scores by Dimension
- Design Consistency: X/20 — [key finding]
- Documentation: X/15 — [key finding]
- Error Handling: X/15 — [key finding]
- Security: X/20 — [key finding]
- Performance: X/15 — [key finding]
- Developer Experience: X/15 — [key finding]

### Critical Issues (fix immediately)
1. [Issue + recommendation]

### High Priority (fix this sprint)
1. [Issue + recommendation]

### Nice to Have (backlog)
1. [Issue + recommendation]

### Positive Highlights
- [What's working well]
```

---

## GraphQL特定指导

### 模式设计原则

```graphql
# Good: clear types, nullable where appropriate, connections for lists
type Order {
  id: ID!
  status: OrderStatus!
  customer: Customer!
  items(first: Int, after: String): ItemConnection!
  total: Money!
  createdAt: DateTime!
  updatedAt: DateTime!
}

type Money {
  amount: Int!       # cents, not dollars (avoid float)
  currency: Currency!
}

enum OrderStatus {
  DRAFT
  CONFIRMED
  PROCESSING
  SHIPPED
  DELIVERED
  CANCELLED
}

# Mutations return the modified resource + errors
type CreateOrderPayload {
  order: Order
  errors: [UserError!]!
}

type UserError {
  field: [String!]
  message: String!
  code: ErrorCode!
}
```

### GraphQL反模式

| 反模式 | 问题 | 解决方案 |
|-------------|---------|-----|
| 无深度限制 | 查询性能问题 | 将查询深度限制在5-7层 |
| 无复杂性限制 | 查询效率低下 | 为每个字段设置成本上限（例如1000次） |
| 多次查询 | 严重影响性能 | 使用数据加载器（DataLoader）模式 |
| 无持久化查询 | 安全风险 | 只允许特定的查询类型 |
| 暴露内部ID | 信息泄露风险 | 使用不可见的全局ID |
| 无分页功能 | 内存消耗过高 | 使用Relay Connection模式 |

---

## 边缘情况与注意事项

### 时区处理
- 始终存储和返回UTC时间（ISO 8601格式，例如 `2024-01-15T10:30:00Z`）
- 接受输入中的时区信息，并立即转换为UTC时间
- 绝不要使用本地服务器时间

### 大容量数据传输
- 设置`Content-Length`限制（例如默认为1MB，上传文件时限制为10MB）
- 对文件上传使用流式传输（multipart/form-data）
- 压缩响应数据（使用`Accept-Encoding: gzip`）
- 对于非常大的数据量，返回202状态码并使用轮询机制获取更新状态

### 最终一致性
- 如果使用异步处理，始终返回202状态码和更新状态URL
- 可能时提供预计完成时间
- 客户端应使用指数级退避策略进行轮询

### 并发更新
- 使用ETag实现乐观并发控制：
  - GET请求返回`ETag: "v1"`头 |
  - PUT/PATCH请求发送`If-Match: "v1"`头 |
  - 如果资源已更改，服务器返回412状态码

### Webhook设计
- 在请求体中包含事件类型、时间戳和完整资源信息
- 对请求体进行签名（使用HMAC-SHA256）
- 预期请求会重复发送，因此处理请求时要保证幂等性
- 快速返回200状态码，并异步处理请求
- 包含Webhook ID以便去重

## 快速命令

| 命令 | 功能 |
|---------|--------|
| "为[领域]设计API" | 执行第1阶段的资源建模和命名工作 |
| "生成OpenAPI规范" | 执行第2阶段的全部步骤 |
| "评估此API" | 使用第8阶段的评分标准 |
| "为[端点]编写测试用例" | 执行第4阶段的测试检查 |
| "安全审计此API" | 执行第5阶段的安全检查 |
| "如何为这个API设置版本?" | 使用第6阶段的策略决策 |
| "调试此API问题" | 检查第7阶段的日志记录和健康检查机制 |
| "为[领域]设计GraphQL模式" | 执行第8阶段的GraphQL相关操作 |

---

## 其他实用命令

| 命令 | 功能 |
|---------|--------|
| "Design an API for [domain]" | 为指定领域设计API |
| "Generate OpenAPI spec" | 生成完整的OpenAPI规范 |
| "Review this API" | 评估此API的质量 |
| "Write tests for [endpoint]" | 为指定端点编写测试用例 |
| "Security audit this API" | 安全审计此API |
| "How should I version this?" | 制定此API的版本控制策略 |
| "Debug this API issue" | 调试此API中的问题 |
| "Design GraphQL schema for [domain]" | 为指定领域设计GraphQL模式 |