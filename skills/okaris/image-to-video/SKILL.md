---
name: image-to-video
description: "静态图像转视频转换指南：模型选择、动作提示及摄像机运动控制  
涵盖Wan 2.5 i2v、Seedance、Fabric、Grok Video等工具的使用场景及适用时机。  
适用场景：图像动画制作、从静态图片生成视频、为图片添加动态效果、产品动画展示等。  
相关功能包括：将图片转换为视频、实现图像动画效果、为静态图片添加动态效果、将照片转换为视频、为照片添加动画效果等。"
allowed-tools: Bash(infsh *)
---
# 将静态图片转换为视频

通过 [inference.sh](https://inference.sh) 命令行工具将静态图片转换为动画视频。

## 快速入门

```bash
curl -fsSL https://cli.inference.sh | sh && infsh login

# Generate a still image
infsh app run falai/flux-dev-lora --input '{
  "prompt": "serene mountain lake at sunset, snow-capped peaks reflected in still water, golden hour light, landscape photography",
  "width": 1248,
  "height": 832
}'

# Animate it
infsh app run falai/wan-2-5-i2v --input '{
  "prompt": "gentle ripples on the lake surface, clouds slowly drifting, warm light shifting, birds flying in the distance",
  "image": "path/to/lake-image.png"
}'
```

> **安装说明：** [安装脚本](https://cli.inference.sh) 仅会检测您的操作系统和架构，然后从 `dist.inference.sh` 下载相应的二进制文件，并验证其 SHA-256 校验和。无需特殊权限或后台进程。也可以手动进行安装和验证：[手动安装与验证](https://dist.inference.sh/cli/checksums.txt)。

## 模型选择

| 模型 | 应用 ID | 适用场景 | 动作风格 |
|-------|--------|----------|-------------|
| **Wan 2.5 i2v** | `falai/wan-2-5-i2v` | 真实感强的动作，自然流畅 | 光影效果细腻 |
| **Seedance 1.5 Pro** | `bytedance/seedance-1-5-pro` | 风格化、富有创意的动画效果 | 艺术感强 |
| **Seedance 1.0 Pro** | `bytedance/seedance-1-0-pro` | 通用型模型，画质优秀 | 平衡性较好 |
| **Fabric 1.0** | `falai/fabric-1-0` | 适用于模拟布料、液体等材质的动态效果 | 基于物理特性的动画 |
| **Grok Imagine Video** | `xai/grok-imagine-video` | 适用于文本引导的动画制作 | 用途广泛 |

### 各模型的适用场景

| 场景 | 最佳模型 | 选择理由 |
|----------|-----------|-----|
| 有水或云层的风景 | **Wan 2.5 i2v** | 更适合表现自然、真实的动作效果 |
| 需要展现细微表情的肖像 | **Wan 2.5 i2v** | 能够保持面部细节的真实性 |
| 需要模拟布料或织物的场景 | **Fabric 1.0** | 专门针对这类材质的物理特性设计 |
| 旗帜飘扬、窗帘摆动等场景 | **Fabric 1.0** | 适用于模拟布料动态 |
| 插画或艺术风格的图片 | **Seedance** | 与风格化的内容更匹配 |
| 需要为图片添加动态效果的场景 | **Seedance 1.5 Pro** | 通用性更强，效果较好 |
| 快速测试或迭代 | **Seedance 1.0 Lite** | 生成速度最快，支持 720p 视频 |

## 动作类型

### 相机运动

| 动作 | 提示关键词 | 效果 |
|----------|---------------|--------|
| 向前推/拉近 | “缓慢推进镜头”，“相机向内移动” | 增强亲密感或聚焦效果 |
| 向后拉/拉远 | “相机向后移动”，“缓慢缩放” | 展示更多背景信息 |
| 向左/向右平移 | “相机缓慢向右平移” | 用于扫描或跟随拍摄对象 |
| 上下倾斜 | “相机向上倾斜” | 用于展示高度信息 |
| 旋转拍摄 | “相机围绕拍摄对象旋转” | 用于三维空间展示 |
| 升高镜头 | “镜头向上移动” | 用于展示全景效果 |
| 静止不动 | （无相机移动提示） | 仅模拟主体动作 |

### 主体动作

| 动作类型 | 示例描述 |
|------|----------------|
| 自然元素 | “水面波纹”，“云朵飘动”，“树叶在风中沙沙作响” |
| 头发/衣物 | “头发在风中轻轻摆动”，“裙摆随风飘动” |
| 大气效果 | “雾气缓缓扩散”，“尘埃在光线中漂浮” |
| 角色动作 | “人物慢慢转向镜头”，“轻微的呼吸动作” |
| 机械装置 | “齿轮转动”，“钟表指针移动” |
| 流体物质 | “咖啡蒸汽升起”，“油漆滴落”，“水倾泻而下” |

## 提示语的使用技巧

### 重要原则：细腻的动作效果优于夸张的动作

AI 视频模型在处理动作时，细腻、自然的效果通常优于夸张的动作。过度使用夸张的动作会导致图像失真或出现瑕疵。

```
❌ "person running and jumping over obstacles while the camera spins"
✅ "person slowly walking forward, gentle breeze, camera follows alongside"

❌ "explosion with debris flying everywhere"
✅ "candle flame flickering gently, warm ambient light shifting"

❌ "fast zoom into the eyes with dramatic camera shake"
✅ "slow dolly forward toward the subject, subtle focus shift"
```

### 提示语的结构

```
[Camera movement] + [Subject motion] + [Atmospheric effects] + [Mood/pace]
```

### 按场景划分的示例

```bash
# Landscape animation
infsh app run falai/wan-2-5-i2v --input '{
  "prompt": "gentle camera pan right, water reflecting moving clouds, trees swaying slightly in breeze, warm golden light, peaceful and slow",
  "image": "landscape.png"
}'

# Portrait animation
infsh app run falai/wan-2-5-i2v --input '{
  "prompt": "subtle breathing motion, slight head turn, natural eye blink, hair moving gently, soft ambient lighting shifts",
  "image": "portrait.png"
}'

# Product shot animation
infsh app run bytedance/seedance-1-5-pro --input '{
  "prompt": "slow 360 degree orbit around the product, gentle spotlight movement, subtle reflections shifting, premium product showcase, smooth motion",
  "image": "product.png"
}'

# Fabric/cloth animation
infsh app run falai/fabric-1-0 --input '{
  "prompt": "fabric flowing and rippling in gentle wind, natural cloth physics, soft movement",
  "image": "fabric-scene.png"
}'

# Architectural visualization
infsh app run falai/wan-2-5-i2v --input '{
  "prompt": "slow dolly forward through the entrance, slight camera tilt upward, ambient light filtering through windows, dust particles in light beams",
  "image": "building-interior.png"
}'
```

## 视频时长建议

| 时长 | 视频质量 | 适用场景 |
|----------|---------|---------|
| 2-3 秒 | 最高质量 | 适用于 GIF 图片、循环背景动画、动态壁纸 |
| 4-5 秒 | 较高质量 | 适用于社交媒体发布、产品展示 |
| 6-8 秒 | 优质视频 | 适用于短片或过渡效果 |
| 10 秒以上 | 视频质量会下降 | 如需更长的视频，请合并多个短片 |

## 延长视频时长

对于较长的视频，可以生成多个短片并通过拼接的方式延长时长：

```bash
# Generate 3 clips from the same image with progressive motion
infsh app run falai/wan-2-5-i2v --input '{
  "prompt": "slow pan left, gentle water motion",
  "image": "scene.png"
}' --no-wait

infsh app run falai/wan-2-5-i2v --input '{
  "prompt": "continuing pan, clouds shifting, light changing",
  "image": "scene.png"
}' --no-wait

# Stitch together
infsh app run infsh/media-merger --input '{
  "media": ["clip1.mp4", "clip2.mp4"]
}'
```

## 完整的工作流程

### 静态图片到最终视频的转换流程

```bash
# 1. Generate source image (best quality)
infsh app run bytedance/seedream-4-5 --input '{
  "prompt": "cinematic landscape, misty mountains at dawn, lake in foreground, dramatic clouds, golden hour, 4K quality, professional photography",
  "size": "2K"
}'

# 2. Animate the image
infsh app run falai/wan-2-5-i2v --input '{
  "prompt": "gentle mist rolling through the valley, lake surface rippling, clouds slowly moving, birds in distance, warm light shifting",
  "image": "landscape.png"
}'

# 3. Upscale video if needed
infsh app run falai/topaz-video-upscaler --input '{
  "video": "animated-landscape.mp4"
}'

# 4. Add ambient audio
infsh app run infsh/hunyuanvideo-foley --input '{
  "video": "animated-landscape.mp4",
  "prompt": "gentle nature ambience, distant birds, soft wind, water lapping"
}'

# 5. Merge video with audio
infsh app run infsh/video-audio-merger --input '{
  "video": "upscaled-landscape.mp4",
  "audio": "ambient-audio.mp3"
}'
```

## 动态壁纸（Cinemagraph）效果

动态壁纸是指图片中只有一个元素在移动（例如，在其他部分静止的场景中，只有瀑布在流动）。实现方法如下：

1. 先生成包含动态元素的静态图片。
2. 仅对该元素进行动态效果的提示。
3. 保持视频时长在 2-4 秒以内，以确保动画能够无缝循环播放。

```bash
infsh app run falai/wan-2-5-i2v --input '{
  "prompt": "only the waterfall is moving, everything else remains perfectly still, water cascading smoothly, rest of scene frozen",
  "image": "waterfall-scene.png"
}'
```

## 常见错误及解决方法

| 错误 | 问题 | 解决方法 |
|---------|---------|-----|
| 请求的动作过于夸张 | 会导致图像失真或出现瑕疵 | 始终选择细腻、自然的动作效果 |
| 选择的模型不适合内容类型 | 会导致视频效果不佳 | 请参考上述模型选择指南 |
| 视频时长过长（超过 10 秒） | 视频质量会显著下降 | 请将视频时长控制在 3-5 秒以内，必要时通过拼接处理 |
| 未指定相机运动方式 | 会导致动作效果混乱或不自然 | 请务必指定相机的运动方式 |
| 动作方向相互冲突 | 会导致画面显得不自然 | 应确保所有动作方向一致 |
| 源图片分辨率较低 | 会导致视频质量降低 | 请使用高分辨率的源图片 |
| 视频中包含复杂的动作场景 | 部分模型可能无法处理 | 请保持动作简单、自然 |

## 相关技能

```bash
npx skills add inference-sh/skills@ai-video-generation
npx skills add inference-sh/skills@ai-image-generation
npx skills add inference-sh/skills@video-prompting-guide
npx skills add inference-sh/skills@prompt-engineering
```

浏览所有可用应用：`infsh app list`