---
name: telnyx-webrtc-client-flutter
description: >-
  Build cross-platform VoIP calling apps with Flutter using Telnyx WebRTC SDK.
  Covers authentication, making/receiving calls, push notifications (FCM + APNS),
  call quality metrics, and AI Agent integration. Works on Android, iOS, and Web.
metadata:
  author: telnyx
  product: webrtc
  language: dart
  platform: flutter
---

# Telnyx WebRTC - Flutter SDK

将实时语音通信功能集成到 Flutter 应用程序中（支持 Android、iOS 和 Web 平台）。

> **先决条件**：需要使用 Telnyx 服务器端 SDK 创建 WebRTC 凭据并生成登录令牌。请参考您所使用的服务器语言插件（如 `telnyx-python`、`telnyx-javascript`）中的 `telnyx-webrtc-*` 文档。

## 快速入门选项

为了更快速地实现功能，可以考虑使用 [Telnyx Common](https://pub.dev/packages/telnyx_common)——这是一个高级抽象层，可以简化 WebRTC 集成过程，且设置步骤较少。

## 安装

在 `pubspec.yaml` 文件中添加以下内容：

```yaml
dependencies:
  telnyx_webrtc: ^latest_version
```

然后运行以下命令进行安装：

```bash
flutter pub get
```

## 平台配置

### Android

在 `AndroidManifest.xml` 文件中添加以下配置：

```xml
<uses-permission android:name="android.permission.INTERNET"/>
<uses-permission android:name="android.permission.RECORD_AUDIO" />
<uses-permission android:name="android.permission.MODIFY_AUDIO_SETTINGS" />
```

### iOS

在 `Info.plist` 文件中添加以下配置：

```xml
<key>NSMicrophoneUsageDescription</key>
<string>$(PRODUCT_NAME) needs microphone access for calls</string>
```

---

## 认证

### 选项 1：基于凭据的登录

```dart
final telnyxClient = TelnyxClient();

final credentialConfig = CredentialConfig(
  sipUser: 'your_sip_username',
  sipPassword: 'your_sip_password',
  sipCallerIDName: 'Display Name',
  sipCallerIDNumber: '+15551234567',
  notificationToken: fcmOrApnsToken,  // Optional: for push
  autoReconnect: true,
  debug: true,
  logLevel: LogLevel.debug,
);

telnyxClient.connectWithCredential(credentialConfig);
```

### 选项 2：基于令牌的登录（JWT）

```dart
final tokenConfig = TokenConfig(
  sipToken: 'your_jwt_token',
  sipCallerIDName: 'Display Name',
  sipCallerIDNumber: '+15551234567',
  notificationToken: fcmOrApnsToken,
  autoReconnect: true,
  debug: true,
);

telnyxClient.connectWithToken(tokenConfig);
```

## 配置选项

| 参数 | 类型 | 描述 |
|-----------|------|-------------|
| `sipUser` / `sipToken` | String | 来自 Telnyx Portal 的凭据 |
| `sipCallerIDName` | String | 显示给接收方的来电显示名称 |
| `sipCallerIDNumber` | String | 来电显示号码 |
| `notificationToken` | String? | FCM（Android）或 APNS（iOS）令牌 |
| `autoReconnect` | bool | 失败时自动重试登录 |
| `debug` | bool | 启用通话质量监控 |
| `logLevel` | LogLevel | 无、错误、警告、调试、信息、全部 |
| `ringTonePath` | String? | 自定义铃声资源路径 |
| `ringbackPath` | String? | 自定义回铃音资源路径 |

---

## 发起外拨电话

```dart
telnyxClient.call.newInvite(
  'John Doe',           // callerName
  '+15551234567',       // callerNumber
  '+15559876543',       // destinationNumber
  'my-custom-state',    // clientState
);
```

---

## 接收来电

监听 socket 事件：

```dart
InviteParams? _incomingInvite;
Call? _currentCall;

telnyxClient.onSocketMessageReceived = (TelnyxMessage message) {
  switch (message.socketMethod) {
    case SocketMethod.CLIENT_READY:
      // Ready to make/receive calls
      break;
      
    case SocketMethod.LOGIN:
      // Successfully logged in
      break;
      
    case SocketMethod.INVITE:
      // Incoming call!
      _incomingInvite = message.message.inviteParams;
      // Show incoming call UI...
      break;
      
    case SocketMethod.ANSWER:
      // Call was answered
      break;
      
    case SocketMethod.BYE:
      // Call ended
      break;
  }
};

// Accept the incoming call
void acceptCall() {
  if (_incomingInvite != null) {
    _currentCall = telnyxClient.acceptCall(
      _incomingInvite!,
      'My Name',
      '+15551234567',
      'state',
    );
  }
}
```

---

## 通话控制

```dart
// End call
telnyxClient.call.endCall(telnyxClient.call.callId);

// Decline incoming call
telnyxClient.createCall().endCall(_incomingInvite?.callID);

// Mute/Unmute
telnyxClient.call.onMuteUnmutePressed();

// Hold/Unhold
telnyxClient.call.onHoldUnholdPressed();

// Toggle speaker
telnyxClient.call.enableSpeakerPhone(true);

// Send DTMF tone
telnyxClient.call.dtmf(telnyxClient.call.callId, '1');
```

---

## 推送通知 - Android（FCM）

### 1. 设置 Firebase

```dart
// main.dart
@pragma('vm:entry-point')
Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  if (defaultTargetPlatform == TargetPlatform.android) {
    await Firebase.initializeApp();
    FirebaseMessaging.onBackgroundMessage(_firebaseBackgroundHandler);
  }
  
  runApp(const MyApp());
}
```

### 2. 后台处理程序

```dart
Future<void> _firebaseBackgroundHandler(RemoteMessage message) async {
  // Show notification (e.g., using flutter_callkit_incoming)
  showIncomingCallNotification(message);
  
  // Listen for user action
  FlutterCallkitIncoming.onEvent.listen((CallEvent? event) {
    switch (event!.event) {
      case Event.actionCallAccept:
        TelnyxClient.setPushMetaData(
          message.data,
          isAnswer: true,
          isDecline: false,
        );
        break;
      case Event.actionCallDecline:
        TelnyxClient.setPushMetaData(
          message.data,
          isAnswer: false,
          isDecline: true,  // SDK handles decline automatically
        );
        break;
    }
  });
}
```

### 3. 应用启动时处理推送通知

```dart
Future<void> _handlePushNotification() async {
  final data = await TelnyxClient.getPushMetaData();
  if (data != null) {
    PushMetaData pushMetaData = PushMetaData.fromJson(data);
    telnyxClient.handlePushNotification(
      pushMetaData,
      credentialConfig,
      tokenConfig,
    );
  }
}
```

### 提前接受/拒绝来电

```dart
bool _waitingForInvite = false;

void acceptCall() {
  if (_incomingInvite != null) {
    _currentCall = telnyxClient.acceptCall(...);
  } else {
    // Set flag if invite hasn't arrived yet
    _waitingForInvite = true;
  }
}

// In socket message handler:
case SocketMethod.INVITE:
  _incomingInvite = message.message.inviteParams;
  if (_waitingForInvite) {
    acceptCall();  // Accept now that invite arrived
    _waitingForInvite = false;
  }
  break;
```

---

## 推送通知 - iOS（APNS + PushKit）

### 1. 设置 AppDelegate

```swift
// AppDelegate.swift
func pushRegistry(_ registry: PKPushRegistry, 
                  didUpdate credentials: PKPushCredentials, 
                  for type: PKPushType) {
    let deviceToken = credentials.token.map { 
        String(format: "%02x", $0) 
    }.joined()
    SwiftFlutterCallkitIncomingPlugin.sharedInstance?
        .setDevicePushTokenVoIP(deviceToken)
}

func pushRegistry(_ registry: PKPushRegistry,
                  didReceiveIncomingPushWith payload: PKPushPayload,
                  for type: PKPushType,
                  completion: @escaping () -> Void) {
    guard type == .voIP else { return }
    
    if let metadata = payload.dictionaryPayload["metadata"] as? [String: Any] {
        let callerName = (metadata["caller_name"] as? String) ?? ""
        let callerNumber = (metadata["caller_number"] as? String) ?? ""
        let callId = (metadata["call_id"] as? String) ?? UUID().uuidString
        
        let data = flutter_callkit_incoming.Data(
            id: callId,
            nameCaller: callerName,
            handle: callerNumber,
            type: 0
        )
        data.extra = payload.dictionaryPayload as NSDictionary
        
        SwiftFlutterCallkitIncomingPlugin.sharedInstance?
            .showCallkitIncoming(data, fromPushKit: true)
    }
}
```

### 2. 在 Flutter 中处理推送通知

```dart
FlutterCallkitIncoming.onEvent.listen((CallEvent? event) {
  switch (event!.event) {
    case Event.actionCallIncoming:
      PushMetaData? pushMetaData = PushMetaData.fromJson(
        event.body['extra']['metadata']
      );
      telnyxClient.handlePushNotification(
        pushMetaData,
        credentialConfig,
        tokenConfig,
      );
      break;
    case Event.actionCallAccept:
      // Handle accept
      break;
  }
});
```

---

## 处理延迟推送通知

```dart
const CALL_MISSED_TIMEOUT = 60;  // seconds

void handlePushMessage(RemoteMessage message) {
  DateTime now = DateTime.now();
  Duration? diff = now.difference(message.sentTime!);
  
  if (diff.inSeconds > CALL_MISSED_TIMEOUT) {
    showMissedCallNotification(message);
    return;
  }
  
  // Handle normal incoming call...
}
```

---

## 通话质量监控

通过在配置中设置 `debug: true` 来启用通话质量监控：

```dart
// When making a call
call.newInvite(
  callerName: 'John',
  callerNumber: '+15551234567',
  destinationNumber: '+15559876543',
  clientState: 'state',
  debug: true,
);

// Listen for quality updates
call.onCallQualityChange = (CallQualityMetrics metrics) {
  print('MOS: ${metrics.mos}');
  print('Jitter: ${metrics.jitter * 1000} ms');
  print('RTT: ${metrics.rtt * 1000} ms');
  print('Quality: ${metrics.quality}');  // excellent, good, fair, poor, bad
};
```

| 质量等级 | MOS 分数范围 |
|---------------|-----------|
| 优秀 | > 4.2 |
| 良好 | 4.1 - 4.2 |
| 一般 | 3.7 - 4.0 |
| 较差 | 3.1 - 3.6 |
| 差 | ≤ 3.0 |

---

## 与 Telnyx 语音 AI 代理集成

### 1. 匿名登录

```dart
try {
  await telnyxClient.anonymousLogin(
    targetId: 'your_ai_assistant_id',
    targetType: 'ai_assistant',  // Default
    targetVersionId: 'optional_version_id',  // Optional
  );
} catch (e) {
  print('Login failed: $e');
}
```

### 2. 开始对话

```dart
telnyxClient.newInvite(
  'User Name',
  '+15551234567',
  '',  // Destination ignored for AI Agent
  'state',
  customHeaders: {
    'X-Account-Number': '123',  // Maps to {{account_number}}
    'X-User-Tier': 'premium',   // Maps to {{user_tier}}
  },
);
```

### 3. 接收对话记录

```dart
telnyxClient.onTranscriptUpdate = (List<TranscriptItem> transcript) {
  for (var item in transcript) {
    print('${item.role}: ${item.content}');
    // role: 'user' or 'assistant'
    // content: transcribed text
    // timestamp: when received
  }
};

// Get current transcript anytime
List<TranscriptItem> current = telnyxClient.transcript;

// Clear transcript
telnyxClient.clearTranscript();
```

### 4. 向 AI 代理发送文本消息

```dart
Call? activeCall = telnyxClient.calls.values.firstOrNull;

if (activeCall != null) {
  activeCall.sendConversationMessage(
    'Hello, I need help with my account'
  );
}
```

---

## 自定义日志记录

```dart
class MyCustomLogger extends CustomLogger {
  @override
  log(LogLevel level, String message) {
    print('[$level] $message');
    // Send to analytics, file, server, etc.
  }
}

final config = CredentialConfig(
  // ... other config
  logLevel: LogLevel.debug,
  customLogger: MyCustomLogger(),
);
```

---

## 故障排除

| 问题 | 解决方案 |
|-------|----------|
| Android 上没有音频 | 检查是否获得了 RECORD_AUDIO 权限 |
| iOS 上没有音频 | 检查 `Info.plist` 中的 NSMicrophoneUsageDescription 设置 |
| 推送通知无法发送（调试模式） | 推送通知仅在发布模式下生效 |
| 登录失败 | 验证 Telnyx Portal 中的 SIP 凭据 |
| 接听超时（10 秒） | 检查网络连接或推送设置 |
| 发送方 ID 不匹配 | 应用程序与服务器之间的 FCM 项目配置不匹配 |

## 资源

- [官方文档](https://developers.telnyx.com/docs/voice/webrtc/flutter-sdk)
- [pub.dev 包](https://pub.dev/packages/telnyx_webrtc)
- [GitHub 仓库](https://github.com/team-telnyx/flutter-voice-sdk)
- [Telnyx Common（简化版）](https://pub.dev/packages/telnyx_common)