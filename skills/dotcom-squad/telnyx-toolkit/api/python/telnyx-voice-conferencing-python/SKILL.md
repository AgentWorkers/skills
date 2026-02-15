---
name: telnyx-voice-conferencing-python
description: >-
  Create and manage conference calls, queues, and multi-party sessions. Use when
  building call centers or conferencing applications. This skill provides Python
  SDK examples.
metadata:
  author: telnyx
  product: voice-conferencing
  language: python
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 语音会议 - Python

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

## 将呼叫放入队列

将呼叫放入队列中。

`POST /calls/{call_control_id}/actions/enqueue` — 必需参数：`queue_name`

```python
response = client.calls.actions.enqueue(
    call_control_id="call_control_id",
    queue_name="support",
)
print(response.data)
```

## 从队列中移除呼叫

从队列中移除呼叫。

`POST /calls/{call_control_id}/actions/leave_queue`

```python
response = client.calls.actions.leave_queue(
    call_control_id="call_control_id",
)
print(response.data)
```

## 列出会议

列出所有会议。

`GET /conferences`

```python
page = client.conferences.list()
page = page.data[0]
print(page.id)
```

## 创建会议

使用 `call_control_id` 和会议名称从现有的通话中创建会议。

`POST /conferences` — 必需参数：`call_control_id`, `name`

```python
conference = client.conferences.create(
    call_control_id="v3:MdI91X4lWFEs7IgbBEOT9M4AigoY08M0WWZFISt1Yw2axZ_IiE4pqg",
    name="Business",
)
print(conference.data)
```

## 查询会议信息

查询已存在的会议信息。

`GET /conferences/{id}`

```python
conference = client.conferences.retrieve(
    id="id",
)
print(conference.data)
```

## 暂停会议参与者的发言

暂停会议中参与者的发言。

`POST /conferences/{id}/actions/hold`

```python
response = client.conferences.actions.hold(
    id="id",
)
print(response.data)
```

## 加入会议

加入现有的会议。

`POST /conferences/{id}/actions/join` — 必需参数：`call_control_id`

```python
response = client.conferences.actions.join(
    id="id",
    call_control_id="v3:MdI91X4lWFEs7IgbBEOT9M4AigoY08M0WWZFISt1Yw2axZ_IiE4pqg",
)
print(response.data)
```

## 退出会议

将通话从会议中移除并恢复到待机状态。

`POST /conferences/{id}/actions/leave` — 必需参数：`call_control_id`

```python
response = client.conferences.actions.leave(
    id="id",
    call_control_id="c46e06d7-b78f-4b13-96b6-c576af9640ff",
)
print(response.data)
```

## 静音会议参与者

静音会议中的所有参与者。

`POST /conferences/{id}/actions/mute`

```python
response = client.conferences.actions.mute(
    id="id",
)
print(response.data)
```

## 播放音频给会议参与者

向会议中的所有或部分参与者播放音频。

`POST /conferences/{id}/actions/play`

```python
response = client.conferences.actions.play(
    id="id",
)
print(response.data)
```

## 暂停会议录制

暂停会议录制。

`POST /conferences/{id}/actions/record_PAUSE`

```python
response = client.conferences.actions.record_pause(
    id="id",
)
print(response.data)
```

## 恢复会议录制

恢复会议录制。

`POST /conferences/{id}/actions/record_resume`

```python
response = client.conferences.actions.record_resume(
    id="id",
)
print(response.data)
```

## 开始会议录制

开始会议录制。

`POST /conferences/{id}/actions/record_start` — 必需参数：`format`

```python
response = client.conferences.actions.record_start(
    id="id",
    format="wav",
)
print(response.data)
```

## 停止会议录制

停止会议录制。

`POST /conferences/{id}/actions/record_stop`

```python
response = client.conferences.actions.record_stop(
    id="id",
)
print(response.data)
```

## 向会议参与者朗读文本

将文本转换为语音并播放给所有或部分参与者。

`POST /conferences/{id}/actions/speak` — 必需参数：`payload`, `voice`

```python
response = client.conferences.actions.speak(
    id="id",
    payload="Say this to participants",
    voice="female",
)
print(response.data)
```

## 停止会议中的音频播放

停止向会议中的所有或部分参与者播放音频。

`POST /conferences/{id}/actions/stop`

```python
response = client.conferences.actions.stop(
    id="id",
)
print(response.data)
```

## 恢复会议参与者的发言权限

恢复会议中参与者的发言权限。

`POST /conferences/{id}/actions/unhold` — 必需参数：`call_control_ids`

```python
response = client.conferences.actions.unhold(
    id="id",
    call_control_ids=["v3:MdI91X4lWFEs7IgbBEOT9M4AigoY08M0WWZFISt1Yw2axZ_IiE4pqg"],
)
print(response.data)
```

## 取消对会议参与者的静音

取消对会议中参与者的静音。

`POST /conferences/{id}/actions/unmute`

```python
response = client.conferences.actions.unmute(
    id="id",
)
print(response.data)
```

## 更新会议参与者信息

更新会议参与者的角色。

`POST /conferences/{id}/actions/update` — 必需参数：`call_control_id`, `supervisor_role`

```python
action = client.conferences.actions.update(
    id="id",
    call_control_id="v3:MdI91X4lWFEs7IgbBEOT9M4AigoY08M0WWZFISt1Yw2axZ_IiE4pqg",
    supervisor_role="whisper",
)
print(action.data)
```

## 列出会议参与者

列出会议中的所有参与者。

`GET /conferences/{conference_id}/participants`

```python
page = client.conferences.list_participants(
    conference_id="conference_id",
)
page = page.data[0]
print(page.id)
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
| `conferenceParticipantPlaybackEnded` | 会议参与者播放结束 |
| `conferenceParticipantPlaybackStarted` | 会议参与者开始播放 |
| `conferenceParticipantSpeakEnded` | 会议参与者发言结束 |
| `conferenceParticipantSpeakStarted` | 会议参与者开始发言 |
| `conferencePlaybackEnded` | 会议播放结束 |
| `conferencePlaybackStarted` | 会议播放开始 |
| `conferenceRecordingSaved` | 会议录制保存 |
| `conferenceSpeakEnded` | 会议发言结束 |
| `conferenceSpeakStarted` | 会议发言开始 |
```
```