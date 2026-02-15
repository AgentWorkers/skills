# youtube-apify-transcript

通过 APIFY API 获取 YouTube 视频的字幕（支持来自云服务器的请求，可绕过 YouTube 的机器人检测机制）。

## 为什么选择 APIFY？

YouTube 会阻止来自云服务器（如 AWS、GCP 等）的字幕请求。APIFY 通过使用居民区代理来发送请求，从而可靠地规避了机器人检测机制。

## 免费 tier

- **每月 5 美元的免费额度**（约可获取 714 个视频的字幕）
- 无需信用卡
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
2. 获取您的 API 令牌：https://console.apify.com/account/integrations
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
# Get transcript as text
python3 scripts/fetch_transcript.py "https://www.youtube.com/watch?v=VIDEO_ID"

# Short URL also works
python3 scripts/fetch_transcript.py "https://youtu.be/VIDEO_ID"
```

### 可选参数

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

### 输出格式

- **文本格式（默认）：**
```
Hello and welcome to this video.
Today we're going to talk about...
```

- **JSON 格式（--json）：**
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
- YouTube URL 不合法
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