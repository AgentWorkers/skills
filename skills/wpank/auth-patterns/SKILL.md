---
name: auth-patterns
model: standard
description: 身份验证和授权模式：JWT（JSON Web Tokens）、OAuth 2.0、会话（sessions）、RBAC（Role-Based Access Control）/ABAC（Attribute-Based Access Control）、密码安全（password security）、多因素认证（MFA）以及漏洞预防（vulnerability prevention）。这些模式适用于实现登录流程（login flows）、保护路由（protecting routes）、管理令牌（managing tokens）或审计身份验证安全性（auditing auth security）。
---

# 认证与授权模式（Authentication & Authorization Patterns）

> **关键安全技能** — 认证（Authentication）是整个系统的“入口”。如果这个环节出问题，其他所有环节都将变得毫无意义。

## 认证方法（Authentication Methods）

| 方法 | 工作原理 | 适用场景 |
|--------|-------------|----------|
| **JWT** | 每个请求都会附带一个签名过的令牌 | 单页应用程序（SPA）、微服务、移动应用程序 API |
| **基于会话的认证（Session-based）** | 服务器存储会话信息，客户端保存会话cookie | 传统Web应用程序、服务器端渲染（SSR） |
| **OAuth 2.0** | 通过授权服务器进行代理认证 | “使用Google/GitHub登录”、API访问 |
| **API密钥（API Keys）** | 在请求头中发送静态密钥 | 内部服务、公共API |
| **一次性登录链接（Magic Links）** | 通过电子邮件发送的一次性登录链接 | 低摩擦度的用户注册流程、B2C场景 |
| **Passkeys/WebAuthn** | 基于硬件/生物特征的认证方式 | 高安全性的应用程序、无密码登录 |

---

## JWT模式（JWT Patterns）

### 双令牌策略（Dual-Token Strategy）

- 短期访问令牌 + 长期刷新令牌：
```
Client → POST /auth/login → Server
Client ← { access_token, refresh_token }

Client → GET /api/data (Authorization: Bearer <access>) → Server
Client ← 401 Expired

Client → POST /auth/refresh { refresh_token } → Server
Client ← { new_access_token, rotated_refresh_token }
```

### 令牌结构（Token Structure）
```json
{
  "header": { "alg": "RS256", "typ": "JWT", "kid": "key-2024-01" },
  "payload": {
    "sub": "user_abc123",
    "iss": "https://auth.example.com",
    "aud": "https://api.example.com",
    "exp": 1700000900,
    "iat": 1700000000,
    "jti": "unique-token-id",
    "roles": ["user"],
    "scope": "read:profile write:profile"
  }
}
```

### 签名算法（Signing Algorithms）

| 算法 | 类型 | 适用场景 |
|-----------|------|-------------|
| **RS256** | 非对称加密（RSA） | 适用于微服务——仅认证服务器持有私钥 |
| **ES256** | 非对称加密（ECDSA） | 与RS256类似，但密钥和签名更小 |
| **HS256** | 对称加密 | 单服务器应用程序——所有验证方共享密钥 |

在分布式系统中，建议使用RS256/ES256算法。

### 令牌存储（Token Storage）

| 存储方式 | 是否安全 | 是否能防止CSRF攻击 | 推荐使用 |
|---------|----------|-----------|----------------|
| **httpOnly cookie** | 是 | 否（需要添加CSRF令牌） | **最适合Web应用程序** |
| **localStorage** | 否 | 是 | 避免使用——XSS攻击可能导致令牌泄露 |
| **内存中的存储（In-memory）** | 是 | 是 | 适用于单页应用程序，但刷新会丢失令牌 |

```
Set-Cookie: access_token=eyJ...; HttpOnly; Secure; SameSite=Strict; Path=/; Max-Age=900
```

### 令牌过期策略（Token Expiration Strategy）

| 令牌类型 | 寿命 | 令牌更新频率 |
|-------|----------|----------|
| **访问令牌（Access Token）** | 5–15分钟 | 每次请求时更新 |
| **刷新令牌（Refresh Token）** | 7–30天 | 每次使用后更新 |
| **ID令牌（ID Token）** | 与访问令牌相同 | 不需要更新 |

---

## OAuth 2.0流程（OAuth 2.0 Flows）

| 流程 | 客户端类型 | 适用场景 |
|------|-------------|-------------|
| **授权码+PKCE（Authorization Code + PKCE）** | 公开客户端（如单页应用程序、移动设备） | **所有公开客户端的默认方式** |
| **授权码（Authorization Code）** | 服务器端处理的客户端 | 需要后端支持的Web应用程序 |
| **客户端凭证（Client Credentials）** | 机器对机器的通信 | 服务之间的通信、定时任务 |
| **设备代码（Device Code）** | 对输入有要求的场景 | 智能电视、物联网设备、无头服务器上的命令行接口 |

> **隐式授权流程（Implicit Flow）已被弃用。** 对于公开客户端，始终使用“授权码+PKCE”流程。

### PKCE流程（PKCE Flow）
```
1. Client generates code_verifier (random 43-128 chars)
2. Client computes code_challenge = BASE64URL(SHA256(code_verifier))
3. Redirect to /authorize?code_challenge=...&code_challenge_method=S256
4. User authenticates, server redirects back with authorization code
5. Client exchanges code + code_verifier for tokens at /token
6. Server verifies SHA256(code_verifier) == code_challenge
```

---

## 会话管理（Session Management）

### 服务器端会话管理（Server-Side Sessions）

```
Client Cookie:  session_id=a1b2c3d4 (opaque, random, no user data)
Server Store:   { "a1b2c3d4": { userId: 123, roles: ["admin"], expiresAt: ... } }
```

| 存储方式 | 存储速度 | 适用场景 |
|-------|-------|-------------|
| **Redis** | 存储速度快 | 生产环境的首选方案——支持过期时间设置、支持水平扩展 |
| **PostgreSQL** | 存储速度中等 | 当Redis不适用时使用，需要审计记录 |
| **内存中的存储（In-memory）** | 存储速度最快 | 仅适用于开发环境 |

### 会话安全（Session Security）

| 威胁 | 防范措施 |
|--------|------------|
| 会话固定（Session Fixation） | 登录后重新生成会话ID |
| 会话劫持（Session Hijacking） | 使用`httpOnly`cookie并设置安全策略，将cookie与IP地址/用户代理绑定 |
| CSRF攻击（CSRF） | 使用`SameSite`cookie和CSRF令牌 |
| 会话闲置超时（Idle Session Timeout） | 15–30分钟无活动后令牌失效 |
| 绝对超时（Absolute Timeout） | 8–24小时后强制重新认证 |

---

## 授权模式（Authorization Patterns）

| 授权模式 | 权限粒度 | 适用场景 |
|---------|-------------|-------------|
| **RBAC（Role-Based Access Control）** | 权限粒度较粗（管理员、编辑者、查看者） | 大多数应用程序——简单的角色层级结构 |
| **ABAC（Attribute-Based Access Control）** | 权限粒度更细（如部门、时间、位置） | 企业级应用——基于上下文的访问控制 |
| **基于权限的授权（Permission-Based）** | 权限控制较为精细 | API——将权限与角色分离 |
| **基于策略的授权（Policy-Based）** | 权限控制灵活 | 微服务——规则可外部化、可审计 |
| **ReBAC（Reversible Role-Based Access Control）** | 权限控制灵活 | 社交应用程序、Google Drive式的共享功能 |

### RBAC实现（RBAC Implementation）
```typescript
const ROLE_PERMISSIONS: Record<string, string[]> = {
  admin:  ["user:read", "user:write", "user:delete", "post:read", "post:write", "post:delete"],
  editor: ["user:read", "post:read", "post:write"],
  viewer: ["user:read", "post:read"],
};

function requirePermission(permission: string) {
  return (req: Request, res: Response, next: NextFunction) => {
    const permissions = ROLE_PERMISSIONS[req.user.role] ?? [];
    if (!permissions.includes(permission)) {
      return res.status(403).json({ error: "Forbidden" });
    }
    next();
  };
}

app.delete("/api/users/:id", requirePermission("user:delete"), deleteUser);
```

---

## 密码安全（Password Security）

| 算法 | 推荐使用 | 不推荐使用 | 备注 |
|-----------|------------|-------------|-------|
| **Argon2id** | **首选算法** | 支持GPU/ASIC攻击防御 |
| **bcrypt** | 可以使用 | 不推荐——已被证明安全性较低 |
| **scrypt** | 可以使用 | 可以使用 | 是一个不错的替代方案 |
| **PBKDF2** | 可以使用 | 不推荐——NIST标准中推荐，但安全性较弱 |
| **SHA-256/MD5** | **绝对不推荐** | 不适合用于密码哈希 |

**NIST 800-63B建议：** 更倾向于使用较长的密码长度（12个字符以上），而非依赖复杂的加密算法。定期检查密码是否存在于已知泄露列表中。除非怀疑发生密码泄露，否则无需强制定期更换密码。

---

## 多因素认证（Multi-Factor Authentication）

| 认证因素 | 安全性 | 备注 |
|--------|----------|-------|
| **TOTP（时间基于令牌的认证）** | 高安全性 | 支持离线认证，例如Google Authenticator/Authy |
| **WebAuthn/Passkeys** | 最高安全性 | 防止钓鱼攻击，依赖硬件设备 |
| **短信验证码（SMS OTP）** | 中等安全性 | 易受SIM卡更换攻击——不适合高安全要求的应用 |
| **硬件密钥（FIDO2）** | 最高安全性 | YubiKey适用于管理员账户 |
| **备用验证码** | 较低安全性 | 仅用于备用，一次性使用，生成后应立即销毁 |

---

## 安全头信息（Security Headers）

| 头信息 | 值 | 说明 |
|--------|-------|-------|
| **Strict-Transport-Security** | `max-age=63072000; includeSubDomains; preload` | 限制传输过程中的安全设置 |
| **Content-Security-Policy** | 限制脚本来源，禁止内联脚本 |
| **X-Content-Type-Options** | `nosniff` | 防止脚本注入 |
| **X-Frame-Options** | `DENY` | 防止跨域脚本执行 |
| **Referrer-Policy** | `strict-origin-when-cross-origin` | 控制跨域请求的来源 |
| **CORS** | 允许特定的跨域请求来源，禁止使用通配符 |

## 常见安全漏洞（Common Vulnerabilities）

| 编号 | 漏洞类型 | 防范措施 |
|---|--------------|------------|
| 1 | 认证机制缺陷 | 使用多因素认证（MFA）、设置强密码策略、定期检查密码泄露情况 |
| 2 | 会话固定漏洞 | 登录后重新生成会话ID |
| 3 | JWT中的`alg:none`设置 | 拒绝使用`alg:none`，确保使用有效的签名算法 |
| 4 | JWT密钥被暴力破解 | 使用RS256/ES256算法，设置足够长的密钥长度（至少256位） |
| 5 | CSRF攻击 | 使用`SameSite`cookie和CSRF令牌 |
| 6 | 凭据填充攻击（Credential Stuffing） | 实施速率限制、定期检查密码是否泄露、使用多因素认证 |
| 7 | 密码存储不安全 | 使用Argon2id/bcrypt进行哈希处理 |
| 8 | 密码重置机制不安全 | 生成带时间限制的令牌，使用后及时失效 |
| 9 | 不安全的重定向机制 | 验证重定向URL是否在允许的范围内 |
| 10 | 令牌在URL中泄露 | 仅通过HTTP头或`httpOnly`cookie传输令牌 |
| 11 | 权限提升漏洞 | 在每次请求时进行服务器端角色验证 |
| 12 | OAuth重定向URL不匹配 | 确保重定向URL正确匹配，避免使用通配符 |
| 13 | 时间攻击（Timing Attacks） | 对密码进行恒定时间的比较处理 |

## 绝对禁止的行为（Never Do）

| 编号 | 禁止的行为 | 原因 |
|---|------|-----|
| 1 | **绝不要以明文或可逆加密方式存储密码** | 一旦密码泄露，所有用户都会受到威胁 |
| 2 | **绝不要将令牌放在URL或查询参数中** | 服务器、代理服务器、引用头都会记录这些信息 |
| 3 | **绝不要在JWT中使用`alg: none`或允许切换签名算法** | 防止攻击者伪造令牌 |
| 4 | **绝不要信任客户端的角色/权限声明** | 客户端可以修改这些信息 |
| 5 | **绝不要使用MD5、SHA-1或简单的SHA-256进行密码哈希** | 这些算法安全性较低 |
| 6 | **绝不要在生产环境中省略HTTPS** | 令牌和密码必须通过HTTPS传输 |
| 7 | **绝不要记录令牌、密码或敏感信息** | 日志可能被广泛访问和保存 |
| 8 | **绝不要使用长期有效的令牌** | 单次泄露可能导致永久性访问权限 |
| 9 | **绝不要自行实现加密算法** | 使用成熟的加密库（如jose、bcrypt、passport） |
| 10 | **绝不要对“用户未找到”和“密码错误”返回不同的错误信息** | 这可能导致用户信息被泄露 |

---

这些内容涵盖了认证与授权相关的关键技术和最佳实践，对于确保应用程序的安全性至关重要。