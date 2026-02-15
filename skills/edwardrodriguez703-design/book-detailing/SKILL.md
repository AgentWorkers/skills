---
name: book-detailing
description: **通过 Lokuli MCP 预订车辆保养服务的文档**  
本文档用于说明用户如何通过 Lokuli MCP 系统预订车辆保养服务。当用户输入诸如“预订保养服务”或“查找附近的保养服务”等请求时，该文档会触发相应的操作流程。  

**主要功能：**  
- **服务查找**：用户可以搜索可用的保养服务，包括服务类型、价格、地点等信息。  
- **服务预订**：用户可以选择所需的服务并完成预订流程，系统会自动生成预约确认信息。  
- **服务提醒**：系统会通过邮件或应用程序通知用户保养服务的具体时间、地点及相关注意事项。  

**使用步骤：**  
1. **登录 Lokuli MCP 系统**：使用您的用户名和密码登录到 Lokuli MCP 网站或应用程序。  
2. **搜索保养服务**：在首页或服务菜单中，输入关键词（如“汽车保养”或“轮胎更换”）进行搜索。  
3. **选择服务**：从搜索结果中选择您需要的保养服务，查看服务详情（价格、时间、地点等）。  
4. **填写预订信息**：根据系统提示，填写您的联系方式和车辆信息。  
5. **确认预订**：核对所有信息无误后，点击“预订”按钮。  
6. **接收确认邮件**：系统会发送一封确认邮件，其中包含预约的详细信息。  

**注意事项：**  
- 请确保您的车辆信息准确无误，以便系统能够顺利安排保养服务。  
- 如需取消或更改预约，请及时联系 Lokuli MCP 的客服团队。  

**常见问题解答：**  
- **如何更改预约时间？**  
  - 登录 Lokuli MCP 系统，进入您的个人账户，找到相应的预约记录，然后修改预约时间。  
- **如果找不到所需的服务怎么办？**  
  - 请尝试使用更具体的搜索关键词，或联系客服咨询。  

**技术支持：**  
如在使用过程中遇到任何技术问题，请访问 Lokuli MCP 的官方支持页面或联系技术支持团队。
---

# 书籍详情服务

通过 Lokuli 的 MCP 服务器提供书籍详情服务。

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
      "query": "detailing",
      "zipCode": "90640",
      "maxResults": 20
    }
  }
}
```

### 检查书籍可用性
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