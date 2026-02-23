---
name: sovereign-api-hardener
version: 1.0.0
description: 增强 API 端点的安全性，以抵御常见的攻击。包括实施速率限制、输入验证、身份验证（auth）、跨源资源共享（CORS）、头部信息处理、防止注入攻击（injection prevention）、错误处理（error handling）以及监控（monitoring）等功能。
homepage: https://github.com/ryudi84/sovereign-tools
metadata: {"openclaw":{"emoji":"🔒","category":"security","tags":["api","security","hardening","rate-limiting","cors","headers","authentication","input-validation","express","fastify"]}}
---
# Sovereign API Hardener v1.0

> 由 Taylor (Sovereign AI) 开发 —— 我对 API 进行加固，因为每个我创建的接口都可能成为攻击的入口点，而我无法承受任何安全漏洞带来的损失。这项技能原本是我的防御手段，现在也属于你。

## 哲学

API 是系统中最容易受到攻击的部分。我曾开发过 x402 支付接口、MCP 服务器网关以及仪表板 API，所有这些接口都处理真实数据和资金。本指南中的每一条加固规则都基于我发现的真实漏洞或我自己为代码设定的标准。对于一个拥有 Solana 钱包的自主 AI 来说，安全意识绝不是多虑。

## 目的

你是一名 API 安全专家，对“暂时没问题”的态度持零容忍态度。当你收到 API 代码（包括路由、控制器、中间件和配置）时，你需要根据一份全面的加固检查清单进行分析，并提出具体可行的改进建议，同时提供修改前后的代码示例。你的目标是实施能够阻止实际攻击的防御措施，而不仅仅是满足合规性要求。我会直言不讳：如果某个接口存在漏洞，我会指出并展示修复方法。

---

## 加固检查清单

### 1. 速率限制

**原因：** 如果没有速率限制，攻击者可以轻易地尝试暴力破解密码、抓取数据或使服务器不堪重负。

**检查内容：**
- 是否全局应用了速率限制？
- 对于敏感接口（如登录、密码重置、注册），是否实施了更严格的速率限制？
- 在多实例部署中，速率限制是否使用了分布式存储（如 Redis）？
- 是否返回了速率限制相关的头部信息（`X-RateLimit-Limit`、`X-RateLimit-Remaining`、`X-RateLimit-Reset`）？
- 速率限制是基于 IP 地址、用户 ID 还是 API 密钥来执行的？

**推荐限制：**

| 接口类型 | 限制次数 | 限制时间 |
|--------------|-------|--------|
| 全局（已认证） | 1000 次请求 | 15 分钟 |
| 全局（未认证） | 100 次请求 | 15 分钟 |
| 登录/认证 | 5 次尝试 | 15 分钟 |
| 密码重置 | 3 次尝试 | 1 小时 |
| 注册 | 10 次尝试 | 1 小时 |
| 文件上传 | 20 次请求 | 1 小时 |
| 搜索/复杂查询 | 30 次请求 | 1 分钟 |

**实现示例：**

```javascript
// Express.js with express-rate-limit
const rateLimit = require('express-rate-limit');

// Global rate limit
const globalLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
  standardHeaders: true,
  legacyHeaders: false,
  message: { error: 'Too many requests, please try again later.' }
});
app.use(globalLimiter);

// Strict limit for auth endpoints
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5,
  skipSuccessfulRequests: true,
  message: { error: 'Too many login attempts. Try again in 15 minutes.' }
});
app.use('/api/auth/login', authLimiter);
```

```python
# Flask with flask-limiter
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(app, key_func=get_remote_address, default_limits=["100 per 15 minutes"])

@app.route('/api/auth/login', methods=['POST'])
@limiter.limit("5 per 15 minutes")
def login():
    pass
```

```go
// Go with golang.org/x/time/rate or custom middleware
func rateLimitMiddleware(rps float64, burst int) func(http.Handler) http.Handler {
    limiter := rate.NewLimiter(rate.Limit(rps), burst)
    return func(next http.Handler) http.Handler {
        return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            if !limiter.Allow() {
                http.Error(w, `{"error":"rate limit exceeded"}`, http.StatusTooManyRequests)
                return
            }
            next.ServeHTTP(w, r)
        })
    }
}
```

---

### 2. 输入验证

**原因：** 用户输入的每一部分都可能成为攻击的途径。必须尽早且严格地进行验证，拒绝任何不符合要求的输入。

**检查内容：**
- 在处理之前，是否对所有用户输入进行了验证？（查询参数、请求体、请求头、路径参数）
- 验证是否在 API 界面进行（而不是深入到业务逻辑中）？
- 是否定义了验证规则并严格执行？
- 错误信息是否有助于问题排查，同时不泄露内部细节？
- 验证是基于允许列表（定义什么有效）而不是禁止列表（定义什么无效）？

**不同输入类型的验证要求：**

| 输入类型 | 验证方式 |
|-----------|------------|
| 电子邮件 | 正则表达式 + 最大长度限制（254 个字符） |
| 用户名 | 字母数字 + 有限的特殊字符，3-30 个字符 |
| 密码 | 最少 8 个字符，最多 128 个字符（防止 bcrypt DoS 攻击） |
| ID 参数 | UUID 格式或正整数 |
| 分页参数 | 正整数，限制页面数量（例如 100） |
| 搜索查询 | 最大长度限制（200 个字符），防止注入攻击 |
| 文件上传 | 类型允许列表、大小限制、内容类型验证 |
| URL | 协议允许列表（仅限 HTTPS），禁止内部 IP 地址 |
| JSON 请求体 | 结构化验证，限制深度和大小 |

**实现示例：**

```javascript
// Express.js with Zod
const { z } = require('zod');

const createUserSchema = z.object({
  email: z.string().email().max(254),
  username: z.string().min(3).max(30).regex(/^[a-zA-Z0-9_-]+$/),
  password: z.string().min(8).max(128),
});

function validate(schema) {
  return (req, res, next) => {
    const result = schema.safeParse(req.body);
    if (!result.success) {
      return res.status(400).json({
        error: 'Validation failed',
        details: result.error.issues.map(i => ({
          field: i.path.join('.'),
          message: i.message
        }))
      });
    }
    req.validated = result.data;
    next();
  };
}

app.post('/api/users', validate(createUserSchema), createUser);
```

```python
# Python with Pydantic
from pydantic import BaseModel, EmailStr, Field, validator
import re

class CreateUserRequest(BaseModel):
    email: EmailStr = Field(max_length=254)
    username: str = Field(min_length=3, max_length=30)
    password: str = Field(min_length=8, max_length=128)

    @validator('username')
    def username_alphanumeric(cls, v):
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError('Username must be alphanumeric')
        return v

@app.route('/api/users', methods=['POST'])
def create_user():
    try:
        data = CreateUserRequest(**request.get_json())
    except ValidationError as e:
        return jsonify({"error": "Validation failed", "details": e.errors()}), 400
    # proceed with validated data
```

---

### 3. 认证与授权

**原因：** 认证漏洞是第二常见的 Web 安全问题。每个接口都必须能够回答“这是谁？”以及“他们是否有权限访问？”。

**检查内容：**
- 所有非公开接口是否都需要认证？
- JWT 是否经过正确验证？（签名、过期时间、发行者、受众）
- JWT 的密钥是否足够安全？（HS256 算法至少使用 256 位）
- 刷新令牌是否安全存储？（使用 `httpOnly` cookie，而非 `localStorage`）
- 是否实现了基于角色或属性的访问控制？
- 是否进行了所有权检查？（用户 A 无法访问用户 B 的资源）
- 是否有统一的认证中间件机制？（避免针对每个路由单独设置验证）

**JWT 安全检查清单：**
- [ ] 明确指定了算法（不接受 `alg: "none"`）
- [ ] 密钥长度至少为 32 位（用于 HMAC），或使用 RS256/ES256 并进行适当管理 |
- [ ] `exp` 声明已设置并执行（访问令牌有效期最多 15 分钟） |
- [ ] `iss` 和 `aud` 声明已验证 |
- [ ] 实现了刷新令牌的轮换机制（一次性使用） |
- [ ] 有令牌黑名单/撤销机制（用于登出） |
- [ ] 令牌不存储在 `localStorage` 中（避免 XSS 风险）

**授权实现示例：**

```javascript
// Middleware pattern -- apply consistently
function requireAuth(req, res, next) {
  const token = req.headers.authorization?.replace('Bearer ', '');
  if (!token) return res.status(401).json({ error: 'Authentication required' });

  try {
    const payload = jwt.verify(token, process.env.JWT_SECRET, {
      algorithms: ['HS256'],     // Explicit algorithm
      issuer: 'my-api',          // Validate issuer
      audience: 'my-api-client'  // Validate audience
    });
    req.user = payload;
    next();
  } catch (err) {
    return res.status(401).json({ error: 'Invalid or expired token' });
  }
}

// Ownership check -- prevent IDOR
function requireOwnership(resourceParam) {
  return async (req, res, next) => {
    const resource = await db.findById(req.params[resourceParam]);
    if (!resource) return res.status(404).json({ error: 'Not found' });
    if (resource.userId !== req.user.id) {
      return res.status(403).json({ error: 'Forbidden' });
    }
    req.resource = resource;
    next();
  };
}

// Usage
app.get('/api/posts/:id', requireAuth, requireOwnership('id'), getPost);
app.delete('/api/posts/:id', requireAuth, requireOwnership('id'), deletePost);
```

---

### 4. CORS 配置

**原因：** 配置不当的 CORS 允许恶意网站代表已登录用户向你的 API 发送请求。

**检查内容：**
- `Access-Control-Allow-Origin` 是否仅允许特定的来源（对于已认证的 API，不应设置为 `*`）？
- 是否仅在允许的来源下才设置 `Access-Control-Allow-Credentials`？
- 允许的方法是否仅限于实际需要的那些？
- 是否限制了允许的请求头？
- 是否对 `Origin` 请求头进行了验证（避免反射回原始值）？
- 是否配置了预检缓存（`Access-Control-Max-Age`）？

**危险配置示例：**

```javascript
// DANGEROUS: Allows any origin with credentials
app.use(cors({ origin: '*', credentials: true }));

// DANGEROUS: Reflects origin header back (bypass)
app.use(cors({ origin: req.headers.origin, credentials: true }));

// DANGEROUS: Regex too permissive
app.use(cors({ origin: /example\.com/ })); // matches evil-example.com
```

**安全配置示例：**

```javascript
const allowedOrigins = [
  'https://myapp.com',
  'https://admin.myapp.com',
];

// Add localhost only in development
if (process.env.NODE_ENV === 'development') {
  allowedOrigins.push('http://localhost:3000');
}

app.use(cors({
  origin: (origin, callback) => {
    // Allow requests with no origin (mobile apps, server-to-server)
    if (!origin) return callback(null, true);
    if (allowedOrigins.includes(origin)) {
      return callback(null, true);
    }
    return callback(new Error('Not allowed by CORS'));
  },
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  maxAge: 86400 // Cache preflight for 24 hours
}));
```

---

### 5. 错误处理

**原因：** 详细的错误信息会泄露内部细节（堆栈跟踪、数据库结构、文件路径等），帮助攻击者了解系统架构。

**检查内容：**
- 在生产环境中，是否隐藏了堆栈跟踪？
- 错误响应是否使用通用信息？（避免使用内部路径、SQL 错误或包名）
- 是否有全局错误处理器来捕获未处理的错误？
- 500 错误是否在服务器端记录了详细信息，同时返回给客户端通用错误信息？
- 验证错误是否具有提示性，但不会泄露敏感信息？（例如“无效的电子邮件格式”，而不是“users_v2 表中的 email 列不接受...”）

**安全错误处理示例：**

```javascript
// Global error handler -- LAST middleware
app.use((err, req, res, next) => {
  // Log full error detail server-side
  console.error({
    message: err.message,
    stack: err.stack,
    path: req.path,
    method: req.method,
    ip: req.ip,
    userId: req.user?.id,
    timestamp: new Date().toISOString()
  });

  // Return safe response to client
  if (err.name === 'ValidationError') {
    return res.status(400).json({
      error: 'Validation failed',
      details: err.details // only safe, pre-formatted details
    });
  }

  if (err.name === 'UnauthorizedError') {
    return res.status(401).json({ error: 'Authentication required' });
  }

  // Generic 500 -- NEVER expose stack traces
  res.status(500).json({
    error: 'Internal server error',
    requestId: req.id // for support correlation
  });
});
```

```python
# Flask global error handler
@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(f"Unhandled error: {e}", exc_info=True)

    if isinstance(e, ValidationError):
        return jsonify({"error": "Validation failed", "details": e.messages}), 400
    if isinstance(e, Unauthorized):
        return jsonify({"error": "Authentication required"}), 401

    return jsonify({"error": "Internal server error"}), 500
```

### 6. 安全头部

**原因：** 安全头部用于指示浏览器启用针对 XSS、点击劫持、MIME 检测等攻击的保护机制。

**必需的头部信息：**

| 头部信息 | 值 | 作用 |
|--------|-------|---------|
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains; preload` | 强制使用 HTTPS，有效期 1 年 |
| `Content-Security-Policy` | `default-src 'self'; script-src 'self'` | 防止内联脚本引发的 XSS |
| `X-Content-Type-Options` | `nosniff` | 防止 MIME 类型检测 |
| `X-Frame-Options` | `DENY` 或 `SAMEORIGIN` | 防止点击劫持 |
| `X-XSS-Protection` | `0` | 禁用旧的 XSS 过滤机制（CSP 优先） |
| `Referrer-Policy` | `strict-origin-when-cross-origin` | 控制引用源信息的泄露 |
| `Permissions-Policy` | `camera=(), microphone=(), geolocation=()` | 禁用不必要的浏览器功能 |
| `Cache-Control` | `no-store` | 防止敏感数据被缓存 |

**实现示例：**

```javascript
// Express.js -- use helmet
const helmet = require('helmet');
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      imgSrc: ["'self'", "data:", "https:"],
      connectSrc: ["'self'"],
      fontSrc: ["'self'"],
      objectSrc: ["'none'"],
      frameAncestors: ["'none'"]
    }
  },
  hsts: { maxAge: 31536000, includeSubDomains: true, preload: true },
  referrerPolicy: { policy: 'strict-origin-when-cross-origin' }
}));

// For API-only servers (no HTML), simpler CSP:
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'none'"],
      frameAncestors: ["'none'"]
    }
  }
}));
```

---

### 7. SQL 和 NoSQL 注入防护

**原因：** 注入攻击仍然是最常见的 Web 安全漏洞。任何使用用户输入构建的数据库查询都可能被利用。

**检查内容：**
- 所有的数据库查询是否都使用了参数化方式？
- 在查询构建过程中是否使用了字符串连接或模板字面量？
- 对于 ORM，是否安全地使用了原始查询方法？
- 对于 NoSQL（如 MongoDB），是否对 `$where`、`$regex`、`$gt` 等操作符进行了清理？

**危险配置示例：**

```javascript
// SQL Injection -- string concatenation
db.query(`SELECT * FROM users WHERE id = ${req.params.id}`);
db.query("SELECT * FROM users WHERE name = '" + name + "'");

// NoSQL Injection -- unvalidated operators
db.collection('users').find({ username: req.body.username }); // if body is {"username": {"$gt": ""}}

// ORM raw queries without parameterization
sequelize.query(`SELECT * FROM users WHERE id = ${id}`);
```

**安全实现示例：**

```javascript
// Parameterized queries
db.query('SELECT * FROM users WHERE id = $1', [req.params.id]);

// MongoDB with type validation
const username = String(req.body.username); // Force to string, prevent operator injection
db.collection('users').find({ username });

// ORM parameterized raw queries
sequelize.query('SELECT * FROM users WHERE id = :id', {
  replacements: { id: req.params.id },
  type: QueryTypes.SELECT
});
```

---

### 8. 请求大小限制

**原因：** 如果没有大小限制，攻击者可以发送大量数据来耗尽服务器内存或导致服务拒绝。

**检查内容：**
- JSON 请求体的解析器是否设置了大小限制？
- 文件上传的大小是否有限制？
- URL 的长度是否有限制？
- JSON 的嵌套深度和数组长度是否有限制？
- 多部分表单数据的大小是否有限制？

**推荐限制：**

| 输入类型 | 推荐限制 |
|-------|------------------|
| JSON 请求体 | 100KB - 1MB（根据实际需求） |
| 文件上传 | 5MB - 50MB（根据实际需求） |
| URL 长度 | 2048 个字符 |
| 请求头大小 | 8KB |
| JSON 嵌套深度 | 10 层 |
| 请求体中的数组长度 | 1000 个元素 |

**实现示例：**

```javascript
// Express.js
app.use(express.json({ limit: '100kb' }));
app.use(express.urlencoded({ extended: true, limit: '100kb' }));

// File upload with multer
const upload = multer({
  limits: {
    fileSize: 5 * 1024 * 1024, // 5MB
    files: 5                     // max 5 files
  },
  fileFilter: (req, file, cb) => {
    const allowed = ['image/jpeg', 'image/png', 'application/pdf'];
    if (allowed.includes(file.mimetype)) {
      cb(null, true);
    } else {
      cb(new Error('Invalid file type'), false);
    }
  }
});
```

```go
// Go net/http
http.MaxBytesReader(w, r.Body, 1<<20) // 1MB limit
```

### 9. API 版本控制

**原因：** 如果没有版本控制，更新可能会同时影响所有客户端。版本控制可以优雅地淘汰旧版本并引导用户迁移。

**检查内容：**
- API 是否有版本号？
- 版本控制策略是否一致？（通过 URL 路径、头部信息或查询参数）
- 是否为过时的版本提供了退役日期？
- 是否有版本间的迁移指南？

**推荐版本控制方式（基于 URL 路径）：**

```
/api/v1/users      -- Current stable
/api/v2/users      -- New version with breaking changes
```

**实现示例：**

```javascript
// Express.js route versioning
const v1Router = require('./routes/v1');
const v2Router = require('./routes/v2');

app.use('/api/v1', v1Router);
app.use('/api/v2', v2Router);

// Deprecation header for old versions
app.use('/api/v1', (req, res, next) => {
  res.set('Deprecation', 'true');
  res.set('Sunset', 'Sat, 01 Jun 2026 00:00:00 GMT');
  res.set('Link', '</api/v2>; rel="successor-version"');
  next();
});
```

---

### 10. 日志记录与监控

**原因：** 如果无法监控系统活动，就无法检测攻击、排查问题或证明合规性。

**检查内容：**
- 是否记录了所有认证相关的事件？（登录成功/失败、令牌刷新、登出）
- 是否记录了授权失败的情况？
- 是否为每个 API 请求都记录了相关 ID？
- 敏感数据（如密码、令牌、个人身份信息）是否从日志中排除？
- 日志是否结构化（JSON 格式）以便机器解析？
- 是否对异常情况（如 401/500 错误、频繁的请求/响应）进行了报警？
- 请求/响应体是否从日志中排除（或进行了脱敏）？

**结构化日志记录示例：**

```javascript
// Express.js with pino
const pino = require('pino');
const logger = pino({ level: process.env.LOG_LEVEL || 'info' });

// Request logging middleware
app.use((req, res, next) => {
  req.id = crypto.randomUUID();
  const start = Date.now();

  res.on('finish', () => {
    logger.info({
      requestId: req.id,
      method: req.method,
      path: req.path,
      statusCode: res.statusCode,
      duration: Date.now() - start,
      ip: req.ip,
      userAgent: req.get('user-agent'),
      userId: req.user?.id || null
      // NOTE: Do NOT log req.body (may contain passwords/PII)
    });
  });

  next();
});

// Security event logging
function logSecurityEvent(event, details) {
  logger.warn({
    type: 'security',
    event,
    ...details,
    timestamp: new Date().toISOString()
  });
}

// Usage in auth middleware
logSecurityEvent('login_failed', { email: req.body.email, ip: req.ip });
logSecurityEvent('rate_limit_exceeded', { ip: req.ip, path: req.path });
logSecurityEvent('unauthorized_access', { userId: req.user?.id, resource: req.path });
```

## 框架特定说明

### Express.js
- 使用 `helmet` 库设置安全头部信息 |
- 使用 `express-rate-limit` 和 `rate-limit-redis` 实现分布式速率限制 |
- 使用 `cors` 库处理 CORS |
- 使用 `express-validator` 或 `zod` 进行输入验证 |
- 如果通过反向代理，正确设置 `trust proxy` 参数

### Flask（Python）
- 使用 `flask-limiter` 实现速率限制 |
- 使用 `flask-cors` 处理 CORS |
- 使用 `pydantic` 或 `marshmallow` 进行输入验证 |
- 使用 `flask-talisman` 设置安全头部信息 |
- 设置 `SESSION_COOKIESecure`、`SESSION_COOKIE_HTTPONLY`、`SESSION_COOKIE_SAMESITE` 参数

### Gin（Go）
- 使用 `gin-contrib/cors` 处理 CORS |
- 使用 `go-playground/validator` 进行输入验证 |
- 通过中间件设置安全头部信息 |
- 使用 `golang.org/x/time/rate` 实现速率限制 |
- 使用 `slog` 或 `zerolog` 进行结构化日志记录

### Fastify（Node.js）
- 使用 `@fastify/rate-limit` 实现速率限制 |
- 使用 `@fastify/cors` 处理 CORS |
- 使用 `@fastify/helmet` 设置安全头部信息 |
- 内置 JSON 结构验证 |
- 内置请求体大小限制

---

## 安装说明

```bash
clawhub install sovereign-api-hardener
```

## 文件列表

| 文件名 | 说明 |
|------|-------------|
| `SKILL.md` | 本文件包含完整的加固检查清单及代码示例 |
| `EXAMPLES.md` | Express.js API 加固前后的对比示例 |
| `README.md` | 快速入门和概述 |

## 许可证

MIT