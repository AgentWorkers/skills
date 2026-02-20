---
name: wavespeed
description: "使用 WaveSpeed AI 的 700 多个模型库来生成和编辑图片及视频。适用于以下场景：  
- 根据文本提示生成图片（如 FLUX、Seedream、Qwen）；  
- 编辑或修图（例如 nano-banana-pro/edit 可在更换服装/背景的同时保留人物面部特征）；  
- 从图片或文本生成视频（Kling、Veo、Sora、Wan、Hailuo）；  
- 将视频升级至 4K 分辨率。  
可使用的功能包括：  
- 生成图片；  
- 编辑图片；  
- 更换图片背景；  
- 为图片更换服装；  
- 从图片制作视频；  
- 为图片添加动画效果；  
- 将视频升级至 4K 分辨率；  
- 使用 WaveSpeed AI 的其他高级功能（如 nano-banana-pro）。"
---
# WaveSpeed AI

通过一个API，您可以访问700多个AI模型（来自Google、OpenAI、ByteDance、Kling和Luma）。图片处理耗时不到2秒，视频处理耗时不到2分钟。

## 设置

```bash
export WAVESPEED_API_KEY="your_key_here"
```

API密钥存储在`TOOLS.md`或`.env`文件中。技能脚本位于`skills/wavespeed/scripts/wavespeed.js`。

## 使用方法

```bash
# Image generation
node wavespeed.js generate --model flux --prompt "sunset over mountains" --output out.png
node wavespeed.js generate --model seedream --prompt "..." --size 1024x1024

# Image editing (face/portrait-safe — preserves identity)
node wavespeed.js edit --model nbp --prompt "change bathrobe to black hoodie, dark background" \
  --image https://example.com/photo.jpg --output result.png

# Video from image
node wavespeed.js video --model wan-i2v --prompt "slow cinematic zoom" \
  --image https://example.com/frame.jpg --output clip.mp4

# List all aliases
node wavespeed.js models

# Check task status
node wavespeed.js status --id task_abc123
```

## 主要模型（快速参考）

| 任务 | 别名 | 适用场景 |
|------|-------|---------|
| 修图（保留面部特征） | `nbp` | 人像修图、更换服装或背景 |
| 快速图像生成 | `flux-schnell` | 草图制作、快速测试 |
| 最高质量图像 | `flux-pro` / `seedream` | 最终输出文件 |
| 图片转视频 | `wan-i2v` | 快速且经济实惠 |
| 高品质视频 | `kling` / `veo` | 电影级画质 |
| 文本转视频 | `sora` / `veo` | 故事视频 |

完整的模型列表（包含模型ID、参数和价格信息）请参见`references/models.md`。

## 重要说明

- **图像编辑**（`nbp`、`nb-edit`）：必须以`images: [url]`数组的形式传递图片文件——这是必需的。
- **面部特征保留**：`google/nano-banana-pro/edit`是用于在编辑图片时保留人物面部特征的最佳模型。
- 输出文件默认保存在当前目录；使用`--output`参数指定保存路径。
- 视频处理可能需要2-5分钟；脚本会自动显示处理进度。
- 如果需要处理多张图片（多参考编辑），请使用`--images url1,url2`参数。