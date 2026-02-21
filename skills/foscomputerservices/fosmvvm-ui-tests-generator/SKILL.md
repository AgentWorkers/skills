---
name: fosmvvm-ui-tests-generator
description: 使用XCTest和FOSTestingUI为FOSMVVM的SwiftUI视图生成UI测试。测试内容包括可访问性标识符（accessibility identifiers）、ViewModelOperations以及测试数据的传输（test data transport）。
homepage: https://github.com/foscomputerservices/FOSUtilities
metadata: {"clawdbot": {"emoji": "🖥️", "os": ["darwin"]}}
---
# FOSMVVM UI 测试生成器

为 FOSMVVM 应用程序中的 ViewModelViews 生成全面的 UI 测试。

## 概念基础

> 有关完整的架构信息，请参阅 [FOSMVVMArchitecture.md](../../docs/FOSMVVMArchitecture.md) | [OpenClaw 参考]({{baseDir}/references/FOSMVVMArchitecture.md)

FOSMVVM 中的 UI 测试遵循特定的模式，该模式利用了以下组件：
- **FOSTestingUI** 框架作为测试基础设施
- **ViewModelOperations** 来验证业务逻辑是否被调用
- **可访问性标识符** 来查找 UI 元素
- **测试数据传输器** 来将操作存根传递给应用程序

```
┌─────────────────────────────────────────────────────────────┐
│                    UI Test Architecture                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Test File (XCTest)                 App Under Test          │
│  ┌──────────────────┐              ┌──────────────────┐     │
│  │ MyViewUITests    │              │ MyView           │     │
│  │                  │              │                  │     │
│  │ presentView() ───┼─────────────►│ Show view with   │     │
│  │   with stub VM   │              │   stubbed data   │     │
│  │                  │              │                  │     │
│  │ Interact via ────┼─────────────►│ UI elements with │     │
│  │   identifiers    │              │   .uiTestingId   │     │
│  │                  │              │                  │     │
│  │ Assert on UI     │              │ .testData────────┼──┐  │
│  │   state          │              │   Transporter    │  │  │
│  │                  │              └──────────────────┘  │  │
│  │ viewModelOps() ◄─┼─────────────────────────────────────┘  │
│  │   verify calls   │              Stub Operations          │
│  └──────────────────┘                                        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 核心组件

### 1. 基础测试用例类

每个项目都应该有一个继承自 `ViewModelViewTestCase` 的基础测试用例：

```swift
class MyAppViewModelViewTestCase<VM: ViewModel, VMO: ViewModelOperations>:
    ViewModelViewTestCase<VM, VMO>, @unchecked Sendable {

    @MainActor func presentView(
        configuration: TestConfiguration,
        viewModel: VM = .stub(),
        timeout: TimeInterval = 3
    ) throws -> XCUIApplication {
        try presentView(
            testConfiguration: configuration.toJSON(),
            viewModel: viewModel,
            timeout: timeout
        )
    }

    override func setUp() async throws {
        try await super.setUp(
            bundle: Bundle.main,
            resourceDirectoryName: "",
            appBundleIdentifier: "com.example.MyApp"
        )

        continueAfterFailure = false
    }
}
```

**关键点：**
- 通用性：适用于所有 `ViewModel` 和 `ViewModelOperations`
- 使用项目特定的配置包装 FOSTestingUI 的 `presentView()`
- 设置 bundle 和应用 bundle 标识符
- `continueAfterFailure = false`：在测试失败时立即停止测试

### 2. 单个 UI 测试文件

每个 ViewModelView 都有一个对应的 UI 测试文件。

**对于具有操作的视图：**

```swift
final class MyViewUITests: MyAppViewModelViewTestCase<MyViewModel, MyViewOps> {
    // UI Tests - verify UI state
    func testButtonEnabled() async throws {
        let app = try presentView(viewModel: .stub(enabled: true))
        XCTAssertTrue(app.myButton.isEnabled)
    }

    // Operation Tests - verify operations were called
    func testButtonTap() async throws {
        let app = try presentView(configuration: .requireSomeState())
        app.myButton.tap()

        let stubOps = try viewModelOperations()
        XCTAssertTrue(stubOps.myOperationCalled)
    }
}

private extension XCUIApplication {
    var myButton: XCUIElement {
        buttons.element(matching: .button, identifier: "myButtonIdentifier")
    }
}
```

**对于没有操作的视图（仅用于显示）：**

使用空的存根操作协议：

```swift
// In your test file
protocol MyViewStubOps: ViewModelOperations {}
struct MyViewStubOpsImpl: MyViewStubOps {}

final class MyViewUITests: MyAppViewModelViewTestCase<MyViewModel, MyViewStubOpsImpl> {
    // UI Tests only - no operation verification
    func testDisplaysCorrectly() async throws {
        let app = try presentView(viewModel: .stub(title: "Test"))
        XCTAssertTrue(app.titleLabel.exists)
    }
}
```

**使用场景：**
- **具有操作的视图**：执行操作的交互式视图（表单、调用 API 的按钮等）
- **没有操作的视图**：仅用于显示的视图（卡片、详细信息视图、静态内容）

### 3. XCUIElement 辅助扩展

用于与 UI 元素交互的常用辅助函数：

```swift
extension XCUIElement {
    var text: String? {
        value as? String
    }

    func typeTextAndWait(_ string: String, timeout: TimeInterval = 2) {
        typeText(string)
        _ = wait(for: \.text, toEqual: string, timeout: timeout)
    }

    func tapMenu() {
        if isHittable {
            tap()
        } else {
            coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: 0.5)).tap()
        }
    }
}
```

### 4. 视图需求

**对于具有操作的视图：**

```swift
public struct MyView: ViewModelView {
    #if DEBUG
    @State private var repaintToggle = false
    #endif

    private let viewModel: MyViewModel
    private let operations: MyViewModelOperations

    public var body: some View {
        Button(action: doSomething) {
            Text(viewModel.buttonLabel)
        }
        .uiTestingIdentifier("myButtonIdentifier")
        #if DEBUG
        .testDataTransporter(viewModelOps: operations, repaintToggle: $repaintToggle)
        #endif
    }

    public init(viewModel: MyViewModel) {
        self.viewModel = viewModel
        self.operations = viewModel.operations
    }

    private func doSomething() {
        operations.doSomething()
        toggleRepaint()
    }

    private func toggleRepaint() {
        #if DEBUG
        repaintToggle.toggle()
        #endif
    }
}
```

**对于没有操作的视图（仅用于显示）：**

```swift
public struct MyView: ViewModelView {
    private let viewModel: MyViewModel

    public var body: some View {
        VStack {
            Text(viewModel.title)
            Text(viewModel.description)
        }
        .uiTestingIdentifier("mainContent")
    }

    public init(viewModel: MyViewModel) {
        self.viewModel = viewModel
    }
}
```

**关键模式（对于具有操作的视图）：**
- 使用 `@State private var repaintToggle = false` 来触发测试数据传输
- 在 `DEBUG` 模式下使用 `.testDataTransporter(viewModelOps:repaintToggle:)` 修饰符
- 每次操作调用后调用 `toggleRepaint()`
- `operations` 从 `viewModelOperations` 中获取

**仅用于显示的视图：**
- 不需要 `repaintToggle`
- 不需要 `.testDataTransporter()`
- 只需要为要测试的元素添加 `.uiTestingIdentifier()`

## ViewModelOperations（可选）

并非所有视图都需要 `ViewModelOperations`：

**需要操作的视图：**
- 具有提交/取消操作的表单
- 调用业务逻辑或 API 的视图
- 触发应用状态变化的交互式视图
- 具有用户发起的异步操作的视图

**不需要操作的视图：**
- 仅用于显示的卡片或详细信息视图
- 静态内容视图
- 仅用于渲染数据的服务器托管视图

**对于没有操作的视图：**

在您的 ViewModel 旁边创建一个空的操作文件：

```swift
// MyDisplayViewModelOperations.swift
import FOSMVVM
import Foundation

public protocol MyDisplayViewModelOperations: ViewModelOperations {}

#if canImport(SwiftUI)
public final class MyDisplayViewStubOps: MyDisplayViewModelOperations, @unchecked Sendable {
    public init() {}
}
#endif
```

然后在测试中使用它：

```swift
final class MyDisplayViewUITests: MyAppViewModelViewTestCase<
    MyDisplayViewModel,
    MyDisplayViewStubOps
> {
    // Only test UI state, no operation verification
}
```

视图本身不需要：
- `repaintToggle` 状态
- `.testDataTransporter()` 修饰符
- `operations` 属性
- `toggleRepaint()` 函数

只需为要验证的元素添加 `.uiTestingIdentifier()`。

## 测试类别

### UI 状态测试

验证 UI 是否根据 ViewModel 状态正确显示：

```swift
func testButtonDisabledWhenNotReady() async throws {
    let app = try presentView(viewModel: .stub(ready: false))
    XCTAssertFalse(app.submitButton.isEnabled)
}

func testButtonEnabledWhenReady() async throws {
    let app = try presentView(viewModel: .stub(ready: true))
    XCTAssertTrue(app.submitButton.isEnabled)
}
```

### 操作测试

验证用户交互是否调用了正确的操作：

```swift
func testSubmitButtonInvokesOperation() async throws {
    let app = try presentView(configuration: .requireAuth())
    app.submitButton.tap()

    let stubOps = try viewModelOperations()
    XCTAssertTrue(stubOps.submitCalled)
    XCTAssertFalse(stubOps.cancelCalled)
}
```

### 导航测试

验证导航流程是否正常工作：

```swift
func testNavigationToDetailView() async throws {
    let app = try presentView()
    app.itemRow.tap()

    XCTAssertTrue(app.detailView.exists)
}
```

## 何时使用此技能

- 为新 ViewModelView 添加 UI 测试
- 为 FOSMVVM 项目设置 UI 测试基础设施
- 遵循需要测试覆盖范围的实现计划
- 验证用户交互流程

## 该技能生成的内容

### 初始设置（每个项目只需执行一次）

| 文件 | 位置 | 用途 |
|------|----------|---------|
| `{ProjectName}ViewModelViewTestCase.swift` | `Tests/UITests/Support/` | 所有 UI 测试的基础测试用例 |
| `XCUIElement.swift` | `Tests/UITests/Support/` | XCUIElement 的辅助扩展 |

### 每个 ViewModelView

| 文件 | 位置 | 用途 |
|------|----------|---------|
| `{ViewName}ViewModelOperations.swift` | `Sources/{ViewModelsTarget}/{Feature}/` | 操作协议和存根（如果视图具有交互功能） |
| `{ViewName}UITests.swift` | `Tests/UITests/Views/{Feature}/` | 视图的 UI 测试 |

**注意：** 没有用户交互的视图使用仅包含协议和最小存根的空操作文件。

## 项目结构配置

| 占位符 | 描述 | 示例 |
|-------------|-------------|---------|
| `{ProjectName}` | 你的项目/应用程序名称 | `MyApp`, `TaskManager` |
| `{ViewName}` | ViewModelView 的名称（不包含 "View" 后缀） | `TaskList`, `Dashboard` |
| `{Feature}` | 功能/模块分组 | `Tasks`, `Settings` |

## 如何使用此技能

**调用方式：**
/fosmvvm-ui-tests-generator

**先决条件：**
- 了解视图和 ViewModel 的结构
- 确定 `ViewModelOperations` 的类型（或确认其为仅用于显示）
- 讨论过交互式元素和用户流程

**工作流程集成：**
此技能通常在实现 ViewModelViews 之后使用。该技能会自动参考之前的讨论内容——无需提供文件路径或进行问答。通常会与 `fosmvvm-swiftui-view-generator` 或 `fosmvvm-react-view-generator` 一起使用。

## 模式实现

此技能根据之前的讨论内容来确定测试结构：

### 测试类型检测

根据讨论内容，技能会识别：
- **是否需要基础测试基础设施**
- **ViewModel 的类型**（来自之前的讨论或视图实现）
- **ViewModelOperations 的类型**（来自视图实现或讨论内容）
- **是否需要验证操作**

### 视图分析

根据已有的需求：
- **交互式元素**（需要测试覆盖的按钮、字段、控件）
- **用户流程**（导航路径、表单提交、拖放）
- **状态变化**（启用/禁用、可见/隐藏、错误状态）
- **操作触发器**（哪些 UI 操作会触发哪些操作）

### 基础设施规划

根据项目状态：
- **基础测试用例**（如果需要首次测试则创建，如果已存在则重用）
- **XCUIElement 扩展**（用于常见交互的辅助方法）
- **应用 bundle 标识符**（用于启动测试宿主）

### 测试文件生成

对于特定的视图：
1. 继承自基础测试用例的测试类
2. UI 状态测试（根据 ViewModel 验证显示效果）
3. 操作测试（验证用户交互是否调用了正确的操作）
4. 包含元素访问器的 `XCUIApplication` 扩展

### 视图需求

确保测试标识符和数据传输：
1. 在所有交互式元素上添加 `.uiTestingIdentifier()`
2. 如果有操作，则添加 `@State private var repaintToggle`
3. 如果有操作，则添加 `.testDataTransporter()` 修饰符
4. 每次操作后调用 `toggleRepaint()`

### 上下文来源

技能参考的信息来自：
- **之前的讨论**：讨论过的视图需求和用户流程
- **视图实现**：如果 Claude 已将视图代码读取到上下文中
- **ViewModelOperations**：来自代码库或讨论内容

## 关键模式

### 测试配置模式

对于需要特定应用状态的测试，使用 `TestConfiguration`：

```swift
func testWithSpecificState() async throws {
    let app = try presentView(
        configuration: .requireAuth(userId: "123")
    )
    // Test with authenticated state
}
```

### 元素访问器模式

在私有扩展中定义元素访问器：

```swift
private extension XCUIApplication {
    var submitButton: XCUIElement {
        buttons.element(matching: .button, identifier: "submitButton")
    }

    var cancelButton: XCUIElement {
        buttons.element(matching: .button, identifier: "cancelButton")
    }

    var firstItem: XCUIElement {
        buttons.element(matching: .button, identifier: "itemButton").firstMatch
    }
}
```

### 操作验证模式

在用户交互后，验证操作是否被调用：

```swift
func testDecrementButton() async throws {
    let app = try presentView(configuration: .requireDevice())
    app.decrementButton.tap()

    let stubOps = try viewModelOperations()
    XCTAssertTrue(stubOps.decrementCalled)
    XCTAssertFalse(stubOps.incrementCalled)
}
```

### 方向设置模式

如果需要，在 `setUp()` 中设置设备方向：

```swift
override func setUp() async throws {
    try await super.setUp()

    #if os(iOS)
    XCUIDevice.shared.orientation = .portrait
    #endif
}
```

## 视图测试检查清单

**所有视图：**
- 在所有要测试的元素上添加 `.uiTestingIdentifier()`

**具有操作的视图（交互式视图）：**
- 设置 `@State private var repaintToggle = false`
- 使用 `.testDataTransporterviewModelOps:repaintToggle:)` 修饰符
- 调用 `toggleRepaint()` 辅助函数
- 每次操作调用后调用 `toggleRepaint()`
- 从 `viewModelOperations` 中获取 `operations`

**没有操作的视图（仅用于显示）：**
- 不需要 `repaintToggle`
- 不需要 `.testDataTransporter()`
- 不需要 `operations` 属性
- 在初始化时从 `viewModelOperations` 中获取 `operations`

## 常见测试模式

### 测试异步操作

```swift
func testAsyncOperation() async throws {
    let app = try presentView()
    app.loadButton.tap()

    // Wait for UI to update
    _ = app.waitForExistence(timeout: 3)

    let stubOps = try viewModelOperations()
    XCTAssertTrue(stubOps.loadCalled)
}
```

### 测试表单输入

```swift
func testFormInput() async throws {
    let app = try presentView()

    let emailField = app.emailTextField
    emailField.tap()
    emailField.typeTextAndWait("user@example.com")

    app.submitButton.tap()

    let stubOps = try viewModelOperations()
    XCTAssertTrue(stubOps.submitCalled)
}
```

### 测试错误状态

```swift
func testErrorDisplay() async throws {
    let app = try presentView(viewModel: .stub(hasError: true))

    XCTAssertTrue(app.errorAlert.exists)
    XCTAssertEqual(app.errorMessage.text, "An error occurred")
}
```

## 文件模板

请参阅 [reference.md](reference.md) 以获取完整的文件模板。

## 命名约定

| 概念 | 命名约定 | 示例 |
|---------|------------|---------|
| 基础测试用例 | `{ProjectName}ViewModelViewTestCase` | `MyAppViewModelViewTestCase` |
| UI 测试文件 | `{ViewName}UITests` | `TaskListViewUITests` |
| 测试方法（UI 状态） | `test{Condition}` | `testButtonEnabled` |
| 测试方法（操作） | `test{Action}` | `testSubmitButton` |
| 元素访问器 | `{elementName}` | `submitButton`, `emailTextField` |
| UI 测试标识符 | `{elementName}Identifier` 或 `{elementName}` | `"submitButton"`, `"emailTextField"` |

## 参考资料

- [Architecture Patterns](../shared/architecture-patterns.md) - 心智模型和模式
- [FOSMVVMArchitecture.md](../../docs/FOSMVVMArchitecture.md) - 完整的 FOSMVVM 架构
- [fosmvvm-viewmodel-generator](../fosmvvm-viewmodel-generator/SKILL.md) - 用于创建 ViewModel
- [fosmvvm-swiftui-app-setup](../fosmvvm-swiftui-app-setup/SKILL.md) - 用于设置应用测试宿主
- [reference.md](reference.md) - 完整的文件模板

## 版本历史

| 版本 | 日期 | 更改内容 |
|---------|------|---------|
| 1.0 | 2026-01-23 | 首个 UI 测试技能 |
| 1.1 | 2026-01-24 | 更新为基于上下文的方法（移除文件解析/问答）。技能参考之前的讨论内容，而不是询问文件路径或接受文件路径。