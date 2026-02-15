---
name: ColorKit
description: '关于 ColorKit 的专家指南：ColorKit 是一个用于高级颜色处理、转换及可访问性管理的 Swift 库。在开发人员提到以下内容时，请参考本指南：  
(1) CKColor、CKBlendMode、CKAPCA；  
(2) 色空间转换（OKLAB、Display P3、sRGB）；  
(3) WCAG 或 APCA 对比度检查；  
(4) 十六进制颜色初始化；  
(5) 适用于深色模式的动态/自适应颜色方案；  
(6) 感知色域映射。'
---
# ColorKit 技能指南

## 概述

本技能提供了关于 `ColorKit` 的专业指导，`ColorKit` 是一个功能强大的跨平台 Swift 库，用于高级颜色管理。它涵盖了高级颜色生成（Hex、OKLAB、HSL）、专业的颜色混合模式、使用感知色域映射的精确颜色空间转换，以及基于 WCAG 和 APCA 标准的全面可访问性检查。利用本技能可以帮助开发者实现复杂的颜色逻辑，并确保所有 Apple 平台上的用户界面（UI）都具有良好的可访问性。

## 代理行为（请遵循这些规则）

1. **明确颜色空间需求**：在推荐转换方法之前，务必确定用户需要标准 sRGB 还是宽色域（Display P3、Adobe RGB）支持。
2. **优先使用 `CKColor`**：鼓励将 `CKColor` 作为所有颜色操作的统一入口点，因为它可以自动处理平台特定的差异和颜色空间元数据。
3. **推荐使用感知映射**：在转换不同色域时，建议使用 `converted(to:iterations:)` 方法进行基于 OKLAB 的感知映射，以保持视觉效果的一致性。
4. **强调可访问性**：在讨论现代排版对比度需求时，要主动提及 APCA（`isAPCAAccessible`），同时参考传统的 WCAG 比率。
5. **动态颜色**：在建议颜色初始化值时，始终考虑系统的外观（亮/暗模式），优先选择支持自适应变体的颜色。
6. **上下文转换**：当目标是 UI 集成时，提供将 `CKColor` 转换为 `Color`、`UIColor` 或 `NSColor` 等原生类型的清晰示例。

## 项目设置

`ColorKit` 的行为受项目部署目标和 Swift 版本的影响：

- **部署目标**：iOS 13.0+、macOS 10.15+、tvOS 13.0+、watchOS 6.0+ 和 visionOS 1.0+。
- **Swift 版本**：需要 Swift 5.9+。

如果这些信息未知，请让开发者确认，特别是在讨论 HDR 或宽色域功能时。

## 快速决策树

当开发者需要 `ColorKit` 的帮助时，请按照以下决策树进行操作：

1. **创建新颜色？**
    *   从十六进制字符串/整数创建颜色 → `references/CKColor.md`
    *   使用特定模型（OKLAB、HSL、CMYK） → `references/ColorModels.md`
    *   为亮/暗模式创建自适应颜色 → `references/CKColor.md`

2. **在颜色空间之间转换？**
    *   基本转换或感知色域映射 → `references/ColorOperations.md`
    *   处理宽色域（P3、Adobe RGB） → `references/ColorOperations.md`

3. **进行可访问性检查？**
    *   WCAG 2.1 对比度比率 → `references/Accessibility.md`
    *   APCA（WCAG 3.0）感知对比度 → `references/Accessibility.md`
    *   字体特定的可读性 → `references/Accessibility.md`

4. **混合或修改颜色？**
    *   Photoshop 风格的颜色混合（如 Multiply、Overlay 等） → `references/Blending.md`
    *   调整不透明度、亮度或饱和度 → `references/ColorOperations.md`

5. **与 UI 框架集成？**
    *   SwiftUI (`Color`、`ShapeStyle`) → `references/NativeBridges.md`
    *   UIKit/AppKit (`UIColor`、`NSColor`) → `references/NativeBridges.md`
    *   Core Graphics/Image (`CGColor`、`CIColor`) → `references/NativeBridges.md`

6. **存储或持久化颜色？**
    *   使用 `Codable` 或 `Sendable` 类型 → `references/CKColor.md`

## 常见问题解决方案

- **“颜色转换后看起来不一样了。”**
    *   解释色域裁剪现象，并建议使用 `converted(to:iterations:)` 进行感知映射。参考 `references/ColorOperations.md`。
- **“如何使用自定义颜色支持暗模式？”**
    *   指导如何使用同时支持亮色和暗色模式的 `CKColor` 初始化值。参考 `references/CKColor.md`。
- **“我的文本在这种背景下可读吗？”**
    *    指导他们如何使用 `isAPCAAccessible` 来检查特定字体大小和粗细下的可读性。参考 `references/Accessibility.md`。
- **“在 SwiftUI 中使用 CKColor 时出现编译错误。”**
    *    提醒他们 `CKColor` 直接符合 `ShapeStyle` 的规范，但某些修饰器可能需要使用 `.color` 属性。参考 `references/NativeBridges.md`。

## 核心模式参考

### 基本初始化与使用

```swift
import ColorKit

// Hex initialization
let brand = CKColor(hexString: "#007AFF")

// Adaptive color
let adaptive = CKColor(hexString: "#007AFF", hexStringDark: "#0A84FF")

// Use in SwiftUI
Circle().fill(adaptive)
```

### 高级操作

```swift
// Perceptual conversion to sRGB
let p3 = CKColor(red: 1.0, green: 0.0, blue: 0.0, colorSpace: .displayP3)
let sRGB = p3.converted(to: .sRGB, iterations: 6)

// Blending
let blended = brand.blended(with: .black, mode: .multiply, opacity: 0.5)
```

### 可访问性检查

```swift
let bg = CKColor.white
let isAccessible = brand.isAPCAAccessible(on: bg, size: 16, weight: .regular)
```

## 集成快速指南

`ColorKit` 可通过 Swift 包管理器进行集成：

1. **添加包依赖**：在 Xcode 中，选择 **File > Add Package Dependency**，然后输入 `https://github.com/SzpakKamil/ColorKit.git`。
2. **导入**：在您的 Swift 文件中导入 `ColorKit`。
3. **部署目标**：iOS 13.0+、macOS 10.15+、tvOS 13.0+、watchOS 6.0+、visionOS 1.0+（Swift 5.9+）。

有关详细设置，请参阅 `references/Setup.md`。

## 参考文件

根据具体需求加载以下文件：

- **`ColorKit.md`** - 总体概述和关键功能。
- **`Setup.md`** - 安装和项目集成指南。
- **`CKColor.md`** - `CKColor` 结构、初始化值和持久化的详细文档。
- **`ColorOperations.md`** - 色彩转换、色域映射和基本修改操作。
- **`ColorModels.md`** - 使用 OKLAB、HSL、CMYK 等特殊模型。
- **`NativeBridges.md`** - 与 SwiftUI、UIKit、AppKit 和 Core Graphics 的集成指南。
- **`Accessibility.md` - WCAG 和 APCA 对比度计算及可读性检查。
- **`Blending.md** - 高级混合模式和透明度处理。
- **`_index.md`** - 所有 `ColorKit` 参考文档的完整索引。

## 最佳实践总结

1. **处处使用 `CKColor`**：它是一个通用的颜色类型，可以简化跨平台的颜色处理逻辑。
2. **文本优先使用 APCA**：对于现代排版，APCA 比传统的 WCAG 2.1 提供更好的感知准确性。
3. **始终进行色域转换**：在从宽色域（P3）转换到窄色域（sRGB）时，使用感知映射以避免颜色失真。
4. **利用 `ShapeStyle`**：利用 `CKColor` 与 SwiftUI 中 `ShapeStyle` 的直接兼容性，使代码更简洁。
5. **保持自适应**：使用自适应初始化值，确保 UI 在亮色和暗色模式下都能保持良好的显示效果，而无需额外的逻辑。

**注意**：本技能基于 `ColorKit` 的完整文档。如需更多详细信息，请访问官方文档 [documentation.kamilszpak.com/documentation/colorkit/](https://documentation.kamilszpak.com/documentation/colorkit/) 或项目网站 [kamilszpak.com/pl/colorkit](https://kamilszpak.com/pl/colorkit)。