---
name: interior-design-visualization
description: 使用 each::sense AI 可以可视化室内设计的变更效果。您可以重新设计房间、更换风格、调整配色方案，并根据现有空间的照片预览改造后的效果。
metadata:
  author: eachlabs
  version: "1.0"
---
# 室内设计可视化

使用 `each::sense` 工具对室内空间进行改造和可视化。该工具可以拍摄现有房间的照片，并生成具有不同风格、家具、颜色和布局的重新设计版本。

## 主要功能

- **房间重新设计**：将现有房间改造为全新的设计
- **风格转换**：应用现代、极简、波西米亚、工业等多种风格
- **家具可视化**：查看新家具在您空间中的效果
- **配色方案调整**：预览墙壁、装饰元素和配色的变化
- **厨房翻新**：可视化橱柜、台面和电器的更新
- **浴室改造**：预览瓷砖、梳妆台和卫浴设施的变更
- **办公室设计**：提升工作空间的效率和美观度
- **前后对比**：生成并展示改造前后的对比图

## 快速入门

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Redesign this living room in a modern minimalist style with neutral colors and clean lines",
    "image_urls": ["https://example.com/my-living-room.jpg"],
    "mode": "max"
  }'
```

## 室内设计风格

| 风格 | 特点 | 适合场景 |
|-------|-----------------|----------|
| 现代 | 简洁的线条、中性色调、极简的装饰 | 客厅、办公室 |
| 极简主义 | 家具较少、白色/浅色调、开放式空间 | 任何房间 |
| 斯堪的纳维亚风格 | 浅色木材、白色墙壁、舒适的纺织品 | 卧室、客厅 |
| 工业风格 | 露露的砖墙、金属装饰元素、原始材料 | 阁楼、厨房 |
| 波西米亚风格 | 鲜艳的色彩、图案丰富的装饰 | 卧室、客厅 |
| 中世纪现代风格 | 复古家具、温暖的木质色调、明亮的色彩 | 客厅、办公室 |
| 乡村风格 | 乡村风格的木材、中性色调、复古元素 | 厨房、餐厅 |
| 当代风格 | 当前流行的设计元素、混合材料、精致的设计 | 任何房间 |
| 海岸风格 | 浅蓝色、白色、自然纹理 | 卧室、浴室 |
| 传统风格 | 经典家具、鲜艳的色彩、精美的细节 | 正式场合 |

## 使用案例示例

### 1. 根据照片进行房间重新设计

在保持房间结构不变的情况下，对现有房间进行全面改造。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Completely redesign this room. Keep the same layout but update all furniture, decor, and colors. Make it feel more luxurious and sophisticated with a contemporary style. Include a statement light fixture and add some greenery.",
    "image_urls": ["https://example.com/current-room.jpg"],
    "mode": "max"
  }'
```

### 2. 风格转换（现代风格到极简主义风格）

将一个房间的设计风格从现代风格转换为极简主义风格。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Transform this cluttered traditional living room into a minimalist Japanese-inspired space. Remove excess furniture, use a neutral color palette with whites and light wood tones, add a low platform sofa, and incorporate zen elements like a simple indoor plant and natural light.",
    "image_urls": ["https://example.com/traditional-room.jpg"],
    "mode": "max"
  }'
```

### 家具摆放可视化

查看特定家具在您空间中的摆放效果。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Add furniture to this empty living room: place a large L-shaped sectional sofa in gray fabric facing the window, a round marble coffee table in the center, two accent armchairs in terracotta velvet, a media console against the wall, and a large area rug underneath. Keep the existing flooring and wall color.",
    "image_urls": ["https://example.com/empty-living-room.jpg"],
    "mode": "max"
  }'
```

### 配色方案调整

预览使用不同墙壁颜色和装饰元素后的房间效果。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Change the color scheme of this room. Paint the walls in a deep forest green, update the curtains to cream linen, add gold accent pieces, and change the throw pillows to mustard yellow and cream. Keep all existing furniture but change the soft furnishings.",
    "image_urls": ["https://example.com/beige-room.jpg"],
    "mode": "max"
  }'
```

### 厨房翻新可视化

预览厨房的翻新效果，包括橱柜、台面和电器的更新。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remodel this dated kitchen into a modern farmhouse style. Replace the cabinets with white shaker-style cabinets, add a large kitchen island with a butcher block top, install stainless steel appliances, add subway tile backsplash, change countertops to white quartz, and include open shelving on one wall. Add pendant lights over the island.",
    "image_urls": ["https://example.com/old-kitchen.jpg"],
    "mode": "max"
  }'
```

### 浴室设计更新

通过新的卫浴设施和装饰元素来改变浴室的整体风格。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Transform this outdated bathroom into a spa-like retreat. Replace the vanity with a floating double vanity in walnut wood, add a frameless glass shower enclosure, install large format white marble-look tiles on the walls, add matte black fixtures and hardware, include a freestanding soaking tub if space allows, and add warm LED lighting behind the mirror.",
    "image_urls": ["https://example.com/bathroom-before.jpg"],
    "mode": "max"
  }'
```

### 办公空间设计

创建高效且美观的家庭办公室或商业工作空间设计。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Design this spare bedroom as a professional home office. Add a large L-shaped desk in walnut, an ergonomic mesh office chair, built-in bookshelves on one wall, proper task lighting with a desk lamp and overhead light, some indoor plants for freshness, and a comfortable reading nook by the window. Keep it professional but warm.",
    "image_urls": ["https://example.com/spare-bedroom.jpg"],
    "mode": "max"
  }'
```

### 卧室改造

使用新的家具、纺织品和氛围来改造卧室。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Give this master bedroom a luxury hotel makeover. Add an upholstered king bed with a tall tufted headboard in gray velvet, matching nightstands with elegant table lamps, a bench at the foot of the bed, floor-to-ceiling curtains in a soft white, layered bedding in white and taupe, and a plush area rug. Create a serene and sophisticated atmosphere.",
    "image_urls": ["https://example.com/bedroom-current.jpg"],
    "mode": "max"
  }'
```

### 多种风格选择

利用会话连续性为同一个房间生成多种风格选项。

```bash
# First option - Modern style
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Redesign this living room in a modern contemporary style with clean lines, neutral colors, and sophisticated furniture. Include a sectional sofa, modern coffee table, and contemporary art.",
    "image_urls": ["https://example.com/living-room.jpg"],
    "session_id": "living-room-options-001",
    "mode": "max"
  }'

# Second option - Bohemian style (same session)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now redesign the same living room in a bohemian style. Use rich colors, layered textiles, eclectic furniture, lots of plants, and global-inspired decor. Make it feel cozy and collected.",
    "session_id": "living-room-options-001",
    "mode": "max"
  }'

# Third option - Scandinavian style (same session)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a third option with Scandinavian style. Light wood floors, white walls, minimal furniture in light colors, cozy textiles like sheepskin throws, and plenty of natural light. Keep it simple and hygge.",
    "session_id": "living-room-options-001",
    "mode": "max"
  }'
```

### 前后对比

生成并展示改造前后的对比图。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a dramatic before and after comparison. Take this dated 1990s living room and transform it into a modern 2024 design. Show both versions side by side - the original on the left and the redesigned version on the right. The new design should feature contemporary furniture, updated lighting, modern color palette, and current design trends.",
    "image_urls": ["https://example.com/dated-room.jpg"],
    "mode": "max"
  }'
```

## 最佳实践

### 照片要求
- **良好的照明**：使用光线充足的照片以获得最佳效果
- **清晰的拍摄角度**：广角镜头能更好地展示整个房间
- **减少杂物**：移除临时物品（如衣物或个人物品）
- **多角度拍摄**：对于复杂的项目，提供多个视角的图片

### 提示建议
- **具体说明**：明确指出所需的具体风格、颜色和材料
- **描述房间现状**：说明哪些部分需要保留，哪些部分需要更改
- **包含细节**：提及照明、材质和装饰品
- **设定氛围**：描述您希望营造的氛围（舒适、豪华、明亮）

### 示例提示结构

```
"Transform this [room type] into a [style] design.
[Specific changes for major elements like walls, floors, furniture]
[Color palette preferences]
[Lighting requirements]
[Accessories and decor]
[Overall mood/atmosphere]"
```

## 模式选择

在生成结果之前，请询问用户：

**“您需要快速且低成本的设计，还是高质量的设计？”**

| 模式 | 适合场景 | 速度 | 质量 |
|------|----------|-------|---------|
| `max` | 最终设计展示、客户提案 | 较慢 | 最高质量 |
| `eco` | 快速的概念探索、初步头脑风暴 | 较快 | 一般质量 |

## 多次迭代设计

使用 `session_id` 进行设计的多次迭代：

```bash
# Initial design
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Redesign this bedroom in a modern style with neutral colors",
    "image_urls": ["https://example.com/bedroom.jpg"],
    "session_id": "bedroom-project-001",
    "mode": "max"
  }'

# Refine based on feedback
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "I like it but make the headboard larger and add more warm wood tones. Also add some plants.",
    "session_id": "bedroom-project-001",
    "mode": "max"
  }'

# Final adjustments
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Perfect! Now add some artwork above the bed and change the throw pillows to a dusty rose color.",
    "session_id": "bedroom-project-001",
    "mode": "max"
  }'
```

## 错误处理

| 错误类型 | 原因 | 解决方案 |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | 数据不平衡 | 在 eachlabs.ai 网站充值数据 |
| 内容政策违规 | 内容不符合规定 | 调整提示内容以符合政策要求 |
| 超时 | 生成过程复杂 | 将客户等待时间设置为至少 10 分钟 |
| 图片无法访问 | 图片链接无效或私密 | 使用可公开访问的图片链接 |

## 相关技能

- `each-sense`：核心 API 文档
- `product-photo-generation`：电子商务产品图片生成
- `meta-ad-creative-generation`：社交媒体广告创意设计