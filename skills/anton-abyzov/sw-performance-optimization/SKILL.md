---
name: performance-optimization
description: 使用 Hermes V1、FlashList、expo-image v2 以及并发渲染技术来优化 React Native 应用的性能。这些技术适用于那些运行速度较慢、存在内存泄漏问题或帧率（FPS）不佳的应用程序。
---

# 性能优化专家（RN 0.83+）

专注于为 React Native 0.83+ 和 Expo SDK 54+ 应用程序进行生产环境下的性能优化。精通 Hermes V1、React 19.2 的并发特性、Intersection Observer API、Web 性能 API 以及现代的优化策略。

## 我的专长

### React Native 0.83 的性能特性

**Hermes V1（实验性）**
- 新一代 JavaScript 引擎
- 改进的垃圾回收机制
- 更快的启动速度
- DevTools 的调试功能得到增强
- 可在 `metro.config.js` 中启用：

```javascript
// metro.config.js
module.exports = {
  transformer: {
    hermesParser: true, // Enable Hermes V1 parser
  },
};
```

**React 19.2 的并发特性**
- `Activity` 组件用于状态保存
- `useEffectEvent` 用于稳定的事件处理
- 改进的并发渲染机制
- 在组件切换时更高效的内存管理

```typescript
// Preserve state while hidden (React 19.2)
import { Activity } from 'react';

function TabContent({ isActive, children }) {
  return (
    <Activity mode={isActive ? 'visible' : 'hidden'}>
      {children}
    </Activity>
  );
}
```

**Intersection Observer API（Canary 版本）**
- 为 React Native 实现类似 Web 的懒加载功能
- 无需滚动事件即可检测元素可见性
- 比手动滚动跟踪更高效

```typescript
import { IntersectionObserver } from 'react-native';

// Lazy load when element enters viewport
const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      loadContent();
    }
  });
});
```

**Web 性能 API（稳定版本）**
- `performance.now()` 用于精确的时间测量
- `User Timing API` 用于自定义性能标记
- `PerformanceObserver` 用于性能监控

```typescript
// Performance measurement
const start = performance.now();
await heavyOperation();
const duration = performance.now() - start;

// User Timing API
performance.mark('loadStart');
await loadData();
performance.mark('loadEnd');
performance.measure('dataLoad', 'loadStart', 'loadEnd');

// PerformanceObserver
const observer = new PerformanceObserver((list) => {
  list.getEntries().forEach((entry) => {
    console.log(`${entry.name}: ${entry.duration}ms`);
  });
});
observer.observe({ entryTypes: ['measure'] });
```

### 包大小优化

**分析包大小**
```bash
# Generate bundle stats (Expo)
npx expo export --dump-sourcemap

# Analyze with source-map-explorer
npx source-map-explorer bundles/**/*.map

# Check production bundle size
npx expo export --platform ios
du -sh dist/

# Metro bundle visualizer
npx react-native-bundle-visualizer
```

**减小包大小**
- 使用 `depcheck` 移除未使用的依赖项
- 使用 Hermes V1 生成更小的字节码
- 启用代码压缩和混淆
- 通过“树摇动”（tree shaking）技术移除未使用的代码
- 对重载的屏幕和组件实现懒加载
- 优化资源文件（图片、字体）的大小
- 使用 `expo-image` 替代 `react-native-fast-image`

**Hermes 配置（RN 0.83）**
```javascript
// app.json (Expo SDK 54+)
{
  "expo": {
    "jsEngine": "hermes", // Default in SDK 54
    "ios": {
      "jsEngine": "hermes"
    },
    "android": {
      "jsEngine": "hermes"
    }
  }
}

// For Hermes V1 experimental
// metro.config.js
module.exports = {
  transformer: {
    hermesParser: true,
  },
};
```

### 渲染性能优化

**使用 `React.memo` 优化组件**
```javascript
import React, { memo } from 'react';

// Without memo: Re-renders on every parent render
const UserCard = ({ user }) => (
  <View>
    <Text>{user.name}</Text>
  </View>
);

// With memo: Only re-renders when user prop changes
const UserCard = memo(({ user }) => (
  <View>
    <Text>{user.name}</Text>
  </View>
));

// Custom comparison function
const UserCard = memo(
  ({ user }) => <View><Text>{user.name}</Text></View>,
  (prevProps, nextProps) => prevProps.user.id === nextProps.user.id
);
```

**`useMemo` 和 `useCallback` 的使用**
```javascript
import { useMemo, useCallback } from 'react';

function UserList({ users, onUserPress }) {
  // Expensive calculation - only recalculates when users changes
  const sortedUsers = useMemo(() => {
    console.log('Sorting users...');
    return users.sort((a, b) => a.name.localeCompare(b.name));
  }, [users]);

  // Stable callback reference - prevents child re-renders
  const handlePress = useCallback((userId) => {
    console.log('User pressed:', userId);
    onUserPress(userId);
  }, [onUserPress]);

  return (
    <FlatList
      data={sortedUsers}
      renderItem={({ item }) => (
        <UserItem user={item} onPress={handlePress} />
      )}
      keyExtractor={item => item.id}
    />
  );
}
```

**避免使用内联函数和对象**
```javascript
// ❌ BAD: Creates new function on every render
<TouchableOpacity onPress={() => handlePress(item.id)}>
  <Text style={{ color: 'blue' }}>Press</Text>
</TouchableOpacity>

// ✅ GOOD: Stable references
const styles = StyleSheet.create({
  buttonText: { color: 'blue' }
});

const handleItemPress = useCallback(() => {
  handlePress(item.id);
}, [item.id]);

<TouchableOpacity onPress={handleItemPress}>
  <Text style={styles.buttonText}>Press</Text>
</TouchableOpacity>
```

### 列表性能优化（FlatList/SectionList）

**优化 FlatList 的配置**
```javascript
import { FlatList } from 'react-native';

function OptimizedList({ data }) {
  const renderItem = useCallback(({ item }) => (
    <UserCard user={item} />
  ), []);

  const keyExtractor = useCallback((item) => item.id, []);

  return (
    <FlatList
      data={data}
      renderItem={renderItem}
      keyExtractor={keyExtractor}

      // Performance optimizations
      initialNumToRender={10}          // Render 10 items initially
      maxToRenderPerBatch={10}         // Render 10 items per batch
      windowSize={5}                   // Keep 5 screens worth of items
      removeClippedSubviews={true}     // Unmount off-screen items
      updateCellsBatchingPeriod={50}   // Batch updates every 50ms

      // Memoization
      getItemLayout={getItemLayout}    // For fixed-height items

      // Optional: Performance monitor
      onEndReachedThreshold={0.5}      // Load more at 50% scroll
      onEndReached={loadMoreData}
    />
  );
}

// For fixed-height items (huge performance boost)
const ITEM_HEIGHT = 80;
const getItemLayout = (data, index) => ({
  length: ITEM_HEIGHT,
  offset: ITEM_HEIGHT * index,
  index,
});
```

**FlashList（优于 FlatList）**
```javascript
// Install: npm install @shopify/flash-list
import { FlashList } from "@shopify/flash-list";

function SuperFastList({ data }) {
  return (
    <FlashList
      data={data}
      renderItem={({ item }) => <UserCard user={item} />}
      estimatedItemSize={80}  // Required: approximate item height
    />
  );
}
```

**使用 Intersection Observer 实现懒加载（RN 0.83 Canary 版本）**
```typescript
import { useRef, useEffect, useState } from 'react';
import { View } from 'react-native';

function LazyLoadItem({ onVisible, children }) {
  const ref = useRef(null);
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    if (!ref.current) return;

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && !isVisible) {
          setIsVisible(true);
          onVisible?.();
          observer.disconnect();
        }
      },
      { threshold: 0.1 }
    );

    observer.observe(ref.current);
    return () => observer.disconnect();
  }, []);

  return (
    <View ref={ref}>
      {isVisible ? children : <Placeholder />}
    </View>
  );
}
```

### 图片优化

**推荐使用 `expo-image`（适用于 Expo SDK 54+）**
```typescript
// expo-image is the recommended solution for Expo projects
import { Image, useImage } from 'expo-image';

// Basic usage with blurhash placeholder
function OptimizedImage({ uri, blurhash }) {
  return (
    <Image
      source={{ uri }}
      placeholder={{ blurhash }}
      contentFit="cover"
      transition={200}
      style={{ width: 100, height: 100 }}
      cachePolicy="memory-disk" // Aggressive caching
    />
  );
}

// Imperative loading with useImage hook (v2)
function PreloadedImage({ uri }) {
  const image = useImage(uri, {
    onError: (error) => console.error('Image load failed:', error),
  });

  if (!image) {
    return <ActivityIndicator />;
  }

  return (
    <Image
      source={image}
      style={{ width: image.width / 2, height: image.height / 2 }}
      contentFit="cover"
    />
  );
}
```

**为纯 React Native 项目使用 `Fast Image`**
```javascript
// For bare React Native projects without Expo
// Install: npm install react-native-fast-image
import FastImage from 'react-native-fast-image';

function ProfilePicture({ uri }) {
  return (
    <FastImage
      style={{ width: 100, height: 100 }}
      source={{
        uri: uri,
        priority: FastImage.priority.normal,
        cache: FastImage.cacheControl.immutable
      }}
      resizeMode={FastImage.resizeMode.cover}
    />
  );
}
```

**图片优化的最佳实践**
```javascript
// Use appropriate sizes (not 4K images for thumbnails)
<Image
  source={{ uri: 'https://example.com/image.jpg?w=200&h=200' }}
  style={{ width: 100, height: 100 }}
/>

// Use local images when possible (bundled)
<Image source={require('./assets/logo.png')} />

// Progressive loading with blurhash
import { Image } from 'expo-image';

<Image
  source={{ uri: imageUrl }}
  placeholder={{ blurhash: 'LGF5]+Yk^6#M@-5c,1J5@[or[Q6.' }}
  contentFit="cover"
  transition={300}
  style={{ width: 200, height: 200 }}
/>
```

### 内存管理

**防止内存泄漏**
```javascript
import { useEffect } from 'react';

function Component() {
  useEffect(() => {
    // Set up subscription
    const subscription = api.subscribe(data => {
      console.log(data);
    });

    // Clean up on unmount (CRITICAL!)
    return () => {
      subscription.unsubscribe();
    };
  }, []);

  // Timers
  useEffect(() => {
    const timer = setInterval(() => {
      console.log('Tick');
    }, 1000);

    return () => clearInterval(timer);  // Clean up timer
  }, []);
}
```

**图片内存管理**
```javascript
// Clear image cache when memory warning
import { Platform, Image } from 'react-native';
import FastImage from 'react-native-fast-image';

if (Platform.OS === 'ios') {
  // iOS: Clear cache on memory warning
  DeviceEventEmitter.addListener('RCTMemoryWarning', () => {
    FastImage.clearMemoryCache();
  });
}

// Manual cache clearing
FastImage.clearMemoryCache();
FastImage.clearDiskCache();
```

### 导航性能优化**

**实现屏幕的懒加载**
```javascript
import { lazy, Suspense } from 'react';
import { ActivityIndicator } from 'react-native';

// Lazy load heavy screens
const ProfileScreen = lazy(() => import('./screens/ProfileScreen'));
const SettingsScreen = lazy(() => import('./screens/SettingsScreen'));

function App() {
  return (
    <Suspense fallback={<ActivityIndicator />}>
      <NavigationContainer>
        <Stack.Navigator>
          <Stack.Screen name="Profile" component={ProfileScreen} />
          <Stack.Screen name="Settings" component={SettingsScreen} />
        </Stack.Navigator>
      </NavigationContainer>
    </Suspense>
  );
}
```

**React Navigation 的优化**
```javascript
// Freeze inactive screens (React Navigation v6+)
import { enableScreens } from 'react-native-screens';
enableScreens();

// Detach inactive screens
<Stack.Navigator
  screenOptions={{
    detachPreviousScreen: true,  // Unmount inactive screens
  }}
>
  <Stack.Screen name="Home" component={HomeScreen} />
</Stack.Navigator>
```

### 启动时间优化

**减少初始加载时间**
```javascript
// app.json - Optimize splash screen
{
  "expo": {
    "splash": {
      "image": "./assets/splash.png",
      "resizeMode": "contain",
      "backgroundColor": "#ffffff"
    }
  }
}

// Use Hermes for faster startup
{
  "expo": {
    "jsEngine": "hermes"
  }
}
```

**延迟非关键功能的初始化**
```javascript
import { InteractionManager } from 'react-native';

function App() {
  useEffect(() => {
    // Critical initialization
    initializeAuth();

    // Defer non-critical tasks until after animations
    InteractionManager.runAfterInteractions(() => {
      initializeAnalytics();
      initializeCrashReporting();
      preloadImages();
    });
  }, []);

  return <AppContent />;
}
```

### 动画性能优化**

**使用原生驱动**
```javascript
import { Animated } from 'react-native';

function FadeInView({ children }) {
  const opacity = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    Animated.timing(opacity, {
      toValue: 1,
      duration: 300,
      useNativeDriver: true,  // Runs on native thread (60fps)
    }).start();
  }, []);

  return (
    <Animated.View style={{ opacity }}>
      {children}
    </Animated.View>
  );
}
```

**对复杂动画使用 `Reanimated` 库**
```javascript
// Install: npm install react-native-reanimated
import Animated, { useSharedValue, useAnimatedStyle, withSpring } from 'react-native-reanimated';

function DraggableBox() {
  const offset = useSharedValue(0);

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ translateX: offset.value }],
  }));

  const handlePress = () => {
    offset.value = withSpring(offset.value + 50);
  };

  return (
    <Animated.View style={[styles.box, animatedStyle]}>
      <Text>Drag me</Text>
    </Animated.View>
  );
}
```

## 何时需要我的帮助

当您遇到以下问题时，请联系我：
- 需要减少应用程序的包大小
- 需要优化 FlatList/SectionList 的性能
- 需要修复内存泄漏问题
- 需要提高应用程序的启动速度
- 需要优化图片加载和缓存
- 需要减少组件的重新渲染次数
- 需要实现懒加载功能
- 需要优化导航性能
- 需要分析性能瓶颈
- 需要正确使用 `React.memo`, `useMemo`, `useCallback`
- 需要实现 60fps 的动画效果
- 需要配置 Hermes V1 以获得更好的性能
- 需要使用 `React 19.2` 的 `Activity` 组件来保存状态
- 需要实现基于 `Intersection Observer` 的懒加载功能
- 需要使用 Web 性能 API 进行性能分析
- 需要将项目迁移到 `expo-image v2`

## 性能监控

### React Native 性能监控工具
```javascript
// In app, shake device → Show Perf Monitor
// Shows:
// - JS frame rate
// - UI frame rate
// - RAM usage
```

### 生产环境下的性能监控
```javascript
// Install: npm install @react-native-firebase/perf
import perf from '@react-native-firebase/perf';

// Custom trace
const trace = await perf().startTrace('user_profile_load');
await loadUserProfile();
await trace.stop();

// HTTP monitoring (automatic with Firebase)
import '@react-native-firebase/perf/lib/modular/index';
```

## 专业技巧与建议

### 1. 使用 React DevTools 的性能分析工具进行性能分析**
```javascript
import { Profiler } from 'react';

function onRender(id, phase, actualDuration) {
  if (actualDuration > 16) {  // Slower than 60fps
    console.warn(`Slow render in ${id}: ${actualDuration}ms`);
  }
}

<Profiler id="UserList" onRender={onRender}>
  <UserList users={users} />
</Profiler>
```

### 2. 对耗时较长的操作进行节流处理**
```javascript
import { debounce } from 'lodash';
import { useCallback } from 'react';

function SearchScreen() {
  const debouncedSearch = useCallback(
    debounce((query) => {
      performSearch(query);
    }, 300),
    []
  );

  return (
    <TextInput
      onChangeText={debouncedSearch}
      placeholder="Search..."
    />
  );
}
```

### 3. 对长列表进行虚拟化处理

对于包含大量项的列表，使用 `FlashList` 或 `RecyclerListView` 替代 `ScrollView`：

```javascript
// ❌ BAD: Renders all 1000 items
<ScrollView>
  {items.map(item => <ItemCard key={item.id} item={item} />)}
</ScrollView>

// ✅ GOOD: Only renders visible items
<FlashList
  data={items}
  renderItem={({ item }) => <ItemCard item={item} />}
  estimatedItemSize={100}
/>
```

### 4. 优化样式表（StyleSheets）

```javascript
// ❌ BAD: Creates new style object on every render
<View style={{ backgroundColor: 'red', padding: 10 }} />

// ✅ GOOD: Reuses style object
const styles = StyleSheet.create({
  container: {
    backgroundColor: 'red',
    padding: 10
  }
});

<View style={styles.container} />
```

## 与 SpecWeave 的集成

**性能要求**
- 在 `spec.md` 中记录性能目标（例如：启动时间小于 2 秒）
- 在 `tasks.md` 的测试计划中包含性能测试
- 在性能优化前后进行对比分析

**性能指标**
- 包大小：在增量报告中跟踪变化
- 启动时间：测量并记录优化效果
- 帧率（FPS）：关键用户界面交互的目标值为 60fps
- 内存使用情况：设置阈值并进行监控

**持续更新的文档**
- 记录性能优化策略
- 跟踪各版本之间的包大小变化趋势
- 为常见问题维护性能优化方案