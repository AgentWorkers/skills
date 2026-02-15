---
name: ohos-react-native-performance
description: OpenHarmony React Native 的性能静态检查与优化。本内容基于 ohos_react_native 的性能文档编写，适用于在开发或审查 OpenHarmony 的 React Native 代码时使用，涉及 bundle-harmony、生命周期管理以及 TurboModule 等技术。优化范围包括 RNAbility、Hermes 字节码以及 React 绘制过程的性能提升。
license: MIT
metadata:
  author: OpenHarmony-SIG / homecheck
  repository: https://gitcode.com/openharmony-sig/homecheck
  path_in_repo: skills/ohos-react-native-performance
  source_en: https://gitcode.com/openharmony-sig/ohos_react_native/blob/master/docs/en/performance-optimization.md
  source_zh: https://gitcode.com/openharmony-sig/ohos_react_native/blob/master/docs/zh-cn/性能调优.md
  version: '1.0.0'
---

# OpenHarmony React Native 性能静态检查技巧

这些静态检查规则和配置适用于 OpenHarmony 版本的 React Native，来源于官方的 [性能优化](https://gitcode.com/openharmony-sig/ohos_react_native/blob/master/docs/en/performance-optimization.md) 文档。为减少字符使用量，这些内容仅以英文提供；中文版本可通过以下链接查看。

## 适用场景

在以下情况下使用这些技巧：
- 编写或审查 OpenHarmony 版本的 React Native 应用代码或项目配置
- 优化 React Native 页面渲染、状态更新（setState）或列表性能
- 配置 **bundle-harmony** 构建过程、Hermes 字节码或发布版本
- 集成或审查 **RNAbility** 的生命周期管理（前台/后台切换）
- 设计或实现 **TurboModule**（主线程与工作线程的协同工作）
- 为使用 Trace、React Marker、FCP 等工具进行性能分析做准备

## 规则分类（按优先级）

| 优先级 | 分类            | 影响程度 | 前缀                    |
| -------- | ------------------- | -------- | ------------------------- |
| 1        | 渲染优化 | 关键性    | `rnoh-render-`              |
| 2        | 打包与原生代码     | 高        | `rnoh-bundle-`, `rnoh-native-` |
| 3        | 生命周期与监控     | 高        | `rnoh-lifecycle-`           |
| 4        | TurboModule       | 中等      | `rnoh-turbo-`               |
| 5        | 列表与数据管理     | 中等      | `rnoh-list-`                |

## 快速参考

### 1. 渲染优化（关键性）

- `rnoh-render-avoid-same-state` — 当状态未发生变化时避免使用 `setState`，以防止不必要的重新渲染
- `rnoh-render-pure-memo` — 使用 `PureComponent` 或 `React.memo` 来避免不必要的重新渲染
- `rnoh-render-props-once` — 在构造函数或组件外部仅创建一次属性对象
- `rnoh-render-split-child` — 将独立的 UI 组件拆分为子组件
- `rnoh-render-merge-setstate` — 合并多个 `setState` 调用，以减少提交次数和渲染次数
- `rnoh-render-state-not-mutate` — 在 `setState` 中使用新对象，不要修改现有状态
- `rnoh-render-batching` — 保持 React 18 的自动批处理功能启用（OpenHarmony 默认值为 `concurrentRoot: true`）

### 2. 打包与原生代码配置（高）

- `rnoh-bundle-release` — 使用 `--dev=false --minify=true` 生成性能优化版或生产版包
- `rnoh-bundle-hbc` — 生产版本优先使用 Hermes 字节码（hermesc）
- `rnoh-native-release` — 在原生代码层面使用发布版本；适当降低 `LOG_VERBOSITY_LEVEL`
- `rnoh-native-bisheng` — 可选使用 BiSheng 编译器（`buildOption.nativeCompiler: "BiSheng"`）

### 3. 生命周期与监控（高）

- `rnoh-lifecycle-foreground-background` — 在 `onPageShow/onPageHide` 或 `onShown/onHidden` 事件中处理前台/后台切换
- `rnoh-lifecycle-fcp` — 通过 `mount` 事件或 `root.onLayout` 监控首帧加载时间（FCP）

### 4. TurboModule（中等）

- `rnoh-turbo-worker` — 将计算密集型任务（如 JSON 处理、加密、图像处理、网络请求、I/O 操作）放在工作线程上执行；避免在 worker 线程中使用 `ImageLoader`

### 5. 列表与数据管理（中等）

- `rnoh-list-key` — 为列表项提供稳定的键值对；避免使用索引作为键

## 使用方法

- **静态检查：** 在代码审查或脚本（JS/TS）中应用上述规则。
- **详细信息与示例：** 查看 `rules/` 目录下的相应规则文件（例如 `rules/rnoh-render-pure-memo.md`）。
- **完整文档：** [性能优化（英文版）](https://gitcode.com/openharmony-sig/ohos_react_native/blob/master/docs/en/performance-optimization.md)。

## 与通用 React Native 技巧的关系

- 本技巧专注于 OpenHarmony 版本的 React Native 性能优化（包括 RNAbility、bundle-harmony、HBC、TurboModule、Trace/React Marker 等功能）。
- 它与 **vercel-react-native-skills** 和 **react-native-best-practices** 相辅相成：例如列表虚拟化（FlashList）、可点击元素（Pressable）、图片处理（expo-image）、样式表（StyleSheet）等技巧仍然适用；本技巧补充了 OpenHarmony 特有的配置和渲染优化细节。