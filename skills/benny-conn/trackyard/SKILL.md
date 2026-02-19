---
name: trackyard
description: 从 Trackyard 的人工智能驱动的音乐目录中搜索并下载授权音乐。这些音乐可用于为视频、社交媒体内容、播客或任何需要免版税音乐的项目制作背景音乐。该服务支持自然语言搜索（例如：“适合科技视频的欢快电子音乐”），能够智能地裁剪音频以精确匹配所需时长，并提供按流派、情绪、每分钟节拍数（BPM）、人声、能量感和乐器类型进行筛选的功能。
homepage: https://trackyard.com
metadata: {"openclaw":{"emoji":"🎵","requires":{"bins":["curl","jq"],"env":["TRACKYARD_API_KEY"]},"primaryEnv":"TRACKYARD_API_KEY"}}
---
# Trackyard 音乐 API

Trackyard 为您提供数万首精心挑选的音乐曲目，所有曲目均经过合法授权，可用于社交媒体、YouTube、播客及在线内容（非电影/电视用途）。该服务的三大亮点如下：

1. **庞大的授权曲库**：数十万首经过人工筛选的曲目，可随时用于各类社交平台，无需担心授权问题。
2. **基于 AI 的搜索功能**：只需用简单的英语描述您的需求（例如：“适合咖啡店 Vlog 的忧郁氛围低音音乐”），API 便会自动找到合适的曲目，并能根据描述推断出曲风的类型、情绪、节拍（BPM）和乐器编配。
3. **智能剪辑工具**：您可以自定义曲目的长度，系统会自动选择最合适的片段。此外，您还可以指定音乐的高潮部分，确保它精确地出现在视频的指定位置。

## 使用场景

- **社交媒体内容制作**：批量为 TikTok、Reels 和 Shorts 等平台自动选择音乐；每次只需输入视频需求，系统即可生成符合平台时长（15 秒、30 秒或 60 秒）的音频片段。
- **社交媒体广告**：寻找与广告风格相匹配的音乐，剪辑成广告所需的时长，并确保广告中的关键部分（如高潮部分）出现在最合适的视觉节点。
- **AI 视频生成**：将 AI 生成的视频与 AI 选定的音乐结合；将视频描述输入搜索系统，系统会自动剪辑出与视频长度完全匹配的音频片段。
- **YouTube 和播客背景音乐**：选择适合背景播放的纯器乐曲目，避免与旁白产生冲突。
- **产品演示和开箱视频**：根据产品风格选择合适的音乐；生产力应用适合使用轻柔的合成器音乐，健身品牌则适合使用充满活力的音乐。
- **房地产和房产展示**：使用舒缓、氛围优美的背景音乐，为视觉内容增添层次感。
- **企业及培训视频**：使用专业且中性的背景音乐，让观众专注于内容。
- **应用和游戏预告片**：通过精确控制音乐高潮部分，营造紧张或兴奋的氛围。

## 设置要求

需要设置 `TRACKYARD_API_KEY` 环境变量。用户可在 [trackyard.com](https://trackyard.com) 获取 API 密钥。

```bash
export TRACKYARD_API_KEY="trackyard_live_..."
```

或者将其添加到 OpenClaw 的配置文件中：`env_vars.TRACKYARD_API_KEY`

## 快速参考

### 音乐搜索

```bash
scripts/trackyard.sh search "upbeat electronic for tech startup video"
```

支持多种过滤条件：

```bash
scripts/trackyard.sh search "chill background music" --limit 5 --no-vocals --energy medium
```

### 下载曲目

- **完整版曲目**：
```bash
scripts/trackyard.sh download TRACK_ID
```

- **剪辑至 22 秒**：
```bash
scripts/trackyard.sh download TRACK_ID --duration 22
```

- **精确控制高潮部分（高潮出现在 12 秒处）**：
```bash
scripts/trackyard.sh download TRACK_ID --duration 22 --hit-point 12
```

### 查看曲目信息

```bash
scripts/trackyard.sh me
```

## 工作流程

1. **使用自然语言进行搜索**，获取曲目 ID 和元数据。
2. **下载所选曲目**（每次下载计 1 个使用次数）。

## 过滤选项

| 过滤条件 | 可选值 |
|---------|---------|
| `--genres` | electronicDance, pop, rock, hiphop, ambient, classical, jazz 等 |
| `--moods` | happy, energetic, sad, calm, dramatic, mysterious, romantic |
| `--energy` | low, medium, high |
| `--min-bpm` / `--max-bpm` | 60-200 |
| `--no-vocals` | 仅限纯器乐 |
| `--instruments` | synthesizer, guitar, piano, drums, strings 等 |

## 剪辑功能

- 使用 `--duration` 参数下载曲目时，系统会自动选择最具感染力的音乐片段，并确保剪辑效果流畅。
- 通过 `--hit-point N` 参数，您可以指定音乐高潮部分出现在视频的 N 秒处，实现精准同步。

## 使用费用

- 搜索功能：每次使用计 1 个使用次数。
- 下载功能：每次下载计 1 个使用次数。
- 账户信息：免费。

## 输出结果

- 搜索结果以 JSON 格式返回曲目元数据。
- 下载的音频文件保存为 `.mp3` 格式，文件名与曲目标题相同，保存在当前目录中。