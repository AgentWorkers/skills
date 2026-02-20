---
name: ai-headshot-generation
description: 使用 each::sense AI 从普通照片中生成专业的 AI 职业头像。您可以制作公司肖像、领英头像、高管头像、团队照片等，所有图片都能保持一致的专业质量。
metadata:
  author: eachlabs
  version: "1.0"
---
# 人工智能头像生成

使用 `each-sense` 技术，可以从普通照片或文字描述中生成专业的人工智能头像。该功能能够生成适合企业使用、社交媒体个人资料、简历和营销材料的精致头像。

## 主要特点

- **企业头像**：适用于公司网站和名录的专业肖像
- **领英头像**：专为职业社交优化的高质量头像
- **高管头像**：适合高管层和领导团队的优质头像
- **团队头像**：确保团队成员头像风格统一
- **背景选择**：办公室、工作室、渐变或自定义背景
- **着装转换**：将休闲装束转换为专业的商务装束
- **表情多样性**：同一张照片可生成多种表情
- **多平台兼容**：支持多种宽高比和用途

## 快速入门

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a professional corporate headshot from this casual photo. Clean background, professional lighting, business appropriate appearance.",
    "mode": "max",
    "image_urls": ["https://example.com/casual-photo.jpg"]
  }'
```

## 头像格式与尺寸

| 用途 | 宽高比 | 推荐尺寸 | 备注 |
|------|---------|-------------|---------|
| 领英 | 1:1 | 400x400 至 800x800 | 方形裁剪，仅显示头部和肩膀 |
| 公司网站 | 3:4 | 600x800 | 标准肖像比例 |
| 简历/简历 | 1:1 或 3:4 | 300x300 或 300x400 | 背景简洁 |
| 电子邮件签名 | 1:1 | 150x150 至 300x300 | 小巧但清晰可辨 |
| 演讲者头像 | 1:1 或 16:9 | 800x800 或 1920x1080 | 适用于会议/活动 |
| 团队页面 | 1:1 | 500x500 | 团队成员头像风格统一 |

## 用途示例

### 1. 从普通照片生成企业头像

将一张休闲的自拍或个人照片转换为专业的企业头像。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Transform this casual photo into a professional corporate headshot. Use a clean neutral gray background, soft professional studio lighting, and ensure the subject looks polished and approachable. Keep the likeness accurate.",
    "mode": "max",
    "image_urls": ["https://example.com/casual-selfie.jpg"]
  }'
```

### 2. 领英个人资料头像

专为领英创建的高质量头像，展现专业性和亲和力。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a LinkedIn-optimized professional headshot from this photo. Square 1:1 format, friendly but professional expression, clean blurred office background, warm natural lighting. The subject should appear confident and approachable.",
    "mode": "max",
    "image_urls": ["https://example.com/source-photo.jpg"]
  }'
```

### 3. 高管头像

适合高管层、董事会成员和高级领导者的优质头像。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a premium executive headshot from this photo. Dark sophisticated background with subtle gradient, dramatic professional lighting, formal business attire appearance. The subject should convey authority, confidence, and leadership. Magazine cover quality.",
    "mode": "max",
    "image_urls": ["https://example.com/ceo-casual.jpg"]
  }'
```

### 4. 团队头像（风格统一）

为团队成员生成统一风格的头像，提升整体形象。

```bash
# First team member - establish the style
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a professional team headshot with these specifications: light gray background, soft diffused lighting from the left, 1:1 square format, head and shoulders framing. Professional but friendly expression. This will be the template style for our entire team.",
    "session_id": "team-headshots-2024",
    "mode": "max",
    "image_urls": ["https://example.com/team-member-1.jpg"]
  }'

# Second team member - maintain consistency
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a headshot for this team member using the exact same style as the previous one - same background, lighting, framing, and overall aesthetic.",
    "session_id": "team-headshots-2024",
    "mode": "max",
    "image_urls": ["https://example.com/team-member-2.jpg"]
  }'

# Third team member
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a headshot for this team member matching our established team style.",
    "session_id": "team-headshots-2024",
    "mode": "max",
    "image_urls": ["https://example.com/team-member-3.jpg"]
  }'
```

### 5. 不同背景的头像

使用不同的背景生成相同的头像。

```bash
# Office background
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a professional headshot with a blurred modern office background. Glass windows, city view visible but out of focus. Natural daylight feel.",
    "session_id": "background-variations",
    "mode": "max",
    "image_urls": ["https://example.com/source-photo.jpg"]
  }'

# Studio gradient background
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now create the same headshot but with a classic studio gradient background - deep blue fading to lighter blue. Keep the same professional lighting on the subject.",
    "session_id": "background-variations",
    "mode": "max"
  }'

# Nature/outdoor background
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create another variation with a natural outdoor background - soft green foliage, blurred bokeh effect, golden hour lighting. More relaxed professional vibe.",
    "session_id": "background-variations",
    "mode": "max"
  }'
```

### 6. 不同着装的头像

通过更换服装来调整人物的专业形象。

```bash
# Navy suit
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a professional headshot from this casual photo. Dress the subject in a classic navy blue business suit with a white dress shirt and subtle tie. Clean gray background, professional studio lighting.",
    "session_id": "outfit-variations",
    "mode": "max",
    "image_urls": ["https://example.com/casual-photo.jpg"]
  }'

# Business casual
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create another version with business casual attire - a blazer over a smart polo shirt or open-collar dress shirt. Same background and lighting as before.",
    "session_id": "outfit-variations",
    "mode": "max"
  }'

# Creative professional
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a version for creative industry - stylish but professional, perhaps a dark turtleneck or modern collarless jacket. Contemporary creative professional look.",
    "session_id": "outfit-variations",
    "mode": "max"
  }'
```

### 7. 简历/简历头像

简洁专业的头像，适合求职和简历使用。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a clean, professional headshot suitable for a resume or CV. Simple solid light background (white or very light gray), professional attire, friendly and confident expression. The photo should be conservative and appropriate for any industry. Square format, head and shoulders framing.",
    "mode": "max",
    "image_urls": ["https://example.com/applicant-photo.jpg"]
  }'
```

### 演讲者/作者头像

适用于会议演讲者、作者和思想领袖的动态头像。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a compelling speaker/author headshot. The subject should appear engaging, confident, and dynamic. Use dramatic lighting with a dark background to create visual impact. Slight smile, eyes that connect with the viewer. This should work well on book covers, conference websites, and keynote slides. High contrast, memorable, professional.",
    "mode": "max",
    "image_urls": ["https://example.com/author-source.jpg"]
  }'
```

### 房地产经纪人头像

适合房地产从业者的亲和力强的头像。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a real estate agent headshot. The subject should appear trustworthy, friendly, and professional. Warm lighting, genuine smile, approachable expression. Background should be a subtle blurred interior of an upscale home or modern building. Professional but not stiff - someone you would trust to help you buy a home.",
    "mode": "max",
    "image_urls": ["https://example.com/agent-photo.jpg"]
  }'
```

### 多种表情头像

同一张照片可生成多种表情。

```bash
# Confident/serious
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a professional headshot with a confident, serious expression. Professional and authoritative, suitable for a law firm or financial services. Neutral gray background, classic professional lighting.",
    "session_id": "expression-variations",
    "mode": "max",
    "image_urls": ["https://example.com/source-photo.jpg"]
  }'

# Friendly/approachable
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now create a variation with a warm, friendly smile. Approachable and welcoming, suitable for customer-facing roles or consulting. Same background and lighting setup.",
    "session_id": "expression-variations",
    "mode": "max"
  }'

# Thoughtful/engaged
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create another variation with a thoughtful, engaged expression - slight smile, intelligent and curious look. Good for tech industry or academia. Same background and lighting.",
    "session_id": "expression-variations",
    "mode": "max"
  }'
```

## 最佳实践

### 照片输入指南
- **面部可见性**：确保面部清晰可见、光线充足且无遮挡
- **分辨率**：建议使用至少 512x512 像素的源照片以获得最佳效果
- **拍摄角度**：正面或轻微倾斜（3/4 视角）效果最佳
- **光线**：避免照片中有明显的阴影或过度逆光
- **表情**：源照片中的表情应保持中性或自然，以便生成更好的效果

### 专业头像标准
- **构图**：仅显示头部和肩膀，面部占垂直空间的 60-70%
- **眼神交流**：人物应看向拍摄者
- **背景**：背景简洁、不分散注意力，与人物形象相得益彰
- **光线**：柔和、 flattering 的光线，减少阴影
- **着装**：符合行业和职位要求

### 行业特定建议

| 行业 | 风格 | 背景 | 着装 |
|------|-------|------------|--------|
| 金融/法律 | 保守、正式 | 中性灰色/蓝色 | 深色西装、传统风格 |
| 科技 | 现代、亲和力强 | 清晰的渐变背景或办公室环境 | 休闲商务装 |
| 创意 | 动感、独特 | 明显的渐变或艺术风格 | 当代、时尚 |
| 医疗保健 | 可信赖、温暖 | 温和的光线、临床或中性背景 | 专业着装（可选白大褂） |
| 房地产 | 友善、可信 | 家居室内背景 | 专业商务装 |
| 学术 | 深思熟虑、可信 | 图书馆或中性背景 | 休闲商务装 |

## 模式选择

生成头像前请询问用户：

**“您需要快速且低成本的效果，还是高质量的效果？”**

| 模式 | 适用场景 | 速度 | 质量 |
|------|---------|--------|---------|
| `max` | 最终头像、客户交付成果、高管肖像 | 较慢 | 最高质量 |
| `eco` | 快速预览、风格测试、批量草图 | 较快 | 良好质量 |

## 多轮头像优化

使用 `session_id` 进行多次迭代，完善头像效果：

```bash
# Initial generation
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a professional headshot from this photo with a blue gradient background",
    "session_id": "headshot-refinement",
    "mode": "max",
    "image_urls": ["https://example.com/source.jpg"]
  }'

# Refine based on feedback
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Make the lighting warmer and the expression slightly more friendly. Keep the same background.",
    "session_id": "headshot-refinement",
    "mode": "max"
  }'

# Final adjustments
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Perfect. Now generate 2 more slight variations of this final result.",
    "session_id": "headshot-refinement",
    "mode": "max"
  }'
```

## 团队头像批量生成

高效地为整个团队生成统一风格的头像：

```bash
# Define team style first
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "I need to create headshots for a team of 10 people. Our brand colors are navy blue and white. We want: 1:1 square format, light gray background, soft professional lighting, business casual attire, friendly but professional expressions. First, create a headshot for this team member to establish the style.",
    "session_id": "acme-corp-team",
    "mode": "max",
    "image_urls": ["https://example.com/team/person-1.jpg"]
  }'

# Continue with remaining team members using same session
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create headshot for next team member, matching established style",
    "session_id": "acme-corp-team",
    "mode": "eco",
    "image_urls": ["https://example.com/team/person-2.jpg"]
  }'
```

## 错误处理

| 错误类型 | 原因 | 解决方案 |
|--------|-------|----------|
| `Failed to create prediction: HTTP 422` | 数据不平衡 | 请访问 eachlabs.ai 补充数据 |
| 未检测到面部 | 源照片中面部不可见 | 使用面部清晰的照片 |
| 生成效果不佳 | 图像质量过低 | 使用更高分辨率的源照片（512x512 或以上） |
| 超时 | 生成过程复杂 | 将客户等待时间设置为至少 10 分钟 |

## 相关技能

- `each-sense`：核心 API 文档
- `product-photo-generation`：电子商务产品摄影
- `meta-ad-creative-generation`：社交媒体广告创意设计