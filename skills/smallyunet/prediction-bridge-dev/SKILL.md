---
name: prediction-bridge-search
description: 通过后端API，可以根据文本或X（Twitter）链接来搜索Search Prediction Bridge平台上的预测市场事件。
homepage: https://www.predictionbridge.xyz
metadata: {"openclaw":{"skillKey":"prediction-bridge-search","homepage":"https://www.predictionbridge.xyz","requires":{"bins":["curl"]}}}
---

**使用说明：**  
当用户需要查找与以下内容相关的预测市场/事件时，请使用此技能：  
- 简短文本查询（主题、问题、标题）  
- 文章的URL  
- X（Twitter）状态链接（后端会解析并提取推文内容）  

**使用场景：**  
当用户提出以下请求时，请使用此技能：  
- “查找与这个主题/标题相关的预测市场”  
- “哪些市场与这条推文/X链接相关？”  
- “在Polymarket/Kalshi中搜索关于……的事件”  

**适用场景：**  
- 将非结构化文本（或X链接）转换为排名靠前的、可操作的事件链接  
- 快速显示前5-10个匹配结果，并提供每个市场的简要信息  

**不适用场景：**  
- 用户需要查看完整的市场订单簿或历史数据（请使用市场数据端点）  
- 需要深入分析市场情绪或时间线（请使用事件深度分析端点）  

**技术原理：**  
此技能会调用现有的`Prediction Bridge`后端端点：`POST /api/v1/search/unified`。  

**返回数据：**  
该请求返回匹配到的`events`（预测市场事件）以及可选的`news`（相关新闻）。  

**配置参数：**  
- **API地址**（默认为生产环境）：`PREDICTION_BRIDGE_API_URL`  
  - 生产环境：`https://prediction-bridge.onrender.com/api/v1`  
  - 本地开发环境（如果后端运行在本地）：`http://localhost:8000/api/v1`  

**使用步骤：**  
1. **构建查询内容**：  
   - 如果用户提供了X状态链接，直接将其作为`text`参数传递；后端会自动解析该链接。  
   - 如果用户提供了纯文本，直接传递该文本。  

2. **执行搜索**：  
   使用`curl`命令执行`exec`操作：  

**注意事项：**  
- 设置`markets_per_event: 1`以减小数据量，同时仍能显示主要的市场信息。  
- 如果用户需要查看更多市场信息，可增加`markets_per_event`的值。  

**API响应格式：**  
`POST /search/unified`返回的JSON数据结构如下（部分字段可能根据数据可用性而缺失或为`null`）：  

```json
{
  "events": [
    {
      "score": 0.82,
      "event": {
        "source_url": "https://www.polymarket.com/event/12345",
        "markets": [
          {
            "name": "Polymarket",
            "outcome_prices": {
              "Yes": 100.0,
              "Long": 95.0
            }
          }
        }
      }
    },
    // ...
  ],
  "news": [
    // ...
  ]
}
```

**结果处理方式：**  
1. **不要直接显示原始JSON响应**：  
   - 必须先解析和验证响应内容，再以易于阅读的形式展示匹配到的事件。  
2. **排序和筛选结果**：  
   - 按`score`降序排列结果（即使后端已经进行了排序）。  
   - 默认显示前5个结果；如用户请求更多结果，则显示前10个。  
3. **提取市场信息**：  
   - 优先使用`event.source_url`作为点击链接；如果缺失，则使用前端详情页链接（`https://www.predictionbridge.xyz/event/<event.id>`）。  
   - 如果`event.markets[0].outcome_prices`存在，显示“YES/Long”价格；否则显示第一个可用的价格。  
4. **简洁展示结果**：  
   - 包括事件标题、来源/平台、相关性得分（四舍五入显示）、链接以及市场概要（概率和成交量/流动性）。  
5. **可选：显示相关新闻**：  
   - 如果有相关新闻，最多展示1-3条，包含标题和链接作为补充信息。  
6. **处理空结果**：  
   - 如果没有匹配结果，说明未找到相关内容；可要求用户提供更具体的查询条件。  

**错误处理：**  
- **HTTP 400**：输入无效或链接解析错误 → 请用户提供新的链接或纯文本。  
- **HTTP 503**：后端数据库不可用 → 建议稍后重试。  
- **网络错误**：确认`PREDICTION_BRIDGE_API_URL`是否可访问。