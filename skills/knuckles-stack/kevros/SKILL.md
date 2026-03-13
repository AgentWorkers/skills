---
name: govern
description: "在采取任何行动之前，务必验证相关操作的正确性，确认数据的来源真实性，并检查其他参与方的信任度。"
version: 0.3.3
author: TaskHawk Systems
license: BSL-1.1
tags: [governance, trust, verification, provenance, compliance, security]
requires: [x402]
---
# 技能治理（Skill Governance）

为您的代理钱包（Agent Wallet）添加治理验证功能。在执行操作前进行验证，操作完成后进行记录，与合作伙伴协作前检查对方的信任度。

## 使用场景

1. **在高风险操作前**（交易金额超过100美元、资产转移、系统部署、外部API调用）：
   调用 `verify_action` 函数，根据加密生成的令牌（release_token）获取“允许（ALLOW）”、“限制（CLAMP）”或“拒绝（DENY）”的决策结果。

2. **操作完成后**：
   调用 `attest_provenance` 函数，将操作记录到不可篡改的、基于哈希链的审计日志中。这有助于逐步提升您的信任评分。

3. **与未知代理协作前**：
   调用 `check_peer_trust` 函数，检查对方的信任评分、链长度以及历史决策记录。

4. **执行已声明的计划前**：
   调用 `bind(intent` 函数，将您的操作意图以加密方式绑定到具体命令上，执行后再次验证结果。

## 端点（Endpoints）

所有端点的费用均为0.02美元（x402定价标准），费用会自动从您的钱包（使用USDC作为支付货币）中扣除。

### verify_action — 费用：0.01美元

```bash
npx awal@latest x402 pay https://governance.taskhawktech.com/governance/verify \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "action_type": "trade",
    "action_payload": {"asset": "ETH", "amount": 500, "side": "buy"},
    "agent_id": "my-agent"
  }
```

响应：
```json
{
  "decision": "ALLOW",
  "verification_id": "vrf_...",
  "release_token": "...",
  "provenance_hash": "...",
  "epoch": 42
}
```

### attest_provenance — 费用：0.02美元

```bash
npx awal@latest x402 pay https://governance.taskhawktech.com/governance/attest \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "my-agent",
    "action_description": "执行了ETH购买订单",
    "action_payload": {"asset": "ETH", "amount": 500, "filled_price": 3200}
```

响应：
```json
{
  "attestation_id": "att_...",
  "hash_prev": "...",
  "hash_curr": "...",
  "chain_length": 42
}
```

### check_peer_trust — 免费

```bash
curl https://governance.taskhawktech.com/governance/reputation/peer-agent-id
```

响应：
```json
{
  "agent_id": "peer-agent-id",
  "trust_score": 1.0,
  "chain_length": 120,
  "attestation_count": 95,
  "outcome_count": 30,
  "achieved_count": 30,
  "chain_intact": true
}
```

### bind(intent — 费用：0.02美元

```bash
npx awal@latest x402 pay https://governance.taskhawktech.com/governance/bind \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "my-agent",
    "intent_type": "AI 自动生成",
    "intent_description": "在价格降至3000美元以下时购买ETH",
    "command_payload": {"action": "limit_buy", "asset": "ETH", "price": 3000},
    "intent_source": "AI_PLANNER"
  }
```

响应：
```json
{
  "intent_id": "int_...",
  "binding_id": "bind_...",
  "binding_hmac": "...",
  "command_hash": "..."
}
```

## 决策流程

```plaintext
代理接收到任务 →
       │
       ▼
  是否属于高风险操作？  ── 否 ──▶ 正常执行
       │
      是
       │
       ▼
  调用 verify_action()
       │
       ├── 允许执行 ──▶ 执行操作并记录审计信息
       │
       ├── 限制执行 ──▶ 在修改后的条件下执行并记录审计信息
       │
       └── 拒绝执行 ──▶ 不得执行，并向管理员报告。
```

## 发现服务（Service Discovery）

该服务可通过x402 Bazaar进行查找：

```bash
# 查找治理相关服务
npx awal@latest x402 bazaar search governance

# 获取完整的服务发现文档
curl https://governance.taskhawktech.com/.well-known/x402
```

## 与AgentKit的集成

如果您使用完整的AgentKit SDK，请安装`ActionProvider`：

```bash
pip install coinbase-agentkit-kevros  # Python
npm install @kevros/agentkit          # TypeScript
```

`ActionProvider`会使用AgentKit的接口模式来封装这些相同的端点功能。