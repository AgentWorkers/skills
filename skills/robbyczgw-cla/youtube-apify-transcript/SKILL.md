---
name: youtube-apify-transcript
version: 1.1.2
description: 通过 APIFY API 获取 YouTube 视频的字幕。该服务支持来自云服务器（如 Hetzner、AWS 等）的请求，并能绕过 YouTube 的机器人检测机制。免费 tier 每月提供 5 美元的信用额度（可转录约 714 个视频），无需使用信用卡支付。
tags: [youtube, transcript, apify, video, subtitles, captions, cloud-ip, free-tier, web-scraping]
---

# youtube-apify-transcript

通过 APIFY API 获取 YouTube 视频的字幕（支持来自云服务器的请求，可绕过 YouTube 的机器人检测机制）。

## 为什么选择 APIFY？

YouTube 会阻止来自云服务器（如 AWS、GCP 等）的字幕请求。APIFY 通过使用居民代理来发起请求，从而可靠地规避了机器人检测机制。

## 免费 tier

- **每月 5 美元的免费额度**（约可获取 714 个视频的字幕）
- 无需使用信用卡
- 非常适合个人使用

## 费用

- **每个视频 0.007 美元**（不到 1 分钱！）
- 可在以下链接查看使用情况：https://console.apify.com/billing

## 链接

- 🔗 [APIFY 定价](https://apify.com/pricing)
- 🔑 [获取 API 密钥](https://console.apify.com/account/integrations)
- 🎬 [YouTube 字幕插件](https://apify.com/karamelo/youtube-transcripts)

## 设置

1. 创建免费的 APIFY 账户：https://apify.com/
2. 获取 API 令牌：https://console.apify.com/account/integrations
3. 设置环境变量：

```bash
# Add to ~/.bashrc or ~/.zshrc
export APIFY_API_TOKEN="apify_api_YOUR_TOKEN_HERE"

# Or use .env file (never commit this!)
echo 'APIFY_API_TOKEN=apify_api_YOUR_TOKEN_HERE' >> .env
```

## 使用方法

### 基本用法

```bash
# Get transcript as text (uses cache by default)
python3 scripts/fetch_transcript.py "https://www.youtube.com/watch?v=VIDEO_ID"

# Short URL also works
python3 scripts/fetch_transcript.py "https://youtu.be/VIDEO_ID"
```

### 配置选项

```bash
# Output to file
python3 scripts/fetch_transcript.py "URL" --output transcript.txt

# JSON format (includes timestamps)
python3 scripts/fetch_transcript.py "URL" --json

# Both: JSON to file
python3 scripts/fetch_transcript.py "URL" --json --output transcript.json

# Specify language preference
python3 scripts/fetch_transcript.py "URL" --lang de
```

### 缓存（节省费用！）

系统会默认将字幕缓存到本地。对同一视频重复请求时，费用为 0 美元。

```bash
# First request: fetches from APIFY ($0.007)
python3 scripts/fetch_transcript.py "URL"

# Second request: uses cache (FREE!)
python3 scripts/fetch_transcript.py "URL"
# Output: [cached] Transcript for: VIDEO_ID

# Bypass cache (force fresh fetch)
python3 scripts/fetch_transcript.py "URL" --no-cache

# View cache stats
python3 scripts/fetch_transcript.py --cache-stats

# Clear all cached transcripts
python3 scripts/fetch_transcript.py --clear-cache
```

缓存位置：`skill` 目录下的 `.cache/` 文件夹（可通过 `YT_TRANSCRIPT_CACHE_DIR` 环境变量进行自定义）

### 批量处理

可以同时处理多个视频：

```bash
# Create a file with URLs (one per line)
cat > urls.txt << EOF
https://youtube.com/watch?v=VIDEO1
https://youtu.be/VIDEO2
https://youtube.com/watch?v=VIDEO3
EOF

# Process all URLs
python3 scripts/fetch_transcript.py --batch urls.txt

# Output: 
# [1/3] Fetching VIDEO1...
# [2/3] [cached] VIDEO2
# [3/3] Fetching VIDEO3...
# Batch complete: 2 fetched, 1 cached, 0 failed
# [Cost: ~$0.014 for 2 API call(s)]

# Batch with JSON output to file
python3 scripts/fetch_transcript.py --batch urls.txt --json --output all_transcripts.json
```

### 输出格式

- **文本格式（默认）：**
```
Hello and welcome to this video.
Today we're going to talk about...
```

- **JSON 格式（使用 `--json` 参数）：**
```json
{
  "video_id": "dQw4w9WgXcQ",
  "title": "Video Title",
  "transcript": [
    {"start": 0.0, "duration": 2.5, "text": "Hello and welcome"},
    {"start": 2.5, "duration": 3.0, "text": "to this video"}
  ],
  "full_text": "Hello and welcome to this video..."
}
```

## 错误处理

该脚本能够处理以下常见错误：
- YouTube URL 无效
- 视频没有字幕
- API 配额已用完
- 网络错误

## 元数据

```yaml
metadata:
  clawdbot:
    emoji: "📹"
    requires:
      env: ["APIFY_API_TOKEN"]
      bins: ["python3"]
```