---
name: book-smog
description: 通过 Lokuli MCP 预约车辆尾气检测服务。当用户需要进行尾气检测、排放测试或车辆检查时，请使用此功能。该功能会在收到如下请求时触发：**“我需要进行尾气检测”**、**“预约尾气测试”**、**“排放检测”**、**“车辆管理局（DMV）要求的尾气检测”**，或任何与尾气检测相关的请求。
---

# 书籍污染检测服务

您可以通过 Lokuli 的 MCP 服务器预约书籍污染检测服务。

## MCP 端点

```
https://lokuli.com/mcp/sse
```

传输协议：SSE | JSON-RPC 2.0 | 使用 POST 请求

## 可用的污染检测服务：
- 污染检测服务
- 仅限污染测试
- 星级认证的污染检测服务
- 柴油车污染检测服务
- 严重污染源认证服务
- 车辆所有权变更时的污染检测服务

## 工具：
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

### 检查可用性（Check Availability）
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

## 工作流程：
1. **了解需求**：确定所需的污染检测类型及检测地点（需提供 ZIP 地址）。
2. **搜索**：查找附近的污染检测站点。
3. **查看结果**：显示搜索结果及对应的费用信息。
4. **检查可用性**：确认检测站点的开放时间。
5. **获取用户确认**：等待用户的明确授权或确认。
6. **创建预约**：生成预约确认链接。