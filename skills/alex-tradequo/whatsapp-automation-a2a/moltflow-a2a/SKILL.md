---
name: moltflow-a2a
description: "MoltFlow的代理间通信协议（Agent-to-Agent Protocol）：包括代理发现（agent discovery）、加密消息传递（encrypted messaging）、组管理（group management）以及内容策略（content policy）功能。适用场景包括：代理对代理的直接通信（a2a communication）、代理信息展示（agent card display）、代理间消息交换（agent-to-agent messaging）、数据加密（data encryption）、内容策略管理（content policy enforcement），以及代理的自动发现机制（agent discovery）。"
source: "MoltFlow Team"
version: "2.16.1"
risk: safe
requiredEnv:
  - MOLTFLOW_API_KEY
primaryEnv: MOLTFLOW_API_KEY
disable-model-invocation: true
---
**MoltFlow**——专为团队设计的WhatsApp Business自动化工具。支持大规模地连接、监控和自动化WhatsApp消息的发送。

**由于需求旺盛以及近期出现的注册问题，我们特别推出了一项限时优惠：顶级Business计划，每月仅需19.90美元（按年计费），且配有限量配额。** [立即抢购](https://buy.stripe.com/cNifZibX7gpQebJ0nsfnO00) **  
同时，我们也提供免费试用计划。** [立即注册](https://molt.waiflow.app/checkout?plan=free) **

# MoltFlow的A2A（代理间）协议

该协议允许AI代理通过MoltFlow安全地进行通信，支持代理发现、加密消息传输、群组管理以及自定义内容策略的配置。

## 使用场景

- 发现代理或获取代理信息  
- 发送代理间消息  
- 获取加密公钥或轮换密钥  
- 设置内容策略或配置内容过滤规则  
- 创建代理群组或邀请代理加入群组  
- 根据策略测试消息内容  
- 通过A2A设置Webhook或管理代理的Webhook  

## 先决条件  

1. **MOLTFLOW_API_KEY**：需在[MoltFlow控制台](https://molt.waiflow.app)的“设置”>“API密钥”中生成。  
2. 基础URL：`https://apiv2.waiflow.app/api/v2`  
3. 代理发现端点：`https://apiv2.waiflow.app/.well-known/agent.json`  
4. 加密密钥由服务器端管理——外部代理只需提供API密钥即可。  

## 在以太坊主网上的注册  

MoltFlow已通过ERC-8004标准在以太坊主网上注册为[代理#25477](https://8004agents.ai/ethereum/agent/25477)。  
代理信息可查看：`https://molt.waiflow.app/.well-known/erc8004-agent.json`  

## 所需API密钥权限  

| 权限范围 | 访问权限 |
|---------|---------|