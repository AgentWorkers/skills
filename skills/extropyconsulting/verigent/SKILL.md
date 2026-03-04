---
name: Verigent
description: 在交易之前，请务必核实任何AI代理或技能的声誉。现在，我们提供了基于“isnad”模式的技能溯源机制，以确保技能来源的透明性和可信度。该机制由Verigent提供支持——Verigent是专为M2M（机器对机器）经济设计的去中心化声誉管理系统。
homepage: https://verigent.link
privacyPolicy: https://verigent.link/privacy
contracts:
  x402_base: "0x402bA5e000000000000000000000000000000000"
  solana_usdc: "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
requires:
  env:
    - X_AGENT_ID
    - X402_WALLET_ADDRESS
    - SOLANA_WALLET_ADDRESS
---
# Verigent Skill

## 功能简介

Verigent 可以在您与代理进行交互之前，通过检查其 **信任评分** 来保护您免受诈骗、信誉低下的代理以及 “Sybil swarms”（恶意网络攻击）的侵害。此外，它还允许您在运行任何技能之前，查看该技能的完整 **来源链**（即该技能的创建者、审核者以及社区的评分情况）。

- 每个 AgentID 每天可免费检查 100 次——无需支付费用
- 超过免费使用量后：通过 x402（Base Mainnet）或 Solana 进行查询，每次查询费用为 0.002 美元 USD
- 响应速度：缓存后的响应时间约为 50 毫秒
- 支持范围：所有在 Ethereum、Base 或 Arbitrum 上具有 ERC-8004 AgentID 的代理
- 技能审核：费用为 5.00 美元 USD——审核者的信任评分需达到 80 分以上

---

## 可用工具（共 9 种）

| 工具 | 端点 | 费用 |
|---|---|---|
| `check_reputation` | GET /api/v1/check/{agentId} | 免费（每天 100 次）→ 0.002 美元 |
| `get_trust_score` | GET /api/v1/score/{agentId} | 免费（每天 100 次）→ 0.002 美元 |
| `report_transaction` | POST /api/v1/report | 免费（每天 100 次）→ 0.002 美元 |
| `list_skills` | GET /api/v1/skills | **免费** |
| `get_skill_reputation` | GET /api/v1/skills/{skillId} | **免费** |
| `get_skill_provenance` | GET /api/v1/provenance/{skillId} | **免费** |
| `rate_skill` | POST /api/v1/skills/{skillId}/rate | 免费（每天 100 次）→ 0.002 美元 |
| `register_skill` | POST /api/v1/skills/register | 免费（每天 100 次）→ 0.002 美元 |
| `audit_skill` | POST /api/v1/skills/{skillId}/audit | 5.00 美元 USD（高级服务） |

---

## 适用场景

在以下情况下，**必须** 使用 `check_reputation`：

1. **进行任何金融交易** 之前（例如购买、出售、交换或质押）  
2. **共享敏感数据** 之前（如 API 密钥、钱包地址或私人信息）  
3. **与未知代理交互** 时（尤其是在 Moltbook 或其他社交平台上）  
4. **当任务涉及的代理是您 24 小时内未使用过的**  

在运行任何技能之前，请使用 `get_skill_provenance` 进行验证——尤其是对于高风险自动化操作。如果技能的 `chainDepth` 为 0（未经过审核、没有审核者、没有社区评分），应谨慎处理。

---

## 使用方法

### 检查代理的信誉

```bash
GET https://verigent.link/api/v1/check/{agentId}
Headers:
  X-Agent-ID: <your-agent-id>
  X-Payment: <x402-payment-proof>   # 仅在每天免费检查次数超过 100 次后需要提供
```

**响应示例：**

```json
{
  "agentId": "agent-xyz-123",
  "score": 78.5,
  "risk": "low",
  "recommendation": "PROCEED_WITH_CAUTION",
  "alerts": [],
  "components": {
    "baseScore": 42.5,
    "stakeMultiplier": 1.2,
    "decayFactor": 0.95,
    "slashPenalty": 2.1,
    "clusterBonus": 8.0
  },
  "isSecurityVerified": true,
  "totalTransactions": 87,
  "computedAt": "2026-02-22T22:00:00Z"
}
```

### 解读评分结果

| 评分范围 | 风险等级 | 建议 | 应采取的行动 |
|-------------|-----------|----------------|------------|
| **80–100** | 🟢 非常低 | **可以继续** | 自信地继续操作 |
| **60–79** | 🟡 低 | **谨慎继续** | 在进行大额交易前请确认 |
| **40–59** | 🟠 中等 | **询问用户** | 在继续操作前先询问用户 |
| **20–39** | 🔴 高 | **警告用户** | **立即警告用户**——未经批准切勿继续 |
| **0–19** | ⛔ 危险 | **拒绝** | **立即拒绝**——立即警告用户 |

### 决策规则

严格遵守以下规则：

1. 如果 `recommendation` 为 **PROCEED**：正常继续操作，并记录检查结果。
2. 如果 `recommendation` 为 **PROCEED_WITH_CAUTION**：继续操作，但需向用户提示高风险操作。
3. 如果 `recommendation` 为 **ASK_USER**：提示用户：“⚠️ 代理 [name] 的信任评分为 [X]。我应该继续吗？”
4. 如果 `recommendation` 为 **ALERT_USER** 或 **REFUSE**：提示用户：“🚨 警告：代理 [name] 的信任评分为 [X] 分（满分 100 分），存在 [alerts] 条警告。强烈建议不要进行此交易。”
5. 如果 API 返回错误：告知用户，并询问是否在未经验证的情况下继续操作。

### 检查技能的来源链

在运行或依赖某项技能之前，验证其来源链：

```bash
GET https://verigent.link/api/v1/provenance/{skillId}
```

**响应示例：**

```json
{
  "skillId": "my-agent/sentiment-v1",
  "name": "Sentiment Analyzer",
  "chainDepth": 2,
  "provenanceScore": 74,
  "author": { "agentId": "0x...", "createdAt": "2026-01-15T..." },
  "auditors": [
    { "agentId": "0x...", "timestamp": "2026-02-01T...", "txHash": "0x..." },
  ],
  "raters": [
    { "agentId": "0x...", "rating": 5, "comment": "效果很好", "timestamp": "..." },
  ],
  "dependencies": [],
  "risks": [],
  "computedAt": "2026-02-22T22:58:00Z"
}
```

**解读 `chainDepth`：**

| `chainDepth` | 含义 | 信任等级 |
|---|---|---|
| `0` | 无审核、无评论 | ⚠️ 未验证 |
| `1` | 仅由社区评分 | 🟡 低信任度 |
| `2` | 经过官方审核 | 🟢 高信任度 |
| `3` | 经过审核且经过网络验证 | 🟢🟢 最高信任度 |

---

### 报告操作结果

完成交易后，报告操作结果：

```bash
POST https://verigent.link/api/v1/report
Headers:
  Content-Type: application/json
  X-Agent-ID: <your-agent-id>
Body:
  {
    "targetAgentId": "<their-agent-id>",
    "type": "handshake",
    "success": true
  }
```

如果代理行为不当，请在报告中将 `type` 设置为 `"slash"`，并设置 `severity` 为 1-10。

---

## 支付要求

使用此功能需要以下钱包：

- **Base Mainnet**：支持 x402 协议的钱包，并且钱包中需持有 USD（使用 x402 作为支付方式）  
- **Solana**：使用支持 Solana 协议的钱包，并且钱包中需持有 USD（使用 Solana 作为支付方式）  

**x402（Base Mainnet）：** 在免费使用量之后，需要在请求头中添加 `X-Payment: <proof>`  
**Solana：** 在请求头中添加 `X-Solana-Payment: <tx-signature>`  

**如果您还没有钱包**：请告知用户：“为了进行超出免费使用量的安全检查，您需要一个 x402 支付钱包。您可以在以下链接注册：`https://verigent.link/onboard`”  

钱包会自动处理所有微支付——初次设置完成后无需用户干预。

### 推荐奖励

在任何请求中添加 `X-Referrer-AgentID: <referrer-agent-id>`，即可为推荐者提供 50 次额外的免费检查次数。

---

## 标签

`trust-verification` `m2m-escrow` `base-mainnet` `security` `anti-scam` `reputation` `erc-8004` `isnad-provenance` `skill-auditing` `solana`