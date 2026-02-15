---
name: fosmvvm-leaf-view-generator
description: 为 FOSMVVM WebApps 生成 Leaf 模板。创建全页视图以及能够渲染 ViewModels 的 HTML 动态片段（HTML-over-the-wire）。
homepage: https://github.com/foscomputerservices/FOSUtilities
metadata: {"clawdbot": {"emoji": "🍃", "os": ["darwin", "linux"]}}
---
# FOSMVVM Leaf视图生成器

该工具用于生成用于Web客户端的视图模板（Leaf templates），这些模板用于渲染视图模型（ViewModels）。

> **架构背景：** 请参阅 [FOSMVVMArchitecture.md](../../docs/FOSMVVMArchitecture.md) | [OpenClaw参考文档]({baseDir}/references/FOSMVVMArchitecture.md)

---

## Web应用程序的视图层（View Layer for WebApps）

在FOSMVVM中，Leaf模板是专为Web客户端设计的**视图层**：

```
Model → ViewModel → Leaf Template → HTML
              ↑           ↑
        (localized)  (renders it)
```

**核心原则：** 视图模型（ViewModel）在传递给模板时已经完成了本地化处理；模板仅负责渲染接收到的数据。

---

## 核心原则：视图模型与视图的匹配（View-ViewModel Alignment）

**Leaf模板的文件名必须与其渲染的视图模型相匹配。**

```
Sources/
  {ViewModelsTarget}/
    ViewModels/
      {Feature}ViewModel.swift        ←──┐
      {Entity}CardViewModel.swift     ←──┼── Same names
                                          │
  {WebAppTarget}/                         │
    Resources/Views/                      │
      {Feature}/                          │
        {Feature}View.leaf            ────┤  (renders {Feature}ViewModel)
        {Entity}CardView.leaf         ────┘  (renders {Entity}CardViewModel)
```

这种匹配机制带来了以下优势：
- **易用性**：可以快速找到对应任何视图模型的模板。
- **一致性**：遵循与SwiftUI相同的项目命名规范。
- **可维护性**：视图模型的任何更改都会体现在模板文件的路径上。

---

## 两种模板类型（Two Template Types）

### 全页面模板（Full-Page Templates）

渲染包含布局、导航以及CSS/JS的完整页面。

**用途：** 用于初始页面加载或导航跳转。

### 片段模板（Fragment Templates）

仅渲染单个组件，不包含布局或页面结构。

**用途：** 用于部分页面更新或通过HTTP直接发送HTML数据的场景。

---

## 通过HTTP直接发送HTML数据（HTML-Over-The-Wire Pattern）

这是一种无需重新加载整个页面即可实现动态更新的机制：

```
JS Event → WebApp Route → ServerRequest.processRequest() → Controller
                                                              ↓
                                                          ViewModel
                                                              ↓
HTML ← JS DOM swap ← WebApp returns ← Leaf renders ←────────┘
```

**Web应用程序的路由处理：**
```swift
app.post("move-{entity}") { req async throws -> Response in
    let body = try req.content.decode(Move{Entity}Request.RequestBody.self)
    let serverRequest = Move{Entity}Request(requestBody: body)
    guard let response = try await serverRequest.processRequest(baseURL: app.serverBaseURL) else {
        throw Abort(.internalServerError)
    }

    // Render fragment template with ViewModel
    return try await req.view.render(
        "{Feature}/{Entity}CardView",
        ["card": response.viewModel]
    ).encodeResponse(for: req)
}
```

**JavaScript接收HTML数据后将其插入到DOM中**——无需进行JSON解析或客户端端的渲染操作。

---

## 适用场景（When to Use This Skill）

- 创建新的全页面模板。
- 创建新的卡片、行或组件模板。
- 为JavaScript事件处理添加数据属性。
- 解决本地化类型显示不正确的问题。
- 设置用于通过HTTP发送HTML数据的模板。

---

## 主要使用模式（Key Patterns）

### 模式1：用于存储状态的数据属性（Data Attributes for State）

片段（fragments）必须包含JavaScript后续操作所需的所有状态信息：

```html
<div class="{entity}-card"
     data-{entity}-id="#(card.id)"
     data-status="#(card.status)"
     data-category="#(card.category)"
     draggable="true">
```

**规则：**
- 使用 `data-{entity}-id` 作为唯一标识符。
- 使用 `data-{field}` 保存状态值（采用kebab-case格式）。
- 保存**原始值**（例如枚举类型），而非本地化后的显示名称。
- JavaScript会读取这些值来构建服务器请求（ServerRequest）的数据。

```javascript
const request = {
    {entity}Id: element.dataset.{entity}Id,
    newStatus: targetColumn.dataset.status
};
```

### 模式2：Leaf模板中的本地化类型（Localizable Types in Leaf Templates）

FOSMVVM的 `LeafDataRepresentable` 类型支持自动处理本地化类型。

**在模板中只需使用相应的属性即可：**
```html
<span class="date">#(card.createdAt)</span>
<!-- Renders: "Dec 27, 2025" (localized) -->
```

**如果本地化类型显示不正确（例如显示 `[ds: "2", ls: "...", v: "..."]`）：**
1. 确保已导入 `FOSMVVMVapor` 库。
2. 检查 `Localizable+Leaf.swift` 文件是否存在并包含相应的实现。
3. 清理构建环境：执行 `swift package clean && swift build`。

### 模式3：显示值与标识符（Display Values vs Identifiers）

视图模型应同时提供原始值（用于数据属性）和本地化后的字符串（用于显示）。关于枚举类型的本地化处理，请参阅 [枚举类型本地化模式](../fosmvvm-viewmodel-generator/SKILL.md#enum-localization-pattern)。

```swift
@ViewModel
public struct {Entity}CardViewModel {
    public let id: ModelIdType              // For data-{entity}-id
    public let status: {Entity}Status       // Raw enum for data-status
    public let statusDisplay: LocalizableString  // Localized (stored, not @LocalizedString)
}
```

```html
<div data-status="#(card.status)">           <!-- Raw: "queued" for JS -->
    <span class="badge">#(card.statusDisplay)</span>  <!-- Localized: "In Queue" -->
</div>
```

### 模式4：片段结构（Fragment Structure）

片段应保持简洁，仅包含所需的组件内容：

**规则：**
- **禁止使用 `#extend("base")`——片段不使用布局结构**。
- **必须有一个根元素**——以便于DOM的替换操作。
- 所有必要的状态信息都应通过 `data-*` 属性传递。
- 显示值应来自视图模型的属性。

### 模式5：全页面结构（Full-Page Structure）

全页面模板基于基础布局进行扩展：

```html
<!-- {Feature}View.leaf -->
#extend("base"):
#export("content"):

<div class="{feature}-container">
    <header class="{feature}-header">
        <h1>#(viewModel.title)</h1>
    </header>

    <main class="{feature}-content">
        #for(card in viewModel.cards):
        #extend("{Feature}/{Entity}CardView")
        #endfor
    </main>
</div>

#endexport
#endextend
```

### 模式6：条件渲染（Conditional Rendering）

```html
#if(card.isHighPriority):
<span class="priority-badge">#(card.priorityLabel)</span>
#endif

#if(card.assignee):
<div class="assignee">
    <span class="name">#(card.assignee.name)</span>
</div>
#else:
<div class="unassigned">#(card.unassignedLabel)</div>
#endif
```

### 模式7：嵌套使用片段（Looping with Embedded Fragments）

```html
<div class="column" data-status="#(column.status)">
    <div class="column-header">
        <h3>#(column.displayName)</h3>
        <span class="count">#(column.count)</span>
    </div>

    <div class="column-cards">
        #for(card in column.cards):
        #extend("{Feature}/{Entity}CardView")
        #endfor

        #if(column.cards.count == 0):
        <div class="empty-state">#(column.emptyMessage)</div>
        #endif
    </div>
</div>
```

---

## 文件组织结构（File Organization）

```
Sources/{WebAppTarget}/Resources/Views/
├── base.leaf                          # Base layout (all pages extend this)
├── {Feature}/
│   ├── {Feature}View.leaf             # Full page → {Feature}ViewModel
│   ├── {Entity}CardView.leaf          # Fragment → {Entity}CardViewModel
│   ├── {Entity}RowView.leaf           # Fragment → {Entity}RowViewModel
│   └── {Modal}View.leaf               # Fragment → {Modal}ViewModel
└── Shared/
    ├── HeaderView.leaf                # Shared components
    └── FooterView.leaf
```

---

## Leaf内置函数（Leaf Built-in Functions）

Leaf提供了许多处理数组的实用函数：

```html
<!-- Count items -->
#if(count(cards) > 0):
<p>You have #count(cards) cards</p>
#endif

<!-- Check if array contains value -->
#if(contains(statuses, "active")):
<span class="badge">Active</span>
#endif
```

### 循环变量（Loop Variables）

在 `#for` 循环中，Leaf提供了用于跟踪循环进度的变量：

```html
#for(item in items):
    #if(isFirst):<span class="first">#endif
    #(item.name)
    #if(!isLast):, #endif
#endfor
```

| 变量 | 描述 |
|----------|-------------|
| `isFirst` | 在第一次迭代时为 `true` |
| `isLast` | 在最后一次迭代时为 `true` |
| `index` | 当前迭代次数（从0开始计数） |

### 数组索引访问（Array Index Access）

Leaf文档中未明确支持直接使用数组下标（如 `array[0]`）的方式。如需访问特定元素，应在视图模型中预先计算好索引。

```swift
public let firstCard: CardViewModel?

public init(cards: [CardViewModel]) {
    self.cards = cards
    self.firstCard = cards.first
}
```

---

## Codable与计算属性（Codable and Computed Properties）

Swift的 `Codable` 协议仅支持编码**已存储的属性**。由于视图模型是通过 `Codable` 编码传递给Leaf的，因此计算属性在Leaf中无法被直接使用。

**如果需要在Leaf模板中使用计算后的值，请在 `init()` 方法中计算并存储该值：**

```swift
public let hasCards: Bool
public let cardCount: Int

public init(cards: [CardViewModel]) {
    self.cards = cards
    self.hasCards = !cards.isEmpty
    self.cardCount = cards.count
}
```

---

## ViewModelId的初始化（ViewModelId Initialization）——非常重要

**重要提示：** 虽然Leaf模板不直接使用 `vmId`，但被渲染的视图模型必须正确初始化 `vmId`，以确保与SwiftUI客户端兼容。

**❌ 错误做法：** **绝对不要这样做：**  
```swift
public var vmId: ViewModelId = .init()  // NO! Generic identity
```

**✅ 最低要求：** 使用基于类型的标识符：**  
```swift
public var vmId: ViewModelId = .init(type: Self.self)
```

**✅ 理想做法：** 在可能的情况下，使用基于数据的标识符：**  
```swift
public struct TaskCardViewModel {
    public let id: ModelIdType
    public var vmId: ViewModelId

    public init(id: ModelIdType, /* other params */) {
        self.id = id
        self.vmId = .init(id: id)  // Ties view identity to data identity
        // ...
    }
}
```

**为什么这对Leaf视图模型很重要：**  
- 视图模型会在Leaf（Web客户端）和SwiftUI（原生客户端）之间共享。  
- SwiftUI使用 `.id(vmId)` 来决定何时重新创建视图或更新视图。  
- 如果`vmId`设置错误，SwiftUI视图可能无法正确更新。  
- 基于数据的标识符（`.init(id:)` 是最佳实践。

---

## 常见错误（Common Mistakes）

### 缺少数据属性（Missing Data Attributes）

```html
<!-- BAD - JS can't identify this element -->
<div class="{entity}-card">

<!-- GOOD - JS reads data-{entity}-id -->
<div class="{entity}-card" data-{entity}-id="#(card.id)">
```

### 保存显示名称而非标识符（Saving Display Names Instead of Identifiers）

```html
<!-- BAD - localized string can't be sent to server -->
<div data-status="#(card.statusDisplayName)">

<!-- GOOD - raw enum value works for requests -->
<div data-status="#(card.status)">
```

### 在片段中使用布局结构（Using Layout in Fragments）

```html
<!-- BAD - fragment should not extend layout -->
#extend("base"):
#export("content"):
<div class="card">...</div>
#endexport
#endextend

<!-- GOOD - fragment is just the component -->
<div class="card">...</div>
```

### 硬编码文本（Hardcoding Text）

```html
<!-- BAD - not localizable -->
<span class="status">Queued</span>

<!-- GOOD - ViewModel provides localized value -->
<span class="status">#(card.statusDisplayName)</span>
```

### 连接本地化字符串（Concatenating Localized Values）

**在模板中进行字符串连接时，应遵循从左到右的顺序。** 可在视图模型中使用 `@LocalizedSubs` 来指定正确的顺序（例如，让YAML文件指定语言环境）：**

```yaml
en:
  ConversationViewModel:
    messageCountDisplay: "%{messageCount} %{messagesLabel}"
ar:
  ConversationViewModel:
    messageCountDisplay: "%{messagesLabel} %{messageCount}"
```

### 模板中的日期格式化（Formatting Dates in Templates）

**在视图模型中使用 `LocalizableDate` 类型——它会根据用户的语言设置进行格式化。** 如果需要添加前缀，可以使用 `@LocalizedSubs`：**

```swift
public let createdAt: LocalizableDate

@LocalizedSubs(\.createdPrefix, \.createdAt)
public var createdDisplay
```

### 文件名不匹配（Mismatched Filenames）

```
<!-- BAD - filename doesn't match ViewModel -->
ViewModel: UserProfileCardViewModel
Template:  ProfileCard.leaf

<!-- GOOD - aligned names -->
ViewModel: UserProfileCardViewModel
Template:  UserProfileCardView.leaf
```

### 视图模型ID初始化错误（Incorrect ViewModelId Initialization）

**Leaf渲染的视图模型通常会与SwiftUI客户端共享。** 正确初始化 `vmId` 对于SwiftUI的视图管理机制至关重要。**

---

## Leaf模板中的渲染错误（Rendering Errors in Leaf Templates）

当Web应用程序的路由处理过程中发生错误时，错误类型在编译时就已经确定。因此，无需使用通用的 `ErrorViewModel` 模式：

**错误的做法（基于JavaScript的思维方式）：**  
```swift
// ❌ WRONG - treating errors as opaque
catch let error as ServerRequestError {
    // "How do I extract the message? The protocol doesn't guarantee it!"
    // This is wrong thinking. You catch the CONCRETE type.
}
```

每个路由都应该处理自己特定的错误类型。这样就能明确哪些属性是可用的。

---

## 如何使用该工具（How to Use This Skill）

**调用方式：**  
`/fosmvvm-leaf-view-generator`

**前提条件：**  
- 了解视图模型的结构。  
- 确定所需的模板类型（全页面模板或片段模板）。  
- 明确JavaScript交互所需的数据属性。  
- 如果使用片段模板，需理解通过HTTP发送HTML数据的机制。

**工作流程整合：**  
该工具用于为Web客户端生成视图模板。它会自动参考之前的讨论内容，无需提供文件路径或额外问题。通常会与 `fosmvvm-viewmodel-generator` 工具配合使用。

## 模式实现方式（Pattern Implementation）

该工具会根据之前的讨论内容来确定模板的具体结构：

### 视图模型分析（ViewModel Analysis）

根据讨论内容，工具会识别以下信息：  
- **视图模型类型**（来自之前的讨论或服务器实现）。  
- **需要显示的属性**（模板将显示哪些数据）。  
- **哪些属性是可本地化的**。  
- **是否存在嵌套的视图模型**（是否有子组件）。

### 模板类型判断（Template Type Detection）

根据视图模型的用途，可以判断模板类型：  
- **页面内容** → 使用全页面模板（包含布局）。  
- **列表项/卡片** → 使用片段模板（无布局，只有一个根元素）。  
- **模态框内容** → 使用片段模板。  
- **内联组件** → 也使用片段模板。

### 属性映射（Property Mapping）

对于每个视图模型属性：  
- `id: ModelIdType` → `data-{entity}-id="#(vm.id)"`（用于JavaScript访问）。  
- **原始枚举值** → `data-{field}="#(vm.field)"`（用于存储状态）。  
- **可本地化的字符串** → `#(vm.displayName)`（用于显示文本）。  
- **可本地化的日期类型** → `#(vm.createdAt)`（格式化后的日期）。  
- **嵌套的视图模型** → 通过片段嵌入或直接访问其属性。

### 数据属性规划（Data Attributes Planning）

根据JavaScript交互的需求，需要规划以下数据属性：  
- **实体标识符**（用于后续操作）。  
- **状态值**（例如枚举类型的原始值）。  
- **拖放操作相关的属性**（如果存在交互功能）。  
- **用于过滤/排序的类别/分组信息**。

### 模板生成流程（Template Generation）

- **全页面模板：**  
  - 扩展基础布局。  
  - 导出页面内容。  
  - 插入所需的组件片段。  

- **片段模板：**  
  - 使用单一的根元素。  
  - 通过数据属性传递状态信息。  
  - 从视图模型中获取本地化后的文本。  
  - 不需要扩展布局结构。

### 信息来源（Context Sources）

该工具的信息来源包括：  
- **之前的讨论内容**：模板的具体需求和用户交互流程。  
- **视图模型代码**：如果Claude已经将视图模型代码解析到上下文中。  
- **现有的模板**：通过对类似模板的代码分析得出的经验。

---

## 参考资料（See Also）

- [架构模式](../shared/architecture-patterns.md)——关于错误处理、类型安全等方面的设计模式。  
- [FOSMVVMArchitecture.md](../../docs/FOSMVVMArchitecture.md)——完整的系统架构文档。  
- [fosmvvm-viewmodel-generator](../fosmvvm-viewmodel-generator/SKILL.md)——用于生成视图模型的工具。  
- [fosmvvm-serverrequest-generator](../fosmvvm-serverrequest-generator/SKILL.md)——用于生成返回视图模型的请求数据。  
- [reference.md]——包含完整的模板示例。

---

## 版本历史（Version History）

| 版本 | 更新日期 | 主要变更内容 |
|---------|------|---------|
| 1.0 | 2025-12-24 | 首次为Kairos项目定制的版本。 |
| 2.0 | 2025-12-27 | 适配FOSMVVM通用需求，新增视图模型与视图的匹配原则、全页面模板功能以及与架构的关联。 |
| 2.1 | 2026-01-08 | 添加了关于Leaf内置函数的部分（如计数、数组遍历变量等），明确了关于`Codable`和计算属性的使用规则，并纠正了之前的错误说明。 |
| 2.2 | 2026-01-19 | 更新了模式3，改为使用本地化后的字符串来显示枚举类型；增加了关于在模板中连接本地化字符串和格式化日期的错误处理方式。 |
| 2.3 | 2026-01-20 | 新增了“Leaf模板中的渲染错误”章节，说明错误类型在编译时就已经确定，无需使用通用的`ErrorViewModel`模式。 |
| 2.4 | 2026-01-24 | 采用基于上下文的信息处理方式，不再依赖文件路径或用户输入，而是直接参考之前的讨论内容。