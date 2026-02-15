---
name: multishot-ugc
description: |
  Generate 10 perspective/angle variations from a single image for multi-shot UGC videos.
  
  ✅ USE WHEN:
  - Have a hero image and need camera angle variations
  - Creating multi-scene UGC videos (need different shots)
  - Want close-ups, wide shots, side angles from one source
  - Building a video with scene changes
  
  ❌ DON'T USE WHEN:
  - Don't have a hero image yet → use morpheus-fashion-design first
  - Need completely different scenes/locations → use Morpheus multiple times
  - Just need one image → skip this step
  - Want to edit images manually → use nano-banana-pro
  
  INPUT: Single image (person with product)
  OUTPUT: 10 PNG variations with different perspectives
  
  TYPICAL PIPELINE: Morpheus → multishot-ugc → select best 4 → veed-ugc each → Remotion edit
---

# 多视角UGC（Multishot-UGC）

使用ComfyDeploy的MULTISHOT-UGC工作流，可以生成一张图片的10种不同视角的变体。

## 概述

Multishot-UGC从一张图片生成10种不同的变体，这些变体展示了不同的视角、角度和构图。这些变体适用于VEED的口型同步工作流，用于创建具有多种镜头效果的动态UGC风格宣传视频。

## API详情

**端点：** `https://api.comfydeploy.com/api/run/deployment/queue`
**部署ID：** `9ccbb29a-d982-48cc-a465-bae916f2c7fd`

## 必需输入参数

| 输入参数 | 描述 | 默认值 |
|---------|-------------|---------|
| `input_image` | 源图片的URL或路径 | 必填 |
| `text` | 变体生成的描述 | "探索这个场景的不同视角" |
| `resolution` | 输出分辨率 | "2K" |
| `aspect_ratio` | 输出宽高比 | "9:16" |

## 使用方法

```bash
uv run ~/.clawdbot/skills/multishot-ugc/scripts/generate.py \
  --image "./person-with-product.png" \
  --output-dir "./multishot-output" \
  [--text "Custom exploration prompt"] \
  [--resolution 1K|2K|4K] \
  [--aspect-ratio 9:16|16:9|1:1|4:3|3:4]
```

### 使用URL调用：
```bash
uv run ~/.clawdbot/skills/multishot-ugc/scripts/generate.py \
  --image "https://example.com/image.png" \
  --output-dir "./variations"
```

## 输出结果

该工作流会生成10张PNG格式的图片（文件名格式为`1_00001_.png`至`10_00001_.png`）：

每张图片都展示了原始场景的不同视角或角度，同时保持了主体和构图的连贯性。

## 工作流集成

### 典型流程

1. 使用Morpheus/Ad-Ready生成主图片  
   ```bash
   uv run morpheus... --output hero.png
   ```

2. 生成10种不同角度的变体  
   ```bash
   uv run multishot-ugc... --image hero.png --output-dir ./shots
   ```

3. 从生成的变体中选择最适合VEED口型同步的版本  
   ```bash
   # Review shots, then generate videos for chosen ones
   uv run veed-ugc... --image ./shots/3_00001_.png --brief "..."
   ```

## 注意事项：

- 源图片应具有高质量（至少1K分辨率）  
- 最适合包含清晰主体或人物的图片  
- 生成10种变体大约需要2-3分钟  
- 除非另有指定，否则所有变体都将保持原始的宽高比