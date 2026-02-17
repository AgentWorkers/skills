# API安全最佳实践

实施安全的API设计模式，包括身份验证、授权、输入验证、速率限制以及防范常见的API漏洞。

## 适用场景

- 设计新的API端点  
- 保护现有的API  
- 实现身份验证和授权（JWT、OAuth 2.0、API密钥）  
- 设置速率限制和节流机制  
- 防范注入攻击（SQL注入、XSS攻击、命令注入）  
- 进行API安全审查或准备审计  
- 处理API中的敏感数据  
- 构建REST、GraphQL或WebSocket API  

## 不适用场景  

- 需要漏洞扫描（使用`vulnerability-scanner`技能）  
- 构建仅包含前端的应用程序（无需API）  
- 需要网络层安全防护（防火墙、WAF配置）  

## 输出内容  

- 安全的身份验证实现（JWT、刷新令牌）  
- 输入验证方案（Zod、Joi）  
- 速率限制配置  
- 安全中间件示例  
- OWASP API安全十大最佳实践指南  

## 工作原理  

### 第1步：身份验证与授权  

- 选择身份验证方法（JWT、OAuth 2.0、API密钥）  
- 实现基于令牌的身份验证  
- 设置基于角色的访问控制（RBAC）  
- 确保会话管理的安全性  
- 实现多因素认证（MFA）  

### 第2步：输入验证与清洗  

- 验证所有输入数据  
- 清洗用户输入  
- 使用参数化查询  
- 实现请求模式验证  
- 防范SQL注入、XSS攻击和命令注入  

### 第3步：速率限制与节流  

- 按用户/IP实施速率限制  
- 配置API节流机制  
- 设置请求配额  
- 优雅地处理速率限制错误  
- 监控异常活动  

### 第4步：数据保护  

- 对传输中的数据进行加密（HTTPS/TLS）  
- 对静态存储的数据进行加密  
- 实现适当的错误处理（防止数据泄露）  
- 清洗错误信息  
- 使用安全的HTTP头部信息  

## JWT身份验证实现  

### 生成安全的JWT令牌  

```javascript
// auth.js
const jwt = require('jsonwebtoken');
const bcrypt = require('bcrypt');

app.post('/api/auth/login', async (req, res) => {
  try {
    const { email, password } = req.body;
    
    // Validate input
    if (!email || !password) {
      return res.status(400).json({ error: 'Email and password required' });
    }
    
    // Find user
    const user = await db.user.findUnique({ where: { email } });
    
    if (!user) {
      // Don't reveal if user exists
      return res.status(401).json({ error: 'Invalid credentials' });
    }
    
    // Verify password
    const validPassword = await bcrypt.compare(password, user.passwordHash);
    if (!validPassword) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }
    
    // Generate JWT token
    const token = jwt.sign(
      { userId: user.id, email: user.email, role: user.role },
      process.env.JWT_SECRET,
      { expiresIn: '1h', issuer: 'your-app', audience: 'your-app-users' }
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
    
    res.json({ token, refreshToken, expiresIn: 3600 });
  } catch (error) {
    console.error('Login error:', error);
    res.status(500).json({ error: 'An error occurred during login' });
  }
});
```  

### JWT验证中间件  

```javascript
// middleware/auth.js
const jwt = require('jsonwebtoken');

function authenticateToken(req, res, next) {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1]; // Bearer TOKEN
  
  if (!token) {
    return res.status(401).json({ error: 'Access token required' });
  }
  
  jwt.verify(
    token, 
    process.env.JWT_SECRET,
    { issuer: 'your-app', audience: 'your-app-users' },
    (err, user) => {
      if (err) {
        if (err.name === 'TokenExpiredError') {
          return res.status(401).json({ error: 'Token expired' });
        }
        return res.status(403).json({ error: 'Invalid token' });
      }
      req.user = user;
      next();
    }
  );
}

module.exports = { authenticateToken };
```  

## 输入验证（防止SQL注入）  

### ❌ 易受攻击的代码示例  

```javascript
// NEVER DO THIS - SQL Injection vulnerability
app.get('/api/users/:id', async (req, res) => {
  const userId = req.params.id;
  const query = `SELECT * FROM users WHERE id = '${userId}'`;
  const user = await db.query(query);
  res.json(user);
});

// Attack: GET /api/users/1' OR '1'='1 → Returns all users!
```  

### ✅ 安全的做法：使用参数化查询  

```javascript
app.get('/api/users/:id', async (req, res) => {
  const userId = req.params.id;
  
  // Validate input first
  if (!userId || !/^\d+$/.test(userId)) {
    return res.status(400).json({ error: 'Invalid user ID' });
  }
  
  // Use parameterized query
  const user = await db.query(
    'SELECT id, email, name FROM users WHERE id = $1',
    [userId]
  );
  
  if (!user) {
    return res.status(404).json({ error: 'User not found' });
  }
  
  res.json(user);
});
```  

### ✅ 安全的做法：使用ORM（Prisma）  

```javascript
app.get('/api/users/:id', async (req, res) => {
  const userId = parseInt(req.params.id);
  
  if (isNaN(userId)) {
    return res.status(400).json({ error: 'Invalid user ID' });
  }
  
  const user = await prisma.user.findUnique({
    where: { id: userId },
    select: { id: true, email: true, name: true } // Don't select sensitive fields
  });
  
  if (!user) {
    return res.status(404).json({ error: 'User not found' });
  }
  
  res.json(user);
});
```  

### 使用Zod进行模式验证  

```javascript
const { z } = require('zod');

const createUserSchema = z.object({
  email: z.string().email('Invalid email format'),
  password: z.string()
    .min(8, 'Password must be at least 8 characters')
    .regex(/[A-Z]/, 'Must contain uppercase letter')
    .regex(/[a-z]/, 'Must contain lowercase letter')
    .regex(/[0-9]/, 'Must contain number'),
  name: z.string().min(2).max(100),
  age: z.number().int().min(18).max(120).optional()
});

function validateRequest(schema) {
  return (req, res, next) => {
    try {
      schema.parse(req.body);
      next();
    } catch (error) {
      res.status(400).json({ error: 'Validation failed', details: error.errors });
    }
  };
}

app.post('/api/users', validateRequest(createUserSchema), async (req, res) => {
  // Input is validated at this point
  const { email, password, name, age } = req.body;
  const passwordHash = await bcrypt.hash(password, 10);
  const user = await prisma.user.create({ data: { email, passwordHash, name, age } });
  const { passwordHash: _, ...userWithoutPassword } = user;
  res.status(201).json(userWithoutPassword);
});
```  

## 速率限制  

```javascript
const rateLimit = require('express-rate-limit');
const RedisStore = require('rate-limit-redis');
const Redis = require('ioredis');

const redis = new Redis({
  host: process.env.REDIS_HOST,
  port: process.env.REDIS_PORT
});

// General API rate limit
const apiLimiter = rateLimit({
  store: new RedisStore({ client: redis, prefix: 'rl:api:' }),
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // 100 requests per window
  message: { error: 'Too many requests, please try again later', retryAfter: 900 },
  standardHeaders: true,
  legacyHeaders: false,
  keyGenerator: (req) => req.user?.userId || req.ip
});

// Strict rate limit for authentication
const authLimiter = rateLimit({
  store: new RedisStore({ client: redis, prefix: 'rl:auth:' }),
  windowMs: 15 * 60 * 1000,
  max: 5, // Only 5 login attempts per 15 minutes
  skipSuccessfulRequests: true,
  message: { error: 'Too many login attempts, please try again later', retryAfter: 900 }
});

app.use('/api/', apiLimiter);
app.use('/api/auth/login', authLimiter);
app.use('/api/auth/register', authLimiter);
```  

## 安全HTTP头部信息（Helmet）  

```javascript
const helmet = require('helmet');

app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      scriptSrc: ["'self'"],
      imgSrc: ["'self'", 'data:', 'https:']
    }
  },
  frameguard: { action: 'deny' },
  hidePoweredBy: true,
  noSniff: true,
  hsts: { maxAge: 31536000, includeSubDomains: true, preload: true }
}));
```  

## 授权检查  

### ❌ 不正确的做法：仅依赖身份验证  

```javascript
app.delete('/api/posts/:id', authenticateToken, async (req, res) => {
  await prisma.post.delete({ where: { id: req.params.id } });
  res.json({ success: true });
});
```  

### ✅ 正确的做法：同时进行身份验证和授权  

```javascript
app.delete('/api/posts/:id', authenticateToken, async (req, res) => {
  const post = await prisma.post.findUnique({ where: { id: req.params.id } });
  
  if (!post) {
    return res.status(404).json({ error: 'Post not found' });
  }
  
  // Check if user owns the post or is admin
  if (post.userId !== req.user.userId && req.user.role !== 'admin') {
    return res.status(403).json({ error: 'Not authorized to delete this post' });
  }
  
  await prisma.post.delete({ where: { id: req.params.id } });
  res.json({ success: true });
});
```  

## 最佳实践  

### ✅ 必须做到的事项：  
- **始终使用HTTPS**——切勿通过HTTP传输敏感数据  
- **实施身份验证**——对受保护的端点要求用户进行身份验证  
- **验证所有输入**——绝不信任用户输入  
- **使用参数化查询**——防止SQL注入  
- **实施速率限制**——防范暴力攻击和DDoS攻击  
- **对密码进行加密**——使用bcrypt算法并设置足够的盐值轮数（≥10）  
- **使用短有效期令牌**——JWT访问令牌应快速过期  
- **正确配置CORS**——仅允许可信的来源访问  
- **记录安全事件**——监控异常活动  
- **使用安全的HTTP头部信息**——启用Helmet.js  
- **清洗错误信息**——避免泄露敏感信息  

### 不应做的事情：  
- **不要以明文形式存储密码**  
- **不要使用弱密码**——使用强密码和随机生成的JWT密钥  
- **不要完全信任用户输入**——始终进行验证和清洗  
- **不要泄露堆栈跟踪信息**——在生产环境中隐藏错误细节  
- **不要使用字符串拼接来构建SQL查询**  
- **不要在JWT中存储敏感数据**——JWT本身不提供加密保护  
- **不要忽略安全更新**——定期更新依赖库  
- **不要记录敏感数据**  

## OWASP API安全十大最佳实践  

1. **对象级授权失效**——始终验证用户是否有权访问资源  
2. **身份验证机制失效**——实施强身份验证机制  
3. **对象属性级授权失效**——验证用户可以访问哪些属性  
4. **资源消耗不受限制**——实施速率限制和配额管理  
5. **函数级授权失效**——为每个功能验证用户角色  
6. **对敏感业务流程的访问不受限制**——保护关键业务流程  
7. **服务器端请求伪造（SSRF）**——验证和清洗URL  
8. **安全配置错误**——遵循安全最佳实践并使用正确的HTTP头部信息  
9. **库存管理不善**——记录并保护所有API端点  
10. **不安全地使用第三方API**——验证来自第三方API的数据  

## 安全检查清单  

### 身份验证与授权  
- [ ] 实施强身份验证（JWT、OAuth 2.0）  
- [ ] 所有端点均使用HTTPS  
- [ ] 使用bcrypt算法对密码进行加密（盐值轮数≥10）  
- [ ] 实现令牌过期机制  
- [ ] 添加刷新令牌功能  
- [ ] 对每个请求进行用户授权验证  
- [ ] 实施基于角色的访问控制（RBAC）  

### 输入验证  
- [ ] 验证所有用户输入  
- [ ] 使用参数化查询或ORM框架  
- [ ] 清洗HTML内容  
- [ ] 验证文件上传  
- [ ] 实现请求模式验证  
- [ ] 使用允许列表而非禁止列表  

### 速率限制与DDoS防护  
- [ ] 按用户/IP实施速率限制  
- [ ] 对身份验证端点设置更严格的限制  
- [ ] 使用Redis进行分布式速率限制  
- [ ] 返回正确的速率限制头部信息  
- [ ] 实现请求节流机制  

### 数据保护  
- [ ] 所有流量均使用HTTPS/TLS  
- [ ] 对静态数据进行加密  
- [ ] 不要在JWT中存储敏感数据  
- [ ] 清洗错误信息  
- [ ] 正确配置CORS  
- [ ] 使用安全的HTTP头部信息（Helmet.js）  

## 额外资源  

- [OWASP API安全十大最佳实践](https://owasp.org/www-project-api-security/)  
- [JWT最佳实践](https://tools.ietf.org/html/rfc8725)  
- [Express框架安全最佳实践](https://expressjs.com/en/advanced/best-practice-security.html)  
- [API安全检查清单](https://github.com/shieldfy/API-Security-Checklist)