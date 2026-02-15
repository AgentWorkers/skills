---
name: winamp
description: 在 Windows（无论是原生系统还是 WSL2）或 Linux（通过 Wine）上控制 Winamp。
metadata:
  moltbot:
    requires:
      bins: ["winamp.exe"]
---

# Winamp 命令行界面（CLI）

使用此技能来控制 Winamp 媒体播放器。

## 可执行文件路径
根据您的环境，Winamp 可执行文件的路径可能会有所不同：
- **Windows（原生系统）：** `C:\Program Files (x86)\Winamp\winamp.exe`
- **WSL2（Windows 宿主环境）：** `/mnt/c/Program Files (x86)/Winamp/winamp.exe`
- **Linux（通过 Wine 运行）：** `wine "C:\Program Files (x86)\Winamp\winamp.exe"`

## 常用命令

### 播放控制
- **播放：** `winamp.exe /PLAY`
- **暂停/恢复播放：** `winamp.exe /PAUSE`
- **停止：** `winamp.exe /STOP`
- **下一首曲目：** `winamp.exe /NEXT`
- **上一首曲目：** `winamp.exe /PREV`

### 管理播放列表
- **播放文件（清空播放队列）：** `winamp.exe "C:\path\to\file.mp3"`
- **将文件/文件夹添加到播放列表：** `winamp.exe /ADD "C:\path\to\file.mp3"`
- **播放播放列表：** `winamp.exe "C:\path\to\playlist.m3u"`

### 高级选项
- **打开新窗口：** `winamp.exe /NEW`（强制打开新窗口）
- **指定特定窗口：** `winamp.exe /CLASS="MyClassName"`（指定要操作的窗口）
- **使用自定义配置文件：** `winamp.exe /INIDIR="C:\path\to\dir"`（使用指定的配置文件）

## 执行注意事项（后台运行）
由于 Winamp 是一个图形界面应用程序，建议将其设置为在后台运行，以防止程序卡顿。命令一旦发送，就会立即执行。

### Moltbot `exec` 的使用方法：
在调用工具时，需要将 `background: true` 参数添加到命令中。

```json
{
  "tool": "exec",
  "command": "\"/mnt/c/Program Files (x86)/Winamp/winamp.exe\" \"C:\\path\\to\\file.mp3\"",
  "background": true
}
```

### 命令行使用方法：
在命令后面添加一个符号 `&`，以便在后台执行该命令。

```bash
"/mnt/c/Program Files (x86)/Winamp/winamp.exe" /PLAY &
```