---
name: telnyx-voice-advanced-python
description: >-
  Advanced call control features including DTMF sending, SIPREC recording, noise
  suppression, client state, and supervisor controls. This skill provides Python
  SDK examples.
metadata:
  author: telnyx
  product: voice-advanced
  language: python
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx Voice Advanced - Python

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

## 更新客户端状态

用于更新客户端状态：

`PUT /calls/{call_control_id}/actions/client_state_update` — 必需参数：`client_state`

```python
response = client.calls.actions.update_client_state(
    call_control_id="call_control_id",
    client_state="aGF2ZSBhIG5pY2UgZGF5ID1d",
)
print(response.data)
```

## SIP 转接呼叫

用于发起 SIP 转接操作：

`POST /calls/{call_control_id}/actions/refer` — 必需参数：`sip_address`

```python
response = client.calls.actions.refer(
    call_control_id="call_control_id",
    sip_address="sip:username@sip.non-telnyx-address.com",
)
print(response.data)
```

## 发送 DTMF 音频

用于从当前通话链路发送 DTMF 音频：

`POST /calls/{call_control_id}/actions/send_dtmf` — 必需参数：`digits`

```python
response = client.calls.actions.send_dtmf(
    call_control_id="call_control_id",
    digits="1www2WABCDw9",
)
print(response.data)
```

## 启动 SIPREC 会话

用于启动在 SIPREC 连接器中配置的 SIPREC 会话：

`POST /calls/{call_control_id}/actions/siprec_start`

```python
response = client.calls.actions.start_siprec(
    call_control_id="call_control_id",
)
print(response.data)
```

## 停止 SIPREC 会话

用于停止 SIPREC 会话：

`POST /calls/{call_control_id}/actions/siprec_stop`

```python
response = client.calls.actions.stop_siprec(
    call_control_id="call_control_id",
)
print(response.data)
```

## 启用噪声抑制（测试版）

用于启用噪声抑制功能：

`POST /calls/{call_control_id}/actions/suppression_start`

```python
response = client.calls.actions.start_noise_suppression(
    call_control_id="call_control_id",
)
print(response.data)
```

## 停用噪声抑制（测试版）

用于停止噪声抑制功能：

`POST /calls/{call_control_id}/actions/suppression_stop`

```python
response = client.calls.actions.stop_noise_suppression(
    call_control_id="call_control_id",
)
print(response.data)
```

## 切换监督者角色

用于切换桥接呼叫的监督者角色：

`POST /calls/{call_control_id}/actions/switch_supervisor_role` — 必需参数：`role`

---

## Webhook

以下 Webhook 事件会被发送到您配置的 Webhook URL。所有 Webhook 都包含 `telnyx-timestamp` 和 `telnyx-signature-ed25519` 标头以进行验证（兼容标准 Webhook）。

| 事件 | 描述 |
|-------|-------------|
| `callReferStarted` | 转接呼叫开始 |
| `callReferCompleted` | 转接呼叫完成 |
| `callReferFailed` | 转接呼叫失败 |
| `callSiprecStarted` | SIPREC 会话开始 |
| `callSiprecStopped` | SIPREC 会话停止 |
| `callSiprecFailed` | SIPREC 会话失败 |