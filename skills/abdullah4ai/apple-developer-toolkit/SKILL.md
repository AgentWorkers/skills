---
name: apple-developer-toolkit
description: "这是一个集成了三种工具的苹果开发者多功能工具包：
1. **文档搜索功能**：支持在苹果的框架、符号以及2014年至2025年间的所有WWDC会议记录中进行搜索。无需任何认证信息即可使用。
2. **App Store Connect CLI**：包含120多个命令，涵盖了应用程序的构建、测试、提交、签名、订阅、In-App购买（IAP）、数据分析、Xcode Cloud管理、元数据处理、发布流程监控、用户反馈分析、促销活动、产品页面设置、开发者提名、无障碍功能配置、预购管理、定价设置等功能。使用该工具需要App Store Connect的API密钥。
3. **iOS应用程序构建工具**：能够根据自然语言描述自动生成完整的Swift/SwiftUI应用程序，并提供自动修复功能及模拟器运行支持。该工具需要LLM（Large Language Model）的API密钥以及Xcode开发环境。此外，还提供了38条iOS开发规范和12份SwiftUI最佳实践指南，涵盖Liquid Glass界面设计、导航逻辑、状态管理以及现代API的使用方法。
**适用场景**：适用于苹果API文档的查阅、App Store Connect的日常管理、WWDC相关信息的查询，以及从零开始开发iOS应用程序的场景。
**不适用场景**：不适用于非苹果平台的开发工作或通用编程任务。"
metadata:
  {
    "openclaw":
      {
        "emoji": "🍎",
        "requires":
          {
            "bins": ["node"],
            "anyBins": ["appstore", "swiftship"],
          },
        "install":
          [
            {
              "id": "appstore",
              "kind": "brew",
              "tap": "Abdullah4AI/tap",
              "formula": "appstore",
              "bins": ["appstore"],
              "label": "App Store Connect CLI (Homebrew)",
            },
            {
              "id": "swiftship",
              "kind": "brew",
              "tap": "Abdullah4AI/tap",
              "formula": "swiftship",
              "bins": ["swiftship"],
              "label": "iOS App Builder (Homebrew)",
            },
          ],
        "env":
          {
            "optional":
              [
                {
                  "name": "APPSTORE_KEY_ID",
                  "description": "App Store Connect API Key ID. Required only for App Store Connect features (Part 2). Get from https://appstoreconnect.apple.com/access/integrations/api",
                },
                {
                  "name": "APPSTORE_ISSUER_ID",
                  "description": "App Store Connect API Issuer ID. Required only for App Store Connect features (Part 2).",
                },
                {
                  "name": "APPSTORE_PRIVATE_KEY_PATH",
                  "description": "Path to App Store Connect API .p8 private key file. Required only for App Store Connect features (Part 2). Alternative: use APPSTORE_PRIVATE_KEY or APPSTORE_PRIVATE_KEY_B64.",
                },
                {
                  "name": "LLM_API_KEY",
                  "description": "LLM API key for code generation. Required only for iOS App Builder (Part 3). swiftship supports multiple AI backends.",
                },
              ],
          },
      },
  }
---
# Apple 开发者工具包（Apple Developer Toolkit）

这是一个集三种工具于一体的工具包，每个工具都可以独立使用，且所需凭证各不相同。

## 各工具的功能及凭证要求

| 功能 | 所需凭证 | 是否需要额外设置 |
|---------|-------------------|-------------------|
| 文档搜索（第1部分） | 无 | 可直接使用 |
| App Store Connect（第2部分） | App Store Connect API 密钥（.p8格式） | 不需要 |
| iOS 应用构建器（第3部分） | LLM API 密钥 + Xcode | 不需要 |

## 设置说明

### 第1部分：文档搜索（无需设置）

可以直接使用 Node.js 运行该工具：

```bash
node cli.js search "NavigationStack"
```

### 第2部分：App Store Connect CLI

通过 Homebrew 安装：

```bash
brew tap Abdullah4AI/tap && brew install appstore
```

使用您的 App Store Connect API 密钥进行身份验证：

```bash
appstore auth login --name "MyApp" --key-id "KEY_ID" --issuer-id "ISSUER_ID" --private-key /path/to/AuthKey.p8
```

或者通过设置环境变量来使用：

```bash
export APPSTORE_KEY_ID="your-key-id"
export APPSTORE_ISSUER_ID="your-issuer-id"
export APPSTORE_PRIVATE_KEY_PATH="/path/to/AuthKey.p8"
```

API 密钥可以在 [https://appstoreconnect.apple.com/access/integrations/api](https://appstoreconnect.apple.com/access/integrations/api) 上生成。

### 第3部分：iOS 应用构建器

通过 Homebrew 安装：

```bash
brew tap Abdullah4AI/tap && brew install swiftship
```

安装前需准备以下工具：Xcode（包含 iOS 模拟器）、XcodeGen 以及用于代码生成的 LLM API 密钥。

```bash
swiftship setup    # Checks and installs prerequisites
```

### 全功能设置脚本

```bash
bash scripts/setup.sh
```

该脚本会显示将要安装的组件，然后询问用户是否确认安装。脚本本身不会安装 Xcode 或配置 API 密钥。若想跳过确认提示，可传递参数 `--yes`。

### 信任与代码来源

这两个 CLI 都是通过 Homebrew 从第三方仓库 `Abdullah4AI/tap` 安装的。源代码是公开透明的，可以在安装前查看：

| 工具名 | 仓库链接 | 安装公式（Tap Formula） |
|--------|--------|-------------|
| `appstore` | [github.com/Abdullah4AI/appstore](https://github.com/Abdullah4AI/appstore) | [homebrew-tap/appstore.rb](https://github.com/Abdullah4AI/homebrew-tap) |
| `swiftship` | [github.com/Abdullah4AI/swiftship](https://github.com/Abdullah4AI/swiftship) | [homebrew-tap/swiftship.rb](https://github.com/Abdullah4AI/homebrew-tap) |

在安装前，可以查看这些仓库的 `Tap Formula` 以确认代码来源：

```bash
brew tap Abdullah4AI/tap
brew cat Abdullah4AI/tap/appstore
brew cat Abdullah4AI/tap/swiftship
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

| 功能 | 命令 |
|------|---------|
| 列出应用 | `appstore apps` |
| 上传构建文件 | `appstore builds upload --app "APP_ID" --ipa "app.ipa" --wait` |
| 发布 TestFlight 测试版本 | `appstore publish testflight --app "APP_ID" --ipa "app.ipa" --group "Beta" --wait` |
| 提交应用到 App Store | `appstore publish appstore --app "APP_ID" --ipa "app.ipa" --submit --confirm --wait` |
| 查看证书 | `appstore certificates list` |
| 查看应用评论 | `appstore reviews --app "APP_ID" --output table` |
| 查看销售报告 | `appstore analytics sales --vendor "VENDOR" --type SALES --subtype SUMMARY --frequency DAILY --date "2024-01-20"` |
| 使用 Xcode Cloud | `appstore xcode-cloud run --app "APP_ID" --workflow "CI" --branch "main" --wait` |
| 提交应用公证文件 | `appstore notarization submit --file ./MyApp.zip --wait` |
| 验证应用 | `appstore validate --app "APP_ID" --version-id "VERSION_ID" --strict` |
| 查看应用状态 | `appstore status --app "APP_ID" --output table` |
| 获取每周分析报告 | `appstore insights weekly --app "APP_ID" --source analytics` |
| 下载应用元数据 | `appstore metadata pull --app "APP_ID" --version "1.2.3" --dir ./metadata` |
| 生成发布说明 | `appstore release-notes generate --since-tag "v1.2.2"` |
| 比较本地化文件 | `appstore diff localizations --app "APP_ID" --path ./metadata` |
| 提交应用提名 | `appstore nominations create --app "APP_ID" --name "Launch"` |

### 环境变量

所有环境变量均为可选设置。设置这些变量后，它们会覆盖命令行参数的默认值。

| 变量 | 说明 |
|----------|-------------|
| `APPSTORE_KEY_ID` | API 密钥 ID |
| `APPSTORE_ISSUER_ID` | API 发行者 ID |
| `APPSTORE_PRIVATE_KEY_PATH` | .p8 密钥文件的路径 |
| `APPSTORE_PRIVATE_KEY` | 私钥的原始字符串 |
| `APPSTORE_PRIVATE_KEY_B64` | 私钥的 Base64 编码形式 |
| `APPSTORE_APP_ID` | 默认应用 ID |
| `APPSTORE_PROFILE` | 默认认证配置 |
| `APPSTORE_DEBUG` | 是否启用调试输出 |
| `APPSTORE_TIMEOUT` | 请求超时时间 |
| `APPSTORE_BYPASS_KEYCHAIN` | 是否跳过系统密钥链验证 |

该工具支持的功能包括：TestFlight、应用构建、签名、订阅管理、IAP（应用内购买）、数据分析、Xcode Cloud、应用公证、Game Center、Webhook（支持本地接收器）、App Clips、截图处理、工作流自动化、元数据管理、状态监控、发布说明生成、价格设置、预购功能、无障碍设置、应用提名、产品页面管理、促销活动、Android 与 iOS 应用的关联、迁移（使用 Fastlane）等。

## 第3部分：iOS 应用构建器

该工具可以利用人工智能生成代码，根据自然语言描述来构建完整的 iOS 应用。

```bash
swiftship              # Interactive mode
swiftship setup        # Install prerequisites (Xcode, XcodeGen, AI backend)
swiftship fix          # Auto-fix build errors
swiftship run          # Build and launch in simulator
swiftship info         # Show project status
swiftship usage        # Token usage and cost
```

### 工作原理

1. **分析**：从描述中提取应用名称、功能及核心业务流程。
2. **规划**：生成文件级别的构建计划（包括数据模型、导航结构、界面设计）。
3. **构建**：生成 Swift 源代码、项目配置文件（project.yml）及资源文件。
4. **修复**：自动编译并修复错误，直到构建成功。
5. **运行**：启动 iOS 模拟器并运行应用。

### 交互式命令

| 命令 | 功能 |
|---------|-------------|
| `/run` | 在模拟器中构建并运行应用 |
| `/fix` | 自动修复编译错误 |
| `/open` | 在 Xcode 中打开项目 |
| `/model [名称]` | 切换应用模型（如 sonnet、opus、haiku 等） |
| `/info` | 显示项目详细信息 |
| `/usage` | 查看令牌的使用情况与费用信息 |

## 参考文档

| 文档链接 | 内容 |
|-----------|---------|
| [references/app-store-connect.md](references/app-store-connect.md) | 完整的 App Store Connect CLI 命令参考 |
| [references/ios-rules/](references/ios-rules/) | 38 条 iOS 开发规范（包括无障碍设计、暗黑模式、本地化等） |
| [references/swiftui-guides/](references/swiftui-guides/) | 12 份 SwiftUI 最佳实践指南（动画效果、状态管理等内容） |
| [references/ios-app-builder-prompts.md](references/ios-app-builder-prompts.md) | 应用分析、规划及构建过程中的系统提示信息 |

### iOS 开发规范（38 份文档）

涵盖的内容包括：无障碍设计、App Clips 功能、应用审核流程、Apple 提供的翻译服务、生物识别技术、相机使用、颜色对比度设置、组件设计、暗黑模式、设计系统规范、用户反馈机制、文件结构要求、禁止使用的设计模式、基础模型、手势交互、HealthKit 功能、实时活动处理、本地化策略、地图集成、MVVM 架构、导航规则、通知服务、Safari 扩展功能、Siri 指令、布局设计、字体样式、视图复杂性、网站链接处理、Widget 组件等。

### SwiftUI 最佳实践指南（12 份文档）

涵盖动画效果、表单与输入界面设计、布局优化、液态玻璃效果（liquid glass）、列表显示方式、媒体处理、性能优化、滚动效果、状态管理、文本格式化等方面的最佳实践。