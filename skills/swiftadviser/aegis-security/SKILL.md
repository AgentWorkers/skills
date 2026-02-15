---
name: aegis-security
version: 1.2.1
description: 用于AI代理的区块链安全API：扫描代币、模拟交易、检测地址是否存在威胁。
homepage: https://aegis402.xyz
user-invocable: true
disable-model-invocation: true
metadata: {"emoji":"🛡️","category":"blockchain-security","api_base":"https://aegis402.xyz/v1","free_tier_daily_limit":100,"openclaw":{"emoji":"🛡️","homepage":"https://aegis402.xyz"}}
---

# Aegis402 防护协议

这是一个专为 AI 代理设计的区块链安全 API。

**免费 tier:** 每天 100 次检查；之后按请求计费，支持使用 USDC（Base 链）或 Solana 作为支付方式。

## 安全默认设置

- 该功能仅限手动使用（`disable-model-invocation: true`）。
- 严禁请求或存储私钥、助记词或密语。
- 在进行付费调用（尤其是 `simulate-tx`）之前，必须确认用户的操作意图。
- 仅当用户明确同意自动化操作时，才能自动执行预签名检查。
- 该功能无需任何环境变量。

## 代理快速入门（交易前扫描）

**代理和钱包的默认策略：**

1. 设置 `X-Client-Fingerprint: <stable_agent_or_user_id>`，以便进行可预测的免费 tier 计费。
2. 在发送任何交易之前，同时执行以下操作：
   - `GET /v1/check-address/:to`
   - `POST /v1/simulate-tx`
   - （可选）`GET /v1/check-token/:token`（用于检查涉及的代币）
3. 如果任何检查结果显示为 `HIGH`/`CRITICAL`、`isSafe=false`，或者接收方被标记为可疑，应阻止交易并要求用户确认。
4. 否则允许交易，但仍会显示审查摘要和原始 JSON 数据。

**注意事项：**

- 免费 tier 仅提供有限的安全保护，并非绝对的安全机制。通过轮换 `X-Client-Fingerprint` 可以规避免费 tier 的限制。
- 如果省略了 `X-Client-Fingerprint`，系统将使用其他请求信息（如 IP 地址或用户代理）进行计费。

## 使用方法（代理模式，从零开始）

当用户准备发送交易时：

1. 请求缺失的必要信息：
   - `from`（发送者地址）、`to`（接收者地址）、`value`（交易金额，单位为 wei）、`data`（交易数据）或 `chain_id`（链ID）。
2. 检查是否在免费 tier 范围内（始终免费）：
   - `GET /v1/usage`
3. 并行执行交易前扫描：
   - `GET /v1/check-address/:to`
   - `POST /v1/simulate-tx`
   - （可选）`GET /v1/check-token/:token`
4. 使用以下模板回复用户（先显示摘要，再提供原始 JSON 数据）。

## 回复模板

### 安全（LOW 风险等级）

```
🛡️ Scan Complete

Risk: LOW (SAFE)
Summary: No critical warnings detected.

✅ OK to proceed.
```

### 警告（MEDIUM 风险等级）

```
🛡️ Scan Complete

Risk: MEDIUM (CAUTION)
Summary: Some warnings detected.

⚠️ Review recommended before proceeding. Want me to explain the top 3 risks?
```

### 危险（HIGH 风险等级）

```
🛡️ Scan Complete

Risk: HIGH (DANGEROUS)
Summary: Significant risks detected.

🚫 Not recommended.
```

### 交易被阻止（CRITICAL 风险等级）

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

| 文件 | URL |
|------|-----|
| **SKILL.md** | `https://aegis402.xyz/skill.md` |
| **skill.json**（元数据） | `https://aegis402.xyz/skill.json` |

**基础 URL:** `https://aegis402.xyz/v1`

### 定价

| API 端点 | 价格 | 用途 |
|----------|-------|----------|
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

**请求体字段：**

- `from`（必填）：发送者地址
- `to`（必填）：接收者地址或合约地址
- `value`（必填）：交易金额（单位为 wei）
- `data`（可选）：交易数据的十六进制表示（格式为 `0x...`）
- `chain_id`（可选）：模拟使用的链ID（默认为 Base 8453，但可根据需要更改）

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

`chain_id` 表示要扫描的链（例如：Ethereum=1，Base=8453 等）。支付方式由 `402` 协议决定（默认使用 USDC）。

### 支付方式（x402）

在免费 tier 用完之前，您可以免费使用该 API。超出免费额度后，系统会返回 “需要支付 402 费用”的提示，此时代理钱包可以自动支付并重试。

| 网络 | 代理钱包签名器 |
|---------|------------------------|
| Base（EVM） | 来自代理钱包提供商的 EVM 签名器 |
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

- 严禁向用户请求私钥、助记词或密语。
- 禁止在提示信息、日志或文档中存储签名器相关信息。
- 在进行付费调用（尤其是 `simulate-tx`）之前，必须确认用户的操作意图。
- 仅当用户明确同意自动化操作时，才能自动执行预签名检查。

## 附录

### 风险等级

| 风险等级 | 含义 | 代理默认处理方式 |
|-------|---------|---------------|
| `LOW` | 较小的风险，一般安全 | 允许交易 |
| `MEDIUM` | 存在一定风险 | 显示警告并请求用户确认 |
| `HIGH` | 高风险 | 阻止交易并要求用户确认 |
| `CRITICAL` | 极高风险 | 立即阻止交易 |

### 错误处理

| 状态码 | 含义 | 代理应采取的措施 |
|--------|---------|--------------------------|
| 400 | 参数无效 | 询问用户缺失或无效的字段并重试 |
| 402 | 需要支付费用 | 确认用户意图后使用已授权的代理钱包签名器进行签名（或等待下一个免费 tier 时段） |
| 500 | 服务或上游错误 | 重试一次；如果问题持续存在，显示错误信息及 `requestId`。

**提示：**

- 所有响应都包含 `_meta.requestId`。服务器还会设置 `x-request-id` 标头，请在错误报告中包含该信息。
- API 标头中可能包含升级提示：
  - `x-aegis-skill-latest-version`
  - `x-aegis-skill-url`
  - `x-aegis-skill-upgrade`

## v1.2.1 的新功能

- 免费 tier 每天 100 次检查（可通过 `GET /v1/usage` 查看剩余次数）。
- 响应中新增 `_meta` 字段以提高透明度（`tier`、`remainingChecks`、`usedToday`、`dailyLimit`、`nextResetAt`、`latencyMs`）。
- 为旧版本客户端提供了升级提示。
- 加强了安全性：禁止直接提供私钥示例，并明确了自动化操作的审批流程。

## 从 v1.1.x 迁移到 v1.2.x 的注意事项：

1. 在请求头中指定已安装的技能版本：`x-aegis-skill-version`。
- 在进行付费检查之前，请先通过 `GET /v1/usage` 查看剩余的免费次数。
- 确保现有的付费请求流程保持不变。

## 系统健康检查（免费）

```bash
curl https://aegis402.xyz/health
```

## 支持的链**

`chain_id` 表示要扫描的链（而非支付使用的链）。

| 链ID | 支持的 API | check-token | check-address | simulate-tx |
|-------|---------|-------------|---------------|-------------|
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
- 演示页面：https://aegis402.xyz/demo.html
- x402 协议文档：https://docs.x402.org

## 社交媒体

- X 社交平台：https://x.com/aegis402
- Telegram 频道：https://t.me/aegis402_channel
- 开发者聊天频道：https://t.me/aegis402_chat

🛡️ 专为代理经济（Agentic Economy）设计，由 x402 协议提供支持。