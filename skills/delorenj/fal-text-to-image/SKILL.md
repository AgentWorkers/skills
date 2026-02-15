---
name: fal-text-to-image
description: 使用 fal.ai 的 AI 模型生成、混搭和编辑图像。支持文本到图像的生成、图像到图像的混搭以及有针对性的图像修复/编辑功能。
---

# fal.ai 图像生成与编辑技能

fal.ai 提供了基于专业 AI 的图像处理服务，利用其先进的模型（如 FLUX、Recraft V3、Imagen4 等）来实现各种图像处理任务。

## 三种操作模式

### 1. 文本转图像（fal-text-to-image）
根据文本提示从零开始生成图像。

### 2. 图像混音（fal-image-remix）
在保持图像构图的前提下对现有图像进行修改。

### 3. 图像编辑（fal-image-edit）
针对特定区域进行修复或遮罩编辑。

## 适用场景

- 当用户需要根据文本描述生成图像时。
- 当用户希望使用 AI 对现有图像进行转换或混音时。
- 当用户需要对图像的特定区域进行修复（如修复瑕疵）时。
- 当用户需要创建具有特定风格的图像（如矢量图、写实图像、文字图像）时。
- 当用户需要高分辨率的专业图像（最高可达 2K）时。
- 当用户需要使用参考图像进行风格迁移时。
- 当用户请求生成徽标、海报或符合品牌风格的图像时。
- 当用户需要去除图像中的对象或进行其他针对性修改时。

## 快速入门

### 文本转图像：从零开始生成图像
```bash
# Basic generation
uv run python fal-text-to-image "A cyberpunk city at sunset with neon lights"

# With specific model
uv run python fal-text-to-image -m flux-pro/v1.1-ultra "Professional headshot"

# With style reference
uv run python fal-text-to-image -i reference.jpg "Mountain landscape" -m flux-2/lora/edit
```

### 图像混音：修改现有图像
```bash
# Transform style while preserving composition
uv run python fal-image-remix input.jpg "Transform into oil painting"

# With strength control (0.0=original, 1.0=full transformation)
uv run python fal-image-remix photo.jpg "Anime style character" --strength 0.6

# Premium quality remix
uv run python fal-image-remix -m flux-1.1-pro image.jpg "Professional portrait"
```

### 图像编辑：针对性修改
```bash
# Edit with mask image (white=edit area, black=preserve)
uv run python fal-image-edit input.jpg mask.png "Replace with flowers"

# Auto-generate mask from text
uv run python fal-image-edit input.jpg --mask-prompt "sky" "Make it sunset"

# Remove objects
uv run python fal-image-edit photo.jpg mask.png "Remove object" --strength 1.0

# General editing (no mask)
uv run python fal-image-edit photo.jpg "Enhance lighting and colors"
```

## 模型选择指南

脚本会根据任务需求智能选择最佳模型：

### **flux-pro/v1.1-ultra**（高分辨率默认模型）
- **适用场景**：专业摄影，高分辨率输出（最高 2K）
- **优势**：照片逼真度，专业品质
- **使用建议**：用户需要用于发布的图像
- **端点**：`fal-ai/flux-pro/v1.1-ultra`

### **recraft/v3/text-to-image**（最新技术水平模型）
- **适用场景**：文字设计、矢量艺术、品牌风格图像、长文本处理
- **优势**：行业领先的基准测试成绩，精确的文本渲染能力
- **使用建议**：创建徽标、海报或文本密集型设计
- **端点**：`fal-ai/recraft/v3/text-to-image`

### **flux-2**（平衡性最佳的模型）
- **适用场景**：通用图像生成
- **优势**：更高的逼真度，清晰的文字显示，原生编辑功能
- **使用建议**：常规图像生成需求
- **端点**：`fal-ai/flux-2`

### **flux-2/lora**（自定义风格模型）
- **适用场景**：特定领域的风格定制
- **优势**：能够适应自定义的风格需求
- **使用建议**：用户需要特定艺术风格的图像时
- **端点**：`fal-ai/flux-2/lora`

### **flux-2/lora/edit**（风格迁移模型）
- **适用场景**：基于参考图像进行风格迁移
- **优势**：专门用于风格迁移
- **使用建议**：用户提供带有 `-i` 标志的参考图像时
- **端点**：`fal-ai/flux-2/lora/edit`

### **imagen4/preview**（谷歌质量模型）
- **适用场景**：高质量通用图像生成
- **优势**：使用谷歌的最高质量模型
- **使用建议**：用户明确要求使用 Imagen 或谷歌模型的情况
- **端点**：`fal-ai/imagen4/preview`

### **stable-diffusion-v35-large**（适用于文字设计）
- **适用场景**：处理复杂的图像元素和文字设计
- **优势**：强大的提示理解能力，高效的资源利用
- **使用建议**：处理包含多个元素的复杂图像时
- **端点**：`fal-ai/stable-diffusion-v35-large`

### **ideogram/v2**（专注于文字设计的模型）
- **适用场景**：海报、徽标、文字密集型设计
- **优势**：出色的文字处理能力，逼真的图像效果
- **使用建议**：对文字精确度要求较高的场景
- **端点**：`fal-ai/ideogram/v2`

### **bria/text-to-image/3.2**（商业安全模型）
- **适用场景**：需要使用授权训练数据的商业项目
- **优势**：适合商业用途，优秀的文字渲染效果
- **使用建议**：涉及法律/许可问题的项目时
- **端点**：`fal-ai/bria/text-to-image/3.2`

## 命令行接口
```bash
uv run python fal-text-to-image [OPTIONS] PROMPT

Arguments:
  PROMPT                    Text description of the image to generate

Options:
  -m, --model TEXT         Model to use (see model list above)
  -i, --image TEXT         Path or URL to reference image for style transfer
  -o, --output TEXT        Output filename (default: generated_image.png)
  -s, --size TEXT          Image size (e.g., "1024x1024", "landscape_16_9")
  --seed INTEGER           Random seed for reproducibility
  --steps INTEGER          Number of inference steps (model-dependent)
  --guidance FLOAT         Guidance scale (higher = more prompt adherence)
  --help                   Show this message and exit
```

## 认证设置

首次使用前，请设置您的 fal.ai API 密钥：

```bash
export FAL_KEY="your-api-key-here"
```

或者在该技能目录下创建一个 `.env` 文件：
```env
FAL_KEY=your-api-key-here
```

您可以从以下链接获取 API 密钥：https://fal.ai/dashboard/keys

## 高级示例

### 高分辨率专业照片生成
```bash
uv run python fal-text-to-image \
  -m flux-pro/v1.1-ultra \
  "Professional headshot of a business executive in modern office" \
  -s 2048x2048
```

### 徽标/文字设计
```bash
uv run python fal-text-to-image \
  -m recraft/v3/text-to-image \
  "Modern tech startup logo with text 'AI Labs' in minimalist style"
```

### 基于参考图像的风格迁移
```bash
uv run python fal-text-to-image \
  -m flux-2/lora/edit \
  -i artistic_style.jpg \
  "Portrait of a woman in a garden"
```

### 可重复的图像生成过程
```bash
uv run python fal-text-to-image \
  -m flux-2 \
  --seed 42 \
  "Futuristic cityscape with flying cars"
```

## 模型选择逻辑

当未指定 `-m` 参数时，脚本会自动选择最佳模型：

- **如果提供了 `-i` 参数**：使用 `flux-2/lora/edit` 进行风格迁移。
- **如果提示中包含文字相关关键词（如徽标、文本、海报、标志）**：使用 `recraft/v3/text-to-image`。
- **如果提示表明需要高分辨率图像（如专业照片、肖像）**：使用 `flux-pro/v1.1-ultra`。
- **如果提示中提到了矢量或品牌相关内容**：使用 `recraft/v3/text-to-image`。
- **默认情况**：使用 `flux-2` 进行通用图像生成。

## 输出格式

生成的图像会包含元数据：
- 文件名包含时间戳和模型名称。
- EXIF 数据中存储了提示内容、模型名称和参数信息。
- 控制台会显示生成时间和费用估算。

## 故障排除

| 问题 | 解决方案 |
|---------|----------|
| FAL_KEY 未设置 | 导出 FAL_KEY 环境变量或创建 `.env` 文件 |
| 模型未找到 | 核对模型名称是否在支持列表中 |
| 图像引用失败 | 确保图像路径/URL 可访问 |
| 生成超时 | 某些模型可能需要更长时间；尝试其他模型 |
| 超过使用频率限制 | 查看 fal.ai 控制台中的使用限制信息 |

## 成本优化

- **免费 tier**：FLUX.2 提供 100 次免费请求（有效期至 2025 年 12 月 25 日）。
- **按使用次数计费**：FLUX Pro 按每兆像素收费。
- **预算优化**：对于一般用途，可以选择 `flux-2` 或 `stable-diffusion-v35-large`。
- **高级 tier**：仅在需要高分辨率时使用 `flux-pro/v1.1-ultra`。

## 图像混音：模型选择指南

可用于图像混音的模型：

### **flux-2/dev**（默认模型，免费）
- **适用场景**：通用混音、风格迁移、快速迭代
- **优势**：质量与速度平衡，提供 100 次免费请求
- **使用建议**：常规混音需求
- **端点**：`fal-ai/flux/dev/image-to-image`

### **flux-pro**（高级质量模型）
- **适用场景**：专业混音，高质量输出
- **优势**：更出色的质量，逼真的图像效果
- **使用建议**：需要专业级或用于发布的混音任务
- **端点**：`fal-ai/flux-pro`

### **flux-1.1-pro**（超高级模型）
- **适用场景**：需要最高质量图像的混音任务
- **优势**：超高的图像质量，细节保留度极高
- **使用建议**：高级项目，要求最佳效果的混音
- **端点**：`fal-ai/flux-pro/v1.1`

### **recraft/v3**（适用于矢量/插图）
- **适用场景**：矢量风格图像、品牌图像的混音
- **优势**：清晰的矢量输出，符合品牌风格的转换
- **使用建议**：将图像转换为矢量或插图格式
- **端点**：`fal-ai/recraft/v3/text-to-image`

### **stable-diffusion-v35**（艺术风格模型）
- **适用场景**：艺术风格图像、绘画效果、创意混音
- **优势**：强大的艺术风格应用能力
- **使用建议**：需要艺术风格或风格化转换的任务
- **端点**：`fal-ai/stable-diffusion-v35-large`

## 图像混音：命令行接口
```bash
uv run python fal-image-remix [OPTIONS] INPUT_IMAGE PROMPT

Arguments:
  INPUT_IMAGE               Path or URL to source image
  PROMPT                    How to transform the image

Options:
  -m, --model TEXT         Model to use (auto-selected if not specified)
  -o, --output TEXT        Output filename (default: remixed_TIMESTAMP.png)
  -s, --strength FLOAT     Transformation strength 0.0-1.0 (default: 0.75)
                           0.0 = preserve original, 1.0 = full transformation
  --guidance FLOAT         Guidance scale (default: 7.5)
  --seed INTEGER           Random seed for reproducibility
  --steps INTEGER          Number of inference steps
  --help                   Show help
```

### 混音强度控制

`--strength` 参数用于控制转换的强度：

| 强度 | 效果 | 使用场景 |
|---------|--------|----------|
| 0.3-0.5 | 微妙的变化 | 轻微的颜色调整、光线调整 |
| 0.5-0.7 | 中等程度的变化 | 在保留细节的同时调整风格 |
| 0.7-0.85 | 明显的变化 | 明确的风格转换 |
| 0.85-1.0 | 最大的变化 | 完整的风格重塑 |

## 混音示例
```bash
# Subtle artistic style (low strength)
uv run python fal-image-remix photo.jpg "Oil painting style" --strength 0.4

# Balanced transformation (default)
uv run python fal-image-remix input.jpg "Cyberpunk neon aesthetic"

# Strong transformation (high strength)
uv run python fal-image-remix portrait.jpg "Anime character" --strength 0.9

# Vector conversion
uv run python fal-image-remix -m recraft/v3 logo.png "Clean vector illustration"

# Premium quality remix
uv run python fal-image-remix -m flux-1.1-pro photo.jpg "Professional studio portrait"
```

## 图像编辑：模型选择指南

可用于针对性编辑和修复的模型：

### **flux-2/redux**（通用编辑模型）
- **适用场景**：无需遮罩的通用图像编辑
- **优势**：快速、平衡的编辑效果，适合整体调整
- **使用建议**：不需要针对特定区域进行编辑时
- **端点**：`fal-ai/flux-2/redux`

### **flux-2/fill**（修复模型，默认设置）
- **适用场景**：遮罩区域的编辑、对象去除、填充
- **优势**：无缝的修复效果，自然的融合
- **使用建议**：编辑带有遮罩的区域
- **端点**：`fal-ai/flux-2/fill`

### **flux-pro-v11/fill**（高级修复模型）
- **适用场景**：需要高质量修复的专业编辑
- **优势**：卓越的修复效果，专业级的修复质量
- **使用建议**：需要高级修复效果时
- **端点**：`fal-ai/flux-pro-v11/fill`

### **stable-diffusion-v35/inpainting**（艺术修复模型）
- **适用场景**：艺术风格的修复、创意性的图像修复
- **优势**：强大的艺术控制能力，详细的修复效果
- **使用建议**：需要艺术或风格化修复的任务
- **端点**：`fal-ai/stable-diffusion-v35-large/inpainting`

### **ideogram/v2/edit**（写实编辑模型）
- **适用场景**：需要高度写实效果的编辑
- **优势**：高度的写实效果，精确的编辑控制
- **使用建议**：需要高度写实修改的任务
- **端点**：`fal-ai/ideogram/v2/edit`

### **recraft/v3/svg**（矢量编辑模型）
- **适用场景**：矢量风格的编辑、清晰的插图处理
- **优势**：清晰的矢量输出，符合插图风格的编辑
- **使用建议**：进行矢量或插图编辑时
- **端点**：`fal-ai/recraft/v3/svg`

## 图像编辑：命令行接口
```bash
uv run python fal-image-edit [OPTIONS] INPUT_IMAGE [MASK_IMAGE] PROMPT

Arguments:
  INPUT_IMAGE               Path or URL to source image
  MASK_IMAGE                Path or URL to mask (white=edit, black=preserve) [optional]
  PROMPT                    How to edit the masked region

Options:
  -m, --model TEXT         Model to use (auto-selected if not specified)
  -o, --output TEXT        Output filename (default: edited_TIMESTAMP.png)
  --mask-prompt TEXT       Generate mask from text (no mask image needed)
  -s, --strength FLOAT     Edit strength 0.0-1.0 (default: 0.95)
  --guidance FLOAT         Guidance scale (default: 7.5)
  --seed INTEGER           Random seed for reproducibility
  --steps INTEGER          Number of inference steps
  --help                   Show help
```

### 编辑强度控制

`--strength` 参数用于控制编辑的强度：

| 强度 | 效果 | 使用场景 |
|---------|--------|----------|
| 0.5-0.7 | 轻微的编辑 | 轻微的调整、颜色调整 |
| 0.7-0.9 | 中等的编辑 | 在保持细节的同时进行明显的风格调整 |
| 0.85-1.0 | 显著的编辑 | 完整的风格转换 |

## 创建遮罩图像

遮罩图像用于定义编辑区域：
- **白色（255）**：需要编辑/修改的区域
- **黑色（0）**：需要保持不变的区域
- **灰色**：根据亮度进行部分融合

创建遮罩的方法：
- 使用图像编辑软件（如 GIMP、Photoshop、Krita）
- 使用绘画工具（选择并填充为白色/黑色）
- 使用基于文本的提示（`--mask-prompt` 参数）

## 编辑示例
```bash
# Edit with mask image
uv run python fal-image-edit photo.jpg mask.png "Replace with beautiful garden"

# Auto-generate mask from text
uv run python fal-image-edit landscape.jpg --mask-prompt "sky" "Make it sunset with clouds"

# Remove objects
uv run python fal-image-edit photo.jpg object_mask.png "Remove completely" --strength 1.0

# Seamless object insertion
uv run python fal-image-edit room.jpg region_mask.png "Add modern sofa" --strength 0.85

# General editing (no mask)
uv run python fal-image-edit -m flux-2/redux photo.jpg "Enhance lighting and saturation"

# Premium quality inpainting
uv run python fal-image-edit -m flux-pro-v11/fill image.jpg mask.png "Professional portrait background"

# Artistic modification
uv run python fal-image-edit -m stable-diffusion-v35/inpainting photo.jpg mask.png "Van Gogh style"
```

## 文件结构
```
fal-text-to-image/
├── SKILL.md                    # This file
├── README.md                   # Quick reference
├── pyproject.toml              # Dependencies (uv)
├── fal-text-to-image           # Text-to-image generation script
├── fal-image-remix             # Image-to-image remixing script
├── fal-image-edit              # Image editing/inpainting script
├── references/
│   └── model-comparison.md     # Detailed model benchmarks
└── outputs/                    # Generated images (created on first run)
```

## 依赖项

依赖项通过 `uv` 管理：
- `fal-client`：fal.ai 官方 Python SDK
- `python-dotenv`：环境变量管理工具
- `pillow`：图像处理和 EXIF 元数据处理库
- `click`：命令行接口库

## 最佳实践

### 通用建议
1. **模型选择**：除非有特殊需求，否则让脚本自动选择模型。
2. **提示设计**：提供具体且详细的提示以获得更好的结果。
3. **费用监控**：定期查看 fal.ai 控制台上的使用情况。
4. **可重复性**：使用 `--seed` 参数以确保每次迭代的结果一致。

### 文本转图像
1. **参考图像**：使用高质量的参考图像以获得最佳的风格迁移效果。
2. **尺寸选择**：根据使用需求选择合适的纵横比（正方形、横向、纵向）。
3. **模型选择**：对于文字设计使用 `recraft/v3`，对于专业摄影使用 `flux-pro`。

### 图像混音
1. **强度调整**：从默认值（0.75）开始，根据所需的转换效果进行调整。
2. **源图像质量**：高质量的源图像能产生更好的混音效果。
3. **迭代**：使用 `--seed` 参数使用不同的提示进行多次尝试。
4. **强度平衡**：较低的强度可以保留更多细节，较高的强度会产生更明显的变化。

### 图像编辑
1. **遮罩质量**：清晰、定义明确的遮罩能产生更好的效果。
2. **遮罩制作**：使用图像编辑软件进行精确控制，或使用 `--mask-prompt` 参数进行快速测试。
3. **融合效果**：在遮罩中使用灰色调以实现平滑的过渡效果。
4. **编辑强度**：使用 0.95 或更高的强度进行对象去除，0.7-0.9 的强度适合一般编辑。
5. **先测试**：在创建详细遮罩之前先使用 `--mask-prompt` 参数进行测试。
6. **分阶段编辑**：对于复杂的修改，建议分步骤进行编辑。

## 资源链接

- fal.ai 文档：https://docs.fal.ai/
- 模型试用平台：https://fal.ai/explore/search
- API 密钥：https://fal.ai/dashboard/keys
- 价格信息：https://fal.ai/pricing

## 工作流程示例

### 完整的图像创建流程
```bash
# 1. Generate base image
uv run python fal-text-to-image -m flux-2 "Modern office space, minimalist" -o base.png

# 2. Remix to different style
uv run python fal-image-remix base.png "Cyberpunk aesthetic with neon" -o styled.png

# 3. Edit specific region
uv run python fal-image-edit styled.png --mask-prompt "desk" "Add holographic display"
```

### 迭代优化
```bash
# Generate with seed for reproducibility
uv run python fal-text-to-image "Mountain landscape" --seed 42 -o v1.png

# Remix with same seed, different style
uv run python fal-image-remix v1.png "Oil painting style" --seed 42 -o v2.png

# Fine-tune with editing
uv run python fal-image-edit v2.png --mask-prompt "sky" "Golden hour lighting" --seed 42
```

### 对象去除与替换
```bash
# 1. Remove unwanted object
uv run python fal-image-edit photo.jpg object_mask.png "Remove" --strength 1.0 -o removed.png

# 2. Fill with new content
uv run python fal-image-edit removed.png region_mask.png "Beautiful flowers" --strength 0.9
```

## 故障排除

| 问题 | 解决方案 | 所需工具 |
|---------|----------|------|
| FAL_KEY 未设置 | 导出 FAL_KEY 或创建 `.env` 文件 | 所有相关操作 |
| 模型未找到 | 在文档中核对模型名称 | 所有相关操作 |
| 图像上传失败 | 确保图像文件存在且可读取 | 混音、编辑操作 |
| 遮罩无法使用 | 确保遮罩文件为灰度 PNG 格式（白色表示可编辑区域） | 编辑操作 |
| 转换效果过强 | 降低 `--strength` 值 | 重新混音或编辑 |
| 转换效果过弱 | 增加 `--strength` 值 | 重新混音或编辑 |
| `mask-prompt` 不准确 | 在图像编辑软件中手动创建遮罩 | 编辑操作 |
| 生成超时 | 尝试其他模型或等待更长时间 | 所有相关操作 |
| 超过使用频率限制 | 查看 fal.ai 控制台中的使用限制 | 所有相关操作 |

## 限制

### 通用限制
- 需要激活 fal.ai API 密钥。
- 受 fal.ai 使用频率限制和配额的影响。
- 需要互联网连接。
- 某些模型需要支付使用费用（请查看价格信息）。

### 文本转图像
- 图像参考功能仅限于特定模型。
- 不同模型的文字处理质量可能有所不同。

### 图像混音
- 源图像的质量会影响最终输出效果。
- 过高的强度设置可能会导致图像出现瑕疵。
- 某些风格可能更适合某些模型。

### 图像编辑
- 遮罩的质量对最终效果至关重要。
- 自动生成的遮罩（`--mask-prompt`）可能不如手动制作的遮罩精确。
- 复杂的编辑可能需要多次处理。
- 某些模型可能不支持所有编辑功能。