---
name: telnyx-webrtc-client-android
description: >-
  Build VoIP calling apps on Android using Telnyx WebRTC SDK. Covers authentication,
  making/receiving calls, push notifications (FCM), call quality metrics, and AI Agent
  integration. Use when implementing real-time voice communication on Android.
metadata:
  author: telnyx
  product: webrtc
  language: kotlin
  platform: android
---

# Telnyx WebRTC - Android SDK

使用 Telnyx WebRTC 将实时语音通信功能集成到 Android 应用程序中。

> **前提条件**：使用 Telnyx 服务器端 SDK 创建 WebRTC 凭据并生成登录令牌。请参考您的服务器语言插件（例如 `telnyx-python`、`telnyx-javascript`）中的 `telnyx-webrtc-*` 技能文档。

## 安装

将 JitPack 仓库添加到项目的 `build.gradle` 文件中：

```gradle
allprojects {
    repositories {
        maven { url 'https://jitpack.io' }
    }
}
```

添加相应的依赖项：

```gradle
dependencies {
    implementation 'com.github.team-telnyx:telnyx-webrtc-android:latest-version'
}
```

## 所需权限

在 `AndroidManifest.xml` 中添加以下权限：

```xml
<uses-permission android:name="android.permission.INTERNET"/>
<uses-permission android:name="android.permission.RECORD_AUDIO" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />

<!-- For push notifications (Android 14+) -->
<uses-permission android:name="android.permission.POST_NOTIFICATIONS" />
<uses-permission android:name="android.permission.FOREGROUND_SERVICE"/>
<uses-permission android:name="android.permission.FOREGROUND_SERVICE_PHONE_CALL"/>
```

---

## 认证

### 选项 1：基于凭据的登录

```kotlin
val telnyxClient = TelnyxClient(context)
telnyxClient.connect()

val credentialConfig = CredentialConfig(
    sipUser = "your_sip_username",
    sipPassword = "your_sip_password",
    sipCallerIDName = "Display Name",
    sipCallerIDNumber = "+15551234567",
    fcmToken = fcmToken,  // Optional: for push notifications
    logLevel = LogLevel.DEBUG,
    autoReconnect = true
)

telnyxClient.credentialLogin(credentialConfig)
```

### 选项 2：基于令牌的登录（JWT）

```kotlin
val tokenConfig = TokenConfig(
    sipToken = "your_jwt_token",
    sipCallerIDName = "Display Name",
    sipCallerIDNumber = "+15551234567",
    fcmToken = fcmToken,
    logLevel = LogLevel.DEBUG,
    autoReconnect = true
)

telnyxClient.tokenLogin(tokenConfig)
```

### 配置选项

| 参数 | 类型 | 描述 |
|-----------|------|-------------|
| `sipUser` / `sipToken` | String | 来自 Telnyx Portal 的凭据 |
| `sipCallerIDName` | String? | 显示给接收方的来电显示名称 |
| `sipCallerIDNumber` | String? | 来电显示号码 |
| `fcmToken` | String? | 用于推送通知的 Firebase Cloud Messaging 令牌 |
| `ringtone` | Any? | 铃声的原始资源 ID 或 URI |
| `ringBackTone` | Int? | 回拨音的原始资源 ID |
| `logLevel` | LogLevel | NONE, ERROR, WARNING, DEBUG, INFO, ALL |
| `autoReconnect` | Boolean | 失败时自动重试登录（最多尝试 3 次） |
| `region` | Region | AUTO, US_EAST, US_WEST, EU_WEST |

---

## 发出外拨电话

```kotlin
// Create a new outbound call
telnyxClient.call.newInvite(
    callerName = "John Doe",
    callerNumber = "+15551234567",
    destinationNumber = "+15559876543",
    clientState = "my-custom-state"
)
```

---

## 接收来电

建议使用 SharedFlow 监听套接字事件：

```kotlin
lifecycleScope.launch {
    telnyxClient.socketResponseFlow.collect { response ->
        when (response.status) {
            SocketStatus.ESTABLISHED -> {
                // Socket connected
            }
            SocketStatus.MESSAGERECEIVED -> {
                response.data?.let { data ->
                    when (data.method) {
                        SocketMethod.CLIENT_READY.methodName -> {
                            // Ready to make/receive calls
                        }
                        SocketMethod.LOGIN.methodName -> {
                            // Successfully logged in
                        }
                        SocketMethod.INVITE.methodName -> {
                            // Incoming call!
                            val invite = data.result as InviteResponse
                            // Show incoming call UI, then accept:
                            telnyxClient.acceptCall(
                                invite.callId,
                                invite.callerIdNumber
                            )
                        }
                        SocketMethod.ANSWER.methodName -> {
                            // Call was answered
                        }
                        SocketMethod.BYE.methodName -> {
                            // Call ended
                        }
                        SocketMethod.RINGING.methodName -> {
                            // Remote party is ringing
                        }
                    }
                }
            }
            SocketStatus.ERROR -> {
                // Handle error: response.errorCode
            }
            SocketStatus.DISCONNECT -> {
                // Socket disconnected
            }
        }
    }
}
```

---

## 通话控制

```kotlin
// Get current call
val currentCall: Call? = telnyxClient.calls[callId]

// End call
currentCall?.endCall(callId)

// Mute/Unmute
currentCall?.onMuteUnmutePressed()

// Hold/Unhold
currentCall?.onHoldUnholdPressed(callId)

// Send DTMF tone
currentCall?.dtmf(callId, "1")
```

### 处理多个通话

```kotlin
// Get all active calls
val calls: Map<UUID, Call> = telnyxClient.calls

// Iterate through calls
calls.forEach { (callId, call) ->
    // Handle each call
}
```

---

## 推送通知（FCM）

### 1. 设置 Firebase

将 Firebase 添加到项目中并获取 FCM 令牌：

```kotlin
FirebaseMessaging.getInstance().token.addOnCompleteListener { task ->
    if (task.isSuccessful) {
        val fcmToken = task.result
        // Use this token in your login config
    }
}
```

### 2. 处理收到的推送通知

在您的 `FirebaseMessagingService` 中处理推送通知：

```kotlin
class MyFirebaseService : FirebaseMessagingService() {
    override fun onMessageReceived(remoteMessage: RemoteMessage) {
        val params = remoteMessage.data
        val metadata = JSONObject(params as Map<*, *>).getString("metadata")
        
        // Check for missed call
        if (params["message"] == "Missed call!") {
            // Show missed call notification
            return
        }
        
        // Show incoming call notification (use Foreground Service)
        showIncomingCallNotification(metadata)
    }
}
```

### 3. 拒绝推送呼叫（简化版）

```kotlin
// The SDK now handles decline automatically
telnyxClient.connectWithDeclinePush(
    txPushMetaData = pushMetaData,
    credentialConfig = credentialConfig
)
// SDK connects, sends decline, and disconnects automatically
```

### Android 14+ 版本的要求

```xml
<service
    android:name=".YourForegroundService"
    android:foregroundServiceType="phoneCall"
    android:exported="true" />
```

---

## 通话质量指标

启用指标以实时监控通话质量：

```kotlin
val credentialConfig = CredentialConfig(
    // ... other config
    debug = true  // Enables call quality metrics
)

// Listen for quality updates
lifecycleScope.launch {
    currentCall?.callQualityFlow?.collect { metrics ->
        println("MOS: ${metrics.mos}")
        println("Jitter: ${metrics.jitter * 1000} ms")
        println("RTT: ${metrics.rtt * 1000} ms")
        println("Quality: ${metrics.quality}")  // EXCELLENT, GOOD, FAIR, POOR, BAD
    }
}
```

| 质量等级 | MOS 分数范围 |
|---------------|-----------|
| EXCELLENT | > 4.2 |
| GOOD | 4.1 - 4.2 |
| FAIR | 3.7 - 4.0 |
| POOR | 3.1 - 3.6 |
| BAD | ≤ 3.0 |

---

## 与 AI 代理集成

无需使用传统的 SIP 凭据即可连接到 Telnyx 语音 AI 代理：

### 1. 匿名登录

```kotlin
telnyxClient.connectAnonymously(
    targetId = "your_ai_assistant_id",
    targetType = "ai_assistant",  // Default
    targetVersionId = "optional_version_id",
    userVariables = mapOf("user_id" to "12345")
)
```

### 2. 开始对话

```kotlin
// After anonymous login, call the AI Agent
telnyxClient.newInvite(
    callerName = "User Name",
    callerNumber = "+15551234567",
    destinationNumber = "",  // Ignored for AI Agent
    clientState = "state",
    customHeaders = mapOf(
        "X-Account-Number" to "123",  // Maps to {{account_number}}
        "X-User-Tier" to "premium"    // Maps to {{user_tier}}
    )
)
```

### 3. 接收转录内容

```kotlin
lifecycleScope.launch {
    telnyxClient.transcriptUpdateFlow.collect { transcript ->
        transcript.forEach { item ->
            println("${item.role}: ${item.content}")
            // role: "user" or "assistant"
        }
    }
}
```

### 4. 向 AI 代理发送文本

```kotlin
// Send text message during active call
telnyxClient.sendAIAssistantMessage("Hello, I need help with my account")
```

---

## 自定义日志记录

实现自己的日志记录功能：

```kotlin
class MyLogger : TxLogger {
    override fun log(level: LogLevel, tag: String?, message: String, throwable: Throwable?) {
        // Send to your logging service
        MyAnalytics.log(level.name, tag ?: "Telnyx", message)
    }
}

val config = CredentialConfig(
    // ... other config
    logLevel = LogLevel.ALL,
    customLogger = MyLogger()
)
```

---

## ProGuard 规则

如果使用代码混淆，请将以下规则添加到 `proguard-rules.pro` 文件中：

```proguard
-keep class com.telnyx.webrtc.** { *; }
-dontwarn kotlin.Experimental$Level
-dontwarn kotlin.Experimental
-dontwarn kotlinx.coroutines.scheduling.ExperimentalCoroutineDispatcher
```

---

## 故障排除

| 问题 | 解决方案 |
|-------|----------|
| 无法播放音频 | 确保已授予 `RECORD_AUDIO` 权限 |
| 未收到推送通知 | 验证配置中是否传递了 FCM 令牌 |
| 登录失败 | 验证 Telnyx Portal 中的 SIP 凭据 |
| 通话中断 | 检查网络稳定性，启用 `autoReconnect` 功能 |
| 发送者 ID 不匹配（推送通知） | FCM 项目不匹配——确保应用的 `google-services.json` 文件与服务器凭据一致 |

## 资源

- [官方文档](https://developers.telnyx.com/docs/voice/webrtc/android-sdk/quickstart)
- [推送通知设置](https://developers.telnyx.com/docs/voice/webrtc/android-sdk/push-notification/portal-setup)
- [GitHub 仓库](https://github.com/team-telnyx/telnyx-webrtc-android)