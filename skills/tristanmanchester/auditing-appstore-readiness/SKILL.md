---
name: auditing-appstore-readiness
description: 审核 iOS 应用程序仓库（使用 Swift/Xcode 或 React Native/Expo 开发），检查其是否符合 App Store 的发布要求以及是否具备发布准备就绪的状态；生成审核结果报告（分为“通过”、“警告”或“失败”），并生成相应的发布检查清单。
metadata: {"openclaw":{"emoji":"🧾","requires":{"bins":["git"]}}}
---

# 应用商店适配性审核

该工具会审查应用程序仓库，并生成一份适用于提交至 iOS 应用商店（App Store）或 TestFlight 的发布准备报告。

**支持的平台：**
- 原生 iOS 应用（使用 Swift/Obj-C 语言开发，基于 Xcode 项目或工作区）
- React Native 应用（基础版本）
- Expo 应用（无论是托管模式还是预构建版本）

## 快速入门（推荐）

从仓库根目录运行只读审核脚本：

```bash
{ "tool": "exec", "command": "node {baseDir}/scripts/audit.mjs --repo . --format md"
}

# 如果需要 JSON 格式的输出：
{ "tool": "exec", "command": "node {baseDir}/scripts/audit.mjs --repo . --format md --json audit.json"
}
```

如果仓库是单项目仓库，请指定应用程序目录：

```bash
{ "tool": "exec", "command": "node {baseDir}/scripts/audit.mjs --repo apps/mobile --format md"
}
```

## 输出内容结构：

审核结果必包含以下内容：
- **总体评估**：**通过（PASS）** / **警告（WARN）** / **失败（FAIL）**
- 检测到的项目类型及其关键标识信息（如应用包 ID、版本号、构建版本）
- 检查项目存在的问题及其对应的修复步骤
- 开发者可勾选的 **发布检查清单**

**参考文档：** [references/report-template.md](references/report-template.md)

## 安全规则（切勿修改仓库内容）

默认情况下，所有命令均为只读操作。除非用户明确要求，或者修复操作非常简单且不会对仓库造成影响，否则请勿执行任何可能修改仓库内容的命令。

**示例性修改操作：**
- 安装依赖项（`npm i`、`yarn`、`pnpm i`、`pod install`）
- 生成配置文件（`expo prebuild`）
- 自动化签名流程（`fastlane match`）
- 创建应用程序打包文件（`xcodebuild archive`、`eas build`）——这些操作可能会生成新的文件并可能需要签名处理

**注意事项：** 如果必须执行修改仓库内容的命令，请在命令前明确标注为 **“修改操作（MUTATING）”**。

## 主要工作流程：

### 1) 确定仓库类型及项目类型

建议使用脚本 `audit.mjs` 进行自动检测。如需手动检测：
- Expo 应用：`package.json` 文件中包含 `expo` 字样，且存在 `app.json` 或 `app.config.*` 文件
- React Native 应用：`package.json` 文件中包含 `react-native` 字样，且存在 `ios/` 目录
- 原生 iOS 应用：存在 `.xcodeproj` 或 `.xcworkspace` 文件

如果仓库中包含多个应用程序，请选择符合用户需求的那个应用程序；如果没有明确指定，可以选择以下条件的目录：
- 包含 `ios/<AppName>/Info.plist` 文件的目录
- 在仓库根目录附近存在唯一的 `.xcodeproj` 或 `.xcworkspace` 文件

### 2) 运行静态合规性检查（适用于所有情况）

即使没有 Xcode，也请执行以下检查：
- 仓库维护情况：确保没有未提交的敏感信息
- iOS 应用的相关标识信息（如应用包 ID、版本号、构建版本）
- 应用图标（包含适用于 App Store 的 1024×1024 像素图标）
- 启动界面是否存在
- 隐私与权限设置：
  - 是否存在隐私声明文件（`PrivacyInfo.xcprivacy`）
  - 相关权限设置是否正确（如相机、位置、跟踪等功能的权限声明）
- 避免使用过于宽泛的 ATS（Application Transport Security）权限豁免规则（`NSAllowsArbitraryLoads`）
- 第三方 SDK 的合规性：检查相关许可证和隐私声明文件
- 应用商店列表的基本信息：确保仓库的文档或联系信息中包含隐私政策链接

脚本会根据检查结果输出 **通过（PASS）**、**警告（WARN）** 或 **失败（FAIL）**。

### 3) 运行构建准确性检查（仅适用于安装了 Xcode 的环境）

**建议执行顺序：**（此步骤会生成构建文件）
1) 查看 Xcode 及相关 SDK 的版本信息：
   ```bash
   { "tool": "exec", "command": "xcodebuild -version"
   ```

2) 列出项目的工作区配置信息：
   ```bash
   { "tool": "exec", "command": "xcodebuild -list -json -workspace <path>.xcworkspace"
   ```
   或
   ```bash
   { "tool": "exec", "command": "xcodebuild -list -json -project <path>.xcodeproj"
   ```

3) 为模拟器生成可发布的构建文件（此步骤可能涉及签名操作）：
   ```bash
   { "tool": "exec", "command": "xcodebuild -workspace <...> -scheme <...> -configuration Release -sdk iphonesimulator -destination 'platform=iOS Simulator,name=iPhone 15' build"
   ```

**注意：** 如果无法执行构建检查，报告中必须明确说明这一点，并将评估结果标记为 **警告（WARN）**（除非存在明确的失败项）。

### 4) 生成最终报告

- 使用 [references/report-template.md] 作为报告模板
- 根据审核结果给出相应的建议：
  - **失败（FAIL）**：提交前需要修复问题
  - **警告（WARN）**：虽然可以提交，但仍存在风险
  - **通过（PASS）**：已满足提交要求，剩余问题属于行政性处理事项

## 手动检查（脚本无法完全覆盖的部分）

即使自动化检查通过，也请务必执行以下手动检查：
- 应用商店连接（App Store Connect）的相关元数据（如截图、应用描述、关键词、年龄分级、价格信息、分类等）
- 隐私设置是否与实际应用行为一致
- 密钥导出（Export Compliance）的相关设置是否正确
- 内容和知识产权相关问题（如许可证、第三方资源的使用情况、商标信息）
- 账户或地区相关要求（例如欧盟贸易商资格等）

**更多参考文档：** [references/manual-checklist.md](references/manual-checklist.md)

## 当用户要求“使应用符合商店要求”时：

- 确定哪些问题可以在仓库内部安全地修复（例如修改 `Info.plist` 文件中的内容、调整 `PrivacyInfo.xcprivacy` 文件中的设置、优化 ATS 权限配置等）
- 提出必要的修复方案，并使用 `apply_patch` 命令应用修复
- 重新运行 `audit.mjs` 以更新审核报告

## 常用资源：
- 权限设置相关参考：[references/permissions-map.md](references/permissions-map.md)
- Expo 应用专项检查：[references/expo.md](references/expo.md)
- React Native 应用检查：[references/react-native.md](references/react-native.md)
- 原生 iOS 应用检查：[references/native-ios.md](references/native-ios.md)