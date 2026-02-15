---
name: PagerKit
description: '关于PagerKit的专家指导：PagerKit是一个用于实现高级、可定制的基于页面的导航功能的SwiftUI库。以下是开发者经常提到的相关内容：

1. **PagerKit、PKPagesView、PKPage**：这些是PagerKit中的核心组件，用于构建页面导航系统。
2. **自定义页面控件、指示器及分页行为**：开发者可以使用PagerKit来创建自定义的页面控件，并自定义分页逻辑和指示器的显示方式。
3. **跨平台的SwiftUI分页功能**：PagerKit支持在各种iOS和macOS设备上实现一致的分页体验。
4. **动态页面生成**：通过PagerKit，可以动态生成页面内容，以满足用户需求。
5. **将页面视图集成到自定义布局中**：开发者可以将PagerKit提供的页面视图轻松地融入到自己的应用程序布局中。
6. **特定的PagerKit修饰符和枚举**：PagerKit提供了一些额外的修饰符和枚举，用于进一步定制分页行为。
7. **页面视图控制器选项**：了解如何配置和使用PagerKit提供的页面视图控制器。
8. **页面切换事件处理**：掌握如何处理页面切换时发生的事件，以确保应用程序的流畅性。

当您在软件文档中看到上述关键词时，可以参考这些专家指导来理解相关功能的实现原理和使用方法。'
---
# PagerKit 技能

## 概述

本技能提供了关于 `PagerKit` 的专业指导，`PagerKit` 是一个功能强大的 SwiftUI 库，用于创建高度可定制且跨平台的基于页面的导航系统。它涵盖了从基本使用和动态页面生成到页面指示器的高级定制、事件处理以及最佳实践等各个方面。利用本技能，可以帮助开发者在所有 Apple 平台上有效地实现灵活且视觉效果丰富的分页体验。

## 代理行为（请遵循这些规则）

1. **明确分页需求**：在提供解决方案之前，务必了解用户对页面内容、指示器样式、导航流程和平台目标的具体需求。
2. **优先使用 SwiftUI 的惯用语法**：推荐使用 `PagerKit` 的 `PKPageBuilder` 和 `ForEach` 来构建页面，以符合 SwiftUI 的设计原则。
3. **平台特定建议**：在讨论指示器图像、进度显示或 `UIPageViewController` 选项时，务必指明平台的兼容性以及正确的类型（`UIImage` 与 `Image`、`UIPageControlProgress`）。
4. **强调修饰符**：引导用户使用相关的 `PKPagesView` 或 `PKPage` 修饰符进行定制，同时提供完整的修饰符签名（例如 `.pkPageNavigationOrientation(_:)`）。
5. **提供上下文相关的代码示例**：提供简洁的代码片段，以展示在 `PKPagesView` 或 `PKPage` 中的推荐用法。
6. **强调跨平台特性**：在可能的情况下，提醒用户 `PagerKit` 的跨平台一致性，并说明如何使用 `#if os(...)` 指令处理平台特定的差异。

## 项目设置

`PagerKit` 的行为会受到项目部署目标和 Swift 版本的影响：

- **部署目标**：`PagerKit` 支持 iOS 14.0+、iPadOS 14.0+、macOS 14.0+、tvOS 14.0+、visionOS 1.0+ 和 watchOS 10.0+。某些功能（例如 `UIPageControlProgress`）仅在特定的平台和操作系统版本上可用。
- **Swift 版本**：需要使用 Swift 5.9+。

如果这些信息未知，请让开发人员确认，尤其是在讨论平台特定功能时。

## 快速决策树

当开发人员需要 `PagerKit` 的帮助时，请按照以下决策树进行操作：

1. **需要设置新的分页系统吗？**
    *   有关基本安装和概念 → 参见 `references/PagerKit.md`
    *   如需定义整个分页系统的结构 → 参见 `references/PKPagesView.md`
    *   如需创建单个页面内容 → 参见 `references/PKPage.md`

2. **需要根据数据动态生成页面吗？**
    *   如需使用项目集合生成页面 → 参见 `references/ForEach.md`

3. **需要控制页面流程或结构吗？**
    *   如需添加条件页面（if/else） → 参见 `references/PKPageBuilder.md`
    *   如需设置水平或垂直导航 → 参见 `references/PKPagesView.md`（`.pkPageNavigationOrientation`）

4. **需要自定义页面指示器（点）吗？**
    *   如需更改颜色（活动/非活动状态） → 参见 `references/PKPagesView.md`（`.pkPageControlIndicatorTintColor`, `.pkPageControlIndicatorCurrentIndicatorTintColor`）
    *   如需更改背景样式（简约、突出显示、自动显示） → 参见 `references/PKPageControlBackgroundStyle.md`
    *   如需调整位置或间距 → 参见 `references/PKPagesView.md`（`.pkPageControlIndicatorAlignment`, `.pkPageControlPadding`）
    *   如需设置布局方向（例如垂直对齐） → 参见 `references/PKPageControlDirection.md`
    *   如需使用自定义图像（全局或每个页面） → 参见 `references/PKPagesView.md`, `references/PKPage.md`
    *   如需隐藏指示器（始终隐藏或仅对单个页面隐藏） → 参见 `references/PKPagesView.md`

5. **需要处理页面切换事件或状态吗？**
    *   如需绑定当前页面索引 → 参见 `references/PKPagesView.md`（`.pkCurrentPageIndex`）
    *   如需响应手动页面切换 → 参见 `references/PKPagesView.md`（`.pkOnManualPageChange`）
    *   如需响应自动页面切换 → 参见 `references/PKPagesView.md`（`.pkOnAutoPageChange`）
    *   如需确定页面切换方向 → 参见 `references/PKPageDirection.md`
    *   如需在切换开始/结束时执行操作 → 参见 `references/PKPagesView.md`

6. **需要自定义单个页面的行为吗？**
    *   如需设置自动切换持续时间 → 参见 `references/PKPage.md`（`.pkPageDuration`）
    *   如需在页面上添加自定义页脚 → 参见 `references/PKPage.md`（`.pkPageFooter`）

## 问题排查指南

- **“我的页面没有显示或显示不正确。”**
    *   确认 `PKPagesView` 中包含有效的 `PKPage` 实例。请参考 `references/PKPagesView.md` 和 `references/PKPage.md`。
    *   如果使用了动态内容，请检查 `ForEach` 的实现。请参考 `references/ForEach.md`。
- **“页面指示器的位置或样式不正确。”**
    *   检查 `PKPagesView` 中的 `.pkPageControlIndicatorAlignment`、`.pkPageControlIndicatorBackgroundStyle`、`.pkPageControlDirection` 修饰符。请参考 `references/PKPagesView.md`、`references/PKPageControlBackgroundStyle.md`、`references/PKPageControlDirection.md`。
- **“我想更改活动点的颜色，但不起作用。”**
    *   确保在 `PKPagesView` 中使用了 `.pkPageControlIndicatorCurrentIndicatorTintColor(_:)`。请参考 `references/PKPagesView.md`。
- **“页面无法自动切换。”**
    *   检查是否为每个 `PKPage` 应用了非空的 `.pkPageDuration(_:)`。请参考 `references/PKPage.md`。
- **“我在 `PKPagesView` 中的条件逻辑（if 语句）引发了编译错误。”**
    *   请复习 `PKPageBuilder` 的概念，确保所有分支都返回有效的 `PKPage` 组件。请参考 `references/PKPageBuilder.md`。
- **“如何判断用户是向前还是向后滑动？”**
    *   使用 `.pkOnManualPageChange` 中的 `PKPageDirection` 参数。请参考 `references/PKPagesView.md`、`references/PKPageDirection.md`。

## 核心模式参考

### 基本分页系统设置

```swift
PKPagesView {
    PKPage { Text("Page A").font(.title) }
    PKPage { Text("Page B").font(.title) }
    PKPage { Text("Page C").font(.title) }
}
.pkCurrentPageIndex(index: $currentPage) // Bind to @State
.pkPageNavigationOrientation(.horizontal)
```

### 使用 `ForEach` 动态生成页面

```swift
struct Item: Identifiable {
    let id = UUID()
    let title: String
}

// ... inside a View
let items = [Item(title: "Item 1"), Item(title: "Item 2")]

PKPagesView {
    ForEach(items) { item in
        PKPage { Text(item.title) }
            .pkPageFooter { Text("Footer for \(item.title)") }
    }
}
```

### 自定义页面指示器样式

```swift
.pkPageControlIndicatorAlignment(spacing: 10, alignment: .bottomTrailing)
.pkPageControlIndicatorBackgroundStyle(.prominent)
.pkPageControlIndicatorDirection(.topToBottom) // Vertical dots
.pkPageControlIndicatorTintColor(.gray)
.pkPageControlIndicatorCurrentIndicatorTintColor(.blue)
// Custom images
#if os(iOS)
.pkPageControlIndicatorPreferredCurrentPageIndicatorImage(image: UIImage(systemName: "star.fill"))
#else
.pkPageControlIndicatorPreferredCurrentPageIndicatorImage(image: Image(systemName: "star.fill"))
#endif
```

### 处理页面切换事件

```swift
.pkOnManualPageChange { currentIndex, direction in
    print("User navigated to page \(currentIndex) by going \(direction).")
}
.pkOnAutoPageChange { previousIndex, currentIndex in
    print("Auto change from \(previousIndex) to \(currentIndex).")
}
.pkOnTransitionEnd { previous, current in
    print("Transition ended. Was on \(previous), now on \(current).")
}
```

## 集成快速指南

`PagerKit` 可通过 Swift 包管理器进行集成：

1. **添加包依赖**：在 Xcode 中，选择 **File > Add Package Dependency**，然后输入 `https://github.com/SzpakKamil/PagerKit.git`。
2. **导入**：在您的 Swift 文件中导入 `PagerKit`。
3. **部署目标**：确保您的项目支持 iOS 14.0+、iPadOS 14.0+、macOS 14.0+、tvOS 14.0+、visionOS 1.0+ 或 watchOS 10.0+（Swift 5.9+）。

有关详细设置，请参阅 `references/PagerKit.md`。

## 参考文件

根据具体需求加载以下文件：

- **`PagerKit.md`** - 通用概述、设置和核心优势。
- **`PKPagesView.md`** - 关于主要分页容器及其全局修饰符的详细信息。
- **`PKPage.md`** - 关于单个页面的创建及页面特定修饰符的信息。
- **`ForEach.md`** - 如何根据数据集合生成页面。
- **`PKPageBuilder.md`** - 了解用于 `PKPagesView` 的声明式内容构建方法。
- **`PKPageControlBackgroundStyle.md`** - 页面指示器背景样式的选项。
- **`PKPageControlDirection.md`** - 页面指示器点布局方向的选项。
- **`PKPageDirection.md`** - 了解页面切换的方向。
- **`_index.md`** - 包含所有 `PagerKit` 参考文档的综合性索引。

## 最佳实践总结

1. **采用声明式 UI**：使用 `PKPageBuilder` 和 `ForEach` 来构建灵活且易于维护的页面。
2. **谨慎进行定制**：充分利用丰富的修饰符 API，以匹配原生平台的美学设计和应用品牌风格，避免过度定制导致可用性下降。
3. **管理分页状态**：始终将 `pkCurrentPageIndex` 绑定到外部状态（`@State` 或 `@Binding`），以便进行程序控制和服务观察。
4. **实现事件处理**：利用回调（例如 `.pkOnManualPageChange`、`.pkOnTransitionEnd`）来进行分析、触觉反馈或根据导航操作执行自定义逻辑。
5. **注意平台差异**：了解在不同 Apple 平台和操作系统版本上表现不同的修饰符和功能。
6. **优先考虑可访问性**：确保自定义指示器和页脚仍然可访问（例如，支持 VoiceOver）。

**注意**：本技能基于 `PagerKit` 的完整文档。如需更多详细信息，请访问官方文档 [documentation.kamilszpak.com/documentation/pagerkit/](https://documentation.kamilszpak.com/documentation/pagerkit/) 或项目网站 [kamilszpak.com/pl/pagerkit](https://kamilszpak.com/pl/pagerkit)。