---
name: transcription
description: 使用 OpenAI Whisper API 对音频和视频文件进行转录。当用户需要转录音频/视频文件、从媒体中提取语音内容或从录音中获取文本时，可以使用该服务。该服务能够自动从视频文件中提取音频内容。
---
# 转录技能

该技能利用 OpenAI Whisper API 提供音频和视频文件的转录功能。

## 快速入门

**请发送音频或视频文件**，我将自动为您进行转录！只需将文件附加到您的消息中即可。

### 手动使用

您也可以直接从命令行运行脚本：

```bash
cd /home/openclaw/.openclaw/workspace/skills/transcription/scripts
python3 transcribe_audio.py inputfile.ogg
```

对于视频文件：
```bash
python3 transcribe_audio.py video.mp4
```

## 支持的格式

**音频：** mp3、wav、mp4、mpeg、mpga、m4a、ogg、webm、flac、aac、wma

**视频：** mp4、mov、avi、mkv（音频会自动提取）

## 使用示例

如何使用 Python 脚本进行转录：

```python
python3 transcribe_audio.py inputfile.ogg
```

## 功能特点

- **根据需要提取时间戳**
- **批量处理**：一次可以发送多个文件
- **支持视频文件**：自动从视频文件中提取音频
- **多种输出格式**：文本、JSON、SRT 字幕、VTT 字幕

## 技术细节

- **API 端点：** `http://192.168.0.11:8080/v1`（本地 Whisper 端点）
- **模型：** whisper-small（默认）
- **确定性结果**：模型输出结果具有较高的可预测性
- **自动转换**：使用 ffmpeg 工具将视频文件转换为音频文件

## 注意事项

- 为获得最佳效果，请确保文件清晰且背景噪音较低
- 语言自动检测功能在大多数情况下都能准确识别语言
- 对于批量处理，请一次发送一个文件，或在请求中指定“batch”参数

---

**脚本：** `scripts/transcribe_audio.py`、`scripts/transcribe_simple.py`
**参考文档：** `references/transcription_guide.md`