---
name: meme-generation
description: 使用 each::sense AI 生成表情包（meme）。您可以创建经典的表情包模板、定制表情包、品牌相关表情包、反应表情包、对比表情包等，适用于社交媒体、市场营销和娱乐领域。
metadata:
  author: eachlabs
  version: "1.0"
---
# 模因生成

使用 `each-sense` 功能生成具有病毒式传播潜力的模因。该技能可生成适用于社交媒体分享、品牌营销、职场幽默以及互联网文化互动的图片。

## 特点

- **经典模板**：生成常见的模因格式（如 Drake、分心的男朋友等）
- **自定义模因**：根据任何提示创建原创模因图片
- **品牌模因**：符合品牌风格的营销用模因
- **反应模因**：用于社交媒体互动的表情图片
- **对比模因**：并排展示或对比前后效果的模因
- **热门格式**：当前流行的模因样式和格式
- **文字叠加模因**：图片上叠加文字的模因
- **多面板模因**：类似连环漫画的序列图片
- **企业/职场模因**：适用于办公室幽默和专业讽刺的模因
- **行业特定模因**：针对特定社区的定制幽默内容

## 快速入门

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a meme about developers when the code works on the first try - shocked and suspicious expression",
    "mode": "max"
  }'
```

## 模因格式与风格

| 格式 | 描述 | 适用场景 |
|--------|-------------|----------|
| 经典模板 | 可识别的模因格式 | 最适合分享 |
| 反应模因 | 表情丰富的图片 | 用于社交媒体回复 |
| 对比模因 | 并排展示的图片 | 对比前后效果或预期与现实 |
| 多面板模因 | 2-4 个面板的序列 | 用于讲述故事或表达幽默 |
| 文字叠加模因 | 图片上带有文字的模因 | 直观、有力的幽默效果 |
| 超现实/抽象模因 | 超现实的图像 | 适合 Z 世代用户或小众社区 |

## 使用案例示例

### 1. 生成经典模因模板

按照流行的模因模板风格生成图片。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a meme image in the style of the Drake meme format. Two panels vertically stacked. Top panel: a person looking away dismissively with hand up rejecting something. Bottom panel: same person smiling and pointing approvingly. Clean white background, expressive poses.",
    "mode": "max"
  }'
```

### 2. 根据提示创建自定义模因

根据创意概念创建原创模因图片。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a meme image of a cat sitting at a computer desk looking extremely confused at the screen, office setting, dramatic lighting from the monitor, the cat has reading glasses on. Funny and relatable vibe for when you receive a confusing email.",
    "mode": "max"
  }'
```

### 3. 品牌模因营销

为品牌社交媒体账号创建合适的模因。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a clean, brand-safe meme image for a coffee company social media. Show a person dramatically hugging a giant coffee cup like it is their best friend. Office morning setting, humorous but professional enough for brand use. Warm, inviting colors.",
    "mode": "max"
  }'
```

### 4. 反应模因

生成用于社交媒体互动的表情图片。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a reaction meme image of a person with an extremely exaggerated surprised face, eyes wide, jaw dropped, hands on cheeks. Simple background, highly expressive, perfect for replying to shocking news or announcements online.",
    "mode": "max"
  }'
```

### 5. 对比模因

创建并排对比的模因。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a two-panel comparison meme image. Left panel labeled area for expectation: a person confidently presenting at a meeting looking professional. Right panel labeled area for reality: the same person nervously fumbling with papers, coffee spilled, chaotic scene. Corporate office setting.",
    "mode": "max"
  }'
```

### 6. 热门格式模因

生成当前流行的模因样式。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a meme image in the style of the woman yelling at cat meme format. Left side: an angry woman pointing and yelling expressively at a dinner table. Right side: a confused white cat sitting at a table with a plate in front of it, looking bewildered. Split panel format.",
    "mode": "max"
  }'
```

### 7. 文字叠加模因

创建适合叠加文字的图片。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a meme background image of a galaxy brain or expanding brain concept. Show a person in meditation pose with a glowing, oversized brain emanating light and energy. Cosmic background with stars. Leave clear space at top and bottom for impact font text overlay.",
    "mode": "max"
  }'
```

### 8. 多面板模因

生成类似连环漫画的序列图片。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 4-panel meme comic strip. Panel 1: person calmly saying they will just check one email. Panel 2: person still at computer, slightly concerned. Panel 3: person surrounded by multiple screens, stressed. Panel 4: person collapsed at desk, it is now nighttime. Office setting, escalating chaos.",
    "mode": "max",
    "session_id": "multi-panel-meme-001"
  }'
```

### 9. 企业/职场模因

为职场环境创建幽默模因。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a workplace meme image. Scene: a meeting room with a person presenting a very simple obvious solution on a whiteboard while everyone else at the table looks shocked and amazed as if it is genius. Exaggerated reactions, corporate office setting, humorous take on overthinking simple problems.",
    "mode": "max"
  }'
```

### 10. 行业特定模因

为特定专业社区生成定制模因。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a programmer/developer meme image. A developer sitting at a desk surrounded by multiple monitors showing code, but they are intensely focused on a tiny bug that is literally represented as a small cartoon bug on the screen. The bug is tiny but the developer is using a magnifying glass. Dramatic lighting, humorous debugging scene.",
    "mode": "max"
  }'
```

## 最佳实践

### 创建易于分享的模因

- **清晰的构图**：保持主要主题突出且画面整洁
- **富有表现力的表情**：反应模因中夸张的表情效果最佳
- **文字空间**：根据需要预留文字叠加的位置
- **普遍适用的幽默**：选择广泛共鸣的情境
- **高对比度**：确保图片在较小尺寸（如手机屏幕）下仍可清晰显示

### 品牌模因制作指南

- **保持品牌风格**：幽默内容应与品牌调性一致
- **避免争议性话题**：避免涉及敏感或争议性内容
- **时效性与永恒性**：在流行格式与持久吸引力之间取得平衡
- **质量胜过数量**：一个优秀的模因胜过十个平庸的模因
- **了解目标受众**：不同平台对幽默内容的偏好不同

### 技术提示

- **正方形格式（1:1）**：最适合 Instagram、Twitter 和 Facebook
- **垂直格式（4:5 或 9:16）**：更适合 Stories 和 TikTok
- **分辨率**：最短边至少为 1080px
- **文件大小**：保持文件大小适中，以便快速加载

## 模因创作提示

在创建模因图片时，请提供以下信息：

1. **格式**：指定面板布局（单面板、双面板、四面板等）
2. **表情**：清晰描述情感表达
3. **场景**：场景发生在哪里？
4. **风格**：现实主义、卡通风格、超现实风格等
5. **文字空间**：如果需要，指定文字叠加的位置
6. **背景**：该模因描绘的是哪种情境？

### 示例提示结构

```
"Create a [format] meme image. [Scene description] with [expression/action].
[Setting details]. [Style preferences].
[Text space requirements if any]."
```

## 模式选择

在生成模因之前询问用户：

**“您需要快速且低成本的模因，还是高质量的模因？”**

| 模式 | 适用场景 | 速度 | 质量 |
|------|----------|-------|---------|
| `max` | 最终成品、高互动性内容、品牌内容 | 较慢 | 最高质量 |
| `eco` | 快速草图、A/B 测试、批量生成 | 较快 | 一般质量 |

## 多轮迭代

使用 `session_id` 对模因概念进行多次迭代：

```bash
# Initial meme concept
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a meme of a dog at a computer looking frustrated",
    "session_id": "meme-project-001"
  }'

# Iterate based on feedback
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Make the dog expression more dramatic, add coffee cup for extra relatability",
    "session_id": "meme-project-001"
  }'

# Request variation
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a cat version of the same meme for comparison",
    "session_id": "meme-project-001"
  }'
```

## 模因系列生成

为某个活动生成多个相关的模因：

```bash
# Meme 1 - Monday mood
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a weekday mood meme - Monday: exhausted office worker barely awake at desk",
    "mode": "eco",
    "session_id": "weekday-series"
  }'

# Meme 2 - Friday mood (same session for consistency)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Same style but Friday: the same worker now energetic and celebrating, leaving the office",
    "mode": "eco",
    "session_id": "weekday-series"
  }'
```

## 错误处理

| 错误 | 原因 | 解决方案 |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | 平衡性不足 | 在 eachlabs.ai 网站充值 |
| 内容政策违规 | 禁止的内容 | 调整提示，避免使用冒犯性、有害或不适当的内容 |
| 超时 | 生成过程复杂 | 将客户端超时时间设置为至少 10 分钟 |

## 相关技能

- `each-sense`：核心 API 文档
- `image-generation`：通用图像生成
- `product-visuals`：产品摄影和营销视觉设计
- `meta-ad-creative-generation`：社交媒体广告创意设计