---
name: elevenlabs-voices
version: 2.1.5
description: 使用 ElevenLabs API，提供高质量的语音合成服务，支持 18 种人物角色（personas）、32 种语言、音效功能，以及批量处理和语音设计功能。
tags: [tts, voice, speech, elevenlabs, audio, sound-effects, voice-design, multilingual]
metadata: {"openclaw":{"requires":{"bins":["python3"],"env":{"ELEVEN_API_KEY":"required","ELEVENLABS_API_KEY":"optional"},"note":"Set ELEVEN_API_KEY. ELEVENLABS_API_KEY is an accepted alias."}}}
---

# ElevenLabs Voice Personas v2.1

这是一个全面的语音合成工具包，支持使用 ElevenLabs 的 API。

## 🚀 首次使用 - 设置向导

当您首次使用此功能时（如果不存在 `config.json` 文件），请运行交互式设置向导：

```bash
python3 scripts/setup.py
```

向导将指导您完成以下步骤：
1. **API 密钥** - 输入您的 ElevenLabs API 密钥（必需）
2. **默认语音** - 从常见的语音中选择（如 Rachel、Adam、Bella 等）
3. **语言** - 设置您喜欢的语言（支持 32 种语言）
4. **音频质量** - 选择标准或高质量的输出
5. **成本跟踪** - 启用使用情况和成本监控
6. **预算限制** - 可选的每月支出上限

**🔒 隐私保护：** 您的 API 密钥仅存储在 `config.json` 文件中，不会离开您的设备，并且会通过 `.gitignore` 文件自动排除在 Git 仓库之外。

如果您需要重新配置，只需再次运行设置向导即可。

---

## ✨ 主要功能

- **18 种语音角色** - 为不同场景精心挑选的语音
- **32 种语言** - 支持多语言合成
- **流式模式** - 生成音频时实时输出
- **音效（SFX）** - 从文本描述中生成 AI 驱动的音效
- **批量处理** - 一次处理多个文本
- **成本跟踪** - 监控语音使用情况和预估成本
- **语音设计** - 根据描述创建自定义语音
- **发音词典** - 自定义单词的发音规则
- **OpenClaw 集成** - 与 OpenClaw 的内置 TTS 功能兼容

---

## 🎙️ 可用语音

| 语音 | 口音 | 性别 | 角色 | 适用场景 |
|-------|--------|--------|---------|----------|
| Rachel | 美国 | 女性 | 温暖 | 对话、教程 |
| Adam | 美国 | 男性 | 叙述者 | 纪录片、有声书 |
| Bella | 美国 | 女性 | 专业 | 商务、演讲 |
| Brian | 美国 | 男性 | 舒缓的 | 冥想、轻松内容 |
| George | 英国 | 男性 | 讲故事的人 | 有声书、故事讲述 |
| Alice | 英国 | 女性 | 教育者 | 教程、解释 |
| Callum | 美国 | 男性 | 有趣的 | 游戏、轻松氛围 |
| Charlie | 澳大利亚 | 男性 | 充满活力的 | 体育、激励性内容 |
| Jessica | 美国 | 女性 | 有趣的 | 社交媒体、非正式场合 |
| Lily | 英国 | 女性 | 演员 | 戏剧、优雅内容 |
| Matilda | 美国 | 女性 | 专业 | 企业、新闻 |
| River | 美国 | 中性 | 中立的语气 | 适合所有人、信息性内容 |
| Roger | 美国 | 男性 | 非正式 | 播客、轻松氛围 |
| Daniel | 英国 | 男性 | 广播员 | 新闻、公告 |
| Eric | 美国 | 男性 | 可信赖的 | 商务、企业场景 |
| Chris | 美国 | 男性 | 友好的 | 教程、易于接近 |
| Will | 美国 | 男性 | 乐观的 | 激励人心、积极向上的内容 |
| Liam | 美国 | 男性 | 社交型 | YouTube、社交媒体 |

## 🎯 快速预设

- `default` → Rachel（温暖、友好的语气）
- `narrator` → Adam（适合纪录片）
- `professional` → Matilda（适合企业场景）
- `storyteller` → George（适合有声书）
- `educator` → Alice（适合教程）
- `calm` → Brian（适合冥想）
- `energetic` → Liam（适合社交媒体）
- `trustworthy` → Eric（适合商务场景）
- `neutral` → River（适合中立的语气）
- `british` → George（英式口音）
- `australian` → Charlie（澳大利亚口音）
- `broadcaster` → Daniel（适合新闻）

---

## 🌍 支持的语言（32 种）

多语言 v2 模型支持以下语言：

| 代码 | 语言 | 代码 | 语言 |
|------|----------|------|----------|
| en | 英语 | pl | 波兰语 |
| de | 德语 | nl | 荷兰语 |
| es | 西班牙语 | sv | 瑞典语 |
| fr | 法语 | da | 丹麦语 |
| it | 意大利语 | fi | 芬兰语 |
| pt | 葡萄牙语 | no | 挪威语 |
| ru | 俄语 | tr | 土耳其语 |
| uk | 乌克兰语 | cs | 捷克语 |
| ja | 日语 | sk | 斯洛伐克语 |
| ko | 韩语 | hu | 匈牙利语 |
| zh | 中文 | ro | 罗马尼亚语 |
| ar | 阿拉伯语 | bg | 保加利亚语 |
| hi | 印地语 | hr | 克罗地亚语 |
| ta | 泰米尔语 | el | 希腊语 |
| id | 印尼语 | ms | 马来语 |
| vi | 越南语 | th | 泰语 |

```bash
# Synthesize in German
python3 tts.py --text "Guten Tag!" --voice rachel --lang de

# Synthesize in French
python3 tts.py --text "Bonjour le monde!" --voice adam --lang fr

# List all languages
python3 tts.py --languages
```

---

## 💻 命令行接口（CLI）使用

### 基本文本转语音

```bash
# List all voices
python3 scripts/tts.py --list

# Generate speech
python3 scripts/tts.py --text "Hello world" --voice rachel --output hello.mp3

# Use a preset
python3 scripts/tts.py --text "Breaking news..." --voice broadcaster --output news.mp3

# Multi-language
python3 scripts/tts.py --text "Bonjour!" --voice rachel --lang fr --output french.mp3
```

### 流式模式

实时生成音频（适合长文本）：

```bash
# Stream audio as it generates
python3 scripts/tts.py --text "This is a long story..." --voice adam --stream

# Streaming with custom output
python3 scripts/tts.py --text "Chapter one..." --voice george --stream --output chapter1.mp3
```

### 批量处理

一次性处理多个文本文件：

```bash
# From newline-separated text file
python3 scripts/tts.py --batch texts.txt --voice rachel --output-dir ./audio

# From JSON file
python3 scripts/tts.py --batch batch.json --output-dir ./output
```

**JSON 批量格式：**
```json
[
  {"text": "First line", "voice": "rachel", "output": "line1.mp3"},
  {"text": "Second line", "voice": "adam", "output": "line2.mp3"},
  {"text": "Third line"}
]
```

**简单文本格式（每行一个文本）：**
```
Hello, this is the first sentence.
This is the second sentence.
And this is the third.
```

### 使用统计信息

```bash
# Show usage stats and cost estimates
python3 scripts/tts.py --stats

# Reset statistics
python3 scripts/tts.py --reset-stats
```

---

## 🎵 音效（SFX）

根据文本描述生成 AI 驱动的音效：

```bash
# Generate a sound effect
python3 scripts/sfx.py --prompt "Thunder rumbling in the distance"

# With specific duration (0.5-22 seconds)
python3 scripts/sfx.py --prompt "Cat meowing" --duration 3 --output cat.mp3

# Adjust prompt influence (0.0-1.0)
python3 scripts/sfx.py --prompt "Footsteps on gravel" --influence 0.5

# Batch SFX generation
python3 scripts/sfx.py --batch sounds.json --output-dir ./sfx

# Show prompt examples
python3 scripts/sfx.py --examples
```

**示例描述：**
- “远处的雷声隆隆”
- “猫满足地发出呼噜声”
- “在机械键盘上打字的声音”
- “宇宙飞船引擎的嗡嗡声”
- “咖啡店的背景嘈杂声”

---

## 🎨 语音设计

根据文本描述创建自定义语音：

```bash
# Basic voice design
python3 scripts/voice-design.py --gender female --age middle_aged --accent american \
  --description "A warm, motherly voice"

# With custom preview text
python3 scripts/voice-design.py --gender male --age young --accent british \
  --text "Welcome to the adventure!" --output preview.mp3

# Save to your ElevenLabs library
python3 scripts/voice-design.py --gender female --age young --accent american \
  --description "Energetic podcast host" --save "MyHost"

# List all design options
python3 scripts/voice-design.py --options
```

**语音设计选项：**

| 选项 | 可选值 |
|--------|--------|
| 性别 | 男性、女性、中性 |
| 年龄 | 年轻、中年、老年 |
| 口音 | 美国、英国、非洲、澳大利亚、印度、拉丁、中东、斯堪的纳维亚、东欧 |
| 口音强度 | 0.3-2.0（从轻微到强烈） |

---

## 📖 发音词典

自定义单词的发音：

编辑 `pronunciations.json` 文件：
```json
{
  "rules": [
    {
      "word": "OpenClaw",
      "replacement": "Open Claw",
      "comment": "Pronounce as two words"
    },
    {
      "word": "API",
      "replacement": "A P I",
      "comment": "Spell out acronym"
    }
  ]
}
```

**使用方法：**
```bash
# Pronunciations are applied automatically
python3 scripts/tts.py --text "The OpenClaw API is great" --voice rachel

# Disable pronunciations
python3 scripts/tts.py --text "The API is great" --voice rachel --no-pronunciations
```

---

## 💰 成本跟踪

该功能会跟踪您的语音使用情况并估算成本：

```bash
python3 scripts/tts.py --stats
```

**输出结果：**
```
📊 ElevenLabs Usage Statistics

  Total Characters: 15,230
  Total Requests:   42
  Since:            2024-01-15

💰 Estimated Costs:
  Starter    $4.57 ($0.30/1k chars)
  Creator    $3.66 ($0.24/1k chars)
  Pro        $2.74 ($0.18/1k chars)
  Scale      $1.68 ($0.11/1k chars)
```

---

## 🤖 OpenClaw TTS 集成

### 与 OpenClaw 的内置 TTS 功能集成

OpenClaw 内置了 TTS 支持，可以使用 ElevenLabs 的服务。请在 `~/.openclaw/openclaw.json` 文件中进行配置：

```json
{
  "tts": {
    "enabled": true,
    "provider": "elevenlabs",
    "elevenlabs": {
      "apiKey": "your-api-key-here",
      "voice": "rachel",
      "model": "eleven_multilingual_v2"
    }
  }
}
```

### 在 OpenClaw 对话中触发 TTS

- 使用 `/tts on` 启用自动 TTS
- 直接使用 `tts` 工具进行一次性语音播放
- 请求 “读出这个内容” 或 “大声说出这个内容”

### 使用 OpenClaw 的脚本

```bash
# OpenClaw can run these scripts directly
exec python3 /path/to/skills/elevenlabs-voices/scripts/tts.py --text "Hello" --voice rachel
```

---

## ⚙️ 配置

脚本会按以下顺序查找 API 密钥：
1. 环境变量 `ELEVEN_API_KEY` 或 `ELEVENLABS_API_KEY`
2. OpenClaw 配置文件（`~/.openclaw/openclaw.json` → `tts.elevenlabs.apiKey`
3. 本技能的本地 `.env` 文件

**创建 `.env` 文件：**
```bash
echo 'ELEVEN_API_KEY=your-key-here' > .env
```

---

## 🎛️ 语音设置

每种语音都有针对最佳输出的个性化设置：

| 设置 | 范围 | 描述 |
|---------|-------|-------------|
| 稳定性 | 0.0-1.0 | 数值越高，语音越稳定；数值越低，表现越富有表现力 |
| 语音相似度 | 0.0-1.0 | 与原始语音的相似程度 |
| 风格 | 0.0-1.0 | 语音表达风格的夸张程度 |

---

## 📝 触发命令

- `use {voice_name}` 语音
- `speak as {persona}` 以 {persona} 角色说话
- `list voices` 列出所有可用语音
- `voice settings` 查看语音设置
- `generate sound effect` 生成音效
- `design a voice` 创建自定义语音

---

## 📁 相关文件

```
elevenlabs-voices/
├── SKILL.md              # This documentation
├── README.md             # Quick start guide
├── config.json           # Your local config (created by setup, in .gitignore)
├── voices.json           # Voice definitions & settings
├── pronunciations.json   # Custom pronunciation rules
├── examples.md           # Detailed usage examples
├── scripts/
│   ├── setup.py          # Interactive setup wizard
│   ├── tts.py            # Main TTS script
│   ├── sfx.py            # Sound effects generator
│   └── voice-design.py   # Voice design tool
└── references/
    └── voice-guide.md    # Voice selection guide
```

---

## 🔗 链接

- [ElevenLabs](https://elevenlabs.io)
- [API 文档](https://docs.elevenlabs.io)
- [语音库](https://elevenlabs.io/voice-library)
- [音效 API](https://elevenlabs.io/docs/api-reference/sound-generation)
- [语音设计 API](https://elevenlabs.io/docs/api-reference/voice-generation)

---

## 📋 更新日志

### v2.1.0
- 添加了交互式设置向导（`scripts/setup.py`）
- 提供关于 API 密钥、语音、语言、质量和预算设置的引导
- 配置信息存储在本地 `config.json` 文件中（已添加到 `.gitignore` 文件）
- 优化了设置流程，注重用户隐私

### v2.0.0
- 增加了对 32 种语言的支持（通过 `--lang` 参数）
- 新增了流式模式（通过 `--stream` 标志）
- 新增了音效生成功能（`sfx.py`）
- 新增了批量处理功能（`--batch` 标志）
- 新增了成本跟踪功能（`--stats` 标志）
- 新增了语音设计工具（`voice-design.py`）
- 新增了发音词典支持
- 更新了 OpenClaw TTS 集成的文档
- 改进了错误处理和进度显示功能