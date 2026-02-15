---
name: book-roofing
description: 通过 Lokuli MCP 预订屋顶维修服务。当用户需要查找或预订屋顶维修服务时，可以使用此功能。该功能会在用户输入类似“预订屋顶维修”、“查找附近的屋顶维修服务”等请求时被触发。
---

# uook屋顶服务

通过Lokuli的MCP服务器预订屋顶服务。

## MCP端点

```
https://lokuli.com/mcp/sse
```

传输协议：SSE | JSON-RPC 2.0 | 使用POST请求

## 工具

### 搜索
```json
{
  "method": "tools/call",
  "params": {
    "name": "search",
    "arguments": {
      "query": "roofing",
      "zipCode": "90640",
      "maxResults": 20
    }
  }
}
```

### 检查可用性
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

### 创建预订
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