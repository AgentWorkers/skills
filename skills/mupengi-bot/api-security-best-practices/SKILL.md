---
name: api-security-best-practices
description: "实现安全的 API 设计模式，包括身份验证（authentication）、授权（authorization）、输入验证（input validation）、速率限制（rate limiting），以及防范常见的 API 漏洞（protection against common API vulnerabilities）。"
author: 무펭이 🐧
---
# API安全最佳实践 🐧

## 概述

本指南通过实施身份验证、授权、输入验证、速率限制以及防范常见漏洞，帮助开发者构建安全的API。本技能涵盖了REST、GraphQL和WebSocket API的安全模式。

## 适用场景

- 在设计新的API端点时使用
- 在保护现有API时使用
- 在实现身份验证和授权时使用
- 在防范API攻击（如注入攻击、DDoS攻击等）时使用
- 在进行API安全审查时使用
- 在准备安全审计时使用
- 在实现速率限制和节流时使用
- 在处理API中的敏感数据时使用

## 工作原理

### 第1步：身份验证与授权

我将帮助您实现安全的身份验证：
- 选择身份验证方法（JWT、OAuth 2.0、API密钥）
- 实现基于令牌的身份验证
- 设置基于角色的访问控制（RBAC）
- 保护会话管理
- 实现多因素身份验证（MFA）

### 第2步：输入验证与清理

防范注入攻击：
- 验证所有输入数据
- 清理用户输入
- 使用参数化查询
- 实现请求模式验证
- 防止SQL注入、XSS和命令注入

### 第3步：速率限制与节流

防止滥用和DDoS攻击：
- 按用户/IP实施速率限制
- 设置API节流
- 配置请求配额
- 优雅地处理速率限制错误
- 监控异常活动

### 第4步：数据保护

保护敏感数据：
- 对传输中的数据进行加密（HTTPS/TLS）
- 对静态数据（非传输中的数据）进行加密
- 实现适当的错误处理（防止数据泄露）
- 清理错误信息
- 使用安全的HTTP头部

### 第5步：API安全测试

验证安全实现：
- 测试身份验证和授权
- 进行渗透测试
- 检查常见漏洞（OWASP API Top 10）
- 验证输入处理

## 示例

### 示例1：实现JWT身份验证

```markdown
## Secure JWT Authentication Implementation

### Authentication Flow

1. User logs in with credentials
2. Server validates credentials
3. Server generates JWT token
4. Client stores token securely
5. Client sends token with each request
6. Server validates token

### Implementation

#### 1. Generate Secure JWT Tokens

\`\`\`javascript
// auth.js
const jwt = require('jsonwebtoken');
const bcrypt = require('bcrypt');

// Login endpoint
app.post('/api/auth/login', async (req, res) => {
  try {
    const { email, password } = req.body;
    
    // Validate input
    if (!email || !password) {
      return res.status(400).json({ 
        error: 'Email and password are required' 
      });
    }
    
    // Find user
    const user = await db.user.findUnique({ 
      where: { email } 
    });
    
    if (!user) {
      // Don't reveal if user exists
      return res.status(401).json({ 
        error: 'Invalid credentials' 
      });
    }
    
    // Verify password
    const validPassword = await bcrypt.compare(
      password, 
      user.passwordHash
    );
    
    if (!validPassword) {
      return res.status(401).json({ 
        error: 'Invalid credentials' 
      });
    }
    
    // Generate JWT token
    const token = jwt.sign(
      { 
        userId: user.id,
        email: user.email,
        role: user.role
      },
      process.env.JWT_SECRET,
      { 
        expiresIn: '1h',
        issuer: 'your-app',
        audience: 'your-app-users'
      }
    );
    
    // Generate refresh token
    const refreshToken = jwt.sign(
      { userId: user.id },
      process.env.JWT_REFRESH_SECRET,
      { expiresIn: '7d' }
    );
    
    // Store refresh token in database
    await db.refreshToken.create({
      data: {
        token: refreshToken,
        userId: user.id,
        expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000)
      }
    });
    
    res.json({
      token,
      refreshToken,
      expiresIn: 3600
    });
    
  } catch (error) {
    console.error('Login error:', error);
    res.status(500).json({ 
      error: 'An error occurred during login' 
    });
  }
});
\`\`\`

#### 2. Verify JWT Tokens (Middleware)

\`\`\`javascript
// middleware/auth.js
const jwt = require('jsonwebtoken');

function authenticateToken(req, res, next) {
  // Get token from header
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1]; // Bearer TOKEN
  
  if (!token) {
    return res.status(401).json({ 
      error: 'Access token required' 
    });
  }
  
  // Verify token
  jwt.verify(
    token, 
    process.env.JWT_SECRET,
    { 
      issuer: 'your-app',
      audience: 'your-app-users'
    },
    (err, user) => {
      if (err) {
        if (err.name === 'TokenExpiredError') {
          return res.status(401).json({ 
            error: 'Token expired' 
          });
        }
        return res.status(403).json({ 
          error: 'Invalid token' 
        });
      }
      
      // Attach user to request
      req.user = user;
      next();
    }
  );
}

module.exports = { authenticateToken };
\`\`\`

#### 3. Protect Routes

\`\`\`javascript
const { authenticateToken } = require('./middleware/auth');

// Protected route
app.get('/api/user/profile', authenticateToken, async (req, res) => {
  try {
    const user = await db.user.findUnique({
      where: { id: req.user.userId },
      select: {
        id: true,
        email: true,
        name: true,
        // Don't return passwordHash
      }
    });
    
    res.json(user);
  } catch (error) {
    res.status(500).json({ error: 'Server error' });
  }
});
\`\`\`

#### 4. Implement Token Refresh

\`\`\`javascript
app.post('/api/auth/refresh', async (req, res) => {
  const { refreshToken } = req.body;
  
  if (!refreshToken) {
    return res.status(401).json({ 
      error: 'Refresh token required' 
    });
  }
  
  try {
    // Verify refresh token
    const decoded = jwt.verify(
      refreshToken, 
      process.env.JWT_REFRESH_SECRET
    );
    
    // Check if refresh token exists in database
    const storedToken = await db.refreshToken.findFirst({
      where: {
        token: refreshToken,
        userId: decoded.userId,
        expiresAt: { gt: new Date() }
      }
    });
    
    if (!storedToken) {
      return res.status(403).json({ 
        error: 'Invalid refresh token' 
      });
    }
    
    // Generate new access token
    const user = await db.user.findUnique({
      where: { id: decoded.userId }
    });
    
    const newToken = jwt.sign(
      { 
        userId: user.id,
        email: user.email,
        role: user.role
      },
      process.env.JWT_SECRET,
      { expiresIn: '1h' }
    );
    
    res.json({
      token: newToken,
      expiresIn: 3600
    });
    
  } catch (error) {
    res.status(403).json({ 
      error: 'Invalid refresh token' 
    });
  }
});
\`\`\`

### Security Best Practices

- ✅ Use strong JWT secrets (256-bit minimum)
- ✅ Set short expiration times (1 hour for access tokens)
- ✅ Implement refresh tokens for long-lived sessions
- ✅ Store refresh tokens in database (can be revoked)
- ✅ Use HTTPS only
- ✅ Don't store sensitive data in JWT payload
- ✅ Validate token issuer and audience
- ✅ Implement token blacklisting for logout
```

### 示例2：输入验证与SQL注入预防

```markdown
## Preventing SQL Injection and Input Validation

### The Problem

**❌ Vulnerable Code:**
\`\`\`javascript
// NEVER DO THIS - SQL Injection vulnerability
app.get('/api/users/:id', async (req, res) => {
  const userId = req.params.id;
  
  // Dangerous: User input directly in query
  const query = \`SELECT * FROM users WHERE id = '\${userId}'\`;
  const user = await db.query(query);
  
  res.json(user);
});

// Attack example:
// GET /api/users/1' OR '1'='1
// Returns all users!
\`\`\`

### The Solution

#### 1. Use Parameterized Queries

\`\`\`javascript
// ✅ Safe: Parameterized query
app.get('/api/users/:id', async (req, res) => {
  const userId = req.params.id;
  
  // Validate input first
  if (!userId || !/^\d+$/.test(userId)) {
    return res.status(400).json({ 
      error: 'Invalid user ID' 
    });
  }
  
  // Use parameterized query
  const user = await db.query(
    'SELECT id, email, name FROM users WHERE id = $1',
    [userId]
  );
  
  if (!user) {
    return res.status(404).json({ 
      error: 'User not found' 
    });
  }
  
  res.json(user);
});
\`\`\`

#### 2. Use ORM with Proper Escaping

\`\`\`javascript
// ✅ Safe: Using Prisma ORM
app.get('/api/users/:id', async (req, res) => {
  const userId = parseInt(req.params.id);
  
  if (isNaN(userId)) {
    return res.status(400).json({ 
      error: 'Invalid user ID' 
    });
  }
  
  const user = await prisma.user.findUnique({
    where: { id: userId },
    select: {
      id: true,
      email: true,
      name: true,
      // Don't select sensitive fields
    }
  });
  
  if (!user) {
    return res.status(404).json({ 
      error: 'User not found' 
    });
  }
  
  res.json(user);
});
\`\`\`

#### 3. Implement Request Validation with Zod

\`\`\`javascript
const { z } = require('zod');

// Define validation schema
const createUserSchema = z.object({
  email: z.string().email('Invalid email format'),
  password: z.string()
    .min(8, 'Password must be at least 8 characters')
    .regex(/[A-Z]/, 'Password must contain uppercase letter')
    .regex(/[a-z]/, 'Password must contain lowercase letter')
    .regex(/[0-9]/, 'Password must contain number'),
  name: z.string()
    .min(2, 'Name must be at least 2 characters')
    .max(100, 'Name too long'),
  age: z.number()
    .int('Age must be an integer')
    .min(18, 'Must be 18 or older')
    .max(120, 'Invalid age')
    .optional()
});

// Validation middleware
function validateRequest(schema) {
  return (req, res, next) => {
    try {
      schema.parse(req.body);
      next();
    } catch (error) {
      res.status(400).json({
        error: 'Validation failed',
        details: error.errors
      });
    }
  };
}

// Use validation
app.post('/api/users', 
  validateRequest(createUserSchema),
  async (req, res) => {
    // Input is validated at this point
    const { email, password, name, age } = req.body;
    
    // Hash password
    const passwordHash = await bcrypt.hash(password, 10);
    
    // Create user
    const user = await prisma.user.create({
      data: {
        email,
        passwordHash,
        name,
        age
      }
    });
    
    // Don't return password hash
    const { passwordHash: _, ...userWithoutPassword } = user;
    res.status(201).json(userWithoutPassword);
  }
);
\`\`\`

#### 4. Sanitize Output to Prevent XSS

\`\`\`javascript
const DOMPurify = require('isomorphic-dompurify');

app.post('/api/comments', authenticateToken, async (req, res) => {
  const { content } = req.body;
  
  // Validate
  if (!content || content.length > 1000) {
    return res.status(400).json({ 
      error: 'Invalid comment content' 
    });
  }
  
  // Sanitize HTML to prevent XSS
  const sanitizedContent = DOMPurify.sanitize(content, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a'],
    ALLOWED_ATTR: ['href']
  });
  
  const comment = await prisma.comment.create({
    data: {
      content: sanitizedContent,
      userId: req.user.userId
    }
  });
  
  res.status(201).json(comment);
});
\`\`\`

### Validation Checklist

- [ ] Validate all user inputs
- [ ] Use parameterized queries or ORM
- [ ] Validate data types (string, number, email, etc.)
- [ ] Validate data ranges (min/max length, value ranges)
- [ ] Sanitize HTML content
- [ ] Escape special characters
- [ ] Validate file uploads (type, size, content)
- [ ] Use allowlists, not blocklists
```

### 示例3：速率限制与DDoS防护

```markdown
## Implementing Rate Limiting

### Why Rate Limiting?

- Prevent brute force attacks
- Protect against DDoS
- Prevent API abuse
- Ensure fair usage
- Reduce server costs

### Implementation with Express Rate Limit

\`\`\`javascript
const rateLimit = require('express-rate-limit');
const RedisStore = require('rate-limit-redis');
const Redis = require('ioredis');

// Create Redis client
const redis = new Redis({
  host: process.env.REDIS_HOST,
  port: process.env.REDIS_PORT
});

// General API rate limit
const apiLimiter = rateLimit({
  store: new RedisStore({
    client: redis,
    prefix: 'rl:api:'
  }),
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // 100 requests per window
  message: {
    error: 'Too many requests, please try again later',
    retryAfter: 900 // seconds
  },
  standardHeaders: true, // Return rate limit info in headers
  legacyHeaders: false,
  // Custom key generator (by user ID or IP)
  keyGenerator: (req) => {
    return req.user?.userId || req.ip;
  }
});

// Strict rate limit for authentication endpoints
const authLimiter = rateLimit({
  store: new RedisStore({
    client: redis,
    prefix: 'rl:auth:'
  }),
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // Only 5 login attempts per 15 minutes
  skipSuccessfulRequests: true, // Don't count successful logins
  message: {
    error: 'Too many login attempts, please try again later',
    retryAfter: 900
  }
});

// Apply rate limiters
app.use('/api/', apiLimiter);
app.use('/api/auth/login', authLimiter);
app.use('/api/auth/register', authLimiter);

// Custom rate limiter for expensive operations
const expensiveLimiter = rateLimit({
  windowMs: 60 * 60 * 1000, // 1 hour
  max: 10, // 10 requests per hour
  message: {
    error: 'Rate limit exceeded for this operation'
  }
});

app.post('/api/reports/generate', 
  authenticateToken,
  expensiveLimiter,
  async (req, res) => {
    // Expensive operation
  }
);
\`\`\`

### Advanced: Per-User Rate Limiting

\`\`\`javascript
// Different limits based on user tier
function createTieredRateLimiter() {
  const limits = {
    free: { windowMs: 60 * 60 * 1000, max: 100 },
    pro: { windowMs: 60 * 60 * 1000, max: 1000 },
    enterprise: { windowMs: 60 * 60 * 1000, max: 10000 }
  };
  
  return async (req, res, next) => {
    const user = req.user;
    const tier = user?.tier || 'free';
    const limit = limits[tier];
    
    const key = \`rl:user:\${user.userId}\`;
    const current = await redis.incr(key);
    
    if (current === 1) {
      await redis.expire(key, limit.windowMs / 1000);
    }
    
    if (current > limit.max) {
      return res.status(429).json({
        error: 'Rate limit exceeded',
        limit: limit.max,
        remaining: 0,
        reset: await redis.ttl(key)
      });
    }
    
    // Set rate limit headers
    res.set({
      'X-RateLimit-Limit': limit.max,
      'X-RateLimit-Remaining': limit.max - current,
      'X-RateLimit-Reset': await redis.ttl(key)
    });
    
    next();
  };
}

app.use('/api/', authenticateToken, createTieredRateLimiter());
\`\`\`

### DDoS Protection with Helmet

\`\`\`javascript
const helmet = require('helmet');

app.use(helmet({
  // Content Security Policy
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      scriptSrc: ["'self'"],
      imgSrc: ["'self'", 'data:', 'https:']
    }
  },
  // Prevent clickjacking
  frameguard: { action: 'deny' },
  // Hide X-Powered-By header
  hidePoweredBy: true,
  // Prevent MIME type sniffing
  noSniff: true,
  // Enable HSTS
  hsts: {
    maxAge: 31536000,
    includeSubDomains: true,
    preload: true
  }
}));
\`\`\`

### Rate Limit Response Headers

\`\`\`
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 87
X-RateLimit-Reset: 1640000000
Retry-After: 900
\`\`\`
```

## 最佳实践

### ✅ 应该这样做

- **始终使用HTTPS** - 绝不要通过HTTP传输敏感数据
- **实施身份验证** - 对受保护的端点要求身份验证
- **验证所有输入** - 绝不要信任用户输入
- **使用参数化查询** - 防止SQL注入
- **实施速率限制** - 防范暴力攻击和DDoS攻击
- **对密码进行哈希处理** - 使用bcrypt并设置至少10轮加盐
- **使用短有效期令牌** - JWT访问令牌应快速过期
- **正确配置CORS** - 仅允许可信来源的请求
- **记录安全事件** - 监控异常活动
- **保持依赖项更新** - 定期更新包
- **使用安全HTTP头部** - 例如使用Helmet.js
- **清理错误信息** - 不要泄露敏感信息

### ❌ 不应该这样做

- **不要以明文形式存储密码** - 始终对密码进行哈希处理
- **不要使用弱密码** - 使用强密码和随机生成的JWT密钥
- **不要信任用户输入** - 始终进行验证和清理
- **不要暴露堆栈跟踪** - 在生产环境中隐藏错误细节
- **不要使用字符串连接来构建SQL查询** - 使用参数化查询
- **不要在JWT中存储敏感数据** - JWT本身不提供加密功能
- **不要忽略安全更新** - 定期更新依赖项
- **不要使用默认凭据** - 更改所有默认密码
- **不要完全禁用CORS** - 而是要正确配置它
- **不要记录敏感数据** - 清理日志中的敏感信息

## 常见陷阱

### 问题：代码中暴露了JWT密钥
**症状：** JWT密钥被硬编码或提交到Git中
**解决方案：**
```javascript
// ❌ 错误做法
const JWT_SECRET = 'my-secret-key';

// ✅ 正确做法
const JWT_SECRET = process.env JWT_SECRET;
if (!JWT_SECRET) {
  throw new Error('需要JWT_SECRET环境变量');
}

// 生成强密码
// node -e "console.log(require('crypto').randomBytes(64).toString('hex'))
```

### 问题：密码要求过低
**症状：** 用户可以设置如"password123"这样的弱密码
**解决方案：**
```javascript
const passwordSchema = z.string()
  .min(12, '密码必须至少包含12个字符')
  .regex(/[A-Z]/, '必须包含大写字母')
  .regex(/[a-z]/, '必须包含小写字母')
  .regex(/[0-9]/, '必须包含数字')
  .regex(/[^A-Za-z0-9]/, '必须包含特殊字符');

// 或使用密码强度检查库
const zxcvbn = require('zxcvbn');
const result = zxcvbn(password);
if (result.score < 3) {
  return res.status(400).json({
    error: '密码太弱',
    suggestions: result.feedback.suggestions
  });
}
```

### 问题：缺少授权检查
**症状：** 用户可以访问他们不应该访问的资源
**解决方案：**
```javascript
// ❌ 错误做法：仅检查身份验证
app.delete('/api/posts/:id', authenticateToken, async (req, res) => {
  await prisma.post.delete({ where: { id: req.params.id } });
  res.json({ success: true });
};

// ✅ 正确做法：同时检查身份验证和授权
app.delete('/api/posts/:id', authenticateToken, async (req, res) => {
  const post = await prisma.post.findUnique({
    where: { id: req.params.id }
  });

  if (!post) {
    return res.status(404).json({ error: '帖子未找到' });
  }

  // 检查用户是否拥有该帖子或是否为管理员
  if (post.userId !== req.user.userId && req.user.role !== 'admin') {
    return res.status(403).json({ 
      error: '无权限删除此帖子' 
    });
  }

  await prisma.post.delete({ where: { id: req.params.id } );
  res.json({ success: true });
};
```

### 问题：错误信息过于详细
**症状：** 错误信息会暴露系统细节
**解决方案：**
```javascript
// ❌ 错误做法：暴露数据库细节
app.post('/api/users', async (req, res) => {
  try {
    const user = await prisma.user.create({ data: req.body });
    res.json(user);
  } catch (error) {
    res.status(500).json({ error: error.message });
    // 错误信息：'字段`email`存在唯一性约束失败'
  };

// ✅ 正确做法：使用通用错误信息
app.post('/api/users', async (req, res) => {
  try {
    const user = await prisma.user.create({ data: req.body });
    res.json(user);
  } catch (error) {
    console.error('用户创建错误:', error); // 记录完整的错误信息

    if (error.code === 'P2002') {
      return res.status(400).json({ 
        error: '电子邮件已存在' 
      });
    }

    res.status(500).json({ 
      error: '创建用户时发生错误' 
    });
  }
};
```

## 安全检查清单

### 身份验证与授权
- [ ] 实施强身份验证（JWT、OAuth 2.0）
- [ ] 所有端点都使用HTTPS
- [ ] 使用bcrypt对密码进行哈希处理（至少10轮加盐）
- [ ] 实现令牌过期机制
- [ ] 添加刷新令牌功能
- [ ] 对每个请求都验证用户授权
- [ ] 实现基于角色的访问控制（RBAC）

### 输入验证
- [ ] 验证所有用户输入
- [ ] 使用参数化查询或ORM
- [ ] 清理HTML内容
- [ ] 验证文件上传
- [ ] 实现请求模式验证
- [ ] 使用允许列表，而不是禁止列表

### 速率限制与DDoS防护
- [ ] 按用户/IP实施速率限制
- [ ] 对授权端点设置更严格的限制
- [ ] 使用Redis进行分布式速率限制
- [ ] 返回正确的速率限制头部
- [ ] 实现请求节流

### 数据保护
- [ ] 所有流量都使用HTTPS/TLS
- [ ] 对静态数据（非传输中的数据）进行加密
- [ ] 不要在JWT中存储敏感数据
- [ ] 清理错误信息
- [ ] 正确配置CORS
- [ ] 使用安全HTTP头部（例如Helmet.js）

### 监控与日志记录
- [ ] 记录安全事件
- [ ] 监控异常活动
- [ ] 为失败的授权尝试设置警报
- [ ] 跟踪API使用情况
- [ ] 不要记录敏感数据

## OWASP API安全Top 10

1. **对象级授权失效** - 始终验证用户是否有权访问资源
2. **身份验证失效** - 实施强身份验证机制
3. **对象属性级授权失效** - 验证用户可以访问哪些属性
4. **资源消耗无限制** - 实施速率限制和配额
5. **函数级授权失效** - 验证用户的角色
6. **对敏感业务流程的访问不受限制** - 保护关键业务流程
7. **服务器端请求伪造（SSRF）** - 验证和清理URL
8. **安全配置不当** - 使用最佳安全实践和HTTP头部
9. **库存管理不善** - 记录并保护所有API端点
10. **不安全地使用API** - 验证来自第三方API的数据

## 相关技能

- `@ethical-hacking-methodology` - 安全测试相关方法
- `@sql-injection-testing` - SQL注入测试
- `@xss-html-injection` - XSS漏洞测试
- `@broken-authentication` - 身份验证漏洞相关
- `@backend-dev-guidelines` - 后端开发标准
- `@systematic-debugging` - 安全问题调试

## 额外资源

- [OWASP API安全Top 10](https://owasp.org/www-project-api-security/)
- [JWT最佳实践](https://tools.ietf.org/html/rfc8725)
- [Express安全最佳实践](https://expressjs.com/en/advanced/best-practice-security.html)
- [Node.js安全检查清单](https://blog.risingstack.com/node-js-security-checklist/)
- [API安全检查清单](https://github.com/shieldfy/API-Security-Checklist)

---

**专业提示：** 安全工作不是一次性完成的任务——定期审计您的API，保持依赖项更新，并关注新的安全漏洞！

---
> 🐧 由**무펭이**制作 — [무펭이즘(Mupengism)](https://github.com/mupeng) 生态系统技能