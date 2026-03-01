---
name: comic-panel-generation
description: 使用 each::sense AI 生成漫画和 manga 的画面、章节以及完整的单页内容。可以创作超级英雄题材的漫画、 manga 页面、网络漫画（webtoons），以及动作场景的情节。此外，还可以将照片转换为具有统一角色风格的漫画作品。
metadata:
  author: eachlabs
  version: "1.0"
---
# 漫画面板生成

使用 `each-sense` 功能生成专业的漫画和 manga 艺术作品。该技能可以创建单幅漫画面板、多幅连环画、整页布局以及完整的漫画序列，并确保角色设计的一致性。

## 主要功能

- **单幅漫画面板**：具有动态构图的独立漫画面板
- **多幅连环画**：传统的 3-4 幅漫画条
- **Manga 页**：符合日式漫画阅读习惯的页面布局
- **超级英雄漫画**：西方漫画风格的画面，色彩鲜艳且充满动作场景
- **Webtoon 格式**：适合移动设备阅读的垂直滚动格式
- **照片转漫画**：将照片转换为漫画/漫画风格的艺术作品
- **对话框**：生成包含对话框的漫画面板
- **动作场景**：带有动态动作线及特效的动作面板
- **角色一致性**：确保角色在不同面板中的外观一致
- **封面设计**：漫画书和 manga 的封面艺术作品

## 快速入门

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a single comic panel of a superhero landing dramatically on a rooftop at night, cape billowing, city lights in background",
    "mode": "max"
  }'
```

## 漫画面板格式与尺寸

| 格式 | 长宽比 | 推荐尺寸 | 适用场景 |
|--------|--------------|------------------|----------|
| 单幅面板 | 1:1 | 1024x1024 | 社交媒体、独立艺术作品 |
| 宽面板 | 16:9 | 1920x1080 | 电影场景、风景画 |
| 高面板 | 9:16 | 1080x1920 | 戏剧性场景、Webtoon |
| 连环画 | 3:1 | 1500x500 | 3-4 幅的水平连环画 |
| Manga 页 | 2:3 | 1200x1800 | 传统 manga 布局 |
| Webtoon | 1:3+ | 800x2400+ | 垂直滚动格式 |
| 漫画封面 | 2:3 | 1200x1800 | 书籍封面、缩略图 |

## 适用场景示例

### 1. 单幅漫画面板

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a single comic panel showing a detective in a noir style examining clues in a dimly lit office. Heavy shadows, black and white with selective color on a red lamp. Include dramatic lighting from venetian blinds.",
    "mode": "max"
  }'
```

### 2. 多幅连环画

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 4-panel horizontal comic strip. Panel 1: A cat staring at an empty food bowl. Panel 2: Cat meowing at its sleeping owner. Panel 3: Cat knocking items off a shelf. Panel 4: Owner finally awake and annoyed, cat looking innocent. Cute cartoon style, pastel colors.",
    "mode": "max"
  }'
```

### 3. Manga 页布局

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a full manga page with 5-6 panels. Scene: A young samurai drawing his sword for the first time. Include dynamic panel sizes - one large panel for the dramatic sword draw moment, smaller panels for reaction shots. Black and white manga style with screentones, speed lines for action. Right-to-left reading flow.",
    "mode": "max"
  }'
```

### 4. 超级英雄漫画风格

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a superhero comic panel in classic Marvel/DC style. A female superhero with electric powers charging up, lightning crackling around her fists, dramatic low angle shot. Bold colors, heavy inks, dynamic pose, Kirby-style energy effects. Include a starburst background.",
    "mode": "max"
  }'
```

### 5. Webtoon 垂直格式

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a vertical webtoon-style comic segment with 3 connected scenes. Scene 1: A student walking into a mysterious antique shop. Scene 2: Close-up of a glowing amulet on a shelf. Scene 3: The shopkeeper appearing mysteriously behind them. Korean webtoon art style, soft colors, vertical scroll format optimized for mobile. 9:16 or taller aspect ratio.",
    "mode": "max"
  }'
```

### 6. 照片转漫画转换

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Convert this photo into a comic book style illustration. Apply bold black outlines, halftone dots for shading, vibrant pop art colors. Make it look like a panel from a graphic novel. Keep the composition but stylize all elements.",
    "mode": "max",
    "image_urls": ["https://example.com/portrait-photo.jpg"]
  }'
```

### 7. 对话框生成

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a comic panel with two characters arguing. Include speech bubbles with placeholder text areas. Character 1 (angry businessman): large jagged speech bubble for shouting. Character 2 (calm woman): regular oval speech bubble for response. Also include a thought bubble above the woman showing she is unimpressed. Western comic style.",
    "mode": "max"
  }'
```

### 8. 动作场景面板

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 3-panel action sequence showing a martial arts fight. Panel 1: Fighter A launching a flying kick (motion blur, speed lines). Panel 2: Impact moment with dramatic POW effect and motion burst. Panel 3: Fighter B crashing through wooden crates. Manga action style with heavy use of speed lines, impact effects, and dynamic camera angles.",
    "mode": "max"
  }'
```

### 9. 不同面板中角色的统一性

```bash
# First panel - establish character
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a comic panel introducing a character: A teenage girl with short blue hair, large round glasses, wearing a yellow raincoat. She is looking up at the rain with wonder. Anime/manga style, soft colors. This is panel 1 of a series - I need to maintain her appearance in future panels.",
    "session_id": "comic-rainy-day-001",
    "mode": "max"
  }'

# Second panel - same character, different scene
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create panel 2 with the same blue-haired girl with glasses and yellow raincoat. Now she is jumping in a puddle, splashing water, with a big smile. Maintain the exact same character design and art style from panel 1.",
    "session_id": "comic-rainy-day-001",
    "mode": "max"
  }'

# Third panel - continue the story
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create panel 3: Same character discovers a small frog on a lily pad in the puddle. She kneels down, delighted. Keep her blue hair, round glasses, yellow raincoat consistent. Same manga art style.",
    "session_id": "comic-rainy-day-001",
    "mode": "max"
  }'
```

### 10. 漫画封面设计

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a comic book cover for issue #1 of SHADOW KNIGHTS. Feature a team of 4 heroes in dramatic poses - a knight with a glowing sword, an archer with shadow powers, a mage with fire magic, and a rogue with dual daggers. Dark fantasy style, dramatic lighting from below, epic composition. Leave space at the top for the title logo and bottom for issue number and barcode area. 2:3 aspect ratio.",
    "mode": "max"
  }'
```

## 漫画艺术风格

| 风格 | 描述 | 适用类型 |
|-------|-------------|----------|
| 西方漫画 | 明显的线条、鲜艳的色彩、动态的姿势 | 超级英雄、动作类作品 |
| Manga | 简洁的线条、背景特效、富有表现力的眼睛 | 戏剧、浪漫、动作类 |
| Webtoon | 温和的色彩、细致的背景、垂直滚动方式 | 浪漫、奇幻、日常生活 |
| Noir | 高对比度、阴影效果、有限的色彩范围 | 侦探、惊悚类 |
| 卡通 | 简化的形状、夸张的表情 | 喜剧、儿童内容 |
| 图画小说 | 细致的描绘、真实的比例 | 成熟主题、文学类 |
| 波普艺术 | 明亮的色彩、半色调、风格化的表现手法 | 现代、艺术类 |

## 生成漫画时的提示建议

在创建漫画面板时，请在提示中包含以下细节：

1. **面板布局**：单幅面板、多幅连环画、整页布局或垂直滚动
2. **艺术风格**：Manga、西方漫画、Webtoon、Noir、卡通等
3. **动作/场景**：每幅面板中发生的内容
4. **角色**：描述角色的外貌、表情和姿势
5. **构图**：拍摄角度、焦点、戏剧性元素
6. **特效**：动作线、冲击效果、背景特效、光线效果
7. **对话框**：如有需要，添加对话框
8. **阅读顺序**：从左到右（西方风格）或从右到左（Manga 风格）

### 示例提示结构

```
"Create a [panel count/layout] comic in [art style] style.
[Panel-by-panel description of action/scene].
Characters: [descriptions].
Include [effects: speed lines, speech bubbles, etc.].
[Color/mood]: [palette preferences]."
```

## 模式选择

在生成作品之前，请询问用户：

**“您需要快速且低成本的结果，还是高质量的作品？”**

| 模式 | 适用类型 | 速度 | 质量 |
|------|----------|-------|---------|
| `max` | 最终成品、适合打印的漫画、详细的页面 | 较慢 | 最高质量 |
| `eco` | 快速草图、故事板制作、概念探索 | 较快 | 良好质量 |

## 多轮漫画创作

使用 `session_id` 在多次请求中构建完整的漫画作品：

```bash
# Page 1 - Establish the story
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create page 1 of a sci-fi manga. A space bounty hunter enters a seedy alien bar. 4 panels: exterior shot of neon-lit bar, hunter walking in (silhouette), aliens turning to look, close-up of hunters determined eyes.",
    "session_id": "space-bounty-comic"
  }'

# Page 2 - Continue the narrative
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create page 2 continuing the scene. The hunter approaches a table of alien criminals. Include panels showing: the target alien recognizing danger, the hunters hand reaching for a weapon, tension building. Same art style as page 1.",
    "session_id": "space-bounty-comic"
  }'

# Request style adjustment
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Recreate page 2 but with more dramatic lighting - add more shadows and a red color accent from the bar neon signs. Keep all other elements the same.",
    "session_id": "space-bounty-comic"
  }'
```

## 漫画项目的批量生成

高效地生成多页或多种风格的漫画作品：

```bash
# Cover variations
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a manga cover - a magical girl transformation scene, sparkles and ribbons, dramatic pose",
    "mode": "eco"
  }'

# Alternative cover style
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create the same magical girl cover but in darker, more mature art style - less sparkles, more dramatic shadows",
    "mode": "eco"
  }'

# Western comic adaptation
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create the magical girl transformation but in Western superhero comic style - bold colors, heavy inks, more muscular proportions",
    "mode": "eco"
  }'
```

## 错误处理

| 错误类型 | 原因 | 解决方案 |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | 资源不足 | 在 eachlabs.ai 网站充值 |
| 内容违规 | 禁止的内容 | 调整提示以避免包含暴力或成人内容 |
| 超时 | 复杂的多幅面板生成 | 将客户端超时时间设置为至少 10 分钟 |
| 角色不一致 | 会话未连续或描述模糊 | 使用相同的 `session_id`，并提供详细的角色描述 |

## 相关技能

- `each-sense` - 核心 API 文档
- `photo-to-illustration` - 将照片转换为各种艺术风格
- `character-design-generation` - 创建统一的角色设计
- `storyboard-generation` - 为动画制作视觉故事板