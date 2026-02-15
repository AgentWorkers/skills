---
name: qwen-tts
description: 使用 Qwen3-TTS-12Hz-1.7B-CustomVoice 进行本地文本转语音（Text-to-Speech, TTS）操作。适用于从文本生成音频、创建语音消息或满足语音转文本需求。支持 10 种语言，包括意大利语；提供 9 种高品质的扬声器语音效果；同时支持基于指令的语音控制（如调整情感、语调和风格）。作为 ElevenLabs 等基于云的 TTS 服务的替代方案，该工具在初次下载模型后即可完全离线使用。
---

# Qwen TTS

使用 Hugging Face 的 Qwen3-TTS-12Hz-1.7B-CustomVoice 模型实现本地文本转语音功能。

## 快速入门

**将文本转换为语音：**
```bash
scripts/tts.py "Ciao, come va?" -l Italian -o output.wav
```

**通过语音指令（表达情感/风格）：**
```bash
scripts/tts.py "Sono felice!" -i "Parla con entusiasmo" -l Italian -o happy.wav
```

**更换说话者：**
```bash
scripts/tts.py "Hello world" -s Ryan -l English -o hello.wav
```

## 安装

**首次设置**（仅需执行一次）：
```bash
cd skills/public/qwen-tts
bash scripts/setup.sh
```

此操作会创建一个本地虚拟环境并安装 `qwen-tts` 包（大小约为 500MB）。

**注意：** 首次使用时会自动从 Hugging Face 下载约 1.7GB 的模型文件。

## 使用方法

```bash
scripts/tts.py [options] "Text to speak"
```

### 参数说明

- `-o, --output PATH`  - 输出文件路径（默认：qwen_output.wav）
- `-s, --speaker NAME`  - 说话者声音（默认：Vivian）
- `-l, --language LANG`  - 语言（默认：自动选择）
- `-i, --instruct TEXT`  - 语音指令（表达情感、风格、语调）
- `--list-speakers`  - 显示可用的说话者列表
- `--model NAME`  - 模型名称（默认：CustomVoice 1.7B）

### 示例

- **基础意大利语语音：**
```bash
scripts/tts.py "Benvenuto nel futuro del text-to-speech" -l Italian -o welcome.wav
```

- **带有情感/指令的语音：**
```bash
scripts/tts.py "Sono molto felice di vederti!" -i "Parla con entusiasmo e gioia" -l Italian -o happy.wav
```

- **更换说话者：**
```bash
scripts/tts.py "Hello, nice to meet you" -s Ryan -l English -o ryan.wav
```

- **查看可用说话者列表：**
```bash
scripts/tts.py --list-speakers
```

## 可用说话者

CustomVoice 模型包含 9 种高级语音效果：

| 说话者 | 语言 | 说明 |
|---------|----------|-------------|
| Vivian | 中文 | 明亮、略带活力的年轻女性声音 |
| Serena | 中文 | 温暖、温柔的年轻女性声音 |
| Uncle_Fu | 中文 | 经验丰富的男性声音，音色低沉醇厚 |
| Dylan | 中文（北京口音） | 青春的北京男性声音，发音清晰 |
| Eric | 中文（四川口音） | 活泼的成都男性声音，音调略带沙哑 |
| Ryan | 英文 | 动感有力的男性声音 |
| Aiden | 英文 | 阳光般的美国男性声音 |
| Ono_Anna | 日文 | 活泼的女性声音，语调轻快 |
| Sohee | 韩文 | 温暖的女性声音，情感表达丰富 |

**建议：** 使用与说话者对应的语言以获得最佳音质；不过所有说话者都支持中文、英文、日文、韩文、德文、法文、俄文、葡萄牙文、西班牙文和意大利文。

## 语音指令

使用 `-i, --instruct` 参数来控制语音的情感、语调和风格：

**意大利语示例：**
- `"Parla con entusiasmo"` （以热情的方式说话）
- `"Tono serio e professionale"` （用严肃专业的音调）
- `"Voce calma e rilassante"` （用平静舒缓的语调）
- `"Leggi come un narratore"` （像叙述者一样朗读）

**英文示例：**
- `"Speak with excitement"` （充满激情地说话）
- `"Very happy and energetic"` （非常开心且充满活力）
- `"Calmo e soothing voice"` （声音平静且令人放松）
- `"Read like a narrator"` （像叙述者一样朗读）

## 与 OpenClaw 的集成

脚本会将音频文件路径输出到标准输出（stdout），从而可以与 OpenClaw 的文本转语音流程无缝集成：
```bash
# OpenClaw captures the output path
cd skills/public/qwen-tts
OUTPUT=$(scripts/tts.py "Ciao" -s Vivian -l Italian -o /tmp/audio.wav 2>/dev/null)
# OUTPUT = /tmp/audio.wav
```

## 性能

- **GPU（CUDA）：** 短语句的转换时间约为 1-3 秒
- **CPU：** 短语句的转换时间约为 10-30 秒
- **模型大小：** 约 1.7GB（首次运行时会自动下载）
- **虚拟环境大小：** 约 500MB（包含安装的依赖库）

## 常见问题及解决方法

- **设置失败：**
```bash
# Ensure Python 3.10-3.12 is available
python3.12 --version

# Re-run setup
cd skills/public/qwen-tts
rm -rf venv
bash scripts/setup.sh
```

- **模型下载缓慢/失败：**
```bash
# Use mirror (China mainland)
export HF_ENDPOINT=https://hf-mirror.com
scripts/tts.py "Test" -o test.wav
```

- **GPU 内存不足：** 如果 GPU 内存不足，系统会自动切换到 CPU 运行模型。

- **音频质量问题：**
  - 尝试更换说话者：`--list-speakers`
  - 添加语音指令：`-i "Speak clearly and slowly"`（请清晰缓慢地说话）
  - 确保语言设置与文本匹配：例如，使用 `-l Italian` 来处理意大利语文本

## 模型详情

- **模型名称：** Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice
- **来源：** Hugging Face（https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice）
- **许可证：** 请查看模型卡片以获取最新的许可条款
- **采样率：** 16kHz
- **输出格式：** WAV（未压缩格式）