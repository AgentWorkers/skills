---
name: fosmvvm-serverrequest-generator
description: 生成用于 CRUD 操作和客户端-服务器通信的 FOSMVVM ServerRequest 类型。这些类型包括请求体、响应体以及类型化的错误处理机制。
homepage: https://github.com/foscomputerservices/FOSUtilities
metadata: {"clawdbot": {"emoji": "🔌", "os": ["darwin", "linux"]}}
---

# FOSMVVM 服务器请求生成器

该工具用于生成用于客户端与服务器之间通信的 `ServerRequest` 类型。

> **架构背景：** 请参阅 [FOSMVVMArchitecture.md](../../docs/FOSMVVMArchitecture.md) | [OpenClaw 参考文档]({{baseDir}}/references/FOSMVVMArchitecture.md)

---

## 重要提示

**`ServerRequest` 是与 FOSMVVM 服务器进行通信的唯一方式。** 无例外。

```
┌──────────────────────────────────────────────────────────────────────┐
│                 ALL CLIENTS USE ServerRequest                         │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  iOS App:         Button tap    →  request.processRequest(mvvmEnv:)   │
│  macOS App:       Button tap    →  request.processRequest(mvvmEnv:)   │
│  WebApp:          JS → WebApp   →  request.processRequest(mvvmEnv:)   │
│  CLI Tool:        main()        →  request.processRequest(mvvmEnv:)   │
│  Data Collector:  timer/event   →  request.processRequest(mvvmEnv:)   │
│  Background Job:  cron trigger  →  request.processRequest(mvvmEnv:)   │
│                                                                       │
│  MVVMEnvironment holds: baseURL, headers, version, error handling     │
│  Configure ONCE at startup, use EVERYWHERE via processRequest()       │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘
```

### 绝对不能做的事情

```swift
// ❌ WRONG - hardcoded URL
let url = URL(string: "http://server/api/users/123")!
var request = URLRequest(url: url)

// ❌ WRONG - string path
try await client.get("/api/users/\(id)")

// ❌ WRONG - manual JSON encoding
let json = try JSONEncoder().encode(body)
request.httpBody = json
```

```javascript
// ❌ WRONG - hardcoded fetch path
fetch('/api/users/123')

// ❌ WRONG - constructing URLs manually
fetch(`/api/ideas/${ideaId}/move`)
```

### 必须始终做的事情

**步骤 1：在启动时配置一次 `MVVMEnvironment`**

```swift
// CLI tool, background job, data collector - configure at startup
// Import your shared module to get SystemVersion.currentApplicationVersion
import ViewModels  // ← Your shared module (see FOSMVVMArchitecture.md)

let mvvmEnv = await MVVMEnvironment(
    currentVersion: .currentApplicationVersion,  // From shared module
    appBundle: Bundle.module,
    deploymentURLs: [.debug: URL(string: "http://localhost:8080")!]
)
// NOTE: Version headers (X-FOS-Version) are AUTOMATIC via SystemVersion.current
```

共享模块中包含 `SystemVersion+App.swift`：
```swift
// In your shared ViewModels module
public extension SystemVersion {
    static var currentApplicationVersion: Self { .v1_0 }
    static var v1_0: Self { .init(major: 1, minor: 0, patch: 0) }
}
```

**步骤 2：在任何地方使用 `processRequest(mvvmEnv:)`**

```swift
// ✅ RIGHT - ServerRequest with MVVMEnvironment
let request = UserShowRequest(query: .init(userId: id))
try await request.processRequest(mvvmEnv: mvvmEnv)
let user = request.responseBody

// ✅ RIGHT - Create operation
let createRequest = CreateIdeaRequest(requestBody: .init(content: content))
try await createRequest.processRequest(mvvmEnv: mvvmEnv)
let newId = createRequest.responseBody?.id

// ✅ RIGHT - Update operation
let updateRequest = MoveIdeaRequest(requestBody: .init(ideaId: id, newStatus: status))
try await updateRequest.processRequest(mvvmEnv: mvvmEnv)
```

**路径由类型名称生成；HTTP 方法来自协议。** **切勿手动编写 URL 字符串。** 配置信息存储在 `MVVMEnvironment` 中，**切勿将 `baseURL` 或 `headers` 传递给单个请求。**

---

## 适用场景

- 实现任何客户端与服务器之间的通信
- 添加 CRUD 操作（创建、读取、更新、删除）
- 构建数据收集器或同步工具
- 任何需要与服务器交互的 Swift 代码

**如果你打算手动编写 `URLRequest` 或硬编码路径字符串，请立即停止，并使用此工具。**

---

## `ServerRequest` 的功能

| 功能 | 处理方式 |
|---------|------------------------------|
| URL 路径 | 通过 `Self.path` 从类型名称生成（例如，`MoveIdeaRequest` → `/move_idea`） |
| HTTP 方法 | 由 `action.httpMethod` 确定（`ShowRequest` = GET，`CreateRequest` = POST 等） |
| 请求体 | 使用 `RequestBody` 类型，通过 `requestBody?.toJSONData()` 自动编码为 JSON |
| 响应体 | 使用 `ResponseBody` 类型，自动解码为 JSON |
| 错误响应 | 使用 `ResponseError` 类型，当响应无法解码为 `ResponseBody` 时自动处理 |
| 验证 | 写入操作时使用 `RequestBody: ValidatableModel` |
| 请求体大小限制 | 对于大文件上传（如图片），使用 `RequestBody.maxBodySize` |
| 类型安全性 | 编译器确保类型正确性 |

---

## 请求协议选择

根据操作类型选择相应的协议：

| 操作 | 协议 | HTTP 方法 | 是否需要请求体？ |
|-----------|----------|-------------|----------------------|
| 读取数据 | `ShowRequest` | GET | 不需要 |
| 读取视图模型 | `ViewModelRequest` | GET | 不需要 |
| 创建实体 | `CreateRequest` | POST | 需要（`ValidatableModel`） |
| 更新实体 | `UpdateRequest` | PATCH | 需要（`ValidatableModel`） |
| 替换实体 | 使用 `.replace` 操作 | PUT | 需要 |
| 软删除 | `DeleteRequest` | DELETE | 不需要 |
| 硬删除 | `DestroyRequest` | DELETE | 不需要 |

---

## 该工具生成的文件

### 核心文件（必生成）

| 文件 | 位置 | 用途 |
|------|----------|---------|
| `{Action}Request.swift` | `{ViewModelsTarget}/Requests/` | 服务器请求类型 |
| `{Action}Controller.swift` | `{WebServerTarget}/Controllers/` | 服务器端处理程序 |

### 可选：WebApp 桥接（适用于 Web 客户端）

| 文件 | 用途 |
|------|---------|
| WebApp 路由 | 将 JavaScript 的请求转换为 `ServerRequest.fetch()` |
| JavaScript 处理指南 | 指导如何在浏览器中调用该请求 |

---

## 使用方法

**调用方式：**
/fosmvvm-serverrequest-generator

**前提条件：**
- 了解操作需求
- 已讨论或记录了 `RequestBody` 和 `ResponseBody` 的结构
- 确定了客户端类型（iOS 应用、WebApp、CLI 工具、后台任务等）

**工作流程集成：**
此工具通常用于实现客户端与服务器之间的通信。它会自动参考对话上下文，无需提供文件路径或额外的问题。

## 模式实现

该工具根据对话上下文来确定 `ServerRequest` 的结构：

### 操作类型检测

从对话上下文中，工具可以识别：
- **CRUD 操作**（创建、读取、更新、删除）
- **HTTP 方法**（读取使用 GET，创建使用 POST，更新使用 PATCH/PUT，删除使用 DELETE）
- **协议选择**（`ShowRequest`、`ViewModelRequest`、`CreateRequest`、`UpdateRequest`、`DeleteRequest`）

### 请求结构设计

根据上下文中的需求：
- **请求体字段**（客户端发送的数据）
- **查询参数**（URL 查询字符串）
- **片段参数**（URL 的片段/锚点）
- **验证要求**（写入操作时需要 `ValidatableModel`）

### 响应结构设计

根据上下文中的需求：
- **响应体类型**（通常是视图模型，有时只是一个 ID）
- **错误响应类型**（自定义错误结构或 `EmptyError`）
- **成功情况**（表示操作成功的条件）
- **错误情况**（需要结构化错误信息的失败情况）

### 客户端识别

从对话上下文中确定：
- **目标平台**（iOS/macOS 应用、WebApp 浏览器、CLI 工具、后台任务）
- **是否需要 WebApp 路由**（针对 WebApp 客户端）
- **`MVVMEnvironment` 的配置**（客户端如何设置 `baseURL` 和 `headers`）

### 文件生成

**核心文件：**
1. 包含 `RequestBody`、`ResponseBody` 和 `ResponseError` 的 `ServerRequest` 类型
2. 包含操作处理程序的控制器
3. 路由注册

**可选（针对 WebApp 客户端）：**
4. 将 JavaScript 请求转换为 `ServerRequest` 的路由
5. JavaScript 处理指南

### 上下文来源

该工具参考以下信息：
- **之前的对话**：操作需求和数据结构
- **规范文件**：如果 Claude 已将 API 规范或功能文档纳入上下文
- **现有代码库中的类似请求模式**

---

### `ServerRequest` 类型模板

```swift
// {Action}Request.swift
import FOSMVVM

public final class {Action}Request: {Protocol}, @unchecked Sendable {
    public typealias Query = EmptyQuery       // or custom Query type
    public typealias Fragment = EmptyFragment
    // ResponseError: use EmptyError OR define nested ResponseError struct (see below)

    public let requestBody: RequestBody?
    public var responseBody: ResponseBody?

    // What the client sends
    public struct RequestBody: ServerRequestBody, ValidatableModel {
        // Fields...
    }

    // What the server returns
    public struct ResponseBody: {Protocol}ResponseBody {
        // Fields (often contains a ViewModel)
    }

    // Optional: Custom error type (nested, not top-level!)
    // public struct ResponseError: ServerRequestError { ... }

    public init(
        query: Query? = nil,
        fragment: Fragment? = nil,
        requestBody: RequestBody? = nil,
        responseBody: ResponseBody? = nil
    ) {
        self.requestBody = requestBody
        self.responseBody = responseBody
    }
}
```

**注意：** 所有子类型（`RequestBody`、`ResponseBody`、`ResponseError`）都嵌套在 `ServerRequest` 类中。这样可以避免命名空间污染，并自动生成唯一的 YAML 局部化键。

### 控制器模板

**控制器动作 = 协议名称（去掉 “Request”）**

| 协议 | 动作 | HTTP 方法 |
|----------|--------|-------------|
| `ShowRequest` | `.show` | GET |
| `ViewModelRequest` | `.show` | GET |
| `CreateRequest` | `.create` | POST |
| `UpdateRequest` | `.update` | PATCH |
| `DeleteRequest` | `.delete` | DELETE |
| 自定义请求 | 根据实际需求命名 | 视具体操作而定 |

### 控制器注册

```swift
// In WebServer routes.swift
try versionedGroup.register(collection: {Action}Controller())
```

### 客户端调用方式

**所有 Swift 客户端（iOS、macOS、CLI、后台任务等）：**

```swift
// MVVMEnvironment configured once at app/tool startup (see "What You Must ALWAYS Do")
let request = {Action}Request(requestBody: .init(...))
try await request.processRequest(mvvmEnv: mvvmEnv)
let result = request.responseBody
```

**WebApp（浏览器客户端）：**
请参阅下面的 [WebApp 桥接模式](#webapp-bridge-pattern)。

---

## WebApp 桥接模式

当客户端是 Web 浏览器时，需要在 JavaScript 和 `ServerRequest` 之间建立桥梁：

```
Browser                    WebApp (Swift)                      WebServer
   │                            │                                  │
   │  POST /action-name         │                                  │
   │  (JSON body)               │                                  │
   │ ─────────────────────────► │                                  │
   │                            │  request.processRequest(mvvmEnv:)│
   │                            │ ────────────────────────────────►│
   │                            │ ◄────────────────────────────────│
   │  ◄──────────────────────── │  (ResponseBody)                  │
   │  (HTML fragment or JSON)   │                                  │
```

**WebApp 路由是内部实现的**——浏览器通过该路由调用 `ServerRequest`，就像在 iOS 中点击按钮一样。

### WebApp 路由

```swift
// WebApp routes.swift
app.post("{action-name}") { req async throws -> Response in
    // 1. Decode what JS sent
    let body = try req.content.decode({Action}Request.RequestBody.self)

    // 2. Call server via ServerRequest (NOT hardcoded URL!)
    // mvvmEnv is configured at WebApp startup
    let serverRequest = {Action}Request(requestBody: body)
    try await serverRequest.processRequest(mvvmEnv: req.application.mvvmEnv)

    // 3. Return response (HTML fragment or JSON)
    guard let response = serverRequest.responseBody else {
        throw Abort(.internalServerError, reason: "No response from server")
    }
    // ...
}
```

### JavaScript 处理程序

```javascript
async function handle{Action}(data) {
    const response = await fetch('/{action-name}', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    // Handle response...
}
```

**注意：** JavaScript 通过 WebApp 发送请求（同源），然后 `ServerRequest` 与 WebServer 进行通信。** 浏览器永远不会直接与 WebServer 通信。**

---

## 常见模式

### 视图模型响应

大多数操作会返回一个视图模型以更新 UI：

```swift
public struct ResponseBody: UpdateResponseBody {
    public let viewModel: IdeaCardViewModel
}
```

### 仅返回 ID 的响应

某些操作只需要确认操作是否成功：

```swift
public struct ResponseBody: CreateResponseBody {
    public let id: ModelIdType
}
```

### 空响应

删除操作通常不返回任何内容：

```swift
// Use EmptyBody as ResponseBody
public typealias ResponseBody = EmptyBody
```

---

## `ResponseError` - 结构化错误处理

每个 `ServerRequest` 都可以定义一个自定义的 `ResponseError` 类型，用于处理来自服务器的结构化错误响应。

### 工作原理

处理响应时：
1. 框架会尝试将其解码为 `ResponseBody`
2. 如果解码失败，会尝试将其解码为 `ResponseError`
3. 如果 `ResponseError` 解码成功，则抛出该错误
4. 客户端在调用处使用 `try/catch` 语句捕获错误

### 何时使用自定义 `ResponseError`

**在以下情况下使用自定义 `ResponseError`：**
- 操作有明确的失败模式（例如验证失败、超出配额等）
- 服务器返回结构化的错误信息（字段名称、错误代码）
- 客户端需要根据错误类型采取特定操作
- 需要显示字段级别的错误信息

**在以下情况下使用 `EmptyError`（默认值）：**
- 操作很少失败
- 失败情况较为罕见（例如网络中断、服务器崩溃）
- 不需要结构化的错误响应
- 只需要知道操作是否成功或失败，而不需要知道具体原因

### 嵌套模式

**`ResponseError` 必须嵌套在 `ServerRequest` 类中**，就像 `RequestBody` 和 `ResponseBody` 一样：

```swift
public final class CreateIdeaRequest: CreateRequest, @unchecked Sendable {
    public typealias Query = EmptyQuery
    public typealias Fragment = EmptyFragment
    // No typealias needed - ResponseError is nested

    public let requestBody: RequestBody?
    public var responseBody: ResponseBody?

    // ✅ All subtypes nested inside the request
    public struct RequestBody: ServerRequestBody, ValidatableModel { ... }
    public struct ResponseBody: CreateResponseBody { ... }
    public struct ResponseError: ServerRequestError { ... }  // ← Nested, not top-level

    public init(...) { ... }
}
```

**嵌套的重要性：**
- 与 `RequestBody`/`ResponseBody` 的模式保持一致
- 避免命名空间污染（避免在顶级使用 `CreateIdeaError`、`MoveIdeaError` 等名称）
- YAML 局部化键具有明确的层次结构（例如 `CreateIdeaRequest.ResponseError.ErrorCode.quotaExceeded`）
- 无需使用像 `GovernanceLessonCreateError` 这样的唯一类型名称——嵌套结构可以确保唯一性

### 模式 1：带有关联值的错误

对于需要动态错误信息的错误，使用 `LocalizableSubstitutions`：

```swift
public final class CreateIdeaRequest: CreateRequest, @unchecked Sendable {
    // ... other typealiases and properties ...

    public struct ResponseError: ServerRequestError {
        public let code: ErrorCode
        public let message: LocalizableSubstitutions

        public enum ErrorCode: Codable, Sendable {
            case duplicateContent
            case quotaExceeded(requestedSize: Int, maximumSize: Int)
            case invalidCategory(category: String)

            var message: LocalizableSubstitutions {
                switch self {
                case .duplicateContent:
                    .init(
                        baseString: .localized(for: Self.self, parentType: ResponseError.self, propertyName: "duplicateContent"),
                        substitutions: [:]
                    )
                case .quotaExceeded(let requestedSize, let maximumSize):
                    .init(
                        baseString: .localized(for: Self.self, parentType: ResponseError.self, propertyName: "quotaExceeded"),
                        substitutions: [
                            "requestedSize": LocalizableInt(value: requestedSize),
                            "maximumSize": LocalizableInt(value: maximumSize)
                        ]
                    )
                case .invalidCategory(let category):
                    .init(
                        baseString: .localized(for: Self.self, parentType: ResponseError.self, propertyName: "invalidCategory"),
                        substitutions: [
                            "category": LocalizableString.constant(category)
                        ]
                    )
                }
            }
        }

        public init(code: ErrorCode) {
            self.code = code
            self.message = code.message  // Required to localize properly via Codable
        }
    }
}
```

### 模式 2：简单错误（基于字符串的错误代码）

对于没有关联值的简单错误，使用基于字符串的错误代码：

```swift
public final class MoveIdeaRequest: UpdateRequest, @unchecked Sendable {
    // ... other typealiases and properties ...

    public struct ResponseError: ServerRequestError {
        public let code: ErrorCode
        public let message: LocalizableString

        public enum ErrorCode: String, Codable, Sendable {
            case ideaNotFound
            case invalidTransition

            var message: LocalizableString {
                .localized(for: Self.self, parentType: ResponseError.self, propertyName: rawValue)
            }
        }

        public init(code: ErrorCode) {
            self.code = code
            self.message = code.message  // Required to localize properly via Codable
        }
    }
}
```

### 类型安全性

**别担心“我怎么知道错误类型？”**

这并不是 JavaScript 的编写方式。Swift 的类型系统在编译时就已经明确了所有类型：

```swift
// When you write this request...
let request = MoveIdeaRequest(requestBody: body)

// ...you KNOW:
// - MoveIdeaRequest.ResponseError exists (it's declared in the type)
// - It has exactly the cases you defined (ideaNotFound, invalidTransition)
// - Each case has whatever properties you gave it

// So when you catch, you catch THE SPECIFIC TYPE:
do {
    try await request.processRequest(mvvmEnv: mvvmEnv)
} catch let error as MoveIdeaRequest.ResponseError {
    // I KNOW this is MoveIdeaRequest.ResponseError
    // I KNOW it has .code
    // I KNOW .code is ErrorCode enum with ideaNotFound, invalidTransition
    // No mystery. No runtime discovery. No "what if?"
}
```

**错误的错误思维方式（JavaScript 的做法）：**
```swift
// ❌ WRONG - treating typed errors as unknown
catch let error as ServerRequestError {
    // "How do I get the message? What properties does it have?"
    // This thinking is WRONG. You're not in a typeless world.
}
```

**正确的做法（Swift 的做法）：**
```swift
// ✅ RIGHT - you know the exact type
catch let error as MoveIdeaRequest.ResponseError {
    switch error.code {
    case .ideaNotFound: // I know this exists
    case .invalidTransition: // I know this exists
    }
}
```

`ServerRequestError` 协议是一个标记（`Error, Codable, Sendable`）。它不需要指定具体的属性，因为**你只需要捕获具体的错误类型，而不是协议本身**。

### 客户端错误处理

主要的错误处理方式是在调用处使用 `try/catch`：

```swift
do {
    try await request.processRequest(mvvmEnv: mvvmEnv)
} catch let error as CreateIdeaError {
    switch error.code {
    case .duplicateContent:
        showDuplicateWarning(message: error.message)
    case .quotaExceeded(let requestedSize, let maximumSize):
        showQuotaError(requested: requestedSize, maximum: maximumSize, message: error.message)
    case .invalidCategory(let category):
        highlightInvalidCategory(category, message: error.message)
    }
} catch {
    showGenericError(error)
}
```

### 内置的 `ValidationError`

FOSMVVM 提供了 `ValidationError` 用于处理字段级别的验证错误：

```swift
// In controller - use Validations to collect errors
let validations = Validations()

if requestBody.email.isEmpty {
    validations.validations.append(.init(
        status: .error,
        fieldId: "email",
        message: .localized(for: CreateUserRequest.self, propertyName: "emailRequired")
    ))
}

// Throw if any errors
if let error = validations.validationError {
    throw error
}
```

**更多详细信息：** 请参阅 [ServerRequestError - 结构化错误响应](../../docs/FOSMVVMArchitecture.md#serverrequesterror---typed-error-responses)。

---

## 测试 `ServerRequest`

**始终通过 `ServerRequest.processRequest(mvvmEnv:)` 进行测试**，**切勿使用手动 HTTP 请求。**

有关完整的测试指南，请参阅 [fosmvvm-serverrequest-test-generator](../fosmvvm-serverrequest-test-generator/SKILL.md)。

```swift
// ✅ RIGHT - tests the actual client code path
let request = Update{Entity}Request(
    query: .init(entityId: id),
    requestBody: .init(name: "New Name")
)
try await request.processRequest(mvvmEnv: testMvvmEnv)
#expect(request.responseBody?.viewModel.name == "New Name")

// ❌ WRONG - manual HTTP bypasses version negotiation
try await app.sendRequest(.PATCH, "/entity/\(id)", body: json)
```

---

## 参考资料

- [架构模式](../shared/architecture-patterns.md) - 关于错误处理、类型安全等方面的概念
- [FOSMVVMArchitecture.md](../../docs/FOSMVVMArchitecture.md) - 完整的架构说明，特别是“`ServerRequest` 是唯一的数据传输方式”这一核心原则
- [fosmvvm-serverrequest-test-generator](../fosmvvm-serverrequest-test-generator/SKILL.md) - 用于测试 `ServerRequest` 类型
- [fosmvvm-viewmodel-generator](../fosmvvm-viewmodel-generator/SKILL.md) - 用于生成视图模型
- [fosmvvm-fields-generator](../fosmvvm-fields-generator/SKILL.md) - 用于处理 `RequestBody` 中的 `ValidatableModel`
- [fosmvvm-leaf-view-generator](../fosmvvm-leaf-view-generator/SKILL.md) - 用于生成渲染视图模型的模板
- [reference.md] - 包含所有文件模板

---

## 版本历史

| 版本 | 更新日期 | 更改内容 |
|---------|------|---------|
| 1.0 | 2025-12-24 | 首次为 Kairos 项目定制的技能 |
| 2.0 | 2025-12-26 | 全面重构：采用自上而下的架构设计，“`ServerRequest` 是唯一的数据传输方式”这一原则得到明确体现；将 WebApp 桥接作为通用模式 |
| 2.1 | 2025-12-27 | `MVVMEnvironment` 成为所有客户端（CLI、iOS、macOS 等）的统一配置来源，不再使用原始的 `baseURL`/`headers`；遵循 DRY（Don’t Repeat Yourself）原则 |
| 2.2 | 2025-12-27 | 添加了共享模块模式；从共享模块中获取 `SystemVersion.currentApplicationVersion`；引用了 `FOSMVVMArchitecture.md` |
| 2.3 | 2025-12-27 | 添加了 `ServerRequestBodySize` 以限制大文件上传的大小（`RequestBody` 中的 `maxBodySize`） |
| 2.4 | 2026-01-08 | 添加了控制器动作映射表和测试指南 |
| 2.5 | 2026-01-08 | 简化了动作映射规则：“动作 = 协议名称去掉 ‘Request’” |
| 2.6 | 2026-01-09 | 添加了 `ResponseError` 部分，包括两种模式：带有关联值的错误（`LocalizableSubstitutions`）和简单的字符串错误代码（`LocalizableString`）；添加了 YAML 示例和 `ValidationError` 的使用方法 |
| 2.7 | 2026-01-20 | 强制要求 `ResponseError` 必须嵌套在 `ServerRequest` 类中 |
| 2.8 | 2026-01-20 | 添加了“类型安全性意味着你已经知道错误类型”这一解释性内容，说明 Swift 的类型系统可以让你在编译时就知道错误类型 |
| 2.9 | 2026-01-24 | 采用基于上下文的信息处理方式（不再解析文件路径或询问用户） |

---

## 注意事项

- 该技能会根据对话上下文自动确定 `ServerRequest` 的结构。