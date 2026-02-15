---
name: mobile-debugging
description: 使用 Flipper、React DevTools 进行 React Native 应用调试，并进行崩溃分析。这些工具适用于移动应用调试以及网络请求相关问题的排查。
---

# 移动应用调试专家

专注于在 iOS 和 Android 平台上调试 React Native 以及 Expo 应用程序。擅长使用调试工具、分析应用程序崩溃、进行网络调试，并解决常见的 React Native 相关问题。

## 我的技能

### 调试工具

**React DevTools**
- 组件树查看
- 属性和状态检查
- 性能分析工具
- 组件重新渲染跟踪
- 安装方式：`npm install -g react-devtools`
- 使用方法：在启动应用程序前运行 `react-devtools`

**Chrome DevTools（远程调试）**
- JavaScript 调试器
- 断点设置和逐步执行调试
- 控制台用于日志记录和代码评估
- 网络标签页用于 API 监控
- 源代码映射功能

**Flipper（Meta 的调试平台）**
- UI 调试工具
- 带有请求/响应详细信息的网络调试工具
- 可过滤的日志查看器
- 集成了 React DevTools 插件
- 数据库调试工具
- 支持崩溃报告功能
- 性能指标监控

**React Native Debugger（独立工具）**
- 一站式调试解决方案
- 集成了 Redux DevTools 和 React DevTools
- 支持网络调试
- 可查看 AsyncStorage 数据

### 调试技巧

**控制台日志记录策略**
```javascript
// Basic logging
console.log('Debug:', value);

// Structured logging
console.log({
  component: 'UserProfile',
  action: 'loadData',
  userId: user.id,
  timestamp: new Date().toISOString()
});

// Conditional logging
if (__DEV__) {
  console.log('Development only:', debugData);
}

// Performance logging
console.time('DataLoad');
await fetchData();
console.timeEnd('DataLoad');

// Table logging for arrays
console.table(users);
```

**断点调试**
```javascript
// Debugger statement
function processData(data) {
  debugger; // Execution pauses here when debugger attached
  return data.map(item => transform(item));
}

// Conditional breakpoints in DevTools
// Right-click on line number → Add conditional breakpoint
// Condition: userId === '12345'
```

**错误边界检测**
```javascript
import React from 'react';
import { View, Text } from 'react-native';

class ErrorBoundary extends React.Component {
  state = { hasError: false, error: null };

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    // Log to error tracking service
    console.error('Error caught:', error, errorInfo);
    logErrorToService(error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <View>
          <Text>Something went wrong.</Text>
          <Text>{this.state.error?.message}</Text>
        </View>
      );
    }

    return this.props.children;
  }
}

// Usage
<ErrorBoundary>
  <App />
</ErrorBoundary>
```

### 网络调试

**拦截网络请求**
```javascript
// Using Flipper (recommended)
// Automatically intercepts fetch() and XMLHttpRequest

// Manual interception for custom debugging
const originalFetch = global.fetch;
global.fetch = async (...args) => {
  console.log('Fetch Request:', args[0], args[1]);
  const response = await originalFetch(...args);
  console.log('Fetch Response:', response.status);
  return response;
};

// Using React Native Debugger Network tab
// Automatically works with fetch() and axios
```

**API 响应调试**
```javascript
// Wrapper for API calls with detailed logging
async function apiCall(endpoint, options = {}) {
  const startTime = Date.now();

  try {
    const response = await fetch(endpoint, options);
    const duration = Date.now() - startTime;

    console.log({
      endpoint,
      method: options.method || 'GET',
      status: response.status,
      duration: `${duration}ms`,
      success: response.ok
    });

    if (!response.ok) {
      const error = await response.text();
      console.error('API Error Response:', error);
      throw new Error(`API Error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('API Call Failed:', {
      endpoint,
      error: error.message,
      duration: `${Date.now() - startTime}ms`
    });
    throw error;
  }
}
```

### 平台特定调试

**iOS 调试**
- 使用 Safari Web Inspector 进行 JavaScript 调试
- 通过 Xcode 控制台查看原生日志
- 使用 Instruments 进行性能分析
- 崩溃日志位置：`~/Library/Logs/DiagnosticReports/`
- 系统日志位置：`log stream --predicate 'processImagePath contains "MyApp"'`

**Android 调试**
- 使用 Chrome DevTools 进行 JavaScript 调试
- 通过 Android Studio 的 Logcat 查看系统日志
- 使用 ADB 过滤 Logcat 日志（仅显示错误信息）：`adb logcat *:E`
- 查看原生崩溃日志：`adb logcat AndroidRuntime:E`
- 监控设备状态：`adb shell top`

### 常见调试场景

- 应用程序启动时崩溃
```bash
# iOS: Check Xcode console
# Open Xcode → Window → Devices and Simulators → Select device → View logs

# Android: Check logcat
adb logcat *:E

# Look for:
# - Missing native modules
# - JavaScript bundle errors
# - Permission issues
# - Initialization errors
```

- 应用程序显示白屏或空白屏幕
```javascript
// Add error boundary to root
import { ErrorBoundary } from 'react-error-boundary';

function ErrorFallback({ error }) {
  return (
    <View>
      <Text>App crashed: {error.message}</Text>
    </View>
  );
}

<ErrorBoundary FallbackComponent={ErrorFallback}>
  <App />
</ErrorBoundary>
```

- 应用程序出现红色错误提示
```javascript
// Globally catch errors in development
if (__DEV__) {
  ErrorUtils.setGlobalHandler((error, isFatal) => {
    console.log('Global Error:', { error, isFatal });
    // Log to crash reporting service in production
  });
}
```

- 网络请求失败
```bash
# Check if Metro bundler is accessible
curl http://localhost:8081/status

# Check if API is accessible from device
# iOS Simulator: localhost works
# Android Emulator: use 10.0.2.2 instead of localhost
# Real device: use computer's IP address

# Test network connectivity
adb shell ping 8.8.8.8  # Android
```

- 性能问题
```javascript
// Use React DevTools Profiler
import { Profiler } from 'react';

function onRenderCallback(
  id,
  phase,
  actualDuration,
  baseDuration,
  startTime,
  commitTime
) {
  console.log({
    component: id,
    phase,
    actualDuration,
    baseDuration
  });
}

<Profiler id="App" onRender={onRenderCallback}>
  <App />
</Profiler>
```

## 何时需要我的帮助

当您遇到以下问题时，请联系我：
- 设置调试工具（如 Flipper、React DevTools）
- 调试应用程序崩溃或错误界面
- 检查网络请求和响应
- 查找性能瓶颈
- 分析组件重新渲染的情况
- 调试原生模块问题
- 阅读崩溃日志和堆栈跟踪信息
- 设置错误边界
- 在真实设备上进行远程调试
- 解决平台特定问题
- 故障排除（如应用程序显示白屏）
- 检查 AsyncStorage 或数据库数据

## 必需的调试命令

### 开始调试
```bash
# Open React DevTools
react-devtools

# Start app with remote debugging
npm start

# In app: Shake device → Debug Remote JS
# Or: Press "d" in Metro bundler terminal
```

### 查看平台日志
```bash
# iOS System Logs (real device)
idevicesyslog

# iOS Simulator Logs
xcrun simctl spawn booted log stream --level=debug

# Android Logs (all)
adb logcat

# Android Logs (app only, errors)
adb logcat *:E | grep com.myapp

# Android Logs (React Native only)
adb logcat ReactNative:V ReactNativeJS:V *:S

# Clear Android logs
adb logcat -c
```

### 性能分析
```bash
# iOS: Use Instruments
# Xcode → Open Developer Tool → Instruments → Time Profiler

# Android: Use Systrace
react-native log-android

# React Native performance monitor
# Shake device → Show Perf Monitor
```

### 设置 Flipper
```bash
# Install Flipper Desktop
brew install --cask flipper

# For Expo dev clients, add to app.json:
{
  "expo": {
    "plugins": ["react-native-flipper"]
  }
}

# Rebuild dev client
eas build --profile development --platform all
```

## 专业技巧与窍门

### 1. 自定义调试菜单
- 向调试菜单中添加自定义调试工具
```javascript
import { DevSettings } from 'react-native';

if (__DEV__) {
  DevSettings.addMenuItem('Clear AsyncStorage', async () => {
    await AsyncStorage.clear();
    console.log('AsyncStorage cleared');
  });

  DevSettings.addMenuItem('Log Redux State', () => {
    console.log('Redux State:', store.getState());
  });

  DevSettings.addMenuItem('Toggle Debug Mode', () => {
    global.DEBUG = !global.DEBUG;
    console.log('Debug mode:', global.DEBUG);
  });
}
```

### 2. 网络请求日志记录器
- 实现全面的网络调试功能
```javascript
// Create a network logger file
import axios from 'axios';

if (__DEV__) {
  axios.interceptors.request.use(
    (config) => {
      console.log('→ API Request', {
        method: config.method?.toUpperCase(),
        url: config.url,
        data: config.data,
        headers: config.headers
      });
      return config;
    },
    (error) => {
      console.error('→ Request Error', error);
      return Promise.reject(error);
    }
  );

  axios.interceptors.response.use(
    (response) => {
      console.log('← API Response', {
        status: response.status,
        url: response.config.url,
        data: response.data
      });
      return response;
    },
    (error) => {
      console.error('← Response Error', {
        status: error.response?.status,
        url: error.config?.url,
        data: error.response?.data
      });
      return Promise.reject(error);
    }
  );
}
```

### 3. React Query DevTools（用于数据获取）
- 使用 React Query DevTools 监控数据请求
```javascript
import { useReactQueryDevTools } from '@tanstack/react-query-devtools';

function App() {
  // Development only
  if (__DEV__) {
    useReactQueryDevTools();
  }

  return <YourApp />;
}
```

### 4. 调试状态更新
- 通过自定义钩子跟踪状态变化
```javascript
import { useEffect, useRef } from 'react';

function useTraceUpdate(props, componentName) {
  const prev = useRef(props);

  useEffect(() => {
    const changedProps = Object.entries(props).reduce((acc, [key, value]) => {
      if (prev.current[key] !== value) {
        acc[key] = {
          from: prev.current[key],
          to: value
        };
      }
      return acc;
    }, {});

    if (Object.keys(changedProps).length > 0) {
      console.log(`[${componentName}] Changed props:`, changedProps);
    }

    prev.current = props;
  });
}

// Usage
function MyComponent(props) {
  useTraceUpdate(props, 'MyComponent');
  return <View>...</View>;
}
```

### 5. 调试离线/在线状态
- 确保应用程序在离线/在线状态下都能正常工作
```javascript
import NetInfo from '@react-native-community/netinfo';

// Monitor network state
NetInfo.addEventListener(state => {
  console.log('Network State:', {
    isConnected: state.isConnected,
    type: state.type,
    isInternetReachable: state.isInternetReachable
  });
});
```

### 6. 生产环境错误追踪
- 集成错误追踪服务（如 Sentry、Bugsnag）
```javascript
// Using Sentry (example)
import * as Sentry from '@sentry/react-native';

Sentry.init({
  dsn: 'YOUR_SENTRY_DSN',
  enableInExpoDevelopment: true,
  debug: __DEV__
});

// Capture custom errors
try {
  await riskyOperation();
} catch (error) {
  Sentry.captureException(error, {
    tags: { feature: 'user-profile' },
    extra: { userId: user.id }
  });
}
```

## 与 SpecWeave 的集成

**开发阶段**
- 在 `reports/` 文件中记录调试方法
- 在 `spec.md` 中记录已知问题及解决方法
- 在 `tasks.md` 的测试计划中包含调试步骤

**生产环境监控**
- 为所有功能设置错误边界
- 集成崩溃报告系统（如 Sentry、Bugsnag）
- 在运行手册中记录调试流程
- 在实时文档中跟踪常见错误