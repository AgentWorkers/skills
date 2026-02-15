---
name: macos-spm-app-packaging
description: 无需使用 Xcode，即可搭建、构建和打包基于 SwiftPM 的 macOS 应用程序。当您需要从零开始设计 macOS 应用程序的架构、使用 SwiftPM 进行项目管理、自定义 `.app` 包的组装脚本，或者需要在 Xcode 之外完成应用程序的签名、公证或 Appcast 发布流程时，此方法非常适用。
---

# macOS SwiftPM 应用打包（无需 Xcode）

## 概述  
无需使用 Xcode，即可快速搭建一个完整的 SwiftPM macOS 应用框架，然后进行构建、打包并运行该应用。可以使用 `assets/templates/bootstrap/` 作为应用的初始布局模板，以及 `references/packaging.md` 和 `references/release.md` 文件来配置打包和发布的相关信息。

## 两步工作流程  
1) 搭建项目框架：  
   - 将 `assets/templates/bootstrap/` 文件夹复制到新的代码仓库中。  
   - 在 `Package.swift`、`Sources/MyApp/` 文件以及 `version.env` 文件中修改相关名称。  
   - 根据需求自定义 `APP_NAME`、`BUNDLE_ID` 和版本信息。  

2) 构建、打包并运行应用：  
   - 将 `assets/templates/` 目录下的脚本文件复制到你的代码仓库中（例如，放入 `Scripts/` 目录）。  
   - 执行构建和测试命令：`swift build` 和 `swift test`。  
   - 执行打包命令：`Scripts/package_app.sh`。  
   - 运行应用：`Scripts/compile_and_run.sh`（推荐）或 `Scripts/launch.sh`。  
   - 发布应用（可选）：执行 `Scripts/sign-and-notarize.sh` 和 `Scripts/make_appcast.sh` 命令。  
   - 创建 Git 标签并发布到 GitHub（可选）：生成 Git 标签，将应用文件（zip 或 appcast 格式）上传到 GitHub，然后发布应用。  

## 模板文件  
- `assets/templates/package_app.sh`：用于构建二进制文件、创建 `.app` 包、复制资源文件以及为应用签名。  
- `assets/templates/compile_and_run.sh`：用于关闭正在运行的应用、打包并启动应用。  
- `assets/templates/build_icon.sh`：使用 Icon Composer 生成应用图标（需要安装 Xcode）。  
- `assets/templates/sign-and-notarize.sh`：对应用进行签名处理。  
- `assets/templates/make_appcast.sh`：生成用于应用更新的 Sparkle appcast 文件。  
- `assets/templates/setup_dev_signing.sh`：用于设置开发环境的代码签名配置。  
- `assets/templates/launch.sh`：用于运行已打包的应用的简单启动脚本。  
- `assets/templates/version.env`：包含版本信息的配置文件，供打包脚本使用。  
- `assets/templates/bootstrap/`：包含 SwiftPM 应用的基本框架结构（`Package.swift`、`Sources/` 文件夹及 `version.env` 文件）。  

## 注意事项：  
- 请确保权限设置和签名配置明确无误；直接使用提供的模板脚本，避免重复编写代码。  
- 如果不使用 Sparkle 进行应用更新，可以忽略相关步骤。  
- Sparkle 依赖于应用的构建编号（`CFBundleVersion`），因此 `version.env` 文件中的 `BUILD_NUMBER` 需要在每次更新时递增。  
- 对于带有菜单栏的应用，在打包时请设置 `MENU_BAR_APP=1`，以便在 `Info.plist` 中生成相应的菜单栏元素。