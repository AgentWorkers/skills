---
name: telnyx-voice-gather-java
description: >-
  Collect DTMF input and speech from callers using standard gather or AI-powered
  gather. Build interactive voice menus and AI voice assistants. This skill
  provides Java SDK examples.
metadata:
  author: telnyx
  product: voice-gather
  language: java
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 语音采集 - Java

## 安装

```text
// See https://github.com/team-telnyx/telnyx-java for Maven/Gradle setup
```

## 设置

```java
import com.telnyx.sdk.client.TelnyxClient;
import com.telnyx.sdk.client.okhttp.TelnyxOkHttpClient;

TelnyxClient client = TelnyxOkHttpClient.fromEnv();
```

以下所有示例均假设 `client` 已按照上述方式初始化。

## 向 AI 助手添加消息

向 AI 助手发起的通话中添加消息。

`POST /calls/{call_control_id}/actions/ai_assistant_add_messages`

```java
import com.telnyx.sdk.models.calls.actions.ActionAddAiAssistantMessagesParams;
import com.telnyx.sdk.models.calls.actions.ActionAddAiAssistantMessagesResponse;

ActionAddAiAssistantMessagesResponse response = client.calls().actions().addAiAssistantMessages("call_control_id");
```

## 启动 AI 助手

在通话中启动 AI 助手。

`POST /calls/{call_control_id}/actions/ai_assistant_start`

```java
import com.telnyx.sdk.models.calls.actions.ActionStartAiAssistantParams;
import com.telnyx.sdk.models.calls.actions.ActionStartAiAssistantResponse;

ActionStartAiAssistantResponse response = client.calls().actions().startAiAssistant("call_control_id");
```

## 停止 AI 助手

在通话中停止 AI 助手。

`POST /calls/{call_control_id}/actions/ai_assistant_stop`

```java
import com.telnyx.sdk.models.calls.actions.ActionStopAiAssistantParams;
import com.telnyx.sdk.models.calls.actions.ActionStopAiAssistantResponse;

ActionStopAiAssistantResponse response = client.calls().actions().stopAiAssistant("call_control_id");
```

## 停止数据采集

停止当前的数据采集操作。

`POST /calls/{call_control_id}/actions/gather_stop`

```java
import com.telnyx.sdk.models.calls.actions.ActionStopGatherParams;
import com.telnyx.sdk.models.calls.actions.ActionStopGatherResponse;

ActionStopGatherResponse response = client.calls().actions().stopGather("call_control_id");
```

## 使用 AI 进行数据采集

使用语音助手收集请求负载中定义的参数。

`POST /calls/{call_control_id}/actions/gather_using_ai` — 必需参数：`parameters`

```java
import com.telnyx.sdk.core.JsonValue;
import com.telnyx.sdk.models.calls.actions.ActionGatherUsingAiParams;
import com.telnyx.sdk.models.calls.actions.ActionGatherUsingAiResponse;

ActionGatherUsingAiParams params = ActionGatherUsingAiParams.builder()
    .callControlId("call_control_id")
    .parameters(ActionGatherUsingAiParams.Parameters.builder()
        .putAdditionalProperty("properties", JsonValue.from("bar"))
        .putAdditionalProperty("required", JsonValue.from("bar"))
        .putAdditionalProperty("type", JsonValue.from("bar"))
        .build())
    .build();
ActionGatherUsingAiResponse response = client.calls().actions().gatherUsingAi(params);
```

## 使用音频进行数据采集

在通话中播放音频文件，直到收集到所需的 DTMF 信号以构建交互式菜单。

`POST /calls/{call_control_id}/actions/gather_using_audio`

```java
import com.telnyx.sdk.models.calls.actions.ActionGatherUsingAudioParams;
import com.telnyx.sdk.models.calls.actions.ActionGatherUsingAudioResponse;

ActionGatherUsingAudioResponse response = client.calls().actions().gatherUsingAudio("call_control_id");
```

## 使用语音转换进行数据采集

将文本转换为语音并在通话中播放，直到收集到所需的 DTMF 信号以构建交互式菜单。

`POST /calls/{call_control_id}/actions/gather_using_speak` — 必需参数：`voice`, `payload`

```java
import com.telnyx.sdk.models.calls.actions.ActionGatherUsingSpeakParams;
import com.telnyx.sdk.models.calls.actions.ActionGatherUsingSpeakResponse;

ActionGatherUsingSpeakParams params = ActionGatherUsingSpeakParams.builder()
    .callControlId("call_control_id")
    .payload("say this on call")
    .voice("male")
    .build();
ActionGatherUsingSpeakResponse response = client.calls().actions().gatherUsingSpeak(params);
```

## 采集数据

收集 DTMF 信号以构建交互式菜单。

`POST /calls/{call_control_id}/actions/gather`

```java
import com.telnyx.sdk.models.calls.actions.ActionGatherParams;
import com.telnyx.sdk.models.calls.actions.ActionGatherResponse;

ActionGatherResponse response = client.calls().actions().gather("call_control_id");
```

---

## Webhook

以下 webhook 事件会被发送到您配置的 webhook URL：
所有 webhook 都包含 `telnyx-timestamp` 和 `telnyx-signature-ed25519` 标头用于验证（兼容标准 Webhook）。

| 事件 | 描述 |
|-------|-------------|
| `callGatherEnded` | 通话数据采集结束 |
| `CallAIGatherEnded` | 通话 AI 数据采集结束 |
| `CallAIGatherMessageHistoryUpdated` | 通话 AI 数据采集消息历史更新 |
| `CallAIGatherPartialResults` | 通话 AI 数据采集部分结果 |
| `CallConversationEnded` | 通话结束 |
| `callPlaybackStarted` | 通话播放开始 |
| `callPlaybackEnded` | 通话播放结束 |
| `callDtmfReceived` | 通话中接收到 DTMF 信号 |
```