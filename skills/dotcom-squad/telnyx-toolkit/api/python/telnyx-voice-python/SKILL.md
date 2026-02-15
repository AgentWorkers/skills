---
name: telnyx-voice-python
description: >-
  Make and receive calls, transfer, bridge, and manage call lifecycle with Call
  Control. Includes application management and call events. This skill provides
  Python SDK examples.
metadata:
  author: telnyx
  product: voice
  language: python
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx Voice - Python

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

以下所有示例均假设 `client` 已按上述方式初始化。

## 接听来电

接听来电。

`POST /calls/{call_control_id}/actions/answer`

```python
response = client.calls.actions.answer(
    call_control_id="call_control_id",
)
print(response.data)
```

## 桥接通话

将两个通话连接桥接在一起。

`POST /calls/{call_control_id}/actions/bridge` — 必需参数：`call_control_id`

```python
response = client.calls.actions.bridge(
    call_control_id_to_bridge="call_control_id",
    call_control_id_to_bridge_with="v3:MdI91X4lWFEs7IgbBEOT9M4AigoY08M0WWZFISt1Yw2axZ_IiE4pqg",
)
print(response.data)
```

## 拨打电话

从指定的连接拨打一个号码或 SIP URI。

`POST /calls` — 必需参数：`connection_id`, `to`, `from`

```python
response = client.calls.dial(
    connection_id="7267xxxxxxxxxxxxxx",
    from_="+18005550101",
    to="+18005550100",
)
print(response.data)
```

## 结束通话

挂断通话。

`POST /calls/{call_control_id}/actions/hangup`

```python
response = client.calls.actions.hangup(
    call_control_id="call_control_id",
)
print(response.data)
```

## 转接通话

将通话转接到新的目的地。

`POST /calls/{call_control_id}/actions/transfer` — 必需参数：`to`

```python
response = client.calls.actions.transfer(
    call_control_id="call_control_id",
    to="+18005550100",
)
print(response.data)
```

## 列出指定连接的所有活动通话

列出指定连接的所有活动通话。

`GET /connections/{connection_id}/active_calls`

```python
page = client.connections.list_active_calls(
    connection_id="1293384261075731461",
)
page = page.data[0]
print(page.call_control_id)
```

## 列出通话控制应用程序

返回通话控制应用程序的列表。

`GET /call_control_applications`

```python
page = client.call_control_applications.list()
page = page.data[0]
print(page.id)
```

## 创建通话控制应用程序

创建一个新的通话控制应用程序。

`POST /call_control_applications` — 必需参数：`application_name`, `webhook_event_url`

```python
call_control_application = client.call_control_applications.create(
    application_name="call-router",
    webhook_event_url="https://example.com",
)
print(call_control_application.data)
```

## 获取通话控制应用程序的详细信息

获取现有通话控制应用程序的详细信息。

`GET /call_control_applications/{id}`

```python
call_control_application = client.call_control_applications.retrieve(
    "id",
)
print(call_control_application.data)
```

## 更新通话控制应用程序

更新现有通话控制应用程序的设置。

`PATCH /call_control_applications/{id}` — 必需参数：`application_name`, `webhook_event_url`

```python
call_control_application = client.call_control_applications.update(
    id="id",
    application_name="call-router",
    webhook_event_url="https://example.com",
)
print(call_control_application.data)
```

## 删除通话控制应用程序

删除通话控制应用程序。

`DELETE /call_control_applications/{id}`

```python
call_control_application = client.call_control_applications.delete(
    "id",
)
print(call_control_application.data)
```

## 列出通话事件

根据指定的过滤参数筛选通话事件。

`GET /call_events`

```python
page = client.call_events.list()
page = page.data[0]
print(page.call_leg_id)
```

---

## Webhook

以下 Webhook 事件会被发送到您配置的 Webhook URL。所有 Webhook 都包含 `telnyx-timestamp` 和 `telnyx-signature-ed25519` 标头以进行验证（兼容标准 Webhook）。

| 事件 | 描述 |
|-------|-------------|
| `callAnswered` | 通话已接听 |
| `callStreamingStarted` | 通话流开始 |
| `callStreamingStopped` | 通话流停止 |
| `callStreamingFailed` | 通话流失败 |
| `callBridged` | 通话被桥接 |
| `callInitiated` | 通话开始 |
| `callHangup` | 通话挂断 |
| `callRecordingSaved` | 通话录音保存 |
| `callMachineDetectionEnded` | 机器检测结束 |
| `callMachineGreetingEnded` | 机器问候结束 |
| `callMachinePremiumDetectionEnded` | 机器高级检测结束 |
| `callMachinePremiumGreetingEnded` | 机器高级问候结束 |
```
```