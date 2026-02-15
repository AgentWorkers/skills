---
name: macOS
description: macOS系统管理、与Linux的命令行差异以及自动化最佳实践。
metadata:
  category: system
  skills: ["macos", "osx", "apple", "darwin", "terminal"]
---

## BSD 与 GNU 命令的差异

- `sed -i` 需要提供一个扩展参数：`sed -i '' 's/a/b/' file` — 使用空字符串表示不进行备份；Linux 系统中不需要这个参数。
- `find` 命令不支持 `-printf` 选项，应使用 `-exec stat` 或 `xargs` 结合 `stat -f` 来实现相同的功能。
- `date` 命令使用不同的格式化选项：`date -j -f '%Y-%m-%d' '2024-01-15' '+%s'` — 使用 `-j` 可以防止时间被修改。
- `grep -P`（用于 Perl 正则表达式）在 Linux 中不存在，可以使用 `grep -E`（扩展模式）或通过 Homebrew 安装 `ggrep`。
- `xargs` 的默认行为是调用 `/usr/bin/echo`，因此必须明确指定要执行的命令。
- `readlink -f` 命令在 Linux 中不存在，可以使用 `realpath` 或 `python3 -c "import os; print(os.path.realpath('path'))` 来替代。

## Homebrew 的路径配置

- Apple Silicon 硬件：`/opt/homebrew/bin`, `/opt/homebrew/lib`
- Intel 硬件：`/usr/local/bin`, `/usr/local/lib`
- 检查硬件架构：`uname -m` 会显示 `arm64` 或 `x86_64`。
- Homebrew 不会自动将命令添加到系统路径（PATH）中，需要检查 `~/.zprofile` 文件中的相关设置。
- 要运行 64 位版本的二进制文件，可以先执行 `arch -x86_4 /bin/bash`，然后再安装或运行仅适用于 64 位系统的工具。

## Keychain（密钥管理）

- 存储密码：`security add-generic-password -a "$USER" -s "service_name" -w "secret_value" -U`
- 查找密码：`security find-generic-password -a "$USER" -s "service_name" -w`
- 使用 `-U` 选项可以更新已存在的密码条目；不使用该选项会导致重复条目错误。
- Keychain 在首次使用时会提示用户授权，以便后续自动化操作能够正常使用。
- 删除密码：`security delete-generic-password -a "$USER" -s "service_name"`。

## launchd（系统服务管理）

- 用户代理服务：存储在 `~/Library/LaunchAgents/` 目录下，以当前用户身份运行。
- 系统守护进程：存储在 `/Library/LaunchDaemons/` 目录下，以 root 用户身份在系统启动时运行。
- 加载服务：`launchctl load -w ~/Library/LaunchAgents/com.example.plist`
- 修改服务配置前需要先卸载服务：`launchctl unload`
- 检查服务错误：`launchctl list | grep service_name`，然后使用 `launchctl error <exit_code>` 查看错误信息。
- 日志记录：`log show --predicate 'subsystem == "com.example"' --last 1h` 可查看相关服务的日志。

## 隐私权限（TCC）

- 如果没有“全盘访问”或“自动化权限”，自动化脚本会默默失败。
- 可以在系统设置 → 隐私与安全 → 相关类别中授予相应的权限。
- Terminal 和 iTerm 需要分别设置权限；授予其中一个权限并不会自动授予另一个。
- 使用 `tccutil reset` 可以清除权限：`tccutil reset AppleEvents` 可用于重置自动化相关的权限。
- 查看已授予的权限：`sqlite3 ~/Library/Application\ Support/com.apple.TCC/TCC.db "SELECT * FROM access"`。

## 默认偏好设置（defaults）

- 读取偏好设置：`defaults read com.apple.finder AppleShowAllFiles`
- 修改偏好设置：`defaults write com.apple.finder AppleShowAllFiles -bool true`
- 删除偏好设置：`defaults delete com.apple.finder AppleShowAllFiles`
- 修改设置后需要重启应用程序：`killall Finder`
- 查找应用程序的 Bundle ID：`osascript -e 'id of app "App Name"'`
- 导出所有偏好设置：`defaults export com.apple.finder -` 会输出 XML 格式的配置文件。

## 文件操作

- `ditto` 命令会保留文件的资源分叉（resource forks）和元数据，适合用于处理应用程序包（app bundles）的复制。
- 创建 DMG 文件：`hdiutil create -volname "Name" -srcfolder ./folder -format UDZO output.dmg`
- 挂载 DMG 文件：`hdiutil attach image.dmg`（返回挂载点的路径）
- 卸载 DMG 文件：`hdiutil detach /Volumes/Name`
- 查看文件扩展属性：`xattr -l file` 可查看属性列表，`xattr -c file` 可清除所有属性。
- 移除文件的隔离状态：`xattr -d com.apple.quarantine app.app`。

## 剪贴板操作

- 将文本复制到剪贴板：`echo "text" | pbcopy`
- 从剪贴板粘贴内容：`pbpaste`
- 复制文件内容：`pbcopy < file.txt`
- 保留 RTF 格式：`pbpaste -Prefer rtf`
- 剪贴板功能在 SSH 会话中也能正常使用，便于远程文件复制。

## 截图操作

- 将屏幕区域截图并保存到文件：`screencapture -i output.png`
- 截取整个窗口的截图并保存到文件：`screencapture -w output.png`
- 直接将截图复制到剪贴板：`screencapture -c`
- 无界面的截图（不显示界面元素）：`screencapture -x`（会抑制声音和光标显示）
- 录制屏幕画面需要先在隐私设置中启用屏幕录制功能。

## 进程管理

- 使用 `caffeinate` 命令防止系统进入睡眠状态：`caffeinate -i command`（命令执行期间系统保持唤醒状态）
- 设置定时器防止系统进入睡眠状态：`caffeinate -t 3600`（例如，设置 3600 秒后自动唤醒）
- 查看系统为何不进入睡眠状态：`pmset -g assertions`
- 查看电源管理设置：`pmset -g`，`sudo pmset -a sleep 0` 可禁用睡眠功能
- 查找当前处于焦点的应用程序：`osascript -e 'tell application "System Events" to get name of first process whose frontmost is true`。

## 网络配置

- 列出所有网络接口：`networksetup -listallhardwareports`
- 获取 IP 地址：`ipconfig getifaddr en0`（笔记本电脑上通常使用 en0 接口）
- 查看 DNS 服务器：`scutil --dns | grep nameserver`
- 清除 DNS 缓存：`sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder`
- 设置代理：`networksetup -getwebproxy "Wi-Fi"`。

## 系统完整性保护

- 检查系统完整性保护的状态：`csrutil status`
- 可以禁用该功能（仅限恢复模式使用）：`csrutil disable`（不建议在生产环境中使用）
- 受保护的目录包括 `/System`, `/usr`（`/usr/local` 除外），`/sbin`, `/bin`；即使以 root 用户权限也无法修改这些目录。
- 在编写自动化脚本时需要考虑到这些限制。

## 日志记录

- 实时查看日志流：`log stream --predicate 'process == "processname'"
- 查找最近的错误日志：`log show --last 1h --predicate 'eventMessage contains "error'"
- 按子系统过滤日志：`log show --predicate 'subsystem == "com.apple.example'"
- 将日志保存到文件：`log collect --output ./logs.logarchive`（日志文件会在 Console.app 中打开）。

## 自动化技巧

- 打开 URL：`open "https://example.com"`（使用默认浏览器）
- 打开应用程序：`open -a "Safari"`（按应用程序名称打开）
- 使用特定应用程序打开文件：`open -a "TextEdit" file.txt`
- 运行 AppleScript：`osascript -e 'tell application "Finder" to get name of home'`
- 使用 Spotlight 搜索：`mdfind "kMDItemDisplayName == 'filename.txt'"`（对于已索引的文件，这种方式比 `find` 更快）。