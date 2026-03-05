---
name: packaging-design-generation
description: 使用 each::sense AI 生成专业的产品包装设计。可以设计盒子包装、食品包装、化妆品容器、饮料标签、营养补充剂瓶子、咖啡包、蜡烛包装、礼品盒、购物袋以及产品标签。
metadata:
  author: eachlabs
  version: "1.0"
---
# 包装设计生成

使用 `each-sense` 生成专业的产品包装设计。该技能可为各种产品类别（从食品和饮料到化妆品和零售商品）创建高质量的包装原型和设计。

## 特点

- **产品盒设计**：电子产品、玩具、软件及各类产品的包装盒
- **食品包装**：零食、冷冻食品、烘焙食品和餐包
- **化妆品/美容包装**：护肤品、化妆品、护发产品及健康护理产品
- **饮料标签**：葡萄酒、啤酒、果汁、水和软饮料的标签
- **补充剂包装**：维生素、蛋白粉和健康补充品
- **咖啡包设计**：特色咖啡、茶和手工饮料的包装
- **蜡烛包装**：高端蜡烛、家居香氛和礼品套装
- **礼品盒设计**：高端礼品包装和展示盒
- **购物袋**：零售袋、纸袋和品牌手提袋
- **产品标签/贴纸**：定制标签、贴纸和封口设计

## 快速入门

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a premium coffee bag packaging design for an artisan roaster called Mountain Peak Coffee, featuring earthy tones and mountain imagery",
    "mode": "max"
  }'
```

## 包装设计类别

| 类别 | 常见尺寸 | 典型风格 |
|----------|--------------|---------------|
| 产品盒 | 多种尺寸 | 简洁、信息丰富、注重品牌特色 |
| 食品包装 | 标准零售包装 | 诱人、色彩鲜艳、符合法规要求 |
| 化妆品 | 紧凑、时尚 | 优雅、极简、高档 |
| 饮料标签 | 750ml、330ml 等 | 吸引眼球、体现品牌特色 |
| 补充剂 | 瓶装/袋装 | 简洁、可信、注重健康 |
| 咖啡包 | 250g、500g、1kg | 手工制作、突出产品特点、注重材质质感 |
| 蜡烛 | 罐装/盒装 | 舒适、高档、适合赠送 |
| 礼品盒 | 多种尺寸 | 高端、优雅、适合节日场合 |
| 购物袋 | 小/中/大尺寸 | 注重品牌展示、环保材料 |
| 标签/贴纸 | 多种类型 | 用途广泛、信息清晰 |

## 使用案例示例

### 1. 产品盒设计

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a sleek product box design for premium wireless headphones. Modern tech aesthetic with dark matte finish, silver accents, and clean typography. Show the box at a 3/4 angle with the product visible through a window cutout. Brand name: SoundWave Pro.",
    "mode": "max"
  }'
```

### 2. 食品包装设计

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design a vibrant snack packaging for organic veggie chips. Colorful, playful design with hand-drawn vegetable illustrations. Kraft paper bag with a window to show the product. Brand: Crunch Garden. Flavors: Sea Salt & Herb. Include organic certification badge space.",
    "mode": "max"
  }'
```

### 3. 化妆品/美容包装

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create luxury skincare packaging for a serum bottle and box set. Minimalist design with soft pink and rose gold accents. Frosted glass bottle with dropper, matching outer box. Brand: Lumina Beauty. Product: Renewal Face Serum. Elegant serif typography.",
    "mode": "max"
  }'
```

### 4. 饮料标签设计

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design a craft beer label for an IPA. Vintage-inspired with modern twist, featuring hop illustrations and mountain scenery. Deep green and gold color palette. Brewery name: Summit Brewing Co. Beer name: Trail Blazer IPA. Include ABV space and tasting notes area.",
    "mode": "max"
  }'
```

### 5. 补充剂/维生素包装

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a clean, trustworthy supplement bottle design for daily multivitamins. White bottle with blue and green accents suggesting health and vitality. Modern sans-serif typography. Brand: VitaCore. Product: Complete Daily Multivitamin. Show front label with dosage info area.",
    "mode": "max"
  }'
```

### 6. 咖啡包设计

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design an artisan coffee bag for single-origin Ethiopian beans. Kraft paper bag with matte black label. Featuring Ethiopian landscape illustration in warm earth tones. Brand: Origin Story Coffee. Include space for roast date, flavor notes (blueberry, citrus, chocolate), and brewing recommendations.",
    "mode": "max"
  }'
```

### 7. 蜡烛包装

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create luxury candle packaging for a home fragrance brand. Amber glass jar with minimalist white label, housed in a elegant black box with gold foil details. Brand: Maison Lumiere. Scent: Fireside & Vanilla. Cozy, sophisticated aesthetic suitable for gifting.",
    "mode": "max"
  }'
```

### 8. 礼品盒设计

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design a premium gift box for a chocolate assortment. Rich burgundy exterior with embossed gold pattern, satin ribbon closure. Interior with velvet-textured compartments visible. Brand: Artisan Chocolatier. Luxurious, festive design suitable for holidays and special occasions.",
    "mode": "max"
  }'
```

### 9. 购物袋设计

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a retail shopping bag design for a boutique fashion store. Thick paper bag with rope handles. Minimalist design with large logo placement, matte white with black typography. Brand: Atelier Mode. Sustainable, premium feel that customers would reuse.",
    "mode": "max"
  }'
```

### 10. 产品标签/贴纸设计

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design a product label for artisan honey jars. Circular label with honeycomb pattern border, featuring bee illustration. Warm amber and golden tones. Brand: Wild Meadow Apiary. Include space for honey type, weight, and harvest date. Rustic yet refined aesthetic.",
    "mode": "max"
  }'
```

## 最佳实践

### 设计元素
- **品牌一致性**：在整个包装中保持标志的位置、颜色调和排版的一致性
- **层次结构**：明确品牌名称、产品名称和关键信息的视觉层次
- **空白空间**：有效利用空白空间，营造高端感
- **材料选择**：考虑设计在不同材料（哑光、光泽、牛皮纸、金属材质）上的呈现效果

### 技术注意事项
- **出血区域**：在设计请求中考虑印刷时的出血问题
- **模切窗口**：指定产品是否需要透过包装显示
- **结构设计**：描述盒子/容器的形状和尺寸
- **印刷效果**：说明所需的印刷效果（箔压、浮雕、局部UV处理）

### 行业标准
- **食品包装**：需包含营养成分表、成分列表和过敏原信息
- **化妆品**：需规划成分列表、使用说明和警告信息
- **饮料**：考虑瓶子的形状和标签的包裹方式
- **补充剂**：需包含补充剂信息栏和FDA免责声明区域

## 包装设计提示

在创建包装设计时，请在提示中包含以下细节：

1. **产品类型**：所包装的产品类型（食品、化妆品、科技产品等）
2. **品牌名称**：需要突出的品牌标识
3. **产品名称**：具体产品或变体的名称
4. **设计风格**：极简、高档、趣味性、复古、现代等
5. **颜色搭配**：具体的颜色或整体色调（自然色调、鲜艳色调、单色系）
6. **材料选择**：牛皮纸、玻璃、哑光纸板、金属装饰
7. **展示角度**：正面视图、3/4 角度、平铺展示或原型图样式
8. **特殊元素**：透明窗口、箔压、浮雕、丝带等装饰

### 示例提示结构

```
"Create a [style] packaging design for [product type].
[Material/container type] with [color palette] colors.
Brand: [name]. Product: [name].
[Special features like windows, finishes, or structural details].
[View angle and presentation style]."
```

## 模式选择

在生成设计之前，请询问用户：

**“您需要快速且低成本的设计，还是高质量的设计？”**

| 模式 | 适用场景 | 速度 | 设计质量 |
|------|----------|-------|---------|
| `max` | 最终包装设计、客户演示、可打印的概念 | 较慢 | 最高等 |
| `eco` | 快速草图、概念探索、初步构思 | 较快 | 一般 |

## 多轮创意迭代

使用 `session_id` 进行包装设计的迭代：

```bash
# Initial design concept
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a protein powder packaging design, modern fitness aesthetic, bold typography",
    "session_id": "protein-packaging-001"
  }'

# Iterate based on feedback
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Make it more premium looking with matte black finish and gold accents. Add a resealable pouch mockup.",
    "session_id": "protein-packaging-001"
  }'

# Request variations
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create 2 flavor variants: Chocolate and Vanilla, keeping the same design language",
    "session_id": "protein-packaging-001"
  }'
```

## 产品线一致性

为不同产品变体生成统一的包装设计：

```bash
# First product in line
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create skincare packaging for a cleanser. Minimalist white with sage green accents. Brand: Pure Botanics. Establish the design system for the entire product line.",
    "session_id": "pure-botanics-line"
  }'

# Second product (same session for consistency)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now create the toner packaging in the same design language. Same brand identity but different bottle shape.",
    "session_id": "pure-botanics-line"
  }'

# Third product
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create the moisturizer jar packaging. Continue the Pure Botanics design system with consistent typography and color palette.",
    "session_id": "pure-botanics-line"
  }'
```

## 错误处理

| 错误 | 原因 | 解决方案 |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | 数据不平衡 | 在 eachlabs.ai 网站补充数据 |
| 内容政策违规 | 包含禁止的内容 | 调整提示以符合内容政策 |
| 超时 | 设计生成过程复杂 | 将客户超时时间设置为至少10分钟 |

## 相关技能

- `each-sense` - 核心 API 文档
- `product-photo-generation` - 电子商务产品图片生成
- `meta-ad-creative-generation` - 社交媒体广告创意生成
- `google-ad-creative-generation` - Google 广告创意生成