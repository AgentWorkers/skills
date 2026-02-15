---
name: lowkey-viral
description: >
  Create short-form social media videos and photo carousel slideshows using the
  lowkey viral API. Generate AI-powered TikTok videos, Instagram Reels, and
  carousel posts programmatically. Supports 2x2 grid videos (1080x1920, 5s,
  30fps) with background music and photo slideshows with text overlays. Use when
  the user wants to create social media content, short videos, viral clips,
  reels, TikToks, carousels, slideshows, or any vertical video for social
  platforms. Requires a lowkey viral API key (PRO or ULTIMATE plan) from
  https://lowkeyviral.com/dashboard/api-keys.
metadata:
  clawdbot:
    requires:
      env:
        - LOWKEY_VIRAL_API_KEY
      bins:
        - curl
    primaryEnv: LOWKEY_VIRAL_API_KEY
    homepage: https://github.com/tiotdev/lowkey-viral
    emoji: "🎬"
---

# lowkey viral — 人工智能驱动的社交媒体视频与幻灯片制作工具

使用 lowkey viral 的 REST API，您可以轻松为 TikTok、Instagram Reels 等平台创建短视频和图片轮播幻灯片。

## 先决条件

**使用此功能需要一个 lowkey viral 的 API 密钥。**

1. 访问 https://lowkeyviral.com 并订阅 PRO 或 ULTIMATE 计划。
2. 从控制面板中生成 API 密钥：https://lowkeyviral.com/dashboard/api-keys
3. 将密钥设置为环境变量：
   ```bash
   export LOWKEY_VIRAL_API_KEY="lkv_sk_your_key_here"
   ```

API 密钥的前缀为 `lkv_sk_`，仅在创建时显示一次。

## 可制作的内容

### 短视频（2x2 网格布局）
- 1080x1920 像素的竖版 MP4 视频，时长 5 秒，帧率 30fps
- 4 张图片以 2x2 网格布局排列，并可添加文字说明
- 可选背景音乐（来自 20 首 CC0 许可的歌曲）
- 3 种布局样式：`default`、`withCaptions`、`noSpaces`

### 图片幻灯片（轮播）
- 2-10 张竖版图片（1080x1920 像素），可添加文字说明
- 3 种文字样式：`classic_bold`、`background_bar`、`neon_glow`
- 适用于 Instagram 轮播或 TikTok 的图片模式

## 认证

所有 API 请求均发送到 `https://lowkeyviral.com/api/v1/`，并需要使用 API 密钥作为 Bearer Token 进行身份验证：
```
Authorization: Bearer $LOWKEY_VIRAL_API_KEY
```

## 请求限制

- PRO 计划：每分钟 10 次请求
- ULTIMATE 计划：每分钟 30 次请求
- 进度查询：每分钟 60 次请求（所有计划均适用）
- 429 状态码响应会包含 `Retry-After` 头部信息

## 工作流程：创建短视频

### 第 1 步 — 生成 AI 设计方案（2 个信用点）

```bash
curl -s -X POST https://lowkeyviral.com/api/v1/briefs \
  -H "Authorization: Bearer $LOWKEY_VIRAL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "A travel app for Gen-Z backpackers"}'
```

返回 5 个设计方案，选择最佳方案并记下其 `id`。

### 第 2 步 — 生成图片（4-8 个信用点）

```bash
curl -s -X POST https://lowkeyviral.com/api/v1/briefs/BRIEF_ID/generate \
  -H "Authorization: Bearer $LOWKEY_VIRAL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"image_model": "z_image_turbo"}'
```

图片模型及价格：
- `z_image_turbo` — 每张图片 1 个信用点（最快生成）
- `p_image` — 每张图片 2 个信用点（高质量）
- `flux_2_dev` — 每张图片 2 个信用点（高细节）

每个设计方案默认包含 4 张图片。

### 第 3 步 — 渲染视频（1 个信用点）

```bash
curl -s -X POST https://lowkeyviral.com/api/v1/briefs/BRIEF_ID/render \
  -H "Authorization: Bearer $LOWKEY_VIRAL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"design": "default", "soundtrack": "City Sunshine"}'
```

返回 `{"render_id": "..."}`。

### 第 4 步 — 等待视频生成完成（0 个信用点）

```bash
curl -s https://lowkeyviral.com/api/v1/briefs/BRIEF_ID/render/RENDER_ID/progress \
  -H "Authorization: Bearer $LOWKEY_VIRAL_API_KEY"
```

每 2-3 秒查询一次进度：
- 进度中：`{"type": "progress", "progress": 0.45, "stalled": false, ...}`
- 完成：`{"type": "done", "url": "https://...out.mp4", "size": 1234567}``
- 错误：`{"type": "error", "message": "..."}`

### 快捷方式 — 一次性生成短视频

通过设置 `render: true` 选项，可以一次性完成所有步骤：
```bash
curl -s -X POST https://lowkeyviral.com/api/v1/briefs/manual \
  -H "Authorization: Bearer $LOWKEY_VIRAL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "hook": "these coffee shops are insane",
    "title": "Best Coffee Shops",
    "render": true,
    "design": "default",
    "soundtrack": "City Sunshine",
    "images": [
      {"title": "Cafe A", "description": "A cozy minimalist cafe with latte art"},
      {"title": "Cafe B", "description": "Industrial style coffee shop with exposed brick"},
      {"title": "Cafe C", "description": "Hidden garden cafe with hanging plants"},
      {"title": "Cafe D", "description": "Rooftop cafe with city skyline view"}
    ],
    "image_model": "z_image_turbo"
  }'
```

带有描述但无链接的图片由 AI 生成。响应中会包含用于查询的 `render_id`。

## 工作流程：创建图片幻灯片

### 第 1 步 — 生成 AI 设计方案（2 个信用点）

```bash
curl -s -X POST https://lowkeyviral.com/api/v1/briefs \
  -H "Authorization: Bearer $LOWKEY_VIRAL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "A skincare brand for 20-somethings", "type": "slideshow", "slide_count": 6}'
```

参数：
- `type` 必须设置为 `"slideshow"`
- `slide_count`：4-10 张（默认 6 张）

### 第 2 步 — 生成图片（每张图片 1-2 个信用点）

```bash
curl -s -X POST https://lowkeyviral.com/api/v1/briefs/BRIEF_ID/generate \
  -H "Authorization: Bearer $LOWKEY_VIRAL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"image_model": "z_image_turbo"}'
```

图片会自动生成为 9:16 的竖版格式。

### 第 3 步 — 渲染幻灯片（1 个信用点）

```bash
curl -s -X POST https://lowkeyviral.com/api/v1/briefs/BRIEF_ID/render \
  -H "Authorization: Bearer $LOWKEY_VIRAL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"caption_style": "classic_bold"}'
```

立即返回渲染完成的幻灯片（无需等待查询）：
```json
{
  "slides": [
    {"index": 0, "url": "https://...slide-0.jpg"},
    {"index": 1, "url": "https://...slide-1.jpg"}
  ]
}
```

### 快捷方式 — 一次性生成幻灯片

```bash
curl -s -X POST https://lowkeyviral.com/api/v1/briefs/manual \
  -H "Authorization: Bearer $LOWKEY_VIRAL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "slideshow",
    "caption_style": "classic_bold",
    "render": true,
    "images": [
      {"title": "Step 1", "description": "Woman applying cleanser, soft morning light"},
      {"title": "Step 2", "description": "Serum dropper on clear skin, close-up"},
      {"title": "Step 3", "description": "Moisturizer application, dewy skin glow"}
    ],
    "image_model": "z_image_turbo"
  }'
```

响应中会立即包含所有幻灯片的数组。

## 上传自定义图片

如果您有自己的图片，请先上传它们：
```bash
# 1. Get presigned upload URL
curl -s -X POST https://lowkeyviral.com/api/v1/uploads \
  -H "Authorization: Bearer $LOWKEY_VIRAL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"content_type": "image/jpeg"}'

# Response: {"upload_url": "https://...", "file_url": "https://...", ...}

# 2. Upload the file (max 10 MB)
curl -X PUT "UPLOAD_URL" \
  -H "Content-Type: image/jpeg" \
  --data-binary @photo.jpg

# 3. Use file_url in your brief
```

支持的图片格式：`image/jpeg`、`image/png`、`image/webp`。

## 检查账户余额与信用点

```bash
curl -s https://lowkeyviral.com/api/v1/account \
  -H "Authorization: Bearer $LOWKEY_VIRAL_API_KEY"
```

返回信息：`{"credits": 42, "plan_type": "PRO", "next_reset_date": "..."}`

## 列出与管理设计方案

```bash
# List all briefs (paginated)
curl -s "https://lowkeyviral.com/api/v1/briefs?limit=20" \
  -H "Authorization: Bearer $LOWKEY_VIRAL_API_KEY"

# Filter by type
curl -s "https://lowkeyviral.com/api/v1/briefs?type=slideshow" \
  -H "Authorization: Bearer $LOWKEY_VIRAL_API_KEY"

# Get single brief
curl -s https://lowkeyviral.com/api/v1/briefs/BRIEF_ID \
  -H "Authorization: Bearer $LOWKEY_VIRAL_API_KEY"

# Delete a brief
curl -s -X DELETE https://lowkeyviral.com/api/v1/briefs/BRIEF_ID \
  -H "Authorization: Bearer $LOWKEY_VIRAL_API_KEY"
```

## 信用点费用总结

| 操作        | 短视频    | 幻灯片     |
|------------|---------|-----------|
| AI 设计方案（5 个） | 2        | 2          |
| 手动设计     | 0         | 0           |
| 图片（z_image_turbo） | 4        | 1/张图片     |
| 图片（p_image）   | 8        | 2/张图片     |
| 图片（flux_2_dev） | 8        | 2/张图片     |
| 渲染        | 1        | 1           |

**完整短视频（包含 AI 设计）：** 7-11 个信用点。
**完整幻灯片（6 张）：** 9-15 个信用点。
**使用自定义图片：** 需额外支付 1 个信用点。

## 可用选项

### 网格布局样式
- `default` — 标准的 2x2 布局
- `withCaptions` — 为每张图片添加文字说明
- `noSpaces` — 紧凑的边缘对齐布局

### 幻灯片文字样式
- `classic_bold` — 白色文字，黑色边框
- `background_bar` — 白色文字，显示在半透明背景上
- `neon_glow` — 绿色文字（#00ff88），带有发光效果

### 音乐（仅适用于短视频）
Advertime, And Just Like That, Blippy Trance, Brewing Potions, City Sunshine, Funshine, Happy Whistling Ukulele, I Guess What I'm Trying to Say, La Citadelle, Lukewarm Banjo, Magical Transition, Martini Sunset, Meditating Beat, Night in Venice, River Meditation, Soundtrack From the Starcourt Mall, Strength of the Titans, Study and Relax, Sun Up Gunned Down, The Celebrated Minuet

### 图片模型
- `z_image_turbo` — 最快生成，每张图片 1 个信用点
- `p_image` — 高质量图片，每张图片 2 个信用点
- `flux_2_dev` — 高细节图片，每张图片 2 个信用点

## 错误处理

所有错误都会返回以下信息：
```json
{"error": {"code": "error_code", "message": "Human-readable description"}}
```

| 状态码 | 错误代码 | 错误原因       |
|--------|---------|--------------|
| 401    | unauthorized | API 密钥无效或缺失     |
| 403    | forbidden | 需要 PRO 或 ULTIMATE 计划   |
| 402    | insufficient_credits | 信用点不足       |
| 402    | validation_error | 参数错误       |
| 404    | not_found | 资源未找到       |
| 429    | rate_limited | 请求次数过多（请查看 `Retry-After` 头部信息） |
| 500    | internal_error | 服务器内部错误     |

## 数据安全与隐私

- 所有请求仅发送到 `https://lowkeyviral.com/api/v1/`。
- API 密钥以 Bearer Token 的形式包含在 Authorization 头部中。
- 上传的图片存储在 AWS S3（us-east-1）上。
- 生成的视频和幻灯片通过 CloudFront 服务托管在 S3 上。
- 数据不会被发送到 lowkeyviral.com 之外的任何第三方服务。