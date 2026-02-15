---
name: sage-auth
description: Sage钱包的认证与密钥管理功能包括：登录/登出、生成助记词、导入/删除密钥以及管理钱包身份信息。
---

# Sage Auth

Sage Auth 提供了钱包的认证和密钥管理功能。

## 接口（Endpoints）

### 会话管理（Session Management）

| 接口 | 请求参数（Payload） | 功能描述 |
|----------|------------------|-------------------|
| `login` | `{"fingerprint": 1234567890}` | 登录钱包 |
| `logout` | `{}` | 注销会话 |

### 密钥管理（Key Management）

| 接口 | 请求参数（Payload） | 功能描述 |
|----------|------------------|-------------------|
| `get_keys` | `{}` | 列出所有钱包密钥 |
| `get_key` | `{"fingerprint": 1234567890}` | 获取特定密钥的信息 |
| `get_secret_key` | `{"fingerprint": 1234567890}` | 获取助记词（敏感信息！） |
| `generate_mnemonic` | `{"use_24_words": false}` | 生成新的助记词 |
| `import_key` | （详见下方） | 通过助记词导入钱包 |
| `delete_key` | `{"fingerprint": 1234567890}` | 删除钱包密钥 |
| `rename_key` | `{"fingerprint": 1234567890, "name": "My Wallet"}` | 重命名钱包 |
| `set_wallet_emoji` | `{"fingerprint": 1234567890, "emoji": "🌱"}` | 设置钱包的图标 |

### 密钥导入请求参数（Import Key Payload）

```json
{
  "name": "My Wallet",
  "key": "abandon abandon abandon ... about",
  "derivation_index": 0,
  "hardened": true,
  "unhardened": true,
  "save_secrets": true,
  "login": true,
  "emoji": "🌱"
}
```

### 数据库管理（Database Management）

| 接口 | 请求参数（Payload） | 功能描述 |
|----------|------------------|-------------------|
| `resync` | `{"fingerprint": 1234567890, "delete_coins": false, ...}` | 同步钱包数据 |
| `delete_database` | `{"fingerprint": 1234567890, "network": "mainnet"}` | 删除钱包数据库 |

### 主题管理（Themes Management）

| 接口 | 请求参数（Payload） | 功能描述 |
|----------|------------------|-------------------|
| `get_user_themes` | `{}` | 列出用户拥有的主题 NFTs |
| `get_user_theme` | `{"nft_id": "nft1..."}` | 获取特定主题 |
| `save_user_theme` | `{"nft_id": "nft1..."}` | 保存用户主题 |
| `delete_user_theme` | `{"nft_id": "nft1..."}` | 删除用户主题 |

## 示例（Examples）

```bash
# Login
sage_rpc login '{"fingerprint": 1234567890}'

# List keys
sage_rpc get_keys '{}'

# Generate new mnemonic
sage_rpc generate_mnemonic '{"use_24_words": true}'

# Import wallet
sage_rpc import_key '{
  "name": "Trading Wallet",
  "key": "word1 word2 ... word24",
  "save_secrets": true,
  "login": true
}'
```

## 安全提示（Security Notes）

- `get_secret_key` 会返回助记词，请务必谨慎处理。
- 切勿以明文形式记录或存储助记词。
- 对于仅用于查看功能的钱包导入操作，建议将 `save_secrets` 参数设置为 `false`。