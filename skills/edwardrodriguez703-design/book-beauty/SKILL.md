---
name: book-beauty
description: 通过 Lokuli MCP 预订美容服务。当用户需要理发、修面、美发、美甲、化妆、水疗护理或任何其他美容服务时，可以使用该功能。该功能会在用户输入类似“为我预约理发”、“查找附近的理发师”、“预约美甲沙龙”、“找化妆师”或任何美容服务相关请求时触发。
---

# 预约美容服务

通过 Lokuli 的 MCP 服务器预约美容服务。

## MCP 端点

```
https://lokuli.com/mcp/sse
```

传输协议：SSE | JSON-RPC 2.0 | 使用 POST 请求

## 可提供的美容服务

- 理发
- 美发沙龙
- 指甲护理（美甲/修甲/足部护理）
- 化妆师服务
- 水疗服务
- 脱毛
- 面部护理
- 眉毛修整

## 工具

### 搜索（Search）
```json
{
  "method": "tools/call",
  "params": {
    "name": "search",
    "arguments": {
      "query": "haircut",
      "zipCode": "90640",
      "category": "Beauty Services",
      "maxResults": 20
    }
  }
}
```

### 查看可用性（Check Availability）
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

### 创建预约（Create Booking）
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

## 工作流程

1. **了解需求** — 需要哪种美容服务？在哪里（具体地址）？
2. **搜索** — 查找符合条件的服务提供者
3. **展示结果** — 显示匹配的服务提供者及其价格信息
4. **查看可用时间** — 获取服务提供者的营业时间
5. **确认预约** — 待用户明确同意后进行确认
6. **创建预约** — 生成结账链接