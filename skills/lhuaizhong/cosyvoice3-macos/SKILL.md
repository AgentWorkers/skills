---
name: cosyvoice3
description: >
  在 macOS 的 Apple Silicon 平台上，使用阿里巴巴的 CosyVoice3 实现本地文本转语音（TTS）功能。  
  支持中文、英文、日文、韩文以及 18 种以上的中文方言。  
  具备零样本语音克隆、跨语言合成以及精细的语音控制功能。  
  适用场景：  
  (1) 用户需要高质量的中文/英文语音进行本地文本转语音服务。  
  (2) 需要从参考音频中克隆语音。  
  (3) 需要离线或推理式的语音生成功能。  
  (4) 用户希望获得具有情感表达和方言特色的自然语音效果。
---
# CosyVoice3 语音合成工具

这是一个基于阿里巴巴的 CosyVoice3 技术的本地文本到语音（TTS）工具，专为 macOS 上的 Apple Silicon 处理器设计。

## 概述

CosyVoice3 是一个先进的语音合成系统，支持以下功能：
- **9 种语言**：中文、英文、日文、韩文、德文、西班牙文、法文、意大利文、俄文
- **18 种以上的中文方言**：粤语、四川话、东北话、上海话等
- **零样本语音克隆**：仅需 3-10 秒的音频即可克隆出新的语音
- **跨语言合成**：可以使用英语语音合成中文内容，或反之亦然
- **精细控制**：通过文本标签来调整语音的情感、语速和音量

## 先决条件

- 安装了 Apple Silicon（M1/M2/M3）版本的 macOS
- 安装了 Python 3.10
- 安装了 Conda
- 硬盘空间至少需 5GB 用于存储模型文件

## 安装步骤

运行安装脚本：

```bash
cd /Users/lhz/.openclaw/workspace/skills/cosyvoice3/scripts
bash install.sh
```

安装过程将完成以下操作：
1. 创建名为 `cosyvoice` 的 Conda 环境
2. 安装适用于 Apple Silicon 的 PyTorch（CPU 版本）
3. 安装 CosyVoice 所需的依赖库
4. 下载预训练的 Fun-CosyVoice3-0.5B 模型（约 2GB 大小）

## 使用方法

### 快速入门 - 基本语音合成

**注意**：在使用 CosyVoice3 时，需要在文本前添加 `<|endofprompt|>` 标签！

```bash
cd /Users/lhz/.openclaw/workspace/cosyvoice3-repo
export PATH="$HOME/miniconda3/bin:$PATH"
conda activate cosyvoice

python -c "
import sys
sys.path.append('third_party/Matcha-TTS')
from cosyvoice.cli.cosyvoice import AutoModel
import torchaudio

cosyvoice = AutoModel(model_dir='pretrained_models/Fun-CosyVoice3-0.5B')
for i, j in enumerate(cosyvoice.inference_zero_shot(
    '你好，这是CosyVoice3语音合成测试。', 
    '希望你以后能够做的比我还好呦。<|endofprompt|>',  # 注意这个标记！
    'asset/zero_shot_prompt.wav'
)):
    torchaudio.save('output.wav', j['tts_speech'], cosyvoice.sample_rate)
print('Generated: output.wav')
"
```

### 使用语音合成脚本

通过脚本将文本转换为语音：

```bash
cd /Users/lhz/.openclaw/workspace/skills/cosyvoice3/scripts
conda activate cosyvoice

# Basic TTS with default voice
python tts.py "你好，这是一个测试。"

# With custom reference audio for voice cloning
python tts.py "你好，这是克隆的声音。" --reference /path/to/reference.wav

# Cross-lingual (English text with Chinese voice)
python tts.py "Hello, this is cross-lingual synthesis." --reference asset/zero_shot_prompt.wav --lang en

# With speed control
python tts.py "这是一段快速的语音。" --speed 1.5

# Save to specific path
python tts.py "你好。" --output ~/Desktop/greeting.wav
```

### 可用资源

相关音频文件位于 `cosyvoice3-repo/asset/` 目录下：
- `zero_shot_prompt.wav` - 默认的中文女性语音样本
- `cross_lingual_prompt.wav` - 用于跨语言合成的英文提示音

## 高级功能

### 语音克隆

根据 3-10 秒的参考音频克隆新的语音：

```python
from cosyvoice.cli.cosyvoice import AutoModel
import torchaudio

cosyvoice = AutoModel(model_dir='pretrained_models/Fun-CosyVoice3-0.5B')

# Clone voice and generate
for i, j in enumerate(cosyvoice.inference_zero_shot(
    '这是克隆后的声音在说话。',
    'Reference text transcription',
    '/path/to/reference.wav'
)):
    torchaudio.save('cloned.wav', j['tts_speech'], cosyvoice.sample_rate)
```

### 精细控制

使用特殊标签来精确控制语音的韵律和表达：

```python
# Add laughter
"他突然[laughter]笑了起来[laughter]。"

# Add breathing
"他说完这句话[breath]，深吸一口气。"

# Strong emphasis
"这是<strong>非常重要</strong>的。"

# Combined
"在面对挑战时，他展现了非凡的<strong>勇气</strong>与<strong>智慧</strong>[breath]。"
```

### 方言支持

针对特定方言，可以使用相应的指令模式进行合成：

```python
cosyvoice = AutoModel(model_dir='pretrained_models/CosyVoice-300M-Instruct')

for i, j in enumerate(cosyvoice.inference_instruct(
    '你好，这是测试语音。',
    '中文男',
    '用四川话说这句话<|endofprompt|>'
)):
    torchaudio.save('sichuan.wav', j['tts_speech'], cosyvoice.sample_rate)
```

## 常见问题解决方法

### 模型未找到

如果出现“模型未找到”的错误，请手动下载模型文件：

```bash
cd /Users/lhz/.openclaw/workspace/cosyvoice3-repo
export PATH="$HOME/miniconda3/bin:$PATH"
conda activate cosyvoice

python -c "
from modelscope import snapshot_download
snapshot_download('FunAudioLLM/Fun-CosyVoice3-0.5B-2512', local_dir='pretrained_models/Fun-CosyVoice3-0.5B')
"
```

### 内存问题

对于较长的文本，建议将其拆分成多个句子进行处理：

```python
text = "很长的文本..."
sentences = text.split('。')
for sent in sentences:
    if sent.strip():
        # Process each sentence
```

### 音频格式要求

参考音频文件应符合以下格式：
- 格式：WAV 或 MP3
- 样本率：16kHz 或更高（系统会自动进行重采样）
- 时长：建议为 3-10 秒
- 内容：语音清晰，背景噪音尽可能低

## 相关资源

### 脚本

- `install.sh`：macOS 安装脚本
- `tts.py`：提供 CLI 接口的主要语音合成脚本
- `download_models.py`：用于下载预训练模型的脚本

### 参考资料

- [CosyVoice 的 GitHub 仓库](https://github.com/FunAudioLLM/CosyVoice)
- [Fun-CosyVoice3 的演示页面](https://funaudiollm.github.io/cosyvoice3/)

### 模型文件位置

模型文件存储在 `cosyvoice3-repo/pretrained_models/` 目录下：
- `Fun-CosyVoice3-0.5B`：推荐使用的模型
- `CosyVoice2-0.5B`：旧版本
- `CosyVoice-300M`：轻量级模型
- `CosyVoice-300M-SFT`：SFT（Soft Fusion）版本
- `CosyVoice-300M-Instruct`：支持指令控制的版本

## 注意事项

- 首次推理可能需要约 30 秒（模型预热时间）
- 后续推理速度会更快
- Apple Silicon 使用 CPU 进行计算（不支持 CUDA）
- 在 M 系列处理器上的实时合成效果约为 0.3-0.5
- 模型文件在首次下载后会缓存到本地