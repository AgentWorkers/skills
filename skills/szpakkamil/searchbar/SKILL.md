---
name: SearchBar
description: '关于 `SearchBar`（一个可定制的 SwiftUI 搜索组件）的专家指南：  
当开发者提到以下内容时，请参考本指南：  
(1) `SearchBar`；  
(2) SwiftUI 中的自定义搜索栏；  
(3) 搜索令牌或建议功能；  
(4) 搜索栏的样式设置（如玻璃材质、胶囊形状等）；  
(5) 跨平台搜索（iOS、macOS、visionOS）；  
(6) 具体的 `SearchBar` 修改器，如 `.searchBarStyle` 或 `.searchBarSuggestions`。'
---
# SearchBar 技能指南

## 概述

本技能提供了关于 `SearchBar` 的专业指导。`SearchBar` 是一个功能强大且高度可定制的 SwiftUI 组件，可用于在 iOS、iPadOS、macOS 和 visionOS 上创建具有原生体验的搜索界面。它弥合了 `UISearchBar`（iOS/visionOS）与原生 SwiftUI 视图（macOS）之间的差距，提供了统一的 API，用于样式设置、行为控制以及高级功能（如搜索提示和动态建议）。

## 代理行为（请遵循以下规则）

1. **识别目标平台**：`SearchBar` 在 iOS/visionOS（使用 `UISearchBar`）和 macOS（使用自定义 SwiftUI）上的行为略有不同。请始终检查或询问目标平台，以提供准确的建议（例如，特定的材质效果或提示行为）。
2. **优先使用修饰符**：建议用户直接使用相关的 `SearchBar` 修饰符（如 `.searchBarStyle`、`.searchBarSuggestions`），而不是从头开始构建自定义视图。
3. **明确版本要求**：在讨论高级功能时，明确说明版本要求（例如，搜索提示功能需要 iOS 14+ 或 visionOS 1.0+）。
4. **强调本地化**：提醒用户 `SearchBar` 具备完全的本地化功能，能够自动适应系统语言。
5. **提供示例代码**：提供简洁的代码片段，展示在视图中的推荐用法，通常会包含对 `@State` 的绑定，用于处理文本和搜索提示。
6. **强调跨平台一致性**：尽可能提醒用户 `SearchBar` 的跨平台一致性，以及如何使用 `#if os(...)` 指令处理平台特定的差异（尽管库内部已经处理了大部分差异）。

## 项目设置

- **部署目标**：iOS 14.0+、iPadOS 14.0+、macOS 11.0+、visionOS 1.0+。
- **高级功能**：搜索提示功能需要 iOS 16.0+ 或 visionOS 1.0+（macOS 上需要 iOS 15.0+）。
- **Swift 版本**：Swift 5.9+。

## 快速决策树

1. **如何设置一个基本的搜索栏？**
    *   基本初始化和设置 → `references/SearchBar.md`

2. **如何自定义外观？**
    *   更改颜色、形状（胶囊形/圆形） → `references/SearchBarStyle.md`
    *   使用“玻璃”或“实心”材质 → `references/SearchBarStyle.md`
    *   更改大小/比例 → `references/SearchBarStyle.md`
    *   自定义图标 → `references/SearchBarModifiers.md`（`.searchBarIconView`）

3. **如何配置行为？**
    *   显示/隐藏取消或清除按钮 → `references/SearchBarDisplayModes.md`
    *   处理事件（开始/结束编辑、清除、取消） → `references/SearchBarModifiers.md`
    *   焦点管理 → `references/SearchBarModifiers.md`（`.searchBarIsFocused`）

4. **如何使用高级搜索功能（iOS 16+/visionOS）？**
    *   添加过滤提示（胶囊形图标） → `references/SearchBarData.md`
    *   显示搜索建议 → `references/SearchBarData.md`
    *   启用自动建议过滤 → `references/SearchBarData.md`

## 常见问题解答

- **“我的搜索栏在 macOS 上看起来不一样。”**
    *   解释 macOS 使用的是纯 SwiftUI 实现，而 iOS 使用的是 `UISearchBar`。虽然样式一致，但底层实现不同。
- **“搜索提示没有显示。”**
    *   确认部署目标是否为 iOS 16.0+ 或 visionOS 1.0+。
    *   确保对搜索提示的绑定是激活的，并且数据已填充。
- **“如何更改背景颜色？”**
    *   使用 `.searchBarStyle(..., backgroundColor: .red)`。请参阅 `references/SearchBarStyle.md`。
- **“我想隐藏取消按钮。”**
    *   使用 `.searchBarCancelButtonDisplayMode(.never)`。请参阅 `references/SearchBarDisplayModes.md`。
- **“如何让搜索栏呈现玻璃质感/透明效果？”**
    *   使用 `.searchBarMaterial(.glass)`。请注意平台/版本限制（iOS 26+）。请参阅 `references/SearchBarStyle.md`。

## 核心模式参考

### 基本设置
```swift
SearchBar(text: $text, prompt: "Search...")
    .searchBarStyle(.rounded)
```

### 高级样式设置
```swift
SearchBar(text: $text)
    .searchBarStyle(.capsule, textColor: .white, tint: .blue, backgroundColor: .black.opacity(0.8))
    .searchBarMaterial(.glass) // iOS 26+ (Experimental/Future)
```

### 搜索提示与过滤
```swift
SearchBar(text: $text)
    .searchBarCurrentTokens($tokens)
    .searchBarSuggestions($suggestions)
    .searchBarEnableAutomaticSuggestionsFiltering(true)
```

### 事件处理
```swift
SearchBar(text: $text)
    .searchBarBeginEditingAction { print("Started") }
    .searchBarEndEditingAction { print("Ended") }
    .searchBarCancelButtonAction { print("Cancelled") }
```

## 集成快速指南

`SearchBar` 可通过 Swift 包管理器进行集成：

1. **添加包依赖**：在 Xcode 中，选择 **File > Add Package Dependency**，然后输入 `https://github.com/SzpakKamil/SearchBar.git`。
2. **导入**：在您的 Swift 文件中导入 `SearchBar`。
3. **部署目标**：确保项目目标支持 iOS 14.0+、macOS 11.0+、visionOS 1.0+。

有关详细设置，请参阅 `references/SearchBar.md`。

## 参考文件

- **`SearchBar.md`** - 总体概述、设置和初始化。
- **`SearchBarModifiers.md`** - 所有修饰符的完整列表。
- **`SearchBarStyle.md`** - 样式设置、材质选择、角部样式和比例调整。
- **`SearchBarDisplayModes.md`** - 取消和清除按钮的行为设置。
- **`SearchBarData.md`** - 搜索提示和过滤功能。
- **`_index.md`** - 所有主题的索引。