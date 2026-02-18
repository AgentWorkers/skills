---
name: aegis-security
version: 1.2.2
description: 用于AI代理的区块链安全API：扫描代币、模拟交易、检测地址中的威胁。
homepage: https://aegis402.xyz
user-invocable: true
disable-model-invocation: true
metadata: {"emoji":"🛡️","category":"blockchain-security","api_base":"https://aegis402.xyz/v1","free_tier_daily_limit":100,"openclaw":{"emoji":"🛡️","homepage":"https://aegis402.xyz"}}
---
# Aegis402 防护协议

这是一个专为 AI 代理设计的区块链安全 API。

**免费 tier:** 每天 100 次检查；之后按请求计费，支持使用 USDC（Base 或 Solana）进行支付。

## 安全默认设置

- 该功能仅支持手动使用（`disable-model-invocation: true`）。
- 严禁请求或存储私钥、助记词或密语。
- 在进行付费调用（尤其是 `simulate-tx`）之前，必须确认用户的操作意图。
- 仅当用户明确同意自动化操作时，才能自动执行预签名检查。
- 该功能不需要任何环境变量。

## 代理快速入门（交易前扫描）

**代理和钱包的默认策略：**

1. 设置 `X-Client-Fingerprint: <stable_agent_or_user_id>`，以便进行可预测的免费 tier 计费。
2. 在发送任何交易之前，同时执行以下操作：
   - `GET /v1/check-address/:to`
   - `POST /v1/simulate-tx`
   - （可选）`GET /v1/check-token/:token`（用于检查涉及的代币）
3. 如果任何检查结果显示 `HIGH`/`CRITICAL`、`isSafe=false`，或者接收方被标记为可疑，应阻止交易并要求用户确认。
4. 否则允许交易，但仍需显示审查摘要和原始 JSON 数据。

**注意事项：**

- 免费 tier 仅提供基本的滥用限制，并非真正的安全机制。通过轮换 `X-Client-Fingerprint` 可以绕过免费 tier 的限制。
- 如果省略了 `X-Client-Fingerprint`，系统将使用其他请求信息（如 IP 或用户代理）来进行计费。

## 使用方法（代理模式，从零开始）

当用户准备发送交易时：

1. 请求缺失的必要信息：
   - `from`（发送方地址）、`to`（接收方地址）、`value`（交易金额，单位为 wei）、`data`（交易数据）或 `chain_id`（使用的区块链）
2. 检查是否在免费 tier 范围内（始终免费）：
   - `GET /v1/usage`
3. 并行执行交易前扫描：
   - `GET /v1/check-address/:to`
   - `POST /v1/simulate-tx`
   - （可选）`GET /v1/check-token/:token`
4. 使用以下模板回复用户（先显示摘要，再提供原始 JSON 数据）。

## 回复模板

### 安全（LOW风险）

```
🛡️ Scan Complete

Risk: LOW (SAFE)
Summary: No critical warnings detected.

✅ OK to proceed.
```

### 警告（中等风险）

```
🛡️ Scan Complete

Risk: MEDIUM (CAUTION)
Summary: Some warnings detected.

⚠️ Review recommended before proceeding. Want me to explain the top 3 risks?
```

### 危险（高风险）

```
🛡️ Scan Complete

Risk: HIGH (DANGEROUS)
Summary: Significant risks detected.

🚫 Not recommended.
```

### 被阻止（严重风险）

```
🛡️ Scan Complete

Risk: CRITICAL (BLOCKED)
Summary: Do not proceed.

🚫 Stop. This transaction/recipient appears malicious or unsafe.
```

### 需要支付 402 费用

```
I tried to run a paid check but payment isn't set up (or the wallet has insufficient USDC).

To enable paid checks:
1. Fund a programmatic wallet with a small amount of USDC (Base default; Solana also supported)
2. Install an x402 client (@x402/fetch + chain package)
3. Configure an agent-managed wallet signer (no raw private keys in prompts/env)
```

## 参考资料

### 相关文件

| 文件名 | URL |
|------|-----|
| **SKILL.md** | `https://aegis402.xyz/skill.md` |
| **skill.json**（元数据）| `https://aegis402.xyz/skill.json` |

**基础 URL:** `https://aegis402.xyz/v1`

### 定价

| API 端点 | 价格 | 用途 |
|---------|-------|----------|
| `POST /simulate-tx` | 0.05 美元 | 交易模拟，DeFi 安全性检查 |
| `GET /check-token/:address` | 0.01 美元 | 代币安全检测 |
| `GET /check-address/:address` | 0.005 美元 | 地址信誉检查 |

**免费 tier:** 每天 100 次检查。可通过 `GET /v1/usage` 查看使用情况。

### 免费使用示例

```bash
curl "https://aegis402.xyz/v1/usage"
```

### check-address

```bash
curl "https://aegis402.xyz/v1/check-address/0x742d35Cc6634C0532925a3b844Bc454e4438f44e?chain_id=8453"
```

### simulate-tx

**请求参数：**

- `from`（必填）：发送方地址
- `to`（必填）：接收方地址或合约地址
- `value`（必填）：交易金额（单位为 wei）
- `data`（可选）：交易数据的十六进制表示（格式为 `0x...`）
- `chain_id`（可选）：要模拟的区块链（默认为 Base 8453，适用于支付；模拟使用的区块链可自行选择）

```bash
curl -X POST "https://aegis402.xyz/v1/simulate-tx" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "0xYourWallet...",
    "to": "0xContract...",
    "value": "0",
    "data": "0x",
    "chain_id": 8453
  }'
```

### check-token

`chain_id` 表示要扫描的区块链（例如：Ethereum=1，Base=8453 等）。支付方式由 `402` 协议决定（默认使用 USDC 在 Base 链上支付）。

### 支付方式（x402）

在免费 tier 期间，您可以免费使用该 API。一旦每日检查次数达到 100 次，系统会返回 “需要支付 402 费用”的提示，此时代理钱包可以自动支付并重试。

| 网络 | 代理钱包签名方式 |
|---------|------------------------|
| Base（EVM）| 来自代理钱包提供商的 EVM 签名器 |
| Solana | 来自代理钱包提供商的 Solana 签名器 |

### 最小化节点客户端（代理管理的 EVM 签名器）

```bash
npm install @x402/fetch@2.2.0 @x402/evm@2.2.0
```

### Solana 客户端（代理管理的签名器）

```bash
npm install @x402/fetch@2.2.0 @x402/svm@2.2.0
```

### 代理安全政策

- 绝不允许用户提供私钥、助记词或密语。
- 禁止在提示信息、日志或文档中存储签名相关的敏感信息。
- 在进行付费调用（尤其是 `simulate-tx`）之前，必须确认用户的操作意图。
- 仅当用户明确同意自动化操作时，才能自动执行预签名检查。

## 附录

### 风险等级

| 风险等级 | 含义 | 代理应采取的措施 |
|-------|---------|---------------|
| `LOW` | 低风险 | 允许交易 |
| `MEDIUM` | 存在一定风险 | 显示警告并请求用户确认 |
| `HIGH` | 高风险 | 阻止交易并要求用户确认 |
| `CRITICAL` | 极高风险 | 立即阻止交易 |

### 错误处理

| 状态码 | 含义 | 代理应采取的措施 |
|--------|---------|--------------------------|
| 400 | 参数无效 | 询问用户缺失或无效的参数并重试 |
| 402 | 需要支付费用 | 确认用户意图后使用已授权的代理钱包签名器进行支付（或等待下一个免费 tier 周期） |
| 500 | 服务端错误 | 重试一次；如果问题持续，显示错误信息及 `requestId` |

**提示：**

- 所有响应都会包含 `_meta.requestId`。服务器还会设置 `x-request-id` 标头，请在错误报告中包含该信息。
- 系统可能会在响应中包含升级提示：
  - `x-aegis-skill-latest-version`
  - `x-aegis-skill-url`
  - `x-aegis-skill-upgrade`

### 可选：反馈与问题报告（对用户友好）

如果您遇到问题或有任何建议，请以对用户友好的方式提供反馈：

- 请勿包含私钥、助记词、API 密钥或任何敏感信息。
- （可选）提供 `_meta.requestId`（或 `x-request-id` 标头），以便我们进行服务器端的数据关联。
- 如果您代表用户操作，请在发送报告前获得用户的授权。默认操作是向用户展示报告模板。

**报告模板（可供复制/粘贴）：**

```text
Aegis402 report

Type: issue | feedback | expectation
RequestId: <_meta.requestId>
Endpoint: <path>
Status: <http status>
ChainId: <chain_id or NULL>
When (UTC): <timestamp>

What I expected:
What happened:
Minimal repro (curl or steps):

Notes (redacted):
```

**反馈渠道（非强制使用 GitHub）：**

- `POST /v1/feedback`（免费，无需消耗资源）

**示例报告（需用户授权后使用）：**

```bash
curl -X POST "https://aegis402.xyz/v1/feedback" \
  -H "Content-Type: application/json" \
  -H "X-Client-Fingerprint: <stable-non-pii-id>" \
  -d '{
    "kind": "issue",
    "summary": "Short summary",
    "expected": "What I expected",
    "happened": "What happened",
    "repro": "Minimal repro steps or curl",
    "endpoint": "/v1/check-token/0x...",
    "status_code": 400,
    "chain_id": "8453",
    "agent": { "name": "my-agent", "version": "1.2.3" },
    "extra": { "failed_request_id": "<_meta.requestId>" }
  }'
```

### 可选：分享风险事件（Moltbook）

仅当检测结果为 `HIGH` 或 `CRITICAL` 时，且用户明确同意公开分享时，才可分享您的经历：

- 请仅分享真实的经历，避免透露任何可能识别用户身份的信息。
- 请勿包含私钥、助记词、签名、原始交易数据、完整钱包地址、完整的交易哈希值、`X-Client-Fingerprint` 或任何可能暴露用户身份的信息。
- 建议使用四舍五入的金额（例如：`$1,000`），并在必要时省略具体时间戳。

**风险事件报告模板（已屏蔽敏感信息）：**

```text
Title: How I caught a scam transaction and saved ~$XXX!

🛡️ What happened
- Action: <swap | approve | transfer | other>
- Chain: <Base | Ethereum | Solana | ...>
- Risk: <HIGH | CRITICAL>

Why it was blocked (top signals):
1) <short reason>
2) <short reason>
3) <short reason>

Impact:
- Prevented loss: ~$<USD_RANGE>

Notes:
- No addresses / tx hash / calldata shared.
- (Optional) RequestId: <_meta.requestId>
- (Optional) Skill: https://aegis402.xyz/skill.md
```

## 系统健康检查（免费）

```bash
curl https://aegis402.xyz/health
```

## 支持的区块链

`chain_id` 表示要扫描的区块链：

| 链名 | ID | check-token | check-address | simulate-tx |
|-------|-----|-------------|---------------|-------------|
| Solana | solana | ✅ | ✅ | ❌ |
| Ethereum | 1 | ✅ | ✅ | ✅ |
| Base | 8453 | ✅ | ✅ | ✅ |
| Polygon | 137 | ✅ | ✅ | ✅ |
| Arbitrum | 42161 | ✅ | ✅ | ✅ |
| Optimism | 10 | ✅ | ✅ | ✅ |
| BSC | 56 | ✅ | ✅ | ✅ |
| Avalanche | 43114 | ✅ | ✅ | ✅ |

## 相关链接

- 官网：https://aegis402.xyz
- API 文档：https://aegis402.xyz/api.html
- 演示页面：https://aegis402.xyz/#demo-lab
- x402 协议文档：https://docs.x402.org

## 社交媒体

- X 社交平台：https://x.com/aegis402
- Telegram：https://t.me/aegis402_channel
- 开发者聊天频道：https://t.me/aegis402_chat

🛡️ 专为代理经济（Agent Economy）设计，由 x402 协议提供支持。