---
name: vgl
description: **对AI图像生成实现最大程度的控制——使用结构化的VGL（视觉生成语言）JSON格式来精确控制所有视觉属性。** 通过JSON明确指定对象的位置、光照方向、相机角度、镜头焦距、构图、配色方案以及艺术风格等参数，而非依赖模糊的自然语言描述。当您需要可复制的图像生成结果、对场景构图有精确的控制要求，或者希望将自然语言中的图像请求转换为适用于Bria FIBO模型的结构化JSON格式时，可运用这一技术。该功能适用于需要结构化提示、可控图像生成、确定性图像描述，以及符合Bria/FIBO格式要求的场景。
license: MIT
metadata:
  author: Bria AI
  version: "1.2.1"
---
# Bria VGL — 完全控制图像生成

通过结构化的 JSON 数据来定义每一个视觉属性，而不是依赖自然语言来准确表达需求。VGL（Visual Generation Language）允许您对 Bria 的 FIBO 模型中的对象、光照、相机设置、构图和风格进行明确、可控的调整。

> **相关技能**：使用 **[bria-ai](../bria-ai/SKILL.md)** 通过 Bria API 来执行这些 VGL 命令。VGL 负责定义结构化的控制格式，而 bria-ai 负责图像的生成、编辑和背景去除工作。

## 核心概念

VGL 用明确的 JSON 数据替换了模糊的自然语言指令，这些 JSON 数据详细规定了所有的视觉属性：对象、光照、相机设置、构图和风格。这确保了图像生成的可重复性和可控性。

## 操作模式

| 模式 | 输入 | 输出 | 使用场景 |
|------|-------|--------|----------|
| **生成** | 文本指令 | VGL JSON | 根据描述创建新图像 |
| **编辑** | 图像 + 指令 | VGL JSON | 修改参考图像 |
| **带遮罩编辑** | 带遮罩的图像 + 指令 | VGL JSON | 填充灰色遮罩区域 |
| **添加标题** | 仅图像 | VGL JSON | 为现有图像添加描述 |
| **优化** | 现有的 JSON 数据 + 编辑 | 更新后的 VGL JSON | 修改现有指令 |

## JSON 数据结构

输出一个包含以下必填键的有效 JSON 对象：

### 1. `short_description` (字符串)
图像内容的简短总结，最多 200 个单词。应包括主要主题、动作、设置和氛围。

### 2. `objects` (数组，最多 5 个元素)
每个对象需要包含以下信息：

**人物主体**：
```json
{
  "pose": "Body position description",
  "expression": "winking | joyful | serious | surprised | calm",
  "clothing": "Attire description",
  "action": "What the person is doing",
  "gender": "Gender description",
  "skin_tone_and_texture": "Skin appearance"
}
```

**对象群组**：
```json
{
  "number_of_objects": 3
}
```

**大小提示**：如果主要主体是人，使用 `"medium-to-large"` 或 `"large within frame"`。

### 3. `background_setting` (字符串)
整体环境、背景元素（不在 `objects` 中的元素）。

### 4. `lighting` (对象)
```json
{
  "conditions": "bright daylight | dim indoor | studio lighting | golden hour | blue hour | overcast",
  "direction": "front-lit | backlit | side-lit from left | top-down",
  "shadows": "long, soft shadows | sharp, defined shadows | minimal shadows"
}
```

### 5. `aesthetics` (对象)
```json
{
  "composition": "rule of thirds | symmetrical | centered | leading lines | medium shot | close-up",
  "color_scheme": "monochromatic blue | warm complementary | high contrast | pastel",
  "mood_atmosphere": "serene | energetic | mysterious | joyful | dramatic | peaceful"
}
```
对于以人物为主体的图像，指定构图类型：`"medium shot"`、`"close-up"`、`"portrait composition"`。

### 6. `photographic_characteristics` (对象)
```json
{
  "depth_of_field": "shallow | deep | bokeh background",
  "focus": "sharp focus on subject | soft focus | motion blur",
  "camera_angle": "eye-level | low angle | high angle | dutch angle | bird's-eye",
  "lens_focal_length": "wide-angle | 50mm standard | 85mm portrait | telephoto | macro"
}
```
**对于人物**：建议使用 `"standard lens (35mm-50mm)"` 或 `"portrait lens (50mm-85mm)"`。除非特别指定，否则避免使用广角镜头。

### 7. `style_medium` (字符串)
`"photograph"` | `"oil painting"` | `"watercolor"` | `"3D render"` | `"digital illustration"` | `"pencil sketch"`
默认值为 `"photograph"`，除非另有明确要求。

### 8. `artistic_style` (字符串)
如果不是照片，用最多 3 个词描述风格特征：`"impressionistic, vibrant, textured"`
对于照片，可以使用 `"realistic"` 或类似的描述。

### 9. `context` (字符串)
描述图像的类型/用途：
- `"High-fashion editorial photograph for magazine spread"`（用于杂志封面的高时尚编辑照片）
- `"Concept art for fantasy video game"`（用于奇幻视频游戏的概念艺术）
- `"Commercial product photography for e-commerce"`（用于电子商务的商品摄影）

### 10. `text_render` (数组)
**默认值：空数组 `[]`
仅在用户明确提供文本内容时填写：
```json
{
  "text": "Exact text from user (never placeholder)",
  "location": "center | top-left | bottom",
  "size": "small | medium | large",
  "color": "white | red | blue",
  "font": "serif typeface | sans-serif | handwritten | bold impact",
  "appearance_details": "Metallic finish | 3D effect | etc."
}
```
**例外情况**：某些对象需要包含特定的文本（例如，停止标志上的 "STOP"）。

### 11. `editinstruction` (字符串)
描述编辑或生成操作的单一命令。

## 编辑指令格式

### 对于标准编辑（无遮罩）
以动词开头，描述具体修改内容，切勿提及“原始图像”：

| 类别 | 重新编写的指令 |
|----------|----------------------|
| 风格更改 | `将图像转换为卡通风格。` |
| 对象属性 | `将狗的颜色改为黑白。` |
| 添加元素 | `在主体上添加一顶宽边毡帽。` |
| 删除对象 | `从主体手中移除书本。` |
| 替换对象 | `将玫瑰替换成明亮的黄色向日葵。` |
| 光照 | `将光照从阴暗忧郁的风格改为明亮鲜艳的风格。` |
| 构图 | `将视角改为更宽广的构图。` |
| 文本更改 | `将文本 “Happy Anniversary” 更改为 “Hello”。` |
| 质量 | `优化图像以提高清晰度和锐度。` |

### 对于遮罩区域编辑
使用 “masked regions” 或 “masked area” 作为目标区域：

| 操作意图 | 重新编写的指令 |
|--------|----------------------|
| 对象生成 | `在遮罩区域内生成一朵中心为蓝色的白色玫瑰。` |
| 扩展区域 | `将图像扩展到遮罩区域，创建一个包含……的场景。` |
| 背景填充 | `在遮罩区域内创建以下背景：一片延伸到地平线的广阔海洋。` |
| 大气填充 | `用清澈明亮的蓝色天空和细云填充遮罩区域。` |
| 主体恢复 | `在遮罩区域内恢复一个年轻女性的图像。` |
| 环境填充 | `在遮罩区域内创建一个温室，里面有排列整齐的植物。` |

## 保真度规则

### 标准编辑模式
除非有明确的指令要求，否则保留所有视觉属性：
- 主体的身份、姿势、外观
- 对象的存在、位置、大小、方向
- 构图、相机角度、镜头特性
- 风格/媒介

仅修改编辑所必需的内容。

### 遮罩编辑模式
- 保留所有可见（未遮罩）的部分
- 将灰色遮罩区域填充成与未遮罩区域无缝融合的颜色
- 保持现有的风格、光照和主题一致
- 不要描述遮罩本身，而是描述填充遮罩区域的内容

## 示例输出

```json
{
  "short_description": "A professional businesswoman in a navy blazer stands confidently in a modern glass office, holding a tablet. Natural daylight streams through floor-to-ceiling windows, creating a warm, productive atmosphere.",
  "objects": [
    {
      "description": "A confident businesswoman in her 30s with shoulder-length dark hair, wearing a tailored navy blazer over a white blouse. She holds a tablet in her left hand while gesturing naturally with her right.",
      "location": "center-right",
      "relative_size": "large within frame",
      "shape_and_color": "Human figure, navy and white clothing",
      "texture": "smooth fabric, professional attire",
      "appearance_details": "Minimal jewelry, well-groomed professional appearance",
      "relationship": "Main subject, interacting with tablet",
      "orientation": "facing slightly left, three-quarter view",
      "pose": "Standing upright, relaxed professional stance",
      "expression": "confident, approachable smile",
      "clothing": "Tailored navy blazer, white silk blouse, dark trousers",
      "action": "Presenting or reviewing information on tablet",
      "gender": "female",
      "skin_tone_and_texture": "Medium warm skin tone, healthy smooth complexion"
    },
    {
      "description": "A modern tablet device with a bright display showing charts and graphs",
      "location": "center, held by subject",
      "relative_size": "small",
      "shape_and_color": "Rectangular, silver frame with illuminated screen",
      "texture": "smooth glass and metal",
      "appearance_details": "Thin profile, business application visible on screen",
      "relationship": "Held by businesswoman, focus of her attention",
      "orientation": "vertical, screen facing viewer at slight angle",
      "pose": null,
      "expression": null,
      "clothing": null,
      "action": null,
      "gender": null,
      "skin_tone_and_texture": null,
      "number_of_objects": null
    }
  ],
  "background_setting": "Modern corporate office interior with floor-to-ceiling windows overlooking a city skyline. Minimalist furniture in neutral tones, potted plants adding touches of green.",
  "lighting": {
    "conditions": "bright natural daylight",
    "direction": "side-lit from left through windows",
    "shadows": "soft, natural shadows"
  },
  "aesthetics": {
    "composition": "rule of thirds, medium shot",
    "color_scheme": "professional blues and neutral whites with warm accents",
    "mood_atmosphere": "confident, professional, welcoming"
  },
  "photographic_characteristics": {
    "depth_of_field": "shallow, background slightly soft",
    "focus": "sharp focus on subject's face and upper body",
    "camera_angle": "eye-level",
    "lens_focal_length": "portrait lens (85mm)"
  },
  "style_medium": "photograph",
  "artistic_style": "realistic",
  "context": "Corporate portrait photography for company website or LinkedIn professional profile.",
  "text_render": [],
  "edit_instruction": "Generate a professional businesswoman in a modern office environment holding a tablet."
}
```

## 常见错误

1. **不要随意编写文本** - 除非用户提供了具体的文本内容，否则保持 `text_render` 为空。
2. **不要过度描述** - 最多描述 5 个对象，优先考虑最重要的信息。
3. **使用正确的格式** - 根据编辑模式（带遮罩或无遮罩）使用正确的 `editInstruction` 格式。
4. **保持图像保真度** - 只修改明确请求的内容。
5. **具体说明** - 使用具体的数值（例如 “85mm 人像镜头”），而不是模糊的描述（如 “不错的相机”）。
6. **无关字段设为空值** - 对于非人物对象，与人物相关的字段应设为空值。

### 使用 curl 的示例

```bash
curl -X POST "https://engine.prod.bria-api.com/v2/image/generate" \
  -H "api_token: $BRIA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "structured_prompt": "{\"short_description\": \"...\", ...}",
    "prompt": "Generate this scene",
    "aspect_ratio": "16:9"
  }'
```

---

## 参考资料

- **[JSON 数据结构参考](references/schema-reference.md)** - 完整的 JSON 数据结构及所有参数值
- **[bria-ai](../bria-ai/SKILL.md)** - 用于执行 VGL 命令的 API 客户端和端点文档