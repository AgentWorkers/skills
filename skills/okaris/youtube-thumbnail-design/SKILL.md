---
name: youtube-thumbnail-design
description: |
  YouTube thumbnail design with specific dimensions, contrast rules, and mobile preview optimization.
  Covers safe zones, text placement, face expression psychology, and A/B testing.
  Use for: YouTube thumbnails, video cover images, click-through optimization.
  Triggers: youtube thumbnail, thumbnail design, video thumbnail, click through rate,
  ctr optimization, youtube cover, video cover image, thumbnail maker, thumbnail tips,
  youtube design, video preview image
allowed-tools: Bash(infsh *)
---

# YouTube缩略图设计

通过[inference.sh](https://inference.sh) CLI利用AI图像生成技术，制作点击率（CTR）高的YouTube缩略图。

## 快速入门

```bash
curl -fsSL https://cli.inference.sh | sh && infsh login

# Generate a thumbnail
infsh app run falai/flux-dev-lora --input '{
  "prompt": "YouTube thumbnail style, close-up of a person with surprised excited expression looking at a glowing laptop screen, vibrant blue and orange color scheme, dramatic studio lighting, shallow depth of field, high contrast, cinematic",
  "width": 1280,
  "height": 720
}'
```

## 规格要求

| 规格 | 值 |
|------|-------|
| 尺寸 | 最小1280 x 720像素 |
| 推荐尺寸 | 1920 x 1080像素 |
| 长宽比 | 16:9 |
| 最大文件大小 | 2MB |
| 格式 | JPG、GIF、PNG |

## 120像素测试

您的缩略图在手机上显示的宽度约为**120像素**——这是大多数观众首次看到缩略图的方式。

**在120像素的尺寸下，观众必须能够识别：**
1. 情绪/情感（通过颜色和表情判断）
2. 主要内容（通过构图判断）
3. 文本（如果有的话——但必须足够大才能看清）

**测试方法：**在120像素的宽度下查看您的缩略图。如果图像模糊不清，请重新设计。

## 安全区域

```
┌─────────────────────────────────────────────┐
│                                             │
│   ✅ SAFE FOR TEXT AND KEY ELEMENTS         │
│                                             │
│                                             │
│                                             │
│                                             │
│                                       ┌───┐ │
│                                       │ ⏱ │ │ ← Timestamp overlay
│                              ┌────────┴───┘ │    (bottom-right)
│   ┌────┐                     │  DURATION    │
│   │ CH │ Chapter marker      └──────────────│
└───┴────┴────────────────────────────────────┘
     ↑ Bottom-left: chapter/progress markers
```

**避免将关键元素放置在以下位置：**
- 右下角（视频时长时间戳）
- 左下角（章节标记、进度条）
- 极端边缘（裁剪效果因设备而异）

## 颜色策略

### 有效的对比色组合

| 组合 | 情绪 | 适用场景 |
|-------------|------|----------|
| 黄色 + 黑色 | 紧急、注意力 | 科技、商业、列表类内容 |
| 红色 + 白色 | 充满活力、兴奋 | 娱乐、评论类内容 |
| 蓝色 + 橙色 | 专业感强 | 教育、教程类内容 |
| 绿色 + 白色 | 成长、金钱 | 金融、成功案例类内容 |
| 紫色 + 黄色 | 高端、创意 | 设计、艺术类内容 |
| 白色 + 深色 | 清晰、简约 | 奢侈品、极简风格频道 |

### 颜色规则

- **背景**和**文本/主要内容**应形成对比或具有高对比度
- 避免使用温度相近的颜色（例如红色和橙色，会导致图像模糊）
- 每个缩略图最多使用**3种颜色**
- 颜色饱和度应比现实生活中的更高——因为缩略图会与亮色的用户界面竞争注意力

## 缩略图上的文本

### 何时使用文本

- 列表/数字：例如“7个技巧”、“前十名”
- 强烈观点：例如“停止这样做”
- 结果展示：例如“30天内赚$10,000”
- 对比信息：例如“对比两种产品”

### 何时不使用文本

- 视频标题已经包含了这些信息（重复）
- 视频中的情感或画面本身已经能够传达信息
- 文本在120像素的尺寸下无法看清

### 文本规则

| 规则 | 原因 |
|------|--------|
| 最多6个单词 | 保证在缩略图尺寸下可读 |
| 文字大小至少为60像素 | 在120像素宽度下必须清晰可见 |
| 使用粗体无衬线字体 | 细字体在小尺寸下难以看清 |
- 为文字添加对比鲜明的边框或阴影 | 无论背景如何都能保证可读性 |
- 不要使用过小的文字 | 如果文字太小而无法看清，就删除它

## 人脸表情心理学

包含人脸的缩略图的点击率通常比没有人脸的缩略图更高。表情对点击率有很大影响：

| 表情 | 对点击率的影响 | 适用场景 |
|------------|-----------|----------|
| **惊讶/震惊** | 最高 | 反应类、揭秘类、发现类内容 |
| **好奇** | 高 | 教程、操作指南、技巧类内容 |
| **兴奋** | 高 | 开箱视频、评论、公告类内容 |
| **担忧** | 中等偏高 | 警告类、错误提示类内容 |
| **自信** | 中等 | 专家建议、权威类内容 |
| **中性** | 最低 | 除非您的品牌风格非常极简，否则避免使用 |

### 人脸构图规则

- 人脸应占据缩略图的**30-50%** |
- 眼睛应**朝向文本或主要内容**（引导观众的注意力）
- 眼睛看向镜头表示亲切感；看向物体表示好奇心 |
- 通常将人脸放在左侧，文本或主要内容放在右侧

```bash
# Generate a face-forward thumbnail
infsh app run falai/flux-dev-lora --input '{
  "prompt": "close-up portrait of a man with genuinely surprised expression, mouth slightly open, raised eyebrows, looking at camera, left side of frame, vibrant teal background, dramatic rim lighting, YouTube thumbnail style, high contrast, cinematic",
  "width": 1280,
  "height": 720
}'

# Generate a face-looking-at-subject thumbnail
infsh app run bytedance/seedream-4-5 --input '{
  "prompt": "person looking amazed at a glowing holographic chart showing upward growth, dramatic blue and green lighting, right side profile view, dark background, tech aesthetic, high energy",
  "size": "2K"
}'
```

## 不同内容类型的缩略图模板

### 教程/操作指南类
```bash
infsh app run falai/flux-dev-lora --input '{
  "prompt": "overhead flat lay of organized workspace with laptop showing code editor, colorful sticky notes, coffee cup, clean bright background, professional setup, tutorial style composition, warm lighting",
  "width": 1280,
  "height": 720
}'
```

### 使用前/使用后对比
```bash
infsh app run falai/flux-dev-lora --input '{
  "prompt": "split composition, left side dark and messy disorganized desk, right side bright clean organized minimalist workspace, dramatic contrast between chaos and order, clear dividing line in center, high contrast",
  "width": 1280,
  "height": 720
}'
```

### 产品评论/对比类
```bash
infsh app run falai/flux-dev-lora --input '{
  "prompt": "two products facing each other with dramatic lighting and sparks between them, competition battle concept, dark background with colorful rim lighting, versus comparison style, high energy, product photography",
  "width": 1280,
  "height": 720
}'
```

### 列表文章/数字类
```bash
infsh app run falai/flux-dev-lora --input '{
  "prompt": "dynamic arrangement of 7 different colorful objects floating in space against dark gradient background, each item distinct and clearly separated, energetic composition, vibrant saturated colors, studio lighting",
  "width": 1280,
  "height": 720
}'
```

## A/B测试

每次只测试一个变量：

| 变量 | A组 vs B组 |
|----------|-------------|
| 有脸 vs 无脸 | 构图相同，是否包含人物 |
| 表情 | 惊讶 vs 好奇 |
| 颜色方案 | 温暖色调 vs 冷色调 |
| 是否有文字 | 有文字覆盖 vs 无文字 |
| 背景 | 明亮背景 vs 深色背景 |
| 主要内容朝向 | 向左 vs 向右 |

```bash
# Generate variant A
infsh app run falai/flux-dev-lora --input '{
  "prompt": "..., bright yellow background, ...",
  "width": 1280, "height": 720
}' --no-wait

# Generate variant B (same prompt, different background)
infsh app run falai/flux-dev-lora --input '{
  "prompt": "..., dark navy background, ...",
  "width": 1280, "height": 720
}' --no-wait
```

## 缩略图检查清单

- [ ] 尺寸至少为1280x720像素（推荐1920x1080像素）
- 文件大小小于2MB
- 在120像素的尺寸下仍清晰可见
- 右下角（时间戳）和左下角（章节标记）没有关键元素
- 最多使用3种颜色，形成高对比度
- 如果有文本，最多6个单词，使用粗体字体，并添加对比鲜明的边框
- 人脸表情与内容的情感相匹配（如果适用）
- 不要与视频标题重复
- 与周围的缩略图区分开来（符合您的内容风格）
- 在明暗不同的YouTube背景下都能清晰显示

## 常见错误

| 错误 | 问题 | 解决方法 |
|---------|---------|-----|
| 文字太多 | 在缩略图尺寸下无法看清 | 最多使用6个单词或不使用文字 |
| 对比度低 | 在视频列表中难以识别 | 使用对比鲜明的颜色 |
- 构图杂乱 | 观众不知道该看哪里 | 保持一个焦点 |
- 使用通用的库存图片 | 缺乏个性，容易被忽略 | 使用真实的人物表情和独特的拍摄角度 |
- 细节过于复杂 | 在120像素的尺寸下无法看清 | 使用粗体字体和简单的形状 |
- 所有视频的缩略图风格相同 | 会导致观众疲劳 | 在品牌规范内保持多样性 |
| 误导性的缩略图 | 会降低观众的信任度 | 使缩略图与实际内容一致 |

## 相关技能

```bash
npx skills add inferencesh/skills@ai-image-generation
npx skills add inferencesh/skills@image-upscaling
npx skills add inferencesh/skills@prompt-engineering
```

查看所有可用工具：`infsh app list`