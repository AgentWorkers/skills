---
name: swiftui-liquid-glass
description: 使用 iOS 26 及更高版本的 Liquid Glass API 来实现、审查或改进 SwiftUI 的功能。当需要在新 SwiftUI 用户界面中采用 Liquid Glass 技术时，或者需要对现有功能进行重构以适配 Liquid Glass 时，或者需要检查 Liquid Glass 的使用情况（包括正确性、性能和设计一致性）时，请使用该 API。
---

# SwiftUI Liquid Glass

**来源说明：** 从 @Dimillian 的 `Dimillian/Skills` 中复制（2025-12-31）。

## 概述  
使用此技能来构建或审查完全符合 iOS 26+ Liquid Glass API 的 SwiftUI 功能。优先使用原生 API（`glassEffect`、`GlassEffectContainer`、玻璃按钮样式）以及 Apple 的设计指南。确保使用方式的一致性，在需要时实现交互性，并关注性能。

## 工作流程决策树  
选择符合需求的路径：  

### 1) 审查现有功能  
- 检查应使用 Liquid Glass 的地方以及不应使用的地方。  
- 验证修饰符的顺序、形状的使用方式以及容器的放置位置。  
- 检查对 iOS 26+ 的兼容性处理及合理的回退方案。  

### 2) 使用 Liquid Glass 改进现有功能  
- 确定需要应用玻璃效果的组件（如表面、按钮等）。  
- 当存在多个玻璃元素时，重构代码以使用 `GlassEffectContainer`。  
- 仅对可点击或可聚焦的元素启用交互式玻璃效果。  

### 3) 使用 Liquid Glass 实现新功能  
- 首先设计玻璃效果的外观和交互方式（形状、突出显示方式等）。  
- 在布局/外观修饰符之后应用玻璃效果修饰符。  
- 仅在视图层次结构发生变化时（通过动画）添加过渡效果。  

## 核心指南  
- 尽量使用原生的 Liquid Glass API，而非自定义模糊效果。  
- 当多个玻璃元素共存时，使用 `GlassEffectContainer`。  
- 在布局和视觉修饰符之后应用 `.glassEffect(...)`。  
- 对于可响应触摸/指针操作的元素，使用 `.interactive()`。  
- 保持相关元素之间的形状一致性，以获得统一的外观。  
- 使用 `#available(iOS 26, *)` 来限制功能的可用性，并提供非玻璃效果的回退方案。  

## 审查检查清单  
- **可用性**：使用 `#available(iOS 26, *)` 来标记功能的可用性，并提供回退界面。  
- **组合方式**：将多个玻璃效果视图包裹在 `GlassEffectContainer` 中。  
- **修饰符顺序**：先应用布局/外观修饰符，再应用玻璃效果修饰符。  
- **交互性**：仅在用户有交互行为时启用交互性。  
- **过渡效果**：使用 `glassEffectID` 和 `@Namespace` 来实现过渡效果。  
- **一致性**：确保整个功能中的形状、色调和间距保持一致。  

## 实现检查清单  
- 明确目标元素及所需的玻璃效果效果（如突出显示程度）。  
- 将相关的玻璃元素包裹在 `GlassEffectContainer` 中，并调整间距。  
- 根据需要使用 `.glassEffect(.regular.tint(...).interactive(), in: .rect(cornerRadius: ...))`。  
- 对于按钮等交互元素，使用 `.buttonStyle(.glass)` 或 `.buttonStyle(.glassProminent)`。  
- 当视图层次结构发生变化时，使用 `glassEffectID` 来添加过渡效果。  
- 为早期版本的 iOS 提供回退的材质和视觉效果。  

## 快速示例代码片段  
可以直接使用这些代码片段，并根据需求自定义形状、色调和间距。  

```swift
if #available(iOS 26, *) {
    Text("Hello")
        .padding()
        .glassEffect(.regular.interactive(), in: .rect(cornerRadius: 16))
} else {
    Text("Hello")
        .padding()
        .background(.ultraThinMaterial, in: RoundedRectangle(cornerRadius: 16))
}
```  
```swift
GlassEffectContainer(spacing: 24) {
    HStack(spacing: 24) {
        Image(systemName: "scribble.variable")
            .frame(width: 72, height: 72)
            .font(.system(size: 32))
            .glassEffect()
        Image(systemName: "eraser.fill")
            .frame(width: 72, height: 72)
            .font(.system(size: 32))
            .glassEffect()
    }
}
```  
```swift
Button("Confirm") { }
    .buttonStyle(.glassProminent)
```  

## 资源  
- 参考指南：`references/liquid-glass.md`  
- 建议参考 Apple 的官方文档以获取最新的 API 详情。