---
name: Auth
description: 为每种使用场景设计并实现符合相应规范的认证系统。
metadata: {"clawdbot":{"emoji":"🛡️","os":["linux","darwin","win32"]}}
---

## 会话（Session）与令牌（Token）  

- **服务器会话（Server Sessions）**：实现简单，可立即撤销，需要会话存储机制——适用于传统Web应用程序。  
- **无状态令牌（Stateless Tokens，如JWT）**：具有可扩展性，无需共享状态——适用于API、微服务及移动应用。  
- **混合模式（Hybrid Approach）**：Web应用使用会话，API接口使用令牌——通常是实际开发中的最佳选择。  
- 为防止CSRF攻击，会话cookie应设置`httpOnly`、`Secure`属性，并将`SameSite`设置为`Lax`。  

## 密码处理（Password Handling）  

- 使用`bcrypt`（计算成本为10-12次哈希运算）、`Argon2id`或`scrypt`进行密码加密；绝对禁止使用`MD5`、`SHA1`或纯`SHA256`。  
- **切勿**存储明文密码、加密后的密码或可逆的哈希值。  
- `bcrypt`/`argon2`的加密过程中会自动包含盐值（salt），无需单独管理。  
- 对密码进行时间安全的比较（time-safe comparison）以防止时间攻击（timing attacks）。  

## 多因素认证（Multi-Factor Authentication, MFA）  

- **TOTP（One-Time Password）**：在安全性和可用性之间取得了良好的平衡。  
- **短信（SMS）**：由于SIM卡容易被替换，安全性较低——高安全性的应用应避免使用。  
- **WebAuthn/Passkeys**：是最强的认证方式，具有抗钓鱼攻击能力——尽可能提供这种认证方式。  
- **恢复码（Recovery Codes）**：在设置多因素认证时生成，存储为哈希值，仅限一次性使用。  

## 无密码登录选项（Passwordless Login Options）  

- **魔法链接（Magic Links）**：通过电子邮件发送包含临时令牌的链接——如果电子邮件可信，则这种方式简单且安全。  
- **WebAuthn**：支持生物识别或安全密钥——当系统支持时，提供最佳的用户体验。  
- **通过电子邮件发送的一次性密码（OTP via Email）**：类似于魔法链接，但用户需要手动复制验证码——适用于不同设备。  
- **仅支持社交登录（Social Login Only）**：适用于消费类应用，可减少用户操作麻烦。  

## 适用场景与选择依据（Use Cases and Selection Criteria）  

- **内部工具（Internal Tools）**：使用公司提供的身份提供者（IdP，如Okta、Azure AD、Google Workspace）进行单点登录（SSO）。  
- **消费类应用（Consumer Apps）**：支持社交登录，并提供电子邮件/密码作为备用方式；对于现代用户界面，优先采用无密码登录。  
- **B2B SaaS（Business-to-Business SaaS）**：为企业客户提供SAML/OIDC支持。  
- **仅提供API访问的应用（API-Only Services）**：为服务账户使用API密钥，为用户授权访问时使用OAuth。  
- **高安全性要求（High Security）**：必须实施多因素认证，优先选择WebAuthn；对于敏感操作，应增加额外的认证步骤。  

## 注册流程（Registration Process）  

- 在账户激活前进行电子邮件验证——防止垃圾邮件并确认用户联系方式的有效性。  
- **最小数据收集（Minimum Data Collection）**：对于大多数应用，电子邮件和密码即可。  
- **密码强度（Password Strength）**：检查密码是否存在于已泄露的密码列表中（如HaveIBeenPwned），而不仅仅是依赖密码复杂度规则。  
- **限制注册频率（Rate Limiting Registration）**：防止注册攻击和滥用。  

## 登录安全（Login Security）  

- **按IP地址和账户限制登录尝试次数（Rate Limiting by IP and Account）**：3-5次失败后应延迟登录或要求输入验证码（CAPTCHA）。  
- **账户锁定（Account Lockout）**：优先采用渐进式锁定机制（progressive locking），而非直接禁用账户（hard lockout）。  
- **不要透露账户是否存在（Don’t Reveal Account Existence）**：无论是输入错误电子邮件还是错误密码，都应显示“凭据无效”。  
- **记录所有认证事件（Log All Authentication Events）**：包括IP地址、用户代理和时间戳。  

## 会话管理（Session Management）  

- **登录时重新生成会话ID（Regenerate Session ID upon Login）**：防止会话被固定（session fixation）。  
- **设置绝对超时时间（Absolute Timeout）**：24小时至7天；同时设置空闲超时时间（idle timeout），以平衡安全性和用户体验。  
- **向用户显示活跃会话（Show Active Sessions）**：允许用户远程登出。  
- **在密码更改或发生安全事件时失效所有会话（ Invalidate All Sessions）**。  

## 账户恢复（Account Recovery）  

- **通过电子邮件链接重置密码（Password Reset via Email Link）**：令牌的有效期最长为1小时，且仅限一次性使用。  
- **避免使用安全问题（Avoid Security Questions）**：这些问题答案容易被猜测或公开。  
- **切勿**在电子邮件中发送密码。  
- **通过其他渠道通知用户密码更改（Notify Users of Password Changes via Alternative Channels）**。  

## “记住我”功能（Remember Me Feature）  

- **使用长期有效的令牌（Use Long-Lived Tokens）**：但不要无限期延长会话的有效期。  
- **服务器端存储哈希后的令牌（Store Hashed Tokens on the Server）**；每次使用时更新令牌。  
- **对于敏感操作（如密码更改、支付）**：仍需用户输入密码。  
- **允许用户撤销已保存的登录设备（Allow Users to Revoke Saved Devices）**。  

## 登出（Logout）  

- **彻底销毁服务器会话（Destroy Server Sessions）**：而不仅仅是清除cookie。  
- **对于令牌（Tokens）**：从客户端删除令牌，并在需要立即撤销时将其加入黑名单。  
- **清除所有与认证相关的存储数据（Clear All Authentication-Related Data）**：包括cookie和localStorage。  
- **提供防CSRF攻击的登出接口（Provide CSRF-Protected Logout Interface）**：防止登出过程中的CSRF攻击。  

## 审计与监控（Audit & Monitoring）  

- **记录所有认证操作（Log All Authentication Activities）**：包括成功登录、失败尝试、密码更改及多因素认证事件。  
- **触发警报的情况（Trigger Alerts for）**：多次登录失败、从新位置/设备登录、用户位置与记录不符等情况。  
- **保留日志（Retain Logs for Compliance）**：至少保留90天，通常为1-2年。  
- **绝不要记录密码或令牌信息（Never Log Passwords or Tokens）**，即使登录失败也不例外。