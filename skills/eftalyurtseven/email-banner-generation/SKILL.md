---
name: email-banner-generation
description: 使用 each::sense AI 生成电子邮件营销横幅和标题。创建适合电子邮件展示的尺寸和最佳实践要求的新闻通讯标题、促销横幅、欢迎邮件以及季节性活动内容。
metadata:
  author: eachlabs
  version: "1.0"
---
# 电子邮件横幅生成

使用 `each-sense` 功能生成高转化率的电子邮件营销横幅和标题。该功能可生成专为电子邮件客户端优化的图片，标准宽度为 600px，以确保最佳兼容性。

## 特点

- **新闻通讯标题**：适用于定期发送的新闻通讯的专业标题
- **促销横幅**：销售公告和折扣活动
- **产品公告**：新产品和功能发布的视觉素材
- **欢迎邮件**：新订阅者的首屏标题
- **季节性活动**：节日和季节性主题的横幅
- **活动邀请**：网络研讨会、会议和活动的标题
- **限时抢购横幅**：带有倒计时的紧急风格图形
- **客户评价横幅**：客户评价和社交证明的视觉素材
- **电子邮件签名**：专业的品牌签名横幅

## 快速入门

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an email newsletter header, 600px wide, for a tech company weekly digest. Modern, clean design with blue gradient background.",
    "mode": "max"
  }'
```

## 电子邮件横幅尺寸及最佳实践

| 横幅类型 | 尺寸 | 使用场景 |
|-------------|------------|----------|
| 标准标题 | 600x200 | 新闻通讯标题、一般公告 |
| 主题横幅 | 600x300 | 促销活动、产品发布 |
| 紧凑型标题 | 600x150 | 极简风格标题、签名横幅 |
| 全功能横幅 | 600x400 | 产品展示、活动邀请 |
| 签名横幅 | 600x100 | 电子邮件签名图形 |

**注意：** 600px 的宽度是所有主流电子邮件客户端（Gmail、Outlook、Apple Mail 等）都能正确显示的安全标准。

## 使用场景示例

### 1. 新闻通讯标题

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 600x200px email newsletter header for a tech startup weekly digest. Clean modern design with subtle geometric patterns, dark blue to purple gradient background. Include space for logo on the left side. Professional and contemporary feel.",
    "mode": "max"
  }'
```

### 2. 促销横幅

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 600x300px promotional email banner for a 50% off summer sale. Bright, energetic design with coral and yellow colors. Include visual space for SALE headline text and shop now button. E-commerce fashion brand style.",
    "mode": "max"
  }'
```

### 3. 产品公告横幅

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 600x300px email banner announcing a new smartphone launch. Premium tech aesthetic with dark background, subtle light rays, and space for product image placement. Apple-style minimalism with focus on elegance.",
    "mode": "max"
  }'
```

### 4. 欢迎邮件标题

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 600x250px welcome email header for a fitness app. Warm, inviting design with energetic person silhouette, sunrise gradient (orange to yellow), motivational atmosphere. Space for Welcome message and brand logo.",
    "mode": "max"
  }'
```

### 5. 节日/季节性横幅

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 600x300px holiday email banner for Christmas sale campaign. Festive design with snow, pine trees silhouettes, red and gold color scheme. Elegant with subtle sparkles, space for holiday greeting text and discount badge.",
    "mode": "max"
  }'
```

### 6. 活动邀请横幅

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 600x350px email header for a virtual conference invitation. Professional corporate design with abstract network visualization, deep blue and teal colors. Include visual areas for event name, date, and register button. Tech conference aesthetic.",
    "mode": "max"
  }'
```

### 7. 新系列产品公告

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 600x300px email banner for a fashion brand new spring collection launch. Elegant, high-fashion aesthetic with soft pastel colors (blush pink, sage green). Minimalist with space for NEW COLLECTION text overlay. Luxury brand feel.",
    "mode": "max"
  }'
```

### 8. 限时抢购横幅

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 600x250px flash sale email banner with urgency. Bold design with red and black colors, dynamic diagonal stripes or lightning bolt elements. Include visual space for countdown timer display boxes (hours:minutes:seconds). High energy, act now feeling.",
    "mode": "max"
  }'
```

### 9. 客户评价横幅

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 600x280px email banner for customer testimonials section. Clean design with soft gradient background (light gray to white), space for circular customer photo placeholder, quote marks design element, 5-star rating visual. Trust-building, professional layout.",
    "mode": "max"
  }'
```

### 10. 电子邮件签名横幅

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 600x100px email signature banner for a marketing agency. Sleek horizontal design with subtle gradient, space for company logo on left, social media icon placeholders on right. Professional, minimal, brand-forward design.",
    "mode": "max"
  }'
```

## 最佳实践

### 电子邮件兼容性设计
- **宽度**：始终使用 600px 的宽度，以确保与所有主流电子邮件客户端的兼容性
- **文件大小**：保持图片大小在 1MB 以下，以加快加载速度
- **格式**：PNG 用于带透明度的图形，JPG 用于照片
- **替代文本**：务必添加描述性的替代文本以提高可访问性
- **Retina 显示支持**：考虑将 1200px 宽度的图片缩放至 600px 以适应 Retina 显示器

### 视觉设计指南
- **文本空间**：为文本叠加留出足够的空间
- **对比度**：确保文本区域有足够的对比度
- **品牌一致性**：在不同活动中保持颜色和风格的统一性
- **移动设备**：考虑移动电子邮件客户端的设计（单列布局）
- **安全区域**：将关键元素放置在远离边缘的位置

### 内容提示
- **清晰的层次结构**：最重要的信息应立即可见
- **单一焦点**：每个横幅只传达一个主要信息
- **点击按钮的可见性**：确保点击按钮区域醒目
- **最少化文本**：尽可能使用辅助性 HTML 文本，而非图片中的文字

## 创建电子邮件横幅的提示

在创建电子邮件横幅时，请包含以下详细信息：

1. **尺寸**：指定确切的尺寸（例如，600x300px）
2. **横幅类型**：标题、促销、公告等
3. **配色方案**：品牌颜色或所需调色板
4. **文本位置**：标题/点击按钮的位置
5. **风格**：极简、醒目、优雅、有趣等
- **行业**：电子商务、SaaS、健身、时尚等

### 示例提示结构

```
"Create a [width]x[height]px email [banner type] for [industry/brand].
[Style description] with [color scheme].
Include space for [text elements like headline, CTA, logo].
[Mood/feeling] aesthetic."
```

## 模式选择

在生成横幅之前，请询问用户：

**“您希望快速且低成本，还是高质量？”**

| 模式 | 适用场景 | 速度 | 质量 |
|------|----------|-------|---------|
| `max` | 最终活动横幅、A/B 测试结果 | 较慢 | 最高质量 |
| `eco` | 快速草图、概念探索、批量生成 | 较快 | 良好质量 |

## 多轮创意迭代

使用 `session_id` 进行电子邮件横幅的迭代设计：

```bash
# Initial banner
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 600x300px promotional email banner for Black Friday sale. Bold design with dark background.",
    "session_id": "email-campaign-bf2024"
  }'

# Iterate based on feedback
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Add more gold accents and make the design more premium looking. Include space for 70% OFF text.",
    "session_id": "email-campaign-bf2024"
  }'

# Request size variation
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a compact 600x150px version of this banner for email signature use.",
    "session_id": "email-campaign-bf2024"
  }'
```

## 活动批量生成

生成多个版本以进行 A/B 测试：

```bash
# Variation A - Bold colors
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 600x300px email banner for spring sale - bold vibrant colors, energetic design",
    "mode": "eco"
  }'

# Variation B - Minimal design
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 600x300px email banner for spring sale - minimal clean design, soft pastels",
    "mode": "eco"
  }'

# Variation C - Photo-centric
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 600x300px email banner for spring sale - lifestyle photography style, person in spring setting",
    "mode": "eco"
  }'
```

## 错误处理

| 错误 | 原因 | 解决方案 |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | 资金不足 | 在 eachlabs.ai 补充资金 |
| 内容违规 | 禁止的内容 | 调整提示以符合内容政策 |
| 超时 | 生成过程复杂 | 将客户端超时设置至少为 10 分钟 |

## 相关技能

- `each-sense` - 核心 API 文档
- `meta-ad-creative-generation` - Meta/Facebook 广告创意生成
- `product-photo-generation` - 电子商务产品图片生成