---
name: image-relighting
description: 使用 each::sense AI 重新调整照片和图像的灯光效果。您可以改变光照条件、添加摄影棚灯光效果、金色时刻（golden hour）的光影效果、戏剧性的阴影效果以及霓虹灯般的发光效果，并使灯光效果与任何环境相匹配。
metadata:
  author: eachlabs
  version: "1.0"
---
# 图像重新布光

使用 `each::sense` 工具来调整照片中的光线效果。该功能允许您改变光线条件、添加专业的摄影棚布光效果、创造戏剧性的视觉效果，或将照片的光线与新的背景相匹配——同时保留原始的主体图像。

## 主要功能

- **专业摄影棚布光**：提供三点布光、伦勃朗布光、蝴蝶布光和分割布光等专业布光方案
- **自然光效果**：模拟黄金时刻、蓝调时刻、阴天或窗光等自然光线效果
- **戏剧性效果**：生成强烈的阴影、边缘光、剪影效果及明暗对比强烈的画面
- **创意布光**：运用霓虹灯、彩色滤镜、迪斯科灯光等创意光源
- **环形灯**：生成适合美妆或人像拍摄的环形光源效果
- **电影级布光**：模拟黑色电影或大片中的氛围感
- **阴影控制**：去除刺眼的阴影、柔和现有光线、填补暗部区域
- **环境匹配**：调整主体图像的光线以适应新的背景或场景

## 快速入门

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Add professional studio lighting to this portrait - soft key light from the left with subtle fill",
    "image_urls": ["https://example.com/portrait.jpg"],
    "mode": "max"
  }'
```

## 布光类型参考

| 布光风格 | 描述 | 适用场景 |
|---------|---------|---------|
| 三点布光 | 包括主光、补光和背光 | 专业人像摄影 |
| 伦勃朗布光 | 面颊处形成三角形光影 | 戏剧性人像摄影 |
| 蝴蝶布光 | 从上方照射光线，鼻子下方形成阴影 | 美妆或 glamour 摄影 |
| 分割布光 | 一半脸部被照亮，另一半处于阴影中 | 戏剧性或艺术性摄影 |
- 环形灯 | 均匀无阴影的前置光源 | 美妆或社交媒体摄影 |
- 金色时刻布光 | 温暖、柔和的方向性光线 | 户外人像或生活方式摄影 |
- 蓝调时刻布光 | 凉爽、柔和的环境光 | 悲伤或氛围感强的场景 |
- 窗光布光 | 柔和的方向性自然光 | 自然人像摄影 |
- 霓虹灯/彩色灯光 | 鲜艳的彩色光源 | 创意或编辑类摄影 |
- 电影级布光 | 高对比度、强烈的阴影效果 | 电影风格的影像 |

## 使用案例示例

### 1. 添加专业摄影棚布光

使用经典的三点布光方案，将一张普通照片转换为专业拍摄的人像。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Add professional studio lighting to this portrait. Use a soft key light from 45 degrees left, fill light from the right to reduce shadows, and a subtle hair light from behind. Keep the background dark for a classic studio look.",
    "image_urls": ["https://example.com/portrait.jpg"],
    "mode": "max"
  }'
```

### 2. 金色时刻/日落布光

模拟在黄金时刻拍摄的照片，营造温暖的金色阳光效果。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Relight this photo with golden hour lighting. Add warm, soft sunlight coming from the side, creating a beautiful golden glow on the skin. Include subtle lens flare and that magical sunset atmosphere.",
    "image_urls": ["https://example.com/outdoor-photo.jpg"],
    "mode": "max"
  }'
```

### 3. 戏剧性侧光

利用强烈的方向性光线和深邃的阴影，打造引人注目的人像。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Apply dramatic side lighting to this portrait. Strong directional light from the left creating deep shadows on the right side of the face. High contrast, moody atmosphere, like a film noir character portrait.",
    "image_urls": ["https://example.com/headshot.jpg"],
    "mode": "max"
  }'
```

### 4. 柔和的散射光

生成均匀的光线，减少刺眼的阴影和皮肤瑕疵。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Relight this photo with soft, diffused lighting. Like shooting through a large softbox or on an overcast day. Even, flattering light with minimal shadows, perfect for beauty photography. Keep the skin looking natural and glowing.",
    "image_urls": ["https://example.com/beauty-shot.jpg"],
    "mode": "max"
  }'
```

### 5. 霓虹灯/彩色灯光

运用鲜艳的彩色灯光，实现创意或编辑类效果。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Add neon lighting to this portrait. Cyberpunk style with pink/magenta light from the left and blue/cyan light from the right. Create that futuristic nightclub vibe with vibrant colored reflections on the skin and a dark background.",
    "image_urls": ["https://example.com/model-photo.jpg"],
    "mode": "max"
  }'
```

### 6. 自然窗光

模拟透过窗户照射的柔和自然光。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Relight this portrait with natural window light. Soft, directional daylight coming from a large window on the left side. Create gentle shadows and that beautiful, airy natural light photographers love. Slightly cool color temperature.",
    "image_urls": ["https://example.com/indoor-portrait.jpg"],
    "mode": "max"
  }'
```

### 7. 环形灯效果

生成在美妆或社交媒体内容中流行的环形光源效果。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Apply ring light effect to this selfie. Even, frontal lighting with that signature circular catchlight in the eyes. Minimize shadows under the nose and chin, create that beauty influencer look with glowing, even skin illumination.",
    "image_urls": ["https://example.com/selfie.jpg"],
    "mode": "max"
  }'
```

### 8. 电影级布光

营造具有强烈对比度和氛围感的电影级光线效果。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Apply cinematic lighting to this portrait. Hollywood movie style with strong key light, deep shadows, and subtle rim light separating the subject from background. Moody and atmospheric like a scene from a thriller. Add subtle haze/atmosphere in the air.",
    "image_urls": ["https://example.com/actor-photo.jpg"],
    "mode": "max"
  }'
```

### 9. 去除刺眼阴影

通过柔和或去除不自然的阴影，改善光线不足的照片。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Remove the harsh shadows from this photo. The midday sun created unflattering dark shadows under the eyes and nose. Relight it with softer, more even lighting while keeping a natural outdoor look. Fill in the shadow areas without making it look flat.",
    "image_urls": ["https://example.com/harsh-shadow-photo.jpg"],
    "mode": "max"
  }'
```

### 10. 与背景匹配

调整主体图像的光线，使其与新背景完美融合。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Relight this person to match the beach sunset background. The subject was photographed indoors with flat lighting, but needs to look like they are actually on the beach during golden hour. Match the warm color temperature, add rim lighting from the setting sun behind them, and ensure the shadows are consistent with the background lighting direction.",
    "image_urls": [
      "https://example.com/subject-indoor.jpg",
      "https://example.com/beach-sunset-background.jpg"
    ],
    "mode": "max"
  }'
```

## 多次迭代布光优化

使用 `session_id` 在多次请求中逐步优化光线效果：

```bash
# Initial relighting
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Add dramatic studio lighting to this portrait with strong shadows",
    "image_urls": ["https://example.com/portrait.jpg"],
    "session_id": "lighting-session-001"
  }'

# Refine the result
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "The shadows are too harsh. Can you soften them slightly while keeping the dramatic feel? Also add a subtle blue rim light on the shadow side.",
    "session_id": "lighting-session-001"
  }'

# Try a variation
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create another version with warmer color temperature, like tungsten lighting",
    "session_id": "lighting-session-001"
  }'
```

## 模式选择

在生成效果前，请询问用户：

**“您需要快速且低成本的效果，还是高质量的效果？”**

| 模式 | 适用场景 | 速度 | 质量 |
|------|---------|-------|---------|
| `max` | 最终输出结果、客户项目、作品集图片 | 较慢 | 最高质量 |
| `eco` | 快速预览、测试布光方案、批量处理 | 较快 | 较好质量 |

## 优化提示

为了获得最佳效果，请在请求重新布光时提供以下详细信息：

1. **光线方向**：指定光线的来源（左侧、右侧、上方、后方）
2. **光线质量**：强烈/柔和、散射光或镜面反射光
3. **色温**：温暖（金色）、冷色调（蓝色）、中性色或特定颜色
4. **阴影强度**：深阴影、微弱阴影或无阴影
5. **氛围/风格**：戏剧性、浪漫、专业或前卫
6. **参考风格**：例如“类似《Vogue》杂志的编辑风格”或“黑色电影风格”

### 示例提示结构

```
"Relight this [subject type] with [lighting style].
Light coming from [direction] with [quality] shadows.
[Color temperature] color temperature.
Mood: [atmosphere description].
[Additional requirements]"
```

## 错误处理

| 错误类型 | 原因 | 解决方案 |
|---------|---------|---------|
| `Failed to create prediction: HTTP 422` | 数据不平衡 | 请在 eachlabs.ai 平台上补充数据 |
| 内容政策违规 | 图像不符合政策要求 | 确保图片符合内容政策 |
| 超时 | 生成过程复杂 | 将客户端超时时间设置为至少 10 分钟 |
| 布光效果不佳 | 提示信息不明确 | 请更具体地描述光线方向、质量和氛围 |
|