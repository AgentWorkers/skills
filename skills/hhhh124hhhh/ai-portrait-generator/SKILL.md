---
name: ai-portrait-generator
description: 使用结构化的 JSON 提示生成超逼真的肖像。适用于创建 AI 生成的肖像、角色艺术作品，或具有电影级质量及详细规格的逼真人物图像。
---

# 人工智能肖像生成器

使用结构化的JSON提示模板生成超写实的肖像。该模板基于@lexx_aura的专业提示框架，针对Nano Banana Pro及类似模型进行了优化，以实现高质量的人工智能图像生成。

## 适用场景

- 为社交媒体头像创建逼真的肖像
- 为游戏或故事生成角色艺术图像
- 制作具有专业品质的营销材料
- 根据精确的视觉要求构建概念艺术
- 创建具有特定光线和氛围的电影级肖像

## 核心功能

### 1. 结构化提示模板
- 基于JSON的配置，实现精确控制
- 模块化设计：包括配置、主体、服装、姿势、环境和光线等部分
- 集成了专业摄影术语
- 提供电影级和超写实风格的选项

### 2. 多维度定制
- 可定制主体的人口统计特征和身体属性
- 详细的头发、皮肤纹理和面部表情
- 服装：包括款式、配饰和材质
- 姿势和动作：包括视角、动作和反射效果
- 环境：包括地点、背景元素和氛围
- 光线：包括类型、质量和情绪效果

### 3. 技术规格
- 相机设置（镜头类型、光圈）
- 对焦和景深控制
- 渲染引擎细节（Unreal Engine 5、Octane Render）
- 高级效果（光线追踪、体积光、次表面散射）

## 快速入门

### 基本肖像模板

```json
{
  "prompt_configuration": {
    "type": "Ultra Photorealistic Portrait",
    "style": "Cinematic Reality",
    "resolution": "8K"
  },
  "subject": {
    "demographics": "Your description here (e.g., 'Young woman, athletic build')",
    "hair": "Hair description (color, style, texture)",
    "skin_texture": "Skin details (tone, texture, complexion)",
    "facial_expression": "Expression description"
  },
  "apparel": {
    "outfit_style": "Overall style (e.g., 'Casual athleisure')",
    "top": "Top description",
    "bottoms": "Bottoms description",
    "accessories": "Accessories description"
  },
  "pose_and_action": {
    "perspective": "View angle (e.g., 'Three-quarter side profile')",
    "action": "What the subject is doing",
    "reflection": "Any reflections (optional)"
  },
  "environment": {
    "location": "Setting location",
    "background_elements": "Background details",
    "flooring": "Floor description"
  },
  "lighting_and_atmosphere": {
    "lighting_type": "Lighting source",
    "quality": "Light quality and color tone",
    "mood": "Overall mood and atmosphere"
  },
  "technical_specifications": {
    "camera": "Camera type and lens",
    "aperture": "Aperture setting (e.g., 'f/2.8')",
    "focus": "Focus description",
    "render_details": "Rendering engine and effects"
  }
}
```

### 示例：健身房肖像

```json
{
  "prompt_configuration": {
    "type": "Ultra Photorealistic Portrait",
    "style": "Cinematic Reality",
    "resolution": "8K"
  },
  "subject": {
    "demographics": "Young woman, athletic build, fit physique",
    "hair": "Dark brown hair, pulled back into a messy high ponytail, loose strands framing face",
    "skin_texture": "Hyper-realistic skin details, post-workout sheen, glistening with sweat, visible pores",
    "facial_expression": "Exhaling slightly, mouth slightly open, focused gaze, tired but accomplished"
  },
  "apparel": {
    "outfit_style": "Monochromatic pastel pink gym set, athleisure",
    "top": "Tight cropped pink camisole with spaghetti straps",
    "bottoms": "Loose-fitting pink sweatpants with visible drawstring",
    "accessories": "Thin silver necklace"
  },
  "pose_and_action": {
    "perspective": "Three-quarter side profile view facing left",
    "action": "Body checking in a gym mirror, left hand pressing against mirror, right hand lifting shirt hem",
    "reflection": "Partial reflection of arm visible in mirror"
  },
  "environment": {
    "location": "Commercial gym interior",
    "background_elements": "Blurred gym equipment, weight racks, cable machines, dumbbells",
    "flooring": "Black speckled rubber gym flooring"
  },
  "lighting_and_atmosphere": {
    "lighting_type": "Overhead artificial gym lighting",
    "quality": "Warm tungsten tones, creating strong specular highlights on sweaty skin",
    "mood": "Intense, raw, fitness-focused, candid moment"
  },
  "technical_specifications": {
    "camera": "DSLR, 85mm portrait lens",
    "aperture": "f/2.8",
    "focus": "Sharp focus on face and abs, creamy bokeh background",
    "render_details": "Unreal Engine 5, Octane Render, ray tracing, subsurface scattering, volumetric lighting"
  }
}
```

## 常见肖像风格

### 专业头像
```json
{
  "prompt_configuration": {
    "type": "Ultra Photorealistic Portrait",
    "style": "Professional Studio",
    "resolution": "8K"
  },
  "subject": {
    "demographics": "Professional executive, confident expression",
    "facial_expression": "Warm, approachable, confident smile",
    "lighting": "Studio portrait lighting"
  },
  "apparel": {
    "outfit_style": "Business formal",
    "top": "Crisp white shirt or professional blouse",
    "accessories": "Minimal, professional"
  },
  "environment": {
    "location": "Professional studio with neutral background",
    "background_elements": "Subtle gradient backdrop",
    "lighting_and_atmosphere": {
      "lighting_type": "Softbox studio lighting",
      "quality": "Clean, even illumination",
      "mood": "Professional, trustworthy, approachable"
    }
  }
}
```

### 休闲生活方式
```json
{
  "prompt_configuration": {
    "type": "Ultra Photorealistic Portrait",
    "style": "Natural Light Lifestyle",
    "resolution": "8K"
  },
  "environment": {
    "location": "Outdoor park or café setting",
    "lighting_and_atmosphere": {
      "lighting_type": "Natural golden hour sunlight",
      "quality": "Warm, soft, directional light",
      "mood": "Relaxed, natural, authentic"
    }
  }
}
```

### 电影级戏剧性风格
```json
{
  "prompt_configuration": {
    "type": "Ultra Photorealistic Portrait",
    "style": "Cinematic Film Noir",
    "resolution": "8K"
  },
  "lighting_and_atmosphere": {
    "lighting_type": "Low-key dramatic lighting",
    "quality": "High contrast, deep shadows",
    "mood": "Dramatic, mysterious, cinematic"
  },
  "technical_specifications": {
    "camera": "DSLR, 50mm lens",
    "aperture": "f/1.4",
    "render_details": "Film grain, vignette, cinematic color grading"
  }
}
```

## 最佳实践

### 1. 使用具体描述
- 使用详细的描述而非泛泛而谈：
  - ✅ “深棕色的头发，扎成一个凌乱的马尾辫”
  - ❌ “棕色头发”

### 2. 添加纹理细节
- 为增强真实感添加纹理信息：
  - ✅ “超真实的皮肤细节，可见的毛孔，脸颊有轻微的红晕”
  - ❌ “光滑的皮肤”

### 3. 明确光线描述
- 详细描述光线质量和效果：
  - ✅ “温暖的钨灯光线，在皮肤上产生强烈的反光”
  - ❌ “光线不错”

### 4. 了解相机知识
- 使用摄影术语：
  - 光圈：f/1.4（浅景深），f/8（深景深）
  - 镜头：85mm（人像），50mm（标准），35mm（广角）
  - 对焦： “主体面部清晰对焦，背景呈现柔美的虚化效果”

### 5. 定义氛围和情绪
- 明确情感基调：
  - ✅ “强烈的、原始的、聚焦于健身的、自然的瞬间”
  - ✅ “专业的、值得信赖的、亲切的”
  - ❌ “良好的氛围”

## 高级技巧

### 结合多种风格
- 混合不同风格的元素：
  - 从“电影级戏剧性风格”中借鉴光线效果
  - 使用“休闲生活方式”中的环境设置
  - 应用“专业头像”中的技术规格

### 季节性调整
- 根据季节调整光线和氛围：
  - 冬季： “冷色调的蓝色光线，柔和的散射光”
  - 夏季： “温暖的黄金时刻，强烈的阴影”
  - 秋季： “丰富的暖色调，金色的树叶”
  - 春季： “清新的绿色调，柔和的散射光”

### 根据受众调整描述
- 年轻人： “清新、充满活力、现代感”
- 专业人士： “精致、自信、优雅”
- 老年人： “优雅、睿智、温暖”

## 提高效果的技巧

1. **从模板开始**：使用提供的示例作为基础
2. **迭代和完善**：生成多个略有不同的版本
3. **测试不同的人工智能模型**：不同模型生成的图像效果可能有所不同
4. **使用高分辨率**：8K分辨率可获得最佳效果
5. **关注细节**：细节越丰富，肖像越真实

## 与人工智能工具的集成

### Nano Banana Pro
该提示格式专为Google的Nano Banana Pro图像生成引擎优化，可提供更出色的细节、真实感和风格多样性。

### 其他兼容工具
- Midjourney（将JSON转换为自然语言）
- DALL-E 3（作为结构化提示使用）
- Stable Diffusion（使用ControlNet进行姿势控制）

## 常见问题及解决方法

### 问题：生成的图像与描述不符
**解决方案**：将复杂的描述分解为更简单的词汇，重点描述关键视觉元素

### 问题：细节过多，图像显得杂乱
**解决方案**：减少环境元素，简化背景描述

### 问题：光线效果平淡
**解决方案**：添加具体的光源描述（例如“温暖的钨灯光”、“冷色调的边缘光”）

### 问题：面部表情不匹配
**解决方案**：使用更具体的面部特征描述（例如“嘴角微微上扬”、“眉毛微微皱起”）

## 实际应用示例

请查看@lexx_aura在Twitter上的原帖：
https://x.com/lexx_aura/status/2016947883807850906
该模板使用上述JSON结构生成了高质量的超写实肖像。

---

*根据@lexx_aura的超写实肖像模板生成*
*Twitter上的互动数据：877个赞，56次转发，544次收藏*
*最后更新时间：2026-01-30*