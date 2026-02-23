---
name: apple-developer-toolkit
description: "这是一款集成了三项功能的苹果开发者工具包，所有工具都打包在一个统一的二进制文件中。  
**功能1：文档搜索**  
- 可在苹果的各个框架、符号文件中搜索文档；  
- 支持查询2014年至2025年期间举办的1,267场WWDC（世界开发者大会）的会议资料；  
- 无需任何登录凭证即可使用。  
**功能2：App Store Connect CLI**  
- 提供超过120条命令，涵盖应用构建、TestFlight测试、提交审核、应用签名、订阅管理、IAP（In-App Purchase）功能、数据分析、Xcode Cloud集成、元数据处理、发布流程监控、用户行为分析、回购促销策略、产品页面优化、开发者提名、可访问性设置、预购管理、定价设置等功能；  
- 需要App Store Connect的API密钥才能使用。  
**功能3：iOS应用构建工具**  
- 可根据自然语言描述自动生成完整的Swift/SwiftUI应用程序；  
- 具有自动代码修复功能，并支持在模拟器上运行测试；  
- 需要LLM（Large Language Model）的API密钥以及Xcode开发环境；  
- 包含38条iOS开发规范和12份SwiftUI最佳实践指南，涵盖界面设计、导航逻辑、状态管理以及现代API的使用方法。  
**使用场景**：  
- 查阅苹果官方API文档；  
- 管理App Store Connect相关事务；  
- 查找WWDC会议资料；  
- 从零开始构建iOS应用程序。  
**不适用场景**：  
- 非苹果平台的相关开发工作；  
- 通用编程任务。"
metadata:
  {
    "openclaw":
      {
        "emoji": "🍎",
        "requires":
          {
            "bins": ["node"],
            "anyBins": ["appledev", "appstore", "swiftship"],
          },
        "install":
          [
            {
              "id": "appledev",
              "kind": "brew",
              "tap": "Abdullah4AI/tap",
              "formula": "appledev",
              "bins": ["appledev", "appstore", "swiftship"],
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
                  "description": "LLM API key for code generation. Required only for iOS App Builder. swiftship supports multiple AI backends.",
                },
              ],
          },
      },
  }
---
# Apple 开发者工具包

这个工具包将三个不同的工具整合到了一个二进制文件中。每个工具都可以独立运行，且对所需的凭证（credentials）有不同的要求。

## 架构

该工具包以一个统一的二进制文件 `appledev` 的形式提供，支持多次调用：

```
appledev build ...    # iOS app builder (SwiftShip)
appledev store ...    # App Store Connect CLI
appledev b ...        # Short alias
appledev s ...        # Short alias
```

`appstore` 和 `swiftship` 这两个符号链接（symlinks）确保了向后兼容性。同一个二进制文件，没有任何重复代码。

## 各功能所需的凭证

| 功能 | 所需凭证 | 是否需要设置 |
|---------|-------------------|-------------------|
| 文档搜索（第1部分） | 无 | 是 |
| App Store Connect（第2部分） | App Store Connect API 密钥（.p8格式） | 否 |
| iOS 应用构建器（第3部分） | LLM API 密钥 + Xcode | 否 |

## 设置

### 第1部分：文档搜索（无需设置）

可以直接使用 Node.js 运行：

```bash
node cli.js search "NavigationStack"
```

### 第2部分：App Store Connect CLI

通过 Homebrew 安装：

```bash
brew tap Abdullah4AI/tap && brew install appledev
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

API 密钥可以在 [https://appstoreconnect.apple.com/access/integrations/api](https://appstoreconnect.apple.com/access/integrations/api) 上生成。

### 第3部分：iOS 应用构建器

**先决条件**：需要安装 Xcode（以及 iOS 模拟器）、XcodeGen，并且需要一个 LLM API 密钥用于代码生成。

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

| 任务 | 命令 |
|------|---------|
| 列出应用 | `appledev store apps` |
| 上传构建文件 | `appledev store builds upload --app "APP_ID" --ipa "app.ipa" --wait` |
| 发布 TestFlight 测试版本 | `appledev store publish testflight --app "APP_ID" --ipa "app.ipa" --group "Beta" --wait` |
| 提交到 App Store | `appledev store publish appstore --app "APP_ID" --ipa "app.ipa" --submit --confirm --wait` |
| 查看证书 | `appledev store certificates list` |
| 查看应用评论 | `appledev store reviews --app "APP_ID" --output table` |
| 查看销售报告 | `appledev store analytics sales --vendor "VENDOR" --type SALES --subtype SUMMARY --frequency DAILY --date "2024-01-20"` |
| 使用 Xcode Cloud | `appledev store xcode-cloud run --app "APP_ID" --workflow "CI" --branch "main" --wait` |
| 提交应用公证文件 | `appledev store notarization submit --file ./MyApp.zip --wait` |
| 验证应用 | `appledev store validate --app "APP_ID" --version-id "VERSION_ID" --strict` |
| 查看应用状态 | `appledev store status --app "APP_ID" --output table` |
| 获取每周分析报告 | `appledev store insights weekly --app "APP_ID" --source analytics` |
| 下载应用元数据 | `appledev store metadata pull --app "APP_ID" --version "1.2.3" --dir ./metadata` |
| 生成应用发布说明 | `appledev store release-notes generate --since-tag "v1.2.2"` |
| 比较本地化文件 | `appledev store diff localizations --app "APP_ID" --path ./metadata` |
| 提交应用提名 | `appledev store nominations create --app "APP_ID" --name "Launch"` |

### 环境变量

所有环境变量都是可选的。设置这些变量可以覆盖相应的命令参数。

| 变量 | 描述 |
|----------|-------------|
| `APPSTORE_KEY_ID` | API 密钥 ID |
| `APPSTORE_ISSUER_ID` | API 发行者 ID |
| `APPSTORE_PRIVATE_KEY_PATH` | .p8 密钥文件的路径 |
| `APPSTORE_PRIVATE_KEY` | 私钥的原始字符串 |
| `APPSTORE_PRIVATE_KEY_B64` | 私钥的 Base64 编码形式 |
| `APPSTORE_APP_ID` | 默认应用 ID |
| `APPSTORE_PROFILE` | 默认的身份验证配置文件 |
| `APPSTORE_DEBUG` | 是否启用调试输出 |
| `APPSTORE_TIMEOUT` | 请求超时时间 |
| `APPSTORE_BYPASS_KEYCHAIN` | 是否跳过系统的密钥链检查 |

## 第3部分：iOS 应用构建器

```bash
appledev build                     # Interactive mode
appledev build setup               # Install prerequisites
appledev build fix                 # Auto-fix build errors
appledev build run                 # Build and launch in simulator
appledev build info                # Show project status
appledev build usage               # Token usage and cost
```

### 工作原理

1. **分析**：从应用描述中提取应用名称、功能及核心业务流程。
2. **规划**：生成文件级别的构建计划（包括数据模型、导航结构、设计文档）。
3. **构建**：生成 Swift 源代码文件、项目配置文件（project.yml）以及资源目录。
4. **修复**：自动编译并修复错误，直到构建成功。
5. **运行**：启动 iOS 模拟器并运行应用。

### 交互式命令

| 命令 | 描述 |
|---------|-------------|
| `/run` | 在模拟器中构建并运行应用 |
| `/fix` | 自动修复编译错误 |
| `/open` | 在 Xcode 中打开项目 |
| `/model [name]` | 切换应用模型（如 sonnet、opus、haiku 等） |
| `/info` | 显示项目信息 |
| `/usage` | 查看令牌的使用情况与费用信息 |

## 参考资料

| 参考文档 | 内容 |
|-----------|---------|
| [references/app-store-connect.md](references/app-store-connect.md) | 完整的 App Store Connect CLI 命令列表 |
| [references/ios-rules/](references/ios-rules/) | 38 条 iOS 开发规则 |
| [references/swiftui-guides/](references/swiftui-guides/) | 12 份 SwiftUI 最佳实践指南 |
| [references/ios-app-builder-prompts.md](references/ios-app-builder-prompts.md) | 应用构建时的系统提示信息 |

### iOS 开发规则（38 份文档）

包括：无障碍设计、应用剪辑、应用审核、生物识别技术、摄像头功能、颜色对比度设置、组件使用、暗黑模式、设计系统规范、用户反馈机制、文件结构要求、禁止使用的设计模式、基础模型设计、手势交互、健康数据管理、实时活动功能、本地化处理、地图集成、MVVM 架构、导航设计规范、通知服务、通知功能、Safari 扩展程序、分享功能、Siri 指令、布局间距设置、语音交互、存储管理规范、代码编写规范、视图组合规则、视图复杂性要求、网站链接处理、小部件设计等。

### SwiftUI 指南（12 份文档）

涵盖动画效果、表单与输入界面设计、布局布局、液态玻璃效果（liquid-glass layout）、列表显示方式、媒体处理、现代 API 设计、导航系统、性能优化、滚动效果、状态管理、文本格式化等方面的内容。