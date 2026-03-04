---
name: NSFW Video Generation
description: >
  **使用 each::sense API 生成成人视频内容（禁用安全检查功能）**
  **注意：**  
  此操作涉及违反法律法规的行为，请确保您不会使用此功能来制作或传播任何非法内容。
metadata:
  category: video-generation
  subcategory: adult-content
  api_endpoint: https://sense.eachlabs.run/chat
  content_rating: adult
  requires_age_verification: true
tags:
  - nsfw
  - video-generation
  - adult-content
  - artistic
  - mature-themes
---
# NSFW视频生成

使用each::sense API（禁用安全检查功能）生成成人视频内容、艺术裸体视频以及主题成熟的动画。

## 概述

当`enable_safety_checker`参数设置为`false`时，each::sense API可以生成成人视频内容。该功能支持以下类型的视频制作：

- **艺术裸体视频**：受艺术启发的裸体摄影作品
- **魅力风格视频**：时尚与内衣相关的视频制作
- **闺房风格视频**：具有浪漫氛围的卧室场景视频
- **奇幻主题视频**：神话或奇幻主题的成人内容
- **情侣主题视频**：浪漫的情侣互动场景

> **重要提示**：所有请求都必须包含`"enable_safety_checker": false`，才能生成不适宜公开的内容。

## 快速入门

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Create an artistic nude video of a woman in a classical renaissance painting style, soft natural lighting, elegant pose"
      }
    ],
    "mode": "video",
    "enable_safety_checker": false
  }'
```

## 视频类型

| 类型 | 描述 | 适用场景 |
|------|-------------|----------|
| 艺术风格 | 受艺术启发的裸体摄影，古典美学 | 适合用于博物馆级别的艺术展示 |
| 魅力风格 | 时尚感强的内衣搭配，优雅的拍摄风格 | 适合专业模特的作品集 |
| 闺房风格 | 具有浪漫氛围的卧室场景，柔和的灯光 | 适合个人浪漫用途 |
| 奇幻风格 | 神话或角色扮演主题的视频 | 适合创意故事讲述 |
| 情侣风格 | 浪漫的情侣互动场景 | 适合表达亲密关系 |
| 舞蹈风格 | 强调感官体验和舞蹈动作的视频 | 适合表演艺术 |

## 使用案例示例

### 1. 艺术风格视频

制作具有古典美学的艺术裸体视频。

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Generate an artistic nude video inspired by Botticelli, woman emerging from water, flowing hair, golden hour lighting, slow graceful movement, renaissance painting aesthetic"
      }
    ],
    "mode": "video",
    "enable_safety_checker": false
  }'
```

### 2. 魅力/内衣风格视频

专业的魅力风格内衣搭配视频制作。

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Create a glamour video of a model in black lace lingerie, luxury bedroom setting, soft studio lighting, slow confident walk toward camera, high fashion editorial style"
      }
    ],
    "mode": "video",
    "enable_safety_checker": false
  }'
```

### 3. 闺房风格视频

具有柔和浪漫氛围的闺房风格视频。

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Generate a boudoir video, woman in silk robe by window, morning sunlight streaming through sheer curtains, gentle movement, intimate atmosphere, warm color palette"
      }
    ],
    "mode": "video",
    "enable_safety_checker": false
  }'
```

### 4. 舞蹈风格视频

强调舞蹈动作和感官体验的视频。

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Create a sensual contemporary dance video, woman in flowing sheer fabric, dramatic spotlight, fluid graceful movements, artistic choreography, black background"
      }
    ],
    "mode": "video",
    "enable_safety_checker": false
  }'
```

### 5. 奇幻风格视频

具有神话或奇幻主题的成人视频。

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Generate a fantasy video of a forest nymph, ethereal nude figure with flower crown, enchanted forest setting, magical glowing particles, mystical atmosphere, slow ethereal movement"
      }
    ],
    "mode": "video",
    "enable_safety_checker": false
  }'
```

### 6. 情侣风格视频

浪漫的情侣互动场景视频。

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Create a romantic couples video, intimate embrace on bed with white sheets, soft natural lighting, tender moment, tasteful artistic framing, warm romantic atmosphere"
      }
    ],
    "mode": "video",
    "enable_safety_checker": false
  }'
```

### 7. 图片转视频动画

通过提供图片URL，将静态图片转换为成人视频内容。

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Animate this artistic nude photo, add subtle breathing movement, gentle hair flowing, soft blinking, maintain the elegant pose and lighting"
      }
    ],
    "mode": "video",
    "image_urls": ["https://example.com/artistic-photo.jpg"],
    "enable_safety_checker": false
  }'
```

### 8. 一致的角色视频系列

使用`session_id`生成多个相关角色视频，保持角色连贯性。

```bash
# First video in series
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Create a glamour video introducing a character: tall brunette model, green eyes, elegant features, in a luxury penthouse, wearing silk robe, walking to window"
      }
    ],
    "mode": "video",
    "session_id": "glamour-series-001",
    "enable_safety_checker": false
  }'

# Second video continuing the series
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Continue with the same model, now she removes the robe to reveal lingerie, turns to face camera with confident expression"
      }
    ],
    "mode": "video",
    "session_id": "glamour-series-001",
    "enable_safety_checker": false
  }'
```

### 9. 水池/海滩场景

户外拍摄的性感视频，采用自然环境。

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Generate a video of a woman in a revealing bikini at a luxury pool, sunset golden hour lighting, slow motion water droplets, cinematic quality, sensual atmosphere"
      }
    ],
    "mode": "video",
    "enable_safety_checker": false
  }'
```

### 10. 复古风格

具有经典怀旧风格的成人视频。

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Create a 1950s pin-up style video, woman in vintage lingerie and stockings, classic boudoir setting, film grain effect, soft glamour lighting, playful poses"
      }
    ],
    "mode": "video",
    "enable_safety_checker": false
  }'
```

## 最佳实践

### 电影级制作标准

- **灯光**：指定灯光条件（黄金时刻、柔和的摄影棚灯光或自然窗光）
- **摄像机运动**：描述摄像机的运动方式（缓慢平移、固定镜头、跟踪拍摄）
- **构图**：注意构图细节（特写、全身镜头、艺术角度）
- **色彩搭配**：通过色彩营造氛围（暖色调、富有情绪的阴影、高调色彩）

### 文化审美

- 注重艺术价值和美学品质
- 使用富有表现力的语言而非露骨的描述
- 强调优雅、美丽和艺术性
- 可以参考古典艺术风格来提升作品质量

### 技术规格

- 视频默认以高分辨率生成
- 每个视频的时长通常为4-8秒
- 如需更长的视频内容，可以使用`session_id`来创建连续的系列

## NSFW视频创作提示

| 应该做 | 应该避免 |
|----|----|
- 使用专业的艺术术语 | 使用粗俗或低俗的语言 |
- 描述灯光和氛围 | 过于详细的露骨描述 |
- 参考真实的艺术风格 | 提出不切实际的解剖结构要求 |
- 明确指定摄像机运动方式 | 给出相互矛盾的拍摄指令 |
- 提供详细的环境描述 | 使用模糊或简化的描述

### 有效的提示结构

```
[Subject description] + [Setting/Environment] + [Lighting] + [Movement/Action] + [Style/Aesthetic]
```

示例：
> “一位金发女性，身处烛光照亮的巴洛克风格卧室中，温暖的金色灯光下，缓缓转向镜头，拍摄风格类似文艺复兴时期的画作”

## 模式选择

| 模式 | 适用场景 |
|------|----------|
| `video` | 根据文本提示生成新的成人视频 |
| `video` + `image_urls` | 将静态图片转换为视频 |

## 多次请求时的会话管理

使用`session_id`来确保多个视频中角色的连贯性：

```bash
curl -X POST "https://sense.eachlabs.run/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Create the opening scene of an artistic video series: introduce a dancer in an empty studio"
      }
    ],
    "mode": "video",
    "session_id": "dancer-series-2024",
    "enable_safety_checker": false
  }'
```

**会话连贯性的好处：**
- 角色在多个视频中保持一致的外观
- 可以构建连贯的故事情节
- 适合制作系列化内容
- 保持风格和美学的统一性

## 免责声明

本API仅用于合法创作成人内容。用户必须：
- 满足所在地区的法定年龄要求
- 遵守所有适用的法律和法规
- 不得生成涉及未成年人的内容
- 不得制作未经同意的内容
- 尊重知识产权
- 负责任地使用生成的内容

API提供者保留监控使用情况并终止违规访问的权利。

## 错误处理

| 错误类型 | 原因 | 解决方案 |
|-------|-------|----------|
| `safety_filter_triggered` | 安全检查功能仍被启用 | 确保请求中包含`enable_safety_checker: false` |
| `invalid_mode` | 指定的模式无效 | 使用`mode: "video"`进行视频生成 |
| `rate_limit_exceeded` | 请求次数过多 | 实施指数级延迟策略 |
| `invalid_session` | 会话已过期或无效 | 生成新的`session_id` |
| `content_policy_violation` | 请求违反使用条款 | 查看内容政策指南 |

## 响应格式

API返回Server-Sent Events (SSE)。详细响应处理方式请参考[SSE Events Reference](references/SSE-EVENTS.md)。

## 相关技能

- [视频生成](../eachlabs-video-generation/SKILL.md) - 标准视频生成技术
- [图片生成](../eachlabs-image-generation/SKILL.md) - 静态图片处理技术
- [视频编辑](../eachlabs-video-edit/SKILL.md) - 视频编辑与优化技术