---
name: book-chiropractor
description: 通过 Lokuli MCP 预约脊椎按摩师服务。当用户需要寻找或预约脊椎按摩师时，可以使用此功能。该功能会在用户输入类似“预约脊椎按摩师”、“查找附近的脊椎按摩师”或任何与脊椎按摩师服务相关的请求时被触发。
---

# 预约脊椎按摩师服务

您可以通过 Lokuli 的 MCP 服务器预约脊椎按摩师服务。

## MCP 端点

```
https://lokuli.com/mcp/sse
```

传输协议：SSE | JSON-RPC 2.0 | 使用 POST 请求

## 工具

### 搜索
```json
{
  "method": "tools/call",
  "params": {
    "name": "search",
    "arguments": {
      "query": "chiropractor",
      "zipCode": "90640",
      "maxResults": 20
    }
  }
}
```

### 查询可用性
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

### 创建预约
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