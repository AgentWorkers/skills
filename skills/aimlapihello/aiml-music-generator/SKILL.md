---
name: aimlapi-music
description: 通过 AIMLAPI 生成高质量的音乐/歌曲。支持 Suno、Udio、Minimax 和 ElevenLabs 等音乐模型。当用户请求具有特定歌词或风格的音乐、歌曲或原声带时，可以使用该功能。
metadata:
  {
    "openclaw":
      {
        "emoji": "🎵",
        "requires": { "bins": ["python"], "env": ["AIMLAPI_API_KEY"] },
        "primaryEnv": "AIMLAPI_API_KEY",
      },
  }
---
# AIMLAPI 音乐生成

## 概述

使用最先进的 AI 模型（Suno、Udio、Minimax、ElevenLabs）生成音乐曲目。

## 快速入门

```bash
# General music (instrumental)
python {baseDir}/scripts/gen_music.py \
  --prompt "cyberpunk synthwave with heavy bass and retro synths" \
  --model "minimax/music-2.0"

# Song with lyrics
python {baseDir}/scripts/gen_music.py \
  --prompt "A happy pop song about a robot learning to feel" \
  --lyrics "[Verse 1]\nWires and gears, clicking in time..." \
  --model "minimax/music-2.0"

# Short clip (ElevenLabs)
python {baseDir}/scripts/gen_music.py \
  --prompt "lo-fi pop hip-hop ambient" \
  --model "elevenlabs/eleven_music" \
  --length 20000
```

## 参数

- `--prompt`：（必选）音乐的风格或背景信息。
- `--lyrics`：（可选）人声曲目的歌词。
- `--model`：所选模型（默认：`minimax/music-2.0`）。
- `--length`：音乐长度（以毫秒为单位，主要用于 ElevenLabs 模型）。
- `--out-dir`：保存最终 MP3 文件的目录。

## 工作流程

该脚本分为两个步骤：
1. 发送 POST 请求到 `/v2/generate/audio`：创建音乐生成任务。
2. 发送 GET 请求到 `/v2/generate/audio?generation_id=...`：持续查询生成结果，直到任务状态变为 `completed` 或 `failed`。