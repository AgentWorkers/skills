---
name: ai-product-photography
description: "生成专业级的人工智能产品照片和商业图片。支持的模型包括 FLUX、Imagen 3、Grok 和 Seedream，可用于产品拍摄、生活方式图片以及模型制作。具备以下功能：工作室照明、生活场景模拟、包装设计以及电商图片制作。适用场景包括电子商务、亚马逊商品列表、Shopify 平台、市场营销和广告宣传。相关术语包括：产品摄影、商业摄影、电商图片、亚马逊产品图片、Shopify 图片、产品模型、生活场景图片、广告图片等。"
allowed-tools: Bash(infsh *)
---
# 人工智能产品摄影

通过 [inference.sh](https://inference.sh) 命令行工具生成专业的产品摄影图片。

![人工智能产品摄影](https://cloud.inference.sh/app/files/u/4mg21r6ta37mpaz6ktzwtt8krr/01kg0v0nz7wv0qwqjtq1cam52z.jpeg)

## 快速入门

```bash
curl -fsSL https://cli.inference.sh | sh && infsh login

# Generate product shot
infsh app run falai/flux-dev --input '{
  "prompt": "Professional product photo of wireless earbuds on white surface, soft studio lighting, commercial photography, high detail"
}'
```

> **安装说明：** [安装脚本](https://cli.inference.sh) 仅会检测您的操作系统和架构，然后从 `dist.inference.sh` 下载相应的二进制文件，并验证其 SHA-256 校验和。无需提升权限或运行后台进程。也可以通过 [手动安装与验证](https://dist.inference.sh/cli/checksums.txt) 来完成安装。

## 可用模型

| 模型 | 应用 ID | 适用场景 |
|-------|--------|----------|
| FLUX Dev | `falai/flux-dev` | 高质量、细节丰富 |
| FLUX Schnell | `falai/flux-schnell` | 快速迭代 |
| Imagen 3 | `google/imagen-3` | 真实感强 |
| Grok | `xai/grok-imagine-image` | 创意风格 |
| Seedream | `bytedance/seedream-3-0` | 商业级质量 |

## 产品摄影风格

### 影室白背景

```bash
infsh app run falai/flux-dev --input '{
  "prompt": "Product photography of a luxury watch on pure white background, professional studio lighting, sharp focus, e-commerce style, high resolution"
}'
```

### 生活方式场景

```bash
infsh app run falai/flux-dev --input '{
  "prompt": "Lifestyle product photo of coffee mug on wooden desk, morning sunlight through window, cozy home office setting, Instagram aesthetic"
}'
```

### 产品特写

```bash
infsh app run falai/flux-dev --input '{
  "prompt": "Hero product shot of smartphone floating at angle, dramatic lighting, gradient background, tech advertising style, premium feel"
}'
```

### 平铺展示

```bash
infsh app run falai/flux-dev --input '{
  "prompt": "Flat lay product photography of skincare products arranged aesthetically, marble surface, eucalyptus leaves as props, beauty brand style"
}'
```

### 使用中/动态场景

```bash
infsh app run falai/flux-dev --input '{
  "prompt": "Action shot of running shoes mid-stride, motion blur background, athletic lifestyle, Nike advertisement style"
}'
```

## 产品类别

### 电子产品

```bash
infsh app run falai/flux-dev --input '{
  "prompt": "Professional product photo of wireless headphones, matte black finish, floating on dark gradient background, rim lighting, tech product photography"
}'
```

### 服装/服饰

```bash
infsh app run falai/flux-dev --input '{
  "prompt": "Fashion product photography of leather handbag, studio setting, soft shadows, luxury brand aesthetic, Vogue style"
}'
```

### 美容/化妆品

```bash
infsh app run falai/flux-dev --input '{
  "prompt": "Beauty product photography of lipstick with color swatches, clean white background, soft lighting, high-end cosmetics advertising"
}'
```

### 食品与饮料

```bash
infsh app run falai/flux-dev --input '{
  "prompt": "Food photography of craft beer bottle with condensation, rustic wooden table, warm lighting, artisanal brand aesthetic"
}'
```

### 家居与家具

```bash
infsh app run falai/flux-dev --input '{
  "prompt": "Interior product photo of modern armchair in minimalist living room, natural lighting, Scandinavian design style, lifestyle context"
}'
```

### 珠宝

```bash
infsh app run falai/flux-dev --input '{
  "prompt": "Jewelry product photography of diamond ring, black velvet surface, dramatic spotlight, sparkle and reflection, luxury advertising"
}'
```

## 照明技巧

### 软质室内光

```bash
infsh app run falai/flux-dev --input '{
  "prompt": "Product photo with soft diffused studio lighting, minimal shadows, clean and professional, commercial photography"
}'
```

### 戏剧性光线/边缘光

```bash
infsh app run falai/flux-dev --input '{
  "prompt": "Product photo with dramatic rim lighting, dark background, glowing edges, premium tech aesthetic"
}'
```

### 自然窗光

```bash
infsh app run falai/flux-dev --input '{
  "prompt": "Product photo with natural window light, soft shadows, lifestyle setting, warm and inviting"
}'
```

### 强烈光线/高对比度

```bash
infsh app run falai/flux-dev --input '{
  "prompt": "Product photo with hard directional lighting, strong shadows, bold contrast, editorial style"
}'
```

## 电子商务模板

### 亚马逊主图

```bash
infsh app run falai/flux-dev --input '{
  "prompt": "Amazon product listing main image, pure white background RGB 255 255 255, product fills 85% of frame, professional studio lighting, no text or graphics"
}'
```

### 亚马逊生活方式图片

```bash
infsh app run falai/flux-dev --input '{
  "prompt": "Amazon lifestyle product image, product in natural use context, relatable setting, shows scale and use case"
}'
```

### Shopify 产品主图

```bash
infsh app run falai/flux-dev --input '{
  "prompt": "Shopify hero banner product image, lifestyle context, space for text overlay on left, premium brand aesthetic"
}'
```

## 批量生成

```bash
# Generate multiple angles
PRODUCT="luxury watch"
ANGLES=("front view" "45 degree angle" "side profile" "detail shot of face")

for angle in "${ANGLES[@]}"; do
  infsh app run falai/flux-dev --input "{
    \"prompt\": \"Professional product photography of $PRODUCT, $angle, white background, studio lighting\"
  }" > "product_${angle// /_}.json"
done
```

## 后处理工作流程

```bash
# 1. Generate base product image
infsh app run falai/flux-dev --input '{
  "prompt": "Product photo of headphones..."
}' > product.json

# 2. Upscale for high resolution
infsh app run falai/topaz-image-upscaler --input '{
  "image_url": "<product-url>",
  "scale": 2
}' > upscaled.json

# 3. Remove background if needed
infsh app run falai/birefnet --input '{
  "image_url": "<upscaled-url>"
}' > cutout.json
```

## 提示语格式

```
[Product Type] + [Setting/Background] + [Lighting] + [Style] + [Technical]
```

### 示例图片

```
"Wireless earbuds on white marble surface, soft studio lighting, Apple advertising style, 8K, sharp focus"

"Sneakers floating on gradient background, dramatic rim lighting, Nike campaign aesthetic, commercial photography"

"Skincare bottle with water droplets, spa setting with stones, natural lighting, luxury beauty brand style"
```

## 最佳实践

1. **保持风格一致性** - 所有图片都要符合品牌美学风格。
2. **高分辨率** - 使用高质量的模型，必要时进行图像放大处理。
3. **多角度拍摄** - 生成产品的正面、侧面和细节图。
4. **场景的重要性** - 与实际使用场景相关的图片效果更佳。
5. **添加道具和场景布置** - 使用相关道具提升视觉效果。
6. **统一照明风格** - 所有产品的照明效果要保持一致。

## 相关技能

```bash
# Image generation models
npx skills add inference-sh/skills@ai-image-generation

# FLUX specific
npx skills add inference-sh/skills@flux-image

# Image upscaling
npx skills add inference-sh/skills@image-upscaling

# Background removal
npx skills add inference-sh/skills@background-removal

# Full platform skill
npx skills add inference-sh/skills@inference-sh
```

浏览所有图像生成工具：`infsh app list --category image`