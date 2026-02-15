---
name: SymbolPicker
description: '关于 `SymbolPicker`（一个原生的 SwiftUI `SF Symbol` 选择器）的专家指南。当开发者提到以下内容时，请参考本指南：  
(1) `SymbolPicker`；  
(2) 选择 `SF Symbols`（SwiftUI 中的符号资源）；  
(3) 选择带颜色的符号；  
(4) 自定义 `SymbolPicker` 的外观；  
(5) 跨平台符号选择（iOS、macOS、visionOS）；  
(6) 特定修饰符，如 `.symbolPickerSymbolsStyle` 或 `.symbolPickerDismiss`。'
---
# SymbolPicker 技能

## 概述

本技能提供了关于 `SymbolPicker` 的专业指导，`SymbolPicker` 是一个原生的、可定制的 SwiftUI 组件，用于在 iOS、iPadOS、macOS 和 visionOS 上选择 SF Symbols（苹果自家的符号资源）。它模仿了苹果的原生界面，同时提供了丰富的自定义选项，包括颜色、样式（实心/轮廓）和行为设置。

## 代理行为（请遵循以下规则）：

1. **识别目标平台**：`SymbolPicker` 会根据不同的平台进行相应的显示（在 iOS 上为表格视图，在 iPad/Mac/visionOS 上为弹出窗口）。务必确认目标平台。
2. **优先推荐修改器**：引导用户使用相关的 `SymbolPicker` 修改器（如 `.symbolPickerSymbolsStyle`、`.symbolPickerDismiss`）来进行自定义。
3. **正确处理颜色选择**：在讨论颜色选择时，明确用户是需要使用 `[Double]`（RGBA 格式）、SwiftUI 的 `Color` 类型，还是 `SymbolColor` 类型。
4. **强调可访问性**：指出 `SymbolPicker` 默认支持 VoiceOver（语音导航）和 Dynamic Type（动态文本显示）功能。
5. **提供示例代码**：提供简洁的代码片段，展示如何将 `.symbolPicker` 修改器应用于视图（通常是按钮或图片），并说明其用于展示和选择的绑定方式。
6. **跨平台一致性**：提醒用户该组件的 API 在所有平台上都是统一的。

## 项目设置：

- **部署目标**：iOS 14.0+、iPadOS 14.0+、macOS 11.0+、visionOS 1.0+。
- **Swift 版本**：Swift 5.9+。
- **Xcode**：Xcode 15.0+。

## 快速决策树：

1. **如何设置基本的符号选择器？**
    *   基本安装和概念 → `references/SymbolPicker.md`
    *   如何将修改器应用于视图 → `references/SymbolPickerView.md`
2. **如何选择带颜色的符号？**
    *   如何使用不同的颜色绑定类型 → `references/SymbolPickerView.md`
    *   了解 `SymbolColor` 模型 → `references/SymbolColor.md`
3. **如何自定义外观或行为？**
    *   在实心图标和轮廓图标之间切换 → `references/SymbolPickerModifiers.md`（`.symbolPickerSymbolsStyle`）
    *   控制选择器关闭的行为 → `references/SymbolPickerModifiers.md`（`.symbolPickerDismiss`）

## 常见问题解决方法：

- **“选择器没有显示。”**
    * 检查是否有 `.symbolPicker(isPresented: ...)` 被绑定到视图上，并且该视图是否属于层级结构的一部分。
    * 确保 `isPresented` 的绑定状态被正确设置。
- **“我希望显示实心图标而不是轮廓图标。”**
    * 使用 `.symbolPickerSymbolsStyle(.filled)`。
- **“如何在选择符号后立即关闭选择器？”**
    * 使用 `.symbolPickerDismiss(type: .onSymbolSelect)`。

## 核心模式参考：

### 基本用法
```swift
@State private var isPresented = false
@State private var icon = "star"

Button("Pick Icon") { isPresented = true }
    .symbolPicker(isPresented: $isPresented, symbolName: $icon)
```

### 带颜色选择的功能
```swift
@State private var isPresented = false
@State private var icon = "star.fill"
@State private var color: Color = .red

Button("Pick Icon & Color") { isPresented = true }
    .symbolPicker(isPresented: $isPresented, symbolName: $icon, color: $color)
    .symbolPickerSymbolsStyle(.filled)
    .symbolPickerDismiss(type: .onSymbolSelect)
```

## 集成快速指南：

1. **添加包依赖**：`https://github.com/SzpakKamil/SymbolPicker.git`（最低版本 1.0.0）。
2. **导入**：`import SymbolPicker`。
3. **系统要求**：iOS 14.0+、macOS 11.0+、visionOS 1.0+。

## 参考文件：

根据需要加载以下文件以获取详细信息：

- **`SymbolPicker.md`** - 总体概述、设置方法及核心优势。
- **`SymbolPickerView.md`** - 关于选择器视图及其初始化方法的详细信息。
- **`SymbolPickerModifiers.md`** - 如何自定义样式（实心/轮廓）和关闭行为。
- **`SymbolColor.md`** - 使用 `SymbolColor` 枚举和颜色绑定的指南。
- **`SetUp.md`** - 逐步安装说明。