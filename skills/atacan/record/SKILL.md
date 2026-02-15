---
name: record
description: 这是一个用于macOS的命令行工具，支持从终端录制音频（通过麦克风）、屏幕视频/截图以及摄像头视频/照片。用户或AI代理可以通过该工具执行以下操作：  
1. 录制麦克风音频；  
2. 捕获屏幕视频或截图；  
3. 捕获摄像头视频或照片；  
4. 列出可用的设备、显示器和摄像头；  
5. 完成任何涉及音频/视频/图像捕获的任务。  

该工具可通过以下关键词触发：  
record, microphone, screen capture, screenshot, screen recording, camera, webcam, photo, audio capture.
---

# record CLI

这是一个适用于 macOS 的命令行工具，用于录制音频、屏幕画面以及摄像头输出。该工具既适用于人类用户，也适用于在终端中运行的 AI 代理。

输出文件路径会打印到 **stdout**，状态信息则会输出到 **stderr**，这使得该工具能够方便地集成到自动化工作流程中。

## 重要提示：需要用户同意

**在运行任何录制命令之前，务必先获得用户的明确许可。** 录制音频（通过麦克风）、屏幕画面或摄像头内容会捕获敏感数据，因此用户可能会感到不适或意外。在执行 `record audio`、`record screen` 或 `record camera` 命令之前，请务必确认用户是否同意进行录制、具体要录制的内容以及录制时长。虽然 `--list-devices`、`--list-displays`、`--list-windows`、`--list-cameras` 等命令对用户的影响较小，但在未获得明确许可的情况下也应先征得用户同意，`--screenshot` 命令同样如此。

## 安装

```bash
brew install atacan/tap/record
```

## 快速参考

```bash
# Audio
record audio --duration 10                    # Record 10s of audio
record audio --duration 5 --json              # JSON output with file path

# Screen
record screen --duration 5                    # Record screen for 5s
record screen --screenshot                    # Take a screenshot
record screen --screenshot --output /tmp/s.png

# Camera
record camera --duration 5                    # Record webcam for 5s
record camera --photo                         # Take a photo
```

## 子命令

| 子命令 | 功能 |
|---|---|
| `record audio` | 通过麦克风录制音频 |
| `record screen` | 录制屏幕视频或截取屏幕截图 |
| `record camera` | 通过网络摄像头录制视频或拍照 |

每个子命令都带有 `--help` 标志，可显示详细的选项信息。

## AI 代理的关键使用技巧

### 获取输出文件路径

该工具会将输出文件路径打印到 stdout。你可以将其保存下来：

```bash
FILE=$(record audio --duration 5)
echo "Recorded to: $FILE"
```

### 使用 `--json` 以结构化格式输出数据

所有子命令都支持 `--json` 选项，可将输出数据以机器可读的 JSON 格式输出到 stdout：

```bash
record audio --duration 5 --json
```

### 使用 `--duration` 实现非交互式录制

如果不使用 `--duration`，工具会一直等待用户按键来停止录制（这需要使用真正的 TTY 环境）。AI 代理应始终使用 `--duration <seconds>` 选项来确保命令能够按时终止。

### 列出可用设备

```bash
record audio --list-devices
record screen --list-displays
record screen --list-windows
record camera --list-cameras
```

使用 `--json` 选项可获取结构化的设备列表。

### 控制输出文件的位置

```bash
record audio --duration 5 --output /tmp/recording.m4a
record screen --screenshot --output /tmp/screen.png --overwrite
```

如果不指定 `--output` 参数，文件将保存在临时目录中。

### 录制包含音频的屏幕画面

```bash
record screen --duration 10 --audio system    # system audio only
record screen --duration 10 --audio mic       # microphone only
record screen --duration 10 --audio both      # system + mic
```

### 捕获特定窗口或显示内容

```bash
record screen --screenshot --window "Safari"
record screen --duration 5 --display primary
```

## macOS 权限要求

终端应用程序（如 Terminal、iTerm2 等）必须在 **系统设置 > 隐私与安全** 中启用以下权限：

- **麦克风**：用于 `record audio` 和 `record camera --audio` 命令 |
- **屏幕录制**：用于 `record screen` 命令 |
- **摄像头**：用于 `record camera` 命令 |

## 故障排除

如果命令执行失败或行为异常，请尝试运行以下命令：

```bash
record <subcommand> --help
```

`--help` 输出的内容会显示当前安装的版本信息，是获取官方使用说明的权威来源。

## 详细命令参考

有关完整的选项列表和高级使用方法，请参阅：

- **音频录制**：[references/audio.md](references/audio.md)
- **屏幕录制**：[references/screen.md](references/screen.md)
- **摄像头录制**：[references/camera.md](references/camera.md)