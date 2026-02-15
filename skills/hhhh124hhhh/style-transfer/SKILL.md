---
name: style-transfer
description: 通过 OpenAI Images API 实现专业的艺术风格转换。可以将图像转换为特定的艺术风格、时代或视觉效果。适用于用户需要将现有图像转换为不同的艺术风格、应用著名的艺术流派，或根据特定的风格参数修改视觉内容的情况（例如：“将这张照片处理成油画风格”、“应用赛博朋克美学”、“将其转换为复古摄影风格”）。
---

# Style Transfer Pro

使用 OpenAI Images API 和精心设计的风格提示，对图像进行艺术风格转换。

## 设置

- 需要的环境变量：`OPENAI_API_KEY`
- 需要的源图像 URL（公共 URL 或 Base64 数据 URI）

## 快速入门

将图像转换为油画风格：

```bash
python3 ~/Projects/agent-scripts/skills/style-transfer/scripts/transfer.py \
  --source "https://example.com/photo.jpg" \
  --style "oil painting on linen, impressionist brushwork, rich texture, van gogh style"
```

同时将图像转换为多种风格：

```bash
python3 ~/Projects/agent-scripts/skills/style-transfer/scripts/transfer.py \
  --source "https://example.com/photo.jpg" \
  --style "oil painting" \
  --style "watercolor illustration" \
  --style "cyberpunk neon" \
  --style "vintage sepia photograph"
```

## 风格库

使用这些预定义的风格名称（或提供自定义提示）：

### 艺术流派
- `impressionist-oil` - 具有明显笔触的印象派油画
- `watercolor-dream` - 带有墨线勾勒的柔和水彩画
- `digital-art` - 细节清晰的现代数字艺术
- `comic-book` - 明显的漫画书插画风格
- `anime-studio` - 动画/漫画工作室风格
- `pixel-art` - 复古像素艺术风格
- `vector-flat` - 简洁的平面矢量插画
- `surreal-abstract` - 超现实主义抽象艺术

### 摄影风格
- `vintage-sepia` - 复古的棕褐色摄影风格
- `polaroid` - 带有褪色色调的即时宝丽来效果
- `film-noir` - 黑白电影风格的暗色调
- `candid-snapshot` - 真实的快照风格
- `studio-portrait` - 专业的摄影工作室风格
- `vogue-editorial` - 时尚杂志插画风格
- `golden-hour` - 金光时刻的温暖光线效果
- `neon-noir` - 未来派的霓虹暗黑风格

### 历史风格
- `renaissance-portrait` - 古典文艺复兴时期的油画
- `baroque-drama` - 戏剧性的巴洛克明暗对比
- `art-deco-elegance` - 艺术装饰风格的几何美感
- `mid-century-modern` - 中世纪现代风格的插画
- `victorian-etching` - 维多利亚时代的蚀刻艺术风格
- `steampunk-gear` - 史前蒸汽朋克机械风格
- `dystopian-grunge` - 反乌托邦的垃圾摇滚风格
- `psychedelic-60s` - 20 世纪 60 年代的迷幻艺术风格

## 自定义风格提示

为了实现更精细的控制，请提供完整的风格提示：

```bash
python3 ~/Projects/agent-scripts/skills/style-transfer/scripts/transfer.py \
  --source "https://example.com/photo.jpg" \
  --prompt "watercolor painting, soft brushstrokes, pastel color palette, hand-painted illustration style, minimal detail, elegant and dreamy"
```

风格提示结构：
1. 介质：`oil painting`（油画）、`watercolor`（水彩）、`digital-art`（数字艺术）、`photography`（摄影）
2. 技法：`impressionist`（印象派）、`glazing`（透明涂层）、`crosshatching`（交叉排线）、`flat design`（平面设计）
3. 光线：`softbox`（柔光箱）、`golden-hour`（金光时刻）、`dramatic chiaroscuro`（戏剧性的明暗对比）、`diffuse`（柔和光线）
4. 颜色：`pastel`（淡色调）、`muted`（柔和色调）、`vibrant`（鲜艳色彩）、`muted earth tones`（柔和的土色调）
5. 质量：`ultra-detailed`（超高细节）、`minimalist`（极简主义）、`sketch`（草图）、`finished artwork`（完成的作品）

## 参数

- `--source` - 源图像 URL（必需）
- `--style` - 预定义的风格名称（可重复使用）
- `--prompt` - 完整的自定义风格提示（会覆盖 `--style` 的设置）
- `--out-dir` - 输出目录（默认：`~/Projects/tmp/style-transfer-*`）
- `--size` - 图像尺寸：1024x1024、1792x1024、1024x1792（默认：1024x1024）
- `--quality` - 高质量/标准质量（默认：高质量）
- `--model` - OpenAI 图像模型（默认：`gpt-image-1.5`）
- `--api-key` - OpenAI API 密钥（或使用环境变量 `OPENAI_API_KEY`）

## 输出

- `*.png` - 转换后的图像文件
- `prompts.json` - 使用的风格提示
- `index.html` - 用于比较各种风格的缩略图画廊