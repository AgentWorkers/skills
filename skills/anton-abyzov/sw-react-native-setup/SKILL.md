---
name: react-native-setup
description: React Native 0.83 及更高版本与 Expo SDK 5.4 及更高版本的环境搭建。Xcode、Android Studio、CocoaPods 的使用，以及 EAS Build 过程中可能遇到的问题排查与解决方案。
---

# React Native 配置专家（2025）

我擅长在 macOS、Windows 和 Linux 系统上配置 React Native 0.83 及更高版本以及 Expo SDK 54 及更高版本的环境。我的专业领域包括新架构的搭建、EAS 构建配置以及开发环境的优化。

## 我的技能

### 先决条件与安装（2025 年的要求）

**Node.js & npm**
- **需要 Node.js 20.x 或更高版本**（Node 18 的支持已于 2025 年 4 月结束）
- 建议使用 Node.js 22 LTS 以获得最佳性能
- 验证版本：`node --version && npm --version`
- 支持的包管理器：npm、yarn、pnpm、bun
- 为 yarn 配置 corepack：`corepack enable && corepack prepare yarn@stable --activate`

**Xcode（macOS - iOS 开发）**
- **需要 Xcode 16.1 或更高版本**（React Native 0.83 的最低要求）
- 建议使用 Xcode 26 以支持 iOS Liquid Glass 功能
- 命令行工具：`xcode-select --install`
- 接受许可证：`sudo xcodebuild -license accept`
- 部署目标至少需要 iOS 15.1
- 为了使用最新功能，建议使用 iOS 18；为了支持 Liquid Glass，建议使用 iOS 26

**Android Studio（Android 开发）**
- **需要 Android Studio Ladybug 或更高版本**（2024.2.1 或更高）
- 必需的 SDK 组件：
  - **Android SDK Platform 35**（API 级别 35）
  - Android SDK Build-Tools 35.0.0
  - Android Emulator
  - Android SDK Platform-Tools
  - **NDK 27.1.12297006**（用于原生模块）
  - CMake 3.22.1 或更高版本（用于 Turbo Modules）
- **配置编译版本（compileSdkVersion）为 35，目标版本（targetSdkVersion）为 35，最小版本（minSdkVersion）为 24**
- 设置 ANDROID_HOME 环境变量
- 支持 Android 15 及更高版本的边缘到边缘显示（edge-to-edge display）

**Watchman**
- 通过 Homebrew 在 macOS 上安装：`brew install watchman`
- 用于快速刷新代码库文件
- 对于大型代码库来说非常重要
- 清除缓存：`watchman watch-del-all`

### 环境配置

**iOS 设置**
- 安装 CocoaPods 1.15 或更高版本：`sudo gem install cocoapods`
- 使用新架构进行 Pod 安装：`RCT_NEW_ARCH_ENABLED=1 pod install`
- 配置 Xcode 项目以使用 Fabric
- 设置 Provisioning Profiles 和证书
- 管理 iOS 模拟器
- 选择设备：`xcrun simctl list devices`
- 测试 Liquid Glass 需要 iOS 26 模拟器

**Android 设置**
- 安装 Gradle 8.10 或更高版本（随 Android Studio Ladybug 自带）
- 配置 Android SDK 路径
- 设置环境变量（ANDROID_HOME, PATH）
- 使用 API 35 图像创建 AVD
- 确保模拟器支持边缘到边缘显示
- 使用 ADB 进行故障排除
- 在 `gradle.properties` 中设置 `newArchEnabled=true`

**Metro Bundler**
- 配置端口 8081
- 清除缓存：`npx react-native start --reset-cache`
- 为新架构配置 Metro
- 支持单仓库（monorepo）的符号链接
- 自定义解析器配置

**EAS 构建设置（Expo）**
- 安装 EAS CLI：`npm install -g eas-cli`
- 登录：`eas login`
- 配置：`eas build:configure`
- 为自定义原生代码生成开发构建
- 使用 EAS 进行 OTA 更新

### 常见问题

**“命令未找到”错误**
- Node.js、Android SDK 和 Xcode 工具的 PATH 配置问题
- Shell 配置文件（.zshrc, .bash_profile）问题
- nvm/fnm 的符号链接问题

**SDK 未找到**
- 验证 SDK 路径：`echo $ANDROID_HOME`
- 检查环境变量
- 重新安装 SDK Manager
- 为原生模块设置 NDK 路径

**Pod 安装失败**
- CocoaPods 版本问题（需要 1.15 或更高版本）
- 在 Apple Silicon 上的 Ffi 包编译错误
- Ruby 版本兼容性问题（使用系统 Ruby 或 rbenv）
- 新架构相关 Pod 安装失败：需要清除并重新构建
- 使用 `pod deintegrate && pod install` 方法

**构建失败**
- 清除构建缓存（参考专业提示）
- 新架构导致的依赖冲突
- 原生模块编译错误
- Xcode 生成的临时文件损坏
- Gradle 缓存损坏

**新架构相关问题**
- Turbo Module 未找到：检查是否运行了 codegen
- Fabric 组件无法渲染：验证原生设置
- Bridge 模块兼容性问题：使用互操作层（interop layer）

## 何时需要我的帮助

当您遇到以下问题时，请联系我：
- 首次配置 React Native 0.83 及更高版本的环境
- 安装和配置 Xcode 16.1 或 Android Studio Ladybug
- 设置 iOS 模拟器或 Android Emulator
- 解决“命令未找到”错误
- 解决 SDK 路径或 ANDROID_HOME 相关问题
- 解决 CocoaPods 安装问题
- 清除 Metro Bundler 缓存
- 配置开发环境变量
- 解决构建失败问题
- 设置 Watchman 以进行文件监控
- 验证开发环境的先决条件
- 配置和排查 EAS 构建问题
- 新架构的搭建和迁移
- 为自定义原生代码生成开发构建
- 设置 Hermes V1 实验性功能

## 快速配置命令

### iOS（macOS）
```bash
# Install Xcode command line tools
xcode-select --install

# Accept Xcode license
sudo xcodebuild -license accept

# Install CocoaPods (1.15+ required)
sudo gem install cocoapods

# Install watchman
brew install watchman

# Verify setup
xcodebuild -version  # Should be 16.1+
pod --version        # Should be 1.15+
watchman version
```

### Android（所有平台）
```bash
# Verify Android setup
echo $ANDROID_HOME
adb --version
emulator -version

# Verify SDK version
$ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager --list | grep "platforms;android-35"

# List available emulators
emulator -list-avds

# List connected devices
adb devices
```

### React Native CLI 项目
```bash
# Create new React Native project (New Architecture enabled by default)
npx @react-native-community/cli init MyProject

# Navigate to project
cd MyProject

# Install iOS dependencies with New Architecture
cd ios && RCT_NEW_ARCH_ENABLED=1 pod install && cd ..

# Start Metro bundler
npm start

# Run on iOS (separate terminal)
npm run ios

# Run on Android (separate terminal)
npm run android
```

### Expo 项目（推荐）
```bash
# Create new Expo project
npx create-expo-app@latest MyProject

# Navigate to project
cd MyProject

# Start development server
npx expo start

# Create development build (for custom native code)
npx expo install expo-dev-client
eas build --profile development --platform ios
eas build --profile development --platform android
```

## 专业提示

1. **清除构建缓存**：遇到问题时，先清除所有构建结果
   ```bash
   # iOS (nuclear option)
   cd ios && rm -rf build Pods Podfile.lock && pod install && cd ..

   # Android
   cd android && ./gradlew clean && cd ..

   # Metro + Watchman
   watchman watch-del-all
   npx react-native start --reset-cache

   # Expo
   npx expo start --clear
   ```

2. **检查环境变量**：更改环境变量后务必进行验证
   ```bash
   # Add to ~/.zshrc or ~/.bash_profile
   export ANDROID_HOME=$HOME/Library/Android/sdk
   export PATH=$PATH:$ANDROID_HOME/emulator
   export PATH=$PATH:$ANDROID_HOME/platform-tools
   export PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin

   # Reload shell
   source ~/.zshrc
   ```

3. **管理模拟器**：列出并启动特定设备
   ```bash
   # iOS
   xcrun simctl list devices
   xcrun simctl boot "iPhone 16 Pro"

   # Android (API 35 for edge-to-edge)
   emulator -list-avds
   emulator -avd Pixel_8_API_35
   ```

4. **快速检查环境状态**：验证整个开发环境
   ```bash
   node --version      # Should be 20+
   npm --version       # npm
   xcodebuild -version # Should be 16.1+
   pod --version       # Should be 1.15+
   adb --version       # Android tools
   watchman version    # Watchman
   eas --version       # EAS CLI (Expo)
   ```

5. **配置 EAS 构建**：eas.json 文件非常重要
   ```json
   {
     "build": {
       "development": {
         "developmentClient": true,
         "distribution": "internal"
       },
       "preview": {
         "distribution": "internal"
       },
       "production": {}
     }
   }
   ```

6. **Hermes V1（实验性）**：启用下一代引擎
   ```javascript
   // metro.config.js
   module.exports = {
     transformer: {
       hermesParser: true,
     },
   };
   ```

   ```bash
   # Verify Hermes is running
   # In app: global.HermesInternal !== undefined
   ```

## 版本兼容性矩阵（2025）

| 组件 | 最低要求 | 推荐版本 | 备注 |
|-----------|---------|-------------|-------|
| Node.js | 20.x | 22 LTS | Node 18 的支持已于 2025 年 4 月结束 |
| React Native | 0.76+ | 0.83 | 自 0.76 版本起默认支持新架构 |
| React | 18.3+ | 19.2 | 新特性（如 Activity, useEffectEvent） |
| Expo SDK | 52+ | 54 | 新功能（如 Native tabs, Liquid Glass） |
| Xcode | 16.1 | 26 | 支持 iOS 26 的 Liquid Glass 功能 |
| Android SDK | 34 | 35 | 支持边缘到边缘显示 |
| CocoaPods | 1.14 | 1.15+ | 新架构兼容性 |
| Gradle | 8.6 | 8.10+ | 支持 K2 编译器 |

## 与 SpecWeave 的集成

我的技能可以与 SpecWeave 的增量工作流程集成：
- 在 `/sw:increment` 计划阶段用于环境配置任务
- 在 `tasks.md` 文件中引用相关的配置标准
- 在 `spec.md` 文件中记录移动开发相关的先决条件
- 在 `reports/` 文件夹中记录配置问题
- 使用 mobile-architect 代理进行架构决策