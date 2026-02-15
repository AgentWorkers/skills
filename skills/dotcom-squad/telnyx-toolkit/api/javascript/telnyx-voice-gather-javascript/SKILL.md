---
name: telnyx-voice-gather-javascript
description: >-
  Collect DTMF input and speech from callers using standard gather or AI-powered
  gather. Build interactive voice menus and AI voice assistants. This skill
  provides JavaScript SDK examples.
metadata:
  author: telnyx
  product: voice-gather
  language: javascript
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 语音采集 - JavaScript

## 安装

```bash
npm install telnyx
```

## 设置

```javascript
import Telnyx from 'telnyx';

const client = new Telnyx({
  apiKey: process.env['TELNYX_API_KEY'], // This is the default and can be omitted
});
```

以下所有示例均假设 `client` 已按照上述方式初始化。

## 向 AI 助手添加消息

向 AI 助手发起的通话中添加消息。

`POST /calls/{call_control_id}/actions/ai_assistant_add_messages`

```javascript
const response = await client.calls.actions.addAIAssistantMessages('call_control_id');

console.log(response.data);
```

## 启动 AI 助手

在通话中启动 AI 助手。

`POST /calls/{call_control_id}/actions/ai_assistant_start`

```javascript
const response = await client.calls.actions.startAIAssistant('call_control_id');

console.log(response.data);
```

## 停止 AI 助手

在通话中停止 AI 助手。

`POST /calls/{call_control_id}/actions/ai_assistant_stop`

```javascript
const response = await client.calls.actions.stopAIAssistant('call_control_id');

console.log(response.data);
```

## 停止数据采集

停止当前的数据采集操作。

`POST /calls/{call_control_id}/actions/gather_stop`

```javascript
const response = await client.calls.actions.stopGather('call_control_id');

console.log(response.data);
```

## 使用 AI 收集数据

使用语音助手收集请求负载中定义的参数。

`POST /calls/{call_control_id}/actions/gather_using_ai` — 必需参数：`parameters`

```javascript
const response = await client.calls.actions.gatherUsingAI('call_control_id', {
  parameters: {
    properties: 'bar',
    required: 'bar',
    type: 'bar',
  },
});

console.log(response.data);
```

## 使用音频收集数据

在通话中播放音频文件，直到收集到所需的 DTMF 信号以构建交互式菜单。

`POST /calls/{call_control_id}/actions/gather_using_audio`

```javascript
const response = await client.calls.actions.gatherUsingAudio('call_control_id');

console.log(response.data);
```

## 使用语音转换功能收集数据

将文本转换为语音并在通话中播放，直到收集到所需的 DTMF 信号以构建交互式菜单。

`POST /calls/{call_control_id}/actions/gather_using_speak` — 必需参数：`voice`, `payload`

```javascript
const response = await client.calls.actions.gatherUsingSpeak('call_control_id', {
  payload: 'say this on call',
  voice: 'male',
});

console.log(response.data);
```

## 收集数据

收集 DTMF 信号以构建交互式菜单。

`POST /calls/{call_control_id}/actions/gather`

```javascript
const response = await client.calls.actions.gather('call_control_id');

console.log(response.data);
```

---

## Webhook

以下 webhook 事件会被发送到您配置的 webhook URL：
所有 webhook 都包含 `telnyx-timestamp` 和 `telnyx-signature-ed25519` 标头，用于验证（兼容标准 Webhook）。

| 事件 | 描述 |
|-------|-------------|
| `callGatherEnded` | 通话数据采集结束 |
| `CallAIGatherEnded` | AI 数据采集结束 |
| `CallAIGatherMessageHistoryUpdated` | AI 数据采集消息历史更新 |
| `CallAIGatherPartialResults` | AI 数据采集部分结果 |
| `CallConversationEnded` | 通话结束 |
| `callPlaybackStarted` | 通话播放开始 |
| `callPlaybackEnded` | 通话播放结束 |
| `callDtmfReceived` | 收到 DTMF 信号 |