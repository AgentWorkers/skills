---
name: ad-creative-analysis
description: 分析从竞争对手研究中提取的广告创意（图片和视频）。当提供广告图片目录、视频文件或文字记录时，使用该功能来评估广告质量、衡量视觉效果和信息传递的有效性，为广告的传播潜力或用户参与度打分，并生成创意之间的对比分析报告。该功能可通过以下请求触发：分析这些广告、对这些创意进行评分、竞争对手使用了哪些吸引用户的元素、评估广告素材库、给出评分结果、分析该广告文件夹，或分析这些广告中的成功要素。
---
# 广告创意分析

分析竞争对手或参考广告的创意文件。为每个创意生成一个 JSON 分析报告，并总结跨创意的共性模式。

## 第一步 — 接收输入

输入可以是：
- 包含图片文件（`.jpg`, `.jpeg`, `.png`, `.webp`, `.gif`）和/或视频文件（`.mp4`, `.mov`, `.avi`, `.webm`）的目录路径
- 该目录中可选的 `metadata.json` 文件，其中包含每个文件的以下字段：`platform`, `spend`, `duration_days`, `impressions`, `format`

如果没有提供目录路径，提示用户：“请提供包含广告创意的目录路径。”

列出目录中的所有文件，并将它们分为图片广告和视频广告。在继续之前，记录每种类型的文件数量。

## 第二步 — 分析图片广告

对于每个图片文件，使用视觉分析工具来评估以下方面：

### 设计评估

评估以下五个维度：
1. **视觉层次** — 视线是否首先被吸引到正确的元素上？是否有明确的焦点？
2. **色彩运用** — 色彩搭配是否具有对比度，能否引发情感，并保持品牌一致性？
3. **文字可读性** — 文字是否一目了然？字体大小、对比度和位置是否合适？
4. **呼叫行动（CTA）的显眼度** — 呼叫行动是否在视觉上醒目，位置是否清晰，且易于点击？
5. **品牌一致性** — 标志的位置、色彩的使用以及字体是否与品牌身份相符。

### 图片评分（每个维度 1-10 分）

- `attention_grab` — 这个创意能多快、多强烈地吸引用户的注意力，使其停止滚动？
- `message_clarity` — 核心信息是否无需背景信息就能清晰传达？
- `cta_strength` — 呼叫行动是否具有吸引力且易于执行？

### 图片信息提取

提取以下内容：
- `primary_message` — 这个广告要传达的核心信息（一句话）
- `emotion_appeal` — 情感诉求：恐惧、渴望、社会认同、紧迫感、好奇心、幽默、信任、归属感或独特性
- `target_audience` — 从视觉元素、文案和上下文中推断出的目标受众（例如：“25-35 岁对健身感兴趣的女性”）
- `hook_text` — 眼睛首先看到的文案部分（标题或正文）

## 第三步 — 分析视频广告

对于每个视频文件，直接使用视觉分析工具进行评估。如果视频旁边有字幕文件（文件名相同，扩展名为 `.txt` 或 `.srt`），请阅读并使用该字幕文件。

### 视频评估

评估以下四个维度：
1. **开头吸引力的质量（前 3 秒）** — 视频是否立即引发好奇心、震撼或共鸣？用户是否会停止滚动？
2. **剧本结构** — 视频是否遵循逻辑性的说服路径（问题、解决方案、证明、呼叫行动）？
3. **节奏** — 编辑节奏是否适合平台和受众？既不太慢也不太快？
4. **呼叫行动的放置** — 呼叫行动是否清晰、时机是否恰当，并在需要时重复出现？

### 视频评分（1-10 分）

为广告的病毒传播潜力和互动潜力分配一个总体评分：
- **9-10**：开头非常吸引人，剧本紧凑，呼叫行动清晰。在高预算下表现优异。
- **7-8**：基础要素不错，但存在小缺点。适合进行测试。
- **5-6**：执行一般。需要更有力的开头或更清晰的呼叫行动才能扩大影响力。
- **3-4**：核心理念存在，但执行效果不佳。需要大幅修改。
- **1-2**：不太可能取得好效果。开头、信息或呼叫行动存在根本性问题。

详细评分标准请参阅 `references/analysis-framework.md`。

### 视频信息提取

提取以下内容：
- `hook_text` — 前 3 秒内说出的或展示的文字
- `hook_type` — 开头类型：问题、强烈主张、痛点、好奇心、社会认同、前后对比、演示
- `main_message` — 广告中陈述的核心价值主张
- `emotion_appeal` — 情感诉求：恐惧、渴望、社会认同、紧迫感、好奇心、幽默、信任、归属感或独特性
- `cta_text` — 呼叫行动的文字内容
- `ctatiming` — 呼叫行动出现的时间（例如：“结尾”、“中间”、“在整个视频中重复出现”）

## 第四步 — 全部广告类型的通用元数据

无论广告类型如何，记录以下信息：
- `filename` — 文件名
- `ad_format` — 广告格式（单张图片、轮播图、视频、故事或系列视频）
- `aspect_ratio` — 检测或推断出的宽高比（例如：`1:1`, `9:16`, `16:9`, `4:5`）
- `dimensions` — 如果可以检测到的话，以像素为单位记录宽度 x 高度
- `ad_objective` — 根据内容和呼叫行动推断出的广告目标：提升知名度、引发考虑或促成转化
- `platform_fit` — 该格式和比例最适合的平台（例如：`["Instagram Feed", "Facebook Feed"]`

## 第五步 — 生成每个创意的 JSON 报告

为每个创意生成一个 JSON 对象。将所有结果合并到一个 JSON 数组中输出。

### 图片广告示例结构

```json
{
  "filename": "ad_001.jpg",
  "type": "image",
  "ad_format": "single_image",
  "aspect_ratio": "1:1",
  "dimensions": "1080x1080",
  "ad_objective": "conversion",
  "platform_fit": ["Instagram Feed", "Facebook Feed"],
  "scores": {
    "attention_grab": 8,
    "message_clarity": 7,
    "cta_strength": 9
  },
  "primary_message": "Lose 10kg in 30 days without giving up your favourite food",
  "emotion_appeal": "aspiration",
  "target_audience": "Women 28-45 who have tried dieting before",
  "hook_text": "Still counting calories? There's a better way."
}
```

### 视频广告示例结构

```json
{
  "filename": "ad_002.mp4",
  "type": "video",
  "ad_format": "video",
  "aspect_ratio": "9:16",
  "dimensions": "1080x1920",
  "ad_objective": "consideration",
  "platform_fit": ["TikTok", "Instagram Reels", "Facebook Reels"],
  "scale_score": 8,
  "hook_text": "I was $40,000 in debt until I found this",
  "hook_type": "before_after",
  "main_message": "This budgeting app helped me pay off debt in 18 months",
  "emotion_appeal": "fear",
  "cta_text": "Download free — link in bio",
  "cta_timing": "end"
}
```

## 第六步 — 生成跨创意总结

分析完所有创意后，生成一个 `summary` 对象并添加到输出结果中。内容包括：
- `total_analyzed` — 分析的创意总数（按类型分类）
- `top_performers` — 按评分排名的前 3 个创意的文件名（图片广告按平均分排序，视频广告按评分排序）
- `dominant_emotion` — 在所有广告中最常出现的情感诉求
- `common_hooks` — 常见的开头模式或短语
- `cta_patterns` — 最常见的呼叫行动结构（例如：“动词 + 免费 + 紧迫感”
- `dominant_objective` — 最常见的广告目标
- `format_breakdown` — 各广告格式的数量统计
- `recommendations` — 3-5 条改进或扩大这些创意的可操作建议

### 总结示例结构

```json
{
  "summary": {
    "total_analyzed": { "images": 5, "videos": 3 },
    "top_performers": ["ad_004.jpg", "ad_002.mp4", "ad_007.jpg"],
    "dominant_emotion": "aspiration",
    "common_hooks": [
      "Question-based hook challenging a common belief",
      "Before/after framing in first sentence"
    ],
    "cta_patterns": [
      "Shop now + scarcity signal",
      "Free trial + no credit card"
    ],
    "dominant_objective": "conversion",
    "format_breakdown": { "single_image": 4, "video": 3, "carousel": 1 },
    "recommendations": [
      "Hooks are strong but CTAs lack urgency — test adding 'today only' or limited quantity",
      "All videos open with talking head — test a demonstration hook for variety",
      "Aspiration dominates — test a fear/pain angle to broaden audience response"
    ]
  }
}
```

## 第七步 — 处理缺失或无法读取的文件

如果某个文件无法分析（损坏、格式不支持或图像太暗/模糊而无法识别）：
- 在输出结果中包含文件名，并附上 `"status": "unreadable"` 以及简要的 „reason“ 说明
- 继续分析剩余的文件，不要停止分析

## 参考资料

请参阅 `skills/ad-creative-analysis/references/analysis-framework.md`，以获取：
- 各指标的详细评分标准
- 广告心理学模式定义
- 开头设计模板
- 扩展的示例输出