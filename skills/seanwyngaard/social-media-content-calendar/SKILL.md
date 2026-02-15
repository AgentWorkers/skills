---
name: social-media-content-calendar
description: 生成结构化的社交媒体内容日历，包括针对不同平台的帖子、相关标签（hashtags）以及发布时间安排。该工具可用于制定社交媒体计划、内容日历或为客户准备社交媒体管理报告。
argument-hint: "[niche-or-brand] [platforms] [timeframe]"
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, WebSearch
---

# 社交媒体内容日历

该工具可生成针对不同平台的内容日历，包括适合各平台的帖子内容、相关标签建议、图片素材以及发布计划，并可将结果导出至 Buffer、Hootsuite 或 Later 等平台。

## 使用方法

```
/social-media-content-calendar "Vegan bakery in Austin" "instagram,tiktok" "4 weeks"
/social-media-content-calendar "B2B SaaS startup" "linkedin,twitter" "2 weeks"
/social-media-content-calendar "Personal fitness coach" "instagram,youtube,tiktok" "1 month"
```

- `$ARGUMENTS[0]`：品牌/细分市场描述
- `$ARGUMENTS[1]`：需要发布的平台（用逗号分隔）：`instagram`, `twitter`, `linkedin`, `tiktok`, `facebook`, `youtube`, `threads`
- `$ARGUMENTS[2]`：时间范围（默认为4周）

## 日历生成流程

### 第一步：品牌与受众分析

根据项目要求，明确以下内容：
- **品牌风格**：专业、轻松、幽默、励志或教育性
- **目标受众**：人口统计特征、兴趣爱好及需求
- **内容主题**（3-5个核心主题）：
  - 以健身教练为例：锻炼方法、营养知识、激励话语、客户成果、幕后花絮
- **竞争对手分析**：在该细分市场中哪些类型的内容效果较好？

### 第二步：平台策略

为每个平台设定发布频率和内容类型：

| 平台 | 每周发布数量 | 最适合的内容类型 | 最佳发布时间 |
|----------|-----------|-------------------|------------|
| Instagram | 4-5条帖子 + 5-7条快拍 | Reels（短视频）、轮播图、单张图片 | 周二至周五上午10点至下午2点 |
| TikTok | 5-7条视频 | 15-60秒的短视频、热门趋势内容 | 周二至周四晚上7点至9点 |
| LinkedIn | 3-4条帖子 | 文本帖子、轮播图、文章 | 周二至周四上午8点至10点 |
| Twitter/X | 5-7条帖子 | Threads（长文本聊天）、观点性内容 | 周一至周五上午8点至10点、中午12点至下午1点 |
| Facebook | 3-4条帖子 | 视频、链接、社区互动内容 | 周三至周五上午1点至下午4点 |
| YouTube | 1-2条视频 | 长视频或短视频 | 周四至周六下午2点至4点 |
| Threads | 4-5条帖子 | 对话式内容、观点分享、实用技巧 | 类似 Instagram 的发布模式 |

### 第三步：内容组合

根据以下比例安排各类内容：

| 内容类型 | 占比 | 目的       |
|-------------|-----------|---------|
| 教育性内容 | 40% | 传授知识、提供技巧、教程 |
| 互动性内容 | 25% | 提问、投票、引发讨论、分享热点 |
| 促销性内容 | 20% | 产品推广、服务介绍、行动号召（CTA） |
| 个人分享/品牌故事 | 15% | 幕后花絮、个人故事、企业文化 |

### 第四步：生成日历

为每条帖子生成详细信息：

```yaml
date: "2026-02-17"
day: "Monday"
platform: "instagram"
content_type: "reel"
content_pillar: "Workouts"
mix_category: "Educational"

caption: |
  Full caption text here.

  Include line breaks for readability.

  End with a CTA (save, share, comment, link in bio).

hashtags:
  primary: ["#fitness", "#homeworkout"]  # 3-5 high-volume
  secondary: ["#fitnesstips", "#workoutmotivation"]  # 3-5 medium
  niche: ["#austinfitness", "#veganfitness"]  # 3-5 low-competition

image_prompt: "Description for AI image generation or photographer brief"
alt_text: "Accessible image description for screen readers"
cta: "Save this for your next workout"
notes: "Any additional context for the social media manager"
```

### 第五步：平台适配

针对每个平台对帖子内容进行个性化调整：

**Instagram**：
- 标题：最多2200个字符，但前125个字符会显示在预览中
- 标签：在第一条评论中添加20-30个相关标签（不要放在标题中）
- Reels（短视频）：在描述的前3秒内加入吸引人的内容
- 轮播图：按顺序展示所有图片

**TikTok**：
- 标题：最多300个字符
- 标签：使用3-5个相关标签
- 包括视频的吸引人开头、建议使用的背景音乐以及视频结构概述
- 重点关注开头1-3秒的吸引部分

**LinkedIn**：
- 正文中不使用标签，仅在底部添加3-5个标签
- 第一行内容要具有吸引力（会在“查看更多”前显示）
- 保持专业风格，内容需基于数据支持
- 多使用换行（每行一个句子）

**Twitter/X**：
- 每条推文最多280个字符
- Threads（长文本聊天）：为每条推文编号
- 推文1中包含吸引人的内容
- 正文中不使用标签（最多使用1-2个）
- 互动方式：提问、投票、分享观点

**Facebook**：
- 可发布较长的帖子（1-2段）
- 通过提问激发用户评论
- 链接帖子时，在链接上方添加吸引人的描述
- 最多使用1-3个标签

### 第六步：输出格式

生成的日历文件将保存在 `output/content-calendar/` 目录下：

```
output/content-calendar/
  calendar-overview.md          # Strategy summary, pillars, mix ratios
  week-1.md                     # All posts for week 1
  week-2.md                     # All posts for week 2
  ...
  calendar-export.csv           # Import-ready for Buffer/Hootsuite/Later
  hashtag-library.md            # All researched hashtags by category
  image-prompts.md              # All image/video descriptions consolidated
```

**CSV导出格式**（兼容 Buffer/Hootsuite）：
```csv
Date,Time,Platform,Content,Hashtags,Image Description,Link
2026-02-17,10:00,instagram,"Caption text here","#tag1 #tag2","Image description",""
```

### 第七步：标签研究

为该细分市场整理一系列相关标签：

```markdown
## Hashtag Library: [Niche]

### High Volume (500K+ posts) — Use 3-5 per post
#fitness #workout #healthylifestyle ...

### Medium Volume (50K-500K) — Use 3-5 per post
#fitnesstips #homeworkoutroutine ...

### Low Competition / Niche (under 50K) — Use 3-5 per post
#austinfitcoach #veganathlete ...

### Branded (create for client)
#[brandname] #[brandname]tips #[brandname]community

### Trending (rotate weekly)
[Research current trending hashtags in niche]
```

## 质量检查标准：
- 每条帖子的字符长度符合平台要求
- 日历中各类内容的比例符合40/25/20/15的比例
- 每周都包含所有预设的内容主题
- 没有两条连续的帖子属于同一类型
- 标签使用多样化（每条帖子的标签都不重复）
- 每条帖子都包含明确的行动号召（CTA）
- 周末的帖子内容更轻松、更具个人风格
- CSV文件格式正确，便于导入到 Buffer/Hootsuite 等平台
- 图片素材具有明确的用途，确保视觉效果的一致性