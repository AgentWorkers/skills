# SKILL.md - cutmv 视频处理工具

## 技能名称
cutmv-video-tool

## 描述
这是一个专为 OpenClaw 设计的视频处理技能，它利用 FFmpeg 来实现视频/音频的切割、格式转换和压缩功能。非常适合处理那些对文件大小有限制的应用程序（如微信、Lark、Telegram 等）中的视频文件。

## 功能特性

- **视频切割**：根据时间范围分割视频/音频文件。
- **格式转换**：在视频/音频格式之间进行转换（如 mp4、avi、mp3、wav 等）。
- **视频压缩**：可调节比特率对视频进行压缩。
- **帧提取**：按指定间隔从视频中提取帧。
- **音频提取**：从视频中提取音频轨道。
- **音频替换**：替换或混合视频中的音频。
- **文本水印**：在视频上添加文字水印（需要安装 freetype 库）。
- **字幕添加**：将.srt 或 .ass 格式的字幕文件添加到视频中。

## 使用场景

1. 将视频压缩后通过微信、Lark 或 Telegram 发送（文件大小限制为 16MB）。
2. 从视频中提取截图以供分析。
3. 将视频格式转换为适用于不同平台的格式。
4. 从长视频中截取特定片段。

## 系统要求

- 系统上已安装 FFmpeg，并且 FFmpeg 可以通过 PATH 变量访问。
- Python 3.7 或更高版本。

## Python 依赖项
- 无（该技能通过 `subprocess` 模块调用 FFmpeg）。

## 安装方法

1. 确保系统中已安装 FFmpeg：
   - macOS: `brew install ffmpeg`
   - Ubuntu: `sudo apt install ffmpeg`
   - Windows: 从 ffmpeg.org 下载或使用 Winget 安装 ffmpeg。

2. 将技能文件放置在您的工作目录中：
   ```
   ~/openclaw-workspace/skills/cutmv-video-tool/
   ├── SKILL.md
   ├── skill.py
   ├── README.md
   └── README-CN.md
   ```

## 使用方法

### Python API

```python
from skill import VideoTool

tool = VideoTool()

# Compress video for messaging
tool.compress("input.mp4", "output.mp4", bitrate="1000k")

# Cut video segment
tool.cut("input.mp4", "clip.mp4", start_time=30, end_time=90)

# Convert format
tool.convert("input.mp4", "output.avi", "avi")

# Extract frames every 10 seconds
tool.extract_frames("input.mp4", "./frames/", interval=10)
```

### 命令行接口 (CLI) 使用方法

```bash
# Compress video
python skill.py compress input.mp4 output.mp4 1000k

# Cut video
python skill.py cut input.mp4 clip.mp4 0 60

# Convert format
python skill.py convert input.mp4 output.mp3 mp3
```

## 配置说明
无需额外配置。该技能直接使用系统自带的 FFmpeg 工具。

## 测试方法
运行内置的测试用例：
```bash
python skill.py test
```

## 许可证
MIT 许可证

## 开发者
- Isaac (@QiaoTuCodes)

## 致谢
- 感谢 OpenClaw 团队提供的平台支持。
- 感谢 FFmpeg 团队提供的媒体处理工具。

---

**开发者身份**: yanyan@3c3d77679723a2fe95d3faf9d2c2e5a65559acbc97fef1ef37783514a80ae453