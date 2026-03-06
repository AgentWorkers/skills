---
name: agentclear
description: "通过 AgentClear 发现、调用并支付 API——这是专为 AI 代理设计的商业平台。您可以在以下情况下使用它：  
1. 通过自然语言描述您的需求来查找相应的 API 或工具；  
2. 通过 AgentClear 代理调用付费 API 服务，并实现自动微支付功能；  
3. 查看市场上可用的服务列表；  
4. 检查您的 AgentClear 帐户余额或状态。  
使用 AgentClear 需要一个 API 密钥（格式以 “axk_” 开头）。您可以在 [https://agentclear.dev](https://agentclear.dev) 免费获取一个 API 密钥，同时还能获得 5 美元的信用额度。"
---
# AgentClear — 代理商业层

通过自然语言发现并调用付费API。每个请求仅使用一个API密钥，按次计费，零摩擦体验。

## 设置

将您的API密钥设置为环境变量或直接在代码中传递：
```bash
export AGENTCLEAR_API_KEY="axk_your_key_here"
```

通过使用$5的信用额度获取免费密钥：https://agentclear.dev/login

## 端点

基础URL：`https://agentclear.dev`

### 发现服务
通过描述您的需求来查找API：
```bash
curl -X POST https://agentclear.dev/api/discover \
  -H "Authorization: Bearer $AGENTCLEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "parse invoices from PDF", "limit": 5}'
```

响应会返回按排名排列的服务列表，包括`id`、`name`、`description`、`price_per_call`和`trust_score`等信息。

### 调用服务
通过AgentClear代理请求（每次请求自动计费）：
```bash
curl -X POST https://agentclear.dev/api/proxy/{service_id} \
  -H "Authorization: Bearer $AGENTCLEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"your": "payload"}'
```

请求数据会被转发给上游服务。响应中包含服务结果以及计费相关信息。

### 列出服务
浏览可用的服务：
```bash
curl https://agentclear.dev/api/services \
  -H "Authorization: Bearer $AGENTCLEAR_API_KEY"
```

## 工作流程

1. **发现** — 描述您的需求 → 获取排名靠前的服务匹配结果
2. **评估** — 检查价格、信任评分和服务描述
3. **调用** — 通过AgentClear代理请求 → 获取结果并按次付费
4. 如果没有合适的服务，可以查看https://agentclear.dev/bounties上的**悬赏板**。

## 价格政策

- 服务费用为每次请求0.001美元至1美元以上（由服务提供商设定）
- 平台手续费：2.5%
- 新账户可享受**5美元的免费信用额度**
- 账户余额会自动用于每次请求的计费

## 提示

- 使用具体且描述性强的查询语句以获得更好的搜索结果（例如：“将QuickBooks QBO文件解析为JSON”比“解析文件”更有效）
- 链式使用服务：先发现服务，再调用该服务，然后将结果作为输入用于其他服务
- 如果搜索查询没有返回结果，该请求会被记录在悬赏板上，供服务提供商参考并可能开发相应服务