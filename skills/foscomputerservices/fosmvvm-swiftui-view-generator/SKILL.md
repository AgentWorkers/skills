---
name: fosmvvm-swiftui-view-generator
description: 生成能够渲染 FOSMVVM 视图模型的 SwiftUI 视图。这些视图模型遵循 “ViewModelView” 模式，并支持数据绑定、加载状态管理以及预览功能。
homepage: https://github.com/foscomputerservices/FOSUtilities
metadata: {"clawdbot": {"emoji": "📱", "os": ["darwin"]}}
---
# FOSMVVM SwiftUI 视图生成器

该工具用于生成能够渲染 FOSMVVM 数据模型的 SwiftUI 视图。

## 概念基础

> 有关完整的架构信息，请参阅 [FOSMVVMArchitecture.md](../../docs/FOSMVVMArchitecture.md) | [OpenClaw 参考文档]({{baseDir}/references/FOSMVVMArchitecture.md)

在 FOSMVVM 中，**视图** 是用于显示数据模型的轻量级渲染层：

```
┌─────────────────────────────────────────────────────────────┐
│                    ViewModelView Pattern                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ViewModel (Data)          ViewModelView (SwiftUI)          │
│  ┌──────────────────┐     ┌──────────────────┐             │
│  │ title: String    │────►│ Text(vm.title)   │             │
│  │ items: [Item]    │────►│ ForEach(vm.items)│             │
│  │ isEnabled: Bool  │────►│ .disabled(!...)  │             │
│  └──────────────────┘     └──────────────────┘             │
│                                                              │
│  Operations (Actions)                                        │
│  ┌──────────────────┐     ┌──────────────────┐             │
│  │ submit()         │◄────│ Button(action:)  │             │
│  │ cancel()         │◄────│ .onAppear { }    │             │
│  └──────────────────┘     └──────────────────┘             │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**关键原则：** 视图不负责数据的转换或计算，而是直接渲染数据模型提供的内容。

---

## 视图与数据模型的对应关系

**视图的文件名应与其渲染的数据模型相匹配。**

```
Sources/
  {ViewModelsTarget}/
    {Feature}/
      {Feature}ViewModel.swift        ←──┐
      {Entity}CardViewModel.swift     ←──┼── Same names
                                          │
  {ViewsTarget}/                          │
    {Feature}/                            │
      {Feature}View.swift             ────┤  (renders {Feature}ViewModel)
      {Entity}CardView.swift          ────┘  (renders {Entity}CardViewModel)
```

这种对应关系具有以下优势：
- **可发现性**：可以立即找到对应的数据模型视图。
- **一致性**：整个代码库中采用统一的命名规范。
- **可维护性**：数据模型的更改会立即反映在视图的位置上。

---

## 核心组件

### 1. ViewModelView 协议

所有视图都必须遵循 `ViewModelView` 协议：

```swift
public struct MyView: ViewModelView {
    private let viewModel: MyViewModel

    public var body: some View {
        Text(viewModel.title)
    }

    public init(viewModel: MyViewModel) {
        self.viewModel = viewModel
    }
}
```

**必备要求：**
- `private let viewModel: {ViewModel}`
- `public init(viewModel:)`
- 遵循 `ViewModelView` 协议

### 2. 操作（可选）

交互式视图具有操作功能：

```swift
public struct MyView: ViewModelView {
    private let viewModel: MyViewModel
    private let operations: MyViewModelOperations

    #if DEBUG
    @State private var repaintToggle = false
    #endif

    public var body: some View {
        Button(action: performAction) {
            Text(viewModel.buttonLabel)
        }
        #if DEBUG
        .testDataTransporter(viewModelOps: operations, repaintToggle: $repaintToggle)
        #endif
    }

    public init(viewModel: MyViewModel) {
        self.viewModel = viewModel
        self.operations = viewModel.operations
    }

    private func performAction() {
        operations.performAction()
        toggleRepaint()
    }

    private func toggleRepaint() {
        #if DEBUG
        repaintToggle.toggle()
        #endif
    }
}
```

**当视图具有操作功能时：**
- 在 `init` 方法中存储来自 `viewModeloperations` 的操作信息。
- 添加 `@State private var repaintToggle = false`（仅用于调试模式）。
- 添加 `.testDataTransporter(viewModelOps:repaintToggle:)` 修饰符（仅用于调试模式）。
- 在每次执行操作后调用 `toggleRepaint()` 方法。

### 3. 子视图绑定

父视图通过 `.bind(appState:)` 方法来绑定子视图：

```swift
public struct ParentView: ViewModelView {
    @Environment(AppState.self) private var appState
    private let viewModel: ParentViewModel

    public var body: some View {
        VStack {
            Text(viewModel.title)

            // Bind child view with subset of parent's data
            ChildView.bind(
                appState: .init(
                    itemId: viewModel.selectedId,
                    isConnected: viewModel.isConnected
                )
            )
        }
    }
}
```

**`.bind()` 方法的用法：**
- 子视图使用 `.bind(appState:)` 从父视图接收数据。
- 父视图根据自身的数据模型创建子视图的状态（`AppState`）。
- 这种方式实现了组件的解耦，避免了紧密耦合。

### 4. 带有验证功能的表单视图

表单视图使用 `FormFieldView` 和 `Validations` 环境：

```swift
public struct MyFormView: ViewModelView {
    @Environment(Validations.self) private var validations
    @Environment(\.focusState) private var focusField
    @State private var error: Error?

    private let viewModel: MyFormViewModel
    private let operations: MyFormViewModelOperations

    public var body: some View {
        Form {
            FormFieldView(
                fieldModel: viewModel.$email,
                focusField: focusField,
                fieldValidator: viewModel.validateEmail,
                validations: validations
            )

            Button(errorBinding: $error, asyncAction: submit) {
                Text(viewModel.submitButtonLabel)
            }
            .disabled(validations.hasError)
        }
        .onAsyncSubmit {
            await submit()
        }
        .alert(
            errorBinding: $error,
            title: viewModel.errorTitle,
            message: viewModel.errorMessage,
            dismissButtonLabel: viewModel.dismissButtonLabel
        )
    }
}
```

**表单相关模式：**
- 使用 `@Environment(Validations.self)` 来获取验证状态。
- 为每个输入字段使用 `FormFieldView`。
- 使用 `Button(errorBinding:asyncAction:)` 来处理异步操作。
- 在提交按钮上使用 `.disabled(validations.hasError)` 来控制按钮的可见性。
- 对验证错误和普通错误进行区分处理。

### 5. 预览

使用 `.previewHost()` 来生成 SwiftUI 预览版本：

```swift
#if DEBUG
#Preview {
    MyView.previewHost(
        bundle: MyAppResourceAccess.localizationBundle
    )
    .environment(AppState())
}

#Preview("With Data") {
    MyView.previewHost(
        bundle: MyAppResourceAccess.localizationBundle,
        viewModel: .stub(title: "Preview Title")
    )
    .environment(AppState())
}
#endif
```

## 视图类型

### 仅显示数据的视图

这些视图仅用于渲染数据，不支持用户交互：

```swift
public struct InfoView: ViewModelView {
    private let viewModel: InfoViewModel

    public var body: some View {
        VStack {
            Text(viewModel.title)
            Text(viewModel.description)

            if viewModel.isActive {
                Text(viewModel.activeStatusLabel)
            }
        }
    }

    public init(viewModel: InfoViewModel) {
        self.viewModel = viewModel
    }
}
```

**特点：**
- 没有 `operations` 属性。
- 没有 `repaintToggle` 或 `testDataTransporter`。
- 仅根据数据模型的状态来渲染内容。
- 可能根据数据模型的状态进行条件渲染。

### 交互式视图

这些视图支持用户操作：

```swift
public struct ActionView: ViewModelView {
    @State private var error: Error?

    private let viewModel: ActionViewModel
    private let operations: ActionViewModelOperations

    #if DEBUG
    @State private var repaintToggle = false
    #endif

    public var body: some View {
        VStack {
            Button(action: performAction) {
                Text(viewModel.actionLabel)
            }

            Button(role: .cancel, action: cancel) {
                Text(viewModel.cancelLabel)
            }
        }
        .alert(
            errorBinding: $error,
            title: viewModel.errorTitle,
            message: viewModel.errorMessage,
            dismissButtonLabel: viewModel.dismissButtonLabel
        )
        #if DEBUG
        .testDataTransporter(viewModelOps: operations, repaintToggle: $repaintToggle)
        #endif
    }

    public init(viewModel: ActionViewModel) {
        self.viewModel = viewModel
        self.operations = viewModel.operations
    }

    private func performAction() {
        operations.performAction()
        toggleRepaint()
    }

    private func cancel() {
        operations.cancel()
        toggleRepaint()
    }

    private func toggleRepaint() {
        #if DEBUG
        repaintToggle.toggle()
        #endif
    }
}
```

### 表单视图

这些视图包含经过验证的输入字段：
- 为每个输入字段使用 `FormFieldView`。
- 使用 `@Environment(Validations.self)` 来获取验证状态。
- 当 `validations.hasError` 为 `true` 时，按钮会被禁用。
- 对验证错误和操作错误进行区分处理。

### 容器视图

这些视图用于组合其他视图：

```swift
public struct ContainerView: ViewModelView {
    @Environment(AppState.self) private var appState
    private let viewModel: ContainerViewModel
    private let operations: ContainerViewModelOperations

    public var body: some View {
        VStack {
            switch viewModel.state {
            case .loading:
                ProgressView()

            case .ready:
                ChildAView.bind(
                    appState: .init(id: viewModel.selectedId)
                )

                ChildBView.bind(
                    appState: .init(
                        isActive: viewModel.isActive,
                        level: viewModel.level
                    )
                )
            }
        }
    }
}
```

## 适用场景

- 为 FOSMVVM 应用程序创建新的 SwiftUI 视图。
- 构建用于渲染数据模型的用户界面。
- 遵循需要新视图的实现计划。
- 创建带有验证功能的表单。
- 构建用于组合其他视图的容器视图。

## 生成的内容

| 文件名 | 所在目录 | 用途 |
|------|----------|---------|
| `{ViewName}View.swift` | `Sources/{ViewsTarget}/{Feature}/` | 生成的 SwiftUI 视图文件 |

**注意：** 相应的数据模型（`ViewModel`）和操作逻辑（`ViewModelOperations`）必须已经存在（可以使用 `fosmvvm-viewmodel-generator` 工具生成）。

## 项目结构配置

| 占位符 | 说明 | 示例 |
|-------------|-------------|---------|
| `{ViewName}` | 视图名称（不含 “View” 后缀） | `TaskList`, `SignIn` |
| `{ViewsTarget}` | SwiftUI 视图的存储目录 | `MyAppViews` |
| `{Feature}` | 功能/模块分组 | `Tasks`, `Auth` |

## 视图生成逻辑

该工具会根据对话内容来确定视图的结构：

### 视图类型识别

根据对话内容，工具会识别：
- **数据模型的结构**（来自之前的讨论或 Claude 阅读的规范）。
- **视图类型**：仅显示数据、交互式、表单或容器类型。
- **是否需要操作功能**：视图是否支持用户操作。
- **是否包含子视图**：视图是否需要绑定子视图。

### 组件选择

根据视图类型选择相应的组件：
- **仅显示数据的视图**：仅需要遵循 `ViewModelView` 协议，并提供 `viewModel` 属性。
- **交互式视图**：需要添加操作功能、`repaintToggle`、`testDataTransporter` 和 `toggleRepaint()` 方法。
- **表单视图**：需要添加 `Validations` 环境、`FormFieldView` 和错误处理逻辑。
- **容器视图**：需要使用 `.bind()` 方法来组合子视图。

### 代码生成

生成的视图文件包含：
- 对 `ViewModelView` 协议的遵守。
- 数据模型（`viewModel`）及其操作逻辑（如果需要）。
- 视图渲染逻辑。
- 在 `init` 方法中存储数据模型和操作信息。
- 如果视图具有交互功能，还会包含相应的操作方法。
- 如果需要，还包括测试逻辑和不同状态下的预览功能。

### 信息来源

该工具的信息来源包括：
- 与用户的讨论内容。
- 规范文件（如果 Claude 已经阅读了相关规范）。
- 代码库中的数据模型定义。

## 关键模式

### 错误处理模式

```swift
@State private var error: Error?

var body: some View {
    VStack {
        Button(errorBinding: $error, asyncAction: submit) {
            Text(viewModel.submitLabel)
        }
    }
    .alert(
        errorBinding: $error,
        title: viewModel.errorTitle,
        message: viewModel.errorMessage,
        dismissButtonLabel: viewModel.dismissButtonLabel
    )
}

private func submit() async {
    do {
        try await operations.submit()
    } catch {
        self.error = error
    }
    toggleRepaint()
}
```

### 验证错误处理模式

对于表单视图，需要单独处理验证错误：

```swift
private func submit() async {
    let validations = validations
    do {
        try await operations.submit(data: viewModel.data)
    } catch let error as MyRequest.ResponseError {
        if !error.validationResults.isEmpty {
            validations.replace(with: error.validationResults)
        } else {
            self.error = error
        }
    } catch {
        self.error = error
    }
    toggleRepaint()
}
```

### 异步任务处理模式

```swift
var body: some View {
    VStack {
        if isLoading {
            ProgressView()
        } else {
            contentView
        }
    }
    .task(errorBinding: $error) {
        try await loadData()
    }
}

private func loadData() async throws {
    isLoading = true
    try await operations.loadData()
    isLoading = false
    toggleRepaint()
}
```

### 条件渲染模式

使用数据模型的状态来进行条件渲染：

```swift
var body: some View {
    VStack {
        if viewModel.isEmpty {
            Text(viewModel.emptyStateMessage)
        } else {
            ForEach(viewModel.items) { item in
                ItemRow(item: item)
            }
        }
    }
}
```

### 可计算视图组件的模式

将可重用的视图片段提取为计算属性：

```swift
private var headerView: some View {
    HStack {
        Text(viewModel.title)
        Spacer()
        Image(systemName: viewModel.iconName)
    }
}

var body: some View {
    VStack {
        headerView
        contentView
    }
}
```

### 结果/错误处理模式

当视图需要渲染多个可能的数据模型（成功或不同类型的错误）时，可以使用枚举来封装这些状态：

**封装数据模型的类：**
```swift
@ViewModel
public struct TaskResultViewModel {
    public enum Result {
        case success(TaskViewModel)
        case notFound(NotFoundViewModel)
        case validationError(ValidationErrorViewModel)
        case permissionDenied(PermissionDeniedViewModel)
    }

    public let result: Result
    public var vmId: ViewModelId = .init(type: Self.self)

    public init(result: Result) {
        self.result = result
    }
}
```

**视图本身：**
```swift
public struct TaskResultView: ViewModelView {
    private let viewModel: TaskResultViewModel

    public var body: some View {
        switch viewModel.result {
        case .success(let vm):
            TaskView(viewModel: vm)
        case .notFound(let vm):
            NotFoundView(viewModel: vm)
        case .validationError(let vm):
            ValidationErrorView(viewModel: vm)
        case .permissionDenied(let vm):
            PermissionDeniedView(viewModel: vm)
        }
    }

    public init(viewModel: TaskResultViewModel) {
        self.viewModel = viewModel
    }
}
```

**关键原则：**
- 每种错误情况都有对应的数据模型类型。
- 使用枚举来关联不同的数据模型。
- 视图根据枚举的值来显示相应的子视图。
- 保证类型安全（避免使用 `any ViewModel` 类型）。
- 不使用通用的错误处理方式——每种错误都有明确的处理方式。

### ViewModelId 的初始化（非常重要）

**重要提示：** `ViewModelId` 通过 `.id(vmId)` 修饰符来控制 SwiftUI 的视图标识系统。错误的初始化会导致视图识别错误，从而影响更新效果。

**❌ 错误用法：** **绝对不要这样做：** 
```swift
public var vmId: ViewModelId = .init()  // NO! Generic identity
```

**✅ 最小要求：** 使用基于类型的标识方式：**
```swift
public var vmId: ViewModelId = .init(type: Self.self)
```
这样可以确保相同类型的视图具有唯一的标识。

**✅ 理想做法：** 在可能的情况下使用基于数据的标识方式：**
```swift
public struct TaskViewModel {
    public let id: ModelIdType
    public var vmId: ViewModelId

    public init(id: ModelIdType, /* other params */) {
        self.id = id
        self.vmId = .init(id: id)  // Ties view identity to data identity
        // ...
    }
}
```

**原因：**  
- SwiftUI 使用 `.id()` 修饰符来决定何时重新创建视图或更新视图。
- `vmId` 为 `ViewModelView` 提供了唯一的标识。
- 错误的标识方式会导致视图在数据变化时无法正确更新。
- 基于数据的标识方式（`.init(id:)`）能够更好地关联视图的生命周期和数据生命周期。

## 文件组织结构

```
Sources/{ViewsTarget}/
├── {Feature}/
│   ├── {Feature}View.swift             # Full page → {Feature}ViewModel
│   ├── {Entity}CardView.swift          # Child component → {Entity}CardViewModel
│   ├── {Entity}RowView.swift           # Child component → {Entity}RowViewModel
│   └── {Modal}View.swift               # Modal → {Modal}ViewModel
├── Shared/
│   ├── HeaderView.swift                # Shared components
│   └── FooterView.swift
└── Styles/
    └── ButtonStyles.swift              # Reusable button styles
```

---

## 常见错误

- 在视图中计算数据：  
```swift
// ❌ BAD - View is transforming data
var body: some View {
    Text("\(viewModel.firstName) \(viewModel.lastName)")
}

// ✅ GOOD - ViewModel provides shaped result
var body: some View {
    Text(viewModel.fullName)  // via @LocalizedCompoundString
}
```

- 忘记调用 `toggleRepaint()` 方法：  
```swift
// ❌ BAD - Test infrastructure won't work
private func submit() {
    operations.submit()
    // Missing toggleRepaint()!
}

// ✅ GOOD - Always call after operations
private func submit() {
    operations.submit()
    toggleRepaint()
}
```

- 将计算属性用于显示：  
```swift
// ❌ BAD - View is computing
var body: some View {
    if !viewModel.items.isEmpty {
        Text("You have \(viewModel.items.count) items")
    }
}

// ✅ GOOD - ViewModel provides the state
var body: some View {
    if viewModel.hasItems {
        Text(viewModel.itemCountMessage)
    }
}
```

- 硬编码文本：  
```swift
// ❌ BAD - Not localizable
Button(action: submit) {
    Text("Submit")
}

// ✅ GOOD - ViewModel provides localized text
Button(action: submit) {
    Text(viewModel.submitButtonLabel)
}
```

- 未正确绑定错误信息：  
```swift
// ❌ BAD - Errors not handled
Button(action: submit) {
    Text(viewModel.submitLabel)
}

// ✅ GOOD - Error binding for async actions
Button(errorBinding: $error, asyncAction: submit) {
    Text(viewModel.submitLabel)
}
```

- 将操作逻辑存储在视图主体中而不是 `init` 方法中：  
```swift
// ❌ BAD - Recomputed on every render
public var body: some View {
    let operations = viewModel.operations
    Button(action: { operations.submit() }) {
        Text(viewModel.submitLabel)
    }
}

// ✅ GOOD - Store in init
private let operations: MyOperations

public init(viewModel: MyViewModel) {
    self.viewModel = viewModel
    self.operations = viewModel.operations
}
```

- 文件名不匹配：  
```
// ❌ BAD - Filename doesn't match ViewModel
ViewModel: TaskListViewModel
View:      TasksView.swift

// ✅ GOOD - Aligned names
ViewModel: TaskListViewModel
View:      TaskListView.swift
```

- `ViewModelId` 初始化错误：  
```swift
// ❌ BAD - Generic identity, views won't update correctly
public var vmId: ViewModelId = .init()

// ✅ MINIMUM - Type-based identity
public var vmId: ViewModelId = .init(type: Self.self)

// ✅ IDEAL - Data-based identity (when id available)
public init(id: ModelIdType) {
    self.id = id
    self.vmId = .init(id: id)
}
```

- 强制解包可本地化的字符串：  
```swift
// ❌ BAD - Force-unwrapping to work around missing overload
import SwiftUI

Text(try! viewModel.title.localizedString)  // Anti-pattern - don't do this!
Label(try! viewModel.label.localizedString, systemImage: "star")

// ✅ GOOD - Request the proper SwiftUI overload instead
// The correct solution is to add an init extension like this:
extension Text {
    public init(_ localizable: Localizable) {
        self.init(localizable.localized)
    }
}

extension Label where Title == Text, Icon == Image {
    public init(_ title: Localizable, systemImage: String) {
        self.init(title.localized, systemImage: systemImage)
    }
}

// Then views use it cleanly without force-unwraps:
Text(viewModel.title)
Label(viewModel.label, systemImage: "star")
```

**原因：**  
FOSMVVM 为所有可本地化的字符串提供了 `Localizable` 协议，并为常见的元素（如 `Text`）提供了 `Localizable` 的初始化方法。但是，并非所有的 SwiftUI 元素都支持 `Localizable`。  
**遇到不支持 `Localizable` 的 SwiftUI 元素时：**  
1. **不要** 使用 `try! localizablelocalizedString` 来绕过类型系统，因为这会导致代码中出现强制解包操作。  
2. **应该** 请求为该元素在 `FOSUtilities` 中添加相应的初始化方法。  
3. **正确的做法是：** 创建接受 `Localizable` 的扩展，并将 `.localized` 传递给标准的初始化方法。  
这种方式可以使代码库保持整洁、类型安全，并完全避免在视图代码中强制解包操作。

---

## 文件模板

完整的文件模板请参阅 [reference.md](reference.md)。

## 命名规范

| 概念 | 命名规则 | 示例 |
|---------|------------|---------|
| 视图结构 | `{Name}View` | `TaskListView`, `SignInView` |
| 数据模型属性 | `viewModel` | 始终使用 `viewModel` |
| 操作逻辑属性 | `operations` | 始终使用 `operations` |
- 错误状态 | `error` | 始终使用 `error` |
- 重绘开关 | `repaintToggle` | 始终使用 `repaintToggle` |

## 常用修饰符

### FOSMVVM 特有的修饰符  

```swift
// Error alert with ViewModel strings
.alert(
    errorBinding: $error,
    title: viewModel.errorTitle,
    message: viewModel.errorMessage,
    dismissButtonLabel: viewModel.dismissButtonLabel
)

// Async task with error handling
.task(errorBinding: $error) {
    try await loadData()
}

// Async submit handler
.onAsyncSubmit {
    await submit()
}

// Test data transporter (DEBUG only)
.testDataTransporter(viewModelOps: operations, repaintToggle: $repaintToggle)

// UI testing identifier
.uiTestingIdentifier("submitButton")
```

### 标准的 SwiftUI 修饰符  

根据需要应用布局、样式等相关的标准修饰符。

## 使用方法

**使用方法：**  
```bash
/fosmvvm-swiftui-view-generator
```

**前提条件：**  
- 了解数据模型及其结构。  
- 可以根据需要阅读规范文件。  
- 明确视图的功能（仅显示数据、交互式、表单或容器类型）。  

**输出结果：**  
生成的 `.ViewName}View.swift` 文件遵循 `ViewModelView` 协议。

**工作流程：**  
通常在讨论需求或阅读规范文件后使用该工具。该工具会自动参考上下文信息，无需提供文件路径或进行问答。

## 参考资料**

- [架构模式](../shared/architecture-patterns.md) – 相关的思维模型和设计模式。
- [FOSMVVMArchitecture.md](../../docs/FOSMVVMArchitecture.md) – 完整的 FOSMVVM 架构文档。
- [fosmvvm-viewmodel-generator](../fosmvvm-viewmodel-generator/SKILL.md) – 用于生成数据模型。
- [fosmvvm-ui-tests-generator](../fosmvvm-ui-tests-generator/SKILL.md) – 用于生成 UI 测试代码。
- [reference.md](reference.md) – 完整的文件模板。

## 版本历史

| 版本 | 发布日期 | 更新内容 |
|---------|------|---------|
| 1.0 | 2026-01-23 | 首个用于生成 SwiftUI 视图的工具版本。 |