---
name: content-recycler
description: 将内容转换并重新用于多个平台，包括 Twitter、LinkedIn、Facebook、Instagram、TikTok 和电子邮件。在将长篇内容适配到社交媒体时使用该工具，创建针对特定平台的内容版本，制定内容发布计划，或在各个渠道之间保持信息传递的一致性。
---

# 内容回收器 (Content Recycler)

## 概述

将现有内容转换为适用于多个平台的优化版本，同时保持品牌语言和信息的一致性。将一篇博客文章转化为适合一周使用的社交媒体内容、新闻通讯内容以及跨平台互动素材。

## 核心功能

### 1. 长篇内容转换为微内容

**将博客文章转换为：**
- Twitter/X 的推文（每条推文限制 280 个字符）
- LinkedIn 的帖子（专业风格，字符数经过优化）
- Facebook 的帖子（对话式，以社区为中心）
- Instagram 的描述（包含大量表情符号，适合使用标签）
- TikTok/YouTube Short 的脚本（60-90 秒）
- 电子邮件新闻通讯的摘要

**示例请求：**
“将这篇关于‘10 个提高效率的技巧’的 2000 字博客文章转换为：(1) 一条 Twitter 推文，(2) 一条 LinkedIn 帖子，(3) 一条 Facebook 帖子，(4) 一条 Instagram 描述，(5) 一段 TikTok 脚本，以及 (6) 一封电子邮件预告。”

### 2. 平台特定优化

**针对每个平台的独特特性进行优化：**

**Twitter/X：**
- 每条推文字符限制：280 个
- 使用分页结构展示较长内容
- 每条推文使用 1-3 个标签
- 语气：对话式，简洁明了，注重价值传递

**LinkedIn：**
- 字符限制：3,000 个
- 专业但对话式的语气
- 数据和统计信息效果显著
- 战略性地使用换行和表情符号

**Facebook：**
- 字符限制：63,206 个
- 对话式，以社区为导向
- 提出问题以促进互动
- 包含图片/视频

**Instagram：**
- 字符限制：2,200 个
- 大量使用表情符号
- 使用 5-30 个标签（最佳：11 个）
- 注重视觉格式和换行

**TikTok/Reels：**
- 脚本时长：60-90 秒（150-250 字）
- 在前 3 秒内吸引观众注意力
- 明确的呼吁行动（CTA）

### 3. 内容日历生成

**将单一内容转化为多天的发布计划：**

以一篇综合性的内容（博客、视频、指南等）为基础，生成一个内容日历，包括：
- 第 1 天：预告（Twitter、Instagram Story）
- 第 2 天：主要内容发布（LinkedIn、Facebook）
- 第 3 天：后续推文（Twitter/X）
- 第 4 天：幕后花絮（Instagram、TikTok）
- 第 5 天：问答或投票（Facebook、Instagram）
- 第 6 天：总结/统计数据（LinkedIn）
- 第 7 天：呼吁行动/下一步行动（电子邮件新闻通讯）

**示例请求：**
“根据这篇关于‘远程工作技巧’的博客文章，生成一个为期 7 天的内容日历，每天发布相应的内容到 Twitter、LinkedIn、Instagram 和 Facebook。”

### 4. SEO 与标签优化

**生成适合每个平台的标签：**

- **LinkedIn：** 在内容中添加标签，以及行业相关的专业标签
- **Instagram：** 5-30 个标签（结合高、中、低活跃度的标签）
- **Twitter：** 每条推文使用 1-3 个标签
- **Facebook：** 使用较少的标签，更注重对话式表达
- **TikTok：** 使用热门音乐或挑战标签

## 快速入门

### 将博客内容转换为所有平台

```python
# Use scripts/recycle_content.py
python3 scripts/recycle_content.py \
  --input blog_post.md \
  --output-dir ./output \
  --platforms twitter,linkedin,facebook,instagram,tiktok,email \
  --format all
```

### 创建 Twitter 推文

```python
# Use scripts/to_twitter_thread.py
python3 scripts/to_twitter_thread.py \
  --input article.md \
  --max-tweets 10 \
  --hashtags 2 \
  --tone conversational
```

### 生成内容日历

```python
# Use scripts/generate_calendar.py
python3 scripts/generate_calendar.py \
  --input content.md \
  --days 7 \
  --platforms twitter,linkedin,facebook,instagram \
  --output calendar.md
```

## 脚本

### `recycle_content.py`
将内容转换为多个平台适用的形式。

**参数：**
- `--input`：输入文件路径（必需）
- `--output-dir`：输出目录（默认：./output）
- `--platforms`：用逗号分隔的平台（twitter,linkedin,facebook,instagram,tiktok,email）
- `--format`：输出格式（all,threads,posts,captions,scripts）
- `--tone`：语气偏好（professional,conversational,playful）
- `--include-hashtags`：是否包含标签建议（true/false）
- `--cta`：是否包含呼吁行动（Call-to-Action）

**示例：**
```bash
python3 scripts/recycle_content.py \
  --input blog_post.md \
  --output-dir ./output \
  --platforms twitter,linkedin,instagram \
  --tone professional \
  --include-hashtags \
  --cta "Read the full article at link in bio"
```

### `to_twitter_thread.py`
将长篇内容转换为 Twitter/X 推文。

**参数：**
- `--input`：输入文件路径
- `--max-tweets`：每条推文的最大数量（默认：10）
- `--hashtags`：每条推文使用的标签数量（默认：2）
- `--tone`：语气偏好（默认：对话式）
- `--include-cta`：是否在最后一条推文中包含呼吁行动

**示例：**
```bash
python3 scripts/to_twitter_thread.py \
  --input article.md \
  --max-tweets 8 \
  --hashtags 3 \
  --tone conversational \
  --include-cta
```

### `to_linkedin_post.py`
根据内容创建适合 LinkedIn 的帖子。

**参数：**
- `--input`：输入文件路径
- `--max-length`：最大字符长度（默认：3000）
- `--tone`：语气（专业、对话式、鼓舞人心）
- `--include-stats`：是否包含统计数据
- `--formatting`：是否使用加粗字体、换行（true/false）

**示例：**
```bash
python3 scripts/to_linkedin_post.py \
  --input article.md \
  --tone professional \
  --include-stats \
  --formatting
```

### `generate_calendar.py**
根据源内容生成多天的内容日历。

**参数：**
- `--input`：输入文件路径
- `--days`：天数（默认：7）
- `--platforms`：用逗号分隔的平台
- `--output`：输出文件
- `--theme`：每日主题（预告、发布、后续、幕后花絮、问答、总结、呼吁行动）

**示例：**
```bash
python3 scripts/generate_calendar.py \
  --input content.md \
  --days 7 \
  --platforms twitter,linkedin,facebook,instagram \
  --output calendar.md
```

### `optimize_hashtags.py`
生成适合每个平台的标签。

**参数：**
- `--input`：输入内容或主题
- `--platforms`：目标平台（instagram,linkedin,twitter,facebook,tiktok）
- `--count`：每个平台使用的标签数量
- `--niche`：行业/领域（科技、营销、金融等）

**示例：**
```bash
python3 scripts/optimize_hashtags.py \
  --input "AI in marketing automation" \
  --platforms instagram,linkedin,twitter \
  --count 15 \
  --niche marketing
```

## 内容优化指南

### Twitter/X 的最佳实践

1. **立即吸引注意力** - 第一条推文最为重要
2. **为推文编号** - 如 1/10, 2/10 等
3. **以呼吁行动结尾** - 跟随、点赞、分享、链接
4. **使用换行** - 每 2-3 句换一行
5. **添加相关图片** - 在推文之间插入图片

**示例推文结构：**
```
Tweet 1: Hook + what you'll learn + (1/X)
Tweet 2-8: Main points (one key insight per tweet)
Tweet 9: Bonus tip/counterintuitive point
Tweet 10: Summary + CTA + hashtags
```

### LinkedIn 的最佳实践

1. **第一行很关键** - 使用 3 行的吸引语句，并适当留白
2. **使用换行** - 每 1-2 句换一行
3. **策略性地使用表情符号** - 每段文字使用 1-2 个表情符号
4. **包含数据/统计信息** - 数字信息效果显著
5. **以问题结尾** - 促进评论
6. **@相关人士** - 最多 @3-5 个人

**格式模板：**
```
[Hook - 3 lines]

[White space]

[Key insight with data point]

[Personal story/example]

[Another key insight]

[Call to action or question]

#hashtags
```

### Instagram 的最佳实践

1. **在第一行吸引注意力** - 让用户不想滚动页面
2. **使用换行** - 每 1-2 句换一行
3. **频繁使用表情符号** - 但不要过度
4. **标签策略**：
   - 5-10 个高活跃度标签
   - 5-10 个中等活跃度标签
   - 5-10 个低活跃度标签
5. **以呼吁行动结尾** - 在个人资料中添加链接，或保存、分享内容

**描述模板：**
```
[Hook - 2-3 lines with emojis]

[White space]

[Value/content]

[Another paragraph]

[CTA]

[Hashtags block]
```

### Facebook 的最佳实践

1. **提出问题** - 促进互动
2. **使用“你”这样的称呼** - 建立个人联系
3. **包含媒体** - 图片或视频
4. **保持对话式** - 不要过于宣传
5. **回复评论** - 提高算法排名

### TikTok 脚本

1. **在 3 秒内吸引观众** - 强调价值主张
2. **保持简洁** - 时长 60-90 秒
3. **使用热门元素** - 音乐、音效、格式
4. **明确呼吁行动** - 在个人资料中添加链接
5. **文字叠加** - 在屏幕上显示关键信息

**脚本结构：**
```
0-3s: Hook
3-45s: Main content (3-5 points)
45-55s: Call to action
55-60s: Outro
```

## 语气指南

### 专业风格
- LinkedIn、电子邮件新闻通讯：
- 以数据为基础，具有权威性
- 使用“我们发现...”、“研究表明...”等表达
- 避免使用俚语和过多的表情符号

### 对话式风格
- Twitter、Facebook：
- 使用个人化的语言，如“我发现...”等
- 每条帖子使用 1-2 个表情符号
- 语气轻松但注重价值传递

### 有趣风格
- Instagram、TikTok：
- 使用流行语言和表情符号
- 使用“这是一个秘密...”、“你猜怎么着？”等表达
- 适当使用表情包和幽默元素

## 自动化集成

### 周期性内容回收流程

```bash
# Weekly cron job - Sunday at 9 AM
0 9 * * 0 /path/to/content-recycler/scripts/recycle_content.py \
  --input ~/blog/posts/$(date +\%Y\%m\%d).md \
  --output-dir ~/content/calendar/$(date +\%Y\%m\%d) \
  --platforms all \
  --include-hashtags \
  --cta "Read more at blog.example.com"
```

### 自动发布到社交媒体

与社交媒体调度工具集成：
- Buffer
- Hootsuite
- Later
- SocialPilot

Content-Recycler 的输出可以直接通过 API 发送，或通过 CSV 文件上传。

## 最佳实践

### 1. 保持一致的品牌语言

- 在品牌指南中定义品牌语言规范
- 适应不同平台的语气，但保持信息的一致性
- 保持关键短语和使命宣言的一致性

### 2. 以平台为中心的思考

不要简单复制粘贴，而是根据以下因素进行优化：
- 字符限制
- 目标受众的期望
- 平台的格式要求
- 互动模式

### 3. 测试与迭代

- 跟踪互动数据
- 对不同版本进行 A/B 测试
- 了解每个平台的效果
- 根据效果优化模板

### 4. 发布时机很重要

- **Twitter：** 工作时间内的互动率较高
- **LinkedIn：** 最佳发布时间为周二至周四上午 8-10 点
- **Instagram：** 周末下午 7-9 点和中午 12-3 点
- **Facebook：** 工作日中午 1-4 点
- **TikTok：** 周末晚上 7-11 点

### 5. 视觉内容

- **Twitter：** 每 3 条推文使用 1 张图片
- **Instagram：** 每条帖子都需要图片或视频
- **LinkedIn：** 文档轮播效果良好
- **Facebook：** 需要图片或视频
- **TikTok：** 仅支持视频

---

**更聪明地工作，而不是更辛苦地工作。一篇内容，十个平台。**