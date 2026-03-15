---
name: mtproto-2.0
description: >
  **MTProto 2.0 协议实现指南——适用于 Telegram 后端开发**  
  本指南用于指导您在 Telegram 后端开发中实现 MTProto 加密、握手协议、消息序列化功能，以及构建兼容 Telegram 的服务器。内容涵盖 DH 密钥交换、AES-256-IGE 加密算法、TL 语言（Telegram 的内部通信协议）以及相关的安全最佳实践。
version: 1.0.1
---
# MTProto 2.0 协议

本文档提供了 Telegram 的 MTProto 2.0 加密协议的完整实现指南。

### 重要安全提示

本文档仅用于教学目的。在实际生产环境中使用前，请务必注意以下安全要求：

1. **验证认证密钥的长度**：确保在整个实现过程中认证密钥始终为 8 字节。
2. **使用 `crypto/rand`**：切勿使用 `math/rand` 进行加密操作。
3. **与官方实现进行对比测试**：使用 Telegram 的参考实现来验证你的代码。
4. **专家审核**：在处理真实密钥之前，请让密码学家对代码进行审查。
5. **仔细检查错误**：仔细验证所有缓冲区的大小和偏移量。

详细的安全修正信息请参阅 [references/security-notice.md](references/security-notice.md)。

## 快速参考

### 核心组件
- **认证密钥**：通过 DH 密钥交换生成的 256 位对称密钥。
- **服务器盐值**：64 位的防重放随机数。
- **消息密钥**：128 位的消息标识符。
- **AES-256-IGE**：一种具有错误传播功能的加密模式。

### 使用场景
- 实现 MTProto 握手过程（`req_pq → req_DH_params → set_client_DH_params`）。
- 加密/解密 MTProto 消息。
- 序列化 TL 对象。
- 构建兼容 Telegram 的网关。
- 调试连接问题。

## 握手流程

```
Client                              Server
  |                                    |
  | 1. req_pq                        |
  |----------------------------------->|
  |                                    |
  | 2. server_public_key_fingerprints|
  |<-----------------------------------|
  |                                    |
  | 3. req_DH_params                 |
  |----------------------------------->|
  |                                    |
  | 4. server_DH_params              |
  |<-----------------------------------|
  |                                    |
  | 5. set_client_DH_params          |
  |----------------------------------->|
  |                                    |
  | 6. dh_gen_ok                     |
  |<-----------------------------------|
```

详细实现过程请参阅 [references/handshake.md](references/handshake.md)。

## 加密

### AES-256-IGE 加密模式

```go
// Key derivation from Auth Key + Message Key
func deriveKeys(authKey, msgKey []byte) (aesKey, aesIV []byte) {
    x := sha256.Sum256(append(msgKey, authKey[:36]...))
    y := sha256.Sum256(append(authKey[40:76], msgKey...))
    
    aesKey = append(x[:8], y[8:24]...)
    aesIV = append(y[:8], x[24:32]...)
    return
}
```

完整的加密算法实现请参阅 [references/encryption.md](references/encryption.md)。

## 消息格式

### 加密后的消息结构

```
┌─────────────────────────────────────────────────────────┐
│ Auth Key ID     │ 8 bytes  │ SHA1(authKey)[96:128]      │
├─────────────────────────────────────────────────────────┤
│ Message Key     │ 16 bytes │ SHA256(plaintext)[8:24]    │
├─────────────────────────────────────────────────────────┤
│ Encrypted Data  │ Variable │ AES-256-IGE encrypted      │
└─────────────────────────────────────────────────────────┘
```

### 明文结构

```
┌─────────────────────────────────────────────────────────┐
│ Salt            │ 8 bytes  │ Server Salt                │
├─────────────────────────────────────────────────────────┤
│ Session ID      │ 8 bytes  │ Unique session ID          │
├─────────────────────────────────────────────────────────┤
│ Message ID      │ 8 bytes  │ Timestamp + sequence       │
├─────────────────────────────────────────────────────────┤
│ Sequence No     │ 4 bytes  │ Packet sequence            │
├─────────────────────────────────────────────────────────┤
│ Length          │ 4 bytes  │ Message body length        │
├─────────────────────────────────────────────────────────┤
│ Message Body    │ Variable │ TL-serialized data         │
├─────────────────────────────────────────────────────────┤
│ Padding         │ 0-15 B   │ Random padding             │
└─────────────────────────────────────────────────────────┘
```

有关消息格式的详细信息，请参阅 [references/message-format.md](references/message-format.md)。

## TL 语言

### 类型序列化

```tl
// Constructor with ID
user#938458c1 id:long first_name:string = User;

// Method definition
checkPhone#6fe51dfb phone_number:string = Bool;
```

有关 TL 语言的详细信息，请参阅 [references/tl-language.md](references/tl-language.md)。

## 安全特性

### 前向保密性
- 认证密钥通过临时 DH 密钥交换生成。
- 密钥定期更新。
- 即使旧密钥被泄露，也不会暴露历史通信记录。

### 防重放保护
- 每次连接都会生成不同的服务器盐值。
- 消息 ID 包含时间戳。
- 支持序列号验证。
- 提供时间窗口验证机制。

### 完整性验证
- 消息密钥通过 SHA256 哈希生成。
- 使用 AES-IGE 加密模式，并支持错误传播。
- 对消息长度进行验证。

## Go 语言实现

### 基本连接流程

```go
type MTProtoConn struct {
    conn      net.Conn
    authKey   []byte
    salt      int64
    sessionID int64
    seqNo     int32
}

func (m *MTProtoConn) Send(msg TLObject) error {
    // 1. Serialize
    plaintext := msg.Encode()
    
    // 2. Calculate Message Key
    msgKey := calcMsgKey(plaintext, m.authKey)
    
    // 3. Derive AES keys
    aesKey, aesIV := deriveKeys(m.authKey, msgKey)
    
    // 4. Encrypt
    encrypted := encryptAESIGE(plaintext, aesKey, aesIV)
    
    // 5. Construct packet
    packet := constructPacket(m.authKey, msgKey, encrypted)
    
    // 6. Send
    _, err := m.conn.Write(packet)
    return err
}
```

## 参考资料
- [握手过程详细信息](references/handshake.md)：完整的 DH 密钥交换流程。
- [加密算法](references/encryption.md)：AES-256-IGE 加密算法。
- [消息格式](references/message-format.md)：二进制协议格式。
- [TL 语言](references/tl-language.md)：类型序列化机制。
- [安全提示](references/security-notice.md)：生产环境中的关键安全修正内容。

## 官方资源
- [MTProto 官方文档](https://core.telegram.org/mtproto)
- [TL 数据结构](https://core.telegram.org/schema)
- [Telegram API](https://coreTelegram.org/api)