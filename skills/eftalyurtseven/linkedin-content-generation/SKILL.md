---
name: linkedin-content-generation
description: 使用 each::sense AI 生成适用于 LinkedIn 的内容图形。可以创建专业的帖子图片、文章标题、公司横幅、活动推广素材、思想领导力相关的视觉资料，以及专为 LinkedIn 的专业用户群体优化的个人品牌内容。
metadata:
  author: eachlabs
  version: "1.0"
---
# LinkedIn内容生成

使用`each-sense`生成具有高影响力的LinkedIn内容图形。该技能可创建符合LinkedIn格式、受众期望以及B2B互动最佳实践的专业图片。

## 特点

- **帖子图片**：适合动态帖子和更新的高吸引力图片
- **文章标题图片**：适用于LinkedIn文章的专业标题图片
- **公司横幅**：与公司品牌一致的公司页面横幅
- **活动推广**：用于网络研讨会、会议和活动的图片
- **思想领导力内容**：展示行业见解和专业知识的视觉素材
- **数据可视化**：以信息图形式展示的数据和统计信息
- **团队公告**：新员工入职、晋升和团队庆祝的图片
- **职位发布**：吸引人的招聘职位图片
- **个人品牌**：适合个人思想领袖的专业图片

## 快速入门

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a LinkedIn post graphic about AI transformation in business, professional and modern style with blue color scheme",
    "mode": "max"
  }'
```

## LinkedIn图片格式与尺寸

| 内容类型 | 长宽比 | 推荐尺寸 | 使用场景 |
|--------------|--------------|------------------|----------|
| 动态帖子（单张） | 1.91:1 | 1200x628 | 标准帖子图片 |
| 动态帖子（方形） | 1:1 | 1080x1080 | 高互动性帖子 |
| 动态帖子（肖像） | 4:5 | 1080x1350 | 最大化在动态中的显示效果 |
| 文章标题 | 1.91:1 | 1200x628 | LinkedIn文章封面 |
| 公司横幅 | 4:1 | 1128x191 | 公司页面标题 |
| 活动封面 | 16:9 | 1600x900 | 活动页面图片 |
- 轮播图 | 1:1 | 1080x1080 | 文档/轮播帖子 |

## 使用场景示例

### 1. 专业帖子图片

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 LinkedIn post graphic about digital transformation. Show a professional in a modern office environment with digital elements and data visualizations floating around. Clean, corporate aesthetic with blue and white tones. Leave space at bottom for text overlay.",
    "mode": "max"
  }'
```

### 2. 文章标题图片

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1200x628 LinkedIn article header image about leadership in remote work. Abstract professional design showing connected people icons, home office elements, and collaboration symbols. Corporate blue gradient background with modern geometric shapes.",
    "mode": "max"
  }'
```

### 3. 公司页面横幅

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a LinkedIn company banner (1128x191 pixels, very wide 4:1 ratio) for a tech consulting firm. Abstract technology-themed design with circuit patterns, subtle gradient from dark blue to teal. Professional and innovative feel. No text, just visual elements.",
    "mode": "max"
  }'
```

### 4. 活动推广图片

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 16:9 LinkedIn event cover for a virtual leadership summit. Show a professional conference stage setup with modern lighting, screens displaying abstract business graphics, and an audience silhouette. Premium corporate event atmosphere with purple and blue accent lighting.",
    "mode": "max"
  }'
```

### 5. 思想领导力视觉素材

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 thought leadership post image about the future of AI in healthcare. Show an abstract visualization of AI and medical imagery merging - neural network patterns combined with medical symbols, DNA helixes, and healthcare icons. Clean white background with blue and green accents. Professional and innovative.",
    "mode": "max"
  }'
```

### 6. 数据/统计可视化背景

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 LinkedIn post background for showcasing business statistics. Abstract data visualization design with subtle chart elements, graph lines, and percentage symbols in the background. Dark professional theme with glowing blue and green data points. Leave large center area for text overlay of actual statistics.",
    "mode": "max"
  }'
```

### 7. 团队公告图片

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 LinkedIn graphic template for a new team member announcement. Professional celebratory design with confetti elements, welcome banner style, and a prominent circular placeholder area for a profile photo. Corporate colors (blue and gold), warm and welcoming atmosphere.",
    "mode": "max"
  }'
```

### 8. 招聘职位图片

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 4:5 LinkedIn job posting graphic for a software engineering position. Show a modern tech workspace with developers collaborating, multiple screens with code, bright and energetic office environment. Diverse team, innovative startup atmosphere. Leave top portion for job title text.",
    "mode": "max"
  }'
```

### 9. 行业洞察图片

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1.91:1 LinkedIn post image about fintech industry trends. Abstract financial technology visualization with blockchain nodes, digital currency symbols, and banking icons interconnected. Gradient from navy to electric blue, futuristic but professional. Suitable for a market analysis post.",
    "mode": "max"
  }'
```

### 10. 个人品牌内容

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 personal brand LinkedIn post image for a business coach sharing advice. Show a professional speaking or presenting, confident pose, modern minimalist office background with motivational elements. Warm, approachable lighting. Space at bottom for quote text overlay.",
    "mode": "max"
  }'
```

## 最佳实践

### 专业美学
- **色彩搭配**：使用蓝色、灰色、白色等专业色彩，并搭配点缀色
- **简洁设计**：避免杂乱；LinkedIn受众偏好精致、简约的设计
- **品牌一致性**：在所有内容中保持一致的视觉形象
- **文本空间**：为标题、统计数据或引文留出足够的空间

### 内容指南
- **专业语气**：内容应体现商务风格
- **高分辨率**：始终生成推荐尺寸的图片，以确保清晰显示
- **以移动设备优先**：大多数LinkedIn用户使用移动设备浏览——确保在小屏幕上也能清晰显示
- **可访问性**：为叠加的文本设置合适的对比度

### 互动优化
- **视觉层次**：引导观众注意力到关键元素
- **情感连接**：使用具有情感共鸣的元素以提高互动性
- **品牌识别**：在适当的地方加入品牌元素

## 创建LinkedIn内容的提示建议

在创建LinkedIn内容时，请在提示中包含以下信息：

1. **格式**：指定长宽比（1:1、1.91:1、4:5、16:9）
2. **内容类型**：帖子、文章标题、横幅、活动等
3. **行业**：科技、金融、医疗保健、咨询等
4. **氛围**：专业、创新、温馨、权威
5. **色彩方案**：企业蓝、品牌色等
6. **文本空间**：需要放置文字的位置
7. **目标受众**：高管、开发者、人力资源等

### 示例提示结构

```
"Create a [aspect ratio] LinkedIn [content type] for [industry/topic].
Show [visual description] with [mood/style].
Color scheme: [colors].
[Additional requirements like text space, brand elements, etc.]"
```

## 模式选择

在生成内容之前，请询问用户：

**“您需要快速且低成本的内容，还是高质量的内容？”**

| 模式 | 适用场景 | 速度 | 质量 |
|------|----------|-------|---------|
| `max` | 最终内容、重要帖子、品牌材料 | 较慢 | 最高质量 |
| `eco` | 快速草图、概念探索、批量测试 | 较快 | 良好质量 |

## 多轮内容迭代

使用`session_id`对LinkedIn内容进行迭代：

```bash
# Initial graphic
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 LinkedIn post about SaaS growth strategies, professional blue theme",
    "session_id": "linkedin-saas-post"
  }'

# Iterate based on feedback
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Make it more dynamic with upward trending graph elements and add some green accent colors for growth theme",
    "session_id": "linkedin-saas-post"
  }'

# Request variation
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an alternative version with a darker background for A/B testing",
    "session_id": "linkedin-saas-post"
  }'
```

## 轮播图内容生成

为LinkedIn轮播帖子生成多张图片：

```bash
# Slide 1 - Cover
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create slide 1 of 5 for a LinkedIn carousel about productivity tips. Cover slide design - bold, attention-grabbing with abstract productivity imagery. 1:1 format, dark blue background with orange accents.",
    "session_id": "productivity-carousel",
    "mode": "max"
  }'

# Slide 2 - Content slide
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create slide 2 of 5 maintaining the same visual style. Show time management concept with clock and calendar elements. Leave space for tip text.",
    "session_id": "productivity-carousel",
    "mode": "max"
  }'
```

## 批量内容生成

生成多个版本的内容以进行测试：

```bash
# Variation A - Abstract style
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 LinkedIn post about cloud computing - abstract geometric style with cloud and server icons",
    "mode": "eco"
  }'

# Variation B - Photo-realistic style
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 LinkedIn post about cloud computing - photo-realistic data center with blue lighting",
    "mode": "eco"
  }'

# Variation C - Minimal style
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 LinkedIn post about cloud computing - minimal line art style with simple cloud icon",
    "mode": "eco"
  }'
```

## 错误处理

| 错误 | 原因 | 解决方案 |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | 数据不平衡 | 在eachlabs.ai中补充数据 |
| 内容政策违规 | 禁止的内容 | 调整提示以符合专业内容指南 |
| 超时 | 生成过程复杂 | 将客户端超时设置为至少10分钟 |

## 相关技能

- `each-sense` - 核心API文档
- `meta-ad-creative-generation` - Meta（Facebook/Instagram）广告创意生成
- `google-ad-creative-generation` - Google Ads创意生成
- `product-photo-generation` - 电子商务产品图片生成