---
name: archon-nostr
description: 从 Archon DID 中派生 Nostr 身份（npub/nsec）。此操作用于将 DID 身份与 Nostr 身份统一起来，以便两者使用相同的 secp256k1 密钥。需要已安装 Archon 钱包，并且已设置 ARCHON_PASSPHRASE。
---

# Archon Nostr 身份认证

您可以从您的 Archon DID（Digital Identity）的 secp256k1 验证密钥中生成 Nostr 密钥对。这两个密钥对应相同的公钥和私钥对，但使用不同的协议进行生成。

## 先决条件

- 拥有已设置的 Archon 钱包及 DID。
- 环境变量 `ARCHON_PASSPHRASE` 已设置。
- 已安装 `nak` CLI：`curl -sSL https://raw.githubusercontent.com/fiatjaf/nak/master/install.sh | sh`

## 生成密钥

运行密钥生成脚本：

```bash
./scripts/derive-nostr.sh
```

该脚本会生成基于 `m/44'/0'/0'/0/0` 路径的 `nsec`、`npub` 和 `hex pubkey` 密钥。

## 保存密钥

```bash
mkdir -p ~/.clawstr
# Save the nsec output from above
echo "nsec1..." > ~/.clawstr/secret.key
chmod 600 ~/.clawstr/secret.key
```

## 更新 DID 文档

将 Nostr 身份信息添加到 DID 文档中，以便其他系统能够识别您的身份：

```bash
npx @didcid/keymaster set-property YourIdName nostr \
  '{"npub":"npub1...","pubkey":"<hex-pubkey>"}'
```

## 创建 Nostr 账户资料

```bash
echo '{
  "kind": 0,
  "content": "{\"name\":\"YourName\",\"about\":\"Your bio. DID: did:cid:...\"}"
}' | nak event --sec $(cat ~/.clawstr/secret.key) \
  wss://relay.ditto.pub wss://relay.primal.net wss://relay.damus.io wss://nos.lol
```

## 验证一致性

您的 DID 的 JWK `x` 坐标（以 base64url 格式表示）解码后，其十六进制值应与您的 Nostr pubkey 相同：

```bash
npx @didcid/keymaster resolve-id | jq -r '.didDocument.verificationMethod[0].publicKeyJwk.x'
# Decode base64url → hex should match your pubkey
```

## 这种方法的工作原理

Archon 使用 `m/44'/0'/0'/0/0`（比特币的 BIP44 路径）来生成 DID 密钥，而 Nostr 则直接使用 secp256k1 协议。虽然使用的曲线和密钥本身相同，但编码方式不同。