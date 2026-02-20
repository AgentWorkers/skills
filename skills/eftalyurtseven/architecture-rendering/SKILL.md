---
name: architecture-rendering
description: 使用 each::sense AI 生成逼真的建筑渲染图和可视化效果。可为建筑师、设计师和房地产专业人士提供室外视图、室内渲染图、从草图到渲染图的转换服务等。
metadata:
  author: eachlabs
  version: "1.0"
---
# 建筑渲染

使用 `each-sense` 功能生成令人惊叹的建筑可视化效果。该技能能够根据草图、平面图和文字描述，为建筑师、室内设计师、房地产开发商和可视化工作室创建逼真的渲染图像。

## 主要功能

- **建筑外观渲染**：包含景观和背景信息的建筑外观图像
- **室内空间可视化**：包含家具、照明和材质的详细室内场景
- **草图到渲染**：将手绘草图转换为逼真图像
- **航拍视图**：鸟瞰图和无人机拍摄风格的图像
- **夜间场景**：带有人工照明的戏剧性夜间渲染效果
- **施工进度可视化**：施工过程中的渲染图像和分阶段开发视图
- **历史建筑修复**：修复后的历史建筑的可视化效果
- **景观建筑设计**：花园、公园和户外空间的可视化

## 快速入门

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a photorealistic exterior render of a modern minimalist house with floor-to-ceiling glass windows, white concrete walls, flat roof, surrounded by a manicured garden with a pool",
    "mode": "max"
  }'
```

## 常见渲染类型及规格

| 渲染类型 | 典型宽高比 | 适用场景 |
|-------------|---------------------|----------|
| 外观全景图 | 16:9 | 营销、演示文稿 |
| 室内房间视图 | 4:3 或 16:9 | 室内设计提案 |
| 航拍/鸟瞰图 | 16:9 或 1:1 | 场地规划、总体规划 |
| 垂直立面图 | 9:16 或 3:4 | 社交媒体、高层建筑 |
| 施工进度图 | 16:9 | 客户更新、文档记录 |

## 使用案例示例

### 1. 建筑外观渲染

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a photorealistic exterior render of a contemporary three-story residential building. Features: exposed concrete and timber cladding, large balconies with glass railings, green roof terrace, floor-to-ceiling windows. Environment: urban street setting, mature trees, late afternoon golden hour lighting, slight overcast for soft shadows. Professional architectural photography style.",
    "mode": "max"
  }'
```

### 2. 室内建筑渲染

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a photorealistic interior render of a luxury open-plan living room. Features: double-height ceiling with exposed wooden beams, polished concrete floors, a large sectional sofa in cream fabric, floor-to-ceiling windows overlooking mountains, modern fireplace with black steel surround, pendant lighting fixtures. Style: Scandinavian minimalism meets industrial. Warm natural daylight flooding through windows.",
    "mode": "max"
  }'
```

### 3. 草图到渲染的转换

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Convert this architectural sketch into a photorealistic render. Interpret it as a modern office building with glass curtain wall facade, steel structural elements visible, rooftop garden. Add realistic context: urban setting, pedestrians, cars, trees. Professional architectural visualization quality, sunny day with blue sky and some clouds.",
    "mode": "max",
    "image_urls": ["https://example.com/architecture-sketch.jpg"]
  }'
```

### 4. 现代住宅可视化

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a photorealistic render of a modern single-family home. Architecture: two-story with cantilevered upper floor, white stucco exterior, dark bronze window frames, integrated garage, flat roof with hidden parapets. Landscaping: drought-tolerant native plants, gravel pathways, specimen olive tree. Setting: hillside lot with city views in background. Time: dusk with interior lights glowing warmly, exterior accent lighting.",
    "mode": "max"
  }'
```

### 5. 商业建筑渲染

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a professional architectural visualization of a 20-story commercial office tower. Design: curtain wall glass facade with vertical aluminum fins for solar shading, ground floor retail with double-height lobby, green terraces every 5 floors, rooftop helipad. Context: downtown business district, plaza with water feature at entrance, people walking. Lighting: midday sun, crisp shadows, reflections in glass.",
    "mode": "max"
  }'
```

### 6. 景观建筑设计可视化

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Render a landscape architecture design for a public urban park. Features: meandering pedestrian paths with permeable pavers, native wildflower meadows, a central pond with wooden deck overlook, children playground with natural materials, seating areas with shade structures, mature deciduous and evergreen trees. Include families enjoying the space, joggers, people walking dogs. Spring season, sunny day, vibrant green foliage.",
    "mode": "max"
  }'
```

### 7. 夜间场景渲染

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a dramatic nighttime architectural render of a luxury boutique hotel entrance. Building: Art Deco revival style with geometric patterns, brass detailing, black granite facade. Lighting: warm interior glow through large windows, facade uplighting highlighting architectural details, subtle landscape lighting, illuminated hotel sign. Scene: valet area with luxury car, doorman, guests arriving. Atmosphere: sophisticated, inviting, slight wet pavement reflections from recent rain.",
    "mode": "max"
  }'
```

### 8. 航拍/鸟瞰图

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate an aerial architectural render of a mixed-use development masterplan. Layout: central public plaza, surrounding mid-rise residential buildings (6-8 stories), ground floor retail, underground parking entrances, community center with distinctive curved roof. Include: rooftop gardens, tree-lined streets, pedestrian promenades, outdoor dining areas. View: 45-degree angle bird's eye perspective, showing the full development and neighborhood context. Clear day, afternoon light.",
    "mode": "max"
  }'
```

### 9. 施工进度可视化

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a construction progress visualization showing a residential tower at 60% completion. Show: concrete core structure complete, lower floors with installed curtain wall glazing, upper floors with exposed steel framing and temporary weather protection, tower crane active, construction workers on scaffolding (safe distances), ground level site office and material staging. Style: documentary realism, overcast day for even lighting, professional construction photography look.",
    "mode": "max"
  }'
```

### 10. 历史建筑修复渲染

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Visualize a restored Victorian-era mansion. Architecture: three-story red brick with ornate white trim, wraparound porch with turned columns, steep gabled roof with decorative shingles, restored original windows with period-appropriate shutters, chimney stacks. Grounds: formal English garden with boxwood hedges, gravel carriage drive, restored iron fence and gate. Show both the historical authenticity and modern updates like subtle landscape lighting. Golden hour lighting, autumn foliage.",
    "mode": "max"
  }'
```

## 最佳实践

### 渲染质量建议

- **照明**：指定时间点和天气条件，以获得合适的阴影和氛围
- **材质**：明确描述材质（抛光混凝土、拉丝钢、哑光木材）
- **背景环境**：包含周围环境（街道、植被、人物）以增强真实感
- **比例参考**：添加人物、车辆或家具以体现比例感
- **拍摄角度**：指定拍摄视角（平视、低角度、鸟瞰）

### 建筑渲染提示结构

在创建建筑渲染时，请包含以下要素：

1. **建筑类型**：住宅、商业、机构、混合用途
2. **建筑风格**：现代、当代、传统、工业风格
3. **关键特征**：使用的材料、立面元素、结构系统
4. **环境**：城市、郊区、乡村、滨水地区
5. **时间和天气**：黄金时刻、正午、黄昏、夜晚；晴天、阴天、戏剧性场景
6. **拍摄角度**：平视、航拍、俯视、四分之三视角
7. **背景元素**：人物、车辆、景观、邻近建筑

### 示例提示模板

```
"Create a photorealistic [view type] render of a [building type].
Architecture: [style], [key features], [materials].
Environment: [setting], [landscaping].
Lighting: [time of day], [weather conditions].
Include: [context elements like people, cars, etc.]
Style: [professional architectural visualization / specific mood]."
```

## 模式选择

在生成渲染之前，请询问用户：

**“您需要快速草图还是最终展示质量的渲染？”**

| 模式 | 适用场景 | 速度 | 质量 |
|------|----------|-------|---------|
| `max` | 最终展示、客户交付物、营销材料 | 较慢 | 最高质量 |
| `eco` | 快速概念探索、早期设计迭代、初步方案 | 较快 | 良好质量 |

## 多轮设计迭代

使用 `session_id` 进行建筑渲染的多次迭代：

```bash
# Initial concept render
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an exterior render of a modern beach house with large glass walls and a wooden deck",
    "session_id": "beach-house-project",
    "mode": "eco"
  }'

# Design revision
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Add a rooftop terrace with a pergola and outdoor kitchen. Make the facade more tropical with natural stone accents.",
    "session_id": "beach-house-project"
  }'

# Time of day variation
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a sunset version of this design with warm lighting and the interior lights starting to glow",
    "session_id": "beach-house-project",
    "mode": "max"
  }'
```

## 整套渲染生成

为项目生成一套完整的渲染图像：

```bash
# Hero exterior shot
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create the main exterior hero shot of our modern villa project - front facade, golden hour, dramatic angle",
    "session_id": "villa-presentation",
    "mode": "max"
  }'

# Interior living space
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now create an interior render of the main living area - open plan, same modern style, afternoon light",
    "session_id": "villa-presentation",
    "mode": "max"
  }'

# Aerial site view
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate an aerial view showing the villa in its landscape context - pool, garden, and property boundaries",
    "session_id": "villa-presentation",
    "mode": "max"
  }'
```

## 错误处理

| 错误类型 | 原因 | 解决方案 |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | 数据不足 | 在 eachlabs.ai 网站补充数据 |
| 内容政策违规 | 内容被禁止 | 调整提示内容以符合政策要求 |
| 超时 | 生成过程复杂 | 将客户等待时间设置为至少 10 分钟 |
| 输出质量低 | 提示中缺乏详细信息 | 增加具体的建筑细节、材质和照明信息 |

## 相关技能

- `each-sense`：核心 API 文档
- `product-photo-generation`：产品可视化工具
- `interior-design-generation`：专注于室内设计的工具