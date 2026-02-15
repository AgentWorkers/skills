---
name: fosmvvm-viewmodel-generator
description: 为 SwiftUI 的屏幕、页面和组件生成 FOSMVVM 视模型（ViewModels）。同时提供 RequestableViewModel、本地化绑定（localization bindings）以及代码片段生成器（stub factories）。
homepage: https://github.com/foscomputerservices/FOSUtilities
metadata: {"clawdbot": {"emoji": "🏗️", "os": ["darwin", "linux"]}}
---

# FOSMVVM 视图模型生成器

该工具根据 FOSMVVM 架构模式生成视图模型（ViewModels）。

## 概念基础

> 有关完整的架构信息，请参阅 [FOSMVVMArchitecture.md](../../docs/FOSMVVMArchitecture.md) | [OpenClaw 参考文档]({baseDir}/references/FOSMVVMArchitecture.md)

视图模型（ViewModel）是 Model-View-ViewModel 架构中的桥梁：

---

## 首要决策：托管模式

**这是针对每个视图模型（ViewModel）做出的决策。** 一个应用程序可以同时使用两种模式——例如，一个独立的 iPhone 应用程序可能包含基于服务器的登录功能。

**关键问题：** 这个视图模型的数据来自哪里？

| 数据来源 | 托管模式 | 工厂（Factory） |
|-------------|--------------|---------|
| 服务器/数据库 | 服务器托管 | 手动编写 |
| 本地状态/偏好设置 | 客户端托管 | 通过宏自动生成 |
| **响应错误（捕获的错误）** | **客户端托管** | 通过宏自动生成 |

### 服务器托管模式

当数据来自服务器时：
- 工厂（Factory）是在服务器上手动编写的（遵循 `ViewModelFactory` 协议）
- 工厂从数据库查询数据并构建视图模型（ViewModel）
- 服务器在 JSON 编码过程中进行本地化处理
- 客户端接收完全本地化的视图模型

**示例：** 登录界面、来自 API 的用户信息、显示服务器数据的仪表盘

### 客户端托管模式

当数据存储在设备本地时：
- 使用 `@ViewModel(options: [.clientHostedFactory])`
- 宏会根据初始化参数自动生成工厂（Factory）
- 客户端将 YAML 资源打包到应用程序中
- 客户端在编码过程中进行本地化处理

**示例：** 设置界面、新用户引导流程、优先支持离线功能的场景、错误显示

### 错误显示模式

错误显示是一个典型的客户端托管场景。你已经从 `ResponseError` 中获取到了错误信息——只需将其封装到一个特定的视图模型（ViewModel）中即可：

---

**每个错误场景都有对应的视图模型：**
- `MoveIdeaErrorViewModel` 用于处理 `MoveIdeaRequest.ResponseError`
- `CreateIdeaErrorViewModel` 用于处理 `CreateIdeaRequest.ResponseError`
- `SettingsValidationErrorViewModel` 用于处理设置表单中的错误

**注意：** 不要创建通用的 “ToastViewModel” 或 “ErrorViewModel”——我们避免使用这种统一的错误处理方式。

**关键点：**
- 不需要发送服务器请求——因为你已经捕获到了错误
- `ResponseError` 中的 `LocalizableString` 属性已经完成了本地化处理（由服务器完成）
- 标准的视图模型（ViewModel）会正确处理字符串的编码；已经本地化的字符串会保持原样传递
- 客户端托管的视图模型会封装现有的数据；工厂（Factory）会通过宏自动生成

### 混合模式应用程序

许多应用程序会同时使用这两种模式：

---

**相同的视图模型模式在两种模式下都适用**——只有工厂的创建方式有所不同。

### 核心职责：数据整理

视图模型（ViewModel）的职责是**整理数据以供展示**。这主要发生在两个阶段：
1. **工厂（Factory）**：确定需要哪些数据以及如何转换这些数据
2. **本地化**：确定如何在上下文中展示这些数据（包括考虑地区设置的排序规则）

**视图（View）仅负责渲染数据**——它不应该对视图模型的属性进行组合、格式化或重新排序。

### 视图模型包含的内容

视图模型（ViewModel）回答的问题是：“视图需要显示什么？”

| 内容类型 | 表示方式 | 示例 |
|--------------|---------------------|---------|
| 静态 UI 文本 | `@LocalizedString` | 页面标题、按钮标签（固定文本） |
| 动态枚举值 | `LocalizableString`（存储在本地化资源中） | 状态/情况的显示（参见枚举本地化模式） |
| 动态文本数据 | `@LocalizedSubs` | “欢迎，{name}!”（包含占位符） |
| 组合文本 | `@LocalizedCompoundString` | 从多个部分组成的全名（考虑地区设置） |
| 格式化的日期 | `LocalizableDate` | `createdAt: LocalizableDate` |
| 格式化的数字 | `LocalizableInt` | `totalCount: LocalizableInt` |
| 动态数据 | 普通属性 | `content: String`, `count: Int` |
| 嵌套组件 | 子视图模型（Child ViewModels） | `cards: [CardViewModel]` |

### 视图模型不包含的内容

- 数据库关系（`@Parent`, `@Siblings`）
- 业务逻辑或验证逻辑（这些逻辑位于 `Fields` 协议中）
- 直接暴露给模板的原始数据库 ID（使用类型化的属性）
- 需要视图查找的未本地化的字符串

### 避免的错误模式：在视图中进行数据组合

如果在视图中看到 `+` 或字符串插值操作，那么数据的整理工作应该由视图模型（ViewModel）来完成。

## 视图模型协议层次结构

**视图模型（ViewModel）** 提供以下功能：
- `ServerRequestBody`：可以通过 HTTP 以 JSON 格式发送
- `RetrievablePropertyNames`：支持使用 `@LocalizedString` 进行绑定
- `Identifiable`：具有 `vmId`，用于在 SwiftUI 中唯一标识视图模型
- `Stubbable`：提供 `stub()` 方法，便于测试和预览

**RequestableViewModel** 协议额外提供了用于从服务器获取数据的 `Request` 类型

## 视图模型的两大类别

### 1. 顶层视图模型（RequestableViewModel）

表示整个页面或屏幕。包含：
- 一个关联的 `ViewModelRequest` 类型
- 一个用于从数据库构建视图模型的 `ViewModelFactory`
- 嵌套在其中的子视图模型（Child ViewModels）

---

### 2. 子视图模型（Plain ViewModel）

由父视图模型的工厂生成的嵌套组件。不包含 `Request` 类型。

---

## 显示视图模型（Display ViewModels）与表单视图模型（Form ViewModels）

视图模型（ViewModels）有两种不同的用途：

| 用途 | 视图模型类型 | 是否采用 `Fields` 协议？ |
|---------|----------------|----------------|
| **显示数据**（只读） | 显示视图模型（Display ViewModel） | 不需要 |
| **收集用户输入**（可编辑） | 表单视图模型（Form ViewModel） | 需要 |

### 显示视图模型（Display ViewModels）

用于显示数据——例如卡片、列表、详细信息页面：

**特点：**
- 属性是 `let` 类型（只读）
- 不需要验证
- 没有 `FormField` 定义
- 只负责将模型数据呈现出来

### 表单视图模型（Form ViewModels）

用于收集用户输入——例如创建表单、编辑表单、设置界面：

**特点：**
- 属性是 `var` 类型（可编辑）
- **采用 `Fields` 协议进行验证**
- 从 `Fields` 协议中获取表单字段定义
- 从 `Fields` 协议中获取验证逻辑
- 从 `Fields` 协议中获取本地化的错误消息

### 视图模型之间的关联

---

## 快速决策指南

**关键问题：** “用户是否正在编辑这个视图模型中的数据？”

- **否** → 使用显示视图模型（Display ViewModel）（不需要 `Fields` 协议）
- **是** → 使用表单视图模型（Form ViewModel）（需要 `Fields` 协议）

| 视图模型 | 用户是否进行编辑？ | 是否采用 `Fields` 协议？ |
|-----------|-------------|---------------|
| `UserCardViewModel` | 否 | 否 |
| `UserRowViewModel` | 否 | 否 |
| `UserDetailViewModel` | 否 | 否 |
| `UserFormViewModel` | 是 | `UserFields` |
| `CreateUserViewModel` | 是 | `UserFields` |
| `EditUserViewModel` | 是 | `UserFields` |
| `SettingsViewModel` | 是 | `SettingsFields` |

---

## 何时使用此技能

- 创建新的页面或屏幕
- 添加新的 UI 组件（如卡片、列表项、模态窗口等）
- 在视图中显示来自数据库的数据
- 遵循需要新视图模型的实现计划

## 该技能生成的文件

### 服务器托管模式：顶层视图模型（4 个文件）

| 文件名 | 所在目录 | 用途 |
|------|----------|---------|
| `{Name}ViewModel.swift` | `{ViewModelsTarget}/` | 视图模型结构体 |
| `{Name}Request.swift` | `{ViewModelsTarget}/` | 视图模型请求类型 |
| `{Name}ViewModel.yml` | `{ResourcesPath}/` | 本地化字符串 |
| `{Name}ViewModel+Factory.swift` | `{WebServerTarget}/` | 从数据库构建视图模型的工厂 |

### 客户端托管模式：顶层视图模型（2 个文件）

| 文件名 | 所在目录 | 用途 |
|------|----------|---------|
| `{Name}ViewModel.swift` | `{ViewModelsTarget}/` | 包含 `clientHostedFactory` 选项的视图模型 |
| `{Name}ViewModel.yml` | `{ResourcesPath}/` | 本地化字符串（打包在应用程序中） |

*不需要 `Request` 或 `Factory` 文件——这些文件由宏自动生成！*

### 子视图模型（1-2 个文件，两种模式均适用）

| 文件名 | 所在目录 | 用途 |
|------|----------|---------|
| `{Name}ViewModel.swift` | `{ViewModelsTarget}/` | 视图模型结构体 |
| `{Name}ViewModel.yml` | `{ResourcesPath}/` | 本地化字符串（如果包含 `@LocalizedString`） |

**注意：** 如果子视图模型仅被一个父视图模型使用，并且仅用于显示汇总信息或作为引用（而不是完整的视图模型），则应将其嵌套在父视图模型文件中。请参阅 “嵌套子类型模式”（Nested Child Types Pattern）。

## 项目结构配置

| 占位符 | 描述 | 示例 |
|-------------|-------------|---------|
| `{ViewModelsTarget}` | 共享视图模型（Shared ViewModels）的目标目录 | `ViewModels` |
| `{ResourcesPath}` | 本地化资源目录 | `Sources/Resources` |
| `{WebServerTarget}` | 服务器端目标目录 | `WebServer`, `AppServer` |

## 如何使用此技能

**使用方法：**
`/fosmvvm-viewmodel-generator`

**先决条件：**
- 了解视图的需求（通过对话确定）
- 确定数据来源（服务器/数据库或本地状态）
- 决定是显示数据还是收集用户输入（如果涉及用户输入，则需要 `Fields` 协议）

**工作流程集成：**  
通常在讨论视图需求或阅读规范文件后使用此技能。该技能会自动参考对话内容——无需提供文件路径或进行问答。对于表单视图模型，先运行 `fosmvvm-fields-generator` 以生成 `Fields` 协议。

## 模式实现

该技能会根据对话内容来确定视图模型的结构：

### 托管模式检测

根据对话内容，技能会判断：
- **数据来源**（服务器/数据库或本地状态/偏好设置）
- 如果数据来自服务器，则使用手动编写的工厂和服务器端的本地化处理
- 如果数据来自客户端，则使用宏自动生成的工厂和客户端的本地化处理

### 视图模型设计

根据已有的需求：
- **视图的目的**（页面、模态窗口、卡片、列表组件）
- **数据需求**（来自数据库查询、应用程序状态、捕获的错误）
- **静态 UI 文本**（需要使用 `@LocalizedString` 的标题、标签、按钮）
- **子视图模型**（嵌套组件）
- **层次结构**（顶层视图模型还是子视图模型）

### 属性规划

根据视图需求：
- **需要显示的属性**
- **需要本地化的属性**
- **标识策略**（使用单例 `vmId` 还是实例化的 `vmId`）
- **是否采用 `Fields` 协议**

### 文件生成

**服务器托管的顶层视图模型：**
1. 视图模型结构体（包含 `RequestableViewModel`）
2. 请求类型（Request type）
3. YAML 格式的本地化字符串
4. 工厂实现代码

**客户端托管的顶层视图模型：**
1. 视图模型结构体（包含 `clientHostedFactory` 选项）
2. YAML 格式的本地化字符串

**子视图模型（两种模式均适用）：**
1. 视图模型结构体
2. （如需要）YAML 格式的本地化字符串

### 数据来源

该技能参考以下信息：
- **之前的对话**：与用户讨论过的视图需求和数据来源
- **规范文件**：Claude 是否已经将 UI 规范或功能文档纳入了讨论范围
- **Fields 协议**：来自代码库或之前的 `fosmvvm-fields-generator` 调用结果

## 关键模式

### `@ViewModel` 宏

始终使用 `@ViewModel` 宏——它用于生成本地化绑定所需的 `propertyNames()` 方法。

**服务器托管模式** 的基本宏实现：

**客户端托管模式**（包含工厂生成逻辑）：

---

### 可测试性（Stubbable Pattern）

所有视图模型都必须支持 `stub()` 方法，以便进行测试和 SwiftUI 预览：

---

### 身份标识：`vmId`

每个视图模型都需要一个 `vmId`，以便在 SwiftUI 中进行唯一标识：

- **单例模式**（每个页面一个 `vmId`）：`vmId = .init(type: Self.self)`
- **实例模式**（每个页面多个实例）：`vmId = .init(id: id)`，其中 `id` 是 `ModelIdType` 类型

### 本地化

静态 UI 文本使用 `@LocalizedString` 进行本地化：

---

**日期和数字的格式化**

切勿发送预格式化的字符串。应使用 `LocalizableString` 类型：

---

**枚举本地化模式**

对于动态枚举值（如状态、类别），应使用 **存储在本地化资源中的 `LocalizableString`**，而不是 `@LocalizedString`。

`@LocalizedString` 总是引用相同的键（属性名称）。而 `LocalizableString` 则存储了枚举值对应的动态键。

---

**限制：** `LocalizableString` 仅适用于使用 `localizingEncoder()` 进行编码的视图模型（ViewModels）。不要在 Fluent JSONB 字段或其他持久化类型中使用它。

### 子视图模型

顶层视图模型会包含其子视图模型：

---

**嵌套子类型模式**

当一个子类型**仅被一个父视图模型使用**，并且仅用于显示汇总信息或作为引用（而不是完整的视图模型）时，应将其嵌套在父视图模型中：

---

**参考示例：** `Sources/KairosModels/Governance/GovernancePrincipleCardViewModel.swift`

**放置规则：**
1. 嵌套类型应放在引用它们的属性之后
2. 放在 `vmId` 和父视图模型的 `init` 方法之前
3. 使用 `// MARK: - Nested Types` 标记
4. 每个嵌套类型都需要有自己的文档注释

**嵌套类型的兼容性要求：**
- 必须实现 `Codable` 协议，以便进行视图模型编码
- 必须实现 `Sendable` 协议，以支持 Swift 6 的并发处理
- 必须实现 `Identifiable` 协议，以便在数组中使用 `ForEach` 方法
- 必须实现 `Stubbable` 协议，以便进行测试和预览

**两层嵌套模式：**

嵌套类型在其扩展名中需要使用完整的路径：

---

**为什么需要两层嵌套：**
- 测试通常只需要 `.[.stub()]` 而不需要具体的值
- 其他测试可能需要具体的值：`.stub(name: "Specific Name")`
- 无参数调用时始终使用带参数的版本（确保一致性）

**何时使用嵌套模式，何时保持顶层结构：**

| 是否仅由一个父视图模型使用 | 是否需要跨多个父视图模型共享 |
|-------------------|----------------|
| 子类型仅用于当前父视图模型 | 子类型被多个父视图模型共享 |
| 子类型仅用于显示汇总信息 | 子类型是一个完整的视图模型 |
| 子类型不包含 `@ViewModel` 宏 | 子类型包含 `@ViewModel` 宏 |
| 子类型不是请求视图模型 | 子类型是请求视图模型 |
| 示例：`VersionSummary`, `Reference` | 示例：`CardViewModel`, `ListViewModel` |

**示例：**

- 带有嵌套摘要的卡片：`
- 带有嵌套引用的列表：`

---

**Codable 和计算属性**

Swift 的 `Codable` 协议仅会编码 **存储在本地化资源中的属性**。由于视图模型会被序列化（用于 JSON 传输、渲染等），因此计算属性不会被包含在内。

---

**何时进行预计算：**

对于简单的模板，可以直接使用模板内置的功能：
- `#if(count(cards) > 0)` —— 不需要 `hasCards` 属性
- `#count(cards)` —— 不需要 `cardCount` 属性

只有在以下情况下才需要进行预计算：
- 需要直接访问数组下标（例如 `firstCard`）
- 复杂逻辑在 Swift 中比在模板中更简洁
- 性能敏感的计算操作

有关 Leaf 模板的更多信息，请参阅 [fosmvvm-leaf-view-generator](../fosmvvm-leaf-view-generator/SKILL.md)。

## 文件模板

完整的文件模板请参阅 [reference.md]。

## 命名规范

| 概念 | 命名规则 | 示例 |
|---------|------------|---------|
| 视图模型结构体 | `{Name}ViewModel` | `DashboardViewModel` |
| 请求类 | `{Name}Request` | `DashboardRequest` |
| 工厂扩展 | `{Name}ViewModel+Factory.swift` | `DashboardViewModel+Factory.swift` |
| YAML 文件 | `{Name}ViewModel.yml` | `DashboardViewModel.yml` |

## 参考资料

- [架构模式](../shared/architecture-patterns.md) —— 关于数据模型（如错误处理、类型安全性等）
- [FOSMVVMArchitecture.md](../../docs/FOSMVVMArchitecture.md) —— 完整的 FOSMVVM 架构
- [fosmvvm-fields-generator](../fosmvvm-fields-generator/SKILL.md) —— 用于表单验证
- [fosmvvm-fluent-datamodel-generator](../fosmvvm-fluent-datamodel-generator/SKILL.md) —— 用于数据模型的持久化处理
- [fosmvvm-leaf-view-generator](../fosmvvm-leaf-view-generator/SKILL.md) —— 用于生成 Leaf 模板
- [reference.md] —— 完整的文件模板列表

## 版本历史

| 版本号 | 发布日期 | 更新内容 |
|---------|------|---------|
| 1.0 | 2024-12-24 | 初始版本 |
| 2.0 | 2024-12-26 | 根据 FOSMVVM 架构进行全面重写 |
| 2.1 | 2024-12-26 | 添加客户端托管模式支持；针对每个视图模型进行托管模式选择 |
| 2.2 | 2024-12-26 | 添加数据整理功能、`@LocalizedSubs`/`@LocalizedCompoundString` 的使用规则以及避免的错误模式 |
| 2.3 | 2025-12-27 | 添加关于显示视图模型和表单视图模型的内容；明确 `Fields` 协议的采用规则 |
| 2.4 | 2026-01-08 | 添加关于 `Codable` 和计算属性的内容；明确预计算的条件 |
| 2.5 | 2026-01-19 | 添加关于枚举本地化的内容；明确 `@LocalizedString` 的使用范围 |
| 2.6 | 2026-01-24 | 采用基于上下文的处理方式；不再依赖文件解析和问答；直接参考对话内容 |
| 2.7 | 2026-01-25 | 添加关于嵌套子类型的规则，包括两层嵌套模式、放置规则、兼容性要求以及判断是否使用嵌套模式的依据 |