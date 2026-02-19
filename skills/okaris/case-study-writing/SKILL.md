---
name: case-study-writing
description: "**B2B案例研究撰写指南（基于STAR框架）**  
本指南涵盖了使用STAR框架进行B2B案例研究的整个流程，包括数据可视化、研究方法以及案例报告的编写与呈现方式。内容涉及案例研究的结构、客户引言、关键指标的展示方式以及报告的发布格式。适用于以下场景：客户成功案例分享、项目作品集展示、销售支持材料、市场营销内容等。  
**适用场景：**  
- 客户成功案例  
- 项目作品集  
- 销售支持材料  
- 市场营销内容  
**核心概念：**  
- **STAR框架**：一种结构化的案例研究编写方法，包括**Story（故事）、Action（行动）、Result（结果）和Impact（影响）**四个部分。  
- **数据可视化**：通过图表和图形直观展示研究数据和分析结果。  
- **研究方法**：系统收集和分析客户数据，以支持案例研究的深度和可信度。  
**主要内容：**  
1. **案例研究结构**：  
   - 引言部分：介绍案例背景、目标和研究目的。  
   - 方法部分：描述研究方法、数据收集和分析过程。  
   - 结果部分：展示关键指标和数据分析结果。  
   - 影响部分：分析案例对客户和业务的影响。  
   - 结论部分：总结案例的价值和启示。  
2. **客户引言**：  
   - 介绍目标客户的基本信息（公司背景、业务规模等）。  
   - 描述与该公司合作的背景和原因。  
3. **指标展示**：  
   - 选择关键业务指标（如销售额、客户满意度等）进行展示。  
   - 使用图表和图形辅助解释数据变化趋势。  
4. **报告格式**：  
   - 采用清晰、易读的格式（如Markdown、PDF等）编写报告。  
   - 确保报告结构一致，便于阅读和理解。  
5. **应用场景**：  
   - 客户成功案例：分享公司与客户合作取得的显著成果。  
   - 项目作品集：展示公司的典型案例和解决方案。  
   - 销售支持材料：帮助销售人员了解产品或服务的实际应用效果。  
   - 市场营销内容：吸引潜在客户，提升品牌知名度。  
**使用建议：**  
- 根据实际需求调整报告内容和格式。  
- 定期更新案例研究，以反映最新业务进展。  
- 利用案例研究提升品牌影响力和客户信任度。"
allowed-tools: Bash(infsh *)
---
# 案例研究撰写

通过 [inference.sh](https://inference.sh) 命令行工具，利用调研数据和可视化元素来撰写引人入胜的 B2B 案例研究。

## 快速入门

```bash
curl -fsSL https://cli.inference.sh | sh && infsh login

# Research the customer's industry
infsh app run tavily/search-assistant --input '{
  "query": "SaaS customer onboarding challenges 2024 statistics"
}'
```

> **安装说明：** [安装脚本](https://cli.inference.sh) 仅会检测您的操作系统和架构，然后从 `dist.inference.sh` 下载相应的二进制文件，并验证其 SHA-256 校验和。无需提升权限或启动后台进程。如需手动安装和验证，请参考 [此处](https://dist.inference.sh/cli/checksums.txt)。

## STAR 框架

每份案例研究都遵循以下结构：**背景情况 -> 面临的挑战 -> 采取的措施 -> 最终结果**

| 部分 | 字数 | 内容 | 目的 |
|---------|--------|---------|---------|
| **背景情况** | 100-150 字 | 客户是谁及其所处的行业环境 | 为故事设定背景 |
| **面临的挑战** | 100-150 字 | 客户具体面临的问题 | 增强读者的共鸣 |
| **采取的措施** | 200-300 字 | 实施了哪些解决方案以及实施方式 | 展示您的产品 |
| **最终结果** | 100-200 字 | 可量化的成果（实施前后的变化） | 证明产品的价值 |

**总字数：800-1200 字。** 字数过多会降低读者的阅读兴趣；字数过少则缺乏可信度。**

## 结构模板

### 1. 标题（以结果开头）

```
❌ "How Company X Uses Our Product"
❌ "Company X Case Study"

✅ "How Company X Reduced Onboarding Time by 60% with [Product]"
✅ "Company X Grew Revenue 340% in 6 Months Using [Product]"
```

标题应具体明确，并陈述最终成果。

### 2. 摘要框

放在页面顶部，便于读者快速了解内容：

```
┌─────────────────────────────────────┐
│ Company: Acme Corp                  │
│ Industry: E-commerce                │
│ Size: 200 employees                 │
│ Challenge: Manual order processing  │
│ Result: 60% faster fulfillment      │
│ Product: [Your Product]             │
└─────────────────────────────────────┘
```

### 3. 背景情况

- 客户是谁（所属行业、规模、地理位置）
- 问题出现之前的相关背景信息
- 公司的基本情况（1-2 句）

### 4. 面临的挑战

- **量化问题**：例如“每周花费 40 小时进行手动数据录入”，而非简单地描述“存在数据问题”
- **说明后果**：如果不解决这个问题会带来什么后果（例如收入损失、客户流失、错过截止日期）
- 包含客户对现状的反馈或不满言论

### 5. 采取的措施/解决方案

- 实施了哪些解决方案（您的产品/服务）
- 时间线：例如“在 2 周内部署”或“分 3 个月逐步推广”
- 选择您的产品而非其他方案的关键原因
- 2-3 个能够解决该挑战的具体功能

### 6. 最终结果

- **量化成果**：务必使用具体数据
- **时间范围**：例如“在 3 个月内”或“第一季度内”
- 超出最初目标的意外收获
- 客户对结果的反馈

## 重要的评估指标

### 如何呈现数据

```
❌ "Improved efficiency"
❌ "Saved time"
❌ "Better results"

✅ "Reduced processing time from 4 hours to 45 minutes (81% decrease)"
✅ "Increased conversion rate from 2.1% to 5.8% (176% improvement)"
✅ "Saved $240,000 annually in operational costs"
```

### 指标类别

| 类别 | 示例 |
|----------|---------|
| **时间** | 节省的时间、完成时间、部署速度 |
| **财务** | 收入增长、成本降低、投资回报率（ROI） |
| **效率** | 处理量、错误率、自动化程度 |
| **增长** | 新用户数量、市场扩张、功能采用率 |
| **满意度** | 客户净推荐值（NPS）变化、客户留存率、支持工单数量减少 |

### 数据可视化

```bash
# Generate a before/after comparison chart
infsh app run infsh/python-executor --input '{
  "code": "import matplotlib.pyplot as plt\nimport matplotlib\nmatplotlib.use(\"Agg\")\n\ncategories = [\"Processing Time\", \"Error Rate\", \"Cost per Order\"]\nbefore = [4, 12, 8.50]\nafter = [0.75, 1.5, 2.10]\n\nfig, ax = plt.subplots(figsize=(10, 6))\nx = range(len(categories))\nwidth = 0.35\nax.bar([i - width/2 for i in x], before, width, label=\"Before\", color=\"#ef4444\")\nax.bar([i + width/2 for i in x], after, width, label=\"After\", color=\"#22c55e\")\nax.set_ylabel(\"Value\")\nax.set_xticks(x)\nax.set_xticklabels(categories)\nax.legend()\nax.set_title(\"Impact of Implementation\")\nplt.tight_layout()\nplt.savefig(\"results-chart.png\", dpi=150)\nprint(\"Chart saved\")"
}'
```

## 客户评价

### 什么是好的客户评价

```
❌ "We love the product." (vague, could be about anything)
❌ "It's great." (meaningless)

✅ "We went from processing 50 orders a day to 200, without adding a single person to the team."
   — Sarah Chen, VP Operations, Acme Corp

✅ "Before [Product], our team dreaded Monday mornings because of the report backlog.
    Now it's automated and they can focus on actual analysis."
   — Marcus Rodriguez, Head of Analytics, DataCo
```

### 评价的放置位置

- **在“面临的挑战”部分放置 1 条评价**——描述客户的不满或困扰
- **在“最终结果”部分放置 1-2 条评价**——描述改进后的效果或变化
- 必须注明评价者的全名、职位和公司名称

### 评价的格式

```markdown
> "We went from processing 50 orders a day to 200, without adding anyone to the team."
>
> — Sarah Chen, VP Operations, Acme Corp
```

## 研究支持

### 如何收集行业背景信息

```bash
# Industry benchmarks
infsh app run tavily/search-assistant --input '{
  "query": "average e-commerce order processing time industry benchmark 2024"
}'

# Competitor landscape
infsh app run exa/search --input '{
  "query": "order management automation solutions market overview"
}'

# Supporting statistics
infsh app run exa/answer --input '{
  "question": "What percentage of e-commerce businesses still use manual order processing?"
}'
```

## 分发格式

| 格式 | 分发渠道 | 说明 |
|--------|-------|-------|
| **网页** | /customers/ 或 /case-studies/ | 提供完整版本，适合搜索引擎优化（SEO） |
| **PDF** | 发送给销售团队或通过电子邮件附件 | 可下载，需经过客户授权 |
| **幻灯片** | 用于销售电话或演示文稿 | 5-8 张幻灯片，以视觉内容为主 |
| **一页纸报告** | 用于贸易展会或快速参考 | 包含摘要、关键数据和客户评价 |
| **社交媒体帖子** | LinkedIn、Twitter | 包含关键数据、客户评价和完整报告链接 |
| **视频** | 网站或 YouTube | 包含客户采访或动画内容 |

### 社交媒体发布要点

```
Headline stat + brief context + customer quote + CTA

Example:
"60% faster order processing.

Acme Corp was drowning in manual fulfillment. 4 hours per batch. 12% error rate.

After implementing [Product]: 45 minutes per batch. 1.5% errors.

'We went from 50 orders a day to 200 without adding headcount.' — Sarah Chen, VP Ops

Read the full story → [link]"
```

## 撰写检查清单

- [ ] 标题中要明确陈述量化结果
- [ ] 摘要框中包含公司名称、行业背景、面临的挑战和最终结果
- [ ] 面临的挑战需要具体量化，避免模糊描述
- [ ] 包含 2-3 条带有来源信息的客户评价
- [ ] 提供带有时间范围的量化数据
- [ ] 总字数控制在 800-1200 字之间
- [ ] 文章结构清晰（使用标题、粗体字和项目符号）
- [ ] 最终版本需获得客户批准
- [ ] 必须包含可视化内容（至少一张图表或实施前后的对比图）

## 常见错误

| 错误 | 问题 | 修正方法 |
|---------|---------|-----|
| 没有具体数据 | 读起来像普通的营销内容 | 所有内容都应量化 |
| 仅介绍产品特点 | 读起来像销售宣传 | 故事的核心应该是客户的需求和体验 |
| 使用泛化的评价 | 缺乏可信度 | 使用具体且带有来源的评价 |
- 忘记提供“实施前”的数据 | 无法体现改进效果 | 必须提供初始数据作为对比 |
- 文章过长 | 会分散读者注意力 | 最佳字数控制在 800-1200 字 |
- 未获得客户批准 | 存在法律或关系风险 | 必须获得客户的正式认可 |

## 相关技能

```bash
npx skills add inference-sh/skills@web-search
npx skills add inference-sh/skills@prompt-engineering
```

可以查看所有可用工具：`infsh app list`