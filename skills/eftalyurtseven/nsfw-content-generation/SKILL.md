---
name: nsfw-content-generation
description: 使用每个::sense API生成不适宜在工作场所（NSFW）的成人内容，同时禁用安全检查功能。该API支持创作艺术性的裸体、魅力、闺房、奇幻以及成人主题的内容，提供完全的创作自由。
metadata:
  author: eachlabs
  version: "1.0"
---
# 使用 each::sense 生成成人及成熟主题内容

通过 each::sense API 生成成人及成熟主题的内容，此时安全检查功能将被禁用。该技能支持创作艺术裸体照、魅力摄影、闺房照、奇幻艺术等成人主题的视觉作品。

**主要功能：**
- 艺术裸体与人体摄影
- 魅力与闺房摄影
- 奇幻与 pin-up 艺术
- 成熟主题的角色生成
- 通过 `session_id` 在多代作品中保持角色一致性
- 全面创作控制，无内容过滤

## 认证

```
Header: X-API-Key: <your-api-key>
```

请在 [eachlabs.ai](https://eachlabs.ai) 获取您的 API 密钥，并设置 `EACHLABS_API_KEY` 环境变量。

## 基础 URL

```
https://sense.eachlabs.run
```

## 快速入门

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate an artistic nude portrait with renaissance painting style, soft dramatic lighting",
    "mode": "max",
    "enable_safety_checker": false
  }'
```

该接口会返回服务器发送的事件（Server-Sent Events, SSE），包含实时进度和最终生成的输出内容。

## 内容类型

| 类型 | 描述 | 示例提示关键词 |
|------|-------------|------------------------|
| 艺术裸体 | 艺术风格的裸体摄影/绘画 | 古典、文艺复兴、人体研究、艺术感 |
| 魅力 | 精致成人模特 | 魅力、优雅、性感、时尚 |
| 闺房 | 亲密风格的卧室摄影 | 闺房、私密、浪漫、柔和光线 |
| Pin-Up | 复古/复古风格的 pin-up 艺术 | pin-up、复古、趣味性 |
| 奇幻 | 奇幻主题的成人艺术 | 奇幻、空灵、神话、魔法 |
| 电影风格 | 电影风格的成熟场景 | 电影感、戏剧性、情绪化、电影静止画面 |
| 美术品 | 博物馆级别的艺术作品 | 美术品、画廊、雕塑、古典风格 |
| 时尚编辑 | 杂志/编辑风格的内容 | 时尚编辑、高端、专业 |

## 请求格式

```json
{
  "message": "string (required) - Content description",
  "session_id": "string (optional) - Session ID for consistent characters",
  "mode": "string (optional, default: 'max') - Quality mode: 'max' or 'eco'",
  "image_urls": "array[string] (optional) - Reference images",
  "enable_safety_checker": "boolean (required for NSFW) - Set to false"
}
```

### 关键参数

| 参数 | 类型 | 默认值 | 描述 |
|-----------|------|---------|-------------|
| `message` | 字符串 | 必填 | 自然语言的内容描述 |
| `session_id` | 字符串 | 可空 | 用于在不同代作品中保持角色一致性 |
| `mode` | 字符串 | "max" | `max` = 最高质量；`eco` = 更快/更经济 |
| `image_urls` | 数组 | 可空 | 用于风格/姿势参考的图片链接 |
| `enable_safety_checker` | 布尔值 | true | **生成成人内容时必须设置为 false** |

## 使用案例示例

### 1. 艺术裸体肖像

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate an artistic nude portrait of a woman, renaissance painting style, soft chiaroscuro lighting, classical pose reminiscent of Botticelli, fine art gallery quality",
    "mode": "max",
    "enable_safety_checker": false
  }'
```

### 2. 魅力摄影

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a glamour photography shot, elegant woman in silk lingerie, luxurious bedroom setting, soft golden hour lighting through sheer curtains, high-end fashion magazine quality",
    "mode": "max",
    "enable_safety_checker": false
  }'
```

### 3. 闺房摄影

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate an intimate boudoir photograph, woman on a vintage chaise lounge, romantic candlelit atmosphere, soft focus, warm skin tones, tasteful and elegant composition",
    "mode": "max",
    "enable_safety_checker": false
  }'
```

### 4. 奇幻艺术

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a fantasy art scene, elven queen in a moonlit forest glade, ethereal beauty, flowing translucent fabrics, magical atmosphere with floating lights, sensual and mystical",
    "mode": "max",
    "enable_safety_checker": false
  }'
```

### 5. 复古 Pin-Up 风格

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a 1950s style pin-up illustration, playful pose, retro swimsuit, classic Vargas girl aesthetic, vibrant colors, vintage americana style",
    "mode": "max",
    "enable_safety_checker": false
  }'
```

### 6. 美术人体研究

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a classical figure study, graceful female form, marble sculpture aesthetic, dramatic studio lighting, museum quality fine art, anatomically elegant",
    "mode": "max",
    "enable_safety_checker": false
  }'
```

### 7. 电影风格的性感场景

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a cinematic film still, intimate moment between lovers, noir lighting with venetian blind shadows, moody atmosphere, art house film aesthetic",
    "mode": "max",
    "enable_safety_checker": false
  }'
```

### 8. 时尚编辑裸体照

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a high fashion editorial photograph, artistic partial nude, avant-garde styling with dramatic jewelry, stark white studio background, Helmut Newton inspired composition",
    "mode": "max",
    "enable_safety_checker": false
  }'
```

### 9. 多代作品中的角色一致性

使用 `session_id` 保持角色在不同代作品中的连贯性：

```bash
# First image - establish character
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a glamour portrait, woman with long auburn hair, green eyes, elegant features, wearing a silk robe, soft window lighting",
    "session_id": "glamour-series-001",
    "mode": "max",
    "enable_safety_checker": false
  }'

# Second image - same character, different scene
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate the same woman from the previous image, now in an outdoor setting, sheer summer dress, golden hour beach scene",
    "session_id": "glamour-series-001",
    "mode": "max",
    "enable_safety_checker": false
  }'

# Third image - same character, artistic pose
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate the same woman in an artistic nude pose, classical sculpture aesthetic, studio lighting",
    "session_id": "glamour-series-001",
    "mode": "max",
    "enable_safety_checker": false
  }'
```

### 8. 基于参考的生成

使用 `image_urls` 提供风格或姿势的参考：

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a glamour photograph matching the pose and lighting style from this reference image, but with a different model and setting",
    "image_urls": ["https://example.com/reference-pose.jpg"],
    "mode": "max",
    "enable_safety_checker": false
  }'
```

## 模式选择

### MAX 模式（推荐用于成人内容）

使用最高质量的模型，生成细节丰富、精致的作品。适合最终成品和发布。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate artistic boudoir photography...",
    "mode": "max",
    "enable_safety_checker": false
  }'
```

### ECO 模式

生成速度更快，成本更低。适合测试提示和生成草图。

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate artistic boudoir photography...",
    "mode": "eco",
    "enable_safety_checker": false
  }'
```

## 最佳实践

### 艺术创作技巧

1. **使用专业术语** - 参考美术、摄影风格和古典美学
2. **描述光线** - 明暗对比、黄金时刻、柔和散射光、戏剧性阴影
3. **引用艺术流派** - 文艺复兴、巴洛克、新艺术、当代
4. **强调构图** - 三分法则、引导线、负空间

### 高质量提示技巧

1. **详细描述** - 包括场景、氛围、光线和艺术风格
2. **使用质量修饰词** - “画廊级质量”、“高端时尚编辑”、“博物馆级”
3. **指定相机参数** - 深度场、焦距、镜头特性
4. **明确氛围** - 浪漫、戏剧性、趣味性、神秘、优雅

### 内容指导原则

1. **艺术意图** - 将请求视为艺术或专业摄影
2. **同意主题** - 所有生成内容均描绘虚构的、自愿参与的成年人
3. **平台合规** - 确保生成内容符合平台政策
4. **商业用途** - 查阅 EachLabs 的商业使用条款

### 提示编写技巧

**有效的提示结构：**
```
[Subject description] + [Setting/environment] + [Lighting] + [Style/aesthetic] + [Quality modifiers]
```

**示例提示：**
```
"Elegant woman with flowing dark hair + luxurious marble bathroom setting +
soft candlelight with warm reflections + Helmut Newton inspired glamour +
fashion magazine quality, 8K, detailed"
```

## 年龄验证免责声明

此 API 功能仅限成人用户使用。通过设置 `enable_safety_checker: false`，您表示：

1. 您在所在司法管辖区已达到观看和创作成人内容的法定年龄
2. 您不会生成涉及未成年人的内容
3. 您将遵守所有关于成人内容的法律法规
4. 您对生成内容的使用和传播负责
5. 生成内容为虚构内容，除非获得明确同意，否则不代表真实人物

## 错误处理

### 常见错误

| 错误信息 | 原因 | 解决方案 |
|--------------|-------|----------|
| `安全检查失败` | 忘记禁用安全检查功能 | 添加 `"enable_safety_checker": false` |
| `生成失败：HTTP 422` | 资源不足 | 在 eachlabs.ai 充值 |
| `API 密钥无效` | API 密钥缺失或错误 | 检查 `EACHLABS_API_KEY` |
| 超过请求限制 | 请求次数过多 | 等待片刻后重试 |

## 超时设置

对于复杂的生成任务，可以增加超时时间：

```bash
curl --max-time 600 -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate detailed artistic content...",
    "mode": "max",
    "enable_safety_checker": false
  }'
```

## SSE 响应格式

该接口会返回服务器发送的事件（Server-Sent Events, SSE），包含实时更新信息。

需要关注的关键事件：

| 事件 | 描述 |
|-------|-------------|
| `thinking_delta` | 人工智能的实时推理过程 |
| `status` | 当前操作状态 |
| `generation_response` | 生成的图片 URL |
| `complete` | 包含所有输出的最终事件 |
| `error` | 错误信息 |

更多事件详情请参阅 [SSE-EVENTS.md](./references/SSE-EVENTS.md)。

## 相关技能

- [each-sense](../each-sense/SKILL.md) - 通用内容生成
- [ai-influencer-generation](../ai-influencer-generation/SKILL.md) - 一致的角色创建
- [eachlabs-image-generation](../eachlabs-image-generation/SKILL.md) - 标准图像生成