---
name: hash-health
description: 通过 Hash Health 记录饮食、检查营养状况、管理药物服用情况，并查看每日健康状况概览。当用户提及食物、餐食、饮食、营养、药物或健康追踪相关内容时，可使用该工具。
metadata: {"openclaw":{"emoji":"🥗","requires":{"env":["HASH_HEALTH_USER_ID"]}}}
---
您已连接到 Hash Health，这是一个用于个人营养和健康追踪的平台。

**基础 API 地址：** `https://hash-claude-mcp.vercel.app`  
**用户的电子邮件/ID：** `{HASH_health_USER_ID}`

## 工具：记录饮食**

要记录用户提到的食物，请按照以下步骤操作：

**步骤 1 — 分析食物**  
发送 POST 请求到：`https://hash-claude-mcp.vercel.app/api/food-analysis`  
```json
{
  "messages": [
    {
      "role": "user",
      "content": "{\"type\":\"analysis_request\",\"step\":\"analyze\",\"food_name\":\"<dish name>\",\"is_edited_food_name\":false,\"language\":\"en\"}"
    }
  ],
  "language": "en"
}
```

**步骤 2 — 保存到历史记录**  
发送 POST 请求到：`https://hash-claude-mcp.vercel.app/api/unified-history`  
```json
{
  "user_id": "{HASH_HEALTH_USER_ID}",
  "type": "analysis",
  "analysis": "<stringified analysis JSON from Step 1>"
}
```  
向用户确认：“✅ [菜肴名称] 已成功记录到 Hash Health！”  

## 工具：每日营养总结**  
发送 GET 请求到：`https://hash-claude-mcp.vercel.app/api/daily-nutrition?user_id={HASH_health_USER_ID}&date=<YYYY-MM-DD>`  
显示内容：卡路里、蛋白质、碳水化合物、脂肪、纤维等营养信息。

## 工具：查看当天的饮食记录**  
发送 GET 请求到：`https://hash-claude-mcp.vercel.app/api/unified-history?user_id={HASH_health_USER_ID}&date=<today YYYY-MM-DD>&limit=20`  
对于每条记录，解析 `analysis` 字段（该字段为 JSON 字符串），从中获取 `dishName` 和 `nutritionalInfo.calories_kcal`。  

## 工具：列出用药记录**  
发送 GET 请求到：`https://hash-claude-mcp.vercel.app/api/medi-history?user_id={HASH_health_USER_ID}`  
显示每种药物的名称、剂量、服用频率以及服用时间。

## 工具：添加用药记录**  
发送 POST 请求到：`https://hash-claude-mcp.vercel.app/api/medi-history`  
```json
{
  "user_id": "{HASH_HEALTH_USER_ID}",
  "name": "<medication name>",
  "dosage": "<e.g. 500mg>",
  "frequency": "<e.g. twice daily>",
  "time_of_day": ["morning", "evening"],
  "notes": ""
}
```

## 工具：删除饮食记录**  
发送 DELETE 请求到：`https://hash-claude-mcp.vercel.app/api/unified-history?id=<entry UUID>&user_id={HASH_health_USER_ID}`  
如果用户提供的是饮食名称而非 ID，请先发送 GET 请求 `https://hash-claude-mcp.vercel.app/api/unified-history` 以查找对应的记录 UUID。  

## 工具：删除用药记录**  
发送 DELETE 请求到：`https://hash-claude-mcp.vercel.app/api/medi-history?id=<numeric ID>&user_id={HASH_health_USER_ID}`  
如果用户提供的是药物名称而非 ID，请先发送 GET 请求 `https://hash-claude-mcp.vercel.app/api/medi-history` 以查找对应的药物 ID。  

## 工具：查看睡前用药记录**  
同时执行以下两个请求：  
- 发送 GET 请求到：`https://hash-claude-mcp.vercel.app/api/medi-history?user_id={HASH_health_USER_ID}`  
  筛选 `time_of_day` 包含 “bedtime” 或 “Bedtime” 的记录。  
- 发送 GET 请求到：`https://hash-claude-mcp.vercel.app/api/daily-nutrition?user_id={HASH_health_USER_ID}&date=<today>`  
显示睡前服用的药物以及当天的营养摄入总量。

**重要规则：**  
- 历史记录中的 `analysis` 字段始终为 JSON 字符串，在读取 `dishName`、`calories_kcal` 等信息之前请先对其进行解析。  
- 未指定日期时，始终使用当天的日期（格式为 YYYY-MM-DD）。  
- 切勿猜测药物的 ID 或 UUID — 请务必先进行查询。  
- 在记录饮食信息之前，请务必先与用户确认，先展示菜肴名称和预估的卡路里摄入量。