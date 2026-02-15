---
name: Passkey
description: 实现 WebAuthn 密码令牌时，需避免关键的安全和兼容性问题。
metadata: {"clawdbot":{"emoji":"🔐","os":["linux","darwin","win32"]}}
---

## 关键安全规则  
- 每次认证过程中的挑战必须是唯一的；重复使用的挑战可能导致重放攻击。  
- 必须进行来源验证；如果省略此步骤，用户可能会受到来自相似域名的网络钓鱼攻击。  
- 需要存储并验证签名次数；如果签名次数没有增加，说明可能存在克隆的认证器。  
- 绝不要手动实现CBOR解析功能——使用成熟的库进行处理，因为加密技术较为复杂。  

## 服务器端实现  
- 使用经过实战验证的库：SimpleWebAuthn（JavaScript）、py_webauthn（Python）、webauthn-rs（Rust）。  
- 挑战的有效期很短（最长60-120秒），需在服务器端进行存储。  
- 将凭证ID以Base64格式存储（二进制数据），存储到数据库前需进行编码。  
- 将公钥以COSE格式存储；相关库会自动处理这一过程，无需手动转换。  

## 凭证存储要求  
- 凭证ID：唯一的标识符，用于`allowCredentials`功能中。  
- 公钥：以COSE格式存储，用于签名验证。  
- 签名次数：通过递增计数来检测凭证是否被克隆。  
- “传输提示”（Transport Hint）：帮助浏览器推荐正确的认证器。  

## 注册过程中的注意事项  
- `userVerification: "required"`强制要求用户使用生物识别或PIN码进行验证；`"preferred"`选项则可以跳过此步骤。  
- 通常情况下，证明机制（Attestation）并非必需；强制使用该机制会降低设备的兼容性。  
- 允许每个账户使用多个Passkey（临时密码）。  
- 不同认证器的“驻留密钥”（Resident Key）功能各不相同；不要假设所有认证器都支持可发现的凭证类型。  

## 认证过程中的问题  
- 如果`allowCredentials`为空，将允许使用可发现的凭证；但并非所有Passkey都支持被自动检测。  
- 超时设置过短会让用户感到沮丧；跨设备认证流程至少需要120秒的等待时间。  
- 跨设备认证（如通过二维码）会增加延迟；在蓝牙连接过程中不要设置超时。  

## 用户体验方面  
- 提供密码作为备用方案；并非所有用户都使用支持Passkey的设备。  
- 根据用户需求使用条件化的用户界面（`mediation: "conditional"`）来实现自动补全功能；Passkey会显示在用户名字段中。  
- 注册时提供清晰的信息提示；用户可能不理解“安全密钥”这一术语。  
- 必须提供账户恢复机制；硬件丢失不应导致账户被永久锁定。  

## 平台同步行为  
- Apple的iCloud Keychain可以在Apple设备之间同步，但不能与Android或Windows设备同步。  
- Google Password Manager可以在Android设备和Chrome浏览器之间同步，但不能与Apple设备同步。  
- Windows Hello依赖于TPM（Trusted Platform Module）技术，默认情况下是本地存储的，因此不支持同步。  
- 1Password/Bitwarden提供跨平台同步功能，具有最广泛的兼容性。  

## 测试方法  
- 使用Chrome DevTools > Application > WebAuthn来模拟认证过程（无需使用物理认证器）。  
- 在持续集成（CI）环境中使用虚拟认证器进行测试；自动化测试不需要物理密钥。  
- 需要同时测试驻留式和非驻留式凭证；不同认证流程需要分别进行测试。  
- 跨浏览器测试至关重要；Safari、Chrome和Firefox的实现可能存在差异。