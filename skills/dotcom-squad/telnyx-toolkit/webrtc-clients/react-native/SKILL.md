---
name: telnyx-webrtc-client-react-native
description: >-
  Build cross-platform VoIP calling apps with React Native using Telnyx Voice SDK.
  High-level reactive API with automatic lifecycle management, CallKit/ConnectionService
  integration, and push notifications. Use for mobile VoIP apps with minimal setup.
metadata:
  author: telnyx
  product: webrtc
  language: typescript
  platform: react-native
---

# Telnyx WebRTC - React Native SDK

使用 `@telnyx/react-voice-commons-sdk` 库，将实时语音通信功能集成到 React Native 应用程序（Android 和 iOS）中。

> **前提条件**：使用 Telnyx 服务器端 SDK 创建 WebRTC 凭据并生成登录令牌。请参考您所使用的服务器语言插件（例如 `telnyx-python`、`telnyx-javascript`）中的 `telnyx-webrtc-*` 技能文档。

## 特点

- **基于 RxJS 的状态管理**：使用 RxJS 进行状态管理
- **自动生命周期管理**：处理应用程序在后台和前台的状态切换
- **原生通话界面**：支持 iOS 的 CallKit 和 Android 的 ConnectionService
- **推送通知**：支持 Android 的 FCM 和 iOS 的 APNs/PushKit
- **TypeScript 支持**：提供完整的类型定义

## 安装

```bash
npm install @telnyx/react-voice-commons-sdk
```

---

## 基本设置

```tsx
import { TelnyxVoiceApp, createTelnyxVoipClient } from '@telnyx/react-voice-commons-sdk';

// Create VoIP client instance
const voipClient = createTelnyxVoipClient({
  enableAppStateManagement: true,  // Auto background/foreground handling
  debug: true,                     // Enable logging
});

export default function App() {
  return (
    <TelnyxVoiceApp 
      voipClient={voipClient} 
      enableAutoReconnect={false} 
      debug={true}
    >
      <YourAppContent />
    </TelnyxVoiceApp>
  );
}
```

---

## 认证

### 基于凭据的登录

```tsx
import { createCredentialConfig } from '@telnyx/react-voice-commons-sdk';

const config = createCredentialConfig('sip_username', 'sip_password', {
  debug: true,
  pushNotificationDeviceToken: 'your_device_token',
});

await voipClient.login(config);
```

### 基于令牌的登录（JWT）

```tsx
import { createTokenConfig } from '@telnyx/react-voice-commons-sdk';

const config = createTokenConfig('your_jwt_token', {
  debug: true,
  pushNotificationDeviceToken: 'your_device_token',
});

await voipClient.loginWithToken(config);
```

### 自动重连

该库会自动保存凭据，以实现无缝的重连：

```tsx
// Automatically reconnects using stored credentials
const success = await voipClient.loginFromStoredConfig();

if (!success) {
  // No stored auth, show login UI
}
```

---

## 基于 RxJS 的状态管理

```tsx
import { useEffect, useState } from 'react';

function CallScreen() {
  const [connectionState, setConnectionState] = useState(null);
  const [calls, setCalls] = useState([]);
  
  useEffect(() => {
    // Subscribe to connection state
    const connSub = voipClient.connectionState$.subscribe((state) => {
      setConnectionState(state);
    });
    
    // Subscribe to active calls
    const callsSub = voipClient.calls$.subscribe((activeCalls) => {
      setCalls(activeCalls);
    });
    
    return () => {
      connSub.unsubscribe();
      callsSub.unsubscribe();
    };
  }, []);
  
  return (/* UI */);
}
```

### 单个通话的状态

```tsx
useEffect(() => {
  if (call) {
    const sub = call.callState$.subscribe((state) => {
      console.log('Call state:', state);
    });
    return () => sub.unsubscribe();
  }
}, [call]);
```

---

## 发起通话

```tsx
const call = await voipClient.newCall('+18004377950');
```

---

## 接收通话

来电会通过推送通知自动处理，并由 `TelnyxVoiceApp` 组件显示。同时，会自动显示原生的通话界面（CallKit/ConnectionService）。

---

## 通话控制

```tsx
// Answer incoming call
await call.answer();

// Mute/Unmute
await call.mute();
await call.unmute();

// Hold/Unhold
await call.hold();
await call.unhold();

// End call
await call.hangup();

// Send DTMF
await call.dtmf('1');
```

---

## 推送通知 - Android（FCM）

### 1. 将 `google-services.json` 文件放置在项目根目录下
### 2. 设置 MainActivity
```kotlin
// MainActivity.kt
import com.telnyx.react_voice_commons.TelnyxMainActivity

class MainActivity : TelnyxMainActivity() {
    override fun onHandleIntent(intent: Intent) {
        super.onHandleIntent(intent)
        // Additional intent processing
    }
}
```

### 3. 设置后台消息处理程序
```tsx
// index.js or App.tsx
import messaging from '@react-native-firebase/messaging';
import { TelnyxVoiceApp } from '@telnyx/react-voice-commons-sdk';

messaging().setBackgroundMessageHandler(async (remoteMessage) => {
  await TelnyxVoiceApp.handleBackgroundPush(remoteMessage.data);
});
```

---

## 推送通知 - iOS（PushKit）

### 设置 AppDelegate

```swift
// AppDelegate.swift
import PushKit
import TelnyxVoiceCommons

@UIApplicationMain
public class AppDelegate: ExpoAppDelegate, PKPushRegistryDelegate {
  
  public override func application(
    _ application: UIApplication,
    didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]? = nil
  ) -> Bool {
    // Initialize VoIP push registration
    TelnyxVoipPushHandler.initializeVoipRegistration()
    return super.application(application, didFinishLaunchingWithOptions: launchOptions)
  }
  
  // VoIP Push Token Update
  public func pushRegistry(_ registry: PKPushRegistry, 
                           didUpdate pushCredentials: PKPushCredentials, 
                           for type: PKPushType) {
    TelnyxVoipPushHandler.shared.handleVoipTokenUpdate(pushCredentials, type: type)
  }
  
  // VoIP Push Received
  public func pushRegistry(_ registry: PKPushRegistry, 
                           didReceiveIncomingPushWith payload: PKPushPayload, 
                           for type: PKPushType, 
                           completion: @escaping () -> Void) {
    TelnyxVoipPushHandler.shared.handleVoipPush(payload, type: type, completion: completion)
  }
}
```

> **注意**：CallKit 的集成由内部的 `CallBridge` 组件自动处理。

---

## 配置选项

### `createTelnyxVoipClient` 的配置选项

| 选项 | 类型 | 默认值 | 说明 |
|--------|------|---------|-------------|
| `enableAppStateManagement` | boolean | true | 启用自动处理应用程序在后台和前台的状态切换 |
| `debug` | boolean | false | 启用调试日志记录 |

### `TelnyxVoiceApp` 的属性

| 属性 | 类型 | 说明 |
|------|------|-------------|
| `voipClient` | TelnyxVoipClient | VoIP 客户端实例 |
| `enableAutoReconnect` | boolean | 断开连接时自动重连 |
| `debug` | boolean | 启用调试日志记录 |

---

## 存储键（自动管理）

该库会自动管理以下 AsyncStorage 键：

- `@telnyx_username` - SIP 用户名
- `@telnyx_password` - SIP 密码
- `@credential_token` - JWT 令牌
- `@push_token` - 推送通知令牌

> 您无需手动管理这些键。

---

## 故障排除

| 问题 | 解决方案 |
|-------|----------|
| 登录重复 | 在使用具有自动重连功能的 `TelnyxVoiceApp` 时，不要手动调用 `login()` 方法 |
| 应用在后台断开连接 | 检查 `enableAutoReconnect` 的设置 |
| Android 的推送通知无法发送 | 确保 `google-services.json` 文件存在，并且 `MainActivity` 继承自 `TelnyxMainActivity` |
| iOS 的推送通知无法发送 | 确保 `AppDelegate` 实现了 `PKPushRegistryDelegate` 并调用了 `TelnyxVoipPushHandler` |
| 内存泄漏 | 在 `useEffect` 的清理代码中取消订阅 RxJS 的观察者 |
| 音频问题 | iOS 的音频处理由 `CallBridge` 负责；Android 的音频问题请检查 `ConnectionService` |

### 清除存储的认证信息（高级操作）

```tsx
import AsyncStorage from '@react-native-async-storage/async-storage';

await AsyncStorage.multiRemove([
  '@telnyx_username',
  '@telnyx_password', 
  '@credential_token',
  '@push_token',
]);
```

---

## 资源

- [官方文档](https://developers.telnyx.com/development/webrtc/react-native-sdk)
- [GitHub 仓库](https://github.com/team-telnyx/react-native-voice-commons)
- [npm 包](https://www.npmjs.com/package/@telnyx/react-voice-commons-sdk)