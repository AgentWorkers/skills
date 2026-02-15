---
name: intellectia-stock-screener
description: 从Intellectia API获取股票筛选器列表数据（无需认证），并汇总结果。
metadata: {"openclaw":{"requires":{"bins":["curl","python3"]},"install":[{"id":"python","kind":"pip","package":"requests","bins":[],"label":"Install requests (pip)"}]}}
---

# Intellectia 股票筛选器

基础 URL：`https://api.intellectia.ai`

## 端点

- `GET /gateway/v1/stock/screener-list`

完整 URL：
- `https://api.intellectia.ai/gateway/v1/stock/screener-list`

## 查询参数

- `symbol_type` (int)：资产类型  
  - `0` = 股票  
  - `1` = ETF  
  - `2` = 加密货币  
- `period_type` (int)：时间周期  
  - `0` = 每日  
  - `1` = 每周  
  - `2` = 每月  
- `trend_type` (int)：趋势类型  
  - `0` = 上涨  
  - `1` = 下跌  
- `profit_asc` (bool)：是否按利润升序排序（`true` 表示从小到大）  
- `market_cap` (int)：市值筛选条件  
  - `0` = 任意  
  - `1` = 微型（<3亿美元）  
  - `2` = 小型（3亿–20亿美元）  
  - `3` = 中型（20亿–100亿美元）  
  - `4` = 大型（100亿–200亿美元）  
  - `5` = 巨型（>200亿美元）  
- `price` (int)：价格筛选条件  
  - `0` = 任意  
  - `1` = <5美元  
  - `2` = <50美元  
  - `3` => 5美元  
  - `4` => 50美元  
  - `5` = 5–50美元  
- `page` (int)：页码（例如：1）  
- `size` (int)：每页显示的记录数（例如：20条）

## 响应（200条记录）

示例响应结构：

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

### 字段说明

- **顶级字段**：  
  - `ret` (int)：状态码（通常 `0` 表示成功）  
  - `msg` (string)：消息（成功时为空字符串）  
  - `data` (object)：数据负载  

- **data**：  
  - `data.list` (array)：结果行  
  - `data.total` (int)：总记录数  
  - `data.detail` (object)：筛选器元数据  

- **data.list` 中的每条记录包含以下字段：**  
  - `code` (string)：完整证券代码（可能包含交易所后缀，例如 `BKD.N`）  
  - `symbol` (string)：股票代码（例如 `BKD`）  
  - `symbol_type` (int)：资产类型  
  - `name` (string)：显示名称  
  - `logo` (string)：标志图片 URL  
  - `pre_close` (number)：前收盘价  
  - `price` (number)：当前价格  
  - `change_ratio` (number)：相对于前收盘价的百分比变化  
  - `timestamp` (string)：报价时间戳（Unix 秒）  
  - `similarity_num` (int)：相似度计数（由 API 返回；保持原样）  
  - `probability` (int)：模型置信度（0–100）  
  - `profit` (number)：预测/预期回报（由 API 返回）  
  - `klines` (array)：价格序列  
    - `klines[].close` (number)：收盘价  
    - `klines[].timestamp` (string)：时间戳（Unix 秒）  
  - `trend_list` (array)：趋势对比序列  
    - `trend_list[].symbol` (string)：序列对应的证券代码（非主要序列可能为空）  
    - `trend_list[].symbol_type` (int)：资产类型  
    - `trend_list[].is_main` (bool)：是否为主要序列  
    - `trend_list[].list` (array)：时间点  
      - `trend_list[].list[].change_ratio` (number)：该时间点的百分比变化  
      - `trend_list[].list[].timestamp` (string)：时间戳（Unix 秒）  
      - `trend_list[].list[].close` (number)：该时间点的收盘价  
  - `update_time` (string)：最后更新时间（Unix 秒）  

- **data.detail**：  
  - `cover_url` (string)：封面图片 URL  
  - `name` (string)：筛选器名称  
  - `screener_type` (int)：筛选器类型 ID  
  - `params` (string)：序列化的参数（通常为 JSON 字符串）  
  - `desc` (string)：筛选器描述  
  - `num` (int，可选）：由 API 返回的计数（可能不存在）

## 示例

### 使用 cURL 请求

```bash
curl -sS "https://api.intellectia.ai/gateway/v1/stock/screener-list?symbol_type=0&period_type=0&trend_type=0&profit_asc=false&market_cap=0&price=0&page=1&size=20"
```

### 使用 Python (requests) 请求

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

## 注意事项：  
- 无需身份验证。  
- 如果遇到请求限制，请减少 `size` 值，并在客户端代码中添加重试机制。