---
name: audio-processing
description: 音频的采集、分析、转换以及生成（包括转录、文本到语音（TTS）功能、语音活动检测（VAD）、以及特征提取等）。
metadata:
  {
    "openclaw":
      {
        "emoji": "🎙️",
        "requires": { 
          "bins": ["ffmpeg", "python3"], 
          "pip": ["openai-whisper", "gTTS", "librosa", "pydub", "soundfile", "numpy", "webrtcvad-wheels"] 
        },
        "install":
          [
            {
              "id": "ffmpeg",
              "kind": "brew",
              "package": "ffmpeg",
              "label": "Install ffmpeg",
            },
            {
              "id": "python-deps",
              "kind": "pip",
              "package": "openai-whisper gTTS librosa pydub soundfile numpy webrtcvad-wheels",
              "label": "Install Python dependencies",
            }
          ],
      },
  }
---
# 音频处理技能

一套用于音频操作和分析的综合性工具集。

## 工具 API

### audio_tool
执行音频操作，如转录、文本转语音（TTS）以及特征提取。

- **参数：**
  - `action` (string, 必填): 可选值：`transcribe`、`tts`、`extract_features`、`vad_segments`、`transform`。
  - `file_path` (string, 可选): 输入音频文件的路径。
  - `text` (string, 可选): 用于文本转语音的文本。
  - `output_path` (string, 可选): 输出文件的路径（默认：自动生成）。
  - `model` (string, 可选): Whisper 模型的大小（tiny、base、small、medium、large）。默认值：`base`。

**使用示例：**

```bash
# Transcribe
uv run --with "openai-whisper" --with "pydub" --with "numpy" skills/audio-processing/tool.py transcribe --file_path input.wav

# TTS
uv run --with "gTTS" skills/audio-processing/tool.py tts --text "Hello world" --output_path hello.mp3

# Features
uv run --with "librosa" --with "numpy" --with "soundfile" skills/audio-processing/tool.py extract_features --file_path input.wav
```