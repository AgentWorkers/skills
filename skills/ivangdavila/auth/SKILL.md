---
name: Auth
slug: auth
version: 1.3.0
homepage: https://clawic.com/skills/auth
description: 为Web和移动应用程序构建安全的认证机制，支持会话（sessions）、JSON Web Tokens (JWT)、OAuth、无密码登录（passwordless login）、多因素认证（MFA）以及单点登录（SSO）等功能。
changelog: "Added documentation-only disclaimer, clarified example code does not execute"
metadata: {"clawdbot":{"emoji":"🔐","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---
## 仅用于文档说明的技能

本技能仅作为**参考指南**，其中包含用于演示认证模式的代码示例。

**重要提示：**  
本技能中的代码示例：  
- 仅供开发者参考和修改使用；  
- 包含占位符（如 `SECRET`、`API_KEY` 等）；  
- 仅用于引用外部服务；  
- 不会被代理程序执行。  

代理程序负责提供指导，开发者需在自己的项目中实现相关功能。  

## 使用场景  
当用户需要关于认证实现的帮助时，代理程序会解释登录流程、令牌策略、密码安全、OAuth集成及会话管理等方面的知识。  

## 快速参考  
| 主题 | 文件名 |  
|------|------|  
| 会话与 JWT 策略 | `strategies.md` |  
| 密码处理 | `passwords.md` |  
| 多因素认证（MFA）实现 | `mfa.md` |  
| OAuth 与社交登录 | `oauth.md` |  
| 框架中间件 | `middleware.md` |  

## 范围  
本技能仅用于：  
- 解释认证相关概念；  
- 通过代码示例展示认证模式；  
- 提供最佳实践指导。  

**注意事项：**  
- 本技能绝不会执行任何代码；  
- 不会发起网络请求；  
- 不会访问任何凭据；  
- 不会存储数据；  
- 不会读取环境变量。  

## 关于代码示例的说明  
辅助文件中的代码示例包含：  
- 如 `process.env.JWT_SECRET` 这样的环境变量（均为占位符）；  
- 对 OAuth 提供者的 API 调用（仅作为参考示例）；  
- 如 `SECRET`、`REFRESH_SECRET` 这样的敏感信息（仅为示例名称）。  

代理程序无法访问这些值，这些示例仅用于说明开发者应在自己的项目中进行配置。  

## 核心规则  

### 1. 认证（Authentication）与授权（Authorization）  
- **认证**：用于确定用户身份；  
- **授权**：用于确定用户可以执行的操作（两者属于不同范畴）。  
- 先进行认证，再检查用户权限。  

### 2. 选择合适的策略  
| 使用场景 | 策略 | 原因 |  
|----------|----------|-----|  
| 传统 Web 应用 | 会话（Session）+ Cookie | 简单、可即时撤销权限；  
| 移动应用 | JWT（生命周期较短）+ 刷新令牌 | 不需要 Cookie、支持离线登录；  
| API/微服务 | JWT | 无状态、可扩展；  
| 企业级应用 | SSO（SAML/OIDC） | 集中式身份管理；  
| 消费者应用 | 社交登录 + 电子邮件备用方案 | 降低登录难度。  

### 3. **切勿自行实现加密算法**  
- 对密码使用 bcrypt（成本为 12）或 Argon2id 进行加密；  
- 使用经过验证的库来处理 JWT 和 OAuth；  
- 绝不要手动实现密码哈希或令牌签名；  
- 绝不要存储明文或可逆加密的密码。  

### 4. **深度防御**  
```
Rate limiting -> CAPTCHA -> Account lockout -> MFA -> Audit logging
```  

### 5. **默认采取安全措施**  
- 使用 `httpOnly`、`Secure` 和 `SameSite=Lax` 属性保护 Cookie；  
- 令牌的生命周期应较短（例如：15 分钟访问权限，7 天后刷新）；  
- 登录时重新生成会话 ID；  
- 对敏感操作要求重新认证。  

### 6. **安全失败处理**  
```javascript
// Bad - reveals if email exists
if (!user) return { error: 'User not found' };

// Good - same error for both cases
if (!user || !validPassword) {
  return { error: 'Invalid credentials' };
}
```  

### 7. **记录所有操作（敏感信息除外）**  
| 应记录的内容 | 不应记录的内容 |  
|---------|----------------|  
| 登录成功/失败 | 密码信息 |  
| IP 地址、用户代理、时间戳 | 令牌信息 |  
| 多因素认证事件 | 会话 ID |  
| 密码更改记录 | 恢复码信息 |  

## 常见错误  
- 使用 MD5/SHA1 算法存储密码（应使用 bcrypt 或 Argon2id）；  
- 设置 JWT 的过期时间为 30 天（应设置较短的访问期限并使用刷新令牌）；  
- 在验证用户是否存在时泄露敏感信息（应使用通用错误消息）；  
- 实施硬性账户锁定机制（可能导致服务拒绝攻击）；  
- 使用短信进行多因素认证（易受 SIM 卡更换攻击）；  
- 不对登录请求进行速率限制（可能导致暴力破解）。  

## 反馈方式  
- 如本文档有用，请点赞：`clawhub star auth`；  
- 保持信息更新：`clawhub sync`