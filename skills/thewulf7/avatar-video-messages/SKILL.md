---
name: video-message
description: 生成并发送带有唇形同步功能的 VRM（Virtual Reality Model）头像的视频消息。适用于用户请求视频消息、头像视频、视频回复的情况，或者当文本转语音（TTS）需要以视频形式而非音频形式呈现时。
metadata:
  {
    "openclaw":
      {
        "emoji": "🎥",
        "requires": { "bins": ["ffmpeg", "avatarcam"] },
        "install":
          [
            {
              "id": "npm",
              "kind": "npm",
              "package": "@thewulf7/openclaw-avatarcam",
              "global": true,
              "bins": ["avatarcam"],
              "label": "Install avatarcam (npm)",
            },
            {
              "id": "brew",
              "kind": "brew",
              "formula": "ffmpeg",
              "bins": ["ffmpeg"],
              "label": "Install ffmpeg (brew)",
            },
            {
              "id": "apt",
              "kind": "apt",
              "packages": ["xvfb", "xauth"],
              "label": "Install headless X dependencies (Linux only)",
            },
          ],
      },
  }
---

# 视频消息

可以将文本或音频转换为头像视频消息，并以 Telegram 视频便签的形式发送（圆形格式）。

## 安装

```bash
npm install -g openclaw-avatarcam
```

## 配置

在 `TOOLS.md` 文件中进行配置：

```markdown
### Video Message (avatarcam)
- avatar: default.vrm
- background: #00FF00
```

### 设置参考

| 设置 | 默认值 | 说明 |
|---------|---------|-------------|
| `avatar` | `default.vrm` | VRM 头像文件路径 |
| `background` | `#00FF00` | 颜色（十六进制）或图片路径 |

## 先决条件

### 系统依赖

| 平台 | 命令 |
|----------|---------|
| **macOS** | `brew install ffmpeg` |
| **Linux** | `sudo apt-get install -y xvfb xauth ffmpeg` |
| **Windows** | 安装 ffmpeg 并将其添加到 PATH 环境变量中 |
| **Docker** | 请参阅下面的 Docker 部分 |

> **注意：** macOS 和 Windows 不需要 `xvfb`，因为它们具有原生显示支持。

### Docker 用户
将以下内容添加到 `OPENCLAW_DOCKER_APT_PACKAGES` 文件中：
```
build-essential procps curl file git ca-certificates xvfb xauth libgbm1 libxss1 libatk1.0-0 libatk-bridge2.0-0 libgdk-pixbuf2.0-0 libgtk-3-0 libasound2 libnss3 ffmpeg
```

## 使用方法

使用 OpenClaw 的 `message` 工具，并通过 `asVideoNote` 参数发送视频消息：

```
message action=send filePath=/tmp/video.mp4 asVideoNote=true
```

## 工作流程

1. 从 `TOOLS.md` 文件中读取配置（头像和背景设置）。
2. 如果提供了文本，使用 `tts` 命令生成音频文件：`tts text="..."` → 生成音频文件路径。
3. 运行 `avatarcam` 工具，使用生成的音频和配置文件生成 MP4 视频文件。
4. 通过 `message action=send filePath=... asVideoNote=true` 将视频文件作为视频便签发送。
5. 发送完成后返回 `NO_REPLY`。

## 示例流程

用户：**“给我发送一条说‘hello’的视频消息”。**

```bash
# 1. TTS
tts text="Hello! How are you today?" → /tmp/voice.mp3

# 2. Generate video
avatarcam --audio /tmp/voice.mp3 --output /tmp/video.mp4 --background "#00FF00"

# 3. Send as video note
message action=send filePath=/tmp/video.mp4 asVideoNote=true

# 4. Reply
NO_REPLY
```

## 技术细节

| 设置 | 值 |
|---------|-------|
| 分辨率 | 384x384（正方形） |
| 帧率 | 30 帧/秒（恒定） |
| 最大时长 | 60 秒 |
| 视频编码格式 | H.264（libx264） |
| 音频编码格式 | AAC |
| 质量 | CRF 18（高质量） |
| 容器格式 | MP4 |

### 处理流程

1. Electron 在 1280x720 分辨率下渲染 VRM 头像，并实现唇形同步。
2. 使用 `canvascaptureStream(30)` 功能捕获视频流。
3. FFmpeg 对视频流进行处理：裁剪、调整帧率、缩放并编码。
4. 使用 OpenClaw 的 `message` 工具通过 Telegram 的 `sendVideoNote` API 发送视频消息。

## 平台支持

| 平台 | 显示方式 | 备注 |
|----------|---------|-------|
| macOS | 原生 Quartz 显示引擎 | 无需额外依赖 |
| Linux | 使用 `xvfb`（无头模式） | 需安装 `xvfb` |
| Windows | 原生显示引擎 | 无需额外依赖 |

## 无头环境渲染

`avatarcam` 会自动检测无头环境：
- 如果 `$DISPLAY` 环境变量未设置，会使用 `xvfb-run` 进行渲染（仅限 Linux）。
- macOS 和 Windows 使用原生显示引擎。
- 可以忽略 GPU 相关的延迟警告。
- 生成视频的时间约为实际时间的 1.5 倍（20 秒的音频处理时间约为 30 秒）。

## 其他注意事项

- 配置信息从 `TOOLS.md` 文件中读取。
- 发送完成后请删除临时文件：`rm /tmp/video*.mp4`。
- 如果需要发送普通视频（非圆形格式），请省略 `asVideoNote=true` 参数。