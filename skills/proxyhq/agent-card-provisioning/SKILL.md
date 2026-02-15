---
name: agent-card-provisioning
description: 根据需求为AI代理提供虚拟支付卡。可以创建一次性使用的或有效期有限的支付卡，这些卡片具有消费限制、商户限制以及自动失效的功能。当政策允许时，支付卡会立即生成并发送给相关代理。
---

# 代理卡配置

为具备内置消费控制功能的AI代理提供虚拟支付卡。

## 工作原理

1. **代理通过支付意图请求卡片**  
2. **策略评估** 请求内容（金额、商户、限额）  
3. 如果符合策略，则**发放卡片**；如果超出限额，则**需要人工审批**  
4. **代理使用卡片** 进行特定购买  
5. **交易会被追踪** 并与原始意图进行匹配  

## 创建卡片（基于支付意图）

卡片是通过支付意图来配置的，而不是直接创建的：  
```
proxy.intents.create
├── merchant: "Amazon"
├── amount: 49.99
├── description: "Office supplies"
└── category: "office_supplies" (optional)
```  

如果请求获得批准（自动或手动），卡片将被发放：  
```
Response:
├── id: "int_abc123"
├── status: "pending" or "card_issued"
├── cardId: "card_xyz789"
└── message: "Card issued successfully"
```  

## 获取卡片详情  

### 遮蔽信息（用于显示）  
```
proxy.cards.get { cardId: "card_xyz789" }
→ { last4: "4242", brand: "Visa", status: "active" }
```  

### 完整详情（用于支付）  
```
proxy.cards.get_sensitive { cardId: "card_xyz789" }
→ {
    pan: "4532015112830366",
    cvv: "847",
    expiryMonth: "03",
    expiryYear: "2027",
    billingAddress: {
      line1: "123 Main St",
      city: "New York",
      state: "NY",
      postalCode: "10001",
      country: "US"
    }
  }
```  

## 卡片控制（通过策略实现）  

策略用于定义哪些卡片可以被使用：  

| 控制方式 | 描述                |  
|---------|------------------|  
| **消费限额** | 每笔交易的最高金额限制    |  
| **每日/每月限额** | 累计消费上限        |  
| **商户类别** | 允许/禁止的商户代码（MCC）    |  
| **自动审批阈值** | 低于阈值 = 自动审批；高于阈值 = 需人工审批 |  
| **有效期** | 卡片的有效期限        |  

## 卡片生命周期  
```
Intent Created
      │
      ▼
┌─────────────┐
│   Policy    │
│  Evaluation │
└──────┬──────┘
       │
  ┌────┴────┐
  ▼         ▼
Auto     Needs
Approve  Approval
  │         │
  ▼         ▼
Card     [Human]
Issued      │
  │         │
  ◀─────────┘
  │
  ▼
Card Used
  │
  ▼
Transaction
 Matched
  │
  ▼
Card
Expired
```  

## 最佳实践  

1. **每次购买使用一个支付意图**——便于审计追踪  
2. **使用描述性强的意图名称**——有助于对交易进行对账  
3. **设置合理的策略**——在保障代理自主性的同时实现有效控制  
4. **监控交易记录**——使用 `proxy.transactions.list_for_card` 功能  

## 安全性措施  

- 卡片具有单一用途（每个支付意图对应一张卡片）  
- 未使用的卡片会自动过期  
- 仅通过 `get_sensitive` 函数获取完整的卡号信息（需要授权）  
- 所有交易都会被记录并定期对账