---
name: emoji-sticker-generation
description: 使用 each::sense AI 生成自定义的表情符号和贴纸包。您可以从照片中创建个性化的表情符号，还可以制作表情符号包、动画贴纸，以及适用于 Slack、Discord、WhatsApp 等平台的专用表情符号集。
metadata:
  author: eachlabs
  version: "1.0"
---
# 表情符号与贴纸生成

使用 `each-sense` 功能生成自定义的表情符号和贴纸包。该功能能够根据用户提供的照片、表情或设计要求，创建个性化的表情符号，以及适用于各种消息应用和团队协作工具的贴纸。

## 主要功能

- **照片转表情符号**：将照片转换为卡通风格的表情符号。
- **表情包**：根据单一参考图像生成一系列表情符号。
- **动态贴纸**：创建可移动的 GIF 动画贴纸。
- **平台适配**：生成适合 Slack、Discord、WhatsApp 和 Telegram 等平台的贴纸。
- **品牌吉祥物**：设计统一的品牌吉祥物表情符号。
- **宠物表情符号**：将宠物照片转换成可爱的贴纸。
- **Bitmoji 风格**：基于用户头像的表情符号。
- **反应表情符号**：提供具有自定义风格的常用反应表情符号。

## 快速入门

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a cute cartoon emoji from this photo, suitable for Slack",
    "mode": "max",
    "image_urls": ["https://example.com/my-photo.jpg"]
  }'
```

## 平台尺寸与格式

| 平台 | 尺寸 | 格式 | 备注 |
|--------|------|--------|---------|
| Slack   | 128x128 | PNG, GIF | 正方形，透明背景 |
| Discord | 128x128 | PNG, GIF | 动画贴纸最大 256KB |
| WhatsApp | 512x512 | WebP | 支持透明背景的贴纸包 |
| Telegram | 512x512 | WebP, TGS | 静态或动态贴纸 |
| iMessage | 300x300 | PNG, GIF | 支持多种尺寸 |
| Teams   | 128x128 | PNG | 正方形格式 |

## 使用场景示例

### 1. 从照片创建自定义表情符号

根据一张肖像照片生成一个个性化的表情符号。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Transform this photo into a cute cartoon emoji. Make it expressive with big eyes and a friendly smile. Style should be like modern emoji with clean lines and vibrant colors. Output at 512x512 with transparent background.",
    "mode": "max",
    "image_urls": ["https://example.com/portrait.jpg"]
  }'
```

### 2. 表情符号表情包

根据一个参考图像生成一套完整的表情符号。

```bash
# Initial emoji creation
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a cartoon character emoji from this photo. I want to use this as a base for an expression pack.",
    "mode": "max",
    "session_id": "emoji-pack-001",
    "image_urls": ["https://example.com/face.jpg"]
  }'

# Generate expression variations
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now create 6 expression variations of this character: happy, sad, laughing, surprised, angry, and thinking. Keep the same style and character design consistent across all expressions.",
    "mode": "max",
    "session_id": "emoji-pack-001"
  }'
```

### 3. 动态表情符号/贴纸

创建带有简单动画的动态贴纸。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an animated emoji sticker of a cute waving hand. Make it loop smoothly with a friendly wave motion. Cartoon style with bold outlines, bright skin tone. Output as a short looping animation suitable for messaging apps.",
    "mode": "max"
  }'
```

### 4. Slack/Discord 表情符号包

为团队工作空间生成一套自定义的表情符号。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a set of 5 custom Slack emoji for a tech startup: 1) Ship it rocket, 2) LGTM thumbs up, 3) Coffee break mug, 4) Bug squash, 5) Celebration party. Modern flat design style with bold colors. 128x128 pixels each with transparent backgrounds.",
    "mode": "max",
    "session_id": "slack-emoji-set"
  }'

# Add more to the set
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Add 3 more emoji to the set in the same style: 1) Thinking face with code brackets, 2) PR approved checkmark, 3) Deploy success. Keep the same flat design aesthetic.",
    "mode": "max",
    "session_id": "slack-emoji-set"
  }'
```

### 5. WhatsApp 贴纸包

为 WhatsApp 生成一套优化的贴纸包。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a WhatsApp sticker pack with a cute cat character. Generate 8 stickers showing: greeting, thank you, love, laughing, sleeping, eating, confused, and celebrating. Kawaii anime style with pastel colors. 512x512 pixels with transparent background for each sticker.",
    "mode": "max"
  }'
```

### 6. Bitmoji 风格头像表情符号

创建一套基于用户头像的 Bitmoji 风格表情符号。

```bash
# Create avatar base
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a Bitmoji-style avatar from this photo. Cartoon character with recognizable features but stylized. Clean vector-like art style similar to Bitmoji/Snapchat avatars.",
    "mode": "max",
    "session_id": "my-avatar-emoji",
    "image_urls": ["https://example.com/my-selfie.jpg"]
  }'

# Generate situational stickers
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create 5 stickers of my avatar in different situations: 1) Working on laptop, 2) Drinking coffee, 3) High-fiving, 4) Mind blown gesture, 5) Dancing celebration. Same Bitmoji art style, keep my avatar consistent.",
    "mode": "max",
    "session_id": "my-avatar-emoji"
  }'
```

### 7. 品牌吉祥物表情符号包

为品牌沟通生成一套统一风格的吉祥物表情符号。

```bash
# Define mascot
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a brand mascot emoji: a friendly robot character with rounded features, blue and white color scheme, expressive LED eyes. This will be used for our tech company Slack and social media. Start with a neutral happy expression.",
    "mode": "max",
    "session_id": "brand-mascot-emoji"
  }'

# Generate mascot pack
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a complete emoji pack with this robot mascot showing: thumbs up, thinking, celebrating, waving hello, error/oops face, loading/processing, success checkmark pose, and question mark confused. Maintain exact same character design and brand colors.",
    "mode": "max",
    "session_id": "brand-mascot-emoji"
  }'
```

### 8. 反应表情符号包

为团队或社区创建自定义的反应表情符号。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a set of 10 reaction emoji in a consistent playful illustrated style: 1) Fire/lit, 2) 100 percent, 3) Eyes looking, 4) Chef kiss, 5) Mind blown explosion, 6) Facepalm, 7) Clapping hands, 8) Raising hands celebration, 9) Laughing crying, 10) Heart eyes. Bold colors, clean outlines, 128x128 transparent PNG style.",
    "mode": "max"
  }'
```

### 9. 从照片创建宠物表情符号

将宠物照片转换成可爱的贴纸。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Turn this photo of my dog into a cute cartoon emoji sticker. Capture the personality and distinctive features. Kawaii style with big sparkly eyes and adorable expression. Create it as a 512x512 sticker with transparent background.",
    "mode": "max",
    "image_urls": ["https://example.com/my-dog.jpg"]
  }'

# Create pet expression pack
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create 6 emoji variations of this dog: happy with tongue out, sleepy, begging for treats, playful with ball, confused head tilt, and excited jumping. Keep the same cartoon style consistent.",
    "mode": "max",
    "session_id": "pet-emoji-pack",
    "image_urls": ["https://example.com/my-dog.jpg"]
  }'
```

### 10. 基于文本的表情符号设计

创建基于文本和字体的表情符号。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create custom text emoji stickers for common team reactions: 1) NICE in rainbow gradient bubble letters, 2) SHIP IT with rocket trail effect, 3) WFH in cozy style with house icon, 4) BRB with clock elements, 5) TY in heart shape, 6) GG in gaming style. Each should be readable at 128x128 with transparent background, bold fun typography.",
    "mode": "max"
  }'
```

## 最佳实践

### 表情符号设计
- **简洁性**：设计要简洁，便于在小尺寸下阅读。
- **粗略的轮廓**：使用粗轮廓以增强视觉效果。
- **颜色限制**：每个表情符号使用 3-5 种颜色。
- **表情夸张**：通过夸张的表情来增强视觉冲击力。
- **一致性**：在整个表情包中保持设计风格的一致性。

### 平台适配
- **透明背景**：为了最佳兼容性，请始终使用透明背景。
- **正方形格式**：大多数平台要求 1:1 的宽高比。
- **文件大小**：动画贴纸的大小应控制在 256KB 以内。
- **小尺寸预览**：在 32x32 的尺寸下预览以确保可读性。

### 动画制作技巧
- **无缝循环**：确保动画能够平滑循环。
- **时长控制**：1-3 秒的动画效果最佳。
- **简单动作**：简单的动作更易于理解。
- **帧率**：10-15 FPS 的帧率适合表情符号。

## 表情符号制作提示

在创建表情符号时，请提供以下信息：
- **风格**：卡通、可爱、扁平设计、3D 等。
- **表情/情感**：希望表达什么情感？
- **尺寸**：指定输出的尺寸。
- **背景**：请求使用透明背景。
- **平台**：指定目标平台以进行优化。
- **一致性**：参考之前的表情符号设计风格。

### 示例提示结构

```
"Create a [style] emoji of [subject/expression].
[Visual details and characteristics].
Output at [size] with transparent background.
Target platform: [Slack/Discord/WhatsApp/etc.]"
```

## 模式选择

在生成表情符号之前，询问用户：
**“您需要快速且低成本的结果，还是高质量的结果？”**

| 模式 | 适用场景 | 速度 | 质量 |
|------|---------|------|---------|
| `max` | 最终的贴纸包、品牌表情符号 | 较慢 | 最高质量 |
| `eco` | 快速概念、测试想法、草图 | 较快 | 适合初步设计 |

## 多轮生成表情符号包

使用 `session_id` 来构建连贯的表情符号包：

```bash
# Start with character design
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design a cute mascot character for my emoji pack - a happy cloud with a face",
    "session_id": "cloud-emoji-project"
  }'

# Add expressions
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create this cloud with a rainy sad expression",
    "session_id": "cloud-emoji-project"
  }'

# Continue building the pack
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now make a sunny happy version with rainbow",
    "session_id": "cloud-emoji-project"
  }'
```

## 批量生成表情符号包

高效地生成完整的表情符号包：

```bash
# Generate full expression set in one request
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a complete emoji pack of 8 food emoji: pizza slice, hamburger, sushi, taco, ice cream cone, donut, coffee cup, and avocado. All in the same cute kawaii style with happy faces, consistent line weight and color palette. 128x128 each with transparent backgrounds.",
    "mode": "eco"
  }'
```

## 错误处理

| 错误类型 | 原因 | 解决方案 |
|--------|--------|---------|
| `Failed to create prediction: HTTP 422` | 资源不足 | 请在 eachlabs.ai 上补充资源。 |
| 内容违规 | 内容不符合规定 | 调整提示以符合使用规范。 |
| 超时 | 生成过程复杂 | 将客户端超时时间设置为至少 10 分钟。 |
| 风格不一致 | 会话不一致 | 使用相同的 `session_id` 以确保风格一致性。 |

## 相关技能

- `each-sense`：核心 API 文档
- `product-photo-generation`：产品图片生成
- `meta-ad-creative-generation`：社交媒体创意内容生成