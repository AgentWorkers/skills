---
name: expo-native-ui
model: standard
version: 1.0.0
description: >
  Build beautiful native iOS/Android apps with Expo Router. Covers route structure,
  native tabs, animations, blur effects, liquid glass, SF Symbols, and platform patterns.
tags: [expo, react-native, ios, android, mobile, navigation, animations]
---

# Expo Native UI

使用 Expo Router 按照 Apple 人类界面指南和现代 React Native 模式构建高质量的原生移动应用。

## 安装

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install expo-native-ui
```

## 本技能的作用

本技能指导如何使用 Expo Router 实现原生移动应用，包括：
- 基于文件的路由系统及原生导航栈
- 原生标签页（NativeTabs）和 iOS 26 的新特性
- 通过 `expo-symbols` 集成 SF Symbols 图标
- 模糊效果（expo-blur）和液态玻璃效果（expo-glass-effect）
- 重新动画化的效果和手势处理
- 原生控件：Switch、Slider、SegmentedControl、DateTimePicker

## 适用场景

- 构建新的 Expo Router 应用
- 添加原生标签页导航
- 实现 iOS 风格的模糊或液态玻璃效果
- 创建平滑的进入/退出过渡动画
- 集成 SF Symbols 图标
- 设置带有分组和动态路由的路由结构

## 关键词

expo router, react native, native tabs, sf symbols, expo blur, liquid glass, reanimated, ios, android, mobile app, navigation stack, form sheet, modal, context menu, link preview

## 参考资料

有关详细实现，请参阅以下资源：

| 参考资料 | 用途 |
|-----------|---------|
| `references/route-structure.md` | 路由规范、动态路由、分组、查询参数 |
| `references/tabs.md` | NativeTabs、从 JS 标签页的迁移、iOS 26 的新特性 |
| `references/icons.md` | 使用 `expo-symbols` 的 SF Symbols 图标、动画效果 |
| `references/controls.md` | 原生 iOS 控件：Switch、Slider、DateTimePicker、Picker |
| `references/visual-effects.md` | 模糊效果和液态玻璃效果 |
| `referencesAnimations.md` | 重新动画化的效果：进入、退出、布局、滚动驱动 |
| `references/search.md` | 搜索栏集成、使用 `useSearch` 钩子、过滤功能 |
| `references/gradients.md` | 通过 `experimental-backgroundImage` 实现 CSS 渐变 |
| `references/media.md` | 相机、音频、视频、文件保存 |
| `references/storage.md` | SQLite、AsyncStorage、SecureStore |
| `references/webgpu-three.md` | 使用 WebGPU 和 Three.js 进行 3D 图形处理 |
| `references/toolbar-and-headers.md` | 标签栏和工具栏定制（iOS） |

## 核心原则

### 运行应用

在创建自定义构建之前，**先尝试使用 Expo Go**：

```bash
npx expo start  # Scan QR with Expo Go
```

只有以下情况才需要使用自定义构建（`npx expo run:ios`）：
- 本地 Expo 模块（`modules/` 目录中的自定义原生代码）
- 需要针对 Apple 设备的组件（通过 `@bacons/apple-targets`）
- 未包含在 Expo Go 中的第三方原生模块

### 代码风格

- 文件名采用驼峰式命名法（例如：`comment-card.tsx`）
- 在 `tsconfig` 中使用路径别名以替代相对导入
- **切勿将组件/工具函数放在 `app/` 目录中**
- **确保** 路由匹配 “/”（可能位于某个组内）
- 在字符串中处理嵌套的反引号时要小心

### 库推荐使用

| 推荐库 | 替代库 |
|-----|------------|
| `expo-audio` | `expo-av` |
| `expo-video` | `expo-av` |
| `expo-symbols` | `@expo/vector-icons` |
| `react-native-safe-area-context` | `RN SafeAreaView` |
| `process.env.EXPO_OS` | `Platform.OS` |
| `React.use` | `React.useContext` |
| `expo-image` | 内置的 `img` 元素 |
| `expo-glass-effect` | 自定义的模糊效果视图 |

### 响应式设计

```tsx
// Always wrap root in ScrollView with automatic insets
<ScrollView contentInsetAdjustmentBehavior="automatic">
  {children}
</ScrollView>

// Use useWindowDimensions, not Dimensions.get()
const { width, height } = useWindowDimensions();

// Flexbox over Dimensions API
<View style={{ flex: 1, flexDirection: 'row', gap: 16 }} />
```

## 导航模式

### 带预览和上下文菜单的链接

```tsx
import { Link } from 'expo-router';

<Link href="/settings">
  <Link.Trigger>
    <Pressable><Card /></Pressable>
  </Link.Trigger>
  <Link.Preview />
  <Link.Menu>
    <Link.MenuAction title="Share" icon="square.and.arrow.up" onPress={handleShare} />
    <Link.MenuAction title="Delete" icon="trash" destructive onPress={handleDelete} />
  </Link.Menu>
</Link>
```

### 表单页模态框

```tsx
// In _layout.tsx
<Stack.Screen
  name="sheet"
  options={{
    presentation: "formSheet",
    sheetGrabberVisible: true,
    sheetAllowedDetents: [0.5, 1.0],
    contentStyle: { backgroundColor: "transparent" }, // Liquid glass on iOS 26+
  }}
/>
```

### 原生标签页结构

```
app/
  _layout.tsx — <NativeTabs />
  (index,search)/
    _layout.tsx — <Stack />
    index.tsx
    search.tsx
```

```tsx
// app/_layout.tsx
import { NativeTabs, Icon, Label } from "expo-router/unstable-native-tabs";

export default function Layout() {
  return (
    <NativeTabs>
      <NativeTabs.Trigger name="(index)">
        <Icon sf="list.dash" />
        <Label>Items</Label>
      </NativeTabs.Trigger>
      <NativeTabs.Trigger name="(search)" role="search" />
    </NativeTabs>
  );
}
```

## 样式指南

- 在可能的情况下，使用 `flex gap` 代替 `margin/padding`
- 使用 `borderCurve: 'continuous'` 以实现圆角效果（而非传统的胶囊形边框）
- 使用 `boxShadow` 样式属性，而非旧的 RN 阴影/凸起效果
- 使用 `stack title` 代替自定义文本元素作为页面标题
- 除非需要复用，否则不要使用 `StyleSheet.create` 来创建样式
- 数字计数器使用 `fontVariant: 'tabular-nums`
- 对于可复制的数据，为文本添加 `selectable` 属性

```tsx
// Shadow example
<View style={{ boxShadow: "0 1px 2px rgba(0, 0, 0, 0.05)" }} />

// Continuous border curve
<View style={{ borderRadius: 12, borderCurve: 'continuous' }} />
```

## 行为规范

- **触觉反馈**：在 iOS 上条件性地使用 `expo-haptics`
- **搜索栏**：优先使用 `Stack.Screen` 中的 `headerSearchBarOptions`
- **可选文本**：为重要数据添加 `selectable` 属性
- **格式化大数字**：使用 1.4M 或 38k 而不是 1,400,000
- **切勿在 DOM 组件之外使用** 内置元素（如 `img`、`div`）

## 绝对不要做的事情

1. **绝对不要使用** 旧版本的 React Native 模块：如 `Picker`、`WebView`、`SafeAreaView`、`AsyncStorage`（旧版本）、`expo-permissions`
2. **绝对不要使用** `Dimensions.get()` — 始终使用 `useWindowDimensions`
3. **切勿将组件放在 `app/` 目录中**
4. **绝对不要使用** `Platform.OS` — 使用 `process.env.EXPO_OS`
5. **切勿使用** 旧的阴影样式 — 使用 CSS 的 `boxShadow`
6. **绝对不要** 从自定义构建开始 — 先尝试使用 Expo Go
7. **切勿为一次性样式使用 `StyleSheet.create`
8. **绝对不要使用** `@expo/vector-icons` — 使用 `expo-symbols`