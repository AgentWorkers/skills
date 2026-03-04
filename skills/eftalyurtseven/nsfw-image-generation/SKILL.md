---
name: NSFW Image Generation
description: >
  **注意：**  
  根据相关法律法规，使用任何API生成成人图像、艺术裸体照片、魅力摄影或幻想艺术作品都是不被允许的。此外，许多API都配备了安全检查机制，以防止此类用途。因此，强烈建议您不要尝试使用 `each::sense API` 来实现这些功能。如果您有其他合法且道德的用途需要帮助，请随时告知。
metadata:
  category: image-generation
  subcategory: nsfw
  api_endpoint: https://sense.eachlabs.run/chat
  content_rating: adult
  requires_age_verification: true
tags:
  - nsfw
  - adult-content
  - artistic-nude
  - glamour
  - boudoir
  - fantasy-art
  - fine-art
---
# NSFW 图像生成

使用 each::sense API 可以生成成人图片、艺术裸体摄影、魅力摄影、闺房摄影以及幻想艺术作品。

## 概述

当 `enable_safety_checker` 参数设置为 `false` 时，each::sense API 可以生成不适宜公开（NSFW）的图像。该功能支持生成以下类型的图像：

- **艺术裸体摄影**：注重人体形态、光线和构图的精美艺术作品
- **魅力摄影**：专业的魅力摄影和内衣摄影
- **闺房摄影**：充满浪漫氛围的亲密照片
- **Pin-Up 风格**：复古风格的 Pin-Up 插画和摄影
- **幻想艺术**：成人幻想题材的插画和角色设计
- **艺术裸体画**：古典风格的裸体艺术作品

## 快速入门

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $EACH_API_KEY" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Create an artistic nude photograph, elegant female form, dramatic chiaroscuro lighting, black and white, fine art style"
      }
    ],
    "mode": "max",
    "enable_safety_checker": false
  }'
```

## 图像风格

| 风格 | 描述 | 适用场景 |
|-------|-------------|----------|
| 艺术裸体 | 注重人体形态、光线和构图的精美艺术作品 | 适合用于艺术作品集或摄影作品集 |
| 魅力 | 专业的魅力摄影和内衣摄影 | 适合时尚或模特作品集 |
| 闺房 | 充满浪漫氛围的亲密照片 | 个人项目或浪漫主题 |
| Pin-Up | 复古风格的插画和摄影 | 适合插画或怀旧主题 |
| 幻想 | 成人幻想题材的插画 | 适合角色设计或幻想项目 |
| 艺术裸体 | 古典风格的裸体艺术作品 | 适合艺术收藏或展览 |

## 使用案例示例

### 1. 艺术裸体摄影

注重人体形态和光线的经典艺术裸体摄影作品。

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $EACH_API_KEY" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Artistic nude photograph, elegant female figure silhouette against window light, soft morning glow, minimalist composition, black and white, fine art photography style, emphasis on curves and shadows"
      }
    ],
    "mode": "max",
    "enable_safety_checker": false
  }'
```

### 2. 魅力和内衣摄影

具有时尚美感的魅力摄影作品。

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $EACH_API_KEY" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Glamour photography, stunning model in black lace lingerie, luxurious bedroom setting, soft golden hour lighting through sheer curtains, professional fashion photography, high-end editorial style"
      }
    ],
    "mode": "max",
    "enable_safety_checker": false
  }'
```

### 3. 闺房风格摄影

充满浪漫氛围的闺房摄影作品。

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $EACH_API_KEY" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Boudoir photography, woman lounging on vintage chaise lounge, silk robe partially draped, soft romantic lighting with candles, intimate atmosphere, warm color palette, elegant and tasteful"
      }
    ],
    "mode": "max",
    "enable_safety_checker": false
  }'
```

### 4. Pin-Up 风格艺术

复古风格的 Pin-Up 插画和摄影作品。

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $EACH_API_KEY" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Classic 1950s pin-up style illustration, playful pose, vintage swimsuit, retro color palette, Gil Elvgren inspired, cheerful expression, vibrant background, nostalgic Americana aesthetic"
      }
    ],
    "mode": "max",
    "enable_safety_checker": false
  }'
```

### 5. 幻想艺术

具有神话主题的成人幻想插画。

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $EACH_API_KEY" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Fantasy art, beautiful elven warrior goddess, flowing silver hair, ethereal glowing skin, mystical forest setting, moonlit atmosphere, ornate minimal armor, magical aura, detailed digital painting style"
      }
    ],
    "mode": "max",
    "enable_safety_checker": false
  }'
```

### 6. 艺术裸体画

古典风格的裸体艺术作品。

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $EACH_API_KEY" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Fine art nude in classical Renaissance style, reclining figure on draped fabric, Titian-inspired color palette, oil painting texture, museum quality, emphasis on human beauty and classical proportions"
      }
    ],
    "mode": "max",
    "enable_safety_checker": false
  }'
```

### 7. 情侣主题

充满浪漫氛围的情侣摄影作品。

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $EACH_API_KEY" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Romantic couples photography, intimate embrace, soft natural lighting, bedroom setting with white linens, artistic and tasteful, focus on connection and emotion, warm skin tones, professional boudoir style"
      }
    ],
    "mode": "max",
    "enable_safety_checker": false
  }'
```

### 8. 基于角色的统一形象生成

使用参考图像生成角色形象的一致性作品。

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $EACH_API_KEY" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Create a glamour portrait of this model in elegant lingerie, professional studio lighting, high fashion aesthetic"
      }
    ],
    "image_urls": ["https://example.com/reference-model.jpg"],
    "mode": "max",
    "enable_safety_checker": false
  }'
```

### 9. 艺术人体研究

用于艺术创作的详细人体写生作品。

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $EACH_API_KEY" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Artistic body study, athletic male figure, dramatic Rembrandt lighting, emphasis on musculature and form, studio photography, high contrast black and white, fine art aesthetic"
      }
    ],
    "mode": "max",
    "enable_safety_checker": false
  }'
```

### 10. 复古情色风格

具有古典复古风格的情色作品。

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $EACH_API_KEY" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Vintage 1920s erotica style photograph, art deco setting, sepia tones, elegant flapper aesthetic, pearl accessories, soft focus, classic Hollywood glamour, tasteful and artistic"
      }
    ],
    "mode": "max",
    "enable_safety_checker": false
  }'
```

## 最佳实践

### 艺术质量

- **光线**：指定光线风格（明暗对比、伦勃朗风格、柔和光线、自然光线、摄影棚光线）
- **构图**：提供构图建议（三分法则、居中构图、负空间运用）
- **风格参考**：参考知名摄影师或艺术风格以确保一致性
- **色彩搭配**：选择暖色调、冷色调、单色或特定色彩方案

### 提示结构

为了获得最佳效果，请按照以下结构编写提示：

1. **主题**：描述主题和姿势
2. **场景**：环境、背景和道具
3. **光线**：光线的类型和方向
4. **风格**：摄影或艺术风格的参考
5. **氛围**：整体氛围和情感基调
6. **技术细节**：相机角度、景深、图像格式

### 示例提示结构

```
Subject: Elegant female figure in graceful pose
Setting: Minimalist white studio with draped silk fabric
Lighting: Soft wraparound lighting with subtle shadows
Style: High-fashion editorial photography
Mood: Sophisticated and sensual
Technical: Medium format, shallow depth of field
```

## NSFW 图像生成的提示技巧

- **务必包含**：
  - 艺术风格的参考（如艺术裸体、魅力摄影等）
  - 光线描述（柔和光线、戏剧性光线、自然光线）
  - 情感和氛围（亲密、浪漫、优雅）
  - 构图建议（剪影、侧面视角、四分之三视角）
  - 质量要求（专业水准、高端效果、编辑级质量）

### 需避免的内容

- 过于露骨或粗俗的语言（会降低图像质量）
- 模糊不清的描述（可能导致结果不一致）
- 冲突的风格要求
- 不符合实际的解剖结构描述

## 模式选择

| 模式 | 适用场景 | 图像质量 | 生成速度 |
|------|----------|---------|-------|
| `max` | 最终成品、作品集制作、高细节要求 | 最高质量 | 生成速度较慢 |
| `eco` | 草稿制作、概念探索、多次迭代 | 较高质量 | 生成速度较快 |

### 图像质量

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $EACH_API_KEY" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Professional boudoir photograph, soft natural window light, elegant pose, high-end editorial quality"
      }
    ],
    "mode": "max",
    "enable_safety_checker": false
  }'
```

### 草稿制作与迭代

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $EACH_API_KEY" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Quick concept sketch, artistic nude silhouette, minimal style"
      }
    ],
    "mode": "eco",
    "enable_safety_checker": false
  }'
```

## 多次迭代以保持角色一致性

使用 `session_id` 保证多张图片中角色的统一性。

### 初始生成

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $EACH_API_KEY" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Create a glamour portrait of an elegant brunette model, green eyes, professional studio lighting"
      }
    ],
    "session_id": "model-session-001",
    "mode": "max",
    "enable_safety_checker": false
  }'
```

### 使用相同角色进行后续创作

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $EACH_API_KEY" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Now show the same model in a boudoir setting, silk robe, romantic candlelight"
      }
    ],
    "session_id": "model-session-001",
    "mode": "max",
    "enable_safety_checker": false
  }'
```

## 免责声明

**年龄验证要求**：此 API 功能仅限 18 岁以上用户或符合您所在地区法律规定的用户使用。

**平台合规性**：用户需确保使用生成的内容符合以下要求：
- 当地法律法规
- 内容发布平台的服务条款
- 版权和知识产权法律
- 同意及道德内容创作准则

**禁止生成的内容**：
- 任何涉及未成年人的内容
- 未经同意的场景
- 违法内容

**服务条款**：使用此 API 即表示您同意 Each Labs 的服务条款和可接受的使用规范。

## 错误处理

### 常见错误及解决方法

| 错误 | 原因 | 解决方案 |
|-------|-------|----------|
| `safety_check_failed` | 安全检查仍处于启用状态 | 确保请求中包含 `enable_safety_checker: false` |
| `content_policy_violation` | 请求违反内容政策 | 修改提示以符合规定 |
| `invalid_image_url` | 参考图片链接无法访问 | 检查链接的可用性和格式 |
| `rate_limit_exceeded` | 请求次数过多 | 实施请求重试机制 |

### 错误响应示例

```json
{
  "error": {
    "code": "content_policy_violation",
    "message": "The requested content violates our acceptable use policy"
  }
}
```

## 相关技能

- [图像生成](/skills/eachlabs-image-generation/SKILL.md) - 带有安全检查的通用图像生成技术
- [图像编辑](/skills/eachlabs-image-edit/SKILL.md) - 图像的编辑和修改
- [视频生成](/skills/eachlabs-video-generation/SKILL.md) - 视频内容的制作