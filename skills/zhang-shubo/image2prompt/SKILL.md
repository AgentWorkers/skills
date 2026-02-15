---
name: image2prompt
description: 分析图像并生成用于图像生成的详细提示。支持肖像、风景、产品、动物、插画等类别，输出形式可以是结构化的或自然的。
homepage: https://docs.openclaw.ai/tools/image2prompt
user-invocable: true
metadata: {"openclaw":{"emoji":"🖼️","primaryEnv":"OPENAI_API_KEY","requires":{"anyBins":["openclaw"]}}}
---

# 图像到提示（Image to Prompt）

该功能可分析图像，并为 AI 图像生成提供详细、高质量的提示。

## 工作流程

**步骤 1：类别检测**
首先，将图像分类为以下类别之一：
- **肖像（Portrait）**：人物为主要对象（照片、艺术作品、数字艺术）
- **风景（Landscape）**：自然风光、城市景观、建筑、户外环境
- **产品（Product）**：商品照片
- **动物（Animal）**：动物为主要对象
- **插图（Illustration）**：图表、信息图、用户界面原型、技术图纸
- **其他（Other）**：不符合上述类别的图像

**步骤 2：针对类别的详细分析**
根据检测到的类别生成相应的详细提示。

## 使用方法

### 基本分析
```bash
# Analyze an image (auto-detect category)
openclaw message send --image /path/to/image.jpg "Analyze this image and generate a detailed prompt for reproduction"
```

### 指定输出格式

- **自然语言（默认）：**
```
Analyze this image and write a detailed, flowing prompt description (600-1000 words for portraits, 400-600 for others).
```

- **结构化 JSON：**
```
Analyze this image and output a structured JSON description with all visual elements categorized.
```

### 提取图像尺寸信息
请求提取图像的尺寸信息，以便为每个视觉元素生成标签：
```
Analyze this image with dimension extraction. Tag phrases for: backgrounds, objects, characters, styles, actions, colors, moods, lighting, compositions, themes.
```

## 各类别的详细分析内容

### 肖像分析涵盖的要素：
- **类型/风格（Model/Style）**：摄影类型、质量水平、视觉风格
- **主体（Subject）**：性别、年龄、种族、肤色、体型
- **面部特征（Facial Features）**：眼睛、嘴唇、脸型、表情
- **头发（Hair）**：颜色、长度、发型、分区
- **姿势（Pose）**：身体姿势、朝向、手臂/腿部的位置、视线方向
- **服装（Clothing）**：类型、颜色、图案、版型、材质、风格
- **配饰（Accessories）**：珠宝、包包、帽子等
- **环境（Environment）**：地点、地面、背景、氛围
- **光线（Lighting）**：类型、时间、阴影、对比度、色温
- **相机（Camera）**：拍摄角度、高度、拍摄类型、镜头、景深、透视效果
- **技术细节（Technical）**：图像的真实性、后期处理效果、分辨率

### 风景分析涵盖的要素：
- 地形和水体特征
- 天空和大气元素
- 前景/背景的构图
- 自然光线和氛围
- 色彩搭配和摄影风格

### 产品分析涵盖的要素：
- 产品特征和材质
- 设计元素和形状
- 拍摄场景和背景
- 摄影棚的灯光设置
- 商业摄影风格

### 动物分析涵盖的要素：
- 动物种类和特征
- 姿势和行为
- 动物的表情和特征
- 生境和拍摄环境
- 野生动物/宠物的拍摄风格

### 插图分析涵盖的要素：
- 图表类型（流程图、信息图、用户界面等）
- 可视元素（图标、形状、连接线）
- 布局和层次结构
- 设计风格（平面图、等轴测图等）
- 色彩方案和意义

## 输出示例

### 自然语言输出（肖像）
```json
{
  "prompt": "A stunning photorealistic portrait of a young woman in her mid-20s with fair porcelain skin and warm pink undertones. She has striking emerald green almond-shaped eyes with long dark lashes, full rose-colored lips curved in a subtle confident smile, and an oval face with high cheekbones..."
}
```

### 结构化输出（肖像）
```json
{
  "structured": {
    "model": "photorealistic",
    "quality": "ultra high",
    "style": "cinematic natural light photography",
    "subject": {
      "identity": "young beautiful woman",
      "gender": "female",
      "age": "mid 20s",
      "ethnicity": "European",
      "skin_tone": "fair porcelain with pink undertones",
      "body_type": "slim athletic",
      "facial_features": {
        "eyes": "emerald green, almond-shaped, intense gaze",
        "lips": "full, rose pink, subtle smile",
        "face_shape": "oval with high cheekbones",
        "expression": "confident and serene"
      },
      "hair": {
        "color": "warm honey blonde",
        "length": "long",
        "style": "soft waves",
        "part": "center"
      }
    },
    "pose": {
      "position": "standing",
      "body_orientation": "three-quarter turn to camera",
      "legs": "weight on right leg, relaxed stance",
      "hands": {
        "right_hand": "resting on hip",
        "left_hand": "hanging naturally at side"
      },
      "gaze": "direct eye contact with camera"
    },
    "clothing": {
      "type": "flowing maxi dress",
      "color": "dusty rose",
      "pattern": "solid",
      "details": "V-neckline, cinched waist, silk material",
      "style": "romantic feminine"
    },
    "accessories": ["delicate gold necklace", "small hoop earrings"],
    "environment": {
      "location": "outdoor garden",
      "ground": "cobblestone path",
      "background": "blooming roses, soft bokeh",
      "atmosphere": "dreamy and romantic"
    },
    "lighting": {
      "type": "natural sunlight",
      "time": "golden hour",
      "shadow_quality": "soft diffused shadows",
      "contrast": "medium",
      "color_temperature": "warm"
    },
    "camera": {
      "angle": "slightly below eye level",
      "camera_height": "chest height",
      "shot_type": "medium shot",
      "lens": "85mm",
      "depth_of_field": "shallow",
      "perspective": "slight compression, flattering"
    },
    "mood": "romantic, confident, ethereal",
    "realism": "highly photorealistic",
    "post_processing": "soft color grading, subtle glow",
    "resolution": "8k"
  }
}
```

### 带有尺寸信息的输出
```json
{
  "prompt": "...",
  "dimensions": {
    "backgrounds": ["outdoor garden", "blooming roses", "soft bokeh"],
    "objects": ["delicate gold necklace", "small hoop earrings"],
    "characters": ["young beautiful woman", "mid 20s", "European"],
    "styles": ["photorealistic", "cinematic natural light photography"],
    "actions": ["standing", "three-quarter turn", "direct eye contact"],
    "colors": ["dusty rose", "honey blonde", "emerald green"],
    "moods": ["romantic", "confident", "ethereal", "dreamy"],
    "lighting": ["golden hour", "natural sunlight", "soft diffused shadows"],
    "compositions": ["medium shot", "85mm", "shallow depth of field"],
    "themes": ["romantic feminine", "portrait photography"]
  }
}
```

## 优化建议

1. **高分辨率图像** 有助于生成更详细的提示。
2. **清晰、光线充足的图像** 有助于提高类别检测的准确性。
3. 当需要程序化访问图像元素时，请选择结构化输出格式。
4. 在构建提示数据库或训练数据时，可以使用尺寸提取功能。
5. 如有需要，可指定自然语言输出的字数要求。

## 集成方式

该功能适用于任何具有视觉处理能力的模型。为了获得最佳效果，建议使用以下模型：
- GPT-4 Vision
- Claude 3 (Opus/Sonnet)
- Gemini Pro Vision