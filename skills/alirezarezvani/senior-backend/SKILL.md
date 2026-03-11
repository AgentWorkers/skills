---
name: "senior-backend"
description: 设计和实现后端系统，包括 REST API、微服务、数据库架构、认证流程以及安全加固措施。适用于用户需要“设计 REST API”、“优化数据库查询”、“实现认证功能”、“构建微服务”、“审查后端代码”、“配置 GraphQL”、“处理数据库迁移”或“进行 API 性能测试”的场景。涵盖 Node.js/Express/Fastify 开发框架、PostgreSQL 数据库优化、API 安全性以及后端架构设计模式。
---
# 高级后端工程师

负责后端开发模式、API设计、数据库优化以及安全实践。

---

## 快速入门

```bash
# Generate API routes from OpenAPI spec
python scripts/api_scaffolder.py openapi.yaml --framework express --output src/routes/

# Analyze database schema and generate migrations
python scripts/database_migration_tool.py --connection postgres://localhost/mydb --analyze

# Load test an API endpoint
python scripts/api_load_tester.py https://api.example.com/users --concurrency 50 --duration 30
```

---

## 工具概述

### 1. API 构建工具

根据数据库模式定义生成 API 路由处理程序、中间件以及 OpenAPI 规范。

**输入：** OpenAPI 规范（YAML/JSON）或数据库模式
**输出：** 路由处理程序、验证中间件、TypeScript 类型

**使用方法：**
```bash
# Generate Express routes from OpenAPI spec
python scripts/api_scaffolder.py openapi.yaml --framework express --output src/routes/
# Output: Generated 12 route handlers, validation middleware, and TypeScript types

# Generate from database schema
python scripts/api_scaffolder.py --from-db postgres://localhost/mydb --output src/routes/

# Generate OpenAPI spec from existing routes
python scripts/api_scaffolder.py src/routes/ --generate-spec --output openapi.yaml
```

**支持的框架：**
- Express.js (`--framework express`)
- Fastify (`--framework fastify`)
- Koa (`--framework koa`)

---

### 2. 数据库迁移工具

分析数据库模式，检测变更，并生成带有回滚支持的迁移文件。

**输入：** 数据库连接字符串或模式文件
**输出：** 迁移文件、模式差异报告、优化建议

**使用方法：**
```bash
# Analyze current schema and suggest optimizations
python scripts/database_migration_tool.py --connection postgres://localhost/mydb --analyze
# Output: Missing indexes, N+1 query risks, and suggested migration files

# Generate migration from schema diff
python scripts/database_migration_tool.py --connection postgres://localhost/mydb \
  --compare schema/v2.sql --output migrations/

# Dry-run a migration
python scripts/database_migration_tool.py --connection postgres://localhost/mydb \
  --migrate migrations/20240115_add_user_indexes.sql --dry-run
```

---

### 3. API 负载测试工具

执行可配置的并发负载测试，测量延迟百分位数和吞吐量。

**输入：** API 端点 URL 和测试配置
**输出：** 性能报告（包含延迟分布、错误率、吞吐量指标）

**使用方法：**
```bash
# Basic load test
python scripts/api_load_tester.py https://api.example.com/users --concurrency 50 --duration 30
# Output: Throughput (req/sec), latency percentiles (P50/P95/P99), error counts, and scaling recommendations

# Test with custom headers and body
python scripts/api_load_tester.py https://api.example.com/orders \
  --method POST \
  --header "Authorization: Bearer token123" \
  --body '{"product_id": 1, "quantity": 2}' \
  --concurrency 100 \
  --duration 60

# Compare two endpoints
python scripts/api_load_tester.py https://api.example.com/v1/users https://api.example.com/v2/users \
  --compare --concurrency 50 --duration 30
```

---

## 后端开发工作流程

### API 设计流程

用于设计新 API 或重构现有端点。

**步骤 1：定义资源及操作**  
```yaml
# openapi.yaml
openapi: 3.0.3
info:
  title: User Service API
  version: 1.0.0
paths:
  /users:
    get:
      summary: List users
      parameters:
        - name: "limit"
          in: query
          schema:
            type: integer
            default: 20
    post:
      summary: Create user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUser'
```

**步骤 2：生成路由框架**  
```bash
python scripts/api_scaffolder.py openapi.yaml --framework express --output src/routes/
```

**步骤 3：实现业务逻辑**  
```typescript
// src/routes/users.ts (generated, then customized)
export const createUser = async (req: Request, res: Response) => {
  const { email, name } = req.body;

  // Add business logic
  const user = await userService.create({ email, name });

  res.status(201).json(user);
};
```

**步骤 4：添加验证中间件**  
```bash
# Validation is auto-generated from OpenAPI schema
# src/middleware/validators.ts includes:
# - Request body validation
# - Query parameter validation
# - Path parameter validation
```

**步骤 5：生成更新的 OpenAPI 规范**  
```bash
python scripts/api_scaffolder.py src/routes/ --generate-spec --output openapi.yaml
```

---

### 数据库优化流程

当查询速度较慢或需要提升数据库性能时使用。

**步骤 1：分析当前性能**  
```bash
python scripts/database_migration_tool.py --connection $DATABASE_URL --analyze
```

**步骤 2：识别慢查询**  
```sql
-- Check query execution plans
EXPLAIN ANALYZE SELECT * FROM orders
WHERE user_id = 123
ORDER BY created_at DESC
LIMIT 10;

-- Look for: Seq Scan (bad), Index Scan (good)
```

**步骤 3：生成索引迁移脚本**  
```bash
python scripts/database_migration_tool.py --connection $DATABASE_URL \
  --suggest-indexes --output migrations/
```

**步骤 4：测试迁移脚本（模拟运行）**  
```bash
python scripts/database_migration_tool.py --connection $DATABASE_URL \
  --migrate migrations/add_indexes.sql --dry-run
```

**步骤 5：应用并验证**  
```bash
# Apply migration
python scripts/database_migration_tool.py --connection $DATABASE_URL \
  --migrate migrations/add_indexes.sql

# Verify improvement
python scripts/database_migration_tool.py --connection $DATABASE_URL --analyze
```

---

### 安全加固流程

在 API 准备上线或经过安全审查后使用。

**步骤 1：审查认证机制**  
```typescript
// Verify JWT configuration
const jwtConfig = {
  secret: process.env.JWT_SECRET,  // Must be from env, never hardcoded
  expiresIn: '1h',                 // Short-lived tokens
  algorithm: 'RS256'               // Prefer asymmetric
};
```

**步骤 2：添加速率限制**  
```typescript
import rateLimit from 'express-rate-limit';

const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,  // 15 minutes
  max: 100,                   // 100 requests per window
  standardHeaders: true,
  legacyHeaders: false,
});

app.use('/api/', apiLimiter);
```

**步骤 3：验证所有输入数据**  
```typescript
import { z } from 'zod';

const CreateUserSchema = z.object({
  email: z.string().email().max(255),
  name: "zstringmin1max100"
  age: z.number().int().positive().optional()
});

// Use in route handler
const data = CreateUserSchema.parse(req.body);
```

**步骤 4：使用攻击模式进行负载测试**  
```bash
# Test rate limiting
python scripts/api_load_tester.py https://api.example.com/login \
  --concurrency 200 --duration 10 --expect-rate-limit

# Test input validation
python scripts/api_load_tester.py https://api.example.com/users \
  --method POST \
  --body '{"email": "not-an-email"}' \
  --expect-status 400
```

**步骤 5：审查安全响应头**  
```typescript
import helmet from 'helmet';

app.use(helmet({
  contentSecurityPolicy: true,
  crossOriginEmbedderPolicy: true,
  crossOriginOpenerPolicy: true,
  crossOriginResourcePolicy: true,
  hsts: { maxAge: 31536000, includeSubDomains: true },
}));
```

---

## 参考文档

| 文件 | 内容 | 使用场景 |
|------|----------|----------|
| `references/api_design_patterns.md` | REST 与 GraphQL 的区别、版本控制、错误处理、分页 | 设计新 API |
| `references/database_optimization_guide.md` | 索引策略、查询优化、N+1 解决方案 | 优化查询速度 |
| `references/backend_security_practices.md` | OWASP 十大安全漏洞、认证模式、输入验证 | 强化系统安全性 |

---

## 常见模式快速参考

### REST API 响应格式  
```json
{
  "data": { "id": 1, "name": "John" },
  "meta": { "requestId": "abc-123" }
}
```

### 错误响应格式  
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email format",
    "details": [{ "field": "email", "message": "must be valid email" }]
  },
  "meta": { "requestId": "abc-123" }
}
```

### HTTP 状态码  
| 代码 | 使用场景 |
|------|----------|
| 200 | 成功（GET、PUT、PATCH） |
| 201 | 创建成功（POST） |
| 204 | 无内容（DELETE） |
| 400 | 验证错误 |
| 401 | 需要认证 |
| 403 | 没有权限 |
| 404 | 资源未找到 |
| 429 | 超过速率限制 |
| 500 | 服务器内部错误 |

### 数据库索引策略  
```sql
-- Single column (equality lookups)
CREATE INDEX idx_users_email ON users(email);

-- Composite (multi-column queries)
CREATE INDEX idx_orders_user_status ON orders(user_id, status);

-- Partial (filtered queries)
CREATE INDEX idx_orders_active ON orders(created_at) WHERE status = 'active';

-- Covering (avoid table lookup)
CREATE INDEX idx_users_email_name ON users(email) INCLUDE (name);
```

---

## 常用命令  
```bash
# API Development
python scripts/api_scaffolder.py openapi.yaml --framework express
python scripts/api_scaffolder.py src/routes/ --generate-spec

# Database Operations
python scripts/database_migration_tool.py --connection $DATABASE_URL --analyze
python scripts/database_migration_tool.py --connection $DATABASE_URL --migrate file.sql

# Performance Testing
python scripts/api_load_tester.py https://api.example.com/endpoint --concurrency 50
python scripts/api_load_tester.py https://api.example.com/endpoint --compare baseline.json
```