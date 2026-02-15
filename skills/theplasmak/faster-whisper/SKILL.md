---
name: faster-whisper
description: 使用 faster-whisper 进行本地语音转文本功能：其转录速度比 OpenAI Whisper 快 4 到 6 倍，同时保持相同的准确性；通过 GPU 加速，可以实现近乎实时的转录（约 20 倍的转录速度）。该工具支持标准模型和精简模型，并可生成包含单词级时间戳的转录结果。
version: 1.0.4
author: ThePlasmak
homepage: https://github.com/ThePlasmak/faster-whisper
tags: ["audio", "transcription", "whisper", "speech-to-text", "ml", "cuda", "gpu"]
platforms: ["windows", "linux", "macos", "wsl2"]
metadata: {"moltbot":{"emoji":"🗣️","requires":{"bins":["ffmpeg","python3"]}}}
---

# Faster Whisper

这是一个基于CTranslate2实现的本地语音转文本工具，它是对OpenAI的Whisper的重新开发版本，运行速度比原版本快4到6倍，同时保持相同的准确性。通过GPU加速，转录速度可达到接近实时的水平（10分钟的音频文件大约30秒内完成）。

## 使用场景

当你需要以下操作时，可以使用这个工具：
- **转录音频/视频文件**：会议记录、访谈、播客、讲座、YouTube视频
- **本地将语音转换为文本**：无需支付API费用，支持离线使用（模型下载完成后即可使用）
- **批量处理多个音频文件**：适用于大量文件的处理
- **生成字幕/标题**：支持添加单词级别的时间戳
- **多语言转录**：支持99种以上语言，并能自动检测语言

**常用指令**：
- “转录这段音频”
- “将语音转换为文本”
- “他们说了什么”
- “生成文本记录”
- “为视频添加字幕”

**不适用场景**：
- 实时/流式转录（请使用专为流处理优化的工具）
- 仅依赖云服务的环境（没有本地计算资源）
- 音频文件时长小于10秒的情况（此时API调用的延迟影响不大）

## 快速参考

| 功能 | 命令 | 备注 |
|------|---------|-------|
| **基本转录** | `./scripts/transcribe audio.mp3` | 使用默认的distil-large-v3模型 |
| **更快的英语转录** | `./scripts/transcribe audio.mp3 --model distil-medium.en --language en` | 仅支持英语，速度提升6.8倍 |
| **最高准确性** | `./scripts/transcribe audio.mp3 --model large-v3-turbo --beam-size 10` | 速度稍慢，但质量最高 |
| **添加单词时间戳** | `./scripts/transcribe audio.mp3 --word-timestamps` | 适用于生成字幕/标题 |
| **JSON格式输出** | `./scripts/transcribe audio.mp3 --json -o output.json` | 支持程序化访问结果 |
| **多语言转录** | `./scripts/transcribe audio.mp3 --model large-v3-turbo` | 可自动检测语言 |
| **去除静音部分** | `./scripts/transcribe audio.mp3 --vad` | 支持语音活动检测 |

## 模型选择

根据你的需求选择合适的模型：

```dot
digraph model_selection {
    rankdir=LR;
    node [shape=box, style=rounded];

    start [label="Start", shape=doublecircle];
    need_accuracy [label="Need maximum\naccuracy?", shape=diamond];
    multilingual [label="Multilingual\ncontent?", shape=diamond];
    resource_constrained [label="Resource\nconstraints?", shape=diamond];

    large_v3 [label="large-v3\nor\nlarge-v3-turbo", style="rounded,filled", fillcolor=lightblue];
    large_turbo [label="large-v3-turbo", style="rounded,filled", fillcolor=lightblue];
    distil_large [label="distil-large-v3\n(default)", style="rounded,filled", fillcolor=lightgreen];
    distil_medium [label="distil-medium.en", style="rounded,filled", fillcolor=lightyellow];
    distil_small [label="distil-small.en", style="rounded,filled", fillcolor=lightyellow];

    start -> need_accuracy;
    need_accuracy -> large_v3 [label="yes"];
    need_accuracy -> multilingual [label="no"];
    multilingual -> large_turbo [label="yes"];
    multilingual -> resource_constrained [label="no (English)"];
    resource_constrained -> distil_small [label="mobile/edge"];
    resource_constrained -> distil_medium [label="some limits"];
    resource_constrained -> distil_large [label="no"];
}
```

### 模型对比表

#### 标准模型（Full Whisper）

| 模型 | 大小（MB） | 转录速度 | 准确率 | 适用场景 |
|-------|------|-------|----------|----------|
| `tiny` / `tiny.en` | 39MB | 最快 | 适用于快速草稿 |
| `base` / `base.en` | 74MB | 非常快 | 适用于一般场景 |
| `small` / `small.en` | 244MB | 较快 | 适用于大多数任务 |
| `medium` / `medium.en` | 769MB | 速度适中 | 适用于高质量转录 |
| `large-v1/v2/v3` | 1.5GB | 速度较慢 | 适用于最高精度要求 |
| **`large-v3-turbo`** | 809MB | 速度快 | **推荐用于需要高准确性的场景** |

#### 精简模型（速度提升约6倍，WER误差降低约1%）

| 模型 | 大小（MB） | 相比标准模型的速度提升 | 准确率 | 适用场景 |
|-------|------|-------------------|----------|----------|
| **`distil-large-v3`** | 756MB | 快速度提升约6.3倍 | WER误差为9.7% | **默认模型，平衡性能与准确率** |
| `distil-large-v2` | 756MB | 快速度提升约5.8倍 | WER误差为10.1% | 作为备用模型 |
| `distil-medium.en` | 394MB | 快速度提升约6.8倍 | 仅支持英语，适合资源有限的环境 |
| `distil-small.en` | 166MB | 快速度提升约5.6倍 | 适用于移动设备或边缘计算设备 |

`.en`后缀的模型仅支持英语内容，且处理英语文本时速度更快、效果更好。

## 设置指南

### Linux / macOS / WSL2

```bash
# Run the setup script (creates venv, installs deps, auto-detects GPU)
./setup.sh
```

### Windows（原生环境）

```powershell
# Run from PowerShell (auto-installs Python & ffmpeg if missing via winget)
.\setup.ps1
```

Windows设置脚本会自动完成以下操作：
- 如果系统中没有Python 3.12，会通过winget工具进行安装
- 如果系统中没有ffmpeg，也会通过winget工具进行安装
- 检测NVIDIA GPU并安装支持CUDA的PyTorch
- 创建虚拟环境（venv）并安装所有依赖库

**系统要求**：
- **Linux/macOS/WSL2**：Python 3.10及以上版本，以及ffmpeg
- **Windows**：无需额外安装，设置脚本会自动安装所有依赖库

## 平台支持

| 平台 | 加速方式 | 转录速度 | 是否支持自动安装 |
|----------|-------------|-------|--------------|
| **Windows + NVIDIA GPU** | 使用CUDA | 转录速度接近实时（约20倍） | 支持 |
| **Linux + NVIDIA GPU** | 使用CUDA | 转录速度接近实时（约20倍） | 需手动安装相关组件 |
| **WSL2 + NVIDIA GPU** | 使用CUDA | 转录速度接近实时（约20倍） | 需手动安装相关组件 |
| **macOS Apple Silicon** | 仅使用CPU | 转录速度约为实时的3到5倍 | 需手动安装相关组件 |
| **macOS Intel** | 使用CPU | 转录速度约为实时的1到2倍 | 需手动安装相关组件 |
| **Windows（无GPU）** | 使用CPU | 转录速度约为实时的1倍 | 支持 |
| **Linux（无GPU）** | 使用CPU | 转录速度约为实时的1倍 | 需手动安装相关组件 |

**注意**：faster-whisper在macOS上仅使用CPU进行转录，但由于Apple Silicon的处理能力较强，实际使用效果仍然不错。

### GPU支持（非常重要！）

设置脚本会自动检测你的GPU并安装支持CUDA的PyTorch。**如果有GPU，请务必使用GPU进行转录**，因为仅使用CPU会大大降低转录速度。

| 硬件配置 | 转录速度（处理10分钟视频的时间） |
|----------|-------|-------------|
| RTX 3070（带GPU） | 约20秒 |
| CPU（int8格式） | 约30秒 |

如果设置脚本未能检测到GPU，请手动安装支持CUDA的PyTorch：

**Linux/macOS/WSL2：**
```bash
# For CUDA 12.x
uv pip install --python .venv/bin/python torch --index-url https://download.pytorch.org/whl/cu121

# For CUDA 11.x
uv pip install --python .venv/bin/python torch --index-url https://download.pytorch.org/whl/cu118
```

**Windows：**
```powershell
# For CUDA 12.x
.venv\Scripts\pip install torch --index-url https://download.pytorch.org/whl/cu121

# For CUDA 11.x
.venv\Scripts\pip install torch --index-url https://download.pytorch.org/whl/cu118
```

- **Windows用户**：确保已安装[NVIDIA驱动程序](https://www.nvidia.com/download/index.aspx)
- **WSL2用户**：确保在Windows上安装了[NVIDIA的WSL兼容CUDA驱动程序](https://docs.nvidia.com/cuda/wsl-user-guide/)

## 使用方法

**Linux/macOS/WSL2：**
```bash
# Basic transcription
./scripts/transcribe audio.mp3

# With specific model
./scripts/transcribe audio.wav --model large-v3-turbo

# With word timestamps
./scripts/transcribe audio.mp3 --word-timestamps

# Specify language (faster than auto-detect)
./scripts/transcribe audio.mp3 --language en

# JSON output
./scripts/transcribe audio.mp3 --json
```

**Windows（cmd或PowerShell）：**
```powershell
# Basic transcription
.\scripts\transcribe.cmd audio.mp3

# With specific model
.\scripts\transcribe.cmd audio.wav --model large-v3-turbo

# With word timestamps (PowerShell native syntax also works)
.\scripts\transcribe.ps1 audio.mp3 -WordTimestamps

# JSON output
.\scripts\transcribe.cmd audio.mp3 --json
```

## 配置选项

```
--model, -m        Model name (default: distil-large-v3)
--language, -l     Language code (e.g., en, es, fr - auto-detect if omitted)
--word-timestamps  Include word-level timestamps
--beam-size        Beam search size (default: 5, higher = more accurate but slower)
--vad              Enable voice activity detection (removes silence)
--json, -j         Output as JSON
--output, -o       Save transcript to file
--device           cpu or cuda (auto-detected)
--compute-type     int8, float16, float32 (default: auto-optimized)
--quiet, -q        Suppress progress messages
```

## 示例用法

```bash
# Transcribe YouTube audio (after extraction with yt-dlp)
yt-dlp -x --audio-format mp3 <URL> -o audio.mp3
./scripts/transcribe audio.mp3

# Batch transcription with JSON output
for file in *.mp3; do
  ./scripts/transcribe "$file" --json > "${file%.mp3}.json"
done

# High-accuracy transcription with larger beam size
./scripts/transcribe audio.mp3 \
  --model large-v3-turbo --beam-size 10 --word-timestamps

# Fast English-only transcription
./scripts/transcribe audio.mp3 \
  --model distil-medium.en --language en

# Transcribe with VAD (removes silence)
./scripts/transcribe audio.mp3 --vad
```

## 常见问题及解决方法

| 问题 | 原因 | 解决方法 |
|---------|---------|----------|
| **在可用GPU的情况下仍使用CPU** | 转录速度会慢10到20倍 | 在Windows/Linux系统中运行`nvidia-smi`命令检查GPU状态；确认CUDA已正确安装 |
| **未指定语言** | 会浪费时间进行语言自动检测 | 如果知道语言类型，请使用`--language en`参数 |
| **选择了错误的模型** | 会导致转录速度变慢或准确率降低 | 默认的`distil-large-v3`模型表现良好；只有在需要更高准确率时才使用`large-v3`模型 |
| **忽略了精简模型** | 无法享受速度提升，且准确率损失不到1% | 在使用标准模型之前，先尝试使用`distil-large-v3`模型 |
| **未安装ffmpeg** | 可能导致设置失败或无法处理音频文件 | 设置脚本会自动处理ffmpeg的安装；如果需要手动安装，请确保已安装 |
| **内存不足** | 模型过大，超出系统内存限制 | 选择更小的模型或使用`--compute-type int8`参数 |
| **设置beam-size过大** | 超过5或7时，速度提升效果不明显 | 默认值5通常足够；对于关键转录任务，可以尝试设置为10 |

## 性能说明

- **首次运行**：模型会一次性下载到`~/.cache/huggingface/`目录 |
- **GPU加速**：如果系统支持GPU，会自动使用CUDA（速度提升约10到20倍） |
- **量化技术**：在CPU上使用INT8格式进行转录，速度提升约4倍，同时准确率损失很小 |
- **内存需求**：
  - `distil-large-v3`：约2GB内存 |
  - `large-v3-turbo`：约4GB内存 |
  - `tiny/base`：小于1GB内存 |

## 为什么选择faster-whisper？

- **速度**：比OpenAI的Whisper快4到6倍 |
- **准确率**：与原模型相同（使用相同的模型权重） |
- **效率**：通过量化技术降低内存消耗 |
- **稳定性**：基于成熟的C++后端（CTranslate2） |
- **精简模型**：速度提升约6倍，准确率损失不到1% |

## 故障排除

- **“CUDA不可用”**：请确保已安装支持CUDA的PyTorch |
- **设置失败**：确认已安装Python 3.10及以上版本 |
- **内存不足**：选择更小的模型或使用`--compute-type int8`参数 |
- **CPU转录速度慢**：建议使用GPU以提高效率 |
- **模型下载失败**：检查`~/.cache/huggingface/`目录的权限（Linux/macOS）或`%USERPROFILE%\.cache\huggingface\`目录（Windows） |

### Windows特有的问题

- **“winget未找到”**：请从Microsoft Store安装[App Installer](https://apps.microsoft.com/detail/9NBLGGH4NNS1)，或手动安装Python/ffmpeg |
- **安装后Python不在PATH路径中**：关闭终端后重新打开，然后再次运行`setup.ps1`脚本 |
- **PowerShell执行策略问题**：运行`Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`，或改用`transcribe.cmd`命令 |
- **虽然有GPU但nvidia-smi命令无法使用**：请确保已安装[NVIDIA驱动程序](https://www.nvidia.com/download/index.aspx) |

## 参考资料

- [faster-whisper的GitHub仓库](https://github.com/SYSTRAN/faster-whisper)
- [关于Distil-Whisper的研究论文](https://arxiv.org/abs/2311.00430)
- [HuggingFace提供的faster-whisper模型](https://huggingface.co/collections/Systran/faster-whisper)