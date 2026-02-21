---
name: brochure-design-generation
description: 使用 each::sense AI 生成专业的宣传册设计。可以创建三折页、两折页、企业宣传册、旅行宣传册、产品宣传册、房地产宣传册、医疗保健宣传册、教育宣传册、活动宣传册和服务宣传册，这些宣传册都具有适合印刷的布局。
metadata:
  author: eachlabs
  version: "1.0"
---
# 小册子设计生成

使用 `each-sense` 功能生成专业的小册子设计。该技能能够为各种行业和用途创建视觉效果出众的小册子布局，适用于企业宣传、旅游营销等多种场景。

## 主要功能

- **三折小册子**：适用于营销材料的经典三页布局
- **二折小册子**：简洁的信息展示，适合使用两页的布局
- **企业小册子**：适用于商务沟通的专业设计
- **旅游/旅行小册子**：为旅游目的地和旅游项目设计吸引人的视觉内容
- **产品目录**：多页布局，用于展示产品系列
- **房地产小册子**：包含房产列表和开发项目信息
- **医疗保健小册子**：介绍医疗服务和患者相关信息
- **教育小册子**：适用于学校、课程和项目的资料
- **活动日程**：会议、婚礼等活动的安排信息
- **服务菜单**：餐厅、水疗中心等的服务价格表

## 快速入门

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a tri-fold brochure design for a digital marketing agency. Modern, clean aesthetic with blue and white color scheme. Include sections for services, case studies, and contact information.",
    "mode": "max"
  }'
```

## 小册子格式与尺寸

| 类型 | 尺寸（平展时） | 页数 | 适用场景 |
|------|-------------------|--------|----------|
| 三折 | 11英寸 x 8.5英寸 | 3页 | 营销材料、服务概览 |
| 二折 | 11英寸 x 8.5英寸 | 2页 | 简洁的信息展示、菜单 |
| Z折 | 11英寸 x 8.5英寸 | 3页 | 顺序性信息展示 |
| 门式折叠 | 17英寸 x 11英寸 | 4页 | 高端演示材料 |
- 折叠式 | 可变 | 4页以上 | 详细的产品目录 |
| A4单页 | 8.27英寸 x 11.69英寸 | 1页 | 传单、单页信息 |

## 适用场景示例

### 1. 三折小册子（营销机构）

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a tri-fold brochure design for a digital marketing agency called Vertex Digital. Modern minimalist design with navy blue and electric orange accents. Front panel: bold logo and tagline. Inside panels: services (SEO, PPC, Social Media), client testimonials, and case study highlights. Back panel: contact info and QR code placeholder. Professional photography style with geometric design elements.",
    "mode": "max"
  }'
```

### 2. 二折小册子（餐厅菜单）

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a bi-fold brochure design for an Italian restaurant called Bella Notte. Elegant design with warm burgundy and cream colors. Front: restaurant name with appetizing pasta dish image. Inside spread: menu sections for antipasti, primi, secondi, and dolci with food photography. Back: location map placeholder, hours, and reservation info. Rustic Italian aesthetic with subtle texture.",
    "mode": "max"
  }'
```

### 3. 企业小册子（公司简介）

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a corporate brochure design for a technology consulting firm called Nexus Solutions. Premium, sophisticated design with charcoal gray and gold accents. Include sections for: company overview, leadership team, service offerings, global presence, and client logos placeholder. Clean typography, professional business photography, and modern data visualization elements. Print-ready A4 format.",
    "mode": "max"
  }'
```

### 4. 旅游/旅行小册子

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a travel brochure for exploring Santorini, Greece. Stunning visuals with white-washed buildings and blue domes. Tri-fold layout with: cover showing iconic sunset view, inside panels featuring top attractions (Oia, Fira, beaches), tour packages with pricing placeholders, and local dining recommendations. Vibrant Mediterranean color palette. Back panel with travel tips and booking information.",
    "mode": "max"
  }'
```

### 5. 产品目录小册子

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a product catalog brochure for a premium watch brand called Chronos. Luxury aesthetic with black background and silver accents. Showcase 6 different watch models with detailed product photography. Include: model names, key features, price placeholders, and specifications. Elegant typography with ample white space. Gate-fold format for premium presentation.",
    "mode": "max"
  }'
```

### 6. 房地产小册子

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a real estate brochure for a luxury condominium development called The Residences at Harbor View. Sophisticated design with deep teal and champagne gold colors. Include: hero image of building exterior, floor plan layouts, amenities section (pool, gym, concierge), neighborhood highlights, and pricing table placeholder. Premium photography showing interiors and waterfront views. Bi-fold format.",
    "mode": "max"
  }'
```

### 7. 医疗保健小册子

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a healthcare brochure for a family medical clinic called Wellness First Medical Center. Calming design with soft blue and green colors. Tri-fold format with: services offered (primary care, pediatrics, lab services), doctor profiles section, patient resources, insurance information, and location with hours. Friendly, approachable imagery of diverse patients and healthcare providers. Clean, easy-to-read layout.",
    "mode": "max"
  }'
```

### 8. 教育小册子（大学）

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an educational brochure for a university business school MBA program. Professional yet inspiring design with maroon and white school colors. Include: program overview, curriculum highlights, faculty showcase, career outcomes statistics, campus life images, and application deadlines. Feature diverse students in academic and professional settings. Tri-fold format with clear call-to-action for applications.",
    "mode": "max"
  }'
```

### 9. 活动日程小册子

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an event program brochure for a tech conference called Innovation Summit 2024. Dynamic design with gradient purple to blue colors and tech-inspired geometric patterns. Include: event schedule over 2 days, keynote speaker profiles, workshop sessions, sponsor logos placeholder, venue map, and networking event details. Modern, energetic aesthetic. Bi-fold format for easy reference.",
    "mode": "max"
  }'
```

### 10. 服务菜单小册子（水疗中心）

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a service menu brochure for a luxury spa called Serenity Wellness Spa. Zen-inspired design with soft sage green, cream, and natural wood tones. Tri-fold format with: massage services and pricing, facial treatments, body treatments, packages and specials, and booking information. Peaceful imagery with natural elements like stones, bamboo, and orchids. Elegant serif typography with generous spacing.",
    "mode": "max"
  }'
```

## 多轮创意迭代

使用 `session_id` 进行小册子设计的迭代：

```bash
# Initial design
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a tri-fold brochure for an eco-friendly cleaning company. Green and natural aesthetic.",
    "session_id": "eco-brochure-001"
  }'

# Iterate based on feedback
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Make the design more modern with less leaf imagery. Add icons for each service type and include a pricing table.",
    "session_id": "eco-brochure-001"
  }'

# Request additional panels
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now create the back panel design with contact information, social media icons, and an eco-certification badge.",
    "session_id": "eco-brochure-001"
  }'
```

## 小册子系列生成

为某个品牌生成多份相关的小册子：

```bash
# Main services brochure
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a tri-fold brochure for a law firm called Sterling & Associates. Navy and gold color scheme, professional photography, services overview.",
    "session_id": "law-firm-brochures"
  }'

# Practice area specific brochure
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a matching brochure specifically for the Corporate Law practice area. Maintain the same brand identity and color scheme.",
    "session_id": "law-firm-brochures"
  }'

# Client testimonial brochure
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a client success stories brochure in the same style. Feature 3-4 case study placeholders with outcome statistics.",
    "session_id": "law-firm-brochures"
  }'
```

## 最佳实践

### 布局与设计
- **视觉层次结构**：通过清晰的标题结构引导读者的视线
- **空白空间**：避免内容过于拥挤，让内容有足够的空间展示
- **折叠考虑**：根据小册子的展开方式放置关键内容
- **出血区**：为专业印刷设置3毫米的出血边距
- **安全区域**：确保重要文本距离折叠线至少5毫米

### 字体排版
- **字体搭配**：最多使用2-3种字体系列
- **可读性**：正文字体大小至少为9-12号
- **标题**：使用加粗字体以便快速阅读
- **对比度**：确保文本在背景上清晰可见

### 图像
- **高分辨率**：使用300 DPI的图像以适应印刷需求
- **风格一致性**：保持各页面之间的视觉一致性
- **品牌色彩**：使用统一的色彩方案
- **图片质量**：使用专业或高质量的图片资源

### 内容结构
- **封面吸引力**：首页应立即吸引读者的兴趣
- **逻辑顺序**：信息应流畅地呈现
- **行动号召**：包含明确的下一步操作建议
- **联系方式**：始终提供联系方式

## 小册子设计提示

在创建小册子设计时，请包含以下详细信息：

1. **格式**：指定小册子的类型（三折、二折等）
2. **行业/用途**：小册子的用途是什么？
3. **品牌特色**：品牌色彩、风格、公司名称
4. **内容结构**：需要包含哪些信息
5. **图片风格**：摄影风格、插图、图标的使用
6. **目标受众**：谁会阅读这份小册子？
7. **印刷规格**：具体尺寸和方向（如有要求）

### 示例提示结构

```
"Create a [brochure type] brochure for [company/purpose].
[Brand colors and style preferences].
Include sections for: [content areas].
Target audience: [demographic].
[Additional requirements like imagery style, special elements, etc.]"
```

## 模式选择

在生成小册子之前，请询问用户：

**“您需要快速且低成本的设计，还是高质量的设计？”**

| 模式 | 适用场景 | 速度 | 质量 |
|------|----------|-------|---------|
| `max` | 最终的印刷版本、客户演示 | 较慢 | 最高质量 |
| `eco` | 快速草图、概念探索、布局测试 | 较快 | 良好 |

## 错误处理

| 错误 | 原因 | 解决方案 |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | 平衡不足 | 在 eachlabs.ai 网站充值 |
| 内容违规 | 包含被禁止的内容 | 调整提示内容以符合规定 |
| 超时 | 生成过程复杂 | 将客户超时时间设置为至少10分钟 |

## 相关技能

- `each-sense`：核心API文档生成工具
- `meta-ad-creative-generation`：社交媒体广告创意生成工具
- `product-photo-generation`：电子商务产品图片生成工具
- `presentation-design-generation`：幻灯片设计工具