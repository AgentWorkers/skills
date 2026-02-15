---
model: standard
description: |
  WHAT: Production-ready Node.js backend patterns - Express/Fastify setup, layered architecture, 
  middleware, error handling, validation, database integration, authentication, and caching.
  
  WHEN: User is building REST APIs, setting up Node.js servers, implementing authentication, 
  integrating databases, adding validation/caching, or structuring backend applications.
  
  KEYWORDS: nodejs, node, express, fastify, typescript, api, rest, middleware, authentication, 
  jwt, validation, zod, postgres, mongodb, redis, caching, rate limiting, error handling
---

# Node.js 后端开发模式

这些模式用于使用 TypeScript 构建可扩展、易于维护的 Node.js 后端应用程序。

## 绝对不要做的事情

- **绝不要将敏感信息存储在代码中**：使用环境变量，切勿硬编码凭证。
- **绝不要跳过输入验证**：在中间件层使用 Zod/Joi 对所有输入进行验证。
- **绝不要在生产环境中暴露错误细节**：返回通用错误信息，将错误日志记录在服务器端。
- **绝不要使用 `any` 类型**：TypeScript 类型可以预防运行时错误。
- **绝不要省略错误处理**：始终为异步处理函数添加错误处理逻辑，并使用全局错误中间件。
- **绝不要使用同步操作**：对于 I/O 操作，使用 `async/await`；处理函数中切勿使用 `fs.readFileSync`。
- **绝不要信任客户端输入**：对所有请求参数进行清洗、验证和参数化。

## 适用场景

- 使用 Express 或 Fastify 构建 REST API。
- 设置中间件管道和错误处理机制。
- 实现身份验证和授权功能。
- 通过连接池和事务集成数据库。
- 添加输入验证、缓存和速率限制功能。

## 项目结构 — 分层架构

```
src/
├── controllers/     # Handle HTTP requests/responses
├── services/        # Business logic
├── repositories/    # Data access layer
├── models/          # Data models and types
├── middleware/      # Auth, validation, logging, errors
├── routes/          # Route definitions
├── config/          # Database, cache, env configuration
└── utils/           # Helpers, custom errors, response formatting
```

控制器负责处理 HTTP 请求，服务层包含业务逻辑，数据访问层负责抽象数据操作。每一层仅调用其下层的服务。

## Express 的配置方式

```typescript
import express from "express";
import helmet from "helmet";
import cors from "cors";
import compression from "compression";

const app = express();

app.use(helmet());
app.use(cors({ origin: process.env.ALLOWED_ORIGINS?.split(",") }));
app.use(compression());
app.use(express.json({ limit: "10mb" }));
app.use(express.urlencoded({ extended: true, limit: "10mb" }));
```

## Fastify 的配置方式

```typescript
import Fastify from "fastify";
import helmet from "@fastify/helmet";
import cors from "@fastify/cors";

const fastify = Fastify({
  logger: { level: process.env.LOG_LEVEL || "info" },
});

await fastify.register(helmet);
await fastify.register(cors, { origin: true });

// Type-safe routes with built-in schema validation
fastify.post<{ Body: { name: string; email: string } }>(
  "/users",
  {
    schema: {
      body: {
        type: "object",
        required: ["name", "email"],
        properties: {
          name: { type: "string", minLength: 1 },
          email: { type: "string", format: "email" },
        },
      },
    },
  },
  async (request) => {
    const { name, email } = request.body;
    return { id: "123", name };
  },
);
```

## 错误处理

### 自定义错误类

```typescript
export class AppError extends Error {
  constructor(
    public message: string,
    public statusCode: number = 500,
    public isOperational: boolean = true,
  ) {
    super(message);
    Object.setPrototypeOf(this, AppError.prototype);
    Error.captureStackTrace(this, this.constructor);
  }
}

export class ValidationError extends AppError {
  constructor(message: string, public errors?: any[]) { super(message, 400); }
}
export class NotFoundError extends AppError {
  constructor(message = "Resource not found") { super(message, 404); }
}
export class UnauthorizedError extends AppError {
  constructor(message = "Unauthorized") { super(message, 401); }
}
export class ForbiddenError extends AppError {
  constructor(message = "Forbidden") { super(message, 403); }
}
```

### 全局错误处理中间件

```typescript
import { Request, Response, NextFunction } from "express";
import { AppError, ValidationError } from "../utils/errors";

export const errorHandler = (
  err: Error, req: Request, res: Response, next: NextFunction,
) => {
  if (err instanceof AppError) {
    return res.status(err.statusCode).json({
      status: "error",
      message: err.message,
      ...(err instanceof ValidationError && { errors: err.errors }),
    });
  }

  // Don't leak details in production
  const message = process.env.NODE_ENV === "production"
    ? "Internal server error"
    : err.message;

  res.status(500).json({ status: "error", message });
};

// Wrap async route handlers to forward errors
export const asyncHandler = (
  fn: (req: Request, res: Response, next: NextFunction) => Promise<any>,
) => (req: Request, res: Response, next: NextFunction) => {
  Promise.resolve(fn(req, res, next)).catch(next);
};
```

## 输入验证（使用 Zod）

```typescript
import { AnyZodObject, ZodError } from "zod";

export const validate = (schema: AnyZodObject) => {
  return async (req: Request, res: Response, next: NextFunction) => {
    try {
      await schema.parseAsync({
        body: req.body,
        query: req.query,
        params: req.params,
      });
      next();
    } catch (error) {
      if (error instanceof ZodError) {
        const errors = error.errors.map((e) => ({
          field: e.path.join("."),
          message: e.message,
        }));
        next(new ValidationError("Validation failed", errors));
      } else {
        next(error);
      }
    }
  };
};

// Usage
import { z } from "zod";
const createUserSchema = z.object({
  body: z.object({
    name: z.string().min(1),
    email: z.string().email(),
    password: z.string().min(8),
  }),
});
router.post("/users", validate(createUserSchema), userController.createUser);
```

## 身份验证 — JWT（JSON Web Tokens）

### 身份验证中间件

```typescript
import jwt from "jsonwebtoken";

interface JWTPayload { userId: string; email: string; }

export const authenticate = async (
  req: Request, res: Response, next: NextFunction,
) => {
  try {
    const token = req.headers.authorization?.replace("Bearer ", "");
    if (!token) throw new UnauthorizedError("No token provided");

    req.user = jwt.verify(token, process.env.JWT_SECRET!) as JWTPayload;
    next();
  } catch {
    next(new UnauthorizedError("Invalid token"));
  }
};

export const authorize = (...roles: string[]) => {
  return (req: Request, res: Response, next: NextFunction) => {
    if (!req.user) return next(new UnauthorizedError("Not authenticated"));
    if (!roles.some((r) => req.user?.roles?.includes(r))) {
      return next(new ForbiddenError("Insufficient permissions"));
    }
    next();
  };
};
```

### 身份验证服务

```typescript
export class AuthService {
  constructor(private userRepository: UserRepository) {}

  async login(email: string, password: string) {
    const user = await this.userRepository.findByEmail(email);
    if (!user || !(await bcrypt.compare(password, user.password))) {
      throw new UnauthorizedError("Invalid credentials");
    }

    return {
      token: jwt.sign(
        { userId: user.id, email: user.email },
        process.env.JWT_SECRET!,
        { expiresIn: "15m" },
      ),
      refreshToken: jwt.sign(
        { userId: user.id },
        process.env.REFRESH_TOKEN_SECRET!,
        { expiresIn: "7d" },
      ),
      user: { id: user.id, name: user.name, email: user.email },
    };
  }
}
```

## 数据库相关模式

### PostgreSQL 连接池

```typescript
import { Pool, PoolConfig } from "pg";

const pool = new Pool({
  host: process.env.DB_HOST,
  port: parseInt(process.env.DB_PORT || "5432"),
  database: process.env.DB_NAME,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

pool.on("error", (err) => {
  console.error("Unexpected database error", err);
  process.exit(-1);
});

export const closeDatabase = async () => { await pool.end(); };
```

### 事务处理模式

```typescript
async createOrder(userId: string, items: OrderItem[]) {
  const client = await this.db.connect();
  try {
    await client.query("BEGIN");

    const { rows } = await client.query(
      "INSERT INTO orders (user_id, total) VALUES ($1, $2) RETURNING id",
      [userId, calculateTotal(items)],
    );
    const orderId = rows[0].id;

    for (const item of items) {
      await client.query(
        "INSERT INTO order_items (order_id, product_id, quantity, price) VALUES ($1, $2, $3, $4)",
        [orderId, item.productId, item.quantity, item.price],
      );
      await client.query(
        "UPDATE products SET stock = stock - $1 WHERE id = $2",
        [item.quantity, item.productId],
      );
    }

    await client.query("COMMIT");
    return orderId;
  } catch (error) {
    await client.query("ROLLBACK");
    throw error;
  } finally {
    client.release();
  }
}
```

## 速率限制

```typescript
import rateLimit from "express-rate-limit";
import RedisStore from "rate-limit-redis";
import Redis from "ioredis";

const redis = new Redis({ host: process.env.REDIS_HOST });

export const apiLimiter = rateLimit({
  store: new RedisStore({ client: redis, prefix: "rl:" }),
  windowMs: 15 * 60 * 1000,
  max: 100,
  standardHeaders: true,
  legacyHeaders: false,
});

export const authLimiter = rateLimit({
  store: new RedisStore({ client: redis, prefix: "rl:auth:" }),
  windowMs: 15 * 60 * 1000,
  max: 5,
  skipSuccessfulRequests: true,
});
```

## 使用 Redis 进行缓存

```typescript
import Redis from "ioredis";

const redis = new Redis({
  host: process.env.REDIS_HOST,
  retryStrategy: (times) => Math.min(times * 50, 2000),
});

export class CacheService {
  async get<T>(key: string): Promise<T | null> {
    const data = await redis.get(key);
    return data ? JSON.parse(data) : null;
  }

  async set(key: string, value: any, ttl?: number): Promise<void> {
    const serialized = JSON.stringify(value);
    ttl ? await redis.setex(key, ttl, serialized) : await redis.set(key, serialized);
  }

  async delete(key: string): Promise<void> { await redis.del(key); }

  async invalidatePattern(pattern: string): Promise<void> {
    const keys = await redis.keys(pattern);
    if (keys.length) await redis.del(...keys);
  }
}
```

## API 响应辅助函数

```typescript
export class ApiResponse {
  static success<T>(res: Response, data: T, message?: string, statusCode = 200) {
    return res.status(statusCode).json({ status: "success", message, data });
  }

  static paginated<T>(res: Response, data: T[], page: number, limit: number, total: number) {
    return res.json({
      status: "success",
      data,
      pagination: { page, limit, total, pages: Math.ceil(total / limit) },
    });
  }
}
```

## 最佳实践

1. **使用 TypeScript**：类型安全可以预防运行时错误。
2. **对所有输入进行验证**：在中间件层使用 Zod 或 Joi 进行验证。
3. **自定义错误类**：将错误映射到相应的 HTTP 状态码，并使用全局错误处理中间件。
4. **切勿硬编码敏感信息**：始终使用环境变量。
5. **结构化日志记录**：使用 Pino 或 Winston 并结合请求上下文记录日志。
6. **实施速率限制**：在分布式部署环境中使用 Redis 进行速率限制。
7. **使用连接池**：对数据库操作始终使用连接池。
8. **依赖注入**：通过构造函数注入依赖项以提高代码的可测试性。
9. **优雅地关闭系统**：在接收到 SIGTERM 信号时关闭数据库连接池并释放所有连接。
10. **健康检查**：使用 `/health` 端点进行系统健康状况检查。