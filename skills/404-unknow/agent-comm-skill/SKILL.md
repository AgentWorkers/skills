# 代理通信技能（PassDeck）

该技能为AI代理群组提供了安全性和网络基础。它负责处理DID（去中心化身份）的注册、使用Ed25519进行加密签名，以及对敏感数据实施端到端加密（E2EE）。

## 🚀 主要功能

### `agent.register`
- **描述**: 注册一个新的本地代理身份或恢复现有的代理身份。返回代理的唯一DID。
- **参数**: `{ alias?: string }`
- **输出**: `{ localId: string, did: string, publicKey: hex }`

### `message.sign`
- **描述**: 使用代理的私钥对数据包进行签名，确保数据的完整性和不可否认性。
- **参数**: `{ localId: string, payload: any }`
- **输出**: `{ signature: hex }`

### `message.verify`
- **描述**: 根据公钥验证已签名的消息，用于检测数据篡改或未经授权的更新。
- **参数**: `{ publicKeyHex: string, payload: any, signatureHex: string }`
- **输出**: `{ verified: boolean }`

### `network.connect`
- **描述**: 建立与Relay服务器的授权连接，实现DID挑战-响应握手协议。
- **参数**: `{ sessionId: string, localId: string, did: string, onUpdate: function }`
- **输出**: `{ success: true }`

### `secret.encrypt / secret.decrypt`
- **描述**: 提供高级的端到端加密功能，用于在协作环境中管理安全凭证。
- **参数**: `{ payload/ciphertext: any, sessionKey: string }`
- **输出**: `{ ciphertext/decrypted: any }`