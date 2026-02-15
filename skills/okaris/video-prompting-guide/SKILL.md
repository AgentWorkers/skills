---
name: video-prompting-guide
description: |
  Best practices and techniques for writing effective AI video generation prompts.
  Covers: Veo, Seedance, Wan, Grok, Kling, Runway, Pika, Sora prompting strategies.
  Learn: shot types, camera movements, lighting, pacing, style keywords, negative prompts.
  Use for: improving video quality, getting consistent results, professional video prompts.
  Triggers: video prompt, how to prompt video, veo prompts, video generation tips,
  better ai video, video prompt engineering, video prompt guide, video prompt template,
  ai video tips, video prompt best practices, video prompt examples, cinematography prompts
allowed-tools: Bash(infsh *)
---

# 视频提示指南

通过 [inference.sh](https://inference.sh) 编写有效的人工智能视频生成提示的最佳实践。

## 快速入门

```bash
curl -fsSL https://cli.inference.sh | sh && infsh login

# Well-structured video prompt
infsh app run google/veo-3-1-fast --input '{
  "prompt": "Cinematic tracking shot of a red sports car driving through Tokyo at night, neon lights reflecting on wet streets, rain falling, 4K, shallow depth of field"
}'
```

## 提示结构公式

```
[Shot Type] + [Subject] + [Action] + [Setting] + [Lighting] + [Style] + [Technical]
```

### 示例解析

```
"Slow motion close-up of coffee being poured into a white ceramic cup,
steam rising, morning sunlight streaming through window, warm color grading,
cinematic, 4K, shallow depth of field"
```

- **镜头类型**：慢动作特写
- **主题**：咖啡
- **动作**：倒咖啡
- **场景**：白色陶瓷杯、窗户
- **光线**：早晨的阳光
- **风格**：暖色调、电影风格
- **技术参数**：4K 分辨率、浅景深

## 镜头类型

| 镜头类型 | 描述 | 适用场景 |
|-----------|-------------|---------|
| 广角镜头 | 展示整个场景 | 建立场景氛围 |
| 中景镜头 | 腰部以上视角 | 对话、动作展示 |
| 特写镜头 | 面部或细节 | 表达情感、展示产品细节 |
| 极近镜头 | 单个物体特写 | 强调戏剧性或质感 |
| 航拍镜头 | 俯视角度 | 展示风景或规模感 |
| 低角度镜头 | 相机从下方拍摄 | 增强视觉冲击力 |
| 高角度镜头 | 相机从上方拍摄 | 强调脆弱感或紧张氛围 |
| 斜角镜头 | 倾斜的拍摄角度 | 增加不安或紧张感 |
| 第一人称视角镜头 | 以第一人称视角拍摄 | 增强沉浸感 |

## 相机移动方式

| 移动方式 | 描述 | 效果 |
|----------|-------------|--------|
| 跟踪拍摄 | 相机跟随拍摄对象 | 使画面更具动态感 |
| 摇摄（推/拉） | 相机向拍摄对象靠近或远离 | 引导观众注意力 |
| 平移 | 水平旋转 | 展示整个场景 |
| 俯仰 | 垂直旋转 | 强调高度感 |
| 起重机拍摄 | 垂直+水平移动 | 创造戏剧性效果 |
| 手持拍摄 | 相机轻微晃动 | 增强真实感 |
| 稳定器拍摄 | 相机稳定移动 | 专业、电影化效果 |
| 缩放 | 镜头放大/缩小 | 快速调整焦点 |
| 静态拍摄 | 相机无移动 | 适合需要深思的场景 |

## 光线关键词

| 关键词 | 效果 |
|---------|--------|
| 金色时刻 | 温暖、柔和的光线 | 适合浪漫场景 |
| 蓝色时刻 | 凉爽、忧郁的光线 | 适合黄昏或夜晚场景 |
| 高调照明 | 明亮、阴影较少 | 适合明亮场景 |
| 低调照明 | 昏暗、阴影明显 | 适合戏剧性场景 |
| 轮廓照明 | 光线勾勒出主体轮廓 |
| 背景光 | 光线来自主体后方 |
| 柔和的光线 | 温和、 flattering（此处可能有误，应为“柔和的光线”） |
| 强烈光线 | 明显的阴影、对比强烈 |
| 霓虹光 | 色彩鲜艳、适合都市或赛博朋克风格 |
| 自然光 | 逼真、适合纪录片风格 |

## 风格关键词

### 电影风格示例

```
cinematic, film grain, anamorphic lens, letterbox,
shallow depth of field, bokeh, 35mm film,
color grading, theatrical
```

### 视觉美学

```
minimalist, maximalist, vintage, retro, futuristic,
cyberpunk, steampunk, noir, pastel, vibrant,
muted colors, high contrast, desaturated
```

### 质量要求

```
4K, 8K, high resolution, photorealistic,
hyperrealistic, ultra detailed, professional,
broadcast quality, HDR
```

## 按使用场景划分的提示示例

### 产品演示

```bash
infsh app run google/veo-3-1-fast --input '{
  "prompt": "Smooth tracking shot around a sleek smartphone on a white pedestal, soft studio lighting, product photography style, reflections on surface, 4K, shallow depth of field"
}'
```

### 自然纪录片

```bash
infsh app run google/veo-3-1 --input '{
  "prompt": "Slow motion extreme close-up of a hummingbird hovering at a red flower, wings in motion blur, shallow depth of field, golden hour lighting, National Geographic style"
}'
```

### 城市生活方式

```bash
infsh app run google/veo-3 --input '{
  "prompt": "Tracking shot following a cyclist through busy city streets, morning rush hour, natural lighting, handheld camera feel, documentary style, authentic and candid"
}'
```

### 食物相关内容

```bash
infsh app run bytedance/seedance-1-5-pro --input '{
  "prompt": "Close-up of chocolate sauce being drizzled over ice cream, slow motion, steam rising, soft lighting, food photography style, appetizing, commercial quality"
}'
```

### 科技/未来风格

```bash
infsh app run xai/grok-imagine-video --input '{
  "prompt": "Futuristic control room with holographic displays, camera slowly pans across the space, blue and cyan lighting, sci-fi atmosphere, Blade Runner aesthetic, 4K",
  "duration": 5
}'
```

## 需避免的常见错误

| 错误 | 问题 | 更好的解决方法 |
|---------|---------|-----------------|
| 提示过于模糊 | “制作一个不错的视频” | 明确指定镜头类型、主题和风格 |
| 提示过于复杂 | 包含多个场景 | 每个提示只针对一个场景 |
| 没有描述相机移动 | 静态描述 | 必须包含相机移动或动作 |
| 风格冲突 | “极简主义与极繁主义结合” | 选择一种统一的美学风格 |
| 没有指定光线条件 | 视频氛围不明确 | 明确指定光线要求 |

## 针对不同模型的使用建议

### Google Veo

- 适合制作逼真、电影风格的内容 |
- 支持音频生成（Veo 3.0及以上版本） |
- 最适合使用详细、专业的提示 |
- 3.1版本支持画面插值功能 |

### Seedance

- 适合捕捉舞蹈和人体动作 |
- 支持对第一帧画面进行精确控制 |
- 适合制作连贯的人物动作 |
- 适合使用参考图片进行创作 |

### Wan 2.5

- 适合将图片转换为视频 |
- 能够自然地动画化静态图片 |
- 具备良好的动作预测能力 |
- 适用于任何风格的图片 |

## 工作流程：迭代式提示设计

```bash
# 1. Start with basic prompt
infsh app run google/veo-3-1-fast --input '{
  "prompt": "A woman walking through a forest"
}'

# 2. Add specificity
infsh app run google/veo-3-1-fast --input '{
  "prompt": "Medium tracking shot of a woman in a red dress walking through an autumn forest"
}'

# 3. Add style and technical details
infsh app run google/veo-3-1-fast --input '{
  "prompt": "Cinematic medium tracking shot of a woman in a flowing red dress walking through an autumn forest, golden hour sunlight filtering through leaves, shallow depth of field, film grain, 4K"
}'
```

## 相关技能

```bash
# Generate videos
npx skills add inference-sh/agent-skills@ai-video-generation

# Google Veo specific
npx skills add inference-sh/agent-skills@google-veo

# Generate images for image-to-video
npx skills add inference-sh/agent-skills@ai-image-generation

# General prompt engineering
npx skills add inference-sh/agent-skills@prompt-engineering

# Full platform skill
npx skills add inference-sh/agent-skills@inference-sh
```

查看所有视频制作工具：`infsh app list --category video`

## 文档资料

- [运行应用程序](https://inference.sh/docs/apps/running) - 通过命令行运行应用程序的方法 |
- [视频生成指南](https://inference.sh/blog/guides/video-generation) - 详细的视频制作指南