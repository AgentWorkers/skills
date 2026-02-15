---
name: openssl
description: 使用 OpenSSL 生成安全的随机字符串、密码和加密令牌。这些生成的随机数据可用于创建密码、API 密钥、机密信息或任何需要安全性的随机数据。
---

# OpenSSL 安全数据生成

使用 `openssl rand` 生成加密安全的随机数据。

## 密码/机密信息生成

```bash
# 32 random bytes as base64 (43 chars, URL-safe with tr)
openssl rand -base64 32 | tr '+/' '-_' | tr -d '='

# 24 random bytes as hex (48 chars)
openssl rand -hex 24

# alphanumeric password (32 chars)
openssl rand -base64 48 | tr -dc 'a-zA-Z0-9' | head -c 32
```

## 常见的数据长度

| 使用场景 | 命令 |
|----------|---------|
| 强密码 | `openssl rand -base64 24` |
| API 密钥 | `openssl rand -hex 32` |
| 会话令牌 | `openssl rand -base64 48` |
| 短 PIN 码（8 位） | `openssl rand -hex 4 | xxd -r -p | od -An -tu4 | tr -d ' ' | head -c 8` |

## 注意事项

- `-base64` 生成的字符串长度约为字节数的 1.33 倍 |
- `-hex` 生成的字符串长度约为字节数的 2 倍 |
- 可通过 `tr -dc` 命令过滤字符集 |
- 对于机密信息，建议至少使用 16 字节（128 位）的长度