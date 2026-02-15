---
name: telnyx-voice-advanced-javascript
description: >-
  Advanced call control features including DTMF sending, SIPREC recording, noise
  suppression, client state, and supervisor controls. This skill provides
  JavaScript SDK examples.
metadata:
  author: telnyx
  product: voice-advanced
  language: javascript
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx Voice Advanced - JavaScript

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

以下所有示例均假设 `client` 已按上述方式初始化。

## 更新客户端状态

更新客户端状态

`PUT /calls/{call_control_id}/actions/client_state_update` — 必需参数：`client_state`

```javascript
const response = await client.calls.actions.updateClientState('call_control_id', {
  client_state: 'aGF2ZSBhIG5pY2UgZGF5ID1d',
});

console.log(response.data);
```

## SIP 转接呼叫

在呼叫控制过程中发起 SIP 转接操作。

`POST /calls/{call_control_id}/actions/refer` — 必需参数：`sip_address`

```javascript
const response = await client.calls.actions.refer('call_control_id', {
  sip_address: 'sip:username@sip.non-telnyx-address.com',
});

console.log(response.data);
```

## 发送 DTMF 音调

从当前通话链路发送 DTMF 音调。

`POST /calls/{call_control_id}/actions/send_dtmf` — 必需参数：`digits`

```javascript
const response = await client.calls.actions.sendDtmf('call_control_id', { digits: '1www2WABCDw9' });

console.log(response.data);
```

## 启动 SIPREC 会话

启动在 SIPREC 连接器中配置的 SIPREC 会话。

`POST /calls/{call_control_id}/actions/siprec_start`

```javascript
const response = await client.calls.actions.startSiprec('call_control_id');

console.log(response.data);
```

## 停止 SIPREC 会话

停止 SIPREC 会话。

`POST /calls/{call_control_id}/actions/siprec_stop`

```javascript
const response = await client.calls.actions.stopSiprec('call_control_id');

console.log(response.data);
```

## 噪音抑制（测试版）

启动噪音抑制功能。

`POST /calls/{call_control_id}/actions/suppression_start`

```javascript
const response = await client.calls.actions.startNoiseSuppression('call_control_id');

console.log(response.data);
```

## 停止噪音抑制（测试版）

停止噪音抑制功能。

`POST /calls/{call_control_id}/actions/suppression_stop`

```javascript
const response = await client.calls.actions.stopNoiseSuppression('call_control_id');

console.log(response.data);
```

## 切换监督者角色

切换桥接呼叫的监督者角色。

`POST /calls/{call_control_id}/actions/switch_supervisor_role` — 必需参数：`role`

```javascript
const response = await client.calls.actions.switchSupervisorRole('call_control_id', {
  role: 'barge',
});

console.log(response.data);
```

---

## Webhook

以下 Webhook 事件会发送到您配置的 Webhook URL。所有 Webhook 都包含 `telnyx-timestamp` 和 `telnyx-signature-ed25519` 标头以进行验证（兼容标准 Webhook）。

| 事件 | 描述 |
|-------|-------------|
| `callReferStarted` | 转接呼叫开始 |
| `callReferCompleted` | 转接呼叫完成 |
| `callReferFailed` | 转接呼叫失败 |
| `callSiprecStarted` | SIPREC 会话开始 |
| `callSiprecStopped` | SIPREC 会话停止 |
| `callSiprecFailed` | SIPREC 会话失败 |
```