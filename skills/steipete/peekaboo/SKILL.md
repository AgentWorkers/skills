---
name: peekaboo
description: 使用 Peekaboo CLI 捕获并自动化 macOS 的用户界面（UI）操作。
homepage: https://peekaboo.boo
metadata: {"clawdbot":{"emoji":"👀","os":["darwin"],"requires":{"bins":["peekaboo"]},"install":[{"id":"brew","kind":"brew","formula":"steipete/tap/peekaboo","bins":["peekaboo"],"label":"Install Peekaboo (brew)"}]}}
---

# Peekaboo

Peekaboo 是一个全面的 macOS UI 自动化命令行工具（CLI），支持捕获/检查屏幕图像、定位 UI 元素、模拟用户输入以及管理应用程序、窗口和菜单。所有命令都会使用一个快照缓存，并支持使用 `--json` 或 `-j` 选项进行脚本编写。运行 `peekaboo` 或 `peekaboo <cmd> --help` 可查看命令参数；`peekaboo --version` 可输出工具的构建元数据。建议通过 `polter peekaboo` 命令来确保使用的是最新版本的 Peekaboo。

## 主要功能（仅包含 CLI 功能，不包含代理/MCP 功能）

### 核心功能
- `bridge`：检查与 Peekaboo Bridge 服务器的连接状态
- `capture`：实时捕获屏幕图像或视频，并提取指定区域的帧
- `clean`：清理快照缓存和临时文件
- `config`：初始化、显示、编辑或验证配置信息（包括提供者、模型和凭据）
- `image`：捕获屏幕截图（包括整个屏幕、特定窗口或菜单栏区域）
- `learn`：打印完整的用户手册和工具目录
- `list`：列出所有应用程序、窗口、屏幕和菜单项
- `permissions`：检查屏幕录制和辅助功能的启用状态
- `run`：执行 `.peekaboo.json` 格式的脚本
- `sleep`：暂停当前操作一段时间
- `tools`：列出所有可用的工具，并提供筛选和显示选项

### 交互功能
- `click`：根据 ID、坐标或智能等待机制点击目标元素
- `drag`：在元素、坐标或 Dock 上执行拖放操作
- `hotkey`：组合使用快捷键（如 `cmd, shift, t`）
- `move`：移动光标，支持平滑移动效果
- `paste`：将内容复制到剪贴板或从剪贴板粘贴
- `press`：模拟连续按下的按键序列
- `scroll`：实现方向性滚动（支持平滑滚动效果）
- `swipe`：通过手势在目标元素之间进行滑动操作
- `type`：模拟文本输入，并可设置输入延迟

### 系统管理功能
- `app`：启动、退出、重新启动、隐藏或切换应用程序
- `clipboard`：读写剪贴板内容（文本、图片或文件）
- `dialog`：与系统对话框进行交互（点击、输入等操作）
- `dock`：操作 Dock 上的图标（如点击、右键点击、显示或隐藏）
- `menu`：列出并点击应用程序菜单及菜单项
- `menubar`：列出并点击状态栏中的菜单项
- `open`：以指定应用程序为目标执行打开操作，并可传递 JSON 数据
- `space`：在多个工作空间之间切换或移动窗口
- `visualizer`：提供直观的视觉反馈效果
- `window`：关闭、最小化、最大化、移动、调整窗口大小或列出所有窗口

### 其他功能
- `see`：查看带有注释的 UI 图谱，并可查看快照的 ID；支持可选的分析功能

## 全局运行参数
- `--json` 或 `-j`：以 JSON 格式输出结果
- `--verbose` 或 `-v`：增加输出详细程度
- `--log-level <level>`：设置日志记录的详细级别
- `--no-remote`：禁用远程连接功能
- `--bridge-socket <path>`：指定与 Peekaboo Bridge 服务器的连接地址

## 快速入门示例
```bash
peekaboo permissions
peekaboo list apps --json
peekaboo see --annotate --path /tmp/peekaboo-see.png
peekaboo click --on B1
peekaboo type "Hello" --return
```

## 常用定位参数（适用于大多数交互命令）
- 应用程序/窗口：`--app`, `--pid`, `--window-title`, `--window-id`, `--window-index`
- 快照定位：`--snapshot`（使用 `see` 命令获取的快照 ID；默认使用最新快照）
- 元素/坐标：`--on`/`--id`（元素 ID），`--coords x,y`
- 聚焦控制：`--no-auto-focus`, `--space-switch`, `--bring-to-current-space`, `--focus-timeout-seconds`, `--focus-retry-count`

## 常用捕获参数
- 输出格式：`--path`（输出路径），`--format png|jpg`（输出格式），`--retina`（是否输出高分辨率图像）
- 定位方式：`--mode screen`/`window`/`frontmost`（定位目标类型），`--screen-index`（窗口索引），`--window-title`（窗口标题），`--window-id`（窗口 ID）
- 分析选项：`--analyze "prompt"`（执行分析操作），`--annotate`（添加注释）
- 捕获引擎：`--capture-engine auto`/`classic`/`cg`/`modern`/`sckit`（选择不同的捕获引擎）

## 常用操作参数
- 时间控制：`--duration`（拖动/滑动操作的持续时间），`--steps`（拖动/滑动操作的步数），`--delay`（按键输入的延迟）
- 动作模拟：`--profile human`（模拟人类操作），`--wpm`（输入速度，单位：字/分钟）
- 滚动设置：`--direction up`/`down`/`left`/`right`（滚动方向），`--amount <ticks>`（滚动距离），`--smooth`（滚动效果）

## 示例用法
- **查看屏幕 -> 点击元素 -> 输入文本**（最常用的操作流程）：```bash
peekaboo see --app Safari --window-title "Login" --annotate --path /tmp/see.png
peekaboo click --on B3 --app Safari
peekaboo type "user@example.com" --app Safari
peekaboo press tab --count 1 --app Safari
peekaboo type "supersecret" --app Safari --return
```
- **根据窗口 ID 定位元素**：```bash
peekaboo list windows --app "Visual Studio Code" --json
peekaboo click --window-id 12345 --coords 120,160
peekaboo type "Hello from Peekaboo" --window-id 12345
```
- **捕获屏幕截图并进行分析**：```bash
peekaboo image --mode screen --screen-index 0 --retina --path /tmp/screen.png
peekaboo image --app Safari --window-title "Dashboard" --analyze "Summarize KPIs"
peekaboo see --mode screen --screen-index 0 --analyze "Summarize the dashboard"
```
- **实时捕获屏幕图像（支持动态操作）**：```bash
peekaboo capture live --mode region --region 100,100,800,600 --duration 30 \
  --active-fps 8 --idle-fps 2 --highlight-changes --path /tmp/capture
```
- **管理应用程序和窗口**：```bash
peekaboo app launch "Safari" --open https://example.com
peekaboo window focus --app Safari --window-title "Example"
peekaboo window set-bounds --app Safari --x 50 --y 50 --width 1200 --height 800
peekaboo app quit --app Safari
```
- **操作菜单、菜单栏和 Dock**：```bash
peekaboo menu click --app Safari --item "New Window"
peekaboo menu click --app TextEdit --path "Format > Font > Show Fonts"
peekaboo menu click-extra --title "WiFi"
peekaboo dock launch Safari
peekaboo menubar list --json
```
- **模拟鼠标操作和手势输入**：```bash
peekaboo move 500,300 --smooth
peekaboo drag --from B1 --to T2
peekaboo swipe --from-coords 100,500 --to-coords 100,200 --duration 800
peekaboo scroll --direction down --amount 6 --smooth
```
- **模拟键盘输入**：```bash
peekaboo hotkey --keys "cmd,shift,t"
peekaboo press escape
peekaboo type "Line 1\nLine 2" --delay 10
```

**注意事项**
- 使用该工具需要具备屏幕录制和辅助功能的权限。
- 建议在使用 `click` 命令之前，先使用 `peekaboo see --annotate` 命令来识别目标元素。