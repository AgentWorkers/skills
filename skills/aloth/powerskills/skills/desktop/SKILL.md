---
name: powerskills-desktop
description: Windows桌面自动化功能：支持抓取全屏或窗口截图，可以列出、聚焦、最小化或最大化窗口，还可以发送按键输入以及启动应用程序。适用于需要捕获Windows屏幕内容、管理窗口、输入键盘指令或执行程序的场景。
license: MIT
metadata:
  author: aloth
  cli: powerskills
  parent: powerskills
---
# PowerSkills — 桌面自动化

桌面自动化功能包括：截图、窗口管理、按键操作以及应用程序的启动。

## 系统要求

- 支持安装了.NET Framework（System.Windows.Forms、System.Drawing）的Windows系统。

## 可用命令

```powershell
.\powerskills.ps1 desktop <action> [--params]
```

| 命令 | 参数 | 说明 |
|--------|--------|-------------|
| `screenshot` | `--out-file path.png [--window "title"]` | 截取全屏或指定窗口的截图 |
| `windows` | | 列出所有可见窗口的信息（包括标题、进程ID和进程名称） |
| `focus` | `--window "title"` | 将指定窗口置于前台 |
| `minimize` | `--window "title"` | 最小化指定窗口 |
| `maximize` | `--window "title"` | 最大化指定窗口 |
| `keys` | `--keys "{ENTER}" [--window "title"]` | 向指定窗口发送按键输入（使用SendKeys方法） |
| `launch` | `--app notepad [--app-args "file.txt"] [--wait-ms 3000]` | 启动指定应用程序（notepad，可传递参数file.txt；--wait-ms 3000表示等待3秒后再启动） |

## 示例

```powershell
# Full screen screenshot
.\powerskills.ps1 desktop screenshot --out-file screen.png

# Capture a specific window
.\powerskills.ps1 desktop screenshot --out-file outlook.png --window "Outlook"

# List all windows
.\powerskills.ps1 desktop windows

# Focus and type into Notepad
.\powerskills.ps1 desktop focus --window "Notepad"
.\powerskills.ps1 desktop keys --keys "Hello world{ENTER}" --window "Notepad"

# Launch an app
.\powerskills.ps1 desktop launch --app "notepad.exe" --app-args "C:\temp\notes.txt"
```

## SendKeys命令的语法

| 键 | 语法表示 |
|-----|--------|
| Enter | `{ENTER}` |
| Tab | `{TAB}` |
| Escape | `{ESC}` |
| Ctrl+C | `^c` |
| Alt+F4 | `%{F4}` |
| Shift+Tab | `+{TAB}` |

更多详细信息，请参阅[Microsoft SendKeys文档](https://learn.microsoft.com/en-us/dotnet/api/system.windows.forms.sendkeys)。

## 输出字段

### windows
- `title`：窗口的标题
- `pid`：窗口的进程ID
- `process`：窗口所属进程的名称
- `hwnd`：窗口的句柄（窗口的窗口句柄）

### screenshot
- `saved`：截图文件是否保存成功
- `width`：截图的宽度
- `height`：截图的高度
- `window`：（如果执行了窗口截图操作）被截图的窗口名称