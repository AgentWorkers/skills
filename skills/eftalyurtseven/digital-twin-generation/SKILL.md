---
name: digital-twin-generation
description: 使用 each::sense AI 生成逼真的数字孪生体及头像克隆。为视频通话、企业沟通、客户服务以及多语言内容创建由 AI 驱动的数字形象。
metadata:
  author: eachlabs
  version: "1.0"
---
# 数字孪生生成

使用 `each-sense` 功能生成逼真的数字孪生和虚拟形象克隆。该技能能够为视频通话、企业沟通、客户服务以及多语言内容传递创建由人工智能驱动的真实人物数字表示。

## 主要功能

- **基于照片的数字孪生**：根据参考照片创建数字克隆
- **逼真虚拟形象**：生成具有真实感的虚拟形象
- **适用于视频通话的数字孪生**：专为虚拟会议优化的数字孪生
- **企业代言人**：用于品牌沟通的专业数字代表
- **客户服务虚拟形象**：用于支持交互的一致性 AI 代表
- **多语言数字孪生**：能够使用多种语言的数字孪生
- **具有表情的数字孪生**：具有自然面部表情和情绪的虚拟形象
- **全身数字孪生**：包括身体和手势的完整数字表示
- **动画视频**：通过视频生成让数字孪生动起来
- **跨平台一致性**：在所有平台上保持外观一致

## 快速入门

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a photorealistic digital twin from these reference photos. Generate a professional headshot suitable for corporate use.",
    "image_urls": ["https://example.com/person-photo1.jpg", "https://example.com/person-photo2.jpg"],
    "mode": "max"
  }'
```

## 数字孪生的使用场景

| 使用场景 | 描述 | 推荐照片 |
|----------|-------------|-------------------|
| 视频通话 | 虚拟会议中的形象展示 | 3-5 张正面照片 |
| 企业代言人 | 品牌沟通 | 5-10 张专业照片 |
| 客户服务 | 客户服务虚拟形象 | 3-5 张中性表情的照片 |
| 多语言内容 | 多语言视频内容 | 5 张以上不同角度的照片 |
| 社交媒体 | 一致的在线形象 | 5-10 张多样化的照片 |
| 培训视频 | 教育内容传递 | 5 张以上带有表情的照片 |

## 使用场景示例

### 1. 根据照片创建数字孪生

根据参考照片生成数字孪生，以实现一致的身份展示。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a digital twin from these reference photos. The twin should capture the exact likeness, skin tone, and facial features. Generate a high-quality portrait with professional studio lighting on a neutral gray background.",
    "image_urls": [
      "https://example.com/reference-front.jpg",
      "https://example.com/reference-angle.jpg",
      "https://example.com/reference-side.jpg"
    ],
    "mode": "max"
  }'
```

### 2. 逼真虚拟形象克隆

创建高度详细的逼真虚拟形象，用于跨平台的数字展示。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a photorealistic avatar clone from these photos. The avatar should be indistinguishable from a real photograph. Include fine details like skin texture, hair strands, and eye reflections. Output as a 1:1 square format suitable for profile pictures.",
    "image_urls": [
      "https://example.com/subject-photo1.jpg",
      "https://example.com/subject-photo2.jpg"
    ],
    "mode": "max"
  }'
```

### 3. 适用于视频通话的数字孪生

为虚拟会议环境创建优化的数字孪生。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a digital twin optimized for video calls. The twin should look natural in a home office setting with soft natural lighting. Include a subtle depth-of-field blur on the background. The person should have a friendly, approachable expression suitable for professional meetings.",
    "image_urls": [
      "https://example.com/ceo-headshot.jpg",
      "https://example.com/ceo-casual.jpg"
    ],
    "mode": "max",
    "session_id": "videocall-twin-001"
  }'
```

### 4. 企业代言人数字孪生

生成用于品牌沟通的专业数字代言人。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a corporate spokesperson digital twin from these executive photos. The twin should appear authoritative yet approachable. Professional business attire, confident posture, clean corporate background with subtle brand colors (navy blue). Suitable for investor presentations and company announcements.",
    "image_urls": [
      "https://example.com/exec-professional.jpg",
      "https://example.com/exec-speaking.jpg",
      "https://example.com/exec-portrait.jpg"
    ],
    "mode": "max"
  }'
```

### 5. 客户服务虚拟形象

创建用于客户支持交互的一致性虚拟形象。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a customer service avatar digital twin. The avatar should have a warm, helpful expression with a genuine smile. Professional but approachable appearance. Clean, minimal background. The twin will be used for chat support and help desk interfaces, so it should feel trustworthy and friendly.",
    "image_urls": [
      "https://example.com/support-rep-photo.jpg"
    ],
    "mode": "max"
  }'
```

### 6. 多语言数字孪生

创建用于多语言内容传递的数字孪生。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a digital twin for multilingual video content. Generate the twin with a neutral mouth position that works well for lip-sync dubbing. Include multiple angles: front-facing, slight left turn, and slight right turn. The lighting should be even and consistent to ensure seamless video dubbing across different languages.",
    "image_urls": [
      "https://example.com/presenter-front.jpg",
      "https://example.com/presenter-left.jpg",
      "https://example.com/presenter-right.jpg"
    ],
    "mode": "max",
    "session_id": "multilingual-twin-project"
  }'
```

### 7. 具有表情的数字孪生

生成具有多种面部表情的数字孪生，以适应动态内容。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a digital twin with multiple expressions from these reference photos. Generate 4 variations: 1) Neutral professional expression, 2) Warm genuine smile, 3) Thoughtful/listening expression, 4) Enthusiastic/excited expression. All variations should maintain perfect identity consistency.",
    "image_urls": [
      "https://example.com/person-neutral.jpg",
      "https://example.com/person-smiling.jpg",
      "https://example.com/person-serious.jpg"
    ],
    "mode": "max",
    "session_id": "expressive-twin-set"
  }'
```

### 8. 全身数字孪生

创建包括姿势和手势的完整全身数字表示。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a full-body digital twin from these reference photos. Include accurate body proportions, clothing style, and natural standing posture. The twin should be shown in a professional presentation pose with hands visible. Full-length view suitable for virtual events and digital stage presentations.",
    "image_urls": [
      "https://example.com/fullbody-front.jpg",
      "https://example.com/fullbody-side.jpg",
      "https://example.com/headshot-detail.jpg"
    ],
    "mode": "max"
  }'
```

### 9. 动画数字孪生视频

生成包含数字孪生讲话或演示的动画视频。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 10-second animated video of my digital twin. The twin should appear to be speaking naturally with subtle head movements and natural blinking. Professional office background with soft lighting. The animation should loop seamlessly for use as a video call placeholder.",
    "image_urls": [
      "https://example.com/my-photo-front.jpg",
      "https://example.com/my-photo-speaking.jpg"
    ],
    "mode": "max"
  }'
```

### 10. 跨平台一致的数字孪生

为跨平台一致性创建多种格式的数字孪生版本。

```bash
# Initial twin creation
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a digital twin master image from these photos. This will be the base for generating consistent avatars across multiple platforms. High resolution, neutral background, perfect lighting for easy adaptation.",
    "image_urls": [
      "https://example.com/master-photo1.jpg",
      "https://example.com/master-photo2.jpg",
      "https://example.com/master-photo3.jpg"
    ],
    "mode": "max",
    "session_id": "cross-platform-twin"
  }'

# LinkedIn format (1:1 square)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Using the digital twin we just created, generate a 1:1 square format version optimized for LinkedIn. Professional appearance with a subtle corporate background.",
    "session_id": "cross-platform-twin"
  }'

# Twitter/X format (circular crop friendly)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a circular-crop-friendly version of the twin for Twitter/X profile. Center the face with enough margin for circular cropping. Slightly more casual than LinkedIn.",
    "session_id": "cross-platform-twin"
  }'

# Video thumbnail format (16:9)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 16:9 landscape version of the twin suitable for YouTube thumbnails and video call backgrounds. Position the twin on the right third with space for text on the left.",
    "session_id": "cross-platform-twin"
  }'
```

## 最佳实践

### 参考照片指南

- **数量**：提供 3-10 张参考照片以获得最佳效果
- **角度**：尽可能包括正面、3/4 轮廓和侧面视图
- **光线**：使用光线充足且无强烈阴影的照片
- **分辨率**：分辨率较高的照片能生成更逼真的数字孪生
- **一致性**：照片应显示同一个人在不同年龄阶段的样貌
- **表情**：提供多样化的表情以生成更具表现力的数字孪生

### 质量优化

- **模式选择**：使用 `max` 模式生成最终成果，使用 `eco` 模式进行快速原型制作
- **迭代优化**：使用 `session_id` 在多次请求中优化数字孪生
- **具体细节**：详细说明光线、背景和表情的要求
- **格式规范**：始终指定宽高比和预期用途

### 身份一致性

- **会话连续性**：为同一数字孪生的所有版本使用相同的 `session_id`
- **参考照片**：在请求不同版本时提供原始照片
- **风格一致性**：描述请求中光线和背景等元素的一致性

## 模式选择

在生成之前询问用户：

**“您需要快速且低成本的结果，还是高质量的结果？”**

| 模式 | 适用场景 | 速度 | 质量 |
|------|----------|-------|---------|
| `max` | 最终数字孪生、制作资产 | 较慢 | 最高质量 |
| `eco` | 快速预览、概念探索 | 较快 | 良好质量 |

## 多轮迭代开发数字孪生

使用 `session_id` 进行数字孪生的迭代开发和优化：

```bash
# Initial twin generation
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a digital twin from these photos for corporate communications",
    "image_urls": ["https://example.com/ceo-photo1.jpg", "https://example.com/ceo-photo2.jpg"],
    "mode": "max",
    "session_id": "ceo-digital-twin"
  }'

# Refine based on feedback
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Make the expression slightly more serious and add subtle rim lighting for more dimension",
    "session_id": "ceo-digital-twin"
  }'

# Generate variations
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create 3 variations with different backgrounds: 1) Modern office, 2) Gradient blue, 3) Pure white",
    "session_id": "ceo-digital-twin"
  }'
```

## 错误处理

| 错误 | 原因 | 解决方案 |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | 平衡不足 | 在 eachlabs.ai 网站补充数据 |
| 内容政策违规 | 内容被禁止 | 确保照片已获得适当授权 |
| 超时 | 生成过程复杂 | 将客户端超时设置为至少 10 分钟 |
| 输出质量低 | 参考照片质量差 | 提供更高质量、光线充足的照片 |

## 隐私与授权

在创建数字孪生时，请确保：

- 获得被克隆者的明确授权
- 数字孪生仅用于授权用途
- 生成的内容符合相关法律法规
- 如有必要，明确标注内容为深度伪造/合成媒体

## 相关技能

- `each-sense` - 核心 API 文档
- `face-swap` - 在现有图像中替换面部
- `video-generation` - 从图像创建视频
- `image-generation` - 通用图像生成