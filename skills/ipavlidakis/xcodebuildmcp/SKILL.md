---
name: xcodebuildmcp
description: **使用场景：**  
当用户需要通过 Xcode 进行构建、测试、运行应用程序；控制模拟器或设备；实现用户界面自动化；生成截图或视频；查看日志；或使用 XcodeBuildMCP 工具进行 LLDB 调试时，均可使用该功能。该功能还涵盖项目/方案的发现、会话默认设置以及常见的模拟器/设备使用流程。
---

# Xcodebuildmcp

## 概述

使用 xcodebuildmcp 工具集来构建/运行/测试应用程序、管理模拟器/设备、自动化用户界面操作，并捕获日志/屏幕截图。该工具集遵循一个安全、可重复的工作流程：发现项目 → 设置默认参数 → 执行任务 → 验证结果。

## 先决条件与 MCP 设置

使用此工具集的前提是 XcodeBuildMCP 服务器已安装，并且能够被 MCP 客户端访问（例如，工具名称为 `mcp__xcodebuildmcp__build_run_sim`）。如果缺少相关工具，请按照 `references/mcp-setup.md` 中的步骤进行设置（包括所需软件和 MCP 客户端配置信息）。

## 示例命令

- “在最新的模拟器上构建并运行 iOS 应用程序，并截取屏幕截图。”
- “在模拟器上运行单元测试，并共享失败的测试日志。”
- “打开模拟器，进入设置界面，切换到深色模式。”
- “在我的连接的 iPhone 上安装并启动应用程序。”

## 快速入门（常见操作流程）

1) 发现项目和工作区以及相关的方案配置：
   - `mcp__xcodebuildmcp__discover_projs`
   - `mcp__xcodebuildmcp__list_schemes`

2) 设置会话默认参数（以避免后续操作重复输入相同参数）：
   - `mcp__xcodebuildmcp__session-set-defaults`（工作区路径/项目路径、方案名称、模拟器 ID/设备 ID）

3) 执行具体任务：
   - 构建/运行应用程序：`mcp__xcodebuildmcp__build_run_sim` 或 `mcp__xcodebuildmcp__build_run_macos`
   - 运行测试：`mcp__xcodebuildmcp__test_sim` / `mcp__xcodebuildmcp__test_macos` / `mcp__xcodebuildmcp__test_device`

4) 验证结果并收集相关数据：
   - 截取模拟器屏幕截图：`mcp__xcodebuildmcp__screenshot`
   - 捕获模拟器日志：`mcp__xcodebuildmcp__start_sim_log_cap` → `mcp__xcodebuildmcp__stop_sim_log_cap`

## 任务分类

- **构建/运行**：iOS 模拟器、macOS 设备上的应用程序安装
- **测试**：模拟器/macOS 设备上的功能测试
- **模拟器管理**：列出模拟器、启动/擦除模拟器、调整模拟器外观/位置、执行模拟器操作
- **用户界面自动化**：描述用户界面操作（点击、输入、滑动等）
- **日志与调试**：查看模拟器/设备日志、使用 LLDB 进行调试
- **媒体记录**：截取屏幕截图、录制屏幕画面

详细操作步骤和命令模式请参考 `references/workflows.md`。

## 操作规则

- 在执行基于位置的点击、滑动或长按操作之前，务必先调用 `mcp__xcodebuildmcp__describe_ui` 以获取正确的界面元素信息。
- 尽量尽早使用 `mcp__xcodebuildmcp__session-set-defaults` 来设置会话参数，以减少参数输入的复杂性。
- 如果用户未指定目标设备/模拟器，系统会列出所有可用选项供用户选择；或者可以使用 `useLatestOS` 功能自动选择最新版本的操作系统。
- 除非用户明确要求，否则请避免执行可能破坏模拟器或数据的操作（如擦除模拟器或清除数据）。