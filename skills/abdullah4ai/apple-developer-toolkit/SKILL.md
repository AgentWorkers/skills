---
name: apple-developer-toolkit
description: "这是一款集成了三项功能的一体化苹果开发者工具，所有功能都打包在一个统一的二进制文件中。  
**功能1：文档查询**  
- 可在苹果的各个框架、符号库中搜索文档；  
- 支持查询2014年至2025年间的1,267场WWDC（世界开发者大会）的会议记录；  
- 无需任何认证信息即可使用。  
**功能2：App Store Connect CLI**  
- 提供超过120条命令，涵盖应用程序的构建（查找/等待/上传）、测试（TestFlight）、提交前验证、签名、订阅（支持家庭共享）、应用内购买（IAP）、数据分析、Xcode Cloud管理、元数据处理、发布流程监控、用户反馈收集、促销活动、产品页面管理、提名流程、可访问性设置等功能；  
- 需要App Store Connect的API密钥才能使用。  
**功能3：多平台应用构建工具**  
- 能够根据自然语言描述自动生成完整的Swift/SwiftUI应用程序；  
- 具有自动修复代码错误的功能、模拟器启动功能、交互式聊天界面，并支持直接在Xcode中打开生成的应用程序；  
- 需要LLM（大型语言模型）的API密钥以及Xcode开发环境；  
- 包含38条iOS开发规范和12份SwiftUI最佳实践指南，涵盖界面设计、状态管理、现代API使用等方面的内容。  
**适用场景**：  
- 查阅苹果官方API文档；  
- 管理App Store Connect相关事务；  
- 查找WWDC会议记录；  
- 从零开始开发iOS、watchOS、tvOS、macOS或visionOS应用程序。  
**不适用场景**：  
- 非苹果平台的应用程序开发；  
- 通用编程任务。"
metadata:
  {
    "openclaw":
      {
        "emoji": "🍎",
        "requires":
          {
            "bins": ["node"],
            "anyBins": ["appledev"],
          },
        "install":
          [
            {
              "id": "appledev",
              "kind": "brew",
              "tap": "Abdullah4AI/tap",
              "formula": "appledev",
              "bins": ["appledev"],
              "label": "Apple Developer Toolkit - unified binary (Homebrew)",
            },
          ],
        "env":
          {
            "optional":
              [
                {
                  "name": "APPSTORE_KEY_ID",
                  "description": "App Store Connect API Key ID. Required only for App Store Connect features. Get from https://appstoreconnect.apple.com/access/integrations/api",
                },
                {
                  "name": "APPSTORE_ISSUER_ID",
                  "description": "App Store Connect API Issuer ID. Required only for App Store Connect features.",
                },
                {
                  "name": "APPSTORE_PRIVATE_KEY_PATH",
                  "description": "Path to App Store Connect API .p8 private key file. Required only for App Store Connect features. Alternative: use APPSTORE_PRIVATE_KEY or APPSTORE_PRIVATE_KEY_B64.",
                },
                {
                  "name": "LLM_API_KEY",
                  "description": "LLM API key for code generation. Required only for iOS App Builder. Supports multiple AI backends.",
                },
              ],
          },
      },
  }
---
# Apple 开发者工具包（Apple Developer Toolkit）

这是一个集成了三个工具的单一二进制文件。每个工具都可以独立运行，并且需要不同的认证凭据。

## 架构

该工具包以一个统一的二进制文件 `appledev` 的形式提供，支持多次调用：

```
appledev build ...    # iOS app builder (SwiftShip)
appledev store ...    # App Store Connect CLI
appledev b ...        # Short alias
appledev s ...        # Short alias
```

一个二进制文件，三个工具，零重复代码。

## 各工具所需的认证凭据

| 功能                | 所需凭据                | 是否需要设置                |
|------------------|------------------|-----------------------|
| 文档搜索（第1部分）        | 无                    | 是                    |
| App Store Connect（第2部分）    | App Store Connect API 密钥（.p8格式） | 否                    |
| iOS 应用构建器（第3部分）     | LLM API 密钥 + Xcode           | 否                    |

## 设置

### 第1部分：文档搜索（无需设置）

可以直接使用 Node.js 运行：

```bash
node cli.js search "NavigationStack"
```

### 第2部分：App Store Connect CLI

通过 Homebrew 安装：

```bash
brew install Abdullah4AI/tap/appledev
```

使用您的 App Store Connect API 密钥进行身份验证：

```bash
appledev store auth login --name "MyApp" --key-id "KEY_ID" --issuer-id "ISSUER_ID" --private-key /path/to/AuthKey.p8
```

或者设置环境变量：

```bash
export APPSTORE_KEY_ID="your-key-id"
export APPSTORE_ISSUER_ID="your-issuer-id"
export APPSTORE_PRIVATE_KEY_PATH="/path/to/AuthKey.p8"
```

API 密钥可以在 [https://appstoreconnect.apple.com/access/integrations/api](https://appstoreconnect.apple.com/access/integrations/api) 上创建。

### 第3部分：iOS 应用构建器

**先决条件**：需要安装 Xcode（包含 iOS 模拟器）、XcodeGen 以及用于代码生成的 LLM API 密钥。

```bash
appledev build setup    # Checks and installs prerequisites
```

### 从源代码构建

```bash
bash scripts/setup.sh
```

## 第1部分：文档搜索

```bash
node cli.js search "NavigationStack"
node cli.js symbols "UIView"
node cli.js doc "/documentation/swiftui/navigationstack"
node cli.js overview "SwiftUI"
node cli.js samples "SwiftUI"
node cli.js wwdc-search "concurrency"
node cli.js wwdc-year 2025
node cli.js wwdc-topic "swiftui-ui-frameworks"
```

## 第2部分：App Store Connect

完整参考文档：[references/app-store-connect.md](references/app-store-connect.md)

| 功能            | 命令                        |
|------------------|---------------------------|
| 列出应用            | `appledev store apps`            |
| 上传构建文件         | `appledev store builds upload --app "APP_ID" --ipa "app.ipa" --wait` |
| 根据编号查找构建文件     | `appledev store builds find --app "APP_ID" --build-number "42"` |
| 等待构建文件处理       | `appledev store builds wait --build "BUILD_ID"` |
| 发布 TestFlight      | `appledev store publish testflight --app "APP_ID" --ipa "app.ipa" --group "Beta" --wait` |
| 提交应用到 App Store     | `appledev store publish appstore --app "APP_ID" --ipa "app.ipa" --submit --confirm --wait` |
| 提交前验证         | `appledev store validate --app "APP_ID" --version-id "VERSION_ID"` |
| 列出证书           | `appledev store certificates list`          |
| 查看应用评论         | `appledev store reviews --app "APP_ID" --output table` |
| 更新应用本地化设置     | `appledev store localizations update --app "APP_ID" --locale "en-US" --name "My App"` |
| 查看销售报告         | `appledev store analytics sales --vendor "VENDOR" --type SALES --subtype SUMMARY --frequency DAILY --date "2024-01-20"` |
| 运行 Xcode Cloud        | `appledev store xcode-cloud run --app "APP_ID" --workflow "CI" --branch "main" --wait` |
| 提交应用公证         | `appledev store notarization submit --file ./MyApp.zip --wait` |
| 查看应用状态         | `appledev store status --app "APP_ID" --output table` |
| 获取每周分析报告       | `appledev store insights weekly --app "APP_ID" --source analytics` |
| 下载应用元数据       | `appledev store metadata pull --app "APP_ID" --version "1.2.3" --dir ./metadata` |
| 生成发布说明         | `appledev store release-notes generate --since-tag "v1.2.2"` |
| 比较不同语言的本地化设置   | `appledev store diff localizations --app "APP_ID" --path ./metadata` |
| 提名应用参加评选       | `appledev store nominations create --app "APP_ID" --name "Launch"` |
| 设置应用价格         | `appledev store pricing price-points --app "APP_ID" --price 0.99` |
| 创建 IAP 订阅计划       | `appledev store iap create --app "APP_ID" --family-sharable` |
| 创建订阅计划         | `appledev store subscriptions create --app "APP_ID" --family-sharable` |

### 环境变量

所有环境变量都是可选的。设置这些变量可以覆盖相应的命令参数。

| 变量                | 描述                        |
|------------------|---------------------------|
| APPSTORE_KEY_ID         | API 密钥 ID                    |
| APPSTORE_ISSUER_ID         | API 发行者 ID                    |
| APPSTORE_PRIVATE_KEY_PATH     | .p8 密钥文件的路径                |
| APPSTORE_PRIVATE_KEY       | 私钥的原始字符串                |
| APPSTORE_PRIVATE_KEY_B64       | 私钥的 Base64 编码形式             |
| APPSTORE_APP_ID         | 默认应用 ID                    |
| APPSTORE_PROFILE       | 默认的认证配置文件                |
| APPSTORE_DEBUG          | 是否启用调试输出                  |
| APPSTORE_TIMEOUT        | 请求超时时间                    |
| APPSTORE_BYPASS_KEYCHAIN     | 是否跳过系统的密钥链                |

## 第3部分：多平台应用构建器

支持 iOS、watchOS、tvOS 和 iPad 平台。能够利用人工智能技术从自然语言描述生成完整的 Swift/SwiftUI 应用程序。

```bash
appledev build                     # Interactive mode
appledev build setup               # Install prerequisites (Xcode, XcodeGen, AI backend)
appledev build fix                 # Auto-fix build errors
appledev build run                 # Build and launch in simulator
appledev build open                # Open project in Xcode
appledev build chat                # Interactive chat mode (edit/ask questions)
appledev build info                # Show project status
appledev build usage               # Token usage and cost
```

### 支持的平台

| 平台                | 支持情况                    |
|------------------|------------------------|
| iOS                | 完全支持                      |
| iPad                | 完全支持                      |
| macOS                | 支持                        |
| watchOS                | 支持                        |
| tvOS                | 支持                        |
| visionOS                | 支持                        |

### 工作原理

1. **分析**：从应用描述中提取应用名称、功能、核心流程和目标平台。
2. **规划**：生成文件级别的构建计划（包括数据模型、导航结构和设计方案）。
3. **构建**：生成 Swift 源代码文件、项目配置文件（project.yml）和资源目录。
4. **修复**：自动编译并修复错误，直到构建成功。
5. **运行**：启动模拟器并运行应用程序。

### 交互式命令

| 命令                | 描述                        |
|------------------|---------------------------|
| /run                | 在模拟器中构建并运行应用程序          |
| /fix                | 自动修复编译错误                |
| /open                | 在 Xcode 中打开项目                |
| /ask [question]         | 提问关于项目的任何问题              |
| /model [name]           | 切换应用模型（如 sonnet、opus、haiku 等）     |
| /info                | 显示项目详细信息                |
| /usage                | 显示令牌的使用情况和费用                |

## 参考文档

| 参考文档            | 内容                        |
|------------------|---------------------------|
| [references/app-store-connect.md](references/app-store-connect.md) | 完整的 App Store Connect CLI 命令列表      |
| [references/ios-rules/](references/ios-rules/) | 38 条 iOS 开发规则                |
| [references/swiftui-guides/](references/swiftui-guides/) | 12 份 SwiftUI 开发最佳实践指南        |
| [references/ios-app-builder-prompts.md](references/ios-app-builder-prompts.md) | 应用构建时的系统提示信息            |

### iOS 开发规则（38 个文件）

包括可访问性（accessibility）、应用剪辑（app_clips）、应用审核（app_review）、生物识别技术（biometrics）、摄像头功能（camera）、图表显示（charts）、颜色对比度（color_contrast）、组件使用（components）、暗黑模式（dark_mode）、设计系统（design-system）、反馈机制（feedback_states）、文件结构（file-structure）、禁止使用的设计模式（forbidden-patterns）、基础模型（foundation_models）、手势操作（gestures）、健康Kit（healthkit）、实时活动（live_activities）、本地化设置（localization）、地图功能（maps）、MVVM 架构（mvvm-architecture）、导航模式（navigation-patterns）、通知服务（notification_service）、通知功能（notifications）、Safari 扩展（safari_extension）、分享扩展（share-extension）、Siri 意图（siri_intents）、布局间距（spacing_layout）、语音交互（speech）、存储策略（storage-patterns）、Swift 编程规范（swift-conventions）、视图组合（view-composition）、视图复杂性（view-complexity）、网站链接（website_links）以及各种视图组件（widgets）等。

### SwiftUI 开发指南（12 份文件）

涵盖动画效果（animations）、表单与输入（forms-and-input）、布局设计（layout）、液态玻璃界面（liquid-glass）、列表布局（list-patterns）、媒体处理（media）、现代 API 设计（modern-apis）、导航系统（navigation）、性能优化（performance）、滚动效果（scroll-patterns）、状态管理（state-management）、文本格式化（text-formatting）等方面的内容。