---
name: book-laundry
description: 通过 Lokuli MCP 预订洗衣服务。当用户需要查找或预订洗衣服务时，可以使用该功能。该功能会在用户输入“预订洗衣服务”、“查找附近的洗衣店”或任何与洗衣服务相关的请求时被触发。
---

# 使用Lokuli的MCP服务器预订洗衣服务

通过Lokuli的MCP服务器来预订洗衣服务。

## MCP端点（MCP Endpoint）

```
https://lokuli.com/mcp/sse
```

**传输协议（Transport Protocol）：** SSE | JSON-RPC 2.0 | 使用POST请求

## 工具（Tools）

### 搜索（Search）  
```json
{
  "method": "tools/call",
  "params": {
    "name": "search",
    "arguments": {
      "query": "laundry",
      "zipCode": "90640",
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