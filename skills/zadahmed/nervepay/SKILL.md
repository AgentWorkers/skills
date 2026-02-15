---
name: nervepay
description: 完整的NervePay技术栈：身份验证 + 数据分析。  
注册DID（Digital Identity），使用Ed25519算法签署请求，追踪所有API的使用情况，构建用户信誉体系。
metadata: {"openclaw":{"emoji":"🔐","requires":{"bins":["node","curl"],"env":["NERVEPAY_DID","NERVEPAY_PRIVATE_KEY"]},"primaryEnv":"NERVEPAY_PRIVATE_KEY"}}
---

# NervePay — 代理使用说明

您是一个拥有 NervePay 身份的 AI 代理。此技能提供了完整的 NervePay 功能栈：包括身份验证和数据分析。通过加密方式证明您的身份，并记录您的操作以生成信誉评分。

## 该技能的功能

- **注册您的身份**：为您创建一个唯一的去中心化标识符（DID）。
- **验证您的身份**：使用 Ed25519 算法对请求进行签名，以确保 API 提供者确认确实是您发出的请求。
- **跟踪您的操作**：记录所有外部 API 调用，以建立您的信誉。
- **建立信任**：经过验证的使用历史证明您的合法性。

## 可用的模块化技能

这是完整的 NervePay 功能栈。您也可以单独使用以下技能：
- `nervepay-identity`：仅包含身份验证功能（注册、认证，不包含数据分析）。
- `nervepay-analytics`：仅包含数据分析功能（需要已注册的身份）。
- `nervepay`：包含完整的身份验证和数据分析功能。

## 更新此技能

要获取此技能的最新版本（包含新功能、错误修复和更新的 API 端点），请执行以下操作：

```bash
# Update skill documentation
curl -o SKILL.md https://nervepay.xyz/skill.md

# Update helper scripts
curl -o nervepay-request.mjs https://nervepay.xyz/nervepay-request.mjs
curl -o nervepay-track.mjs https://nervepay.xyz/nervepay-track.mjs
curl -o nervepay-instrument.mjs https://nervepay.xyz/nervepay-instrument.mjs
chmod +x nervepay-request.mjs nervepay-track.mjs nervepay-instrument.mjs
```

**何时更新：** 当您遇到意外错误、出现新的 API 端点，或者距离上次更新已经有一段时间时。

## 第一步：确保辅助脚本可用

NervePay 的辅助脚本应该已经包含在这个技能中。如果缺少这些脚本，请下载它们：

```bash
# Check if scripts exist, download only if missing
for script in nervepay-request.mjs nervepay-track.mjs nervepay-instrument.mjs; do
  if [ ! -f "$script" ]; then
    echo "Downloading $script..."
    curl -o "$script" "https://nervepay.xyz/$script"
    chmod +x "$script"
  fi
done
```

这些脚本负责处理 Ed25519 签名和数据分析跟踪工作。它们位于与此 `SKILL.md` 文件相同的目录中。

## 第二步：获取您的身份

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
- `mnemonic` → 用于恢复的 24 个单词助记词
- `claim_url` → 提供给您的人类所有者，以便他们可以声明您的身份

您可以立即开始进行身份验证。虽然通过 `claim_url` 进行人类身份验证是可选的，但建议这样做以获得更高的信誉评分。

## 发送经过验证的请求

使用辅助脚本进行签名并发送请求：

```bash
# Authenticated GET
node ./nervepay-request.mjs GET /v1/agent-identity/whoami

# Authenticated POST
node ./nervepay-request.mjs POST /v1/agent-identity/track-service '{"service_name":"openai","endpoint":"/v1/chat/completions","success":true}'
```

该脚本会自动处理 Ed25519 签名。它会从环境中读取 `NERVEPAY_DID`、`NERVEPAY_PRIVATE_KEY` 和 `NERVEPAY_API_URL`（默认值：`https://api.nervepay.xyz`）。

## ⚠️ 强制要求：必须跟踪外部 API 使用情况 ⚠️

**您必须记录每一次外部 API 调用。这是强制性的要求。**

每次您调用 OpenAI、Stripe、GitHub、天气 API 或任何其他外部服务时，都必须立即向 NervePay 报告。这是此技能的核心功能。

### 快速跟踪（最简单的方法）

在每次外部调用后立即使用简化的跟踪辅助脚本：

```bash
# Minimal - just service, endpoint, and success/failure
node ./nervepay-track.mjs openai /v1/chat/completions success

# With response time
node ./nervepay-track.mjs openai /v1/chat/completions success 1250

# With cost
node ./nervepay-track.mjs stripe /v1/charges success 850 10.00
```

### 完整跟踪（更多详细信息）

为了进行全面的跟踪，请使用以下方法：

```bash
node ./nervepay-request.mjs POST /v1/agent-identity/track-service '{
  "service_name": "openai",
  "endpoint": "/v1/chat/completions",
  "method": "POST",
  "success": true,
  "response_time_ms": 1250,
  "amount": "0.05",
  "currency": "USD"
}'
```

### 示例工作流程

```bash
# 1. Call external API
response=$(curl https://api.openai.com/v1/chat/completions ...)

# 2. IMMEDIATELY track it (don't forget!)
node ./nervepay-track.mjs openai /v1/chat/completions success

# 3. Continue with your work
echo "$response"
```

**为什么必须进行跟踪：**
- 建立您的信誉评分（证明您的合法性）。
- 向 API 提供者展示您的使用历史记录。
- 跟踪所有服务的成本和成功率。
- 这正是 NervePay 存在的目的——如果不进行跟踪，就等于没有使用它。

**记住：** 在调用后立即进行跟踪，不要延迟。养成这个习惯。

## 🚀 自动跟踪（推荐给懒惰的代理）

**厌倦了手动跟踪吗？** 使用自动跟踪功能——它会自动拦截所有的 HTTP 请求！

### 自动跟踪的工作原理

`nervepay-instrument.mjs` 脚本会修改 Node.js 的 `fetch()`、`http.request()` 和 `https.request()` 方法，从而自动跟踪所有的外部 API 调用。无需修改任何代码！

### 设置：启用自动跟踪

**选项 1：命令行参数（推荐）**
```bash
node --import ./nervepay-instrument.mjs your-agent.js
```

**选项 2：环境变量（全局设置）**
```bash
export NODE_OPTIONS="--import /path/to/nervepay-instrument.mjs"
node your-agent.js
```

**选项 3：编程方式（在您的代码中设置）**
```javascript
// At the very top of your entry file
import './nervepay-skill/nervepay-instrument.mjs';

// Now all HTTP calls are auto-tracked!
await fetch('https://api.openai.com/...');  // Automatically tracked
```

### 自动跟踪的内容

✅ 所有对外部 API 的 `fetch()` 调用。
✅ 所有的 `http.request()` 和 `https.request()` 调用。
✅ 请求的成功/失败状态。
✅ 响应时间（以毫秒为单位）。
✅ HTTP 状态码。

**注意：** 不会跟踪以下内容：**
- 对 NervePay 自身的调用（避免无限循环）。
- `localhost` 或内部 IP 地址（如 `192.168.x.x`、`10.x.x.x`）。

### 禁用自动跟踪

```bash
export NERVEPAY_AUTO_TRACK=false
```

### 示例

```bash
# Set your credentials
export NERVEPAY_DID="your-did"
export NERVEPAY_PRIVATE_KEY="your-key"

# Run your agent with auto-instrumentation
node --import ./nervepay-instrument.mjs your-agent.js

# All HTTP calls in your-agent.js are now automatically tracked!
```

**总结：** 使用自动跟踪功能后，您根本不需要忘记进行跟踪。这一切都会自动完成。🎉

## 与 OpenClaw 网关配对（ClawBot 的自动配置）

如果您是管理 OpenClaw 网关实例的代理（如 ClawBot），可以使用 NervePay 的配对流程进行自动配置。

### 先决条件

**您必须先拥有 NervePay 身份！** 请完成上面的“设置：获取您的身份”部分，注册并获取 `NERVEPAY_DID` 和 `NERVEPAY_PRIVATE_KEY`，然后再进行配对。

**建议：** 在配对网关之前，让您的人类所有者通过 `claim_url` 声明您的身份，以获得更高的信誉评分。

### 配对流程

1. **首次配对：** 注册您的代理身份，并可选地让人类所有者进行身份验证。
2. **用户在 NervePay 仪表板上生成配对代码**（代码有效期为 10 分钟）。
3. **您使用代理的 DID（Ed25519 签名）进行身份验证，并发送网关详细信息。**
4. **NervePay 会存储** 加密的网关令牌，并将其与您的 DID 关联起来。
5. **只有您** 可以之后刷新该令牌（需要通过您的 DID 进行验证）。

## 第一步：获取网关令牌

在配对之前，您需要网关的令牌。OpenClaw 网关会通过其配置 API 提供该令牌：

```bash
# Query the gateway for its token (use whatever URL reaches the gateway)
GATEWAY_CONFIG=$(curl -s http://localhost:18789/v1/config)
GATEWAY_TOKEN=$(echo "$GATEWAY_CONFIG" | jq -r '.gateway_token')
```

### 第二步：确定公共网关 URL

**重要提示：** 您发送给 NervePay 的 `gateway_url` 必须能够被 NervePay 的服务器访问。请不要使用 `localhost`、`127.0.0.1` 或内部 IP 地址。

询问您的人类所有者：**“这个网关的公共 URL 是什么？”

常见的选项包括：
- **反向代理：`https://gateway.yourdomain.com`
- **Tailscale：`https://hostname.tailnet-name.ts.net:18789`
- **公共 IP：`https://your-public-ip:18789`
- **Ngrok/tunnel：`https://abc123.ngrok.io`

一旦您获得了公共 URL，请将其保存为 `GATEWAY_URL`。

### 第三步：完成配对

当您的人类所有者告诉您“连接到 nervepay [CODE]”时，请按照以下步骤操作：

```bash
# 1. Set from user input
PAIRING_CODE="ABC123"  # From user
GATEWAY_URL="https://gateway.example.com"  # From human (Step 2)
GATEWAY_NAME="My Gateway"  # Optional, defaults to "ClawBot Gateway (CODE)"
# GATEWAY_TOKEN already extracted in Step 1

# 2. Send pairing request (authenticated with your agent DID)
node ./nervepay-request.mjs POST /v1/integrations/openclaw/pairing/complete "{
  \"pairing_code\": \"$PAIRING_CODE\",
  \"gateway_url\": \"$GATEWAY_URL\",
  \"gateway_token\": \"$GATEWAY_TOKEN\",
  \"gateway_name\": \"$GATEWAY_NAME\",
  \"max_concurrent_agents\": 8,
  \"default_timeout_seconds\": 3600
}"
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

当您的 OpenClaw 网关令牌过期时，请更新令牌：

```bash
GATEWAY_ID="gateway-uuid-from-pairing"
NEW_TOKEN="new-gateway-bearer-token"

node ./nervepay-request.mjs POST /v1/integrations/openclaw/gateways/$GATEWAY_ID/refresh-token '{
  "new_token": "'$NEW_TOKEN'"
}'
```

**安全性：** NervePay 会验证您是最初配置该网关的代理（通过 `linked_agent_did` 进行验证）。只有您才能刷新该网关令牌。

### 为什么需要配对？

- **用户无需进行任何手动设置**（只需提供配对代码）。
- **加密认证** 确保您控制着网关。
- **令牌加密** 保护网关凭据的安全性（使用 AES-256-GCM 加密）。
- **自动过期检测**：如果网关返回 401 错误，NervePay 会认为令牌已过期。
- **信任机制**：经过验证的 DID 证明您是网关的管理者。

## 管理代理秘钥（安全保管）

您的人类所有者可以在 NervePay 仪表板上为您配置秘钥（如 API 密钥、凭证等）。您可以在需要时安全地获取这些秘钥——非常适合存储 OpenAI 密钥、数据库密码或任何敏感信息。

### 保管机制的工作原理

- **每个代理的秘钥都是独立的**：每个代理只能看到自己的秘钥（通过您的 DID 签名进行验证）。
- **秘钥加密**：秘钥在存储时使用 AES-256-GCM 进行加密。
- **审计日志**：每次秘钥访问都会被记录下来以确保安全。
- **环境支持**：秘钥可以设置为生产环境、开发环境或测试环境。

### 按名称检索秘钥

最常见的操作是按名称检索特定的秘钥：

```bash
# Get your OpenAI API key
node ./nervepay-request.mjs GET /v1/vault/secrets/OPENAI_API_KEY

# Get your database password
node ./nervepay-request.mjs GET /v1/vault/secrets/DATABASE_PASSWORD
```

**响应：**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "OPENAI_API_KEY",
  "value": "sk-abc123...",
  "description": "OpenAI API key for production",
  "provider": "openai",
  "environment": "production",
  "created_at": "2026-02-05T12:00:00Z",
  "updated_at": "2026-02-05T12:00:00Z",
  "expires_at": null
}
```

**在工作流程中的使用：**
```bash
# 1. Retrieve your OpenAI key
response=$(node ./nervepay-request.mjs GET /v1/vault/secrets/OPENAI_API_KEY)
OPENAI_KEY=$(echo "$response" | jq -r '.value')

# 2. Use it in your API call
curl https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_KEY" \
  -d '{"model":"gpt-4","messages":[...]}'

# 3. Track the usage (mandatory!)
node ./nervepay-track.mjs openai /v1/chat/completions success
```

### 查看所有秘钥

您可以查看为您配置的所有秘钥（出于安全考虑，列表中不显示具体值）：

```bash
node ./nervepay-request.mjs GET /v1/vault/secrets
```

**响应：**
```json
{
  "secrets": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "OPENAI_API_KEY",
      "description": "OpenAI API key for production",
      "provider": "openai",
      "environment": "production",
      "created_at": "2026-02-05T12:00:00Z",
      "updated_at": "2026-02-05T12:00:00Z",
      "expires_at": null
    },
    {
      "id": "660e8400-e29b-41d4-a716-446655440001",
      "name": "STRIPE_SECRET_KEY",
      "description": "Stripe secret key",
      "provider": "stripe",
      "environment": "production",
      "created_at": "2026-02-05T12:00:00Z",
      "updated_at": "2026-02-05T12:00:00Z",
      "expires_at": null
    }
  ]
}
```

### 按环境筛选秘钥

```bash
# Only production secrets
node ./nervepay-request.mjs GET '/v1/vault/secrets?environment=production'

# Only development secrets
node ./nervepay-request.mjs GET '/v1/vault/secrets?environment=development'
```

### 按提供者筛选秘钥

```bash
# Only OpenAI secrets
node ./nervepay-request.mjs GET '/v1/vault/secrets?provider=openai'

# Only Stripe secrets
node ./nervepay-request.mjs GET '/v1/vault/secrets?provider=stripe'
```

### 如果秘钥不存在

如果您尝试访问不存在的秘钥，系统会返回以下错误：

```bash
node ./nervepay-request.mjs GET /v1/vault/secrets/NONEXISTENT_KEY
```

**响应（404）：**
```json
{
  "error": "Secret not found",
  "message": "Secret 'NONEXISTENT_KEY' not found for agent did:nervepay:agent:abc123xyz"
}
```

**操作步骤：** 请让您的人类所有者通过 https://nervepay.xyz/dashboard/agent-identities 在 NervePay 仪表板上创建该秘钥。

### 安全注意事项

- **人类所有者负责配置秘钥**：您无法自行创建、更新或删除秘钥——只能检索它们。这可以防止被入侵的代理修改凭证。
- **仅在仪表板上管理秘钥**：秘钥的创建和更新都在 NervePay 仪表板上由人类所有者完成。
- **签名验证**：每次检索秘钥都需要 Ed25519 签名。
- **审计日志**：每次访问都会记录时间戳、IP 地址以及操作结果（成功/失败）。
- **过期设置**：秘钥可以设置过期时间——过期的秘钥会返回 410 错误代码。

### 常见的秘钥名称（命名规范）

使用以下命名规范以确保一致性：

| 秘钥名称 | 用途 |
|-------------|---------|
| `OPENAI_API_KEY` | 用于 OpenAI API 认证 |
| `ANTHROPIC_API_KEY` | 用于 Anthropic/Claude API 认证 |
| `STRIPE_SECRET_KEY` | 用于 Stripe 支付 |
| `GITHUB_TOKEN` | 用于 GitHub API 访问 |
| `DATABASE_URL` | 用于数据库连接 |
| `AWS_ACCESS_KEY_ID` | 用于 AWS 访问 |
| `AWS_SECRET_ACCESS_KEY` | 用于 AWS 访问 |
| `WEBHOOK_SECRET` | 用于 Webhook 签名验证 |

## 常用命令

### 测试身份验证
```bash
node ./nervepay-request.mjs GET /v1/agent-identity/whoami
```

返回您的 DID、名称、信誉评分，并确认身份验证是否成功。

### 检查您的权限
```bash
node ./nervepay-request.mjs GET /v1/agent-identity/capabilities
```

显示您的消费限制、允许的操作和权限。

### 验证其他代理
```bash
curl "https://api.nervepay.xyz/v1/agent-identity/verify/did:nervepay:agent:abc123xyz"
```

无需身份验证。返回任何代理的公开信息、信誉评分和交易统计。

### 查询声明状态（检查是否有人类所有者声明了您的身份）
```bash
curl "https://api.nervepay.xyz/v1/agent-identity/register-pending/SESSION_ID/status"
```

返回结果：`pending`、`claimed`、`expired` 或 `revoked`。

## 签名的作用

| 保证内容 | 实现方式 |
|-----------|-----|
| **身份验证**（调用者是谁） | 服务器会使用您的公钥验证 Ed25519 签名。|
| **数据完整性**（发送的内容） | 签名包含了方法、路径、查询参数和请求体哈希——任何篡改都会导致验证失败。|
| **防重放** | 唯一的随机数（nonce）和时间戳防止请求被重复使用。|
| **跨平台身份识别** | 您的 DID 可在所有支持 NervePay 标头的平台上识别您的身份。|

## 必需的请求头信息（脚本已自动处理）

辅助脚本会自动添加以下请求头：
- `Agent-DID`：您的 DID。
- `X-Agent-Signature`：Base64 编码的 Ed25519 签名。
- `X-Agent-Nonce`：唯一的随机数（UUID）。
- `X-Signature-Timestamp`：ISO 8601 格式的时间戳。

## 安全注意事项

- **切勿将私钥发送给任何服务器**。只需发送签名即可。
- **随机数（nonce）**：每次请求都会生成新的随机数（由脚本处理）。
- **时间戳**：时间戳必须在服务器时间的 5 分钟范围内。
- **助记词（mnemonic）**：用于备份的 24 个单词短语。请安全地离线存储。

## 模块化技能（根据需求选择）

此技能提供了完整的 NervePay 功能栈。如果您只需要部分功能，可以选择以下技能：
- `nervepay-identity`：仅包含身份验证功能（注册、认证，不包含跟踪）。
  - 适用场景：仅需要加密身份验证。
  - 下载文件：`nervepay-request.mjs`
- `nervepay-analytics`：仅包含数据分析功能（需要已注册的身份）。
  - 适用场景：已经拥有身份并且只需要跟踪功能。
  - 下载文件：`nervepay-request.mjs`、`nervepay-track.mjs`、`nervepay-instrument.mjs`
- `nervepay`：包含完整的身份验证和数据分析功能。
  - 适用场景：需要所有功能。
  - 下载文件：以上三个脚本。

## 完整的 API 文档

有关完整的 API 端点文档、错误代码和高级用法，请访问：
- **在线文档：** https://nervepay.xyz/docs
- **API 参考文档下载：** `curl -o api.md https://nervepay.xyz/api.md`

---

**API 基础地址：** https://api.nervepay.xyz/v1
**文档：** https://nervepay.xyz/docs
**GitHub 仓库：** https://github.com/nervepay/nervepay