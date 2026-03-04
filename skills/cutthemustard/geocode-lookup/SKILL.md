---
name: geocode-lookup
description: **前向/反向地理编码以及大圆距离计算**
version: 1.0.0
metadata:
  openclaw:
    emoji: "📍"
    homepage: https://geocode.agentutil.net
    always: false
---
# 地理编码服务

提供地址到坐标的转换（正向地理编码）、坐标到地址的转换（反向地理编码）以及哈弗辛距离（Haversine distance）的计算功能。

## 数据处理

该服务会将地址和坐标数据发送到外部API。未经用户明确同意，严禁发送包含私人信息的地址。服务仅会存储和处理用于生成响应的数据，不会长期保存或记录输入数据。

## 接口端点

### 正向地理编码

```bash
curl -X POST https://geocode.agentutil.net/v1/forward \
  -H "Content-Type: application/json" \
  -d '{"address": "Auckland, New Zealand"}'
```

可选参数：`limit`（1-5，默认值为1）。

### 反向地理编码

```bash
curl -X POST https://geocode.agentutil.net/v1/reverse \
  -H "Content-Type: application/json" \
  -d '{"lat": -36.8485, "lon": 174.7633}'
```

### 距离计算

```bash
curl -X POST https://geocode.agentutil.net/v1/distance \
  -H "Content-Type: application/json" \
  -d '{"from": {"address": "London, UK"}, "to": {"address": "New York, US"}, "unit": "km"}'
```

距离单位：km、mi、m、nm。支持以下两种输入格式：`{lat, lon}` 或 `{address}`。

## 响应格式

```json
{
  "results": [
    {"lat": -36.8485, "lon": 174.7633, "display_name": "Auckland, New Zealand", "type": "city"}
  ],
  "request_id": "abc-123",
  "service": "https://geocode.agentutil.net"
}
```

## 价格政策

- 免费 tier：每天10次查询，无需身份验证。
- 付费 tier：每次查询费用为0.001美元，通过x402协议支付（货币单位：Base上的USDC）。

## 隐私政策

免费 tier无需身份验证，不会收集任何个人数据。速率限制仅通过IP地址进行实现。