---
name: blowfish-launch
description: 通过 Blowfish Agent API 在 Solana 上启动代币（使用 Meteora 动态绑定曲线）。当用户需要在 Solana 上启动、部署或创建代币、检查代币的启动状态、列出已启动的代币或领取交易费用时，可以使用此功能。相关事件触发条件包括：`launch token`、`deploy token`、`create token`、`blowfish launch`、`check launch status`、`claim fees`。
---

# Blowfish代币的发布

通过Blowfish Agent API以编程方式在Solana上发布代币。

**基础URL：** `https://api-blowfish.neuko.ai`

## 先决条件

- 一个Solana密钥对（ed25519格式）。私钥应作为`WALLET_SECRET_KEY`环境变量（JSON字节数组）提供。
- Node.js 18.0或更高版本，或装有`@solana/web3.js`、`tweetnacl`、`bs58`库的Bun环境。

## 工作流程

1. **身份验证** — 基于钱包的挑战-响应机制 → 生成JWT令牌（有效期15分钟）
2. **发布代币** — 发送POST请求并传递代币参数 → 接收`eventId`（代币发布的唯一标识符）
3. **状态检查** — 通过`eventId`发送GET请求以获取代币的发布状态（成功或失败）
4. **完成** — 代币通过Meteora DBC在Solana上成功发布

## 快速发布方式

运行捆绑好的脚本：

```bash
WALLET_SECRET_KEY='[...]' bun run scripts/blowfish-launch.ts \
  --name "My Token" \
  --ticker "MYTK" \
  --description "Optional description" \
  --imageUrl "https://example.com/logo.png"
```

## API接口

### 身份验证
- `POST /api/auth/challenge` — 发送 `{wallet}` 和 `{nonce}` 参数 → 生成JWT令牌
- `POST /api/auth/verify` — 发送 `{wallet, nonce, signature}` 参数 → 验证身份并获取 `{token}`（生成的JWT令牌）

**签名方式**：使用ed25519算法对消息“Sign this message to authenticate: <nonce>`进行签名，并使用base58编码生成签名。

### 代币管理
- `POST /api/v1/tokens/launch` — 发送 `{name, ticker, description?, imageUrl?}` 参数 → 发布代币并获取`eventId`
- `GET /api/v1/tokens/launch/status/:eventId` — 持续检查代币的状态（成功、失败或处于速率限制中）
- `GET /api/v1/tokens/` — 查看所有已发布的代币
- `GET /api/v1/tokens/:id` — 获取特定代币的详细信息

### 代币费用领取
- `GET /api/v1/claims/` — 查看可领取的费用
- `POST /api/v1/claims/:tokenId` — 领取指定代币的费用

## 代币参数规则

| 参数 | 规则 |
|-------|-------|
| `name` | 1-255个字符，必填 |
| `ticker` | 2-10个字符，必须以`^[A-Z0-9]+`开头，必填 |
| `description` | 最多1000个字符，可选 |
| `imageUrl` | 最多255个字符，可选 |

## 错误处理

- **409** — 所选的`ticker`已被占用，请选择其他`ticker`。
- **401** — JWT令牌已过期，请重新进行身份验证。
- **速率限制**：每个代理每天只能发布一次代币。

## 完整API参考

请参阅[references/api.md](references/api.md)以获取完整的API接口文档。