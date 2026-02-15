---
name: native-modules
description: React Native的本地模块采用了新架构（New Architecture）、Turbo Modules、JSI（JavaScript Interpreter）以及Codegen技术。这些技术用于将JavaScript代码与Swift或Kotlin编写的本地代码进行桥接（即实现两者之间的交互）。
---

# 本地模块专家（新架构）

专注于将第三方本地模块集成到React Native的新架构中。精通Turbo Modules、JSI、Fabric、Codegen以及现代的本地开发模式。可以使用Context7来获取特定版本的React Native官方文档以获取详细信息。

## 我的专长

### 本地模块基础

**什么是本地模块？**
- JavaScript与平台原生代码之间的直接接口
- 访问平台特定的API（如蓝牙、NFC、HealthKit等）
- 通过JSI执行对性能要求较高的操作
- 与现有的原生SDK集成

**新架构（RN 0.76+ 默认配置）**
- **JSI**（JavaScript Interface）：实现JavaScript与原生代码之间的直接通信（无需JSON序列化）
- **Turbo Modules**：使用Codegen技术实现延迟加载、类型安全的本地模块
- **Fabric**：新的并发渲染引擎
- **Codegen**：将TypeScript代码转换为原生代码

**新架构的主要优势**
- 性能提升10到100倍
- 支持同步方法调用
- 在JavaScript与原生代码之间保持类型安全
- 模块延迟加载（提升应用启动速度）
- 利用Fabric实现并发渲染

### 使用第三方本地模块

**通过Autolinking进行安装**
```bash
# Install module
npm install react-native-camera

# iOS: Install pods (autolinking handles most configuration)
cd ios && pod install && cd ..

# Rebuild the app
npm run ios
npm run android
```

**手动链接（旧版本）**
```bash
# React Native < 0.60 (rarely needed now)
react-native link react-native-camera
```

**与Expo的集成**
```bash
# For Expo managed workflow, use config plugins
npx expo install react-native-camera

# Add plugin to app.json
{
  "expo": {
    "plugins": [
      [
        "react-native-camera",
        {
          "cameraPermission": "Allow $(PRODUCT_NAME) to access your camera"
        }
      ]
    ]
  }
}

# Rebuild dev client
eas build --profile development --platform all
```

### 创建自定义本地模块

**iOS本地模块（Swift）**
```swift
// RCTCalendarModule.swift
import Foundation

@objc(CalendarModule)
class CalendarModule: NSObject {

  @objc
  static func requiresMainQueueSetup() -> Bool {
    return false
  }

  @objc
  func createEvent(_ name: String, location: String, date: NSNumber) {
    // Native implementation
    print("Creating event: \(name) at \(location)")
  }

  @objc
  func getEvents(_ callback: @escaping RCTResponseSenderBlock) {
    let events = ["Event 1", "Event 2", "Event 3"]
    callback([NSNull(), events])
  }

  @objc
  func findEvents(_ resolve: @escaping RCTPromiseResolveBlock, rejecter reject: @escaping RCTPromiseRejectBlock) {
    // Async with Promise
    DispatchQueue.global().async {
      let events = self.fetchEventsFromNativeAPI()
      resolve(events)
    }
  }
}
```

**Android本地模块（Kotlin）**
```objectivec
// RCTCalendarModule.m (Bridge file)
#import <React/RCTBridgeModule.h>

@interface RCT_EXTERN_MODULE(CalendarModule, NSObject)

RCT_EXTERN_METHOD(createEvent:(NSString *)name location:(NSString *)location date:(nonnull NSNumber *)date)

RCT_EXTERN_METHOD(getEvents:(RCTResponseSenderBlock)callback)

RCT_EXTERN_METHOD(findEvents:(RCTPromiseResolveBlock)resolve rejecter:(RCTPromiseRejectBlock)reject)

@end
```

**JavaScript使用方法**
```javascript
// CalendarModule.js
import { NativeModules } from 'react-native';

const { CalendarModule } = NativeModules;

export default {
  createEvent: (name, location, date) => {
    CalendarModule.createEvent(name, location, date);
  },

  getEvents: (callback) => {
    CalendarModule.getEvents((error, events) => {
      if (error) {
        console.error(error);
      } else {
        callback(events);
      }
    });
  },

  findEvents: async () => {
    try {
      const events = await CalendarModule.findEvents();
      return events;
    } catch (error) {
      console.error(error);
      throw error;
    }
  }
};

// Usage in components
import CalendarModule from './CalendarModule';

function MyComponent() {
  const handleCreateEvent = () => {
    CalendarModule.createEvent('Meeting', 'Office', Date.now());
  };

  const handleGetEvents = async () => {
    const events = await CalendarModule.findEvents();
    console.log('Events:', events);
  };

  return (
    <View>
      <Button title="Create Event" onPress={handleCreateEvent} />
      <Button title="Get Events" onPress={handleGetEvents} />
    </View>
  );
}
```

### Turbo Modules（新架构 - RN 0.76+ 默认配置）

**使用Codegen创建Turbo模块**

步骤1：创建TypeScript规范文件（类型定义的来源）：
```typescript
// specs/NativeCalendarModule.ts
import type { TurboModule } from 'react-native';
import { TurboModuleRegistry } from 'react-native';

export interface Spec extends TurboModule {
  // Sync method (fast, blocks JS thread)
  getConstants(): {
    DEFAULT_REMINDER_MINUTES: number;
  };

  // Async methods (recommended for most cases)
  createEvent(name: string, location: string, date: number): Promise<string>;
  findEvents(): Promise<string[]>;
  deleteEvent(eventId: string): Promise<boolean>;

  // Callback-based (legacy pattern, prefer Promise)
  getEventsWithCallback(callback: (events: string[]) => void): void;
}

export default TurboModuleRegistry.getEnforcing<Spec>('CalendarModule');
```

步骤2：在`package.json`中配置Codegen：
```json
{
  "codegenConfig": {
    "name": "CalendarModuleSpec",
    "type": "modules",
    "jsSrcsDir": "specs",
    "android": {
      "javaPackageName": "com.myapp.calendar"
    }
  }
}
```

步骤3：实现原生代码（iOS - Swift）：
```swift
// CalendarModule.swift
import Foundation

@objc(CalendarModule)
class CalendarModule: NSObject {

  @objc static func moduleName() -> String! {
    return "CalendarModule"
  }

  @objc static func requiresMainQueueSetup() -> Bool {
    return false
  }

  @objc func getConstants() -> [String: Any] {
    return ["DEFAULT_REMINDER_MINUTES": 15]
  }

  @objc func createEvent(_ name: String, location: String, date: Double,
                         resolve: @escaping RCTPromiseResolveBlock,
                         reject: @escaping RCTPromiseRejectBlock) {
    DispatchQueue.global().async {
      // Native implementation
      let eventId = UUID().uuidString
      resolve(eventId)
    }
  }

  @objc func findEvents(_ resolve: @escaping RCTPromiseResolveBlock,
                        reject: @escaping RCTPromiseRejectBlock) {
    DispatchQueue.global().async {
      let events = ["Meeting", "Lunch", "Call"]
      resolve(events)
    }
  }

  @objc func deleteEvent(_ eventId: String,
                         resolve: @escaping RCTPromiseResolveBlock,
                         reject: @escaping RCTPromiseRejectBlock) {
    resolve(true)
  }
}
```

步骤4：实现原生代码（Android - Kotlin）：
```kotlin
// CalendarModule.kt
package com.myapp.calendar

import com.facebook.react.bridge.*
import com.facebook.react.module.annotations.ReactModule

@ReactModule(name = CalendarModule.NAME)
class CalendarModule(reactContext: ReactApplicationContext) :
    NativeCalendarModuleSpec(reactContext) {

    companion object {
        const val NAME = "CalendarModule"
    }

    override fun getName(): String = NAME

    override fun getConstants(): MutableMap<String, Any> {
        return mutableMapOf("DEFAULT_REMINDER_MINUTES" to 15)
    }

    override fun createEvent(name: String, location: String, date: Double, promise: Promise) {
        val eventId = java.util.UUID.randomUUID().toString()
        promise.resolve(eventId)
    }

    override fun findEvents(promise: Promise) {
        val events = Arguments.createArray().apply {
            pushString("Meeting")
            pushString("Lunch")
            pushString("Call")
        }
        promise.resolve(events)
    }

    override fun deleteEvent(eventId: String, promise: Promise) {
        promise.resolve(true)
    }
}
```

**Turbo模块的优势**
- **延迟加载**：仅在首次使用时加载
- **类型安全**：Codegen从TypeScript生成原生接口
- **性能提升**：直接使用JSI调用，无需JSON序列化
- **同步调用**：`getConstants()`方法可以同步执行
- **更好的开发体验**：TypeScript错误在编译时就能被捕获

### 原生UI组件

**自定义iOS原生视图（Swift）**
```swift
// RCTCustomViewManager.swift
import UIKit

@objc(CustomViewManager)
class CustomViewManager: RCTViewManager {

  override static func requiresMainQueueSetup() -> Bool {
    return true
  }

  override func view() -> UIView! {
    return CustomView()
  }

  @objc func setColor(_ view: CustomView, color: NSNumber) {
    view.backgroundColor = RCTConvert.uiColor(color)
  }
}

class CustomView: UIView {
  override init(frame: CGRect) {
    super.init(frame: frame)
    self.backgroundColor = .blue
  }

  required init?(coder: NSCoder) {
    fatalError("init(coder:) has not been implemented")
  }
}
```

**自定义Android原生视图（Kotlin）**
```kotlin
// CustomViewManager.kt
class CustomViewManager : SimpleViewManager<View>() {

    override fun getName(): String {
        return "CustomView"
    }

    override fun createViewInstance(reactContext: ThemedReactContext): View {
        return View(reactContext).apply {
            setBackgroundColor(Color.BLUE)
        }
    }

    @ReactProp(name = "color")
    fun setColor(view: View, color: Int) {
        view.setBackgroundColor(color)
    }
}
```

**JavaScript使用方法**
```javascript
import { requireNativeComponent } from 'react-native';

const CustomView = requireNativeComponent('CustomView');

function MyComponent() {
  return (
    <CustomView
      style={{ width: 200, height: 200 }}
      color="red"
    />
  );
}
```

### 常见的本地模块问题

**模块找不到**
```bash
# iOS: Clear build and reinstall pods
cd ios && rm -rf build Pods && pod install && cd ..
npm run ios

# Android: Clean and rebuild
cd android && ./gradlew clean && cd ..
npm run android

# Clear Metro cache
npx react-native start --reset-cache
```

**Autolinking无法正常工作**
```bash
# Verify module in package.json
npm list react-native-camera

# Re-run pod install
cd ios && pod install && cd ..

# Check react-native.config.js for custom linking config
```

**原生应用崩溃**
```bash
# iOS: Check Xcode console for crash logs
# Look for:
# - Unrecognized selector sent to instance
# - Null pointer exceptions
# - Memory issues

# Android: Check logcat
adb logcat *:E
# Look for:
# - Java exceptions
# - JNI errors
# - Null pointer exceptions
```

## 何时需要我的帮助

当您遇到以下问题时，请联系我：
- 集成第三方本地模块
- 创建自定义本地模块
- 解决本地模块安装问题
- 编写iOS原生代码（Swift/Objective-C）
- 编写Android原生代码（Kotlin/Java）
- 调试原生应用崩溃
- 理解Turbo Modules和JSI的工作原理
- 迁移到新架构
- 创建自定义原生UI组件
- 处理平台特定的API
- 解决Autolinking相关问题
- 配置Codegen以实现类型安全
- 创建基于新架构的Fabric组件
- 为同步原生调用编写JSI绑定
- 为Expo项目配置相关插件
- 为旧版本的Bridge模块提供互操作层

## 必需掌握的命令

### 模块开发相关命令**
```bash
# Create module template
npx create-react-native-module my-module

# Build iOS module
cd ios && xcodebuild

# Build Android module
cd android && ./gradlew assembleRelease

# Test module locally
npm link
cd ../MyApp && npm link my-module
```

### 调试原生代码相关命令**
```bash
# iOS: Run with Xcode debugger
open ios/MyApp.xcworkspace

# Android: Run with Android Studio debugger
# Open android/ folder in Android Studio

# Print native logs
# iOS
tail -f ~/Library/Logs/DiagnosticReports/*.crash

# Android
adb logcat | grep "CalendarModule"
```

## 专业技巧与建议

### 1. 使用Codegen实现类型安全的本地模块
利用Codegen技术确保代码的类型安全性：
```typescript
// NativeMyModule.ts
import type { TurboModule } from 'react-native';
import { TurboModuleRegistry } from 'react-native';

export interface Spec extends TurboModule {
  getString(key: string): Promise<string>;
  setString(key: string, value: string): void;
}

export default TurboModuleRegistry.getEnforcing<Spec>('MyModule');
```

### 2. 实现原生代码与JavaScript之间的事件通信
```swift
// iOS - Emit events to JavaScript
import Foundation

@objc(DeviceOrientationModule)
class DeviceOrientationModule: RCTEventEmitter {

  override func supportedEvents() -> [String]! {
    return ["OrientationChanged"]
  }

  @objc
  override static func requiresMainQueueSetup() -> Bool {
    return true
  }

  @objc
  func startObserving() {
    NotificationCenter.default.addObserver(
      self,
      selector: #selector(orientationChanged),
      name: UIDevice.orientationDidChangeNotification,
      object: nil
    )
  }

  @objc
  func stopObserving() {
    NotificationCenter.default.removeObserver(self)
  }

  @objc
  func orientationChanged() {
    let orientation = UIDevice.current.orientation
    sendEvent(withName: "OrientationChanged", body: ["orientation": orientation.rawValue])
  }
}
```

### 3. 带有回调函数的本地模块
```kotlin
// Android - Pass callbacks
@ReactMethod
fun processData(data: String, successCallback: Callback, errorCallback: Callback) {
    try {
        val result = heavyProcessing(data)
        successCallback.invoke(result)
    } catch (e: Exception) {
        errorCallback.invoke(e.message)
    }
}
```

### 4. 尽量避免使用同步原生方法
```swift
// iOS - Synchronous method (blocks JS thread!)
@objc
func getDeviceId() -> String {
    return UIDevice.current.identifierForVendor?.uuidString ?? "unknown"
}
```

**注意**：同步方法会阻塞JavaScript线程，仅适用于执行时间极短（<5毫秒）的操作。

### 5. Expo项目中的配置插件
对于Expo项目，可以使用配置插件来修改原生代码：
```typescript
// plugins/withCalendarPermission.ts
import { ConfigPlugin, withInfoPlist, withAndroidManifest } from '@expo/config-plugins';

const withCalendarPermission: ConfigPlugin = (config) => {
  // iOS: Modify Info.plist
  config = withInfoPlist(config, (config) => {
    config.modResults.NSCalendarsUsageDescription =
      'This app needs calendar access to schedule events';
    return config;
  });

  // Android: Modify AndroidManifest.xml
  config = withAndroidManifest(config, (config) => {
    const mainApplication = config.modResults.manifest.application?.[0];
    if (mainApplication) {
      // Add permissions
      config.modResults.manifest['uses-permission'] = [
        ...(config.modResults.manifest['uses-permission'] || []),
        { $: { 'android:name': 'android.permission.READ_CALENDAR' } },
        { $: { 'android:name': 'android.permission.WRITE_CALENDAR' } },
      ];
    }
    return config;
  });

  return config;
};

export default withCalendarPermission;
```

### 6. 为旧版本的Bridge模块提供互操作层
RN 0.76+版本为旧版本的Bridge模块提供了互操作层：
```typescript
// For legacy modules that don't support Turbo Modules yet
import { NativeModules, TurboModuleRegistry } from 'react-native';

// This works in New Architecture via interop layer
const LegacyModule = NativeModules.LegacyBridgeModule;

// Or use the Turbo Module if available
const TurboModule = TurboModuleRegistry.get('ModernModule');

// Recommended: Create a wrapper that handles both
export function getCalendarModule() {
  // Try Turbo Module first
  const turbo = TurboModuleRegistry.get('CalendarModule');
  if (turbo) return turbo;

  // Fall back to Bridge module via interop
  return NativeModules.CalendarModule;
}
```

## 与SpecWeave的集成

**本地模块规划**
- 在`spec.md`文件中记录本地模块的依赖关系
- 在`plan.md`文件中说明本地模块的配置方式
- 将本地代码编译步骤添加到`tasks.md`文件中

**测试策略**
- 分别对原生代码进行单元测试
- 测试JavaScript与原生代码之间的交互
- 在iOS和Android平台上进行联合测试
- 记录平台特定的行为

**文档编写**
- 为本地模块API编写详细的文档
- 说明平台特定的特性
- 为常见的本地问题准备解决方案文档