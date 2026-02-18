---
name: dj-set-ripper
description: >
  **从DJ合集或混音中下载单首歌曲**  
  当用户提供来自YouTube、SoundCloud、Mixcloud或1001Tracklists的链接时，系统会从页面描述或元数据中提取曲目列表，然后使用`dj-mp3-sourcer`技能逐一下载这些歌曲。该功能适用于以下场景：  
  - 用户分享DJ合集/混音链接并希望下载其中的单首歌曲；  
  - 用户提供曲目列表并希望系统获取所有歌曲的下载信息。  
  系统会生成一个带有时间戳的日志文件，记录每首歌曲的下载状态（已下载、需要购买链接、未找到、盗版/无法获取、无法识别）。此外，用户还可以选择下载整个混音文件作为备份。
---
# DJ Set Ripper

该工具用于从DJ表演中提取曲目列表，并单独下载每首歌曲。

> **⚠️ 法律声明：** 本工具仅用于下载您有权访问的音乐资源（包括购买的音乐、免费发布的音乐或遵循知识共享许可的音乐）。请遵守您所在地区的版权法规。作者不对该工具的滥用行为负责。

## 依赖项

与 [dj-mp3-sourcer](https://clawhub.ai/Robinnnnn/dj-mp3-sourcer) 的依赖项相同（包括 yt-dlp、ffmpeg/ffprobe、spotdl）。无需额外依赖任何其他软件。

## 工作流程

### 1. 提取页面内容

获取DJ表演的URL，并提取页面上的原始文本（描述、元数据、评论等）：

- **YouTube：**  
  使用相应的代码块（```bash
yt-dlp --dump-json "<url>" | jq -r '.description'
```）来获取页面内容。

- **SoundCloud / Mixcloud：**  
  使用 `web_fetch` 命令以Markdown格式获取页面内容。

- **1001Tracklists：**  
  该平台提供的数据结构较为规范，优先使用该来源。

### 2. 解析曲目列表

将提取到的页面内容传递给模型，并使用以下提示结构进行解析：

```
Extract all tracks from this DJ set description. Return a JSON array of objects:
[{"number": 1, "timestamp": "0:00", "artist": "Artist Name", "title": "Track Title (Mix Name)"}]

Rules:
- Preserve remix/mix names in the title (e.g. "Original Mix", "Extended Mix", "Remix")
- If a track is listed as "ID - ID" or "ID", set artist and title both to "ID"
- If only a timestamp exists with no track info, skip it
- Normalize artist names (fix ALL CAPS, etc.)
- If no timestamps exist, set timestamp to null
- Number tracks sequentially starting from 1

Raw content:
"""
{description_text}
"""
```

如果解析结果为空（即没有找到曲目列表），请告知用户并建议用户：
- 手动在1001Tracklists网站上查找曲目列表；
- 直接复制曲目列表内容。

### 3. 下载每首歌曲

对于每一首被解析出的歌曲（跳过艺术家名称和歌曲名称均为“ID”的歌曲）：
1. 使用 [dj-mp3-sourcer](https://clawhub.ai/Robinnnnn/dj-mp3-sourcer) 的工作流程，按优先顺序搜索音乐资源，优先下载扩展版混音版本或购买链接。
2. 使用 `sessions_spawn` 命令并行下载多首歌曲（每次下载3-5首，以避免超过下载速度限制）。
3. 将下载后的歌曲保存到：`~/Downloads/{set-name}/` 目录中。
   曲目文件名会根据混音作品的名称进行规范化处理（例如：`Artist - Title.mp3`）。

### 4. （可选）下载完整混音版本

询问用户是否需要下载完整的混音版本。如果用户同意，执行相应的代码块（```bash
yt-dlp -x --audio-format mp3 --audio-quality 0 \
  --embed-thumbnail --add-metadata \
  -o "~/Downloads/{set-name}/{set-name} [Full Mix].%(ext)s" "<url>"
```）。

### 5. 规范化文件名

在所有歌曲下载完成后（注意：不是逐批下载，而是等待所有子任务完成后再执行），运行文件名规范化脚本：

```bash
# 1. Write the parsed tracklist as JSON
cat > /tmp/tracklist.json << 'EOF'
[{"artist": "Artist", "title": "Title"}, ...]
EOF

# 2. Run normalize
scripts/normalize-filenames.sh ~/Downloads/{set-name} /tmp/tracklist.json
```

该脚本会自动将每个MP3文件名与曲目列表中的信息匹配，并将其重命名为规范的格式（例如：`Artist - Title.mp3`）。脚本会处理一些特殊情况，如文件名中包含“NA -”、“(Official Video)”等无效信息，或艺术家名称错误等问题。

**重要提示：** 请在所有子任务完成后在主任务中运行该脚本，切勿依赖子任务来完成文件名重命名工作。解析得到的曲目列表是文件名生成的唯一依据。

### 6. 生成日志文件

在 `~/Downloads/{set-name}/{timestamp}.log` 文件中记录下载过程，日志文件格式如下：

```
DJ Set Ripper Log
=================
Set: {set title}
URL: {original url}
Date: {ISO timestamp}
Tracks found: {total}

#   | Artist              | Title                          | Status         | Source   | Bitrate | Size  | File/Link
----|---------------------|--------------------------------|----------------|----------|---------|-------|----------
01  | Argy                | Aria (Original Mix)            | ✅ downloaded   | spotdl   | 320k    | 8.2MB | Argy - Aria (Original Mix).mp3
02  | ID                  | ID                             | ⬛ unidentified | —        | —       | —     | —
03  | Massano             | Odyssey                        | ✅ downloaded   | youtube  | 271k    | 6.5MB | Massano - Odyssey.mp3
04  | Boris Brejcha       | Gravity (Extended Mix)         | 🛒 purchase     | beatport | —       | —     | https://...
05  | Some Bootleg        | Unreleased VIP                 | ❌ not found    | —        | —       | —     | —

Summary: 3 downloaded, 1 purchase link, 1 not found, 1 unidentified
Total size: ~XXM (individual tracks) + XXM (full mix)
Full mix: ✅ downloaded → {set-name} [Full Mix].mp3

Notes:
- Bitrate via `ffprobe -v quiet -show_entries format=bit_rate -of csv=p=0 "<file>"`
- File size via `ls -lh`
```

## 特殊情况处理：

- **页面描述中未包含曲目列表**：通过 `web_search` 在1001Tracklists网站上查找相关曲目列表（例如：`"{set title}" site:1001tracklists.com`）。
- 如果发现曲目名称为“ID - ID”的歌曲，将其记录为未识别的曲目，不要尝试下载。
- 对于盗版或混音作品，尽管仍会尝试下载，但可能会失败，应记录为“未找到”并附上说明。
- 如果DJ表演包含多位艺术家，需妥善处理这种情况。
- 对于包含重复歌曲的情况，需在下载前根据艺术家名称和歌曲名称进行去重处理。
- 对于歌曲数量较多的表演（超过50首），请分批下载（每批5首），并在每批下载完成后更新进度。

## 配置选项

| 配置项 | 默认值 | 说明 |
|---------|---------|-------|
| 输出目录 | `~/Downloads/{set-name}/` | 每个DJ表演对应一个子文件夹 |
| 文件格式 | mp3 320k | 通过 [dj-mp3-sourcer] 设置文件格式 |
| 是否下载完整混音版本 | 询问用户 | 可设置为始终下载或从不下载 |
| 仅下载免费音乐 | true | 该设置会传递给 [dj-mp3-sourcer]，以便跳过付费资源，仅使用 spotdl/yt-dlp 进行下载 |
| 并行下载数量 | 5 | 同时允许的最大下载任务数量 |