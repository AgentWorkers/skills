---
name: gemini-nano-banana-pro-portraits
description: 使用 Gemini Nano Banana Pro 生成超写实的肖像图像，该工具配备了全面的 JSON 配置模板。适用于制作电影级质量的肖像照片、健身摄影作品或逼真的角色图像。配置文件包含完整的 JSON 结构，涵盖了提示语设置、主体信息、服装、姿势、环境、光线效果以及技术参数等详细内容。
---

# Gemini Nano Banana Pro 人像生成模板

## 概述

本模板提供了用于使用 Gemini Nano Banana Pro 生成超写实人像的完整 JSON 配置文件。它允许用户精确控制图像生成的各个方面，从人物特征到渲染技术细节。

## JSON 配置结构

### 完整模板

```json
{
  "prompt_configuration": {
    "type": "Ultra Photorealistic Portrait",
    "style": "Cinematic Reality",
    "resolution": "8K"
  },
  "subject": {
    "demographics": "[Name, build type, complexion]",
    "hair": "[Hair color, style, texture details]",
    "skin_texture": "[Skin details, effects, realism]",
    "facial_expression": "[Expression details, mood, emotion]"
  },
  "apparel": {
    "outfit_style": "[Overall style]",
    "top": "[Top description]",
    "bottoms": "[Bottoms description]",
    "accessories": "[Accessories list]"
  },
  "pose_and_action": {
    "perspective": "[Camera angle/view]",
    "action": "[What the subject is doing]",
    "reflection": "[Any reflections in scene]"
  },
  "environment": {
    "location": "[Where it takes place]",
    "background_elements": "[Background details]",
    "flooring": "[Flooring description]"
  },
  "lighting_and_atmosphere": {
    "lighting_type": "[Lighting source]",
    "quality": "[Lighting characteristics]",
    "mood": "[Overall mood/atmosphere]"
  },
  "technical_specifications": {
    "camera": "[Camera type]",
    "aperture": "[f-stop]",
    "focus": "[Focus details]",
    "render_details": "[Rendering engine and techniques]"
  }
}
```

## 各部分说明

### 1. 提示配置

用于设置人像的整体类型和风格。

**字段：**
- `type`：人像类型（例如：“超写实人像”、“电影风格头像”、“编辑用人像”）
- `style`：视觉风格（例如：“电影级真实感”、“高级时尚”、“编辑级摄影”）
- `resolution`：图像分辨率（例如：“8K”、“4K”、“2K”）

**示例：**
```json
{
  "type": "Ultra Photorealistic Portrait",
  "style": "Cinematic Reality",
  "resolution": "8K"
}
```

### 2. 人物详情

详细描述被拍摄者的外貌特征。

**字段：**
- `demographics`：身份、体型、肤色
- `hair`：颜色、发型、质地、层次
- `skin_texture`：皮肤的真实质感、效果、状态
- `facial_expression`：面部表情、情绪、氛围

**示例：**
```json
{
  "demographics": "Sydney Sweeney, athletic build, fit physique, pale complexion",
  "hair": "Dark brown to black hair, pulled back into a messy high ponytail, loose sweaty strands framing the face",
  "skin_texture": "Hyper-realistic skin details, intense post-workout sheen, glistening with heavy sweat, visible pores, slight flush on cheeks",
  "facial_expression": "Exhaling slightly, mouth slightly open in a 'phew' expression, focused gaze, tired but accomplished"
}
```

**人物详情提示：**
- 使用具体名称或描述：例如：“Zendaya”、“运动员型身材”、“苗条优雅”
- 包括体型描述：例如：“肌肉型身材”、“纤瘦型身材”、“运动型体型”
- 注意肤色描述：例如：“苍白”、“橄榄色皮肤”、“暖色调”、“冷色调”

### 3. 服装

详细定义服装和配饰。

**字段：**
- `outfit_style`：整体服装风格
- `top`：上身服装
- `bottoms`：下身服装
- `accessories`：珠宝、配饰等物品

**示例：**
```json
{
  "outfit_style": "Monochromatic pastel pink gym set, athleisure",
  "top": "Tight cropped pink camisole/tank top with spaghetti straps, rolled up slightly",
  "bottoms": "Loose-fitting pink sweatpants with visible drawstring and elastic waistband, soft cotton texture",
  "accessories": "Thin silver necklace"
}
```

**服装提示：**
- 包括服装的合身度：例如：“紧身”、“宽松”、“定制款”、“宽松款”
- 提及面料：例如：“棉质”、“丝绸”、“牛仔”、“运动面料”
- 描述面料质感：例如：“柔软”、“挺括”、“有光泽”、“哑光”

### 4. 姿势和动作

描述人物的动作以及相机视角。

**字段：**
- `perspective`：相机角度和观察方向
- `action`：人物的动作或姿势
- `reflection`：场景中可见的反射效果

**示例：**
```json
{
  "perspective": "Three-quarter side profile view facing left",
  "action": "Body checking in a gym mirror, left hand pressing against the mirror surface, right hand lifting the hem of shirt to reveal defined abdominal muscles (six-pack)",
  "reflection": "Partial reflection of the arm visible in the mirror on the left edge"
}
```

**姿势提示：**
- 使用具体角度：例如：“四分之三视角”、“侧脸”、“正面朝向”、“低角度”
- 动作描述要准确：例如：“查看反射”、“伸展身体”、“看向相机”
- 包括细节：手部位置、身体姿态、朝向

### 5. 环境

定义场景的背景元素。

**字段：**
- `location`：场景发生的地点
- `background_elements`：背景中的物体和人物
- `flooring`：地面或表面的材质

**示例：**
```json
{
  "location": "Commercial gym interior",
  "background_elements": "Blurred gym equipment, weight racks, cable machines, dumbbells, other gym-goers faintly visible in the distance",
  "flooring": "Black speckled rubber gym flooring"
}
```

**环境提示：**
- 明确地点类型：例如：“商业健身房”、“家庭工作室”、“户外环境”
- 包括背景的远近层次：例如：“模糊的背景”、“远处的物体”
- 描述表面材质：例如：“木质地面”、“大理石地面”、“粗糙地面”

### 6. 光线和氛围

控制光线质量和整体氛围。

**字段：**
- `lighting_type`：光源类型
- `quality`：光线的特性和效果
- `mood`：整体氛围和情感色调

**示例：**
```json
{
  "lighting_type": "Overhead artificial gym lighting",
  "quality": "Warm tungsten tones, creating strong specular highlights on the sweaty skin and hair",
  "mood": "Intense, raw, fitness-focused, candid moment"
}
```

**光线提示：**
- 指定光源：例如：“头顶人造光”、“自然日光”、“摄影棚闪光灯”、“霓虹灯”
- 描述光线质量：例如：“暖色调”、“冷色调”、“高光效果”、“柔和的光线分布”
- 设定氛围：例如：“强烈”、“轻松”、“充满活力”、“自然”、“刻意摆拍”

### 7. 技术规格

定义相机和渲染参数，以实现超写实效果。

**字段：**
- `camera`：相机类型和镜头
- `aperture`：光圈值（控制景深）
- `focus`：焦点位置和景深范围
- `render_details`：渲染引擎和技巧

**示例：**
```json
{
  "camera": "DSLR, 85mm portrait lens",
  "aperture": "f/2.8",
  "focus": "Sharp focus on subject's face and abs, creamy bokeh background",
  "render_details": "Unreal Engine 5, Octane Render, ray tracing, subsurface scattering on skin, volumetric lighting"
}
```

**技术提示：**
- 使用真实的相机参数：例如：“单反相机”、“无反相机”、“85mm 人像镜头”、“50mm 定焦镜头”
- 光圈对景深的影响：f/1.2-2.8 = 朦胧的背景效果；f/5.6-11 = 更深的景深
- 包括渲染技术：例如：“光线追踪”、“次表面散射”、“体积光照”

## 完整示例

### 示例 1：健身人像

基于 @lexx_aura 在 Twitter 上发布的成功案例（877 个赞、56 次转发、544 次收藏）

```json
{
  "prompt_configuration": {
    "type": "Ultra Photorealistic Portrait",
    "style": "Cinematic Reality",
    "resolution": "8K"
  },
  "subject": {
    "demographics": "Sydney Sweeney, athletic build, fit physique, pale complexion",
    "hair": "Dark brown to black hair, pulled back into a messy high ponytail, loose sweaty strands framing face",
    "skin_texture": "Hyper-realistic skin details, intense post-workout sheen, glistening with heavy sweat, visible pores, slight flush on cheeks",
    "facial_expression": "Exhaling slightly, mouth slightly open in a 'phew' expression, focused gaze, tired but accomplished"
  },
  "apparel": {
    "outfit_style": "Monochromatic pastel pink gym set, athleisure",
    "top": "Tight cropped pink camisole/tank top with spaghetti straps, rolled up slightly",
    "bottoms": "Loose-fitting pink sweatpants with visible drawstring and elastic waistband, soft cotton texture",
    "accessories": "Thin silver necklace"
  },
  "pose_and_action": {
    "perspective": "Three-quarter side profile view facing left",
    "action": "Body checking in a gym mirror, left hand pressing against the mirror surface, right hand lifting the hem of shirt to reveal defined abdominal muscles (six-pack)",
    "reflection": "Partial reflection of the arm visible in the mirror on the left edge"
  },
  "environment": {
    "location": "Commercial gym interior",
    "background_elements": "Blurred gym equipment, weight racks, cable machines, dumbbells, other gym-goers faintly visible in the distance",
    "flooring": "Black speckled rubber gym flooring"
  },
  "lighting_and_atmosphere": {
    "lighting_type": "Overhead artificial gym lighting",
    "quality": "Warm tungsten tones, creating strong specular highlights on the sweaty skin and hair",
    "mood": "Intense, raw, fitness-focused, candid moment"
  },
  "technical_specifications": {
    "camera": "DSLR, 85mm portrait lens",
    "aperture": "f/2.8",
    "focus": "Sharp focus on subject's face and abs, creamy bokeh background",
    "render_details": "Unreal Engine 5, Octane Render, ray tracing, subsurface scattering on skin, volumetric lighting"
  }
}
```

### 示例 2：工作室时尚人像

```json
{
  "prompt_configuration": {
    "type": "Editorial Portrait",
    "style": "High Fashion",
    "resolution": "8K"
  },
  "subject": {
    "demographics": "Fashion model, tall and slender, elegant pose",
    "hair": "Straight blonde hair, sleek center part, shoulder-length",
    "skin_texture": "Flawless porcelain skin, subtle sheen, minimal pores visible",
    "facial_expression": "Confident gaze directly at camera, slight smile, fierce expression"
  },
  "apparel": {
    "outfit_style": "Minimalist luxury fashion",
    "top": "Crisp white silk blouse, slightly unbuttoned at collar",
    "bottoms": "Black tailored high-waisted trousers, perfect fit",
    "accessories": "Gold hoop earrings, minimalist gold ring"
  },
  "pose_and_action": {
    "perspective": "Direct front-facing portrait, eye-level",
    "action": "Standing confidently, one hand on hip, other resting on thigh",
    "reflection": "None"
  },
  "environment": {
    "location": "Professional photography studio",
    "background_elements": "Solid light gray backdrop, subtle studio lighting equipment visible in edges",
    "flooring": "Glossy studio floor, subtle reflection"
  },
  "lighting_and_atmosphere": {
    "lighting_type": "Studio three-point lighting with beauty dish",
    "quality": "Soft, even lighting, subtle rim light on hair and shoulders, clean shadows",
    "mood": "Professional, elegant, fashion-forward"
  },
  "technical_specifications": {
    "camera": "Medium format camera, 100mm macro lens",
    "aperture": "f/4.0",
    "focus": "Pin-sharp focus on eyes, slight fall-off toward ears",
    "render_details": "8K resolution, subsurface scattering, HDRI lighting, global illumination"
  }
}
```

### 示例 3：户外自然光人像

```json
{
  "prompt_configuration": {
    "type": "Cinematic Portrait",
    "style": "Natural Light Photography",
    "resolution": "8K"
  },
  "subject": {
    "demographics": "Young professional, early 20s, casual but put-together",
    "hair": "Wavy dark brown hair, windblown texture, loose ponytail",
    "skin_texture": "Natural skin texture, slight sun-kissed glow, visible fine details",
    "facial_expression": "Warm genuine smile, eyes bright, relaxed demeanor"
  },
  "apparel": {
    "outfit_style": "Casual chic",
    "top": "White linen button-down, sleeves rolled up, slightly unbuttoned",
    "bottoms": "Light wash denim jeans, tailored fit, slight distressing",
    "accessories": "Simple leather watch, silver chain bracelet"
  },
  "pose_and_action": {
    "perspective": "Slightly low angle, capturing subject against sky",
    "action": "Walking away from camera, turning back to look over shoulder with smile",
    "reflection": "Sunlight reflecting off sunglasses in hand"
  },
  "environment": {
    "location": "Urban rooftop at golden hour",
    "background_elements": "City skyline silhouette, scattered clouds, distant buildings",
    "flooring": "Rooftop terrace with subtle texture"
  },
  "lighting_and_atmosphere": {
    "lighting_type": "Golden hour natural sunlight, backlight creating halo effect",
    "quality": "Warm golden tones, soft shadows, lens flare, rim lighting on hair",
    "mood": "Hopeful, cinematic, aspirational"
  },
  "technical_specifications": {
    "camera": "Full-frame DSLR, 50mm prime lens",
    "aperture": "f/1.8",
    "focus": "Focus on face, bokeh background",
    "render_details": "Photorealistic rendering, lens flare simulation, natural light physics"
  }
}
```

## 最佳实践

### 1. 详细具体
- 使用精确的描述：例如：“凌乱的高马尾”而不是“扎起的高马尾”
- 包括材质描述：例如：“汗湿的”、“有光泽的”、“哑光的”
- 提及可见的细节：例如：“可见的毛孔”、“轻微的红晕”、“细微的皱纹”

### 2. 光线与氛围匹配
- 健身场景：使用强烈、戏剧性的光线
- 时尚场景：使用控制良好的摄影棚光线
- 休闲场景：使用自然、柔和的光线

### 3. 控制景深
- f/1.2-2.8：朦胧的背景效果
- f/4.0-5.6：适中的景深，部分背景可见
- f/8.0-11：整体清晰，适合环境人像

### 4. 添加环境背景
- 将人物置于具体环境中
- 添加真实的背景元素
- 描述地面和表面材质

### 5. 使用专业术语
- “单反相机”、“无反相机”、“85mm 人像镜头”
- “光线追踪”、“次表面散射”、“体积光照”
- “Unreal Engine 5”、“Octane Render”、“HDRI 光照”

## 常见风格

### 健身摄影
- 人物：运动员型身材、出汗状态、运动后
- 服装：健身服、运动装备
- 环境：健身房、户外训练场地
- 光线：戏剧性、突出肌肉
- 氛围：强烈、真实、充满力量感

### 编辑级时尚
- 人物：模特、自信、时尚
- 服装：设计师品牌服装、精心搭配的服饰
- 环境：摄影棚、城市环境
- 光线：控制良好、干净、具有编辑感
- 氛围：精致、时尚前卫

### 自然光人像
- 人物：放松、自然、真实
- 服装：休闲、舒适的日常服装
- 环境：户外、自然环境
- 光线：阳光、黄金时刻、柔和的光线
- 氛围：温暖、亲切、具有吸引力

## 测试配置

在生成图像之前，请验证：
1. **JSON 是否有效**：检查是否有缺失的逗号或括号
2. **所有字段是否填写**：不要遗漏必填字段
3. **细节是否一致**：光线应与氛围相匹配，服装应与场景相符
4. **规格是否合理**：相机设置应符合实际情况
5. **描述是否连贯**：配置文件应能完整表达一个清晰的故事

## 资源

本模板包含以下资源：

### 参考资料：
- 目前暂无（所有示例和模板均包含在 SKILL.md 文件中）

### 脚本：
- 目前暂无（本模板仅用于配置提示）

### 资产：
- 目前暂无（本模板为知识型模板，不涉及资产文件）