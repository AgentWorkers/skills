---
name: ace-music
description: 使用 ACE Music 的免费 API，通过 ACE-Step 1.5 生成 AI 音乐。当用户请求创建、生成或创作音乐、歌曲、节拍、器乐曲或音频轨道时，可以使用此功能。该 API 支持添加歌词、指定音乐风格、制作翻唱版本等。完全免费，无需支付任何费用。
---
# ACE Music – 人工智能音乐生成

您可以通过 ACE Music 提供的免费托管 API（ACE-Step 1.5 模型）来生成音乐。

## 设置

**API 密钥** 存储在环境变量 `ACE_MUSIC_API_KEY` 中。如果未设置：
1. 在浏览器中访问 https://acemusic.ai/playground/api-key
2. 注册（免费）并获取 API 密钥
3. 将密钥保存为：`export ACE_MUSIC_API_KEY=<key>`，或将其添加到 `TOOLS.md` 文件中

## 快速生成

使用 `scripts/generate.sh` 脚本进行一次性音乐生成：

```bash
# Simple prompt (AI decides everything)
scripts/generate.sh "upbeat pop song about summer" --duration 30 --output summer.mp3

# With lyrics
scripts/generate.sh "gentle acoustic ballad, female vocal" \
  --lyrics "[Verse 1]\nSunlight through the window\n\n[Chorus]\nWe are the dreamers" \
  --duration 60 --output ballad.mp3

# Instrumental only
scripts/generate.sh "lo-fi hip hop beats, chill, rainy day" --instrumental --duration 120 --output lofi.mp3

# Natural language (AI writes everything)
scripts/generate.sh "write me a jazz song about coffee" --sample-mode --output jazz.mp3

# Specific settings
scripts/generate.sh "rock anthem" --bpm 140 --key "E minor" --language en --seed 42 --output rock.mp3

# Multiple variations
scripts/generate.sh "electronic dance track" --batch 3 --output edm.mp3
```

脚本会将生成的文件路径输出到标准输出（stdout）。您可以将生成的文件发送给用户。

## 高级用法（curl/直接调用 API）

有关封面制作、音频修改等功能，请参阅 `references/api-docs.md` 以获取完整的 API 规范。

**主要任务类型：**
- `text2music`（默认）：根据文本/歌词生成音乐
- `cover`：为现有歌曲制作封面（需要音频输入）
- `repaint`：修改现有音频的某部分内容

## 参数说明

| 功能 | 使用方法 |
|------|-----|
| 生成特定风格的音乐 | 在命令行中指定风格，例如：“jazz, saxophone solo, smoky bar” |
| 自定义歌词 | 使用 `--lyrics` 参数输入歌词，格式为：“[Verse]...[Chorus]...” |
| 由 AI 完全创作音乐 | 使用 `--sample-mode` 参数 |
| 不包含人声 | 使用 `--instrumental` 参数 |
| 生成较长长度的音乐 | 使用 `--duration` 参数设置时长（单位：秒） |
| 设置特定曲调 | 使用 `--key` 参数指定调性（例如：“C major”） |
| 批量生成多个文件 | 使用 `--batch` 参数设置生成文件的数量（例如：`--batch 3`） |
| 保证生成结果的可重复性 | 使用 `--seed` 参数设置随机种子值（例如：`--seed 42`） |
| 支持非英语歌词 | 使用 `--language` 参数指定歌词语言（例如：`--language ja` 表示日语） |

## 注意事项：
- 该 API 可永久免费使用（经 ACE Music 团队确认）
- 基础 URL：`https://api.acemusic.ai`
- 返回的音频文件为 Base64 编码的 MP3 格式，脚本会自动解码
- 如果省略时长参数，AI 会根据音乐内容自动确定时长
- 为获得最佳效果，请使用带有标签的命令格式（例如：`text2music jazz --lyrics "I want a jazz song with a saxophone solo..."`）