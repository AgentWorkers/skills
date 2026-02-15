---
name: case-study-writing
description: |
  B2B case study writing with STAR framework, data visualization, and research.
  Covers structure, customer quotes, metrics presentation, and distribution formats.
  Use for: customer success stories, portfolio pieces, sales enablement, marketing content.
  Triggers: case study, customer story, success story, b2b case study, client testimonial,
  customer case study, portfolio case study, use case, customer win, results story
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

## STAR 框架

每个案例研究都遵循以下结构：**背景情况 -> 面临的挑战 -> 采取的措施 -> 最终结果**

| 部分 | 字数 | 内容 | 目的 |
|---------|--------|---------|---------|
| **背景情况** | 100-150 字 | 客户是谁，他们的背景信息 | 设定场景 |
| **面临的挑战** | 100-150 字 | 他们具体面临的问题 | 建立共鸣 |
| **采取的措施** | 200-300 字 | 实施了哪些解决方案，以及实施方式 | 展示你的产品 |
| **最终结果** | 100-200 字 | 可量化的成果（实施前后的变化） | 证明产品的价值 |

**总字数：800-1200 字。** 字数过长会失去读者的兴趣；过短则缺乏可信度。**

## 结构模板

### 1. 标题（以结果开头）

```
❌ "How Company X Uses Our Product"
❌ "Company X Case Study"

✅ "How Company X Reduced Onboarding Time by 60% with [Product]"
✅ "Company X Grew Revenue 340% in 6 Months Using [Product]"
```

标题应当具体、量化，并明确说明最终结果。

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
- 公司的简要背景

### 4. 面临的挑战

- **量化问题**：例如“每周花费 40 小时进行手动数据录入”，而不是简单地说“存在数据问题”
- **说明后果**：如果问题得不到解决会带来什么后果（例如收入损失、客户流失、错过截止日期）
- 包含客户关于问题的反馈或抱怨

### 5. 采取的措施/解决方案

- 实施了哪些解决方案（你的产品/服务）
- 时间线：例如“在两周内部署”或“分三个月逐步推广”
- 选择你的产品而非其他解决方案的原因（简要说明）
- 2-3 个具体解决了问题的功能

### 6. 最终结果

- **量化指标**：务必使用具体数据
- **时间范围**：例如“在三个月内”或“第一季度”
- 超出最初目标的意外收获
- 客户对结果的反馈

## 重要的指标

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
| **满意度** | 客户净推荐值（NPS）变化、客户保留率、支持工单数量减少 |

### 数据可视化

```bash
# Generate a before/after comparison chart
infsh app run infsh/python-executor --input '{
  "code": "import matplotlib.pyplot as plt\nimport matplotlib\nmatplotlib.use(\"Agg\")\n\ncategories = [\"Processing Time\", \"Error Rate\", \"Cost per Order\"]\nbefore = [4, 12, 8.50]\nafter = [0.75, 1.5, 2.10]\n\nfig, ax = plt.subplots(figsize=(10, 6))\nx = range(len(categories))\nwidth = 0.35\nax.bar([i - width/2 for i in x], before, width, label=\"Before\", color=\"#ef4444\")\nax.bar([i + width/2 for i in x], after, width, label=\"After\", color=\"#22c55e\")\nax.set_ylabel(\"Value\")\nax.set_xticks(x)\nax.set_xticklabels(categories)\nax.legend()\nax.set_title(\"Impact of Implementation\")\nplt.tight_layout()\nplt.savefig(\"results-chart.png\", dpi=150)\nprint(\"Chart saved\")"
}'
```

## 客户反馈

### 什么是好的客户反馈

```
❌ "We love the product." (vague, could be about anything)
❌ "It's great." (meaningless)

✅ "We went from processing 50 orders a day to 200, without adding a single person to the team."
   — Sarah Chen, VP Operations, Acme Corp

✅ "Before [Product], our team dreaded Monday mornings because of the report backlog.
    Now it's automated and they can focus on actual analysis."
   — Marcus Rodriguez, Head of Analytics, DataCo
```

### 反馈的放置位置

- 在“面临的挑战”部分放置 1 条客户反馈，内容关于问题或困扰
- 在“最终结果”部分放置 1-2 条客户反馈，内容关于成果或变化
- 必须注明：客户的全名、职位、公司名称

### 反馈的格式

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

| 格式 | 分发渠道 | 备注 |
|--------|-------|-------|
| **网页** | /customers/ 或 /case-studies/ | 完整版本，优化过搜索引擎排名（SEO） |
| **PDF** | 销售团队使用，可作为电子邮件附件 | 可下载，需授权 |
| **幻灯片** | 销售电话、演示文稿 | 5-8 张幻灯片，以视觉内容为主 |
| **一页纸报告** | 展览会、快速参考资料 | 包含摘要、关键指标和客户反馈 |
| **社交媒体帖子** | LinkedIn、Twitter | 包含关键数据、客户反馈和完整报告链接 |
| **视频** | 网站、YouTube | 客户访谈或动画视频 |

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

- 标题以量化结果开头
- 摘要框中包含公司名称、行业信息、面临的挑战和最终结果
- 面临的挑战需要具体量化，不能含糊不清
- 包含 2-3 条带有来源的客户反馈
- 提供带有时间范围的量化指标
- 总字数控制在 800-1200 字之间
- 便于阅读（使用标题、加粗字体、项目符号）
- 客户已审核最终版本
- 必须包含可视化内容（至少一张图表或前后对比图）

## 常见错误

| 错误 | 问题 | 解决方法 |
|---------|---------|-----|
| 没有具体数据 | 读起来像营销宣传 | 所有内容都应量化 |
| 内容全部围绕产品展开 | 读起来像销售演讲 | 案例研究的核心应该是客户的需求和解决方案 |
| 使用泛泛的反馈 | 缺乏可信度 | 使用具体且带有来源的客户反馈 |
| 忽略“实施前”的情况 | 无法体现改进效果 | 必须展示问题的起始状态 |
| 文字过长 | 会失去读者的注意力 | 总字数控制在 800-1200 字 |
| 未获得客户批准 | 存在法律或关系风险 | 必须获得客户的最终确认 |

## 相关技能

```bash
npx skills add inferencesh/skills@web-search
npx skills add inferencesh/skills@prompt-engineering
```

查看所有可用工具：`infsh app list`