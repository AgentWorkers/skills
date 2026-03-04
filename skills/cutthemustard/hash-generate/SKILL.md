---
name: hash-generate
description: 哈希（Hashing）、HMAC（Hash Message Authentication Code, 哈希消息认证码）、编码/解码（Encoding/Decoding）、UUID（Universally Unique Identifier, 全球唯一标识符）生成以及基于哈希的识别技术。
version: 1.0.0
metadata:
  openclaw:
    emoji: "🔐"
    homepage: https://hash.agentutil.net
    always: false
---
# hash-generate

该功能支持计算哈希值（MD5、SHA-1、SHA-256、SHA-512、CRC32）、生成HMAC签名，以及进行数据的编码/解码（base64、十六进制、URL格式），还能生成UUID，并能识别未知的哈希算法类型。

## 数据处理

该功能会将用户提供的输入数据发送到外部API进行处理。未经用户明确同意，不得发送敏感数据（如密码、密钥或私钥）。服务在处理完成后会立即销毁输入数据，不会对其进行存储或记录。

## 接口端点

### 哈希计算

```bash
curl -X POST https://hash.agentutil.net/v1/hash \
  -H "Content-Type: application/json" \
  -d '{"input": "hello world", "algorithm": "sha256"}'
```

支持的算法：md5、sha1、sha256、sha512、crc32。可选的编码格式：hex（默认）或base64。

### HMAC签名生成

```bash
curl -X POST https://hash.agentutil.net/v1/hmac \
  -H "Content-Type: application/json" \
  -d '{"input": "hello", "key": "secret", "algorithm": "sha256"}'
```

### 数据编码/解码

```bash
curl -X POST https://hash.agentutil.net/v1/encode \
  -H "Content-Type: application/json" \
  -d '{"input": "hello", "operation": "encode", "format": "base64"}'
```

支持的编码格式：base64、hex、URL；解码功能仅支持base64和hex格式。

### 未知哈希算法识别

```bash
curl -X POST https://hash.agentutil.net/v1/identify \
  -H "Content-Type: application/json" \
  -d '{"hash": "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"}'
```

## 响应格式

```json
{
  "hash": "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9",
  "algorithm": "sha256",
  "encoding": "hex",
  "input_length": 11,
  "request_id": "abc-123",
  "service": "https://hash.agentutil.net"
}
```

## 价格方案

- 免费 tier：每天10次查询，无需身份验证。
- 付费 tier：每次查询费用为0.001美元，通过x402协议支付（支付货币为Base上的USDC）。

## 隐私政策

免费 tier无需身份验证，也不会收集任何个人数据。对于付费 tier，仅使用IP地址进行速率限制。