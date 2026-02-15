# Pocket TTS 技能

这是一个完全基于本地的离线文本转语音（TTS）工具，使用 Kyutai 的 Pocket TTS 模型。无需任何 API 调用或网络连接即可将文本转换为高质量音频。该工具支持 8 种内置语音、语音克隆功能，并且完全在 CPU 上运行。

## 特点

- 🎯 **完全本地化**：无需 API 调用，完全离线运行
- 🚀 **仅依赖 CPU**：无需 GPU，可在任何计算机上使用
- ⚡ **快速生成**：在 CPU 上的生成速度约为实时的 2-6 倍
- 🎤 **8 种内置语音**：alba、marius、javier、jean、fantine、cosette、eponine、azelma
- 🎭 **语音克隆**：可以从 WAV 样本中克隆任意语音
- 🔊 **低延迟**：首次生成音频片段的时间约为 200 毫秒
- 📚 **简单的 Python API**：易于集成到任何项目中

## 安装

```bash
# 1. Accept the model license on Hugging Face
# https://huggingface.co/kyutai/pocket-tts

# 2. Install the package
pip install pocket-tts

# Or use uv for automatic dependency management
uvx pocket-tts generate "Hello world"
```

## 使用方法

### 命令行界面 (CLI)

```bash
# Basic usage
pocket-tts "Hello, I am your AI assistant"

# With specific voice
pocket-tts "Hello" --voice alba --output hello.wav

# With custom voice file (voice cloning)
pocket-tts "Hello" --voice-file myvoice.wav --output output.wav

# Adjust speed
pocket-tts "Hello" --speed 1.2

# Start local server
pocket-tts --serve

# List available voices
pocket-tts --list-voices
```

### Python API

```python
from pocket_tts import TTSModel
import scipy.io.wavfile

# Load model
tts_model = TTSModel.load_model()

# Get voice state
voice_state = tts_model.get_state_for_audio_prompt(
    "hf://kyutai/tts-voices/alba-mackenna/casual.wav"
)

# Generate audio
audio = tts_model.generate_audio(voice_state, "Hello world!")

# Save to WAV
scipy.io.wavfile.write("output.wav", tts_model.sample_rate, audio.numpy())

# Check sample rate
print(f"Sample rate: {tts_model.sample_rate} Hz")
```

## 可用语音

| 语音 | 描述 |
|-------|-------------|
| alba | 休闲女性语音 |
| marius | 男性语音 |
| javert | 清晰的男性语音 |
| jean | 自然男性语音 |
| fantine | 女性语音 |
| cosette | 女性语音 |
| eponine | 女性语音 |
| azelma | 女性语音 |

或者使用 `--voice-file /path/to/wav.wav` 来克隆自定义语音。

## 选项

| 选项 | 描述 | 默认值 |
|--------|-------------|---------|
| `text` | 需要转换的文本 | 必填 |
| `-o, --output` | 输出 WAV 文件 | `output.wav` |
| `-v, --voice` | 语音预设 | `alba` |
| `-s, --speed` | 语音速度（0.5-2.0） | `1.0` |
| `--voice-file` | 用于克隆的自定义 WAV 文件 | 无 |
| `--serve` | 启动 HTTP 服务器 | 否 |
| `--list-voices` | 列出所有语音 | 否 |

## 系统要求

- Python 3.10-3.14
- PyTorch 2.5 或更高版本（支持 CPU 版本）
- 需要至少 2 个 CPU 核心

## 注意事项

- ⚠️ 该模型受 Hugging Face 许可证限制，使用前请先获取许可证
- 🌍 仅支持英语语言（版本 1）
- 💾 首次运行时会下载模型数据（约 100MB 参数）
- 🔊 音频以 1D torch 张量（PCM 数据）的形式返回

## 链接

- [演示](https://kyutai.org/tts)
- [GitHub 仓库](https://github.com/kyutai-labs/pocket-tts)
- [Hugging Face 页面](https://huggingface.co/kyutai/pocket-tts)
- [论文](https://arxiv.org/abs/2509.06926)