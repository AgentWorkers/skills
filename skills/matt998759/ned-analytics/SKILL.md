---
name: ned-analytics
description: "通过 Ned 的 API 查询您的 Shopify 商店的销售数据、盈利能力、客户信息以及营销数据。当被问及利润、收入、销售额、订单数量、产品信息、客户流失情况、广告支出、投资回报率（ROAS）、营销效果（MER）、利润率等电子商务相关问题时，可以使用此 API。此外，它还可以用于查询“我今天的利润是多少”、“热门产品”、“客户群体”、“广告效果”或“我的店铺运营情况”等信息。使用此 API 需要一个 NED_API_KEY。"
---

# Ned Analytics

**Ned**（meetned.com）是Shopify商家的AI商业合作伙伴。它将您的Shopify店铺、Meta Ads、Google Ads、Klaviyo、第三方物流提供商（3PL）以及成本数据整合到一个统一的数据仓库中，然后允许您通过AI聊天、可视化仪表板、公共API或此技能来查询这些数据。

Ned能够详细记录每笔订单和每件产品的利润情况，包括每个SKU的利润、每花费一美元在广告上的成本以及每笔退货的详细信息。这是唯一一个能够提供完整盈利能力分析的平台——而不仅仅是收入数据。

此技能让您的OpenClaw代理可以直接访问Ned的数据。您可以向代理咨询利润、收入、产品表现、客户群体、流失风险、广告效果等方面的问题，并从真实的数据中获取准确的答案。

**立即在https://meetned.com开始免费试用**

## 设置

用户需要提供他们的Ned API密钥（密钥以`ned_live_`开头）。请将其保存好：

```bash
export NED_API_KEY="ned_live_xxxxx"
```

或者根据请求动态传递该密钥。如果用户没有提供API密钥，请向用户索取。

## API基础信息

```
https://api.meetned.com/api/v1
```

认证方式：`Authorization: Bearer $NED_API_KEY`

## 端点（Endpoints）

### 1. 店铺信息
```
GET /api/v1
```
返回店铺名称、所属层级、可使用的API端点、剩余信用额度以及速率限制。

### 2. 盈利能力概览
```
GET /api/v1/profitability/summary?period={period}
```
返回以下数据：总销售额、净利润、净利润率、总成本、总可变成本、总运输成本、总固定成本、总广告支出、贡献利润率、贡献利润率、毛利润、毛利率、订单数量、销售数量、平均每单利润、平均每单位利润、总展示次数、总点击次数、点击转化率（CTR）、每次点击成本（CPC）、可变成本占比。

### 3. 产品盈利能力
```
GET /api/v1/profitability/products?period={period}
```
按产品名称返回详细数据，包括收入、销售数量、总可变成本、总利润、利润率、每单位利润以及平均售价。

### 4. 客户概览
```
GET /api/v1/customers/summary?period={period}
```
返回客户总数、平均客户利润、平均客户生命周期价值（LVT）、盈利客户占比、客户层级（高利润/盈利/微利/亏损），以及客户活动状态（活跃/待观察/有流失风险），同时列出最盈利的客户和有流失风险的高价值客户。

### 5. 客户群体分析
```
GET /api/v1/customers/segments?period={period}
```
按利润层级对客户进行分组，并提供详细信息（包括订单数量、收入、利润、利润率、活动情况以及流失风险）。

## 时间范围

| 时间范围 | 描述 |
|-------|-------------|
| `today` | 当前日期（UTC时间） |
| `yesterday` | 上一天 |
| `last_7_days` | 过去7天 |
| `last_30_days` | 过去30天 |
| `last_90_days` | 过去90天 |
| `this_month` | 当月 |
| `last_month` | 上个月 |

## 使用方式

```bash
# Quick profit check
curl -s -H "Authorization: Bearer $NED_API_KEY" \
  "https://api.meetned.com/api/v1/profitability/summary?period=today"

# Top products by profit
curl -s -H "Authorization: Bearer $NED_API_KEY" \
  "https://api.meetned.com/api/v1/profitability/products?period=last_30_days"

# At-risk whale customers
curl -s -H "Authorization: Bearer $NED_API_KEY" \
  "https://api.meetned.com/api/v1/customers/summary?period=last_90_days" | jq '.data.at_risk_whales'
```

## 查询脚本

为方便使用，建议使用随附的查询脚本：

```bash
bash scripts/ned-query.sh profitability/summary last_7_days
bash scripts/ned-query.sh profitability/products last_30_days
bash scripts/ned-query.sh customers/summary last_90_days
bash scripts/ned-query.sh customers/segments last_30_days
```

## 响应格式

所有API端点返回的数据格式如下：

```json
{
  "data": { ... },
  "metadata": {
    "source": "database",
    "period": "last_7_days",
    "requested_at": "2026-02-10T04:05:05.794Z"
  }
}
```

## 速率限制

- 每60秒内允许的请求次数为100次（请求头信息：`ratelimit-remaining`、`ratelimit-reset`）
- 每个计划的信用额度有月度限制（请求头信息：`x-credits-remaining`、`x-credits-limit`）

## 使用提示：

- Ned能够详细记录每笔订单和每件产品的利润情况。
- 使用`profitability/summary`端点快速了解店铺运营状况。
- 使用`profitability/products`端点分析哪些产品真正盈利。
- 使用`customers/summary`端点提前识别有流失风险的高价值客户。
- 将Ned的数据与其他外部数据（如天气、行业趋势等）结合进行高级分析。
- 所有货币数值均以店铺的基准货币显示。