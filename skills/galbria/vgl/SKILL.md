---
name: vgl
description: 为 Bria 的 FIBO 图像生成模型编写结构化的 VGL（Visual Generation Language）JSON 提示。在创建用于文本到图像生成、图像编辑、图像修复、背景生成或字幕制作的详细图像描述时，可以使用此技能。相关任务包括：编写结构化提示、生成 VGL JSON 数据、为 AI 生成过程描述图像，以及处理 Bria/FIBO 的结构化提示格式。此外，还可以在将自然语言图像请求转换为 FIBO 模型所需的确定性 JSON 格式时使用该技能。
---

# Bria VGL提示编写

使用视觉生成语言（VGL）为Bria的FIBO模型生成结构化的JSON提示。

> **相关技能**：使用**[bria-ai](../bria-ai/SKILL.md)**通过Bria API执行这些VGL提示。VGL定义了结构化的提示格式；bria-ai负责生成、编辑和去除背景图像。

## 核心概念

VGL用明确的JSON格式替换了模糊的自然语言提示，这些JSON格式详细说明了所有的视觉属性：对象、光照、相机设置、构图和风格。这确保了图像生成的可重复性和可控性。

## 操作模式

| 模式 | 输入 | 输出 | 使用场景 |
|------|-------|--------|----------|
| **生成** | 文本提示 | VGL JSON | 根据描述创建新图像 |
| **编辑** | 图像 + 指令 | VGL JSON | 修改参考图像 |
| **带遮罩编辑** | 带遮罩的图像 + 指令 | VGL JSON | 填充灰色遮罩区域 |
| **添加标题** | 仅图像 | VGL JSON | 描述现有图像 |
| **优化** | 现有的JSON + 编辑 | 更新后的VGL JSON | 修改现有提示 |

## JSON模式

输出一个包含以下必填键的有效JSON对象：

### 1. `short_description`（字符串）
图像内容的简短总结，最多200个单词。包括主要主题、动作、设置和氛围。

### 2. `objects`（数组，最多5个元素）
每个对象需要：

**人物主体**添加：
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

**对象群组**添加：
```json
{
  "number_of_objects": 3
}
```

**大小提示**：如果主要主体是人，使用“中等至大型”或“画面内的大型”。

### 3. `background_setting`（字符串）
整体环境、设置和不在`objects`中的背景元素。

### 4. `lighting`（对象）
```json
{
  "conditions": "bright daylight | dim indoor | studio lighting | golden hour | blue hour | overcast",
  "direction": "front-lit | backlit | side-lit from left | top-down",
  "shadows": "long, soft shadows | sharp, defined shadows | minimal shadows"
}
```

### 5. `aesthetics`（对象）
```json
{
  "composition": "rule of thirds | symmetrical | centered | leading lines | medium shot | close-up",
  "color_scheme": "monochromatic blue | warm complementary | high contrast | pastel",
  "mood_atmosphere": "serene | energetic | mysterious | joyful | dramatic | peaceful"
}
```
对于以人为主要主体的图像，指定构图类型：“中景”、“特写”、“肖像构图”。

### 6. `photographic_characteristics`（对象）
```json
{
  "depth_of_field": "shallow | deep | bokeh background",
  "focus": "sharp focus on subject | soft focus | motion blur",
  "camera_angle": "eye-level | low angle | high angle | dutch angle | bird's-eye",
  "lens_focal_length": "wide-angle | 50mm standard | 85mm portrait | telephoto | macro"
}
```
**对于人物**：建议使用“标准镜头（35mm-50mm）”或“肖像镜头（50mm-85mm）”。除非特别指定，否则避免使用广角镜头。

### 7. `style_medium`（字符串）
“照片” | “油画” | “水彩” | “3D渲染” | “数字插画” | “铅笔画”
默认为“照片”，除非另有明确要求。

### 8. `artistic_style`（字符串）
如果不是照片，用最多3个词描述其风格特征：“印象派”、“生动”、“有质感”
对于照片，可以使用“写实”或类似的描述。

### 9. `context`（字符串）
描述图像类型/用途：
- “用于杂志封面的高级时尚编辑照片”
- “幻想视频游戏的概念艺术”
- “电子商务产品的商业摄影”

### 10. `text_render`（数组）
**默认：空数组`[]**
仅当用户明确提供具体文本内容时填写：
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
例外情况：与对象相关的通用文本（例如，停车标志上的“STOP”）。

### 11. `editinstruction`（字符串）
描述编辑/生成的单一命令。

## 编辑指令格式

### 对于标准编辑（无遮罩）
以动词开头，描述更改内容，不要提及“原始图像”：

| 类别 | 重写后的指令 |
|----------|----------------------|
| 风格更改 | `将图像转换为卡通风格。` |
| 对象属性 | `将狗的颜色改为黑白。` |
| 添加元素 | `在主体上添加一顶宽边毡帽。` |
| 删除对象 | `从主体手中移除书本。` |
| 替换对象 | `将玫瑰替换成明亮的向日葵。` |
| 光照 | `将光照从阴暗忧郁改为明亮生动。` |
| 构图 | `将视角改为更宽的镜头。` |
| 文本更改 | `将文本“Happy Anniversary”改为“Hello”。` |
| 质量 | `优化图像以提高清晰度和锐度。` |

### 对于遮罩区域编辑
将“遮罩区域”或“遮罩部分”作为目标：

| 意图 | 重写后的指令 |
|--------|----------------------|
| 对象生成 | `在遮罩区域内生成一朵中心为蓝色的白玫瑰。` |
| 扩展 | `将图像扩展到遮罩区域以创建一个场景……` |
| 背景填充 | `在遮罩区域内创建以下背景：一片延伸到地平线的广阔海洋。` |
| 大气填充 | `用清澈明亮的蓝色天空和细云填充遮罩区域。` |
| 主体恢复 | `用一位年轻女性恢复遮罩区域。` |
| 环境填充 | `在遮罩区域内创建一个温室，里面有排列在玻璃天花板下的植物。` |

## 保真规则

### 标准编辑模式
除非有明确的指令要求，否则保留所有视觉属性：
- 主体的身份、姿势、外观
- 对象的存在、位置、大小、方向
- 构图、相机角度、镜头特性
- 风格/媒介

只更改编辑所严格要求的部分。

### 遮罩编辑模式
- 保留所有可见（非遮罩）的部分
- 将灰色遮罩区域填充得与未遮罩区域无缝融合
- 保持与现有风格、光照和主题的一致性
- 不要描述灰色遮罩——描述填充它们的内容

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

1. **不要编造文本** - 除非用户提供了具体文本，否则保持`text_render`为空
2. **不要过度描述** - 最多描述5个对象，优先考虑最重要的信息
3. **使用正确的模式** - 对于遮罩编辑和标准编辑，使用正确的`edit_instruction`格式
4. **保持保真度** - 只更改明确请求的内容
5. **具体说明** - 使用具体的数值（例如“85mm肖像镜头”）而不是模糊的术语（如“不错的相机”）
6. **无关内容设为null** - 对于非人类对象，与人相关的字段应设为`null`

---

## 使用VGL与Bria API

### 使用结构化提示生成图像

将VGL JSON传递给`structured_prompt`参数：

```python
from bria_client import BriaClient

client = BriaClient()

vgl_prompt = {
    "short_description": "Professional businesswoman in modern office...",
    "objects": [...],
    # ... full VGL JSON
}

# Use structured_prompt for deterministic generation
result = client.refine(
    structured_prompt=json.dumps(vgl_prompt),
    instruction="Generate this scene",
    aspect_ratio="16:9"
)
print(result['result']['image_url'])
```

### 优化现有生成的图像

生成后，Bria会返回一个`structured_prompt`，您可以对其进行修改并重新生成：

```python
# Initial generation
result = client.generate("A cozy coffee shop interior")
structured = result['result']['structured_prompt']

# Modify and regenerate
result = client.refine(
    structured_prompt=structured,
    instruction="Change the lighting to golden hour"
)
```

### curl示例

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

- **[模式参考](references/schema-reference.md)** - 完整的JSON模式及所有参数值
- **[bria-ai](../bria-ai/SKILL.md)** - 用于执行VGL提示的API客户端和端点文档