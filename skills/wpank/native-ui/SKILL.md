---
name: native-ui
model: standard
version: 1.0.0
description: >
  Building native mobile UIs with Expo Router and React Native. Covers routing,
  navigation, styling, native controls, animations, and platform conventions
  following Apple Human Interface Guidelines.
tags: [expo, react-native, ios, mobile, navigation, native-ui]
---

# 使用 Expo Router 的原生 UI

使用 Expo Router 和 React Native 构建原生移动应用程序的模式和惯例。

## 参考资料

根据需要查阅以下文档：

- `./references/route-structure.md` — 路由规范、动态路由、路由组、文件夹组织结构
- `./references/tabs.md` — 原生标签栏（使用 NativeTabs 实现），支持 iOS 26 的特性
- `./references/icons.md` — 使用 expo-symbols 提供的 SF Symbols 图标，包括图标名称和动画效果
- `./references/controls.md` — 原生 iOS 控件：Switch、Slider、SegmentedControl、DateTimePicker
- `./references/visual-effects.md` — 模糊效果（expo-blur）和液态玻璃效果（expo-glass-effect）
- `./references/animations.md` — 动画效果：进入/离开屏幕、布局变化、滚动操作、手势交互
- `./references/search.md` — 搜索栏，包括搜索框和过滤功能
- `./references/gradients.md` — 通过 experimental-backgroundImage 实现 CSS 渐变效果（仅适用于新架构）
- `./references/media.md` — 相机、音频、视频处理及文件保存功能
- `./references/storage.md` — SQLite、AsyncStorage、SecureStore 数据存储
- `./references/webgpu-three.md` — 使用 WebGPU/Three.js 实现 3D 图形和 GPU 可视化
- `./references toolbar-and-headers.md` — 带有按钮和菜单的导航栏（iOS 版本）
- `./references/form-sheet.md` — 表单组件的展示方式

## 运行应用程序

**在创建自定义构建之前，请务必先尝试使用 Expo Go。**

1. 使用 `npx expo start` 启动应用程序，并扫描 QR 码。
2. 在 Expo Go 中测试应用程序的功能。
3. 仅在需要时才创建自定义构建。

### 需要创建自定义构建的情况

仅在使用以下情况时使用 `npx expo run:ios/android` 或 `eas build`：

- 本地 Expo 模块（位于 `modules/` 目录中的自定义原生代码）
- Apple 平台的目标应用（使用 `@bacons/apple-targets`）
- 未包含在 Expo Go 中的第三方原生模块
- 需要修改 `app.json` 中的自定义原生配置

Expo Go 支持所有的 `expo-*` 包、Expo Router、Reanimated、Gesture Handler、推送通知以及深度链接功能。

## 安装

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install native-ui
```

---

## 代码风格规范

- 正确处理嵌套的反引号和引号。
- 文件开头必须包含导入语句。
- 文件名应使用驼峰式命名法（例如：`comment-card.tsx`）。
- 重构导航结构时，请删除旧的路由文件。
- 文件名中不允许使用特殊字符。
- 配置 `tsconfig.json` 中的路径别名；优先使用别名而非相对导入。

## 路由规则

详细规范请参阅 `./references/route-structure.md`：

- 路由文件应放在 `app` 目录下。
- 组件、类型或工具类不应与路由文件放在同一目录下（这是反模式）。
- 必须存在一个匹配 `/` 的路由，该路由可能位于某个路由组内。

## 库的替代使用

| 库名 | 替代库名 |
|-----|------------|
| `expo-audio` | `expo-av` |
| `expo-video` | `expo-av` |
| `expo-symbols` | `@expo/vector-icons` |
| `react-native-safe-area-context` | `RN SafeAreaView` |
| `process.env.EXPO_OS` | `Platform.OS` |
| `React.use` | `React.useContext` |
| `expo-image` | 内置的 `img` 元素 |
| `expo-glass-effect` | 自定义的玻璃背景效果 |

请避免使用已弃用的模块：Picker、WebView、SafeAreaView、AsyncStorage（来自 RN 核心库），以及旧的 `expo-permissions`。

---

## 响应式设计

- 将根组件包裹在 `ScrollView` 中。
- 使用 `<ScrollView contentInsetAdjustmentBehavior="automatic" />` 代替 `<SafeAreaView>`。
- 也应用 `contentInsetAdjustmentBehavior="automatic"` 到 `FlatList` 和 `SectionList` 上。
- 使用 flexbox 替代 `Dimensions` API 进行屏幕尺寸获取。
- 使用 `useWindowDimensions` 而不是 `Dimensions.get()` 来获取屏幕尺寸。

## 行为规范

- 在 iOS 上根据需要条件性地使用 `expo-haptics` 以实现更好的交互体验。
- 使用具有内置触觉效果的视图（如 `<Switch />`、`@react-native-community/datetimepicker`）。
- `Stack` 路由的第一个子元素通常应该是 `contentInsetAdjustmentBehavior="automatic"` 的 `ScrollView`。
- 对于搜索栏，建议使用 `Stack.Screen` 选项中的 `headerSearchBarOptions`。
- 对于用户可能想要复制的文本，使用 `<Text selectable />`。
- 大数字的格式化方式：1.4M、38k。
- 请勿在 WebView 或 Expo DOM 组件之外使用内置元素（如 `img`、`div`）。

## 样式设计

遵循 Apple 人类界面指南：

- 相比边距（margin）和内边距（padding），优先使用弹性间距（flex gap）。
- 相比内边距（padding），优先使用内边距（padding）。
- 通过导航栏、标签栏或 `contentInsetAdjustmentBehavior="automatic"` 确保安全区域（safe area）得到处理。
- 除非需要重用样式，否则优先使用内联样式（inline styles）而非 `StyleSheet.create`。
- 为状态变化添加进入/离开屏幕的动画效果。
- 使用 `{ borderCurve: 'continuous' }` 以实现圆角效果（而非胶囊形状）。
- 使用导航栏标题（navigation stack title）代替自定义文本标题。
- 在 `ScrollView` 中使用 `contentContainerStyle` 来设置内边距/间距（避免裁剪问题）。
- 不支持 CSS 和 Tailwind，请使用内联样式。

### 文本样式

- 对于显示重要数据或错误的 `<Text/>` 元素，添加 `selectable` 属性。
- 对于计数器，使用 `{ fontVariant: 'tabular-nums' }` 来对齐文本。

### 阴影效果

使用 CSS 的 `boxShadow` 样式属性。请勿使用旧版的 RN 阴影效果或 `elevation` 样式。

```tsx
<View style={{ boxShadow: "0 1px 2px rgba(0, 0, 0, 0.05)" }} />
```

支持内边距阴影（Inset shadows）。

---

## 导航功能

### 链接（Links）

使用 `expo-router` 提供的 `<Link href="/path" />` 进行导航。

```tsx
import { Link } from 'expo-router';

<Link href="/path" />

<Link href="/path" asChild>
  <Pressable>...</Pressable>
</Link>
```

尽可能使用 `<Link.Preview>` 来遵循 iOS 的规范，并添加上下文菜单和预览功能。

### 导航栈（Navigation Stack）

- 使用 `_layout.tsx` 文件来定义导航栈结构。
- 使用 `expo-router/stack` 中的 `Stack` 组件来实现原生导航。
- 在 `Stack.Screen` 选项中设置页面标题：`options={{ title: "Home" }}`。

### 上下文菜单（Context Menus）

为 `<Link>` 组件添加长按触发的上下文菜单：

```tsx
<Link href="/settings" asChild>
  <Link.Trigger>
    <Pressable><Card /></Pressable>
  </Link.Trigger>
  <Link.Menu>
    <Link.MenuAction title="Share" icon="square.and.arrow.up" onPress={handleShare} />
    <Link.MenuAction title="Block" icon="nosign" destructive onPress={handleBlock} />
    <Link.Menu title="More" icon="ellipsis">
      <Link.MenuAction title="Copy" icon="doc.on.doc" onPress={() => {}} />
      <Link.MenuAction title="Delete" icon="trash" destructive onPress={() => {}} />
    </Link.Menu>
  </Link.Menu>
</Link>
```

### 链接预览（Link Previews）

```tsx
<Link href="/settings">
  <Link.Trigger>
    <Pressable><Card /></Pressable>
  </Link.Trigger>
  <Link.Preview />
</Link>
```

可以结合上下文菜单一起使用。

### 模态框（Modal）

将屏幕以模态框的形式展示：

```tsx
<Stack.Screen name="modal" options={{ presentation: "modal" }} />
```

建议使用这种方式而不是自定义的模态框组件。

### 表单组件（Form Sheets）

将表单组件以动态形式展示：

```tsx
<Stack.Screen
  name="sheet"
  options={{
    presentation: "formSheet",
    sheetGrabberVisible: true,
    sheetAllowedDetents: [0.5, 1.0],
    contentStyle: { backgroundColor: "transparent" },
  }}
/>
```

`contentStyle: { backgroundColor: "transparent" }` 可以在 iOS 26 及更高版本上实现液态玻璃效果。

---

## 常见的路由结构

标准的应用程序布局包含标签栏和导航栈：

```
app/
  _layout.tsx        — <NativeTabs />
  (index,search)/
    _layout.tsx      — <Stack />
    index.tsx        — Main list
    search.tsx       — Search view
```

**根布局（Root Layout）：**

```tsx
// app/_layout.tsx
import { NativeTabs, Icon, Label } from "expo-router/unstable-native-tabs";
import { Theme } from "../components/theme";

export default function Layout() {
  return (
    <Theme>
      <NativeTabs>
        <NativeTabs.Trigger name="(index)">
          <Icon sf="list.dash" />
          <Label>Items</Label>
        </NativeTabs.Trigger>
        <NativeTabs.Trigger name="(search)" role="search" />
      </NativeTabs>
    </Theme>
  );
}
```

**共享组件布局（Shared Component Layout）：**

```tsx
// app/(index,search)/_layout.tsx
import { Stack } from "expo-router/stack";
import { PlatformColor } from "react-native";

export default function Layout({ segment }) {
  const screen = segment.match(/\((.*)\)/)?.[1]!;
  const titles: Record<string, string> = { index: "Items", search: "Search" };

  return (
    <Stack
      screenOptions={{
        headerTransparent: true,
        headerShadowVisible: false,
        headerLargeTitleShadowVisible: false,
        headerLargeStyle: { backgroundColor: "transparent" },
        headerTitleStyle: { color: PlatformColor("label") },
        headerLargeTitle: true,
        headerBlurEffect: "none",
        headerBackButtonDisplayMode: "minimal",
      }}
    >
      <Stack.Screen name={screen} options={{ title: titles[screen] }} />
      <Stack.Screen name="i/[id]" options={{ headerLargeTitle: false }} />
    </Stack>
  );
}
```