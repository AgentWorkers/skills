---
name: hume-evi-langgraph
description: 将 Hume EVI 语音 AI 与 LangGraph 集成，使用中断/恢复（interrupt/resume）模式。适用于构建需要处理 Twilio 呼叫、创建 Hume EVI 人物角色、获取带有情感分析的通话记录以及在整个通话生命周期中管理 LangGraph 状态的语音 AI 代理。内容包括动态配置 Hume 参数、生成 TwiML 代码、处理 Webhook 事件、获取聊天组信息以及提取情感时间线等功能。
---
# Hume EVI 与 LangGraph 的集成

## 架构

使用单一的 LangGraph StateGraph，并支持中断/恢复功能：

```
receive_call → verify_pin → select_persona → create_hume_config → generate_twiml
    → await_call_end [INTERRUPT] → fetch_transcript → analyze → coach → store → END
```

中断边界用于区分调用前的同步状态和调用后的异步状态（由 webhook 触发）。

## 关键模式

### 1. 异步调用的中断/恢复机制

```python
from langgraph.types import interrupt, Command

def await_call_end(state):
    resume_data = interrupt({"reason": "waiting_for_webhook"})
    return {**state, "chat_id": resume_data["chat_id"]}

# In webhook handler:
graph.invoke(Command(resume={"chat_id": "xxx"}), config)
```

### 2. Hume 配置的创建

每次调用时都会创建动态的 EVI 配置。将温度设置为较低值（0.6），以防止系统过于活跃：

```python
request_body = {
    "evi_version": "3",
    "name": f"Session-{persona_name}-{timestamp}",
    "prompt": {"text": voice_prompt},
    "voice": {"provider": "HUME_AI", "name": "KORA"},  # or "ITO" for male
    "language_model": {
        "model_provider": "OPEN_AI",
        "model_resource": "gpt-4o-mini",
        "temperature": 0.6,  # CRITICAL: default is too warm/eager
    },
    "event_messages": {"on_new_chat": {"enabled": True, "text": first_message}},
    "webhooks": [{"events": ["chat_ended"], "url": webhook_url}],
}
resp = httpx.post("https://api.hume.ai/v0/evi/configs", json=request_body, headers=headers)
```

### 3. TwiML 重定向（非数据流传输）

在 XML 格式中，应使用 `&` 而不是 `&` 符号：

```python
twiml = f'''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Matthew">Connecting now.</Say>
    <Redirect>https://api.hume.ai/v0/evi/twilio?config_id={config_id}&amp;api_key={api_key}</Redirect>
</Response>'''
```

### 4. 转录内容的获取（⚠️ 已知问题区域）

Hume 的 `/chats/{id}/events` 端点会返回 404 错误。必须使用 `chat_groups` 来获取数据：

```python
# Step 1: Get chat_group_id
chat_resp = httpx.get(f"https://api.hume.ai/v0/evi/chats/{chat_id}", headers=headers)
chat_group_id = chat_resp.json().get("chat_group_id")

# Step 2: Fetch events via chat_group
events_resp = httpx.get(
    f"https://api.hume.ai/v0/evi/chat_groups/{chat_group_id}/events",
    headers=headers, params={"page_size": 100}
)
events = events_resp.json().get("events_page", [])
```

字段名采用 **snake_case** 格式：`message_text`、`emotion_features`（而非 `messageText`）。

### 5. 情感提取

```python
for msg in messages:
    ef = msg.get("emotion_features")  # dict of ~48 emotions with float scores
    if ef and msg.get("role") == "USER":  # USER = the human caller
        top = sorted(ef.items(), key=lambda x: x[1], reverse=True)[:5]
        emotion_timeline.append({"turn": n, "text": text, "top_emotions": dict(top)})
```

### 6. Webhook 会话的解析

Hume 的 `chat_ended` webhook 不会包含 `call_sid` 参数。需要使用 `config_id` 来进行会话的识别：

```python
config_to_thread: dict[str, str] = {}  # hume_config_id → langgraph_thread_id

# On config creation:
config_to_thread[config_id] = thread_id

# On webhook:
thread_id = config_to_thread.pop(body["config_id"])
```

## 预防措施

有关完整的错误记录和预防措施，请参阅 `references/bug-prevention.md` 文件。