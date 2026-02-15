---
name: fosmvvm-swiftui-app-setup
description: 为 FOSMVVM SwiftUI 应用程序设置 `@main` App 结构体。配置 MVVMEnvironment、部署 URL 以及测试基础设施。
homepage: https://github.com/foscomputerservices/FOSUtilities
metadata: {"clawdbot": {"emoji": "🚀", "os": ["darwin"]}}
---

# FOSMVVM SwiftUI 应用程序设置

使用 FOSMVVM 架构生成 SwiftUI 应用程序的主 `App` 结构。

## 概念基础

> 有关完整的架构信息，请参阅 [FOSMVVMArchitecture.md](../../docs/FOSMVVMArchitecture.md) | [OpenClaw 参考]({{baseDir}}/references/FOSMVVMArchitecture.md)

`App` 结构是 SwiftUI 应用程序的入口点。在 FOSMVVM 中，它有三个核心职责：

```
┌─────────────────────────────────────────────────────────────┐
│                      @main App Struct                        │
├─────────────────────────────────────────────────────────────┤
│  1. MVVMEnvironment Setup                                   │
│     - Bundles (app + localization resources)                │
│     - Deployment URLs (production, staging, debug)          │
│                                                              │
│  2. Environment Injection                                   │
│     - .environment(mvvmEnv) on WindowGroup                  │
│     - Custom environment values                             │
│                                                              │
│  3. Test Infrastructure (DEBUG only)                        │
│     - .testHost { } modifier for UI testing                 │
│     - registerTestingViews() for individual view testing    │
└─────────────────────────────────────────────────────────────┘
```

## 核心组件

### 1. MVVMEnvironment

`MVVMEnvironment` 为所有视图提供 FOSMVVM 基础设施：

```swift
private var mvvmEnv: MVVMEnvironment {
    MVVMEnvironment(
        appBundle: Bundle.main,
        resourceBundles: [
            MyAppViewModelsResourceAccess.localizationBundle,
            SharedResourceAccess.localizationBundle
        ],
        deploymentURLs: [
            .production: .init(serverBaseURL: URL(string: "https://api.example.com")!),
            .debug: .init(serverBaseURL: URL(string: "http://localhost:8080")!)
        ]
    )
}
```

**关键配置：**
- `appBundle` - 通常是 `Bundle.main`（应用程序的主包）
- `resourceBundles` - 来自各个模块的本地化资源包数组
- `deploymentURLs` - 每个部署环境的 URL

**资源包访问器：**

每个包含本地化资源的模块都应提供一个资源包访问器：

```swift
// In your ViewModels module (e.g., MyAppViewModels/ResourceAccess.swift)
public enum MyAppViewModelsResourceAccess {
    public static var localizationBundle: Bundle { Bundle.module }
}
```

这种模式：
- 使用 `Bundle.module`，SPM 会为每个模块自动提供该功能
- 提供一个清晰的公共 API 来访问模块的资源
- 将资源包访问集中到一个位置（每个模块中）

### 2. 环境注入

`MVVMEnvironment` 在 `WindowGroup` 级别被注入：

```swift
var body: some Scene {
    WindowGroup {
        MyView()
    }
    .environment(mvvmEnv)  // ← Makes FOSMVVM infrastructure available
}
```

这使得环境对层次结构中的所有视图都可用。

### 3. 测试基础设施

测试基础设施支持使用特定配置进行 UI 测试：

**`.testHost { }` 修改器：**
```swift
var body: some Scene {
    WindowGroup {
        ZStack {
            LandingPageView()
        }
        #if DEBUG
        .testHost { testConfiguration, testView in
            // Handle specific test configurations...

            default:
                testView
                    .onAppear {
                        underTest = ProcessInfo.processInfo.arguments.count > 1
                    }
        }
        #endif
    }
}
```

**关键点：**
- 适用于 `WindowGroup` 中的顶层视图（层次结构中最外层的视图）
- 确保该修改器能够覆盖整个视图层次结构以拦截测试配置
- 必须包含 `default:` 情况
- `default:` 情况通过进程参数检测测试模式
- 设置 `@State private var underTest = false` 标志
- 可选：为高级场景添加特定的测试配置

**`registerTestingViews()` 函数：**
```swift
#if DEBUG
private extension MyApp {
    @MainActor func registerTestingViews() {
        mvvmEnv.registerTestView(LandingPageView.self)
        mvvmEnv.registerTestView(SettingsView.self)
        // ... register all ViewModelViews for individual testing
    }
}
#endif
```

**关键点：**
- 是 `App` 结构的扩展（而非 `MVVMEnvironment` 的扩展）
- 从 `init()` 方法调用
- 注册所有用于隔离测试的 `ViewModelView`
- 仅适用于调试（DEBUG）模式

## 何时使用此技能

- 开始新的 FOSMVVM SwiftUI 应用程序
- 将现有的 SwiftUI 应用程序迁移到 FOSMVVM
- 设置带有适当 FOSMVVM 基础设施的 `App` 结构
- 配置 UI 测试的测试基础设施

## 此技能生成的文件

| 组件 | 位置 | 用途 |
|-----------|----------|---------|
| 主 `App` 结构 | `Sources/App/{AppName}.swift` | 包含 `MVVMEnvironment` 设置的入口点 |
| MVVMEnvironment 配置 | `App` 结构中的计算属性 | 包和部署 URL |
| 测试基础设施 | `App` 结构中的调试（DEBUG）代码块 | 支持 UI 测试 |

## 项目结构配置

| 占位符 | 描述 | 示例 |
|-------------|-------------|---------|
| `{AppName}` | 你的应用程序名称 | `MyApp`, `AccelApp` |
| `{AppTarget}` | 主应用程序目标 | `App` |
| `{ResourceBundles}` | 包含本地化资源的模块名称 | `MyAppViewModels`, `SharedResources` |

## 如何使用此技能

**调用方式：**
/fosmvvm-swiftui-app-setup

**先决条件：**
- 从对话中了解应用程序名称
- 已经讨论或记录了部署 URL
- 已确定资源包（包含本地化资源的模块）
- 明确了测试支持的需求

**工作流程集成：**
此技能用于设置新的 FOSMVVM SwiftUI 应用程序或在现有应用程序中添加 FOSMVVM 基础设施。该技能会自动参考对话内容——无需提供文件路径或进行问答。

## 模式实现

此技能根据对话内容来确定 `App` 结构的配置：

### 配置检测

从对话内容中，技能会识别：
- **应用程序名称**（来自项目讨论或现有代码）
- **部署环境**（生产环境、测试环境、调试环境的 URL）
- **资源包**（包含本地化 YAML 文件的模块）
- **测试基础设施**（是否需要支持 UI 测试）

### MVVMEnvironment 设置

根据项目结构：
- **应用程序主包**（通常是 `Bundle.main`）
- **资源包访问器**（来自已识别的模块）
- **部署 URL**（每个环境的 URL）
- **当前版本**（来自共享模块）

### 测试基础设施规划

如果需要测试支持：
- **测试检测**（通过进程参数进行检查）
- **测试主机修改器**（覆盖顶层视图）
- **视图注册**（所有用于测试的 `ViewModelView`）

### 文件生成

1. 带有 `@main` 属性的主 `App` 结构
2. `MVVMEnvironment` 的计算属性
3. 具有环境注入的 `WindowGroup`
4. 测试基础设施（如果需要，则仅适用于调试模式）
5. `registerTestingViews()` 扩展（如果需要测试支持）

### 来源信息

技能参考的信息来自：
- **之前的对话**：应用程序需求、部署环境的讨论
- **项目结构**：通过对代码库的分析
- **现有的模式**：如果有的话，参考其他 FOSMVVM 应用程序的模式

## 关键模式

### `MVVMEnvironment` 作为计算属性

`MVVMEnvironment` 是一个计算属性，而不是存储属性：

```swift
private var mvvmEnv: MVVMEnvironment {
    MVVMEnvironment(
        appBundle: Bundle.main,
        resourceBundles: [...],
        deploymentURLs: [...]
    )
}
```

**为什么使用计算属性？**
- 将初始化逻辑分离
- 可以在调试（DEBUG）和发布（RELEASE）模式下进行自定义
- 明确依赖于资源包和 URL

### 测试检测模式

默认的测试检测使用进程参数：

```swift
@State private var underTest = false

// In .testHost default case:
testView
    .onAppear {
        // Right now there's no other way to detect if the app is under test.
        // This is only debug code, so we can proceed for now.
        underTest = ProcessInfo.processInfo.arguments.count > 1
    }
```

**为什么使用这种方法？**
- 对于调试（DEBUG）构建来说简单可靠
- 没有额外的依赖项
- 进程参数由测试运行器设置

### 注册所有 `ViewModelView`

所有 `ViewModelView` 都应被注册以进行测试：

```swift
@MainActor func registerTestingViews() {
    // Landing Page
    mvvmEnv.registerTestView(LandingPageView.self)

    // Settings
    mvvmEnv.registerTestView(SettingsView.self)
    mvvmEnv.registerTestView(ProfileView.self)

    // Dashboard
    mvvmEnv.registerTestView(DashboardView.self)
    mvvmEnv.registerTestView(CardView.self)
}
```

**组织建议：**
- 按功能/屏幕分组并添加注释
- 在组内按字母顺序排列
- 每行一个视图以便于扫描

## 常见自定义

### 多个环境值

你可以注入多个环境值：

```swift
var body: some Scene {
    WindowGroup {
        MyView()
    }
    .environment(mvvmEnv)
    .environment(appState)
    .environment(\.colorScheme, .dark)
    .environment(\.customValue, myCustomValue)
}
```

### 条件性视图注册

你可以根据构建配置有条件地注册视图：

```swift
#if DEBUG
@MainActor func registerTestingViews() {
    mvvmEnv.registerTestView(LandingPageView.self)

    #if INCLUDE_ADMIN_FEATURES
    mvvmEnv.registerTestView(AdminPanelView.self)
    #endif
}
#endif
```

### 高级测试配置

你可以在 `.testHost` 中添加特定的测试配置：

```swift
.testHost { testConfiguration, testView in
    switch try? testConfiguration.fromJSON() as MyTestConfiguration {
    case .specificScenario(let data):
        testView.environment(MyState.stub(data: data))
            .onAppear { underTest = true }

    default:
        testView
            .onAppear {
                underTest = ProcessInfo.processInfo.arguments.count > 1
            }
    }
}
```

## 文件模板

有关完整的文件模板，请参阅 [reference.md](reference.md)。

## 命名约定

| 概念 | 命名约定 | 示例 |
|---------|------------|---------|
| `App` 结构 | `{Name}App` | `MyApp`, `AccelApp` |
| 主文件 | `{Name}App.swift` | `MyApp.swift` |
| `MVVMEnvironment` 属性 | `mvvmEnv` | 始终使用 `mvvmEnv` |
| 测试标志 | `underTest` | 始终使用 `underTest` |

## 部署配置

FOSMVVM 支持通过 `Info.plist` 进行部署检测：

```
CI Pipeline Sets:
   FOS_DEPLOYMENT build setting (e.g., "staging" or "production")
        ↓
Info.plist Contains:
   FOS-DEPLOYMENT = $(FOS_DEPLOYMENT)
        ↓
Runtime Detection:
   FOSMVVM.Deployment.current reads from Bundle.main.infoDictionary
```

**本地开发覆盖方式：**
- 编辑 Scheme → 运行 → 参数 → 环境变量
- 添加：`FOS-DEPLOYMENT = staging`

## 参考资料

- [Architecture Patterns](../shared/architecture-patterns.md) - 思维模型和模式
- [FOSMVVMArchitecture.md](../../docs/FOSMVVMArchitecture.md) - 完整的 FOSMVVM 架构
- [fosmvvm-viewmodel-generator](../fosmvvm-viewmodel-generator/SKILL.md) - 用于创建 `ViewModel`
- [reference.md](reference.md) - 完整的文件模板

## 版本历史

| 版本 | 日期 | 更改内容 |
|---------|------|---------|
| 1.0 | 2026-01-23 | 首个用于 SwiftUI 应用程序设置的技能 |
| 1.1 | 2026-01-24 | 更新为基于上下文感知的方法（移除了文件解析和问答环节）。技能现在参考对话内容，而不是询问问题或接受文件路径。