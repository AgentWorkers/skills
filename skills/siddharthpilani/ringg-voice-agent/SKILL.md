---
name: ringg-voice-agent
description: >
  Integrate Ringg AI voice agents with OpenClaw for making, receiving, and managing phone calls
  powered by Ringg's Voice OS. Use this skill when the user wants to: (1) make outbound voice calls
  via Ringg AI agents, (2) trigger Ringg AI campaigns from OpenClaw, (3) check call status or
  retrieve call history/analytics from Ringg, (4) manage Ringg AI assistants (list, create, update),
  (5) connect OpenClaw to Ringg's voice platform for automated phone interactions like lead
  qualification, feedback collection, appointment reminders, or order confirmations, (6) set up
  Ringg AI as a voice provider for the OpenClaw agent. Triggers on mentions of "ringg", "voice call",
  "phone call via ringg", "ringg agent", "ringg campaign", "voice AI call", or any request to
  initiate/manage calls through the Ringg AI platform.
---

# OpenClaw的Ringg语音代理技能

该技能将OpenClaw与[Ringg AI](https://www.ringg.ai)连接起来——Ringg AI是一款为企业设计的语音操作系统，提供低延迟（<337毫秒）、多语言（20多种语言）的语音代理服务，支持电话交互，包括潜在客户筛选、反馈收集、确认等操作。

## 先决条件

- 拥有具备API访问权限的Ringg AI账户
- 设置`RINGG_API_KEY`环境变量（从Ringg AI控制面板获取）
- 设置`RINGG_WORKSPACE_ID`环境变量
- 可选：设置`RINGG_DEFAULT_ASSISTANT_ID`以使用默认的语音代理
- 可选：设置`RINGG_DEFAULT_FROM_NUMBER`以指定呼出电话的号码

## 配置

将以下配置添加到`openclaw.json`文件中的`skills.entries`部分：

```json
{
  "skills": {
    "entries": {
      "ringg-voice-agent": {
        "enabled": true,
        "apiKey": "RINGG_API_KEY",
        "env": {
          "RINGG_API_KEY": "<your-ringg-api-key>",
          "RINGG_WORKSPACE_ID": "<your-workspace-id>",
          "RINGG_DEFAULT_ASSISTANT_ID": "<optional-default-assistant-id>",
          "RINGG_DEFAULT_FROM_NUMBER": "<optional-default-number>"
        }
      }
    }
  }
}
```

## 可用的操作

### 1. 发起呼出电话

使用Ringg AI代理拨打指定的电话号码。

```bash
# Basic outbound call
curl -X POST "https://api.ringg.ai/v1/calls/outbound" \
  -H "Authorization: Bearer $RINGG_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "assistant_id": "<assistant-id>",
    "to_number": "+919876543210",
    "from_number": "+918001234567",
    "dynamic_variables": {
      "customer_name": "Rahul",
      "order_id": "ORD-12345"
    }
  }'
```

**参数：**
- `assistant_id` — 要使用的语音代理的ID（默认使用`RINGG_DEFAULT_ASSISTANT_ID`）
- `to_number` — 目标电话号码（E.164格式）
- `from_number` — 主叫方号码（默认使用`RINGG_DEFAULT_FROM_NUMBER`）
- `dynamic_variables` — 传递给代理对话上下文的键值对

当用户输入“call +91XXXXXXXXXX”或“make a call to [name/number]”时，使用此操作。
如果未指定`assistant_id`，则使用`RINGG_DEFAULT_ASSISTANT_ID`；如果未指定`from_number`，则使用`RINGG_DEFAULT_FROM_NUMBER`。

### 2. 启动呼叫活动

批量拨打多个联系人的电话。

```bash
curl -X POST "https://api.ringg.ai/v1/campaigns/launch" \
  -H "Authorization: Bearer $RINGG_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "campaign_id": "<campaign-id>",
    "contacts": [
      {"phone": "+919876543210", "name": "Rahul", "custom_field": "value"},
      {"phone": "+919876543211", "name": "Priya", "custom_field": "value"}
    ]
  }'
```

当用户请求“launch a campaign”、“start calling a list”或“run outbound calls for [list/segment]”时，使用此操作。

### 3. 检查呼叫状态

```bash
curl -X GET "https://api.ringg.ai/v1/calls/{call_id}/status" \
  -H "Authorization: Bearer $RINGG_API_KEY"
```

返回呼叫状态（正在拨出、进行中、已完成、失败）、通话时长、通话记录摘要以及通话结果。

### 4. 获取通话记录与分析数据

```bash
# Recent call history
curl -X GET "https://api.ringg.ai/v1/calls/history?limit=20" \
  -H "Authorization: Bearer $RINGG_API_KEY"

# Analytics for a time range
curl -X GET "https://api.ringg.ai/v1/analytics?from=2026-02-01&to=2026-02-06" \
  -H "Authorization: Bearer $RINGG_API_KEY"
```

当用户询问“通话情况如何”、“显示通话分析数据”或“查看昨天的通话记录”时，使用这些功能。

### 5. 列出代理

```bash
curl -X GET "https://api.ringg.ai/v1/assistants" \
  -H "Authorization: Bearer $RINGG_API_KEY"
```

当用户询问“我有哪些代理？”或需要在拨打电话前选择代理时，使用此操作。

### 6. 获取通话记录

```bash
curl -X GET "https://api.ringg.ai/v1/calls/{call_id}/transcript" \
  -H "Authorization: Bearer $RINGG_API_KEY"
```

当用户询问“通话中说了什么”或“获取通话记录”时，使用此操作。

## Webhook集成（入站事件）

Ringg AI可以通过Webhook将实时通话事件推送到OpenClaw。要接收通话状态更新、通话记录和通话结果，需执行以下操作：

1. 暴露OpenClaw的Webhook端点：
   ```bash
   ngrok http 18789
   ```

2. 在Ringg AI控制面板或通过API配置Webhook URL：
   ```bash
   curl -X POST "https://api.ringg.ai/v1/webhooks" \
     -H "Authorization: Bearer $RINGG_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
       "url": "https://your-ngrok-url.ngrok.io/webhook/ringg",
       "events": ["call.completed", "call.failed", "call.transcript_ready"]
     }'
   ```

3. OpenClaw将接收到包含通话事件的POST请求，这些事件可以触发相应的代理操作。

## 使用模式

**用户指令 → 对应操作：**

| 用户指令 | 操作 |
|-----------|--------|
| “Call Rahul at +919876543210” | 使用默认代理发起呼出电话 |
| “Use the PolicyBazaar agent to call this lead” | 使用特定代理发起呼出电话 |
| “Launch the feedback campaign” | 启动反馈收集活动 |
| “How did the last 10 calls go?” | 查看最近10次通话的记录 |
| “Get the transcript for call XYZ” | 获取通话XYZ的记录 |
| “What agents do I have in Ringg?” | 列出所有代理 |
| “Show me today’s call analytics” | 查看今天的通话分析数据 |

## 错误处理

- **401 Unauthorized**：检查`RINGG_API_KEY`是否有效
- **404 Not Found**：确认`assistant_id`、`call_id`或`campaign_id`是否存在
- **429 Rate Limited**：等待指定时间后再重试
- **电话号码格式**：始终使用E.164格式（例如，印度地区的号码格式为+919876543210）

## API参考

有关完整的API详细信息，请参阅该技能目录下的`references/api_reference.md`文件，或访问[Ringg AI API文档](https://docs.ringg.ai)。