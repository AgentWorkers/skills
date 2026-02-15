---
name: Encryption
description: 加密文件、保护密码、管理密钥，并对代码进行审计，以遵循加密的最佳实践。
---

## 使用场景  
- 加密文件、数据库字段或应用程序存储数据  
- 密码哈希处理（使用 bcrypt 或 argon2）  
- 密钥管理（包括密钥的生成、轮换和派生）  
- TLS/证书配置  
- 代码审计（检查是否存在与加密相关的安全漏洞）  
- 移动设备上的安全存储（如 Keychain 或 Keystore）  

## 算法选择  

| 目的                | 推荐算法             | 应避免的算法             |  
|------------------|------------------|------------------|  
| 密码存储            | argon2id, bcrypt (成本≥12)       | MD5, SHA1, 平原 SHA256          |  
| 对称加密            | AES-256-GCM, ChaCha20-Poly1305     | AES-ECB, DES, RC4           |  
| 非对称加密            | RSA-4096+OAEP, Ed25519, P-256     | RSA-1024, PKCS#1 v1.5         |  
| 密钥派生            | PBKDF2 (迭代次数≥600,000), scrypt, argon2  | 单次哈希算法             |  
| JWT 签名            | RS256, ES256             | 使用弱密钥的 HS256           |  
| TLS 安全           | 仅支持 TLS 1.2 及更高版本     | TLS 1.0/1.1, SSLv3           |  

## 重要规则  
1. **切勿重复使用初始化向量（IV）或随机数（nonce）**——使用 AES-GCM 时，重复使用 nonce 可能导致严重安全问题。  
2. **必须使用认证加密（AEAD）**——普通的 CBC 模式可能允许攻击者利用填充信息进行攻击。  
3. **对密码进行哈希处理，而非直接加密**——哈希操作是单向的，无法逆向还原原始密码。  
4. **禁止使用硬编码的密钥**——应使用环境变量、KMS（Key Management Service）或 Vault 等安全存储机制来管理密钥。  
5. **加密过程中禁止使用 `Math.random()`**——必须使用安全的随机数生成器（如 CSPRNG）。  
6. **进行常数时间比较**——防止攻击者通过计时攻击获取密钥信息。  
7. **根据用途分离密钥**——加密密钥、签名密钥和备份密钥应分开存储。  

## 文件加密（命令行接口）  
（具体实现代码请参见 **```bash
# age (modern, simple)
age -p -o file.age file.txt
age -d -o file.txt file.age

# GPG
gpg -c --cipher-algo AES256 file.txt
```**）  

## 平台特定内容  
- 有关代码示例，请参阅 `patterns.md`：  
  - 密码哈希处理（Node.js、Python、Go）  
  - 使用 KMS 的信封加密（Envelope Encryption）  
  - 基于 RS256 的 JWT 签名  
  - 安全令牌的生成  

- 有关移动设备安全存储的详细信息，请参阅 `mobile.md`：  
  - iOS 的 Keychain 支持  
  - Android 的 EncryptedSharedPreferences  
  - SQLCipher 的配置  
  - 生物特征认证的集成  
  - 证书的固定（Certificate Pinning）  

- 有关基础设施安全的详细信息，请参阅 `infra.md`：  
  - TLS 证书的自动续订  
  - HashiCorp Vault 的配置策略  
  - 服务之间的 mTLS（Multi-Protocol TLS）  
  - 备份数据的加密验证  

## 安全审计检查清单  
- [ ] 数据库、日志或环境变量中不存在明文密码  
- [ ] Git 历史记录中不存在敏感信息  
- [ ] 源代码中不存在硬编码的密钥  
- [ ] 加密过程中未使用 `Math.random()`  
- [ ] 未使用过时的加密算法（如 MD5、SHA1、DES）  
- [ ] 未禁用证书验证功能  
- [ ] 初始向量（IV）和随机数（nonce）从未被重复使用  
- [ ] PBKDF2 的迭代次数≥600,000 次；bcrypt 的计算成本≥12  
- [ ] 强制使用 TLS 1.2 及更高版本，禁用旧版本  
- [ ] 密钥轮换流程有明确的文档记录