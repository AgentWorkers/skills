---
name: intellectia-stock-forecast
description: **US Stock AI Trading Assistant | Intellectia AI Stock Forecast**  
– 智能分析股票买入/卖出时机、目标价格预测、概率计算以及技术评级；  
– 支持“是否应该买入”的投资决策咨询功能。
metadata: {"openclaw":{"requires":{"bins":["curl","python3"]},"install":[{"id":"python","kind":"pip","package":"requests","bins":[],"label":"Install requests (pip)"}]}}
---

# Intellectia 股票预测

该技能提供了来自 Intellectia API 的单只股票 **预测**（年度预测）以及 **“我应该买入吗？”** 的分析结果。

基础 URL：`https://api.intellectia.ai`

## 概述

该技能包含两个终端点：

- **预测（predictions）**：`GET /gateway/v1/stock/screener-public`
- **为什么/我应该买入（analysis）**：`POST /gateway/v1/finance/should-i-buy`

## 适用场景

当您需要以下信息时，请使用该技能：
- 获取某只股票/加密货币的报价及 2026–2035 年的年度预测
- 了解为何应该买入某只股票，并获得结构化的分析理由

## 使用方法（高命中率）

如果您希望 OpenClaw 自动使用该技能，请提供以下信息：
- **服务提供商**：Intellectia
- **股票代码**（例如：TSLA、AAPL、BTC-USD）
- 指定您需要的是 **预测** 还是 **分析** 结果

要强制使用该技能，请输入：`/skill intellectia-stock-forecast <您的请求>`

**示例请求**：
- “获取 TSLA 的预测结果。显示价格、概率、盈利情况以及 2026–2035 年的预测。”
- “我应该买入 TSLA 吗？请提供分析结果。”
- “我应该买入 AAPL 吗？请给出结论、买入理由、分析师评级以及 52 周的价格区间。”
- “获取 BTC-USD 的年度预测结果（资产类型为 2）。”

## 终端点

| 用途 | 方法 | 路径 |
|---|---|---|
| 获取 2026–2035 年的预测 | GET | `/gateway/v1/stock/screener-public` |
| 为什么/我应该买入分析 | POST | `/gateway/v1/finance/should-i-buy` |

## API：预测（screener-public）

- **方法**：`GET /gateway/v1/stock/screener-public`
- **查询参数**：
  - `ticker`（字符串，必填）
  - `asset_type`（整数，必填）：`0=股票`、`1=ETF`、`2=加密货币`
- **返回值**：`data.list`（单个对象）+ `data.prediction_2026` … `data.prediction_2035`

### 示例（cURL）

```bash
curl -sS "https://api.intellectia.ai/gateway/v1/stock/screener-public?ticker=TSLA&asset_type=0"
```

### 示例（Python）

```bash
python3 - <<'PY'
import requests
r = requests.get("https://api.intellectia.ai/gateway/v1/stock/screener-public", params={"ticker": "TSLA", "asset_type": 0}, timeout=30)
r.raise_for_status()
data = r.json().get("data") or {}
obj = data.get("list") or {}
print("symbol:", obj.get("symbol"), "price:", obj.get("price"))
for y in range(2026, 2036):
    k = f"prediction_{y}"
    if k in data: print(k, data[k])
PY
```

## API：为什么/我应该买入（should-i-buy）

- **方法**：`POST /gateway/v1/finance/should-i-buy`
- **请求头**：`Content-Type: application/json`
- **请求体**：

```json
{ "asset": { "ticker": "TSLA", "asset_type": 0, "locale": "en" } }
```

- **返回值**：`data.action_type`、`data.conclusion`、买入理由、技术分析、分析师评级以及价格信息

### 示例（cURL）

```bash
curl -sS -X POST "https://api.intellectia.ai/gateway/v1/finance/should-i-buy" \
  -H "Content-Type: application/json" \
  -d '{"asset":{"ticker":"TSLA","asset_type":0,"locale":"en"}}'
```

### 示例（Python）

```bash
python3 - <<'PY'
import requests
r = requests.post("https://api.intellectia.ai/gateway/v1/finance/should-i-buy",
  json={"asset": {"ticker": "TSLA", "asset_type": 0, "locale": "en"}}, timeout=30)
r.raise_for_status()
d = r.json().get("data") or {}
print("conclusion:", d.get("conclusion"))
print("action_type:", d.get("action_type"))
print("positive_catalysts:", d.get("postive_catalysts"))
print("negative_catalysts:", d.get("negative_catalysts"))
PY
```

## 工具配置

| 工具 | 用途 |
|---|---|
| `curl` | 用于执行一次性的 GET 或 POST 请求 |
| `python3` / `requests` | 用于编写脚本；需先安装 `requests` 库 |

## 在 OpenClaw 中使用该技能

1. **启动一个新的 OpenClaw 会话**。
2. 使用相应的命令或脚本调用该技能。

## 免责声明与数据说明

- **免责声明**：该技能提供的数据和分析仅用于信息参考，不构成财务、投资或交易建议。过去的表现和模型预测并不能保证未来的结果。您需自行承担投资决策的全部责任；在做出财务决策前，请咨询专业顾问。
- **数据延迟**：API 提供的数据（价格、预测结果、分析内容）可能存在延迟，并非实时数据。请勿依赖这些数据进行需要即时响应的交易决策。
- **实时数据**：如需实时数据，请访问 [Intellectia](https://intellectia.ai/?channelId=601&activityId=1)。

## 注意事项

- **screener-public**：每次请求仅支持一个股票代码。
- **should-i-buy**：当用户询问“我应该买入某只股票吗？”时，请使用该功能，并在回答中提供分析结论及买入理由。