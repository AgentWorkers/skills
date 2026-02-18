# 认证与授权模式

掌握 JWT、OAuth2、会话管理以及基于角色的访问控制（RBAC）等认证与授权模式，以构建安全、可扩展的访问控制系统。

## 适用场景

- 实现用户认证系统
- 保护 REST 或 GraphQL API 的安全性
- 添加 OAuth2 或社交登录功能
- 设计会话管理机制
- 实施基于角色的访问控制（RBAC）或权限管理系统
- 调试认证相关问题

## 不适用场景

- 仅需要用户界面/登录页面的样式设计
- 任务仅涉及基础设施层面，无需处理身份验证相关问题
- 无法更改认证策略

---

## 认证（Authentication）与授权（Authorization）的区别

| 认证（AuthN） | 授权（AuthZ） |
|------------------|----------------------|
| 验证用户身份 | 检查用户权限 |
| 发放凭证 | 强制执行访问策略 |
| 登录/登出 | 控制用户访问权限 |

---

## 认证策略

| 策略 | 优点 | 缺点 | 适用场景 |
|---------|------|------|---------|
| **会话认证（Session Authentication）** | 简单、安全 | 需要维护会话状态，难以扩展 | 传统 Web 应用 |
| **JWT（JSON Web Tokens）** | 无状态、可扩展 | 令牌大小较大，存在吊销风险 | API、微服务 |
| **OAuth2/OIDC（OpenID Connect）** | 基于授权的登录机制 | 设置复杂 | 社交登录、企业级应用 |

---

## JWT 的实现

### 生成令牌

```typescript
import jwt from 'jsonwebtoken';

function generateTokens(user: User) {
  const accessToken = jwt.sign(
    { userId: user.id, email: user.email, role: user.role },
    process.env.JWT_SECRET!,
    { expiresIn: '15m' }  // Short-lived
  );

  const refreshToken = jwt.sign(
    { userId: user.id },
    process.env.JWT_REFRESH_SECRET!,
    { expiresIn: '7d' }  // Long-lived
  );

  return { accessToken, refreshToken };
}
```

### 验证令牌

```typescript
function authenticate(req: Request, res: Response, next: NextFunction) {
  const authHeader = req.headers.authorization;
  if (!authHeader?.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'No token provided' });
  }

  const token = authHeader.substring(7);
  try {
    const payload = jwt.verify(token, process.env.JWT_SECRET!);
    req.user = payload;
    next();
  } catch (error) {
    return res.status(401).json({ error: 'Invalid token' });
  }
}
```

### 刷新令牌流程

```typescript
app.post('/api/auth/refresh', async (req, res) => {
  const { refreshToken } = req.body;
  
  try {
    // Verify refresh token
    const payload = jwt.verify(refreshToken, process.env.JWT_REFRESH_SECRET!);
    
    // Check if token exists in database (not revoked)
    const storedToken = await db.refreshTokens.findOne({
      token: await hash(refreshToken),
      expiresAt: { $gt: new Date() }
    });
    
    if (!storedToken) {
      return res.status(403).json({ error: 'Token revoked' });
    }
    
    // Generate new access token
    const user = await db.users.findById(payload.userId);
    const accessToken = jwt.sign(
      { userId: user.id, email: user.email, role: user.role },
      process.env.JWT_SECRET!,
      { expiresIn: '15m' }
    );
    
    res.json({ accessToken });
  } catch {
    res.status(401).json({ error: 'Invalid refresh token' });
  }
});
```

---

## 基于会话的认证

```typescript
import session from 'express-session';
import RedisStore from 'connect-redis';

app.use(session({
  store: new RedisStore({ client: redisClient }),
  secret: process.env.SESSION_SECRET!,
  resave: false,
  saveUninitialized: false,
  cookie: {
    secure: process.env.NODE_ENV === 'production',  // HTTPS only
    httpOnly: true,   // No JavaScript access
    maxAge: 24 * 60 * 60 * 1000,  // 24 hours
    sameSite: 'strict'  // CSRF protection
  }
}));

// Login
app.post('/api/auth/login', async (req, res) => {
  const { email, password } = req.body;
  const user = await db.users.findOne({ email });
  
  if (!user || !(await verifyPassword(password, user.passwordHash))) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }
  
  req.session.userId = user.id;
  req.session.role = user.role;
  res.json({ user: { id: user.id, email: user.email } });
});

// Logout
app.post('/api/auth/logout', (req, res) => {
  req.session.destroy(() => {
    res.clearCookie('connect.sid');
    res.json({ message: 'Logged out' });
  });
});
```

---

## OAuth2 / 社交登录

```typescript
import passport from 'passport';
import { Strategy as GoogleStrategy } from 'passport-google-oauth20';

passport.use(new GoogleStrategy({
  clientID: process.env.GOOGLE_CLIENT_ID!,
  clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
  callbackURL: '/api/auth/google/callback'
}, async (accessToken, refreshToken, profile, done) => {
  // Find or create user
  let user = await db.users.findOne({ googleId: profile.id });
  
  if (!user) {
    user = await db.users.create({
      googleId: profile.id,
      email: profile.emails?.[0]?.value,
      name: profile.displayName
    });
  }
  
  return done(null, user);
}));

// Routes
app.get('/api/auth/google', 
  passport.authenticate('google', { scope: ['profile', 'email'] }));

app.get('/api/auth/google/callback',
  passport.authenticate('google', { session: false }),
  (req, res) => {
    const tokens = generateTokens(req.user);
    res.redirect(`${FRONTEND_URL}/auth/callback?token=${tokens.accessToken}`);
  });
```

---

## 基于角色的访问控制（RBAC）

```typescript
enum Role {
  USER = 'user',
  MODERATOR = 'moderator',
  ADMIN = 'admin'
}

const roleHierarchy: Record<Role, Role[]> = {
  [Role.ADMIN]: [Role.ADMIN, Role.MODERATOR, Role.USER],
  [Role.MODERATOR]: [Role.MODERATOR, Role.USER],
  [Role.USER]: [Role.USER]
};

function hasRole(userRole: Role, requiredRole: Role): boolean {
  return roleHierarchy[userRole].includes(requiredRole);
}

function requireRole(...roles: Role[]) {
  return (req: Request, res: Response, next: NextFunction) => {
    if (!req.user) {
      return res.status(401).json({ error: 'Not authenticated' });
    }
    if (!roles.some(role => hasRole(req.user.role, role))) {
      return res.status(403).json({ error: 'Insufficient permissions' });
    }
    next();
  };
}

// Usage
app.delete('/api/users/:id',
  authenticate,
  requireRole(Role.ADMIN),
  async (req, res) => {
    await db.users.delete(req.params.id);
    res.json({ message: 'User deleted' });
  }
);
```

---

## 基于权限的访问控制

```typescript
enum Permission {
  READ_USERS = 'read:users',
  WRITE_USERS = 'write:users',
  DELETE_USERS = 'delete:users',
  READ_POSTS = 'read:posts',
  WRITE_POSTS = 'write:posts'
}

const rolePermissions: Record<Role, Permission[]> = {
  [Role.USER]: [Permission.READ_POSTS, Permission.WRITE_POSTS],
  [Role.MODERATOR]: [Permission.READ_POSTS, Permission.WRITE_POSTS, Permission.READ_USERS],
  [Role.ADMIN]: Object.values(Permission)
};

function requirePermission(...permissions: Permission[]) {
  return (req: Request, res: Response, next: NextFunction) => {
    if (!req.user) return res.status(401).json({ error: 'Not authenticated' });
    
    const hasAll = permissions.every(p => 
      rolePermissions[req.user.role]?.includes(p)
    );
    
    if (!hasAll) return res.status(403).json({ error: 'Insufficient permissions' });
    next();
  };
}
```

---

## 资源所有权管理

```typescript
function requireOwnership(resourceType: 'post' | 'comment') {
  return async (req: Request, res: Response, next: NextFunction) => {
    if (!req.user) return res.status(401).json({ error: 'Not authenticated' });
    
    // Admins can access anything
    if (req.user.role === Role.ADMIN) return next();
    
    const resource = await db[resourceType].findById(req.params.id);
    if (!resource) return res.status(404).json({ error: 'Not found' });
    
    if (resource.userId !== req.user.userId) {
      return res.status(403).json({ error: 'Not authorized' });
    }
    
    next();
  };
}

// Usage: Users can only update their own posts
app.put('/api/posts/:id', authenticate, requireOwnership('post'), updatePost);
```

---

## 密码安全

```typescript
import bcrypt from 'bcrypt';
import { z } from 'zod';

const passwordSchema = z.string()
  .min(12, 'Password must be at least 12 characters')
  .regex(/[A-Z]/, 'Must contain uppercase')
  .regex(/[a-z]/, 'Must contain lowercase')
  .regex(/[0-9]/, 'Must contain number')
  .regex(/[^A-Za-z0-9]/, 'Must contain special character');

async function hashPassword(password: string): Promise<string> {
  return bcrypt.hash(password, 12);  // 12 rounds
}

async function verifyPassword(password: string, hash: string): Promise<boolean> {
  return bcrypt.compare(password, hash);
}
```

---

## 最佳实践

### 建议的做法

- 在所有请求中使用 HTTPS 协议
- 使用 bcrypt 算法对密码进行至少 12 轮哈希处理
- 使用有效期较短的访问令牌（15–30 分钟）
- 将刷新令牌存储在数据库中（并确保可撤销）
- 验证所有输入数据
- 对认证接口实施速率限制
- 记录安全事件
- 使用安全的 Cookie 属性（如 `httpOnly`、`secure`、`sameSite`）

### 不建议的做法

- 以明文形式存储密码
- 将 JWT 存储在 `localStorage` 中（容易受到 XSS 攻击）
- 使用安全性较低的 JWT 密钥
- 仅依赖客户端进行认证验证
- 在错误信息中暴露服务器端的执行细节
- 忽略服务器端的验证机制
- 不实施速率限制

---

## 常见问题及解决方法

| 问题 | 解决方案 |
|-------|----------|
| JWT 存储在 `localStorage` 中 | 使用 `httpOnly` 属性的 Cookie |
| 令牌没有过期时间 | 设置合理的过期时间并使用刷新令牌 |
| 密码强度不足 | 强制使用安全的密码策略（如 zod） |
- 未实施速率限制 | 使用 `express-rate-limit` 库和 Redis 进行速率控制 |
- 仅依赖客户端进行认证 | 必须始终进行服务器端验证 |

---