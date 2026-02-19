---
name: twitter-thread-creation
description: "**使用钩子推文（hook tweets）撰写Twitter/X线程：线程结构与互动优化指南**  
本指南涵盖了推文格式、字符限制、媒体附件以及发布策略等内容，适用于Twitter线程、X平台帖子、推文风暴（tweet storms）的创作。  
**主要内容：**  
- 推文格式与规范  
- 字符长度限制  
- 媒体附件的使用  
- 发布策略  
- 如何创建有效的Twitter/X线程  
- 提高用户互动（增加点赞、评论和分享）的方法  
**适用场景：**  
- Twitter线程（Twitter Threads）  
- X平台帖子（X Posts）  
- 推文风暴（Tweet Storms）  
- 社交媒体内容创作  
**关键词：**  
- Twitter线程（Twitter Threads）  
- X平台帖子（X Posts）  
- 推文风暴（Tweet Storms）  
- 推文格式（Tweet Formatting）  
- 线程结构（Thread Structure）  
- 用户互动（User Interaction）  
- 媒体附件（Media Attachments）  
- 发布策略（Publishing Strategies）  
**推荐阅读：**  
- [Twitter官方文档](https://docs.twitter.com/en/v16/user/tweets/threads)  
- [X平台官方文档](https://docs.x.com/en/latest/social-media/threads)  
**使用提示：**  
- 请确保遵循平台的相关规则和指南。  
- 适当使用钩子推文（hook tweets）来增加帖子的吸引力和互动性。  
- 根据目标受众调整推文内容和风格。  
**适用人群：**  
- 社交媒体内容创作者  
- 营销人员  
- 自媒体博主  
**注意事项：**  
- 本指南仅供参考，具体操作可能因平台更新而有所变化。  
- 如需最新信息，请随时查阅官方文档。"
allowed-tools: Bash(infsh *)
---
# 在 Twitter/X 上创建高互动性的帖子和话题

通过 [inference.sh](https://inference.sh) 命令行工具来创建高互动性的 Twitter/X 帖子和话题。

## 快速入门

```bash
curl -fsSL https://cli.inference.sh | sh && infsh login

# Post a tweet
infsh app run x/post-create --input '{
  "text": "I analyzed 1,000 landing pages.\n\n90% make the same 5 mistakes.\n\nHere are the fixes (with examples):\n\n🧵👇"
}'
```

> **安装说明：** [安装脚本](https://cli.inference.sh) 仅会检测您的操作系统和架构，然后从 `dist.inference.sh` 下载相应的二进制文件，并验证其 SHA-256 校验和。无需提升权限或启动后台进程。也可以通过 [手动安装与验证](https://dist.inference.sh/cli/checksums.txt) 来完成安装。

## 字符限制

| 元素 | 限制 |
|---------|-------|
| 推文文本 | 280 个字符（免费账户），25,000 个字符（高级账户） |
| 话题长度 | 无限制（10-15 条推文为最佳） |
| 图片说明文字 | 1,000 个字符 |
| 引用推文 | 280 个字符 |
| 回复 | 280 个字符 |
| 显示名称 | 50 个字符 |

## 话题结构

### 基本构成

```
Tweet 1 (Hook):     Bold claim + "thread 🧵"
Tweet 2:            Context / why this matters
Tweet 3-9:          One point per tweet (numbered)
Tweet 10:           Summary or biggest takeaway
Tweet 11:           CTA (follow, retweet, bookmark)
```

### 第一条推文：吸引注意力的内容

这条推文可以独立存在于时间线上，但它必须能够独立吸引读者的兴趣，即使没有后续的话题内容也能发挥作用。

| 推文类型 | 模板 |
|-----------|----------|
| “我做了某事 + 结果” | “我分析了 1,000 个数据点。以下是我的发现：” |
| “[数量] 个[主题]的小贴士” | “[数量]个[主题]的小贴士，它们能[带来好处]：” |
| “与众不同的观点” | “一个不受欢迎的观点：[强调的观点]” |
| “故事开头” | “2019 年，我经历了[重大事件]。以下是详细经过：” |
| “操作指南” | “如何[达成目标]（分步骤说明）：” |
| “令人惊讶的事实” | “[看似错误的统计数据]。让我来解释一下：” |

```bash
# Post hook tweet
infsh app run x/post-create --input '{
  "text": "I spent 3 years building SaaS products.\n\nHere are 10 things I wish someone told me on day 1:\n\n🧵"
}'
```

### 后续推文（3-9 条）

| 规则 | 原因 |
|------|-----|
| 每条推文只包含一个主题 | 保持清晰度，便于转发 |
| 推文编号（1/、2/ 等） | 表示进度，便于引用 |
| 每条推文都应该独立成篇 | 人们更愿意分享单条推文 |
| 首先提出观点 | 不要隐藏重点 |
| 使用换行符 | 便于阅读 |
| 包含示例 | 从抽象到具体 |

```bash
# Content tweet with visual
infsh app run x/post-create --input '{
  "text": "3/ Your pricing page is the second most visited page on your site.\n\nBut most founders treat it as an afterthought.\n\nThe fix:\n→ Show 3 tiers (not 2, not 5)\n→ Highlight the middle one\n→ Annual toggle defaulted ON\n→ Feature comparison below"
}'
```

### 结尾推文

```bash
# CTA tweet
infsh app run x/post-create --input '{
  "text": "11/ That'\''s the full playbook.\n\nTL;DR:\n• Validate before building\n• Launch ugly, iterate fast\n• Pricing is positioning\n• Talk to users weekly\n\nIf this was useful:\n→ Retweet the first tweet\n→ Follow me @username for more\n→ Bookmark this thread"
}'
```

## 格式规则

### 推文格式

```
❌ Dense:
"If you want to grow on Twitter you need to post consistently and engage with your audience while also making sure your content provides value to your followers."

✅ Formatted:
"Want to grow on Twitter?

3 non-negotiable rules:

→ Post daily (consistency > quality)
→ Reply to 20 accounts bigger than you
→ Every tweet must teach OR entertain

No shortcuts."
```

### 列表符号的使用

| 符号 | 用途 |
|--------|---------|
| → | 表示步骤、动作或方向 |
| • | 项目符号列表 |
| — | 旁注或引用 |
| ✅ | 表示“应该做”的事项 |
| ❌ | 表示“不应该做”的事项 |
| 1/ 2/ 3/ | 用于编号推文 |

### 换行策略

### 换行符的运用

换行符有助于控制阅读节奏和强调重点。

## 话题中的媒体内容

### 何时添加图片

| 推文位置 | 图片类型 | 目的 |
|---------------|-----------|---------|
| 吸引注意力的推文（第一条） | 吸引眼球的图片 | 阻止用户继续向下滚动 |
| 关键内容 | 屏幕截图、示例 | 作为证据 |
| 总结 | 信息图 | 便于分享的总结内容 |

```bash
# Generate thread header image
infsh app run infsh/html-to-image --input '{
  "html": "<div style=\"width:1200px;height:675px;background:linear-gradient(135deg,#0f172a,#1e293b);display:flex;align-items:center;justify-content:center;padding:60px;font-family:system-ui;color:white;text-align:center\"><div><h1 style=\"font-size:48px;font-weight:900;line-height:1.2;margin:0\">10 SaaS Pricing Mistakes<br>That Cost You Revenue</h1><p style=\"font-size:22px;opacity:0.5;margin-top:20px\">A thread 🧵</p></div></div>"
}'

# Generate screenshots for evidence
infsh app run infsh/agent-browser --input '{
  "url": "https://example.com/pricing",
  "action": "screenshot"
}'
```

### 图片规格

| 格式 | 尺寸 | 最大文件大小 |
|--------|-----------|----------|
| 单张图片 | 推荐尺寸为 1200 x 675（16:9） | 最大 5 MB |
| 两张图片 | 每张 700 x 800 | 每张 5 MB |
| 四张图片 | 每张 600 x 600 | 每张 5 MB |
| GIF 图片 | 最大尺寸为 1280 x 1080 | 最大 15 MB |

## 话题类型

### 教育类话题

```
1/ [Topic] explained simply:
2/ What is [concept]?
3/ Why it matters
4-8/ Key principles (numbered)
9/ Common mistakes
10/ Resources
11/ CTA
```

### 故事/经历分享

```
1/ [Dramatic opener]
2/ Background/context
3-7/ Chronological events
8/ The turning point
9/ The lesson
10/ How to apply it
11/ CTA
```

### 信息整理/列表展示

```
1/ [Number] [things] every [audience] needs:
2-10/ One item per tweet with brief explanation
11/ CTA
```

### 分析与总结

```
1/ I analyzed [thing]. Here's what I found:
2/ The setup (what I looked at)
3-8/ Finding 1, 2, 3... with evidence
9/ The biggest surprise
10/ Takeaways
11/ CTA
```

## 提高互动性的策略

| 行动 | 时间 | 原因 |
|--------|--------|-----|
| 发布吸引注意力的推文 | 在受众的高活跃时段（当地时间上午 8-10 点、中午 12-2 点） | 最大化初始曝光率 |
| 通过回复串联话题 | 在发布吸引注意力的推文后立即回复 | 完成整个话题的构建 |
| 固定话题链接 | 发布后立即固定链接 | 让访客能够看到你的最佳内容 |
| 与回复互动 | 在发布后的前 60 分钟内 | 提高算法推荐度 |
| 引用推文 | 第二天 | 提高第二波曝光率 |
| 重新发布吸引注意力的推文 | 1-2 周后 | 吸引新粉丝 |

## 将其他内容转化为话题形式

```bash
# Research source material
infsh app run tavily/search-assistant --input '{
  "query": "latest statistics on remote work productivity 2024"
}'

# Generate visual for the thread
infsh app run infsh/html-to-image --input '{
  "html": "<div style=\"width:1200px;height:675px;background:#0f172a;display:flex;align-items:center;padding:60px;font-family:system-ui;color:white\"><div><p style=\"font-size:20px;color:#38bdf8;text-transform:uppercase;letter-spacing:2px\">Data Deep Dive</p><h1 style=\"font-size:52px;font-weight:900;margin:12px 0;line-height:1.2\">Remote Work in 2024:<br>What the Data Actually Says</h1></div></div>"
}'
```

## 常见错误

| 错误 | 问题 | 解决方法 |
|---------|---------|-----|
| 吸引注意力的推文不够有力 | 话题在第一条推文后就结束了 | 使用引人好奇的标题和具体内容 |
| 推文太多（超过 20 条） | 读者在阅读 10-12 条后就会失去兴趣 | 最佳数量为 8-12 条 |
| 每条推文包含多个主题 | 令人困惑，不易转发 | 每条推文只讨论一个主题 |
| 推文中没有编号 | 难以跟随，缺乏进度感 | 必须使用编号（1/、2/、3/） |
| 没有图片 | 有图片的话题互动性更高 | 在吸引注意力的推文和关键内容中添加图片 |
| 只发布话题内容（没有独立推文） | 错过了非话题内容的受众 | 也要发布独立的推文 |
| 结尾没有行动号召 | 错失了增加关注和互动的机会 | 始终要求读者转发、关注或收藏 |
| 发布时间不当 | 在受众的低活跃时段发布 | 在受众的高活跃时段发布 |
| 推文内容过于冗长 | 人们不会阅读冗长的推文 | 使用换行符、符号和简短句子 |

## 相关技能

```bash
npx skills add inference-sh/skills@linkedin-content
npx skills add inference-sh/skills@content-repurposing
npx skills add inference-sh/skills@social-media-carousel
```

查看所有可用工具：`infsh app list`