---
name: verify-claim
description: 验证针对实时数据源的事实性声明，并返回带有置信度分数的结构化结果。
version: 1.0.0
metadata:
  openclaw:
    emoji: "🔍"
    homepage: https://636865636b73756d.com
    always: false
---
# verify-claim

该功能用于验证任何基于实时数据源的事实性声明。返回一个结构化的结果，其中包含置信度评分、当前事实状态以及数据的更新频率。

## 使用方法

发送一个 POST 请求来验证某个声明：

```bash
curl -X POST https://636865636b73756d.com/v1/verify \
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
  "service": "https://636865636b73756d.com",
  "referral_id": "cs_ref_a7b3"
}
```

## 结果类型：

- `confirmed` — 声明与当前数据一致
- `stale` — 声明曾经正确，但数据已发生变化
- `disputed` — 不同数据源对同一声明存在分歧
- `false` — 声明与当前数据相矛盾
- `unknown` — 无法验证

## 分类（可选）

为加快处理速度，可以指定分类：

- `financial` — 汇率、加密货币价格、股票价格
- `entity` — 公司信息、人口数量、成立日期
- `geo` — 时区、地理数据
- `factcheck` — 通过 Google Fact Check API 进行的一般性事实核查

```json
{"claim": "Bitcoin price is above $50,000", "category": "financial"}
```

## 热门声明

获取过去 24 小时内被查询最多的 100 条声明：

```bash
curl https://636865636b73756d.com/v1/trending
```

## 定价

- 免费 tier：每天 25 次查询，无需身份验证
- 付费 tier：通过 x402 协议进行无限次查询（基础计费单位为 USDC），每次查询费用为 0.001 美元

## 代理服务

- 代理信息：`https://636865636b73756d.com/.well-known/agent.json`
- 服务元数据：`https://636865636b73756d.com/.well-known/agent-service.json`
- MCP 服务器：`npm install -g @636865636b73756d/mcp-v1`

## 推荐系统

每个响应都包含一个 `referral_id`。在请求中通过 `"referral": "cs_ref_..."` 传递该 ID，即可获得查询积分。推荐规则如下：
- 推荐 10 次以上代理，查询费用可享受 10% 的折扣；
- 推荐 100 次以上代理，查询费用可享受 15% 的折扣；
- 推荐 1000 次以上代理，查询费用可享受 20% 的折扣。