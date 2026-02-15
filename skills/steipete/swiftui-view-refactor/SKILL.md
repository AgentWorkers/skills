---
name: swiftui-view-refactor
description: 重构并审查 SwiftUI 视图文件，以确保其结构的一致性、依赖注入的正确实现以及 Observation 的合理使用。当需要优化视图布局/排序、安全地处理视图模型（如果可能的话，这是必须的），或者标准化依赖项和 @Observable 状态的初始化及传递方式时，请使用此方法。
---

# SwiftUI 视图重构

## 来源：复制自 @Dimillian 的 `Dimillian/Skills`（2025-12-31）

## 概述
为 SwiftUI 视图应用一致的结构和依赖模式，重点关注视图顺序、模型-视图（MV）模式、视图模型的正确处理以及观察者（Observation）的使用。

## 核心指南

### 1) 视图顺序（从上到下）
- `Environment`
- `private`/`public` `let` 声明
- `@State` 或其他存储属性
- 计算属性 `var`（非视图相关）
- `init` 方法
- `body` 主体部分
- 计算属性生成器或其他视图辅助函数
- 辅助函数/异步函数

### 2) 优先使用模型-视图（MV）模式
- 默认采用 MV 模式：视图仅用于表示轻量级的状态；业务逻辑由模型或服务负责。
- 使用 `@State`、`@Environment`、`@Query` 以及 `task`/`onChange` 来实现逻辑协调。
- 通过 `@Environment` 注入服务和共享模型；保持视图简洁且可复用。
- 将复杂的视图拆分为多个子视图，而不是创建额外的视图模型。

### 3) 分割较大的视图结构和属性
- 如果 `body` 的内容超出屏幕显示范围或包含多个逻辑部分，将其拆分为较小的子视图。
- 当计算属性包含状态或复杂的逻辑分支时，将其提取为独立的 `View` 类型。
- 相关的子视图可以保留在同一个文件中作为计算属性；只有当结构上合理或需要复用时，才将其提取为独立的 `View` 结构。
- 优先传递简单的输入数据、绑定值或回调函数，而不是重复使用整个父视图的状态。

**示例：** 提取部分内容：

```swift
var body: some View {
    VStack(alignment: .leading, spacing: 16) {
        HeaderSection(title: title, isPinned: isPinned)
        DetailsSection(details: details)
        ActionsSection(onSave: onSave, onCancel: onCancel)
    }
}
```

**示例：** 将长主体拆分为多个部分，并在同一文件中使用计算属性：

```swift
var body: some View {
    List {
        header
        filters
        results
        footer
    }
}

private var header: some View {
    VStack(alignment: .leading, spacing: 6) {
        Text(title).font(.title2)
        Text(subtitle).font(.subheadline)
    }
}

private var filters: some View {
    ScrollView(.horizontal, showsIndicators: false) {
        HStack {
            ForEach(filterOptions, id: \.self) { option in
                FilterChip(option: option, isSelected: option == selectedFilter)
                    .onTapGesture { selectedFilter = option }
            }
        }
    }
}
```

**示例：** 提取复杂的计算属性：

```swift
private var header: some View {
    HeaderSection(title: title, subtitle: subtitle, status: status)
}

private struct HeaderSection: View {
    let title: String
    let subtitle: String?
    let status: Status

    var body: some View {
        VStack(alignment: .leading, spacing: 4) {
            Text(title).font(.headline)
            if let subtitle { Text(subtitle).font(.subheadline) }
            StatusBadge(status: status)
        }
    }
}
```

### 4) 视图模型处理（仅在必要时使用）
- 除非有明确的需求或现有代码需要，否则不要创建视图模型。
- 如果确实需要视图模型，请确保它是必需的（即不可缺少的）。
- 通过 `init` 方法将依赖项传递给视图，然后在视图的 `init` 方法中将这些依赖项传递给视图模型。
- 避免使用 `bootstrapIfNeeded` 等模式。

**示例：** 基于观察者的用法：

```swift
@State private var viewModel: SomeViewModel

init(dependency: Dependency) {
    _viewModel = State(initialValue: SomeViewModel(dependency: dependency))
}
```

### 5) 观察者的使用
- 对于 `@Observable` 类型的数据，将其作为 `@State` 属性存储在根视图中。
- 根据需要显式地将可观察对象向下传递；除非必要，否则避免使用可选状态。

## 工作流程
1) 根据规则重新排列视图的结构。
2) 优先使用 MV 模式：使用 `@State`、`@Environment`、`@Query`、`task` 和 `onChange` 来实现视图逻辑。
3) 如果存在视图模型，将其设置为必需的（不可缺少的），并在 `init` 方法中通过传递依赖项来初始化。
4) 确认观察者的使用方式：根视图模型应使用 `@State` 来存储可观察对象，避免不必要的封装层。

## 注意事项
- 优先使用简洁、明确的辅助函数，而不是复杂的条件判断块。
- 将计算属性生成器放在 `body` 下方，将非视图相关的计算属性放在 `init` 方法上方。
- 有关 MV 模式的更多指导和原理，请参考 `references/mv-patterns.md`。