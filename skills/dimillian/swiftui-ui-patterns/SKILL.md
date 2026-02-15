---
name: swiftui-ui-patterns
description: 最佳实践及基于示例的指导，用于构建 SwiftUI 视图和组件。适用于创建或重构 SwiftUI 用户界面、使用 TabView 设计标签页架构、组合屏幕内容，或在需要特定组件模式及示例时参考。
---

# SwiftUI 用户界面模式

## 快速入门

根据您的目标选择合适的开发路径：

### 现有项目

- 确定需要实现的功能或界面，以及主要的交互方式（列表、详情页、编辑器、设置界面等）。
- 在仓库中查找与 `rg "TabView\"` 相关的示例，然后研究相应的 SwiftUI 视图实现。
- 遵循项目中的本地开发规范：优先使用 SwiftUI 的原生状态管理机制；尽可能将状态数据保留在组件内部；对于共享的依赖项，使用 `@Environment` 进行注入。
- 从 `references/components-index.md` 中选择相应的组件，并按照其文档中的指导进行开发。
- 使用简洁、专注的子视图以及 SwiftUI 的原生数据流来构建界面。

### 新项目的搭建

- 首先参考 `references/app-scaffolding-wiring.md` 文件，将 `TabView`、`NavigationStack` 和 ` Sheets` 组件组合起来。
- 根据提供的模板，添加一个基本的 `AppTab` 和 `RouterPath`。
- 根据实际需求选择下一个需要使用的组件（如 `TabView`、`NavigationStack` 或 ` Sheets`），并更新相应的组件文档。
- 随着新界面的添加，逐步扩展路由（`route`）和界面组件的枚举（`enum`）。

## 需要遵循的一般规则

- 使用现代的 SwiftUI 状态管理机制（`@State`、`@Binding`、`@Observable`、`@Environment`），避免使用不必要的视图模型。
- 优先采用组合式设计（composition）；保持每个视图的功能简洁、专注。
- 使用 `.task` 实现异步操作，并明确处理加载和错误状态。
- 仅在修改旧代码时才保留原有的设计模式。
- 遵循项目规定的格式化和样式指南。
- **对于 `Sheet` 组件**：当状态表示某个选中的模型时，建议使用 `.sheet(item:)` 而不是 `.sheet(isPresented:)`。避免在 `sheet` 内部使用 `if let` 语句；`Sheet` 组件应自行处理用户交互逻辑，并通过 `dismiss()` 方法来关闭自身，而不是将 `onCancel`/`onConfirm` 事件传递给外部。

## 新 SwiftUI 视图的开发流程

1. 定义视图的状态及其所属组件。
2. 确定需要通过 `@Environment` 注入的依赖项。
3. 设计视图的结构，并将重复出现的部分提取为子视图。
4. 如有需要，使用 `.task` 实现异步加载，并明确定义状态枚举。
5. 为交互式元素添加可访问性标签或标识符。
6. 运行构建测试，根据需要更新相关使用场景的代码。

## 组件参考

请以 `references/components-index.md` 作为组件信息的入口点。每个组件文档应包含以下内容：
- 组件的用途及适用场景。
- 基本的用法示例及项目中的本地开发规范。
- 使用该组件时可能遇到的问题及性能注意事项。
- 仓库中该组件的示例代码链接。

## `Sheet` 组件的模式

### 以数据项驱动的 `Sheet` 组件（推荐使用）

```swift
@State private var selectedItem: Item?

.sheet(item: $selectedItem) { item in
    EditItemSheet(item: item)
}
```

### `Sheet` 组件自行处理用户交互逻辑

```swift
struct EditItemSheet: View {
    @Environment(\.dismiss) private var dismiss
    @Environment(Store.self) private var store

    let item: Item
    @State private var isSaving = false

    var body: some View {
        VStack {
            Button(isSaving ? "Saving…" : "Save") {
                Task { await save() }
            }
        }
    }

    private func save() async {
        isSaving = true
        await store.save(item)
        dismiss()
    }
}
```

## 添加新的组件文档

- 创建一个新的组件文档（文件名格式为 `references/<组件名称>.md`）。
- 文档内容应简洁明了，便于快速上手；同时提供指向仓库中具体实现文件的链接。
- 更新 `references/components-index.md`，添加新的组件条目。