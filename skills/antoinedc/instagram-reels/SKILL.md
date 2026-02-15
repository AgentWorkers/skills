---
name: instagram-reels
version: "1.0.0"
description: 下载 Instagram 的 Reels 视频，转录其中的音频内容，并提取视频的文字说明。只需分享 Reel 的 URL，即可获得包含完整文字说明及原始描述的文件。
metadata:
  openclaw:
    requires:
      env:
        - GROQ_API_KEY
      bins:
        - curl
        - yt-dlp
        - ffmpeg
        - python3
    primaryEnv: GROQ_API_KEY
    homepage: https://groq.com
---

# Instagram Reels 技能

下载 Instagram Reels 视频，转录其中的音频内容，并提取视频的标题/描述信息。

## 准备工作

1. 安装所需工具：

```bash
pip install yt-dlp
apt install ffmpeg    # or: brew install ffmpeg
```

2. 在 [https://console.groq.com](https://console.groq.com) 获取免费的 Groq API 密钥。
3. 设置环境变量：

```bash
export GROQ_API_KEY="your-groq-api-key"
```

## 使用方法

分三步处理视频：提取元数据、下载音频、转录音频内容。

### 第一步：提取元数据和音频 URL

```bash
yt-dlp --write-info-json --skip-download -o "/tmp/reel" "REEL_URL"
```

该步骤会生成 `/tmp/reel.info.json` 文件，其中包含视频的标题、上传者信息、CDN 链接以及其他元数据。对于公开发布的视频，无需登录即可操作。

### 第二步：下载音频并转换为 MP3 格式

从元数据中提取音频的 CDN 链接，然后直接下载该音频文件：

```bash
AUDIO_URL=$(python3 -c "
import json
d = json.load(open('/tmp/reel.info.json'))
for f in d.get('formats', []):
    if f.get('ext') == 'm4a':
        print(f['url'])
        break
")
curl -sL "$AUDIO_URL" -o /tmp/reel-audio.m4a
ffmpeg -y -i /tmp/reel-audio.m4a -acodec libmp3lame -q:a 4 /tmp/reel-audio.mp3
```

### 第三步：使用 Groq Whisper 进行音频转录

```bash
curl -s https://api.groq.com/openai/v1/audio/transcriptions \
  -H "Authorization: Bearer $GROQ_API_KEY" \
  -F "file=@/tmp/reel-audio.mp3" \
  -F "model=whisper-large-v3-turbo" \
  -F "response_format=verbose_json"
```

该步骤会返回一个 JSON 文件，其中包含完整的转录文本（`text`）以及带有时间戳的音频片段（`segments`）。系统会自动检测音频语言。

### 从元数据中提取视频标题

```bash
python3 -c "
import json
d = json.load(open('/tmp/reel.info.json'))
print('Caption:', d.get('description', 'No caption'))
print('Author:', d.get('uploader', 'Unknown'))
print('Duration:', round(d.get('duration', 0)), 'seconds')
"
```

## 注意事项

- 公开发布的视频无需认证即可提取元数据。
- 对于私密发布的视频，需要使用以下命令传递 Cookie：`yt-dlp --cookies /path/to/cookies.txt --write-info-json --skip-download -o "/tmp/reel" "REEL_URL"`
- 可以使用浏览器扩展程序（如 “Get Cookies.txt LOCALLY”）来保存 Cookie。
- Groq Whisper 是免费服务，但存在使用频率限制，处理结果通常在 1-2 秒内返回。
- 每次请求的最大音频时长为 25 分钟。
- 使用完成后，请清理临时文件：`rm -f /tmp/reel.info.json /tmp/reel-audio.*`
- 该工具同样适用于 TikTok、YouTube Shorts 以及其他受 yt-dlp 支持的平台。

## 示例

```bash
# Full transcription pipeline
yt-dlp --write-info-json --skip-download -o "/tmp/reel" "https://www.instagram.com/reel/ABC123/" && \
AUDIO_URL=$(python3 -c "import json; [print(f['url']) for f in json.load(open('/tmp/reel.info.json')).get('formats',[]) if f.get('ext')=='m4a'][:1]") && \
curl -sL "$AUDIO_URL" -o /tmp/reel-audio.m4a && \
ffmpeg -y -i /tmp/reel-audio.m4a -acodec libmp3lame -q:a 4 /tmp/reel-audio.mp3 2>/dev/null && \
curl -s https://api.groq.com/openai/v1/audio/transcriptions \
  -H "Authorization: Bearer $GROQ_API_KEY" \
  -F "file=@/tmp/reel-audio.mp3" \
  -F "model=whisper-large-v3-turbo" \
  -F "response_format=verbose_json"

# Just get the caption (no transcription)
yt-dlp --write-info-json --skip-download -o "/tmp/reel" "https://www.instagram.com/reel/ABC123/" && \
python3 -c "import json; d=json.load(open('/tmp/reel.info.json')); print(d.get('description',''))"

# Transcribe a TikTok video (same pipeline)
yt-dlp --write-info-json --skip-download -o "/tmp/reel" "https://www.tiktok.com/@user/video/123" && \
AUDIO_URL=$(python3 -c "import json; [print(f['url']) for f in json.load(open('/tmp/reel.info.json')).get('formats',[]) if f.get('ext')=='m4a'][:1]") && \
curl -sL "$AUDIO_URL" -o /tmp/reel-audio.m4a && \
ffmpeg -y -i /tmp/reel-audio.m4a -acodec libmp3lame -q:a 4 /tmp/reel-audio.mp3 2>/dev/null && \
curl -s https://api.groq.com/openai/v1/audio/transcriptions \
  -H "Authorization: Bearer $GROQ_API_KEY" \
  -F "file=@/tmp/reel-audio.mp3" \
  -F "model=whisper-large-v3-turbo" \
  -F "response_format=verbose_json"
```