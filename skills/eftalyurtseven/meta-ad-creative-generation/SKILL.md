---
name: meta-ad-creative-generation
description: 使用 each::sense AI 生成 Meta（Facebook 和 Instagram）广告创意。可以创建适合 Meta 广告格式和最佳实践的动态广告、故事广告、视频广告以及轮播图片广告。
metadata:
  author: eachlabs
  version: "1.0"
---
# 元广告创意生成

使用 `each-sense` 生成具有高转化率的 Meta（Facebook 和 Instagram）广告创意。该技能能够生成符合 Meta 广告投放要求、格式规范及最佳实践的图片和视频。

## 功能

- **信息流广告**：适用于 Facebook/Instagram 信息流的静态图片和视频
- **故事/Reels**：适合沉浸式展示的 9:16 比例内容
- **轮播广告**：用于产品展示的多张图片
- **视频广告**：吸引用户互动的短形式视频内容
- **产品广告**：结合生活方式元素的产品广告创意
- **品牌提升**：用于提升品牌知名度的醒目视觉素材
- **潜在客户生成**：包含明确呼叫行动（CTA）的引人注目的视觉内容

## 快速入门

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a Facebook feed ad for a fitness app showing someone working out with energetic vibes, include space for headline text",
    "mode": "max"
  }'
```

## Meta 广告格式与尺寸

| 放置位置 | 长宽比 | 推荐尺寸 | 适用场景 |
|-----------|--------------|------------------|----------|
| 信息流（图片） | 1:1 | 1080x1080 | 产品广告、品牌提升 |
| 信息流（图片） | 4:5 | 1080x1350 | 更多的垂直空间，更高的互动率 |
| 信息流（视频） | 1:1 或 4:5 | 1080x1080 或 1080x1350 | 产品演示、用户评价 |
| 故事/Reels | 9:16 | 1080x1920 | 全屏沉浸式广告 |
| 轮播广告 | 1:1 | 1080x1080 | 产品目录、功能介绍 |
| 右侧栏 | 1.91:1 | 1200x628 | 桌面侧边栏广告 |

## 适用场景示例

### 1. 产品广告（电子商务）

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 Facebook product ad for wireless earbuds. Show the earbuds on a clean minimal background with lifestyle context - someone at a gym or running. Modern, premium feel. Leave space at top for headline.",
    "mode": "max"
  }'
```

### 2. Instagram 故事广告

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 9:16 Instagram Stories ad for a skincare brand. Show a woman with glowing skin, soft natural lighting, minimalist aesthetic. Leave safe zones at top and bottom for UI elements.",
    "mode": "max"
  }'
```

### 3. Facebook 视频广告

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 5 second 1:1 video ad for a coffee subscription service. Show steaming coffee being poured, cozy morning vibes, warm color grading. Eye-catching for autoplay without sound.",
    "mode": "max"
  }'
```

### 4. 轮播广告（多款产品）

```bash
# First image
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 carousel ad image 1 of 4 for a furniture store. Show a modern sofa in a stylish living room. Clean, aspirational lifestyle photography style.",
    "session_id": "carousel-furniture-001"
  }'

# Second image (same session for consistency)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create carousel image 2 of 4. Show a dining table set in the same style as the previous image. Maintain consistent lighting and aesthetic.",
    "session_id": "carousel-furniture-001"
  }'
```

### 5. Reels 视频广告

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 9:16 vertical video ad for Instagram Reels. Fashion brand summer collection - show a model walking on a beach in a flowing dress, cinematic slow motion, golden hour lighting. 5 seconds.",
    "mode": "max"
  }'
```

### 6. 应用安装广告

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 4:5 Facebook ad for a meditation app. Show a peaceful person meditating in nature, soft morning light, calming colors (blues and greens). Include visual space for app store badges and CTA button.",
    "mode": "max"
  }'
```

### 7. 餐厅/食品广告

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 Facebook ad for an Italian restaurant. Show a delicious pasta dish with steam rising, rustic table setting, warm inviting atmosphere. Food photography style, make it look appetizing.",
    "mode": "max"
  }'
```

### 8. 潜在客户生成广告（B2B）

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 Facebook lead gen ad for a B2B SaaS product. Show a professional working on a laptop with data visualizations, modern office environment, confident and productive mood. Corporate but not boring.",
    "mode": "max"
  }'
```

### 9. 用户生成内容（UGC）风格广告

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a UGC-style 9:16 video ad for a teeth whitening product. Show a young woman doing a selfie-style testimonial, authentic iPhone footage look, bathroom mirror setting, before/after reveal moment. 10 seconds.",
    "mode": "max"
  }'
```

### 10. 再定位广告（含产品图片）

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 retargeting ad for sneakers. Show white sneakers prominently with a lifestyle background (urban street scene). Add visual urgency - style that says limited time offer. Clean product focus.",
    "mode": "max",
    "image_urls": ["https://example.com/product-sneakers.jpg"]
  }'
```

## 最佳实践

### 图片广告
- **文本覆盖**：保持文本简洁——Meta 建议文本占比不超过 20%
- **安全区域**：在图片顶部/底部留出 14% 的空间以容纳故事/Reels 的 UI 元素
- **焦点**：将关键视觉元素放在中心
- **对比度**：使用对比鲜明的颜色以在信息流中突出显示
- **品牌颜色**：在所有广告中保持一致的品牌形象

### 视频广告
- **3 秒内吸引注意力**：立即抓住用户的目光
- **考虑无声播放**：使用字幕和视觉叙事
- **适合循环播放**：为短视频创建无缝循环效果
- **以移动设备优先**：设计适合移动设备的竖屏或正方形屏幕

### 轮播广告
- **视觉一致性**：所有图片保持相同的风格
- **故事连贯性**：在图片之间建立叙事逻辑
- **首张图片的吸引力**：让第一张图片最具吸引力

## 创建 Meta 广告创意的提示建议

在创建 Meta 广告创意时，请在提示中包含以下信息：

1. **格式**：指定长宽比（1:1、4:5、9:16）
2. **放置位置**：说明是用于信息流、故事还是 Reels
3. **产品/服务**：明确说明你要推广的内容
4. **目标受众**：该广告针对的是谁？
5. **情绪/风格**：活力四射、平静、奢华、趣味等
6. **文本空间**：如需要，请求预留标题/呼叫行动的位置
7. **品牌指南**：提及品牌使用的颜色和风格偏好

### 示例提示结构

```
"Create a [aspect ratio] [placement] ad for [product/service].
Show [visual description] with [mood/style].
Target audience: [demographic].
[Additional requirements like text space, brand colors, etc.]"
```

## 模式选择

在生成广告创意之前，请询问用户：

**“您需要快速且低成本的结果，还是高质量的结果？”**

| 模式 | 适用场景 | 速度 | 质量 |
|------|----------|-------|---------|
| `max` | 最终广告创意、A/B 测试结果 | 较慢 | 最高质量 |
| `eco` | 快速草图、概念探索、批量测试 | 较快 | 良好质量 |

## 多轮创意迭代

使用 `session_id` 进行广告创意的迭代：

```bash
# Initial creative
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 Facebook ad for a watch brand, luxury feel",
    "session_id": "watch-ad-project"
  }'

# Iterate based on feedback
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Make it more dramatic with darker background, add some bokeh lights",
    "session_id": "watch-ad-project"
  }'

# Request variation
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create 2 more variations of this ad with different angles",
    "session_id": "watch-ad-project"
  }'
```

## A/B 测试批量生成

生成多个版本以进行测试：

```bash
# Variation A - Lifestyle focus
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 ad for protein powder - lifestyle shot with athlete in gym",
    "mode": "eco"
  }'

# Variation B - Product focus
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 ad for protein powder - clean product shot with ingredients",
    "mode": "eco"
  }'

# Variation C - Benefit focus
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 ad for protein powder - before/after transformation style",
    "mode": "eco"
  }'
```

## 错误处理

| 错误 | 原因 | 解决方案 |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | 资源不足 | 在 eachlabs.ai 补充资源 |
| 内容政策违规 | 内容被禁止 | 调整提示以符合 Meta 广告政策 |
| 超时 | 生成过程复杂 | 将客户端超时设置为至少 10 分钟 |

## 相关技能

- `each-sense`：核心 API 文档
- `google-ad-creative-generation`：Google 广告创意生成
- `tiktok-ad-creative-generation`：TikTok 广告创意生成
- `product-photo-generation`：电子商务产品图片生成