---
name: elevenlabs
description: 通过 ElevenLabs API 实现文本转语音、音效生成、音乐制作、语音管理以及配额检查等功能。在利用 ElevenLabs 生成音频或管理语音资源时，请使用这些功能。
metadata: {"clawdbot":{"requires":{"bins":["python3"],"env":["ELEVENLABS_API_KEY"]},"primaryEnv":"ELEVENLABS_API_KEY"}}
---

# ElevenLabs Skill

这是一套用于与 ElevenLabs API 交互的核心工具，支持声音生成、音乐处理和语音管理功能。

## 设置

运行这些工具需要将 `ELEVENLABS_API_KEY` 环境变量设置为有效的 API 密钥。

## 输出格式

所有脚本都支持通过 `--format` 参数选择多种输出格式：

| 格式 | 描述 |
|--------|-------------|
| `mp3_44100_128` | MP3 格式，44.1kHz 频率，128kbps 流量（默认格式） |
| `mp3_44100_192` | MP3 格式，44.1kHz 频率，192kbps 流量 |
| `pcm_16000` | 原始 PCM 格式，16kHz 频率 |
| `pcm_22050` | 原始 PCM 格式，22.05kHz 频率 |
| `pcm_24000` | 原始 PCM 格式，24kHz 频率 |
| `pcm_44100` | 原始 PCM 格式，44.1kHz 频率 |
| `ulaw_8000` | μ-law 格式，8kHz 频率（适用于电话通信） |

## 工具列表

### 1. Speech (`speech.py`)
使用 ElevenLabs 提供的语音库将文本转换为语音。

```bash
# Basic usage
python3 {baseDir}/scripts/speech.py "Hello world" -v <voice_id> -o output.mp3

# With format option
python3 {baseDir}/scripts/speech.py "Hello world" -v <voice_id> -o output.pcm --format pcm_44100

# With voice settings
python3 {baseDir}/scripts/speech.py "Hello" -v <voice_id> -o out.mp3 --stability 0.7 --similarity 0.8
```

### 2. Sound Effects (`sfx.py`)
生成音效和简短的音频片段。

```bash
# Generate a sound
python3 {baseDir}/scripts/sfx.py "Cinematic boom" -o boom.mp3

# Generate a loop
python3 {baseDir}/scripts/sfx.py "Lo-fi hip hop beat" --duration 10 --loop -o beat.mp3

# Different format
python3 {baseDir}/scripts/sfx.py "Whoosh" -o whoosh.pcm --format pcm_44100
```

### 3. Music Generation (`music.py`)
创作完整的音乐作品或器乐曲目。

```bash
# Generate instrumental intro
python3 {baseDir}/scripts/music.py --prompt "Upbeat 6s news intro sting, instrumental" --length-ms 6000 -o intro.mp3

# Generate background bed
python3 {baseDir}/scripts/music.py --prompt "Soft ambient synth pad" --length-ms 30000 -o bed.mp3

# High quality MP3
python3 {baseDir}/scripts/music.py --prompt "Jazz piano" --length-ms 10000 -o jazz.mp3 --output-format mp3_44100_192
```

### 4. Voices (`voices.py`)
列出可用的语音资源及其对应的 ID。

```bash
# List voices
python3 {baseDir}/scripts/voices.py

# JSON output
python3 {baseDir}/scripts/voices.py --json
```

### 5. Voice Cloning (`voiceclone.py`
根据音频样本创建语音克隆版本。

```bash
# Clone from audio files
python3 {baseDir}/scripts/voiceclone.py --name "MyVoice" --files sample1.mp3 sample2.mp3

# With language and gender labels
python3 {baseDir}/scripts/voiceclone.py --name "Andi" --files *.m4a --language de --gender male

# With description and noise removal
python3 {baseDir}/scripts/voiceclone.py --name "Andi" --files *.m4a --description "German male" --denoise
```

### 6. Quota & Usage (`quota.py`)
查询订阅配额和使用情况统计信息。

```bash
# Show current quota
python3 {baseDir}/scripts/quota.py

# Include usage breakdown by voice
python3 {baseDir}/scripts/quota.py --usage

# Last 7 days usage
python3 {baseDir}/scripts/quota.py --usage --days 7

# JSON output
python3 {baseDir}/scripts/quota.py --json
```

## 输出结果
```
📊 ElevenLabs Quota
=======================================
Plan:      pro (active) — annual
Characters: 66.6K / 500.0K (13.3%)
           [███░░░░░░░░░░░░░░░░░░░░░░░░░░░]
Resets:    2026-02-18 (29 days)
Voices:    22 / 160 (IVC: ✓)
Pro Voice: 0 / 1 (PVC: ✓)
```