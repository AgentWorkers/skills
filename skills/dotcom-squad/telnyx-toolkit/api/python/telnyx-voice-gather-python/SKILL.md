---
name: telnyx-voice-gather-python
description: >-
  Collect DTMF input and speech from callers using standard gather or AI-powered
  gather. Build interactive voice menus and AI voice assistants. This skill
  provides Python SDK examples.
metadata:
  author: telnyx
  product: voice-gather
  language: python
  generated_by: telnyx-ext-skills-generator
---

<!-- 本文档由 Telnyx OpenAPI 规范自动生成，请勿修改。 |

# Telnyx 语音采集 - Python

## 安装

```bash
pip install telnyx
```

## 设置

```python
import os
from telnyx import Telnyx

client = Telnyx(
    api_key=os.environ.get("TELNYX_API_KEY"),  # This is the default and can be omitted
)
```

以下所有示例均假设 `client` 已按照上述方式初始化。

## 向 AI 助手添加消息

向由 AI 助手发起的通话中添加消息。

`POST /calls/{call_control_id}/actions/ai_assistant_add_messages`

```python
response = client.calls.actions.add_ai_assistant_messages(
    call_control_id="call_control_id",
)
print(response.data)
```

## 启动 AI 助手

在通话中启动 AI 助手。

`POST /calls/{call_control_id}/actions/ai_assistant_start`

```python
response = client.calls.actions.start_ai_assistant(
    call_control_id="call_control_id",
)
print(response.data)
```

## 停止 AI 助手

在通话中停止 AI 助手。

`POST /calls/{call_control_id}/actions/ai_assistant_stop`

```python
response = client.calls.actions.stop_ai_assistant(
    call_control_id="call_control_id",
)
print(response.data)
```

## 停止数据采集

停止当前的数据采集操作。

`POST /calls/{call_control_id}/actions/gather_stop`

```python
response = client.calls.actions.stop_gather(
    call_control_id="call_control_id",
)
print(response.data)
```

## 使用 AI 进行数据采集

使用语音助手收集请求负载中定义的参数。

`POST /calls/{call_control_id}/actions/gather_using_ai` — 必需参数：`parameters`

```python
response = client.calls.actions.gather_using_ai(
    call_control_id="call_control_id",
    parameters={
        "properties": "bar",
        "required": "bar",
        "type": "bar",
    },
)
print(response.data)
```

## 使用音频进行数据采集

在通话中播放音频文件，直到收集到所需的 DTMF 信号以构建交互式菜单。

`POST /calls/{call_control_id}/actions/gather_using_audio`

```python
response = client.calls.actions.gather_using_audio(
    call_control_id="call_control_id",
)
print(response.data)
```

## 使用文本转语音功能进行数据采集

将文本转换为语音并在通话中播放，直到收集到所需的 DTMF 信号以构建交互式菜单。

`POST /calls/{call_control_id}/actions/gather_using_speak` — 必需参数：`voice`, `payload`

```python
response = client.calls.actions.gather_using_speak(
    call_control_id="call_control_id",
    payload="say this on call",
    voice="male",
)
print(response.data)
```

## 收集数据

收集 DTMF 信号以构建交互式菜单。

`POST /calls/{call_control_id}/actions/gather`

```python
response = client.calls.actions.gather(
    call_control_id="call_control_id",
)
print(response.data)
```

---

## Webhook

以下 webhook 事件会被发送到您配置的 webhook 地址。
所有 webhook 都包含 `telnyx-timestamp` 和 `telnyx-signature-ed25519` 标头，用于验证（兼容标准 Webhook）。

| 事件 | 描述 |
|-------|-------------|
| `callGatherEnded` | 通话数据采集结束 |
| `CallAIGatherEnded` | 通话 AI 数据采集结束 |
| `CallAIGatherMessageHistoryUpdated` | 通话 AI 数据采集消息历史更新 |
| `CallAIGatherPartialResults` | 通话 AI 数据采集部分结果 |
| `CallConversationEnded` | 通话结束 |
| `callPlaybackStarted` | 通话播放开始 |
| `callPlaybackEnded` | 通话播放结束 |
| `callDtmfReceived` | 收到 DTMF 信号 |