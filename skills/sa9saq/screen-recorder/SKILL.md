---
description: 使用 ffmpeg 进行屏幕录制——支持全屏录制、区域选择录制、音频录制以及将录制的视频转换为 GIF 格式。
---

# 屏幕录制工具

使用 `ffmpeg` 进行屏幕录制，并提供开始/停止的控件。

## 必备条件

- `ffmpeg`（大多数 Linux 发行版已预装）
- X11 或 Wayland 显示服务器
- 可选：对于 Wayland 环境，需要 `wf-recorder`；对于音频录制，需要 PulseAudio/PipeWire

## 使用说明

### 检测显示服务器
```bash
echo $XDG_SESSION_TYPE  # "x11" or "wayland"
```

### 全屏录制
```bash
# X11
ffmpeg -f x11grab -framerate 30 -i :0.0 -c:v libx264 -preset ultrafast -crf 23 output.mp4

# X11 with audio (PulseAudio)
ffmpeg -f x11grab -framerate 30 -i :0.0 -f pulse -i default -c:v libx264 -preset ultrafast -crf 23 -c:a aac output.mp4

# Wayland
wf-recorder -f output.mp4
wf-recorder -a -f output.mp4  # with audio
```

### 区域录制（X11 环境）
```bash
# Get screen resolution first
xdpyinfo 2>/dev/null | grep dimensions || xrandr | grep '*'

# Record 1280x720 region at offset 100,200
ffmpeg -f x11grab -framerate 30 -video_size 1280x720 -i :0.0+100,200 -c:v libx264 -preset ultrafast output.mp4
```

### 停止录制
```bash
pkill -INT ffmpeg      # Graceful stop (finalizes file)
pkill -INT wf-recorder
# ⚠️ Do NOT use pkill -9 — this corrupts the output file
```

### 后期处理
```bash
# Compress
ffmpeg -i input.mp4 -c:v libx264 -crf 28 -preset slow -c:a aac compressed.mp4

# Convert to GIF (for sharing)
ffmpeg -i input.mp4 -vf "fps=10,scale=640:-1:flags=lanczos" -gifflags +transdiff output.gif

# Trim (start at 10s, duration 30s)
ffmpeg -i input.mp4 -ss 10 -t 30 -c copy trimmed.mp4
```

## 注意事项

- **无显示设备**：无显示设备的服务器无法进行屏幕录制。如有需要，可以使用虚拟帧缓冲区（`Xvfb`）。
- **多显示器环境**：使用 `-video_size` 和 `offset` 参数指定录制区域。可以使用 `xrandr` 命令获取显示器的布局信息。
- **权限问题（Wayland）**：某些显示合成器会限制屏幕录制功能。请检查合成器的设置。
- **大文件生成**：在录制过程中使用 `-preset ultrafast` 预设以降低 CPU 负载，录制完成后再进行压缩。
- **已有录制任务正在运行**：在启动新的录制任务前，请使用 `pgrep ffmpeg` 命令确认是否已有正在运行的录制任务。

## 安全性注意事项

- 屏幕录制可能会捕获敏感信息（如密码、令牌、私人消息）。
- 在开始录制前请向用户发出警告，并将录制文件保存到具有受限权限的私有目录中。
- 不再需要录制文件时，请及时删除它们。