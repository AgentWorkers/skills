---
name: product-photography
description: |
  AI product photography with studio lighting, lifestyle shots, and packshot conventions.
  Covers angles, backgrounds, shadow types, hero shots, and e-commerce image requirements.
  Use for: product photos, e-commerce images, Amazon listings, packshots, lifestyle photography.
  Triggers: product photography, product photo, packshot, e-commerce photography,
  product shot, product image, studio photography, lifestyle product, amazon product photo,
  product listing image, hero shot, product mockup, commercial photography
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

## 图片类型

### 1. 主图（Hero Shot）

这是顾客首先看到的图片。图片应该清晰、焦点明确，能够激发消费者的购买欲望。

```bash
infsh app run bytedance/seedream-4-5 --input '{
  "prompt": "hero product shot, premium smartwatch floating at slight angle, clean gradient background transitioning from white to light grey, dramatic rim lighting, subtle reflection below, commercial photography, magazine quality, sharp details",
  "size": "2K"
}'
```

| 规则 | 原因 |
|------|-----|
| 产品占据画面的80% | 最大化视觉冲击力 |
| 采用15-30度的角度 | 使画面更具立体感，避免正面平视的效果 |
| 使用一个主光源并添加背景光 | 创造深度感，同时避免强烈的阴影 |
| 背景为中性色或品牌指定颜色 | 使焦点始终放在产品上 |

### 2. 包装图（电商用白色背景）

亚马逊、Shopify等大多数电商平台要求使用纯白色背景。

```bash
# Pure white background packshot
infsh app run bytedance/seedream-4-5 --input '{
  "prompt": "product packshot, leather wallet standing upright at slight angle on pure white background #FFFFFF, soft even studio lighting, no shadows, e-commerce product photography, Amazon listing style, clean sharp focus",
  "size": "2K"
}'
```

**亚马逊要求：**
- 背景为纯白色（RGB 255, 255, 255）
- 产品占据画面的85%以上 |
- 不允许出现道具、文字、标志或水印 |
- 最长边长度至少为1000像素（建议使用1600像素以上以适应缩放）
- 图片格式为JPEG或PNG，颜色模式为sRGB

### 3. 使用场景图（Lifestyle Shot）

展示产品在实际使用中的样子或其所处的环境。

```bash
infsh app run bytedance/seedream-4-5 --input '{
  "prompt": "lifestyle product photography, premium coffee mug on rustic wooden table beside an open book and reading glasses, morning sunlight streaming through window, cozy home atmosphere, shallow depth of field, warm tones, editorial style",
  "size": "2K"
}'
```

### 4. 比例图（Scale Shot）

通过将产品与熟悉的物体或人手进行对比，展示产品的实际大小。

```bash
infsh app run falai/flux-dev-lora --input '{
  "prompt": "product scale photography, compact portable speaker held in one hand, person showing how small and portable it is, clean blurred background, natural lighting, lifestyle tech photography",
  "width": 1024,
  "height": 1024
}'
```

### 5. 详细图/特写图（Detail / Close-Up Shot）

突出产品的纹理、材质质量或特定功能。

```bash
infsh app run bytedance/seedream-4-5 --input '{
  "prompt": "extreme close-up product detail, premium leather bag stitching and grain texture, macro photography, shallow depth of field, soft directional lighting highlighting texture, luxury product photography, editorial quality",
  "size": "2K"
}'
```

### 6. 组合图/系列图（Group / Collection Shot）

展示多个产品或不同款式。

```bash
infsh app run bytedance/seedream-4-5 --input '{
  "prompt": "product collection flat lay photography, three skincare bottles arranged in triangular composition on marble surface, minimal props, soft overhead lighting, beauty product photography, editorial style, coordinated brand aesthetic",
  "size": "2K"
}'
```

## 相机角度

| 角度 | 适用场景 | 关键提示词 |
|-------|----------|---------------|
| **平视角度** | 适用于大多数产品 | “平视角度” |
| **稍高于产品（30°）** | 适用于平面摆放的产品，如食品、化妆品 | “俯视角度” |
| **鸟瞰角度（90°）** | 适用于平面摆放的构图 | “俯视角度” |
| **低角度** | 使产品看起来更显高端/专业 | “低角度” |
| **3/4角度** | 适用场景广泛，能展现产品深度 | “三分之二视角” |

## 照明设置

| 照明方式 | 效果 | 关键提示词 |
|-------|------|----------------|
| **柔光箱（漫射光）** | 光线均匀，阴影较少 | “柔和的摄影棚灯光” |
| **边缘光** | 产生明显的轮廓光 | “边缘光” |
| **自然光线（窗户光）** | 温暖、真实，适合生活场景 | “自然光线” |
| **定向强光** | 形成强烈的阴影，适合编辑类图片 | “定向强光” |
| **均匀照明** | 适用于电商图片，无阴影 | “均匀照明” |

## 阴影类型

| 阴影类型 | 效果 | 适用场景 |
|--------|--------|-------------|
| **无阴影** | 画面干净、清晰 | 适用于亚马逊/电商图片 |
| **接触阴影** | 产品与表面接触处产生的微小阴影 | 使画面更立体 |
| **投影阴影** | 产品下方的柔和阴影 | 增加深度感，显得专业 |
| **戏剧性阴影** | 长而明显的阴影 | 适合编辑类或高端风格的图片 |
| **反射阴影** | 表面反射的光线 | 适用于科技产品或高端产品 |

## 背景选择指南

| 背景类型 | 适用场景 | 关键提示词 |
|------------|----------|----------------|
| 纯白色（#FFFFFF） | 适用于电商和大多数电商平台 | “纯白色背景” |
| 浅灰色渐变背景 | 适用于主图或高端产品 | “白色到灰色的渐变背景” |
| 大理石/石材背景 | 适用于奢侈品或珠宝类产品 | “大理石表面” |
| 木质/乡村风格背景 | 适用于手工艺品、食品或自然产品 | “乡村风格的木质背景” |
| 有颜色的背景（品牌专属） | 保持品牌一致性 | “品牌指定颜色” |
| 生活场景背景 | 适用于展示产品使用场景的图片 | “厨房台面”、“书桌”、“浴室架子” |

## 构图规则

| 规则 | 应用场景 |
|------|------------|
| **三分法则** | 在使用场景图中，将产品放置在画面的三分线交点处 |
| **产品居中** | 适用于电商或包装图 | 将产品放在画面正中央 |
| **留出空白区域** | 如果需要添加文字说明，可以留出空间 |
| **引导视线** | 利用桌面边缘或阴影引导观众的视线到产品上 |
| **产品数量** | 3个或5个产品组成的组合看起来更美观 |
| **三角形构图** | 将3个产品排列成三角形以保持平衡 |

## 电商产品图片集

一个完整的产品列表需要按照以下顺序准备7-9张图片：

| 位置 | 图片类型 | 用途 |
|----------|-----------|---------|
| 1 | **主图/包装图** | 主要展示图片，使用白色背景 |
| 2 | **使用场景图** | 展示产品实际使用情况 |
| 3 | **功能特写** | 突出产品的主要功能 |
| 4 | **比例参考图** | 通过人手或其他已知物体展示产品大小 |
| 5 | **细节特写** | 展示产品的材质和质量 |
| 6 | **其他角度图** | 产品的背面或侧面视图 |
| 7 | **信息图** | 显示产品的尺寸、规格及附带配件 |
| 8 | **包装图** | 展示开箱过程 |
| 9 | **用户评价或使用场景图** | 包含用户评价或与产品相关的使用场景 |

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
| 背景过于复杂 | 产品会被掩盖 | 选择简洁、干净的背景，让产品成为焦点 |
| 采用正面平视角度 | 画面显得呆板 | 采用15-30度的角度增加立体感 |
| 照明与产品类别不匹配 | 例如在乡村风格的背景下使用科技产品，或在冷光下拍摄食品 | 根据产品类别选择合适的照明方式 |
| 道具过多 | 会分散观众的注意力 | 在使用场景图中最多使用2-3个辅助道具 |
| 图片风格不一致 | 会影响专业感 | 保持统一的照明方式和背景风格 |
| 没有尺寸参考 | 顾客无法判断产品大小 | 至少添加一张包含人手或其他已知物体的图片 |
| 图像分辨率过低 | 无法放大，看起来不专业 | 图像分辨率应至少为2K以上，必要时进行高清处理 |
| 所有元素都居中 | 画面显得呆板 | 在使用场景图中遵循三分法则，包装图中可以居中 |

## 相关技能

```bash
npx skills add inferencesh/skills@ai-image-generation
npx skills add inferencesh/skills@flux-image
npx skills add inferencesh/skills@prompt-engineering
```

浏览所有可用工具：`infsh app list`