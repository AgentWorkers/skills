---
name: local-llama-tts
description: 使用 llama-tts（llama.cpp）和 OuteTTS-1.0-0.6B 模型进行本地文本转语音功能。
metadata:
  {
    "openclaw":
      {
        "emoji": "🔊",
        "requires": { "bins": ["llama-tts"] },
      },
  }
---
# 本地Llama TTS

使用`llama-tts`和`OuteTTS-1.0-0.6B`模型在本地合成语音。

## 使用方法

您可以使用以下脚本：
- `scripts/tts-local.sh [选项] "<文本>"`

### 选项
- `-o, --output <文件>`：输出WAV文件（默认：`output.wav`）
- `-s, --speaker <文件>`：说话者参考文件（可选）
- `-t, --temp <值>`：温度参数（默认：`0.4`）

## 脚本

- **位置：** `scripts/tts-local.sh`（位于`skill`文件夹内）
- **模型：** `/data/public/machine-learning/models/text-to-speach/OuteTTS-1.0-0.6B-Q4_K_M.gguf`
- **语音合成器：** `/data/public/machine-learning/models/text-to-speach/WavTokenizer-Large-75-Q4_0.gguf`
- **GPU：** 通过`llama-tts`启用

## 设置

1. **模型：** 从[OuteAI/OuteTTS-1.0-0.6B-GGUF](https://huggingface.co/OuteAI/OuteTTS-1.0-0.6B-GGUF/resolve/main/OuteTTS-1.0-0.6B-Q4_K_M.gguf?download=true)下载
2. **语音合成器：** 从[ggml-org/WavTokenizer](https://huggingface.co/ggml-org/WavTokenizer/resolve/main/WavTokenizer-Large-75-Q5_1.gguf?download=true)下载（注：Felix使用的是Q4_0版本，此处提供Q5_1作为高质量替代选项）

将文件放置在`/data/public/machine-learning/models/text-to-speach/`目录中，或更新`scripts/tts-local.sh`脚本。

## 采样配置
模型卡片推荐以下配置（在脚本中已硬编码）：
- **温度参数（Temperature）：** 0.4
- **重复惩罚（Repetition Penalty）：** 1.1
- **重复范围（Repetition Range）：** 64
- **前k个结果（Top-k）：** 40
- **前p个结果（Top-p）：** 0.9
- **最小概率（Min-p）：** 0.05