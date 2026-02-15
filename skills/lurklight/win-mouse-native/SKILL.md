---
name: win-mouse-native
description: 通过 user32.dll 实现对 Windows 的原生鼠标控制（移动、点击、拖动）。当用户要求你在 Windows 上移动鼠标、点击、拖动或自动化指针操作时，可以使用此方法。
---

# Win Mouse Native

在 **Windows** 系统上提供确定性的鼠标控制功能。

## 命令（本地执行）

此 ClawHub 包包含 **文档** 和 **纯文本形式的脚本**（ClawHub 仅支持文本文件）。

安装步骤：
1) 将 `win-mouse.cmd.txt` 保存为 `win-mouse.cmd`
2) 将 `scripts/win-mouse.ps1.txt` 保存为 `scripts/win-mouse.ps1`

然后运行以下命令：
- `win-mouse move <dx> <dy>` （相对坐标）
- `win-mouse abs <x> <y>` （屏幕绝对坐标）
- `win-mouse click left|right|middle` （左键/右键/中键点击）
- `win-mouse down left|right|middle` （左键/右键/中键按下）
- `win-mouse up left|right|middle` （左键/右键/中键释放）

命令返回值：以 JSON 格式输出一行数据。

## OpenClaw 的使用方式

当用户请求移动或点击鼠标时：
1) 如果用户未提供坐标或移动距离，系统会提示用户输入。
2) 使用 `exec` 命令来执行 `win-mouse ...` 命令。
3) 在不确定如何操作时，优先选择简单且可撤销的操作（例如微小的移动或单次点击）。

## 注意事项：
- 仅支持 **Windows** 系统。
- 该工具通过 `user32.dll` 使用 Win32 的 `SetCursorPos` 和 `SendInput` 函数来实现鼠标控制。