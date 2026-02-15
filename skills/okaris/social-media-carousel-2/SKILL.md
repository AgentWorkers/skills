---
name: social-media-carousel
description: |
  Multi-slide carousel design for Instagram, LinkedIn, and Twitter/X with layout rules and hooks.
  Covers slide structure, text hierarchy, swipe psychology, and platform-specific specs.
  Use for: carousel posts, Instagram carousels, LinkedIn carousels, slide posts, educational content.
  Triggers: carousel, instagram carousel, linkedin carousel, slide post, carousel design,
  swipe post, multi-image post, carousel template, educational carousel, carousel content,
  instagram slides, linkedin slides
allowed-tools: Bash(infsh *)
---

# 社交媒体轮播图

通过 [inference.sh](https://inference.sh) 命令行工具设计高互动性的轮播图内容。

## 快速入门

```bash
curl -fsSL https://cli.inference.sh | sh && infsh login

# Generate a carousel slide
infsh app run infsh/html-to-image --input '{
  "html": "<div style=\"width:1080px;height:1080px;background:#0f172a;display:flex;align-items:center;justify-content:center;padding:80px;font-family:system-ui;color:white;text-align:center\"><div><p style=\"font-size:24px;color:#818cf8;text-transform:uppercase;letter-spacing:3px\">5 Rules for</p><h1 style=\"font-size:64px;margin:16px 0;font-weight:900;line-height:1.1\">Writing Headlines That Convert</h1><p style=\"font-size:22px;opacity:0.5;margin-top:24px\">Swipe →</p></div></div>"
}'
```

## 平台规格

| 平台 | 尺寸 | 幻灯片数量 | 宽高比 |
|----------|-----------|--------|---------------|
| **Instagram** | 1080 x 1080 像素 | 最多 20 张 | 1:1（默认），4:5，16:9 |
| **LinkedIn** | 1080 x 1080 像素 或 1080 x 1350 像素 | 最多 20 张 | 1:1，4:5 |
| **Twitter/X** | 1080 x 1080 像素 | 最多 4 张 | 1:1，16:9 |
| **Facebook** | 1080 x 1080 像素 | 最多 10 张 | 1:1，4:5 |

**在 Instagram 和 LinkedIn 上使用 1080 x 1350（4:5）的格式**——这种格式在信息流中占据更多显示空间。

## 轮播图结构

### 7 张幻灯片的框架

| 幻灯片 | 用途 | 内容 |
|-------|---------|---------|
| 1 | **吸引注意力** | 强烈的陈述、问题或承诺——阻止用户继续滑动 |
| 2 | **背景信息** | 说明为什么这个内容重要，介绍问题背景 |
| 3-6 | **价值点** | 每张幻灯片展示一个要点 |
| 7 | **行动号召** | 要求用户关注、保存、分享、评论或点击链接 |

### 幻灯片 1：吸引注意力

这是最重要的幻灯片。如果这部分设计失败，用户就不会继续滑动浏览了。

| 吸引注意力的方式 | 例子 |
|-----------|---------|
| 强烈的陈述 | “90% 的着陆页都犯了这个错误” |
| 问题 | “为什么你的广告有点击量，但没有转化？” |
| 数字 + 承诺 | “7 个我早该学到的 Python 技巧” |
| 反传统建议 | “别写博客文章了，试试这个方法” |
| 前后对比 | 展示变化效果 |

```bash
# Hook slide
infsh app run infsh/html-to-image --input '{
  "html": "<div style=\"width:1080px;height:1350px;background:linear-gradient(180deg,#1e1b4b,#312e81);display:flex;align-items:center;justify-content:center;padding:80px;font-family:system-ui;color:white;text-align:center\"><div><h1 style=\"font-size:72px;font-weight:900;line-height:1.15;margin:0\">90% of Landing Pages Make This Mistake</h1><p style=\"font-size:28px;opacity:0.6;margin-top:32px\">Swipe to find out →</p></div></div>"
}'
```

### 幻灯片 2-6：内容幻灯片

每张幻灯片只展示一个要点。切勿堆砌多个信息。

```bash
# Content slide template
infsh app run infsh/html-to-image --input '{
  "html": "<div style=\"width:1080px;height:1350px;background:#1e1b4b;padding:80px;font-family:system-ui;color:white;display:flex;flex-direction:column;justify-content:center\"><div><p style=\"font-size:120px;font-weight:900;color:#818cf8;margin:0;line-height:1\">01</p><h2 style=\"font-size:48px;margin:24px 0 16px;font-weight:800;line-height:1.2\">Your headline is too vague</h2><p style=\"font-size:26px;opacity:0.8;line-height:1.6\">\"Welcome to our platform\" tells the visitor nothing. Lead with the outcome: \"Ship docs in minutes, not days.\"</p></div></div>"
}'
```

### 幻灯片 7：行动号召幻灯片

```bash
# CTA slide
infsh app run infsh/html-to-image --input '{
  "html": "<div style=\"width:1080px;height:1350px;background:linear-gradient(180deg,#312e81,#1e1b4b);display:flex;align-items:center;justify-content:center;padding:80px;font-family:system-ui;color:white;text-align:center\"><div><h2 style=\"font-size:56px;font-weight:900;margin:0;line-height:1.2\">Found this useful?</h2><p style=\"font-size:32px;opacity:0.8;margin-top:24px;line-height:1.5\">Save this post for later 🔖<br>Follow for more tips</p><p style=\"font-size:24px;opacity:0.4;margin-top:40px\">@yourusername</p></div></div>"
}'
```

## 设计规则

### 文本层次结构

| 元素 | 在 1080 像素屏幕上的大小 | 重要性 |
|---------|-----------------|--------|
| 幻灯片编号 | 96-120 像素 | 黑色（字体颜色 900） |
| 标题 | 48-64 像素 | 加粗（字体颜色 700-800） |
| 正文 | 24-28 像素 | 普通字体（字体颜色 400） |
| 标注/标签 | 18-22 像素 | 中等字体（字体颜色 500） |

### 可读性

| 规则 | 重要性 |
|------|-------|
| 每张幻灯片的字数上限 | 30-40 个字 |
| 正文行数上限 | 4-5 行 |
| 行高 | 1.5-1.6 倍 |
| 字体 | 无衬线字体（如 Inter, Montserrat, Poppins） |
| 文字对比度 | 最低 4.5:1（符合 WCAG AA 标准） |

### 视觉一致性

| 元素 | 所有幻灯片要保持一致 |  
|---------|----------------------------------|
| 背景颜色/渐变 | 使用相同的配色方案，允许轻微变化 |
| 字体系列 | 全部幻灯片使用相同的字体 |
| 文本对齐方式 | 保持相同的对齐方式（左对齐或居中） |
| 边距/内边距 | 保持相同的间距 |
| 强调颜色 | 使用相同的高亮颜色 |
| 编号格式 | 保持统一的编号格式（如 01, 02 或 1., 2.） |

## 轮播图类型

### 教育性内容 / 提示

```
Slide 1: "5 CSS tricks you need to know"
Slide 2: Trick 1 with code example
Slide 3: Trick 2 with code example
...
Slide 6: Trick 5 with code example
Slide 7: "Follow for more dev tips"
```

### 故事讲述 / 案例研究

```
Slide 1: "How we grew from 0 to $1M ARR"
Slide 2: The beginning (context)
Slide 3: The challenge
Slide 4: What we tried (failed)
Slide 5: What worked
Slide 6: The result (numbers)
Slide 7: Key takeaway + CTA
```

### 前后对比

```
Slide 1: "I redesigned this landing page"
Slide 2: Before screenshot
Slide 3: Problem 1 annotated
Slide 4: After screenshot
Slide 5: Improvement 1 explained
Slide 6: Results (conversion lift)
Slide 7: "Want a review? DM me"
```

### 列表文章 / 工具推荐

```
Slide 1: "10 tools every designer needs in 2025"
Slides 2-6: 2 tools per slide with logo + one-liner
Slide 7: "Save this for later 🔖"
```

## 用户滑动行为心理学

| 原理 | 应用方法 |
|-----------|------------|
| **好奇心驱动** | 用吸引人的内容促使用户继续滑动 |
| **编号进度** | “3/7” 的格式激发用户完成任务的欲望 |
| **视觉连贯性** | 一致的设计让人感觉到还有更多内容 |
| **逐步增加价值** | 最重要的提示放在最后，鼓励用户完成整个内容 |
| **滑动提示** | 在第一张幻灯片上添加“滑动 →”的提示 |

## 批量生成轮播图

```bash
# Generate all slides for a carousel
for i in 1 2 3 4 5 6 7; do
  infsh app run infsh/html-to-image --input "{
    \"html\": \"<div style='width:1080px;height:1350px;background:#1e1b4b;display:flex;align-items:center;justify-content:center;padding:80px;font-family:system-ui;color:white'><div style='text-align:center'><p style='font-size:28px;opacity:0.5'>Slide $i of 7</p></div></div>\"
  }" --no-wait
done
```

## 人工智能生成的轮播图视觉效果

```bash
# Generate illustrations for each slide
infsh app run falai/flux-dev-lora --input '{
  "prompt": "minimal flat illustration, person at desk with laptop, clean modern style, simple shapes, limited color palette purple and blue tones, white background, icon style",
  "width": 1080,
  "height": 1080
}'
```

## 常见错误

| 错误 | 问题 | 解决方法 |
|---------|---------|-----|
| 吸引注意力的内容不足（幻灯片 1） | 用户不会继续滑动 | 使用强烈的陈述、问题或数字 + 承诺 |
| 每张幻灯片文字过多 | 信息过于繁杂，用户无法阅读 | 每张幻灯片最多 30-40 个字 |
| 视觉设计不一致 | 各个幻灯片看起来像不同的内容 | 保持相同的颜色、字体和边距 |
| 没有滑动提示 | 用户不知道还有更多内容 | 在第一张幻灯片上添加“滑动 →”或箭头提示 |
| 最后一张幻灯片没有行动号召 | 错失互动机会 | 提供保存、关注、分享或评论的选项 |
| 编号格式不一致 | 使内容显得杂乱无章 | 所有幻灯片的编号格式要保持一致 |
| 每张幻灯片包含多个要点 | 用户难以理解 | 每张幻灯片只展示一个要点 |
| 在 Instagram 上使用方形格式 | 会浪费信息流空间 | 使用 1080x1350（4:5）的格式以提高可见性 |

## 相关技能

```bash
npx skills add inferencesh/skills@ai-image-generation
npx skills add inferencesh/skills@content-repurposing
npx skills add inferencesh/skills@linkedin-content
```

浏览所有应用：`infsh app list`