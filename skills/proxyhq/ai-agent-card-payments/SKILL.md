---
name: ai-agent-card-payments
description: 用于AI代理的虚拟卡支付功能：可以创建相应的支付意图（intents），在政策允许的范围内发行虚拟卡，并在获得高级别审批后自主完成高价值交易。
---

# AI代理卡片支付功能

该功能允许AI代理在Proxy系统执行政策管控的同时，使用虚拟卡片进行购物操作。

## 功能概述：
- 在预设的限额范围内实现自主购物；
- 根据具体购物意图发放或解锁相应的卡片；
- 支持在需要时人工审核以执行政策规定；
- 生成交易证据和收据，以便进行审计追踪。

## 快速入门（代理令牌）

```
1) proxy.kyc.status
2) proxy.balance.get
3) proxy.policies.simulate (optional)
4) proxy.intents.create
5) if approvalRequired/pending_approval -> proxy.intents.request_approval
6) proxy.cards.get_sensitive
7) proxy.transactions.list_for_card
```

## MCP服务器配置

```json
{
  "mcpServers": {
    "proxy": {
      "type": "http",
      "url": "https://mcp.useproxy.ai/api/mcp",
      "headers": {
        "Authorization": "Bearer $PROXY_AGENT_TOKEN"
      }
    }
  }
}
```

## 核心工具（代理令牌）

### 意图管理（Intents）与卡片管理（Cards）：
- `proxy.intents.create`（需要代理令牌）
- `proxy.intents.list`
- `proxy.intents.get`
- `proxy_cards.getSensitive`

### 政策管理（Policies）与账户状态（Status）：
- `proxy.policies.get`
- `proxy.policies.simulate`
- `proxy.kyc.status`
- `proxy.balance.get`
- `proxy.tools.list`

### 交易管理（Transactions）与证据记录（Evidence）：
- `proxy.transactions.list_for_card`
- `proxy.transactions.get`
- `proxy.receipts.attach`
- `proxy.evidence.list_for(intent`

### 商户信息查询（Merchant Intelligence）：
- `proxy.merchants.resolve`
- `proxy.mcc.explain`
- `proxy.merchants.allowlist_suggest`

## 仅限人工使用的工具：
这些功能对代理令牌是受限的，需通过仪表板或OAuth授权才能使用：
- `proxy.funding.get`
- `proxy_cards.list` / `proxy_cards.get` / `proxy_cards.freeze` / `proxy_cards.unfreeze` / `proxy_cards.rotate` / `proxy_cards.close`
- `proxy.intents.approve` / `proxy.intents.reject`
- `proxy.webhooks.list` / `proxy.webhooks.test_event`

## 示例：完成购物流程

```
proxy.intents.create(
  purpose="Buy API credits",
  expectedAmount=5000,
  expectedMerchant="OpenAI"
)

proxy.cards.get_sensitive(
  cardId="card_xyz",
  intentId="int_abc123",
  reason="Complete OpenAI checkout"
)
```

如果购物意图尚未获得批准，请执行以下操作：

```
proxy.intents.request_approval(
  intentId="int_abc123",
  context="Above auto-approve threshold"
)
```

## 最佳实践：
- 为每个AI代理分配专属的令牌，以保障操作的自主性；在令牌被泄露时及时更换；
- 在创建购物意图前先进行模拟测试，以减少操作失败的风险；
- 通过`expectedAmount`和`expectedMerchant`参数对购物意图进行限制；
- 除非启用了发行机构（MCC）的强制审核机制，否则将MCC/商户白名单信息仅作为参考信息使用；
- 绝不要通过`proxy_cards.getSensitive`函数获取持卡人的PAN/CVV验证码信息。