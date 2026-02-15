---
name: auth-checker
description: 审计认证流程以检测安全漏洞
---

# **身份验证检查器（Auth Checker）**

该工具用于扫描您的身份验证实现，以发现潜在的安全漏洞，帮助您避免被黑客攻击。

## **快速入门**

```bash
npx ai-auth-check ./src/auth/
```

## **功能介绍**

- 审查登录/注册流程中的安全风险  
- 检查会话管理的安全性  
- 识别不安全的密码策略  
- 标记不安全的令牌处理方式  

## **使用示例**

```bash
# Audit auth directory
npx ai-auth-check ./src/auth/

# Scan specific auth file
npx ai-auth-check ./src/lib/auth.ts

# Full project scan
npx ai-auth-check ./src --recursive
```

## **能检测的问题**

- 硬编码的凭证  
- 缺少速率限制机制  
- 不安全的会话存储方式  
- JWT（JSON Web Tokens）相关漏洞  
- 缺少CSRF（跨站请求伪造）防护  
- 弱密码验证机制  

## **系统要求**

- 必需安装 Node.js 18 及以上版本。  
- 需要配置 OPENAI_API_KEY。  

## **许可证**

- MIT 许可证。永久免费使用。  

---

**开发团队：LXGIC Studios**  
- GitHub 仓库：[github.com/lxgicstudios/ai-auth-check](https://github.com/lxgicstudios/ai-auth-check)  
- Twitter 账号：[@lxgicstudios](https://x.com/lxgicstudios)