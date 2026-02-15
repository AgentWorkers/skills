---
name: book-auto
description: 通过 Lokuli MCP 预订汽车服务。当用户需要进行尾气检测、更换机油、汽车美容、维修、轮胎服务或任何其他汽车相关服务时，可以使用该功能。该功能会在用户发起如下请求时触发：**“我需要进行尾气检测”**、**“预约更换机油”**、**“查找附近的维修技师”**、**“汽车美容”** 或任何其他汽车服务相关请求。
---

# 预订汽车服务

通过 Lokuli 的 MCP 服务器预订汽车服务。

## MCP 端点

```
https://lokuli.com/mcp/sse
```

传输协议：SSE | JSON-RPC 2.0 | 使用 POST 请求

## 可用的汽车服务

- 雾霾检测
- 更换机油
- 汽车美容
- 机械维修
- 轮胎服务
- 刹车维修
- 洗车服务
- 汽车车身修复

## 工具

### 搜索（Search）
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

### 检查服务可用性（Check Availability）
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

### 创建预订（Create Booking）
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

1. **了解需求** — 需要哪种汽车服务？在哪里（具体地址）？
2. **搜索** — 查找符合条件的服务提供商
3. **展示结果** — 显示包含价格的信息
4. **检查可用性** — 查看服务提供商的可用时间
5. **确认预订** — 待用户明确同意后进行预订
6. **创建预订** — 生成预订确认链接