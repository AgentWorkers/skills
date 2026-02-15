---
name: telnyx-webrtc-client-js
description: >-
  Build browser-based VoIP calling apps using Telnyx WebRTC JavaScript SDK.
  Covers authentication, voice calls, events, debugging, call quality
  metrics, and AI Agent integration. Use for web-based real-time communication.
metadata:
  author: telnyx
  product: webrtc
  language: javascript
  platform: browser
---

# Telnyx WebRTC - JavaScript SDK

将实时语音通信功能集成到浏览器应用程序中。

> **前提条件**：使用 Telnyx 服务器端 SDK 创建 WebRTC 凭据并生成登录令牌。请参考您所使用的服务器语言插件（例如 `telnyx-python`、`telnyx-javascript`）中的 `telnyx-webrtc-*` 技能文档。

## 安装

```bash
npm install @telnyx/webrtc --save
```

导入客户端库：

```js
import { TelnyxRTC } from '@telnyx/webrtc';
```

---

## 认证

### 选项 1：基于令牌的认证（推荐）

```js
const client = new TelnyxRTC({
  login_token: 'your_jwt_token',
});

client.connect();
```

### 选项 2：基于凭据的认证

```js
const client = new TelnyxRTC({
  login: 'sip_username',
  password: 'sip_password',
});

client.connect();
```

> **重要提示**：切勿在前端代码中硬编码凭据。请使用环境变量或提示用户输入凭据。

### 断开连接

```js
// When done, disconnect and remove listeners
client.disconnect();
client.off('telnyx.ready');
client.off('telnyx.notification');
```

---

## 媒体元素

指定用于播放远程音频的 HTML 元素：

```js
client.remoteElement = 'remoteMedia';
```

HTML 代码：

```html
<audio id="remoteMedia" autoplay="true" />
```

---

## 事件

```js
let activeCall;

client
  .on('telnyx.ready', () => {
    console.log('Ready to make calls');
  })
  .on('telnyx.error', (error) => {
    console.error('Error:', error);
  })
  .on('telnyx.notification', (notification) => {
    if (notification.type === 'callUpdate') {
      activeCall = notification.call;
      
      // Handle incoming call
      if (activeCall.state === 'ringing') {
        // Show incoming call UI
        // Call activeCall.answer() to accept
      }
    }
  });
```

### 事件类型

| 事件 | 描述 |
|-------|-------------|
| `telnyx_ready` | 客户端已连接并准备好使用 WebRTC |
| `telnyx.error` | 发生错误 |
| `telnyx.notification` | 来电通知、新来电信息 |
| `telnyx.stats.frame` | 通话中的质量指标（在启用调试模式时可用） |

---

## 发起通话

```js
const call = client.newCall({
  destinationNumber: '+18004377950',
  callerNumber: '+15551234567',
});
```

---

## 接听来电

```js
client.on('telnyx.notification', (notification) => {
  const call = notification.call;
  
  if (notification.type === 'callUpdate' && call.state === 'ringing') {
    // Incoming call - show UI and answer
    call.answer();
  }
});
```

---

## 通话控制

```js
// End call
call.hangup();

// Send DTMF tones
call.dtmf('1234');

// Mute audio
call.muteAudio();
call.unmuteAudio();

// Hold
call.hold();
call.unhold();
```

---

## 调试与通话质量

### 启用调试日志

```js
const call = client.newCall({
  destinationNumber: '+18004377950',
  debug: true,
  debugOutput: 'socket',  // 'socket' (send to Telnyx) or 'file' (save locally)
});
```

### 通话中的质量指标

```js
const call = client.newCall({
  destinationNumber: '+18004377950',
  debug: true,  // Required for metrics
});

client.on('telnyx.stats.frame', (stats) => {
  console.log('Quality stats:', stats);
  // Contains jitter, RTT, packet loss, etc.
});
```

---

## 通话前诊断

在发起通话前检查网络连接：

```js
import { PreCallDiagnosis } from '@telnyx/webrtc';

PreCallDiagnosis.run({
  credentials: {
    login: 'sip_username',
    password: 'sip_password',
    // or: loginToken: 'jwt_token'
  },
  texMLApplicationNumber: '+12407758982',
})
  .then((report) => {
    console.log('Diagnosis report:', report);
  })
  .catch((error) => {
    console.error('Diagnosis failed:', error);
  });
```

---

## 预设编码格式

设置通话的编码格式偏好：

```js
const allCodecs = RTCRtpReceiver.getCapabilities('audio').codecs;

// Prefer Opus for AI/high quality
const opusCodec = allCodecs.find(c => 
  c.mimeType.toLowerCase().includes('opus')
);

// Or PCMA for telephony compatibility
const pcmaCodec = allCodecs.find(c => 
  c.mimeType.toLowerCase().includes('pcma')
);

client.newCall({
  destinationNumber: '+18004377950',
  preferred_codecs: [opusCodec],
});
```

---

## 客户端注册状态

检查客户端是否已注册：

```js
const isRegistered = await client.getIsRegistered();
console.log('Registered:', isRegistered);
```

---

## 与 AI 助手的集成

### 匿名登录

无需 SIP 凭据即可连接到 AI 助手：

```js
const client = new TelnyxRTC({
  anonymous_login: {
    target_id: 'your-ai-assistant-id',
    target_type: 'ai_assistant',
  },
});

client.connect();
```

> **注意**：AI 助手必须将 `telephony_settings.supports_unauthenticated_web_calls` 设置为 `true`。

### 向 AI 助手发起通话

```js
// After anonymous login, destinationNumber is ignored
const call = client.newCall({
  destinationNumber: '',  // Can be empty
  remoteElement: 'remoteMedia',
});
```

### 推荐的 AI 通话编码格式

```js
const allCodecs = RTCRtpReceiver.getCapabilities('audio').codecs;
const opusCodec = allCodecs.find(c => 
  c.mimeType.toLowerCase().includes('opus')
);

client.newCall({
  destinationNumber: '',
  preferred_codecs: [opusCodec],  // Opus recommended for AI
});
```

---

## 浏览器支持

| 平台 | Chrome | Firefox | Safari | Edge |
|----------|--------|---------|--------|------|
| Android | ✓ | ✓ | - | - |
| iOS | - | - | ✓ | - |
| Linux | ✓ | ✓ | - | - |
| macOS | ✓ | ✓ | ✓ | ✓ |
| Windows | ✓ | ✓ | - | ✓ |

### 检查浏览器支持情况

```js
const webRTCInfo = TelnyxRTC.webRTCInfo;
console.log('WebRTC supported:', webRTCInfo.supportWebRTC);
```

---

## 故障排除

| 问题 | 解决方案 |
|-------|----------|
| 无法播放音频 | 检查浏览器的麦克风权限设置 |
| 回声/反馈 | 使用耳机或启用回声消除功能 |
| 连接失败 | 检查网络连接、防火墙设置，或使用 TURN 中继服务 |
| 通话质量不佳 | 启用调试模式（`debug: true`），并查看 `telnyx.stats.frame` 事件日志 |

---

## 资源

- [官方文档](https://developers.telnyx.com/development/webrtc/js-sdk/quickstart)
- [npm 包](https://www.npmjs.com/package/@telnyx/webrtc)
- [GitHub 仓库](https://github.com/team-telnyx/webrtc)
- [演示应用](https://github.com/team-telnyx/webrtc-demo-js)