---
name: ios-simulator
description: 自动化 iOS 模拟器的工作流程（使用 simctl 和 idb）：创建/启动/删除设备、安装/运行应用程序、推送通知、处理用户隐私设置、截图以及实现基于辅助功能的 UI 导航。适用于与 iOS 应用程序、Xcode、模拟器（Simulator）、simctl、idb 工具、UI 自动化技术或 iOS 测试相关的工作场景。
metadata: {"clawdbot":{"emoji":"📱","os":["darwin"],"requires":{"bins":["xcrun"]},"install":[{"brew":{"formula":"idb-companion","bins":["idb_companion"],"tap":"facebook/fb"}}]}}
---

# iOS模拟器自动化

此技能提供了一个**仅基于Node.js**的命令行工具（CLI），用于执行以下操作：
- 使用 `xcrun simctl` 进行模拟器、设备或应用程序的管理；
- 使用 `idb` 检查**辅助功能树（accessibility-tree）** 并生成模拟用户的输入操作（如点击、输入文本或按钮）。

该工具专为**AI代理**设计：默认输出格式简洁明了，可根据需要提供更详细的输出信息。

## 重要限制

- **必须运行在macOS系统上**，并且需要安装Xcode命令行工具（或Xcode）。
- 如果使用的是ClawdBot网关，需在连接的**macOS节点**上执行这些命令（详见“远程macOS节点”部分）。
- `idb`为可选组件，但用于生成模拟用户操作的详细数据（如点击事件）。请参阅下方安装说明。

## 快速入门

```bash
# 1) Sanity check
node {baseDir}/scripts/ios-sim.mjs health

# 2) List simulators (compact)
node {baseDir}/scripts/ios-sim.mjs list

# 3) Select a default simulator (writes .ios-sim-state.json in the current dir)
node {baseDir}/scripts/ios-sim.mjs select --name "iPhone" --runtime "iOS" --boot

# 4) Install + launch an .app
node {baseDir}/scripts/ios-sim.mjs app install --app path/to/MyApp.app
node {baseDir}/scripts/ios-sim.mjs app launch --bundle-id com.example.MyApp

# 5) Inspect current UI (requires idb)
node {baseDir}/scripts/ios-sim.mjs ui summary
node {baseDir}/scripts/ios-sim.mjs ui tap --query "Log in"
node {baseDir}/scripts/ios-sim.mjs ui type --text "hello world"

# 6) Screenshot
node {baseDir}/scripts/ios-sim.mjs screenshot --out artifacts/screen.png
```

## 远程macOS节点

如果您不在macOS系统上，可以使用ClawdBot的节点执行功能在macOS节点上运行这些命令（例如使用`exec`命令，并指定`host: node`）。请确保目标节点上存在该技能文件夹，或者将其复制到该节点上。

## 输出格式（高效且易于阅读）

- **默认输出**：**单行JSON格式**，包含操作结果的简要总结。
- 使用`--pretty`选项可生成更易阅读的JSON格式输出。
- 使用`--text`选项可获取命令提供的简短人类可读的摘要信息。
- 部分命令（如`ui tree`、`list --full`）会产生大量输出，这些选项为可选。

## 状态与默认UDID

`select`命令会生成一个状态文件（默认路径为`./.ios-sim-state.json`），用于存储当前选择的UDID。所有命令都支持`--udid <UUID>`参数；若未指定UDID，系统会从状态文件中获取当前UDID。

您可以通过以下方式修改状态文件的保存位置：
- `IOS_SIM_STATE_FILE=/path/to/state.json`

## 依赖项说明

### Xcode与simctl的配置
如果`xcrun`无法找到`simctl`，请确保已通过Xcode设置或`xcode-select`工具启用Xcode命令行工具，并执行首次启动时的配置脚本：
- `xcodebuild -runFirstLaunch`

### idb（用于辅助功能自动化）
请安装`idb_companion`及`idb`命令行工具：
```bash
brew tap facebook/fb
brew install idb-companion
python3 -m pip install --upgrade fb-idb
```

## 安全性级别

| 安全级别 | 命令            | 备注                          |
|---------|-----------------|------------------------------|
| SAFE     | `list`, `health`, `boot`, `shutdown`, `screenshot`, `ui *` | 不会修改任何数据                   |
| CAUTION | `privacy *`, `push`, `clipboard *`, `openurl` | 可能会修改模拟器或应用程序的状态           |
| DANGEROUS | `erase`, `delete`       | 需要使用`--yes`参数才能执行这些危险操作         |

## 命令索引

所有命令的完整列表请参见：
```bash
node {baseDir}/scripts/ios-sim.mjs <command> [subcommand] [flags]
```

### 模拟器的基本操作

- `list [--full]`          ：列出所有可用的模拟器或应用程序。
- `select --name <substr> [--runtime <substr>] [--boot]`：选择指定的模拟器或应用程序并启动。
- `boot [--udid <uuid>] [--wait]`    ：启动指定的模拟器。
- `shutdown [--udid <uuid>|--all]`    ：关闭所有模拟器。
- `erase --yes [--udid <uuid>|--all]`    ：删除所有模拟器。
- `delete --yes [--udid <uuid>]    ：删除指定的模拟器。

### 应用程序管理

- `app install --app <path/to/App.app> [--udid ...]`：安装指定的应用程序。
- `app uninstall --bundle-id <id> [--udid ...]`：卸载指定的应用程序。
- `app launch --bundle-id <id> [--udid ...] [-- <args...>]`：启动指定的应用程序。
- `app terminate --bundle-id <id> [--udid ...]`：终止指定的应用程序。
- `app container --bundle-id <id> [--type data|app] [--udid ...]`：管理应用程序的容器。

### 截图与视频录制

- `screenshot --out <file.png> [--udid ...]`：拍摄指定模拟器的截图。
- `record-video --out <file.mp4> [--udid ...]`：录制指定模拟器的视频（持续到按下Ctrl+C为止）。

### 复制粘贴板内容与URL操作

- `clipboard get [--udid ...]`：获取指定模拟器上的剪贴板内容。
- `clipboard set --text <text> [--udid ...]`：将文本设置到指定模拟器的剪贴板。
- `openurl --url <url> [--udid ...]`：在指定模拟器中打开指定的URL。

### 模拟器权限与推送通知

- `privacy grant --bundle-id <id> --service <svc[,svc...]> [--udid ...]`：授予指定应用程序访问特定系统服务的权限。
- `privacy revoke --bundle-id <id> --service <svc[,svc...]> [--udid ...]`：撤销指定应用程序的权限。
- `privacy reset --bundle-id <id> --service <svc[,svc...]> [--udid ...]`：重置指定应用程序的权限设置。
- `push --bundle-id <id> --payload <json-string> [--udid ...]`：向指定模拟器发送推送通知。

### 日志记录

- `logs show [--last 5m] [--predicate <expr>] [--udid ...]`：查看指定模拟器的日志记录（最近5分钟内的记录）。

### 基于辅助功能的UI自动化（需使用idb）

- `ui summary [--limit 12]`：获取模拟器界面的简要信息。
- `ui tree`：获取模拟器界面的完整JSON数据结构。
- `ui find --query <text> [--limit 20]`：查找界面中包含指定文本的元素。
- `ui tap --query <text>`：点击界面中包含指定文本的元素。
- `ui tap --x <num> --y <num>`：在指定坐标位置点击界面元素。
- `ui type --text <text>`：获取指定文本元素的类型信息。
- `ui button --name HOME|LOCK|SIRI|SIDE_BUTTON|APPLE_PAY`：操作模拟器上的按钮。

## 故障排除

请参考：[references/TROUBLESHOOTING.md](references/TROUBLESHOOTING.md)以获取故障排除指南。