---
name: apple-developer-toolkit
description: "完整的苹果开发者工具包：包含文档搜索功能、2014-2025年的WWDC视频、App Store Connect管理工具（支持TestFlight、应用程序构建、签名、数据分析以及订阅服务），以及一个集成了50条SwiftUI/iOS最佳实践指南的自动化iOS应用程序构建工具。  
**适用场景**：当用户需要查询苹果API相关信息、查找开发文档、管理App Store Connect账户、根据应用程序描述构建iOS应用程序或搜索WWDC会议内容时使用。  
**不适用场景**：非苹果平台相关的开发工作，或与苹果技术无关的通用编程任务。"
metadata: {"clawdbot":{"emoji":"🍎"}}
---
# Apple 开发者工具包

一个工具包中包含三项核心功能：文档搜索、App Store Connect 管理以及自主构建 iOS 应用程序。

## 设置

所有所需的二进制文件均已包含在内，无需额外安装任何外部组件。

```bash
# Binaries are in bin/ directory
export PATH="$SKILL_DIR/bin:$PATH"
```

对于 App Store Connect，需要进行身份验证：
```bash
appstore auth login --name "MyApp" --key-id "KEY_ID" --issuer-id "ISSUER_ID" --private-key /path/to/AuthKey.p8
```

## 第一部分：文档搜索

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

## 第二部分：App Store Connect

完整参考文档：[references/app-store-connect.md](references/app-store-connect.md)

| 任务 | 命令 |
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

该工具包涵盖的功能包括：TestFlight 测试、应用程序构建、签名流程、订阅服务、In-App Purchase (IAP)、应用分析、财务管理、Xcode Cloud、应用公证、Game Center 集成、Webhook 功能、App Clips 的使用、截图生成、工作流自动化以及应用程序迁移（支持 Fastlane 工具）。

## 第三部分：iOS 应用构建器

能够根据自然语言描述自动生成完整的 iOS 应用程序。

```bash
swiftship              # Interactive mode
swiftship setup        # Install prerequisites (Xcode, XcodeGen, Claude Code)
swiftship fix          # Auto-fix build errors
swiftship run          # Build and launch in simulator
swiftship info         # Show project status
swiftship usage        # Token usage and cost
```

### 工作原理

1. **分析**：从描述中提取应用程序的名称、主要功能及核心业务流程。
2. **规划**：生成详细的文件级构建方案（包括数据模型、导航结构及用户界面设计）。
3. **构建**：生成 Swift 源代码文件及项目配置文件（`project.yml`）。
4. **修复错误**：自动编译并修复代码中的问题，直到构建成功。
5. **运行**：启动 iOS 模拟器并运行应用程序。

### 交互式命令

| 命令 | 功能描述 |
|---------|-------------|
| `/run` | 在模拟器中构建并运行应用程序 |
| `/fix` | 自动修复编译错误 |
| `/open` | 在 Xcode 中打开项目 |
| `/model [name]` | 切换应用程序的界面类型（如 sonnet、opus、haiku 等） |
| `/info` | 显示项目相关信息 |
| `/usage` | 查看令牌的使用情况与费用信息 |

## 参考资料

| 参考文档 | 内容 |
|-----------|---------|
| [references/app-store-connect.md](references/app-store-connect.md) | 完整的 App Store Connect 命令行接口参考 |
| [references/ios-rules/](references/ios-rules/) | 38 条 iOS 开发规范（涵盖无障碍设计、暗黑模式、本地化等主题） |
| [references/swiftui-guides/](references/swiftui-guides/) | 12 份 SwiftUI 开发最佳实践指南（包括动画效果、界面设计等） |
| [references/ios-app-builder-prompts.md](references/ios-app-builder-prompts.md) | 应用分析、规划及构建过程中的系统提示信息 |

### iOS 开发规范（38 份文档）

- 无障碍设计（accessibility）
- App Clips 功能
- 应用评论处理（app_review）
- 生物识别技术（biometrics）
- 相机功能（camera）
- 图表显示（charts）
- 色彩对比度设置（color_contrast）
- 应用组件（components）
- 暗黑模式（dark_mode）
- 设计系统规范（design-system）
- 用户反馈处理（feedback_states）
- 文件结构要求（file-structure）
- 禁用某些设计模式（forbidden-patterns）
- Foundation 框架相关内容（foundation_models）
- 手势交互（gestures）
- HealthKit 健康数据管理（healthkit）
- 动态内容展示（live_activities）
- 本地化支持（localization）
- 地图功能（maps）
- MVVM 架构（mvvm-architecture）
- 导航系统（navigation-patterns）
- 通知服务（notification_service）
- 通知系统（notifications）
- Safari 扩展功能（safari_extension）
- Siri 意图处理（siri_intents）
- 布局间距调整（spacing_layout）
- 语音交互（speech）
- 存储管理（storage-patterns）
- Swift 编程规范（swift-conventions）
- 布局复杂性管理（view-complexity）
- 网站链接处理（website_links）
- 控件组件（widgets）

### SwiftUI 最佳实践指南（12 份文档）

- 动画效果（animations）
- 表单与输入界面（forms-and-input）
- 布局设计（layout）
- 动态界面效果（liquid-glass）
- 列表显示方式（list-patterns）
- 媒体处理（media）
- 现代化 API 设计（modern-apis）
- 导航系统优化（navigation）
- 性能优化（performance）
- 滚动效果（scroll-patterns）
- 状态管理（state-management）
- 文本格式化（text-formatting）