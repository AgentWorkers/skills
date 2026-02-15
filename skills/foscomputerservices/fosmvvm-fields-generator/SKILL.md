---
name: fosmvvm-fields-generator
description: 生成具有验证规则的 FOSMVVM 字段协议、表单字段（FormField）定义以及本地化消息。只需定义一次表单契约（form contract），即可在所有地方进行验证。
homepage: https://github.com/foscomputerservices/FOSUtilities
metadata: {"clawdbot": {"emoji": "📋", "os": ["darwin", "linux"]}}
---

# FOSMVVM 表单字段生成器

根据 FOSMVVM 模式生成表单规范。

## 概念基础

> 有关完整的架构信息，请参阅 [FOSMVVMArchitecture.md](../../docs/FOSMVVMArchitecture.md) | [OpenClaw 参考文档]({{baseDir}}/references/FOSMVVMArchitecture.md)

**表单规范**（实现为 `{Name}Fields` 协议）是用户输入的**唯一权威来源**。它回答了以下问题：

1. **用户可以提供哪些数据？**（属性）
2. **这些数据应该如何呈现？**（`FormField`，包括类型、键盘输入方式、自动填充功能）
3. **有哪些约束条件？**（验证规则）
4. **应该显示哪些提示信息？**（本地化的标题、占位符、错误信息）

### 为什么这很重要

表单规范**只需定义一次，即可在所有地方使用**：

```swift
// Same protocol adopted by different consumers:
struct CreateIdeaRequestBody: ServerRequestBody, IdeaFields { ... }  // HTTP transmission
@ViewModel struct IdeaFormViewModel: IdeaFields { ... }              // Form rendering
final class Idea: Model, IdeaFields { ... }                          // Persistence validation
```

这确保了：
- **一致的验证规则**——客户端和服务器使用相同的规则
- **共享的本地化资源**——一个 YAML 文件可以在所有地方使用
- **单一的权威来源**——一旦修改，所有地方都会受到影响

### 与 FOSMVVM 的关联

表单规范与以下系统集成：
- **本地化系统**：`FormField` 的标题/占位符和验证信息使用 `LocalizableString`
- **验证系统**：实现 `ValidatableModel` 协议
- **请求系统**：`RequestBody` 类型使用 `Fields` 进行验证后传输
- **视图模型系统**：视图模型使用 `Fields` 来渲染表单

## 何时使用此技能

- 定义新的表单（创建、编辑、过滤、搜索）
- 为请求体添加验证功能
- 任何需要遵循 `ValidatableModel` 规范的数据类型
- 当 `fosmvvm-fluent-datamodel-generator` 需要为数据模型生成表单字段时

## 该技能生成的文件内容

一个完整的表单规范由 **3 个文件** 组成：

| 文件 | 用途 |
|------|---------|
| `{Name}Fields.swift` | 协议 + `FormField` 定义 + 验证方法 |
| `{Name}FieldsMessages.swift` | 包含 `@LocalizedString` 属性的 `@FieldValidationModel` 结构体 |
| `{Name}FieldsMessages.yml` | 包含本地化字符串的 YAML 文件（标题、占位符、错误信息） |

## 项目结构配置

请将占位符替换为您项目的实际路径：

| 占位符 | 描述 | 示例 |
|-------------|-------------|---------|
| `{ViewModelsTarget}` | 共享视图模型的目标目录 | `ViewModels`, `SharedViewModels` |
| `{ResourcesPath}` | 本地化资源路径 | `Sources/Resources` |

**预期结构：**
```
Sources/
  {ViewModelsTarget}/
    FieldModels/
      {Name}Fields.swift
      {Name}FieldsMessages.swift
  {ResourcesPath}/
    FieldModels/
      {Name}FieldsMessages.yml
```

## 如何使用此技能

**调用方式：**
`/fosmvvm-fields-generator`

**前提条件：**
- 从对话上下文中理解表单的用途
- 讨论了字段的要求（名称、类型、约束条件）
- 确定了表单所关联的实体（该表单用于创建或编辑什么实体）

**工作流程集成：**
此技能用于定义表单验证和用户输入契约。它自动参考对话上下文，无需提供文件路径或问答信息。通常在 `fosmvvm-fluent-datamodel-generator` 之前使用，用于基于表单的数据模型。

## 模式实现

此技能根据对话上下文来确定 `Fields` 协议的结构：

### 表单分析

从对话上下文中，技能会识别：
- **表单的用途**（创建、编辑、过滤、登录、设置）
- **表单关联的实体**（用户、想法、文档等）
- **协议命名**（例如 `CreateIdeaFields`, `UpdateProfile`, `LoginCredentials`）

### 字段设计

对于每个字段，需要指定：
- **属性信息**（名称、类型、是否必填）
- **显示类型**（`FormFieldType`：文本、文本区域、下拉菜单、复选框）
- **输入方式**（`FormInputType`：电子邮件、密码、电话号码、日期）
- **约束条件**（是否必填、长度范围、值范围、日期范围）
- **本地化设置**（标题、占位符、验证错误信息）

### 文件生成顺序

1. 包含 `FormField` 定义和验证方法的 `Fields` 协议
2. 包含 `@LocalizedString` 属性的 `FieldsMessages` 结构体
3. 包含本地化字符串的 `FieldsMessages.yml` 文件

### 信息来源

此技能参考以下信息：
- **之前的对话**：讨论的表单要求和字段规范
- **规范文件**：如果 Claude 已将表单规范读取到上下文中
- **现有代码库中的模式**：分析类似的 `Fields` 协议

## 关键模式

### 协议结构

```swift
public protocol {Name}Fields: ValidatableModel, Codable, Sendable {
    var fieldName: FieldType { get set }
    var {name}ValidationMessages: {Name}FieldsMessages { get }
}
```

### `FormField` 定义

```swift
static var contentField: FormField<String?> { .init(
    fieldId: .init(id: "content"),
    title: .localized(for: {Name}FieldsMessages.self, propertyName: "content", messageKey: "title"),
    placeholder: .localized(for: {Name}FieldsMessages.self, propertyName: "content", messageKey: "placeholder"),
    type: .textArea(inputType: .text),
    options: [
        .required(value: true)
    ] + FormInputOption.rangeLength(contentRange)
) }
```

### `FormField` 类型参考

| `FormFieldType` | 使用场景 |
|---------------|----------|
| `.text(inputType:)` | 单行输入 |
| `.textArea(inputType:)` | 多行输入 |
| `.checkbox` | 布尔值切换 |
| `.select` | 下拉菜单选择 |
| `.colorPicker` | 颜色选择 |

### `FormInputType` 参考（常见类型）

| `FormInputType` | 输入方式/自动填充方式 |
|---------------|-------------------|
| `.text` | 默认键盘输入 |
| `.emailAddress` | 电子邮件输入框，支持自动填充 |
| `.password` | 安全输入框 |
| `.tel` | 电话号码输入框 |
| `.url` | URL 输入框 |
| `.date`, `.datetimeLocal` | 日期选择器 |
| `.givenName`, `.familyName` | 姓名自动填充 |

### 验证方法模式

```swift
internal func validateContent(_ fields: [FormFieldBase]?) -> [ValidationResult]? {
    guard fields == nil || (fields?.contains(Self.contentField) == true) else {
        return nil
    }

    var result = [ValidationResult]()

    if content.isEmpty {
        result.append(.init(
            status: .error,
            field: Self.contentField,
            message: {name}ValidationMessages.contentRequiredMessage
        ))
    } else if !Self.contentRange.contains(NSString(string: content).length) {
        result.append(.init(
            status: .error,
            field: Self.contentField,
            message: {name}ValidationMessages.contentOutOfRangeMessage
        ))
    }

    return result.isEmpty ? nil : result
}
```

### 错误信息结构模式

```swift
@FieldValidationModel public struct {Name}FieldsMessages {
    @LocalizedString("content", messageGroup: "validationMessages", messageKey: "required")
    public var contentRequiredMessage

    @LocalizedString("content", messageGroup: "validationMessages", messageKey: "outOfRange")
    public var contentOutOfRangeMessage
}
```

### YAML 结构

```yaml
en:
  {Name}FieldsMessages:
    content:
      title: "Content"
      placeholder: "Enter your content..."
      validationMessages:
        required: "Content is required"
        outOfRange: "Content must be between 1 and 10,000 characters"
```

## 命名规范

| 概念 | 命名规则 | 示例 |
|---------|------------|---------|
| 协议 | `{Name}Fields` | `IdeaFields`, `CreateIdeaFields` |
| 错误信息结构体 | `{Name}FieldsMessages` | `IdeaFieldsMessages` |
| 错误信息属性 | `{name}ValidationMessages` | `ideaValidationMessages` |
| 字段定义 | `{fieldName}Field` | `contentField` |
| 范围常量 | `{fieldName}Range` | `contentRange` |
| 验证方法 | `validate{FieldName}` | `validateContent` |
| 必填提示信息 | `{fieldName}RequiredMessage` | `contentRequiredMessage` |
| 超出范围提示信息 | `{fieldName}OutOfRangeMessage` | `contentOutOfRangeMessage` |

## 参考资料

- [FOSMVVMArchitecture.md](../../docs/FOSMVVMArchitecture.md) - 完整的 FOSMVVM 架构参考
- [fosmvvm-viewmodel-generator](../fosmvvm-viewmodel-generator/SKILL.md) - 用于使用 `Fields` 的视图模型
- [fosmvvm-fluent-datamodel-generator](../fosmvvm-fluent-datamodel-generator/SKILL.md) - 用于实现 `Fields` 的流畅数据模型
- [reference.md] - 完整的文件模板集合

## 版本历史

| 版本 | 更新日期 | 更改内容 |
|---------|------|---------|
| 1.0 | 2024-12-24 | 初始版本 |
| 2.0 | 2024-12-26 | 重新编写，加入概念基础；从 Kairos 特定版本进行通用化 |
| 2.1 | 2026-01-24 | 采用上下文感知的方法（不再解析文件或进行问答；直接参考对话上下文）