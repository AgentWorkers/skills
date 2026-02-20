---
name: ar-filter-generation
description: 使用 each::sense AI 生成 AR 过滤器和面部效果。为社交媒体平台创建面部滤镜、美妆效果、化妆叠加层、品牌化的 AR 体验以及 3D 面部追踪效果。
metadata:
  author: eachlabs
  version: "1.0"
---
# AR滤镜生成

使用`each::sense`功能生成创意十足的AR滤镜和面部效果。该技能可用于创建适用于Instagram、Snapchat和TikTok等平台的AR滤镜、面部追踪效果以及社交媒体滤镜。

## 主要功能

- **面部滤镜**：动物耳朵、鼻子、胡须等面部元素，以及角色叠加效果
- **美容滤镜**：皮肤平滑、轮廓修饰和美化效果
- **化妆AR效果**：虚拟口红、眼影、腮红等完整妆容效果
- **配饰滤镜**：太阳镜、帽子、珠宝等可穿戴装饰元素
- **背景效果**：背景替换和模糊处理
- **面部扭曲效果**：有趣的面部变形效果
- **品牌滤镜**：品牌标志叠加和促销性AR体验
- **3D面部追踪**：能够跟随面部动作移动的3D元素

## 快速入门

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an AR filter concept showing a person with cute dog ears and a dog nose overlay, playful and fun style",
    "mode": "max"
  }'
```

## AR滤镜类型及应用场景

| 滤镜类型 | 描述 | 应用平台 |
|-------------|-------------|--------------|
| 面部滤镜 | 动物耳朵、角色面具 | Instagram、Snapchat、TikTok |
| 美容滤镜 | 皮肤美化、面部轮廓调整 | 所有平台 |
| 化妆滤镜 | 虚拟化妆品效果 | 美妆品牌、影响者 |
| 配饰滤镜 | 太阳镜、帽子、珠宝 | 时尚、零售 |
| 背景滤镜 | 背景替换效果 | 视频通话、内容创作 |
| 面部扭曲滤镜 | 有趣的面部变形效果 | 娱乐、病毒式内容 |
| 品牌滤镜 | 品牌标志叠加、促销活动 | 营销活动 |
| 3D滤镜 | 跟随面部动作移动的3D元素 | 游戏、娱乐 |

## 应用场景示例

### 1. 面部滤镜设计（动物耳朵和鼻子）

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an AR filter concept showing a young woman with realistic fluffy golden retriever dog ears on top of her head and a cute black dog nose overlay on her nose. Add subtle whisker dots on cheeks. The filter should look natural and integrate well with the face. Show front-facing selfie view.",
    "mode": "max"
  }'
```

### 2. 美容滤镜效果

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a beauty AR filter effect showing before and after comparison. Show a person with the beauty filter applied: smooth skin, subtle face slimming, brightened eyes, soft glow effect, and enhanced jawline definition. Natural-looking enhancement, not overdone. Professional beauty app style.",
    "mode": "max"
  }'
```

### 3. 化妆AR滤镜

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a virtual makeup AR filter concept. Show a woman with AR-applied makeup: bold red lipstick, smoky eye shadow in bronze and gold tones, defined eyebrows, subtle blush, and winged eyeliner. The makeup should look realistic as if professionally applied. Glamorous evening look. Front-facing portrait.",
    "mode": "max"
  }'
```

### 4. 太阳镜和配饰滤镜

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an AR try-on filter showing a person wearing virtual aviator sunglasses with gold frames and gradient lenses. Add a matching gold chain necklace and small hoop earrings. The accessories should look photorealistic and properly positioned on the face. Fashion e-commerce style visualization.",
    "mode": "max"
  }'
```

### 5. 背景替换滤镜

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an AR background replacement filter concept. Show a person in selfie view with their original background replaced by a tropical beach paradise - palm trees, turquoise water, golden sand, sunset sky. Clean edge detection around the person, natural lighting blend between subject and background.",
    "mode": "max"
  }'
```

### 6. 面部扭曲/搞笑滤镜

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a funny face distortion AR filter. Show a person with comically enlarged eyes (anime style big), tiny mouth, and slightly enlarged forehead. Add sparkles around the eyes and a rainbow effect. Cute and comedic style like popular Snapchat filters. Exaggerated but still recognizable.",
    "mode": "max"
  }'
```

### 7. 品牌AR滤镜（品牌标志叠加）

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a branded AR filter concept for a sports event. Show a person with face paint in team colors (blue and white stripes on cheeks), a virtual foam finger appearing next to their head, confetti particles falling, and a banner frame around the image that says GO TEAM. Celebratory sports fan atmosphere.",
    "mode": "max"
  }'
```

### 8. 节日主题滤镜

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a Christmas holiday AR filter. Show a person wearing a virtual Santa hat, with a red Rudolph nose overlay, snowflakes falling around them, and a subtle frost effect on the edges of the frame. Add twinkling lights in the background. Festive and cheerful holiday spirit.",
    "mode": "max"
  }'
```

### 9. 游戏风格滤镜（例如《Among Us》）

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a gaming-inspired AR filter in the style of Among Us. Transform the person into a crewmate character - their face visible through a space helmet visor, wearing the iconic colored spacesuit (red), with a small pet companion floating nearby. Add a spaceship interior background. Fun and recognizable gaming aesthetic.",
    "mode": "max"
  }'
```

### 10. 3D对象追踪滤镜

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 3D face tracking AR filter concept. Show a person with a 3D floating crown hovering above their head that follows head movement, 3D butterflies orbiting around them, and magical sparkle particles emanating from their eyes. The 3D elements should have realistic lighting and shadows. Fantasy magical theme.",
    "mode": "max"
  }'
```

## 最佳实践

### 面部滤镜设计
- **自然融合**：滤镜元素应与面部特征完美融合
- **正确的追踪点**：根据标准面部标志（眼睛、鼻子、嘴巴、额头）进行设计
- **光照一致性**：确保滤镜的光照效果与自拍时的光照条件相匹配
- **元素比例**：确保滤镜元素与面部大小成比例

### 平台注意事项
- **Instagram/TikTok**：采用9:16的竖屏格式，以移动设备优先进行设计
- **Snapchat**：考虑镜头的拍摄限制和功能特点
- **视频通话**：使用在低分辨率下也能正常显示的柔和效果

### 性能优化建议
- **简洁性**：元素越少，实时性能越好
- **透明度**：正确使用alpha通道来处理叠加效果
- **动画效果**：考虑静态设计如何转化为动态滤镜效果

## 模式选择

在生成滤镜之前，请询问用户：
**“您需要快速且低成本的滤镜，还是高质量的滤镜？”**

| 模式 | 适用场景 | 速度 | 质量 |
|------|----------|-------|---------|
| `max` | 最终滤镜效果、客户演示、作品集展示 | 较慢 | 最高质量 |
| `eco` | 快速草图、概念探索、创意构思 | 较快 | 良好质量 |

## 多轮创意迭代

使用`session_id`进行滤镜设计的多次迭代：

```bash
# Initial filter concept
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a cat face AR filter with whiskers and cat ears",
    "session_id": "cat-filter-project"
  }'

# Iterate based on feedback
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Make the ears more realistic and fluffy, add a pink nose, and include subtle face contouring to make cheeks more cat-like",
    "session_id": "cat-filter-project"
  }'

# Request variation
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a variation with black cat features instead of tabby, and add glowing yellow eyes effect",
    "session_id": "cat-filter-project"
  }'
```

## 滤镜集合生成

为某个营销活动生成多个相关的滤镜：

```bash
# Filter 1 - Dog
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an AR filter with golden retriever dog ears and nose, cute and playful",
    "mode": "eco",
    "session_id": "animal-filter-pack"
  }'

# Filter 2 - Cat
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now create a matching cat filter with the same style - tabby cat ears and whiskers",
    "mode": "eco",
    "session_id": "animal-filter-pack"
  }'

# Filter 3 - Bunny
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Complete the pack with a bunny filter - long floppy ears and a pink bunny nose",
    "mode": "eco",
    "session_id": "animal-filter-pack"
  }'
```

## 错误处理

| 错误类型 | 原因 | 解决方案 |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | 数据平衡不足 | 请在eachlabs.ai平台上补充数据 |
| 内容违规 | 内容不符合平台规定 | 调整提示以符合平台要求 |
| 超时 | 生成过程复杂 | 将客户端的超时时间设置为至少10分钟 |

## AR滤镜提示技巧

在创建AR滤镜概念时，请在提示中包含以下信息：
1. **滤镜类型**：明确滤镜的类别（面部滤镜、美容滤镜、化妆滤镜等）
2. **所需元素**：列出所有需要的叠加元素（耳朵、鼻子、配饰等）
3. **风格**：选择现实主义、卡通风格、极简风格或复杂风格
4. **元素位置**：指定元素在面部特征上的显示位置
5. **效果类型**：如颗粒效果、光晕效果、色彩渐变、面部扭曲等
6. **目标平台**：如果有特定平台要求，请明确说明
7. **情感氛围**：选择轻松、华丽、恐怖、节日主题等

### 示例提示结构

```
"Create a [filter type] AR filter showing [subject description].
Include [overlay elements] with [style/aesthetic].
Add [effects/particles] and [additional features].
[Platform/mood requirements]."
```

## 相关技能

- `each-sense`：核心API文档
- `product-photo-generation`：产品可视化工具
- `video-generation`：视频内容生成工具
- `image-generation`：通用图像生成工具