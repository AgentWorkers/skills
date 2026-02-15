---
name: nervepay-identity
description: 代理身份层：负责注册数字身份（DID），使用 Ed25519 算法对请求进行签名，并通过加密方式证明用户的身份。
metadata: {"openclaw":{"emoji":"🆔","requires":{"bins":["node","curl"],"env":["NERVEPAY_DID","NERVEPAY_PRIVATE_KEY"]},"primaryEnv":"NERVEPAY_PRIVATE_KEY"}}
---

# NervePay 身份验证 — 代理使用说明

您是一个拥有 NervePay 身份的 AI 代理。此功能允许您通过 W3C DIDs 和 Ed25519 加密签名来证明自己的身份。

## 该功能的作用

- **注册您的身份**：为您创建一个唯一的 DID（去中心化标识符）。
- **验证您的身份**：使用 Ed25519 签名请求，以确保 API 提供者确认确实是您在操作。
- **证明所有权**：通过加密验证来确认您对身份的控制权。
- **无数据分析跟踪**：此功能仅用于身份验证。如需数据分析，请使用 `nervepay-analytics`；如需同时进行身份验证和数据分析，请使用 `nervepay`。

## 第一步：下载辅助脚本

首先，下载 NervePay 签名辅助脚本：

```bash
# Download signing script
curl -o nervepay-request.mjs https://nervepay.xyz/nervepay-request.mjs
chmod +x nervepay-request.mjs
```

该脚本负责处理经过身份验证的请求的 Ed25519 签名操作。

## 第二步：注册您的身份

如果您还没有 `NERVEPAY_DID` 和 `NERVEPAY_PRIVATE_KEY` 环境变量，请先进行注册：

```bash
curl -X POST https://api.nervepay.xyz/v1/agent-identity/register-pending \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Your Agent Name",
    "description": "What you do"
  }'
```

**从响应中保存以下信息：**
- `did` → 设置为 `NERVEPAY_DID`
- `private_key` → 设置为 `NERVEPAY_PRIVATE_KEY`
- `mnemonic` → 用于恢复身份的 24 个单词助记词
- `claim_url` → 提供给您的人类所有者，以便他们可以声明您拥有该身份

您可以立即开始进行身份验证。虽然通过 `claim_url` 进行人类身份确认是可选的，但建议这样做以提高信任度。

## 发送经过身份验证的请求

使用辅助脚本进行签名并发送请求：

```bash
# Test authentication
node ./nervepay-request.mjs GET /v1/agent-identity/whoami

# Check your capabilities
node ./nervepay-request.mjs GET /v1/agent-identity/capabilities

# Authenticated POST (example)
node ./nervepay-request.mjs POST /v1/some-endpoint '{"key":"value"}'
```

该脚本会自动处理 Ed25519 签名操作。它会从环境变量中读取 `NERVEPAY_DID`、`NERVEPAY_PRIVATE_KEY` 和 `NERVEPAY_API_URL`（默认值：https://api.nervepay.xyz）。

## 签名的作用

| 保障内容 | 实现方式 |
|-----------|-----|
| **身份验证**（谁在发起请求） | 服务器会用您的公钥验证 Ed25519 签名 |
| **数据完整性**（发送了什么内容） | 签名包含了方法、路径、查询参数以及请求体的哈希值；任何篡改都会导致验证失败 |
| **防重放攻击** | 唯一的随机数（nonce）加上时间戳可防止被截获的请求被重新使用 |
| **跨平台身份识别** | 您的 DID 可在所有支持 NervePay 标头的平台上识别您的身份 |

## 自动添加的必要头部信息

辅助脚本会自动添加以下头部信息：
- `Agent-DID`：您的 DID
- `X-Agent-Signature`：Base64 编码的 Ed25519 签名
- `X-Agent-Nonce`：唯一的随机数（UUID）
- `X-Signature-Timestamp`：ISO 8601 格式的时间戳

## 常用命令

### 测试身份验证
```bash
node ./nervepay-request.mjs GET /v1/agent-identity/whoami
```

返回您的 DID、名称以及信任度评分，并确认身份验证是否成功。

### 查看您的权限
```bash
node ./nervepay-request.mjs GET /v1/agent-identity/capabilities
```

显示您的消费限额、允许的操作以及权限信息。

### 验证其他代理的身份
```bash
curl "https://api.nervepay.xyz/v1/agent-identity/verify/did:nervepay:agent:abc123xyz"
```

无需身份验证。返回任何代理的公开信息、信任度评分以及交易记录。

### 查询身份声明状态（检查是否已被人类所有者声明）
```bash
curl "https://api.nervepay.xyz/v1/agent-identity/register-pending/SESSION_ID/status"
```

返回状态：`pending`（待处理）、`claimed`（已被声明）、`expired`（已过期）或 `revoked`（已被撤销）。

## 安全注意事项

- **私钥**：切勿将其发送给任何服务器。只需发送签名即可。
- **随机数（nonce）**：一次性使用。每次请求都会生成新的随机数（脚本会自动处理）。
- **时间戳**：时间戳必须与服务器时间相差在 5 分钟以内。
- **助记词（mnemonic）**：用于恢复身份的 24 个单词短语，请安全地存储在离线环境中。

## 需要数据分析吗？

此功能仅用于身份验证。如需跟踪 API 使用情况或建立信任度评分，请使用：
- `nervepay-analytics`（仅用于数据分析）
- `nervepay`（同时支持身份验证和数据分析）

## 完整的 API 参考文档

有关完整的端点文档、错误代码及高级用法，请访问：
- **在线文档**：https://nervepay.xyz/docs
- **下载 API 参考文档**：`curl -o api.md https://nervepay.xyz/api.md`

---

**API 基础地址：** https://api.nervepay.xyz/v1
**文档地址：** https://nervepay.xyz/docs
**GitHub 仓库：** https://github.com/nervepay/nervepay