---
name: senior-backend
description: 当用户请求“设计 REST API”、“优化数据库查询”、“实现身份验证”、“构建微服务”、“审查后端代码”、“设置 GraphQL”、“处理数据库迁移”或“进行 API 性能测试”时，应使用此技能。该技能适用于 Node.js/Express/Fastify 开发、PostgreSQL 数据库优化、API 安全性以及后端架构设计。
---

# 高级后端工程师

负责后端开发模式、API设计、数据库优化以及安全实践。

## 目录

- [快速入门](#quick-start)
- [工具概述](#tools-overview)
  - [API搭建工具](#1-api-scaffolder)
  - [数据库迁移工具](#2-database-migration-tool)
  - [API负载测试工具](#3-api-load-tester)
- [后端开发工作流程](#backend-development-workflows)
  - [API设计工作流程](#api-design-workflow)
  - [数据库优化工作流程](#database-optimization-workflow)
  - [安全加固工作流程](#security-hardening-workflow)
- [参考文档](#reference-documentation)
- [常见模式快速参考](#common-patterns-quick-reference)

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

### 1. API搭建工具

根据数据库模式定义生成API路由处理程序、中间件以及OpenAPI规范。

**输入:** OpenAPI规范（YAML/JSON）或数据库模式
**输出:** 路由处理程序、验证中间件、TypeScript类型

**使用方法:**
```bash
# Generate Express routes from OpenAPI spec
python scripts/api_scaffolder.py openapi.yaml --framework express --output src/routes/

# Output:
# Generated 12 route handlers in src/routes/
# - GET /users (listUsers)
# - POST /users (createUser)
# - GET /users/{id} (getUser)
# - PUT /users/{id} (updateUser)
# - DELETE /users/{id} (deleteUser)
# ...
# Created validation middleware: src/middleware/validators.ts
# Created TypeScript types: src/types/api.ts

# Generate from database schema
python scripts/api_scaffolder.py --from-db postgres://localhost/mydb --output src/routes/

# Generate OpenAPI spec from existing routes
python scripts/api_scaffolder.py src/routes/ --generate-spec --output openapi.yaml
```

**支持的框架:**
- Express.js (`--framework express`)
- Fastify (`--framework fastify`)
- Koa (`--framework koa`)

---

### 2. 数据库迁移工具

分析数据库模式，检测变化，并生成带有回滚支持的迁移文件。

**输入:** 数据库连接字符串或模式文件
**输出:** 迁移文件、模式差异报告、优化建议

**使用方法:**
```bash
# Analyze current schema and suggest optimizations
python scripts/database_migration_tool.py --connection postgres://localhost/mydb --analyze

# Output:
# === Database Analysis Report ===
# Tables: 24
# Total rows: 1,247,832
#
# MISSING INDEXES (5 found):
#   orders.user_id - 847ms avg query time, ADD INDEX recommended
#   products.category_id - 234ms avg query time, ADD INDEX recommended
#
# N+1 QUERY RISKS (3 found):
#   users -> orders relationship (no eager loading)
#
# SUGGESTED MIGRATIONS:
#   1. Add index on orders(user_id)
#   2. Add index on products(category_id)
#   3. Add composite index on order_items(order_id, product_id)

# Generate migration from schema diff
python scripts/database_migration_tool.py --connection postgres://localhost/mydb \
  --compare schema/v2.sql --output migrations/

# Output:
# Generated migration: migrations/20240115_add_user_indexes.sql
# Generated rollback: migrations/20240115_add_user_indexes_rollback.sql

# Dry-run a migration
python scripts/database_migration_tool.py --connection postgres://localhost/mydb \
  --migrate migrations/20240115_add_user_indexes.sql --dry-run
```

---

### 3. API负载测试工具

执行可配置并发量的HTTP负载测试，测量延迟百分位数和吞吐量。

**输入:** API端点URL和测试配置
**输出:** 性能报告（包含延迟分布、错误率、吞吐量指标）

**使用方法:**
```bash
# Basic load test
python scripts/api_load_tester.py https://api.example.com/users --concurrency 50 --duration 30

# Output:
# === Load Test Results ===
# Target: https://api.example.com/users
# Duration: 30s | Concurrency: 50
#
# THROUGHPUT:
#   Total requests: 15,247
#   Requests/sec: 508.2
#   Successful: 15,102 (99.0%)
#   Failed: 145 (1.0%)
#
# LATENCY (ms):
#   Min: 12
#   Avg: 89
#   P50: 67
#   P95: 198
#   P99: 423
#   Max: 1,247
#
# ERRORS:
#   Connection timeout: 89
#   HTTP 503: 56
#
# RECOMMENDATION: P99 latency (423ms) exceeds 200ms target.
# Consider: connection pooling, query optimization, or horizontal scaling.

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

### API设计工作流程

用于设计新的API或重构现有端点。

**步骤1: 定义资源与操作**
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
        - name: limit
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

**步骤2: 生成路由框架**
```bash
python scripts/api_scaffolder.py openapi.yaml --framework express --output src/routes/
```

**步骤3: 实现业务逻辑**
```typescript
// src/routes/users.ts (generated, then customized)
export const createUser = async (req: Request, res: Response) => {
  const { email, name } = req.body;

  // Add business logic
  const user = await userService.create({ email, name });

  res.status(201).json(user);
};
```

**步骤4: 添加验证中间件**
```bash
# Validation is auto-generated from OpenAPI schema
# src/middleware/validators.ts includes:
# - Request body validation
# - Query parameter validation
# - Path parameter validation
```

**步骤5: 生成更新的OpenAPI规范**
```bash
python scripts/api_scaffolder.py src/routes/ --generate-spec --output openapi.yaml
```

---

### 数据库优化工作流程

当查询速度较慢或需要提升数据库性能时使用。

**步骤1: 分析当前性能**
```bash
python scripts/database_migration_tool.py --connection $DATABASE_URL --analyze
```

**步骤2: 识别慢速查询**
```sql
-- Check query execution plans
EXPLAIN ANALYZE SELECT * FROM orders
WHERE user_id = 123
ORDER BY created_at DESC
LIMIT 10;

-- Look for: Seq Scan (bad), Index Scan (good)
```

**步骤3: 生成索引迁移脚本**
```bash
python scripts/database_migration_tool.py --connection $DATABASE_URL \
  --suggest-indexes --output migrations/
```

**步骤4: 测试迁移（预运行）**
```bash
python scripts/database_migration_tool.py --connection $DATABASE_URL \
  --migrate migrations/add_indexes.sql --dry-run
```

**步骤5: 应用并验证**
```bash
# Apply migration
python scripts/database_migration_tool.py --connection $DATABASE_URL \
  --migrate migrations/add_indexes.sql

# Verify improvement
python scripts/database_migration_tool.py --connection $DATABASE_URL --analyze
```

---

### 安全加固工作流程

在API准备上线或经过安全审查后使用。

**步骤1: 审查认证设置**
```typescript
// Verify JWT configuration
const jwtConfig = {
  secret: process.env.JWT_SECRET,  // Must be from env, never hardcoded
  expiresIn: '1h',                 // Short-lived tokens
  algorithm: 'RS256'               // Prefer asymmetric
};
```

**步骤2: 添加速率限制**
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

**步骤3: 验证所有输入数据**
```typescript
import { z } from 'zod';

const CreateUserSchema = z.object({
  email: z.string().email().max(255),
  name: z.string().min(1).max(100),
  age: z.number().int().positive().optional()
});

// Use in route handler
const data = CreateUserSchema.parse(req.body);
```

**步骤4: 使用攻击模式进行负载测试**
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

**步骤5: 审查安全头部信息**
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
| `references/api_design_patterns.md` | REST与GraphQL的对比、版本控制、错误处理、分页 | 设计新API |
| `references/database_optimization_guide.md` | 索引策略、查询优化、N+1解决方案 | 修复慢速查询问题 |
| `references/background_security_practices.md` | OWASP十大安全漏洞、认证模式、输入验证 | 安全加固 |

---

## 常见模式快速参考

### REST API响应格式
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

### HTTP状态码
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