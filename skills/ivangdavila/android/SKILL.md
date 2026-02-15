---
name: android
description: Android 构建系统与部署模式
---

# Android 构建与部署

## ADB 基础知识

```bash
# Debug builds require -t flag (agents forget this)
adb install -r -t app-debug.apk

# Filter logcat for app + errors only
adb logcat -s "YourApp:*" "*:E"
```

## Gradle 的关键修复问题

```gradle
android {
    compileSdk 35
    defaultConfig {
        targetSdk 35  // MUST match or Play Console rejects
        multiDexEnabled true  // Required for 64K+ methods
    }
}

dependencies {
    // BOM prevents Compose version conflicts
    implementation platform('androidx.compose:compose-bom:2024.12.01')
}
```

## Compose 的状态错误

```kotlin
// WRONG - recomputed every recomposition
val filtered = items.filter { it.isValid }

// CORRECT - remember expensive operations  
val filtered = remember(items) { items.filter { it.isValid } }

// WRONG - state resets on recomposition
var count by mutableStateOf(0)

// CORRECT - remember state
var count by remember { mutableStateOf(0) }
```

## AndroidManifest 文件中的常见陷阱

```xml
<!-- Declare camera optional or Play Console auto-requires it -->
<uses-feature android:name="android.hardware.camera" android:required="false" />
```