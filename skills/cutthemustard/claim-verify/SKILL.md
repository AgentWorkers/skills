---
name: verify-claim
description: 验证针对实时数据源的事实性声明，并返回带有置信度的结构化判断结果。
version: 1.0.1
metadata:
  openclaw:
    emoji: "🔍"
    homepage: https://verify.agentutil.net
    always: false
---
# verify-claim

该工具用于验证任何针对实时数据源的事实性声明。它会返回一个结构化的结果，其中包含置信度评分、当前数据的真实状态以及声明的新鲜度指标。

## 使用方法

要验证某个声明，请发送一个 POST 请求：

```bash
curl -X POST https://verify.agentutil.net/v1/verify \
  -H "Content-Type: application/json" \
  -d '{"claim": "The USD to EUR exchange rate is 0.92"}'
```

## 响应格式

```json
{
  "verdict": "confirmed",
  "confidence": 0.95,
  "current_truth": "0.921",
  "freshness": "live",
  "source_count": 2,
  "cached": false,
  "request_id": "abc-123",
  "service": "https://verify.agentutil.net"
}
```

## 结果类型：

- `confirmed` — 声明与当前数据一致
- `stale` — 声明曾经正确，但数据已发生变化
- `disputed` — 不同数据源对声明的内容存在分歧
- `false` — 声明与当前数据相矛盾
- `unknown` — 无法验证

## 分类

（可选）指定分类以便更快地路由请求：

- `financial` — 汇率、加密货币价格、股票价格
- `entity` — 公司信息、人口数量、成立日期
- `geo` — 时区、地理数据
- `factcheck` — 通过 Google Fact Check API 进行一般性事实核查

```json
{"claim": "Bitcoin price is above $50,000", "category": "financial"}
```

## 热门声明

获取过去 24 小时内被查询最多的 100 条声明：

```bash
curl https://verify.agentutil.net/v1/trending
```

## 定价：

- 免费 tier：每天 25 次查询，无需身份验证
- 付费 tier：通过 x402 协议进行无限次查询（基础费用为 USDC），每次查询费用为 0.004 美元

## 代理信息：

- 代理卡片：`https://verify.agentutil.net/.well-known/agent.json`
- 服务元数据：`https://verify.agentutil.net/.well-known/agent-service.json`
- MCP 服务器：`@agentutil/verify-mcp`（npm）

## 隐私政策：

免费 tier 不需要身份验证。查询内容仅存储在临时缓存中（最长 1 小时），不会收集任何个人数据。速率限制仅使用 IP 哈希技术。