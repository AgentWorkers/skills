---
name: expo-workflow
description: Expo SDK 54+ 提供了丰富的工作流程，支持轻松构建（EAS Build/Update）和路由管理（Expo Router v6），同时支持原生标签页（native tabs）功能。该 SDK 可用于 Expo 应用程序的开发，以及实现在线软件更新（OTA）策略。
---

# Expo 工作流程专家（SDK 54+）

具备丰富的 Expo SDK 54+ 开发工作流程、EAS（Expo 应用服务）以及快速移动应用开发优化策略方面的专业知识。专注于原生标签页、Expo Router v6、iOS Liquid Glass、Android 边到边显示效果以及现代部署流程。

## 我的专长

### Expo SDK 54 的特性（2025年8月）

**SDK 54 的新功能**
- **原生标签页导航**：通过 React Navigation 7 实现真正的原生标签页导航
- **iOS Liquid Glass 支持**：支持半透明玻璃效果（iOS 26+）
- **Android 边到边显示**：默认采用沉浸式显示效果
- **expo-video** 和 **expo-audio**：新的媒体 API，替代了旧的 expo-av
- **expo-image v2**：使用 useImage 钩子实现命令式的图片加载
- **React Native 0.81**：基于新架构的开发框架
- **改进的开发者体验**：更快的构建速度和更详细的错误信息

**与 SDK 53 的主要变化**
- `expo-av` 被弃用 → 替换为 `expo-video` 和 `expo-audio`
- 原生标签页的导航 API 发生变化
- Android 的边到边显示效果现在成为默认设置（需要调整内边距）

### Expo 基础知识

**托管工作流程与裸工作流程**
- **托管工作流程**：使用完整的 Expo SDK，最小化原生代码的使用
- **裸工作流程**：完全使用原生代码，并通过 Expo 模块进行开发
- **CNG（持续原生生成）**：结合了托管和裸工作流程的优点
- 在不同工作流程之间的迁移策略

**Expo Go 与开发构建**
- **Expo Go**：适用于快速测试，但原生模块功能有限
- **Dev Client**：支持完整的原生模块和自定义构建
- 何时从 Expo Go 转换到开发构建
- 使用 EAS Build 创建自定义的 Dev Client

**Expo SDK 与模块**
- 核心 Expo 模块（expo-camera、expo-location、expo-video、expo-audio）
- 第三方原生模块的兼容性
- 模块安装：`npx expo install <package>`
- 自动处理模块的安装和配置

### EAS 构建（云构建）

**构建配置文件**
- **开发构建**：快速迭代，适用于开发环境
- **预览构建**：用于内部测试和 TestFlight/内部测试
- **生产构建**：提交至 App Store/Play Store
- 在 eas.json 中配置自定义构建选项

**平台特定配置**
- iOS 认证信息管理
- Android 密钥库处理
- 构建缓存策略
- 环境变量注入

**构建优化**
- 缓存 node_modules 和 gradle 依赖项
- 增量构建
- 选择合适的构建机器（如 M1、Ubuntu）
- 优化构建时间

### EAS 更新（OTA 更新）

**空中更新**
- 不需要通过 App Store 即可更新 JavaScript 包
- 支持多种更新渠道和分支
- 提供渐进式或即时更新策略
- 具备回滚功能

**更新工作流程**
- **开发渠道**：持续更新
- **预览渠道**：用于质量保证测试
- **生产渠道**：分阶段发布更新
- 紧急情况下的快速修复流程

**最佳更新实践**
- 管理版本兼容性
- 优化更新频率
- 监控更新 adoption 状态
- 灵活处理更新失败的情况

### 应用配置

**app.json / app.config.js**
- 应用元数据（名称、slug、版本）
- 平台特定的配置
- 资产和图标设置
- 拥抱界面定制
- 深度链接设置（scheme、关联域名）
- 权限配置
- 构建时的环境变量设置

**eas.json**
- 构建配置文件设置
- 提交配置文件管理
- 环境密钥管理
- 平台特定的构建参数

**动态配置**
- 根据环境（开发、测试、生产）调整配置
- 集成功能开关
- 支持应用变体（白标签应用）

### 开发工作流程

**快速刷新与热重载**
- 了解快速刷新的原理
- 解决快速刷新相关的问题
- 确定何时使用完整重载或快速刷新

**调试工具**
- 集成 React DevTools
- 使用 Chrome DevTools 进行远程调试
- 通过 Flipper 进行高级调试
- 检查网络请求
- 分析性能

**本地开发**
- 在真实设备上运行应用（通过 QR 码扫描）
- 在模拟器/虚拟机上运行应用
- 离线开发策略
- Tunnel 模式与 LAN 模式的使用

### 部署与分发

**App Store 提交**
- iOS：集成 TestFlight 和 App Store Connect
- Android：进行内部测试后提交至 Play Store
- 自动化使用 EAS Submit 命令进行提交
- 管理应用商店的元数据

**内部分发**
- 针对 iOS 的临时构建
- 分发 Android APK 文件
- 企业级应用分发
- 使用 TestFlight 进行外部测试

**CI/CD 集成**
- 使用 GitHub Actions 与 EAS Build 集成
- 与 GitLab CI 集成
- 自动触发构建过程
- 在合并代码时自动进行 OTA 更新

## 何时需要我的帮助

当您遇到以下问题时，请联系我：
- 设置 Expo SDK 54+ 的开发工作流程
- 使用 EAS Build 创建开发构建
- 配置 app.json 或 eas.json
- 设置 OTA 更新
- 解决 Expo Go 的限制
- 优化构建时间
- 管理应用认证信息和密钥
- 配置深度链接和 URL 方式
- 设置 Expo 应用的 CI/CD 流程
- 将应用部署到 App Store 或 Play Store
- 了解 Expo SDK 54 的功能
- 从 Expo Go 迁移到 Dev Client
- 管理 Expo 项目中的原生模块
- **实现原生标签页导航**
- **设置 iOS Liquid Glass 效果**
- **配置 Android 边到边显示**
- **从 expo-av 迁移到 expo-video/expo-audio**
- **使用 Expo Router v6 的基于文件的路由**

## 必备的 Expo 命令

### 项目设置
```bash
# Create new Expo project
npx create-expo-app@latest MyApp

# Navigate to project
cd MyApp

# Start development server
npx expo start

# Install Expo module
npx expo install expo-camera

# Check project health
npx expo-doctor
```

### 开发
```bash
# Start with cache cleared
npx expo start -c

# Start with specific mode
npx expo start --dev-client  # Development build
npx expo start --go          # Expo Go

# Run on specific platform
npx expo run:ios
npx expo run:android

# Prebuild native projects (bare workflow)
npx expo prebuild
```

### EAS 构建
```bash
# Login to EAS
eas login

# Configure EAS
eas build:configure

# Build for all platforms
eas build --platform all

# Build development version
eas build --profile development --platform ios

# Build for production
eas build --profile production --platform all

# Check build status
eas build:list
```

### EAS 更新
```bash
# Configure EAS Update
eas update:configure

# Publish update to default channel
eas update --branch production --message "Fix critical bug"

# Publish to specific channel
eas update --channel preview --message "QA testing"

# List published updates
eas update:list

# Rollback update
eas update:rollback
```

### EAS 提交
```bash
# Submit to App Store
eas submit --platform ios

# Submit to Play Store
eas submit --platform android

# Submit specific build
eas submit --platform ios --id <build-id>
```

## 专业技巧与窍门

### 1. 开发构建优化

创建一次可重用的开发构建，然后使用 EAS Update 进行日常更新：
```json
// eas.json
{
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal",
      "ios": {
        "simulator": true
      }
    }
  }
}
```

**一次性构建**：
```bash
eas build --profile development --platform all
```

**每日更新 JavaScript**：
```bash
eas update --branch development --message "Daily changes"
```

### 2. 基于环境的配置**

使用 app.config.js 进行动态配置：
```javascript
// app.config.js
export default ({ config }) => {
  const isProduction = process.env.APP_ENV === 'production';

  return {
    ...config,
    name: isProduction ? 'MyApp' : 'MyApp Dev',
    slug: 'myapp',
    extra: {
      apiUrl: isProduction
        ? 'https://api.myapp.com'
        : 'https://dev-api.myapp.com',
      analyticsKey: process.env.ANALYTICS_KEY,
    },
    updates: {
      url: 'https://u.expo.dev/your-project-id'
    }
  };
};
```

### 3. 自动管理认证信息

让 EAS 自动处理认证信息的配置：
```json
// eas.json
{
  "build": {
    "production": {
      "ios": {
        "credentialsSource": "remote"
      },
      "android": {
        "credentialsSource": "remote"
      }
    }
  }
}
```

### 4. 高效构建缓存

通过缓存依赖项来加速构建过程：
```json
// eas.json
{
  "build": {
    "production": {
      "cache": {
        "key": "myapp-v1",
        "paths": ["node_modules", "ios/Pods", "android/.gradle"]
      }
    }
  }
}
```

### 5. 渐进式 OTA 更新

安全地将更新部署到生产环境：
```bash
# Start with 10% rollout
eas update --branch production --message "New feature" --rollout-percentage 10

# Monitor metrics, then increase
eas update:configure-rollout --branch production --percentage 50

# Full rollout
eas update:configure-rollout --branch production --percentage 100
```

### 6. 在真实设备上进行快速测试

**对于 Expo Go**：适合快速测试：
```bash
# Start dev server
npx expo start

# Scan QR code with:
# - iOS: Camera app
# - Android: Expo Go app
```

**对于 Dev Client**：支持所有功能：
```bash
# Install dev client once
eas build --profile development --platform ios

# Daily JavaScript updates via EAS Update
eas update --branch development
```

### 7. 常见问题排查**

- **“无法解析模块”**
```bash
# Clear Metro cache
npx expo start -c

# Reinstall dependencies
rm -rf node_modules && npm install
```

- **在 EAS 中构建失败**
```bash
# Check build logs
eas build:list
eas build:view <build-id>

# Run prebuild locally to catch issues early
npx expo prebuild
```

- **更新未显示在应用中**
```bash
# Check update channel matches app's channel
eas channel:list

# Verify update was published successfully
eas update:list --branch production

# Force reload in app (shake device → reload)
```

### 8. 第三方原生模块集成**

当需要使用 Expo SDK 未提供的原生模块时：
```bash
# Install the module
npm install react-native-awesome-module

# Prebuild to generate native projects
npx expo prebuild

# Rebuild dev client with new module
eas build --profile development --platform all

# Continue using EAS Update for JS changes
eas update --branch development
```

### 9. 原生标签页导航（SDK 54+）

使用 Expo Router v6 实现真正的原生标签页导航：
```typescript
// app/(tabs)/_layout.tsx
import { Tabs } from 'expo-router';
import { Platform } from 'react-native';

export default function TabLayout() {
  return (
    <Tabs
      screenOptions={{
        // Enable native tabs (iOS has translucent effect by default)
        tabBarStyle: Platform.select({
          ios: { position: 'absolute' }, // For Liquid Glass
          default: {},
        }),
      }}
    >
      <Tabs.Screen
        name="index"
        options={{ title: 'Home', tabBarIcon: ({ color }) => <HomeIcon color={color} /> }}
      />
      <Tabs.Screen
        name="profile"
        options={{ title: 'Profile', tabBarIcon: ({ color }) => <ProfileIcon color={color} /> }}
      />
    </Tabs>
  );
}
```

### 10. iOS Liquid Glass（SDK 54+ / iOS 26+）

创建美观的半透明效果：
```typescript
// components/GlassCard.tsx
import { View, StyleSheet, Platform } from 'react-native';
import { BlurView } from 'expo-blur';

export function GlassCard({ children }) {
  if (Platform.OS === 'ios' && parseInt(Platform.Version, 10) >= 26) {
    return (
      <BlurView
        style={styles.card}
        intensity={60}
        tint="systemMaterial" // Liquid Glass tint
      >
        {children}
      </BlurView>
    );
  }

  return <View style={[styles.card, styles.fallback]}>{children}</View>;
}

const styles = StyleSheet.create({
  card: {
    borderRadius: 16,
    overflow: 'hidden',
  },
  fallback: {
    backgroundColor: 'rgba(255, 255, 255, 0.8)',
  },
});
```

### 11. Android 边到边显示（SDK 54+）

正确处理沉浸式显示效果：
```typescript
// app/_layout.tsx
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { View, StyleSheet, Platform } from 'react-native';

export default function RootLayout() {
  const insets = useSafeAreaInsets();

  return (
    <View
      style={[
        styles.container,
        {
          // Account for edge-to-edge on Android 15+
          paddingTop: insets.top,
          paddingBottom: insets.bottom,
        },
      ]}
    >
      <Slot />
    </View>
  );
}
```

### 12. expo-video（替代 expo-av）

实现现代的视频播放功能：
```typescript
// components/VideoPlayer.tsx
import { useVideoPlayer, VideoView } from 'expo-video';
import { useEvent } from 'expo';
import { StyleSheet, View } from 'react-native';

export function VideoPlayer({ source }: { source: string }) {
  const player = useVideoPlayer(source, (player) => {
    player.loop = true;
    player.play();
  });

  useEvent(player, 'statusChange', ({ status }) => {
    console.log('Player status:', status);
  });

  return (
    <View style={styles.container}>
      <VideoView
        style={styles.video}
        player={player}
        allowsFullscreen
        allowsPictureInPicture
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  video: { width: '100%', aspectRatio: 16 / 9 },
});
```

### 13. expo-audio（替代 expo-av）

实现现代的音频处理功能：
```typescript
// hooks/useAudio.ts
import { useAudioPlayer, useAudioPlayerStatus } from 'expo-audio';

export function useAudio(source: string) {
  const player = useAudioPlayer(source);
  const status = useAudioPlayerStatus(player);

  return {
    play: () => player.play(),
    pause: () => player.pause(),
    seek: (position: number) => player.seekTo(position),
    isPlaying: status.playing,
    position: status.currentTime,
    duration: status.duration,
  };
}
```

### 14. expo-image v2 与 useImage**

使用 useImage 实现命令式的图片加载：
```typescript
import { useImage, Image } from 'expo-image';

export function PreloadedImage({ uri }: { uri: string }) {
  const image = useImage(uri, {
    onError: (error) => console.error('Failed to load image:', error),
  });

  if (!image) {
    return <ActivityIndicator />;
  }

  return (
    <Image
      source={image}
      style={{ width: image.width, height: image.height }}
      contentFit="cover"
    />
  );
}
```

## 与 SpecWeave 的集成

**增量规划**
- 在 `spec.md` 中记录 Expo 的设置步骤
- 在 `plan.md` 中包含 EAS 构建/更新的配置信息
- 在 `tasks.md` 中跟踪构建和部署任务

**测试策略**
- 使用开发构建进行功能开发
- 使用预览构建进行质量保证测试
- 使用生产构建进行利益相关者演示

**动态文档管理**
- 在 `.specweave/docs/internal/operations/` 中记录构建配置文件
- 在运行手册中记录部署流程
- 管理认证信息的相关流程

**成本优化**
- 对于仅涉及 JavaScript 的更改，使用 EAS Update 而不是重新构建
- 缓存依赖项以减少构建时间
- 在增量报告中监控 EAS 的使用情况