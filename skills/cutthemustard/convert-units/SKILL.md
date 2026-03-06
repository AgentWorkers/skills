---
name: unit-convert
description: 在各种格式之间转换货币、物理单位和编码。
version: 1.0.0
metadata:
  openclaw:
    emoji: "🔄"
    homepage: https://convert.agentutil.net
    always: false
---
# unit-convert

该服务支持货币转换（实时汇率）、物理单位转换（涵盖8个类别的80多种单位）以及编码转换（base64、hex、URL）。

## 端点（Endpoints）

### 货币转换（Currency Conversion）

```bash
curl -X POST https://convert.agentutil.net/v1/currency \
  -H "Content-Type: application/json" \
  -d '{"value": 100, "from": "USD", "to": "NZD"}'
```

### 单位转换（Unit Conversion）

```bash
curl -X POST https://convert.agentutil.net/v1/units \
  -H "Content-Type: application/json" \
  -d '{"value": 1, "from": "mi", "to": "km"}'
```

支持的类别包括：长度、重量、体积、面积、速度、数据、时间、温度。

### 编码转换（Encoding Conversion）

```bash
curl -X POST https://convert.agentutil.net/v1/encoding \
  -H "Content-Type: application/json" \
  -d '{"input": "hello", "from": "utf8", "to": "base64"}'
```

支持的编码格式：utf8、base64、hex、url。

## 响应格式（Response Format）

```json
{
  "result": 1.609344,
  "from": "mi",
  "to": "km",
  "value": 1,
  "formula": "1 mi = 1.609344 km",
  "request_id": "abc-123",
  "service": "https://convert.agentutil.net"
}
```

## 价格（Pricing）

- 免费 tier：每天10次查询，无需身份验证
- 付费 tier：通过x402协议每次查询0.001美元（基于Base货币，使用USDC）

## 隐私政策（Privacy）

免费 tier无需身份验证，不会收集任何个人数据。速率限制仅使用IP哈希技术进行控制。