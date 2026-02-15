---
name: React Native
description: 使用 React Native 组件、导航系统以及原生模块来构建高性能的跨平台移动应用程序。
metadata: {"clawdbot":{"emoji":"📱","requires":{"anyBins":["npx","expo"]},"os":["linux","darwin","win32"]}}
---

# React Native 开发规范

## 组件性能
- 当列表项超过 10 个时，使用 `FlatList`；使用 `ScrollView` 并结合 `map` 会将所有内容加载到内存中，而 `FlatList` 会进行虚拟化处理。
- `keyExtractor` 必须返回稳定且唯一的字符串——使用索引可能会导致重新排序或删除操作时出现问题。
- `React.memo` 可以防止在属性未更改时重新渲染组件——请将纯显示组件包裹在 `React.memo` 中。
- 对传递给子组件的函数，使用 `useCallback`——新的函数引用会触发子组件的重新渲染。
- 避免在 `render` 方法中使用内联样式——每次渲染都会创建新的样式对象，应将其提取到 `StyleSheet.create` 中。

## 状态管理
- `useState` 适用于组件本地状态——对于简单的状态切换，无需使用 Redux 或 Zustand。
- 只将状态提升到最低级别的共同祖先组件——否则会导致不必要的重新渲染。
- 对于计算成本较高的操作，可以使用 `useMemo` 进行缓存——但不要过度使用，因为缓存也会带来开销。
- 当上下文发生变化时，所有依赖该上下文的组件都会重新渲染——请根据更新频率来划分上下文。
- 避免在状态中存储派生数据——应在渲染时根据源状态重新计算相关数据。

## 导航
- React Navigation 是标准导航库——在 Expo 项目中，使用 Expo Router 进行基于文件的路由管理。
- 默认情况下，堆叠的屏幕会保持挂载状态——请在 `useEffect` 的清理逻辑中取消订阅和定时器。
- 仅传递可序列化的参数——函数和复杂对象可能会导致深度链接和状态持久化出现问题。
- 使用 `useFocusEffect` 来处理特定于屏幕的副作用——该效果会在屏幕获得焦点时触发，而不仅仅是组件挂载时。
- 使用 `navigation.reset` 来处理认证流程——这可以清除返回登录页面的逻辑。

## 样式设置
- 将样式代码放在组件体外——这样只需生成一次样式，而不会在每次渲染时都重新生成。
- Flexbox 的默认行为与网页有所不同——使用 `flexDirection: 'column'`，无需添加 `display: flex`。
- 尺寸应使用与设备密度无关的像素单位——不要直接使用设计工具中的像素值。
- 使用 `Platform.select` 来设置特定于平台的样式——这比在样式对象中使用条件语句更简洁。
- 不要使用 CSS 继承——文本样式不会自动应用，每个 `Text` 组件都需要单独设置样式。

## 原生模块
- Expo 模块可以满足大多数开发需求——对于相机、位置、通知等常见功能，无需使用 `eject` 功能。
- `expo-dev-client` 可以在不完全卸载整个应用的情况下启用原生模块——这兼顾了原生功能和 React Native 的优势。
- React Native 的新架构（Fabric、TurboModules）是可选的——在启用之前请检查库的兼容性。
- 原生组件崩溃时不会在 JavaScript 调试器中显示——请查看 Xcode 或 Android Studio 的日志。

## 性能调试
- 确保启用了 Hermes 引擎——这可以显著提升应用启动速度并降低内存消耗。
- 使用 `InteractionManager.runAfterInteractions` 来延迟处理耗时的操作——这样动画效果会更加流畅。
- 对于动画处理，设置 `useNativeDriver: true`——这样动画会在 UI 线程上执行，而不是 JS 线程上。
- 在生产环境中，避免使用 `console.log`——否则会影响性能——可以使用 `__DEV__` 来标记调试代码。
- 使用 Flipper 工具进行调试——它可以帮助分析网络请求、布局和性能问题。

## 图像处理
- 适当设置 `resizeMode`——`cover` 用于裁剪图片，`contain` 用于保持图片在指定区域内，`stretch` 会导致图片变形。
- 为提升用户体验，使用 `Image.prefetch(url)` 预加载图片。
- 本地图片需要明确指定尺寸——对于远程图片，如果知道其中一个尺寸，可以使用宽高比进行缩放。
- 使用 `react-native-svg` 绘制 SVG 图像——SVG 在图标显示方面比 PNG 更适合。
- 使用 `react-native-fast-image` 对远程图片进行缓存——默认的 `Image` 组件没有持久化缓存功能。

## 常见错误
- 不要在 `useEffect` 中直接使用 `async` 关键字——必须先定义一个异步函数，然后再调用它。
- 列表中缺少 `key` 属性会导致警告——请始终使用唯一且稳定的键值。
- 假设 Web 上的 React 开发模式同样适用于 React Native——注意 React Native 没有 DOM 和 CSS，事件系统也有所不同。
- 忘记在 `useEffect` 中进行清理操作——未清理的订阅、定时器和监听器可能会导致资源泄漏。
- 仅在一个平台上进行测试——iOS 和 Android 的行为可能存在差异，请定期在两个平台上进行测试。

## 平台差异
- 在 Android 上，需要明确设置 `overflow: 'hidden'` 以控制边框圆角的显示——iOS 会自动处理边框圆角。
- 阴影效果：iOS 使用 `shadow*` 属性，Android 使用 `elevation` 属性。
- StatusBar 的行为在不同平台上有所不同——请在两个平台上测试其可见性和颜色设置。
- 返回按钮仅存在于 Android 上——请使用 `BackHandler` 或导航监听器来处理返回操作。
- 推送通知的设置因平台而异——需要根据具体平台进行配置。

## 构建与发布
- 使用 `npx react-native clean` 命令清除构建失败的原因——这可以清除缓存和派生数据。
- 在添加原生依赖后，对于 iOS 环境，执行 `cd ios && pod install`；这个步骤经常被忽略。
- 对于 Android 环境，执行 `cd android && ./gradlew clean` 来解决构建问题。
- EAS Build（Expo 提供的构建工具）可以简化持续集成/持续部署流程——它负责处理签名、版本管理和提交流程。
- 在提交之前，请在本地测试发布版本——开发和生产环境中的行为可能会有所不同。