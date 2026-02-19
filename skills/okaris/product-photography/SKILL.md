---
name: product-photography
description: "使用摄影棚灯光进行AI产品摄影，包括生活方式照片的拍摄以及产品包装图的制作。内容涵盖拍摄角度、背景选择、阴影处理方法、产品特写（hero shot）的拍摄技巧，以及电商图片所需的标准。适用场景包括：产品照片、电商图片、亚马逊商品列表、产品包装图、生活方式摄影等。相关术语包括：产品摄影（product photography）、产品图片（product image）、摄影棚摄影（studio photography）、电商摄影（e-commerce photography）、产品特写（hero shot）、产品模型（product mockup）等。"
allowed-tools: Bash(infsh *)
---
# 产品摄影

通过 [inference.sh](https://inference.sh) 命令行工具，利用人工智能生成专业的产品图片。

## 快速入门

```bash
curl -fsSL https://cli.inference.sh | sh && infsh login

# Clean studio packshot
infsh app run bytedance/seedream-4-5 --input '{
  "prompt": "professional product photography, single premium wireless headphone on clean white background, soft studio lighting with subtle shadow, commercial e-commerce style, sharp focus, 4K quality",
  "size": "2K"
}'
```

> **安装说明：** [安装脚本](https://cli.inference.sh) 仅会检测您的操作系统和架构，然后从 `dist.inference.sh` 下载相应的二进制文件，并验证其 SHA-256 校验和。无需特殊权限或后台进程。也可以选择 [手动安装与验证](https://dist.inference.sh/cli/checksums.txt)。

## 图片类型

### 1. 主图（Hero Shot）

这是客户首先看到的图片。图片应简洁、焦点清晰，能够体现产品的吸引力。

```bash
infsh app run bytedance/seedream-4-5 --input '{
  "prompt": "hero product shot, premium smartwatch floating at slight angle, clean gradient background transitioning from white to light grey, dramatic rim lighting, subtle reflection below, commercial photography, magazine quality, sharp details",
  "size": "2K"
}'
```

| 规则 | 原因 |
|------|-----|
| 产品占据画面 80% | 最大化视觉冲击力 |
| 采用 15-30 度的倾斜角度 | 使画面更具立体感（避免平视角度） |
| 使用一个主光源 + 背景光 | 创造深度感，同时避免强烈的阴影 |
| 背景颜色为中性色或品牌专属颜色 | 使焦点始终放在产品上 |

### 2. 电商用白背景图片（Packshot）

亚马逊、Shopify 和大多数电商平台要求使用纯白色背景。

```bash
# Pure white background packshot
infsh app run bytedance/seedream-4-5 --input '{
  "prompt": "product packshot, leather wallet standing upright at slight angle on pure white background #FFFFFF, soft even studio lighting, no shadows, e-commerce product photography, Amazon listing style, clean sharp focus",
  "size": "2K"
}'
```

**亚马逊的要求：**
- 背景颜色为纯白色（RGB 255, 255, 255）
- 产品占据画面 85% 以上 |
- 不允许出现配饰、文字、标志或水印 |
- 最长边长度至少为 1000 像素（建议使用 1600 像素以上以适应缩放）
- 图片格式为 JPEG 或 PNG，颜色模式为 sRGB

### 3. 生活场景图（Lifestyle Shot）

展示产品在实际使用中的样子或其所处的环境。

```bash
infsh app run bytedance/seedream-4-5 --input '{
  "prompt": "lifestyle product photography, premium coffee mug on rustic wooden table beside an open book and reading glasses, morning sunlight streaming through window, cozy home atmosphere, shallow depth of field, warm tones, editorial style",
  "size": "2K"
}'
```

### 4. 比例图（Scale Shot）

通过将产品与常见物品或人手进行对比，展示产品的实际大小。

```bash
infsh app run falai/flux-dev-lora --input '{
  "prompt": "product scale photography, compact portable speaker held in one hand, person showing how small and portable it is, clean blurred background, natural lighting, lifestyle tech photography",
  "width": 1024,
  "height": 1024
}'
```

### 5. 细节/特写图（Detail / Close-Up Shot）

突出产品的纹理、材质质量或特定特征。

```bash
infsh app run bytedance/seedream-4-5 --input '{
  "prompt": "extreme close-up product detail, premium leather bag stitching and grain texture, macro photography, shallow depth of field, soft directional lighting highlighting texture, luxury product photography, editorial quality",
  "size": "2K"
}'
```

### 6. 组合图（Group / Collection Shot）

展示多个产品或不同款式的产品。

```bash
infsh app run bytedance/seedream-4-5 --input '{
  "prompt": "product collection flat lay photography, three skincare bottles arranged in triangular composition on marble surface, minimal props, soft overhead lighting, beauty product photography, editorial style, coordinated brand aesthetic",
  "size": "2K"
}'
```

## 摄影角度

| 角度 | 适合的场景 | 相关提示词 |
|-------|----------|---------------|
| **平视角度** | 大多数产品 | “平视角度” |
| **略微仰角（30°）** | 平铺展示的产品（如食品、化妆品） | “45 度角度” |
| **俯视角度（90°）** | 平铺展示的产品 | “俯视角度” |
| **低角度** | 使产品看起来更高端/精致 | “低角度” |
| **三分之二视角** | 适用性最强，能展现产品深度 | “三分之二视角” |

## 照明设置

| 照明方式 | 效果 | 相关提示词 |
|-------|------|----------------|
| **柔光箱（散射光）** | 光线均匀，阴影较少 | “柔和的摄影棚灯光” |
| **边缘照明** | 产品轮廓清晰 | “边缘照明” |
| **自然光** | 温暖、真实感强 | “自然光线” |
| **定向强光** | 明显的阴影，适合编辑类图片 | “定向强光” |
| **均匀照明** | 适合电商图片，无阴影 | “均匀照明” |

## 阴影类型

| 阴影类型 | 效果 | 适用场景 |
|--------|--------|-------------|
| **无阴影** | 画面干净、清晰 | 适合亚马逊/电商场景 |
| **接触阴影** | 产品与表面接触处产生的微小阴影 | 使画面更真实 |
| **投影阴影** | 产品下方的柔和阴影 | 增加深度感，显得专业 |
| **戏剧性阴影** | 长而明显的阴影 | 适合编辑类或高端产品 |
| **反射光** | 表面有反射效果 | 适合科技产品或高端产品 |

## 背景选择指南

| 背景类型 | 适合的场景 | 相关提示词 |
|------------|----------|----------------|
| 纯白色 (#FFFFFF) | 电商、大多数电商平台 | “纯白色背景” |
| 浅灰色渐变 | 适合主图或高端产品 | “白色到灰色的渐变背景” |
| 大理石/石材 | 适合奢侈品或珠宝类产品 | “大理石表面” |
| 木质/乡村风格 | 适合手工艺品、食品或自然产品 | “乡村风格的木质桌面” |
| 品牌专属颜色 | 保持品牌一致性 | “背景颜色 [十六进制代码]” |
| 生活场景背景 | 适合展示产品使用场景 | “厨房台面”、“书桌”、“浴室架子” |

## 构图规则

| 规则 | 应用场景 |
|------|------------|
| **三分法则** | 在生活场景图中，将产品放置在画面的三分线交点处 |
| **居中展示** | 电商或产品包装图——产品居中展示 |
| **留白空间** | 如用于营销宣传，可留出文字叠加的位置 |
| **引导线条** | 利用桌面边缘或阴影引导观众的视线到产品 |
| **产品数量** | 3 或 5 个产品组合看起来更美观 |
| **三角形构图** | 将 3 个产品排列成三角形以保持平衡 |

## 电商产品图片集

一个完整的产品列表需要按照以下顺序准备 7-9 张图片：

| 位置 | 图片类型 | 用途 |
|----------|-----------|---------|
| 1 | **主图/电商用白背景图片** | 主要展示图片 |
| 2 | **生活场景图** | 展示产品实际使用场景 |
| 3 | **产品特点图** | 突出产品的主要特点 |
| 4 | **比例参考图** | 通过手或已知物品展示产品大小 |
| 5 | **细节特写图** | 展示材质质量或工艺 |
| 6 | **其他角度图** | 产品的背面或侧面视图 |
| 7 | **信息图** | 显示产品尺寸、规格及附带配件 |
| 8 | **包装图** | 展示开箱过程 |
| 9 | **用户评价图** | 显示用户评价或与产品的搭配场景 |

```bash
# Generate a complete e-commerce set
# 1. Hero packshot
infsh app run bytedance/seedream-4-5 --input '{
  "prompt": "product packshot, premium bluetooth speaker on pure white background, slight angle, soft studio lighting, subtle contact shadow, e-commerce photography, sharp, 4K",
  "size": "2K"
}' --no-wait

# 2. Lifestyle
infsh app run bytedance/seedream-4-5 --input '{
  "prompt": "lifestyle product photography, bluetooth speaker on poolside table, summer setting, sunglasses and drink nearby, warm natural light, vacation vibes, editorial style",
  "size": "2K"
}' --no-wait

# 3. Detail
infsh app run bytedance/seedream-4-5 --input '{
  "prompt": "extreme close-up of speaker grille texture and premium materials, macro product photography, soft lighting, showing build quality, sharp detail",
  "size": "2K"
}' --no-wait

# 4. Scale
infsh app run falai/flux-dev-lora --input '{
  "prompt": "person holding compact bluetooth speaker in one hand, showing portable size, clean blurred background, natural light, lifestyle tech photography",
  "width": 1024,
  "height": 1024
}' --no-wait
```

## 产品类别

### 食品与饮料

```
Key: overhead angles, natural light, visible texture, steam/freshness cues
Prompt add: "food photography, appetizing, fresh, natural daylight, shallow depth of field"
Avoid: artificial-looking colors, perfectly symmetrical plating (looks fake)
```

### 珠宝与配饰

```
Key: macro detail, reflective surfaces, black or gradient backgrounds
Prompt add: "jewelry photography, macro, sparkle, reflective surface, luxury"
Avoid: flat lighting (kills sparkle), busy backgrounds
```

### 电子产品与科技产品

```
Key: clean lines, dark or gradient backgrounds, rim lighting
Prompt add: "tech product photography, sleek, modern, rim lighting, premium"
Avoid: warm/rustic backgrounds (wrong aesthetic)
```

### 化妆品与美容产品

```
Key: flat lay or slight angle, marble/clean surfaces, soft pastels
Prompt add: "beauty product photography, clean, minimal, soft light, editorial"
Avoid: harsh shadows, dark moody lighting (unless luxury/niche)
```

### 服装与时尚产品

```
Key: on model or flat lay, lifestyle context, brand mood
Prompt add: "fashion photography, editorial, styled, natural pose"
Avoid: pure white background for lifestyle (save for e-commerce only)
```

## 图片编辑流程

```bash
# Generate base product image
infsh app run bytedance/seedream-4-5 --input '{
  "prompt": "premium headphones on white background, studio product photography",
  "size": "2K"
}'

# Edit: change background to lifestyle
infsh app run bytedance/seededit-3-0-i2i --input '{
  "prompt": "change the background to a modern minimalist desk setup with warm afternoon light, keep the headphones exactly the same",
  "image": "headphones-white.png"
}'

# Upscale for print
infsh app run falai/topaz-image-upscaler --input '{
  "image": "headphones-lifestyle.png"
}'
```

## 常见错误

| 错误 | 问题 | 解决方法 |
|---------|---------|-----|
| 背景过于复杂 | 产品会被背景掩盖 | 使用简洁、干净的背景，确保产品是焦点 |
| 平视角度拍摄 | 画面显得呆板 | 采用 15-30 度的倾斜角度 |
| 照明与产品类别不匹配 | 例如将科技产品放在乡村风格的背景下，或食品在冷光下拍摄 | 根据产品类别选择合适的照明方式 |
| 配饰过多 | 会分散观众对产品的注意力 | 生活场景图中最多使用 2-3 个辅助配饰 |
| 图片风格不一致 | 会影响专业感 | 使用相同的照明方式和背景风格 |
| 无比例参考 | 客户无法判断产品大小 | 至少添加一张产品与手或已知物品搭配的图片 |
| 图像分辨率过低 | 缩放效果差，显得业余 | 图像分辨率应至少为 2K，必要时进行高清处理 |
| 所有元素都居中 | 画面显得呆板 | 生活场景图使用三分法则，包装图可居中展示 |

## 相关技能

```bash
npx skills add inference-sh/skills@ai-image-generation
npx skills add inference-sh/skills@flux-image
npx skills add inference-sh/skills@prompt-engineering
```

浏览所有可用工具：`infsh app list`