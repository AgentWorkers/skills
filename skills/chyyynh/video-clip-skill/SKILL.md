---
name: clip-local
description: 使用 `yt-dlp` 和 `ffmpeg` 将 YouTube 视频下载并保存到本地。支持自动提取视频中的精彩片段（高亮部分）、添加字幕以及生成卡拉OK 格式的字幕。当用户需要剪辑视频、提取高亮部分或生成字幕时，该工具会自动启动。通过设置环境变量 `GROQ_API_KEY`，可以在 YouTube 没有字幕的情况下使用 `Whisper` 服务进行转录。
argument-hint: "[youtube-url-or-id] [start] [end] [output]"
---
# 视频剪辑（本地）

需要 `yt-dlp`、`ffmpeg` 和 `python3`。可以通过运行 `command -v` 来检查这些工具是否已安装。

## 查找插件脚本

此插件附带了 ASS 卡拉OK 生成器。请在开始时找到该生成器文件（此步骤仅搜索插件自带的文件）：

```bash
ASS_SCRIPT=$(find ~/.claude/plugins -path '*/clip-local/*/scripts/ass-karaoke.py' 2>/dev/null | head -1)
```

## 自动高亮显示模式

当用户未指定开始/结束时间时（例如：“帮我剪辑这个视频的精华部分”或“剪辑最精彩的部分”）：

1. 下载完整的字幕文件（参见步骤 1–2）。
2. 阅读整个字幕文件，挑选出 3–5 个高亮片段。对于每个片段，记录以下信息：
   - 开始和结束的时间戳。
   - 该片段有趣的简要描述（关键信息、搞笑时刻、戏剧性转折等）。
3. 以编号的形式向用户展示这些高亮片段，并询问用户希望剪辑哪些片段。
4. 仅剪辑用户选中的片段，然后继续执行后续的处理流程（如翻译、添加字幕等）。

## 处理流程

### 1. 获取视频信息及原始语言

```bash
yt-dlp --print title --print duration_string --print language \
  --no-playlist --no-warnings --force-ipv4 "<URL>"
```

第三行表示视频的原始语言代码（例如 `en`、`en-US`、`ja`、`zh-Hant`）。使用该代码作为下载字幕的依据。

### 2. 下载原始语言的字幕文件

```bash
yt-dlp --write-auto-sub --sub-lang "<LANG>*" --sub-format vtt --skip-download \
  --no-playlist --no-warnings --force-ipv4 \
  --extractor-args 'youtube:player-client=default,mweb' \
  -o "subs" "<URL>"
```

将 `<LANG>` 替换为步骤 1 中得到的原始语言代码（例如 `en`、`ja`）。通配符 `*` 可匹配类似 `en-orig` 的变体。请不要使用 YouTube 自动生成的字幕——它们的质量较低。所有字幕翻译工作都由您完成。

### 3. 修剪 VTT 文件以匹配剪辑范围

在剪辑视频片段时（例如 10–130 秒），需要过滤 VTT 文件，仅保留时间戳在该范围内的片段。**请保留原始的时间戳，不要进行任何调整**。`ass-karaoke.py` 脚本中的 `--offset` 参数用于处理时间偏移问题。

在过滤过程中，请删除时间戳行中的多余元数据（例如 `align:start position:0%`），仅保留 `HH:MM:SS.mmm --> HH:MM:SS.mmm` 的格式。ASS 解析器要求时间戳行格式简洁明了。

### 4. 翻译字幕

编写并执行一个 Python 脚本，完成以下操作：
1. 解析修剪后的 VTT 文件（格式为 `HH:MM:SS.mmm --> HH:MM:SS.mmm` + 文本行）。
2. 将所有文本行收集到一个列表中。
3. 翻译这些文本行。
4. 生成新的 VTT 文件，保持时间戳不变，但文本内容为翻译后的内容。

示例脚本结构如下：
```python
import re

# Parse original VTT
with open("clip.vtt") as f:
    content = f.read()
cues = re.findall(r'(\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3})\n((?:(?!\d{2}:\d{2}).+\n?)*)', content)

# Translations — fill this list with your translations, one per cue
translations = [
    "translated line 1",
    "translated line 2",
    # ...
]

# Write translated VTT
with open("clip_translated.vtt", "w") as f:
    f.write("WEBVTT\n\n")
    for (timestamp, _), translation in zip(cues, translations):
        f.write(f"{timestamp}\n{translation.strip()}\n\n")
```

使用填充好的 `translations` 列表生成相应的 Python 脚本，然后执行它。这样可以确保时间戳的准确性以及 VTT 格式的正确性。

### 5. 生成 ASS 卡拉OK 字幕

```bash
python3 "$ASS_SCRIPT" <original.vtt> -o subs.ass -t <translated.vtt> --offset <START_SECONDS>
```

- 第一个参数是原始语言的 VTT 文件（其中包含卡拉OK 的时间信息）。
- `-t` 参数是翻译后的 VTT 文件（显示在卡拉OK 字幕下方）。
- `--offset` 参数用于调整剪辑的开始时间。

该脚本支持处理 YouTube 的滚动字幕去重问题、中文/日文字符的分割问题以及双语字幕的显示方式。

### 6. 获取视频和音频的流媒体地址

**通过一次调用** 获取视频和音频的流媒体地址：

```bash
URLS=$(yt-dlp --get-url -f 'bv[height<=720]+ba/b[height<=720]' \
  --no-playlist --no-warnings --force-ipv4 \
  --extractor-args 'youtube:player-client=default,mweb' "<URL>")
VIDEO_URL=$(echo "$URLS" | head -1)
AUDIO_URL=$(echo "$URLS" | tail -1)
```

然后使用 `ffmpeg` 进行剪辑：
- 如果有字幕：`-vf "ass=subs.ass" -c:v libx264 -preset fast -crf 23 -c:a aac -b:a 128k -movflags +faststart`
- 如果没有字幕：`-c copy -avoid_negative_ts make_zero`
- 在每个视频文件前使用 `-ss <START>` 参数指定开始剪辑的位置。
- 分离视频和音频流：`-map 0:v:0 -map 1:a:0`

### 备用方案（无 YouTube 字幕）

如果 `yt-dlp` 无法自动获取字幕，并且用户设置了 `GROQ_API_KEY`：

1. 下载音频文件：`yt-dlp -f ba -x --audio-format mp3 --postprocessor-args 'ffmpeg:-ac 1 -ar 16000 -b:a 64k`
2. 使用 `POST https://api.groq.com/openai/v1/audio/transcriptions` 进行语音转文字处理，设置 `model=whisper-large-v3` 和 `response_format=verbose_json`。
3. 将转录结果转换为 VTT 格式。

如果用户未设置 `GROQ_API_KEY`，请告知用户无法获取字幕，并询问用户是否希望继续剪辑（不添加字幕或设置 API 密钥）。

## 常见问题

- YouTube 的流量限制：将 cookies 存储到文件中，然后使用 `--cookies cookies.txt` 参数来绕过限制。
- 如果系统中缺少中文/日文字体的支持，可以在 macOS 上执行 `brew install font-noto-sans-cjk-tc` 来安装相应的字体。
- Groq 对音频文件的大小有限制（最大 25MB），对于超过 50 分钟的视频需要分割音频文件。
- 流媒体地址可能会在 6 小时后失效，此时需要重新获取地址。
- 添加字幕时可能会对视频进行重新编码（对于 60 秒的片段，重新编码时间约为 1–3 分钟）。