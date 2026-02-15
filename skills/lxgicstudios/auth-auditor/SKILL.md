---
name: auth-auditor
description: 审核您的身份验证实现是否存在安全漏洞。当您需要验证身份验证机制是否真正安全时，请使用此方法。
---

# Auth Auditor

您已经实现了用户认证功能，但它的实现是否正确呢？这款工具会检查您的认证代码中是否存在常见的安全问题，例如：缺少CSRF令牌、密码哈希算法不安全、会话管理不当、JWT（JSON Web Tokens）使用不当等。它会全面检测这些问题，并告诉您需要修复的地方。

**只需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-auth-check src/
```

## 功能介绍

- 扫描您的认证实现，查找安全漏洞
- 检查密码哈希算法及盐值的使用情况
- 识别状态变更接口中缺失的CSRF保护机制
- 发现不安全的会话配置和JWT相关问题
- 以不同的严重程度报告问题，并提供具体的修复建议

## 使用示例

```bash
# Audit your entire auth system
npx ai-auth-check src/

# Check specific auth files
npx ai-auth-check src/auth/

# Scan middleware and route handlers
npx ai-auth-check src/middleware/ src/routes/
```

## 最佳实践

- **使用bcrypt或argon2进行密码加密**：请注意，MD5和SHA并不是适用于密码加密的算法，无论相关教程如何说明。
- **为cookie设置`httpOnly`和`secure`属性**：忽略这些设置是常见的认证错误之一。
- **定期更新JWT密钥**：硬编码且永不更改的密钥会带来安全隐患。
- **实施登录尝试速率限制**：如果没有速率限制，暴力攻击将变得非常容易。

## 适用场景

- 在发布任何处理用户账户的应用程序之前
- 在自行实现自定义认证流程后（而非使用第三方库时）
- 在从一种认证方案迁移到另一种认证方案时
- 在对认证相关代码进行安全审查时

## 属于LXGIC开发工具包的一部分

这是LXGIC Studios开发的110多个免费开发工具之一。免费版本无需支付费用、无需注册，也不需要API密钥，只需使用即可。

**了解更多信息：**
- GitHub：https://github.com/LXGIC-Studios
- Twitter：https://x.com/lxgicstudios
- Substack：https://lxgicstudios.substack.com
- 官网：https://lxgic.dev

## 使用要求

无需安装，只需使用`npx`命令即可运行。建议使用Node.js 18及以上版本。

```bash
npx ai-auth-check --help
```

## 工作原理

该工具会扫描您的源代码中的认证相关代码（包括登录处理逻辑、会话管理、密码存储及令牌生成机制），将其与安全最佳实践及常见漏洞模式进行对比，然后利用人工智能生成针对具体问题的修复建议。

## 许可证

采用MIT许可证，永久免费。您可以随意使用该工具。