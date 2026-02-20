---
name: product-hunt-launch
description: "**产品发布优化方案：具体规格、时间安排与图片展示策略**  
本方案涵盖了产品发布的核心要素，包括宣传口号、产品图片、创作者评论以及发布当天的具体执行策略。适用于以下场景：产品发布、初创企业产品发布、副业项目推广等。  
**触发条件：**  
- 产品发布活动（Product Hunt）  
- 新产品发布（Product Launch）  
- 产品发布策略（Launch Strategy）  
- 初创企业产品发布（Startup Launch）  
**主要内容：**  
1. **宣传口号（Taglines）**：精心设计吸引人的宣传口号，提升产品知名度。  
2. **产品图片（Gallery Images）**：高质量的产品图片有助于用户直观了解产品特性。  
3. **创作者评论（Maker Comments）**：邀请产品开发者或相关专家撰写评论，增加用户信任度。  
4. **发布当天策略（Launch Day Tactics）**：制定详细的发布当天执行计划，确保活动顺利进行。  
**适用场景：**  
- 产品发布（Product Launch）  
- 初创企业产品发布（Startup Launch）  
- 产品发布优化（Product Launch Optimization）  
- 产品发布活动（Product Hunt）  
**相关术语解释：**  
- Product Hunt：一种在线产品发现与推广活动。  
- Startup Launch：初创企业的产品发布活动。  
- Launch Strategy：产品发布的整体规划与执行方案。"
allowed-tools: Bash(infsh *)
---
# 产品发布攻略

通过 [inference.sh](https://inference.sh) 命令行工具，利用研究和视觉元素来优化你的产品发布。

## 快速入门

```bash
curl -fsSL https://cli.inference.sh | sh && infsh login

# Generate gallery hero image
infsh app run falai/flux-dev-lora --input '{
  "prompt": "clean product showcase, modern SaaS dashboard interface on laptop screen, floating UI elements around it, soft gradient background from blue to purple, professional marketing hero shot, minimal clean design",
  "width": 1248,
  "height": 832
}'

# Research competitor launches
infsh app run tavily/search-assistant --input '{
  "query": "Product Hunt top launches this week SaaS tools"
}'
```

> **安装说明：** [安装脚本](https://cli.inference.sh) 仅会检测你的操作系统和架构，然后从 `dist.inference.sh` 下载相应的二进制文件，并验证其 SHA-256 校验和。无需特殊权限或后台进程。也可以[手动安装并验证](https://dist.inference.sh/cli/checksums.txt)。

## 产品信息规范

| 项目名称 | 规范 | 备注 |
|---------|------|-------|
| 产品名称 | — | 简短易记 |
| 标语 | **限制在60个字符以内** | 末尾不要加句号 |
| 产品描述 | 预览中显示前260个字符 | 完整描述可以更长 |
| 图库图片 | 最多8张图片 | 建议使用1270 x 760像素的图片 |
| 关键主题 | 最多3个 | 选择最相关的主题 |
| 制作者 | 标记所有团队成员 | 他们可以参与评论 |
| 链接 | 产品网址 | 点赞者会通过此链接访问产品 |

## 图库图片

### 第一张图片至关重要

第一张图库图片会显示在信息流、邮件摘要和社交媒体分享中。它就是你的第一印象。

| 位置 | 内容 | 目标 |
|----------|---------|------|
| **1（首页图片）** | 产品实际使用场景，核心价值一目了然 | 让用户停下滚动，了解产品的功能 |
| **2** | 关键功能演示 | 展示产品的“惊喜时刻” |
| **3** | 使用前后的对比或问题/解决方案 | 展示产品的改变 |
| **4** | 社交证明或数据指标 | 增强产品的可信度 |
| **5** | 技术优势或集成情况 | 供评估者参考 |

### 图片尺寸

- 建议尺寸：**1270 x 760像素**（约16:9比例）
- 最小宽度：600像素 |
- 支持使用GIF格式的动画演示

### 生成图库图片

```bash
# Image 1: Hero product shot
infsh app run falai/flux-dev-lora --input '{
  "prompt": "modern SaaS product showcase, clean dashboard interface floating above gradient background, UI showing analytics charts and metrics, professional product marketing style, soft shadows, blue and white color scheme, wide format",
  "width": 1248,
  "height": 832
}'

# Image 2: Feature demo
infsh app run falai/flux-dev-lora --input '{
  "prompt": "product feature showcase, split screen showing drag-and-drop interface on left and generated output on right, clean UI design, modern SaaS aesthetic, subtle grid background, professional marketing",
  "width": 1248,
  "height": 832
}'

# Image 3: Before/after
infsh app run infsh/stitch-images --input '{
  "images": ["before-state.png", "after-state.png"],
  "direction": "horizontal"
}'

# Image 4: Social proof / metrics
infsh app run falai/flux-dev-lora --input '{
  "prompt": "clean infographic style image showing upward growth metrics, large numbers and charts on dark background, professional data visualization, startup metrics dashboard style, modern minimal design",
  "width": 1248,
  "height": 832
}'
```

## 标语

60个字符，不要加句号。必须清楚地传达产品的功能以及用户为何应该关注它。

### 有效的标语编写公式

| 公式 | 例子 |
|---------|---------|
| [目标受众]的[功能] | “专为开发者设计的AI写作助手” |
| [无需额外努力的][结果] | “无需设计技能即可生成美观的文档” |
| [工具]带来的[好处] | “自解释式的分析工具” |
| [形容词] + [类别] | “即时客户反馈调查工具” |
| [特定领域的][工具] | “数据可视化的Figma替代品” |

### 例子

```
❌ "The best project management tool ever created" (superlative, 52 chars)
❌ "We help you manage projects better." (vague, has period, 37 chars)
❌ "AI-powered machine learning project management SaaS" (buzzword soup)

✅ "Ship docs in minutes, not days" (31 chars)
✅ "AI turns your data into stories" (32 chars)
✅ "The open-source Calendly alternative" (37 chars)
```

## 发布时机

### 何时发布

| 因素 | 建议 |
|--------|----------------|
| 发布日 | **周二、周三或周四**（流量最高） |
| 时间 | **太平洋时间凌晨12:01**（产品发布日的开始时间） |
| 避免 | 周末、节假日，以及苹果/谷歌的重大活动期间 |
| 发布时长 | 产品发布日从太平洋时间午夜持续到午夜 |

### 为什么选择太平洋时间凌晨12:01？

- 可以在当天获得最长的展示时间 |
- 全天都能积累点赞 |
- 美国时间的早间邮件摘要会包含你的产品信息 |
- 能够覆盖所有美国时区用户

## 制作者评论

产品发布后**5分钟内**必须发布评论。这是你的产品介绍机会。

### 发布结构

```
Hey Product Hunt! 👋

[1 sentence: what it is]

[2-3 sentences: why you built it / the problem you noticed]

[1-2 sentences: how it works / key differentiator]

[1 sentence: what's next / what you're looking for]

Would love to hear your thoughts — happy to answer any questions!
```

### 例子

```
Hey Product Hunt!

DataFlow turns raw SQL queries into visual dashboards in seconds.

As a data engineer, I was frustrated spending more time formatting
reports than actually analyzing data. Every BI tool I tried required
a PhD in their configuration. So I built DataFlow — paste your SQL,
get a dashboard.

It auto-detects chart types, handles large datasets, and exports
to PDF/PNG with one click.

We're offering 50% off the first year for PH users. Would love
your feedback — what reporting pain points do you have?
```

## 发布日流程

### 发布前（1-2周）

- [ ] 图库图片最终确定（建议5张）
- [ ] 与5人以上测试标语（他们是否理解其含义？）
- [ ] 起草并校对制作者评论 |
- [ ] 准备好带有产品徽章的登录页面 |
- [ ] 准备好早期支持者名单（希望尝试产品的人） |
- [ ] 起草社交媒体公告内容

### 发布日时间表

| 时间（太平洋时间） | 行动 |
|-----------|--------|
| 凌晨12:01 | 产品上线，立即发布制作者评论 |
| 凌晨12:15 | 在个人社交媒体上分享 |
| 上午6:00 | 首次检查用户互动——回复所有评论 |
| 上午9:00 | 在相关社区分享（自然发布，避免刷屏） |
| 中午12:00 | 下午再次检查——回复所有新评论 |
| 下午3:00 | 分享任何早期反馈或有趣的内容 |
| 下午6:00 | 晚间互动——回复剩余的评论 |
| 晚上11:59 | 发布日结束——结果确定 |

### 互动规则

- **回复每条评论**——积极参与的制作者会获得更多关注 |
- **提出问题**——引发讨论 |
- **真诚交流**——避免使用模板化回复 |
- **切勿请求点赞**——违反产品发布规则 |
- **自然分享链接**——使用“请访问[链接]”而非“请点赞”

## 发布前的准备工作

```bash
# Study similar product launches
infsh app run tavily/search-assistant --input '{
  "query": "Product Hunt top launches analytics tools best practices"
}'

# Competitive landscape
infsh app run exa/search --input '{
  "query": "Product Hunt analytics dashboard tools launched 2024 2025"
}'

# Community sentiment
infsh app run tavily/search-assistant --input '{
  "query": "Product Hunt launch tips what works 2024 maker advice"
}'
```

## 发布后的行动

| 时间 | 行动 |
|------|--------|
| 第1-3天 | 回复所有剩余评论，感谢支持者 |
| 第1周 | 发布“经验分享”博客文章/推特帖子 |
| 第2周 | 联系评论中感兴趣的用户 |
| 第1个月 | 查看是否有资格获得“本周/本月最佳产品”称号 |

## 常见错误

| 错误 | 问题 | 解决方法 |
|---------|---------|-----|
| 在周五/周末发布 | 流量低，发布效果不佳 | 仅在工作日（周二至周四）发布 |
| 在中午发布 | 一半时间已经过去 | 选择太平洋时间凌晨12:01发布 |
| 未发布制作者评论 | 产品看起来被遗弃 | 发布后5分钟内必须发布评论 |
| 请求点赞 | 违反服务条款，可能被标记 | 自然分享，让产品本身说话 |
| 图库图片普通 | 无法展示产品实际效果 | 使用真实的用户界面和功能 |
| 不回复评论 | 互动率低 | 回复每一条评论 |
| 主题过多 | 降低产品曝光度 | 最多选择3个相关主题 |
| 使用流行词作为标语 | 用户不明白产品功能 | 使用清晰、具体且突出优势的标语 |

## 相关技能

```bash
npx skills add inference-sh/skills@ai-image-generation
npx skills add inference-sh/skills@web-search
npx skills add inference-sh/skills@prompt-engineering
```

浏览所有应用：`infsh app list`