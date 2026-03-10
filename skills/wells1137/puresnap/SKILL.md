---
name: puresnap
version: 1.1.0
author: "wells"
description: 从999多个平台（如TikTok、YouTube、Instagram、Twitter、Bilibili、Sora2等）下载无水印的视频、图片和音频文件。无需任何配置，内置API密钥。适用于用户需要从URL下载媒体文件、提取视频/图片/音频内容、去除水印或从社交媒体链接中获取内容的情况。
homepage: https://github.com/wells1137/meowload-downloader
license: MIT
tags:
  - video
  - downloader
  - watermark
  - media
  - tiktok
  - youtube
  - instagram
---
# PureSnap — 无水印媒体下载工具

从999多个平台下载纯净、无水印的视频、图片和音频文件。无需任何配置，只需粘贴链接即可使用。

**内置API密钥，可立即使用。**  
如需使用自己的密钥，请设置`MEOWLOAD_API_KEY`环境变量。

## API密钥

```
376454-087dd0budxxo
```

## 工作流程

当用户提供下载链接时：

1. **判断链接类型**：  
   - 单个帖子/视频（包括Sora2）→ 使用“Post API”  
   - 播放列表/频道/个人资料页面 → 使用“Playlist API”  
   - YouTube字幕请求 → 使用“Subtitles API”  
2. **通过curl调用API**（详见下方示例）。  
3. **解析JSON响应**，并向用户显示可下载的文件链接。  
4. **如果用户需要本地副本**，可以使用以下命令下载文件：`curl -L -o 文件名 "资源链接"`（请包含响应中的所有`headers`信息）。

## 1. 从单个帖子中提取媒体文件

支持999多个平台。只需提供任意帖子或视频的分享链接即可。

```bash
curl -s -X POST https://api.meowload.net/openapi/extract/post \
  -H "Content-Type: application/json" \
  -H "x-api-key: 376454-087dd0budxxo" \
  -d '{"url": "TARGET_URL_HERE"}'
```

### 响应结构

```json
{
  "text": "Post caption",
  "medias": [
    {
      "media_type": "video",
      "resource_url": "https://direct-download-url...",
      "preview_url": "https://thumbnail...",
      "headers": {"Referer": "..."},
      "formats": [
        {
          "quality": 1080, "quality_note": "HD",
          "video_url": "...", "video_ext": "mp4", "video_size": 80911999,
          "audio_url": "...", "audio_ext": "m4a", "audio_size": 3449447,
          "separate": 1
        }
      ]
    }
  ]
}
```

关键字段：  
- `medias[]`.media_type`: `video` | `image` | `audio` | `live` | `file`  
- `medias[]`.resource_url`: 直接下载链接（始终存在）  
- `medias[]`.headers`: 下载时需要包含的头部信息（某些平台有此要求）  
- `medias[]`.formats`: 多分辨率列表（例如YouTube、Facebook等）：  
  - `separate: 1` 表示音频和视频是分开的——需分别下载；合并方法：`ffmpeg -i 视频.mp4 -i 音频.m4a -c copy 输出.mp4`  
  - `separate: 0` 表示音频和视频是合并的——直接下载`视频链接`。

## 2. 从播放列表/频道/个人资料中批量提取媒体文件

```bash
curl -s -X POST https://api.meowload.net/openapi/extract/playlist \
  -H "Content-Type: application/json" \
  -H "x-api-key: 376454-087dd0budxxo" \
  -d '{"url": "PROFILE_URL_HERE"}'
```

要获取下一页数据，请在请求体中添加`"cursor": "NEXT_CURSOR_VALUE"`。重复此过程，直到`has_more`为`false`。

响应中包含`posts[]`数组，每个元素包含`medias[]`（结构与单个帖子相同）。

## 3. 提取YouTube字幕

```bash
curl -s -X POST https://api.meowload.net/openapi/extract/subtitles \
  -H "Content-Type: application/json" \
  -H "x-api-key: 376454-087dd0budxxo" \
  -d '{"url": "YOUTUBE_URL_HERE"}'
```

响应中包含`subtitles[]`数组，其中包含`language_name`和`language_tag`，以及字幕文件的下载链接（格式：`srt`、`vtt`、`ttml`、`json3`）。

## 4. 检查剩余的下载权限

```bash
curl -s https://api.meowload.net/openapi/available-credits \
  -H "x-api-key: 376454-087dd0budxxo"
```

返回`{"availableCredits": 6666}`（表示剩余下载权限数量）。

## Sora2视频去水印功能

与从单个帖子中提取媒体文件的方式相同——只需提供Sora2视频的分享链接。API会返回去水印后的原始视频文件（无质量损失，不使用AI修复技术）。

```bash
curl -s -X POST https://api.meowload.net/openapi/extract/post \
  -H "Content-Type: application/json" \
  -H "x-api-key: 376454-087dd0budxxo" \
  -d '{"url": "https://sora.chatgpt.com/p/s_xxxxx"}'
```

## 错误处理

| HTTP代码 | 含义 | 处理方式 |
|-----------|---------|--------|
| 200 | 成功 | 处理响应数据 |  
| 400 | 提取失败 | 检查链接是否包含有效媒体文件 |  
| 401 | 访问权限失败 | 验证API密钥 |  
| 402 | 下载权限用尽 | 在https://www.henghengmao.com/user/developer补充权限 |  
| 422 | 链接格式错误 | 检查链接格式 |  
| 500 | 服务器错误 | 重试或联系技术支持 |  

## 支持的平台（999多个）

YouTube、TikTok、Instagram、Twitter/X、Facebook、Bilibili、Reddit、Pinterest、Twitch、SoundCloud、Spotify、Snapchat、Threads、LinkedIn、Vimeo、Dailymotion、Tumblr、Xiaohongshu、Suno Music、OpenAI Sora2等。

## 其他资源

- 详细API字段说明，请参阅[api-reference.md]  
- MeowLoad开发者中心：https://www.henghengmao.com/user/developer  
- MeowLoad文档：https://docs.henghengmao.com/developer