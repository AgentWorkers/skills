---
name: dj-mp3-sourcer
description: **从链接（如 YouTube、Spotify 等）下载音乐**：该工具会自动查找最合适的音乐来源，并按优先顺序在多个平台上进行搜索（Bandcamp、Beatport、Amazon Music、Spotify（通过 spotdl）、YouTube（通过 yt-dlp））。当用户提供音乐链接并希望下载高质量音频文件时，或者需要从多个来源批量下载歌曲时，该工具可派上用场。它支持处理单首歌曲或批量歌曲列表；对于需要付费的平台，系统会显示购买链接，而对于免费来源则直接进行下载。默认输出格式为 MP3 320kbps。此外，该工具还提供了“仅限免费资源”模式，可完全跳过付费平台。
---
# DJ MP3 Sourcer

这是一个专为DJ设计的音乐下载工具。它可以接收任何音乐链接，并自动寻找最佳的音乐来源，优先选择扩展混音版本（extended mixes）和320kbps比特率的MP3文件。

> **⚠️ 法律声明：** 本工具仅用于下载您有权下载的音乐资源（例如已购买的音乐、免费发布的音乐或遵循知识共享许可的音乐）。请遵守您所在地区的版权法律。作者不对任何不当使用行为负责。

## 所需依赖库/工具

```bash
pip install yt-dlp spotdl
brew install ffmpeg  # needed by yt-dlp for audio extraction

# optional
pip install bandcamp-dl  # for free bandcamp downloads
```

## 音乐来源的优先级

搜索顺序如下，遇到第一个匹配结果即可停止：
1. **Bandcamp**：直接支持艺术家上传的音乐，通常提供扩展混音版本。
2. **Beatport**：符合DJ的标准格式，包含BPM（节拍率）和音乐键信息，也提供扩展混音版本。
3. **Amazon Music**：提供数字音乐购买服务。
4. **Spotify**（通过`spotdl`插件）：元数据/标签信息完整，支持320kbps比特率的MP3文件下载。
5. **YouTube**（通过`yt-dlp`插件）：作为备用方案，始终可以下载音乐。

对于需要付费购买的资源（Bandcamp、Beatport、Amazon Music），会显示包含价格的购买链接；对于免费资源，则直接进行下载。

如果启用了“仅下载免费资源”模式（free only），则跳过步骤1-3，直接使用`spotdl`和`yt-dlp`进行下载。

## 核心原则：优先选择扩展混音版本

**始终优先选择扩展混音版本，而非电台编辑版本。** 即使来源的优先级较低，只要提供扩展混音版本，也应优先选择它。  
**示例：** 如果YouTube上有扩展混音版本，优先下载该版本，而非Spotify上的电台编辑版本。

在搜索时，请在查询中添加“extended mix”关键字；如果仅找到电台编辑版本，请在结果中予以说明。

## 工作流程：
1. **确定音乐信息**：提取艺术家名称和歌曲名称。
   ```bash
   yt-dlp --dump-json "<url>" | jq '{title, artist: .artist // .uploader, duration}'
   ```
2. **使用`web_search`插件搜索每个音乐来源**。
   ```
   "<artist> <title> extended mix site:bandcamp.com"
   "<artist> <title> extended mix site:beatport.com"
   "<artist> <title> site:amazon.com/music"
   ```
3. **下载或获取链接**：免费资源直接下载；付费资源会返回包含价格的购买链接。
4. **为文件添加标签**：包括艺术家名称、歌曲名称、专辑名称以及封面图片；如果来自Beatport，还需添加BPM和音乐键信息。

## 下载命令：
### 使用`spotdl`插件下载：
```bash
spotdl download "<spotify-url>" --output "{artist} - {title}" --format mp3 --bitrate 320k
```

### 使用`yt-dlp`插件下载：
```bash
yt-dlp -x --audio-format mp3 --audio-quality 0 \
  --embed-thumbnail --add-metadata \
  --metadata-from-title "%(artist)s - %(title)s" \
  -o "%(artist)s - %(title)s.%(ext)s" "<url>"
```

## 配置选项：
| 配置项 | 默认值 | 说明 |
|---------|---------|-------|
| 输出目录 | `~/Music/downloads/` | 文件保存的位置 |
| 音频格式 | mp3 320kbps | 支持高比特率的MP3格式；可根据需要设置为flac |
| 是否优先选择扩展混音 | always | 始终优先下载扩展混音版本 |
| 是否仅下载免费资源 | false | 如果设置为true，将跳过付费资源（Bandcamp、Beatport、Amazon Music），仅使用`spotdl`和`yt-dlp` |

## 批量处理
当提供多个音乐链接时，可以使用`sub-agents`（`sessions_spawn`）同时处理这些链接，并在每个任务完成后立即报告结果。

## 特殊情况处理：
- **DJ混音或长音乐集**：直接使用`yt-dlp`下载，无需进行来源搜索。
- **无法下载的资源**：需明确报告错误情况，并提供替代下载选项。
- **受地区限制的内容**：需注明内容的使用限制，并尝试其他来源。
- **混音版本与原版音乐**：如果链接指向的是特定混音版本，请直接搜索该混音版本，而非原版音乐。