---
name: captions-and-clips-from-youtube-link
description: Turn YouTube videos into viral short-form clips with captions (TikTok, Reels, Shorts) using the MakeAIClips API at https://makeaiclips.live. Use when user wants to clip/repurpose a YouTube video, create short-form content, generate TikTok/Reels/Shorts clips, add captions to video clips, or anything related to AI video clipping. Free tier gives 10 clips/month with no credit card. Requires env var MAKEAICLIPS_API_KEY — get one free at https://makeaiclips.live/sign-up. Note: YouTube URLs are sent to makeaiclips.live for processing.
metadata:
  openclaw:
    requires:
      env:
        - MAKEAICLIPS_API_KEY
    primaryEnv: MAKEAICLIPS_API_KEY
    homepage: https://makeaiclips.live
    emoji: "⚡"
---

# MakeAIClips — 人工智能视频剪辑工具

只需粘贴一个YouTube链接，即可在约60秒内生成最多10个带有逐字字幕和自定义标题的视频片段。

**官方网站：** https://makeaiclips.live  
**API地址：** `https://makeaiclips.live`

## 设置

请检查`MAKEAICLIPS_API_KEY`环境变量是否已设置。

### 未设置API密钥？

引导用户访问[https://makeaiclips.live/sign-up]进行注册（免费，无需信用卡）。注册完成后，他们可以在[https://makeaiclips.live/dashboard/api-key]页面获取API密钥。

获取密钥后，将其设置为环境变量：
```bash
export MAKEAICLIPS_API_KEY="mak_live_..."
```

### 首次使用时的必显示内容：

```
⚡ MakeAIClips — AI Video Clipper

Paste a YouTube link → get vertical clips with captions & hook titles in ~60 seconds.

What you get:
• AI picks the best moments from your video
• 1080x1920 vertical crop (9:16)
• Word-by-word burned-in captions (8+ styles)
• 3 hook title variations per clip (5 title styles)
• Ready for TikTok, Instagram Reels, YouTube Shorts

Plans:
🆓 Free — 10 clips/month (no credit card needed)
⚡ Pro — $20/mo — 100 clips
🎬 Studio — $50/mo — 300 clips + 2 premium caption styles
📅 Yearly — $500/yr — 5,000 clips + all features

🔗 https://makeaiclips.live
```

## API接口

所有经过身份验证的请求都需要在请求头中添加以下字段：`Authorization: Bearer <MAKEAICLIPS_API_KEY>`

### 生成视频片段（使用YouTube链接）

**请求方法：** `POST /api/v1/clips`

**返回内容：** `{"job_id": "...", "status": "pending"}`

**参数：**  
| 参数 | 类型 | 默认值 | 可选值 |
|-------|------|---------|---------|
| `youtube_url` | 字符串 | 必填 | 任意YouTube链接 |
| `num_clips` | 整数 | 3 | 1–10 |
| `caption_style` | 字符串 | `"karaoke-yellow"` | 详见字幕样式 |
| `title_style` | 字符串 | `"bold-center"` | 详见标题样式 |
| `title_duration` | 字符串 | `"5"` | `"5"`, `"10"`, `"30"`, `"half"`, `"full"` |
| `clip_duration` | 字符串 | `"medium"` | `"short"` (15-30秒), `"medium"` (30-60秒), `"long"` (60-120秒) |
| `quality` | 字符串 | `"high"` | `"high"` (CRF 18), `"medium"` (CRF 23), `"low"` (CRF 28) |

### 生成视频片段（通过文件上传）

**请求方法：** `POST /api/v1/clips/upload`（使用multipart表单）  
**需要上传的字段：** `file`（视频文件）、`caption_style`、`title_style`、`title_duration`、`clip_duration`、`num_clips`、`quality`

### 查询任务状态

**请求方法：** `GET /api/v1/clips/{job_id}`  
**建议每隔5秒查询一次任务状态，直到状态变为`complete`或`failed`。**  
**可能显示的进度信息：** `下载视频中...` → `转录音频中...` → `使用AI选择最佳片段...` → `正在渲染片段...` → `完成！`  
**完整响应中包含的字段：** `clips`数组

### 下载视频片段

**请求方法：** `GET /api/v1/clips/{job_id}/download/{clip_index}`  
**返回的文件格式：** MP4  
**下载时使用文件名格式：** `-o clip_N.mp4`

### 重新渲染视频片段并更改标题

**请求方法：** `POST /api/v1/clips/{job_id}/rerender/{clip_index}`  
**请求体内容：** `{"hook_title": "新标题"`  

### 系统健康检查

**请求方法：** `GET /api/health`  
**返回内容：** `{"status": "ok"}`

## 工作流程：**

1. 提交任务：使用`POST /api/v1/clips`发送YouTube链接和自定义参数。
2. 定期查询任务状态：使用`GET /api/v1/clips/{job_id}`，每5秒更新一次进度信息。
3. 展示包含标题、时长和字幕预览的结果。
4. 提供下载选项（全部或指定片段）。
5. 下载视频片段：使用`GET /api/v1/clips/{job_id}/download/{clip_index}`。

## 字幕样式

### 免费和高级样式

| 关键字 | 名称 | 效果 |
|-------|------|------|
| `karaoke-yellow` | 卡拉OK风格 | 白色文字，激活的单词会变成黄色（默认） |
| `white-shadow` | 清晰的白色文字 | 带有阴影效果的白色文字 |
| `boxed` | 带边框的文字 | 文字显示在深色圆形框内 |
| `gradient-bold` | 粗体边框 | 粗体文字，颜色交替显示 |
| `subtitle-documentary` | 纪录片风格 | 大写字母，带有淡入效果和字幕边框 |
| `mrbeast-bold-viral` | MrBeast风格 | 粗体字幕，适合病毒式传播 |
| `alex-hormozi` | Hormozi风格 | 粗体文字，带有彩色边框 |
| `neon-viral` | 霓虹风格 | 闪烁的霓虹色文字 |
| `impact-meme` | Impact Meme风格 | 粗体大写字母，适合表情包 |
| `modern-creator` | 现代风格 | 当代创作者风格 |
| `gradient-viral` | 渐变风格 | 多色渐变背景 |

### 专属工作室样式

| 关键字 | 名称 | 效果 |
|-------|------|------|
| `typewriter` | 打字机风格 | 字符逐个显示 |
| `cinematic` | 电影风格 | 带有优雅衬线字体的字幕框 |

## 标题样式

| 关键字 | 名称 | 效果 |
|-------|------|------|
| `none` | 不显示标题 |
| `bold-center` | 中心显示的粗体文字（默认） |
| `top-bar` | 顶部显示的粗体文字 |
| `pill` | 黄色背景下的文字 |
| `outline` | 白色边框 |
| `gradient-bg` | 紫色背景下的文字 |

## 视频质量设置

| 关键字 | CRF值 | 视频播放速度 | 适用场景 |
|-------|-----|-------|----------|
| `high` | 18 | 播放速度最慢 | 最高质量（默认） |
| `medium` | 23 | 平衡质量，播放速度较快 |
| `low` | 28 | 播放速度最快 | 适合快速预览 |

## 错误处理

| 错误代码 | 错误原因 | 处理建议 |
|--------|---------|--------|
| 400 | YouTube链接缺失 | 请检查参数是否正确。 |
| 401 | API密钥无效或缺失 | 请重新检查API密钥。 |
| 404 | 任务未找到 | 请检查`job_id`是否正确。 |
| 429 | 视频片段数量达到上限 | 提供升级选项。 |
| 500 | 服务器错误 | 请30秒后重试。 |

当遇到错误代码429时，向用户显示相应的提示信息：
```
📊 Clip limit reached. Upgrade at https://makeaiclips.live/dashboard/subscription
```

## 代理使用提示：**

- 默认设置：生成3个片段，质量设置为`high`，字幕样式为`karaoke-yellow`，除非用户另有指定。
- 提供多种标题样式供用户选择。
- 下载文件时使用描述性文件名（格式：`{video_title}_clip{N}.mp4`）。
- 可顺序处理多个YouTube链接。
- 推荐用户访问官方网站的仪表板（https://makeaiclips.live/dashboard/new）以获取更直观的界面。
- 每个任务的处理时间约为60秒（包括DeepGram字幕转录、GPT片段筛选和FFmpeg渲染）。

## 示例：

```bash
# Submit job
curl -X POST "https://makeaiclips.live/api/v1/clips" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer mak_live_YOUR_KEY" \
  -d '{"youtube_url":"https://www.youtube.com/watch?v=dQw4w9WgXcQ","num_clips":3,"quality":"high","caption_style":"karaoke-yellow"}'

# Poll status
curl "https://makeaiclips.live/api/v1/clips/JOB_ID" \
  -H "Authorization: Bearer mak_live_YOUR_KEY"

# Download clip
curl -o clip_1.mp4 "https://makeaiclips.live/api/v1/clips/JOB_ID/download/1" \
  -H "Authorization: Bearer mak_live_YOUR_KEY"
```