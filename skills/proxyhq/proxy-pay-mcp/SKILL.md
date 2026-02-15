---
name: proxy-pay-mcp
description: **用于代理MCP服务器的集成方案，以实现代理支付功能：**  
通过MCP工具创建支付相关的意图（intents），根据政策要求发行支付卡片（cards），并追踪交易流程。该方案支持使用代理令牌（agent tokens）进行自主操作，同时兼容OAuth协议以支持交互式客户端（interactive clients）的接入。
---

# 代理MCP集成

连接到代理的MCP服务器以进行代理支付。

## MCP服务器配置

### 代理令牌（自主操作）

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

### OAuth（交互式客户端）

添加MCP服务器并运行您的客户端的OAuth登录流程。OAuth适用于交互式客户端（如Codex、Claude、Cursor）。

## 核心流程（代理令牌）

```
proxy.kyc.status
proxy.balance.get
proxy.policies.simulate (optional)
proxy.intents.create
if approvalRequired/pending_approval -> proxy.intents.request_approval
proxy.cards.get_sensitive (include intentId + reason)
proxy.transactions.list_for_card
```

## 代理令牌相关工具（自主操作）

- `proxy.user.get`
- `proxy.kyc.status`
- `proxy.kyc.link`
- `proxy.policies.get`
- `proxy.policies.simulate`
- `proxy.balance.get`
- `proxy.tools.list`
- `proxy.intents.create`（需要代理令牌）
- `proxy.intents.list`
- `proxy.intents.get`
- `proxy.intents.request_approval`
- `proxy.intents.approval_status`
- `proxy_cards.get_sensitive`
- `proxy.transactions.list_for_card`
- `proxytransactions.get`
- `proxy.receipts.attach`
- `proxy.evidence.list_for(intent`
- `proxy.merchants.resolve`
- `proxy.mcc.explain`（建议性操作）
- `proxy.merchants.allowlist_suggest`（建议性操作）

## 仅限人工使用的工具（对代理令牌禁用）

- `proxy.funding.get`
- `proxy_cards.list`
- `proxy_cards.get`
- `proxy_cards.freeze`
- `proxy_cards.unfreeze`
- `proxy_cards.rotate`
- `proxy_cards.close`
- `proxy.intents.approve`
- `proxy.intents.reject`
- `proxy.webhooks.list`
- `proxy.webhooks.test_event`

## 审批规则

- 仅当`policy.requireApproval`为`true`且金额超过`autoApproveBelow`时才需要审批。
- 代理应仅在必要时调用`proxy.intents.request_approval`。

## 注意事项

- 每次购买都需要使用`intents`。在处理多个请求期间，卡片状态将保持锁定状态。
- 除非启用了发行机构级别的控制，否则商家/MCC规则仅具有建议性作用。
- 使用`proxy_cards.getSensitive`时需要提供`intentId`和明确的原因；请避免记录PAN/CVV信息。
- 金额以分为单位；适用的情况下，会提供格式化的显示字段。

## 错误格式

```json
{
  "success": false,
  "error": {
    "code": "POLICY_REQUIRED",
    "message": "No policy configured",
    "hint": "Assign a policy to this agent",
    "context": "intents.create"
  }
}
```