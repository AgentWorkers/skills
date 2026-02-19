---
name: youtube-thumbnail-design
description: "**YouTube缩略图设计指南：特定尺寸、对比度规则及移动预览优化**  
本指南涵盖了YouTube缩略图的设计要素，包括安全区域、文本布局、面部表情对观众情绪的影响，以及A/B测试方法。适用于YouTube缩略图、视频封面图片的优化，旨在提升点击率（CTR）。  
**主要内容：**  
1. **具体尺寸与对比度规则**：介绍YouTube缩略图的标准尺寸要求及如何通过调整对比度来提升视觉效果。  
2. **移动预览优化**：针对移动设备用户优化缩略图显示效果，确保在各种屏幕尺寸下都能提供良好的用户体验。  
3. **文本放置策略**：指导如何在缩略图中合理布局文字，以提升信息的可读性。  
4. **面部表情心理学**：分析面部表情对观众情绪的影响，以及如何在缩略图中运用这一元素来增强视频吸引力。  
5. **A/B测试**：介绍如何通过对比不同设计方案来评估哪种方案更有效。  
**适用场景：**  
- YouTube视频制作  
- 视频封面设计  
- 点击率提升策略  
**关键词：**  
- YouTube缩略图  
- 缩略图设计  
- 对比度优化  
- 移动预览  
- 文本布局  
- 面部表情心理学  
- A/B测试  
**相关工具与资源：**  
- YouTube缩略图生成工具  
- 设计软件  
- A/B测试平台"
allowed-tools: Bash(infsh *)
---
# YouTube缩略图设计

通过[inference.sh](https://inference.sh)命令行工具，利用AI图像生成技术来创建点击率（CTR）高的YouTube缩略图。

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

> **安装说明：** [安装脚本](https://cli.inference.sh)仅会检测您的操作系统和架构，然后从`dist.inference.sh`下载相应的二进制文件，并验证其SHA-256校验和。无需特殊权限或后台进程。也可以[手动安装并验证](https://dist.inference.sh/cli/checksums.txt)。

## 规格要求

| 规格 | 值 |
|------|-------|
| 尺寸 | 最小1280 x 720像素 |
| 推荐尺寸 | 1920 x 1080像素 |
| 长宽比 | 16:9 |
| 文件大小上限 | 2MB |
| 支持的格式 | JPG、GIF、PNG |

## 120像素测试

您的缩略图在移动设备上的显示宽度约为**120像素**——这是大多数观众首次看到缩略图时的尺寸。

**在120像素的尺寸下，观众必须能够识别：**
1. 视频的情绪/氛围（通过颜色和表情判断）
2. 视频的主题（通过构图判断）
3. 文本内容（如果有的话——前提是文本足够大）

**测试方法：** 在120像素的宽度下查看您的缩略图。如果图像模糊不清，就需要重新设计。

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

**请避免将以下关键元素放置在缩略图中：**
- 右下角（视频时长时间戳）
- 左下角（章节标记、进度条）
- 极端边缘（不同设备的裁剪效果可能不同）

## 颜色策略

### 有效的对比色组合

| 组合 | 情绪 | 适用场景 |
|-------------|------|----------|
| 黄色 + 黑色 | 紧急、吸引注意力 | 科技、商业类内容 |
| 红色 + 白色 | 充满活力、激发兴趣 | 娱乐、评论类内容 |
| 蓝色 + 橙色 | 专业感强 | 教育、教程类内容 |
| 绿色 + 白色 | 代表成长、金钱 | 金融、成功案例类内容 |
| 紫色 + 黄色 | 高端、创意感 | 设计、艺术类内容 |
| 白色 + 深色 | 清晰、简约 | 奢侈品、极简风格频道 |

### 颜色使用规则

- **背景**和**文本/主题**的颜色应形成对比或互补
- 避免使用温度相近的颜色（例如红色和橙色，会导致图像模糊）
- 每个缩略图最多使用**3种颜色**
- 颜色饱和度应比现实生活中的更高——因为缩略图会与亮色的用户界面竞争注意力

## 缩略图上的文字

### 何时使用文字

- 列表/数字：例如“7个技巧”、“前十名”
- 强烈的观点：例如“停止这样做”
- 结果展示：例如“30天内赚1万美元”
- 对比信息：例如“对比两种产品”

### 何时不使用文字

- 视频标题已经包含了这些信息（避免重复）
- 视频的情绪或画面本身已经能够传达信息
- 如果文字太小，在120像素的尺寸下无法看清

### 文字使用规则

| 规则 | 原因 |
|------|--------|
| 最多6个单词 | 保证在缩略图尺寸下仍可读 |
| 字体至少为60像素高 | 在120像素宽度下必须清晰可见 |
| 使用粗体无衬线字体 | 细字体在小尺寸下难以辨认 |
| 为文字添加对比鲜明的边框或阴影 | 无论背景如何都能保证可读性 |
| 不要使用过小的文字 | 如果文字太小，就删除它

## 人脸表情心理学

带有人脸的缩略图的点击率通常比没有人脸的缩略图更高。表情对点击率有很大影响：

| 表情 | 对点击率的影响 | 适用场景 |
|------------|-----------|----------|
| **惊讶/震惊** | 最高 | 反应类、揭秘类、发现类内容 |
| **好奇** | 高 | 教程、操作指南、技巧类内容 |
| **兴奋** | 高 | 开箱视频、评论、公告类内容 |
| **担忧/焦虑** | 中等偏高 | 警告、错误提示、问题类内容 |
| **自信** | 中等 | 专家建议、权威类内容 |
| **中性** | 最低 | 除非您的品牌风格非常极简，否则避免使用 |

### 人脸构图规则

- 人脸应占据缩略图的**30-50%**面积 |
- 眼睛应**朝向文字或主题**（引导观众的注意力）
- 眼睛看向镜头表示亲切感；看向物体表示好奇心 |
- 通常将人脸放在左侧，文字或主题放在右侧

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

### 列表/数据类
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
|---------|-------------|
| 有脸 vs 无脸 | 构图相同，是否包含人物 |
| 表情 | 惊讶 vs 好奇 |
| 颜色方案 | 温暖色调 vs 冷色调 |
| 是否有文字 | 有文字覆盖 vs 无文字 |
| 背景 | 明亮背景 vs 深色背景 |
| 主体朝向 | 主体朝向左侧 vs 右侧 |

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

- 尺寸：至少1280x720像素（推荐1920x1080像素）
- 文件大小：不超过2MB
- 在120像素的尺寸下仍清晰可见
- 右下角（时间戳）和左下角（章节标记）没有关键元素
- 最多使用3种颜色，颜色对比鲜明
- 文字（如果有的话）最多6个单词，使用粗体字体，并添加对比鲜明的边框
- 人脸表情与视频内容的情感相匹配
- 文字不与视频标题重复
- 与周围的缩略图区分开来（符合您的内容风格）
- 在明暗不同的YouTube背景下都能正常显示

## 常见错误

| 错误 | 问题 | 解决方法 |
|---------|---------|-----|
| 文字太多 | 在缩略图尺寸下无法看清 | 最多使用6个单词或完全不使用文字 |
| 颜色对比度低 | 在视频播放列表中难以辨认 | 使用互补色 |
- 构图杂乱 | 观众无法确定重点 | 保持一个焦点 |
- 使用通用的库存图片 | 缺乏个性，容易被忽略 | 使用真实的人物表情和独特的拍摄角度 |
- 细节过小 | 在120像素的尺寸下无法看清 | 使用粗体、简单的形状 |
- 所有视频的缩略图风格相同 | 会导致观众疲劳 | 在品牌规范内进行变化 |
- 缩略图与视频内容不符 | 会降低用户的信任度 | 使缩略图与视频内容保持一致 |

## 相关技能

```bash
npx skills add inference-sh/skills@ai-image-generation
npx skills add inference-sh/skills@image-upscaling
npx skills add inference-sh/skills@prompt-engineering
```

浏览所有可用工具：`infsh app list`