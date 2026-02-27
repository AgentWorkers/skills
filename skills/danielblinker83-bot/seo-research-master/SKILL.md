---
name: seo-research-master
version: 1.0.0
description: 基于人工智能的SEO关键词研究、竞争对手分析以及针对任何细分市场的内容机会识别工具。能够准确找出目标受众搜索的关键词，评估其难度，并制定基于数据的SEO内容策略。
tags: [seo, keyword-research, competitor-analysis, content-strategy, marketing, search]
author: contentai-suite
license: MIT
---
# SEO研究大师 — 全方位关键词与内容策略

## 该技能的功能

本技能通过人工智能分析，指导您完成整个SEO研究流程。它能帮助您识别高潜力的关键词，分析竞争对手的市场定位，并制定优先级明确的内容计划，从而提升网站的有机流量。

## 使用方法

**输入格式：**
```
NICHE: [Your industry/specialty]
LOCATION: [City, Region, or "Global"]
MAIN SERVICES/PRODUCTS: [List 3-5 core offerings]
CURRENT WEBSITE: [URL if you have one, or "none"]
COMPETITORS: [2-3 competitor names or websites]
TARGET AUDIENCE: [Brief description]
GOAL: [Traffic / Leads / Brand awareness / Local visibility]
```

---

## 第一阶段：关键词发现

### 生成种子关键词

使用以下提示让AI生成种子关键词：
```
Generate 20 seed keywords for [NICHE] targeting [AUDIENCE] in [LOCATION].
Include: informational, commercial, navigational, and local keywords.
Format as a table with: keyword | intent | estimated monthly searches | competition level
```

### 需要覆盖的关键词类别

**信息型关键词**（用于博客内容）：
- “如何[解决您所在领域的具体问题]”
- “[您的核心服务/产品]是什么”
- “为什么[常见用户问题]”
- “[主题]技巧/指南/检查清单”

**商业型关键词**（用于服务/产品页面）：
- “[您的服务]在[地区]的最佳选择”
- “[您的服务]在我附近”
- “[您的服务]的价格/费用”
- “在[地区]雇佣[您的专业服务]”

**对比型关键词**（用于吸引潜在客户）：
- “[您的服务]与[替代方案]相比”
- “[您的服务]值得购买吗”
- “[您的服务]的优缺点”

**本地SEO关键词**（如服务基于地理位置）：
- “[服务][城市名称]”
- “[专业服务][社区名称]”
- “在我附近有[服务]”

---

## 第二阶段：关键词优先级矩阵

根据以下标准为每个关键词打分：

| 关键词 | 每月搜索量 | 难度（1-10） | 商业价值 | 优先级得分 |
|---------|---------------|-------------------|----------------|----------------|
| [关键词] | [预估搜索量] | [1-10] | [高/中/低] | [(搜索量×难度) × 商业价值] |

**优先级计算公式：**
- 高优先级 = 高搜索量 + 低难度 + 高商业价值
- 快速见效的关键词 = 中等搜索量 + 极低难度（新网站可优先选择）
- 长期目标关键词 = 高搜索量 + 高难度（先建立权威性）

---

## 第三阶段：竞争对手分析

### 竞争对手内容差距分析

针对每个竞争对手，识别其内容中的不足之处：
```
COMPETITOR: [Name/URL]
Their top ranking keywords: [list]
Content they rank for that you don't: [gap list]
Content you rank for that they don't: [your advantage]
Their weak spots (thin content, poor UX, missing topics): [list]
```

### 内容差距机会

AI会识别出竞争对手尚未充分覆盖的主题——这些是您快速提升排名机会的关键领域。

**使用提示：**
```
Analyze content gaps between [YOUR BRAND] and [COMPETITOR] in [NICHE].
List 10 topics that [COMPETITOR] ranks for but hasn't covered thoroughly.
These are opportunities to create better content and outrank them.
```

---

## 第四阶段：SEO内容计划

### 12个月内容规划结构

**第1-3个月：基础建设**
- 专注于长尾关键词、竞争较小的关键词以及用户意图明确的关键词
- 发布4篇针对信息型关键词的博客文章
- 优化2个服务/产品页面
- （如涉及本地服务）优化Google商业资料

**第4-6个月：建立权威性**
- 专注于核心主题中竞争程度适中的关键词
- 发布4篇包含内部链接的博客文章（链接指向第1-3个月的内容）
- 编写一篇2000字以上的综合指南（核心内容）
- （如服务覆盖多个地区）创建2个本地 landing page

**第7-12个月：竞争型关键词**
- 专注于搜索量高的关键词
- 在现有内容的基础上进一步提升权威性
- 用优质内容针对竞争对手的关键词进行链接建设（例如通过合作或撰写客座文章）

---

## 第五阶段：页面SEO优化检查清单

请确保所有内容都符合以下要求：

### 标题标签（50-60个字符）
- [ ] 关键词位于开头
- [ ] 品牌名称位于结尾（长关键词可选）
- 标题对人类读者有吸引力，同时符合搜索引擎的规则

### 元描述（150-160个字符）
- [ ] 包含关键词
- [ ] 清晰传达价值主张
- [ ] 包含行动号召（如“了解更多”、“获取免费报价”等）

### 内容结构
- [ ] H1标签包含关键词（每页仅使用一个H1标签）
- [ ] H2标签包含次要关键词或相关关键词
- [ ] 关键词出现在前100个单词内
- [ ] 关键词密度：1-2%（避免过度使用）
- [ ] 与网站内2-3个相关页面建立内部链接
- [ ] 添加1-2个权威外部链接

### 技术基础要求
- [ ] URL路径中包含关键词
- [ ] 图片alt文本自然地包含关键词
- [ ] 页面加载时间不超过3秒
- [ ] 适配移动设备

---

## 第六阶段：本地SEO策略（如服务基于地理位置）

### Google商业资料优化

**必备元素：**
1. 商业名称与注册名称一致
- 线上所有信息中保持名称、地址、电话的一致性
- 添加至少5个相关类别
- 每月更新5张以上图片
- 每周发布Google商业资料相关内容
- 在24小时内回复所有评论

### 本地引用建设

**优先推荐的引用平台：**
- Google商业资料（必备）
- Yelp（具有较高权威性的平台）
- 行业特定的本地目录
- 当地商会
- 当地新闻/博客的提及

---

## 跟踪与报告模板

### 月度SEO报告

```
PERIOD: [Month/Year]
TOP 5 RANKING KEYWORDS: [list with position]
NEW KEYWORDS RANKING: [list]
ORGANIC TRAFFIC: [sessions this month vs last month]
TOP PERFORMING PAGES: [list with traffic]
NEXT MONTH FOCUS: [2-3 priority actions]
```

**可免费使用的跟踪工具：**
- Google搜索控制台（用于监控排名和点击数据）
- Google Analytics 4（用于分析流量和用户行为）
- Google商业资料洞察（用于查看本地曝光情况）

---

## 与ContentAI Suite结合使用

本技能可与**[ContentAI Suite](https://contentai-suite.vercel.app)**无缝集成——这是一个免费的多工具营销平台。只需输入关键词，AI即可自动生成所有SEO相关内容。

→ **免费试用：** https://contentai-suite.vercel.app