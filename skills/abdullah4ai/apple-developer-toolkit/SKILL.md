---
name: apple-developer-toolkit
description: "这是一款集成了三项功能的一体化苹果开发者工具，所有功能都打包在一个统一的二进制文件中。  
**功能一：文档查询**  
- 可在苹果的各个框架、符号文件中搜索文档；  
- 支持查询2014年至2025年期间举办的1,267场WWDC（世界开发者大会）的会议内容；  
- 无需任何认证信息即可使用。  
**功能二：App Store Connect CLI**  
- 提供超过120条命令，涵盖应用程序的构建（查找/等待/上传）、测试（TestFlight）、提交前的验证、签名流程、订阅管理（支持家庭共享）、In-App购买（IAP）、数据分析、Xcode Cloud集成、元数据处理、发布流程监控、用户洞察分析等功能；  
- 需要App Store Connect的API密钥才能使用。  
**功能三：多平台应用程序构建工具**  
- 可使用自然语言生成完整的Swift/SwiftUI应用程序；  
- 具有自动修复代码错误的功能、模拟器启动功能以及交互式聊天模式；  
- 支持将生成的应用程序直接打开在Xcode中编辑；  
- 需要LLM（Large Language Model）的API密钥以及Xcode开发环境；  
- 包含38条iOS开发规范和12份SwiftUI最佳实践指南，涵盖界面设计、状态管理以及现代API的使用方法。  
**适用场景**：  
- 查阅苹果官方API文档；  
- 管理App Store Connect相关事务；  
- 查找WWDC会议资料；  
- 从零开始构建iOS、watchOS、tvOS、macOS或visionOS应用程序。  
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
# Apple 开发者工具包

这个工具包将三个不同的工具整合到一个二进制文件中，每个工具都可以独立运行，并且需要不同的凭证信息。

## 架构

该工具包以一个统一的二进制文件 `appledev` 的形式提供，支持多次调用：

```
appledev build ...    # iOS app builder (SwiftShip)
appledev store ...    # App Store Connect CLI
appledev b ...        # Short alias
appledev s ...        # Short alias
```

一个二进制文件，三个工具，零重复代码。

## 各功能的凭证要求

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

先决条件：Xcode（需安装 iOS 模拟器）、XcodeGen 以及用于代码生成的 LLM API 密钥。

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
| 根据编号查找构建文件 | `appledev store builds find --app "APP_ID" --build-number "42"` |
| 等待构建完成 | `appledev store builds wait --build "BUILD_ID"` |
| 发布 TestFlight 测试版本 | `appledev store publish testflight --app "APP_ID" --ipa "app.ipa" --group "Beta" --wait` |
| 提交应用到 App Store | `appledev store publish appstore --app "APP_ID" --ipa "app.ipa" --submit --confirm --wait` |
| 提交前验证 | `appledev store validate --app "APP_ID" --version-id "VERSION_ID"` |
| 查看证书 | `appledev store certificates list` |
| 查看应用评论 | `appledev store reviews --app "APP_ID" --output table` |
| 更新本地化设置 | `appledev store localizations update --app "APP_ID" --locale "en-US" --name "My App"` |
| 查看销售报告 | `appledev store analytics sales --vendor "VENDOR" --type SALES --subtype SUMMARY --frequency DAILY --date "2024-01-20"` |
| 配置 Xcode Cloud | `appledev store xcode-cloud run --app "APP_ID" --workflow "CI" --branch "main" --wait` |
| 提交文件公证 | `appledev store notarization submit --file ./MyApp.zip --wait` |
| 查看应用状态 | `appledev store status --app "APP_ID" --output table` |
| 获取每周分析数据 | `appledev store insights weekly --app "APP_ID" --source analytics` |
| 下载元数据 | `appledev store metadata pull --app "APP_ID" --version "1.2.3" --dir ./metadata` |
| 生成发布说明 | `appledev store release-notes generate --since-tag "v1.2.2"` |
| 比较本地化设置 | `appledev store diff localizations --app "APP_ID" --path ./metadata` |
| 提名应用 | `appledev store nominations create --app "APP_ID" --name "Launch"` |
| 设置价格区间 | `appledev store pricing price-points --app "APP_ID" --price 0.99` |
| 配置 IAP（家庭共享） | `appledev store iap create --app "APP_ID" --family-sharable` |
| 配置订阅服务（家庭共享） | `appledev store subscriptions create --app "APP_ID" --family-sharable` |

### 环境变量

所有环境变量都是可选的。设置这些变量可以覆盖相应的命令参数。

| 变量 | 说明 |
|----------|-------------|
| `APPSTORE_KEY_ID` | API 密钥 ID |
| `APPSTORE_ISSUER_ID` | API 发行者 ID |
| `APPSTORE_PRIVATE_KEY_PATH` | .p8 密钥文件的路径 |
| `APPSTORE_PRIVATE_KEY` | 私钥字符串 |
| `APPSTORE_PRIVATE_KEY_B64` | 私钥的 Base64 编码形式 |
| `APPSTORE_APP_ID` | 默认应用 ID |
| `APPSTORE_PROFILE` | 默认认证配置 |
| `APPSTORE_DEBUG` | 是否启用调试输出 |
| `APPSTORE_TIMEOUT` | 请求超时时间 |
| `APPSTORE_BYPASS_KEYCHAIN` | 是否跳过系统密钥链 |

## 第3部分：多平台应用构建器

支持 iOS、watchOS、tvOS 和 iPad 平台。可以通过自然语言描述，利用 AI 生成完整的 Swift/SwiftUI 应用程序。

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

| 平台 | 支持情况 |
|----------|--------|
| iOS | 完全支持 |
| iPad | 完全支持 |
| macOS | 支持 |
| watchOS | 支持 |
| tvOS | 支持 |
| visionOS | 支持 |

### 工作原理

1. **分析**：从应用描述中提取应用名称、功能、核心流程和目标平台。
2. **规划**：生成文件级别的构建计划（包括数据模型、导航结构和设计方案）。
3. **构建**：生成 Swift 源代码文件、项目配置文件（project.yml）和资源目录。
4. **修复**：自动编译并修复错误，直到构建成功。
5. **运行**：启动模拟器并运行应用程序。

### 交互式命令

| 命令 | 说明 |
|---------|-------------|
| `/run` | 在模拟器中构建并运行应用程序 |
| `/fix` | 自动修复编译错误 |
| `/open` | 在 Xcode 中打开项目 |
| `/ask [问题]` | 提问关于项目的问题 |
| `/model [名称]` | 切换应用模型（如 sonnet、opus、haiku 等） |
| `/info` | 显示项目信息 |
| `/usage` | 查看令牌使用情况和费用 |

## 钩子（Hooks）

该工具包支持生命周期钩子，用于自动化操作。在构建和存储操作的关键节点，可以执行脚本或发送通知。

### 快速入门

```bash
# Initialize hook system with indie dev template
bash scripts/hook-init.sh --template indie

# Test a hook
bash scripts/hook-runner.sh build.done STATUS=success APP_NAME=MyApp DURATION_SEC=42

# Dry run (preview without executing)
bash scripts/hook-runner.sh --dry-run build.done STATUS=success APP_NAME=MyApp

# Per-project hooks
bash scripts/hook-init.sh --template indie --project
```

### 配置位置

- **全局配置**：`~/.appledev/hooks.yaml`（适用于所有项目）
- **项目级配置**：`.appledev/hooks.yaml`（覆盖全局配置）
- **钩子脚本**：`~/.appledev/hooks/`（可重用的 shell 脚本）
- **日志**：`~/.appledev/hook-logs/`（每日执行日志）

### 模板

通过 `hook-init.sh --template` 可以选择三种模板：

| 模板 | 适用场景 |
|----------|-------|
| `indie` | 独立开发者：使用 Telegram 通知、自动提交 TestFlight 测试 |
| `team` | 团队协作：使用 Slack 和 Telegram、git 标签、更新变更日志 |
| `ci` | 持续集成/持续部署（CI/CD）：记录日志、运行测试、不显示交互式通知 |

### 内置钩子脚本

| 脚本 | 功能 |
|--------|---------|
| `notify-telegram.sh` | 发送 Telegram 通知 |
| `git-tag-release.sh` | 创建并推送 git 标签 |
| `run-swift-tests.sh` | 运行 Swift 测试（使用 SPM 或 Xcode） |
| `generate-changelog.sh` | 从 git 历史记录生成变更日志 |

### 事件目录

共有 42 个事件，分为 4 个类别：构建（13 个）、存储（20 个）、文档（4 个）和管道（5 个）。完整参考文档：[references/hooks-reference.md](references/hooks-reference.md)

### 代理集成

当通过技能（skill）执行 `appledev` 命令时，完成后会触发相应的钩子事件：

```bash
# After appledev build completes
bash scripts/hook-runner.sh build.done STATUS=success APP_NAME=AppName DURATION_SEC=30

# After store upload
bash scripts/hook-runner.sh store.upload.done STATUS=success APP_ID=123 BUILD_NUMBER=42
```

## 参考资料

- [references/app-store-connect.md](references/app-store-connect.md)：完整的 App Store Connect CLI 命令参考 |
- [references/ios-rules/](references/ios-rules/)：38 条 iOS 开发规则 |
- [references/swiftui-guides/](references/swiftui-guides/)：12 份 SwiftUI 最佳实践指南 |
- [references/ios-app-builder-prompts.md](references/ios-app-builder-prompts.md)：应用构建时的系统提示信息 |

### iOS 开发规则（38 份文档）

包括可访问性、应用剪辑、应用审核、生物识别、相机功能、图表显示、颜色对比度、组件使用、暗黑模式设置、设计系统、反馈机制、文件结构、禁用模式、基础模型、手势识别、健康数据管理、实时活动记录、本地化设置、地图功能、MVVM 架构、导航模式、通知服务、Safari 扩展、分享功能、Siri 指令、布局间距、语音交互、存储策略、代码规范、文本格式、视图组合方式、网站链接等方面的规则。

### SwiftUI 指南（12 份文档）

涵盖动画效果、表单与输入界面、布局设计、液态玻璃效果（liquid-glass layout）、列表显示方式、媒体处理、现代 API 使用、导航系统、性能优化、滚动效果、状态管理、文本格式化等方面的指南。