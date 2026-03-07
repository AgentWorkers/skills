---
name: seo-content-pro
description: 具备多语言支持、内容更新功能、SEO评分系统以及竞争对手分析能力的高级SEO内容创作工具。非常适合内容创作者和营销机构使用。
author: fly3094
version: 1.0.0
tags: [seo, content, writing, article, blog, marketing, multi-language, research]
metadata:
  clawdbot:
    emoji: 📝
    requires:
      bins:
        - python3
        - curl
    config:
      env:
        CONTENT_TONE:
          description: Default tone (professional|casual|technical|friendly)
          default: "professional"
          required: false
        DEFAULT_LENGTH:
          description: Default word count
          default: "2000"
          required: false
        CONTENT_LANGUAGE:
          description: Target language (en|zh|es|fr|de|ja)
          default: "en"
          required: false
        SEARXNG_URL:
          description: SearXNG instance for privacy-respecting research
          default: "http://localhost:8080"
          required: false
---
# SEO Content Pro 📝

这是一项高级的SEO内容创作工具，支持多语言处理、内容更新以及基于AI的优化功能。

## 主要功能

- 🔍 **主题研究**：使用SearXNG（尊重用户隐私的搜索引擎）分析高排名内容。
- 📋 **大纲生成**：生成符合SEO规范的文章结构。
- ✍️ **初稿撰写**：撰写1500至3000字的文章，并使用恰当的标题层级。
- 🎯 **关键词整合**：推荐并整合主要/次要关键词。
- 📊 **竞争对手分析**：识别内容缺口与排名前十的页面之间的差异。
- 🌐 **多语言支持**：支持英语、中文、西班牙语、法语、德语、日语。
- 🔄 **内容更新**：用新数据和见解更新旧文章。
- 📈 **SEO评分**：提供内容质量评分（0-100分），并给出改进建议。

## 安装

```bash
clawhub install seo-content-pro
```

## 命令

### 研究主题
```
Research "[keyword/topic]" for SEO content
```

### 生成大纲
```
Create outline for "[article title]" targeting "[primary keyword]"
```

### 撰写初稿
```
Write draft for "[article title]" using outline, 2000 words, tone: professional
```

### 完整工作流程
```
Create SEO article about "[topic]" - research, outline, and draft (2500 words)
```

### 内容更新
```
Update and improve this article with latest data and SEO best practices
```

### SEO分析
```
Analyze this content and provide SEO score with improvement suggestions
```

### 多语言支持
```
Create SEO article about "[topic]" in Chinese, 2000 words
```

## 配置

### 环境变量
```bash
# Default content tone
export CONTENT_TONE="professional"  # professional|casual|technical|friendly

# Default word count
export DEFAULT_LENGTH="2000"

# Include FAQ section
export INCLUDE_FAQ="true"  # true|false

# Target language
export CONTENT_LANGUAGE="en"  # en|zh|es|fr|de|ja

# SearXNG instance (for privacy-respecting research)
export SEARXNG_URL="http://localhost:8080"
```

### OpenClaw配置
```json
{
  "env": {
    "CONTENT_TONE": "professional",
    "DEFAULT_LENGTH": "2000",
    "INCLUDE_FAQ": "true",
    "CONTENT_LANGUAGE": "en"
  }
}
```

## 输出格式

每篇文章包含以下内容：

- **元标题**（50-60个字符）
- **元描述**（150-160个字符）
- **H1标题**（吸引读者的标题，包含主要关键词）
- **引言**（150-200字，吸引读者兴趣）
- **H2/H3段落**（使用恰当的层级结构，优化关键词）
- **结论及下一步行动建议**（明确下一步该做什么）
- **内部/外部链接建议**
- **常见问题解答**（3-5个问题及答案）
- **SEO评分**（0-100分，包含详细评分依据）

## 使用示例

### 基本文章示例
```
User: Create SEO article about "best AI automation tools for small business" - 2500 words

Assistant: 
1. 🔍 Researching top 10 ranking pages...
2. 📊 Analyzing content gaps and keyword opportunities...
3. 📋 Generating optimized outline...
4. ✍️ Writing 2500-word draft with H2/H3 structure...
5. 📈 Calculating SEO score and suggestions...

✅ Article ready! SEO Score: 87/100
```

### 多语言支持示例
```
User: Create SEO article about "remote work productivity" in Chinese, 2000 words

Assistant:
Generating Chinese content for "远程工作效率"...
✅ 文章完成！SEO 分数：85/100
```

### 内容更新示例
```
User: [paste old article]
Update this article with 2026 data and improve SEO

Assistant:
1. Analyzing current content...
2. Researching latest data and statistics...
3. Identifying SEO improvements...
4. Updating with fresh insights...

✅ Refreshed! SEO Score improved from 62 to 89 (+27 points)
```

## SEO评分构成

您的内容评分依据以下因素：

| 评分因素 | 权重 | 说明 |
|--------|--------|-------------|
| 关键词使用 | 20% | 主要/次要关键词的放置位置 |
| 内容长度 | 15% | 适合该主题的最佳字数 |
| 可读性 | 15% | Flesch readability评分，句子结构 |
| 标题层级 | 15% | 正确的H1/H2/H3层级结构 |
| 元标签 | 10% | 标题和描述的优化 |
| 内部链接 | 10% | 建议的内部链接 |
| 外部链接 | 10% | 高质量的外部引用 |
| 常见问题解答 | 5% | 全面的常见问题解答 |

## 与其他工具的集成

### social-media-automator
```
1. Create SEO article with seo-content-pro
2. Generate social posts with social-media-automator
3. Schedule and publish across platforms
```

### rss-to-social
```
1. Monitor industry RSS feeds with rss-to-social
2. Identify trending topics
3. Create content with seo-content-pro
4. Auto-publish to social media
```

实现完整的内容自动化流程！🔄

## 使用场景

### 内容营销人员
- 将内容生成量提高5-10倍。
- 保持内容质量的一致性。
- 高效地针对多个关键词进行优化。

### SEO机构
- 以白标形式提供内容创作服务。
- 用同一团队服务更多客户。
- 统一所有作者的内容质量。

### 独立创业者
- 无需雇佣员工即可创建专业内容。
- 每月节省500-2000美元的写作成本。
- 专注于业务发展，而非内容创作。

### 多语言企业
- 为不同市场本地化内容。
- 在多种语言中保持品牌一致性。
- 以统一的质量实现全球扩展。

## 优化效果的技巧

1. **提供背景信息**：向目标受众说明该工具的用途和目标。
2. **指定语气**：与您的品牌风格相匹配（专业、随意或技术性）。
3. **提供示例**：分享您喜欢的文章作为风格参考。
4. **审核与编辑**：AI生成的初稿只是一个起点——加入您的专业意见。
5. **定期更新**：每季度使用内容更新功能保持文章的时效性。
6. **瞄准长尾关键词**：更具体的关键词更容易获得排名。

## 价格方案

该工具为LobsterLabs的内容服务提供支持：

| 服务 | 价格 | 交付时间 |
|---------|-------|----------|
| 单篇文章 | $300-500 | 3-5天 |
| 月度套餐（4篇文章） | $1,500-2,500 | 每月 |
| 白标代理服务 | $3,000+/月 | 无限篇数 |
| 内容+社交媒体服务包 | $2,000-4,000/月 | 全方位服务 |

**投资回报率示例：**
- 成本：每月$2,000（4篇文章+社交媒体服务）
- 客户通过内容获得的收入：每月$10,000-50,000
- 投资回报率：5-25倍

联系方式：PayPal 492227637@qq.com

## 常见问题解答

### SEO评分较低
- 检查关键词密度（主要关键词的密度应为1-2%）。
- 增加H2/H3子标题的数量。
- 如果文章字数少于1500字，请延长文章长度。
- 如果缺少常见问题解答部分，请添加该部分。

### 研究相关问题
- 确保SearXNG正在运行。
- 检查网络连接。
- 尝试使用其他搜索词。

### 语言质量
- 在命令中明确指定所需语言。
- 为了获得最佳效果，请使用目标语言。
- 审查并调整文化相关的内容。

## 更新日志

### 1.0.0（2026-03-07）
- 初始版本发布
- 支持多语言（6种语言）
- 添加内容更新功能
- SEO评分系统
- 竞争对手分析功能
- 与social-media-automator和rss-to-social的集成