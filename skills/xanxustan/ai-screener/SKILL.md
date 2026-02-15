---
name: intellectia-stock-screener
description: Intellectia股票/加密货币筛选器，支持设置“明日/本周/本月看涨/看跌”的预设条件。通过调用 `/gateway/v1/stock/screener-list`（无需认证）来执行筛选，并汇总筛选结果。
metadata: {"openclaw":{"requires":{"bins":["curl","python3"]},"install":[{"id":"python","kind":"pip","package":"requests","bins":[],"label":"Install requests (pip)"}]}}
---

# Intellectia 股票筛选器

用于获取并汇总 Intellectia 的股票/加密货币筛选结果。

## 何时使用此功能

当您需要以下操作时，请使用此功能：
- 获取最新的 **看涨/看跌** 筛选结果（针对股票或加密货币）
- 使用内置的 **预设筛选列表** 作为股票/加密货币的挑选工具
- 将预设筛选条件转换为精确的 API 查询参数（`symbol_type`、`period_type`、`trend_type`）
- 使用 `probability`、`profit`、`price`、`change_ratio`、`klines` 和 `trend_list` 来汇总或比较筛选结果

## 预设筛选条件（UI 列表对应关系）

选择一个预设名称并运行它（这是使用该功能的最简单方法）：

| 预设名称（UI 名称） | `symbol_type` | `period_type` | `trend_type` |
|---|---|---|---:|
| 明天看涨的股票 | 0 | 0 | 0 |
| 明天看跌的股票 | 0 | 0 | 1 |
| 本周看涨的股票 | 0 | 1 | 0 |
| 本周看跌的股票 | 0 | 1 | 1 |
| 本月看涨的股票 | 0 | 2 | 0 |
| 本月看跌的股票 | 0 | 2 | 1 |
| 明天看涨的加密货币 | 2 | 0 | 0 |
| 明天看跌的加密货币 | 2 | 0 | 1 |
| 本周看涨的加密货币 | 2 | 1 | 0 |
| 本周看跌的加密货币 | 2 | 1 | 1 |
| 本月看涨的加密货币 | 2 | 2 | 0 |
| 本月看跌的加密货币 | 2 | 2 | 1 |

### 预设筛选条件说明（可直接复制使用）

- **明天看涨的股票**：此列表会显示根据 AI 算法预测会上涨的股票。该算法通过分析市场整体价格数据，找出那些最有可能延续上涨趋势的股票（基于已验证的看涨模式）。
- **明天看跌的股票**：此列表会显示根据 AI 算法预测会下跌的股票。该算法通过分析市场整体价格数据，找出那些最有可能延续下跌趋势的股票（基于已验证的看跌模式）。

## 如何使用（高命中率）

如果您希望 OpenClaw 自动执行此功能，请包含以下信息：
- `Intellectia` 或 `screener`（或 “看涨/看跌”、“股票筛选器”、“加密货币筛选器”）
- 上述表格中的一个 **预设名称**
- 您的输出要求（例如：前 N 个结果、排序方式、需要显示的字段）

如果您希望强制执行此功能，请使用以下命令：
- `/skill intellectia-stock-screener <您的请求>`

示例请求：
- “Intellectia 筛选器：**明天看涨的股票**。按 `probability` 降序排列，前 10 个结果。输出格式：`symbol, name, price, change_ratio, probability, profit`。”
- “Intellectia 筛选器：**本周看涨的股票**。解释 `probability` 和 `profit` 的含义，然后返回一个表格。”
- “Intellectia 筛选器：**本月看涨的加密货币**。显示第 1 页，每页 50 个结果。筛选条件：`probability >= 70`。”

## 工具配置

| 工具 | 用途 | 配置方式 |
|---|---|---|
| `curl` | 一次性快速请求 | 使用完整的 URL 和查询字符串 |
| `python3` | 可重复使用的脚本 | 使用 `requests` 库并解析返回的数据 |
| `requests` | HTTP 客户端库 | 需先安装 `pip install requests` |

## 在 OpenClaw 中使用此功能

1. 将相关代码安装到当前工作区中：
```bash
clawhub install intellectia-stock-screener
```

2. 启动一个新的 **OpenClaw 会话**，以便代理能够识别并执行此功能（技能会在会话开始时被加载）。
3. 确认该功能是否可用/符合使用要求：
```bash
openclaw skills list
openclaw skills info intellectia-stock-screener
openclaw skills check
```

## API 端点

- 基本 URL：`https://api.intellectia.ai`
- 请求路径：`GET /gateway/v1/stock/screener-list`

## 查询参数

| 参数名称 | 类型 | 含义 |
|---|---|---|
| `symbol_type` | int | 资产类型：`0=股票`、`1=ETF`、`2=加密货币` |
| `period_type` | int | 时间周期：`0=每天`、`1=每周`、`2=每月` |
| `trend_type` | int | 趋势类型：`0=看涨`、`1=看跌` |
| `profit_asc` | bool | 是否按利润升序排序（`true` 表示从小到大排序） |
| `market_cap` | int | 市值筛选条件：`0=任意`、`1=微型（<3亿美元）`、`2=小型（3亿-20亿美元）`、`3=中型（20亿-100亿美元）`、`4=大型（100亿-200亿美元）`、`5=巨型（>200亿美元）` |
| `price` | int | 价格筛选条件：`0=任意`、`1=<5`、`2=<50`、`3=>5`、`4=>50`、`5=5-50` |
| `page` | int | 页码（示例：1） |
| `size` | int | 每页显示的数量（示例：20） |

## 响应数据（示例结构）

```json
{
  "ret": 0,
  "msg": "",
  "data": {
    "list": [
      {
        "code": "BKD.N",
        "symbol": "BKD",
        "symbol_type": 0,
        "name": "Brookdale Senior Living Inc",
        "logo": "https://intellectia-public-documents.s3.amazonaws.com/image/logo/BKD_logo.png",
        "pre_close": 14.5,
        "price": 15,
        "change_ratio": 3.45,
        "timestamp": "1769749200",
        "simiar_num": 10,
        "probability": 80,
        "profit": 5.27,
        "klines": [{ "close": 15, "timestamp": "1769749200" }],
        "trend_list": [
          {
            "symbol": "BKD",
            "symbol_type": 0,
            "is_main": true,
            "list": [{ "change_ratio": 5.27, "timestamp": "1730260800", "close": 16 }]
          }
        ],
        "update_time": "1769806800"
      }
    ],
    "total": 3,
    "detail": {
      "cover_url": "https://d159e3ysga2l0q.cloudfront.net/image/cover_image/stock-1.png",
      "name": "Stocks Bullish Tomorrow",
      "screener_type": 1011,
      "params": "{}",
      "desc": "..."
    }
  }
}
```

### 数据字段说明

- `ret`（整数）：状态码（通常 `0` 表示成功）
- `msg`（字符串）：消息（成功时为空字符串）
- `data`（对象）：返回的数据

`data` 对象包含以下内容：
- `data.list`（数组）：筛选结果行
- `data.total`（整数）：总行数
- `data.detail`（对象）：筛选器元数据

`data.list` 中的每一项包含以下字段：
- `code`（字符串）：完整证券代码（可能包含交易所后缀，例如 `BKD.N`）
- `symbol`（字符串）：证券代码
- `symbol_type`（整数）：资产类型（`0=股票`、`1=ETF`、`2=加密货币`
- `name`（字符串）：显示名称
- `logo`（字符串）：图标 URL
- `pre_close`（数字）：前收盘价
- `price`（数字）：当前价格
- `change_ratio`（数字）：相对于前收盘价的百分比变化
- `timestamp`（字符串）：报价时间戳（Unix 秒）
- `similar_num`（整数）：相似度计数（由 API 返回，保持原样）
- `probability`（整数）：模型置信度（0-100）
- `profit`（数字）：预测/预期回报（由 API 返回）
- `klines`（数组）：价格序列
  - `klines[].close`（数字）：收盘价
  - `klines[].timestamp`（字符串）：时间戳（Unix 秒）
- `trend_list`（数组）：趋势对比序列
  - `trend_list[].symbol`（字符串）：序列对应的证券代码（非主要序列可能为空）
  - `trend_list[].symbol_type`（整数）：资产类型
  - `trend_list[].is_main`（布尔值）：是否为主要序列
  - `trend_list[].list`（数组）：时间点信息
    - `trend_list[].list[].change_ratio`（数字）：该时间点的百分比变化
    - `trend_list[].list[].timestamp`（字符串）：时间戳（Unix 秒）
    - `trend_list[].list[].close`（数字）：该时间点的收盘价
- `update_time`（字符串）：最后更新时间（Unix 秒）

`data.detail` 包含以下字段：
- `cover_url`（字符串）：封面图片 URL
- `name`（字符串）：筛选器名称
- `screener_type`（整数）：筛选器类型 ID
- `params`（字符串）：序列化的参数（通常为 JSON 格式）
- `desc`（字符串）：筛选器描述
- `num`（整数，可选）：由 API 返回（可能不存在）

## 示例请求方式

### 使用 cURL

```bash
curl -sS "https://api.intellectia.ai/gateway/v1/stock/screener-list?symbol_type=0&period_type=0&trend_type=0&profit_asc=false&market_cap=0&price=0&page=1&size=20"
```

### 使用 Python 和 `requests` 库

```bash
python3 - <<'PY'
import requests

base_url = "https://api.intellectia.ai"
params = {
  "symbol_type": 0,
  "period_type": 0,
  "trend_type": 0,
  "profit_asc": False,
  "market_cap": 0,
  "price": 0,
  "page": 1,
  "size": 20,
}

r = requests.get(f"{base_url}/gateway/v1/stock/screener-list", params=params, timeout=30)
r.raise_for_status()
payload = r.json()

print("ret:", payload.get("ret"))
print("msg:", payload.get("msg"))
data = payload.get("data") or {}
rows = data.get("list") or []
print("total:", data.get("total"))
for row in rows[:10]:
  print(row.get("symbol"), row.get("price"), row.get("change_ratio"), row.get("probability"), row.get("profit"))
PY
```

## 注意事项

- 无需身份验证。
- 如果遇到请求限制，请减少每次请求的数据量，并在客户端代码中添加重试机制。