---
name: youtube-summarize
description: 通过提取视频的文字记录（字幕）来总结 YouTube 视频内容。当您需要快速了解视频的概要、提取关键信息，或在不观看视频的情况下分析其内容时，可以使用这种方法。
metadata: {"openclaw":{"requires":{"bins":["yt-dlp"]},"install":[{"id":"python","kind":"pip","package":"yt-dlp","bins":["yt-dlp"],"label":"Install yt-dlp (pip)"}]}}
---

# YouTube 视频摘要工具

## 设置

安装 yt-dlp：
```bash
pip install yt-dlp
```

## 提取字幕

- 获取自动生成的字幕：
```bash
yt-dlp --write-auto-sub --sub-lang en --skip-download --sub-format vtt -o "%(title)s" "VIDEO_URL"
```

- 获取手动添加的字幕（如果有的话）：
```bash
yt-dlp --write-sub --sub-lang en --skip-download --sub-format vtt -o "%(title)s" "VIDEO_URL"
```

- 列出可用的字幕：
```bash
yt-dlp --list-subs "VIDEO_URL"
```

## 提取纯文本

- 下载视频并转换为纯文本：
```bash
yt-dlp --write-auto-sub --sub-lang en --skip-download --sub-format vtt -o "transcript" "VIDEO_URL" && \
sed -e '/^$/d' -e '/^[0-9]/d' -e '/-->/d' -e 's/<[^>]*>//g' transcript.en.vtt | sort -u > transcript.txt
```

## 将字幕快速输出到标准输出（stdout）：
```bash
yt-dlp --write-auto-sub --sub-lang en --skip-download --sub-format json3 -o - "VIDEO_URL" 2>/dev/null | \
python3 -c "
import sys, json
data = json.load(sys.stdin)
for event in data.get('events', []):
    for seg in event.get('segs', []):
        if text := seg.get('utf8', '').strip():
            print(text, end=' ')"
```

## 获取视频元数据

```bash
yt-dlp --dump-json "VIDEO_URL" | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(f\"Title: {d['title']}\")
print(f\"Channel: {d['channel']}\")
print(f\"Duration: {d['duration']//60}:{d['duration']%60:02d}\")
print(f\"Views: {d.get('view_count', 'N/A'):,}\")
print(f\"Upload: {d.get('upload_date', 'N/A')}\")
print(f\"Description:\n{d.get('description', '')[:500]}...\")"
```

## 摘要生成流程

1. 提取字幕：
```bash
yt-dlp --write-auto-sub --sub-lang en --skip-download -o "video" "VIDEO_URL"
```

2. 将 VTT 格式的字幕转换为纯文本：
```bash
python3 -c "
import re
with open('video.en.vtt', 'r') as f:
    content = f.read()
# Remove VTT headers and timestamps
content = re.sub(r'WEBVTT.*?\n\n', '', content, flags=re.DOTALL)
content = re.sub(r'\d+:\d+:\d+\.\d+ --> \d+:\d+:\d+\.\d+.*?\n', '', content)
content = re.sub(r'<[^>]+>', '', content)
lines = [l.strip() for l in content.split('\n') if l.strip()]
unique = []
for l in lines:
    if l not in unique[-1:]:
        unique.append(l)
print(' '.join(unique))" > transcript.txt
```

3. 将处理后的字幕发送给大型语言模型（LLM）进行摘要生成（此时字幕已准备好供 Claude 分析）

## 多语言支持

- 提取其他语言的字幕：
```bash
# Russian
yt-dlp --write-auto-sub --sub-lang ru --skip-download "VIDEO_URL"

# Spanish
yt-dlp --write-auto-sub --sub-lang es --skip-download "VIDEO_URL"

# Multiple languages
yt-dlp --write-auto-sub --sub-lang "en,ru,es" --skip-download "VIDEO_URL"
```

## 提取视频章节

- 获取视频的章节信息（如果有的话）：
```bash
yt-dlp --dump-json "VIDEO_URL" | python3 -c "
import sys, json
d = json.load(sys.stdin)
for ch in d.get('chapters', []):
    start = int(ch['start_time'])
    print(f\"{start//60}:{start%60:02d} - {ch['title']}\")"
```

## 常见选项

| 选项          | 描述                                      |
|----------------|-----------------------------------------|
| `--sub-lang en`    | 字幕语言（en, ru, es, de, fr 等）                         |
| `--write-auto-sub`   | 获取自动生成的字幕                         |
| `--write-sub`    | 获取手动添加的字幕                         |
| `--sub-format vtt`   | 输出字幕格式（vtt, srt, json3）                     |
| `--skip-download` | 不下载视频                             |

## 注意事项

- 自动生成的字幕可能存在错误；
- 并非所有视频都配有字幕；
- 有些视频的字幕可能被上传者禁用了；
- 使用 `--sub-lang` 时请指定正确的语言代码；
- 该工具更适合处理口语内容（如讲座、播客、教程等）。