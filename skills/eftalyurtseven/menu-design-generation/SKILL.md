---
name: menu-design-generation
description: 使用 each::sense AI 为餐厅、咖啡馆和酒吧生成专业的菜单设计。这些设计包括可用于打印的纸质菜单、数字显示屏菜单、二维码菜单，以及包含精美食物照片和优雅排版布局的季节性特色菜谱。
metadata:
  author: eachlabs
  version: "1.0"
---
# 菜单设计生成

使用 `each::sense` 为餐厅、咖啡馆、酒吧和餐饮服务企业生成专业的菜单设计。该技能能够创建视觉效果出色的菜单布局，结合食物图片、排版设计元素，以适应各种展示格式和用餐体验。

## 主要功能

- **完整版菜单**：包含各个菜系和价格的完整餐厅菜单
- **数字显示屏**：适用于电视屏幕和数字标牌的高对比度菜单
- **咖啡馆菜单**：适合咖啡店的温馨、手工艺风格设计
- **酒吧/鸡尾酒菜单**：风格优雅的饮品菜单
- **快餐菜单**：简洁醒目的快餐菜单
- **高级餐厅菜单**：豪华、极简风格的设计
- **季节性特餐**：具有节日主题的限时菜单设计
- **二维码菜单**：专为移动端优化的无接触点餐菜单

## 快速入门

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a modern restaurant menu design for an Italian trattoria with appetizers, pasta, mains, and desserts sections. Warm rustic aesthetic with elegant typography.",
    "mode": "max"
  }'
```

## 菜单格式与尺寸

| 菜单类型 | 长宽比 | 推荐尺寸 | 使用场景 |
|-----------|--------------|------------------|----------|
| 打印菜单（Letter纸） | 8.5:11 | 2550x3300 像素 | 传统打印菜单 |
| 打印菜单（A4纸） | 1:1.414 | 2480x3508 像素 | 国际通用打印格式 |
| 数字显示屏 | 16:9 | 1920x1080 像素 | 电视屏幕、显示器 |
| 数字显示屏（竖屏） | 9:16 | 1080x1920 像素 | 竖向数字标牌 |
| 桌面展示牌 | 4:6 | 1200x1800 像素 | 桌面展示用 |
| 二维码菜单（移动端） | 9:16 | 1080x1920 像素 | 专为移动端优化的菜单 |
| 墙壁展示牌 | 3:2 | 1800x1200 像素 | 墙壁安装的展示牌 |

## 使用场景示例

### 1. 餐厅菜单（完整版）

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a full-page restaurant menu design for a Mediterranean bistro. Include sections for Starters (hummus, falafel, calamari), Mains (grilled lamb, seafood platter, moussaka), and Desserts (baklava, tiramisu). Use warm earth tones, elegant serif typography, and include subtle olive branch decorative elements. Portrait orientation for print.",
    "mode": "max"
  }'
```

### 2. 咖啡馆菜单

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design a cozy coffee shop menu board for an artisan cafe. Include Hot Drinks (espresso, latte, cappuccino, mocha), Cold Drinks (iced coffee, cold brew, frappes), and Pastries (croissants, muffins, cookies). Rustic chalkboard aesthetic with hand-drawn style illustrations, warm brown and cream colors. Horizontal format for counter display.",
    "mode": "max"
  }'
```

### 3. 酒吧/鸡尾酒菜单

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an upscale cocktail bar menu design. Include Signature Cocktails (Old Fashioned, Negroni, Espresso Martini), Classic Cocktails, Wine by the Glass, and Premium Spirits sections. Dark moody aesthetic with gold accents, art deco styling, elegant script typography. Tall format suitable for leather menu holder.",
    "mode": "max"
  }'
```

### 4. 快餐菜单

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design a bold fast food menu board for a burger joint. Include Burgers (classic, bacon, veggie), Sides (fries, onion rings, nuggets), Drinks, and Combo Meals with large pricing. Bright colors (red, yellow, white), high contrast, appetizing burger photography, easy to read from distance. 16:9 landscape for overhead display.",
    "mode": "max"
  }'
```

### 5. 高级餐厅菜单

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an elegant fine dining tasting menu design. Include 7-course tasting menu: Amuse-bouche, First Course, Fish Course, Palate Cleanser, Main Course, Pre-Dessert, Dessert. Minimalist luxury aesthetic with lots of white space, thin elegant fonts, subtle gold foil accents on cream paper texture. Portrait A4 format.",
    "mode": "max"
  }'
```

### 6. 早午餐菜单

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design a vibrant weekend brunch menu for a trendy cafe. Include Eggs & Benedicts, Pancakes & Waffles, Healthy Bowls, Bottomless Brunch Drinks (mimosas, bloody marys, bellinis). Fresh, light aesthetic with pastel colors, modern sans-serif typography, watercolor fruit illustrations. Portrait format for table menus.",
    "mode": "max"
  }'
```

### 7. 甜点菜单

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a decadent dessert menu for a patisserie. Include Cakes (chocolate lava, cheesecake, tiramisu), Pastries (eclairs, macarons, tarts), Ice Cream & Sorbets, and Specialty Coffee Pairings. Luxurious aesthetic with rich colors (burgundy, gold, chocolate brown), elegant cursive headers, beautiful dessert photography. Square format.",
    "mode": "max"
  }'
```

### 8. 数字显示屏菜单

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design a digital menu display for a sushi restaurant TV screen. Include Sashimi, Nigiri, Maki Rolls, Special Rolls with prices. Modern Japanese aesthetic with dark background for screen display, high contrast white and red text, clean grid layout, subtle wave patterns. 16:9 HD format optimized for digital signage.",
    "mode": "max"
  }'
```

### 9. 二维码菜单设计

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a mobile-optimized QR code menu design for a taco restaurant. Include Tacos (carnitas, al pastor, fish), Burritos, Sides (rice, beans, guacamole), and Drinks. Scrollable single-column layout, large touch-friendly sections, vibrant Mexican colors (orange, green, pink), playful typography. 9:16 mobile portrait format with clear section headers.",
    "mode": "max"
  }'
```

### 10. 季节性/特餐菜单

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design a winter holiday special menu for a restaurant. Include Holiday Appetizers, Seasonal Mains (roast turkey, prime rib, glazed ham), Festive Desserts (pumpkin pie, yule log, gingerbread), and Holiday Cocktails. Elegant winter theme with deep greens, gold, and cream colors, snowflake accents, festive but sophisticated typography. Portrait format for table insert.",
    "mode": "max"
  }'
```

## 最佳实践

### 设计原则
- **层次结构**：使用清晰的视觉层次结构，包括章节标题、菜品名称和价格
- **可读性**：确保文本在预期观看距离内可读
- **空白空间**：避免内容过于拥挤，让菜品信息有足够的空间展示
- **一致性**：保持所有章节的设计风格一致
- **品牌匹配**：与餐厅的整体品牌和氛围相协调

### 排版技巧
- **章节标题**：使用装饰性或衬线字体
- **正文**：使用清晰易读的字体来展示菜品描述
- **价格**：统一价格显示方式（右对齐或使用小数点对齐）
- **字号**：菜品名称应比描述文字更大

### 颜色指南
- **高级餐厅**：中性色调，搭配黑色/白色和金色点缀
- **休闲餐厅**：与菜品主题相匹配的温暖、邀请性色彩
- **快餐**：鲜艳、对比度高的颜色（红色、黄色、橙色）
- **咖啡馆**：自然色调、柔和的粉色调
- **酒吧**：深色背景搭配金属质感的装饰元素

### 格式注意事项
- **打印菜单**：高分辨率（300 DPI），使用CMYK色彩模式
- **数字显示屏**：使用RGB色彩，确保高对比度以便清晰显示
- **移动端菜单**：设置较大的点击区域，支持滚动浏览
- **墙壁展示牌**：确保从10英尺外仍可清晰阅读

## 菜单设计提示

在创建菜单设计时，请在提示中包含以下信息：

1. **餐厅类型**：意大利菜、墨西哥菜、日式料理、高级餐厅等
2. **菜单章节**：列出具体的菜系和示例菜品
3. **设计风格**：现代风格、乡村风格、优雅风格、趣味风格或极简风格
4. **色彩搭配**：具体的色彩或整体色调（温暖、冷色调、鲜艳色调）
5. **展示格式**：打印版、数字显示屏、移动端版本，以及具体的尺寸要求
6. **排版风格**：优雅、醒目、手写风格或现代风格
7. **特殊元素**：可使用的装饰元素、照片风格、边框设计

### 示例提示结构

```
"Create a [format] menu design for a [restaurant type].
Include sections for [menu sections with example items].
[Aesthetic style] with [color palette], [typography style].
[Special elements or requirements].
[Dimensions/orientation] for [intended use]."
```

## 模式选择

在生成菜单设计之前，请询问用户：

**“您需要快速且便宜的设计，还是高质量的设计？”**

| 模式 | 适用场景 | 生成速度 | 设计质量 |
|------|----------|-------|---------|
| `max` | 最终打印版菜单、客户演示 | 较慢 | 最高质量 |
| `eco` | 快速草图、概念探索、布局测试 | 较快 | 适合初步设计 |

## 多轮菜单迭代

使用 `session_id` 进行菜单设计的多次迭代：

```bash
# Initial menu design
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a menu design for a modern Asian fusion restaurant with appetizers, mains, and drinks",
    "session_id": "menu-project-001"
  }'

# Iterate based on feedback
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Make the background darker and add more gold accents. Also add a dessert section.",
    "session_id": "menu-project-001"
  }'

# Request format variation
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now create a digital display version of this menu in 16:9 landscape format",
    "session_id": "menu-project-001"
  }'
```

## 菜单集生成

生成一套完整的配套菜单：

```bash
# Main dinner menu
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a dinner menu for an upscale steakhouse with elegant dark theme, gold accents",
    "session_id": "steakhouse-brand"
  }'

# Matching wine menu
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a matching wine list menu in the same style - include Reds, Whites, and Champagne sections",
    "session_id": "steakhouse-brand"
  }'

# Matching dessert menu
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a matching dessert menu in the same brand style",
    "session_id": "steakhouse-brand"
  }'
```

## 错误处理

| 错误类型 | 原因 | 解决方案 |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | 数据不平衡 | 请在 eachlabs.ai 平台上补充数据 |
| 内容违规 | 内容不符合规定 | 调整提示以符合政策要求 |
| 超时 | 生成过程复杂 | 将客户端的超时时间设置为至少10分钟 |

## 相关技能

- `each-sense`：核心API文档
- `product-photo-generation`：用于菜单的食品照片生成服务
- `meta-ad-creative-generation`：餐厅广告创意设计
- `google-ad-creative-generation`：餐厅Google广告创意设计