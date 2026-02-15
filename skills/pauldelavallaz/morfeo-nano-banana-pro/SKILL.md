---
name: nano-banana-pro
description: 使用 Google 的 Nano Banana Pro (Gemini 3 Pro Image) API 生成和编辑图片。当用户请求生成、创建、编辑、修改、更改或更新图片时，可以使用此功能。当用户引用现有的图片文件并要求以任何方式对其进行修改时（例如：“修改这张图片”、“更换背景”、“将 X 替换为 Y”），也可以使用此功能。该 API 支持文本到图片的生成以及图片到图片的编辑，并且支持可配置的分辨率（默认为 1K，高分辨率为 2K 或 4K）。**请勿先读取图片文件**——可以直接通过 `--input-image` 参数使用此功能。
---

# Nano Banana Pro 图像生成与编辑

使用 Google 的 Nano Banana Pro API（Gemini 3 Pro Image）生成新图像或编辑现有图像。

## API 技术规范

### 端点与身份验证

**Google AI Studio（公开预览）：**
```
POST https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent?key=${API_KEY}
```

**Vertex AI（企业版）：**
```
POST https://${REGION}-aiplatform.googleapis.com/v1/projects/${PROJECT_ID}/locations/${REGION}/publishers/google/models/gemini-3-pro-image-preview:predict
```

### 模型 ID
- API：`gemini-3-pro-image-preview`
- 内部 SDK：`nanobanana-pro-001`

### 参数

| 参数 | 值 | 描述 |
|-----------|--------|-------------|
| `aspect_ratio` | `1:1`, `4:3`, `3:4`, `16:9`, `9:16` | 输出宽高比 |
| `output_mime_type` | `image/png`, `image/jpeg` | 输出格式 |
| `reference_images` | 数组（最多 14 张） | 用于保持一致性的参考图像 |
| `reference_type` | `CHARACTER`, `STYLE`, `SUBJECT` | 参考图像的用途 |
| `person_generation` | `ALLOW_ADULT`, `DONT_ALLOW`, `FILTER_SENSITIVE` | 人物生成策略 |
| `image_size` | `1K`, `2K`, `4K` | 输出分辨率 |

### 参考类型

- **STYLE**：从参考图像中转移视觉风格、色彩调色板或情绪 |
- **CHARACTER**：在多张图像中保持面部特征和特性的统一性 |
- **SUBJECT**：保持主体/产品的统一性（适用于产品摄影！）

### 高级功能

- **文本渲染**：原生文本渲染，无拼写错误 |
- **上下文编辑**：发送现有图像及修改提示（自动进行图像修补） |
- **高分辨率**：通过 `upscale: true` 功能实现原生升级至 4K 分辨率 |

## 使用方法

使用绝对路径运行脚本（请勿先进入 `skill` 目录）：

**生成新图像：**
```bash
uv run ~/.clawdbot/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "your image description" \
  --filename "output-name.png" \
  [--resolution 1K|2K|4K] \
  [--api-key KEY]
```

**编辑现有图像：**
```bash
uv run ~/.clawdbot/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "editing instructions" \
  --filename "output-name.png" \
  --input-image "path/to/input.png" \
  [--resolution 1K|2K|4K]
```

**使用参考图像（保持产品/风格/人物的一致性）：**
```bash
uv run ~/.clawdbot/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "your description" \
  --filename "output-name.png" \
  --reference-image "path/to/reference.jpg" \
  --reference-type SUBJECT|STYLE|CHARACTER \
  [--resolution 1K|2K|4K]
```

**重要提示：**始终从用户当前的工作目录运行脚本，以确保图像保存在用户的工作目录中，而非 `skill` 目录中。

## 分辨率选项

- **1K**（默认） - 约 1024px 分辨率 |
- **2K** - 约 2048px 分辨率（推荐用于大多数场景） |
- **4K** - 约 4096px 分辨率（高质量）

**用户请求解析：**
- 未提及分辨率 → 使用 `1K`
- “低分辨率”、“1080”、“1080p”、“1K” → 使用 `1K`
- “2K”、“2048”、“正常分辨率”、“中等分辨率” → 使用 `2K`
- “高分辨率”、“高画质”、“4K”、“超高清” → 使用 `4K`

## API 密钥

脚本会按以下顺序检查 API 密钥：
1. `--api-key` 参数 |
2. `GEMINI_API_KEY` 环境变量

## 文件名生成规则

文件名格式：`{timestamp}-{descriptive-name}.png`
- `timestamp`：`yyyy-mm-dd-hh-mm-ss`（24 小时格式）
- `name`：描述性的小写名称，使用连字符分隔

**示例：**
- `2025-11-23-14-23-05-japanese-garden.png`
- `2025-11-23-15-30-12-sunset-mountains.png`

---

# 提示工程框架

您是一位专注于 Nano Banana Pro 的专业提示工程师，负责将用户的简单想法和参考图像转化为高质量、描述性强的提示。

## 1. 输入分析

收到用户想法和参考图像后，需要评估：

- **主题内容**：确定主要人物、对象或焦点 |
- **参考图像的用途**：判断图像是否提供了构图（布局）、风格（美学/纹理）或人物特征 |
- **文本要求**：记录需要在图像中渲染的特定文本

## 2. 提示构建框架

使用以下层次结构优化提示：

### 核心主题与动作
清晰描述“谁”正在“做什么”。

### 风格与媒介
指定艺术媒介：
- 超现实主义摄影 |
- 油画 |
- 3D 渲染 |
- 极简主义矢量图 |
- 商业食品摄影 |
- 编辑风格

### 参考图像的整合
明确指示如何使用上传的参考图像：
> “保留参考图像中的产品包装作为主要元素”
> “应用参考图像 A 的温暖光线效果”

### 技术细节

**光线效果：**
- 电影级边缘光 |
- 柔和的散射阳光 |
- 刺眼的闪光灯 |
- 温暖的钨丝灯 |
- 金色的光线效果

**构图：**
- 广角拍摄 |
- 微距细节 |
- 鸟瞰视角 |
- 浅景深 |
- 产品作为主要元素

**色彩理论：**
- 单色蓝色 |
- 高对比度的互补色 |
- 温暖的琥珀色调 |
- 深沉、忧郁的色彩调色板

**文本渲染：**
使用双引号标注特定文本：
> “‘FUTURE’ 一词用粗体、金属质感的 3D 字体显示在中心”

## 3. 优化规则

### 应该做的：
- 使用描述性强的正面语言 |
- 对模糊的术语进行具体化（例如：“cool” → “iridescent”（彩虹色的），“pretty” → “ethereal”（空灵的），“realistic” → “photorealistic 8k texture”（8K 真实感的纹理） |
- 与参考图像保持一致性 |
- 使用富有表现力的形容词来描述情绪（如 “gritty”（粗糙的）、“serene”（宁静的）、“industrial”（工业风格的）、“whimsical”（奇异的） |
- 明确指定“8k texture detail”或“8k photorealistic detail”以体现高质量

### 不应该做的：
- 使用否定性的提示（直接说明不要做什么） |
- 与参考图像中的视觉信息相矛盾 |
- 使用不具体的术语

## 4. 产品摄影最佳实践

在生成以产品为主角的图像时：

1. **始终使用 `--reference-type SUBJECT` 选项** 以保持产品的一致性 |
2. **在提示中突出描述产品**：
   > “Milkaut Crematto 容器，带有蓝色标签和红色盖子，需明显展示” |
3. **将产品置于显眼位置**：
   > “将产品容器作为主要元素进行展示” |
   > “确保产品容器清晰对焦” |
4. **自然地融入场景**：
   > “将产品放置在……旁边”或“以显眼的方式排列”

### 产品摄影示例提示：

```
Hyper-realistic commercial food photography with a [PRODUCT NAME] container 
prominently displayed next to [FOOD ITEM], [food description], 
[setting/background], [lighting style], the [product] as hero element, 
8k photorealistic detail
```

## 5. 输出格式

以英文提供优化后的提示，无需额外注释。

---

## 示例

### 产品 + 食品场景
```bash
uv run ~/.clawdbot/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "Hyper-realistic commercial food photography with a Milkaut Crematto container prominently displayed next to a gourmet double smash burger with perfectly melted cheddar cheese cascading down juicy beef patties, artisan brioche bun, wisps of steam rising, dark moody background with dramatic rim lighting, the cream cheese container as hero product placement, 8k texture detail" \
  --filename "2026-01-28-product-burger.png" \
  --reference-image "product-photo.jpg" \
  --reference-type SUBJECT \
  --resolution 2K
```

### 风格迁移
```bash
uv run ~/.clawdbot/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "Using the warm golden hour aesthetic from the reference, create a serene Japanese garden with cherry blossoms, koi pond reflecting soft pink petals, traditional wooden bridge, ethereal morning mist, 8k photorealistic detail" \
  --filename "2026-01-28-japanese-garden.png" \
  --reference-image "style-reference.jpg" \
  --reference-type STYLE \
  --resolution 2K
```

### 图像编辑
```bash
uv run ~/.clawdbot/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "Change the background to a dramatic sunset over mountains, maintain the subject in sharp focus" \
  --filename "2026-01-28-edited-sunset.png" \
  --input-image "original.jpg" \
  --resolution 2K
```