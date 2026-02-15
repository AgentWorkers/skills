---
name: omarchy
description: "Omarchy为日常系统管理工作提供了操作指南：默认情况下，系统主机被认定为Omarchy；优先选择与Omarchy原生兼容的工作流程；将用户操作意图映射到相应的Omarchy相关封装工具或脚本；避免使用可能与Omarchy行为冲突的通用Linux命令。在处理该主机上的本地系统任务时，除非用户明确指出系统不是Omarchy，否则应始终遵循这些指南。优先使用安全的Omarchy命令，防止使用非Omarchy的快捷方式（例如随意终止或重启进程的操作）；在遇到桌面系统问题时进行故障排查，并在执行脚本前验证其正确性。"
---

# Omarchy 技能指南

请将此技能视为 Omarchy 的一种操作模式，而不仅仅是一个命令目录。在处理 Omarchy 系统时，应优先使用 Omarchy 自带的封装工具和工作流程，而非可能绕过系统状态管理的通用 Linux 命令。请根据本地脚本的文档和名称来选择正确的执行路径。每个脚本的顶部都有关于其用途的说明。在确定脚本的用途之前，请勿直接运行它。

## 操作规则

1. 首先根据命令名称以及 `/home/achals/.local/share/omarchy/bin` 目录下的文件内注释来选择相应的命令。
2. 优先使用只读或状态查询类命令（如 `*list`、`*status`、`*current`、`*available`、`*version`）。
3. 在执行影响范围较大或操作力度较大的命令（如 `*install`、`*remove`、`*reinstall`、`*update`、`*pkg`、`*setup`、`*set`）之前，请先询问确认。
4. 避免批量执行操作；应先进行静态检查。
5. 切勿假设所有以 `omarchy-*` 开头的脚本都支持标准的 CLI 参数（包括 `--help`）。请将每个脚本视为自定义工具，并先查看其文件或头部注释。

## 正确与错误的操作示例

在操作 Omarchy 时，请始终遵循这些规则。目标不是“不惜一切代价地运行命令”，而是避免绕过 Omarchy 设计好的状态管理流程。

### 1) 重启 Waybar

用户意图：“Waybar 出现问题了，需要重启它。”

- 错误做法（使用通用命令）：
  - `pkill waybar && waybar`
- 正确做法（使用 Omarchy 自带命令）：
  - `omarchy-restart-waybar`
- 原因：Omarchy 的封装工具通常能更好地处理环境/会话相关的细节，比简单的 `kill-and-relaunch` 命令更可靠。

### 2) 编辑配置后刷新界面

用户意图：“我修改了配置，需要应用这些更改。”

- 错误做法：
  - 手动重启多个进程直到问题解决
- 正确做法：
  - 使用针对性的刷新脚本，例如 `omarchy-refresh-waybar`、`omarchy-refresh-hyprland`、`omarchy-refresh-config`（根据需要选择具体组件）
- 原因：刷新脚本操作明确且可逆；手动重启可能会导致不必要的干扰和风险。

### 3) 包管理

用户意图：“安装/卸载某个软件包。”

- 错误做法：
  - 直接使用 `pacman` 或 `yay` 而不先检查 Omarchy 的封装工具
- 正确做法：
  - 先使用 `omarchy-pkg-*` 系列命令（如 `...-present`、`...-missing`，然后再执行 `...-install` 或 `...-remove`）
- 原因：封装工具能确保操作符合 Omarchy 的设计规范。

### 4) 更换主题

用户意图：“切换主题或同步应用的主题。”

- 错误做法：
  - 先手动编辑配置文件，然后随机重启应用
- 正确做法：
  - 使用 `omarchy-theme-list` 查看可用主题，然后使用 `omarchy-theme-set` 设置主题，必要时再针对特定应用进行额外设置（如 `omarchy-theme-set-vscode`、`...-browser`、`...-obsidian`）
- 原因：Omarchy 的主题管理流程可能包含额外的集成步骤，不仅仅是简单的配置修改。

### 5) 音频/蓝牙/Wi-Fi 问题

用户意图：“音频/蓝牙/Wi-Fi 出现故障。”

- 错误做法：
  - 随机重启相关进程（如 `killall pipewire`）
- 正确做法：
  - 使用针对性的封装工具重启相关服务（如 `omarchy-restart-pipewire`、`omarchy-restart-bluetooth`、`omarchy-restart-wifi`）
- 原因：这样能减少不必要的影响，并符合 Omarchy 的服务管理模型。

### 6) “应该运行哪个命令？”的查找流程

用户意图：“我的显示系统出问题了，需要修复。”

- 错误做法：
  - 执行多个命令来查找可用选项（如 `for c in omarchy-*; do $c --help; done`)
- 正确做法：
  1. 静态检查 `/home/achals/.local/share/omarchy/bin` 目录下的命令名称。
  2. 阅读脚本顶部的注释以确定可能的解决方案。
  3. 优先使用只读或状态查询类命令。
  4. 提出 1-3 个可能的命令，并在执行影响较大的操作前先询问确认。
- 原因：静态检查更安全、更快捷，且符合不进行批量查询的原则。

### 7) 系统更新

用户意图：“更新系统。”

- 错误做法：
  - 直接执行完整的更新流程而不先检查系统状态
- 正确做法：
  - 先使用 `omarchy-update-available` 检查系统是否支持更新。
  - 确认后，再执行相应的更新命令。
- 原因：分阶段更新可以减少意外故障的风险。

## 决策模板（每次操作前都应遵循）

对于任何 Omarchy 任务，请遵循以下检查步骤：

1. 确定需要处理的组件（如界面、软件包、主题、网络设置等）。
2. 根据名称和脚本头部注释找到对应的 `omarchy-*` 命令。
3. 优先使用只读或状态查询类命令。
4. 使用针对性的 `omarchy-refresh-*` 或 `omarchy-restart-*` 命令，而非简单的重启操作。
5. 在执行影响较大的操作（如安装、卸载、重新安装、更新等）之前，请先询问确认。

## Omarchy 命令目录（本地版本，包含 161 个命令）

### 电池相关命令（2 个）
- `omarchy-battery-monitor`
- `omarchy-battery-remaining`

### 分支管理命令（1 个）
- `omarchy-branch-set`

### 频道管理命令（1 个）
- `omarchy-channel-set`

### 控制台命令（12 个）
- `omarchy-cmd-apple-display-brightness`
- `omarchy-cmd-audio-switch`
- `omarchy-cmd-first-run`
- `omarchy-cmd-missing`
- `omarchy-cmd-present`
- `omarchy-cmd-reboot`
- `omarchy-cmd-screenrecord`
- `omarchy-cmd-screensaver`
- `omarchy-cmd-screenshot`
- `omarchy-cmd-share`
- `omarchy-cmd-shutdown`
- `omarchy-cmd-terminal-cwd`

### 调试命令（1 个）
- `omarchy-debug`

### 开发相关命令（1 个）
- `omarchy-dev-add-migration`

### 硬盘管理命令（3 个）
- `omarchy-drive-info`
- `omarchy-drive-select`
- `omarchy-drive-set-password`

### 字体管理命令（3 个）
- `omarchy-font-current`
- `omarchy-font-list`
- `omarchy-font-set`

### 休眠管理命令（3 个）
- `omarchy-hibernation-available`
- `omarchy-hibernation-remove`
- `omarchy-hibernation-setup`

### 钩子管理命令（1 个）
- `omarchy-hook`

### Hyprland 相关命令（3 个）
- `omarchy-hyprland-window-close-all`
- `omarchy-hyprland-window-pop`
- `omarchy-hyprland-workspace-toggle-gaps`

### 安装相关命令（9 个）
- `omarchy-install-chromium-google-account`
- `omarchy-install-dev-env`
- `omarchy-install-docker-dbs`
- `omarchy-install-dropbox`
- `omarchy-install-steam`
- `omarchy-install-tailscale`
- `omarchy-install-terminal`
- `omarchy-install-vscode`
- `omarchy-install-xbox-controllers`

### 启动相关命令（14 个）
- `omarchy-launch-about`
- `omarchy-launch-audio`
- `omarchy-launch-bluetooth`
- `omarchy-launch-browser`
- `omarchy-launch-editor`
- `omarchy-launch-floating-terminal-with-presentation`
- `omarchy-launch-or-focus`
- `omarchy-launch-or-focus-tui`
- `omarchy-launch-or-focus-webapp`
- `omarchy-launch-screensaver`
- `omarchy-launch-tui`
- `omarchy-launch-walker`
- `omarchy-launch-webapp`
- `omarchy-launch-wifi`

### 锁屏相关命令（1 个）
- `omarchy-lock-screen`

### 菜单管理命令（2 个）
- `omarchy-menu`
- `omarchy-menu-keybindings`

### 迁移相关命令（1 个）
- `omarchy-migrate`

### 通知管理命令（1 个）
- `omarchy-notification-dismiss`

### 包管理命令（9 个）
- `omarchy-pkg-add`
- `omarchy-pkg-aur-accessible`
- `omarchy-pkg-aur-add`
- `omarchy-pkg-aur-install`
- `omarchy-pkg-drop`
- `omarchy-pkg-install`
- `omarchy-pkg-missing`
- `omarchy-pkg-present`
- `omarchy-pkg-remove`

### 电源配置命令（1 个）
- `omarchy-powerprofiles-list`

### 刷新相关命令（14 个）
- `omarchy-refresh-applications`
- `omarchy-refresh-chromium`
- `omarchy-refresh-config`
- `omarchy-refresh-fastfetch`
- `omarchy-refresh-hypridle`
- `omarchy-refresh-hyprland`
- `omarchy-refresh-hyprlock`
- `omarchy-refresh-hyprsunset`
- `omarchy-refresh-limine`
- `omarchy-refresh-pacman`
- `omarchy-refresh-plymouth`
- `omarchy-refresh-swayosd`
- `omarchy-refresh-walker`
- `omarchy-refresh-waybar`

### 重新安装相关命令（4 个）
- `omarchy-reinstall`
- `omarchy-reinstall-configs`
- `omarchy-reinstall-git`
- `omarchy-reinstall-pkgs`

### 卸载相关命令（1 个）
- `omarchy-remove-dev-env`

### 重置相关命令（1 个）
- `omarchy-reset-sudo`

### 重启相关命令（15 个）
- `omarchy-restart-app`
- `omarchy-restart-bluetooth`
- `omarchy-restart-btop`
- `omarchy-restart-hyprctl`
- `omarchy-restart-hypridle`
- `omarchy-restart-hyprsunset`
- `omarchy-restart-mako`
- `omarchy-restart-opencode`
- `omarchy-restart-pipewire`
- `omarchy-restart-swayosd`
- `omarchy-restart-terminal`
- `omarchy-restart-walker`
- `omarchy-restart-waybar`
- `omarchy-restart-wifi`
- `omarchy-restart-xcompose`

### 设置相关命令（3 个）
- `omarchy-setup-dns`
- `omarchy-setup-fido2`
- `omarchy-setup-fingerprint`

### 显示设置相关命令（2 个）
- `omarchy-show-done`
- `omarchy-show-logo`

### 快照相关命令（1 个）
- `omarchy-snapshot`

### 系统状态查询命令（1 个）
- `omarchy-state`

### 主题管理命令（13 个）
- `omarchy-theme-bg-install`
- `omarchy-theme-bg-next`
- `omarchy-theme-current`
- `omarchy-theme-install`
- `omarchy-theme-list`
- `omarchy-theme-remove`
- `omarchy-theme-set`
- `omarchy-theme-set-browser`
- `omarchy-theme-set-gnome`
- `omarchy-theme-set-obsidian`
- `omarchy-theme-set-templates`
- `omarchy-theme-set-vscode`
- `omarchy-theme-update`

### 切换相关命令（5 个）
- `omarchy-toggle-idle`
- `omarchy-toggle-nightlight`
- `omarchy-toggle-screensaver`
- `omarchy-toggle-suspend`
- `omarchy-toggle-waybar`

### 用户界面相关命令（2 个）
- `omarchy-tui-install`
- `omarchy-tui-remove`

### 时区管理命令（1 个）
- `omarchy-tz-select`

### 更新相关命令（14 个）
- `omarchy-update`
- `omarchy-update-analyze-logs`
- `omarchy-update-available`
- `omarchy-update-available-reset`
- `omarchy-update-branch`
- `omarchy-update-confirm`
- `omarchy-update-firmware`
- `omarchy-update-git`
- `omarchy-update-keyring`
- `omarchy-update-perform`
- `omarchy-update-restart`
- `omarchy-update-system-pkgs`
- `omarchy-update-time`
- `omarchy-update-without-idle`

### 上传相关命令（1 个）
- `omarchy-upload-log`

### 版本管理命令（4 个）
- `omarchy-version`
- `omarchy-version-branch`
- `omarchy-version-channel`
- `omarchy-version-pkgs`

### 音频设备管理命令（5 个）
- `omarchy-voxtype-config`
- `omarchy-voxtype-install`
- `omarchy-voxtype-model`
- `omarchy-voxtype-remove`
- `omarchy-voxtype-status`

### Web 应用管理命令（4 个）
- `omarchy-webapp-handler-hey`
- `omarchy-webapp-handler-zoom`
- `omarchy-webapp-install`
- `omarchy-webapp-remove`

### Windows 相关命令（1 个）
- `omarchy-windows-vm`