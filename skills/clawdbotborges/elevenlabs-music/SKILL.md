---
name: elevenlabs-music
description: 使用 ElevenLabs 的 Eleven Music API 根据文本提示生成音乐。该 API 可用于创作歌曲、配乐、短片音乐、摇篮曲或任何类型的音频作品，支持加入 AI 生成的歌词的人声、纯器乐曲目以及多种音乐风格。但需要订阅 ElevenLabs 的付费服务才能使用该功能。
metadata: {"clawdbot":{"emoji":"🎵","requires":{"bins":["uv"],"env":["ELEVENLABS_API_KEY"]},"primaryEnv":"ELEVENLABS_API_KEY"}}
---

# ElevenLabs 音乐生成

利用人工智能技术，根据文本提示生成完整的歌曲，包括歌词和人声。

## 快速入门

```bash
# Basic generation (30 seconds)
uv run {baseDir}/scripts/generate_music.py "upbeat jazz piano"

# Longer track (3 minutes)
uv run {baseDir}/scripts/generate_music.py "epic orchestral battle music" --length 180

# Instrumental only (no vocals)
uv run {baseDir}/scripts/generate_music.py "lo-fi hip hop beats" --length 120 --instrumental

# Custom output path
uv run {baseDir}/scripts/generate_music.py "romantic bossa nova" -o /tmp/bossa.mp3
```

## 选项

| 标志 | 描述 |
|------|-------------|
| `-l, --length` | 音乐时长（秒，范围：3-600，默认值：30秒） |
| `-o, --output` | 输出文件路径（默认值：/tmp/music.mp3） |
| `-i, --instrumental` | 强制使用纯器乐版本，不含人声 |

## 提示编写技巧

### 明确指定风格
- 包括音乐类型、情绪、节奏和乐器
- 指定音乐年代或风格：例如：“90年代巴西浪漫派帕戈德音乐（90s Brazilian romantic pagode）”、“1960年代科幻电视剧主题曲（1960s sci-fi TV theme）”
- 描述音乐氛围：例如：“从柔和逐渐变得激昂（builds from soft to explosive）”、“轻松而亲密（relaxed and intimate）”

### 人声相关选项
- 指定语言：例如：“使用葡萄牙语演唱（vocals in Portuguese）”
- 描述人声风格：例如：“富有感染力的男性嗓音（soulful male vocals）”、“空灵的女性合唱（ethereal female choir）”
- 提及歌词主题：例如：“关于爱与思念（about love and saudade）”、“庆祝友谊（celebrating friendship）”

### 避免版权问题
- 不要直接提及艺术家或乐队的名称
- 用音乐风格来描述：例如：“经典的90年代浪漫桑巴风格（classic 90s romantic samba style）”，而不是“类似Raça Negra的风格”

### 示例提示

**MPB（巴西流行音乐）**
```
A soulful MPB track featuring gentle acoustic guitar, warm nylon strings, 
and dreamy Rhodes piano. Bossa nova-influenced rhythm with soft brushed 
drums. Vocals in Portuguese express themes of saudade and the beauty of life.
```

**史诗级管弦乐**
```
Epic military march with powerful brass fanfares, thundering timpani drums, 
and a soaring choir. Triumphant and heroic, with deep bass tubas, bold 
trumpets, snare rolls, and an anthemic melody building to a glorious crescendo.
```

**摇篮曲**
```
Gentle orchestral lullaby with sweeping strings, soft brass, and ethereal 
wordless soprano vocals. Peaceful yet majestic, evoking wonder and hope. 
Perfect for falling asleep while dreaming of adventures.
```

**喜剧摇滚**
```
Brazilian comedy rock with absurd, hilarious Portuguese lyrics full of 
wordplay. Mix energetic rock guitars with unexpected rhythms - forró 
breakdowns, pagode moments. Theatrical, exaggerated vocals singing about 
ridiculous situations.
```

## 使用要求

- **ElevenLabs API密钥**：需要设置环境变量 `ELEVENLABS_API_KEY`
- **付费计划**：使用音乐API需要Creator计划或更高级别的订阅
- **uv**：用于运行包含依赖项的Python脚本

## 支持的功能

- 支持将文本转换为最长10分钟的音频文件
- 支持多种语言的AI生成歌词和人声（英语、西班牙语、葡萄牙语、德语、日语等）
- 支持纯器乐模式
- 支持大多数音乐风格和类型