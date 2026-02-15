---
name: siwa
version: 0.2.0
description: >
  SIWA (Sign-In With Agent) authentication for ERC-8004 registered agents.
---

# SIWA SDK

**使用代理进行登录（Sign-In With Agent, SIWA）**：该功能允许AI代理通过其ERC-8004链上身份验证来访问各种服务。

## 安装

```bash
npm install @buildersgarden/siwa
```

## 技能（Skills）

### 代理端（签名操作，Agent-Side Signing）

根据您的钱包提供商选择相应的技能：

- [Circle](https://siwa.id/skills/circle/skill.md) — 由Circle控制的开发者钱包
- [Privy](https://siwa.id/skills/privy/skill.md) — Privy服务器钱包
- [Private Key](https://siwa.id/skills/private-key/skill.md) — 原始私钥（适用于Viem LocalAccount）
- [Keyring Proxy](https://siwa.id/skills/keyring-proxy/skill.md) — 自托管代理，支持可选的双因素认证（2FA）

### 服务器端（验证操作，Server-Side Verification）

- [服务器端验证](https://siwa.id/skills/server-side/skill.md) — 支持Next.js、Express、Hono、Fastify等框架

## SDK模块（SDK Modules）

| 导入路径 | 描述 |
|--------|-------------|
| `@buildersgarden/siwa` | 核心模块：用于签名、验证和生成随机数（signSIWAMessage, verifySIWA, createSIWANonce） |
| `@buildersgarden/siwa/signer` | 提供签名器工厂（Signer factories） |
| `@buildersgarden/siwa/erc8128` | 支持ERC-8128协议的HTTP签名/验证功能 |
| `@buildersgarden/siwa/receipt` | 提供HMAC收据生成辅助工具 |
| `@buildersgarden/siwa/nonce-store` | 用于存储随机数的模块（支持内存、Redis、KV存储方式） |
| `@buildersgarden/siwa/next` | Next.js中间件 |
| `@buildersgarden/siwa/express` | Express中间件 |
| `@buildersgarden/siwa/hono` | Hono中间件 |
| `@buildersgarden/siwa/fastify` | Fastify中间件 |

## 链接（Links）

- [官方文档](https://siwa.id/docs)
- [ERC-8004标准](https://eips.ethereum.org/EIPS/eip-8004)
- [ERC-8128标准](https://eips.ethereum.org/EIPS/eip-8128)