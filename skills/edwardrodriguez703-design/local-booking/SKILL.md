---
name: local-booking
description: 通过 Lokuli MCP 预订现实世界中的服务。当用户需要查找、查询服务可用性或预订诸如水管工、电工、清洁工、机械师、理发师、私人教练等本地服务时，可以使用该功能。该功能会在用户发出“帮我预约理发”、“找附近的水管工”、“我需要检测烟雾浓度”或任何其他本地服务请求时触发。目前提供超过 75 种服务类别。
---

# 本地预订

通过 Lokuli 的 MCP 服务器预订真实的本地服务。

## MCP 端点

```
https://lokuli.com/mcp/sse
```

**传输协议**：SSE | JSON-RPC 2.0 | 使用 POST 请求

## 工具

### search
根据查询条件和位置查找服务。
```json
{
  "method": "tools/call",
  "params": {
    "name": "search",
    "arguments": {
      "query": "smog check",
      "zipCode": "90640",
      "category": "Auto Services",
      "maxResults": 20
    }
  }
}
```
- `query`（必填）：要搜索的内容
- `zipCode`：要搜索的邮政编码
- `category`：可选类别：汽车服务、音乐与音频、美容服务、健康与养生、纹身与身体艺术、技术维修、辅导与教育、家居服务、摄影与视频、活动
- `maxResults`：1-50 个结果，默认为 20 个

### fetch
获取提供者的详细信息。
```json
{
  "method": "tools/call",
  "params": {
    "name": "fetch",
    "arguments": {
      "id": "provider_id_from_search"
    }
  }
}
```

### check_availability
查询可用的时间段。
```json
{
  "method": "tools/call",
  "params": {
    "name": "check_availability",
    "arguments": {
      "providerId": "xxx",
      "serviceId": "yyy",
      "date": "2025-02-10"
    }
  }
}
```

### create_booking
预订服务并获取 Stripe 支付链接。
```json
{
  "method": "tools/call",
  "params": {
    "name": "create_booking",
    "arguments": {
      "providerId": "xxx",
      "serviceId": "yyy",
      "timeSlot": "2025-02-10T14:00:00-08:00",
      "customerName": "John Doe",
      "customerEmail": "john@example.com",
      "customerPhone": "+13105551234"
    }
  }
}
```
返回用于支付的 Stripe 结账页面链接。

### get_booking
查询预订状态。
```json
{
  "method": "tools/call",
  "params": {
    "name": "get_booking",
    "arguments": {
      "bookingId": "stripe_session_id"
    }
  }
}
```

### get_service_catalog
列出所有 75 种以上的服务类型。
```json
{
  "method": "tools/call",
  "params": {
    "name": "get_service_catalog",
    "arguments": {
      "category": "All"
    }
  }
}
```

### get_pricing_estimates
获取服务的典型价格信息。
```json
{
  "method": "tools/call",
  "params": {
    "name": "get_pricing_estimates",
    "arguments": {
      "serviceType": "smog check"
    }
  }
}
```

### validate_location
检查该邮政编码是否支持相关服务。

### create_cart
使用 JWT 签名的授权信息创建购物车（作为直接支付的替代方案）。
```json
{
  "method": "tools/call",
  "params": {
    "name": "create_cart",
    "arguments": {
      "shopId": "provider_id",
      "services": [
        {"sku": "service_id", "name": "Smog Check", "price": 39.99, "quantity": 1}
      ]
    }
  }
}
```

## 类别

- **汽车服务**：烟雾检测、换油、汽车保养、汽车维修、轮胎服务
- **音乐与音频**：录音室、音乐课程、DJ 服务
- **美容服务**：理发、美发沙龙、美甲、化妆服务
- **健康与养生**：按摩、脊椎按摩师服务、私人健身教练
- **纹身与身体艺术**：纹身、穿孔服务
- **技术维修**：手机维修、电脑维修
- **辅导与教育**：辅导服务、考试辅导、语言培训
- **家居服务**：水管维修、电工服务、暖通空调维修、清洁服务
- **摄影与视频**：摄影服务、视频制作服务
- **活动**：餐饮服务、活动策划服务

## 工作流程

1. **了解需求**：需要哪种服务？在哪个地点（邮政编码）？
2. **搜索**：查找符合条件的服务提供者
3. **展示结果**：显示包含价格的顶级服务选项
4. **获取详情**：获取所选提供者的详细信息
5. **查询可用时间**：查询可用的时间段
6. **确认预订**：获取用户的明确同意
7. **创建预订**：生成 Stripe 结账页面
8. **分享链接**：用户完成支付

## 规则

- **未经确认切勿预订**：务必获得用户的明确同意
- **提前显示价格**：如有需要，使用 `get_pricing_estimates` 功能
- **收集必要信息**：预订前需收集用户的姓名、电子邮件和电话号码
- **默认使用用户的邮政编码**：如果上下文明确提供了用户地址，则使用该地址