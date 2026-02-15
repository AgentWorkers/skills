---
name: logo-design-guide
description: |
  Logo design principles and AI image generation best practices for creating logos.
  Covers logo types, prompting techniques, scalability rules, and iteration workflows.
  Use for: brand identity, startup logos, app icons, favicons, logo concepts.
  Triggers: logo design, create logo, brand logo, logo generation, ai logo,
  logo maker, icon design, brand mark, logo concept, startup logo, app icon logo
allowed-tools: Bash(infsh *)
---

# 标志设计指南

通过 [inference.sh](https://inference.sh) 命令行工具，利用人工智能图像生成技术来设计有效的标志。

## 快速入门

```bash
curl -fsSL https://cli.inference.sh | sh && infsh login

# Generate a logo concept
infsh app run falai/flux-dev-lora --input '{
  "prompt": "flat vector logo of a mountain peak with a sunrise, minimal geometric style, single color, clean lines, white background",
  "width": 1024,
  "height": 1024
}'
```

## 标志类型

| 类型 | 描述 | 适用场景 | 示例 |
|------|-------------|-------------|---------|
| **文字标志** | 以标志形式呈现的公司名称 | 品牌名称简洁（少于10个字符） | Google、Coca-Cola |
| **字母标志** | 仅使用首字母 | 公司名称较长，正式场合使用 | IBM、HBO、CNN |
| **图形标志** | 易于识别的图标/符号 | 适用于通用品牌，无需文字 | Apple、Twitter的鸟形图标 |
| **抽象标志** | 几何形状或非具象的图形 | 科技公司或概念性品牌 | Nike的Swoosh标志、Pepsi的标志 |
| **吉祥物标志** | 以字符或形象为特色的标志 | 适合友好型品牌或食品/体育相关品牌 | KFC的Colonel标志、Pringles的标志 |
| **组合标志** | 图标与文字标志结合 | 需要同时具备识别度和名称的新品牌 | Burger King、Adidas的标志 |

## 人工智能的局限性

**人工智能图像生成工具无法可靠地处理文本。** 文字可能会变形、拼写错误或出现乱码。

**应对策略：**
1. 仅使用人工智能生成图标/符号。
2. 在设计工具（如Figma、Canva、Illustrator）中添加文字/文字标志。
3. 或者采用组合方式：先使用人工智能生成图标，再手动设置文字。

## 设计标志时的提示词

### 有效的提示词

```
flat vector logo, simple minimal icon, single color silhouette,
geometric logo mark, clean lines, negative space design,
line art logo, flat design icon, minimalist symbol
```

### 无效的提示词

```
❌ photorealistic logo (contradiction — logos aren't photos)
❌ 3D rendered logo (too complex, won't scale down)
❌ gradient logo (inconsistent results, hard to reproduce)
❌ logo with text "Company Name" (text rendering fails)
```

### 提示词的结构

```
flat vector logo of [subject], [style], [color constraint], [background], [additional detail]
```

### 各类型标志的示例

```bash
# Abstract geometric
infsh app run falai/flux-dev-lora --input '{
  "prompt": "flat vector abstract logo, interlocking hexagonal shapes forming a letter S, minimal geometric style, single navy blue color, white background, clean sharp edges"
}'

# Pictorial nature
infsh app run falai/flux-dev-lora --input '{
  "prompt": "flat vector logo of a fox head in profile, geometric faceted style, orange and white, minimal clean lines, white background, negative space design"
}'

# Mascot style
infsh app run bytedance/seedream-4-5 --input '{
  "prompt": "friendly cartoon owl mascot logo, simple flat illustration, wearing graduation cap, purple and gold colors, white background, clean vector style"
}'

# Tech abstract
infsh app run xai/grok-imagine-image-pro --input '{
  "prompt": "minimal abstract logo mark, interconnected nodes forming a brain shape, line art style, single teal color, white background, tech startup aesthetic"
}'
```

## 可扩展性要求

标志必须适用于各种尺寸：

| 使用场景 | 尺寸 | 必须满足的条件 |
|---------|------|----------------|
| 网站图标（Favicon） | 16x16像素 | 图标轮廓清晰可辨 |
| 应用程序图标 | 1024x1024像素 | 图标细节完整可见 |
| 社交媒体头像 | 400x400像素 | 一眼就能看清楚 |
| 名片 | 约1英寸大小 | 印刷效果清晰 |
| 广告牌 | 超过10英尺高 | 无像素化，设计简单 |

### 可扩展性检查清单

- [ ] 作为16像素的Favicon时仍可识别（眯眼看也能辨认）
- [ ] 在单色背景下（黑白）仍可识别
- [ ] 在反色背景下（黑白）仍可识别
- [ ] 小尺寸下没有细节丢失
- [ ] 线条细小不会在缩小后消失
- [ ] 轮廓清晰，无需依赖颜色

## 颜色指南

- **主要标志的颜色不超过2-3种**
- 必须能在**单色**背景下显示（黑色、白色或品牌主色调）
- 考虑**色彩心理学**：
  - 蓝色：代表信任、专业（金融、科技、医疗）
  - 红色：代表活力、紧迫感（食品、娱乐、零售）
  - 绿色：代表成长、自然（健康、可持续性、金融）
  - 橙色：代表友好、创意（初创企业、年轻品牌）
  - 紫色：代表奢华、智慧（美容、教育）
  - 黑色：代表高端、优雅（时尚、奢侈品、科技）
- 在浅色和深色背景下都进行测试

## 设计迭代流程

```bash
# Step 1: Generate 5-10 broad concepts
for i in {1..5}; do
  infsh app run falai/flux-dev-lora --input '{
    "prompt": "flat vector logo of a lighthouse, minimal geometric, single color, white background"
  }' --no-wait
done

# Step 2: Refine the best concept with variations
infsh app run falai/flux-dev-lora --input '{
  "prompt": "flat vector logo of a geometric lighthouse with light beam rays, minimal line art, navy blue, white background, negative space design"
}'

# Step 3: Generate at high resolution for final
infsh app run bytedance/seedream-4-5 --input '{
  "prompt": "flat vector logo of a geometric lighthouse with radiating light beams, minimal clean design, navy blue single color, pure white background",
  "size": "2K"
}'

# Step 4: Upscale for production use
infsh app run falai/topaz-image-upscaler --input '{
  "image": "path/to/best-logo.png",
  "scale": 4
}'
```

## 常见错误

| 错误 | 问题 | 解决方法 |
|---------|---------|-----|
| 细节过多 | 小尺寸时轮廓模糊 | 简化为基本形状 |
| 过度依赖颜色 | 在黑白背景下无法识别 | 先设计纯黑色的版本 |
| 人工智能生成的文字 | 文字出现乱码或拼写错误 | 先生成图标，再手动添加文字 |
- 过于追求潮流的效果（如发光、阴影） | 易过时，打印时可能出现问题 | 保持设计简洁、 timeless（永恒的设计风格） |
- 颜色过多 | 打印时难以呈现，成本较高 | 颜色不超过2-3种 |
- 无意义的不对称设计 | 看起来不完整 | 有意识地使用不对称设计，或保持对称性 |

## 文件格式及用途

| 格式 | 适用场景 |
|--------|----------|
| SVG | 可缩放的矢量格式，适用于网页和编辑 |
| PNG（透明背景） | 数字用途，如演示文稿 |
| PNG（白色背景） | 文档、电子邮件签名 |
| ICO / Favicon | 网站图标（16x16px、32x16px、48x16px） |
| 高分辨率PNG（4096px以上） | 打印、广告牌 |

**注意：** 人工智能生成的图像为位图（PNG格式）。如需真正的矢量SVG格式，可将AI生成的图像作为参考，在矢量编辑工具中重新绘制，或使用AI转SVG的工具进行转换。

## 相关技能

```bash
npx skills add inferencesh/skills@ai-image-generation
npx skills add inferencesh/skills@prompt-engineering
```

查看所有可用工具：`infsh app list`