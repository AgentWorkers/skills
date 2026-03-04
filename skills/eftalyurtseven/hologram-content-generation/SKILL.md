---
name: hologram-content-generation
description: 使用 each::sense AI 生成全息图和 3D 显示内容。可以用于创建全息产品展示、演示工具、3D 标志、交互式菜单、活动展示、博物馆展品、零售展示以及贸易展览中的全息效果。
metadata:
  author: eachlabs
  version: "1.0"
---
# 全息内容生成

使用 `each-sense` 功能生成令人惊叹的全息图和 3D 显示内容。该技能可创建专为全息显示器、3D 全息风扇、LED 金字塔及其他立体显示技术优化的图像和视频。

## 主要功能

- **产品全息图**：用于零售和展厅的悬浮式 3D 产品可视化效果
- **全息演示者**：虚拟代言人和品牌大使
- **3D 标志动画**：适用于全息显示的动态品牌标志
- **交互式菜单**：全息界面和菜单系统
- **活动全息图**：适用于音乐会、会议和发布会的舞台内容
- **博物馆展览**：用于展览的教育性全息内容
- **零售展示**：吸引眼球的全息广告
- **贸易展会内容**：吸引观众注意力的展位全息图
- **全息问候**：个性化的 3D 消息和邀请函
- **交互式设计**：支持触摸响应的全息界面

## 快速入门

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a holographic product display showing a luxury watch floating and slowly rotating with particle effects and blue glow",
    "mode": "max"
  }'
```

## 全息显示格式

| 显示类型 | 长宽比 | 推荐格式 | 适用场景 |
|--------------|--------------|-------------|----------|
| 全息风扇 | 1:1 | 1080x1080 | 零售、活动、贸易展会 |
| LED 金字塔 | 1:1 | 1080x1080 | 产品展示、博物馆 |
| Pepper’s Ghost | 16:9 | 1920x1080 | 舞台表演、大型活动 |
| 全息盒子 | 1:1 | 1080x1080 | 小型产品展示 |
| 立体显示器 | 1:1 | 1080x1080 | 高端安装 |
| 透明 OLED | 16:9 | 1920x1080 | 零售橱窗、展览 |

## 适用场景示例

### 1. 全息产品展示

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a holographic product display for a premium perfume bottle. The bottle should float in the center, slowly rotating with a magical mist swirling around it. Add sparkle particles and a soft pink/purple glow. Black background for hologram fan display. 1:1 aspect ratio, 5 second loop.",
    "mode": "max"
  }'
```

### 2. 全息演示者/代言人

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a holographic presenter - a professional woman in business attire appearing as a blue-tinted hologram. She should be gesturing welcomingly as if greeting visitors. Add scan lines and digital glitch effects for authentic hologram look. Full body shot, black background, 16:9 aspect ratio.",
    "mode": "max"
  }'
```

### 3. 3D 标志动画

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 3D holographic logo animation. A futuristic tech company logo (abstract geometric shape) assembles from floating particles, rotates to reveal depth, then pulses with energy. Cyan and white color scheme with electric effects. Black background, 1:1 square format, 6 second seamless loop.",
    "mode": "max"
  }'
```

### 4. 全息菜单/界面

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a holographic menu interface for a futuristic restaurant. Floating translucent panels showing food items with 3D dish previews. Sci-fi UI design with glowing borders, subtle animations. Blue and orange accent colors on dark background. 16:9 aspect ratio, interactive feel.",
    "mode": "max"
  }'
```

### 5. 活动全息图内容

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create holographic stage content for a product launch event. A smartphone emerging from an explosion of light particles, floating and rotating to show all angles. Dynamic camera movement, epic reveal moment with lens flares and energy waves. 16:9 cinematic format, 10 seconds.",
    "mode": "max"
  }'
```

### 6. 博物馆/展览全息图

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a holographic museum exhibit showing a dinosaur (T-Rex) in educational display format. The dinosaur should appear as a detailed 3D hologram, slowly rotating with anatomical labels floating around it. Scientific visualization style with blue holographic effect. Black background, 1:1 format, 8 second loop.",
    "mode": "max"
  }'
```

### 7. 零售全息展示

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a retail holographic display for sneakers. The shoe floats and rotates showing all angles, with dynamic lighting highlighting materials and details. Add speed lines and energy effects suggesting performance. Price tag holographically appears. Attention-grabbing for store window. 1:1 square, 5 second loop.",
    "mode": "max"
  }'
```

### 8. 贸易展会全息图

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an attention-grabbing trade show booth hologram. A futuristic robot mascot waving and beckoning visitors, surrounded by floating company info graphics and product highlights. High energy, playful but professional. Include particle effects and holographic glitches. 1:1 format, 10 second loop.",
    "mode": "max"
  }'
```

### 9. 全息问候

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a holographic birthday greeting. A magical 3D birthday cake with floating candles, sparkles swirling around it, and the text HAPPY BIRTHDAY appearing in glowing 3D letters above. Warm golden and pink colors with festive particle effects. Black background, 1:1 square format, 6 seconds.",
    "mode": "max"
  }'
```

### 10. 交互式全息设计

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an interactive holographic globe interface. A 3D Earth slowly rotating with data points lighting up across continents, connection lines between cities, and floating info panels that appear. Sci-fi command center aesthetic. Blue and cyan tones on black background. 1:1 format, 8 second loop.",
    "mode": "max"
  }'
```

## 最佳实践

### 全息设计原则
- **黑色背景**：对于全息风扇和大多数显示类型来说至关重要——内容会显得像是在悬浮
- **高对比度**：在深色背景上使用明亮、发光的元素
- **居中显示**：确保主要内容在 3D 全息风扇显示屏上居中
- **流畅的动作**：避免突然的移动——平滑的旋转和过渡效果最佳
- **无缝循环**：创建能够连续播放的内容

### 为增强真实感而设计的视觉效果
- **扫描线**：水平线条可营造复古未来感
- **故障效果**：微妙的数字伪影可提升真实感
- **粒子效果**：漂浮的粒子可增加深度和神秘感
- **光晕/模糊效果**：元素周围的柔和光晕可增强 3D 效果
- **透明度**：半透明元素更具全息感

### 颜色选择
- **青色/蓝色**：经典的全息颜色，具有高科技感
- **白色/银色**：干净、高端的外观
- **紫色/粉色**：适合娱乐场景
- **绿色**：适合数据可视化的矩阵风格
- **橙色/金色**：适合温暖、豪华的产品

### 技术要求
- **帧率**：至少 30fps，旋转效果需要 60fps
- **分辨率**：与显示设备匹配——通常为 1080x1080
- **时长**：循环内容建议 5-15 秒，叙事内容可适当延长
- **文件格式**：使用 H.264/H.265 编解码器的 MP4 格式

## 创建全息内容的提示

在创建全息内容时，请包含以下信息：
- **显示类型**：指定是全息风扇、金字塔还是其他类型
- **长宽比**：全息风扇和金字塔使用 1:1，舞台使用 16:9
- **展示内容**：需要展示的产品、人物或标志
- **动作效果**：旋转、悬浮、组合动画等
- **视觉效果**：粒子效果、光晕、扫描线、故障效果等
- **颜色方案**：指定全息图的颜色
- **背景**：为了正确的显示效果，通常应使用黑色
- **时长**：循环时长及是否需要无缝循环

### 示例提示结构

```
"Create a holographic [content type] for [display type].
Show [subject] with [motion/animation].
Add [effects] with [color scheme].
Black background, [aspect ratio] format, [duration] second loop."
```

## 模式选择

在生成内容之前，请询问用户：

**“您需要快速草图还是高质量成品？”**

| 模式 | 适用场景 | 速度 | 质量 |
|------|----------|-------|---------|
| `max` | 最终成品、客户交付物 | 较慢 | 最高质量 |
| `eco` | 快速概念、迭代、测试想法 | 较快 | 良好质量 |

## 多轮创意迭代

使用 `session_id` 进行全息内容的迭代：

```bash
# Initial concept
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a holographic car display for an auto showroom, the car floating and rotating",
    "session_id": "car-hologram-001"
  }'

# Refine based on feedback
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Make it more dramatic - add energy lines tracing the car body, and have parts explode outward to show the engine",
    "session_id": "car-hologram-001"
  }'

# Request variations
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a version with different color scheme - red and orange energy effects instead of blue",
    "session_id": "car-hologram-001"
  }'
```

## 行业应用

### 零售与电子商务
- 店内产品展示
- 橱窗展示
- 产品发布会

### 活动与娱乐
- 音乐会视觉效果
- 会议舞台
- 颁奖典礼
- 主题公园景点

### 博物馆与教育
- 历史场景再现
- 科学可视化展示
- 互动展览
- 游客信息展示

### 企业与营销
- 大厅展示
- 贸易展会展位
- 品牌互动活动
- 高管演示

### 酒店与服务业
- 餐厅菜单
- 酒店礼宾服务
- 导航系统
- 娱乐场所

## 错误处理

| 错误类型 | 原因 | 解决方案 |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | 资源不足 | 请在 eachlabs.ai 网站充值 |
| 内容违规 | 内容不符合政策 | 调整提示以符合内容政策 |
| 超时 | 生成过程复杂 | 将客户等待时间设置为至少 10 分钟 |

## 相关技能

- `each-sense`：核心 API 文档
- `product-photo-generation`：产品摄影
- `video-generation`：通用视频内容生成
- `3d-animation`：3D 动画制作