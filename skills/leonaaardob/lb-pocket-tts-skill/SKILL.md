---
id: pocket-tts
name: Pocket-TTS
version: 1.0.0
author: Leonardo Balland
description: 使用 Kyutai Pocket TTS 从文本生成语音——这是一个轻量级、对 CPU 资源要求较低的语音合成工具，支持语音克隆功能。在 M4 MacBook Air 上，其实时语音合成速度可达到约 6 倍于其他同类工具。
categories:
  - text-to-speech
  - documentation
tags:
  - kyutai
  - text-to-speech
  - tts
  - cpu
  - streaming
  - voice-cloning
homepage: https://kyutai.org/blog/2026-01-13-pocket-tts
repository: https://github.com/kyutai-labs/pocket-tts
documentation: https://github.com/kyutai-labs/pocket-tts/tree/main/docs
---

# Pocket TTS

这是一个轻量级的、对CPU要求较低的文本转语音（TTS）工具，支持语音克隆功能，且无需GPU。

## 使用场景

- 在没有GPU的情况下，使用CPU将文本转换为语音
- 从音频样本中克隆语音
- 实时生成流式音频（低延迟）
- 无需依赖API即可进行本地语音合成
- 实时语音合成速度约为普通方法的6倍

---

## 主要特性

- **模型参数数量：1亿个** – 体积小、效率高的模型
- **针对CPU优化** – 无需GPU，仅使用2个CPU核心
- **实时生成速度：约6倍** – 在现代CPU上可实现快速语音生成
- **延迟：约200毫秒** – 从开始到输出第一段音频数据
- **语音克隆** – 可以从3到10秒的音频样本中克隆语音
- **输出格式：24kHz单声道WAV** – 高质量音频
- **仅支持英语** – 未来将支持更多语言

---

## 安装

```bash
pip install pocket-tts
# or
uv add pocket-tts
```

---

## 命令行接口（CLI）命令

### 生成语音

```bash
# Basic generation (default voice)
pocket-tts generate --text "Hello world"

# Custom voice (local file, URL, or safetensors)
pocket-tts generate --voice ./my_voice.wav
pocket-tts generate --voice "hf://kyutai/tts-voices/alba-mackenna/casual.wav"
pocket-tts generate --voice ./voice.safetensors

# Quality tuning
pocket-tts generate --temperature 0.7 --lsd-decode-steps 3
```

请参阅`docs/generate.md`以获取完整的CLI使用说明。

### 启动Web服务器

```bash
# Start FastAPI server with web UI
pocket-tts serve

# Custom host/port
pocket-tts serve --host localhost --port 8080
```

请参阅`docs/serve.md`以了解服务器配置选项。

### 导出语音嵌入文件

将音频文件转换为`.safetensors`格式，以便更快地加载：

```bash
# Single file
pocket-tts export-voice voice.mp3 voice.safetensors

# Batch conversion
pocket-tts export-voice voices/ embeddings/ --truncate
```

请参阅`docs/export_voice.md`以获取导出选项。

---

## Python API

### 基本用法

```python
from pocket_tts import TTSModel
import scipy.io.wavfile

# Load model
model = TTSModel.load_model()

# Get voice state
voice = model.get_state_for_audio_prompt(
    "hf://kyutai/tts-voices/alba-mackenna/casual.wav"
)

# Generate audio
audio = model.generate_audio(voice, "Hello world!")

# Save
scipy.io.wavfile.write("output.wav", model.sample_rate, audio.numpy())
```

### 加载模型

```python
model = TTSModel.load_model(
    config="b6369a24",       # Model variant
    temp=0.7,                # Temperature (0.5-1.0)
    lsd_decode_steps=1,      # Generation steps (1-5)
    eos_threshold=-4.0       # End-of-sequence threshold
)
```

### 管理语音状态

```python
# From audio file/URL
voice = model.get_state_for_audio_prompt("./voice.wav")
voice = model.get_state_for_audio_prompt("hf://kyutai/tts-voices/alba-mackenna/casual.wav")

# From safetensors (fast loading)
voice = model.get_state_for_audio_prompt("./voice.safetensors")
```

### 实时语音生成

```python
# Stream audio chunks
for chunk in model.generate_audio_stream(voice, "Long text..."):
    # Process/save/play each chunk as generated
    print(f"Chunk: {chunk.shape[0]} samples")
```

### 多语音管理

```python
# Preload multiple voices
voices = {
    "casual": model.get_state_for_audio_prompt("hf://kyutai/tts-voices/alba-mackenna/casual.wav"),
    "announcer": model.get_state_for_audio_prompt("./announcer.safetensors"),
}

# Use different voices
audio1 = model.generate_audio(voices["casual"], "Hey there!")
audio2 = model.generate_audio(voices["announcer"], "Breaking news!")
```

请参阅`docs/python-api.md`以获取完整的API文档。

---

## 可用语音

预制作的语音资源来自`hf://kyutai/tts-voices/`：

- `alba-mackenna/casual.wav`（默认女性声音）
- `jessica-jian/casual.wav`（女性声音）
- `voice-donations/Selfie.wav`（男性声音，Marius）
- `voice-donations/Butter.wav`（男性声音，Javert）
- `ears/p010/freeform_speech_01.wav`（男性声音，Jean）
- `vctk/p244_023.wav`（女性声音，Fantine）
- `vctk/p262_023.wav`（女性声音，Eponine）
- `vctk/p303_023.wav`（女性声音，Azelma）

您也可以根据自己的音频样本克隆新的语音。

---

## 语音克隆技巧

- **音频质量** – 清除背景噪音（建议使用[Adobe Podcast Enhance](https://podcast.adobe.com/en/enhance)工具）
- **音频长度** – 3到10秒的音频片段最为理想
- **音频质量** – 输入音频的质量会直接影响输出效果
- **支持的音频格式** – WAV、MP3或其他常见音频格式

---

## 性能优化技巧

- **仅使用CPU** – 由于模型体积小，GPU无法提供加速效果（批量处理数量为1）
- **高效利用CPU核心** – 仅使用2个CPU核心
- **低延迟** – 从开始到输出第一段音频数据的延迟小于200毫秒
- **预处理音频** – 将音频文件转换为`.safetensors`格式，以便快速加载

---

## 输出格式

所有命令生成的音频文件均为WAV格式：
- **采样率**：24 kHz
- **声道**：单声道
- **位深度**：16位PCM

---

## 相关链接

- [GitHub仓库](https://github.com/kyutai-labs/pocket-tts)
- [技术报告](https://kyutai.org/blog/2026-01-13-pocket-tts)
- [学术论文（arXiv链接）](https://arxiv.org/abs/2509.06926)
- [HuggingFace模型页面](https://huggingface.co/kyutai/pocket-tts)
- **语音资源库**：[https://huggingface.co/kyutai/tts-voices]
- **在线演示**：[https://kyutai.org/pocket-tts]