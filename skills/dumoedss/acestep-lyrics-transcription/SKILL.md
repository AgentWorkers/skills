---
name: acestep-lyrics-transcription
description: 使用 OpenAI Whisper 或 ElevenLabs Scribe API 将音频转录为带有时间戳的歌词。输出格式可以是 LRC、SRT 或 JSON，其中包含单词级别的时间戳。该功能适用于用户需要将歌曲转录为歌词、生成 LRC 文件或从音频中提取带有时间戳的歌词的场景。
allowed-tools: Read, Write, Bash
---

# 歌词转录功能

通过 OpenAI Whisper 或 ElevenLabs Scribe API，将音频文件转录为带有时间戳的歌词（格式为 LRC/SRT/JSON）。

## API 密钥设置指南

**在开始转录之前，必须确认用户的 API 密钥是否已配置。** 运行以下命令进行检查：

```bash
cd "{project_root}/{.claude or .codex}/skills/acestep-lyrics-transcription/" && bash ./scripts/acestep-lyrics-transcription.sh config --check-key
```

该命令仅会显示当前使用的提供者的 API 密钥是否已设置或为空，并不会显示实际的密钥值。**切勿查看或显示用户的 API 密钥内容。** 不要在配置字段中使用 `config --get` 命令，也不要直接读取 `config.json` 文件。`config --list` 命令是安全的，因为它会在输出中将 API 密钥自动替换为 `***`。

**如果命令显示密钥为空**，必须停止操作并指导用户先进行配置。**在没有有效密钥的情况下尝试转录会导致失败。**

使用 `AskUserQuestion` 功能向用户请求提供他们的 API 密钥，并提供以下选项和指导：
1. 告知用户当前使用的提供者（openai 或 elevenlabs）以及其 API 密钥尚未配置。解释没有密钥则无法继续转录。
2. 提供获取密钥的明确说明：
   - **OpenAI**：在 https://platform.openai.com/api-keys 获取 API 密钥——需要启用计费的 OpenAI 账户。Whisper API 的费用约为每分钟 0.006 美元。
   - **ElevenLabs**：在 https://elevenlabs.io/app/settings/api-keys 获取 API 密钥——需要 ElevenLabs 账户。免费套餐包含有限的信用额度。
3. 如果用户已经拥有另一个提供者的密钥，也可以提供切换提供者的选项。
4. 用户提供密钥后，使用以下命令进行配置：
   ```bash
   cd "{project_root}/{.claude or .codex}/skills/acestep-lyrics-transcription/" && bash ./scripts/acestep-lyrics-transcription.sh config --set <provider>.api_key <KEY>
   ```
5. 如果用户希望更换提供者，还需运行以下命令：
   ```bash
   cd "{project_root}/{.claude or .codex}/skills/acestep-lyrics-transcription/" && bash ./scripts/acestep-lyrics-transcription.sh config --set provider <provider_name>
   ```
6. 配置完成后，重新运行 `config --check-key` 命令以确认密钥已正确设置，然后再继续操作。

**如果 API 密钥已经配置完成**，可以直接进行转录。

## 快速入门

```bash
# 1. cd to this skill's directory
cd {project_root}/{.claude or .codex}/skills/acestep-lyrics-transcription/

# 2. Configure API key (choose one)
./scripts/acestep-lyrics-transcription.sh config --set openai.api_key sk-...
# or
./scripts/acestep-lyrics-transcription.sh config --set elevenlabs.api_key ...
./scripts/acestep-lyrics-transcription.sh config --set provider elevenlabs

# 3. Transcribe
./scripts/acestep-lyrics-transcription.sh transcribe --audio /path/to/song.mp3 --language zh

# 4. Output saved to: {project_root}/acestep_output/<filename>.lrc
```

## 先决条件

- curl、jq、python3（或 python）
- OpenAI 或 ElevenLabs 的 API 密钥

## 脚本使用方法

```bash
./scripts/acestep-lyrics-transcription.sh transcribe --audio <file> [options]

Options:
  -a, --audio      Audio file path (required)
  -l, --language   Language code (zh, en, ja, etc.)
  -f, --format     Output format: lrc, srt, json (default: lrc)
  -p, --provider   API provider: openai, elevenlabs (overrides config)
  -o, --output     Output file path (default: acestep_output/<filename>.lrc)
```

## 转录后的歌词校正（必选）

**重要提示**：**转录完成后，必须手动校正 LRC 文件才能将其用于音乐视频（MV）的渲染。** 转录模型经常会在歌词上产生错误：
- 名词：例如 “ACE-Step” 应改为 “AC step”，“Spotify” 应改为 “spot a fly”；
- 发音相似的单词：例如 “arrives” 应改为 “eyes”，“open source” 应改为 “open sores”；
- 合并或拆分的单词：例如 “lighting up” 应改为 “lightin' nup”。

### 校正流程

1. 使用 Read 工具读取转录后的 LRC 文件。
2. 从 ACE-Step 的输出 JSON 文件中读取原始歌词。
3. **以原始歌词为参考**：不要尝试逐行对齐——转录结果可能会与原始歌词在行数、顺序上有所不同。应先完整阅读原始歌词以理解正确的表达方式，然后逐行检查 LRC 文件中的内容，并根据对原始歌词的了解修正错误的单词。
4. **修正转录错误**：用正确的原始单词替换错误的单词，同时保持时间戳不变。
5. 使用 Write 工具将校正后的 LRC 文件写回。

### 需要校正的内容

- 用正确的原始单词替换错误的单词。
- 保持所有 `[MM:SS.cc]` 时间戳不变（转录生成的时间戳是准确的）。
- 不要添加 `[Verse]` 或 `[Chorus]` 等结构标签——LRC 文件中应仅包含带有时间戳的文本行。

### 示例

**转录结果（错误）：**
```
[00:46.96]AC step alive,
[00:50.80]one point five eyes.
```

**原始歌词参考：**
```
ACE-Step alive
One point five arrives
```

**校正后的结果：**
```
[00:46.96]ACE-Step alive,
[00:50.80]One point five arrives.
```

## 配置文件

配置文件：`scripts/config.json`

```bash
# Switch provider
./scripts/acestep-lyrics-transcription.sh config --set provider openai
./scripts/acestep-lyrics-transcription.sh config --set provider elevenlabs

# Set API keys
./scripts/acestep-lyrics-transcription.sh config --set openai.api_key sk-...
./scripts/acestep-lyrics-transcription.sh config --set elevenlabs.api_key ...

# View config
./scripts/acestep-lyrics-transcription.sh config --list
```

| 选项 | 默认值 | 说明 |
|--------|---------|-------------|
| `provider` | `openai` | 当前使用的提供者（openai 或 elevenlabs） |
| `output_format` | `lrc` | 默认输出格式：lrc、srt 或 json |
| `openai.api_key` | `""` | OpenAI API 密钥 |
| `openai.api_url` | `https://api.openai.com/v1` | OpenAI API 的基础 URL |
| `openai.model` | `whisper-1` | OpenAI 模型（用于生成单词时间戳） |
| `elevenlabs.api_key` | `""` | ElevenLabs API 密钥 |
| `elevenlabs.api_url` | `https://api.elevenlabs.io/v1` | ElevenLabs API 的基础 URL |
| `elevenlabs.model` | `scribe_v2` | ElevenLabs 模型 |

## 提供者相关信息

| 提供者 | 模型 | 是否支持单词时间戳 | 定价 |
|---------|-------|-----------------|---------|
| OpenAI | whisper-1 | 支持（分段和时间戳） | 每分钟 0.006 美元 |
| ElevenLabs | scribe_v2 | 支持（单词级别时间戳） | 根据套餐不同而异 |

- OpenAI 的 `whisper-1` 是唯一支持单词级别时间戳的 OpenAI 模型。
- ElevenLabs 的 `scribe_v2` 可生成单词级别的时间戳，并支持类型过滤。
- 两者都支持多语言转录。

## 示例
```bash
# Basic transcription (uses config defaults)
./scripts/acestep-lyrics-transcription.sh transcribe --audio song.mp3

# Chinese song to LRC
./scripts/acestep-lyrics-transcription.sh transcribe --audio song.mp3 --language zh

# Use ElevenLabs, output SRT
./scripts/acestep-lyrics-transcription.sh transcribe --audio song.mp3 --provider elevenlabs --format srt

# Custom output path
./scripts/acestep-lyrics-transcription.sh transcribe --audio song.mp3 --output ./my_lyrics.lrc
```