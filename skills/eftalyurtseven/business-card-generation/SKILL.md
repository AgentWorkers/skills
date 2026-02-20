---
name: business-card-generation
description: 使用 each::sense AI 生成专业的名片。可以创建企业风格、创意风格、极简风格、豪华风格以及专业风格的名片，这些名片均针对标准 3.5 x 2 英寸的打印尺寸进行了优化。
metadata:
  author: eachlabs
  version: "1.0"
---
# 名片生成

使用 `each-sense` 功能生成专业的名片。该技能能够为各种行业、风格和用途生成适合打印的名片设计，标准尺寸为 3.5 x 2 英寸（1050 x 600 像素）。

## 特点

- **企业名片**：为商务高管和员工设计的专业名片
- **创意名片**：适合设计师、艺术家和创意专业人士的艺术风格名片
- **极简风格名片**：以排版为主的简洁设计
- **豪华风格名片**：具有高级美学效果的精致设计
- **行业专用名片**：为房地产、摄影、餐饮、科技等行业定制的设计
- **竖版名片**：采用竖屏布局，设计更加独特醒目
- **双面名片**：正面和背面设计相互呼应

## 快速入门

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a professional business card for a marketing consultant, clean modern design with space for name, title, phone, email, and website",
    "mode": "max"
  }'
```

## 名片规格

| 类型 | 尺寸 | 像素 | 适用场景 |
|------|------------|--------|----------|
| 标准横版 | 3.5 x 2 英寸 | 1050 x 600 像素 | 最常见的格式 |
| 标准竖版 | 2 x 3.5 英寸 | 600 x 1050 像素 | 创意或独特的展示用途 |
| 欧洲标准 | 85 x 55 毫米 | 1004 x 650 像素 | 国际通用标准 |
| 正方形 | 2.5 x 2.5 英寸 | 750 x 750 像素 | 现代或创意企业的选择 |

## 适用场景示例

### 1. 企业名片

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a corporate business card at 1050x600 pixels for a senior financial advisor. Navy blue and gold color scheme, professional and trustworthy feel. Include placeholder areas for: name, title (Senior Financial Advisor), company name, phone number, email, and office address. Add a subtle geometric pattern in the background. Clean sans-serif typography.",
    "mode": "max"
  }'
```

### 2. 创意/设计师名片

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an artistic business card at 1050x600 pixels for a graphic designer. Bold, creative design with vibrant gradient colors (purple to pink to orange). Abstract geometric shapes, modern and eye-catching. Include space for name, title (Creative Director), portfolio website, email, and Instagram handle. Make it memorable and showcase design skills.",
    "mode": "max"
  }'
```

### 3. 极简风格名片

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a minimalist business card at 1050x600 pixels. White background with black typography only. Elegant serif font for the name, clean sans-serif for contact details. Generous white space, sophisticated and refined. Include areas for: name, job title, email, phone, and a small logo placeholder in the corner. Less is more aesthetic.",
    "mode": "max"
  }'
```

### 4. 豪华风格名片

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a luxury business card at 1050x600 pixels for a high-end jewelry brand owner. Black background with gold foil effect elements. Elegant script font for the name, refined serif for details. Include subtle embossed texture effect, ornate border detail. Space for: name, title (Founder & Creative Director), brand name, phone, email, and boutique address. Premium, exclusive feel.",
    "mode": "max"
  }'
```

### 5. 科技初创企业名片

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a modern tech startup business card at 1050x600 pixels. Dark theme with neon accent colors (electric blue or cyan). Futuristic, innovative aesthetic with subtle circuit board or data visualization patterns. Clean modern typography. Include space for: name, title (Co-Founder & CTO), company name, email, LinkedIn profile, and QR code placeholder. Tech-forward and cutting-edge vibe.",
    "mode": "max"
  }'
```

### 6. 房地产经纪人名片

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a real estate agent business card at 1050x600 pixels. Professional yet approachable design. Include a photo placeholder area on the left side. Color scheme: deep teal and white with gold accents. Include space for: agent name, title (Licensed Real Estate Agent), brokerage name, phone, email, website, and license number. Add a small house icon or property silhouette. Trustworthy and established feel.",
    "mode": "max"
  }'
```

### 7. 摄影师名片

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a photographer business card at 1050x600 pixels. Artistic design with a large image placeholder area showing a blurred/abstract photograph background. Camera aperture icon or lens element as design feature. Elegant typography in white over the image. Include space for: photographer name, specialty (Wedding & Portrait Photography), phone, email, Instagram, and website. Creative and visual storytelling aesthetic.",
    "mode": "max"
  }'
```

### 8. 餐厅/厨师名片

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a restaurant chef business card at 1050x600 pixels. Warm, inviting color palette - cream background with burgundy and copper accents. Include a chef hat or knife icon. Elegant typography mixing script and serif fonts. Subtle food-related pattern or texture. Include space for: chef name, title (Executive Chef), restaurant name, phone, email, and restaurant address. Culinary excellence and artistry feel.",
    "mode": "max"
  }'
```

### 9. 竖版名片

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a vertical business card at 600x1050 pixels (portrait orientation) for an architect. Modern architectural design with clean lines and geometric shapes. Black and white with one accent color (coral or mustard). Include building silhouette or blueprint element. Space for: name at top, title (Principal Architect), firm name, contact details stacked vertically - phone, email, website, office address. Contemporary and structural aesthetic.",
    "mode": "max"
  }'
```

### 10. 双面名片（正面和背面）

```bash
# Front side
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create the FRONT side of a double-sided business card at 1050x600 pixels for a law firm partner. Clean, prestigious design with navy blue background. Large centered logo placeholder area, firm name in elegant gold serif typography below. Established, authoritative, trustworthy aesthetic. This is the presentation side - minimal information, maximum impact.",
    "session_id": "lawfirm-card-001"
  }'

# Back side (same session for visual consistency)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create the BACK side of the same business card. White background with navy blue text to complement the front. Include all contact details: attorney name, title (Senior Partner), bar number, phone, fax, email, office address, and website. Clean layout with clear hierarchy. Add a thin gold accent line. Same typography style as front for consistency.",
    "session_id": "lawfirm-card-001"
  }'
```

## 最佳实践

### 设计指南
- **出血区**：在所有边缘预留 0.125 英寸（3.75 像素）的出血边距以适应打印需求
- **安全区**：确保重要内容距离边缘至少 0.125 英寸
- **分辨率**：设计时使用 300 DPI 以确保打印效果清晰
- **字体**：使用至少 8 磅的字体以保证可读性
- **对比度**：确保文字在背景上清晰可见

### 内容层次结构
1. **姓名**：最显眼的元素
2. **职位/头衔**：次级显眼的元素
3. **公司/品牌**：辅助信息
4. **联系方式**：清晰且条理分明
5. **Logo**：与其他元素平衡搭配

### 颜色选择
- 使用 CMYK 安全色以确保打印准确性
- 颜色搭配控制在 2-3 种以内以保持整体一致性
- 豪华名片可考虑使用金属质感或箔纸效果
- 确保足够的对比度以便文字清晰可读

## 名片制作提示

在制作名片时，请在提示中包含以下信息：
1. **尺寸**：指定像素尺寸（标准横版为 1050x600）
2. **行业/职位**：该名片适用于哪个行业或职位？
3. **风格**：企业风格、创意风格、极简风格、豪华风格等
4. **配色方案**：具体的颜色或颜色范围
5. **信息字段**：需要包含哪些文本内容
6. **特殊元素**：图标、图案、照片区域、二维码
7. **字体样式**：衬线字体、无衬线字体、手写体、现代风格或经典风格

### 示例提示结构

```
"Create a [style] business card at [dimensions] for a [profession/industry].
[Color scheme description]. Include space for: [list of information fields].
[Design elements and aesthetic description].
[Additional requirements like icons, patterns, effects]."
```

## 模式选择

在生成名片之前，请询问用户：

**“您需要快速且低成本的名片，还是高质量的名片？”**

| 模式 | 适用场景 | 速度 | 质量 |
|------|----------|-------|---------|
| `max` | 最终的打印成品、客户演示 | 较慢 | 最高质量 |
| `eco` | 快速的概念设计、草图迭代、批量制作 | 较快 | 一般质量 |

## 多轮设计迭代

使用 `session_id` 进行名片设计的多次迭代：

```bash
# Initial design
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a business card for a yoga instructor, calming natural aesthetic",
    "session_id": "yoga-card-project"
  }'

# Iterate based on feedback
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Make the colors warmer, add a lotus flower icon, and use a more elegant script font for the name",
    "session_id": "yoga-card-project"
  }'

# Request variation
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create 2 more variations with different color palettes - one with sage green, one with dusty rose",
    "session_id": "yoga-card-project"
  }'
```

## 团队批量生成

为团队成员生成统一风格的名片：

```bash
# Template card
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a corporate business card template for Acme Corporation. Blue and white color scheme with the company logo area in top left. Fields: employee name, job title, department, phone, email, office location.",
    "session_id": "acme-team-cards",
    "mode": "max"
  }'

# Generate variations
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Using the same design, create cards with these titles: CEO, CFO, VP of Marketing, Head of Engineering. Keep all other design elements consistent.",
    "session_id": "acme-team-cards"
  }'
```

## 错误处理

| 错误 | 原因 | 解决方案 |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | 资金不足 | 在 eachlabs.ai 网站充值 |
| 内容违规 | 包含禁止的内容 | 调整提示内容 |
| 超时 | 设计过程复杂 | 将客户等待时间设置为至少 10 分钟 |

## 相关技能

- `each-sense`：核心 API 文档
- `meta-ad-creative-generation`：元广告创意设计
- `product-photo-generation`：产品照片生成
- `logo-generation`：Logo 设计