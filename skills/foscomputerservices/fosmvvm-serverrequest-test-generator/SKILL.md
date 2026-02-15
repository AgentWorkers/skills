---
name: fosmvvm-serverrequest-test-generator
description: 使用 VaporTesting 生成 ServerRequest 测试用例。这些测试用例涵盖了 Show（显示）、Create（创建）、Update（更新）和 Delete（删除）操作的请求/响应数据类型验证。
homepage: https://github.com/foscomputerservices/FOSUtilities
metadata: {"clawdbot": {"emoji": "🧪", "os": ["darwin", "linux"]}}
---
# FOSMVVM ServerRequest 测试生成器

使用 VaporTesting 基础设施为 ServerRequest 类型生成测试文件。

## 概念基础

> 有关完整的架构信息，请参阅 [FOSMVVMArchitecture.md](../../docs/FOSMVVMArchitecture.md) | [OpenClaw 参考]({{baseDir}/references/FOSMVVMArchitecture.md)

ServerRequest 的测试使用 **VaporTesting** 基础设施来发送类型化的请求，并通过整个服务器堆栈进行处理：

```
┌─────────────────────────────────────────────────────────────────────┐
│                    ServerRequest Test Flow                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Test Code:                                                          │
│    let request = MyRequest(query: .init(...))                        │
│    app.testing().test(request, locale: en) { response in }           │
│                                                                      │
│  Infrastructure handles:                                             │
│    • Path derivation from type name (MyRequest → /my)                │
│    • HTTP method from action (ShowRequest → GET)                     │
│    • Query/body encoding                                             │
│    • Header injection (locale, version)                              │
│    • Response decoding to ResponseBody type                          │
│                                                                      │
│  You verify:                                                         │
│    • response.status (HTTPStatus)                                    │
│    • response.body (R.ResponseBody? - typed!)                        │
│    • response.error (R.ResponseError? - typed!)                      │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 请阅读以下内容

**测试 ServerRequest 时使用 VaporTesting 基础设施。** **绝对不要** 手动构建 URL。**

```
┌──────────────────────────────────────────────────────────────────────┐
│          SERVERREQUEST TESTING USES TestingApplicationTester          │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  1. Configure Vapor Application with routes                           │
│  2. Use app.testing().test(request, locale:) { response in }          │
│  3. Verify response.status, response.body, response.error             │
│                                                                       │
│  TestingServerRequestResponse<R> provides TYPED access to:            │
│    • status: HTTPStatus                                               │
│    • headers: HTTPHeaders                                             │
│    • body: R.ResponseBody?     ← Auto-decoded!                        │
│    • error: R.ResponseError?   ← Auto-decoded!                        │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘
```

### 绝对不能做的事情

```swift
// ❌ WRONG - manual URL construction
let url = URL(string: "http://localhost:8080/my_request?query=value")!
let response = try await URLSession.shared.data(from: url)

// ❌ WRONG - string path with method
try await app.test(.GET, "/my_request") { response in }

// ❌ WRONG - manual JSON encoding/decoding
let json = try JSONEncoder().encode(requestBody)
let decoded = try JSONDecoder().decode(ResponseBody.self, from: data)

// ❌ WRONG - constructing TestingHTTPRequest manually
let httpRequest = TestingHTTPRequest(method: .GET, url: "/path", headers: headers)
try await app.testing().performTest(request: httpRequest)
```

### 必须始终做的事情

```swift
// ✅ RIGHT - Use TestingApplicationTester.test() with ServerRequest
let request = MyShowRequest(query: .init(userId: userId))
try await app.testing().test(request, locale: en) { response in
    #expect(response.status == .ok)
    #expect(response.body?.viewModel.name == "Expected Name")
}

// ✅ RIGHT - Test multiple locales
for locale in [en, es] {
    try await app.testing().test(request, locale: locale) { response in
        #expect(response.status == .ok)
        // Localized values are automatically handled
    }
}

// ✅ RIGHT - Test error responses
let badRequest = MyShowRequest(query: .init(userId: invalidId))
try await app.testing().test(badRequest, locale: en) { response in
    #expect(response.status == .notFound)
    #expect(response.error != nil)
}
```

**路径由 ServerRequest 类型决定。HTTP 方法来自相应的操作。头部信息是自动生成的。** **你绝对不能** 手动编写 URL 字符串或解码 JSON。**

---

## 何时使用此技能

- 测试任何 ServerRequest 实现
- 验证 CRUD 操作的服务器响应
- 测试错误处理和边缘情况
- 多语言环境的响应验证
- 客户端请求类型与服务器控制器之间的集成测试

**如果你打算编写 `URLSession`、`app.test(.GET, "/path")` 或手动解码 JSON，请停止使用这些方法，转而使用此技能。**

## 该技能生成的内容

| 文件 | 位置 | 用途 |
|------|----------|---------|
| `{Feature}RequestTests.swift` | `Tests/{Target}Tests/Requests/` | ServerRequest 的测试套件 |
| 测试 YAML（如需要） | `Tests/{Target}Tests/TestYAML/` | 测试视图模型的本地化配置 |

## 项目结构配置

| 占位符 | 描述 | 示例 |
|-------------|-------------|---------|
| `{Feature}` | 特性或实体名称（PascalCase） | `Idea`, `User`, `Dashboard` |
| `{Target}` | 服务器测试目标 | `WebServerTests`, `AppTests` |
| `{ViewModelsTarget}` | 共享视图模型 SPM 目标 | `ViewModels` |
| `{WebServerTarget}` | 服务器端目标 | `WebServer`, `AppServer` |
| `{ResourceDir}` | YAML 资源目录 | `TestYAML`, `Resources` |

---

## 关键类型

### TestingServerRequestResponse<R>

用于封装类型化的 HTTP 响应：

| 属性 | 类型 | 描述 |
|----------|------|-------------|
| `status` | `HTTPStatus` | HTTP 状态码（.ok, .notFound 等） |
| `headers` | `HTTPHeaders` | 响应头部信息 |
| `body` | `RResponseBody?` | **类型化** 的响应体（自动解码） |
| `error` | `R.ResponseError?` | **类型化** 的错误信息（自动解码） |

### TestingApplicationTester 扩展

```swift
func test<R: ServerRequest>(
    _ request: R,
    locale: Locale = en,
    headers: HTTPHeaders = [:],
    afterResponse: (TestingServerRequestResponse<R>) async throws -> Void
) async throws -> any TestingApplicationTester
```

### 便捷的语言设置

`TestingApplicationTester` 支持以下语言设置：
- `en` - 英语
- `enUS` - 美式英语
- `enGB` - 英国英语
- `es` - 西班牙语

---

## 测试结构

### 基本测试套件

```swift
import FOSFoundation
@testable import FOSMVVM
import FOSTesting
import FOSTestingVapor
import Foundation
import Testing
import Vapor
import VaporTesting

@Suite("MyFeature Request Tests")
struct MyFeatureRequestTests {
    @Test func showRequest_success() async throws {
        try await withTestApp { app in
            let request = MyShowRequest(query: .init(id: validId))

            try await app.testing().test(request, locale: en) { response in
                #expect(response.status == .ok)
                #expect(response.body?.viewModel != nil)
            }
        }
    }

    @Test func showRequest_notFound() async throws {
        try await withTestApp { app in
            let request = MyShowRequest(query: .init(id: invalidId))

            try await app.testing().test(request, locale: en) { response in
                #expect(response.status == .notFound)
            }
        }
    }
}

private func withTestApp(_ test: (Application) async throws -> Void) async throws {
    try await withApp { app in
        // Configure routes
        try app.routes.register(collection: MyController())
        try await test(app)
    }
}
```

### 测试不同的请求类型

| 请求类型 | HTTP 方法 | 需要测试的内容 |
|--------------|-------------|--------------|
| `ShowRequest` | GET | 查询参数、响应体、本地化内容 |
| `ViewModelRequest` | GET | 视图模型数据的填充、所有本地化字段 |
| `CreateRequest` | POST | 请求体验证、创建的实体、返回的 ID |
| `UpdateRequest` | PATCH | 请求体验证、更新的实体、响应结果 |
| `DeleteRequest` | DELETE | 实体的删除、状态码 |

---

## 如何使用此技能

**调用方式：**
/fosmvvm-serverrequest-test-generator

**先决条件：**
- 理解 ServerRequest 类型的含义
- 确定了测试场景（成功路径、错误路径、验证规则）
- 控制器实现已经存在或正在创建中
- 熟悉 VaporTesting 基础设施

**工作流程集成：**
此技能用于测试 ServerRequest 的实现。它会自动参考对话内容——无需提供文件路径或问题解答。通常会按照 `fosmvvm-serverrequest-generator` 的方式使用。

## 模式实现

此技能会根据对话内容来确定测试结构：

### 请求分析

从对话内容中，技能会识别：
- **ServerRequest 的类型**（来自之前的讨论或服务器实现）
- **请求协议**（如 ShowRequest、CreateRequest、UpdateRequest 等）
- **ResponseBody 的类型**（视图模型或简单结构）
- **ResponseError 的类型**（自定义错误或 EmptyError）

### 测试场景规划

根据操作语义：
- **成功路径**（有效输入、预期输出）
- **错误路径**（未找到、验证失败、业务逻辑错误）
- **本地化**（如果 ResponseBody 包含本地化字段）
- **多语言环境**（针对支持的语言进行测试）

### 基础设施检测

根据项目状态：
- **现有的测试模式**（代码库中的类似测试文件）
- **本地化设置**（需要 YAML 固定文件）
- **数据库需求**（测试所需的种子数据）

### 测试文件生成

1. 符合 VaporTesting 模式的测试套件
2. 每个测试场景对应一个 `@Test` 函数
3. 使用 `withTestApp` 辅助函数进行应用程序设置
4. 注册路由
5. 使用 `app.testing().test()` 调用请求

### 信息来源

技能会参考以下信息：
- **之前的讨论**：测试需求和讨论的测试场景
- **ServerRequest**：如果 Claude 已将 ServerRequest 代码读取到上下文中
- **控制器**：来自服务器实现的信息
- **现有的测试**：代码库中类似测试文件的分析结果

---

## 常见场景

### 带有本地化的 ViewModelRequest 测试

```swift
@Test func viewModelRequest_multiLocale() async throws {
    try await withTestApp { app in
        let request = DashboardViewModelRequest()

        // Test English
        try await app.testing().test(request, locale: en) { response in
            #expect(response.status == .ok)
            let vm = try #require(response.body)
            #expect(try vm.pageTitle.localizedString == "Dashboard")
        }

        // Test Spanish
        try await app.testing().test(request, locale: es) { response in
            #expect(response.status == .ok)
            let vm = try #require(response.body)
            #expect(try vm.pageTitle.localizedString == "Tablero")
        }
    }
}
```

### 带有验证的 CreateRequest 测试

```swift
@Test func createRequest_validInput() async throws {
    try await withTestApp { app in
        let request = CreateIdeaRequest(requestBody: .init(
            content: "Valid idea content"
        ))

        try await app.testing().test(request, locale: en) { response in
            #expect(response.status == .ok)
            #expect(response.body?.id != nil)
        }
    }
}

@Test func createRequest_invalidInput() async throws {
    try await withTestApp { app in
        let request = CreateIdeaRequest(requestBody: .init(
            content: ""  // Empty content should fail validation
        ))

        try await app.testing().test(request, locale: en) { response in
            #expect(response.status == .badRequest)
            #expect(response.error != nil)
        }
    }
}
```

### UpdateRequest 测试

```swift
@Test func updateRequest_success() async throws {
    try await withTestApp { app in
        // First create an entity
        let createRequest = CreateIdeaRequest(requestBody: .init(content: "Original"))
        var createdId: ModelIdType?
        try await app.testing().test(createRequest, locale: en) { response in
            createdId = response.body?.id
        }

        // Then update it
        let updateRequest = UpdateIdeaRequest(requestBody: .init(
            ideaId: try #require(createdId),
            content: "Updated content"
        ))

        try await app.testing().test(updateRequest, locale: en) { response in
            #expect(response.status == .ok)
            #expect(response.body?.viewModel.content == "Updated content")
        }
    }
}
```

### DeleteRequest 测试

```swift
@Test func deleteRequest_success() async throws {
    try await withTestApp { app in
        // Create, then delete
        let deleteRequest = DeleteIdeaRequest(requestBody: .init(ideaId: existingId))

        try await app.testing().test(deleteRequest, locale: en) { response in
            #expect(response.status == .ok)
        }

        // Verify deleted (should return not found)
        let showRequest = ShowIdeaRequest(query: .init(ideaId: existingId))
        try await app.testing().test(showRequest, locale: en) { response in
            #expect(response.status == .notFound)
        }
    }
}
```

### 带有查询参数的 ShowRequest 测试

```swift
@Test func showRequest_withQuery() async throws {
    try await withTestApp { app in
        let request = UserShowRequest(query: .init(
            userId: userId,
            includeDetails: true
        ))

        try await app.testing().test(request, locale: en) { response in
            #expect(response.status == .ok)
            #expect(response.body?.user.details != nil)
        }
    }
}
```

---

## ServerRequestError 的本地化测试

### 为什么错误本地化测试有所不同

与视图模型不同，`ServerRequestError` 类型：
- 通常是 **枚举类型**，而不是结构体
- 不遵循 `Stubbable` 或 `RetrievablePropertyNames` 规范
- 不能像视图模型那样使用 `expectTranslations(ErrorType.self)` 方法

这意味着你必须 **逐一手动测试每个错误情况**。

### 测试模式

对于每个错误类型的 `Localizable` 属性，使用 `LocalizableTestCase.expectTranslations(_ localizable:)` 方法：

```swift
@Suite("MyError Localization Tests")
struct MyErrorLocalizationTests: LocalizableTestCase {
    let locStore: LocalizationStore

    init() throws {
        self.locStore = try Self.loadLocalizationStore(
            bundle: Bundle.module,
            resourceDirectoryName: "TestYAML"
        )
    }

    @Test func errorMessages_simpleErrors() throws {
        // Test each error case individually
        let serverFailed = MyError(code: .serverFailed)
        try expectTranslations(serverFailed.message)

        let appFailed = MyError(code: .applicationFailed)
        try expectTranslations(appFailed.message)
    }

    @Test func errorMessages_withSubstitutions() throws {
        // For errors with associated values, test with representative values
        let quotaError = QuotaError(code: .quotaExceeded(requested: 100, maximum: 50))
        try expectTranslations(quotaError.message)
    }
}
```

### 在集成测试中测试错误信息

在测试完整的请求/响应周期时，需要验证错误信息是否正确显示：

```swift
@Test func createRequest_validationError_hasLocalizedMessage() async throws {
    try await withTestApp { app in
        let request = CreateIdeaRequest(requestBody: .init(content: ""))

        try await app.testing().test(request, locale: en) { response in
            #expect(response.status == .badRequest)
            let error = try #require(response.error)

            // Verify the message resolved (not empty or pending)
            #expect(!error.message.isEmpty)

            // Optionally verify specific text for English locale
            #expect(try error.message.localizedString.contains("required"))
        }
    }
}
```

### 为什么不能使用 `Stubbable` 方法？

`Stubbable` 方法适用于视图模型，因为：
- 视图模型是具有多个属性的结构体
- 单个 `stub()` 可以提供一个完整的测试实例

而对于 `ServerRequestError` 类型：
- 每个错误类型可能有不同的关联值
- 每个错误类型可能有不同的本地化消息
- 单个 `stub()` 无法覆盖所有情况

**你必须逐一列举并测试每个错误情况。**

### 错误本地化测试的检查清单

- [ ] 测试每个枚举类型的简单错误情况
- [ ] 测试参数化错误的代表性关联值
- [ ] 验证所有配置的语言环境中错误信息是否正确显示
- [ ] 验证 `LocalizableSubstitutions` 中的替换占位符是否被正确替换

---

## 故障排除

### “Route not found” 错误

**原因：** 控制器未在测试应用程序中注册。

**解决方法：** 在测试之前注册控制器：
```swift
try app.routes.register(collection: MyController())
```

### 响应体为 `nil` 但状态码为 `.ok`

**原因：** JSON 解码失败且未引发异常。

**解决方法：** 确保 `ResponseBody` 的类型与服务器响应完全匹配。使用 `response.headers` 来验证 `Content-Type`。

### 本地化未应用

**原因：** 未将语言设置传递给编码器。

**解决方法：** `test(_:locale:)` 方法会自动处理语言设置。确保传递了正确的语言参数。

### 响应中缺少本地化内容

**原因：** YAML 本地化配置未加载。

**解决方法：** 在测试应用程序设置中初始化本地化存储：
```swift
try app.initYamlLocalization(
    bundle: Bundle.module,
    resourceDirectoryName: "TestYAML"
)
```

---

## 命名规范

| 概念 | 规范 | 示例 |
|---------|------------|---------|
| 测试套件 | `{Feature}RequestTests` | `IdeaRequestTests` |
| 测试文件 | `{Feature}RequestTests.swift` | `IdeaRequestTests.swift` |
| 测试方法（成功情况） | `{action}Request_success` | `showRequest_success` |
| 测试方法（错误情况） | `{action}Request_{errorCase}` | `showRequest_notFound` |
| 测试方法（验证情况） | `{action}Request_{validationCase}` | `createRequest_emptyContent` |
| 测试辅助函数 | `withTestApp` | `withTestApp { app in }` |
| 语言常量 | `en`, `es`, `enUS`, `enGB` | `locale: en` |

---

## 文件模板

有关完整的文件模板，请参阅 [reference.md](reference.md)。

---

## 参考资料

- [FOSMVVMArchitecture.md](../../docs/FOSMVVMArchitecture.md) - 完整的架构信息
- [fosmvvm-serverrequest-generator](../fosmvvm-serverrequest-generator/SKILL.md) - 创建 ServerRequest 类型
- [fosmvvm-viewmodel-test-generator](../fosmvvm-viewmodel-test-generator/SKILL.md) - 测试视图模型（仅包含本地化功能）
- [reference.md](reference.md) - 完整的文件模板

---

## 版本历史

| 版本 | 日期 | 更改内容 |
|---------|------|---------|
| 1.1 | 2025-01-20 | 添加 ServerRequestError 的本地化测试指导 |
| 1.2 | 2026-01-24 | 采用基于上下文的信息处理方式（不再解析文件或询问路径）。技能会自动参考对话内容，而不是依赖文件路径或问题解答。 |
| 1.0 | 2025-01-05 | 初始版本 |