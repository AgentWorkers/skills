---
name: youtube-knowledge-extractor
description: 通过音频（字幕）和视觉（帧提取 + 图像分析）两种渠道对 YouTube 视频进行多模态分析。这种技术尤其适用于教学视频、教程、演示视频以及解释性视频，因为在这些视频中，展示的内容（截图、用户界面演示、图表、代码、实际操作等）与所说的内容同样重要。当用户需要分析、总结 YouTube 视频或创建分步指南，或者分享 YouTube 链接并希望了解视频中的内容时，都可以使用这项技能。该功能会在收到如下请求时触发：**“分析这个 YouTube 视频”**、**“根据这个视频创建分步指南”**、**“这个视频展示了什么？”**、**“总结这个教程”**，以及其他任何带有分析目的的 YouTube 链接请求。
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - ffmpeg
        - python3
        - curl
    emoji: "🎬"
    os:
      - linux
      - macos
    install:
      - kind: uv
        package: yt-dlp
        bins: [yt-dlp]
---
# YouTube 视频分析器 — 多模态分析

该工具通过以下两个信息渠道对 YouTube 视频进行深度分析：
- **音频渠道**：包含时间戳的文字记录（视频中说了什么）
- **视觉渠道**：提取视频帧并进行图像分析（视频中展示了什么）

大多数 YouTube 分析工具仅提取文字记录。而该工具通过将视频帧与语音内容同步，填补了这一空白，从而能够提供准确的逐步指导：例如，“点击蓝色按钮”这一操作会与显示该按钮的实际截图相对应。

## 工作流程概述

```
YouTube URL
    |
    +---> 1. Get metadata (title, duration, video ID)
    |
    +---> 2. Extract transcript (yt-dlp --dump-json + curl)
    |         -> Timestamped segments
    |
    +---> 3. Extract frames (yt-dlp + ffmpeg)
    |         -> Keyframes at strategic intervals
    |
    +---> 4. Synchronize frames <-> transcript
    |         -> Match frames to spoken content by timestamp
    |
    +---> 5. Multimodal analysis
              -> Read each frame image, combine with transcript
              -> Generate structured output
```

## 第 1 步：设置工作目录

```bash
VIDEO_URL="<YOUTUBE_URL>"
WORK_DIR=$(mktemp -d /tmp/yt-analysis-XXXXXX)
mkdir -p "$WORK_DIR/frames"
```

## 第 2 步：获取视频元数据

```bash
yt-dlp --print title --print duration --print id "$VIDEO_URL" 2>/dev/null
```

该步骤会返回三行信息：视频标题、视频时长（以秒为单位）以及视频 ID。请将这些信息保存下来以供后续使用。

## 第 3 步：提取文字记录

**重要提示：** 直接使用 `--write-sub` 命令下载字幕时，很容易触发 YouTube 的速率限制（HTTP 429 错误）。请改用以下可靠的两步方法。

### 第 3a 步：从视频 JSON 数据中获取字幕 URL

```bash
yt-dlp --dump-json "$VIDEO_URL" 2>/dev/null | python3 -c "
import json, sys
data = json.load(sys.stdin)
auto = data.get('automatic_captions', {})
subs = data.get('subtitles', {})

# Priority: manual subs > auto subs. Prefer user's language, fallback chain.
for source in [subs, auto]:
    for lang in ['en', 'de', 'en-orig', 'fr', 'es']:
        if lang in source:
            for fmt in source[lang]:
                if fmt.get('ext') == 'json3':
                    print(fmt['url'])
                    sys.exit(0)

# Fallback: take first available auto-caption, get json3 URL
for lang in sorted(auto.keys()):
    for fmt in auto[lang]:
        if fmt.get('ext') == 'json3':
            url = fmt['url']
            # Remove translation param to get original language
            import re
            url = re.sub(r'&tlang=[^&]+', '', url)
            print(url)
            sys.exit(0)

print('NO_SUBS', file=sys.stderr)
sys.exit(1)
" > "$WORK_DIR/sub_url.txt"
```

### 第 3b 步：下载并解析字幕文件

```bash
curl -s "$(cat "$WORK_DIR/sub_url.txt")" -o "$WORK_DIR/transcript.json3"
```

请验证字幕文件是否为有效的 JSON 格式（而非 HTML 错误页面）：

```bash
head -c 20 "$WORK_DIR/transcript.json3"
# Should start with { — if it starts with <html, retry after 10s sleep
```

### 第 3c 步：将 JSON 数据解析为带有时间戳的文本片段

```bash
python3 -c "
import json

with open('$WORK_DIR/transcript.json3') as f:
    data = json.load(f)

for event in data.get('events', []):
    segs = event.get('segs', [])
    if not segs:
        continue
    start_ms = event.get('tStartMs', 0)
    duration_ms = event.get('dDurationMs', 0)
    text = ''.join(s.get('utf8', '') for s in segs).strip()
    if not text or text == '\n':
        continue
    s = start_ms / 1000
    e = (start_ms + duration_ms) / 1000
    print(f'[{int(s//60):02d}:{int(s%60):02d} - {int(e//60):02d}:{int(e%60):02d}] {text}')
" > "$WORK_DIR/transcript.txt"
```

请阅读 `$WORK_DIR/transcript.txt` 文件，以获取包含时间戳的完整字幕内容。

### 备选方案：无法获取字幕

如果视频中完全没有字幕，请通知用户，并继续进行仅基于视觉内容的分析。

## 第 4 步：下载视频并提取视频帧

### 第 4a 步：下载视频（720p 分辨率的视频即可用于帧分析）

```bash
yt-dlp -f "bestvideo[height<=720]+bestaudio/best[height<=720]" \
       -o "$WORK_DIR/video.mp4" "$VIDEO_URL"
```

### 第 4b 步：获取视频的准确时长

```bash
DURATION=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$WORK_DIR/video.mp4")
```

### 第 4c 步：使用自适应间隔策略提取视频帧

根据视频时长选择合适的提取间隔：

| 视频时长 | 提取间隔 | 大约提取的帧数 | 选择理由 |
|----------|----------|-----------------|-----------|
| < 5 分钟 | 10 秒 | 20-30 帧 | 足够详细分析 |
| 5-20 分钟 | 20 秒 | 15-60 帧 | 在覆盖范围和视频质量之间取得平衡 |
| 20-60 分钟 | 30-45 秒 | 30-120 帧 | 专注于关键场景 |
| > 60 分钟 | 60 秒 | 60-120 帧以上 | 询问用户是否需要关注特定时间段 |

```bash
# Example for a 5-20 minute video (interval=20):
ffmpeg -i "$WORK_DIR/video.mp4" -vf "fps=1/20" -q:v 3 "$WORK_DIR/frames/frame_%04d.jpg" 2>&1
```

**用于场景切换检测（软件操作指南、用户界面演示）**

```bash
ffmpeg -i "$WORK_DIR/video.mp4" \
       -vf "select='gt(scene,0.3)',showinfo" \
       -vsync vfr -q:v 3 "$WORK_DIR/frames/scene_%04d.jpg" 2>&1
```

### 第 4d 步：为每一帧计算时间戳

对于固定间隔提取帧的情况，第 N 帧的时间戳为 `(N-1) * 提取间隔` 秒。

```
frame_0001.jpg -> 0:00
frame_0002.jpg -> 0:20
frame_0003.jpg -> 0:40
...
```

## 第 5 步：将视频帧与文字记录同步

对于每一帧：
1. 计算该帧的时间戳（以秒为单位）
2. 找到对应的时间戳范围内的文字记录片段
3. 创建一个包含时间戳、文字记录和帧路径的同步对：`{timestamp, transcript_text, frame_path}`

这可以通过手动完成，也可以通过简单的查找工具来实现——无需使用外部脚本。

## 第 6 步：多模态分析

### 第 6a 步：读取并分析每一帧

使用 `Read` 工具（或 `view` 工具）查看每一帧的内容。对于每一帧，需要考虑以下方面：
- **用户界面元素**：可见的按钮、菜单、对话框、设置面板
- **屏幕上的文本**：代码、标签、错误信息、URL、终端输出
- **图表/图形**：图表、流程图、架构图
- **物理操作**：手部动作、工具使用情况（适用于物理操作相关的教程）
- **变化**：与上一帧相比发生了哪些变化？

### 第 6b 步：整合音频和视觉信息

对于每一个关键时刻，将音频和视觉信息结合起来进行分析：

```
Segment [TIMESTAMP]:
  SAID: "Click the blue button in the top right"
  SHOWN: Settings page screenshot, blue "Save" button highlighted
         in top-right corner, cursor pointing at it
  SYNTHESIS: -> On the Settings page, click the blue "Save" button
               in the top-right corner
```

### 第 6c 步：识别仅通过视觉信息可以获取的内容

标记那些在音频中未出现的视觉信息：
- 具体的按钮名称、菜单路径、用户界面的确切位置
- 屏幕上显示但未朗读的代码
- 可见的错误信息
- 动作前的变化与动作后的变化

## 输出格式

根据用户的需求生成相应的输出格式：

### 格式 A：逐步指导（最常见格式）

```markdown
# [Video Title] — Guide

## Step 1: [Action] (00:15)
[Description based on transcript + frame analysis]
> Visual: [What the screen/image shows at this point]

## Step 2: [Action] (00:42)
[...]
```

### 格式 B：包含视觉元素的全面总结

```markdown
# [Video Title] — Summary

## Overview
[2-3 sentence summary of the entire video]

## Key Sections

### [Section Name] (00:00 - 02:30)
[Summary of this section]
- Key visual: [Description of what's shown]
- Key quote: "[Important spoken content]"

### [Section Name] (02:30 - 05:00)
[...]

## Key Takeaways
- [Takeaway 1]
- [Takeaway 2]
```

### 格式 C：技术细节分析

分别分析音频和视觉信息，并检测两者之间的差异：

```markdown
# [Video Title] — Technical Analysis

## Audio Channel Analysis
[What was said, key points, structure]

## Visual Channel Analysis
[What was shown, UI flows, code, diagrams]

## Channel Synchronization
[Where audio and visual complement each other]

## Visual-Only Information
[Important details only visible in frames, not mentioned in speech]
```

## 错误处理与特殊情况

| 问题 | 解决方案 |
|---------|----------|
| 下载字幕时遇到 HTTP 429 错误 | 使用 `--dump-json` 方法（步骤 3a）。如果 `curl` 也被阻止，请等待 10-15 秒后使用不同的用户代理重新尝试 |
| 完全无法获取字幕 | 继续进行仅基于视觉内容的分析，并通知用户 |
| 原始音频语言不在自动字幕列表中 | 原始语言是视频的原始语言，自动字幕是翻译版本。请从任何自动字幕 URL 中删除 `&tlang=XX` 以获取原始语言的字幕 |
| `transcript.json3` 文件内容为 HTML 而非 JSON | YouTube 返回了错误页面。等待 10 秒后，使用以下命令重新尝试：`curl -s --user-agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "$URL"` |
| 视频时长超过 60 分钟 | 询问用户是否需要关注特定的时间范围或章节 |
| 视频质量较差/帧模糊 | 使用更短的间隔提取更多帧以改善分析效果 |
| 视频受到年龄限制或属于私密视频 | 通知用户无法访问该视频。如果用户有权限，可以尝试使用 `--cookies-from-browser` 参数 |
| 使用 yt-dlp 下载失败 | 尝试使用另一种格式：`-f "best[height<=720]"`（不分离音频和视频流）

## 清理临时文件

分析完成后，请删除所有临时文件：

```bash
rm -rf "$WORK_DIR"
```

## 优化建议

- **针对软件操作指南**：使用场景切换检测功能，因为用户界面的切换会形成明显的视觉间隔
- **针对物理操作相关的教程**：使用更短的提取间隔（10-15 秒），以便更清晰地捕捉细微的动作
- **先阅读字幕**：在提取帧之前先阅读字幕，寻找如 “如您所见” 或 “让我为您展示” 等提示性语句，这些语句通常表示重要的视觉内容
- **结合上下文进行分析**：在分析每一帧时，务必提供相应的文字记录背景信息。演讲者通常会解释即将展示的内容
- **分批读取帧**：每次读取 8-10 帧，以便保持帧之间的上下文连贯性并检测视觉变化
- **并行处理音频和视频数据**：在处理字幕的同时开始下载视频，以节省时间