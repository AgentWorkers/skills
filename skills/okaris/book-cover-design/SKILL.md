---
name: book-cover-design
description: |
  Book cover design with genre-specific conventions, typography rules, and AI image generation.
  Covers fiction and non-fiction genres, sizing, thumbnail testing, and iteration workflows.
  Use for: self-publishing, ebook covers, print covers, audiobook covers, cover mockups.
  Triggers: book cover, cover design, ebook cover, book art, novel cover, self publishing cover,
  kindle cover, audiobook cover, book jacket, cover illustration, fiction cover, nonfiction cover
allowed-tools: Bash(infsh *)
---

# 书籍封面设计

通过 [inference.sh](https://inference.sh) 命令行工具，利用人工智能图像生成技术来设计符合书籍类型的封面。

## 快速入门

```bash
curl -fsSL https://cli.inference.sh | sh && infsh login

# Generate a thriller cover concept
infsh app run falai/flux-dev-lora --input '{
  "prompt": "dark moody book cover art, lone figure standing at end of a rain-soaked alley, dramatic chiaroscuro lighting, noir atmosphere, cinematic, high contrast shadows",
  "width": 832,
  "height": 1248
}'
```

## 类型规范

读者往往根据封面来评判一本书的质量。因此，封面设计与书籍类型的高度契合至关重要——例如，浪漫小说的读者会因为封面看起来像科幻小说而直接放弃阅读，无论内容如何。

### 小说类型

| 类型 | 色彩搭配 | 图像元素 | 字体风格 | 氛围 |
|-------|---------|---------|------------|------|
| **惊悚/悬疑** | 深色调（黑色、海军蓝、血红色） | 独自的人物、城市场景、阴影 | 粗体无衬线字体、全大写 | 紧张、阴森 |
| **浪漫** | 温暖色调（粉色、红色、金色、淡紫色） | 情侣、花朵、风景背景 | 脚本体/花体字体、优雅的衬线字体 | 浪漫、梦幻 |
| **科幻** | 冷色调（蓝色、青绿色、紫色、银色） | 太空、科技元素、几何形状 | 简洁的无衬线字体、未来感十足 | 宏大、科技感强 |
| **奇幻** | 鲜艳的色彩（翡翠绿、深红色、金色） | 剑、魔法、风景、奇幻生物 | 装饰性衬线字体 | 壮丽、充满魔法感 |
| **文学小说** | 色调柔和、风格高雅 | 抽象的图案、简约的设计 | 优雅的衬线字体、低调的风格 | 思考性强、艺术感十足 |
| **恐怖** | 高对比度的暗色调 | 人脸、阴影、孤立感、腐朽元素 | 粗糙的字体、强烈的视觉冲击 | 令人恐惧、不安 |
| **历史小说** | 淡色调、符合时代背景 | 当代服装、建筑、文物元素 | 古典衬线字体 | 怀旧、真实感强 |

### 非小说类书籍

| 类别 | 风格 | 图像元素 | 字体风格 |
|----------|-------|---------|------------|
| **商业/自助类** | 简洁、字体粗体、使用2-3种颜色 | 最少使用图像，图标可选 | 大号粗体无衬线字体作为标题 |
| **回忆录** | 个人化风格、温暖色调 | 作者照片或具有氛围感的场景图片 | 混合使用衬线字体和无衬线字体 |
| **科学/学术类** | 专业风格、结构清晰 | 图表、抽象视觉元素 | 简洁的衬线字体、条理分明的布局 |
| **食谱** | 食物图片吸引人、色彩鲜艳 | 温暖、友好的字体风格 |
| **旅行类** | 鲜艳的色彩、充满正能量 | 旅行目的地照片 | 适合冒险题材的字体 |

## 封面尺寸

### 印刷版（裁剪后的尺寸）

| 格式 | 尺寸 | 适用类型 |
|--------|-----------|------------|
| 大众市场平装书 | 4.25 x 6.87英寸 | 大多数小说类书籍 |
| 专业平装书 | 5.5 x 8.5英寸 | 大多数小说类和非小说类书籍 |
| 标准尺寸 | 6 x 9英寸 | 非小说类书籍、教科书 |
| 大开本 | 7 x 10英寸 | 适合咖啡桌阅读或艺术类书籍 |

### 数字版

| 平台 | 封面尺寸 | 宽高比 |
|----------|-----------|--------------|
| Amazon Kindle | 2560 x 1600 像素（最小要求 1000 x 625 像素） | 1.6:1 |
| Apple Books | 最小 1400 x 1873 像素 | 约 3:4 |
| 通用电子书 | 2500 x 3750 像素 | 2:3 |

## 封面脊部宽度

**大致计算方法：** **页数 / 400 = 封面脊部宽度（单位：英寸）**（具体数值因纸张材质而异）：
- 200页 ≈ 0.5英寸的脊部宽度
- 400页 ≈ 1.0英寸的脊部宽度

## 布局区域

```
┌─────────────────────────┐
│     TITLE ZONE          │ ← Top 1/3: Title must be readable here
│     (largest text)      │    This is what shows in thumbnails
│                         │
│                         │
│     MAIN IMAGE          │ ← Middle: Core visual/illustration
│     ZONE                │    The emotional hook
│                         │
│                         │
│     SUBTITLE /          │ ← Bottom area: Author name, subtitle
│     AUTHOR ZONE         │    Smaller text, less critical at thumbnail
└─────────────────────────┘
```

## 缩略图测试

在 Amazon 上，封面将以 80x120px 的尺寸展示；在搜索结果中以 60x90px 的尺寸显示；在移动设备上以约 40x60px 的尺寸显示。

**在缩略图尺寸下，读者需要能够识别：**
1. 书籍类型（通过色彩和构图判断）
2. 书名（如果足够大）
3. 书籍的氛围（通过图像元素判断）

**测试方法：** 将封面缩小到 80px 宽度。如果无法看清书名或判断不出类型，请重新设计封面。

## 按类型指导设计

### 惊悚小说
```bash
infsh app run falai/flux-dev-lora --input '{
  "prompt": "dark cinematic book cover scene, silhouette of a person standing before a foggy bridge at night, single streetlamp casting long shadows, noir atmosphere, high contrast, desaturated blue tint, dramatic tension",
  "width": 832,
  "height": 1248
}'
```

### 浪漫小说
```bash
infsh app run bytedance/seedream-4-5 --input '{
  "prompt": "romantic soft-focus scene, couple silhouetted against golden sunset on a beach, warm pink and gold tones, bokeh lights, dreamy atmosphere, soft pastel sky, intimate mood",
  "size": "2K"
}'
```

### 科幻小说
```bash
infsh app run falai/flux-dev-lora --input '{
  "prompt": "science fiction book cover art, massive space station orbiting a ringed planet, deep blue and teal color palette, stars and nebula background, hard sci-fi aesthetic, cinematic scale, clean geometric architecture",
  "width": 832,
  "height": 1248
}'
```

### 奇幻小说
```bash
infsh app run xai/grok-imagine-image-pro --input '{
  "prompt": "epic fantasy book cover illustration, ancient stone castle on a cliff overlooking a misty valley, magical aurora in the sky, rich emerald and gold colors, detailed environment, sense of wonder and adventure",
  "aspect_ratio": "2:3"
}'
```

### 非小说类/商业类书籍
```bash
infsh app run falai/flux-dev-lora --input '{
  "prompt": "minimal abstract book cover background, clean gradient from deep navy to white, subtle geometric pattern, professional and modern, negative space, corporate aesthetic",
  "width": 832,
  "height": 1248
}'
```

## 字体规则

**人工智能无法可靠地渲染文本。** 先使用人工智能生成封面图像/背景，再在设计工具中添加文字。

### 标题层次结构
1. **书名** — 最大、最显眼的位置，位于封面顶部1/3处
2. **副标题** — 较小，位于书名下方或底部
3. **作者姓名** — 位于封面底部，字体大小根据作者的知名度而定

### 不同类型的字体搭配
- **惊悚小说**：粗体无衬线字体作为书名，作者姓名使用简洁的无衬线字体
- **浪漫小说**：脚本体/花体字体作为书名，作者姓名使用优雅的衬线字体
- **科幻小说**：两者都使用几何形状的无衬线字体
- **奇幻小说**：书名使用装饰性衬线字体，作者姓名使用简洁的衬线字体
- **商业类书籍**：书名使用粗体无衬线字体，副标题使用轻量级的无衬线字体

## 设计迭代流程

```bash
# 1. Generate 5+ concepts across different models
infsh app run falai/flux-dev-lora --input '{"prompt": "...", "width": 832, "height": 1248}' --no-wait
infsh app run bytedance/seedream-4-5 --input '{"prompt": "..."}' --no-wait
infsh app run xai/grok-imagine-image-pro --input '{"prompt": "...", "aspect_ratio": "2:3"}' --no-wait

# 2. Refine best concept with image-to-image editing
infsh app run bytedance/seededit-3-0-i2i --input '{
  "prompt": "make the sky more dramatic with storm clouds, increase contrast",
  "image": "path/to/best-concept.png"
}'

# 3. Upscale for print quality
infsh app run falai/topaz-image-upscaler --input '{
  "image": "path/to/final-cover.png",
  "scale": 4
}'
```

## 常见错误

| 错误 | 问题 | 解决方法 |
|---------|---------|-----|
| 书籍类型判断错误 | 读者会直接放弃阅读 | 研究你所在类型的畅销书设计 |
| 书名太小 | 在缩略图中无法看清 | 书名应占据封面顶部1/3的空间 |
| 图像细节过多 | 在小尺寸下显得模糊不清 | 简化设计，合理使用负空间 |
| 使用人工智能生成的文字 | 文字显示混乱 | 在设计工具中手动添加文字 |
| 所有元素都居中 | 设计显得呆板、缺乏吸引力 | 有意使用不对称布局 |
| 盲目跟随设计趋势 | 设计很快过时 | 经典的类型规范依然具有持久的价值 |

## 检查清单

- [ ] 通过色彩和构图能够立即判断出书籍类型
- [ ] 书名在80px宽度的缩略图中清晰可读
- [ ] 封面上没有使用人工智能生成的文字
- [ ] 设计在彩色和灰度模式下均能正常显示
- [ ] 尺寸符合目标平台的规格
- [ ] 作者姓名清晰可见，且不会与书名抢镜
- [ ] 分辨率高（印刷版300 DPI，数字版2500px以上）
- [ ] 封面脊部的文字清晰可读（适用于印刷版）

## 相关技能

```bash
npx skills add inferencesh/skills@ai-image-generation
npx skills add inferencesh/skills@prompt-engineering
npx skills add inferencesh/skills@image-upscaling
```

可以浏览所有相关工具：`infsh app list`