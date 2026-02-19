---
name: audio-processing
description: 音频的摄取、分析、转换以及生成（包括转录、文本到语音（TTS）、语音活动检测（VAD）以及特征提取等）。
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
        "version": "1.1.0",
      },
  }
---
# 音频处理技能

这是一个用于音频操作和分析的综合性工具集，同时具备安全验证功能。

## 安全性

- 对文件路径进行验证，以防止路径遍历攻击；
- 禁止访问系统目录（/etc、/proc、/sys、/root）；
- 限制TTS文本输入的长度为10,000个字符；
- 所有文件操作均使用解析后的绝对路径。

## 工具API

### audio_tool
执行音频操作，如转录、文本转语音（TTS）和特征提取。

- **参数：**
  - `action`（字符串，必选）：`transcribe`、`tts`、`extract_features`、`vad_segments`、`transform`之一；
  - `file_path`（字符串，可选）：输入音频文件的路径；
  - `text`（字符串，可选）：用于TTS的文本（最长10,000个字符）；
  - `output_path`（字符串，可选）：输出文件的路径（默认：自动生成）；
  - `model`（字符串，可选）：Whisper模型的大小（tiny、base、small、medium、large）。默认值：`base`；
  - `ops`（字符串，可选）：用于`transform`操作的JSON字符串。

**使用方法：**

```bash
# Transcribe audio file
uv run --with "openai-whisper" --with "pydub" --with "numpy" skills/audio-processing/tool.py transcribe --file_path input.wav

# Transcribe with specific model
uv run --with "openai-whisper" skills/audio-processing/tool.py transcribe --file_path input.wav --model small

# Text-to-speech
uv run --with "gTTS" skills/audio-processing/tool.py tts --text "Hello world" --output_path hello.mp3

# Extract audio features
uv run --with "librosa" --with "numpy" --with "soundfile" skills/audio-processing/tool.py extract_features --file_path input.wav

# Voice activity detection (find speech segments)
uv run --with "pydub" skills/audio-processing/tool.py vad_segments --file_path input.wav

# Transform audio (trim, resample, normalize)
uv run --with "pydub" skills/audio-processing/tool.py transform --file_path input.wav --ops '[{"op": "trim", "start": 10, "end": 30}, {"op": "normalize"}]'
```

## 操作说明

### transcribe
使用OpenAI Whisper将语音转换为文本。

- 返回值：`{ "text": "...", "segments": [...] }`
- 可用的模型：tiny、base、small、medium、large（模型越大，准确性越高，处理速度越慢）

### tts
使用Google TTS将文本转换为语音。

- 返回值：`{ "file_path": "output.mp3", "status": "created" }`
- 语言：默认为英语

### extract_features
提取音频特征以供分析。

- 返回值：持续时间（duration）、采样率（sample_rate）、MFCC均值（mfcc_mean）、均方根均值（rms_mean）；
- 适用于音频分类和质量分析

### vad_segments
使用静音检测功能检测语音片段。

- 返回值：`{ "segments": [{ "start": 0.5, "end": 3.2 }, ...] }`
- 使用FFmpeg的silencedetect过滤器；
- 检测灵敏度：1-3（默认值：2）

### transform
对音频文件进行转换操作（如裁剪、重采样、标准化）。

- 返回值：`{ "file_path": "output.wav" }`

## 系统要求

- **ffmpeg**：VAD和转换操作需要此工具；
- **Python 3.8+**：所有操作均需此版本；
- **磁盘空间**：Whisper模型的大小从100MB（tiny）到3GB（large）不等。

## 错误处理

- 失败时返回JSON格式的错误信息；
- 在处理前验证所有文件路径；
- 能够优雅地处理缺失的依赖项。