---
name: faster-whisper-gpu
description: 使用Faster Whisper技术结合NVIDIA GPU加速，实现高性能的本地语音转文本功能。无需将音频文件发送到外部服务，即可完成本地转录。
homepage: https://github.com/FelipeOFF/faster-whisper-gpu
metadata:
  clawdbot:
    emoji: 🎙️
    category: audio
    tags:
      - transcription
      - stt
      - speech-to-text
      - whisper
      - gpu
      - cuda
      - local
      - privacy
    requires:
      bins:
        - python3
      python_packages:
        - faster-whisper
        - torch
    install:
      - id: pip
        kind: pip
        packages:
          - faster-whisper
          - torch
        label: Install faster-whisper and PyTorch
---
# 🎙️ 更快的 Whisper GPU 版本

使用 [Faster Whisper](https://github.com/SYSTRAN/faster-whisper) 结合 NVIDIA GPU 加速技术，实现高性能的本地语音转文本功能。

## ✨ 主要特性

- **🚀 GPU 加速**：利用 NVIDIA CUDA 实现超快速的语音转文本处理
- **🔒 100% 本地处理**：所有数据均保留在您的设备上，完全保护隐私
- **💰 永久免费**：无需支付 API 费用，可无限次进行语音转文本操作
- **🌍 多语言支持**：支持 99 种语言，并能自动识别语言
- **📁 多种输出格式**：输入格式包括 MP3、WAV、FLAC、OGG、M4A；输出格式包括 TXT、SRT、JSON
- **🎯 多种模型选择**：提供多种模型，从小型模型（速度快）到大型模型（准确度高）
- **🎬 字幕生成**：支持生成包含单词时间戳的 SRT 格式字幕

## 📋 系统要求

### 硬件
- 支持 CUDA 的 NVIDIA GPU（推荐配置：4GB 以上显存）
- 或仅使用 CPU（速度较慢，但适用于所有设备）

### 软件
- Python 3.8 或更高版本
- NVIDIA 驱动程序
- CUDA Toolkit 11.8 或 12.x 版本

## 🚀 快速入门

### 安装

```bash
# Install dependencies
pip install faster-whisper torch

# Verify GPU is available
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"
```

### 基本用法

```bash
# Transcribe an audio file (auto-detects GPU)
python transcribe.py audio.mp3

# Specify language explicitly
python transcribe.py audio.mp3 --language pt

# Output as SRT subtitles
python transcribe.py audio.mp3 --format srt --output subtitles.srt

# Use larger model for better accuracy
python transcribe.py audio.mp3 --model large-v3
```

## 🔧 高级用法

### 命令行参数

```bash
python transcribe.py <audio_file> [options]

Options:
  --model {tiny,base,small,medium,large-v1,large-v2,large-v3}
                        Model size to use (default: base)
  --language LANG       Language code (e.g., 'pt', 'en', 'es'). Auto-detect if not specified.
  --format {txt,srt,json,vtt}
                        Output format (default: txt)
  --output FILE         Output file path (default: stdout)
  --device {cuda,cpu}   Device to use (default: cuda if available)
  --compute_type {int8,int8_float16,int16,float16,float32}
                        Computation precision (default: float16)
  --task {transcribe,translate}
                        Task: transcribe or translate to English (default: transcribe)
  --vad_filter          Enable voice activity detection filter
  --vad_parameters MIN_DURATION_ON,MIN_DURATION_OFF
                        VAD parameters as comma-separated values
  --condition_on_previous_text
                        Condition on previous text (default: True)
  --initial_prompt PROMPT
                        Initial prompt to guide transcription
  --word_timestamps     Include word-level timestamps (for SRT/JSON)
  --hotwords WORDS      Comma-separated hotwords to boost recognition
```

### 使用示例

#### 葡萄牙语转文本（输出为 SRT 格式）
```bash
python transcribe.py meeting.mp3 --language pt --format srt --output meeting.srt
```

#### 从任意语言翻译成中文
```bash
python transcribe.py japanese_audio.mp3 --task translate --format txt
```

#### 使用高精度模型进行翻译
```bash
python transcribe.py podcast.mp3 --model large-v3 --vad_filter --word_timestamps
```

#### 仅使用 CPU（不使用 GPU）的模式
```bash
python transcribe.py audio.mp3 --device cpu --compute_type int8
```

## 🐍 Python API

```python
from faster_whisper import WhisperModel

# Load model
model = WhisperModel("base", device="cuda", compute_type="float16")

# Transcribe
segments, info = model.transcribe("audio.mp3", language="pt")

print(f"Detected language: {info.language} (probability: {info.language_probability:.2f})")

for segment in segments:
    print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
```

## 📊 模型规格与显存需求

| 模型        | 参数            | 所需显存（MB） | 相对速度 | 精确度     |
|------------|----------------|-----------|---------|---------|
| tiny       | 39 MB           | 约 1 GB      | 约 32 倍    | 基础级别   |
| base       | 74 MB           | 约 1 GB      | 约 16 倍    | 良好       |
| small      | 244 MB           | 约 2 GB      | 约 6 倍    | 更好       |
| medium     | 769 MB           | 约 5 GB      | 约 2 倍    | 非常好    |
| large-v3     | 1550 MB          | 约 10 GB     | 1 倍      | 最佳       |

*基准测试基于 NVIDIA RTX 4090 进行*

## 🛠️ 支持的语言

Faster Whisper 支持 99 种语言，包括：
- **葡萄牙语** (`pt`)
- **英语** (`en`)
- **西班牙语** (`es`)
- **法语** (`fr`)
- **德语** (`de`)
- **意大利语** (`it`)
- **日语** (`ja`)
- **中文** (`zh`)
- **俄语** (`ru`)
- **以及更多语言...**

## 🛠️ 故障排除

### CUDA 内存不足问题
```bash
# Use smaller model
python transcribe.py audio.mp3 --model tiny

# Or use CPU
python transcribe.py audio.mp3 --device cpu

# Or reduce precision
python transcribe.py audio.mp3 --compute_type int8
```

### 模型下载问题
首次使用时，模型会自动下载到 `~/.cache/huggingface/hub/` 目录中。
如果使用代理服务器，请设置相关配置：
```bash
export HF_HOME=/path/to/custom/cache
```

### 转文本速度较慢的问题
- 确保 GPU 被正确使用（在转文本过程中查看 `nvidia-smi` 输出）
- 选择较小的模型以获得更快结果
- 启用 VAD（Voice Activity Detection）过滤器以跳过静音部分

## 🤝 贡献方式

欢迎贡献代码！请按照以下步骤操作：
1. 克隆项目仓库
2. 创建一个新的功能分支
3. 提交拉取请求（pull request）

## 📜 许可证

本项目采用 MIT 许可证，详细信息请参阅 [LICENSE](LICENSE) 文件。

Faster Whisper 由 [SYSTRAN](https://github.com/SYSTRAN/faster-whisper) 开发，基于 OpenAI 的 Whisper 模型进行优化。

## 🙏 致谢

- [OpenAI Whisper](https://github.com/openai/whisper)：原始模型
- [Faster Whisper](https://github.com/SYSTRAN/faster-whisper)：优化后的实现
- [CTranslate2](https://github.com/OpenNMT/CTranslate2)：快速推理引擎

---

**专为 OpenClaw 社区精心制作 ❤️**