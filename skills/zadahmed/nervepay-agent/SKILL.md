---
name: nervepay
description: 代理身份与分析：使用 Ed25519 签署请求，追踪 API 使用情况，建立代理的信誉度。这些功能应在调用外部 API 之后启用。
metadata: {"openclaw":{"emoji":"🔐","requires":{"bins":["node","curl"],"env":["NERVEPAY_DID","NERVEPAY_PRIVATE_KEY"]},"primaryEnv":"NERVEPAY_PRIVATE_KEY"}}
---

# NervePay — 代理使用说明

您是一个拥有 NervePay 身份的 AI 代理。此技能允许您通过加密方式证明自己的身份，并记录您的操作（用于分析/建立信誉）。

## 该技能的功能

- **身份验证**：使用 Ed25519 算法对请求进行签名，以确保 API 提供者确认请求确实来自您。
- **记录操作**：记录每次对外 API 的调用，以建立您的信誉。
- **建立信任**：经过验证的使用历史证明您的合法性。

## 设置：获取您的身份信息

如果您还没有 `NERVEPAY_DID` 和 `NERVEPAY_PRIVATE_KEY` 环境变量，请先完成注册：

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
- `claim_url` → 提供给您的人类所有者，以便他们可以认领您

您可以立即开始身份验证。虽然通过 `claim_url` 进行人类认领是可选的，但为了获得更高的信任分数，我们建议这样做。

## 发送经过身份验证的请求

使用辅助脚本对请求进行签名并发送：

```bash
# Authenticated GET
node {baseDir}/nervepay-request.mjs GET /v1/agent-identity/whoami

# Authenticated POST
node {baseDir}/nervepay-request.mjs POST /v1/agent-identity/track-service '{"service_name":"openai","endpoint":"/v1/chat/completions","success":true}'
```

该脚本会自动处理 Ed25519 签名。它会从环境中读取 `NERVEPAY_DID`、`NERVEPAY_PRIVATE_KEY` 和 `NERVEPAY_API_URL`（默认值：https://api.nervepay.xyz）。

## ⚠️ 强制要求：必须记录对外 API 的使用情况 ⚠️

**您必须记录每一次对外 API 的调用。这是必须的，没有例外。**

每当您调用 OpenAI、Stripe、GitHub、天气 API 或任何其他外部服务时，都必须立即向 NervePay 报告。这是此技能的核心功能。

### 快速追踪（最简单的方法）

在每次对外调用后，立即使用简化的追踪辅助工具：

```bash
# Minimal - just service, endpoint, and success/failure
node {baseDir}/nervepay-track.mjs openai /v1/chat/completions success

# With response time
node {baseDir}/nervepay-track.mjs openai /v1/chat/completions success 1250

# With cost
node {baseDir}/nervepay-track.mjs stripe /v1/charges success 850 10.00
```

### 完整追踪（更多详细信息）

如需包含所有字段的完整追踪记录，请使用：

```bash
node {baseDir}/nervepay-request.mjs POST /v1/agent-identity/track-service '{
  "service_name": "openai",
  "endpoint": "/v1/chat/completions",
  "method": "POST",
  "success": true,
  "response_time_ms": 1250,
  "amount": "0.05",
  "currency": "USD"
}'
```

### 示例工作流程（请按照此步骤操作）

```bash
# 1. Call external API
response=$(curl https://api.openai.com/v1/chat/completions ...)

# 2. IMMEDIATELY track it (don't forget!)
node {baseDir}/nervepay-track.mjs openai /v1/chat/completions success

# 3. Continue with your work
echo "$response"
```

**为什么必须进行追踪：**
- 建立您的信誉分数（证明您的合法性）。
- 向 API 提供者展示您的使用历史。
- 跟踪所有服务的成本和成功率。
- 这正是 NervePay 存在的目的——如果不进行追踪，就等于没有使用它。

**请记住：** 必须在调用后立即进行记录，切勿延迟。养成这个习惯。

## 🚀 自动追踪（推荐给懒惰的代理）

**厌倦了每次都记得记录吗？** 使用自动追踪功能吧！它会自动拦截所有的 HTTP 请求！

### 自动追踪的工作原理

`nervepay-instrument.mjs` 脚本会修改 Node.js 的 `fetch()`、`http.request()` 和 `https.request()` 方法，从而自动记录每一次对外 API 的调用。无需任何代码修改！

### 设置：启用自动追踪

**选项 1：命令行参数（推荐）**
```bash
node --import {baseDir}/nervepay-instrument.mjs your-agent.js
```

**选项 2：环境变量（全局设置）**
```bash
export NODE_OPTIONS="--import /path/to/nervepay-instrument.mjs"
node your-agent.js
```

**选项 3：在代码中编程实现**
```javascript
// At the very top of your entry file
import './nervepay-skill/nervepay-instrument.mjs';

// Now all HTTP calls are auto-tracked!
await fetch('https://api.openai.com/...');  // Automatically tracked
```

### 自动追踪的内容包括：

✅ 所有对外 API 的 `fetch()` 调用
✅ 所有的 `http.request()` 和 `https.request()` 调用
✅ 调用的成功/失败状态
✅ 响应时间（以毫秒为单位）
✅ HTTP 状态码

**注意：** 不会追踪以下内容：
- 对 NervePay 本身的调用（避免无限循环）
- `localhost` 或内部 IP 地址（192.168.x.x, 10.x.x.x）的调用

### 禁用自动追踪

```bash
export NERVEPAY_AUTO_TRACK=false
```

### 示例

```bash
# Set your credentials
export NERVEPAY_DID="your-did"
export NERVEPAY_PRIVATE_KEY="your-key"

# Run your agent with auto-instrumentation
node --import {baseDir}/nervepay-instrument.mjs your-agent.js

# All HTTP calls in your-agent.js are now automatically tracked!
```

**总结：** 使用自动追踪功能后，您根本无需担心忘记记录。这一切都会自动完成。🎉

## 与 OpenClaw 网关配对（ClawBot 的自动配置）

如果您是像 ClawBot 这样的代理，负责管理 OpenClaw 网关实例，可以使用 NervePay 的配对流程进行自动配置。

### 先决条件

**您必须先拥有 NervePay 身份！** 请先完成上述的“设置：获取您的身份信息”部分，注册并获取 `NERVEPAY_DID` 和 `NERVEPAY_PRIVATE_KEY`，然后再进行配对。

**建议：** 在配对网关之前，让人类所有者通过 `claim_url` 对您进行认领，以获得更高的信任分数。

### 配对流程

1. **首次配对：** 注册您的代理身份，并选择是否让人类所有者进行认领。
2. **用户在 NervePay 仪表板中生成配对代码**（代码有效期为 10 分钟）。
3. **您使用代理的 DID（Ed25519 签名）进行身份验证，并发送网关详细信息**。
4. **NervePay 会存储** 加密的网关令牌，并将其与您的 DID 关联起来。
5. **只有您** 可以之后刷新该令牌（需要使用您的 DID 进行验证）。

### 完成配对

当您的人类所有者告诉您“连接到 nervepay [CODE]”时，请按照以下步骤操作：

```bash
# 1. Collect gateway details from your environment/config
PAIRING_CODE="ABC123"  # From user
GATEWAY_URL="https://your-openclaw-gateway.com"
GATEWAY_TOKEN="your-gateway-bearer-token"
GATEWAY_NAME="My Gateway"

# 2. Send pairing request (authenticated with your agent DID)
node {baseDir}/nervepay-request.mjs POST /v1/integrations/openclaw/pairing/complete '{
  "pairing_code": "'$PAIRING_CODE'",
  "gateway_url": "'$GATEWAY_URL'",
  "gateway_token": "'$GATEWAY_TOKEN'",
  "gateway_name": "'$GATEWAY_NAME'",
  "max_concurrent_agents": 8,
  "default_timeout_seconds": 3600
}'
```

**成功后的响应：**
```json
{
  "gateway_id": "uuid-here",
  "gateway_name": "My Gateway",
  "status": "completed",
  "message": "Gateway 'My Gateway' successfully paired with agent did:nervepay:agent:xyz"
}
```

### 刷新网关令牌

当您的 OpenClaw 网关令牌过期时，请推送新的令牌：

```bash
GATEWAY_ID="gateway-uuid-from-pairing"
NEW_TOKEN="new-gateway-bearer-token"

node {baseDir}/nervepay-request.mjs POST /v1/integrations/openclaw/gateways/$GATEWAY_ID/refresh-token '{
  "new_token": "'$NEW_TOKEN'"
}'
```

**安全性：** NervePay 会验证您是最初配置该网关的代理（通过 `linked_agent_did` 进行验证）。只有您才能刷新该网关的令牌。

### 为什么需要配对？

- **用户无需进行任何手动设置**（只需提供一个代码即可）。
- **加密身份验证** 确保您控制着网关。
- **令牌加密** 保护网关凭证的安全（使用 AES-256-GCM 加密）。
- **自动过期检测**：如果网关返回 401 错误，NervePay 会标记令牌为过期。
- **信任机制**：经过验证的 DID 证明网关由您管理。

## 常用命令

### 测试身份验证
```bash
node {baseDir}/nervepay-request.mjs GET /v1/agent-identity/whoami
```

返回您的 DID、名称、信誉分数，并确认身份验证是否成功。

### 检查您的权限
```bash
node {baseDir}/nervepay-request.mjs GET /v1/agent-identity/capabilities
```

显示您的消费限制、允许的操作和权限。

### 验证其他代理
```bash
curl "https://api.nervepay.xyz/v1/agent-identity/verify/did:nervepay:agent:abc123xyz"
```

无需身份验证。返回任何代理的公开信息、信誉和交易统计。

### 查询认领状态（检查是否已被人类认领）
```bash
curl "https://api.nervepay.xyz/v1/agent-identity/register-pending/SESSION_ID/status"
```

返回结果：`pending`、`claimed`、`expired` 或 `revoked`。

## 签名的作用

| 保证内容 | 实现方式 |
|-----------|-----|
| **身份验证**（调用者是谁） | 服务器使用您的公钥验证 Ed25519 签名 |
| **数据完整性**（发送了什么内容） | 签名包含方法、路径、查询参数和请求体哈希值——任何篡改都会导致验证失败 |
| **防重放** | 唯一的随机数加上时间戳，防止被截获的请求被重新使用 |
| **跨平台身份识别** | 您的 DID 可在所有支持 NervePay 标头的平台上识别您的身份 |

## 必需的请求头信息（脚本已自动处理）

辅助脚本会自动添加以下请求头：
- `Agent-DID`：您的 DID
- `X-Agent-Signature`：Base64 编码的 Ed25519 签名
- `X-Agent-Nonce`：唯一的随机数（UUID）
- `X-Signature-Timestamp`：ISO 8601 标识的时间戳

## 安全注意事项

- **私钥**：切勿将其发送给任何服务器。只需发送签名即可。
- **随机数**：每次请求都生成新的随机数（由脚本处理）。
- **时间戳**：必须与服务器时间相差在 5 分钟以内。
- **助记词**：用于恢复身份的 24 个单词短语。请安全地离线存储。

## 完整的 API 文档

请参阅 `{baseDir}/api.md` 以获取完整的端点文档、错误代码和高级使用说明。

---

**API 基础地址：** https://api.nervepay.xyz/v1
**文档：** https://nervepay.xyz/docs
**GitHub：** https://github.com/nervepay/nervepay