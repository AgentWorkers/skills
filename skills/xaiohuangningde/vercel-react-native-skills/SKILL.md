---
name: vercel-react-native-skills
description:
  React Native and Expo best practices for building performant mobile apps. Use
  when building React Native components, optimizing list performance,
  implementing animations, or working with native modules. Triggers on tasks
  involving React Native, Expo, mobile performance, or native platform APIs.
license: MIT
metadata:
  author: vercel
  version: '1.0.0'
---
# React Native 技能指南

本指南提供了关于 React Native 和 Expo 应用程序的全面最佳实践，涵盖了性能优化、动画处理、UI 设计模式以及平台特定优化等多个方面的内容。

## 适用场景

在以下情况下，请参考这些指南：
- 构建 React Native 或 Expo 应用程序
- 优化列表和滚动性能
- 使用 Reanimated 实现动画效果
- 处理图片和媒体文件
- 配置原生模块和字体
- 设计包含原生依赖项的单仓库（monorepo）项目结构

## 规则分类（按优先级排序）

| 优先级 | 分类            | 影响程度 | 前缀            |
|--------|----------------|---------|-------------------|
| 1       | 列表性能        | 关键性    | `list-performance-`     |
| 2       | 动画处理        | 高        | `animation-`        |
| 3       | 导航系统        | 高        | `navigation-`       |
| 4       | UI 设计模式      | 高        | `ui-`            |
| 5       | 状态管理        | 中等      | `react-state-`       |
| 6       | 渲染性能        | 中等      | `rendering-`       |
| 7       | 单仓库管理      | 中等      | `monorepo-`        |
| 8       | 配置设置        | 低        | `fonts-`, `imports-`     |

## 快速参考

### 1. 列表性能（关键性）

- `list-performance-virtualize`：对于大型列表，使用 FlashList 来提高性能。
- `list-performance-item-memo`：对列表项组件进行缓存处理，以减少重复计算。
- `list-performance-callbacks`：稳定回调函数的引用，避免不必要的性能开销。
- `list-performance-inline-objects`：避免在列表中直接使用内联样式对象。
- `list-performance-function-references`：将函数提取到渲染过程之外，提高执行效率。
- `list-performance-images`：优化列表中的图片加载方式。
- `list-performance-item-expensive`：将计算密集型操作移到列表项之外，减轻性能负担。
- `list-performance-item-types`：根据列表项的类型进行适当处理，以提高渲染效率。

### 2. 动画处理（高）

- `animation-gpu-properties`：仅对变换和透明度属性进行动画处理，以节省 GPU 资源。
- `animation-derived-value`：使用 `useDerivedValue` 来处理计算型动画。
- `animation-gesture-detector-press`：使用 `Gesture.Tap` 替代 `Pressable` 组件来处理触摸事件。

### 3. 导航系统（高）

- `navigation-native-navigators`：优先使用原生导航组件而非 JavaScript 导航器。

### 4. UI 设计模式（高）

- `ui-expo-image`：统一使用 `expo-image` 组件来显示所有图片。
- `ui-image-gallery`：使用 `Galeria` 组件来创建图片轮播效果。
- `ui-pressable`：使用 `Pressable` 组件替代 ` TouchableOpacity` 组件。
- `ui-safe-area-scroll`：正确处理 `ScrollView` 中的安全区域。
- `ui-scrollview-content-inset`：使用 `contentInset` 属性来设置滚动视图内的内边距。
- `ui-menus`：优先使用原生上下文菜单。
- `ui-native-modals`：尽可能使用原生模态框。
- `ui-measure-views`：使用 `onLayout` 而不是 `measure()` 方法进行布局计算。
- `ui-styling`：使用 `StyleSheet.create` 或 `Nativewind` 进行样式设置。

### 5. 状态管理（中等）

- `react-state-minimize`：减少状态订阅的数量，降低状态更新带来的性能开销。
- `react-state-dispatcher`：使用回调分发器模式来管理状态变化。
- `react-state-fallback`：在首次渲染时显示默认值或备用内容。
- `react-compiler-destructure-functions`：为 React 编译器优化函数结构。
- `react-compiler-reanimated-shared-values`：合理处理共享状态值。

### 6. 渲染性能（中等）

- `rendering-text-in-text-component`：将文本包装在 `Text` 组件中，提高渲染效率。
- `rendering-no-falsy-and`：避免在条件渲染中使用 `false &&` 运算符。

### 7. 单仓库管理（中等）

- `monorepo-native-deps-in-app`：将原生依赖项包含在应用程序包中。
- `monorepo-single-dependency-versions`：确保所有包使用相同的原生依赖版本。

### 8. 配置设置（低）

- `fonts-config-plugin`：使用配置插件来管理自定义字体。
- `imports-design-system-folder`：整理设计系统相关的导入文件。
- `js-hoist-intl`：将国际化（Intl）相关代码统一管理。

## 使用方法

详细说明和代码示例请参阅相应的规则文件：

```
rules/list-performance-virtualize.md
rules/animation-gpu-properties.md
```

每个规则文件包含以下内容：
- 该规则的重要性的简要说明
- 错误的代码示例及其原因
- 正确的代码示例及其实现方式
- 相关的补充信息和参考资料

## 完整文档

如需查看包含所有规则的完整指南，请参阅 `AGENTS.md` 文件。