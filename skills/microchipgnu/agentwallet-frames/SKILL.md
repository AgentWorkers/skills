---
name: agentwallet
version: 0.1.10
description: 专为AI代理设计的钱包，支持x402支付签名功能、推荐奖励机制以及基于策略的控制动作。
homepage: https://frames.ag
metadata: {"moltbot":{"category":"finance","api_base":"https://frames.ag/api"},"x402":{"supported":true,"chains":["solana","evm"],"networks":["solana:EtWTRABZaYq6iMfeYKouRu166VU2xqa1","solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp","eip155:8453","eip155:84532"],"tokens":["USDC"],"endpoint":"/api/wallets/{username}/actions/x402/fetch","legacyEndpoint":"/api/wallets/{username}/actions/x402/pay"},"referrals":{"enabled":true,"endpoint":"/api/wallets/{username}/referrals"}}
---
# AgentWallet

AgentWallet 为 AI 代理提供服务器端钱包服务。钱包会在用户通过电子邮件进行 OTP 验证后分配。所有签名操作均在服务器端完成，并受到策略控制。

---

## 快速参考

**首先：** 通过读取 `~/.agentwallet/config.json` 文件来检查是否已连接。如果文件中存在 `apiToken`，则表示已连接——无需再次请求用户的电子邮件地址。

**需要连接（但没有配置文件）？** 请求用户的电子邮件地址 → 发送 POST 请求到 `/api/connect/start` → 用户输入 OTP → 发送 POST 请求到 `/api/connect/complete` → 保存 API 令牌。

**x402 支付？** 使用一步式的 `/x402/fetch` 端点（推荐）——只需发送目标 URL 和请求体，服务器会处理所有后续操作。

---

## x402/fetch - 一步式支付代理（推荐）

**这是调用 x402 API 的最简单方法。** 发送目标 URL 和请求体，服务器会自动处理 402 错误检测、支付签名以及重试操作。

```bash
curl -s -X POST "https://frames.ag/api/wallets/USERNAME/actions/x402/fetch" \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://enrichx402.com/api/exa/search","method":"POST","body":{"query":"AI agents","numResults":3}}'
```

**就是这样！** 响应中包含最终的 API 结果：

```json
{
  "success": true,
  "response": {
    "status": 200,
    "body": {"results": [...]},
    "contentType": "application/json"
  },
  "payment": {
    "chain": "eip155:8453",
    "amountFormatted": "0.01 USDC",
    "recipient": "0x..."
  },
  "paid": true,
  "attempts": 2,
  "duration": 1234
}
```

### x402/fetch 请求参数

| 参数 | 类型 | 是否必填 | 描述 |
|-------|------|----------|-------------|
| `url` | 字符串 | 是 | 目标 API 的 URL（生产环境中必须使用 HTTPS） |
| `method` | 字符串 | 否 | HTTP 方法：GET、POST、PUT、DELETE、PATCH（默认为 GET） |
| `body` | 对象 | 否 | 请求体（自动序列化为 JSON 格式） |
| `headers` | 对象 | 否 | 需要发送的额外头部信息 |
| `preferredChain` | 字符串 | 否 | 选择合适的区块链（默认为 `"auto"`、`"evm"` 或 `"solana"`；系统会自动选择 USDC 余额充足的区块链） |
| `dryRun` | 布尔值 | 否 | 免费预览支付费用（不进行实际支付） |
| `timeout` | 数字 | 请求超时时间（以毫秒为单位，默认为 30000，最大为 120000） |
| `idempotencyKey` | 字符串 | 用于防止重复请求 |

### 免费预览（dryRun）

在请求体中添加 `"dryRun": true` 即可预览支付详情，而无需实际支付：

```json
{
  "success": true,
  "dryRun": true,
  "payment": {
    "required": true,
    "chain": "eip155:8453",
    "amountFormatted": "0.01 USDC",
    "policyAllowed": true
  }
}
```

### 错误代码

| 代码 | HTTP 状态码 | 描述 |
|------|------|-------------|
| `INVALID_URL` | 400 | URL 格式错误或被阻止（例如本地主机、内部 IP） |
| `POLICY_DENIED` | 403 | 政策检查失败（例如金额过高） |
| `WALLET_FROZEN` | 403 | 钱包被冻结 |
| `TARGET_TIMEOUT` | 504 | 目标 API 超时 |
| `TARGET_ERROR` | 502 | 目标 API 返回 5xx 错误 |
| `PAYMENT_REJECTED` | 402 | 支付被目标 API 拒绝 |
| `NO_PAYMENT_option` | 400 | 未找到兼容的支付网络 |

---

## 配置文件说明

配置文件存储在 `~/.agentwallet/config.json` 中：

```json
{
  "username": "your-username",
  "email": "your@email.com",
  "evmAddress": "0x...",
  "solanaAddress": "...",
  "apiToken": "mf_...",
  "moltbookLinked": false,
  "moltbookUsername": null,
  "xHandle": null
}
```

| 参数 | 描述 |
|-------|-------------|
| `username` | 你的唯一 AgentWallet 用户名 |
| `email` | 用于 OTP 验证的电子邮件地址 |
| `evmAddress` | EVM 钱包地址 |
| `solanaAddress` | Solana 钱包地址 |
| `apiToken` | 认证请求所需的 API 令牌（以 `mf_` 开头） |
| `moltbookLinked` | 是否关联了 Moltbook 账户 |
| `moltbookUsername` | 关联的 Moltbook 用户名（如有） |
| `xHandle` | 来自 Moltbook 的 X/Twitter 账号（如有） |

**安全提示：** 请勿将配置文件提交到 Git。设置文件权限为 `chmod 600`，并将 `apiToken` 视为敏感信息进行保护。

---

## 连接流程

**Web 流程：** 请求用户的电子邮件地址 → 直接跳转至 `https://frames.ag/connect?email=EMAIL` → 用户输入 6 位 OTP → 页面显示凭据（`AGENTWALLET_USERNAME`、`AGENTWALLET_API_TOKEN` 等）。用户应妥善保存 API 令牌。

**API 流程（适用于 CLI/代理）：**

步骤 1 - 发送 OTP：
```bash
curl -X POST https://frames.ag/api/connect/start \
  -H "Content-Type: application/json" \
  -d '{"email":"your@email.com"}'
```
响应中会返回 `username`。如果是推荐链接，请在请求体中添加 `"ref":"REFERRER_USERNAME"`。

步骤 2 - 请求用户输入 OTP，然后完成连接：
```bash
curl -X POST https://frames.ag/api/connect/complete \
  -H "Content-Type: application/json" \
  -d '{"username":"USERNAME_FROM_STEP_1","email":"your@email.com","otp":"USER_OTP"}'
```
响应中会返回 `apiToken`、`evmAddress` 和 `solanaAddress`。请保存 `apiToken` 以用于后续的钱包操作。

---

## 推荐与空投计划

分享你的推荐链接：`https://frames.ag/connect?ref=YOUR_USERNAME&email=THEIR_EMAIL`

推荐者和新代理都会获得空投奖励。奖励规则如下：
- 推荐奖励：200 分
- 首次交易奖励：50 分
- 每日活跃奖励：10 分
- 每周连续操作奖励：100 分

奖励等级划分：
- 青铜级（0-4 次推荐）：1 倍奖励
- 银级（5-24 次推荐）：1.5 倍奖励
- 金级（25-99 次推荐）：2 倍奖励
- 钻石级（100 次以上推荐）：3 倍奖励

查看奖励详情：
```bash
curl https://frames.ag/api/wallets/YOUR_USERNAME/referrals \
  -H "Authorization: Bearer FUND_API_TOKEN"
```

## 网络状态

公共网络统计信息：`GET https://frames.ag/api/network/pulse` — 获取活跃代理数量、交易量、交易趋势等数据。

个人账户统计信息（需认证）：`GET https://frames.ag/api/wallets/YOUR_USERNAME/stats` — 查看排名、交易历史、交易量、推荐信息等。

---

## 技能文档文件

| 文件名 | 链接 |
|------|-----|
| **SKILL.md** （当前文件） | `https://frames.ag/skill.md` |
| **HEARTBEAT.md** | `https://frames.ag/heartbeat.md` |
| **package.json**（元数据） | `https://frames.ag/skill.json` |

### Heartbeat

定期运行 Heartbeat 文件以检查技能更新、钱包状态和近期活动：

**基础 URL：** `https://frames.ag/api/v1`

---

## 认证

使用你的 API 令牌（以 `mf_` 开头）进行认证，格式为：`Authorization: Bearer FUND_API_TOKEN`

检查连接状态（无需认证）：`GET https://frames.ag/api/wallets/USERNAME` — 返回 `connected: true/false` 及钱包地址（如果已连接）。

---

## 资金充值

引导用户访问 `https://frames.ag/u/YOUR_USERNAME` 通过 Coinbase Onramp 进行充值（支持银行卡、信用卡或 Coinbase 账户）。支持 Base（USDC）和 Solana（SOL）货币。

充值后查看余额：
```bash
curl https://frames.ag/api/wallets/USERNAME/balances \
  -H "Authorization: Bearer FUND_API_TOKEN"
```

## 钱包操作

**余额查询：** `GET /api/wallets/USERNAME/balances`（需要认证）

**活动记录：** `GET /api/wallets/USERNAME/activity?limit=50`（可选认证——认证用户可查看所有操作记录，公开用户仅查看部分记录）。操作类型包括：`otp.*`、`policy.*`、`wallet.action.*`、`x402authorization.signed`。

---

## 操作（受策略控制）

### EVM 转账
```bash
curl -X POST "https://frames.ag/api/wallets/USERNAME/actions/transfer" \
  -H "Authorization: Bearer TOKEN" -H "Content-Type: application/json" \
  -d '{"to":"0x...","amount":"1000000","asset":"usdc","chainId":8453}'
```
参数：`to`（收款地址）、`amount`（最小单位：ETH 保留 18 位小数，USDC 保留 6 位小数）、`asset`（`"eth"` 或 `"usdc"`）、`chainId`、`idempotencyKey`（可选）。

支持的 USDC 链接包括：Ethereum（1）、Sepolia（11155111）、Optimism（10）、Polygon（137）、Arbitrum（42161）、Base（8453）、Base Sepolia（84532）。

### Solana 转账
```bash
curl -X POST "https://frames.ag/api/wallets/USERNAME/actions/transfer-solana" \
  -H "Authorization: Bearer TOKEN" -H "Content-Type: application/json" \
  -d '{"to":"RECIPIENT","amount":"1000000000","asset":"sol","network":"devnet"}'
```
参数：`to`（收款地址）、`amount`（最小单位：SOL 保留 9 位小数，USDC 保留 6 位小数）、`asset`（`"sol"` 或 `"usdc"`）、`network`（`"mainnet"` 或 `"devnet"`）、`idempotencyKey`（可选）。

### EVM 合同调用
```bash
curl -X POST "https://frames.ag/api/wallets/USERNAME/actions/contract-call" \
  -H "Authorization: Bearer TOKEN" -H "Content-Type: application/json" \
  -d '{"to":"0x...","data":"0x...","value":"0","chainId":8453}'
```

### 签名消息
```bash
curl -X POST "https://frames.ag/api/wallets/USERNAME/actions/sign-message" \
  -H "Authorization: Bearer TOKEN" -H "Content-Type: application/json" \
  -d '{"chain":"solana","message":"hello"}'
```

### Solana Devnet 水龙头

用于测试目的，可申请免费的 Devnet SOL。每次最多申请 0.1 SOL 到用户的 Solana 钱包。24 小时内最多申请 3 次。

**所有操作的响应格式：** `{"actionId":"...","status":"confirmed","amount":"0.1 SOL","txHash":"...","explorer":"..."}`

---

## x402 手动操作（高级用法）

仅在你需要精细控制时使用此方法。**大多数情况下，建议使用 `/x402/fetch`。**

### 协议版本

| 版本 | 支付头部信息 | 使用的网络格式 |
|---------|---------------|----------------|
| v1 | `X-PAYMENT` | 使用简短名称（如 `solana`、`base`） |
| v2 | `PAYMENT-SIGNATURE` | 使用 CAIP-2 格式（例如：`solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp`） |

### 操作流程：

1. 调用目标 API 并获取 402 响应。支付相关信息包含在 `payment-required` 头部字段中（请求体可能为空 `{}`）。
2. 使用以下格式发送签名请求：`POST /api/wallets/USERNAME/actions/x402/pay`，其中 `{"requirement": "<头部信息或 JSON>"`，`"preferredChain": "evm"`。`requirement` 字段支持 Base64 字符串或 JSON 对象。
3. 使用 `usage.header` 字段中的头部信息和 `paymentSignature` 值重新发送原始请求。

**签名请求端点：** `/api/wallets/{USERNAME}/actions/x402/pay`（注意使用斜杠 `/`，而非破折号 `-`）

### 签名请求参数

| 参数 | 类型 | 描述 |
|-------|------|-------------|
| `requirement` | 字符串或对象 | 支付相关要求（格式为 Base64 或 JSON） |
| `preferredChain` | `"evm"` 或 `"solana"` | 优先使用的区块链 |
| `preferredChainId` | 数字 | 特定的 EVM 链接 ID |
| `idempotencyKey` | 字符串 | 用于防止重复请求 |
| `dryRun` | 布尔值 | 是否仅进行签名操作（用于测试） |

### 注意事项：
- 签名是一次性使用的——即使请求失败也会被消耗。
- 使用单行命令行工具 `curl` 进行操作（多行命令可能导致转义错误）。
- USDC 金额保留 6 位小数（10000 等于 0.01 USDC）。
- 必须使用 `requirement` 参数（旧的 `paymentRequiredHeader` 已弃用）。

### 支持的网络

| 网络 | CAIP-2 标识符 | 使用的令牌 |
|---------|-------------------|-------|
| Base Mainnet | `eip155:8453` | USDC |
| Base Sepolia | `eip155:84532` | USDC |
| Solana Mainnet | `solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp` | USDC |
| Solana Devnet | `solana:EtWTRABZaYq6iMfeYKouRu166VU2xqa1` | USDC |

### 常见错误

| 错误代码 | 解决方案 |
|-------|----------|
| 签名失败（404/405） | 使用 `/api/wallets/{USERNAME}/actions/x402/pay`（使用斜杠 `/`，而非破折号 `-`） |
| 参数为空 | 使用单行命令行工具 `curl`，避免使用多行命令 |
| 已经处理过该请求 | 为每个请求重新生成签名 |
| 资金不足 | 请访问 `https://frames.ag/u/USERNAME` 为钱包充值 |

---

## 策略设置

获取当前策略：```bash
curl https://frames.ag/api/wallets/YOUR_USERNAME/policy \
  -H "Authorization: Bearer FUND_API_TOKEN"
```

更新策略：```bash
curl -X PATCH https://frames.ag/api/wallets/YOUR_USERNAME/policy \
  -H "Authorization: Bearer FUND_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"max_per_tx_usd":"25","allow_chains":["base","solana"],"allow_contracts":["0x..."]}'
```

## 响应格式

成功：```json
{"success": true, "data": {...}}
```

失败：```json
{"success": false, "error": "Description", "hint": "How to fix"}
```