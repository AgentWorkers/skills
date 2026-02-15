---
name: swiftui-empty-app-init
description: 使用 XcodeGen 在当前目录下初始化一个简单的 SwiftUI iOS 应用程序，生成一个 `.xcodeproj` 文件（除非有明确要求，否则不生成工作区、包或测试文件）。
---

# SwiftUI 空应用初始化

## 概述
在当前目录下初始化一个简洁的、单目标的 SwiftUI iOS 应用。该项目是通过 **XcodeGen** 生成的，生成一个单独的 `.xcodeproj` 文件，使开发者可以立即开始添加功能。

## 先决条件
- 已安装 Xcode 并通过 `xcode-select` 选择它。
- **XcodeGen** 已添加到系统的 `PATH` 环境变量中。

如果缺少任何先决条件：
- 停止执行当前操作。
- 明确告知用户缺少什么。
- **不要** 尝试使用其他脚手架工具或自动安装方式。

## 输入参数
- **项目名称**（必填）
- **最低 iOS 部署目标**（例如：iOS 12）
- **可选的 Bundle 标识符**（或使用默认值）

## 默认值（无需额外确认即可使用）
- Bundle 标识符默认值：`com.example.<ProjectName>`
- 提供所需输入后，立即开始生成项目（无需额外确认）。

## 核心要求
生成的项目必须满足以下条件：
- 通过 **XcodeGen** 生成（不要手动创建 `project.pbxproj` 文件）。
- 使用一个单独的 `.xcodeproj` 文件（不使用 `.xcworkspace`）。
- 仅包含一个应用目标（app target）。
- 使用 SwiftUI 的 `@main App` 生命周期。
- 包含一个最小的 `ContentView` 占位组件。
- 包含一个最小的 `Info.plist` 文件（避免不必要的键或配置）。
- **不包含任何 Swift 包**。
- 除非特别要求，否则不包含测试目标（test targets）。

## 生成过程
- 使用提供的输入参数创建一个最小的 `project.yml` 文件。
- 使用 XcodeGen 生成 `YourApp.xcodeproj` 文件。
- 确保生成的文件符合所有核心要求。

## 预期结构
- `project.yml`
- `YourApp.xcodeproj`
- `YourApp/`（应用目标的源代码文件）
- 可选的配置文件

项目中不应包含额外的文件夹、包、工作区（workspaces）、脚本或资源文件。

## 最简单的验证步骤
- 确认 `YourApp.xcodeproj` 文件已成功由 XcodeGen 生成。
- 确认默认的方案（scheme）存在（例如，通过简单的方案列表来验证）。
- 除非有明确要求，否则**不要** 启动模拟器、进行构建、安装或运行应用。

## 注意事项
- 保持项目的简洁性，避免添加不必要的组件（如图标、脚本、包或架构相关的文件）。
- 本技能仅用于应用初始化，不涉及功能的搭建或开发。