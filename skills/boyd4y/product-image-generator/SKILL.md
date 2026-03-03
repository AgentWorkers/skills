---
name: product-image-generator
description: 为电子商务平台（如 Amazon、Shopify、eBay 等）生成专业的产品图片。支持 8 种视觉风格和 6 种场景类型，这些风格和类型针对不同的产品类别进行了优化。当用户提到“商品图片”、“产品照片”、“Amazon 商品列表”或需要电子商务产品摄影时，可以使用该服务。
metadata:
  version: 1.0.0
---
# 电子商务产品图片生成器

本工具可生成专为电子商务平台优化的高质量产品图片，满足各平台的特定需求，并支持多种视觉风格。

## 使用方法

```bash
# Auto-select style based on product
/product-image-generator product-description.md

# Specify style
/product-image-generator product.md --style minimal

# Specify platform (auto-adjusts image requirements)
/product-image-generator product.md --platform amazon

# Specify scene type
/product-image-generator product.md --scene studio

# Combine options
/product-image-generator product.md --style premium --platform shopify --scene lifestyle

# Direct input
/product-image-generator
[paste product description]

# Direct input with options
/product-image-generator --style minimal --scene studio
[paste product description]

# With reference image (for style consistency)
/product-image-generator product.md --ref brand-style.png

# Multiple reference images
/product-image-generator product.md --ref style.png --ref competitor.jpg
```

## 选项

| 选项 | 描述 |
|--------|-------------|
| `--style <名称>` | 视觉风格（详见风格库） |
| `--scene <类型>` | 场景类型（详见场景库） |
| `--platform <名称>` | 电子商务平台（自动调整相关设置） |
| `--ref <路径>` | 参考图片（用于保持风格一致性） |

## 三大核心要素

| 要素 | 控制项 | 可选值 |
|--------|----------|---------|
| **风格** | 视觉效果：色调、光影处理 | 极简风、高级风、生活方式风、鲜明风、柔和风、科技风、自然风、奢华风 |
| **场景** | 背景与情境 | 拍摄环境、日常生活场景、产品使用场景、分解图、对比图、信息图 |
| **平台** | 平台要求 | Amazon、Shopify、eBay、Etsy、Taobao、JD.com、Pinduoduo |

风格、场景和平台可以自由组合。例如：`--style premium --scene lifestyle --platform amazon` 可生成符合 Amazon 图片要求的高端生活方式图片。

## 风格库

| 风格 | 描述 | 适用产品类型 |
|-------|-------------|----------|
| `minimal`（默认） | 简洁的白色背景，突出产品本身 | 电子产品、配件、专业产品 |
| `premium` | 精致的光线处理，细腻的阴影效果 | 奢侈品、珠宝、高端化妆品 |
| `lifestyle` | 产品在实际使用中的场景 | 家居用品、时尚产品、户外用品 |
| `bold` | 高对比度，色彩鲜艳，引人注目 | 运动产品、游戏用品、面向年轻人的产品 |
| `soft` | 温和的光线，柔和的色调 | 婴儿用品、护肤品、健康产品 |
| `tech` | 未来感强，设计时尚 | 电子产品、小工具、软件产品、人工智能产品 |
| `natural` | 自然、环保的色调 | 可持续发展产品、食品、天然化妆品 |
| `luxury` | 金色点缀，戏剧性的光线效果，丰富的色彩 | 高端品牌产品、珠宝、高端时尚 |

详细风格说明请参阅：`references/presets/<风格>.md`

## 场景库

| 场景 | 描述 | 图片数量 |
|-------|-------------|-------------|
| `studio`（默认） | 纯白色/渐变背景，专业的摄影棚灯光 | 1-3 张图片 |
| `lifestyle` | 产品在实际使用中的场景 | 2-5 张图片 |
| `contextual` | 产品置于特定环境中的场景 | 2-4 张图片 |
| `exploded` | 产品部件分解图，突出关键特征 | 3-6 张图片 |
| `comparison` | 产品使用前后的对比图 | 2-4 张图片 |
| `infographic` | 附带文字说明的产品特性和优势 | 2-5 张图片 |

## 平台要求

| 平台 | 主图片要求 | 额外图片要求 | 备注 |
|----------|------------|-------------------|-------|
| Amazon | 图像尺寸至少 1000x1000 像素，背景为纯白色 | 最多可上传 9 张图片 | 主图片必须使用纯白色背景 |
| Shopify | 推荐图像尺寸为 1024x1024 像素 | 图片数量无限制 | 建议使用 1:1 或 4:3 的比例 |
| eBay | 图像尺寸至少 500x500 像素 | 最多可上传 12 张免费图片 | 建议使用白色背景 |
| Etsy | 图像尺寸至少 760x760 像素 | 最多可上传 10 张图片 | 生活方式风格的图片效果较好 |
| Taobao | 图像尺寸至少 800x800 像素 | 最多可上传 15 张图片 | 信息图风格受欢迎 |
| JD.com | 图像尺寸至少 800x800 像素 | 最多可上传 15 张图片 | 需要简洁专业的图片风格 |
| Pinduoduo | 图像尺寸至少 750x750 像素 | 最多可上传 10 张图片 | 侧重展示产品价值 |

各平台的详细要求请参阅：`references/platforms/<平台>.md`

## 自动选择规则

| 产品类别 | 推荐风格 | 推荐场景 |
|------------------|-------|-------|
| 电子产品、小工具 | `tech` 或 `minimal` | 拍摄环境 + 产品部件分解图 |
| 时尚、配件 | `premium` 或 `lifestyle` | 日常生活场景 + 产品使用场景 |
| 美容、化妆品 | `soft` 或 `premium` | 拍摄环境 + 产品使用场景 |
| 家居用品、家具 | `lifestyle` 或 `natural` | 产品使用场景 + 环境背景 |
| 运动、户外用品 | `bold` 或 `lifestyle` | 日常生活场景 + 环境背景 |
| 珠宝、奢侈品 | `luxury` 或 `premium` | 拍摄环境 + 产品使用场景 |
| 婴儿用品、儿童用品 | `soft` 或 `natural` | 日常生活场景 + 环境背景 |
| 食品、保健品 | `natural` 或 `minimal` | 拍摄环境 + 信息图 |

## 设计策略

### 策略 A：产品聚焦型

| 设计要点 | 描述 |
|--------|-------------|
| **核心理念** | 以产品为中心，简洁明了的展示方式 |
| **重点元素** | 从多个角度展示产品，提供细节特写 |
| **适用产品** | 电子产品、配件、奢侈品 |
| **设计结构** | 主图片 → 多角度展示 → 产品细节特写 → 产品尺寸/使用环境说明 |

### 策略 B：场景融入型

| 设计要点 | 描述 |
|--------|-------------|
| **核心理念** | 将产品置于真实使用环境中展示 |
| **重点元素** | 强调产品的使用场景和情感联系 |
| **适用产品** | 家居用品、时尚产品、户外用品 |
| **设计结构** | 产品使用场景图片 → 使用场景说明 → 产品优势展示 |

### 策略 C：信息传达型

| 设计要点 | 描述 |
|--------|-------------|
| **核心理念** | 清晰传达产品特性和优势 |
| **重点元素** | 通过文字说明和标注突出关键信息 |
| **适用产品** | 复杂产品、工具、保健品 |
| **设计结构** | 主图片展示核心优势 → 产品特性分解 → 产品对比 → 详细规格/使用方法 |

## 文件结构

每个产品的图片生成过程会创建一个独立的文件夹，文件夹名称由产品名称组成（采用驼峰式命名法，例如：`wireless-earbuds`）。

**文件名生成规则**：
1. 从产品名称中提取 2-4 个单词作为文件夹名（驼峰式命名法）。

**冲突解决规则**：
如果文件夹 `product-images/{产品名称}` 已经存在，会在文件夹名后添加时间戳（格式为 `{产品名称}-YYYYMMDD-HHMMSS`）。

## 工作流程

### 进度检查表

```
Product Image Generation Progress:
- [ ] Step 0: Check preferences (EXTEND.md) ⛔ BLOCKING
- [ ] Step 1: Analyze product → analysis.md
- [ ] Step 2: Confirmation 1 - Product understanding ⚠️ REQUIRED
- [ ] Step 3: Generate 3 outline + style variants
- [ ] Step 4: Confirmation 2 - Outline & style & platform ⚠️ REQUIRED
- [ ] Step 5: Generate images (sequential)
- [ ] Step 6: Completion report
```

### 流程图

```
Input → [Step 0: Preferences] ─┬─ Found → Continue
                               │
                               └─ Not found → First-Time Setup ⛔ BLOCKING
                                              │
                                              └─ Complete setup → Save EXTEND.md → Continue
                                                                                      │
        ┌─────────────────────────────────────────────────────────────────────────────┘
        ↓
Analyze → [Confirm 1] → 3 Outlines → [Confirm 2: Outline + Style + Platform] → Generate → Complete
```

### 第 0 步：加载用户偏好设置（EXTEND.md） ⛔ 此步骤为必填

**目的**：加载用户偏好设置或执行首次设置。

**重要提示**：如果未找到 EXTEND.md 文件，必须先完成首次设置才能继续后续步骤。

使用 Bash 命令检查 EXTEND.md 文件是否存在：

```bash
# Check project-level first
test -f .teamclaw-skills/product-image-generator/EXTEND.md && echo "project"

# Then user-level
test -f "$HOME/.teamclaw-skills/product-image-generator/EXTEND.md" && echo "user"
```

| 检查结果 | 应采取的行动 |
|--------|--------|
| 文件存在 | 读取文件内容，解析后显示摘要 → 继续执行第 1 步 |
| 文件不存在 | ⛔ 此步骤为必填：执行首次设置 → 保存 EXTEND.md 文件 → 然后继续执行第 1 步 |

**首次设置流程**（当 EXTEND.md 文件不存在时）：
使用 `AskUserQuestion` 脚本一次性收集所有用户设置信息：

1. **默认平台选择**：Amazon / Shopify / eBay / Etsy / Taobao / JD.com / Pinduoduo / 无特定偏好 |
2. **默认风格选择**：极简风 / 高级风 / 日常生活风 / 明显风 / 柔和风 / 科技风 / 自然风 / 奢侈风 |
3. **水印设置**：是否启用水印（如启用，请指定水印文字和位置 |
4. **语言设置**：中文 / 英文 / 自动检测语言

详细设置信息请参阅：`references/config/preferences-schema.md`

### 第 1 步：分析产品信息 → `analysis.md`

**操作步骤**：
1. **保存原始产品信息**：
   - 如果提供了文件路径，直接使用该文件；
   - 如果信息是手动粘贴的，保存到 `source.md` 文件中；
   **备份规则**：如果原始文件已存在，将其重命名为 `source-backup-YYYYMMDD-HHMMSS.md`。
2. 阅读并分析产品信息，确定：
   - 产品类别；
   - 目标受众；
   - 产品的主要特点和卖点；
   - 产品的市场定位；
   - 产品的视觉表现潜力。
3. 根据分析结果，确定所需的图片数量和类型。
4. 提出相关问题以进一步明确设计方向（详见第 2 步）。
5. 将分析结果保存到 `analysis.md` 文件中。

### 第 2 步：确认用户需求 ⚠️

**目的**：验证用户理解情况并收集缺失的信息。

**显示确认内容**：
- 产品类别；
- 产品的主要特点；
- 目标受众；
- 适合的平台选择。

**使用 `AskUserQuestion` 脚本收集以下信息**：
1. **主要卖点**（多选）：
   - 设计/外观；
   - 功能/特性；
   - 价格/性价比；
   - 质量/耐用性；
   - 品牌/地位；
   - 创新性/技术含量；
   - 可持续性/环保性；
   - 便利性/易用性。
2. **目标客户群体**：
   - 注重预算的客户；
   | 关注质量的客户；
   | 倾向于购买奢侈品的客户；
   | 熟悉技术的客户；
   | 关注环保的客户；
   | 家庭用户；
   | 专业人士/企业用户；
   | 关注潮流的年轻用户。
3. **产品的主要使用场景**：
   | 室内/家居环境；
   | 户外环境；
   | 办公环境；
   | 旅行场景；
   | 运动/健身场景；
   | 社交活动场景；
   | 交通工具使用场景。
4. **其他相关信息**（可选）。

**根据用户反馈更新 `analysis.md` 文件，然后进入第 3 步。

### 第 3 步：生成三种设计方案及风格建议

为产品生成三种不同的设计方案，每种方案包含具体的设计结构和视觉风格建议。

| 设计方案 | 文件名 | 设计重点 | 推荐风格 |
|----------|----------|-------|-------------------|
| A | `outline-strategy-a.md` | 产品聚焦型 | 极简风、科技风 |
| B | `outline-strategy-b.md` | 日常生活融入型 | 柔和风、自然风 |
| C | `outline-strategy-c.md` | 信息传达型 | 明显风、信息图风格 |

**设计方案文件格式**（使用 YAML 格式编写文件开头部分）：

```yaml
---
strategy: a  # a, b, or c
name: Product-Focused
style: minimal
style_reason: "Clean presentation highlights product design and build quality"
scene: studio
platform: amazon
image_count: 5
---

## P1 Hero Shot
**Type**: hero
**Purpose**: Main product image, first impression
**Visual**: Product on pure white background, professional lighting
**Platform**: Amazon main image compliant (1000x1000, pure white)

## P2 Angle Variation
**Type**: angle
**Purpose**: Show product from different perspective
**Visual**: 45-degree angle, slight shadow for depth

## P3 Detail Close-up
**Type**: detail
**Purpose**: Highlight key feature or quality detail
**Visual**: Macro shot of texture/material/connection point

...
```

**根据用户反馈更新 `analysis.md` 文件，然后进入第 3 步。**

### 第 4 步：选择设计方案、视觉风格和平台 ⚠️

**目的**：让用户选择设计方案、视觉风格和目标平台。

**展示每种设计方案的详细信息**：
- 设计方案名称；
- 需要生成的图片数量；
- 推荐的视觉风格。
**使用 `AskUserQuestion` 脚本收集用户反馈**：
1. **设计方案选择**：
   - 方案 A（产品聚焦型）；
   - 方案 B（日常生活融入型）；
   - 方案 C（信息传达型）；
   - 如果选择组合方案，请指定每种方案所需的图片。
2. **视觉风格选择**：
   - 选择设计方案推荐的风格；
   - 或者从以下选项中选择：极简风、高级风、柔和风、科技风、自然风、奢华风；
   - 或者自定义风格描述。
3. **平台选择**：
   | 选择设计方案推荐的平台；
   | 或者从以下选项中选择：Amazon / Shopify / eBay / Etsy / Taobao / JD.com；
   | 或者自定义平台要求。
4. **场景类型选择**：
   | 选择设计方案推荐的场景类型；
   | 或者从以下选项中选择：拍摄环境、日常生活场景、产品使用场景、产品分解图、对比图、信息图。
**根据用户反馈**：
- 如果用户选择了某种设计方案，将其设置内容复制到 `outline.md` 文件中；
- 如果选择了组合方案，合并所有指定的图片；
- 更新 `outline.md` 文件的开头部分，包含最终的设计方案和图片设置。

### 第 5 步：生成图片

根据用户选择的方案、视觉风格和场景要求生成图片：

**确保视觉一致性**：
1. **检查用户提供的参考图片**（使用 `--ref` 选项）：
   - 如果提供了参考图片，将其作为主要风格参考；
   - 如果没有提供参考图片，使用内部参考图片库（详见下文）。
2. **使用内部参考图片库**（当用户未提供参考图片时）：
   - **首先生成主图片**（无需 `--ref` 选项）；
   - **使用生成的主图片作为后续所有图片的参考**（例如：`--ref <用户提供的参考图片路径>`）。
   **生成其他图片时**：
     - 如果有用户提供的参考图片，使用 `--ref` 选项；
     - **如果没有用户提供的参考图片**，首先生成主图片，然后使用该图片作为后续图片的参考；
     - **生成其他图片时，使用 `--ref <参考图片路径>` 选项。
3. **保存生成图片的提示文件**：
   - 为每个图片生成一个提示文件，文件名为 `prompts/NN-{类型}-[产品名称].md`；
   **备份规则**：如果文件已存在，将其重命名为 `prompts/NN-{类型}-[产品名称]-backup-YYYYMMDD-HHMMSS.md`；
   - 在提示文件中包含参考图片的路径。
4. **生成图片后**：
   - 如果有用户提供的参考图片，使用相应的 `--ref` 选项；
   - **如果没有用户提供的参考图片**，首先生成主图片，然后使用该图片作为后续图片的参考；
   - **生成其他图片时**，使用提供的参考图片路径。

**参考图片使用指南**：
- **风格参考图片**：确保图片符合品牌风格；
- **竞争对手参考图片**：选择与产品类别相符的参考图片；
- **内部参考图片库**：首先生成的主图片用于保证图片系列的一致性。

**平台特定要求**：
- 自动应用平台的图片格式要求：
  - Amazon：主图片背景必须为纯白色（RGB 255,255,255）；
  - 图像尺寸至少为 1000x1000 像素（以便支持缩放功能）；
  - 主图片上不得包含文字、LOGO 或水印；
  - 允许使用额外的生活场景图片和信息图。
- **Shopify**：
  - 推荐图片尺寸为 1024x1024 像素或 4:3 的比例；
  - 更灵活的风格设计；
  - 生活方式风格的图片效果较好；
  - 所有产品图片的风格需保持一致。
- **eBay**：
  - 图像尺寸至少为 500x500 像素；
  - 建议使用白色背景，但非强制要求；
  - 每个商品最多可上传 12 张免费图片。
- **其他平台的具体要求**：
  见相应的平台文档。

## 文件管理规则

- 所有生成的图片使用统一的会话 ID：`product-{产品名称}-{时间戳}`。

### 第 6 步：完成报告

```
Product Image Set Complete!

Product: [product name]
Strategy: [A/B/C/Combined]
Style: [style name]
Scene: [scene type]
Platform: [platform] (requirements applied)
Location: [directory path]
Images: N total

✓ analysis.md
✓ outline-strategy-a.md
✓ outline-strategy-b.md
✓ outline-strategy-c.md
✓ outline.md (selected: [strategy])

Files:
- 01-hero-[slug].png ✓ Main image ([platform] compliant)
- 02-angle-[slug].png ✓ Angle variation
- 03-detail-[slug].png ✓ Detail shot
...
```

## 图片后期处理

| 操作 | 具体步骤 |
|--------|-------|
| **编辑图片** | 首先编辑提示文件，然后使用相同的会话 ID 重新生成图片 |
| **添加新图片** | 指定图片在页面中的位置，生成新的提示文件，然后生成图片，并重新编号文件 |
| **删除图片** | 删除旧的图片文件，重新编号剩余的文件，并更新相应的文件列表 |

## 平台特定要求

- **Amazon**：
  - 主图片背景必须为纯白色（RGB 255,255,255）；
  - 图像尺寸至少为 1000x1000 像素；
  - 产品必须占据画面的 85% 以上；
  - 主图片上不得包含文字、LOGO 或水印；
  - 允许使用生活场景图片、信息图和对比图。
- **Shopify**：
  - 推荐图片尺寸为 1024x1024 像素或 4:3 的比例；
  - 更灵活的风格设计；
  - 生活方式风格的图片效果较好；
  - 所有产品图片的风格需保持一致。
- **eBay**：
  - 图像尺寸至少为 500x500 像素；
  - 建议使用白色背景，但非强制要求；
  - 每个商品最多可上传 12 张免费图片。
- **其他平台的具体要求**：
  见相应的平台文档。

## 其他注意事项

- 如操作失败，系统会自动尝试重新生成图片；
- 系统会自动应用平台的特定要求；
- 需要用户完成两次确认（第 2 步和第 4 步）；
- 使用参考图片库以确保图片的视觉一致性。

## 扩展功能

通过修改 `EXTEND.md` 文件可以自定义配置。具体操作方法请参见第 0 步的说明。