---
name: game-asset-generation
description: 使用 each::sense AI 生成游戏艺术资源。包括创建 2D 精灵图、角色精灵表、无缝纹理、用户界面元素、图标、瓦片集、加载界面、标志以及游戏的概念艺术。
metadata:
  author: eachlabs
  version: "1.0"
---
# 游戏资源生成

使用 `each-sense` 生成专业的游戏艺术资源。该技能可以创建 2D 精灵图、纹理、用户界面元素、图标、环境等，这些资源都针对游戏开发工作流程进行了优化。

## 成本节约

与传统游戏艺术制作方法相比，成本可降低 60-80%。基于 AI 的资源生成技术显著减少了独立开发者、游戏工作室和游戏竞赛的时间和预算成本。

## 主要功能

- **2D 精灵图**：像素艺术风格的角色、物体和道具
- **精灵图集**：包含多种姿势的动画准备就绪的角色图片
- **游戏纹理**：适用于游戏环境的无缝平铺纹理
- **用户界面元素**：按钮、框架、生命值条、物品栏
- **游戏图标**：物品图标、技能图标、成就徽章
- **平铺集**：适用于平台游戏、角色扮演游戏和策略游戏的背景瓷砖
- **加载界面**：具有氛围感的加载界面和启动画面
- **游戏标志**：游戏标题标志和品牌资产
- **概念艺术**：用于视觉开发和创意构思的素材

## 快速入门

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 32x32 pixel art sword icon for an RPG game, golden blade with ornate hilt, transparent background",
    "mode": "max"
  }'
```

## 常见的游戏艺术资源尺寸

| 资源类型 | 常见尺寸 | 用途 |
|------------|--------------|----------|
| 像素艺术图标 | 16x16, 32x32, 64x64 | 物品栏物品、技能图标 |
| 角色精灵图 | 32x32, 64x64, 128x128 | 玩家/非玩家角色 |
| 精灵图集 | 512x512, 1024x1024 | 动画帧 |
| 纹理 | 256x256, 512x512, 1024x1024 | 游戏环境表面 |
| 用户界面元素 | 各种尺寸 | 按钮、框架、状态条 |
| 加载界面 | 1920x1080, 2560x1440 | 全屏显示 |

## 用途示例

### 1. 2D 精灵图生成（像素艺术）

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 64x64 pixel art character sprite of a medieval knight with blue armor and silver sword. Retro 16-bit style, side view facing right, transparent background. Clean pixel edges, no anti-aliasing.",
    "mode": "max"
  }'
```

### 2. 角色精灵图集

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a character sprite sheet for a pixel art wizard character. Include 8 frames: 2 idle poses, 2 walking frames, 2 attack frames, 1 jump, 1 hurt pose. 32x32 per frame, arranged in a 4x2 grid (256x64 total). Purple robe, white beard, wooden staff.",
    "mode": "max"
  }'
```

### 3. 无缝游戏纹理生成

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a seamless tileable 512x512 stone dungeon floor texture. Dark gray cobblestones with moss growing between cracks, worn and weathered look. Must tile perfectly with no visible seams when repeated.",
    "mode": "max"
  }'
```

### 4. 游戏图标集

```bash
# First icon
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 64x64 pixel art health potion icon for an RPG. Red liquid in a glass flask with cork stopper, glowing effect, transparent background. Fantasy game style.",
    "session_id": "rpg-icons-set"
  }'

# Second icon (same session for style consistency)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a mana potion icon in the same style. Blue liquid instead of red, same flask design, matching art style.",
    "session_id": "rpg-icons-set"
  }'

# Third icon
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a stamina potion icon. Green liquid, same consistent style as the health and mana potions.",
    "session_id": "rpg-icons-set"
  }'
```

### 5. 用户界面元素（按钮、框架、状态条）

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a fantasy RPG UI kit containing: 1 rectangular button (200x50) with stone texture and gold border, 1 health bar frame (300x30) with ornate metal design, 1 inventory slot frame (64x64) with wooden texture and metal corners. Arrange on transparent background. Medieval fantasy style matching games like Diablo or Baldur'\''s Gate.",
    "mode": "max"
  }'
```

### 6. 游戏环境/平铺集生成

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 2D platformer tileset for a forest level. Include 16x16 pixel tiles: grass top, dirt fill, grass corner pieces (4 corners), tree trunk, leaves, flowers, rocks, wooden platform. Arrange in a tileset grid. Colorful cartoon style similar to classic platformers. 256x256 total sheet.",
    "mode": "max"
  }'
```

### 7. 物品/武器图标

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a set of 6 weapon icons for a fantasy game, each 48x48 pixels: iron sword, wooden bow, fire staff, battle axe, throwing daggers, war hammer. Arrange in a 3x2 grid. Consistent hand-painted style with slight glow effects, transparent backgrounds. Top-down perspective for inventory display.",
    "mode": "max"
  }'
```

### 8. 加载界面设计

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1920x1080 loading screen for a dark fantasy action RPG. Epic scene showing a lone warrior silhouette standing before a massive gothic castle on a cliff, stormy sky with lightning, dark moody atmosphere. Leave space at bottom center for a loading bar. Painterly digital art style.",
    "mode": "max"
  }'
```

### 9. 游戏标志设计

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a game logo for a space shooter called \"NOVA STRIKE\". Bold metallic chrome letters with neon blue glow effects, slight 3D perspective, stars and energy particles around it. Sci-fi futuristic style. Transparent background, 1024x512 resolution. Suitable for title screen and marketing.",
    "mode": "max"
  }'
```

### 10. 游戏概念艺术

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create concept art for a post-apocalyptic survival game. Show an abandoned city overgrown with vegetation, rusted vehicles, crumbling skyscrapers with trees growing through them, dramatic sunset lighting breaking through clouds. Painterly concept art style like The Last of Us or Horizon. 16:9 aspect ratio for presentation.",
    "mode": "max"
  }'
```

## 最佳实践

### 精灵图制作
- **指定精确尺寸**：始终提供像素尺寸（例如 32x32, 64x64）
- **说明透明度要求**：请求透明背景以便集成到游戏中
- **定义视角**：侧视图、俯视图、等轴测图、正面视图
- **艺术风格**：像素艺术、手绘、矢量图、复古 8 位/16 位风格

### 纹理制作
- **要求无缝平铺**：对于重复使用的纹理，务必指定“无缝平铺”属性
- **使用 2 的幂次方尺寸**：使用 256x256、512x512、1024 的尺寸以获得最佳 GPU 性能
- **描述材质特性**：如磨损、老化、状态变化等细节

### 图标制作
- **使用 `session_id`**：确保多个图标保持一致的风格
- **网格布局**：请求有序的精灵图集布局
- **统一光照效果**：指定光照方向以增强整体一致性

### 用户界面元素设计
- **预留空间**：考虑文本和动态内容的显示需求
- **可伸缩性**：考虑资源在不同分辨率下的显示效果
- **状态变化**：请求按钮的正常状态、悬停状态和点击状态

## 模式选择

在生成资源之前，请询问用户：

**“您需要快速且低成本的结果，还是高质量的结果？”**

| 模式 | 适用场景 | 速度 | 质量 |
|------|----------|-------|---------|
| `max` | 最终制作资源、英雄图片、关键艺术元素 | 较慢 | 最高质量 |
| `eco` | 快速迭代、概念探索、原型制作 | 较快 | 良好质量 |

## 多轮资源迭代

使用 `session_id` 进行多次迭代，以创建一致的资源集：

```bash
# Initial character design
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a pixel art hero character for a platformer game, 64x64, knight with red cape",
    "session_id": "hero-character-project"
  }'

# Request variations
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create the same character but with a blue cape for player 2, matching style exactly",
    "session_id": "hero-character-project"
  }'

# Create matching enemy
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an enemy character in the same pixel art style - a skeleton warrior, same size and art direction",
    "session_id": "hero-character-project"
  }'
```

## 批量资源生成

高效地生成多种变体资源：

```bash
# Style A - Pixel Art
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a treasure chest icon, 32x32, pixel art, closed position",
    "mode": "eco"
  }'

# Style B - Hand-painted
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a treasure chest icon, 64x64, hand-painted fantasy style, closed position",
    "mode": "eco"
  }'

# Style C - Modern Vector
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a treasure chest icon, 128x128, clean vector style with gradients, modern mobile game look",
    "mode": "eco"
  }'
```

## 错误处理

| 错误类型 | 原因 | 解决方案 |
|-------|-------|----------|
| **生成失败（HTTP 422）** | 资源不足 | 请在 eachlabs.ai 上补充资源 |
| 内容违规 | 禁止的内容 | 调整提示以避免包含暴力或露骨的内容 |
| 超时 | 生成过程复杂 | 将客户端超时时间设置为至少 10 分钟 |

## 创建游戏艺术资源的提示建议

在创建游戏艺术资源时，请在提示中包含以下详细信息：

1. **尺寸**：精确的像素尺寸（例如 32x32, 512x512）
2. **艺术风格**：像素艺术、手绘、矢量图、复古风格或现代风格
3. **视角**：侧视图、俯视图、等轴测图、3/4 视角
4. **背景**：透明背景、纯色背景或具有场景背景的背景
5. **色彩调色板**：有限的色彩范围、鲜艳的色彩、柔和的色彩或特定的色彩
6. **游戏类型**：角色扮演游戏、平台游戏、射击游戏、解谜游戏等——这些信息会影响艺术风格的预期
7. **参考风格**：例如“类似《星露谷物语》的风格”、“受《塞尔达》启发的风格”等

### 示例提示结构

```
"Create a [dimensions] [art style] [asset type] for a [game genre].
[Visual description with colors, materials, details].
[Perspective/view angle]. [Background requirement].
[Additional technical requirements]."
```

## 相关技能

- `each-sense`：核心 API 文档
- `product-visuals`：产品可视化工具
- `image-generation`：通用图像生成工具

## 参考资料

- [SSE 事件参考](./references/SSE-EVENTS.md)：服务器发送事件的文档说明