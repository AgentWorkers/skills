---
name: fosmvvm-viewmodel-test-generator
description: 生成具有可编码的往返数据传输功能、版本控制稳定性以及多语言翻译验证能力的 ViewModel 测试用例。
homepage: https://github.com/foscomputerservices/FOSUtilities
metadata: {"clawdbot": {"emoji": "🔬", "os": ["darwin", "linux"]}}
---
# FOSMVVM 视模型测试生成器

该工具可根据 FOSMVVM 的测试模式为视图模型生成测试文件。

## 概念基础

> 有关完整的架构信息，请参阅 [FOSMVVMArchitecture.md](../../docs/FOSMVVMArchitecture.md#testing-support) | [OpenClaw 参考文档]({baseDir}/references/FOSMVVMArchitecture.md)

在 FOSMVVM 中，视图模型的测试主要验证三个关键方面：

1. **可编码的往返转换** – 视模型能够进行编码和解码操作，且数据不会丢失。
2. **版本稳定性** – 结构没有发生意外变化。
3. **多语言支持** – 所有的 `@LocalizedString` 属性在所有支持的语言中都有对应的值。

`LocalizableTestCase` 协议提供了统一的测试基础设施，可以一次性完成这三个方面的验证。

---

## 适用场景

- 为新视图模型创建测试用例。
- 为现有视图模型添加测试覆盖。
- 验证不同语言环境下的本地化完整性。
- 测试包含嵌套子视图模型的视图模型。
- 验证 `@LocalizedSubs` 的替换行为。

## 生成内容

| 文件 | 位置 | 用途 |
|------|----------|---------|
| `{Name}ViewModelTests.swift` | `Tests/{Target}Tests/Localization/` | 符合 `LocalizableTestCase` 标准的测试套件 |
| `{Name}ViewModel.yml` | `Tests/{Target}Tests/TestYAML/` | 测试用到的 YAML 翻译文件（如需要） |

---

## 测试模式

### 标准模式（大多数测试）

对于大多数视图模型，只需一行代码即可完成所有测试：

```swift
@Test func dashboardViewModel() throws {
    try expectFullViewModelTests(DashboardViewModel.self)
}
```

该代码会验证：
- 可编码的编码/解码功能。
- 视模型的版本稳定性。
- 所有语言（默认为 en 和 es）的翻译是否正确。

**这适用于绝大多数视图模型的测试。**

### 扩展模式（特定格式验证）

当需要验证特定的格式行为（如替换操作、复合字符串等）时，可以添加针对特定语言的断言：

```swift
@Test func greetingWithSubstitution() throws {
    try expectFullViewModelTests(GreetingViewModel.self)

    // Verify specific substitution behavior
    let vm: GreetingViewModel = try .stub()
        .toJSON(encoder: encoder(locale: en))
        .fromJSON()

    #expect(try vm.welcomeMessage.localizedString == "Welcome, John!")
}
```

此模式为可选选项，仅在需要验证特定格式时使用。

---

## LocalizableTestCase 协议

测试套件遵循 `LocalizableTestCase` 协议，以使用统一的测试基础设施：

```swift
import FOSFoundation
@testable import FOSMVVM
import FOSTesting
import Foundation
import Testing
@testable import {ViewModelsTarget}

@Suite("My ViewModel Tests")
struct MyViewModelTests: LocalizableTestCase {
    let locStore: LocalizationStore

    init() throws {
        self.locStore = try Self.loadLocalizationStore(
            bundle: {ViewModelsTarget}.resourceAccess,
            resourceDirectoryName: ""
        )
    }
}
```

`{ViewModelsTarget}.resourceAccess` 是在创建视图模型 SPM 目标时通过 `FOSResourceAccessor` 构建工具插件定义的资源访问器。

### LocalizableTestCase 提供的功能

| 属性/方法 | 用途 |
|-----------------|---------|
| `locStore` | 必需 - 用于存储本地化数据的存储机制 |
| `locales` | 可选 - 需要测试的语言（默认为 en 和 es） |
| `encoder(locale:)` | 创建用于本地化的 JSONEncoder 对象 |
| `en`, `es`, `enGB`, `enUS` | 语言常量 |

### 测试方法

| 方法 | 适用场景 |
|--------|----------|
| `expectFullViewModelTests(_:)` | **主要** - 完整的视图模型测试 |
| `expectTranslations(_:)` | 仅验证翻译内容 |
| `expectFullFieldValidationModelTests(_:)` | 测试字段验证模型 |
| `expectFullFormFieldTests(_:)` | 测试表单字段实例 |
| `expectCodable(_:encoder:)` | 仅验证可编码性 |
| `expectVersionedViewModel(_:)` | 仅验证版本稳定性 |

---

## YAML 文件要求

### 包含 `@LocalizedString` 的视图模型

每个具有 `@LocalizedString` 属性的视图模型都需要对应的 YAML 文件：

```swift
@ViewModel
public struct DashboardViewModel: RequestableViewModel {
    @LocalizedString public var pageTitle      // Needs YAML entry
    @LocalizedString public var emptyMessage   // Needs YAML entry
    public let itemCount: Int                   // No YAML needed
}
```

```yaml
# DashboardViewModel.yml
en:
  DashboardViewModel:
    pageTitle: "Dashboard"
    emptyMessage: "No items yet"

es:
  DashboardViewModel:
    pageTitle: "Tablero"
    emptyMessage: "No hay elementos todavía"
```

### 嵌套视图模型

如果视图模型包含子视图模型，则层次结构中的所有类型都需要对应的 YAML 文件：

```swift
@ViewModel
public struct BoardViewModel: RequestableViewModel {
    @LocalizedString public var title
    public let cards: [CardViewModel]  // Child ViewModel
}

@ViewModel
public struct CardViewModel {
    @LocalizedString public var cardTitle
}
```

`BoardViewModel` 和 `CardViewModel` 需要各自的 YAML 文件。

### 私有测试视图模型

如果测试中使用了私有视图模型结构来模拟特定场景，这些私有模型也需要对应的 YAML 文件：

```swift
// In test file
private struct TestParentViewModel: ViewModel {
    @LocalizedString var title
    let children: [TestChildViewModel]
}

private struct TestChildViewModel: ViewModel {
    @LocalizedString var label
}
```

请将这些私有模型的信息添加到测试 YAML 文件中。

---

## 使用方法

**调用方式：**
/fosmvvm-viewmodel-test-generator

**前提条件：**
- 了解视图模型的结构。
- 确定了需要测试的本地化属性（如 `@LocalizedString`、`@LocalizedSubs` 等）。
- 已经存在或需要创建 YAML 本地化文件。
- 如果有嵌套的子视图模型，也需要识别它们。

**工作流程整合：**
此工具用于为视图模型添加测试覆盖。它会自动参考之前的讨论内容，无需提供文件路径或进行问答。通常与 `fosmvvm-viewmodel-generator` 工具配合使用。

## 模式实现

该工具会根据之前的讨论内容来确定测试的结构：

### 视模型分析

根据讨论内容，工具会识别：
- 需要测试的视图模型。
- 需要验证的本地化属性。
- 嵌套在父视图模型中的子视图模型。
- 需要特别验证的替换行为。

### YAML 文件完整性检查

验证以下内容的完整性：
- 视模型的 YAML 文件是否完整（包含所有 `@LocalizedString` 属性）。
- 嵌套视图模型的 YAML 文件是否齐全。
- 是否覆盖了所需的语言（en、es 或项目自定义的语言）。

### 测试文件生成

生成的测试套件包含：
- 符合 `LocalizableTestCase` 标准的测试代码。
- 本地化数据存储的初始化。
- 对每个视图模型调用 `expectFullViewModelTests()` 方法。
- 可选的针对特定格式的测试（如替换操作、复合字符串）。

### 信息来源

该工具的信息来源包括：
- 之前的讨论内容：讨论过的或新创建的视图模型。
- 视模型代码：Claude 从代码库中读取的视图模型信息。
- YAML 文件：从代码库中分析现有的本地化数据。
- 项目中的现有测试文件：用于参考的测试模式。

---

## 文件模板

完整的文件模板请参阅 [reference.md](reference.md)。

---

## 常见场景

- **测试单个顶层视图模型**  
```swift
@Test func dashboardViewModel() throws {
    try expectFullViewModelTests(DashboardViewModel.self)
}
```

- **测试多个相关视图模型**  
```swift
@Test func boardViewModels() throws {
    try expectFullViewModelTests(BoardViewModel.self)
    try expectFullViewModelTests(ColumnViewModel.self)
    try expectFullViewModelTests(CardViewModel.self)
}
```

- **使用自定义语言进行测试**  
```swift
var locales: Set<Locale> { [en, es, enGB] }  // Override default

@Test func multiLocaleViewModel() throws {
    try expectFullViewModelTests(MyViewModel.self)
    // Tests en, es, AND en-GB
}
```

- **测试替换行为**  
```swift
@Test func greetingSubstitutions() throws {
    try expectFullViewModelTests(GreetingViewModel.self)

    let vm: GreetingViewModel = try .stub(userName: "Alice")
        .toJSON(encoder: encoder(locale: en))
        .fromJSON()

    #expect(try vm.welcomeMessage.localizedString == "Welcome, Alice!")
}
```

- **测试嵌套视图模型**  
```swift
@Test func parentWithChildren() throws {
    // Tests parent AND verifies children can be encoded/decoded
    try expectFullViewModelTests(ParentViewModel.self)

    // Optionally verify specific child values
    let vm: ParentViewModel = try .stub()
        .toJSON(encoder: encoder(locale: en))
        .fromJSON()

    #expect(try vm.children[0].label.localizedString == "Child 1")
}
```

---

## 故障排除

### “缺少翻译” 错误

**原因：** 某个 `@LocalizedString` 属性对应的 YAML 文件缺失。

**解决方法：** 在 YAML 文件中添加该属性：
```yaml
en:
  MyViewModel:
    pageTitle: "Page Title"  # Add this
```

### “本地化待处理” 错误

**原因：** 视模型在编码时没有使用正确的本地化编码器。

**解决方法：** 确保使用了 `encoderlocale:)` 或 `expectFullViewModelTests()` 方法。

### 测试通过但翻译结果不正确

**原因：** YAML 文件中的值可能存在拼写错误或内容错误。

**解决方法：** 添加相应的断言来验证值的准确性：
```swift
let vm = try .stub().toJSON(encoder: encoder(locale: en)).fromJSON()
#expect(try vm.title.localizedString == "Expected Value")
```

---

## 命名规范

| 术语 | 命名规则 | 例子 |
|---------|------------|---------|
| 测试套件 | `{Feature}ViewModelTests` | 例如：`DashboardViewModelTests` |
| 测试文件 | `{Feature}ViewModelTests.swift` | 例如：`DashboardViewModelTests.swift` |
| YAML 文件 | `{ViewModelName}.yml` | 例如：`DashboardViewModel.yml` |
| 测试方法 | `{viewModelName}()` 或描述性名称 | 例如：`dashboardViewModel()` |

---

## 参考资料

- [FOSMVVMArchitecture.md - 测试支持](../../docs/FOSMVVMArchitecture.md#testing-support) - 架构概述
- [fosmvvm-viewmodel-generator](../fosmvvm-viewmodel-generator/SKILL.md) - 用于生成视图模型的工具
- [fosmvvm-fields-generator](../fosmvvm-fields-generator/SKILL.md) - 用于表单验证测试的工具
- [reference.md](reference.md) - 完整的文件模板

---

## 版本历史

| 版本 | 更新日期 | 更新内容 |
|---------|------|---------|
| 1.0 | 2025-01-02 | 初始版本 |
| 1.1 | 2026-01-19 | 更新 `LocalizableTestCase` 示例，使用 `{ViewModelsTarget}.resourceAccess` 模式。 |
| 1.2 | 2026-01-24 | 采用基于上下文的信息处理方式（不再解析文件路径或进行问答）。工具现在直接参考之前的讨论内容，而不是依赖文件路径或用户输入。 |