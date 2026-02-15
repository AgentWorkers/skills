---
name: fliz-ai-video-generator
version: 1.0.0
author: gregorybeyrouti
description: |
  Complete integration guide for the Fliz REST API - an AI-powered video generation platform that transforms text content into professional videos with voiceovers, AI-generated images, and subtitles.
  
  Use this skill when:
  - Creating integrations with Fliz API (WordPress, Zapier, Make, n8n, custom apps)
  - Building video generation workflows via API
  - Implementing webhook handlers for video completion notifications
  - Developing automation tools that create, manage, or translate videos
  - Troubleshooting Fliz API errors or authentication issues
  - Understanding video processing steps and status polling
  
  Key capabilities: video creation from text/Brief, video status monitoring, translation, duplication, voice/music listing, webhook notifications.
homepage: https://fliz.ai
tags: [video, ai, fliz, content-creation, automation, api]
metadata:
  clawdbot:
    emoji: "🎬"
    primaryEnv: FLIZ_API_KEY
---

# Fliz API集成技能

**功能概述：**  
通过编程方式将文本内容转换为AI生成的视频。

## 快速参考  

| 项目 | 详细信息 |
|------|---------|
| 基本URL | `https://app.fliz.ai` |
| 认证 | 承载令牌（JWT） |
| 获取令牌 | `https://app.fliz.ai/api-keys` |
| API文档 | `https://app.fliz.ai/api-docs` |
| 数据格式 | JSON |

## 认证  

所有请求均需要使用承载令牌（Bearer Token）进行身份验证：  
```bash
curl -X GET "https://app.fliz.ai/api/rest/voices" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json"
```

**测试连接：**  
调用 `GET /api/rest/voices`——如果令牌有效，将返回200状态码。

## 核心接口  

### 1. 创建视频  

**最小请求格式：**  
```json
{
  "fliz_video_create_input": {
    "name": "Video Title",
    "description": "Full content text to transform into video",
    "format": "size_16_9",
    "lang": "en"
  }
}
```  
**响应内容：**  
```json
{
  "fliz_video_create": {
    "video_id": "a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d"
  }
}
```  

> **重要提示：** `description` 字段必须包含完整的文本内容。Fliz不会从URL中提取内容——上游系统需要先获取并处理这些内容。  

### 2. 获取视频状态  

**通过调用此接口可跟踪视频生成进度。**  
检查 `step` 字段的值：  
| 步骤 | 状态 |  
|------|--------|  
| `pending` → `scrapping` → `script` → `image_*` → `speech` → `video_rendering` | 处理中 |
| `complete` | ✅ 已完成——`url` 字段包含MP4视频链接 |
| `failed` / `failed_unrecoverable` | ❌ 出错——请查看 `error` 字段 |
| `user_action` | ⚠️ 需要手动干预 |

### 3. 列出视频  

### 4. 翻译视频  

**将视频翻译成目标语言。**  

### 5. 复制视频  

### 6. 列出可用的语音/音乐资源  

## 视频创建参数  

**必填字段：**  
- `name`（字符串）：视频标题  
- `description`（字符串）：完整文本内容  
- `format`（枚举）：`size_16_9` | `size_9_16` | `square`  
- `lang`（字符串）：ISO 639-1语言代码（如 en, fr, es, de, pt 等）  

**可选自定义参数：**  
| 参数 | 说明 | 默认值 |  
|-------|-------------|---------|  
| `category` | 类型（`article`、`product`、`ad`） | `article` |  
| `script_style` | 叙述风格 | `auto` |  
| `image_style` | 视觉风格 | `hyperrealistic` |  
| `caption_style` | 字幕样式 | `animated_background` |  
| `caption_position` | 字幕位置（`bottom`、`center`、`bottom`） | `bottom` |  
| `caption_font` | 字体 | `poppins` |  
| `caption_color` | 十六进制颜色（#FFFFFF） | `white` |  
| `caption_uppercase` | 是否大写显示字幕 | `false` |  
| `voice_id` | 自定义语音ID | `auto` |  
| `is_male_voice` | 是否使用男性声音 | `auto` |  
| `music_id` | 音乐ID | `auto` |  
| `music_url` | 音乐URL | `null` |  
| `music_volume` | 音量（0-100） | `15` |  
| `watermark_url` | 水印图片URL | `null` |  
| `site_url` | CTA链接 | `null` |  
| `site_name` | CTA文本 | `null` |  
| `webhook_url` | 回调URL | `null` |  
| `is_automatic` | 是否自动处理 | `true` |  
| `video_animation_mode` | 视频动画模式（`full_video`、`hook_only`、`full_video`） | `full_video` |  
| `image_urls` | 图片URL数组 | `null` |  

> **注意：** 对于 `product` 和 `ad` 类型的视频，必须提供 `image_urls`（3-10 张图片）。  
完整的枚举值请参见 [references/enums-values.md]。  

## Webhook  

配置 `webhook_url` 以在视频生成完成或失败时接收通知：  
```json
{
  "event": "video.complete",
  "video_id": "a1b2c3d4-...",
  "step": "complete",
  "url": "https://cdn.fliz.ai/videos/xxx.mp4"
}
```  

## 错误处理  

| HTTP状态码 | 含义 | 应对措施 |  
|-----------|---------|--------|  
| 200 | 成功 | 继续操作 |  
| 400 | 请求错误 | 检查请求参数 |  
| 401 | 未经授权 | 令牌无效/已过期 |  
| 404 | 未找到视频 | 视频ID错误 |  
| 429 | 请求频率限制 | 请稍后重试 |  
| 500 | 服务器错误 | 请稍后重试 |  

## 集成方式  

### 推荐的轮询方式：**  
```
1. POST /api/rest/video → get video_id
2. Loop: GET /api/rest/videos/{id}
   - If step == "complete": done, get url
   - If step contains "failed": error
   - Else: wait 10-30s, retry
```  
### Webhook集成方式：**  
```
1. POST /api/rest/video with webhook_url
2. Process webhook callback when received
```  

## 代码示例  

请参阅 [assets/examples/](assets/examples/)，了解可用的实现示例：  
- `python_client.py`：完整的Python客户端示例  
- `nodejs_client.js`：Node.js客户端实现  
- `curl_examples.sh`：cURL命令示例  
- `webhook_handler.py`：Flask框架下的Webhook服务器示例  

## 示例脚本  

| 脚本 | 用途 |  
|--------|-------|  
| `scripts/test_connection.py` | 验证API密钥 |  
| `scripts/create_video.py` | 从文本文件创建视频 |  
| `scripts/poll_status.py` | 监控视频生成进度 |  
| `scripts/list_resources.py` | 获取可用的语音/音乐资源 |  

**运行方式：**  
`python scripts/<脚本>.py --api-key YOUR_KEY`  

## 常见问题：  

- **“API响应无效”**：确保JSON结构与文档完全匹配。  
- **视频生成失败**：检查 `step` 字段的值——某些步骤（如 `user_action`）需要通过Fliz控制台进行手动处理。  
- **无法提取视频内容**：API要求直接提供文本内容，请在集成过程中自行实现内容提取功能。  

## 参考资料：  
- [API参考文档](references/api-reference.md)：完整接口说明  
- [枚举值](references/enums-values.md)：所有有效的参数值  
- [集成示例](assets/examples/)：可直接使用的代码示例