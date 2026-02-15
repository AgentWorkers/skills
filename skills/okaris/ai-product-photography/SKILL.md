---
name: ai-product-photography
description: |
  Generate professional AI product photography and commercial images.
  Models: FLUX, Imagen 3, Grok, Seedream for product shots, lifestyle images, mockups.
  Capabilities: studio lighting, lifestyle scenes, packaging, e-commerce photos.
  Use for: e-commerce, Amazon listings, Shopify, marketing, advertising, mockups.
  Triggers: product photography, product shot, commercial photography, e-commerce images,
  amazon product photo, shopify images, product mockup, studio product shot,
  lifestyle product image, advertising photo, packshot, product render, product image ai
allowed-tools: Bash(infsh *)
---

# 人工智能产品摄影

通过 [inference.sh](https://inference.sh) 命令行工具生成专业的产品摄影图片。

## 快速入门

```bash
curl -fsSL https://cli.inference.sh | sh && infsh login

# Generate product shot
infsh app run falai/flux-dev --input '{
  "prompt": "Professional product photo of wireless earbuds on white surface, soft studio lighting, commercial photography, high detail"
}'
```

## 可用模型

| 模型 | 应用 ID | 适用场景 |
|-------|--------|----------|
| FLUX Dev | `falai/flux-dev` | 高质量、细节丰富 |
| FLUX Schnell | `falai/flux-schnell` | 快速迭代 |
| Imagen 3 | `google/imagen-3` | 真实感强 |
| Grok | `xai/grok-imagine-image` | 创意风格 |
| Seedream | `bytedance/seedream-3-0` | 商业级质量 |

## 产品摄影风格

### 摄影棚白背景

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

### 产品特写（Hero Shot）

```bash
infsh app run falai/flux-dev --input '{
  "prompt": "Hero product shot of smartphone floating at angle, dramatic lighting, gradient background, tech advertising style, premium feel"
}'
```

### 平铺展示（Flat Lay）

```bash
infsh app run falai/flux-dev --input '{
  "prompt": "Flat lay product photography of skincare products arranged aesthetically, marble surface, eucalyptus leaves as props, beauty brand style"
}'
```

### 使用中/动态场景（In-Use / Action）

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

### 柔和的摄影棚灯光

```bash
infsh app run falai/flux-dev --input '{
  "prompt": "Product photo with soft diffused studio lighting, minimal shadows, clean and professional, commercial photography"
}'
```

### 戏剧性灯光/边缘光

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

### Amazon 主图片

```bash
infsh app run falai/flux-dev --input '{
  "prompt": "Amazon product listing main image, pure white background RGB 255 255 255, product fills 85% of frame, professional studio lighting, no text or graphics"
}'
```

### Amazon 生活方式图片

```bash
infsh app run falai/flux-dev --input '{
  "prompt": "Amazon lifestyle product image, product in natural use context, relatable setting, shows scale and use case"
}'
```

### Shopify 产品特写

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

## 后期处理流程

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

## 生成提示语（Prompt Formula）

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

1. **保持风格一致** - 所有图片都要符合品牌美学风格。
2. **高分辨率** - 使用高质量的模型，必要时进行图像放大处理。
3. **多角度拍摄** - 生成正面、侧面和细节图片。
4. **场景的重要性** - 与生活场景相关的图片效果更好。
5. **道具与场景布置** - 添加相关的道具以增加视觉趣味性。
6. **照明一致性** - 所有产品的照明风格要保持一致。

## 相关技能

```bash
# Image generation models
npx skills add inference-sh/agent-skills@ai-image-generation

# FLUX specific
npx skills add inference-sh/agent-skills@flux-image

# Image upscaling
npx skills add inference-sh/agent-skills@image-upscaling

# Background removal
npx skills add inference-sh/agent-skills@background-removal

# Full platform skill
npx skills add inference-sh/agent-skills@inference-sh
```

查看所有图像生成工具：`infsh app list --category image`