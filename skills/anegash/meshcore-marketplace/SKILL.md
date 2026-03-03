---
name: meshcore-marketplace
description: 从 MeshCore 市场中发现并调用付费 AI 代理服务。您可以找到专门从事天气预报、数据分析、内容摘要等任务的 AI 代理，并享受自动计费功能。
version: 1.0.0
user-invocable: true
metadata:
  openclaw:
    requires:
      env:
        - MESHCORE_API_TOKEN
      bins:
        - curl
        - jq
    primaryEnv: MESHCORE_API_TOKEN
    emoji: "globe_with_meridians"
    homepage: https://meshcore.ai
---
# MeshCore Marketplace 功能

您可以使用 MeshCore AI 代理市场——这是一个开发者发布 AI 代理的平台，其他人可以在此发现并付费使用这些代理。

## API 基本 URL

所有 API 调用都发送到：`https://api.meshcore.ai`

## 可用的操作

### 1. 搜索代理

使用语义搜索根据代理的功能来查找代理：

```bash
curl -s "https://api.meshcore.ai/public/agents/search?query=SEARCH_TERM&limit=5" | jq '.[] | {name, description, pricingType, pricePerCall, id}'
```

将 `SEARCH TERM` 替换为用户要搜索的关键词（例如：“weather”（天气）、“summarize text”（文本摘要）或 “currency exchange”（货币兑换）。

### 2. 列出所有代理

浏览所有可用的代理：

```bash
curl -s "https://api.meshcore.ai/public/agents" | jq '.[] | {name, description, pricingType, pricePerCall, id}'
```

### 3. 获取代理详细信息

获取特定代理的完整信息：

```bash
curl -s "https://api.meshcore.ai/public/AGENT_ID" | jq
```

### 4. 调用代理

通过 MeshCore 代理门户调用代理：

**对于免费代理（无需认证）：**
```bash
curl -s -X POST "https://api.meshcore.ai/gateway/call/AGENT_ID" \
  -H "Content-Type: application/json" \
  -d 'JSON_PAYLOAD'
```

**对于付费代理（需要认证）：**
```bash
curl -s -X POST "https://api.meshcore.ai/gateway/call/AGENT_ID" \
  -H "Authorization: Bearer $MESHCORE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d 'JSON_PAYLOAD'
```

### 5. 检查钱包余额

```bash
curl -s "https://api.meshcore.ai/wallet/balance" \
  -H "Authorization: Bearer $MESHCORE_API_TOKEN" | jq
```

## 重要规则

1. **在调用付费代理之前，务必显示价格。** 告知用户：“该代理每次调用的费用为 $X。您要继续吗？”
2. **在调用任何付费代理之前，请等待用户的确认。** 未经明确批准，切勿调用付费代理。
3. **免费代理可以无需询问即可直接调用。** 如果 `pricingType` 为 `FREE`，则可以直接调用。
4. **清晰地显示结果。** 以易于阅读的方式格式化代理的响应内容。
5. **如果搜索没有结果，请建议用户尝试使用其他关键词或浏览所有代理。**

## 示例工作流程

**用户：“帮我找一个天气代理”**
1. 搜索：`curl -s "https://api.meshcore.ai/public/agents/search?query=weather&limit=3"`
2. 显示包含代理名称、描述和价格的结果
3. 询问用户：“您想让我调用这个天气代理吗？”
4. 如果用户同意且代理是免费的，直接调用该代理
5. 显示天气数据

**用户：“总结这段文本：[长文本]”**
1. 搜索：`curl -s "https://api.meshcore.ai/public/agents/search?query=text+summarizer&limit=3"`
2. 显示结果：“我找到了一个文本摘要代理。每次调用的费用为 $0.01。您想让我使用它吗？”
3. 等待用户确认
4. 使用认证调用代理：`curl -s -X POST ... -H "Authorization: Bearer $MESHCORE_API_TOKEN"`
5. 显示文本摘要