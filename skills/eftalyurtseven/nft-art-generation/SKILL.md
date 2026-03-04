---
name: nft-art-generation
description: 使用 each::sense AI 生成 NFT 艺术品。可以创建头像（PFP）系列、生成式艺术作品、独一无二的艺术品（1/1 原创作品）、像素艺术、3D 渲染图，以及适用于 Web3 项目的基于特定特性的角色。
metadata:
  author: eachlabs
  version: "1.0"
---
# NFT艺术生成

使用`each-sense`功能生成令人惊叹的NFT艺术品。该技能能够创建专为NFT收藏、市场平台及Web3项目优化的图像和视频。

## 主要功能

- **PFP收藏**：包含10,000张风格统一的头像图片
- **生成艺术**：受算法启发的抽象和几何风格作品
- **独一无二的艺术品**：高质量的单版杰作
- **像素艺术**：复古风格的像素化NFT艺术品
- **3D NFT**：渲染的3D角色和物体
- **动画NFT**：带有动态效果的GIF和视频NFT
- **AI艺术收藏**：独特的AI生成艺术系列
- **基于属性的角色**：具有可组合属性的角色

## 快速入门

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a PFP NFT of an ape character with cyberpunk style, neon colors, wearing futuristic sunglasses and a hoodie, dark background",
    "mode": "max"
  }'
```

## NFT艺术格式与尺寸

| 类型 | 宽高比 | 推荐尺寸 | 适用场景 |
|------|--------------|------------------|----------|
| PFP收藏 | 1:1 | 1024x1024或2048x2048 | 头像、头像 |
| 生成艺术 | 1:1 | 2048x2048或4096x4096 | 艺术作品、画廊展示 |
| 独一无二的艺术品 | 多种尺寸 | 2048x2048及以上 | 高价值的单版作品 |
| 像素艺术 | 1:1 | 32x32至512x512 | 复古风格收藏 |
| 3D渲染 | 1:1或4:3 | 2048x2048 | 3D角色NFT |
| 动画GIF | 1:1 | 1024x1024 | 动态NFT |
| 视频NFT | 1:1或16:9 | 1080x1080或1920x1080 | 高级动画作品 |

## 适用场景示例

### 1. PFP收藏（10K风格）

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 PFP NFT in the style of a 10K collection. An anthropomorphic fox character with purple fur, wearing a gold chain necklace and a backwards cap. Solid gradient background from teal to purple. Clean digital art style, bold outlines, vibrant colors.",
    "mode": "max"
  }'
```

### 2. 生成艺术作品

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a generative art piece inspired by algorithmic patterns. Abstract flowing lines and geometric shapes, inspired by Tyler Hobbs and Dmitri Cherniak. Use a limited color palette of deep blues, whites, and gold accents. Mathematical precision with organic flow. 1:1 aspect ratio.",
    "mode": "max"
  }'
```

### 3. 独一无二的艺术品

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a high-quality 1/1 NFT artwork. A surreal dreamscape with a floating island in a cosmic void, ancient ruins overgrown with bioluminescent plants, multiple moons in the sky, ethereal atmosphere. Ultra detailed, cinematic lighting, museum-quality digital painting.",
    "mode": "max"
  }'
```

### 4. 像素艺术NFT

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a pixel art NFT character. A retro-style warrior knight with glowing sword, 32x32 pixel style scaled up cleanly. Limited color palette, nostalgic 8-bit aesthetic, solid color background. CryptoPunks meets fantasy RPG vibe.",
    "mode": "max"
  }'
```

### 5. 3D NFT艺术作品

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 3D rendered NFT character. A stylized robot head with chrome finish, glowing LED eyes, intricate mechanical details, floating in a dark studio environment with dramatic rim lighting. Octane render quality, subsurface scattering, 1:1 aspect ratio.",
    "mode": "max"
  }'
```

### 6. 动画NFT（GIF/视频）

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an animated NFT, 3-5 seconds loop. A mystical crystal orb with swirling energy inside, particles floating around it, pulsing glow effect. Seamless loop, hypnotic motion, dark background with subtle ambient particles. 1:1 square format.",
    "mode": "max"
  }'
```

### 7. AI艺术收藏

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an AI art piece for a collection exploring digital consciousness. Abstract portrait merging human and digital elements, data streams flowing through a face, glitch art effects, neural network visualization overlay. Vaporwave color palette with pink, cyan, and purple. Unique artistic interpretation.",
    "mode": "max"
  }'
```

### 8. 基于属性的角色生成

```bash
# First character with base traits
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a trait-based NFT character for a collection. Base: Cat humanoid. Traits: Background=Sunset Orange, Fur=Calico pattern, Eyes=Laser red, Accessory=Pirate eyepatch, Clothing=Leather jacket, Headwear=None. Consistent flat illustration style suitable for a 10K PFP collection.",
    "session_id": "nft-collection-cats-001"
  }'

# Second character variation (same session for consistency)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create another character with different traits. Same style as before. Traits: Background=Deep Space, Fur=White, Eyes=Diamond blue, Accessory=Monocle, Clothing=Tuxedo, Headwear=Top hat. Maintain the exact same art style.",
    "session_id": "nft-collection-cats-001"
  }'
```

### 9. 抽象生成艺术

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an abstract generative art NFT. Inspired by Art Blocks aesthetic - recursive geometric patterns, flow fields, mathematical beauty. Colors emerge from chaos into order. Black background with vibrant color accents in orange, pink, and electric blue. Crisp vector-like precision. 1:1 format.",
    "mode": "max"
  }'
```

### 10. 科技朋克/未来主义NFT

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a cyberpunk NFT artwork. A futuristic street samurai character with cybernetic augmentations, neon-lit visor, holographic HUD elements, rain-soaked environment reflected on surfaces. Blade Runner meets anime aesthetic. Neon pink and cyan color scheme, dark atmospheric mood. Premium collectible quality.",
    "mode": "max"
  }'
```

## 最佳实践

### 收藏一致性
- **艺术风格**：确保收藏中的所有作品保持一致的风格
- **色彩调色板**：定义并使用统一的色彩方案
- **属性系统**：为角色设计明确的属性（背景、身体、配饰等）
- **分辨率**：所有作品使用相同的分辨率
- **会话ID**：相关作品使用相同的`session_id`以保持一致性

### 技术质量
- **高分辨率**：生成2048x2048及以上分辨率的作品以确保显示效果
- **清晰的边缘**：PFP收藏要求边缘清晰
- **正确的格式**：静态作品使用PNG格式，动画作品使用MP4/GIF格式
- **适合市场平台**：确保输出符合OpenSea、Foundation等平台的要求

### NFT特定注意事项
- **稀有性设计**：设计具有辨识度的稀有属性
- **可缩放性**：确保作品在缩略图尺寸下仍保持美观
- **独特性**：每件作品在视觉上都要具有独特性
- **元数据准备**：生成时附带清晰的属性描述

## NFT艺术创作提示

在创建NFT艺术品时，请在提示中包含以下信息：

1. **收藏类型**：PFP、生成艺术、独一无二的艺术品、像素艺术等
2. **艺术风格**：描述作品的视觉风格（平面、3D、像素化、绘画风格）
3. **主题**：作品的主要主题（角色、抽象、风景等）
4. **属性**：如果基于属性设计，请列出具体特征
5. **色彩调色板**：指定使用的颜色或整体色调
6. **背景**：纯色、渐变或细节丰富的背景
7. **质量要求**：说明是否需要高级或博物馆级别的质量

### 示例提示结构

```
"Create a [collection type] NFT.
[Subject description] with [traits/attributes].
Style: [art style].
Colors: [color palette].
Background: [background description].
[Additional quality/format requirements]"
```

## 模式选择

在生成作品前询问用户：

**“您需要快速且低成本的结果，还是高质量的作品？”**

| 模式 | 适用场景 | 速度 | 质量 |
|------|----------|-------|---------|
| `max` | 最终收藏作品、独一无二的艺术品、高级版本 | 较慢 | 最高质量 |
| `eco` | 概念探索、属性测试、草图迭代 | 较快 | 良好质量 |

## 多轮迭代开发收藏

使用`session_id`进行迭代式开发收藏：

```bash
# Establish collection style
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a base character for my NFT collection. A stylized bear with streetwear fashion, bold flat colors, minimalist background.",
    "session_id": "bear-nft-project"
  }'

# Request trait variation
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create the same bear character but with different accessories - add sunglasses and a gold chain. Keep the exact same art style.",
    "session_id": "bear-nft-project"
  }'

# Request rare variant
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a rare legendary variant - same bear but with cosmic/galaxy fur pattern, glowing eyes, and a crown. This is the 1/1 rare for the collection.",
    "session_id": "bear-nft-project"
  }'
```

## 批量生成收藏作品

高效生成多个变体：

```bash
# Variation 1 - Common trait
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create PFP NFT: Robot character, silver body, blue LED eyes, plain gray background, minimal style",
    "mode": "eco"
  }'

# Variation 2 - Uncommon trait
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create PFP NFT: Robot character, gold body, green LED eyes, gradient purple background, minimal style",
    "mode": "eco"
  }'

# Variation 3 - Rare trait
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create PFP NFT: Robot character, holographic rainbow body, laser red eyes, cosmic space background, minimal style",
    "mode": "eco"
  }'
```

## 错误处理

| 错误 | 原因 | 解决方案 |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | 账户余额不足 | 在eachlabs.ai充值 |
| 内容违规 | 内容不符合规定 | 调整提示以符合平台内容政策 |
| 超时 | 生成过程复杂 | 将客户端超时时间设置为至少10分钟 |
| 风格不一致 | 会话中断 | 使用相同的`session_id`生成所有作品 |

## 相关技能

- `each-sense`：核心API文档
- `product-photo-generation`：产品图片生成
- `meta-ad-creative-generation`：社交媒体创意内容生成