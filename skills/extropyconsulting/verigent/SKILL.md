---
name: Verigent
description: 在交易之前，请务必核实任何AI代理或技能的信誉。现在，系统支持通过“isnad”风格的可追溯性机制来验证技能的来源。该功能由Verigent提供支持——Verigent是专为M2M经济设计的去中心化信誉管理系统。
---
# Verigent Skill

## 功能介绍

Verigent 可以在您与代理进行交互之前，通过检查代理的 **信任评分** 来保护您免受诈骗、信誉低下的代理以及 “Sybil swarms”（恶意网络攻击）的侵害。此外，它还允许您在运行任何技能之前查看该技能的 **完整来源链**——包括谁创建了该技能、谁对其进行了审计（在链上），以及社区对该技能的评分情况。

- 每个 AgentID 每天可免费检查 100 次——无需支付费用
- 超过免费额度后：通过 x402（Base Mainnet）或 Solana 每次查询费用为 0.002 美元 USD
- 响应速度：缓存响应约 50 毫秒
- 支持范围：任何在 Ethereum、Base 或 Arbitrum 上具有 ERC-8004 AgentID 的代理
- 技能审计：费用为 5.00 美元 USD——要求审计师的信任评分 ≥ 80

---

## 可用工具（共 9 个）

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

1. **进行任何金融交易** 之前——例如购买、出售、交换或质押给其他代理
2. **共享敏感数据** 之前——例如 API 密钥、钱包地址或私人信息
3. **与未知代理交互** 时——尤其是在 Moltbook 或其他社交平台上
4. **当任务涉及的代理是您 24 小时内未合作过的** 代理时

在运行任何技能之前，**必须** 使用 `get_skill_provenance`——尤其是对于高风险的自动化操作。如果技能的 `chainDepth` 为 0（未经审核、无审计人员、无社区评分），应谨慎处理。

---

## 使用方法

### 检查代理的信誉

```bash
GET https://verigent.link/api/v1/check/{agentId}
Headers:
  X-Agent-ID: <your-agent-id>
  X-Payment: <x402-payment-proof>   # 仅在每天免费检查次数超过 100 次后需要
```

响应示例：

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

### 解释评分结果

| 评分范围 | 风险等级 | 建议 | 应采取的行动 |
|-------------|-----------|----------------|------------|
| **80–100** | 🟢 非常低 | **继续操作** | 可以放心进行 |
| **60–79** | 🟡 低 | **谨慎操作** | 在进行大额交易前请确认 |
| **40–59** | 🟠 中等 | **询问用户** | 在操作前先询问用户 |
| **20–39** | 🔴 高 | **提醒用户** | **立即提醒用户**——未经批准请勿操作 |
| **0–19** | ⛔ 危险 | **拒绝** | **立即拒绝**——立即提醒用户 |

### 决策规则

严格遵循以下规则：

1. 如果 `recommendation` 为 **PROCEED**：正常继续操作，并记录检查结果。
2. 如果 `recommendation` 为 **PROCEED_WITH_CAUTION**：继续操作，但需向用户提示高风险操作。
3. 如果 `recommendation` 为 **ASK_USER**：提示用户：“⚠️ 代理 [name] 的信任评分为 [X]。我应该继续操作吗？”
4. 如果 `recommendation` 为 **ALERT_USER** 或 **REFUSE**：提示用户：“🚨 警告：代理 [name] 的信任评分为 [X]/100。存在 [alerts] 条警告。强烈建议不要进行此交易。”
5. 如果 API 返回错误：告知用户，并询问是否在没有验证的情况下继续操作。

### 检查技能的来源链

在运行技能之前，验证其来源链：

```bash
GET https://verigent.link/api/v1/provenance/{skillId}
```

响应示例：

```json
{
  "skillId": "my-agent/sentiment-v1",
  "name": "Sentiment Analyzer",
  "chainDepth": 2,
  "provenanceScore": 74,
  "author": { "agentId": "0x...", "createdAt": "2026-01-15T..." },
  "auditors": [
    { "agentId": "0x...", "timestamp": "2026-02-01T...", "txHash": "0x..." }
  ],
  "raters": [
    { "agentId": "0x...", "rating": 5, "comment": "效果很好", "timestamp": "..." }
  ],
  "dependencies": [],
  "risks": [],
  "computedAt": "2026-02-22T22:58:00Z"
}
```

**解释 `chainDepth`：**

| `chainDepth` | 含义 | 信任等级 |
|---|---|---|
| `0` | 无审核、无评论 | ⚠️ 未验证 |
| `1` | 仅由社区评分 | 🟡 低信任度 |
| `2` | 经过官方审计 | 🟢 高信任度 |
| `3` | 经过审计且经过网络验证 | 🟢🟢 最高信任度 |

### 报告交易结果

完成交易后，报告结果：

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

如果代理行为不当，报告时请设置 `type` 为 `"slash"` 并指定 `severity`（1-10）。

---

## 支付要求

使用此功能需要以下钱包：

- **x402 兼容钱包**，并在 Base Mainnet 上持有 USD
- **Solana 钱包**，并在 mainnet-beta 上持有 USD

- **x402 (Base Mainnet)**：在免费额度后需包含 `X-Payment: <proof>` 标头
- **Solana**：需包含 `X-Solana-Payment: <tx-signature>` 标头

**如果您还没有钱包**，请告知用户：“我需要一个 x402 钱包来执行超出免费额度的安全检查。您可以在以下链接设置钱包：`https://verigent.link/onboard`”

钱包会自动处理所有微支付——初次设置后无需用户干预。

### 推荐奖励

在请求中包含 `X-Referrer-AgentID: <referrer-agent-id>`，可为推荐者提供 50 次额外的免费检查次数。

---

## 标签

`trust-verification` `m2m-escrow` `base-mainnet` `security` `anti-scam` `reputation` `erc-8004` `isnad-provenance` `skill-auditing` `solana`