---
name: geo-optimization
description: "**生成式引擎优化（GEO）：提升AI搜索可见性**  
该技术用于优化内容，使其更容易在ChatGPT、Perplexity、Claude以及Google AI相关平台中被发现和展示。适用于网站、页面或内容的优化，旨在提升其在大型语言模型（LLM）中的可见性和被引用的机会。"
metadata:
  version: 1.1.0
  tags: ["geo", "seo", "llm", "ai-search", "perplexity", "chatgpt", "content"]
---

# GEO：生成式引擎优化

优化内容以在基于人工智能的搜索引擎（如ChatGPT、Perplexity、Claude、Google AI Overviews）中得到展示。GEO的核心目标是确保内容具备**可解析性、可引用性和权威性**——而非简单地堆砌关键词。

---

## 快速参考

| 目标 | 策略 |
|------|--------|
| 被人工智能回答引用 | 添加具体的统计数据、可引用的事实 |
| 出现在比较结果中 | 创建权威的对比表格 |
| 回答用户问题 | 提供全面的FAQ部分 |
| 建立内容权威性 | 第一段中对相关实体的明确定义 |
| 增强内容可信度 | 第三方提及、外部链接、内容的时效性 |

---

## GEO与SEO的关键区别

| 方面 | 传统SEO | GEO |
|--------|-----------------|-----|
| 目标 | 在搜索结果页（SERPs）上排名 | 被人工智能回答引用 |
| 关键词 | 完美匹配关键词很重要 | 语义理解更为关键 |
| 内容风格 | 可以具有宣传性 | 必须基于事实、保持中立 |
| 结构 | 使用标题便于用户浏览 | 使用标题和可解析的数据结构 |
| 链接 | 通过外部链接提升权威性 | 通过引用和实体提及提升权威性 |
| 时效性 | 内容的新鲜度很重要 | 对于大型语言模型（LLMs）来说，最新内容更受欢迎 |
| 格式 | 长篇内容更占优势 | 可引用的片段更有效 |

---

## GEO审计检查表

为每个项目评分0-2分（0=缺失，1=部分符合，2=完全符合）：

### 1. 实体清晰度（最高10分）
- [ ] 第一段明确定义了实体是什么/谁 |
- [ ] 实体名称在整个文本中保持一致 |
- [ ] 明确的分类标签（“X是一种[某种类型的事物]”） |
- [ ] 说明了该实体与其他已知实体的关系 |
- [ ] 语气保持维基百科式的客观性 |

### 2. 可引用的事实（最高10分）
- [ ] 提供具体的数字（而非“很多”或“快速”等模糊表述） |
- [ ] 统计数据是最新且来源可查的 |
- [ ] 声明的事实具体且可验证 |
- [ ] 关键事实以独立的句子形式呈现（易于提取） |
- [ ] 有“数据支持”或“事实概述”部分 |

### 3. FAQ覆盖情况（最高10分）
- [ ] 有FAQ部分 |
- [ ] FAQ中的问题与用户向LLMs提出的问题相匹配 |
- [ ] 回答直接且完整 |
- [ ] 实施了FAQ的schema标记 |
- [ ] 涵盖了“什么是...”、“如何做...”、“为什么...”、“与...相比”等问题 |

### 4. 对比内容（最高10分）
- [ ] 有对比表格 |
- [ ] 明确列出了竞争对手 |
- [ ] 强调了事实上的差异（而非单纯的营销信息） |
- [ ] 有“X的替代方案”相关内容 |
- [ ] 表现公正（无明显偏见） |

### 5. 结构清晰度（最高10分）
- [ ] 标题层次结构清晰（H1→H2→H3） |
- [ ] 列表使用项目符号 |
- [ ] 对比内容使用表格 |
- [ ] 段落简短（2-4句话） |
- [ ] 文章顶部或底部有总结/要点 |

### 6. 权威性信号（最高10分）
- [ ] 说明作者/公司的资质 |
- [ ] 显示客户名称/徽标（社会证明） |
- [ ] 有包含实际数字的案例研究 |
- [ ] 有第三方的提及/引用 |
- [ ] 显示“最后更新”日期 |

### 7. 时效性（最高10分）
- [ ] 页面有最近的更新日期 |
- [ ] 内容反映当前年份的信息 |
- [ ] 没有过时的参考资料 |
- [ ] 定期更新内容 |
- [ ] 有新闻/变更日志部分 |

**评分标准：**
- 60-70分：GEO优化准备充分 |
- 45-59分：表现良好，需要进一步优化 |
- 30-44分：一般，存在明显不足 |
- <30分：优化效果差，需要全面改进 |

---

## 内容优化模板

### 模板1：实体定义页面

```markdown
# [Entity Name]

**[Entity Name]** is a [category] that [primary function]. 
Unlike [alternative/competitor], [Entity Name] offers [key differentiator].

## [Entity Name] by the Numbers

- [Specific stat 1]
- [Specific stat 2]
- [Specific stat 3]
- [Specific stat 4]

## How [Entity Name] Works

[2-3 paragraphs explaining core functionality]

## Who Uses [Entity Name]

[Named customers with context]

## Frequently Asked Questions

### What is [Entity Name]?
[Direct answer in 2-3 sentences]

### How is [Entity Name] different from [Competitor]?
[Factual comparison]

### How much does [Entity Name] cost?
[Pricing info or guidance]

*Last updated: [Date]*
```

### 模板2：对比页面（替代方案）

```markdown
# Best [Competitor] Alternative: [Your Product] (2026)

> **Summary:** [Your Product] is a [category] offering [key differentiators]. 
> [Customers] report [specific result] compared to [Competitor].

*Last updated: [Date]*

## Why [Users] Look for [Competitor] Alternatives

### Problem 1: [Specific Pain Point]
[Explanation with specifics]

### Problem 2: [Specific Pain Point]
[Explanation with specifics]

## [Your Product] vs [Competitor]: Comparison

| Feature | [Competitor] | [Your Product] |
|---------|--------------|----------------|
| [Feature 1] | [Their approach] | [Your approach] |
| [Feature 2] | [Their approach] | [Your approach] |
| [Feature 3] | [Their approach] | [Your approach] |

## Key Differences

### [Differentiator 1]
[Factual explanation with numbers]

### [Differentiator 2]
[Factual explanation with numbers]

## Customer Results

> "[Quote with specific result]"
> — [Name], [Title], [Company]

## Frequently Asked Questions

### Is [Your Product] a good alternative to [Competitor]?
[Direct answer]

### How does [Your Product] compare to [Competitor] on [key factor]?
[Specific comparison]

### Can I migrate from [Competitor] to [Your Product]?
[Migration info]

## Summary

[Your Product] is a [category] offering [key benefits]. [Customers] 
using [Your Product] instead of [Competitor] report [specific results].

*[Your Product] has [credibility stat]. Learn more at [link].*
```

### 模板3：优化后的FAQ页面

```markdown
# [Topic] FAQ

Answers to common questions about [topic].

*Last updated: [Date]*

## General Questions

### What is [thing]?
[Thing] is a [category] that [function]. It is used by [who] to [accomplish what].

### How does [thing] work?
[Thing] works by [process]. [Additional detail].

### Who uses [thing]?
[Thing] is used by [user types], including [specific examples like Company A, Company B].

## Comparison Questions

### How is [thing] different from [alternative]?
[Thing] differs from [alternative] in [specific ways]:
- [Difference 1]
- [Difference 2]
- [Difference 3]

### Is [thing] better than [alternative]?
[Thing] is better suited for [use cases] because [reasons]. 
[Alternative] may be better for [other use cases].

## Pricing & Access

### How much does [thing] cost?
[Pricing information or range]

### Is there a free trial?
[Trial information]

## Technical Questions

### What are the requirements for [thing]?
[Requirements list]

### How do I get started with [thing]?
1. [Step 1]
2. [Step 2]
3. [Step 3]
```

---

## 平台特定的优化策略

### Perplexity AI

**工作原理：** 三层重新排名系统
1. 从网络索引中初步检索内容
2. 根据相关性进行评分
3. 根据权威性和时效性选择要引用的内容

**优化策略：**
- 强大的领域权威性很重要 |
- 内容的时效性至关重要（更新日期）
- 直接回答用户问题 |
- 被其他权威来源引用 |
- 结构化的数据有助于搜索引擎解析内容

### ChatGPT / SearchGPT

**工作原理：** 基于Bing的搜索系统 + 大型语言模型（LLM）生成内容

**优化策略：**
- 在Bing中提交站点地图（sitemap） |
- 重视E-E-A-T（易读性、易懂性、准确性）信号 |
- 采用对话式的内容结构 |
- FAQ格式非常有效 |
- 使用明确的实体名称有助于识别内容

### Google AI Overviews

**工作原理：** 利用Google的索引 + Gemini技术生成内容

**优化策略：**
- 传统的SEO策略仍然有效（有助于排名） |
- 优化特色摘要的展示 |
- 实施FAQ、操作指南（HowTo）、产品相关的schema标记 |
- 提供清晰、权威的内容 |
- 优先考虑移动设备的索引体验

### Claude

**工作原理：** 使用训练数据 + 根据网络状态检索内容

**优化策略：**
- 训练数据的质量很重要 |
- 被维基百科提及有助于实体识别 |
- 重视内容的准确性 |
- 文章结构清晰、条理分明 |
- 被权威来源引用 |

---

## 技术实现

### GEO的Schema标记

**组织结构Schema：**
```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Company Name",
  "description": "Clear description of what company does",
  "url": "https://example.com",
  "foundingDate": "2017",
  "numberOfEmployees": "50-100",
  "sameAs": [
    "https://twitter.com/company",
    "https://linkedin.com/company/company"
  ]
}
```

**FAQ Schema：**
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "What is [thing]?",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "Direct answer here."
    }
  }]
}
```

**产品Schema：**
```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Product Name",
  "description": "Product description",
  "brand": {"@type": "Brand", "name": "Brand"},
  "offers": {
    "@type": "Offer",
    "priceCurrency": "USD",
    "price": "99"
  }
}
```

### llms.txt协议

在站点根目录下创建`/llms.txt`文件，以帮助大型语言模型（LLMs）理解您的网站结构：

```
# Site Name

> Brief description of what this site/company is.

## Main Sections

- [Products](/products): Description of products section
- [Documentation](/docs): Technical documentation
- [Blog](/blog): Industry insights and updates

## Key Facts

- Founded: 2017
- Customers: 500+ companies
- Key metric: [specific number]

## Contact

- Website: https://example.com
- Email: hello@example.com
```

---

## 监控GEO优化效果

### 手动测试

定期在各个平台上搜索以下关键词：

**Perplexity：**
- “[您的公司]是什么？”
- “最佳[竞争对手]替代方案”
- “[您的产品类别]的对比”
- “[您的产品]是如何工作的？”

**ChatGPT：**
- 启用网页浏览功能后使用相同关键词进行搜索 |
- “比较[您的产品]和[竞争对手]”

**Google（AI Overview）：**
- “[您的产品类别]解决方案”
- “[竞争对手]的替代方案”

### 监控工具

| 工具 | 监控内容 | 价格 |
|------|----------------|-------|
| Otterly.AI | 多平台AI内容可见性监控 | 免费 |
| Ahrefs Brand Radar | AI搜索提及监控 | 每月129美元以上 |
| Profound | 企业级基准测试工具 | 企业版 |
| 手动跟踪 | 自定义电子表格 | 免费 |

### 关键指标

- **提及率：** 相关查询中您被提及的百分比 |
- **引用率：** 被引用的内容中提到/链接到您的内容所占的比例 |
- **情感倾向：** 正面/中性/负面评价 |
- **声音份额：** 您的提及次数与竞争对手的对比 |
- **显示位置：** 在AI回答中的排名位置 |

---

## GEO内容编写原则

### 应该做的：
- ✅ 使用具体的数字（例如“0.5秒”而非“快速”）
- ✅ 使声明具体且可独立引用 |
- ✅ 使用清晰的层次结构组织内容 |
- ✅ 包含FAQ部分 |
- ✅ 定期更新内容并标注日期 |
- ✅ 创建对比内容 |
- ✅ 使用表格展示数据 |
- ✅ 保持内容的中立性和事实性 |
- ✅ 提及真实的客户和结果

### 不应该做的：
- ❌ 使用模糊的形容词（如“最佳”、“领先”、“顶级”）
- ❌ 堆砌关键词（LLMs能识破这种技巧） |
- ❌ 写长篇无结构的文本 |
- ❌ 隐藏重要信息（应提供全面的信息） |
- ❌ 使用过时的统计数据 |
- ❌ 忽视竞争对手（应直接与他们竞争） |
- ❌ 明显带有宣传性质的内容（中立的内容更受欢迎）

---

## 快速启动检查清单

对于任何想要进行GEO优化的页面：
1. [ ] 在第一段中添加明确的实体定义 |
2. [ ] 包含5个以上具体的、可引用的统计数据 |
3. [ ] 添加包含5个以上问题的FAQ部分 |
4. [ ] 如果适用，创建对比表格 |
5. [ ] 添加“最后更新”日期 |
6. [ ] 实施FAQ的schema标记 |
7. [ ] 确保标题层次结构为H1→H2→H3 |
8. [ ] 在Perplexity平台上测试：您的内容是否被展示？

---

## 自动化GEO监控

使用提供的监控脚本跟踪您的引用率变化！

### 快速启动

**测试当前可见性：**
```bash
python3 scripts/geo-monitor.py --test
```

**单次查询测试：**
```bash
python3 scripts/geo-monitor.py --query "best game server orchestration platform"
```

**生成每日报告：**
```bash
python3 scripts/geo-daily-report.py
```

### 设置自动化监控

**1. 创建测试查询文件**（`scripts/geo-test-queries.json`）：
```json
{
  "queries": [
    {
      "query": "your target query here",
      "category": "brand|product|comparison|problem|competitor"
    }
  ]
}
```

**2. 运行每日监控：**
```bash
# Add to cron for daily 9am checks
0 9 * * * cd /path/to/skill && bash scripts/geo-daily-monitor.sh
```

### 解读报告

**引用率：** 在AI回答中您被提及的查询百分比：
- 0-20%：初期阶段，需要改进 |
- 20-40%：逐渐提升可见性 |
- 40-60%：表现良好 |
- 60%以上：具有主导地位

**监控的类别包括：**
- 品牌相关查询（这些应该是您的重点） |
- 产品/功能相关查询 |
- 对比相关查询 |
- 问题/痛点相关查询 |
- 竞争对手对比相关查询

### 监控最佳实践

1. **首先针对15-20个关键查询进行测试** |
- **在优化期间每天进行测试**（前两周） |
- **达到目标引用率后每周检查一次** |
- **内容更新后跟踪变化**（预计有3-7天的延迟） |
- **关注薄弱环节**——未被引用的查询是优化机会

### 需要跟踪的数据

**当前状态：**
- 总引用率 |
- 按类别划分的引用情况 |
- 被引用的位置（第1位、第2位等） |
- 显著的差距（0%的引用率）

**长期跟踪：**
- 引用率趋势（每周/每月） |
- 新增的引用次数 |
- 引用减少的情况（可能是内容过时的原因） |
- 各类别的优化情况

### 包含的文件

- `scripts/geo-monitor.py` - 主要测试脚本（使用Perplexity API） |
- `scripts/geo-daily-report.py` - 格式化的报告生成工具 |
- `scripts/geo-daily-monitor.sh` - 适合Cron任务的脚本 |
- `scripts/geo-test-queries.json` - 示例查询文件

**所需资源：** Perplexity API密钥（通过Clawdbot的web_search功能配置）

---

## 参考资源

- [Awesome GEO GitHub](https://github.com/amplifying-ai/awesome-generative-engine-optimization) |
- [普林斯顿大学关于GEO的研究论文](https://arxiv.org/pdf/2311.09735) |
- [Google AI搜索优化指南](https://developers.google.com/search/blog/2025/05/succeeding-in-ai-search) |
- [Perplexity的排名因素](https://firstpagesage.com/seo-blog/perplexity-ai-optimization-ranking-factors-and-strategy/)