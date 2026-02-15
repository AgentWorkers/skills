---
name: telnyx-voice-conferencing-java
description: >-
  Create and manage conference calls, queues, and multi-party sessions. Use when
  building call centers or conferencing applications. This skill provides Java
  SDK examples.
metadata:
  author: telnyx
  product: voice-conferencing
  language: java
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 语音会议 - Java

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

以下所有示例均假设 `client` 已按上述方式初始化。

## 将呼叫放入队列

将呼叫放入队列中。

`POST /calls/{call_control_id}/actions/enqueue` — 必需参数：`queue_name`

```java
import com.telnyx.sdk.models.calls.actions.ActionEnqueueParams;
import com.telnyx.sdk.models.calls.actions.ActionEnqueueResponse;

ActionEnqueueParams params = ActionEnqueueParams.builder()
    .callControlId("call_control_id")
    .queueName("support")
    .build();
ActionEnqueueResponse response = client.calls().actions().enqueue(params);
```

## 从队列中移除呼叫

从队列中移除呼叫。

`POST /calls/{call_control_id}/actions/leave_queue`

```java
import com.telnyx.sdk.models.calls.actions.ActionLeaveQueueParams;
import com.telnyx.sdk.models.calls.actions.ActionLeaveQueueResponse;

ActionLeaveQueueResponse response = client.calls().actions().leaveQueue("call_control_id");
```

## 列出会议

列出所有会议。

`GET /conferences`

```java
import com.telnyx.sdk.models.conferences.ConferenceListPage;
import com.telnyx.sdk.models.conferences.ConferenceListParams;

ConferenceListPage page = client.conferences().list();
```

## 创建会议

使用 `call_control_id` 和会议名称从现有通话中创建会议。

`POST /conferences` — 必需参数：`call_control_id`, `name`

```java
import com.telnyx.sdk.models.conferences.ConferenceCreateParams;
import com.telnyx.sdk.models.conferences.ConferenceCreateResponse;

ConferenceCreateParams params = ConferenceCreateParams.builder()
    .callControlId("v3:MdI91X4lWFEs7IgbBEOT9M4AigoY08M0WWZFISt1Yw2axZ_IiE4pqg")
    .name("Business")
    .build();
ConferenceCreateResponse conference = client.conferences().create(params);
```

## 获取会议信息

获取现有会议的信息。

`GET /conferences/{id}`

```java
import com.telnyx.sdk.models.conferences.ConferenceRetrieveParams;
import com.telnyx.sdk.models.conferences.ConferenceRetrieveResponse;

ConferenceRetrieveResponse conference = client.conferences().retrieve("id");
```

## 暂停会议参与者的发言

暂停会议中参与者的发言。

`POST /conferences/{id}/actions/hold`

```java
import com.telnyx.sdk.models.conferences.actions.ActionHoldParams;
import com.telnyx.sdk.models.conferences.actions.ActionHoldResponse;

ActionHoldResponse response = client.conferences().actions().hold("id");
```

## 加入会议

加入现有的通话。

`POST /conferences/{id}/actions/join` — 必需参数：`call_control_id`

```java
import com.telnyx.sdk.models.conferences.actions.ActionJoinParams;
import com.telnyx.sdk.models.conferences.actions.ActionJoinResponse;

ActionJoinParams params = ActionJoinParams.builder()
    .id("id")
    .callControlId("v3:MdI91X4lWFEs7IgbBEOT9M4AigoY08M0WWZFISt1Yw2axZ_IiE4pqg")
    .build();
ActionJoinResponse response = client.conferences().actions().join(params);
```

## 退出会议

将通话从会议中移除并恢复到待机状态。

`POST /conferences/{id}/actions/leave` — 必需参数：`call_control_id`

```java
import com.telnyx.sdk.models.conferences.actions.ActionLeaveParams;
import com.telnyx.sdk.models.conferences.actions.ActionLeaveResponse;

ActionLeaveParams params = ActionLeaveParams.builder()
    .id("id")
    .callControlId("c46e06d7-b78f-4b13-96b6-c576af9640ff")
    .build();
ActionLeaveResponse response = client.conferences().actions().leave(params);
```

## 静音会议参与者

静音会议中的参与者。

`POST /conferences/{id}/actions/mute`

```java
import com.telnyx.sdk.models.conferences.actions.ActionMuteParams;
import com.telnyx.sdk.models.conferences.actions.ActionMuteResponse;

ActionMuteResponse response = client.conferences().actions().mute("id");
```

## 播放音频给会议参与者

向会议中的所有或部分参与者播放音频。

`POST /conferences/{id}/actions/play`

```java
import com.telnyx.sdk.models.conferences.actions.ActionPlayParams;
import com.telnyx.sdk.models.conferences.actions.ActionPlayResponse;

ActionPlayResponse response = client.conferences().actions().play("id");
```

## 暂停会议录音

暂停会议录音。

`POST /conferences/{id}/actions/record_PAUSE`

```java
import com.telnyx.sdk.models.conferences.actions.ActionRecordPauseParams;
import com.telnyx.sdk.models.conferences.actions.ActionRecordPauseResponse;

ActionRecordPauseResponse response = client.conferences().actions().recordPause("id");
```

## 恢复会议录音

恢复会议录音。

`POST /conferences/{id}/actions/record.resume`

```java
import com.telnyx.sdk.models.conferences.actions.ActionRecordResumeParams;
import com.telnyx.sdk.models.conferences.actions.ActionRecordResumeResponse;

ActionRecordResumeResponse response = client.conferences().actions().recordResume("id");
```

## 开始会议录音

开始会议录音。

`POST /conferences/{id}/actions/record_start` — 必需参数：`format`

```java
import com.telnyx.sdk.models.conferences.actions.ActionRecordStartParams;
import com.telnyx.sdk.models.conferences.actions.ActionRecordStartResponse;

ActionRecordStartParams params = ActionRecordStartParams.builder()
    .id("id")
    .format(ActionRecordStartParams.Format.WAV)
    .build();
ActionRecordStartResponse response = client.conferences().actions().recordStart(params);
```

## 停止会议录音

停止会议录音。

`POST /conferences/{id}/actions/record_stop`

```java
import com.telnyx.sdk.models.conferences.actions.ActionRecordStopParams;
import com.telnyx.sdk.models.conferences.actions.ActionRecordStopResponse;

ActionRecordStopResponse response = client.conferences().actions().recordStop("id");
```

## 为会议参与者朗读文本

将文本转换为语音并播放给所有或部分参与者。

`POST /conferences/{id}/actions/speak` — 必需参数：`payload`, `voice`

```java
import com.telnyx.sdk.models.conferences.actions.ActionSpeakParams;
import com.telnyx.sdk.models.conferences.actions.ActionSpeakResponse;

ActionSpeakParams params = ActionSpeakParams.builder()
    .id("id")
    .payload("Say this to participants")
    .voice("female")
    .build();
ActionSpeakResponse response = client.conferences().actions().speak(params);
```

## 停止向会议参与者播放音频

停止向会议中的所有或部分参与者播放音频。

`POST /conferences/{id}/actions/stop`

```java
import com.telnyx.sdk.models.conferences.actions.ActionStopParams;
import com.telnyx.sdk.models.conferences.actions.ActionStopResponse;

ActionStopResponse response = client.conferences().actions().stop("id");
```

## 恢复会议参与者的发言权限

恢复会议中参与者的发言权限。

`POST /conferences/{id}/actions/unhold` — 必需参数：`call_control_ids`

```java
import com.telnyx.sdk.models.conferences.actions.ActionUnholdParams;
import com.telnyx.sdk.models.conferences.actions.ActionUnholdResponse;

ActionUnholdParams params = ActionUnholdParams.builder()
    .id("id")
    .addCallControlId("v3:MdI91X4lWFEs7IgbBEOT9M4AigoY08M0WWZFISt1Yw2axZ_IiE4pqg")
    .build();
ActionUnholdResponse response = client.conferences().actions().unhold(params);
```

## 解除会议参与者的静音状态

解除会议中参与者的静音状态。

`POST /conferences/{id}/actions/unmute`

```java
import com.telnyx.sdk.models.conferences.actions.ActionUnmuteParams;
import com.telnyx.sdk.models.conferences.actions.ActionUnmuteResponse;

ActionUnmuteResponse response = client.conferences().actions().unmute("id");
```

## 更新会议参与者信息

更新会议参与者的角色。

`POST /conferences/{id}/actions/update` — 必需参数：`call_control_id`, `supervisor_role`

```java
import com.telnyx.sdk.models.conferences.actions.ActionUpdateParams;
import com.telnyx.sdk.models.conferences.actions.ActionUpdateResponse;
import com.telnyx.sdk.models.conferences.actions.UpdateConference;

ActionUpdateParams params = ActionUpdateParams.builder()
    .id("id")
    .updateConference(UpdateConference.builder()
        .callControlId("v3:MdI91X4lWFEs7IgbBEOT9M4AigoY08M0WWZFISt1Yw2axZ_IiE4pqg")
        .supervisorRole(UpdateConference.SupervisorRole.WHISPER)
        .build())
    .build();
ActionUpdateResponse action = client.conferences().actions().update(params);
```

## 列出会议参与者

列出会议中的所有参与者。

`GET /conferences/{conference_id}/participants`

```java
import com.telnyx.sdk.models.conferences.ConferenceListParticipantsPage;
import com.telnyx.sdk.models.conferences.ConferenceListParticipantsParams;

ConferenceListParticipantsPage page = client.conferences().listParticipants("conference_id");
```

---

## Webhook

以下 Webhook 事件会被发送到您配置的 Webhook URL。所有 Webhook 都包含 `telnyx-timestamp` 和 `telnyx-signature-ed25519` 标头以进行验证（兼容标准 Webhook）。

| 事件 | 描述 |
|-------|-------------|
| `callEnqueued` | 呼叫被放入队列 |
| `callLeftQueue` | 呼叫离开队列 |
| `conferenceCreated` | 会议创建 |
| `conferenceEnded` | 会议结束 |
| `conferenceFloorChanged` | 会议发言权变更 |
| `conferenceParticipantJoined` | 会议参与者加入 |
| `conferenceParticipantLeft` | 会议参与者离开 |
| `conferenceParticipantPlaybackEnded` | 会议参与者的语音播放结束 |
| `conferenceParticipantPlaybackStarted` | 会议参与者的语音播放开始 |
| `conferenceParticipantSpeakEnded` | 会议参与者发言结束 |
| `conferenceParticipantSpeakStarted` | 会议参与者开始发言 |
| `conferencePlaybackEnded` | 会议语音播放结束 |
| `conferencePlaybackStarted` | 会议语音播放开始 |
| `conferenceRecordingSaved` | 会议录音保存 |
| `conferenceSpeakEnded` | 会议发言结束 |
| `conferenceSpeakStarted` | 会议发言开始 |
```
```