---
name: mm-easy-voice
description: 使用 MiniMax Voice API 的简单文本转语音功能：可将文本转换为音频，并支持自定义语音选择。适用于从文本生成语音音频的场景。
---
# MiniMax Easy Voice

这是一个基于 MiniMax Voice API 的简单文本转语音（TTS）技能，可以将任何文本转换为自然音色的音频，并支持自定义语音选择。

## 使用方法
### [步骤 1] 准备工作

**重要提示：** 在使用此技能之前，请务必验证环境配置：

```bash
python check_environment.py
```

**如果 API 密钥未设置：**
```bash
export MINIMAX_VOICE_API_KEY="your-api-key-here"
```

**系统要求：**
- Python 3.8 或更高版本
- 必须设置 `MINIMAX_VOICE_API_KEY` 环境变量
- FFmpeg（可选，用于音频合并/转换）

### [步骤 2] 通过命令将文本转换为语音

只需一条命令即可将文本转换为语音：

```bash
# Default voice (male-qn-qingse)
python mmvoice.py tts "Hello, this is a test." -o test.mp3

# Chinese text
python mmvoice.py tts "你好，这是一个测试。" -o test_cn.mp3

# Specify a different voice by "-v voice_id"
python mmvoice.py tts "Hello world" -v female-shaonv -o hello.mp3

# Specify output path
python mmvoice.py tts "Your text" -o /path/to/output.mp3
```

**必需参数：**
- `text`：要转换为语音的文本
- `-o OUTPUT`：输出音频文件的路径（必需）

**可选参数：**
- `-v VOICE_ID`：要使用的语音（默认值：male-qn-qingse）

### 使用细节

- **文本长度限制：** 每次请求最多支持 10,000 个字符。
- 如果文本过长，可以分成多个请求并稍后合并。

- **暂停插入：** 使用 `<#x#>` 标记暂停位置（x 代表暂停时长，单位为秒）。例如：`"Hello<#1.5#>world"` 表示单词之间有 1.5 秒的暂停。
- 暂停时长范围：0.01 到 99.99 秒。

- **情感匹配：** speech-2.8 模型会自动根据文本内容匹配相应的情感。

## 语音选择

请参考语音目录来选择适合您内容的语音：

```bash
# List all available voices
python mmvoice.py list-voices
```

**语音目录：`reference/voice_catalog.md`**
- 包含所有可用的系统语音（男声、女声）
- 语音特性及推荐使用场景
- 如何为内容选择合适的语音

## 高级选项

### 语音管理

- **查看可用语音：**
```bash
python mmvoice.py list-voices
```

- **从音频样本克隆语音：**
```bash
python mmvoice.py clone audio_file.mp3 --voice-id my-custom-voice
```

- **根据描述创建新语音：**
```bash
python mmvoice.py design "A warm, gentle female voice" --voice-id designed-voice
```

### 音频处理

- **合并多个音频文件：**
```bash
python mmvoice.py merge file1.mp3 file2.mp3 file3.mp3 -o combined.mp3
```

- **转换音频格式：**
```bash
python mmvoice.py convert input.wav -o output.mp3 --format mp3
```

## 参考文档

如需更多详细信息，请查阅以下文档：

| 文档 | 使用场景 |
|---------|-------------|
| `reference/voice_catalog.md` | 选择合适的语音 ID |
| `reference/getting-started.md` | 环境配置指南 |
| `reference/audio-guide.md` | 音频处理相关内容 |
| `reference/voice-guide.md` | 语音克隆与创建方法 |
| `reference/troubleshooting.md` | 常见问题及解决方法 |

## 常见问题与解决方法

- **API 密钥未设置：** 运行 `export MINIMAX_VOICE_API_KEY="your-key"` 命令进行设置。
- **FFmpeg 未安装：** 在 macOS 上使用 `brew install ffmpeg`，在 Ubuntu 上使用 `sudo apt install ffmpeg` 安装。
- **找不到所需语音：** 使用 `python mmvoice.py list-voices` 命令查看可用语音列表。

运行环境检查：
```bash
python check_environment.py
```

如需更多解决方案，请参阅 `reference/troubleshooting.md`。