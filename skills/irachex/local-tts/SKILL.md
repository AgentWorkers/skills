---
name: local-tts
description: 使用 Qwen3-TTS 实现本地文本转语音功能，支持 mlx_audio（macOS Apple Silicon）或 qwen-tts（Linux/Windows）平台。该技术采用隐私优先的离线语音合成方式，能够实现自然、逼真的语音克隆与语音设计，适用于本地、安全、高质量的多语言语音合成需求。
license: MIT
---
# 使用 Qwen3-TTS 进行本地语音合成

**隐私优先 | 离线使用 | 高质量 | 自然真实的人声**

Qwen3-TTS 支持在本地进行文本到语音的合成。您的文本永远不会离开您的设备。

## 为什么选择本地语音合成？

与云语音合成服务（如 Google、AWS、Azure）不同，本地语音合成具有以下优势：
- **零数据传输**：所有处理都在设备上完成；
- **无需网络**：完全离线使用；
- **无需 API 密钥**：无需依赖外部服务；
- **符合 GDPR/HIPAA 标准**：简化了合规性要求。

详情请参阅 [隐私与安全说明](references/privacy_security.md)。

## 平台概述

| 平台 | 后端 | 安装方式 | 适用系统 |
|--------|--------|------------|---------|
| macOS (Apple Silicon) | `mlx_audio` | `pip install mlx-audio` | M1/M2/M3/M4 Mac 电脑 |
| Linux/Windows | `qwen-tts` | `pip install qwen-tts` | 需要 CUDA 显卡 |

## 快速入门

### macOS

```bash
pip install mlx-audio
brew install ffmpeg

# Natural female voice
python -m mlx_audio.tts.generate \
    --text "Hello world" \
    --model mlx-community/Qwen3-TTS-12Hz-1.7B-CustomVoice-8bit \
    --voice Chelsie
```

### Linux/Windows

```bash
pip install qwen-tts

# With optimizations (FlashAttention, bfloat16, auto-device)
python scripts/tts_linux.py "Hello world" --female
```

## 关键概念

### `--voice` 与 `--instruct`（重要）

| 模型 | `--voice` | `--instruct` | 备注 |
|------|---------|--------------|--------|
| **CustomVoice** | 选择预设语音 | 添加语音风格/情感 | 可同时使用 |
| **VoiceDesign** | 不适用 | 根据描述创建新语音 | 仅支持 `--instruct` |
| **Base** | 不适用 | 用于语音克隆（需配合 `--ref_audio` 使用 |

**支持风格控制的 CustomVoice 示例：**
```bash
python -m mlx_audio.tts.generate \
    --text "Hello there!" \
    --model mlx-community/Qwen3-TTS-12Hz-1.7B-CustomVoice-8bit \
    --voice Serena \
    --instruct "excited and enthusiastic"
```

### 9 种预设语音（开源 CustomVoice）

| 语音 | 性别 | 语言 | 特点 |
|------|------|---------|--------|
| Chelsie | 女性 | 英语（美式） | 温柔、富有同理心 |
| Serena | 女性 | 英语 | 温暖、亲切 |
| Ono Anna | 女性 | 日语 | 活泼有趣 |
| Sohee | 女性 | 韩语 | 温暖 |
| Aiden | 男性 | 英语（美式） | 阳光开朗 |
| Dylan | 男性 | 英语 | 自然流畅 |
| Eric | 男性 | 英语 | 逼真自然 |
| Ryan | 男性 | 英语 | 自然流畅 |
| Uncle Fu | 男性 | 中语 | 具有年轻北京口音 |

**默认设置：** 女性 = Serena，男性 = Aiden

## 使用示例

### 使用预设语音

```bash
# Natural female
python -m mlx_audio.tts.generate \
    --text "Your text" --voice Serena --lang_code en \
    --model mlx-community/Qwen3-TTS-12Hz-1.7B-CustomVoice-8bit

# Real male
python -m mlx_audio.tts.generate \
    --text "Your text" --voice Aiden --lang_code en \
    --model mlx-community/Qwen3-TTS-12Hz-1.7B-CustomVoice-8bit
```

### 基于描述创建新语音（VoiceDesign）

```bash
python -m mlx_audio.tts.generate \
    --text "Hello" \
    --model mlx-community/Qwen3-TTS-12Hz-1.7B-VoiceDesign-8bit \
    --instruct "A warm female voice, professional and clear"
```

### 处理长文本

对于长文本，可以增加 `--max_tokens` 参数，并启用 `--join_audio`（仅适用于 macOS/MLX）：

```bash
python -m mlx_audio.tts.generate \
    --text "Your very long text here..." \
    --model mlx-community/Qwen3-TTS-12Hz-1.7B-CustomVoice-8bit \
    --voice Serena \
    --max_tokens 4096 \
    --join_audio \
    --output long_audio.wav
```

### 语音克隆

```bash
python -m mlx_audio.tts.generate \
    --text "Cloned voice speaking" \
    --model mlx-community/Qwen3-TTS-12Hz-1.7B-Base-8bit \
    --ref_audio sample.wav --ref_text "Sample transcript"
```

## 参数说明

| 参数 | 说明 | 可选值 |
|--------|------------|---------|
| `--text` | 需要合成的文本 | 必填 |
| `--model` | 模型 ID | 详见下表 |
| `--voice` | 预设语音（CustomVoice） | Chelsie, Serena, Aiden 等 |
| `--instruct` | 语音描述（VoiceDesign）或风格/情感（CustomVoice） | 例如：`excited`（兴奋）、`calm`（平静）、`professional`（专业） |
| `--speed` | 说话速度 | 0.5-2.0（默认：1.0） |
| `--pitch` | 语音音调 | 0.5-2.0（默认：1.0） |
| `--lang_code` | 语言 | en, cn, ja, ko, de, fr 等 |
| `--ref_audio` | 用于克隆的语音文件路径 | 可选 |
| `--output` | 输出文件路径 | 如果省略则自动生成 |
| `--max_tokens` | 最大生成词数 | 整数（默认：2048） | 长文本时建议增加 |
| `--join_audio` | 是否合并音频片段 | `true`（默认）或 `false` | 长文本时推荐使用 |

## 模型介绍

| 模型 | 大小 | 用途 |
|------|------|---------|
| `Qwen3-TTS-12Hz-1.7B-CustomVoice` | 1700 万参数 | 支持 9 种预设语音及风格控制 |
| `Qwen3-TTS-12Hz-1.7B-VoiceDesign` | 1700 万参数 | 基于文本创建新语音 |
| `Qwen3-TTS-12Hz-1.7B-Base` | 1700 万参数 | 用于语音克隆 |
| `Qwen3-TTS-12Hz-0.6B-*` | 600 万参数 | 轻量级版本 |

**macOS 上的模型前缀**：`mlx-community/`（例如：`mlx-community/Qwen3-TTS-12Hz-1.7B-Base-8bit`）

## 脚本

- `scripts/tts_macos.py` | macOS 版本的工具脚本 |
- `scripts/tts_linux.py` | Linux/Windows 版本的工具脚本（包含优化）

## 优化设置（Linux/Windows）

`tts_linux.py` 自动启用以下功能：
- **FlashAttention**：更快、更节省内存 |
- **bfloat16**：更高精度 |
- **自动选择设备**：优先使用 CUDA，否则切换到 CPU |
- **混合精度计算**：提升计算速度和音质

## 常见问题及解决方法

| 问题 | 解决方案 |
|------|---------|
| macOS：找不到模型 | 使用 `mlx-community/` 前缀 |
| macOS：音频格式问题 | 安装 `brew install ffmpeg` |
| Linux：CUDA 内存不足 | 使用 600 万参数的轻量级模型 |
| Linux：运行缓慢 | 检查 CUDA 是否可用：`torch.cuda.is_available()` |

## 参考资料

- [macOS 使用说明](references/macos_mlx_audio.md) |
- [Linux/Windows 使用说明](references/linux_windows_transformers.md) |
- [隐私与安全政策](references/privacy_security.md)

## 版本信息

**1.0.0** | 详细信息请参阅 [版本说明](VERSION) 和 `package.json` 文件。