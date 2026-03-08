---
name: agentclear
description: "通过 AgentClear 发现、调用并支付 API——这是专为 AI 代理设计的商业平台。您可以在以下情况下使用它：  
1. 通过自然语言描述您的需求来查找相应的 API 或工具；  
2. 通过 AgentClear 代理调用付费 API 服务，并实现自动计费功能；  
3. 查看市场上可用的服务列表；  
4. 检查您的 AgentClear 帐户余额或状态。  
使用 AgentClear 需要一个 API 密钥（格式以 “axk_” 开头）。您可以在 [https://agentclear.dev](https://agentclear.dev) 免费获取一个 API 密钥，同时还能获得 5 美元的信用额度。"
metadata:
  openclaw:
    requires:
      env:
        - AGENTCLEAR_API_KEY
---
# AgentClear — 代理商业层

通过自然语言发现并调用付费API。每个请求仅使用一个API密钥，按次计费，零摩擦。

## 设置

需要`AGENTCLEAR_API_KEY`环境变量（以`axk_`开头）。

```bash
export AGENTCLEAR_API_KEY="axk_your_key_here"
```

使用5美元的免费信用额度获取API密钥：https://agentclear.dev/login

## 数据与隐私

- **发现查询**用于语义匹配，并被记录以用于Bounty Board（用于收集缺失服务的需求信号）。不会收集任何个人身份信息（PII）。
- **代理请求**会将您的数据包转发到您选择的上游服务提供商。AgentClear不存储请求/响应的数据包，仅存储计费元数据（服务ID、时间戳、费用）。
- **API密钥**用于身份验证和计量使用情况。密钥仅限于您的账户，并可随时被撤销。
- 所有流量均通过HTTPS传输。详情请参阅https://agentclear.dev/security。

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

响应会返回排名靠前的服务，包括`id`、`name`、`description`、`price_per_call`和`trust_score`。

### 调用服务
通过AgentClear代理请求（每次请求自动计费）：
```bash
curl -X POST https://agentclear.dev/api/proxy/{service_id} \
  -H "Authorization: Bearer $AGENTCLEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"your": "payload"}'
```

数据包会被转发到上游服务。响应中包含服务结果以及计费元数据。

### 列出服务
浏览可用的服务：
```bash
curl https://agentclear.dev/api/services \
  -H "Authorization: Bearer $AGENTCLEAR_API_KEY"
```

## 工作流程

1. **发现** — 描述您的需求 → 获取排名靠前的服务匹配结果
2. **评估** — 检查价格、信任评分和描述
3. **调用** — 通过AgentClear代理请求 → 获取结果并按次付费
4. 如果没有服务可用，请查看https://agentclear.dev/bounties上的**Bounty Board**

## 价格

- 服务费用每次请求从0.001美元到1美元以上不等（由服务提供商设定）
- 平台费用：2.5%
- 新账户可享受**5美元的免费信用额度**
- 账户余额会自动扣除每次请求的费用

## 提示

- 使用具体且描述性强的查询语句以获得更好的搜索结果（例如：“将QuickBooks QBO文件解析为JSON”比“解析文件”更有效）
- 链式使用服务：先发现服务 → 调用服务 → 将结果作为输入用于另一个服务
- 如果发现查询没有返回结果，该查询会被记录在Bounty Board上作为需求信号——服务提供商会根据此信号开发相应服务