---
name: gifhorse
description: 搜索视频中的对话内容，并生成带有定时字幕的反应动图。非常适合从电影和电视剧中制作出适合制作模因的片段。
homepage: https://github.com/Coyote-git/gifhorse
metadata: {"clawdbot":{"emoji":"🐴","requires":{"bins":["gifhorse","ffmpeg"]},"install":[{"id":"gifhorse-setup","kind":"shell","command":"git clone https://github.com/Coyote-git/gifhorse.git ~/gifhorse && cd ~/gifhorse && python3 -m venv venv && source venv/bin/activate && pip install -e .","bins":["gifhorse"],"label":"Install gifhorse CLI tool"},{"id":"ffmpeg-full","kind":"shell","command":"brew install ffmpeg-full","bins":["ffmpeg"],"label":"Install FFmpeg-full (macOS)"}],"config":{"examples":[{"GIFHORSE_DB":"~/gifhorse/transcriptions.db"}]}}}
---

# GifHorse - 对话搜索与GIF生成工具

通过搜索视频中的对话内容并添加定时字幕，您可以从自己的视频库中创建反应GIF。

## GifHorse的功能

1. **转录视频**：通过下载字幕文件、使用本地.srt文件或Whisper AI技术，提取带有时间戳的对话内容。
2. **搜索对话**：能够快速在整个视频库中查找特定的对话片段。
3. **预览片段**：在生成GIF之前，您可以预览最终效果。
4. **创建GIF**：生成带有完美时间对齐的字幕以及可选水印的GIF。

## 设置

### 首次使用

1. 安装gifhorse（通过上方的安装按钮）。
2. 安装FFmpeg-full以支持字幕渲染（通过上方的安装按钮）。
3. 转录您的视频库（系统会自动下载字幕文件）：

```bash
cd ~/gifhorse && source venv/bin/activate
gifhorse transcribe ~/Movies
```

`gifhorse`命令必须在虚拟环境中运行。您可以使用以下命令激活虚拟环境：

```bash
cd ~/gifhorse && source venv/bin/activate
```

或者使用激活辅助工具：

```bash
source ~/gifhorse/activate.sh
```

## 可用命令

### 转录视频

从视频中提取对话内容（每个视频仅执行一次）：

```bash
# Default: downloads subtitles from online providers (fast, recommended)
gifhorse transcribe /path/to/videos

# Use only local .srt files (no downloading, no Whisper)
gifhorse transcribe /path/to/videos --use-subtitles

# Use Whisper AI (slow but works for any video)
gifhorse transcribe /path/to/video.mp4 --use-whisper

# Re-transcribe videos already in database
gifhorse transcribe /path/to/videos --force
```

### 仅下载字幕

下载.srt文件，但不将其存储在数据库中：

```bash
gifhorse fetch-subtitles /path/to/videos
gifhorse fetch-subtitles /path/to/videos --skip-existing
```

### 搜索对话

在整个视频库中查找指定的对话片段：

```bash
# Basic search
gifhorse search "memorable quote"

# Search with surrounding context
gifhorse search "memorable quote" --context 2

# Show all results (no limit)
gifhorse search "memorable quote" --all

# Custom result limit (default: 100)
gifhorse search "memorable quote" --limit 50
```

### 创建前预览

在生成GIF之前，您可以查看最终效果：

```bash
gifhorse preview "memorable quote" 1
gifhorse preview "quote" 1 --include-before 1 --include-after 1
```

### 创建GIF

生成带有字幕的GIF：

```bash
# Basic GIF (auto-named from dialogue, saved to exports/)
gifhorse create "memorable quote" 1

# Explicit output path
gifhorse create "memorable quote" 1 -o reaction.gif

# High quality for social media
gifhorse create "quote" 1 --width 720 --fps 24 --quality high

# Include conversation context
gifhorse create "quote" 1 --include-before 2 --include-after 1

# Substitute words in subtitles (repeatable, target segments by number from preview)
gifhorse create "the age of men" 1 --include-after 1 \
  -s 1 "men" "standardized software" \
  -s 2 "orc" "custom applications"

# Clean replace (no strikethrough)
gifhorse create "quote" 1 -r 1 "old word" "new word"

# Create and send via iMessage
gifhorse create "quote" 1 --send
gifhorse create "quote" 1 --send-to "+15551234567"
```

### 管理数据库

```bash
# Remove videos by path pattern (SQL LIKE wildcards)
gifhorse remove "%Adventure Time%"
gifhorse remove "%S01%" --yes

# Check subtitle status for a directory
gifhorse subtitle-status ~/Videos
gifhorse subtitle-status ~/Videos --missing-only
```

### 检查状态

```bash
# See transcription stats
gifhorse stats

# List all transcribed videos
gifhorse list
```

### 配置

```bash
# Set phone number for iMessage sending
gifhorse config --set-phone "+15551234567"

# Show current configuration
gifhorse config --show
```

## 时间控制选项

您可以精确控制哪些内容会被包含在GIF中：

- `--include-before N`：在目标对话片段之前显示N个对话片段。
- `--include-after N`：在目标对话片段之后显示N个对话片段。
- `--padding-before SECS`：在对话开始前添加缓冲时间（默认值：1.0秒）。
- `--padding-after SECS`：在对话结束后添加缓冲时间（默认值：1.0秒）。
- `--start-offset SECS`：手动调整开始时间（可以为负数）。
- `--end-offset SECS`：手动调整结束时间（可以为负数）。

**注意**：对于需要在对话之后的反应动画，应使用`--padding-after`选项，而不是`--include-after`。`--include-after`选项会捕获直到下一个对话片段开始的所有内容（可能会超过30秒）。

## 质量选项

- `--quality low|medium|high`：颜色调色板的质量（影响文件大小）。
- `--fps N`：每秒帧数（默认值：15帧；使用24帧可获得更流畅的效果）。
- `--width N`：GIF的宽度（以像素为单位，默认值：480像素；使用720像素可生成高清GIF）。

## 字幕选项

- `-s, --sub NUM OLD NEW`：替换视频中的特定单词。被替换的单词会以红色显示，替换后的内容也会以红色显示；片段编号会在预览中显示。
- `-r, --replace NUM OLD NEW`：彻底替换单词（不会显示删除线）。该操作可重复执行。
- `--no-subtitles`：创建不带字幕覆盖层的GIF。

## 输出设置

- 默认输出文件名根据对话内容自动生成（例如：`i_dont_think_so.gif`），并保存在`exports/`目录下。
- 可使用`-o PATH`参数覆盖输出路径。如果文件名冲突，系统会自动添加后缀（如 `_2`、`_3` 等）。

## iMessage功能

- `--send`：通过iMessage将生成的GIF发送到指定的电话号码（仅适用于macOS）。
- `--send-to NUMBER`：直接发送到指定的电话号码（覆盖默认设置）。

**注意**：所有生成的GIF都会在右下角添加一个微小的“gifhorse”水印。

## 常见使用场景

- **快速反应GIF**：创建简短的反应GIF。
- **完整对话片段**：提取并展示完整的对话内容。
- **带文字替换的Meme**：在GIF中替换特定单词。
- **高画质GIF（适用于Twitter/X平台）**：生成适合社交媒体的高质量GIF。
- **带对话后反应效果的场景**：在对话结束后添加相应的动画效果。
- **通过iMessage发送GIF**：通过iMessage发送GIF。

## 使用技巧

1. **务必先预览**：在生成GIF之前，请使用`preview`功能检查时间对齐是否正确。
2. **自动下载字幕**：只需运行`gifhorse transcribe`，系统会自动下载字幕。
3. **注意文件大小**：高质量和长视频会导致文件体积较大（20秒的视频可能超过20MB）。
4. **选择合适的缓冲时间**：对于反应动画，使用`--padding-after`而非`--include-after`。
5. **添加上下文信息**：使用`--context 2`查看对话的上下文。
6. **重新转录**：如果字幕内容更新，可以使用`--force`选项重新生成转录结果。
7. **检查字幕覆盖情况**：使用`subtitle-status`命令查看哪些视频需要添加字幕。

## 文件大小参考

- **低画质，10秒，360p**：约1-2 MB
- **中等画质，10秒，480p**：约3-5 MB
- **高画质，20秒，720p**：约20 MB以上

## 常见问题解决方法

- **“command not found: gifhorse”**：请确保已激活虚拟环境。
- **字幕渲染错误**：请确认已安装FFmpeg-full。
- **视频文件未找到**：由于数据库存储的是绝对路径，如果视频位置发生变化，请重新进行转录。

## 网络共享支持

GifHorse支持通过网络挂载的视频文件。

## 适用场景

当用户需要执行以下操作时，可以使用GifHorse：

- 在视频库中搜索特定对话或片段。
- 从电影或电视剧中创建反应GIF。
- 制作带有文字替换的Meme GIF。
- 为视频片段添加字幕。
- 转录视频以方便后续搜索。
- 在生成GIF之前预览效果。
- 通过iMessage发送GIF。
- 从数据库中删除视频文件。
- 检查视频库中的字幕状态。

## 更多信息

- **GitHub仓库**：https://github.com/Coyote-git/gifhorse
- **使用指南**：https://github.com/Coyote-git/gifhorse/blob/main/USAGE_GUIDE.md
- **开发计划**：https://github.com/Coyote-git/gifhorse/blob/main/ROADMAP.md

## 许可证

MIT许可证