---
name: nostrkey
description: 用于AI代理的加密身份SDK——生成Nostr密钥对、签署事件、加密消息以及持久化身份信息。
version: 0.1.1
metadata:
  openclaw:
    requires:
      bins:
        - pip
    install:
      - kind: uv
        package: nostrkey
        bins: []
    homepage: https://github.com/HumanjavaEnterprises/nostrkey.app.OC-python.src
---
# NostrKey — 用于 AI 代理的加密身份验证机制

您是一个 AI 代理，需要在 Nostr 协议上拥有可验证的身份。使用 `nostrkey` Python SDK 来生成密钥对、签署事件、加密消息，并在会话之间持久化您的身份。

## 安装

```bash
pip install nostrkey
```

## 核心功能

### 生成身份

使用您自己的 npub/nsec 密钥对创建一个新的 Nostr 身份：

```python
from nostrkey import Identity

me = Identity.generate()
# me.npub  — your public identity (share freely)
# me.nsec  — your private key (never expose)
```

### 导入现有身份

如果您已经拥有密钥：

```python
me = Identity.from_nsec("nsec1...")
# or
me = Identity.from_hex("deadbeef...")
```

### 签署事件

签署任何 Nostr 事件（类型 1 = 文本笔记，类型 0 = 元数据等）：

```python
event = me.sign_event(
    kind=1,
    content="Hello from an AI agent",
    tags=[]
)
# event.id, event.sig are now set and verifiable by anyone
```

### 发布到中继

将已签署的事件发送到 Nostr 网络：

```python
from nostrkey.relay import RelayClient

async with RelayClient("wss://relay.damus.io") as relay:
    await relay.publish(event)
```

### 加密私有消息（NIP-44）

将加密后的消息发送给另一个 npub：

```python
from nostrkey.crypto import encrypt, decrypt

ciphertext = encrypt(
    sender_nsec=me.nsec,
    recipient_npub="npub1recipient...",
    plaintext="This is private"
)

plaintext = decrypt(
    recipient_nsec=me.nsec,
    sender_npub="npub1sender...",
    ciphertext=ciphertext
)
```

### 保存和加载身份（加密文件）

在会话之间持久化您的身份：

```python
# Save (encrypted with passphrase)
me.save("my-identity.nostrkey", passphrase="strong-passphrase")

# Load later
me = Identity.load("my-identity.nostrkey", passphrase="strong-passphrase")
```

### 通过 NIP-46 Bunker 进行委托签名

对于高风险操作，请求人类发起人共同签名：

```python
from nostrkey.bunker import BunkerClient

bunker = BunkerClient(me.private_key_hex)
await bunker.connect("bunker://npub1human...?relay=wss://relay.damus.io")
signed = await bunker.sign_event(kind=1, content="Human-approved action")
```

## 各模块的使用场景

| 任务 | 模块 | 功能 |
|------|--------|----------|
| 生成新身份 | `nostrkey` | `Identity.generate()` |
| 导入现有密钥 | `nostrkey` | `Identity.from_nsec()` / `Identity.from_hex()` |
| 签署事件 | `nostrkey` | `identity.sign_event()` |
| 发布到中继 | `nostrkey.relay` | `RelayClient.publish()` |
| 订阅事件 | `nostrkey.relay` | `RelayClient.subscribe()` |
| 加密消息 | `nostrkey.crypto` | `encrypt()` / `decrypt()` |
| 委托签名 | `nostrkey.bunker` | `BunkerClient.sign_event()` |
| 保存/加载身份 | `nostrkey` | `identity.save()` / `Identity.load()` |
| 低级密钥操作 | `nostrkey.keys` | `generate_keypair()`、`hex_to_npub()` 等 |

## 重要提示

- **切勿泄露您的 nsec 密钥。** 将其视作密码一样保护。使用强密码通过 `identity.save()` 方法来保存它。
- **优先使用异步操作。** 中继和委托签名操作需要 `asyncio`。请使用 `async with` 来处理中继连接。
- **所有事件均使用 secp256k1 算法进行 Schnorr 签名**，符合 Nostr 协议（NIP-01）的要求。
- **NIP-44 加密** 使用 ECDH + HKDF + ChaCha20 算法，并添加长度填充——适用于代理之间的安全通信或代理与人类之间的通信。
- `.nostrkey` 文件在存储时会被加密。切勿将原始的 nsec 值保存在磁盘上。