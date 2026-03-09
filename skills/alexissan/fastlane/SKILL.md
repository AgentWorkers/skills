---
name: fastlane
emoji: "\U0001F680"
requires: fastlane
install: brew install fastlane
description: iOS/macOS 应用自动化：通过 CLI 进行构建、签名、上传至 TestFlight 以及发布到 App Store
---
# Fastlane

Fastlane 是一个自动化工具，可以用于执行 iOS 和 macOS 应用的构建、代码签名、TestFlight 分发以及 App Store 提交等任务——所有这些操作都可以通过简单的 CLI 命令来完成，无需使用 Fastfile。

---

## 验证安装

```bash
fastlane --version
```

如果尚未安装：

```bash
brew install fastlane
```

或者通过 RubyGems 安装：

```bash
sudo gem install fastlane -NV
```

安装完成后，请将 Fastlane 添加到您的 shell 配置文件中：

```bash
export PATH="$HOME/.fastlane/bin:$PATH"
```

---

## 认证

### 使用 App Store Connect API 密钥（推荐）

API 密钥可以避免 2FA 验证，是自动化和持续集成（CI）的推荐方式。

1. 在 [App Store Connect → Users and Access → Keys](https://appstoreconnect.apple.com/access/api) 生成密钥。
2. 下载 `.p8` 文件。
3. 设置环境变量：

```bash
export APP_STORE_CONNECT_API_KEY_KEY_ID="XXXXXXXXXX"
export APP_STORE_CONNECT_API_KEY_ISSUER_ID="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
export APP_STORE_CONNECT_API_KEY_KEY_FILEPATH="/path/to/AuthKey_XXXXXXXXXX.p8"
```

或者将密钥以 JSON 格式直接传递：

```bash
export APP_STORE_CONNECT_API_KEY_KEY='{"key_id":"XXXXXXXXXX","issuer_id":"xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx","key_filepath":"/path/to/AuthKey.p8"}'
```

> **提示：** 始终优先使用 API 密钥进行认证。只有在用户明确表示没有 API 密钥访问权限时，才使用 Apple ID 进行认证。

### 使用 Apple ID 作为备用方案

```bash
export FASTLANE_USER="user@example.com"
export FASTLANE_PASSWORD="app-specific-password"
```

在 [appleid.apple.com](https://appleid.apple.com) 生成一个与应用相关的密码。如果启用了 2FA，您可能还需要：

```bash
export FASTLANE_APPLE_APPLICATION_SPECIFIC_PASSWORD="xxxx-xxxx-xxxx-xxxx"
export SPACESHIP_2FA_SMS_DEFAULT_PHONE_NUMBER="+1 (xxx) xxx-xxxx"
```

### 环境变量 — 认证相关配置

| 变量 | 用途 |
|---|---|
| `APP_STORE_CONNECT_API_KEY_KEY_ID` | 来自 App Store Connect 的 API 密钥 ID |
| `APP_STORE_CONNECT_API_KEY_ISSUER_ID` | 来自 App Store Connect 的发行者 ID |
| `APP_STORE_CONNECT_API_KEY_KEY_FILEPATH` | `.p8` 私钥文件的路径 |
| `APP_STORE_CONNECT_API_KEY_KEY` | 包含所有密钥字段的 JSON 字符串 |
| `FASTLANE_USER` | Apple ID 电子邮件 |
| `FASTLANE_PASSWORD` | Apple ID 密码或应用专用密码 |
| `FASTLANE_APPLE_APPLICATION_SPECIFIC_PASSWORD` | 用于 2FA 账户的应用专用密码 |
| `MATCH_PASSWORD` | 用于匹配证书仓库的加密密码 |
| `MATCH_GIT_URL` | 匹配证书仓库的 Git URL |

---

## 单次执行任务

Fastlane 的各种操作可以直接通过 CLI 命令执行，无需 Fastfile：

```bash
fastlane run <action_name> key:value key2:value2
```

查看可用的操作：

```bash
fastlane actions                    # List all actions
fastlane action <action_name>      # Show details for one action
fastlane search_actions <query>    # Search by keyword
```

> **提示：** 对于一次性任务，使用 `fastlane run <操作名称>` 命令。以下每个部分都同时展示了简写命令和对应的 `fastlane run` 命令。

---

## pilot（TestFlight）

### 将构建文件上传到 TestFlight

```bash
fastlane pilot upload --ipa "/path/to/App.ipa"
```

等效命令：

```bash
fastlane run upload_to_testflight ipa:"/path/to/App.ipa"
```

使用 API 密钥时：

```bash
fastlane pilot upload \
  --ipa "/path/to/App.ipa" \
  --api_key_path "/path/to/api_key.json"
```

### 列出所有构建结果

```bash
fastlane pilot builds
```

### 管理测试人员

```bash
# Add a tester
fastlane pilot add email:"tester@example.com" group_name:"Beta Testers"

# Remove a tester
fastlane pilot remove email:"tester@example.com"

# List testers
fastlane pilot list
```

### 分发给外部测试人员

```bash
fastlane pilot distribute \
  --build_number "42" \
  --groups "External Beta" \
  --changelog "Bug fixes and performance improvements"
```

### 常用的 pilot 命令参数

| 参数 | 用途 |
|---|---|
| `--ipa` | IPA 文件的路径 |
| `--app_identifier` | 应用包 ID（例如：`com.example.app`） |
| `--skip_waiting_for_build_processing` | 不等待 Apple 的处理结果 |
| `--distribute_external` | 发送给外部测试人员 |
| `--groups` | 测试人员组名称（用逗号分隔） |
| `--changelog` | 要测试的内容 |
| `--beta_app_review_info` | 包含审核信息的 JSON 数据 |

---

## deliver（App Store）

### 向 App Store 提交应用

```bash
fastlane deliver --ipa "/path/to/App.ipa" --submit_for_review
```

等效命令：

```bash
fastlane run upload_to_app_store ipa:"/path/to/App.ipa" submit_for_review:true
```

### 仅上传元数据

```bash
fastlane deliver --skip_binary_upload --skip_screenshots
```

### 仅上传截图

```bash
fastlane deliver --skip_binary_upload --skip_metadata
```

### 下载现有的元数据

```bash
fastlane deliver download_metadata --app_identifier "com.example.app"
```

### 下载现有的截图

```bash
fastlane deliver download_screenshots --app_identifier "com.example.app"
```

### 常用的 deliver 命令参数

| 参数 | 用途 |
|---|---|
| `--ipa` | IPA 文件的路径 |
| `--pkg` | macOS 应用的 PKG 文件路径 |
| `--app_identifier` | 应用包 ID |
| `--submit_for_review` | 上传后自动提交审核 |
| `--automatic_release` | 审核通过后自动发布 |
| `--force` | 跳过 HTML 预览验证 |
| `--skip_binary_upload` | 仅上传元数据和截图 |
| `--skip_metadata` | 仅上传二进制文件和截图 |
| `--skip_screenshots` | 仅上传二进制文件或元数据 |
| `--metadata_path` | 元数据文件夹的路径 |
| `--screenshots_path` | 截图文件夹的路径 |
| `--phased_release` | 启用分阶段发布 |
| `--reject_if_possible` | 在上传前拒绝当前版本 |

---

## gym / build_app（构建）

### 构建 IPA 文件

```bash
fastlane gym \
  --workspace "App.xcworkspace" \
  --scheme "App" \
  --export_method "app-store" \
  --output_directory "./build"
```

等效命令：

```bash
fastlane run build_app \
  workspace:"App.xcworkspace" \
  scheme:"App" \
  export_method:"app-store" \
  output_directory:"./build"
```

### 使用 Xcode 项目构建（无需工作区）

```bash
fastlane gym \
  --project "App.xcodeproj" \
  --scheme "App" \
  --export_method "app-store"
```

### 导出方法

| 方法 | 用途 |
|---|---|
| `app-store` | 用于 App Store 和 TestFlight 提交 |
| `ad-hoc` | 通过配置文件直接在设备上安装应用 |
| `development` | 为已注册的设备构建调试版本 |
| `enterprise` | 用于企业内部的发布 |
| `developer-id` | 用于 macOS 的非 App Store 发布 |
| `mac-application` | 用于 macOS App Store 的发布 |
| `validation` | 仅进行验证，不生成可执行文件 |

### 常用的 gym 命令参数

| 参数 | 用途 |
|---|---|
| `--workspace` | `.xcworkspace` 文件的路径 |
| `--project` | `.xcodeproj` 文件的路径 |
| `--scheme` | 构建方案 |
| `--configuration` | 构建配置（调试/发布模式） |
| `--export_method` | 查看导出方法 |
| `--output_directory` | 保存 IPA 文件的路径 |
| `--output_name` | 自定义 IPA 文件名 |
| `--clean` | 构建前清理项目 |
| `--include_bitcode` | 包含二进制代码 |
| `--include_symbols` | 包含 dSYM 符号 |
| `--xcargs` | 额外的 xcodebuild 参数 |
| `--derived_data_path` | 自定义的 DerivedData 文件路径 |
| `--catalyst_platform` | 对于 Catalyst 应用，指定平台（`macos` 或 `ios`） |

> **提示：** 如果项目使用了 `.xcworkspace`（例如：CocoaPods 或 SPM），请务必使用 `--workspace` 参数。只有在没有 `.xcworkspace` 时才使用 `--project` 参数。

---

## match（代码签名）

从共享的 Git 仓库或云存储中同步证书和配置文件。

### 为 App Store 同步证书和配置文件

```bash
fastlane match appstore --app_identifier "com.example.app"
```

等效命令：

```bash
fastlane run sync_code_signing type:"appstore" app_identifier:"com.example.app"
```

### 为开发环境同步证书和配置文件

```bash
fastlane match development --app_identifier "com.example.app"
```

### 为 Ad Hoc 环境同步证书和配置文件

```bash
fastlane match adhoc --app_identifier "com.example.app"
```

### 读取模式（持续集成使用）

```bash
fastlane match appstore --readonly --app_identifier "com.example.app"
```

> **提示：** 在持续集成（CI）服务器上始终使用 `--readonly` 参数。这样可以防止意外创建新证书并影响团队工作。

### Nuke（清除所有证书）

```bash
# Remove all certificates and profiles for a type
fastlane match nuke appstore
fastlane match nuke development
```

> **警告：** `Nuke` 命令具有破坏性且不可撤销。在执行前请务必获得用户确认。

### 常用的 match 命令参数

| 参数 | 用途 |
|---|---|
| `--type` | `appstore`、`development`、`adhoc`、`enterprise` |
| `--app_identifier` | 应用包 ID（多个应用包 ID 用逗号分隔） |
| `--git_url` | 证书的 Git 仓库 URL |
| `--readonly` | 不创建新的证书/配置文件 |
| `--force` | 更新现有的配置文件 |
| `--team_id` | Apple 开发者团队 ID |
| `--storage_mode` | 证书存储方式（`git`、`google_cloud`、`s3`） |
| `--verbose` | 显示详细输出 |

> **提示：** 对于团队来说，建议使用 `match` 命令，因为它可以集中管理证书签名过程，避免出现“在我的机器上可以正常工作”的问题。

---

## scan / run_tests（测试）

### 运行测试

```bash
fastlane scan \
  --workspace "App.xcworkspace" \
  --scheme "AppTests" \
  --device "iPhone 16 Pro"
```

等效命令：

```bash
fastlane run run_tests \
  workspace:"App.xcworkspace" \
  scheme:"AppTests" \
  device:"iPhone 16 Pro"
```

### 在多台设备上运行测试

```bash
fastlane scan \
  --workspace "App.xcworkspace" \
  --scheme "AppTests" \
  --devices "iPhone 16 Pro,iPad Pro (13-inch) (M4)"
```

### 输出格式

```bash
fastlane scan \
  --scheme "AppTests" \
  --output_types "html,junit" \
  --output_directory "./test_results"
```

### 常用的 scan 命令参数

| 参数 | 用途 |
|---|---|
| `--workspace` | `.xcworkspace` 文件的路径 |
| `--project` | `.xcodeproj` 文件的路径 |
| `--scheme` | 测试方案 |
| `--device` | 测试使用的模拟器名称 |
| `--devices` | 多个模拟器（用逗号分隔） |
| `--output_types` | 输出格式（`html`、`junit`、`json`） |
| `--output_directory` | 保存测试结果的路径 |
| `--code_coverage` | 启用代码覆盖率检查 |
| `--clean` | 测试前清理项目 |
| `--fail_build` | 测试失败时终止构建（默认值：`true`） |
| `--xcargs` | 额外的 xcodebuild 参数 |
| `--result_bundle` | 生成 Xcode 测试结果文件 |

---

## snapshot（截图）

自动捕获 App Store 应用的截图（支持多种设备和语言）。

### 拍摄截图

```bash
fastlane snapshot \
  --workspace "App.xcworkspace" \
  --scheme "AppUITests" \
  --devices "iPhone 16 Pro Max,iPhone SE (3rd generation),iPad Pro (13-inch) (M4)" \
  --languages "en-US,es-ES,fr-FR" \
  --output_directory "./screenshots"
```

等效命令：

```bash
fastlane run capture_screenshots \
  workspace:"App.xcworkspace" \
  scheme:"AppUITests" \
  devices:"iPhone 16 Pro Max,iPhone SE (3rd generation),iPad Pro (13-inch) (M4)" \
  languages:"en-US,es-ES,fr-FR" \
  output_directory:"./screenshots"
```

### 常用的 snapshot 命令参数

| 参数 | 用途 |
|---|---|
| `--workspace` | `.xcworkspace` 文件的路径 |
| `--scheme` | 包含截图生成的测试方案 |
| `--devices` | 使用的模拟器名称（用逗号分隔） |
| `--languages` | 需要捕获的本地化语言代码（用逗号分隔） |
| `--output_directory` | 保存截图的路径 |
| `--clear_previous_screenshots` | 在捕获新截图前清除之前的截图 |
| `--stop_after_first_error` | 在遇到第一个错误时停止操作 |
| `--override_status_bar` | 自定义状态栏显示内容（例如：9:41、电池电量满格） |

---

## cert + sigh（证书和配置文件管理）

用于单独管理证书和配置文件。

### 创建/获取证书

```bash
fastlane cert --development
fastlane cert  # Distribution certificate by default
```

等效命令：

```bash
fastlane run get_certificates development:true
```

### 创建/获取配置文件

```bash
# App Store profile
fastlane sigh --app_identifier "com.example.app"

# Development profile
fastlane sigh --development --app_identifier "com.example.app"

# Ad hoc profile
fastlane sigh --adhoc --app_identifier "com.example.app"
```

等效命令：

```bash
fastlane run get_provisioning_profile app_identifier:"com.example.app"
```

### 修复配置文件

```bash
fastlane sigh repair
```

### 常用的命令参数

| 参数 | 用途 |
|---|---|
| `--development` | 开发环境用的证书/配置文件 |
| `--adhoc` | Ad Hoc 环境用的配置文件 |
| `--app_identifier` | 应用包 ID |
| `--team_id` | 开发者团队 ID |
| `--output_path` | 保存配置文件的路径 |
| `--force` | 即使现有配置文件有效也强制更新 |
| `--readonly` | 仅获取配置文件，不创建新文件 |

> **提示：** 对于单个开发者来说，`cert + sigh` 命令也可以使用。但对于团队来说，建议使用 `match` 命令，因为它可以避免证书冲突。

---

## precheck（验证）

在提交应用之前验证元数据，以避免 App Store 审核被拒绝。

```bash
fastlane precheck --app_identifier "com.example.app"
```

等效命令：

```bash
fastlane run check_app_store_metadata app_identifier:"com.example.app"
```

### 需要验证的内容包括：
- 元数据中的无效 URL
- 提及的其他平台（如 Android 等）
- 不适当的文本或内容
- 占位符文本
- 版权日期的准确性

---

## pem（推送通知证书）

生成用于 APNs 的推送通知证书。

```bash
fastlane pem --app_identifier "com.example.app" --output_path "./certs"
```

等效命令：

```bash
fastlane run get_push_certificate app_identifier:"com.example.app" output_path:"./certs"
```

### 常用的 pem 命令参数

| 参数 | 用途 |
|---|---|
| `--app_identifier` | 应用包 ID |
| `--output_path` | 证书保存路径 |
| `--development` | 开发环境用的推送证书 |
| `--generate_p12` | 同时生成 `.p12` 文件 |
| `--p12_password` | `.p12` 文件的密码 |
| `--force` | 即使现有证书有效也强制生成新证书 |
| `--team_id` | 开发者团队 ID |

> **提示：** 对于使用基于令牌的 APNs（`.p8` 密钥）的项目，`pem` 命令是多余的。只有在使用基于证书的 APNs 时才需要使用 `pem` 命令。

---

## frameit（添加截图边框和标题）

为 App Store 提交的截图添加设备边框和标题。

```bash
fastlane frameit --path "./screenshots"
```

添加标题的命令：

```bash
fastlane frameit silver --path "./screenshots"
```

等效命令：

```bash
fastlane run frame_screenshots path:"./screenshots"
```

`Framefile.json` 文件用于控制截图中的标题、字体和颜色设置。

---

## 常见的工作流程

### 构建并上传到 TestFlight

```bash
fastlane gym \
  --workspace "App.xcworkspace" \
  --scheme "App" \
  --export_method "app-store" \
  --output_directory "./build" && \
fastlane pilot upload \
  --ipa "./build/App.ipa" \
  --changelog "Latest build from CI"
```

### 构建并提交到 App Store

```bash
fastlane gym \
  --workspace "App.xcworkspace" \
  --scheme "App" \
  --export_method "app-store" \
  --output_directory "./build" && \
fastlane deliver \
  --ipa "./build/App.ipa" \
  --submit_for_review \
  --automatic_release \
  --force
```

### 同步签名配置文件并构建应用，然后上传

```bash
fastlane match appstore \
  --app_identifier "com.example.app" \
  --readonly && \
fastlane gym \
  --workspace "App.xcworkspace" \
  --scheme "App" \
  --export_method "app-store" \
  --output_directory "./build" && \
fastlane pilot upload \
  --ipa "./build/App.ipa"
```

### 进行测试并构建应用，然后上传

```bash
fastlane scan \
  --workspace "App.xcworkspace" \
  --scheme "AppTests" && \
fastlane gym \
  --workspace "App.xcworkspace" \
  --scheme "App" \
  --export_method "app-store" \
  --output_directory "./build" && \
fastlane pilot upload \
  --ipa "./build/App.ipa"
```

### 拍摄截图并添加边框，然后上传

```bash
fastlane snapshot \
  --workspace "App.xcworkspace" \
  --scheme "AppUITests" \
  --output_directory "./screenshots" && \
fastlane frameit silver --path "./screenshots" && \
fastlane deliver --skip_binary_upload --skip_metadata
```

---

## 环境变量

### 通用参数

| 变量 | 用途 |
|---|---|
| `FASTLANE_XCODEBUILD_SETTINGS_TIMEOUT` | xcodebuild 的超时时间（秒） |
| `FASTLANE_XCODEBUILD_SETTINGS_RETRIES` | xcodebuild 的重试次数 |
| `FASTLANE_OPT_OUT_USAGE` | 设置为 `YES` 以禁用分析功能 |
| `FL_OUTPUT_DIR` | 默认的输出目录 |
| `FASTLANE_SKIP_UPDATE_CHECK` | 跳过更新提示 |
| `FASTLANE_HIDE_TIMESTAMP` | 隐藏日志时间戳 |
| `FASTLANE_DISABLE_colors` | 禁用彩色输出 |

### 适用于持续集成（CI）的参数

| 参数 | 用途 |
|---|---|
| `CI` | 在持续集成环境中设置为 `true` |
| `FASTLANE_DONT_STORE_PASSWORD` | 不将密码保存到钥匙链 |
| `MATCH_KEYCHAIN_NAME` | 用于持续集成的钥匙链名称 |
| `MATCH_KEYCHAIN_PASSWORD` | 用于持续集成的钥匙链密码 |

### 适用于 Xcode 的参数

| 参数 | 用途 |
|---|---|
| `GYMWORKSPACE` | 默认的工作区路径 |
| `GYM_SCHEME` | 默认的构建方案 |
| `GYM_OUTPUT_directory` | 默认的输出目录 |
| `GYM_EXPORT_METHOD` | 默认的导出方法 |
| `SCANWORKSPACE` | 默认的测试工作区 |
| `SCAN_SCHEME` | 默认的测试方案 |
| `SCAN_DEVICE` | 默认的测试设备 |

---

## 注意事项

### CLI 命令语法规则

- 所有的 `fastlane run` 命令参数都使用 `key:value` 的格式（不允许使用破折号或等号）。
- 工具的简写命令（如 `fastlane gym`、`fastlane pilot`）使用 `--key value` 或 `--key "value` 的格式。
- 布尔参数：在 `fastlane run` 命令中使用 `true`/`false`，在简写命令中使用 `--flag` 或 `no flag`。
- 数组参数：使用逗号分隔的字符串（例如：`devices:"iPhone 16,iPad Pro"`）。
- 包含空格的路径必须用引号括起来。

### 错误处理

- **会话过期：** 使用 `fastlane spaceauth -u user@example.com` 重新认证，或刷新 API 密钥。
- **代码签名错误：** 运行 `fastlane match` 同步证书信息，或使用 `security find-identity -v -p codesigning` 验证本地证书。
- **“找不到应用”：** 确保 `app_identifier` 与 App Store Connect 中注册的应用包 ID 一致。
- **上传超时：** 设置 `FASTLANE_XCODEBUILD_SETTINGS_TIMEOUT=120` 并重试。
- **配置文件不匹配：** 运行 `fastlane sigh repair` 或使用 `--force` 参数更新配置文件。

### 给操作员的建议

- 当用户请求“部署”或“发布”iOS应用时，通常的操作流程是：先使用 `match`（签名）命令，然后使用 `gym`（构建）命令，接着使用 `pilot`（TestFlight）或 `deliver`（App Store）命令。
- 如果用户提供了 Fastfile，请按照文件中的命令格式执行操作。但对于一次性任务，始终使用 CLI 命令。
- 在使用 `.xcodeproj` 文件之前，请先检查是否存在 `.xcworkspace` 文件。可以使用 `ls *.xcworkspace` 命令进行验证。
- 在持续集成环境中，使用 `--readonly` 参数，并设置 `CI=true` 环境变量。
- 如果不确定应该使用哪个命令，可以运行 `fastlane actions` 或 `fastlane search_actions <关键词>` 来查找合适的命令。