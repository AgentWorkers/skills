# Node.js 与 TypeScript 的生产级工程实践

本文档提供了构建生产级 Node.js 后端应用的完整方法论，涵盖了架构设计、框架选择、错误处理、数据库模式、安全性、测试、可观测性以及部署等方面的内容。

---

## 快速健康检查（Quick Health Check）（/16）

请检查以下 8 项内容，得分范围为 0（未满足）到 2（全部满足）：

| 序号 | 检查项 | 是否满足 |
|---|--------|-------|
| 1 | 严格使用 TypeScript | `tsconfig` 中设置 `strict` 为 `true`，且不使用 `any` 类型 |
| 2 | 使用结构化的错误处理机制 | 使用自定义错误类并附带错误代码，而非简单的字符串错误信息 |
| 3 | 对所有外部接口进行输入验证 | 使用 Zod 或 Valibot 进行输入验证 |
| 4 | 数据库迁移操作 | 迁移操作受版本控制，可逆，并通过持续集成（CI）流程强制执行 |
| 5 | 健康检查接口 | 提供 `/health`（应用运行状态）和 `/ready`（应用准备就绪）接口，并进行依赖检查 |
| 6 | 结构化的日志记录 | 日志采用 JSON 格式，并包含请求 ID；在生产环境中禁止使用 `console.log` |
| 7 | 测试覆盖率 | 单元测试和集成测试的覆盖率超过 80%，尤其是关键路径 |
| 8 | 平稳优雅地关闭应用 | 应用在接收到 SIGTERM 信号时能够优雅关闭，并释放所有连接 |

**得分解释：** 0-6 分表示存在严重问题；8-10 分表示需要改进；12-14 分表示应用达到生产级标准；16 分表示应用已完全符合生产级要求。

---

## 第 1 阶段：架构与项目结构

### 框架选择矩阵

| 框架 | 适用场景 | 性能 | 生态系统 | 学习难度 | 对 TypeScript 的支持 |
|-----------|----------|-----------|-----------|----------------|------------|
| **Hono** | 适用于边缘计算/无服务器（serverless）场景，轻量级 API | 非常适合 | 发展迅速 | 对 TypeScript 的支持较低 |
| **Fastify** | 适用于高性能的单体应用和 JSON API | 非常适合 | 成熟稳定 | 对 TypeScript 的支持较好 |
| **Express** | 适用于传统应用，拥有丰富的中间件生态系统 | 非常适合 | 对 TypeScript 的支持较低 |
| **NestJS** | 适用于企业级应用和大型团队，依赖注入（DI）需求较高 | 非常适合 | 对 TypeScript 的支持较好 |
| **Elysia** | 以 Bun 为基础构建的类型安全 API | 非常适合 | 对 TypeScript 的支持较低 |
| **tRPC** | 全栈 TypeScript 应用，支持类型安全的远程过程调用（RPC） | 不直接支持 TypeScript | 对 TypeScript 的支持较低 |

**决策建议：**
- 新项目或小团队 → 选择 **Hono**（轻量级、快速开发） |
- 需要处理大量请求的 JSON API → 选择 **Fastify**（性能优异） |
- 企业级应用，团队规模超过 10 人 → 选择 **NestJS**（结构清晰） |
- 需要使用全栈 TypeScript 的项目 → 选择 **tRPC**（类型安全） |
- 如果现有代码基于 Express → 逐步将 Express 代码迁移到新的框架 |

### 推荐的项目结构

```
src/
├── index.ts              # Entry point — bootstrap only
├── app.ts                # App factory (createApp)
├── config/
│   ├── env.ts            # Environment validation (Zod)
│   └── database.ts       # DB connection config
├── routes/
│   ├── index.ts          # Route registry
│   ├── users.ts          # /users routes
│   └── orders.ts         # /orders routes
├── services/
│   ├── user.service.ts   # Business logic
│   └── order.service.ts
├── repositories/
│   ├── user.repo.ts      # Data access (Drizzle/Prisma)
│   └── order.repo.ts
├── middleware/
│   ├── auth.ts           # Authentication
│   ├── validate.ts       # Request validation
│   ├── error-handler.ts  # Global error handler
│   └── request-id.ts     # Correlation ID
├── errors/
│   └── index.ts          # Custom error classes
├── types/
│   └── index.ts          # Shared types
├── utils/
│   └── index.ts          # Pure utility functions
├── jobs/                 # Background jobs/queues
│   └── email.job.ts
└── __tests__/            # Tests mirror src/ structure
    ├── services/
    └── routes/
drizzle/                  # Database migrations
├── 0001_create_users.sql
└── meta/
tsconfig.json
package.json
Dockerfile
docker-compose.yml
.env.example
```

---

### 7 条架构原则

1. **路由 → 服务 → 数据库仓库**：务必遵循这一层次结构 |
2. **服务中包含业务逻辑**：路由层仅负责请求验证和调用服务，不处理业务逻辑 |
3. **数据库仓库负责数据访问**：服务层不应直接导入数据库客户端 |
4. **避免循环依赖**：依赖关系必须严格向下传递 |
5. **每个文件只导出一个函数**：这样有助于代码的可预测性和测试的便利性 |
6. **配置在启动时进行验证**：确保配置错误能立即被发现，避免运行时出现问题 |
7. **每个函数不超过 50 行代码，每个文件不超过 300 行代码**：超出这些限制时应及时拆分代码 |

---

## 第 2 阶段：TypeScript 配置

### 生产环境的 `tsconfig.json` 文件配置

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "lib": ["ES2022"],
    "outDir": "dist",
    "rootDir": "src",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "noPropertyAccessFromIndexSignature": true,
    "exactOptionalPropertyTypes": true,
    "forceConsistentCasingInFileNames": true,
    "isolatedModules": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "skipLibCheck": true,
    "esModuleInterop": true
  },
  "include": ["src"],
  "exclude": ["node_modules", "dist", "**/*.test.ts"]
}
```

---

### 8 条 TypeScript 编写规范

1. **严禁使用 `any` 类型**：应使用 `unknown` 或具体的类型定义 |
2. **启用 `noUncheckedIndexedAccess` 配置**：强制对数组/对象访问进行空值检查 |
3. 为标识符定义类型别名 | 例如：`type UserId = string & { __brand: 'UserId' }`
4. 使用 Zod 生成类型定义 | 例如：`type User = z.infer<typename UserSchema>`
5. 使用区分式的联合类型表示状态 | 例如：`{ status: 'active'; data: T } | { status: 'error'; error: E }`
6. 使用 `satisfies` 而不是 `as` 进行类型检查 | 这有助于保持类型安全性 |
7. 将枚举定义为常量对象 | 例如：`const Status = { ACTIVE: 'active', INACTIVE: 'inactive } as const`
8. 在公共 API 中明确指定返回类型 | 确保函数返回类型清晰明确

### 类型别名定义示例

```typescript
// types/branded.ts
declare const __brand: unique symbol;
type Brand<T, B extends string> = T & { [__brand]: B };

export type UserId = Brand<string, 'UserId'>;
export type OrderId = Brand<string, 'OrderId'>;
export type Email = Brand<string, 'Email'>;

export function UserId(id: string): UserId { return id as UserId; }
export function Email(email: string): Email {
  if (!email.includes('@')) throw new ValidationError('Invalid email');
  return email as Email;
}
```

---

## 第 3 阶段：环境与配置

### 使用 Zod 进行配置验证

```typescript
// config/env.ts
import { z } from 'zod';

const EnvSchema = z.object({
  NODE_ENV: z.enum(['development', 'test', 'production']).default('development'),
  PORT: z.coerce.number().int().min(1).max(65535).default(3000),
  DATABASE_URL: z.string().url(),
  REDIS_URL: z.string().url().optional(),
  JWT_SECRET: z.string().min(32),
  JWT_EXPIRES_IN: z.string().default('15m'),
  LOG_LEVEL: z.enum(['fatal', 'error', 'warn', 'info', 'debug', 'trace']).default('info'),
  CORS_ORIGINS: z.string().transform(s => s.split(',')).default('*'),
  RATE_LIMIT_MAX: z.coerce.number().default(100),
  RATE_LIMIT_WINDOW_MS: z.coerce.number().default(60_000),
});

export type Env = z.infer<typeof EnvSchema>;

// Validate at import time — fail fast
const parsed = EnvSchema.safeParse(process.env);
if (!parsed.success) {
  console.error('❌ Invalid environment variables:', parsed.error.flatten().fieldErrors);
  process.exit(1);
}

export const env = parsed.data;
```

---

### 5 条配置原则

1. **在启动时验证所有环境变量**：避免在运行时直接读取 `process.env` |
2. **仅允许类型安全的访问方式**：通过 `env` 对象访问环境变量 |
3. 重要配置信息应存储在安全的地方（如 vault/env） | 避免将配置硬编码到代码中 |
4. 确保 `.env.example` 文件中的配置始终是最新的 | 为每个配置项添加描述和默认值 |
5. 根据环境不同设置不同的配置 | 使用 `NODE_ENV` 来区分不同的环境配置 |

---

## 第 4 阶段：错误处理架构

### 自定义错误处理机制

```typescript
// errors/index.ts
export class AppError extends Error {
  constructor(
    message: string,
    public readonly code: string,
    public readonly statusCode: number,
    public readonly details?: Record<string, unknown>,
  ) {
    super(message);
    this.name = this.constructor.name;
    Error.captureStackTrace(this, this.constructor);
  }
}

export class ValidationError extends AppError {
  constructor(message: string, details?: Record<string, unknown>) {
    super(message, 'VALIDATION_ERROR', 400, details);
  }
}

export class NotFoundError extends AppError {
  constructor(resource: string, id: string) {
    super(`${resource} not found: ${id}`, 'NOT_FOUND', 404, { resource, id });
  }
}

export class UnauthorizedError extends AppError {
  constructor(message = 'Authentication required') {
    super(message, 'UNAUTHORIZED', 401);
  }
}

export class ForbiddenError extends AppError {
  constructor(message = 'Insufficient permissions') {
    super(message, 'FORBIDDEN', 403);
  }
}

export class ConflictError extends AppError {
  constructor(message: string, details?: Record<string, unknown>) {
    super(message, 'CONFLICT', 409, details);
  }
}

export class RateLimitError extends AppError {
  constructor(retryAfterMs: number) {
    super('Too many requests', 'RATE_LIMITED', 429, { retryAfterMs });
  }
}
```

### 全局错误处理函数

```typescript
// middleware/error-handler.ts
import type { ErrorHandler } from 'hono';
import { AppError } from '../errors/index.js';
import { logger } from '../utils/logger.js';

export const errorHandler: ErrorHandler = (err, c) => {
  const requestId = c.get('requestId');

  if (err instanceof AppError) {
    if (err.statusCode >= 500) {
      logger.error({ err, requestId }, 'Server error');
    } else {
      logger.warn({ err, requestId }, 'Client error');
    }

    return c.json({
      error: { code: err.code, message: err.message, details: err.details },
    }, err.statusCode as any);
  }

  // Unexpected errors — don't leak internals
  logger.error({ err, requestId }, 'Unhandled error');
  return c.json({
    error: { code: 'INTERNAL_ERROR', message: 'An unexpected error occurred' },
  }, 500);
};
```

### 6 条错误处理规则

1. **自定义错误类型并在适当的位置捕获错误**：服务层抛出错误，由路由层或中间件层捕获 |
2. **禁止使用字符串作为错误信息**：始终使用 `throw new SomeError(message)` 来抛出错误 |
3. **避免泄露内部细节**：对于 5xx 错误，返回通用错误信息，并记录真实的错误原因 |
4. **包含错误代码**：提供机器可读的错误代码以便客户端处理 |
5. **尽早进行错误验证**：在业务逻辑执行之前使用 Zod 进行验证 |
6. **自动捕获异步错误**：使用支持异常处理的框架（如 Hono 或 Fastify）

---

## 第 5 阶段：输入验证

### 使用 Zod 定义输入验证规则

```typescript
// routes/users.ts
import { z } from 'zod';
import { zValidator } from '@hono/zod-validator';

const CreateUserSchema = z.object({
  email: z.string().email().max(255).toLowerCase(),
  name: z.string().min(1).max(100).trim(),
  role: z.enum(['user', 'admin']).default('user'),
});

const PaginationSchema = z.object({
  cursor: z.string().optional(),
  limit: z.coerce.number().int().min(1).max(100).default(20),
});

const UserIdParamSchema = z.object({
  id: z.string().uuid(),
});

// Usage with Hono
app.post('/users', zValidator('json', CreateUserSchema), async (c) => {
  const body = c.req.valid('json'); // Fully typed!
  const user = await userService.create(body);
  return c.json({ data: user }, 201);
});

app.get('/users', zValidator('query', PaginationSchema), async (c) => {
  const { cursor, limit } = c.req.valid('query');
  const result = await userService.list({ cursor, limit });
  return c.json({ data: result.items, nextCursor: result.nextCursor });
});
```

### 验证规则

1. **在接口层进行输入验证**：每个路由处理函数在调用服务之前都必须验证输入数据 |
2. **使用 Zod 定义数据结构**：从 Zod 中派生 TypeScript 类型，而不是反过来 |
3. 在 Zod 中进行数据转换（如 `.trim()`、`.toLowerCase()`、`.default()`） |
4. 重用常见的验证规则 | 例如：`PaginationSchema`、`DateRangeSchema`、`SortSchema` |
5. **验证路径参数**：确保路径参数符合预期格式（如 UUID、Slugs、数字 ID）

---

## 第 6 阶段：数据库模式

### 选择合适的 ORM（对象关系映射）框架

| ORM | 适用场景 | 类型安全性 | 迁移支持 | 查询构建器 | 学习难度 |
|-----|----------|-------------|-----------|---------------|----------------|
| **Drizzle** | 优先使用 SQL，适用于边缘计算场景，性能优异 | 非常适合 | 内置查询构建器 | 学习难度较低 |
| **Prisma** | 适用于快速开发，注重数据库模式的设计 | 非常适合 | 提供自定义查询构建器 | 学习难度较低 |
| **Kysely** | 适合 SQL 熟练的开发者，适用于复杂查询 | 非常适合 | 需要外部查询构建器 | 类型安全性较高 |
| **TypeORM** | 适用于传统项目，使用装饰器进行配置 | 非常适合 | 内置 ORM 功能 | 学习难度中等 |

**推荐选择：** Drizzle（适用于新项目，因为它符合 SQL 的思维模式，支持 TypeScript 的类型推断，且与边缘计算场景兼容）。

### Drizzle 数据库模式示例

```typescript
// drizzle/schema.ts
import { pgTable, text, timestamp, uuid, varchar, boolean, index } from 'drizzle-orm/pg-core';

export const users = pgTable('users', {
  id: uuid('id').primaryKey().defaultRandom(),
  email: varchar('email', { length: 255 }).notNull().unique(),
  name: varchar('name', { length: 100 }).notNull(),
  role: text('role', { enum: ['user', 'admin'] }).notNull().default('user'),
  isActive: boolean('is_active').notNull().default(true),
  createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
  updatedAt: timestamp('updated_at', { withTimezone: true }).notNull().defaultNow(),
}, (table) => [
  index('idx_users_email').on(table.email),
  index('idx_users_created').on(table.createdAt),
]);
```

### 数据库仓库设计规范

```typescript
// repositories/user.repo.ts
import { eq, desc, gt } from 'drizzle-orm';
import { db } from '../config/database.js';
import { users } from '../../drizzle/schema.js';
import type { UserId } from '../types/branded.js';
import { NotFoundError } from '../errors/index.js';

export class UserRepository {
  async findById(id: UserId) {
    const [user] = await db.select().from(users).where(eq(users.id, id)).limit(1);
    if (!user) throw new NotFoundError('User', id);
    return user;
  }

  async list(opts: { cursor?: string; limit: number }) {
    const query = db.select().from(users).orderBy(desc(users.createdAt)).limit(opts.limit + 1);
    if (opts.cursor) query.where(gt(users.id, opts.cursor));
    const rows = await query;
    const hasMore = rows.length > opts.limit;
    return { items: rows.slice(0, opts.limit), nextCursor: hasMore ? rows[opts.limit - 1].id : undefined };
  }

  async create(data: { email: string; name: string; role?: string }) {
    const [user] = await db.insert(users).values(data).returning();
    return user;
  }

  async update(id: UserId, data: Partial<{ name: string; role: string; isActive: boolean }>) {
    const [user] = await db.update(users).set({ ...data, updatedAt: new Date() }).where(eq(users.id, id)).returning();
    if (!user) throw new NotFoundError('User', id);
    return user;
  }
}
```

### 数据库使用规则

1. **使用基于游标的分页机制**：在用户界面展示数据时避免使用 OFFSET 参数 |
2. **迁移操作需受版本控制**：使用 `drizzle-kit` 生成迁移脚本，然后通过 CI 流程执行迁移 |
3. **使用连接池**：为每个进程分配至少 2 个数据库连接（最多 10 个连接）；对于无服务器场景，可以使用相应的数据库驱动程序 |
4. **进行事务处理**：使用 `db.transaction` 进行数据库操作 |
5. **为查询添加索引**：为 `WHERE` 和 `ORDER BY` 列添加索引，并监控查询性能 |
6. **开发环境使用 SQLite，生产环境使用 PostgreSQL**：Drizzle 支持这两种数据库，并提供统一的接口 |

---

## 第 7 阶段：认证与授权

### 使用 JWT 进行身份验证（以 Hono 为例）

```typescript
// middleware/auth.ts
import { jwt } from 'hono/jwt';
import { env } from '../config/env.js';
import type { UserId } from '../types/branded.js';

type JwtPayload = { sub: UserId; role: 'user' | 'admin'; iat: number; exp: number };

export const authenticate = jwt({ secret: env.JWT_SECRET });

export const requireRole = (...roles: string[]) => {
  return async (c: any, next: any) => {
    const payload = c.get('jwtPayload') as JwtPayload;
    if (!roles.includes(payload.role)) {
      throw new ForbiddenError(`Required role: ${roles.join(' or ')}`);
    }
    await next();
  };
};
```

### 安全性检查清单

| 序号 | 安全性措施 | 优先级 |
|---|------|----------|
| 1 | 使用 Helmet 和安全头部（CSP、HSTS、X-Frame） | 高优先级 |
| 2 | 对每个 IP 和用户实施速率限制 | 高优先级 |
| 3 | 对所有接口进行输入验证 | 高优先级 |
| 4 | 配置 CORS（生产环境中不要使用通配符） | 高优先级 |
| 5 | 使用短生命周期的 JWT 和定期刷新令牌 | 高优先级 |
| 6 | 对密码进行加密处理（使用argon2id 算法） | 高优先级 |
| 7 | 防止 SQL 注入攻击 | 高优先级 |
| 8 | 限制请求大小（默认为 1MB） | 高优先级 |
| 9 | 定期进行依赖项审计 | 高优先级 |
| 10 | 为 API 设置不同的访问权限（只读/写入/管理员） | 高优先级 |

---

## 第 8 阶段：结构化的日志记录与可观测性

### 使用 Pino 进行日志记录

```typescript
// utils/logger.ts
import pino from 'pino';
import { env } from '../config/env.js';

export const logger = pino({
  level: env.LOG_LEVEL,
  ...(env.NODE_ENV === 'development' && { transport: { target: 'pino-pretty' } }),
  serializers: { err: pino.stdSerializers.err },
  redact: ['req.headers.authorization', '*.password', '*.token', '*.secret'],
  formatters: {
    level: (label) => ({ level: label }),
  },
});
```

### 请求 ID 处理机制

```typescript
// middleware/request-id.ts
import { randomUUID } from 'node:crypto';

export const requestId = () => {
  return async (c: any, next: any) => {
    const id = c.req.header('x-request-id') || randomUUID();
    c.set('requestId', id);
    c.header('x-request-id', id);
    await next();
  };
};
```

### 请求日志记录中间件

```typescript
// middleware/request-logger.ts
import { logger } from '../utils/logger.js';

export const requestLogger = () => {
  return async (c: any, next: any) => {
    const start = performance.now();
    const requestId = c.get('requestId');

    await next();

    const duration = Math.round(performance.now() - start);
    const level = c.res.status >= 500 ? 'error' : c.res.status >= 400 ? 'warn' : 'info';

    logger[level]({
      requestId,
      method: c.req.method,
      path: c.req.path,
      status: c.res.status,
      durationMs: duration,
      userAgent: c.req.header('user-agent'),
    }, `${c.req.method} ${c.req.path} ${c.res.status} ${duration}ms`);
  };
};
```

### 健康检查接口

```typescript
// routes/health.ts
app.get('/health', (c) => c.json({ status: 'ok', timestamp: new Date().toISOString() }));

app.get('/ready', async (c) => {
  const checks = {
    database: false,
    redis: false,
  };

  try {
    await db.execute(sql`SELECT 1`);
    checks.database = true;
  } catch {}

  try {
    await redis.ping();
    checks.redis = true;
  } catch {}

  const ready = Object.values(checks).every(Boolean);
  return c.json({ status: ready ? 'ready' : 'degraded', checks }, ready ? 200 : 503);
});
```

---

## 第 9 阶段：测试策略

### 测试层次结构

| 测试类型 | 目标覆盖范围 | 使用工具 | 测试内容 |
|-------|----------------|-------|-------------|
| **单元测试** | 覆盖 80% 以上的代码 | 使用 Vitest | 服务层、工具函数、纯逻辑部分 |
| **集成测试** | 测试关键路径 | 使用 Vitest 和 testcontainers | 路由层与数据库之间的交互 |
| **端到端测试** | 测试正常业务流程 | 使用 Vitest 和 supertest | 完整的 HTTP 请求流程 |
| **契约测试** | 验证 API 接口的契约遵守情况 | 使用 Vitest | |

### Vitest 配置示例

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    include: ['src/**/*.test.ts'],
    coverage: { provider: 'v8', reporter: ['text', 'lcov'], thresholds: { lines: 80, branches: 75 } },
    setupFiles: ['./src/__tests__/setup.ts'],
    pool: 'forks', // Isolation for DB tests
  },
});
```

### 服务单元测试示例

```typescript
// __tests__/services/user.service.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { UserService } from '../../services/user.service.js';
import type { UserRepository } from '../../repositories/user.repo.js';

describe('UserService', () => {
  let service: UserService;
  let repo: jest.Mocked<UserRepository>;

  beforeEach(() => {
    repo = { findById: vi.fn(), create: vi.fn(), update: vi.fn(), list: vi.fn() } as any;
    service = new UserService(repo);
  });

  it('creates user with normalized email', async () => {
    repo.create.mockResolvedValue({ id: '1', email: 'test@example.com', name: 'Test' } as any);
    const result = await service.create({ email: 'Test@Example.COM', name: 'Test' });
    expect(repo.create).toHaveBeenCalledWith(expect.objectContaining({ email: 'test@example.com' }));
    expect(result.email).toBe('test@example.com');
  });
});
```

### 集成测试示例

```typescript
// __tests__/routes/users.test.ts
import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { createApp } from '../../app.js';
import { testDb, migrate, cleanup } from '../helpers/db.js';

describe('POST /users', () => {
  let app: any;

  beforeAll(async () => {
    await migrate(testDb);
    app = createApp({ db: testDb });
  });

  afterAll(async () => { await cleanup(testDb); });

  it('creates user and returns 201', async () => {
    const res = await app.request('/users', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: 'new@example.com', name: 'New User' }),
    });

    expect(res.status).toBe(201);
    const body = await res.json();
    expect(body.data.email).toBe('new@example.com');
  });

  it('rejects invalid email with 400', async () => {
    const res = await app.request('/users', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: 'not-an-email', name: 'Bad' }),
    });

    expect(res.status).toBe(400);
  });
});
```

### 7 条测试规则

1. **测试功能行为，而非实现细节**：验证函数的输出结果，而非内部方法调用 |
| 2. **每个测试都是独立的**：避免测试之间共享可变状态 |
| 3. 为测试用例添加明确的名称 | 例如：`it('拒绝过期的 JWT，并返回 401 错误')` |
| **单元测试快速执行，集成测试独立运行**：使用 `pool: 'forks` 机制进行数据库测试 |
| **在接口边界处使用模拟对象**：服务测试中使用模拟对象，集成测试中使用真实数据库 |
| **测试错误路径**：确保所有错误类型（400、404、409、500 等）都能被正确处理 |
| **持续集成（CI）强制要求达到一定的测试覆盖率**：如果覆盖率低于阈值，测试失败 |

---

## 第 10 阶段：优雅关闭与应用管理

### 实现优雅的应用关闭机制

```typescript
// index.ts
import { serve } from '@hono/node-server';
import { createApp } from './app.js';
import { logger } from './utils/logger.js';
import { env } from './config/env.js';
import { db } from './config/database.js';

const app = createApp();
const server = serve({ fetch: app.fetch, port: env.PORT });

logger.info({ port: env.PORT }, 'Server started');

const shutdown = async (signal: string) => {
  logger.info({ signal }, 'Shutdown signal received');

  // Stop accepting new connections
  server.close(() => { logger.info('HTTP server closed'); });

  // Drain existing work (give 10s)
  const timeout = setTimeout(() => {
    logger.error('Forced shutdown after timeout');
    process.exit(1);
  }, 10_000);

  try {
    // Close DB pool, Redis, queues, etc.
    await db.$client.end();
    logger.info('Database pool closed');
    clearTimeout(timeout);
    process.exit(0);
  } catch (err) {
    logger.error({ err }, 'Error during shutdown');
    process.exit(1);
  }
};

process.on('SIGTERM', () => shutdown('SIGTERM'));
process.on('SIGINT', () => shutdown('SIGINT'));

// Catch unhandled errors
process.on('unhandledRejection', (err) => {
  logger.fatal({ err }, 'Unhandled rejection');
  process.exit(1);
});
```

---

## 第 11 阶段：生产环境部署

### 多阶段的 Dockerfile 构建脚本

```dockerfile
# Build stage
FROM node:22-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --ignore-scripts
COPY tsconfig.json ./
COPY src/ src/
COPY drizzle/ drizzle/
RUN npm run build
RUN npm ci --omit=dev --ignore-scripts

# Production stage
FROM node:22-alpine
RUN apk add --no-cache tini dumb-init
WORKDIR /app
COPY --from=builder /app/dist dist/
COPY --from=builder /app/drizzle drizzle/
COPY --from=builder /app/node_modules node_modules/
COPY --from=builder /app/package.json .

ENV NODE_ENV=production
USER node
EXPOSE 3000
ENTRYPOINT ["tini", "--"]
CMD ["node", "dist/index.js"]
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
        env: { POSTGRES_DB: test, POSTGRES_PASSWORD: test }
        ports: ['5432:5432']
        options: >-
          --health-cmd pg_isready --health-interval 10s --health-timeout 5s --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 22, cache: npm }
      - run: npm ci
      - run: npm run lint
      - run: npm run typecheck
      - run: npm test -- --coverage
        env: { DATABASE_URL: 'postgresql://postgres:test@localhost:5432/test' }
      - run: npm run build
```

### 生产环境检查清单

**必填项：**
- 设置 `NODE_ENV=production` |
- 使用严格类型的 TypeScript（`tsc --noEmit` 命令编译代码） |
- 启动时验证所有环境变量 |
- 提供健康检查接口和应用准备就绪接口 |
- 应用在接收到 SIGTERM 信号时能够优雅关闭 |
- 使用结构化的 JSON 格式记录日志（禁止使用 `console.log`） |
- 错误处理机制不会泄露内部堆栈信息 |
- 启用速率限制 |
- 配置 CORS（不允许通配符请求） |
- 设置必要的安全头部

**推荐项：**
- 在所有日志中记录请求 ID |
- 配置数据库连接池 |
- 定期进行依赖项审计（使用 `npm audit`） |
- 保持 Docker 镜像大小在 200MB 以内 |
- 对响应数据进行压缩（使用 gzip 或 brotli） |
- 确定 API 的版本策略 |
- 配置监控和警报机制

---

## 第 12 阶段：性能优化

### 优先考虑的优化措施

| 优化措施 | 影响程度 | 实施难度 |
|---|-----------|--------|--------|
| 1. 使用连接池（数据库和 Redis） | 高 | 较低 |
| 2. 使用缓存（Redis 或内存缓存） | 高 | 中等 |
| 3. 优化查询性能（使用索引等） | 高 | 中等 |
| 4. 优化 JSON 序列化格式 | 中等 | 低 |
| 5. 使用压缩中间件 | 中等 | 低 |
| 6. 对大体积数据使用流式响应格式 | 中等 | 中等 |
| 7. 为 CPU 密集型任务分配线程 | 高 | 高 |
| 8. 使用 HTTP/2 协议和保持连接活跃（keep-alive） | 低 | 低 |

### 常见的优化方法

```typescript
// N+1 prevention — batch with dataloader or SQL JOIN
// ❌ Bad: for loop with individual queries
for (const order of orders) {
  order.user = await db.query.users.findFirst({ where: eq(users.id, order.userId) });
}

// ✅ Good: single query with join
const ordersWithUsers = await db
  .select()
  .from(orders)
  .leftJoin(users, eq(orders.userId, users.id))
  .where(inArray(orders.id, orderIds));

// In-memory caching for hot data
import { LRUCache } from 'lru-cache';
const cache = new LRUCache<string, any>({ max: 1000, ttl: 60_000 });

async function getCachedUser(id: string) {
  const cached = cache.get(id);
  if (cached) return cached;
  const user = await userRepo.findById(id);
  cache.set(id, user);
  return user;
}
```

---

## 第 13 阶段：后台任务与队列管理

### 使用 BullMQ 进行任务调度

```typescript
// jobs/email.job.ts
import { Queue, Worker } from 'bullmq';
import { env } from '../config/env.js';
import { logger } from '../utils/logger.js';

const connection = { url: env.REDIS_URL };

export const emailQueue = new Queue('email', { connection });

export const emailWorker = new Worker('email', async (job) => {
  const { to, subject, body } = job.data;
  logger.info({ jobId: job.id, to }, 'Sending email');
  // Send via provider
  await sendEmail({ to, subject, body });
}, {
  connection,
  concurrency: 5,
  limiter: { max: 10, duration: 1000 }, // 10 per second
});

emailWorker.on('failed', (job, err) => {
  logger.error({ jobId: job?.id, err }, 'Email job failed');
});
```

### 任务管理规则

1. **确保任务是幂等的**：相同的任务 ID 两次执行会产生相同的结果 |
| 2. 对于临时性的失败，采用指数级退避策略 | 
| 3. 失败的任务会被放入死信队列（DLQ）进行后续处理 |
| 4. 为任务设置超时机制 | 设置 `removeOnComplete` 和 `removeOnFail` 等定时器 |
| 5. 监控队列的状态 | 监控队列的长度、处理时间和失败率 |

---

## 第 14 阶段：高级开发技巧

### 手动实现依赖注入

```typescript
// app.ts — compose dependencies explicitly
export function createApp(deps?: { db?: Database; redis?: Redis }) {
  const database = deps?.db ?? defaultDb;
  const app = new Hono();

  // Compose service graph
  const userRepo = new UserRepository(database);
  const userService = new UserService(userRepo);

  // Mount routes with injected services
  app.route('/users', createUserRoutes(userService));

  return app;
}
```

### 实施速率限制

```typescript
// middleware/rate-limit.ts (using hono-rate-limiter)
import { rateLimiter } from 'hono-rate-limiter';

export const apiRateLimit = rateLimiter({
  windowMs: 60_000,
  limit: 100,
  keyGenerator: (c) => c.get('jwtPayload')?.sub || c.req.header('x-forwarded-for') || 'anonymous',
  message: { error: { code: 'RATE_LIMITED', message: 'Too many requests' } },
});
```

### 使用 WebSocket 进行实时通信（以 Hono 和 @hono/node-ws 为例）

```typescript
import { createNodeWebSocket } from '@hono/node-ws';

const { injectWebSocket, upgradeWebSocket } = createNodeWebSocket({ app });

app.get('/ws', upgradeWebSocket((c) => ({
  onOpen(evt, ws) { logger.info('WebSocket connected'); },
  onMessage(evt, ws) {
    const data = JSON.parse(evt.data.toString());
    // Handle message
    ws.send(JSON.stringify({ type: 'ack', id: data.id }));
  },
  onClose() { logger.info('WebSocket disconnected'); },
})));
```

---

## 2025 年推荐的开发栈

| 技术栈组件 | 推荐版本 | 替代方案 |
|-------|-------------|-------------|
| **运行时环境** | Node.js 22 LTS | Bun |
| **框架** | Hono | Fastify |
| **编程语言** | TypeScript（严格类型检查） | 可选 |
| **输入验证** | Zod | Valibot |
| **对象关系映射（ORM）** | Drizzle | Prisma |
| **数据库** | PostgreSQL | SQLite（开发环境） |
| **缓存** | Redis 或 Upstash | 使用 LRU 算法进行内存缓存 |
| **认证机制** | JWT 和刷新令牌 | Lucia 或 Better Auth |
| **任务队列** | BullMQ | pg-boss |
| **测试工具** | Vitest | 可选 |
| **代码检查工具** | Pino | ESLint 和 Prettier |
| **持续集成/持续部署（CI/CD）** | GitHub Actions | 可选 |
| **部署工具** | Docker 和 Railway/Fly | Vercel（无服务器部署方案） |

---

## 开发规范（10 条）

1. **在接口层进行严格的数据验证**：使用 Zod 对所有输入数据进行验证 |
2. **在启动时立即发现错误**：确保环境变量、数据库连接和迁移操作都能正确处理 |
| ** everywhere 使用结构化的日志记录**：采用 JSON 格式记录日志，并包含请求 ID |
| **使用自定义错误类型**：避免使用简单的字符串错误信息 |
| **使用基于游标的分页机制**：避免使用 OFFSET 参数 |
| **实现优雅的应用关闭机制**：应用在接收到 SIGTERM 信号时能够优雅关闭 |
| **确保所有错误路径都能被正确处理**：4xx/5xx 错误比正常请求更重要 |
| **明确指定所有数据的类型**：避免使用 `any` 类型，使用具体的类型别名和 Zod 生成的类型 |
| **默认采用安全措施**：实施速率限制、使用 Helmet 安全头部、配置 CORS、定期审计依赖项 |
| **保持代码简洁**：每个函数不超过 50 行代码，每个文件不超过 300 行 |

## 常见错误及解决方法

| 错误类型 | 常见问题 | 解决方案 |
|---|---------|-----|
| 1. 在生产环境中使用 `console.log` | 应使用 Pino 进行日志记录，并输出 JSON 格式的数据 |
| 2. 在所有地方使用 `any` 类型 | 应使用 `unknown` 类型并进行类型限定 |
| 3. 不对输入数据进行验证 | 在每个接口层使用 Zod 进行输入验证 |
| 4. 使用 OFFSET 进行分页 | 应使用基于游标的分页机制 |
| 5. 应用无法优雅关闭 | 在应用接收到 SIGTERM 信号时释放所有连接 |
| 6. 配置硬编码 | 在启动时使用 Zod 对环境变量进行验证 |
| 7. 控制器代码过于复杂 | 将功能拆分为多个服务，并将逻辑封装在服务层中 |
| 8. 不使用错误处理机制 | 为每个错误类型定义自定义的错误类 |
| 9. 只测试正常业务流程 | 必须测试所有类型的错误路径（400、404、409、500 等） |
| 10. 不记录请求信息 | 使用请求 ID 中间件进行请求追踪 |

## 质量评估（0-100 分）

| 评估维度 | 权重 | 评估内容 |
|-----------|--------|----------------|
| 类型安全性 | 20% | 严格使用 TypeScript，避免使用 `any` 类型，使用类型别名 |
| 错误处理 | 15% | 使用自定义错误处理机制，避免错误信息泄露 |
| 测试 | 15% | 单元测试和集成测试的覆盖率，覆盖关键路径 |
| 安全性 | 15% | 实施身份验证、输入验证、速率限制等安全措施 |
| 可观测性 | 10% | 使用结构化的日志记录和健康检查机制 |
| 性能 | 10% | 使用连接池、缓存等性能优化措施 |
| 代码结构 | 10% | 代码的层次结构清晰，文件大小合理，依赖项管理得当 |
| 部署 | 5% | 使用 Docker、持续集成/持续部署（CI/CD）等部署工具 |

---

## 特殊情况处理建议

### 初期项目/最小可行产品（MVP）开发

- 从使用 Hono、SQLite 和 Drizzle 开始开发，快速上线 |
- 在需要处理并发写操作时再引入 PostgreSQL |
- 在需要缓存或队列功能时再引入 Redis |

### 单一代码仓库（Monorepo）开发

- 共享代码包：使用 `@org/types`、`@org/db`、`@org/validation` 等包 |
- 每个服务都是独立的代码包，具有独立的构建和测试流程 |
- 使用工作空间协议：`"@org/types": "workspace:*"` 

### 无服务器（Serverless）开发

- Hono 可以在任何环境中运行，代码通用性强 |
- 使用相应的无服务器数据库驱动程序（如 Neon、PlanetScale、Turso） |
- 由于无状态设计，因此不需要实现优雅关闭机制

### 传统 Express 项目的迁移

- 逐步将代码迁移到 TypeScript（在 `.js` 文件旁边添加 `.ts` 文件） |
- 为每个 Express 路由添加 Zod 验证中间件 |
- 逐步将 `console.log` 替换为 Pino 日志记录工具 |
- 使用适配器逐个路由地迁移代码到 Hono 或 Fastify

## 常用命令

- “设置一个新的 TypeScript API 项目” → 执行第 1-3 阶段的开发工作 |
- “为我的 API 添加认证功能” → 执行第 7 阶段的开发工作 |
- “检查我的错误处理机制” → 执行第 4 阶段的开发工作 |
- “为我的项目添加数据库支持” → 执行第 6 阶段的开发工作 |
- “准备进行生产环境部署” → 执行第 11 阶段的部署准备工作 |
- “优化 API 性能” → 执行第 12 阶段的优化工作 |
- “添加后台任务” → 执行第 13 阶段的开发工作 |
- “审计我的 API 安全性” → 执行第 7 阶段的安全检查 |
- “配置日志记录和监控机制” → 执行第 8 阶段的开发工作 |
- “检查我的项目结构” → 执行第 1 阶段的代码审查工作 |
- “进行全面健康检查” → 执行快速健康检查并评估项目质量

---

⚡ 本文档由 [AfrexAI](https://afrexai-cto.github.io/context-packs/) 提供支持——基于人工智能的自动化工具。