---
name: faster-whisper
description: "使用 faster-whisper 实现本地语音转文本功能：其转换速度比 OpenAI Whisper 快 4 到 6 倍，同时保持相同的准确率；通过 GPU 加速，可以实现接近实时的转录效果（约 20 倍的转换速度）。支持 SRT/VTT 字幕格式、说话者身份识别、URL/YouTube 视频输入以及批量处理功能。"
version: 1.4.3
author: ThePlasmak
homepage: https://github.com/ThePlasmak/faster-whisper
tags: ["audio", "transcription", "whisper", "speech-to-text", "ml", "cuda", "gpu", "subtitles", "diarization"]
platforms: ["linux", "macos", "wsl2"]
metadata: {"openclaw":{"emoji":"🗣️","requires":{"bins":["ffmpeg","python3"],"optionalBins":["yt-dlp"],"optionalPaths":["~/.cache/huggingface/token"]}}}
---
# Faster Whisper

这是一个基于CTranslate2实现的本地语音转文本工具，它使用了OpenAI的Whisper模型，运行速度比原版快4到6倍，同时保持了相同的准确率。通过GPU加速，可以实现接近实时的转录效果（例如，10分钟的音频文件可以在30秒内完成转录）。

## 使用场景

当你需要以下功能时，可以使用这个工具：
- **转录音频/视频文件**：会议记录、采访、播客、讲座、YouTube视频
- **生成字幕**：支持SRT和VTT格式，包含单词级别的时间戳
- **识别说话者**：为音频内容标注说话者
- **从URL转录**：自动从YouTube链接或直接音频URL下载并转录（使用yt-dlp）
- **批量处理文件**：支持通配符匹配和目录操作，可以跳过已存在的文件
- **本地将语音转换为文本**：无需API费用，支持离线使用（模型下载完成后即可使用）
- **多语言转录**：支持99多种语言，并能自动检测语言
- **针对特定领域优化**：使用`--initial-prompt`参数来处理专业术语较多的内容

**常用指令：**
- `transcribe this audio`：转录这段音频
- `convert speech to text`：将语音转换为文本
- `what did they say`：识别音频中的内容
- `make a transcript`：生成转录文本
- `audio to text`：将音频转换为文本
- `subtitle this video`：为视频添加字幕
- `who's speaking`：识别视频中的说话者

**注意事项：**
- **简化调用方式**：
  - 默认命令`./scripts/transcribe audio.mp3`是最快的方式，不要添加用户未请求的参数
  - 仅在用户询问“谁说了什么”或“识别说话者”时添加`--diarize`
  - 仅在用户需要字幕时添加`--format srt/vtt`
  - 仅在需要单词级别时间戳时添加`--word-timestamps`
  - 仅在处理特定领域内容时添加`--initial-prompt`
  - 所有单词级别的处理会自动使用wav2vec2对齐算法（额外耗时约5-10秒）
  - 使用`--diarize`会额外增加20-30秒的处理时间

**不适用场景：**
- **实时/流式转录**：请使用专为流媒体优化的工具
- **没有本地计算资源的云环境**
- **音频文件时长小于10秒的情况**：在这种情况下，API调用的延迟无关紧要

## 快速参考

| 功能 | 命令 | 说明 |
|------|---------|-------|
| **基本转录** | `./scripts/transcribe audio.mp3` | 批量处理，开启语音活动检测（VAD），使用distil-large-v3.5模型 |
| **SRT字幕** | `./scripts/transcribe audio.mp3 --format srt -o subs.srt` | 自动添加单词时间戳 |
| **VTT字幕** | `./scripts/transcribe audio.mp3 --format vtt -o subs.vtt` | 生成WebVTT格式的字幕 |
| **单词时间戳** | `./scripts/transcribe audio.mp3 --word-timestamps --format srt` | 使用wav2vec2算法对齐时间戳 |
| **说话者识别** | `./scripts/transcribe audio.mp3 --diarize` | 需要安装pyannote.audio库 |
| **YouTube/URL转录** | `./scripts/transcribe https://youtube.com/watch?v=...` | 通过yt-dlp自动下载音频 |
| **批量处理** | `./scripts/transcribe *.mp3 -o ./transcripts/` | 将结果输出到指定目录 |
| **跳过已存在的文件** | `./scripts/transcribe *.mp3 --skip-existing -o ./out/` | 继续处理未完成的批次 |
| **领域术语优化** | `./scripts/transcribe audio.mp3 --initial-prompt 'Kubernetes gRPC'` | 优化专业术语的转录 |
| **优化英语转录** | `./scripts/transcribe audio.mp3 --model distil-medium.en -l en` | 仅处理英语内容，速度提升6.8倍 |
| **最高准确率** | `./scripts/transcribe audio.mp3 --model large-v3 --beam-size 10` | 使用完整模型 |
| **JSON格式输出** | `./scripts/transcribe audio.mp3 --format json -o out.json` | 提供可编程访问的转录结果和统计信息 |
| **过滤噪声** | `./scripts/transcribe audio.mp3 --min-confidence 0.6` | 过滤低置信度的音频片段 |
| **减少批量大小** | `./scripts/transcribe audio.mp3 --batch-size 4` | 如果GPU内存不足，可以减小批量大小 |

## 模型选择

根据你的需求选择合适的模型：

### 模型列表

#### 标准模型（完整版Whisper）
| 模型 | 大小（MB） | 运行速度 | 准确率 | 适用场景 |
|-------|------|-------|----------|----------|
| `tiny` / `tiny.en` | 39MB | 最快 | 基础用途 | 快速草稿 |
| `base` / `base.en` | 74MB | 非常快 | 通用用途 |
| `small` / `small.en` | 244MB | 较快 | 大多数任务 |
| `medium` / `medium.en` | 769MB | 中等速度 | 高质量转录 |
| `large-v1/v2/v3` | 1.5GB | 较慢 | 最高准确率 |
| `large-v3-turbo` | 809MB | 快速 | 高准确率（但速度略慢于distil版本） |

#### 提炼模型（速度提升约6倍，WER误差降低约1%）
| 模型 | 大小（MB） | 相对于标准模型的速度提升 | 准确率 | 适用场景 |
| **`distil-large-v3.5`** | 756MB | 快速度提升约6.3倍 | WER误差为7.08% | 默认推荐模型 |
| `distil-large-v3` | 756MB | 快速度提升约6.3倍 | WER误差为7.53% | 之前的默认模型 |
| `distil-large-v2` | 756MB | 快速度提升约5.8倍 | WER误差为10.1% | 备用模型 |
| `distil-medium.en` | 394MB | 快速度提升约6.8倍 | WER误差为11.1% | 仅支持英语 |
| `distil-small.en` | 166MB | 快速度提升约5.6倍 | WER误差为12.1% | 适用于移动设备 |

`.en`后缀的模型仅支持英语内容，且处理英语内容的速度更快、准确率更高。

## 设置

### Linux / macOS / WSL2环境

**所需软件：**
- Python 3.10及以上版本
- ffmpeg
- （可选）yt-dlp（用于处理URL/YouTube音频）
- （可选）pyannote.audio（用于`--diarize`功能，通过`setup.sh --diarize`安装）

### 平台支持

| 平台 | 加速方式 | 运行速度 |
|----------|-------------|-------|
| **Linux + NVIDIA GPU** | 使用CUDA | 实时转录速度约20倍 |
| **WSL2 + NVIDIA GPU** | 使用CUDA | 实时转录速度约20倍 |
| macOS Apple Silicon** | 使用CPU | 实时转录速度约3-5倍 |
| macOS Intel** | 使用CPU | 实时转录速度约1-2倍 |
| **无GPU的Linux系统** | 使用CPU | 实时转录速度约1倍 |

*`faster-whisper`在macOS上仅使用CPU，但由于Apple Silicon的性能足够好，实际使用中效果依然不错。*

### GPU支持（非常重要！）

设置脚本会自动检测你的GPU并安装PyTorch及CUDA。**如果有GPU，请务必使用**，因为使用CPU进行转录会非常慢。

**硬件配置建议：**
- **RTX 3070 GPU**：实时转录速度约20倍，处理时间约27秒 |
- **普通CPU**：实时转录速度约0.3倍，处理时间约30分钟

如果设置脚本未检测到GPU，请手动安装PyTorch及CUDA：

### 使用方法

### 参数说明

### 输出格式

- **文本格式**：纯文本转录结果，使用`--diarize`参数会标注说话者信息。
- **JSON格式**：包含转录内容、时间戳、语言检测结果和性能统计信息的JSON文件。
- **SRT格式**：标准的视频字幕格式。
- **VTT格式**：适用于Web视频播放器的字幕格式。

### 说话者识别

使用`pyannote.audio`库可以识别音频中的说话者。设置和用法详见相关文档。

**注意事项：**
- 需要在`~/.cache/huggingface/token`路径下存放HuggingFace的token文件（使用`huggingface-cli login`登录）。
- 支持的模型协议包括：`https://hf.co/pyannote/speaker-diarization-3.1`和`https://hf.co/pyannote/segmentation-3.0`。

### 常见问题及解决方法**

- **建议使用GPU而非CPU**：使用GPU可显著提升转录速度。
- **指定语言**：如果知道音频语言，请使用`--language en`参数以避免不必要的自动语言检测。
- **选择合适的模型**：默认模型`distil-large-v3.5`性能良好；只有在需要更高准确率时才使用`large-v3`模型。
- **注意模型选择**：使用`distil-large-v3.5`可提升6倍速度，同时准确率损失不到1%。
- **确保安装必要的工具**：`yt-dlp`用于从URL下载音频。
- **批量处理**：可以使用通配符和目录路径批量处理文件。
- **输出格式**：输出文件名格式为`{input-stem}.{ext}`（例如，`audio.mp3`转换为`audio.srt`）。

## 性能说明**

- **首次运行**：会自动将模型下载到`~/.cache/huggingface/`目录。
- **批量处理**：默认启用批量处理功能，速度比单次处理快3倍；同时会开启语音活动检测（VAD）。
- **GPU加速**：如果系统支持CUDA，会自动使用GPU加速。
- **量化设置**：使用INT8格式可提升约4倍的转录速度，同时几乎不影响准确率。
- **性能统计**：每次转录结果都会显示音频时长、处理时间和实时转录速度。
- **基准测试**：在RTX 3070显卡上，使用`distil-large-v3`模型的批量处理时间为约24秒，而不使用GPU时为约69秒。
- **额外开销**：使用wav2vec2算法进行对齐会额外增加5-10秒的处理时间。
- **内存限制**：根据GPU内存大小选择合适的模型（例如，`large-v3`模型需要约2GB RAM）。

## 为什么faster-whisper更快速？

- **运行速度**：比OpenAI的Whisper快4到6倍。
- **准确率**：与原版模型相同。
- **效率**：通过量化技术降低内存占用。
- **稳定性**：使用稳定的C++后端（CTranslate2）。
- **模型优化**：使用提炼模型（distil系列）可提升速度，同时准确率损失不到1%。
- **输出格式**：支持SRT/VTT字幕格式。
- **对齐精度**：自动使用wav2vec2算法进行精确对齐。
- **附加功能**：支持通过`pyannote`进行说话者识别。
- **输入方式**：可以直接使用URL或YouTube链接输入音频。

## 故障排除**

- **CUDA未安装**：请确保安装了PyTorch及CUDA。
- **设置失败**：检查是否安装了Python 3.10及以上版本。
- **内存不足**：选择合适的模型或调整参数（如`--compute-type int8`或`--batch-size`）。
- **CPU性能慢**：建议使用GPU进行转录。
- **模型下载失败**：检查`~/.cache/huggingface/`目录的权限设置。
- **说话者识别失败**：确保HuggingFace token文件存在并接受相关协议。
- **URL下载失败**：请确保安装了`yt-dlp`工具。
- **输出格式问题**：检查输入文件的格式是否正确。

## 参考资料**

- [faster-whisper的GitHub仓库](https://github.com/SYSTRAN/faster-whisper)
- [关于distil-Whisper的论文](https://arxiv.org/abs/2311.00430)
- [HuggingFace提供的相关模型](https://huggingface.co/collections/Systran/faster-whisper)
- **用于说话者识别的pyannote.audio库**（https://github.com/pyannote/pyannote-audio）
- **用于下载音频的yt-dlp工具**（https://github.com/yt-dlp/yt-dlp）