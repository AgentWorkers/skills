---
name: telnyx-webrtc-client-ios
description: >-
  Build VoIP calling apps on iOS using Telnyx WebRTC SDK. Covers authentication,
  making/receiving calls, CallKit integration, PushKit/APNS push notifications,
  call quality metrics, and AI Agent integration. Use when implementing real-time
  voice communication on iOS.
metadata:
  author: telnyx
  product: webrtc
  language: swift
  platform: ios
---

# Telnyx WebRTC - iOS SDK

使用 Telnyx WebRTC 将实时语音通信功能集成到 iOS 应用程序中。

> **前提条件**：使用 Telnyx 服务器端 SDK 创建 WebRTC 凭据并生成登录令牌。请参考您所使用的服务器语言插件（例如 `telnyx-python`、`telnyx-javascript`）中的 `telnyx-webrtc-*` 技能文档。

## 安装

### CocoaPods

```ruby
pod 'TelnyxRTC', '~> 0.1.0'
```

然后运行：

```bash
pod install --repo-update
```

### Swift 包管理器

1. 在 Xcode 中：文件 → 添加包
2. 输入：`https://github.com/team-telnyx/telnyx-webrtc-ios.git`
3. 选择 `main` 分支

## 项目配置

1. **禁用 Bitcode**：构建设置 → “Bitcode” → 设置为 “NO”
2. **启用后台模式**：签名与功能 → +功能 → 后台模式：
   - IP 语音通话
   - 音频、AirPlay 和画中画功能
3. **麦克风权限**：将其添加到 `Info.plist` 中：
   ```xml
   <key>NSMicrophoneUsageDescription</key>
   <string>Microphone access required for VoIP calls</string>
   ```

---

## 认证

### 选项 1：基于凭据的登录

```swift
import TelnyxRTC

let telnyxClient = TxClient()
telnyxClient.delegate = self

let txConfig = TxConfig(
    sipUser: "your_sip_username",
    password: "your_sip_password",
    pushDeviceToken: "DEVICE_APNS_TOKEN",
    ringtone: "incoming_call.mp3",
    ringBackTone: "ringback_tone.mp3",
    logLevel: .all
)

do {
    try telnyxClient.connect(txConfig: txConfig)
} catch {
    print("Connection error: \(error)")
}
```

### 选项 2：基于令牌的登录（JWT）

```swift
let txConfig = TxConfig(
    token: "your_jwt_token",
    pushDeviceToken: "DEVICE_APNS_TOKEN",
    ringtone: "incoming_call.mp3",
    ringBackTone: "ringback_tone.mp3",
    logLevel: .all
)

try telnyxClient.connect(txConfig: txConfig)
```

### 配置选项

| 参数 | 类型 | 描述 |
|-----------|------|-------------|
| `sipUser` / `token` | 字符串 | 来自 Telnyx Portal 的凭据 |
| `password` | 字符串 | SIP 密码（基于凭据的认证） |
| `pushDeviceToken` | 字符串？ | APNS VoIP 推送令牌 |
| `ringtone` | 字符串？ | 来电时的音频文件 |
| `ringBackTone` | 字符串？ | 回拨时的音频文件 |
| `logLevel` | 日志级别 | .none, .error, .warning, .debug, .info, .all |
| `forceRelayCandidate` | 布尔值 | 强制使用 TURN 中继（避免使用本地网络） |

### 地区选择

```swift
let serverConfig = TxServerConfiguration(
    environment: .production,
    region: .usEast  // .auto, .usEast, .usCentral, .usWest, .caCentral, .eu, .apac
)

try telnyxClient.connect(txConfig: txConfig, serverConfiguration: serverConfig)
```

---

## 客户端代理

实现 `TxClientDelegate` 以接收事件：

```swift
extension ViewController: TxClientDelegate {
    
    func onSocketConnected() {
        // Connected to Telnyx backend
    }
    
    func onSocketDisconnected() {
        // Disconnected from backend
    }
    
    func onClientReady() {
        // Ready to make/receive calls
    }
    
    func onClientError(error: Error) {
        // Handle error
    }
    
    func onIncomingCall(call: Call) {
        // Incoming call while app is in foreground
        self.currentCall = call
    }
    
    func onPushCall(call: Call) {
        // Incoming call from push notification
        self.currentCall = call
    }
    
    func onCallStateUpdated(callState: CallState, callId: UUID) {
        switch callState {
        case .CONNECTING:
            break
        case .RINGING:
            break
        case .ACTIVE:
            break
        case .HELD:
            break
        case .DONE(let reason):
            if let reason = reason {
                print("Call ended: \(reason.cause ?? "Unknown")")
                print("SIP: \(reason.sipCode ?? 0) \(reason.sipReason ?? "")")
            }
        case .RECONNECTING(let reason):
            print("Reconnecting: \(reason.rawValue)")
        case .DROPPED(let reason):
            print("Dropped: \(reason.rawValue)")
        }
    }
}
```

---

## 发出外拨电话

```swift
let call = try telnyxClient.newCall(
    callerName: "John Doe",
    callerNumber: "+15551234567",
    destinationNumber: "+18004377950",
    callId: UUID()
)
```

---

## 接收来电

```swift
func onIncomingCall(call: Call) {
    // Store reference and show UI
    self.currentCall = call
    
    // Answer the call
    call.answer()
}
```

---

## 通话控制

```swift
// End call
call.hangup()

// Mute/Unmute
call.muteAudio()
call.unmuteAudio()

// Hold/Unhold
call.hold()
call.unhold()

// Send DTMF
call.dtmf(digit: "1")

// Toggle speaker
// (Use AVAudioSession for speaker routing)
```

---

## 推送通知（PushKit + CallKit）

### 1. 配置 PushKit

```swift
import PushKit

class AppDelegate: UIResponder, UIApplicationDelegate, PKPushRegistryDelegate {
    
    private var pushRegistry = PKPushRegistry(queue: .main)
    
    func initPushKit() {
        pushRegistry.delegate = self
        pushRegistry.desiredPushTypes = [.voIP]
    }
    
    func pushRegistry(_ registry: PKPushRegistry, 
                      didUpdate credentials: PKPushCredentials, 
                      for type: PKPushType) {
        if type == .voIP {
            let token = credentials.token.map { String(format: "%02X", $0) }.joined()
            // Save token for use in TxConfig
        }
    }
    
    func pushRegistry(_ registry: PKPushRegistry, 
                      didReceiveIncomingPushWith payload: PKPushPayload, 
                      for type: PKPushType, 
                      completion: @escaping () -> Void) {
        if type == .voIP {
            handleVoIPPush(payload: payload)
        }
        completion()
    }
}
```

### 2. 处理 VoIP 推送

```swift
func handleVoIPPush(payload: PKPushPayload) {
    guard let metadata = payload.dictionaryPayload["metadata"] as? [String: Any] else { return }
    
    let callId = metadata["call_id"] as? String ?? UUID().uuidString
    let callerName = (metadata["caller_name"] as? String) ?? ""
    let callerNumber = (metadata["caller_number"] as? String) ?? ""
    
    // Reconnect client and process push
    let txConfig = TxConfig(sipUser: sipUser, password: password, pushDeviceToken: token)
    try? telnyxClient.processVoIPNotification(
        txConfig: txConfig, 
        serverConfiguration: serverConfig,
        pushMetaData: metadata
    )
    
    // Report to CallKit (REQUIRED on iOS 13+)
    let callHandle = CXHandle(type: .generic, value: callerNumber)
    let callUpdate = CXCallUpdate()
    callUpdate.remoteHandle = callHandle
    
    provider.reportNewIncomingCall(with: UUID(uuidString: callId)!, update: callUpdate) { error in
        if let error = error {
            print("Failed to report call: \(error)")
        }
    }
}
```

### 3. CallKit 集成

```swift
import CallKit

class AppDelegate: CXProviderDelegate {
    
    var callKitProvider: CXProvider!
    
    func initCallKit() {
        let config = CXProviderConfiguration(localizedName: "TelnyxRTC")
        config.maximumCallGroups = 1
        config.maximumCallsPerCallGroup = 1
        callKitProvider = CXProvider(configuration: config)
        callKitProvider.setDelegate(self, queue: nil)
    }
    
    // CRITICAL: Audio session handling for WebRTC + CallKit
    func provider(_ provider: CXProvider, didActivate audioSession: AVAudioSession) {
        telnyxClient.enableAudioSession(audioSession: audioSession)
    }
    
    func provider(_ provider: CXProvider, didDeactivate audioSession: AVAudioSession) {
        telnyxClient.disableAudioSession(audioSession: audioSession)
    }
    
    func provider(_ provider: CXProvider, perform action: CXAnswerCallAction) {
        // Use SDK method to handle race conditions
        telnyxClient.answerFromCallkit(answerAction: action)
    }
    
    func provider(_ provider: CXProvider, perform action: CXEndCallAction) {
        telnyxClient.endCallFromCallkit(endAction: action)
    }
}
```

---

## 通话质量指标

通过设置 `debug: true` 来启用这些指标：

```swift
let call = try telnyxClient.newCall(
    callerName: "John",
    callerNumber: "+15551234567",
    destinationNumber: "+18004377950",
    callId: UUID(),
    debug: true
)

call.onCallQualityChange = { metrics in
    print("MOS: \(metrics.mos)")
    print("Jitter: \(metrics.jitter * 1000) ms")
    print("RTT: \(metrics.rtt * 1000) ms")
    print("Quality: \(metrics.quality.rawValue)")
    
    switch metrics.quality {
    case .excellent, .good:
        // Green indicator
    case .fair:
        // Yellow indicator
    case .poor, .bad:
        // Red indicator
    case .unknown:
        // Gray indicator
    }
}
```

| 质量等级 | MOS 分数范围 |
|---------------|-----------|
| .excellent | > 4.2 |
| .good | 4.1 - 4.2 |
| .fair | 3.7 - 4.0 |
| .poor | 3.1 - 3.6 |
| .bad | ≤ 3.0 |

---

## AI 代理集成

### 1. 匿名登录

```swift
client.anonymousLogin(
    targetId: "your-ai-assistant-id",
    targetType: "ai_assistant"
)
```

### 2. 开始对话

```swift
// After anonymous login, destination is ignored
let call = client.newInvite(
    callerName: "User",
    callerNumber: "user",
    destinationNumber: "ai-assistant",  // Ignored
    callId: UUID()
)
```

### 3. 接收通话记录

```swift
let cancellable = client.aiAssistantManager.subscribeToTranscriptUpdates { transcripts in
    for item in transcripts {
        print("\(item.role): \(item.content)")
        // role: "user" or "assistant"
    }
}
```

### 4. 发送文本消息

```swift
let success = client.sendAIAssistantMessage("Hello, can you help me?")
```

---

## 自定义日志记录

```swift
class MyLogger: TxLogger {
    func log(level: LogLevel, message: String) {
        // Send to your logging service
        MyAnalytics.log(level: level, message: message)
    }
}

let txConfig = TxConfig(
    sipUser: sipUser,
    password: password,
    logLevel: .all,
    customLogger: MyLogger()
)
```

---

## 故障排除

| 问题 | 解决方案 |
|-------|----------|
| 无音频 | 确保已授予麦克风权限 |
| 推送失败 | 验证 Telnyx Portal 中的 APNS 证书 |
| iOS 13+ 上的 CallKit 崩溃 | 必须将来电通知给 CallKit |
| 音频路由问题 | 在 CXProviderDelegate 中使用 `enableAudioSession`/`disableAudioSession` |
| 登录失败 | 验证 Telnyx Portal 中的 SIP 凭据 |

## 资源

- [官方文档](https://developers.telnyx.com/docs/voice/webrtc/ios-sdk)
- [推送通知设置](https://developers.telnyx.com/docs/voice/webrtc/ios-sdk/push-notification/portal-setup)
- [GitHub 仓库](https://github.com/team-telnyx/telnyx-webrtc-ios)